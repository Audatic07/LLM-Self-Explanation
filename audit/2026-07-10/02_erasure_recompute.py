"""Audit 02 — erasure axis: independent recompute + occurrence-asymmetry probe.

Part of RESEARCH_AUDIT_2026-07-10 (WS7 erasure + WS4.1). Two halves:

A. RECOMPUTE (independent implementations, nothing imported from src/):
   from erasure_instances.jsonl alone, rebuild per-model and pooled
   strategy/CC3/CC4/random flip rates, cc3_minus_random gaps, the family-(b)
   sign-flip + Holm p-values, and held-out CF rates — then diff against
   aggregate_erasure.json. p-values are expected bit-exact (same algorithm,
   np.default_rng(42), diffs in file order).

B. OCCURRENCE-ASYMMETRY PROBE (deliberately imports the pipeline's own
   erase()/Normalizer — here we measure what the production design DOES, not
   whether its arithmetic is right): CC3 evidence tokens are fixed-point
   lemmas whose 3-tier matching can erase several surface variants at once,
   while the random control samples surface forms. Both arms erase
   k = |CC3| token TYPES; do they destroy the same number of token
   OCCURRENCES? For each instance: tokens destroyed by the CC3 erase vs the
   Monte-Carlo mean destroyed over fresh random content-word samples of the
   same k (M=100, seeded, same pool construction as random_flip_rate).
   A systematic excess on the CC3 side = mechanical advantage for the
   treatment arm = the CC3-vs-random gap is partly artifact.

Usage:  python audit/2026-07-10/02_erasure_recompute.py
Output: audit/2026-07-10/02_results.json + console summary.
"""
from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "outputs" / "20260708_191145_0fe76508"
OUT = Path(__file__).resolve().parent / "02_results.json"

sys.path.insert(0, str(REPO))
from scripts.run_validity_tests import erase, _PUNCT  # noqa: E402  (probe B fidelity)
from src.normalization.normalizer import Normalizer  # noqa: E402

OPERATORS = ["mask", "delete"]
STRATS = ["H", "R", "CF", "RO"]
MIN_N = 6
N_PERMS = 10000
SEED = 42


def sign_flip(diffs, n_permutations=N_PERMS, seed=SEED):
    xs = np.array([d for d in diffs if d is not None], dtype=float)
    if len(xs) < 2:
        return None
    observed = float(np.mean(xs))
    rng = np.random.default_rng(seed)
    signs = rng.choice([-1.0, 1.0], size=(n_permutations, len(xs)))
    perm_means = (signs * xs).mean(axis=1)
    return (int(np.sum(perm_means >= observed)) + 1) / (n_permutations + 1)


def holm(p_values):
    indexed = [(i, p) for i, p in enumerate(p_values) if p is not None]
    m = len(indexed)
    adjusted = [None] * len(p_values)
    indexed.sort(key=lambda t: t[1])
    running = 0.0
    for rank, (i, p) in enumerate(indexed):
        running = max(running, min((m - rank) * p, 1.0))
        adjusted[i] = running
    return adjusted


def rate(vals):
    xs = [1 if v else 0 for v in vals if v is not None]
    return (sum(xs) / len(xs)) if xs else None


def mean(vals):
    xs = [v for v in vals if v is not None]
    return (float(np.mean(xs)) if xs else None)


def close(x, y, tol=1e-9):
    if x is None and y is None:
        return True
    if x is None or y is None:
        return False
    return abs(x - y) <= tol


def load_jsonl(p: Path):
    with open(p, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def aggregate_mine(records):
    out = {"n": len(records), "strategy_flip_rate": {}}
    for s in STRATS:
        out["strategy_flip_rate"][s] = {
            op: rate([r["strategy_erasure"].get(s, {}).get(op) for r in records])
            for op in OPERATORS}
    out["cc3_flip_rate"] = {op: rate([r["cc3"].get(op) for r in records]) for op in OPERATORS}
    out["cc4_flip_rate"] = {op: rate([r["cc4"].get(op) for r in records]) for op in OPERATORS}
    out["random_flip_rate"] = {op: mean([r["random_cc3"].get(f"{op}_rate") for r in records])
                               for op in OPERATORS}
    out["cc3_minus_random"] = {
        op: (out["cc3_flip_rate"][op] - out["random_flip_rate"][op])
        if (out["cc3_flip_rate"][op] is not None and out["random_flip_rate"][op] is not None)
        else None for op in OPERATORS}
    raw = []
    n_paired = {}
    for op in OPERATORS:
        diffs = [(1.0 if r["cc3"].get(op) else 0.0) - r["random_cc3"].get(f"{op}_rate")
                 for r in records
                 if r["cc3"].get(op) is not None and r["random_cc3"].get(f"{op}_rate") is not None]
        n_paired[op] = len(diffs)
        raw.append(sign_flip(diffs) if len(diffs) >= MIN_N else None)
    hol = holm(raw)
    out["cc3_vs_random_test"] = {op: {"n_paired": n_paired[op], "p_raw": raw[i], "p_holm": hol[i]}
                                 for i, op in enumerate(OPERATORS)}
    heldout = [r.get("cf_flip_heldout") for r in records]
    out["cf_flip_heldout_rate"] = rate(heldout)
    out["n_cf_heldout_checked"] = sum(1 for v in heldout if v is not None)
    return out


def diff_against_stored(mine: dict, stored: dict, label: str, mismatches: list):
    def cmp(path, a, b, tol=1e-9):
        if not close(a, b, tol):
            mismatches.append({"group": label, "path": path, "stored": b, "recomputed": a})
    for s in STRATS:
        for op in OPERATORS:
            cmp(f"strategy_flip_rate.{s}.{op}", mine["strategy_flip_rate"][s][op],
                stored.get("strategy_flip_rate", {}).get(s, {}).get(op))
    for key in ["cc3_flip_rate", "cc4_flip_rate", "random_flip_rate", "cc3_minus_random"]:
        for op in OPERATORS:
            cmp(f"{key}.{op}", mine[key][op], stored.get(key, {}).get(op))
    for op in OPERATORS:
        for f in ["p_raw", "p_holm"]:
            cmp(f"cc3_vs_random_test.{op}.{f}",
                mine["cc3_vs_random_test"][op][f],
                stored.get("cc3_vs_random_test", {}).get(op, {}).get(f), 1e-12)
    cmp("cf_flip_heldout_rate", mine["cf_flip_heldout_rate"], stored.get("cf_flip_heldout_rate"))


def main():
    erasure = load_jsonl(RUN / "erasure_instances.jsonl")
    stored_agg = json.loads((RUN / "aggregate_erasure.json").read_text(encoding="utf-8"))
    instances = load_jsonl(RUN / "instance_results.jsonl")
    inst_by_key = {(r["instance_id"], r["model"]): r for r in instances}

    findings = {"A_mismatches": [], "B_occurrence_asymmetry": {}, "counts": {}}

    # ---------- A: recompute aggregates ----------
    by_model = defaultdict(list)
    for r in erasure:
        by_model[r.get("model", "unknown")].append(r)

    stored_per_model = stored_agg.get("per_model", {})
    for m, recs in sorted(by_model.items()):
        mine = aggregate_mine(recs)
        stored = stored_per_model.get(m, {}).get("overall", stored_per_model.get(m, {}))
        diff_against_stored(mine, stored, f"per_model:{m}", findings["A_mismatches"])
    pooled_mine = aggregate_mine(erasure)
    stored_pooled = stored_agg.get("pooled", {}).get("overall", stored_agg.get("pooled", {}))
    diff_against_stored(pooled_mine, stored_pooled, "pooled", findings["A_mismatches"])
    findings["counts"]["A_mismatches"] = len(findings["A_mismatches"])

    # ---------- B: occurrence-asymmetry probe ----------
    normalizer = Normalizer(use_lemmatization=True, remove_stopwords=True)
    M = 100
    rows = []
    for r in erasure:
        key = (r["instance_id"], r.get("model", ""))
        inst = inst_by_key.get(key)
        if inst is None:
            continue
        cc3 = set(inst.get("cc3_tokens") or [])
        if not cc3 or not r.get("original_prediction"):
            continue
        text = inst["text"]
        n_words = len(text.split())
        k = len(cc3)

        destroyed_cc3 = n_words - len(erase(text, cc3, "delete", normalizer).split())

        # random pool exactly as random_flip_rate builds it
        surface = list(dict.fromkeys(
            w.strip(_PUNCT).lower() for w in text.split() if w.strip(_PUNCT)))
        pool = [w for w in surface if normalizer.normalize(w) is not None]
        kk = min(k, len(pool))
        if kk == 0:
            continue
        rng = random.Random(1234)
        destroyed_rand = []
        for _ in range(M):
            sample = set(rng.sample(pool, kk))
            destroyed_rand.append(n_words - len(erase(text, sample, "delete", normalizer).split()))
        exp_rand = float(np.mean(destroyed_rand))

        row = {
            "instance_id": r["instance_id"], "model": r.get("model", ""),
            "dataset": r.get("dataset", ""), "k_types": k, "k_rand": kk,
            "n_words": n_words,
            "destroyed_cc3": destroyed_cc3, "destroyed_rand_mean": exp_rand,
            "excess": destroyed_cc3 - exp_rand,
            "excess_per_type": (destroyed_cc3 - exp_rand) / k,
        }
        # join the paired flip gap for the dose-response / subsample probes
        for op in OPERATORS:
            cc_flip = r.get("cc3", {}).get(op)
            rnd_rate = r.get("random_cc3", {}).get(f"{op}_rate")
            row[f"gap_{op}"] = ((1.0 if cc_flip else 0.0) - rnd_rate
                                if cc_flip is not None and rnd_rate is not None else None)
        rows.append(row)

    ex = np.array([row["excess"] for row in rows], dtype=float)
    rel = np.array([row["destroyed_cc3"] / max(row["destroyed_rand_mean"], 1e-9) for row in rows])
    by_ds = defaultdict(list)
    for row in rows:
        by_ds[row["dataset"]].append(row["excess"])
    p_excess = sign_flip([row["excess"] for row in rows])  # is CC3 destroying MORE, paired?
    findings["B_occurrence_asymmetry"] = {
        "n_instances": len(rows),
        "mean_destroyed_cc3": float(np.mean([r_["destroyed_cc3"] for r_ in rows])),
        "mean_destroyed_random": float(np.mean([r_["destroyed_rand_mean"] for r_ in rows])),
        "mean_excess_tokens": float(ex.mean()),
        "median_excess_tokens": float(np.median(ex)),
        "mean_ratio_cc3_over_random": float(rel.mean()),
        "share_instances_excess_pos": float((ex > 0).mean()),
        "share_instances_excess_neg": float((ex < 0).mean()),
        "sign_flip_p_excess_gt_0": p_excess,
        "mean_excess_by_dataset": {d: float(np.mean(v)) for d, v in sorted(by_ds.items())},
        "worst_10": sorted(rows, key=lambda r_: -r_["excess"])[:10],
    }

    # Confound severity probes: (1) does the paired CC3-vs-random gap survive in
    # the subsample with NO destruction advantage (excess <= 0)? (2) is the gap
    # dose-responsive to the excess across instances?
    from scipy.stats import pearsonr, spearmanr
    probes = {}
    for op in OPERATORS:
        have = [r_ for r_ in rows if r_[f"gap_{op}"] is not None]
        gaps = np.array([r_[f"gap_{op}"] for r_ in have])
        exc = np.array([r_["excess"] for r_ in have])
        no_adv = gaps[exc <= 0]
        adv = gaps[exc > 0]
        pr, pp = pearsonr(exc, gaps) if len(have) > 2 else (None, None)
        sr, sp = spearmanr(exc, gaps) if len(have) > 2 else (None, None)
        probes[op] = {
            "n": len(have),
            "gap_full": float(gaps.mean()),
            "gap_excess_le_0": float(no_adv.mean()) if len(no_adv) else None,
            "n_excess_le_0": int(len(no_adv)),
            "p_gap_excess_le_0": sign_flip(no_adv.tolist()) if len(no_adv) >= MIN_N else None,
            "gap_excess_gt_0": float(adv.mean()) if len(adv) else None,
            "n_excess_gt_0": int(len(adv)),
            "pearson_r_excess_gap": float(pr) if pr is not None else None,
            "pearson_p": float(pp) if pp is not None else None,
            "spearman_r_excess_gap": float(sr) if sr is not None else None,
            "spearman_p": float(sp) if sp is not None else None,
        }
    findings["B_confound_probes"] = probes
    findings["B_rows"] = rows

    OUT.write_text(json.dumps(findings, indent=2, default=str), encoding="utf-8")

    print(f"A erasure aggregate mismatches: {findings['counts']['A_mismatches']}")
    for m_ in findings["A_mismatches"][:15]:
        print("   ", m_)
    b = findings["B_occurrence_asymmetry"]
    print(f"B occurrence asymmetry over {b['n_instances']} instances with CC3:")
    print(f"   mean destroyed: cc3 {b['mean_destroyed_cc3']:.2f} vs random {b['mean_destroyed_random']:.2f}"
          f"  (mean excess {b['mean_excess_tokens']:+.2f} tokens, median {b['median_excess_tokens']:+.1f})")
    print(f"   ratio cc3/random {b['mean_ratio_cc3_over_random']:.3f} | share excess>0 {b['share_instances_excess_pos']:.2f}"
          f" | excess<0 {b['share_instances_excess_neg']:.2f} | sign-flip p(excess>0) {b['sign_flip_p_excess_gt_0']}")
    print(f"   mean excess by dataset: {b['mean_excess_by_dataset']}")
    print("B confound probes (gap = paired cc3_flip - random_rate):")
    for op, pr in findings["B_confound_probes"].items():
        print(f"   [{op}] gap full {pr['gap_full']:+.3f} (n={pr['n']}) | "
              f"excess<=0 subsample {pr['gap_excess_le_0']:+.3f} (n={pr['n_excess_le_0']}, p={pr['p_gap_excess_le_0']}) | "
              f"excess>0 {pr['gap_excess_gt_0']:+.3f} (n={pr['n_excess_gt_0']})")
        print(f"        dose-response: pearson r={pr['pearson_r_excess_gap']:+.3f} (p={pr['pearson_p']:.3g}), "
              f"spearman r={pr['spearman_r_excess_gap']:+.3f} (p={pr['spearman_p']:.3g})")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
