"""Audit 03 — cross-model contrast: recompute + composition fairness decomposition.

Part of RESEARCH_AUDIT_2026-07-10 (WS7 + WS8.1).

A. RECOMPUTE (independent implementation): rebuild cross_model_agreement.json's
   headline AJ-scale numbers from instance_results.jsonl — per-strategy cross-model
   AJ means, dataset cross/within means, and the paired per-instance delta with its
   seeded bootstrap CI (bit-exact expected: same np.default_rng(42) recipe, file
   order preserved).

B. COMPOSITION FAIRNESS (new analysis): the shipped paired delta_aj compares
     cross side  = flat mean over available same-strategy model-pairs
                   (CF mostly missing — it parses ~40%),
     within side = paradigm-balanced ecs_adj where CF-bearing components
                   (E-P, R-P) hold fixed 2/3 weight.
   If CF pairs agree less than other pairs, the within side is dragged down by
   construction relative to the cross side. Decomposition:
     (1) per-strategy cross-model AJ vs the within components (er/ep/rp);
     (2) strategy-matched variant: cross side restricted to {H,R,RO} pairs vs
         within er-component only (the cross-paradigm pairs among {H,R,RO});
     (3) CF-representation shares on each side.

Usage:  python audit/2026-07-10/03_crossmodel_recompute.py
Output: audit/2026-07-10/03_results.json + console summary.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import hypergeom

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "outputs" / "20260708_191145_0fe76508"
OUT = Path(__file__).resolve().parent / "03_results.json"

EPS = 0.10
STRATS = ["H", "R", "CF", "RO"]


def expected_jaccard_exact(a: int, b: int, V: int) -> float:
    a, b = min(a, V), min(b, V)
    if V <= 0 or a <= 0 or b <= 0:
        return 0.0
    ks = np.arange(max(0, a + b - V), min(a, b) + 1)
    pmf = hypergeom.pmf(ks, V, a, b)
    return float(np.sum(pmf * (ks / (a + b - ks))))


def adjusted_jaccard(s1: set, s2: set, V: int, eps: float = EPS):
    a, b = len(s1), len(s2)
    if a == 0 or b == 0 or V <= 0:
        return None
    j = len(s1 & s2) / len(s1 | s2)
    ej = expected_jaccard_exact(a, b, V)
    j_max = min(a, b) / max(a, b)
    if (j_max - ej) < eps:
        return None
    return (j - ej) / (j_max - ej)


def jaccard(s1: set, s2: set) -> float:
    return len(s1 & s2) / len(s1 | s2) if (s1 | s2) else 1.0


def paired(d, n_bootstrap=1000, seed=42):
    if not d:
        return {"mean_delta": None, "ci_lower": 0.0, "ci_upper": 0.0, "n": 0,
                "direction": "indeterminate"}
    rng = np.random.default_rng(seed)
    n = len(d)
    boot = [float(np.mean(rng.choice(d, size=n, replace=True))) for _ in range(n_bootstrap)]
    lo, hi = float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))
    direction = ("cross_model_exceeds" if lo > 0 else
                 "within_model_exceeds" if hi < 0 else "indeterminate")
    return {"mean_delta": float(np.mean(d)), "ci_lower": lo, "ci_upper": hi,
            "n": n, "direction": direction}


def close(x, y, tol=1e-9):
    if x is None and y is None:
        return True
    if x is None or y is None:
        return False
    return abs(x - y) <= tol


def evidence(rec, s):
    if s == "H" and rec.get("highlighting_valid"):
        return set(rec.get("highlighting_tokens") or [])
    if s == "R" and rec.get("rationale_valid"):
        return set(rec.get("rationale_tokens") or [])
    if s == "CF" and rec.get("counterfactual_valid"):
        return set(rec.get("counterfactual_tokens") or [])
    if s == "RO" and rec.get("rank_ordering_valid"):
        ro = rec.get("rank_ordering_set")
        if not ro:
            ro = [t for t, _ in (rec.get("rank_ordering_tokens") or [])]
        return set(ro)
    return set()


def main():
    with open(RUN / "instance_results.jsonl", encoding="utf-8") as f:
        instances = [json.loads(line) for line in f if line.strip()]
    stored = json.loads((RUN / "cross_model_agreement.json").read_text(encoding="utf-8"))

    by_instance = defaultdict(list)
    for r in instances:
        by_instance[(r["dataset"], r["instance_id"])].append(r)

    agg_aj = defaultdict(lambda: defaultdict(list))
    within_adj = defaultdict(list)
    deltas_aj = defaultdict(list)
    deltas_matched = defaultdict(list)   # variant B: {H,R,RO} cross vs within er-component
    cf_share_cross = defaultdict(lambda: [0, 0])   # dataset -> [cf_pairs, total_pairs]
    multi = defaultdict(set)

    for (dataset, iid), rows in by_instance.items():
        if len(rows) < 2:
            continue
        multi[dataset].add(iid)
        inst_adj = [r["ecs_adj"] for r in rows if r.get("ecs_adj") is not None]
        for v in inst_adj:
            within_adj[dataset].append(v)
        inst_ajs, inst_ajs_hrro = [], []
        for s in STRATS:
            sets_ = [(evidence(r, s), r.get("vocab_size") or 0) for r in rows]
            sets_ = [x for x in sets_ if x[0]]
            for i in range(len(sets_)):
                for j in range(i + 1, len(sets_)):
                    (si, vi), (sj, vj) = sets_[i], sets_[j]
                    v_pair = max(int(vi), int(vj), len(si | sj))
                    aj = adjusted_jaccard(si, sj, v_pair)
                    cf_share_cross[dataset][1] += 1
                    if s == "CF":
                        cf_share_cross[dataset][0] += 1
                    if aj is not None:
                        agg_aj[dataset][s].append(aj)
                        inst_ajs.append(aj)
                        if s != "CF":
                            inst_ajs_hrro.append(aj)
        if inst_ajs and inst_adj:
            deltas_aj[dataset].append(float(np.mean(inst_ajs)) - float(np.mean(inst_adj)))
        # variant B: within er-component only (cross-paradigm pairs among H,R,RO)
        inst_er = [r.get("ecs_adj_er") for r in rows if r.get("ecs_adj_er") is not None]
        if inst_ajs_hrro and inst_er:
            deltas_matched[dataset].append(
                float(np.mean(inst_ajs_hrro)) - float(np.mean(inst_er)))

    results = {"A_recompute": {}, "B_decomposition": {}, "counts": {}}
    mismatches = []
    for dataset in sorted(multi):
        mine_cross = float(np.mean([v for s in STRATS for v in agg_aj[dataset].get(s, [])]))
        mine_within = float(np.mean(within_adj[dataset])) if within_adj[dataset] else None
        mine_paired = paired(deltas_aj[dataset])
        st = stored.get(dataset, {})
        for path, mine_v, stored_v, tol in [
            ("cross_model_same_strategy_mean_aj", mine_cross,
             st.get("cross_model_same_strategy_mean_aj"), 1e-9),
            ("within_model_cross_strategy_mean_ecs_adj", mine_within,
             st.get("within_model_cross_strategy_mean_ecs_adj"), 1e-9),
            ("paired_contrast_aj.mean_delta", mine_paired["mean_delta"],
             st.get("paired_contrast_aj", {}).get("mean_delta"), 1e-9),
            ("paired_contrast_aj.ci_lower", mine_paired["ci_lower"],
             st.get("paired_contrast_aj", {}).get("ci_lower"), 1e-9),
            ("paired_contrast_aj.ci_upper", mine_paired["ci_upper"],
             st.get("paired_contrast_aj", {}).get("ci_upper"), 1e-9),
        ]:
            if not close(mine_v, stored_v, tol):
                mismatches.append({"dataset": dataset, "path": path,
                                   "stored": stored_v, "recomputed": mine_v})
        per_strat = {s: {"mean_aj": (float(np.mean(agg_aj[dataset][s]))
                                     if agg_aj[dataset].get(s) else None),
                         "n_pairs": len(agg_aj[dataset].get(s, []))} for s in STRATS}
        results["A_recompute"][dataset] = {
            "cross_mean_aj": mine_cross, "within_mean_ecs_adj": mine_within,
            "paired_aj": mine_paired, "per_strategy_aj": per_strat,
        }
        results["B_decomposition"][dataset] = {
            "cf_pair_share_cross": (cf_share_cross[dataset][0] / cf_share_cross[dataset][1]
                                    if cf_share_cross[dataset][1] else None),
            "strategy_matched_delta_HRRO_vs_er": paired(deltas_matched[dataset]),
        }
    results["counts"]["A_mismatches"] = len(mismatches)
    results["A_mismatches"] = mismatches

    OUT.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")

    print(f"A cross-model recompute mismatches: {len(mismatches)}")
    for m in mismatches[:10]:
        print("   ", m)
    print("B decomposition:")
    for ds, a in results["A_recompute"].items():
        b = results["B_decomposition"][ds]
        pm = a["paired_aj"]
        sm = b["strategy_matched_delta_HRRO_vs_er"]
        print(f"   {ds}: shipped delta_aj {pm['mean_delta']:+.3f} [{pm['ci_lower']:+.3f},{pm['ci_upper']:+.3f}] "
              f"(n={pm['n']}) | CF share of cross pairs {b['cf_pair_share_cross']:.2%}")
        print(f"        per-strategy AJ: " + ", ".join(
            f"{s}={a['per_strategy_aj'][s]['mean_aj']:.3f}(n={a['per_strategy_aj'][s]['n_pairs']})"
            if a['per_strategy_aj'][s]['mean_aj'] is not None else f"{s}=–(0)"
            for s in STRATS))
        print(f"        strategy-matched delta (HRRO cross vs within er): {sm['mean_delta']:+.3f} "
              f"[{sm['ci_lower']:+.3f},{sm['ci_upper']:+.3f}] (n={sm['n']}, {sm['direction']})")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
