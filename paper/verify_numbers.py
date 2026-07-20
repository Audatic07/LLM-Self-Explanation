"""Verify every number in paper tables 1-5 (and headline prose values) against
the run-of-record artifacts. Exits nonzero on any mismatch.

Run from repo root:  python paper/verify_numbers.py
"""
import json
import math
import sys
from pathlib import Path

RUN = Path("outputs/20260718_041618_eaa24e67")
failures = []


def check(name, paper_value, artifact_value, tol=5e-4):
    ok = (
        abs(paper_value - artifact_value) <= tol
        if isinstance(paper_value, float)
        else paper_value == artifact_value
    )
    if not ok:
        failures.append(f"{name}: paper={paper_value} artifact={artifact_value}")
    return ok


nums = json.loads((RUN / "paper/numbers.json").read_text())
dis = json.loads((RUN / "disattenuated_agreement.json").read_text())
xm = json.loads((RUN / "cross_model_agreement.json").read_text())
er = json.loads((RUN / "aggregate_erasure.json").read_text())
sim = json.loads((RUN / "aggregate_simulatability.json").read_text())
agg = json.loads((RUN / "aggregate_metrics.json").read_text())

# ---------- Table 1: primary per-cell ----------
T1 = {  # (dataset, model): (N_cc, ecs_cc, N_avail, ecs_avail)
    ("sst2", "nova-pro"): (109, 0.414, 186, 0.426),
    ("sst2", "qwen3-235b"): (125, 0.449, 188, 0.443),
    ("sst2", "deepseek-v3"): (143, 0.617, 197, 0.618),
    ("mnli", "nova-pro"): (37, 0.284, 182, 0.475),
    ("mnli", "qwen3-235b"): (39, 0.431, 191, 0.508),
    ("mnli", "deepseek-v3"): (51, 0.441, 193, 0.501),
    ("ag_news", "nova-pro"): (30, 0.355, 190, 0.439),
    ("ag_news", "qwen3-235b"): (14, 0.427, 195, 0.489),
    ("ag_news", "deepseek-v3"): (80, 0.503, 194, 0.544),
    ("cad_imdb", "nova-pro"): (154, 0.301, 198, 0.287),
    ("cad_imdb", "qwen3-235b"): (178, 0.370, 199, 0.354),
    ("cad_imdb", "deepseek-v3"): (193, 0.465, 200, 0.459),
}
cells = {e["group_name"]: e for e in agg if e["aggregation_level"] == "model_dataset"}
for (ds, m), (n_cc, v_cc, n_av, v_av) in T1.items():
    cell = nums["per_cell"][f"{m}_{ds}"]
    check(f"T1 {m}/{ds} N_cc", n_cc, cell["n"])
    check(f"T1 {m}/{ds} ecs_cc", v_cc, cell["mean_ecs_adj_complete"])
    check(f"T1 {m}/{ds} p_holm", 0.0012, round(cell["p_holm_complete"], 4), tol=1e-9)
    a = cells[f"{m}_{ds}"]
    check(f"T1 {m}/{ds} N_avail", n_av, a["n_ecs_adj"])
    check(f"T1 {m}/{ds} ecs_avail", v_av, a["mean_ecs_adj"])
overall = nums["overall"]
check("T1 pooled cc", 0.432, overall["mean_ecs_adj_complete"])
check("T1 pooled cc N", 1153, overall["n_ecs_adj_complete"])
check("T1 pooled avail", 0.462, overall["mean_ecs_adj_available"])

# ---------- Table 2: pooled disattenuation ----------
T2 = {  # pair: (obs, rel_a, rel_b, corrected, ci_lo, ci_hi)
    "RO_CF": (0.653, 0.75, 0.62, 0.956, 0.909, 1.006),
    "H_CF": (0.555, 0.64, 0.62, 0.883, 0.830, 0.935),
    "H_R": (0.495, 0.64, 0.90, 0.654, 0.623, 0.684),
    "RO_R": (0.424, 0.75, 0.90, 0.516, 0.491, 0.539),
    "R_CF": (0.291, 0.90, 0.62, 0.391, 0.352, 0.429),
}
for pair, (obs, ra, rb, corr, lo, hi) in T2.items():
    p = dis["overall"]["pairs"][pair]
    check(f"T2 {pair} obs", obs, p["observed"])
    check(f"T2 {pair} rel_a", ra, p["rel_a"], tol=6e-3)
    check(f"T2 {pair} rel_b", rb, p["rel_b"], tol=6e-3)
    check(f"T2 {pair} corrected", corr, p["corrected"])
    check(f"T2 {pair} ci_lo", lo, p["ci_lower"])
    check(f"T2 {pair} ci_hi", hi, p["ci_upper"])

# ---------- Table 3: cross-model ----------
T3 = {
    "sst2": (0.622, 0.498, 0.129, 0.073, 0.190),
    "mnli": (0.596, 0.495, 0.046, 0.009, 0.087),
    "ag_news": (0.569, 0.491, 0.066, 0.035, 0.100),
    "cad_imdb": (0.585, 0.367, 0.218, 0.187, 0.248),
}
for ds, (cm, wm, d, lo, hi) in T3.items():
    e = xm[ds]
    check(f"T3 {ds} cross", cm, e["cross_model_same_strategy_mean_aj"])
    check(f"T3 {ds} within", wm, e["within_model_cross_strategy_mean_ecs_adj"])
    mc = e["paired_contrast_aj_matched"]
    check(f"T3 {ds} delta", d, mc["mean_delta"])
    check(f"T3 {ds} lo", lo, mc["ci_lower"])
    check(f"T3 {ds} hi", hi, mc["ci_upper"])

# ---------- Table 4: erasure ----------
T4 = {
    ("deepseek.v3-v1:0", "mask"): (0.316, 0.123, 0.192),
    ("deepseek.v3-v1:0", "delete"): (0.330, 0.125, 0.205),
    ("eu.amazon.nova-pro-v1:0", "mask"): (0.291, 0.147, 0.144),
    ("eu.amazon.nova-pro-v1:0", "delete"): (0.311, 0.132, 0.179),
    ("qwen.qwen3-235b-a22b-2507-v1:0", "mask"): (0.276, 0.104, 0.172),
    ("qwen.qwen3-235b-a22b-2507-v1:0", "delete"): (0.305, 0.112, 0.193),
}
ratios = []
for (m, op), (cc3, rnd, gap) in T4.items():
    o = er["per_model"][m]["overall"]
    check(f"T4 {m} {op} cc3", cc3, o["cc3_flip_rate"][op])
    check(f"T4 {m} {op} random", rnd, o["random_flip_rate"][op])
    check(f"T4 {m} {op} gap", gap, o["cc3_minus_random"][op])
    check(f"T4 {m} {op} p", 0.0002, round(o["cc3_vs_random_test"][op]["p_holm"], 4), tol=1e-9)
    ratios.append(o["cc3_flip_rate"][op] / o["random_flip_rate"][op])
# prose: ratio range 2.0-2.7x
assert 1.95 <= min(ratios) <= 2.05 and 2.65 <= max(ratios) <= 2.75, f"ratio range {min(ratios):.2f}-{max(ratios):.2f}"
# prose: tier gaps (pooled, delete + mask)
tiers = er["pooled"]["by_ecs_lift_tier"]
for tier, exp in [("low", 0.152), ("mid", 0.206), ("high", 0.213)]:
    check(f"tier {tier} delete gap", exp, tiers[tier]["gap_delete"])
check("heldout cf flip", 0.963, er["pooled"]["overall"]["cf_flip_heldout_rate"])

# ---------- Table 5: simulatability ----------
T5 = {
    "eu.amazon.nova-pro-v1:0": (0.877, -0.009, -0.002, -0.006, -0.001, -0.011, -0.155, 0.144),
    "qwen.qwen3-235b-a22b-2507-v1:0": (0.870, 0.005, 0.012, -0.069, 0.003, 0.006, -0.141, 0.172),
    "deepseek.v3-v1:0": (0.767, 0.016, 0.038, 0.020, 0.013, -0.015, -0.159, 0.146),
}
for m, (b, gh, gr, gcf, gro, rho, lo, hi) in T5.items():
    e = sim["per_model"][m]
    check(f"T5 {m} baseline", b, e["sim_acc"]["baseline"]["mean"])
    for s, g in [("H", gh), ("R", gr), ("CF", gcf), ("RO", gro)]:
        check(f"T5 {m} gain {s}", g, e["gain"][s]["mean"])
    check(f"T5 {m} rho", rho, e["c1_spearman"]["rho"])
    check(f"T5 {m} rho lo", lo, e["c1_spearman"]["ci_lower"])
    check(f"T5 {m} rho hi", hi, e["c1_spearman"]["ci_upper"])
    check(f"T5 {m} c1 holm", 1.0, e["c1_spearman"]["p_holm"], tol=1e-9)
p = sim["pooled"]
check("T5 pooled baseline", 0.838, p["sim_acc"]["baseline"]["mean"])
check("T5 pooled rho", -0.001, p["c1_spearman"]["rho"])
check("T5 pooled gain R", 0.016, p["gain"]["R"]["mean"])
check("T5 pooled gain CF", -0.015, p["gain"]["CF"]["mean"])
# red-flag precision bound (prose: <= 0.04)
prec = [sim["per_model"][m]["red_flag"]["precision"] for m in T5] + [p["red_flag"]["precision"]]
assert max(prec) <= 0.04, f"red-flag precision max {max(prec)}"

# ---------- headline prose ----------
check("components er (avail)", 0.438, overall["mean_ecs_adj_er"])
check("components ep (avail)", 0.606, overall["mean_ecs_adj_ep"])
check("components rp (avail)", 0.291, overall["mean_ecs_adj_rp"])
models = {e["group_name"]: e for e in agg if e["aggregation_level"] == "model"}
check("model pooled deepseek", 0.52, models["deepseek.v3-v1:0"]["mean_ecs_adj_complete"], tol=5e-3)
check("model pooled qwen", 0.41, models["qwen.qwen3-235b-a22b-2507-v1:0"]["mean_ecs_adj_complete"], tol=5e-3)
check("model pooled nova", 0.34, models["eu.amazon.nova-pro-v1:0"]["mean_ecs_adj_complete"], tol=5e-3)
dsets = {e["group_name"]: e for e in agg if e["aggregation_level"] == "dataset"}
check("dataset pooled cad", 0.38, dsets["cad_imdb"]["mean_ecs_adj_complete"], tol=6e-3)
ov = [e for e in agg if e["aggregation_level"] == "overall"][0]
check("free-CF cc", 0.382, ov["mean_ecs_adj_free_cf_complete"])
check("free-CF cc N", 1318, ov["n_ecs_adj_free_cf_complete"])
wn = json.loads((RUN / "weighted_null_sensitivity.json").read_text())
check("weighted null pooled", 0.421, wn["pooled"]["weighted_complete_mean"])
sm = json.loads((RUN / "soft_match_sensitivity.json").read_text())
# CAD-IMDb corrected extraction-CF pairs: 5 of 6 in [0.88, 1.06], exception ~0.55
ecf = []
for m in ("deepseek-v3", "nova-pro", "qwen3-235b"):
    for pr in ("H_CF", "RO_CF"):
        ecf.append(dis["per_cell"][f"{m}_cad_imdb"]["pairs"][pr]["corrected"])
inside = [v for v in ecf if 0.875 <= v <= 1.065]
assert len(inside) == 5 and min(ecf) < 0.56, f"CAD ext-CF pairs: {sorted(round(v,3) for v in ecf)}"
rcf_cad = [dis["per_cell"][f"{m}_cad_imdb"]["pairs"]["R_CF"]["corrected"] for m in ("deepseek-v3", "nova-pro", "qwen3-235b")]
assert 0.115 <= min(rcf_cad) and max(rcf_cad) <= 0.355, f"CAD R-CF {rcf_cad}"

# ---------- reviewer-round additions ----------
# Item 8: cross-model pairs not conditioned on matching predicted label
inst = [json.loads(l) for l in (RUN / "instance_results.jsonl").open(encoding="utf-8")]


def _sets(r):
    o = {}
    if r.get("highlighting_valid") and r.get("highlighting_tokens"):
        o["H"] = set(r["highlighting_tokens"])
    if r.get("rationale_valid") and r.get("rationale_tokens"):
        o["R"] = set(r["rationale_tokens"])
    if r.get("counterfactual_valid") and r.get("counterfactual_tokens"):
        o["CF"] = set(r["counterfactual_tokens"])
    if r.get("rank_ordering_valid"):
        ro = r.get("rank_ordering_set") or [t for t, _ in (r.get("rank_ordering_tokens") or [])]
        if ro:
            o["RO"] = set(ro)
    return o


from collections import defaultdict  # noqa: E402

by_inst = defaultdict(list)
for r in inst:
    by_inst[(r["dataset"], r["instance_id"])].append(r)
n_pairs = n_same = 0
for rs in by_inst.values():
    if len(rs) < 2:
        continue
    for s in ("H", "R", "CF", "RO"):
        have = [r for r in rs if s in _sets(r)]
        for i in range(len(have)):
            for j in range(i + 1, len(have)):
                n_pairs += 1
                n_same += have[i]["predicted_label"] == have[j]["predicted_label"]
check("item8 cross-model pairs", 8074, n_pairs)
check("item8 same-label pct", 93.9, round(100 * n_same / n_pairs, 1))

# Items 11/12: degeneracy by pair type, forced-overlap share, non-degenerate ladder
sys.path.insert(0, ".")
from src.metrics.metrics_calculator import MetricsCalculator  # noqa: E402

calc = MetricsCalculator()
PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
elic, degn = defaultdict(int), defaultdict(int)
forced = nondegen_total = 0
for r in inst:
    ss, V = _sets(r), int(r.get("vocab_size") or 0)
    for a, b in PAIRS:
        if a in ss and b in ss:
            key = f"{a}-{b}"
            elic[key] += 1
            _aj, is_deg = calc.adjusted_jaccard(ss[a], ss[b], V, 0.10)
            if is_deg:
                degn[key] += 1
            else:
                nondegen_total += 1
                if len(ss[a]) + len(ss[b]) > V:
                    forced += 1
for key, pct in [("H-R", 17.3), ("RO-R", 2.5), ("H-CF", 17.0), ("RO-CF", 4.8), ("R-CF", 13.7)]:
    check(f"item12 degen% {key}", pct, round(100 * degn[key] / elic[key], 1))
check("item11 forced-overlap share", 5.8, round(100 * forced / nondegen_total, 1))

cc_rows = [r for r in inst if r.get("ecs_adj_complete")]
nd_rows = [r for r in cc_rows if int(r.get("n_degenerate_pairs") or 0) == 0]
check("item12 nondegen cc N", 850, len(nd_rows))


def _mean(rows, field):
    v = [r[field] for r in rows if r.get(field) is not None]
    return sum(v) / len(v)


for comp, exp_all, exp_nd in [("ep", 0.615, 0.618), ("er", 0.395, 0.451), ("rp", 0.286, 0.313)]:
    check(f"item12 cc {comp}", exp_all, _mean(cc_rows, f"ecs_adj_{comp}"), tol=6e-4)
    check(f"item12 nondegen {comp}", exp_nd, _mean(nd_rows, f"ecs_adj_{comp}"), tol=6e-4)

# Item 13: correctness split (pooled + the two table extremes)
corr = [r["ecs_adj"] for r in cc_rows if r.get("correct")]
inc = [r["ecs_adj"] for r in cc_rows if not r.get("correct")]
check("item13 correct mean", 0.437, sum(corr) / len(corr), tol=6e-4)
check("item13 correct N", 1085, len(corr))
check("item13 incorrect mean", 0.360, sum(inc) / len(inc), tol=6e-4)
check("item13 incorrect N", 68, len(inc))

# Minor: overlap-coefficient composite preserves the paradigm ordering
o = {k: ov[f"mean_overlap_{k}"] for k in ("H_R", "R_RO", "H_CF", "CF_RO", "R_CF")}
ov_ep = (o["H_CF"] + o["CF_RO"]) / 2
ov_er = (o["H_R"] + o["R_RO"]) / 2
check("minor overlap E-P", 0.786, ov_ep)
check("minor overlap E-R", 0.689, ov_er)
check("minor overlap R-P", 0.526, o["R_CF"])
assert ov_ep > ov_er > o["R_CF"], "overlap composite must preserve paradigm ordering"

# ---------- review-round-2 additions ----------
# Item 2: degeneracy regimes. (a) small-V: J_max healthy but E[J] risen to meet it;
# (b) size imbalance: J_max itself < eps-scale. Split at J_max = 0.35.
regime = defaultdict(lambda: defaultdict(int))
vsz, jmax_deg, ej_deg = defaultdict(list), defaultdict(list), defaultdict(list)
for r in inst:
    ss, V = _sets(r), int(r.get("vocab_size") or 0)
    ds = r["dataset"]
    vsz[ds].append(V)
    for a, b in PAIRS:
        if a in ss and b in ss:
            sa, sb = len(ss[a]), len(ss[b])
            ej = calc.expected_jaccard_exact(sa, sb, V)
            jm = min(sa, sb) / max(sa, sb)
            if jm - ej < 0.10:
                regime[ds]["B" if jm < 0.35 else "A"] += 1
                jmax_deg[ds].append(jm)
                ej_deg[ds].append(ej)


def _med(v):
    return sorted(v)[len(v) // 2]


for ds, a_exp, b_exp in [("cad_imdb", 0, 398), ("ag_news", 0, 48),
                         ("mnli", 41, 248), ("sst2", 65, 148)]:
    check(f"item2 {ds} regimeA", a_exp, regime[ds]["A"])
    check(f"item2 {ds} regimeB", b_exp, regime[ds]["B"])
check("item2 cad median V", 68, _med(vsz["cad_imdb"]))
check("item2 mnli median V", 12, _med(vsz["mnli"]))
check("item2 sst2 median V", 10, _med(vsz["sst2"]))
check("item2 cad median jmax(degen)", 0.108, _med(jmax_deg["cad_imdb"]), tol=6e-4)
check("item2 sst2 mean E[J](degen)", 0.37,
      sum(ej_deg["sst2"]) / len(ej_deg["sst2"]), tol=6e-3)
check("item2 mnli mean E[J](degen)", 0.18,
      sum(ej_deg["mnli"]) / len(ej_deg["mnli"]), tol=6e-3)
assert sum(regime[d]["A"] + regime[d]["B"] for d in regime) == 948, "regime totals must sum to 948"
# CAD-IMDb median evidence-set sizes quoted in Appendix D
cad = [r for r in inst if r["dataset"] == "cad_imdb"]
cad_sz = defaultdict(list)
for r in cad:
    for s, st in _sets(r).items():
        cad_sz[s].append(len(st))
for s, exp in [("H", 30), ("CF", 11), ("R", 6)]:
    check(f"item2 cad median |{s}|", exp, _med(cad_sz[s]))

# Item 4: ceiling gate is parse-level, so low-validity cells still clear n>=10
qwen_ag = [r for r in inst if r["dataset"] == "ag_news"
           and r["model"] == "qwen.qwen3-235b-a22b-2507-v1:0"]
n_cf_valid = sum(1 for r in qwen_ag if r.get("counterfactual_valid"))
check("item4 qwen/ag CF validity %", 7.5, round(100 * n_cf_valid / len(qwen_ag), 1))
abl = json.loads(Path("outputs/20260716_195651/ablations/ablation_results.json").read_text())
check("item4 qwen/ag ceiling n", 13,
      abl["ag_news_prompt"]["CF_alt"]["self_consistency_aj_n"])
check("item4 qwen/ag rel_CF", 0.736,
      abl["ag_news_prompt"]["CF_alt"]["self_consistency_aj_mean"], tol=6e-4)

# Item 5: erasure set sizes and per-token flip densities
sz = defaultdict(list)
cc3_sizes = []
for r in inst:
    ss = _sets(r)
    cnt = defaultdict(int)
    for s, st in ss.items():
        sz[s].append(len(st))
        for t in st:
            cnt[t] += 1
    n_cc3 = sum(1 for t, c in cnt.items() if c >= 3)
    if n_cc3:
        cc3_sizes.append(n_cc3)
mean_cc3 = sum(cc3_sizes) / len(cc3_sizes)
check("item5 mean CC3 size", 3.1, mean_cc3, tol=0.05)
check("item5 mean |H|", 12.6, sum(sz["H"]) / len(sz["H"]), tol=0.05)
check("item5 mean |CF|", 6.2, sum(sz["CF"]) / len(sz["CF"]), tol=0.05)
pooled_er = er["pooled"]["overall"]
dens = {}
for op in ("mask", "delete"):
    dens[("CC3", op)] = pooled_er["cc3_flip_rate"][op] / mean_cc3
    dens[("rand", op)] = pooled_er["random_flip_rate"][op] / mean_cc3
    for s in ("H", "R", "CF", "RO"):
        dens[(s, op)] = pooled_er["strategy_flip_rate"][s][op] / (sum(sz[s]) / len(sz[s]))
for (k_, op), exp in [(("CC3", "mask"), 0.096), (("CC3", "delete"), 0.103),
                      (("CF", "mask"), 0.072), (("CF", "delete"), 0.079),
                      (("RO", "mask"), 0.072), (("RO", "delete"), 0.078),
                      (("R", "mask"), 0.057), (("R", "delete"), 0.061),
                      (("H", "mask"), 0.035), (("H", "delete"), 0.036),
                      (("rand", "mask"), 0.041), (("rand", "delete"), 0.040)]:
    check(f"item5 density {k_}/{op}", exp, dens[(k_, op)], tol=6e-4)
# the ordering claim: CC3 densest under both operators
for op in ("mask", "delete"):
    assert dens[("CC3", op)] > max(dens[(s, op)] for s in ("H", "R", "CF", "RO")), \
        f"CC3 must be densest under {op}"
    assert dens[("CC3", op)] / dens[("rand", op)] > 2.3, "CC3 vs random density ratio"

# Appendix D: E-R delta under the non-degenerate restriction
check("appD E-R delta", 0.056,
      _mean(nd_rows, "ecs_adj_er") - _mean(cc_rows, "ecs_adj_er"), tol=6e-4)

# §3.3 simulation numbers are asserted in tests/test_disattenuation_recovery.py
# (run: python -m pytest tests/test_disattenuation_recovery.py)

print(f"checks run; failures: {len(failures)}")
for f in failures:
    print("  MISMATCH:", f)
sys.exit(1 if failures else 0)
