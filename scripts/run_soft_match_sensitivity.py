"""W6 semantic soft-matching sensitivity (offline; ECS_ROBUSTNESS_PLAN §5, review R5).

Runs AFTER a collection pass, over ``<run>/instance_results.jsonl``, with ZERO API
cost. Answers R5/W6: how much of the depressed rationale-pair (R) agreement is
mere lexical variation ("terrible" vs "awful") rather than evidential disagreement?

For every instance it recomputes the five cross-paradigm pairs BOTH ways:
  * hard adjusted Jaccard (exact hypergeometric null) — the primary metric;
  * soft adjusted Jaccard (τ=0.8 GloVe soft-matching, MC null) — this sensitivity.
The vocabulary the null draws from is reconstructed from the instance text via the
EXACT production code path (pre_clean_text + Normalizer + evidence-set union, the
P1.1 support closure); the reconstruction is validated against the stored
``vocab_size`` and the match rate is reported.

Outputs into the run dir:
  * ``soft_match_sensitivity.json`` — per-pair-type and per-component hard/soft/Δ
    means, complete-case ECS-adj hard vs soft, the R-pair lexical-share headline,
    and full provenance (embedder descriptor, τ, ε, MC draws, seed, match rate);
  * ``soft_match_sensitivity.md`` — a human-readable summary for the paper draft.

Usage:
    python scripts/run_soft_match_sensitivity.py --results-dir outputs/<run> \
        [--tau 0.8] [--eps 0.10] [--mc-draws 200] [--seed 42] \
        [--thresholds 0.7,0.8,0.9]   # diagnostic sweep; primary stays τ=0.8
"""
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np

from src.metrics.metrics_calculator import MetricsCalculator
from src.metrics.soft_match import SoftMatcher, SpacyVectorEmbedder
from src.normalization.normalizer import Normalizer
from src.utils.config_loader import load_config_from_snapshot, load_and_validate_config

logger = logging.getLogger(__name__)

# Mirrors run_experiment.py's vocab block (the structural label guard).
STRUCTURAL_LABELS = {"premise:", "hypothesis:", "sentence1:", "sentence2:", "text:", "label:"}

# Pair taxonomy for the lexical-share analysis. E-P (extraction↔perturbation) is
# the R-free reference; the E-R and R-P pairs are the ones lexical variation in the
# free-text rationale can depress (review R5). "H_RO" is same-paradigm (excluded
# from ECS) but reported as the extraction-internal ceiling.
PAIR_TYPES = ["H_R", "RO_R", "H_CF", "RO_CF", "R_CF", "H_RO"]
R_PAIRS = ["H_R", "RO_R", "R_CF"]          # rationale-containing (may be lexical)
EP_PAIRS = ["H_CF", "RO_CF"]               # extraction↔perturbation (R-free reference)


def _pre_clean_text(text: str) -> str:
    """Identical to run_experiment.pre_clean_text (imported indirectly to avoid the
    heavy run_experiment import chain of API clients)."""
    import html as html_mod
    import re
    text = html_mod.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"#(\d+);", lambda m: chr(int(m.group(1))), text)
    text = re.sub(r"&[a-zA-Z]+;", "", text)
    return text


def reconstruct_vocab(record: Dict, normalizer: Normalizer,
                      evidence: Dict[str, Set[str]]) -> Set[str]:
    """Rebuild the instance vocabulary in the normalized lemma space, exactly as
    run_experiment.py does: input tokens (structural labels dropped) unioned with
    every evidence token any strategy selected (P1.1 support closure)."""
    clean_text = _pre_clean_text(record.get("text", ""))
    input_tokens = normalizer.normalize_input_text(clean_text).split()
    vocab: Set[str] = set()
    for t in input_tokens:
        if t in STRUCTURAL_LABELS:
            continue
        norm = normalizer.normalize(t)
        if norm:
            vocab.add(norm)
    for ev in evidence.values():
        vocab |= ev
    return vocab


def load_evidence(record: Dict) -> Dict[str, Set[str]]:
    """The four strategies' normalized evidence sets as stored in the run."""
    return {
        "H": set(record.get("highlighting_tokens") or []),
        "R": set(record.get("rationale_tokens") or []),
        "CF": set(record.get("counterfactual_tokens") or []),
        "RO": set(record.get("rank_ordering_set") or []),
    }


def _mean(vals: List[float]) -> Optional[float]:
    return float(np.mean(vals)) if vals else None


def _agg(pair_hard: Dict[str, List[float]], pair_soft: Dict[str, List[float]]) -> Dict[str, Dict]:
    """Per-pair-type hard/soft means, Δ and n (paired on instances where BOTH the
    hard and soft AJ are defined, so Δ is a within-instance comparison)."""
    out = {}
    for pt in PAIR_TYPES:
        h, s = pair_hard.get(pt, []), pair_soft.get(pt, [])
        n = min(len(h), len(s))
        hm, sm = _mean(h), _mean(s)
        out[pt] = {
            "hard_aj_mean": hm,
            "soft_aj_mean": sm,
            "delta_soft_minus_hard": (sm - hm) if (hm is not None and sm is not None) else None,
            "n": n,
        }
    return out


def run(results_dir: Path, tau: float, eps: float, mc_draws: int, seed: int,
        thresholds: List[float]) -> Dict:
    jsonl = results_dir / "instance_results.jsonl"
    if not jsonl.exists():
        raise FileNotFoundError(f"No instance_results.jsonl in {results_dir}")

    # Normalization settings: prefer the run's own snapshot so V is rebuilt with the
    # exact config that produced the evidence sets; fall back to the live config.
    snapshot = results_dir / "config_snapshot.yaml"
    try:
        config = load_config_from_snapshot(snapshot) if snapshot.exists() else load_and_validate_config()
    except Exception as e:  # pragma: no cover - config drift is non-fatal for a sensitivity
        logger.warning(f"Config load failed ({e}); using v3.0 defaults")
        config = None
    if config is not None:
        norm = config.normalization
        normalizer = Normalizer(use_lemmatization=norm.use_lemmatization,
                                remove_stopwords=norm.remove_stopwords,
                                lemmatizer=norm.lemmatizer)
    else:
        normalizer = Normalizer(use_lemmatization=True, remove_stopwords=True, lemmatizer="wordnet")

    calc = MetricsCalculator()
    logger.info("Loading pinned offline embedder (en_core_web_md)...")
    embedder = SpacyVectorEmbedder()
    logger.info(f"Embedder: {embedder.descriptor}")

    records = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
    logger.info(f"{len(records)} instances loaded from {jsonl}")

    # Primary matcher at the pre-registered tau; diagnostic matchers for the sweep.
    matchers = {t: SoftMatcher(embedder, tau=t, eps=eps, mc_draws=mc_draws, seed=seed)
                for t in sorted(set(thresholds) | {tau})}

    # Accumulators keyed by threshold.
    pair_hard: Dict[str, List[float]] = {pt: [] for pt in PAIR_TYPES}
    pair_soft: Dict[float, Dict[str, List[float]]] = {t: {pt: [] for pt in PAIR_TYPES} for t in matchers}
    cc_hard: List[float] = []
    cc_soft: Dict[float, List[float]] = {t: [] for t in matchers}
    vocab_match = 0

    # Hard AJ per pair uses the exact null; identical across thresholds, so compute once.
    hard_pair_keys = {"H_R": ("H", "R"), "RO_R": ("RO", "R"), "H_CF": ("H", "CF"),
                      "RO_CF": ("RO", "CF"), "R_CF": ("R", "CF"), "H_RO": ("H", "RO")}

    for rec in records:
        evidence = load_evidence(rec)
        vocab = reconstruct_vocab(rec, normalizer, evidence)
        if len(vocab) == rec.get("vocab_size"):
            vocab_match += 1
        vocab_list = sorted(vocab)

        # hard AJ per pair (exact null)
        hard_vals: Dict[str, Optional[float]] = {}
        for pt, (s1, s2) in hard_pair_keys.items():
            set1, set2 = evidence[s1], evidence[s2]
            if set1 and set2:
                val, _ = calc.adjusted_jaccard(set1, set2, len(vocab))
                hard_vals[pt] = val
                if val is not None:
                    pair_hard[pt].append(val)
            else:
                hard_vals[pt] = None

        # hard complete-case ECS-adj (paradigm-balanced) for the headline denominator check
        hard_ecs = calc.compute_ecs_adjusted(evidence, len(vocab))
        if hard_ecs["ecs_adj_complete"]:
            cc_hard.append(hard_ecs["ecs_adj"])

        for t, sm in matchers.items():
            soft_ecs = sm.soft_ecs_adjusted(evidence, vocab_list)
            for pt, (s1, s2) in hard_pair_keys.items():
                v = soft_ecs["pair_soft_aj"].get(f"{s1}_{s2}")
                if v is not None:
                    pair_soft[t][pt].append(v)
            if soft_ecs["ecs_adj_complete"]:
                cc_soft[t].append(soft_ecs["ecs_adj"])

    match_rate = vocab_match / len(records) if records else 0.0

    # Assemble per-threshold summaries.
    def lexical_share(pair_agg: Dict[str, Dict]) -> Optional[Dict]:
        """Fraction of the E-P↔R-pair gap that soft-matching closes = share of the
        gap attributable to lexical variation. gap = mean(EP) - mean(R-pairs)."""
        def bundle(keys, field):
            vals = [pair_agg[k][field] for k in keys if pair_agg[k][field] is not None]
            return _mean(vals)
        ep_hard = bundle(EP_PAIRS, "hard_aj_mean")
        r_hard = bundle(R_PAIRS, "hard_aj_mean")
        ep_soft = bundle(EP_PAIRS, "soft_aj_mean")
        r_soft = bundle(R_PAIRS, "soft_aj_mean")
        if None in (ep_hard, r_hard, ep_soft, r_soft):
            return None
        gap_hard = ep_hard - r_hard
        gap_soft = ep_soft - r_soft
        share = ((gap_hard - gap_soft) / gap_hard) if abs(gap_hard) > 1e-9 else None
        return {
            "ep_pairs_hard_mean": ep_hard, "r_pairs_hard_mean": r_hard, "gap_hard": gap_hard,
            "ep_pairs_soft_mean": ep_soft, "r_pairs_soft_mean": r_soft, "gap_soft": gap_soft,
            "gap_closed_by_soft_matching": (gap_hard - gap_soft),
            "lexical_share_of_gap": share,
        }

    thresholds_out = {}
    for t in sorted(matchers):
        agg = _agg(pair_hard, pair_soft[t])
        thresholds_out[f"{t:.2f}"] = {
            "pair_types": agg,
            "complete_case_ecs_adj_hard_mean": _mean(cc_hard),
            "complete_case_ecs_adj_soft_mean": _mean(cc_soft[t]),
            "complete_case_n": len(cc_hard),
            "lexical_share": lexical_share(agg),
        }

    result = {
        "results_dir": str(results_dir),
        "n_instances": len(records),
        "provenance": {
            "embedder": embedder.descriptor,
            "primary_tau": tau,
            "eps": eps,
            "mc_draws": mc_draws,
            "seed": seed,
            "thresholds_swept": sorted(matchers),
            "vocab_reconstruction_match_rate": match_rate,
            "note": ("Sensitivity analysis only (ECS_ROBUSTNESS_PLAN §5) — never the "
                     "headline metric. Soft-matching introduces an embedding-model "
                     "confound; reported to BOUND the lexical-variation share of the "
                     "R-pair gap, not to replace exact-token ECS-adj."),
        },
        "primary_threshold": f"{tau:.2f}",
        "thresholds": thresholds_out,
    }
    return result


def write_markdown(result: Dict, path: Path) -> None:
    prov = result["provenance"]
    primary = result["thresholds"][result["primary_threshold"]]
    lines = [
        "# W6 Semantic Soft-Matching Sensitivity",
        "",
        f"**Run:** `{result['results_dir']}`  |  **Instances:** {result['n_instances']}",
        f"**Embedder:** {prov['embedder']}  |  **τ (primary):** {prov['primary_tau']}  "
        f"|  **ε:** {prov['eps']}  |  **MC draws:** {prov['mc_draws']} (seed {prov['seed']})",
        f"**Vocab reconstruction match rate:** {prov['vocab_reconstruction_match_rate']:.1%}",
        "",
        "> Sensitivity analysis only (ECS_ROBUSTNESS_PLAN §5). Soft-matching credits "
        "cross-token cosine ≥ τ via 1-to-1 bipartite matching; the MC null accounts for "
        "the fact that soft-matching lifts chance agreement too. This BOUNDS how much of "
        "the rationale-pair depression is lexical, and is never the headline metric.",
        "",
        f"## Per-pair-type AJ (hard vs soft, τ={result['primary_threshold']})",
        "",
        "| Pair | Kind | Hard AJ | Soft AJ | Δ (soft−hard) | n |",
        "|---|---|---|---|---|---|",
    ]
    kind = {"H_R": "E-R", "RO_R": "E-R", "R_CF": "R-P", "H_CF": "E-P", "RO_CF": "E-P", "H_RO": "E-E (ref)"}
    for pt in PAIR_TYPES:
        d = primary["pair_types"][pt]
        def f(x):
            return f"{x:+.3f}" if isinstance(x, (int, float)) else "—"
        lines.append(f"| {pt.replace('_','–')} | {kind[pt]} | {f(d['hard_aj_mean'])} | "
                     f"{f(d['soft_aj_mean'])} | {f(d['delta_soft_minus_hard'])} | {d['n']} |")

    ls = primary["lexical_share"]
    lines += ["", "## Lexical-share of the E-P ↔ R-pair gap", ""]
    if ls and ls.get("lexical_share_of_gap") is not None:
        lines += [
            f"- Hard: E-P pairs {ls['ep_pairs_hard_mean']:+.3f} vs R-pairs "
            f"{ls['r_pairs_hard_mean']:+.3f} → **gap {ls['gap_hard']:+.3f}**",
            f"- Soft (τ={result['primary_threshold']}): E-P {ls['ep_pairs_soft_mean']:+.3f} vs "
            f"R-pairs {ls['r_pairs_soft_mean']:+.3f} → **gap {ls['gap_soft']:+.3f}**",
            f"- Soft-matching closes **{ls['gap_closed_by_soft_matching']:+.3f}** of the gap "
            f"→ **lexical share ≈ {ls['lexical_share_of_gap']:.1%}** of the R-pair depression "
            "is attributable to lexical variation; the remainder is evidential disagreement.",
        ]
    else:
        lines.append("- Gap undefined at this N (a pair-type had no defined AJ instances).")

    lines += ["", "## Complete-case ECS-adj: hard vs soft", "",
              "| τ | Hard ECS-adj | Soft ECS-adj | n |", "|---|---|---|---|"]
    for tkey in sorted(result["thresholds"]):
        t = result["thresholds"][tkey]
        h, s = t["complete_case_ecs_adj_hard_mean"], t["complete_case_ecs_adj_soft_mean"]
        hs = f"{h:+.4f}" if h is not None else "—"
        ss = f"{s:+.4f}" if s is not None else "—"
        star = " ← primary" if tkey == result["primary_threshold"] else ""
        lines.append(f"| {tkey}{star} | {hs} | {ss} | {t['complete_case_n']} |")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="W6 semantic soft-matching sensitivity (offline)")
    ap.add_argument("--results-dir", required=True, help="Run directory with instance_results.jsonl")
    ap.add_argument("--tau", type=float, default=0.8, help="Pre-registered cosine threshold (default 0.8)")
    ap.add_argument("--eps", type=float, default=0.10, help="Degeneracy guard epsilon (default 0.10)")
    ap.add_argument("--mc-draws", type=int, default=200, help="Monte-Carlo draws for the soft null")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--thresholds", default="0.7,0.8,0.9",
                    help="Comma-separated diagnostic sweep (primary stays --tau)")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    results_dir = Path(args.results_dir)
    thresholds = [float(x) for x in args.thresholds.split(",") if x.strip()]

    result = run(results_dir, args.tau, args.eps, args.mc_draws, args.seed, thresholds)

    json_path = results_dir / "soft_match_sensitivity.json"
    md_path = results_dir / "soft_match_sensitivity.md"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(result, md_path)

    prov = result["provenance"]
    primary = result["thresholds"][result["primary_threshold"]]
    ls = primary["lexical_share"]
    logger.info(f"Wrote {json_path}")
    logger.info(f"Wrote {md_path}")
    logger.info(f"Vocab reconstruction match rate: {prov['vocab_reconstruction_match_rate']:.1%}")
    if ls and ls.get("lexical_share_of_gap") is not None:
        logger.info(f"Lexical share of R-pair gap (τ={args.tau}): {ls['lexical_share_of_gap']:.1%}")


if __name__ == "__main__":
    main()
