"""Salience baseline for the erasure axis (family (b) hardening, 2026-07-20).

WHY THIS EXISTS
---------------
The erasure pass compares consensus-core (CC3) erasure against a *random* content-word
control. That establishes consensus beats NOISE, not that it beats any salient-token
heuristic — a reviewer can reasonably answer "of course erasing model-selected tokens
flips predictions; you never showed consensus adds anything over salience." The
per-token density analysis is suggestive (CC3 is the densest arm) but is a descriptive
comparison across arms of different sizes, not a controlled test.

This script supplies the controlled version. For every instance with a consensus core it
builds a NON-CONSENSUS salient set, matched to CC3 on both type count and destroyed-token
count, erases it with the same operators, and re-classifies with the instance's OWN model:

  * ``ss1`` (primary) — tokens named by EXACTLY ONE strategy. These are tokens some
    elicitation method called evidence, but which no consensus formed around. This is the
    sharpest available contrast: same provenance (model-selected), differing only in
    whether the paradigms agreed.
  * ``tfidf`` (secondary) — top-TF-IDF content words of the instance excluding CC3
    tokens, with IDF computed over that dataset's own curated corpus. Tests consensus
    against a purely lexical salience heuristic that never consults the model.

Both arms exclude CC3 tokens by construction, so any flip they cause is attributable to
non-consensus evidence.

PRE-REGISTRATION STATUS: post-hoc. Added in revision, after the registered families were
analyzed, in response to external review. Reported as post-hoc wherever it appears; it
does not enter any registered test family.

USAGE
  python scripts/run_salience_baseline.py --results-dir outputs/<run> [--arms ss1 tfidf]
                                          [--max-instances N] [--operators mask delete]
Writes ``<run>/salience_baseline.jsonl`` (per instance, append-only/resumable) and
``<run>/aggregate_salience_baseline.json``.
"""
import argparse
import asyncio
import json
import logging
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv  # noqa: E402

from src.inference.inference_engine import InferenceEngine  # noqa: E402
from src.normalization.normalizer import Normalizer  # noqa: E402
from src.parsing.parser import Parser  # noqa: E402
from src.statistics.statistical_tests import sign_flip_permutation_test, holm_correction  # noqa: E402
from src.utils.config_loader import load_and_validate_config, parse_command_line_args  # noqa: E402
from src.utils.logging_config import setup_logging  # noqa: E402

# Reuse the erasure primitives verbatim — the whole point is that this arm is
# mechanically identical to the CC3 arm except for which tokens it selects.
from scripts.run_validity_tests import (  # noqa: E402
    classify,
    erase,
    erased_token_count,
    load_instance_results,
    _ro_tokens,
)

logger = logging.getLogger(__name__)
_PUNCT = ".,!?;:\"'()[]{}"


def strategy_sets(data: Dict[str, Any]) -> Dict[str, Set[str]]:
    return {
        "H": set(data.get("highlighting_tokens", [])),
        "R": set(data.get("rationale_tokens", [])),
        "CF": set(data.get("counterfactual_tokens", [])),
        "RO": set(_ro_tokens(data)),
    }


def single_strategy_pool(data: Dict[str, Any]) -> List[str]:
    """Tokens named by exactly one strategy (non-consensus, model-selected)."""
    counts: Counter = Counter()
    for toks in strategy_sets(data).values():
        for t in toks:
            counts[t] += 1
    cc3 = set(data.get("cc3_tokens", []))
    # Deterministic order: by descending count then alphabetically. All have count==1
    # here, so this is simply alphabetical — stated explicitly so the selection is
    # reproducible rather than set-iteration-order dependent.
    return sorted(t for t, c in counts.items() if c == 1 and t not in cc3)


def build_idf(instances: List[Dict[str, Any]], normalizer: Normalizer) -> Dict[str, Dict[str, float]]:
    """Per-dataset IDF over that dataset's own instance texts (deduplicated by
    instance_id, since each text appears once per model)."""
    docs: Dict[str, Dict[str, Set[str]]] = defaultdict(dict)
    for d in instances:
        docs[d.get("dataset", "")][d["instance_id"]] = {
            n for n in (normalizer.normalize(w.strip(_PUNCT).lower())
                        for w in d["text"].split() if w.strip(_PUNCT))
            if n
        }
    idf: Dict[str, Dict[str, float]] = {}
    for ds, by_id in docs.items():
        n_docs = len(by_id)
        df: Counter = Counter()
        for toks in by_id.values():
            df.update(toks)
        idf[ds] = {t: math.log((n_docs + 1) / (c + 1)) + 1.0 for t, c in df.items()}
    return idf


def tfidf_pool(data: Dict[str, Any], normalizer: Normalizer,
               idf: Dict[str, Dict[str, float]]) -> List[str]:
    """Instance content tokens ranked by TF-IDF, excluding CC3 tokens."""
    ds_idf = idf.get(data.get("dataset", ""), {})
    tf: Counter = Counter()
    for w in data["text"].split():
        n = normalizer.normalize(w.strip(_PUNCT).lower())
        if n:
            tf[n] += 1
    cc3 = set(data.get("cc3_tokens", []))
    scored = [(t, c * ds_idf.get(t, 1.0)) for t, c in tf.items() if t not in cc3]
    # Descending score, alphabetical tie-break (determinism).
    scored.sort(key=lambda x: (-x[1], x[0]))
    return [t for t, _ in scored]


def matched_sample(text: str, pool: List[str], n_types: int, target_occ: Optional[int],
                   normalizer: Normalizer) -> Set[str]:
    """Take from `pool` in its given (deterministic) order until the sample matches
    CC3 on type count AND, when requested, on destroyed-token count — the same
    matching rule the random control uses (audit F2)."""
    sample: Set[str] = set()
    for t in pool:
        if len(sample) >= n_types and (target_occ is None
                                       or erased_token_count(text, sample, normalizer) >= target_occ):
            break
        sample.add(t)
    return sample


async def flip(engine, parser, class_prompt, text, tokens, op, label_set, original,
               normalizer) -> Optional[bool]:
    if not tokens:
        return None
    pred = await classify(engine, parser, class_prompt, erase(text, tokens, op, normalizer), label_set)
    if not pred:
        return None
    return pred != original


async def process_instance(data, engine, parser, class_prompt, label_set, operators,
                           normalizer, arms, idf) -> Dict[str, Any]:
    text, original = data["text"], data.get("predicted_label", "")
    cc3 = set(data.get("cc3_tokens", []))
    rec: Dict[str, Any] = {
        "instance_id": data["instance_id"],
        "dataset": data.get("dataset", ""),
        "model": data.get("model", ""),
        "ecs_adj": data.get("ecs_adj"),
        "original_prediction": original,
        "cc3_size": len(cc3),
        "arms": {},
    }
    if not original or not cc3:
        rec["skipped"] = "no prediction" if not original else "no cc3"
        return rec
    target_occ = erased_token_count(text, cc3, normalizer)
    rec["cc3_target_occurrences"] = target_occ

    pools = {}
    if "ss1" in arms:
        pools["ss1"] = single_strategy_pool(data)
    if "tfidf" in arms:
        pools["tfidf"] = tfidf_pool(data, normalizer, idf)

    for arm, pool in pools.items():
        sample = matched_sample(text, pool, len(cc3), target_occ, normalizer)
        n_occ = erased_token_count(text, sample, normalizer) if sample else 0
        entry: Dict[str, Any] = {
            "pool_size": len(pool),
            "n_types": len(sample),
            "n_occurrences": n_occ,
            "tokens": sorted(sample),
            # A small non-consensus pool can leave the arm UNDER-matched (fewer types
            # or fewer destroyed occurrences than CC3), which biases it toward fewer
            # flips and would unfairly flatter the consensus arm. Flag it per instance
            # so aggregation can report the strictly-matched subset separately.
            "matched": bool(sample) and len(sample) >= len(cc3) and n_occ >= target_occ,
        }
        if not sample:
            entry["skipped"] = "empty pool"
        else:
            for op in operators:
                entry[op] = await flip(engine, parser, class_prompt, text, sample, op,
                                       label_set, original, normalizer)
        rec["arms"][arm] = entry
    return rec


def aggregate(records: List[Dict[str, Any]], cc3_by_id: Dict[str, Dict[str, Any]],
              operators: List[str], arms: List[str], seed: int) -> Dict[str, Any]:
    """Per model and pooled: arm flip rates, the CC3 contrast, and a paired sign-flip
    test of (CC3 flip - arm flip) per operator, Holm-corrected within each arm."""
    def _rate(vals):
        v = [x for x in vals if x is not None]
        return (sum(1 for x in v if x) / len(v)) if v else None

    out: Dict[str, Any] = {
        "provenance": {
            "prereg": "POST-HOC (added in revision; not in the registered families)",
            "matching": "CC3 type count and destroyed-token count",
            "arms": {"ss1": "tokens named by exactly one strategy (non-consensus, model-selected)",
                     "tfidf": "top-TF-IDF content tokens excluding CC3 (lexical, model-free)"},
            "seed": seed,
            "n_permutations": 10000,
        },
        "per_model": {},
        "pooled": {},
    }
    by_model: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in records:
        by_model[r.get("model", "")].append(r)

    def _block(recs):
        block: Dict[str, Any] = {"n": len(recs), "arms": {}}
        for arm in arms:
            a: Dict[str, Any] = {}
            for op in operators:
                def _collect(matched_only: bool):
                    arm_vals, cc_vals, paired = [], [], []
                    for r in recs:
                        e = r.get("arms", {}).get(arm, {})
                        if e.get(op) is None:
                            continue
                        if matched_only and not e.get("matched"):
                            continue
                        cc = cc3_by_id.get((r["instance_id"], r.get("model", "")), {}).get(op)
                        arm_vals.append(e[op])
                        if cc is not None:
                            cc_vals.append(cc)
                            paired.append((1 if cc else 0) - (1 if e[op] else 0))
                    return arm_vals, cc_vals, paired

                arm_vals, cc_vals, paired = _collect(False)
                a[op] = {
                    "arm_flip_rate": _rate(arm_vals),
                    "cc3_flip_rate_paired": _rate(cc_vals),
                    "n_paired": len(paired),
                    "mean_paired_diff": (sum(paired) / len(paired)) if paired else None,
                }
                if len(paired) >= 6:
                    # Returns a scalar p-value (None when it cannot run).
                    a[op]["p_raw"] = sign_flip_permutation_test(
                        paired, n_permutations=10000, seed=seed, alternative="greater")
                # Strictly-matched subset: instances where the arm reached CC3's type
                # AND destroyed-occurrence counts. Under-matched instances erase less
                # text, so excluding them removes a bias that favours the CC3 arm.
                m_arm, m_cc, m_paired = _collect(True)
                a[op]["matched_only"] = {
                    "arm_flip_rate": _rate(m_arm),
                    "cc3_flip_rate_paired": _rate(m_cc),
                    "n_paired": len(m_paired),
                    "mean_paired_diff": (sum(m_paired) / len(m_paired)) if m_paired else None,
                    "p_raw": (sign_flip_permutation_test(m_paired, n_permutations=10000,
                                                         seed=seed, alternative="greater")
                              if len(m_paired) >= 6 else None),
                }
                sizes = [r["arms"][arm]["n_types"] for r in recs
                         if "n_types" in r.get("arms", {}).get(arm, {})]
                a[op]["n_types_mean"] = (sum(sizes) / len(sizes)) if sizes else None
                flags = [r["arms"][arm].get("matched") for r in recs
                         if "matched" in r.get("arms", {}).get(arm, {})]
                a[op]["pct_matched"] = (100 * sum(1 for f in flags if f) / len(flags)) if flags else None
            # Holm within arm across operators
            ps = [(op, a[op].get("p_raw")) for op in operators if a[op].get("p_raw") is not None]
            if ps:
                corrected = holm_correction([p for _, p in ps])
                for (op, _), pc in zip(ps, corrected):
                    a[op]["p_holm"] = pc
            block["arms"][arm] = a
        return block

    for mid, recs in by_model.items():
        out["per_model"][mid] = _block(recs)
    out["pooled"] = _block(records)
    return out


async def run(config, args):
    results_file = Path(args.results_dir)
    if results_file.suffix != ".jsonl":
        results_file = results_file / "instance_results.jsonl"
    if not results_file.exists():
        logger.error(f"No instance_results.jsonl at {results_file}")
        return
    out_dir = results_file.parent
    setup_logging(log_dir=out_dir / "logs", console_level=config.output.log_level)

    instances = load_instance_results(str(results_file))
    if args.max_instances:
        instances = instances[:args.max_instances]
    operators = list(args.operators) if args.operators else list(config.validity.erasure_operators)
    arms = list(args.arms)

    # CC3 flip results from the completed erasure pass — the paired comparator.
    cc3_by_id: Dict[Any, Dict[str, Any]] = {}
    erasure_file = out_dir / "erasure_instances.jsonl"
    if erasure_file.exists():
        for line in erasure_file.open(encoding="utf-8"):
            r = json.loads(line)
            cc3_by_id[(r["instance_id"], r.get("model", ""))] = r.get("cc3", {})
        logger.info(f"Loaded {len(cc3_by_id)} CC3 comparator records")
    else:
        logger.warning(f"{erasure_file} missing — arm rates will be reported without the paired CC3 contrast")

    configured_ids = {m.model_id for m in config.models}
    by_model: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for d in instances:
        by_model[d.get("model", "")].append(d)
    unknown = sorted(set(by_model) - configured_ids)
    if unknown:
        raise RuntimeError(f"Records from unconfigured model(s): {unknown}. Re-classification "
                           f"must use the SAME model that made each prediction.")

    engines = {mid: InferenceEngine(model_name=mid,
                                    max_retries=config.inference.max_retries,
                                    concurrent_requests=config.inference.concurrent_requests)
               for mid in by_model}
    parser = Parser()
    normalizer = Normalizer(use_lemmatization=config.normalization.use_lemmatization,
                            remove_stopwords=config.normalization.remove_stopwords,
                            lemmatizer=config.normalization.lemmatizer)
    idf = build_idf(instances, normalizer) if "tfidf" in arms else {}

    prompt_cache: Dict[str, str] = {}

    def class_prompt_for(ds: str) -> str:
        if ds not in prompt_cache:
            p = Path(f"prompts/classification_{ds}.txt")
            if not p.exists():
                p = Path("prompts/classification.txt")
            prompt_cache[ds] = p.read_text(encoding="utf-8")
        return prompt_cache[ds]

    labels_for = {d.name: list(d.labels) for d in config.datasets}

    # Resume: skip instance+model rows already collected.
    out_jsonl = out_dir / "salience_baseline.jsonl"
    done = set()
    if out_jsonl.exists():
        for line in out_jsonl.open(encoding="utf-8"):
            try:
                r = json.loads(line)
                done.add((r["instance_id"], r.get("model", "")))
            except json.JSONDecodeError:
                continue
        logger.info(f"Resuming: {len(done)} instances already collected")

    records: List[Dict[str, Any]] = []
    if out_jsonl.exists():
        records = [json.loads(l) for l in out_jsonl.open(encoding="utf-8") if l.strip()]

    todo = [(mid, d) for mid, ds in by_model.items() for d in ds
            if (d["instance_id"], mid) not in done]
    logger.info(f"Salience baseline: {len(todo)} instances to collect "
                f"(arms={arms}, operators={operators})")

    with out_jsonl.open("a", encoding="utf-8") as fh:
        for i, (mid, data) in enumerate(todo, 1):
            rec = await process_instance(
                data, engines[mid], parser, class_prompt_for(data.get("dataset", "")),
                labels_for.get(data.get("dataset", ""), []), operators, normalizer, arms, idf)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            records.append(rec)
            if i % 50 == 0 or i == len(todo):
                logger.info(f"  {i}/{len(todo)} instances")

    scored = [r for r in records if r.get("arms")]
    agg = aggregate(scored, cc3_by_id, operators, arms, seed=42)
    with (out_dir / "aggregate_salience_baseline.json").open("w", encoding="utf-8") as f:
        json.dump(agg, f, indent=2)
    logger.info(f"Wrote {out_dir / 'aggregate_salience_baseline.json'}")
    for arm in arms:
        p = agg["pooled"]["arms"].get(arm, {})
        for op in operators:
            e = p.get(op, {})
            logger.info(f"  pooled {arm}/{op}: arm={e.get('arm_flip_rate')} "
                        f"cc3={e.get('cc3_flip_rate_paired')} "
                        f"diff={e.get('mean_paired_diff')} p_holm={e.get('p_holm')}")


def main():
    load_dotenv()
    extra = argparse.ArgumentParser(add_help=False)
    extra.add_argument("--results-dir", type=str, required=True)
    extra.add_argument("--arms", type=str, nargs="+", default=["ss1"],
                       choices=["ss1", "tfidf"])
    extra.add_argument("--operators", type=str, nargs="+", default=None,
                       choices=["mask", "delete"])
    extra.add_argument("--max-instances", type=int, default=None)
    own, remaining = extra.parse_known_args()
    args = parse_command_line_args(remaining)
    for k, v in vars(own).items():
        setattr(args, k, v)
    config = load_and_validate_config(args=args)
    asyncio.run(run(config, args))


if __name__ == "__main__":
    main()
