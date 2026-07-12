"""Frequency-weighted null sensitivity for ECS-adj (audit F4, RESEARCH_AUDIT_2026-07-10).

ECS-adj centres each pair's Jaccard at E[J] under UNIFORM draws from the
instance's content vocabulary. Explanation strategies plausibly gravitate to
frequent tokens, so the uniform null can be mildly anti-conservative. This
offline pass (zero API) recomputes every pair's AJ under a null where token
types are drawn without replacement with probability proportional to their
occurrence count in the instance text (support-closure evidence tokens absent
from the text count once), and reports the shift in the complete-case and
available-component ECS-adj, pooled and per cell.

Companion to the legacy pipeline's salience-weighted lift (ecs_lift_weighted):
this puts the same robustness instinct on the primary metric's scale.
N=25 measurement: pooled complete-case 0.4867 -> 0.4635 (-0.023); every cell
stays positive (see audit/2026-07-10/04_results.json).

Usage:  python scripts/run_weighted_null_sensitivity.py --results-dir outputs/<run>
Output: <run>/weighted_null_sensitivity.json
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from scipy.stats import hypergeom

from src.normalization.normalizer import Normalizer

logger = logging.getLogger(__name__)

EPS = 0.10
AJ_PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
MODEL_NAME = {
    "eu.amazon.nova-pro-v1:0": "nova-pro",
    "qwen.qwen3-235b-a22b-2507-v1:0": "qwen3-235b",
    "deepseek.v3-v1:0": "deepseek-v3",
}


def expected_jaccard_exact(a: int, b: int, V: int) -> float:
    a, b = min(a, V), min(b, V)
    if V <= 0 or a <= 0 or b <= 0:
        return 0.0
    ks = np.arange(max(0, a + b - V), min(a, b) + 1)
    pmf = hypergeom.pmf(ks, V, a, b)
    return float(np.sum(pmf * (ks / (a + b - ks))))


def expected_jaccard_weighted(a: int, b: int, weights: np.ndarray,
                              rng: np.random.Generator, draws: int) -> float:
    V = len(weights)
    a, b = min(a, V), min(b, V)
    idx = np.arange(V)
    p = weights / weights.sum()
    vals = np.empty(draws)
    for t in range(draws):
        s1 = set(rng.choice(idx, size=a, replace=False, p=p).tolist())
        s2 = set(rng.choice(idx, size=b, replace=False, p=p).tolist())
        vals[t] = len(s1 & s2) / len(s1 | s2)
    return float(vals.mean())


def aj_from(j: float, ej: float, a: int, b: int):
    j_max = min(a, b) / max(a, b)
    if (j_max - ej) < EPS:
        return None
    return (j - ej) / (j_max - ej)


def ecs_adj_from_pairs(aj: dict):
    def mean_of(keys):
        vals = [aj[k] for k in keys if aj.get(k) is not None]
        return float(np.mean(vals)) if vals else None
    er = mean_of([("H", "R"), ("RO", "R")])
    ep = mean_of([("H", "CF"), ("RO", "CF")])
    rp = aj.get(("R", "CF"))
    comps = [c for c in (er, ep, rp) if c is not None]
    return (float(np.mean(comps)) if comps else None,
            er is not None and ep is not None and rp is not None)


def run(results_dir: Path, draws: int, seed: int) -> dict:
    jsonl = results_dir / "instance_results.jsonl"
    instances = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
    normalizer = Normalizer(use_lemmatization=True, remove_stopwords=True)
    rng = np.random.default_rng(seed)

    rows = []
    for rec in instances:
        expl = {
            "H": set(rec.get("highlighting_tokens") or []),
            "R": set(rec.get("rationale_tokens") or []),
            "CF": set(rec.get("counterfactual_tokens") or []),
            "RO": set(rec.get("rank_ordering_set") or []),
        }
        V = rec.get("vocab_size") or 0
        if V <= 0:
            continue
        cell = f"{MODEL_NAME.get(rec['model'], rec['model'])}_{rec['dataset']}"
        freq = Counter()
        for w in normalizer.normalize_input_text(rec["text"]).split():
            n = normalizer.normalize(w)
            if n:
                freq[n] += 1
        for s_ in expl.values():
            for t in s_:
                if t not in freq:
                    freq[t] += 1
        types = sorted(freq)
        weights = np.array([freq[t] for t in types], dtype=float)

        aj_u, aj_w = {}, {}
        for (x, y) in AJ_PAIRS:
            s1, s2 = expl[x], expl[y]
            if not s1 or not s2:
                continue
            a_, b_ = len(s1), len(s2)
            j = len(s1 & s2) / len(s1 | s2)
            aj_u[(x, y)] = aj_from(j, expected_jaccard_exact(a_, b_, len(types)), a_, b_)
            aj_w[(x, y)] = aj_from(j, expected_jaccard_weighted(a_, b_, weights, rng, draws), a_, b_)
        u_val, u_c = ecs_adj_from_pairs(aj_u)
        w_val, w_c = ecs_adj_from_pairs(aj_w)
        rows.append({"cell": cell, "uniform": u_val, "weighted": w_val,
                     "u_complete": u_c, "w_complete": w_c})

    def summarize(sub):
        u_cc = [r["uniform"] for r in sub if r["u_complete"] and r["uniform"] is not None]
        w_cc = [r["weighted"] for r in sub if r["w_complete"] and r["weighted"] is not None]
        u_av = [r["uniform"] for r in sub if r["uniform"] is not None]
        w_av = [r["weighted"] for r in sub if r["weighted"] is not None]
        return {
            "uniform_complete_mean": float(np.mean(u_cc)) if u_cc else None, "n_u_cc": len(u_cc),
            "weighted_complete_mean": float(np.mean(w_cc)) if w_cc else None, "n_w_cc": len(w_cc),
            "uniform_available_mean": float(np.mean(u_av)) if u_av else None,
            "weighted_available_mean": float(np.mean(w_av)) if w_av else None,
            "n_available": len(u_av),
        }

    out = {
        "provenance": {"draws": draws, "seed": seed, "weighting": "token occurrence count",
                       "note": "Sensitivity only (audit F4) — the pre-registered primary stays "
                               "the uniform exact-hypergeometric null."},
        "pooled": summarize(rows),
        "per_cell": {c: summarize([r for r in rows if r["cell"] == c])
                     for c in sorted({r["cell"] for r in rows})},
        "n_instances": len(rows),
    }
    out_path = results_dir / "weighted_null_sensitivity.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    logger.info(f"weighted-null sensitivity -> {out_path}")
    p = out["pooled"]
    logger.info(f"pooled complete-case: uniform {p['uniform_complete_mean']:.4f} -> "
                f"weighted {p['weighted_complete_mean']:.4f}")
    return out


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    ap = argparse.ArgumentParser(description="Frequency-weighted null sensitivity for ECS-adj (audit F4)")
    ap.add_argument("--results-dir", required=True)
    ap.add_argument("--draws", type=int, default=400)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    run(Path(args.results_dir), args.draws, args.seed)


if __name__ == "__main__":
    main()
