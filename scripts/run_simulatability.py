"""Counterfactual-simulatability bridge — Move 3 of
STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md, pre-registered as ECS_ROBUSTNESS_PLAN §H.3
(family (c), NEW).

Descriptive disagreement becomes decision-relevant if it predicts when
explanations fail their core job: letting an observer predict model behavior
(counterfactual simulatability — Chen et al., ICML 2024, arXiv:2307.08678; cf.
arXiv:2606.01148). Design: build explanation-INDEPENDENT perturbations of each
instance, get the target model's actual answers on them, then ask a *different*
model (the simulator, next in config order round-robin — same rule as the
held-out CF judge) to predict those answers given (original text, model's
original prediction, ONE strategy's explanation) vs a no-explanation baseline.

Pre-registered hypothesis (H-sim): instance-level cross-paradigm agreement
(ecs_adj, available-component) is positively associated with simulatability gain
(mean_s gain_s, gain_s = sim_acc_s - sim_acc_baseline). Tests, Holm-corrected
within each family: (c1) pooled Spearman rho(ecs_adj, mean_gain) with cluster
bootstrap CI (cluster = instance), per model; (c2) tercile contrast: sign-flip
permutation (alternative="greater") on top-tercile - bottom-tercile mean_gain,
per model (rank-paired within terciles, deterministic). Descriptive companion:
the "red-flag" operating point — precision/recall of ecs_adj < median for
predicting instances where even the best strategy arm underperforms baseline.

Cohort (pre-registered): first --subset (default 50) instances per dataset per
model in instance_results.jsonl file order (= the ablation cohort's seeded
slice). Checkpointed: appends to simulatability_instances.jsonl after each
instance; re-runs skip already-collected (instance_id, model) rows.

Usage:
    python scripts/run_simulatability.py --results-dir outputs/<run> [--subset 50] [--max-instances N]

Budget at --subset 50 (450 cohort rows): ~1.35k target-label calls + ~6.75k
simulator calls ~= 8.1k requests before retries. Do NOT scale past --subset 50
without explicit approval.
"""
import argparse
import asyncio
import json
import logging
import sys
import zlib
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import scipy.stats
from dotenv import load_dotenv

from src.inference.inference_engine import InferenceEngine
from src.normalization.normalizer import Normalizer
from src.parsing.parser import Parser
from src.statistics.statistical_tests import sign_flip_permutation_test, holm_correction
from src.utils.config_loader import load_and_validate_config
from src.utils.logging_config import setup_logging
# Reuse the erasure pass's operators verbatim (spec §3.1): pool construction,
# 3-tier morphology-aware erasure, and occurrence counting.
from scripts.run_validity_tests import (
    _PUNCT, classify, erase, erased_token_count, load_instance_results,
    random_control_samples,
)

logger = logging.getLogger(__name__)

STRATEGY_ARMS = ["H", "R", "CF", "RO"]
ALL_ARMS = ["baseline"] + STRATEGY_ARMS
N_PERMUTATIONS = 10000
N_BOOTSTRAP = 1000
SEED = 42

SIM_PROMPT_PATH = Path("prompts/simulatability_predict.txt")
SIM_BASELINE_PROMPT_PATH = Path("prompts/simulatability_predict_baseline.txt")


# --------------------------------------------------------------------------- #
#  §3.1 Perturbation generator (deterministic, explanation-independent)        #
# --------------------------------------------------------------------------- #
def perturbation_seeds(instance_id: str) -> Tuple[int, int]:
    """Stable across runs/resumes: s1 = crc32(instance_id) ^ 42, s2 = s1 + 1."""
    s1 = zlib.crc32(instance_id.encode("utf-8")) ^ 42
    return s1, s1 + 1


def content_type_pool(text: str, normalizer: Normalizer) -> List[str]:
    """Unique surface content words — exactly random_control_samples' pool
    construction (order-preserving dedup, normalize survivors)."""
    surface_words = list(dict.fromkeys(
        w.strip(_PUNCT).lower() for w in text.split() if w.strip(_PUNCT)))
    return [w for w in surface_words if normalizer.normalize(w) is not None]


def top_frequency_types(text: str, normalizer: Normalizer, k: int = 3) -> List[str]:
    """The k highest-frequency content types (surface occurrences, ties broken
    alphabetically) — deterministic, text-statistics only (P3)."""
    pool = content_type_pool(text, normalizer)
    pool_set = set(pool)
    freq = Counter(w.strip(_PUNCT).lower() for w in text.split()
                   if w.strip(_PUNCT).lower() in pool_set)
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in ranked[:k]]


def build_perturbations(instance_id: str, text: str,
                        normalizer: Normalizer) -> Tuple[List[Dict[str, str]], int]:
    """<=3 explanation-independent perturbations of the ORIGINAL text:
      P1 delete 3 random content types (seed s1),
      P2 mask 3 random content types (different draw, seed s2),
      P3 delete the 3 highest-frequency content types (deterministic).
    Pool < 3 types -> use all available; a perturbation equal to the original
    text (nothing matched) is dropped and counted. Returns (perturbations,
    n_dropped_noop)."""
    s1, s2 = perturbation_seeds(instance_id)
    specs = []
    p1 = random_control_samples(text, 3, trials=1, seed=s1, normalizer=normalizer)
    if p1:
        specs.append(("P1", p1[0], "delete"))
    p2 = random_control_samples(text, 3, trials=1, seed=s2, normalizer=normalizer)
    if p2:
        specs.append(("P2", p2[0], "mask"))
    top = top_frequency_types(text, normalizer, k=3)
    if top:
        specs.append(("P3", set(top), "delete"))

    perturbations = []
    n_dropped = 0
    for kind, sample, operator in specs:
        new_text = erase(text, set(sample), operator, normalizer)
        if new_text == text:
            n_dropped += 1
            continue
        perturbations.append({"kind": kind, "text": new_text})
    return perturbations, n_dropped


# --------------------------------------------------------------------------- #
#  §3.2 Explanation rendering                                                   #
# --------------------------------------------------------------------------- #
def render_explanation(strategy: str, rec: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """(explanation_text, skip_reason). skip_reason is set when the strategy's
    explanation is missing/invalid for this instance (the arm is skipped)."""
    if strategy == "H":
        tokens = rec.get("highlighting_tokens") or []
        if not tokens:
            return None, "no highlighting evidence"
        return "Most important words: " + ", ".join(tokens), None
    if strategy == "R":
        txt = (rec.get("rationale_text") or "").strip()
        if not txt:
            return None, "no rationale text"
        return txt, None
    if strategy == "CF":
        if not rec.get("cf_flip_verified"):
            return None, "no verified flip"
        cf_text = (rec.get("cf_counterfactual_text") or "").strip()
        if not cf_text:
            return None, "no counterfactual text"
        return f'Minimal edit that flips the prediction: "{cf_text}"', None
    if strategy == "RO":
        ranked = rec.get("rank_ordering_tokens") or []
        tokens = [t for t, _ in ranked] if ranked and isinstance(ranked[0], (list, tuple)) \
            else list(ranked)
        if not tokens:
            return None, "no rank-ordering evidence"
        return "Words ranked by importance: " + ", ".join(tokens), None
    raise ValueError(f"Unknown strategy: {strategy}")


def format_sim_prompt(template: str, rec: Dict[str, Any], perturbed_text: str,
                      label_set: List[str], explanation: Optional[str] = None) -> str:
    kwargs = dict(
        predicted_label=rec["predicted_label"],
        input_text=rec["text"],
        perturbed_text=perturbed_text,
        label_set=", ".join(label_set),
    )
    if explanation is not None:
        kwargs["explanation"] = explanation
    return template.format(**kwargs)


# --------------------------------------------------------------------------- #
#  §3.3 Collection                                                              #
# --------------------------------------------------------------------------- #
async def sim_classify(engine: InferenceEngine, parser: Parser, prompt: str,
                       label_set: List[str]) -> Optional[str]:
    """Classify with a fully-formatted prompt; None on failure (mirrors the
    erasure classify helper's failures-are-unknown policy)."""
    try:
        resp = await engine._make_request(prompt, max_tokens=50)
        pred = parser.parse_classification(resp, label_set)
        return pred or None
    except Exception as e:
        logger.warning(f"simulatability classify failed ({type(e).__name__}: {str(e)[:120]})")
        return None


async def process_instance_sim(rec: Dict[str, Any], target_engine, sim_engine,
                               simulator_id: str, parser: Parser,
                               class_prompt: str, sim_prompt: str,
                               sim_baseline_prompt: str, label_set: List[str],
                               normalizer: Normalizer) -> Dict[str, Any]:
    """One cohort row: build perturbations, get the target model's own labels,
    then the simulator's per-arm predictions."""
    perturbations, n_dropped = build_perturbations(rec["instance_id"], rec["text"], normalizer)

    # Which strategy arms have a usable explanation for this instance?
    explanations: Dict[str, str] = {}
    skipped_arms: Dict[str, str] = {}
    for s in STRATEGY_ARMS:
        expl, reason = render_explanation(s, rec)
        if expl is None:
            skipped_arms[s] = reason
        else:
            explanations[s] = expl

    pert_records = []
    for p in perturbations:
        # Target-model ground truth: the instance's OWN model labels its perturbation.
        target_label = await classify(target_engine, parser, class_prompt,
                                      p["text"], label_set)
        target_label = target_label or None
        arms: Dict[str, Optional[str]] = {}
        arms["baseline"] = await sim_classify(
            sim_engine, parser,
            format_sim_prompt(sim_baseline_prompt, rec, p["text"], label_set), label_set)
        for s in STRATEGY_ARMS:
            if s not in explanations:
                arms[s] = None
                continue
            arms[s] = await sim_classify(
                sim_engine, parser,
                format_sim_prompt(sim_prompt, rec, p["text"], label_set,
                                  explanation=explanations[s]), label_set)
        pert_records.append({"kind": p["kind"], "target_label": target_label, "arms": arms})

    return {
        "instance_id": rec["instance_id"],
        "model": rec["model"],
        "simulator": simulator_id,
        "dataset": rec["dataset"],
        "ecs_adj": rec.get("ecs_adj"),
        "ecs_adj_complete": rec.get("ecs_adj_complete"),
        "perturbations": pert_records,
        "n_perturbations": len(pert_records),
        "n_dropped_noop": n_dropped,
        "skipped_arms": skipped_arms,
    }


def load_done(out_path: Path) -> Set[Tuple[str, str]]:
    """(instance_id, model) keys already collected — the checkpoint skip set."""
    done: Set[Tuple[str, str]] = set()
    if out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    done.add((r["instance_id"], r["model"]))
    return done


def filter_todo(cohort: List[Dict[str, Any]],
                done: Set[Tuple[str, str]]) -> List[Dict[str, Any]]:
    """Checkpoint skip: drop cohort rows already present in the output JSONL
    (keyed instance_id + model) so a re-run never re-collects them."""
    return [r for r in cohort if (r["instance_id"], r["model"]) not in done]


def select_cohort(instances: List[Dict[str, Any]], subset: int) -> List[Dict[str, Any]]:
    """First `subset` instances per dataset per model, in file order (equals the
    ablation cohort's seeded slice — pre-registered §H.3)."""
    counts: Dict[Tuple[str, str], int] = {}
    cohort = []
    for rec in instances:
        key = (rec.get("model", ""), rec.get("dataset", ""))
        if counts.get(key, 0) < subset:
            counts[key] = counts.get(key, 0) + 1
            cohort.append(rec)
    return cohort


# --------------------------------------------------------------------------- #
#  Aggregation (§3.3 bottom)                                                    #
# --------------------------------------------------------------------------- #
def instance_arm_stats(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Per instance x arm: sim_acc_arm = fraction of perturbations with
    arms[arm] == target_label (both non-null); gain_s = sim_acc_s -
    sim_acc_baseline; mean_gain = mean over available strategy arms."""
    sim_acc: Dict[str, Optional[float]] = {}
    for arm in ALL_ARMS:
        hits = []
        for p in rec.get("perturbations", []):
            t = p.get("target_label")
            a = p.get("arms", {}).get(arm)
            if t is None or a is None:
                continue
            hits.append(1.0 if a == t else 0.0)
        sim_acc[arm] = float(np.mean(hits)) if hits else None
    gains: Dict[str, float] = {}
    base = sim_acc["baseline"]
    if base is not None:
        for s in STRATEGY_ARMS:
            if sim_acc[s] is not None:
                gains[s] = sim_acc[s] - base
    mean_gain = float(np.mean(list(gains.values()))) if gains else None
    return {"sim_acc": sim_acc, "gain": gains, "mean_gain": mean_gain}


def spearman_cluster_bootstrap(x: List[float], y: List[float],
                               n_bootstrap: int = N_BOOTSTRAP,
                               seed: int = SEED) -> Dict[str, Any]:
    """Spearman rho with a seeded cluster bootstrap CI (cluster = instance; one
    row per instance per model here, so resampling rows = resampling clusters)."""
    n = len(x)
    if n < 3:
        return {"rho": None, "p_value": None, "ci_lower": None, "ci_upper": None, "n": n}
    rho, p = scipy.stats.spearmanr(x, y)
    rng = np.random.default_rng(seed)
    xs, ys = np.asarray(x), np.asarray(y)
    boot = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        if len(set(ys[idx])) < 2 or len(set(xs[idx])) < 2:
            continue
        r, _ = scipy.stats.spearmanr(xs[idx], ys[idx])
        if not np.isnan(r):
            boot.append(float(r))
    lo, hi = (np.percentile(boot, [2.5, 97.5]) if boot else (None, None))
    return {"rho": float(rho) if not np.isnan(rho) else None,
            "p_value": float(p) if not np.isnan(p) else None,
            "ci_lower": float(lo) if lo is not None else None,
            "ci_upper": float(hi) if hi is not None else None, "n": n}


def tercile_contrast(ecs: List[float], gains: List[float],
                     n_permutations: int = N_PERMUTATIONS,
                     seed: int = SEED) -> Dict[str, Any]:
    """(c2) top-vs-bottom ecs_adj tercile contrast on mean_gain: instances are
    ranked by ecs_adj; the top and bottom terciles are rank-paired (i-th of each,
    both in ecs_adj order, truncated to equal length — deterministic), and the
    paired differences go to the pre-registered one-sided sign-flip test."""
    n = len(ecs)
    if n < 6:
        return {"observed_diff": None, "p_value": None, "n_top": 0, "n_bottom": 0}
    order = np.argsort(ecs, kind="stable")
    third = n // 3
    bottom_idx = order[:third]
    top_idx = order[-third:]
    top = [gains[i] for i in top_idx]
    bottom = [gains[i] for i in bottom_idx]
    diffs = [t - b for t, b in zip(top, bottom)]
    p = sign_flip_permutation_test(diffs, n_permutations=n_permutations,
                                   seed=seed, alternative="greater")
    return {"observed_diff": float(np.mean(top) - np.mean(bottom)),
            "p_value": p, "n_top": len(top), "n_bottom": len(bottom)}


def red_flag_stats(ecs: List[float], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Descriptive red-flag operating point: precision/recall of
    `ecs_adj < median` for predicting instances where even the best strategy
    arm's sim_acc is below baseline (best_s sim_acc_s < baseline_acc)."""
    if not ecs:
        return {"precision": None, "recall": None, "n": 0, "n_flagged": 0, "n_bad": 0}
    med = float(np.median(ecs))
    flagged = [e < med for e in ecs]
    bad = []
    for r in rows:
        sa = r["stats"]["sim_acc"]
        base = sa.get("baseline")
        strat_vals = [sa[s] for s in STRATEGY_ARMS if sa.get(s) is not None]
        bad.append(base is not None and bool(strat_vals) and max(strat_vals) < base)
    tp = sum(1 for f, b in zip(flagged, bad) if f and b)
    n_flagged = sum(flagged)
    n_bad = sum(bad)
    return {
        "median_ecs_adj": med,
        "precision": (tp / n_flagged) if n_flagged else None,
        "recall": (tp / n_bad) if n_bad else None,
        "n": len(ecs), "n_flagged": n_flagged, "n_bad": n_bad,
    }


def aggregate(records: List[Dict[str, Any]], model_order: List[str],
              n_permutations: int = N_PERMUTATIONS, seed: int = SEED,
              provenance: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Full aggregate: per-model (primary unit) + pooled arm means, H-sim tests
    (c1)/(c2) Holm-corrected within each family across the per-model tests, and
    the descriptive red-flag block."""
    rows = []
    for rec in records:
        stats = instance_arm_stats(rec)
        rows.append({"rec": rec, "stats": stats})

    def _arm_means(sub):
        out = {}
        for arm in ALL_ARMS:
            vals = [r["stats"]["sim_acc"][arm] for r in sub
                    if r["stats"]["sim_acc"][arm] is not None]
            out[arm] = {"mean": float(np.mean(vals)) if vals else None, "n": len(vals)}
        return out

    def _gain_means(sub):
        out = {}
        for s in STRATEGY_ARMS:
            vals = [r["stats"]["gain"][s] for r in sub if s in r["stats"]["gain"]]
            out[s] = {"mean": float(np.mean(vals)) if vals else None, "n": len(vals)}
        return out

    def _tested(sub):
        pairs = [(r["rec"]["ecs_adj"], r["stats"]["mean_gain"], r)
                 for r in sub
                 if r["rec"].get("ecs_adj") is not None
                 and r["stats"]["mean_gain"] is not None]
        return ([p[0] for p in pairs], [p[1] for p in pairs], [p[2] for p in pairs])

    per_model: Dict[str, Any] = {}
    c1_ps, c2_ps, tested_models = [], [], []
    for mid in model_order:
        sub = [r for r in rows if r["rec"]["model"] == mid]
        if not sub:
            continue
        ecs, gains, trows = _tested(sub)
        c1 = spearman_cluster_bootstrap(ecs, gains, seed=seed)
        c2 = tercile_contrast(ecs, gains, n_permutations=n_permutations, seed=seed)
        per_model[mid] = {
            "n_instances": len(sub),
            "n_tested": len(ecs),
            "sim_acc": _arm_means(sub),
            "gain": _gain_means(sub),
            "c1_spearman": c1,
            "c2_tercile": c2,
            "red_flag": red_flag_stats(ecs, trows),
        }
        tested_models.append(mid)
        c1_ps.append(c1["p_value"])
        c2_ps.append(c2["p_value"])

    # Holm within each family across the per-model tests (family size = number of
    # non-None tests; holm_correction passes None through untouched).
    for mid, p1, p2 in zip(tested_models, holm_correction(c1_ps), holm_correction(c2_ps)):
        per_model[mid]["c1_spearman"]["p_holm"] = p1
        per_model[mid]["c2_tercile"]["p_holm"] = p2

    ecs_all, gains_all, trows_all = _tested(rows)
    pooled = {
        "n_instances": len(rows),
        "n_tested": len(ecs_all),
        "sim_acc": _arm_means(rows),
        "gain": _gain_means(rows),
        "c1_spearman": spearman_cluster_bootstrap(ecs_all, gains_all, seed=seed),
        "c2_tercile": tercile_contrast(ecs_all, gains_all,
                                       n_permutations=n_permutations, seed=seed),
        "red_flag": red_flag_stats(ecs_all, trows_all),
    }

    return {
        "provenance": provenance or {},
        "per_model": per_model,
        "pooled": pooled,
    }


# --------------------------------------------------------------------------- #
#  Orchestration                                                               #
# --------------------------------------------------------------------------- #
async def run(config, args):
    results_dir = Path(args.results_dir)
    results_file = results_dir / "instance_results.jsonl"
    if not results_file.exists():
        logger.error(f"No instance_results.jsonl in {results_dir}")
        return

    setup_logging(log_dir=results_dir / "logs", console_level=config.output.log_level)
    instances = load_instance_results(str(results_file))
    cohort = select_cohort(instances, args.subset)
    if args.max_instances:
        cohort = cohort[:args.max_instances]
    logger.info(f"Simulatability cohort: {len(cohort)} rows "
                f"(subset={args.subset}/dataset/model, file order)")

    out_path = results_dir / "simulatability_instances.jsonl"
    done = load_done(out_path)
    todo = filter_todo(cohort, done)
    logger.info(f"{len(done)} rows already collected; {len(todo)} to collect")

    # Group by model; hard error on unknown ids (mirrors run_validity_tests.run).
    configured_ids = [m.model_id for m in config.models]
    unknown = sorted({r["model"] for r in todo} - set(configured_ids))
    if unknown:
        raise RuntimeError(
            f"instance_results.jsonl contains records from model(s) not in the "
            f"current config: {unknown}.")
    if len(configured_ids) < 2:
        raise RuntimeError("Simulatability needs >= 2 configured models "
                           "(the simulator is the NEXT model round-robin, never the target).")

    engines = {mid: InferenceEngine(
        model_name=mid,
        max_retries=config.inference.max_retries,
        concurrent_requests=config.inference.concurrent_requests,
    ) for mid in configured_ids}
    simulator_for = {
        mid: configured_ids[(configured_ids.index(mid) + 1) % len(configured_ids)]
        for mid in configured_ids
    }

    parser = Parser()
    normalizer = Normalizer(
        use_lemmatization=config.normalization.use_lemmatization,
        remove_stopwords=config.normalization.remove_stopwords,
        lemmatizer=config.normalization.lemmatizer,
    )
    sim_prompt = SIM_PROMPT_PATH.read_text(encoding="utf-8")
    sim_baseline_prompt = SIM_BASELINE_PROMPT_PATH.read_text(encoding="utf-8")

    prompt_cache: Dict[str, str] = {}

    def class_prompt_for(ds: str) -> str:
        if ds not in prompt_cache:
            p = Path(f"prompts/classification_{ds}.txt")
            if not p.exists():
                p = Path("prompts/classification.txt")
            prompt_cache[ds] = p.read_text(encoding="utf-8")
        return prompt_cache[ds]

    n_done = 0
    for rec in todo:
        mid = rec["model"]
        ds_cfg = config.get_dataset_by_name(rec["dataset"])
        label_set = ds_cfg.labels if ds_cfg else ["positive", "negative"]
        out_rec = await process_instance_sim(
            rec, engines[mid], engines[simulator_for[mid]], simulator_for[mid],
            parser, class_prompt_for(rec["dataset"]), sim_prompt,
            sim_baseline_prompt, label_set, normalizer)
        # Checkpoint: append-only after each instance.
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(out_rec) + "\n")
        n_done += 1
        logger.info(f"[{n_done}/{len(todo)}] {rec['instance_id']} ({mid}) simulatability done")

    # Aggregate everything collected so far (prior + this run).
    all_records = []
    with open(out_path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                all_records.append(json.loads(line))
    import hashlib
    provenance = {
        "prereg": "ECS_ROBUSTNESS_PLAN §H.3 (family (c))",
        "subset": args.subset,
        "seed": SEED,
        "perturbation_seeds": "s1=crc32(instance_id)^42, s2=s1+1; P3 deterministic top-frequency",
        "n_permutations": N_PERMUTATIONS,
        "n_bootstrap": N_BOOTSTRAP,
        "simulator_rule": "next configured model round-robin (never the target)",
        "prompt_hashes": {
            "simulatability_predict": hashlib.sha256(sim_prompt.encode()).hexdigest(),
            "simulatability_predict_baseline": hashlib.sha256(sim_baseline_prompt.encode()).hexdigest(),
        },
    }
    agg = aggregate(all_records, configured_ids, provenance=provenance)
    agg_path = results_dir / "aggregate_simulatability.json"
    with open(agg_path, "w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)
    logger.info(f"Wrote {agg_path} ({len(all_records)} instance rows)")
    for mid, m in agg["per_model"].items():
        c1, c2 = m["c1_spearman"], m["c2_tercile"]
        logger.info(f"{mid}: rho={c1['rho']} (p_holm={c1.get('p_holm')}), "
                    f"tercile diff={c2['observed_diff']} (p_holm={c2.get('p_holm')})")


def main():
    load_dotenv()
    ap = argparse.ArgumentParser(description="Counterfactual-simulatability bridge (family (c))")
    ap.add_argument("--results-dir", type=str, required=True,
                    help="Main run dir containing instance_results.jsonl")
    ap.add_argument("--subset", type=int, default=50,
                    help="Cohort size per dataset per model (pre-registered 50; "
                         "do not scale up without approval)")
    ap.add_argument("--max-instances", type=int, default=None,
                    help="Hard cap on cohort rows (smoke runs)")
    ap.add_argument("--config-dir", type=str, default="config")
    args = ap.parse_args()
    config = load_and_validate_config(config_dir=args.config_dir)
    asyncio.run(run(config, args))


if __name__ == "__main__":
    main()
