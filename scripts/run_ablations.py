import argparse
import asyncio
import json
import logging
import random
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set, Optional
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from src.load.dataset_loader import DatasetLoader
from src.inference.inference_engine import InferenceEngine
from src.parsing.parser import Parser
from src.normalization.normalizer import Normalizer
from src.metrics.metrics_calculator import MetricsCalculator
from src.plots.visualization_generator import VisualizationGenerator
from src.utils.config_loader import load_and_validate_config, parse_command_line_args
from src.utils.logging_config import setup_logging
from src.utils.exceptions import APIError, ConfigurationError, ParsingError
# Reuse the main run's prompt resolution + formatting so the ablation's BASELINE
# elicitation is byte-identical to the study's (PROMPT_LITERATURE_VERIFICATION_2026-07-09.md §1).
from scripts.run_experiment import (
    create_prompt_map,
    format_explain_prompt,
    format_prompt,
    pre_clean_text,
    quote_labels,
)

logger = logging.getLogger(__name__)

STRATEGY_IDS = ["H", "R", "CF", "RO"]

# The ONE pre-registered robustness ablation (FIX_PLAN §P3.3): prompt paraphrase.
# Each strategy's elicitation is re-worded (*_alt.txt) and the ECS delta vs the
# baseline wording is measured. The former normalization and highlighting-k
# ablations were cut: normalization is pinned by the v3.0 shared-token-space
# requirement (varying it re-introduces the review §8.2 asymmetry by construction),
# and dynamic_k superseded fixed-k highlighting.
#
# PARAPHRASE VARIANTS (2026-07-20). The original single paraphrase per strategy made
# every reliability ceiling a point estimate that conflates instrument stability with
# the disruptiveness of that one rewording — and because a low reliability INFLATES the
# disattenuated ratio, the "extraction<->CF at ceiling" reading was the claim most
# exposed to it. `--paraphrase alt2|alt3` collects additional independent rewordings so
# each ceiling becomes a distribution. The variants are semantically equivalent and keep
# every format slot and JSON schema identical; only surface wording differs.
ALT_PROMPT_SETS = {
    "alt": {
        "H": "prompts/highlighting_alt.txt",
        "R": "prompts/rationale_alt.txt",
        "CF": "prompts/counterfactual_alt.txt",
        "RO": "prompts/rank_ordering_alt.txt",
    },
    "alt2": {
        "H": "prompts/highlighting_alt2.txt",
        "R": "prompts/rationale_alt2.txt",
        "CF": "prompts/counterfactual_alt2.txt",
        "RO": "prompts/rank_ordering_alt2.txt",
    },
    "alt3": {
        "H": "prompts/highlighting_alt3.txt",
        "R": "prompts/rationale_alt3.txt",
        "CF": "prompts/counterfactual_alt3.txt",
        "RO": "prompts/rank_ordering_alt3.txt",
    },
}
# Back-compat alias: existing call sites read ALT_PROMPTS for the original paraphrase.
ALT_PROMPTS = ALT_PROMPT_SETS["alt"]


def resolve_paraphrase(name: Optional[str]) -> str:
    """Resolve a --paraphrase variant name against ALT_PROMPT_SETS. None keeps the
    historical default ('alt'); an unknown name is a hard error listing valid names,
    mirroring resolve_model/resolve_datasets — a silent fallback would produce a
    ceilings file whose _meta claims a variant it did not actually run."""
    if name is None:
        return "alt"
    if name in ALT_PROMPT_SETS:
        return name
    valid = ", ".join(sorted(ALT_PROMPT_SETS))
    raise ConfigurationError(f"Unknown --paraphrase '{name}'; valid variants: {valid}")


def resolve_datasets(config, names: Optional[list]):
    """Resolve a --datasets NAME list against config.datasets. None keeps the
    historical default (every configured dataset); any unknown name is a hard error
    listing the valid names — never a silent skip, because a misspelled dataset would
    otherwise silently produce a ceilings file missing a study cell (the exact gap
    this flag exists to close: collecting cad_imdb ceilings for models whose original
    ablation pass predates the CAD-IMDb arm)."""
    if names is None:
        return list(config.datasets)
    by_name = {d.name: d for d in config.datasets}
    unknown = [n for n in names if n not in by_name]
    if unknown:
        valid = ", ".join(d.name for d in config.datasets)
        raise ConfigurationError(
            f"Unknown --datasets {unknown}; valid dataset names: {valid}")
    return [by_name[n] for n in names]


def resolve_model(config, name: Optional[str]):
    """Resolve a --model NAME (the config model name, e.g. 'qwen3-235b') against
    config.models. None keeps the historical default (config.models[0]); an unknown
    name is a hard error listing the valid names — never a silent fallback, because
    the resolved model is stamped into _meta and drives the per-model reliability
    ceilings (STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md §1.1)."""
    if name is None:
        return config.models[0]
    for m in config.models:
        if m.name == name:
            return m
    valid = ", ".join(m.name for m in config.models)
    raise ConfigurationError(f"Unknown --model '{name}'; valid model names: {valid}")


def load_prompt(filepath: str) -> str:
    path = Path(filepath)
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


# Structural markers excluded from the instance vocabulary — mirrors the vocab block
# in scripts/run_experiment.py (they are prompt scaffolding, not content the
# strategies can select).
STRUCTURAL_LABELS = {"premise:", "hypothesis:", "sentence1:", "sentence2:", "text:", "label:"}


def compute_self_consistency_aj(base_set: Set[str], alt_set: Set[str], text: str,
                                normalizer: Normalizer, calc: MetricsCalculator,
                                eps: float = 0.10) -> Tuple[Optional[float], bool]:
    """Same-strategy paraphrase self-consistency on the AJ scale (ML review R1,
    2026-07-08): AJ between the SAME strategy's evidence under the baseline wording
    and under the paraphrased (*_alt.txt) wording, chance- and ceiling-corrected over
    the instance's own content vocabulary.

    This is the SELF-CONSISTENCY CEILING for ECS-adj: cross-strategy ECS-adj is only
    interpretable relative to how much a single strategy agrees with itself under a
    trivial re-elicitation. If cross-strategy ECS-adj ~= this ceiling, the paradigms
    do not meaningfully disagree beyond elicitation noise; if it sits well below,
    the cross-paradigm divergence is real. Zero extra API cost — both sets are
    already collected by the prompt-paraphrase ablation.

    Vocab = normalized content lemmas of the input (structural labels excluded)
    unioned with both evidence sets (support closure, mirroring run_experiment P1.1).
    Returns (aj, degenerate) exactly like MetricsCalculator.adjusted_jaccard;
    (None, False) when either set is empty (missing, not degenerate).
    """
    if not base_set or not alt_set:
        return None, False
    from scripts.run_experiment import pre_clean_text
    vocab_tokens = set()
    for t in normalizer.normalize_input_text(pre_clean_text(text)).split():
        if t in STRUCTURAL_LABELS:
            continue
        norm = normalizer.normalize(t)
        if norm:
            vocab_tokens.add(norm)
    vocab_tokens |= base_set | alt_set
    return calc.adjusted_jaccard(base_set, alt_set, len(vocab_tokens), eps)


def build_baseline_explain_prompt(strategy_id: str, prompts: Dict[str, str],
                                  predicted_label: str, clean_text: str,
                                  label_set: List[str]) -> str:
    """Format a strategy's BASELINE explain prompt byte-identically to the main run
    (run_experiment.process_instance): CF selects the multiclass variant when the label
    set has >2 classes and receives the other_labels / other_labels_quoted target slots;
    every other strategy gets predicted_label + input_text.

    The prior implementation passed the RAW, UNFORMATTED template — the model literally
    received `{predicted_label}` / `{input_text}` braces, so every self-consistency
    ceiling and prompt-ablation delta compared an unformatted baseline against a
    formatted paraphrase (PROMPT_LITERATURE_VERIFICATION_2026-07-09.md §1)."""
    if strategy_id == "CF":
        cf_prompt_key = "CF_explain"
        if len(label_set) > 2 and "CF_explain_multiclass" in prompts:
            cf_prompt_key = "CF_explain_multiclass"
        cf_targets = [l for l in label_set if l != predicted_label]
        return format_explain_prompt(
            prompts[cf_prompt_key], predicted_label, input_text=clean_text,
            other_labels=", ".join(cf_targets),
            other_labels_quoted=quote_labels(cf_targets),
        )
    return format_explain_prompt(prompts[f"{strategy_id}_explain"], predicted_label,
                                 input_text=clean_text)


def format_alt_prompt(template: str, predicted_label: str, input_text: str,
                      label_set: List[str]) -> str:
    """Format a paraphrase (*_alt.txt) prompt. Supplies the CF target slots
    (other_labels / other_labels_quoted) so the CF alt pins the same target(s) as its
    base; str.format ignores the extras for the H/R/RO alts, which reference only
    predicted_label + input_text (no alt references {label_set} any more)."""
    cf_targets = [l for l in label_set if l != predicted_label]
    return template.format(
        predicted_label=predicted_label,
        input_text=input_text,
        other_labels=", ".join(cf_targets),
        other_labels_quoted=quote_labels(cf_targets),
    )


def parse_raw_tokens(strategy_id: str, raw: str, text: str,
                     predicted_label: str, label_set: List[str],
                     parser: Parser, normalizer: Normalizer) -> List[str]:
    """Parse raw response and return raw token strings (pre-normalization)."""
    if not raw:
        return []
    try:
        if strategy_id == "H":
            return parser.parse_highlighting(raw, text, normalizer, skip_validation=True)
        elif strategy_id == "R":
            # skip_validation=False so the rationale's content-word evidence is actually
            # extracted and anchored (P0.2): with skip_validation=True parse_rationale
            # returns an EMPTY evidence list, so R never entered the ablation ECS and
            # every R-alt delta was structurally 0.
            _, evidence = parser.parse_rationale(raw, text, normalizer, skip_validation=False)
            return evidence
        elif strategy_id == "CF":
            cf_text, _pred, _from = parser.parse_counterfactual(raw, text, predicted_label, label_set,
                                                                normalizer, skip_validation=True)
            orig_words = set(text.lower().split())
            cf_words = set(cf_text.lower().split())
            return list((orig_words - cf_words) | (cf_words - orig_words))
        elif strategy_id == "RO":
            ranked = parser.parse_rank_ordering(raw, text, normalizer, skip_validation=True)
            return [t for t, _ in ranked]
    except (ParsingError, json.JSONDecodeError) as e:
        logger.debug(f"Parse failed for {strategy_id}: {e}")
        return []


def normalize_token_list(raw_tokens: List[str], normalizer: Normalizer) -> Set[str]:
    return normalizer.normalize_tokens(raw_tokens)


def compute_ecs_from_token_sets(sets: Dict[str, Set[str]], calc: MetricsCalculator) -> Optional[float]:
    explanations = {s: sets.get(s, set()) for s in STRATEGY_IDS}
    agreements = calc.compute_pairwise_agreements(explanations)
    return calc.compute_ecs(agreements)


def compute_ecs_adj_from_token_sets(sets: Dict[str, Set[str]], text: str,
                                    normalizer: Normalizer, calc: MetricsCalculator) -> Optional[float]:
    """ECS-adj (available-component) over the instance's own vocabulary — audit F10
    (RESEARCH_AUDIT_2026-07-10): the paraphrase deltas were reported only on the
    legacy raw-Jaccard ECS while the ceilings in the same report are AJ; this puts
    the deltas on the primary metric's scale too. Vocab mirrors
    compute_self_consistency_aj: normalized input lemmas (structural labels
    excluded) unioned with every evidence set (support closure)."""
    explanations = {s: sets.get(s, set()) for s in STRATEGY_IDS}
    vocab_tokens = set()
    for t in normalizer.normalize_input_text(pre_clean_text(text)).split():
        if t in STRUCTURAL_LABELS:
            continue
        norm = normalizer.normalize(t)
        if norm:
            vocab_tokens.add(norm)
    for ev in explanations.values():
        vocab_tokens |= ev
    if not vocab_tokens:
        return None
    return calc.compute_ecs_adjusted(explanations, len(vocab_tokens)).get("ecs_adj")


async def run_classify(engine, class_prompt, parser, label_set):
    result = await engine.classify(class_prompt)
    predicted_label = parser.parse_classification(result.raw_response, label_set)
    return predicted_label, result.raw_response


def strategy_max_tokens(strategy_id: str, input_text: str, base: int = 512) -> int:
    """Per-strategy output budget mirroring the live run (P0.2): H scores EVERY word,
    so on long inputs a flat budget truncates its salience list. Give H a
    length-proportional budget; other strategies keep the flat base."""
    if strategy_id == "H":
        n_words = len(input_text.split())
        return max(base * 2, 12 * n_words + 200)
    return base


async def run_explain(engine, class_prompt, class_raw, explain_prompt, max_tokens=512) -> str:
    messages = [
        {"role": "user", "content": class_prompt},
        {"role": "assistant", "content": class_raw},
        {"role": "user", "content": explain_prompt},
    ]
    return await engine.chat(messages, max_tokens=max_tokens)


async def run_ablations(config, args, model_cfg=None, dataset_cfgs=None, paraphrase="alt"):
    # model_cfg: the resolved ModelConfig to ablate (--model override); default keeps
    # the historical single-model behavior (config.models[0]).
    # dataset_cfgs: the resolved dataset subset (--datasets override); default keeps
    # the historical behavior (all configured datasets).
    # paraphrase: which reworded prompt set to elicit (--paraphrase override); default
    # 'alt' keeps the original single-paraphrase behavior byte-for-byte.
    if model_cfg is None:
        model_cfg = config.models[0]
    if dataset_cfgs is None:
        dataset_cfgs = list(config.datasets)
    alt_prompt_map = ALT_PROMPT_SETS[paraphrase]
    # Scope the run directory by model AND paraphrase variant, not by timestamp alone.
    # Ablation passes are routinely launched one-per-model in parallel; the second-
    # resolution timestamp collides when they start in the same second, and every
    # process then writes ablation_results.json to the SAME path — last writer wins and
    # the other models' ceilings are silently lost (observed 2026-07-20: three parallel
    # alt2 passes, only one survived). The suffix makes the path a function of the run's
    # identity, so a collision is impossible and provenance is readable from the path.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = f"{timestamp}_{model_cfg.name}_{paraphrase}"
    output_dir = Path(config.output.base_dir) / run_dir / "ablations"
    if output_dir.exists() and any(output_dir.iterdir()):
        raise RuntimeError(
            f"{output_dir} already exists and is non-empty — refusing to overwrite "
            f"collected ceilings. Move it aside or wait a second and retry.")
    output_dir.mkdir(parents=True, exist_ok=True)

    setup_logging(log_dir=output_dir / "logs", console_level=config.output.log_level)
    logger.info(f"Starting ablation studies (model: {model_cfg.name} = {model_cfg.model_id}, "
                f"paraphrase: {paraphrase})...")

    loader = DatasetLoader(seed=config.experiment.seed)
    parser = Parser()
    calc = MetricsCalculator()
    engine = InferenceEngine(
        model_name=model_cfg.model_id,
        max_retries=config.inference.max_retries,
        concurrent_requests=config.inference.concurrent_requests,
    )

    all_results = {}
    all_plot_data = []

    for dataset_config in dataset_cfgs:
        subset_n = min(dataset_config.sample_size, config.ablations.subset_size)
        # Prefer the frozen curated set, sliced with the SAME seeded shuffle as the main
        # run (P0.2), so the ablation runs on a subset of the very instances the study
        # analyses — not a fresh, incomparable live HuggingFace draw.
        curated_path = Path("data/processed") / f"{dataset_config.name}_curated.jsonl"
        if curated_path.exists():
            instances = loader.load_curated(str(curated_path))
            rng_slice = random.Random(config.experiment.seed)
            rng_slice.shuffle(instances)
            instances = instances[:subset_n]
            logger.info(f"Loaded {len(instances)} CURATED instances for {dataset_config.name} "
                        f"ablation from {curated_path}")
        else:
            dataset = loader.load_dataset(dataset_config.huggingface_id, dataset_config.split)
            instances = loader.sample_balanced(
                dataset=dataset,
                n_samples=subset_n,
                label_field=getattr(dataset_config, "label_field", "label"),
                text_field=getattr(dataset_config, "text_field", "text"),
                secondary_text_field=getattr(dataset_config, "secondary_text_field", None),
                dataset_name=dataset_config.name,
                split=dataset_config.split,
                label_names=dataset_config.labels if hasattr(dataset_config, "labels") else None,
            )
            logger.info(f"Loaded {len(instances)} sampled instances for {dataset_config.name} ablation")

        # Resolve prompts through the SAME path as the live run (dataset-specific and
        # multiclass variants, CF-free, classification) so the baseline elicitation the
        # ablation sends is byte-identical to the study's.
        prompts, _prompt_sources = create_prompt_map(config, dataset_config.name)
        label_set = dataset_config.labels

        # --- Step 1: Compute baseline for all instances ---
        # baseline_data[i] = {predicted_label, class_raw, class_prompt, clean_text,
        #                     raw_tokens: {s: [str]}, baseline_ecs}
        baseline_data = []
        for instance in instances:
            # Mirror the live run: pre-clean HTML/markup before prompting, and format the
            # classification prompt with the cleaned text (run_experiment.process_instance).
            clean_text = pre_clean_text(instance.text)
            class_prompt = format_prompt(prompts["classification"], clean_text, label_set)

            try:
                predicted_label, class_raw = await run_classify(engine, class_prompt, parser, label_set)
            except (APIError, ParsingError) as e:
                logger.warning(f"Classification failed for {instance.instance_id}: {e}")
                continue

            # Mirror the live run's normalization (v3.0 shared token space).
            normalizer = Normalizer(
                use_lemmatization=config.normalization.use_lemmatization,
                remove_stopwords=config.normalization.remove_stopwords,
                lemmatizer=config.normalization.lemmatizer,
            )
            raw_tokens = {}
            for s in STRATEGY_IDS:
                try:
                    explain_prompt = build_baseline_explain_prompt(
                        s, prompts, predicted_label, clean_text, label_set)
                    raw_response = await run_explain(engine, class_prompt, class_raw,
                                                     explain_prompt,
                                                     max_tokens=strategy_max_tokens(s, clean_text))
                    raw_tokens[s] = parse_raw_tokens(s, raw_response, clean_text, predicted_label,
                                                     label_set, parser, normalizer)
                except (APIError, ParsingError, json.JSONDecodeError) as e:
                    logger.debug(f"  {s} failed for {instance.instance_id}: {e}")
                    raw_tokens[s] = []

            token_sets = {s: normalize_token_list(raw_tokens[s], normalizer) for s in STRATEGY_IDS}
            baseline_ecs = compute_ecs_from_token_sets(token_sets, calc)
            baseline_ecs_adj = compute_ecs_adj_from_token_sets(token_sets, clean_text, normalizer, calc)

            baseline_data.append({
                "instance": instance,
                "clean_text": clean_text,
                "predicted_label": predicted_label,
                "class_raw": class_raw,
                "class_prompt": class_prompt,
                "raw_tokens": raw_tokens,
                "token_sets": token_sets,
                "baseline_ecs": baseline_ecs,
                "baseline_ecs_adj": baseline_ecs_adj,
            })

        # --- Step 2: Prompt Ablation ---
        prompt_results = {}
        if config.ablations.prompt_variants and baseline_data:
            logger.info("Running prompt wording ablation...")
            for s in STRATEGY_IDS:
                alt_template = load_prompt(alt_prompt_map[s])
                if not alt_template:
                    continue

                deltas = []
                deltas_aj = []       # audit F10: same contrast on the primary (AJ) scale
                sc_ajs = []          # R1: same-strategy AJ(base, alt) — self-consistency ceiling
                sc_degenerate = 0
                sc_missing = 0
                for bd in baseline_data:
                    inst = bd["instance"]
                    clean_text = bd["clean_text"]
                    alt_prompt = format_alt_prompt(alt_template, bd["predicted_label"],
                                                   clean_text, label_set)

                    try:
                        raw_alt = await run_explain(engine, bd["class_prompt"],
                                                    bd["class_raw"], alt_prompt,
                                                    max_tokens=strategy_max_tokens(s, clean_text))
                        alt_raw_tokens = parse_raw_tokens(
                            s, raw_alt, clean_text, bd["predicted_label"],
                            label_set, parser, Normalizer())
                        alt_normalizer = Normalizer()
                        alt_set = normalize_token_list(alt_raw_tokens, alt_normalizer)
                    except (APIError, ParsingError, json.JSONDecodeError) as e:
                        logger.debug(f"  alt {s} failed for {inst.instance_id}: {e}")
                        alt_set = set()

                    variant_sets = dict(bd["token_sets"])
                    variant_sets[s] = alt_set
                    variant_ecs = compute_ecs_from_token_sets(variant_sets, calc)
                    if variant_ecs is not None and bd["baseline_ecs"] is not None:
                        deltas.append(variant_ecs - bd["baseline_ecs"])
                    variant_ecs_adj = compute_ecs_adj_from_token_sets(
                        variant_sets, clean_text, Normalizer(), calc)
                    if variant_ecs_adj is not None and bd.get("baseline_ecs_adj") is not None:
                        deltas_aj.append(variant_ecs_adj - bd["baseline_ecs_adj"])

                    # R1 self-consistency ceiling: same strategy, baseline vs paraphrase
                    # wording, on the chance/ceiling-corrected AJ scale.
                    base_set = bd["token_sets"].get(s, set())
                    if not base_set or not alt_set:
                        sc_missing += 1
                    else:
                        aj, degen = compute_self_consistency_aj(
                            base_set, alt_set, clean_text, Normalizer(), calc)
                        if degen:
                            sc_degenerate += 1
                        if aj is not None:
                            sc_ajs.append(aj)

                mean_delta = float(np.mean(deltas)) if deltas else 0.0
                prompt_results[f"{s}_alt"] = {
                    "mean_delta": mean_delta,
                    "n_instances": len(deltas),
                    "deltas": deltas,
                    # Audit F10: the same paraphrase contrast on the PRIMARY metric's
                    # (ECS-adj, available-component) scale — mean_delta above is on the
                    # legacy raw-Jaccard ECS scale and is NOT comparable to AJ ceilings.
                    "mean_delta_aj": (float(np.mean(deltas_aj)) if deltas_aj else None),
                    "n_instances_aj": len(deltas_aj),
                    "deltas_aj": deltas_aj,
                    # Same-strategy paraphrase stability (R1): the ceiling against which
                    # cross-strategy ECS-adj is read. mean AJ(base_set, alt_set) over
                    # instances where both wordings produced evidence.
                    "self_consistency_aj_mean": (float(np.mean(sc_ajs)) if sc_ajs else None),
                    "self_consistency_aj_n": len(sc_ajs),
                    "self_consistency_aj_values": sc_ajs,
                    "self_consistency_n_degenerate": sc_degenerate,
                    "self_consistency_n_missing": sc_missing,
                }
                sc_str = (f"{float(np.mean(sc_ajs)):.4f} (n={len(sc_ajs)})" if sc_ajs else "—")
                logger.info(f"  {s}_alt: mean delta = {mean_delta:.4f} ({len(deltas)} instances); "
                            f"self-consistency AJ = {sc_str}")
                for d in deltas:
                    all_plot_data.append({
                        "Variation": f"prompt_{s}_alt",
                        "ECS_delta": d,
                        "Dataset": dataset_config.name,
                        "Ablation": "prompt",
                    })

            with open(output_dir / f"prompt_ablation_{dataset_config.name}.json", "w") as f:
                json.dump(prompt_results, f, indent=2)
            all_results[f"{dataset_config.name}_prompt"] = prompt_results

    # Save combined results BEFORE plotting (P0.2): the plot must never be able to lose
    # the results JSON if it raises after all the API spend.
    # Audit F10: stamp scope + scales so single-model provenance and the
    # legacy-vs-AJ delta scales are explicit in the artifact itself.
    all_results["_meta"] = {
        # Reflects the RESOLVED model (--model override), not config.models[0].
        "model": model_cfg.model_id,
        "model_name": model_cfg.name,
        "single_model_scope": True,
        # Which reworded prompt set produced these ceilings (--paraphrase). Downstream
        # aggregation pools ceilings ACROSS variants, so the variant must be
        # machine-readable here rather than inferred from the output directory.
        "paraphrase_variant": paraphrase,
        "paraphrase_prompts": alt_prompt_map,
        # Reflects the RESOLVED dataset subset (--datasets override). A partial-scope
        # ceilings file is merged with the model's other ablation dirs downstream
        # (run_disattenuated_agreement.py --ablation-dirs), so the subset must be
        # machine-readable here, not inferred from which keys happen to exist.
        "datasets": [d.name for d in dataset_cfgs],
        "full_dataset_scope": len(dataset_cfgs) == len(config.datasets),
        "delta_scales": {
            "mean_delta": "legacy raw-Jaccard ECS (5 cross-paradigm pairs)",
            "mean_delta_aj": "ECS-adj, available-component (primary metric's scale)",
        },
        "audit": "RESEARCH_AUDIT_2026-07-10 F10",
    }
    with open(output_dir / "ablation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    logger.info(f"Ablation results saved to {output_dir / 'ablation_results.json'}")

    # Generate robustness plot. The plot frame's value column is ECS_delta, not ECS.
    if all_plot_data:
        plot_df = pd.DataFrame(all_plot_data)
        viz = VisualizationGenerator(output_dir, dpi=config.output.figure_dpi)
        viz.plot_robustness_analysis(plot_df, value_col="ECS_delta")
        logger.info(f"Robustness analysis plot saved to {output_dir}")

    logger.info(f"Ablation studies complete. Results saved to {output_dir}")
    return all_results


def main():
    load_dotenv()
    # --model is ablation-specific (which configured model's ceilings to collect);
    # peel it off before delegating the shared flags to parse_command_line_args.
    extra = argparse.ArgumentParser(add_help=False)
    extra.add_argument("--model", type=str, default=None,
                       help="Config model NAME to ablate (e.g. qwen3-235b); default: first configured model")
    extra.add_argument("--datasets", type=str, nargs="+", default=None,
                       help="Config dataset NAMEs to ablate (e.g. cad_imdb); default: all configured datasets")
    extra.add_argument("--paraphrase", type=str, default=None,
                       choices=sorted(ALT_PROMPT_SETS),
                       help="Which reworded prompt set to elicit for the reliability "
                            "ceiling (default: alt, the original single paraphrase)")
    model_args, remaining = extra.parse_known_args()
    args = parse_command_line_args(remaining)
    config = load_and_validate_config(args=args)
    model_cfg = resolve_model(config, model_args.model)
    dataset_cfgs = resolve_datasets(config, model_args.datasets)
    paraphrase = resolve_paraphrase(model_args.paraphrase)
    asyncio.run(run_ablations(config, args, model_cfg=model_cfg, dataset_cfgs=dataset_cfgs,
                              paraphrase=paraphrase))


if __name__ == "__main__":
    main()
