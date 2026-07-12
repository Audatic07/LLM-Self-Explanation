"""Audit 06 — soft-matching probes + consistency-ladder CIs.

Part of RESEARCH_AUDIT_2026-07-10 (WS5 + WS8.2).

A. ANTONYM / NEAR-MISS HAZARD (WS5.2). The W6 soft-matcher uses static GloVe
   vectors (en_core_web_md) at cosine tau=0.8. Static antonyms are notoriously
   close in GloVe space; if canonical antonym pairs sit in [0.6, 0.8), then
   LOWERING tau (the naive response to "soft matching changed nothing") would
   start crediting polarity-flipping matches — catastrophic for a sentiment
   task. Measure cosines for canonical antonym pairs and for same-field
   near-synonyms, with the pipeline's own embedder.

B. MC-NULL NOISE (WS5.3). The soft null E[soft J] is Monte-Carlo (200 draws,
   seed 42). Bound the seed-sensitivity of the headline soft numbers: recompute
   the H_R soft-AJ pair mean at tau=0.8 under a different MC seed and report
   the shift. (Uses the pipeline's SoftMatcher for fidelity.)

C. LADDER CIs (WS8.2). The N25 analysis reads a "consistency ladder"
   (E-P > E-R > R-P) off pooled pair-type means. Attach seeded cluster
   bootstrap CIs (resampling instances) to each pooled pair-type AJ mean and
   to the pairwise ladder differences, so the report can say which rungs are
   separated at N=25 and which are narrative.

Usage:  python audit/2026-07-10/06_softmatch_probe.py
Output: audit/2026-07-10/06_results.json + console summary.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import hypergeom

REPO = Path(__file__).resolve().parents[2]
RUN = REPO / "outputs" / "20260708_191145_0fe76508"
OUT = Path(__file__).resolve().parent / "06_results.json"

sys.path.insert(0, str(REPO))
from src.metrics.soft_match import SoftMatcher, SpacyVectorEmbedder  # noqa: E402

EPS = 0.10
AJ_PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
PAIR_KIND = {("H", "R"): "E-R", ("RO", "R"): "E-R",
             ("H", "CF"): "E-P", ("RO", "CF"): "E-P",
             ("R", "CF"): "R-P"}

ANTONYMS = [("good", "bad"), ("positive", "negative"), ("rise", "fall"),
            ("increase", "decrease"), ("win", "lose"), ("happy", "sad"),
            ("best", "worst"), ("love", "hate"), ("up", "down"), ("buy", "sell")]
NEAR_SYNONYMS = [("movie", "film"), ("big", "large"), ("company", "firm"),
                 ("profit", "earnings"), ("game", "match"), ("great", "excellent"),
                 ("rise", "climb"), ("say", "state"), ("buy", "purchase"),
                 ("war", "conflict")]


def expected_jaccard_exact(a, b, V):
    a, b = min(a, V), min(b, V)
    if V <= 0 or a <= 0 or b <= 0:
        return 0.0
    ks = np.arange(max(0, a + b - V), min(a, b) + 1)
    pmf = hypergeom.pmf(ks, V, a, b)
    return float(np.sum(pmf * (ks / (a + b - ks))))


def aj_hard(s1, s2, V):
    a, b = len(s1), len(s2)
    if a == 0 or b == 0 or V <= 0:
        return None
    j = len(s1 & s2) / len(s1 | s2)
    ej = expected_jaccard_exact(a, b, V)
    j_max = min(a, b) / max(a, b)
    if (j_max - ej) < EPS:
        return None
    return (j - ej) / (j_max - ej)


def main():
    results = {"A_cosines": {}, "B_mc_noise": {}, "C_ladder": {}}

    # ---------- A ----------
    emb = SpacyVectorEmbedder()
    def cos(w1, w2):
        return float(emb.similarity(w1, w2))
    results["A_cosines"]["antonyms"] = {f"{a}/{b}": cos(a, b) for a, b in ANTONYMS}
    results["A_cosines"]["near_synonyms"] = {f"{a}/{b}": cos(a, b) for a, b in NEAR_SYNONYMS}
    ant = np.array(list(results["A_cosines"]["antonyms"].values()))
    syn = np.array(list(results["A_cosines"]["near_synonyms"].values()))
    results["A_cosines"]["summary"] = {
        "antonym_mean": float(ant.mean()), "antonym_max": float(ant.max()),
        "antonyms_in_0.6_0.8": int(((ant >= 0.6) & (ant < 0.8)).sum()),
        "antonyms_ge_0.8": int((ant >= 0.8).sum()),
        "synonym_mean": float(syn.mean()),
        "synonyms_ge_0.8": int((syn >= 0.8).sum()),
        "synonyms_in_0.6_0.8": int(((syn >= 0.6) & (syn < 0.8)).sum()),
    }

    # ---------- load instances (shared by B and C) ----------
    with open(RUN / "instance_results.jsonl", encoding="utf-8") as f:
        instances = [json.loads(line) for line in f if line.strip()]

    def evidence(rec):
        return {
            "H": set(rec.get("highlighting_tokens") or []),
            "R": set(rec.get("rationale_tokens") or []),
            "CF": set(rec.get("counterfactual_tokens") or []),
            "RO": set(rec.get("rank_ordering_set") or []),
        }

    # vocab list reconstruction: reuse production reconstruct_vocab
    from scripts.run_soft_match_sensitivity import reconstruct_vocab  # noqa: E402
    from src.normalization.normalizer import Normalizer  # noqa: E402
    normalizer = Normalizer(use_lemmatization=True, remove_stopwords=True)

    # ---------- B: MC-null seed sensitivity on H_R at tau=0.8 ----------
    def hr_soft_mean(seed):
        sm = SoftMatcher(embedder=emb, tau=0.8, eps=EPS, mc_draws=200, seed=seed)
        vals = []
        for rec in instances:
            ev = evidence(rec)
            if not ev["H"] or not ev["R"]:
                continue
            vocab = reconstruct_vocab(rec, normalizer, ev)
            aj, _degen, _extras = sm.soft_adjusted_jaccard(ev["H"], ev["R"], sorted(vocab))
            if aj is not None:
                vals.append(aj)
        return float(np.mean(vals)), len(vals)

    m42, n42 = hr_soft_mean(42)
    m43, n43 = hr_soft_mean(43)
    results["B_mc_noise"] = {
        "H_R_soft_aj_mean_seed42": m42, "n_seed42": n42,
        "H_R_soft_aj_mean_seed43": m43, "n_seed43": n43,
        "abs_shift": abs(m42 - m43),
        "artifact_value_tau_0.80": 0.4295490930849158,
    }

    # ---------- C: ladder CIs (hard AJ, pooled, cluster bootstrap over instances) ----------
    by_kind_per_instance = defaultdict(dict)   # instance idx -> kind -> [ajs]
    for idx, rec in enumerate(instances):
        ev = evidence(rec)
        V = rec.get("vocab_size") or 0
        for (x, y) in AJ_PAIRS:
            if not ev[x] or not ev[y]:
                continue
            aj = aj_hard(ev[x], ev[y], V)
            if aj is not None:
                by_kind_per_instance[idx].setdefault(PAIR_KIND[(x, y)], []).append(aj)

    idxs = sorted(by_kind_per_instance)
    rng = np.random.default_rng(42)
    kinds = ["E-R", "E-P", "R-P"]

    def kind_means(sample_idxs):
        pools = {k: [] for k in kinds}
        for i in sample_idxs:
            for k, vals in by_kind_per_instance[i].items():
                pools[k].extend(vals)
        return {k: (float(np.mean(v)) if v else None) for k, v in pools.items()}

    point = kind_means(idxs)
    boots = {k: [] for k in kinds}
    dif_boots = defaultdict(list)
    for _ in range(2000):
        sample = rng.choice(idxs, size=len(idxs), replace=True)
        km = kind_means(sample)
        for k in kinds:
            if km[k] is not None:
                boots[k].append(km[k])
        for (k1, k2) in [("E-P", "E-R"), ("E-R", "R-P"), ("E-P", "R-P")]:
            if km[k1] is not None and km[k2] is not None:
                dif_boots[f"{k1} minus {k2}"].append(km[k1] - km[k2])

    results["C_ladder"]["means"] = {
        k: {"point": point[k],
            "ci_lower": float(np.percentile(boots[k], 2.5)),
            "ci_upper": float(np.percentile(boots[k], 97.5))} for k in kinds}
    results["C_ladder"]["differences"] = {
        name: {"point": float(np.mean(v)),
               "ci_lower": float(np.percentile(v, 2.5)),
               "ci_upper": float(np.percentile(v, 97.5)),
               "excludes_0": bool(np.percentile(v, 2.5) > 0 or np.percentile(v, 97.5) < 0)}
        for name, v in dif_boots.items()}

    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

    s = results["A_cosines"]["summary"]
    print("A antonym/synonym cosines (en_core_web_md):")
    print(f"   antonyms: mean {s['antonym_mean']:.3f}, max {s['antonym_max']:.3f}, "
          f"in [0.6,0.8): {s['antonyms_in_0.6_0.8']}/10, >=0.8: {s['antonyms_ge_0.8']}/10")
    print("   " + ", ".join(f"{k}={v:.2f}" for k, v in results["A_cosines"]["antonyms"].items()))
    print(f"   near-synonyms: mean {s['synonym_mean']:.3f}, >=0.8: {s['synonyms_ge_0.8']}/10, "
          f"in [0.6,0.8): {s['synonyms_in_0.6_0.8']}/10")
    b = results["B_mc_noise"]
    print(f"B MC-null seed sensitivity (H_R soft AJ mean, tau=0.8): "
          f"seed42 {b['H_R_soft_aj_mean_seed42']:.4f} vs seed43 {b['H_R_soft_aj_mean_seed43']:.4f} "
          f"(|shift| {b['abs_shift']:.4f}; artifact {b['artifact_value_tau_0.80']:.4f})")
    print("C ladder (pooled hard AJ, cluster bootstrap):")
    for k, e in results["C_ladder"]["means"].items():
        print(f"   {k}: {e['point']:.3f} [{e['ci_lower']:.3f}, {e['ci_upper']:.3f}]")
    for name, e in results["C_ladder"]["differences"].items():
        print(f"   {name}: {e['point']:+.3f} [{e['ci_lower']:+.3f}, {e['ci_upper']:+.3f}] "
              f"{'separated' if e['excludes_0'] else 'NOT separated'}")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
