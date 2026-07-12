"""Audit 05 — statistics probes: sign-flip calibration, MNAR selection, 200-run power.

Part of RESEARCH_AUDIT_2026-07-10 (WS2.2 / WS2.4 / WS2.5).

A. SIGN-FLIP CALIBRATION (WS2.2). The primary test applies a sign-flip
   permutation test directly to per-instance ECS-adj values, assuming symmetry
   around 0 under H0. But AJ's null distribution is right-skewed by
   construction (floor -E[J]/(Jmax-E[J]) ~ -0.2, ceiling 1). The spec (P1.4)
   claims the one-sided test is therefore CONSERVATIVE. Verify by simulation:
   for each testable cell, generate H0 replicates by drawing each instance's
   four evidence sets uniformly from its own (sizes, V) geometry, computing
   complete-case ECS-adj exactly as production does, and running the exact
   same sign-flip test. Report the empirical type-I error at alpha=0.05.

B. MNAR SELECTION PROBE (WS2.4). Complete-case membership is driven by CF
   validity (~40%). Compare complete vs incomplete instances on observables
   that exist for BOTH groups: er-component AJ, H/R/RO set sizes, vocab size,
   text length, accuracy. Large gaps = the complete-case population is a
   selected subsample on measured covariates (evidence the R8 MNAR caveat has
   bite beyond missingness rate).

C. POWER PROJECTION FOR N=200 (WS2.5). Per cell: complete-case rate and
   ECS-adj mean/sd from N=25 -> projected complete-case n at N=200 -> normal-
   approximation power for the one-sided test at alpha=0.05 raw and
   alpha=0.05/9 (Bonferroni floor for the 9-cell Holm family).

Usage:  python audit/2026-07-10/05_stats_probes.py
Output: audit/2026-07-10/05_results.json + console summary.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import hypergeom, norm, mannwhitneyu

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "outputs" / "20260708_191145_0fe76508"
OUT = Path(__file__).resolve().parent / "05_results.json"

EPS = 0.10
AJ_PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
MODEL_NAME = {
    "eu.amazon.nova-pro-v1:0": "nova-pro",
    "qwen.qwen3-235b-a22b-2507-v1:0": "qwen3-235b",
    "deepseek.v3-v1:0": "deepseek-v3",
}
MIN_N = 6
ALPHA = 0.05
N_REPS = 400          # H0 replicates per cell
N_PERMS = 2000        # perms per replicate (calibration, not reporting)
SEED = 42


_EJ_CACHE: dict = {}


def expected_jaccard_exact(a: int, b: int, V: int) -> float:
    key = (a, b, V)
    if key not in _EJ_CACHE:
        a2, b2 = min(a, V), min(b, V)
        if V <= 0 or a2 <= 0 or b2 <= 0:
            _EJ_CACHE[key] = 0.0
        else:
            ks = np.arange(max(0, a2 + b2 - V), min(a2, b2) + 1)
            pmf = hypergeom.pmf(ks, V, a2, b2)
            _EJ_CACHE[key] = float(np.sum(pmf * (ks / (a2 + b2 - ks))))
    return _EJ_CACHE[key]


def aj_from(j, a, b, V):
    ej = expected_jaccard_exact(a, b, V)
    j_max = min(a, b) / max(a, b)
    if (j_max - ej) < EPS:
        return None
    return (j - ej) / (j_max - ej)


def ecs_adj_from_sets(sets: dict, V: int):
    aj = {}
    for (x, y) in AJ_PAIRS:
        s1, s2 = sets.get(x), sets.get(y)
        if not s1 or not s2:
            continue
        j = len(s1 & s2) / len(s1 | s2)
        val = aj_from(j, len(s1), len(s2), V)
        if val is not None:
            aj[(x, y)] = val

    def mean_of(keys):
        vals = [aj[k] for k in keys if k in aj]
        return float(np.mean(vals)) if vals else None

    er = mean_of([("H", "R"), ("RO", "R")])
    ep = mean_of([("H", "CF"), ("RO", "CF")])
    rp = aj.get(("R", "CF"))
    comps = [c for c in (er, ep, rp) if c is not None]
    return (float(np.mean(comps)) if comps else None,
            er is not None and ep is not None and rp is not None)


def sign_flip_p(xs: np.ndarray, rng: np.random.Generator, n_perms=N_PERMS) -> float:
    observed = xs.mean()
    signs = rng.choice([-1.0, 1.0], size=(n_perms, len(xs)))
    perm_means = (signs * xs).mean(axis=1)
    return (int(np.sum(perm_means >= observed)) + 1) / (n_perms + 1)


def main():
    with open(RUN / "instance_results.jsonl", encoding="utf-8") as f:
        instances = [json.loads(line) for line in f if line.strip()]

    per_cell = defaultdict(list)
    for rec in instances:
        cell = f"{MODEL_NAME.get(rec['model'], rec['model'])}_{rec['dataset']}"
        sizes = {
            "H": len(rec.get("highlighting_tokens") or []),
            "R": len(rec.get("rationale_tokens") or []),
            "CF": len(rec.get("counterfactual_tokens") or []),
            "RO": len(rec.get("rank_ordering_set") or []),
        }
        per_cell[cell].append({
            "sizes": sizes, "V": rec.get("vocab_size") or 0,
            "ecs_adj": rec.get("ecs_adj"),
            "complete": bool(rec.get("ecs_adj_complete")),
            "er": rec.get("ecs_adj_er"),
            "text_len": len((rec.get("text") or "").split()),
            "correct": bool(rec.get("correct")),
            "cf_valid": bool(rec.get("counterfactual_valid")),
        })

    results = {"A_calibration": {}, "B_mnar": {}, "C_power": {}}
    rng = np.random.default_rng(SEED)

    # ---------- A: H0 calibration per testable cell ----------
    for cell, rows in sorted(per_cell.items()):
        cc_rows = [r for r in rows if r["complete"] and r["ecs_adj"] is not None]
        if len(cc_rows) < MIN_N:
            continue
        rejections = 0
        skew_pool = []
        for _ in range(N_REPS):
            vals = []
            for r in cc_rows:
                V = r["V"]
                pop = np.arange(V)
                sets = {}
                for s, sz in r["sizes"].items():
                    sz = min(sz, V)
                    if sz > 0:
                        sets[s] = set(rng.choice(pop, size=sz, replace=False).tolist())
                v, complete = ecs_adj_from_sets(sets, V)
                # production population: this instance IS complete-case (geometry-fixed)
                if v is not None and complete:
                    vals.append(v)
            if len(vals) >= MIN_N:
                p = sign_flip_p(np.array(vals), rng)
                if p <= ALPHA:
                    rejections += 1
                skew_pool.extend(vals)
        skew_arr = np.array(skew_pool)
        results["A_calibration"][cell] = {
            "n_complete": len(cc_rows), "reps": N_REPS,
            "type_I_at_0.05": rejections / N_REPS,
            "h0_mean": float(skew_arr.mean()),
            "h0_skew": float(((skew_arr - skew_arr.mean()) ** 3).mean()
                             / (skew_arr.std() ** 3 + 1e-12)),
        }

    # ---------- B: MNAR probe (pooled) ----------
    complete = [r for rows in per_cell.values() for r in rows if r["complete"]]
    incomplete = [r for rows in per_cell.values() for r in rows if not r["complete"]]

    def cmp_field(f, getter):
        a = np.array([getter(r) for r in complete if getter(r) is not None], dtype=float)
        b = np.array([getter(r) for r in incomplete if getter(r) is not None], dtype=float)
        if len(a) == 0 or len(b) == 0:
            return None
        u = mannwhitneyu(a, b, alternative="two-sided")
        return {"complete_mean": float(a.mean()), "incomplete_mean": float(b.mean()),
                "n_complete": len(a), "n_incomplete": len(b),
                "mannwhitney_p": float(u.pvalue)}

    results["B_mnar"] = {
        "er_component": cmp_field("er", lambda r: r["er"]),
        "text_len": cmp_field("text_len", lambda r: r["text_len"]),
        "vocab_size": cmp_field("V", lambda r: r["V"]),
        "H_size": cmp_field("H", lambda r: r["sizes"]["H"] or None),
        "R_size": cmp_field("R", lambda r: r["sizes"]["R"] or None),
        "accuracy": cmp_field("correct", lambda r: 1.0 if r["correct"] else 0.0),
    }

    # ---------- C: power projection ----------
    for cell, rows in sorted(per_cell.items()):
        cc = [r["ecs_adj"] for r in rows if r["complete"] and r["ecs_adj"] is not None]
        p_cc = len(cc) / len(rows)
        n200 = int(round(200 * p_cc))
        entry = {"cc_rate_n25": p_cc, "projected_n_cc_at_200": n200}
        if len(cc) >= 3:
            mu, sd = float(np.mean(cc)), float(np.std(cc, ddof=1))
            for alpha, tag in [(ALPHA, "raw"), (ALPHA / 9, "bonf9")]:
                z_a = norm.ppf(1 - alpha)
                power = float(norm.cdf(np.sqrt(max(n200, 1)) * mu / sd - z_a)) if sd > 0 else 1.0
                entry[f"power_{tag}"] = power
            entry["mean"] = mu
            entry["sd"] = sd
        results["C_power"][cell] = entry

    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("A sign-flip calibration under H0 (target <= 0.05):")
    for cell, e in results["A_calibration"].items():
        print(f"   {cell:24s} type-I {e['type_I_at_0.05']:.3f}  (n_cc={e['n_complete']}, "
              f"H0 mean {e['h0_mean']:+.4f}, skew {e['h0_skew']:+.2f})")
    print("B MNAR probe (complete vs incomplete):")
    for k, v in results["B_mnar"].items():
        if v:
            print(f"   {k:14s} complete {v['complete_mean']:.3f} vs incomplete {v['incomplete_mean']:.3f} "
                  f"(p={v['mannwhitney_p']:.4f}, n {v['n_complete']}/{v['n_incomplete']})")
    print("C power at N=200 (one-sided):")
    for cell, e in results["C_power"].items():
        pw_r = e.get("power_raw")
        pw_b = e.get("power_bonf9")
        print(f"   {cell:24s} cc_rate {e['cc_rate_n25']:.2f} -> n~{e['projected_n_cc_at_200']:3d}"
              + (f" | power raw {pw_r:.2f} / bonf9 {pw_b:.2f} (mu {e['mean']:.3f}, sd {e['sd']:.3f})"
                 if pw_r is not None else " | too few cc at N=25 to project"))
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
