"""Audit 01 — independent recomputation of the N=25 run's headline numbers.

Part of RESEARCH_AUDIT_2026-07-10 (WS7 + WS1.1/1.4 + WS2.1). Reads ONLY the run
artifacts of outputs/20260708_191145_0fe76508 and recomputes everything with
implementations written independently for this audit (nothing imported from
src/ — deliberate: an import would inherit any defect being audited).

Checks
  A  per-instance: legacy ECS (from stored pairwise Jaccards AND re-derived from
     the stored evidence token sets), per-pair adjusted Jaccard, ECS-adj
     components/aggregate/complete flag, degenerate-pair count  — vs stored fields
  B  per-cell and pooled means (complete-case + available + legacy)  — vs
     aggregate_metrics.json and paper/numbers.json
  C  the three pre-registered NHST families (legacy lift / primary complete-case
     ECS-adj / a2 available), incl. min_n_for_test=6 gating and Holm — vs stored
     p-values (bit-exact expected: same algorithm, np.default_rng(42))
  D  exact hypergeometric E[J] vs an independent Monte-Carlo estimate over the
     (a,b,V) geometries that actually occur in the run  (WS1.1)
  E  degeneracy-guard census: which pairs die at eps=0.10, by pair and cell (WS1.4)
  F  support-closure invariant: vocab_size >= |union of the 4 evidence sets|
  G  provenance of the per-cell p-values quoted in paper/numbers.json: do they
     come from the complete-case family (correct) or the available family? (WS2.1)

Usage:  python audit/2026-07-10/01_recompute_headlines.py
Output: audit/2026-07-10/01_results.json + console summary.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import hypergeom

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "outputs" / "20260708_191145_0fe76508"
OUT = Path(__file__).resolve().parent / "01_results.json"

MODEL_NAME = {
    "eu.amazon.nova-pro-v1:0": "nova-pro",
    "qwen.qwen3-235b-a22b-2507-v1:0": "qwen3-235b",
    "deepseek.v3-v1:0": "deepseek-v3",
}

PAIRS = [("H", "R"), ("H", "CF"), ("R", "CF"), ("R", "RO"), ("CF", "RO")]  # ECS pairs (no H-RO)
AJ_PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
EPS = 0.10
MIN_N = 6
N_PERMS = 10000
SEED = 42


# ---------- independent metric implementations ----------

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def expected_jaccard_exact(a: int, b: int, V: int) -> float:
    a, b = min(a, V), min(b, V)
    if V <= 0 or a <= 0 or b <= 0:
        return 0.0
    k_lo, k_hi = max(0, a + b - V), min(a, b)
    ks = np.arange(k_lo, k_hi + 1)
    pmf = hypergeom.pmf(ks, V, a, b)
    return float(np.sum(pmf * (ks / (a + b - ks))))


def expected_jaccard_mc(a: int, b: int, V: int, n_sims: int = 20000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed)
    vals = np.empty(n_sims)
    pop = np.arange(V)
    for i in range(n_sims):
        s1 = set(rng.choice(pop, size=a, replace=False).tolist())
        s2 = set(rng.choice(pop, size=b, replace=False).tolist())
        vals[i] = len(s1 & s2) / len(s1 | s2)
    return float(vals.mean())


def adjusted_jaccard(s1: set, s2: set, V: int, eps: float = EPS):
    """Returns (aj_or_None, degenerate: bool) — mirrors the spec, written fresh."""
    a, b = len(s1), len(s2)
    if a == 0 or b == 0 or V <= 0:
        return None, True
    j = jaccard(s1, s2)
    ej = expected_jaccard_exact(a, b, V)
    j_max = min(a, b) / max(a, b)
    denom = j_max - ej
    if denom < eps:
        return None, True
    return (j - ej) / denom, False


def ecs_adjusted(expl: dict, V: int):
    aj, n_degen = {}, 0
    for (x, y) in AJ_PAIRS:
        s1, s2 = expl.get(x, set()), expl.get(y, set())
        if not s1 or not s2:
            continue
        val, degen = adjusted_jaccard(s1, s2, V)
        if degen:
            n_degen += 1
        if val is not None:
            aj[(x, y)] = val

    def mean_of(keys):
        vals = [aj[k] for k in keys if k in aj]
        return float(np.mean(vals)) if vals else None

    er = mean_of([("H", "R"), ("RO", "R")])
    ep = mean_of([("H", "CF"), ("RO", "CF")])
    rp = aj.get(("R", "CF"))
    comps = [c for c in (er, ep, rp) if c is not None]
    return {
        "er": er, "ep": ep, "rp": rp,
        "ecs_adj": float(np.mean(comps)) if comps else None,
        "complete": (er is not None and ep is not None and rp is not None),
        "n_degenerate": n_degen,
        "aj_pairs": {f"{x}_{y}": v for (x, y), v in aj.items()},
    }


def sign_flip(diffs, n_permutations=N_PERMS, seed=SEED, alternative="greater"):
    xs = np.array([d for d in diffs if d is not None], dtype=float)
    if len(xs) < 2:
        return None
    observed = float(np.mean(xs))
    rng = np.random.default_rng(seed)
    signs = rng.choice([-1.0, 1.0], size=(n_permutations, len(xs)))
    perm_means = (signs * xs).mean(axis=1)
    if alternative == "greater":
        count = int(np.sum(perm_means >= observed))
    else:
        raise ValueError(alternative)
    return (count + 1) / (n_permutations + 1)


def holm(p_values):
    indexed = [(i, p) for i, p in enumerate(p_values) if p is not None]
    m = len(indexed)
    adjusted = [None] * len(p_values)
    if m == 0:
        return adjusted
    indexed.sort(key=lambda t: t[1])
    running = 0.0
    for rank, (i, p) in enumerate(indexed):
        running = max(running, min((m - rank) * p, 1.0))
        adjusted[i] = running
    return adjusted


# ---------- load artifacts ----------

def load_jsonl(p: Path):
    with open(p, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def close(x, y, tol=1e-9):
    if x is None and y is None:
        return True
    if x is None or y is None:
        return False
    return abs(x - y) <= tol


def main():
    instances = load_jsonl(RUN / "instance_results.jsonl")
    agg = json.loads((RUN / "aggregate_metrics.json").read_text(encoding="utf-8"))
    numbers = json.loads((RUN / "paper" / "numbers.json").read_text(encoding="utf-8"))

    findings = {"A_instance_mismatches": [], "B_aggregate": {}, "C_tests": {},
                "D_exact_vs_mc": [], "E_degeneracy": {}, "F_support_closure": [],
                "G_p_provenance": {}, "counts": {}}

    # ---------- A: per-instance recompute ----------
    per_cell = defaultdict(list)
    n_checked = 0
    for rec in instances:
        cell = f"{MODEL_NAME.get(rec['model'], rec['model'])}_{rec['dataset']}"
        expl = {
            "H": set(rec.get("highlighting_tokens") or []),
            "R": set(rec.get("rationale_tokens") or []),
            "CF": set(rec.get("counterfactual_tokens") or []),
            "RO": set(rec.get("rank_ordering_set") or []),
        }
        V = rec.get("vocab_size") or 0

        # F: support closure
        union_ev = expl["H"] | expl["R"] | expl["CF"] | expl["RO"]
        if V < len(union_ev):
            findings["F_support_closure"].append(
                {"id": rec["instance_id"], "cell": cell, "V": V, "union": len(union_ev)})

        # legacy ECS two ways
        stored_pairs = {p: rec.get(f"jaccard_{p[0]}_{p[1]}") for p in PAIRS}
        my_pairs = {}
        for (x, y) in PAIRS:
            s1, s2 = expl[x], expl[y]
            my_pairs[(x, y)] = jaccard(s1, s2) if (s1 and s2) else None
        # compare stored pairwise vs recomputed-from-sets
        for p in PAIRS:
            sp, mp = stored_pairs[p], my_pairs[p]
            if not close(sp, mp):
                findings["A_instance_mismatches"].append(
                    {"id": rec["instance_id"], "field": f"jaccard_{p[0]}_{p[1]}",
                     "stored": sp, "recomputed": mp})
        pair_vals = [v for v in my_pairs.values() if v is not None]
        my_ecs = float(np.mean(pair_vals)) if pair_vals else None
        # legacy ECS gate: n_valid >= 3 at collection; the stored field respects it
        if rec.get("ecs") is not None and not close(rec.get("ecs"), my_ecs, 1e-9):
            findings["A_instance_mismatches"].append(
                {"id": rec["instance_id"], "field": "ecs",
                 "stored": rec.get("ecs"), "recomputed": my_ecs})

        # ECS-adj recompute
        mine = ecs_adjusted(expl, V)
        for field, key in [("ecs_adj_er", "er"), ("ecs_adj_ep", "ep"),
                           ("ecs_adj_rp", "rp"), ("ecs_adj", "ecs_adj")]:
            if not close(rec.get(field), mine[key]):
                findings["A_instance_mismatches"].append(
                    {"id": rec["instance_id"], "field": field,
                     "stored": rec.get(field), "recomputed": mine[key]})
        if bool(rec.get("ecs_adj_complete")) != mine["complete"]:
            findings["A_instance_mismatches"].append(
                {"id": rec["instance_id"], "field": "ecs_adj_complete",
                 "stored": rec.get("ecs_adj_complete"), "recomputed": mine["complete"]})
        if rec.get("n_degenerate_pairs") is not None and \
                int(rec["n_degenerate_pairs"]) != mine["n_degenerate"]:
            findings["A_instance_mismatches"].append(
                {"id": rec["instance_id"], "field": "n_degenerate_pairs",
                 "stored": rec.get("n_degenerate_pairs"), "recomputed": mine["n_degenerate"]})

        per_cell[cell].append({
            "ecs": rec.get("ecs"), "ecs_lift": rec.get("ecs_lift"),
            "ecs_adj": mine["ecs_adj"], "complete": mine["complete"],
            "stored_ecs_adj": rec.get("ecs_adj"),
            "stored_complete": bool(rec.get("ecs_adj_complete")),
            "expl_sizes": {k: len(v) for k, v in expl.items()}, "V": V,
            "aj_pairs": mine["aj_pairs"], "n_degenerate": mine["n_degenerate"],
        })
        n_checked += 1

    findings["counts"]["instances"] = n_checked
    findings["counts"]["A_mismatches"] = len(findings["A_instance_mismatches"])

    # ---------- B: aggregates ----------
    agg_by_group = {}
    for g in (agg if isinstance(agg, list) else agg.get("groups", agg.get("aggregates", []))):
        agg_by_group[(g.get("aggregation_level"), g.get("group_name"))] = g

    b = {}
    all_rows = [r for rows in per_cell.values() for r in rows]

    def series(rows, key, complete_only=False):
        out = []
        for r in rows:
            if complete_only and not r["complete"]:
                continue
            v = r[key]
            if v is not None:
                out.append(v)
        return out

    checks = []
    for (level, gname), g in agg_by_group.items():
        if level == "model_dataset":
            rows = per_cell.get(gname, [])
        elif level in ("overall",):
            rows = all_rows
        elif level == "dataset":
            rows = [r for c, rr in per_cell.items() for r in rr if c.endswith("_" + gname)]
        elif level == "model":
            mname = MODEL_NAME.get(gname, gname)
            rows = [r for c, rr in per_cell.items() for r in rr if c.startswith(mname + "_")]
        else:
            continue
        for stored_key, my_vals in [
            ("mean_ecs", series(rows, "ecs")),
            ("mean_ecs_adj", series(rows, "ecs_adj")),
            ("mean_ecs_adj_complete", series(rows, "ecs_adj", complete_only=True)),
        ]:
            stored = g.get(stored_key)
            mine = float(np.mean(my_vals)) if my_vals else None
            ok = close(stored, mine, 1e-6)
            checks.append({"group": f"{level}:{gname}", "key": stored_key,
                           "stored": stored, "recomputed": mine, "match": ok,
                           "n": len(my_vals)})
    b["group_checks"] = checks
    b["n_mismatched_groups"] = sum(1 for c in checks if not c["match"])
    findings["B_aggregate"] = b

    # ---------- C: NHST families ----------
    cells = sorted(per_cell.keys())
    fam = {}
    # family (a) legacy: ecs_lift > 0
    raw_lift = []
    for c in cells:
        lifts = [r["ecs_lift"] for r in per_cell[c] if r["ecs_lift"] is not None]
        raw_lift.append(sign_flip(lifts) if len(lifts) >= MIN_N else None)
    # family (a) primary: complete-case ecs_adj > 0  (uses STORED ecs_adj to match run)
    raw_cc = []
    for c in cells:
        vals = [r["stored_ecs_adj"] for r in per_cell[c]
                if r["stored_complete"] and r["stored_ecs_adj"] is not None]
        raw_cc.append(sign_flip(vals) if len(vals) >= MIN_N else None)
    # family (a2): available ecs_adj > 0
    raw_av = []
    for c in cells:
        vals = [r["stored_ecs_adj"] for r in per_cell[c] if r["stored_ecs_adj"] is not None]
        raw_av.append(sign_flip(vals) if len(vals) >= MIN_N else None)

    fam["cells"] = cells
    fam["legacy_lift"] = {"raw": raw_lift, "holm": holm(raw_lift)}
    fam["primary_complete"] = {"raw": raw_cc, "holm": holm(raw_cc)}
    fam["a2_available"] = {"raw": raw_av, "holm": holm(raw_av)}
    # compare vs stored per-cell p's
    comp = []
    for i, c in enumerate(cells):
        g = agg_by_group.get(("model_dataset", c), {})
        comp.append({
            "cell": c,
            "stored_lift_p_holm": g.get("ecs_lift_p_holm"),
            "mine_lift_p_holm": fam["legacy_lift"]["holm"][i],
            "stored_cc_p_holm": g.get("ecs_adj_complete_p_holm"),
            "mine_cc_p_holm": fam["primary_complete"]["holm"][i],
            "stored_av_p_holm": g.get("ecs_adj_p_holm"),
            "mine_av_p_holm": fam["a2_available"]["holm"][i],
            "n_complete": sum(1 for r in per_cell[c] if r["stored_complete"]),
            "n_available": sum(1 for r in per_cell[c] if r["stored_ecs_adj"] is not None),
        })
    fam["comparison"] = comp
    findings["C_tests"] = fam

    # ---------- D: exact vs MC null on observed geometries ----------
    geoms = sorted({(min(s["expl_sizes"][x], s["V"]), min(s["expl_sizes"][y], s["V"]), s["V"])
                    for rows in per_cell.values() for s in rows
                    for (x, y) in AJ_PAIRS
                    if s["expl_sizes"][x] > 0 and s["expl_sizes"][y] > 0 and s["V"] > 0})
    rng = np.random.default_rng(7)
    sample = [geoms[i] for i in rng.choice(len(geoms), size=min(40, len(geoms)), replace=False)]
    for (a_, b_, V_) in sample:
        ex = expected_jaccard_exact(a_, b_, V_)
        mc = expected_jaccard_mc(a_, b_, V_, n_sims=20000, seed=11)
        findings["D_exact_vs_mc"].append({"a": a_, "b": b_, "V": V_,
                                          "exact": ex, "mc": mc, "abs_diff": abs(ex - mc)})
    findings["counts"]["D_max_abs_diff"] = max(d["abs_diff"] for d in findings["D_exact_vs_mc"])

    # ---------- E: degeneracy census ----------
    # Degeneracy depends only on the (a,b,V) geometry, never on set contents.
    def degenerate_geom(a_: int, b_: int, V_: int) -> bool:
        if a_ == 0 or b_ == 0 or V_ <= 0:
            return True
        j_max = min(a_, b_) / max(a_, b_)
        return (j_max - expected_jaccard_exact(a_, b_, V_)) < EPS

    census = defaultdict(lambda: defaultdict(int))
    for cell, rows in per_cell.items():
        for r in rows:
            for (x, y) in AJ_PAIRS:
                a_, b_ = r["expl_sizes"][x], r["expl_sizes"][y]
                V_ = r["V"]
                if a_ == 0 or b_ == 0 or V_ <= 0:
                    continue  # empty sets are skipped upstream, not counted degenerate
                if degenerate_geom(a_, b_, V_):
                    census[f"{x}_{y}"][cell] += 1
    findings["E_degeneracy"] = {p: dict(cells_) for p, cells_ in census.items()}
    findings["counts"]["E_total_degenerate_pair_instances"] = int(
        sum(v for cells_ in census.values() for v in cells_.values()))

    # ---------- G: numbers.json p provenance ----------
    pc = numbers.get("per_cell", {})
    prov = []
    for i, c in enumerate(cells):
        entry = pc.get(c) if isinstance(pc, dict) else None
        if entry is None:
            continue
        quoted = entry.get("p_holm", entry.get("p_value"))
        prov.append({
            "cell": c, "numbers_json_p": quoted,
            "equals_complete_family": close(quoted, fam["primary_complete"]["holm"][i], 1e-12),
            "equals_available_family": close(quoted, fam["a2_available"]["holm"][i], 1e-12),
            "equals_legacy_lift": close(quoted, fam["legacy_lift"]["holm"][i], 1e-12),
        })
    findings["G_p_provenance"]["per_cell"] = prov
    findings["G_p_provenance"]["numbers_overall_keys"] = sorted(numbers.get("overall", {}).keys())

    OUT.write_text(json.dumps(findings, indent=2, default=str), encoding="utf-8")

    # ---------- console summary ----------
    print(f"instances checked: {n_checked}")
    print(f"A per-instance mismatches: {findings['counts']['A_mismatches']}")
    for m in findings["A_instance_mismatches"][:10]:
        print("   ", m)
    print(f"B aggregate mismatches: {b['n_mismatched_groups']} of {len(checks)} group-stats")
    for c in checks:
        if not c["match"]:
            print("   ", c)
    print("C tests (per cell): cell | n_cc | stored_cc_pH -> mine | n_av | stored_av_pH -> mine | stored_lift_pH -> mine")
    for row in comp:
        print(f"   {row['cell']:24s} | {row['n_complete']:2d} | "
              f"{row['stored_cc_p_holm']} -> {row['mine_cc_p_holm']} | {row['n_available']:2d} | "
              f"{row['stored_av_p_holm']} -> {row['mine_av_p_holm']} | "
              f"{row['stored_lift_p_holm']} -> {row['mine_lift_p_holm']}")
    print(f"D exact-vs-MC E[J], max |diff| over {len(sample)} geometries: "
          f"{findings['counts']['D_max_abs_diff']:.5f}")
    print(f"E degenerate pair-instances total: {findings['counts']['E_total_degenerate_pair_instances']}")
    print("  by pair:", {p: sum(cc.values()) for p, cc in findings['E_degeneracy'].items()})
    print(f"F support-closure violations: {len(findings['F_support_closure'])}")
    print("G numbers.json per-cell p provenance:")
    for row in prov:
        tag = ("complete" if row["equals_complete_family"] else
               "available" if row["equals_available_family"] else
               "legacy_lift" if row["equals_legacy_lift"] else "UNMATCHED")
        print(f"   {row['cell']:24s} p={row['numbers_json_p']} -> {tag}")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
