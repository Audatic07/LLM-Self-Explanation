"""Audit 04 — is the uniform-draw null the right chance model for AJ? (WS1.3)

Part of RESEARCH_AUDIT_2026-07-10.

ECS-adj centres each pair at E[J] under UNIFORM draws of the two set sizes from
the instance's content vocabulary V. But explanation strategies do not sample
words uniformly: they concentrate on frequent / salient tokens. If two
strategies both lean toward the same high-frequency tokens for reasons
unrelated to shared evidence, uniform-null AJ overstates above-chance
agreement. The legacy lift has a salience-weighted secondary null
(expected_random_overlap_weighted); AJ has no weighted companion.

This script recomputes every pair's AJ under a FREQUENCY-weighted null:
token types are drawn without replacement with probability proportional to
their occurrence count in the instance text (support-closure evidence tokens
absent from the text get count 1). E_w[J] is Monte-Carlo (400 draws, seeded).
The pipeline's own Normalizer builds the frequency table so the token space
is exactly the production one (we are testing the DESIGN, not the arithmetic).

Outputs the pooled + per-cell complete-case ECS-adj under both nulls and the
shift, plus how many instances change complete-case status (degeneracy under
the shifted null uses the same eps=0.10 guard).

Usage:  python audit/2026-07-10/04_null_sensitivity.py
Output: audit/2026-07-10/04_results.json + console summary.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import hypergeom

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "outputs" / "20260708_191145_0fe76508"
OUT = Path(__file__).resolve().parent / "04_results.json"

sys.path.insert(0, str(REPO))
from src.normalization.normalizer import Normalizer  # noqa: E402

EPS = 0.10
AJ_PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
MODEL_NAME = {
    "eu.amazon.nova-pro-v1:0": "nova-pro",
    "qwen.qwen3-235b-a22b-2507-v1:0": "qwen3-235b",
    "deepseek.v3-v1:0": "deepseek-v3",
}
MC_DRAWS = 400
SEED = 42


def expected_jaccard_exact(a: int, b: int, V: int) -> float:
    a, b = min(a, V), min(b, V)
    if V <= 0 or a <= 0 or b <= 0:
        return 0.0
    ks = np.arange(max(0, a + b - V), min(a, b) + 1)
    pmf = hypergeom.pmf(ks, V, a, b)
    return float(np.sum(pmf * (ks / (a + b - ks))))


def expected_jaccard_weighted(a: int, b: int, types: list, weights: np.ndarray,
                              rng: np.random.Generator, draws: int = MC_DRAWS) -> float:
    """MC E[J] when both sets are drawn without replacement with prob ∝ weights."""
    V = len(types)
    a, b = min(a, V), min(b, V)
    idx = np.arange(V)
    p = weights / weights.sum()
    vals = np.empty(draws)
    for t in range(draws):
        s1 = set(rng.choice(idx, size=a, replace=False, p=p).tolist())
        s2 = set(rng.choice(idx, size=b, replace=False, p=p).tolist())
        vals[t] = len(s1 & s2) / len(s1 | s2)
    return float(vals.mean())


def aj_from(j: float, ej: float, a: int, b: int) -> float | None:
    j_max = min(a, b) / max(a, b)
    if (j_max - ej) < EPS:
        return None
    return (j - ej) / (j_max - ej)


def ecs_adj_from_pairs(aj: dict) -> tuple[float | None, bool]:
    def mean_of(keys):
        vals = [aj[k] for k in keys if aj.get(k) is not None]
        return float(np.mean(vals)) if vals else None
    er = mean_of([("H", "R"), ("RO", "R")])
    ep = mean_of([("H", "CF"), ("RO", "CF")])
    rp = aj.get(("R", "CF"))
    comps = [c for c in (er, ep, rp) if c is not None]
    return (float(np.mean(comps)) if comps else None,
            er is not None and ep is not None and rp is not None)


def main():
    with open(RUN / "instance_results.jsonl", encoding="utf-8") as f:
        instances = [json.loads(line) for line in f if line.strip()]

    normalizer = Normalizer(use_lemmatization=True, remove_stopwords=True)
    rng = np.random.default_rng(SEED)

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

        # rebuild the production token space + frequencies over the input text
        freq = Counter()
        for w in normalizer.normalize_input_text(rec["text"]).split():
            n = normalizer.normalize(w)
            if n:
                freq[n] += 1
        # support closure: any selected evidence token missing from text gets count 1
        for s_ in expl.values():
            for t in s_:
                if t not in freq:
                    freq[t] += 1
        types = sorted(freq)
        weights = np.array([freq[t] for t in types], dtype=float)
        # sanity: production vocab_size should equal len(types); track drift
        v_match = (len(types) == V)

        aj_u, aj_w = {}, {}
        for (x, y) in AJ_PAIRS:
            s1, s2 = expl[x], expl[y]
            if not s1 or not s2:
                continue
            a_, b_ = len(s1), len(s2)
            j = len(s1 & s2) / len(s1 | s2)
            aj_u[(x, y)] = aj_from(j, expected_jaccard_exact(a_, b_, len(types)), a_, b_)
            ej_w = expected_jaccard_weighted(a_, b_, types, weights, rng)
            aj_w[(x, y)] = aj_from(j, ej_w, a_, b_)

        u_val, u_complete = ecs_adj_from_pairs(aj_u)
        w_val, w_complete = ecs_adj_from_pairs(aj_w)
        rows.append({"cell": cell, "uniform": u_val, "weighted": w_val,
                     "u_complete": u_complete, "w_complete": w_complete,
                     "v_match": v_match,
                     "max_freq_ratio": float(weights.max() / weights.sum())})

    res = {"per_cell": {}, "pooled": {}, "counts": {}}
    res["counts"]["n_instances"] = len(rows)
    res["counts"]["n_vocab_match"] = int(sum(r["v_match"] for r in rows))

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
            "n_avail": len(u_av),
        }

    res["pooled"] = summarize(rows)
    cells = sorted({r["cell"] for r in rows})
    for c in cells:
        res["per_cell"][c] = summarize([r for r in rows if r["cell"] == c])

    OUT.write_text(json.dumps(res, indent=2), encoding="utf-8")

    p = res["pooled"]
    print(f"instances: {len(rows)} | vocab reconstruction match: {res['counts']['n_vocab_match']}/{len(rows)}")
    print(f"POOLED complete-case ECS-adj: uniform {p['uniform_complete_mean']:.4f} (n={p['n_u_cc']})"
          f" -> freq-weighted {p['weighted_complete_mean']:.4f} (n={p['n_w_cc']})"
          f"  shift {p['weighted_complete_mean'] - p['uniform_complete_mean']:+.4f}")
    print(f"POOLED available    ECS-adj: uniform {p['uniform_available_mean']:.4f}"
          f" -> freq-weighted {p['weighted_available_mean']:.4f}"
          f"  shift {p['weighted_available_mean'] - p['uniform_available_mean']:+.4f}")
    print("per cell (complete-case, uniform -> weighted):")
    for c in cells:
        e = res["per_cell"][c]
        if e["uniform_complete_mean"] is not None and e["weighted_complete_mean"] is not None:
            print(f"   {c:24s} {e['uniform_complete_mean']:+.4f} -> {e['weighted_complete_mean']:+.4f}"
                  f"  (n {e['n_u_cc']}->{e['n_w_cc']})")
        else:
            print(f"   {c:24s} n too small / undefined (n {e['n_u_cc']}->{e['n_w_cc']})")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
