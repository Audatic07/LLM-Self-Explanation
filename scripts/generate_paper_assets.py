#!/usr/bin/env python
r"""Generate every paper table, figure, and headline number from ONE frozen run dir.

    python scripts/generate_paper_assets.py outputs/<run> \
        [--erasure-dir outputs/<run>] [--ablation-dir outputs/<run>] \
        [--sim-json ECS_ADJ_SIMULATION_2026-07-06.json] [--out paper/]

Reads only committed artifacts (zero API cost) and writes:
    <out>/tables/*.tex     booktabs tables (T1–T10 where inputs exist)
    <out>/figures/*.{pdf,png}   figures F1–F8 (F4/F8 need the erasure/ablation dirs)
    <out>/numbers.json     every headline number, keyed, so the LaTeX text \input's
                           them and nothing is retyped.

Design: every asset is produced inside its own try/except — a missing erasure or
ablation directory (those passes run after the main run) downgrades to a skip with
a logged warning, never a crash. This mirrors PAPER_DATA_VIZ_PLAN_2026-07-07.md §B1.
"""
import argparse
import json
import logging
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.plots.visualization_generator import (
    VisualizationGenerator, STRATEGY_LABELS, PARADIGM_LABELS,
)
from src.metrics.metrics_calculator import MetricsCalculator

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("paper_assets")
# Silence matplotlib/fontTools PDF-subsetting chatter (they log at INFO).
for _noisy in ("matplotlib", "fontTools", "PIL"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)


def cell_label(group_name: str) -> str:
    """'nova-pro_ag_news' -> 'nova-pro/ag_news' (split on the model/dataset
    separator only, so multi-word dataset names keep their underscores)."""
    parts = group_name.split("_", 1)
    return "/".join(parts)

PAIRS = [("H", "R"), ("H", "CF"), ("H", "RO"), ("R", "CF"), ("R", "RO"), ("CF", "RO")]
TOKEN_FIELD = {"H": "highlighting_tokens", "R": "rationale_tokens",
               "CF": "counterfactual_tokens", "RO": "rank_ordering_set"}
TOKEN_FIELD_FALLBACK = {"RO": "rank_ordering_tokens"}


# --------------------------------------------------------------------------- #
#  Loading + shared helpers                                                    #
# --------------------------------------------------------------------------- #
def load_run(run_dir: Path):
    """Load the core artifacts a main run always produces."""
    art = {}
    with open(run_dir / "instance_results.jsonl", encoding="utf-8") as f:
        art["instances"] = [json.loads(line) for line in f if line.strip()]
    with open(run_dir / "aggregate_metrics.json", encoding="utf-8") as f:
        art["aggregate"] = json.load(f)
    cma = run_dir / "cross_model_agreement.json"
    art["cross_model"] = json.load(open(cma, encoding="utf-8")) if cma.exists() else {}
    # model_id -> short study name, from the config snapshot committed with the run.
    snap = run_dir / "config_snapshot.yaml"
    id2name = {}
    if snap.exists():
        cfg = yaml.safe_load(open(snap, encoding="utf-8"))
        for m in cfg.get("models", []):
            id2name[m.get("model_id", m.get("name"))] = m.get("name", m.get("model_id"))
    art["id2name"] = id2name
    return art


def instances_df(instances, id2name):
    df = pd.DataFrame(instances)
    df["model_name"] = df["model"].map(lambda mid: id2name.get(mid, mid))
    df["cell"] = df["model_name"] + "/" + df["dataset"]
    return df


def agg_index(aggregate):
    """{(level, group_name): row_dict}."""
    return {(e.get("aggregation_level"), e.get("group_name")): e for e in aggregate}


def _fmt(x, nd=3):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "--"
    return f"{x:.{nd}f}"


def write_booktabs(path: Path, caption: str, label: str, header, rows, align=None):
    ncol = len(header)
    align = align or ("l" + "r" * (ncol - 1))
    lines = [r"\begin{table}[t]", r"\centering", f"\\caption{{{caption}}}",
             f"\\label{{{label}}}", f"\\begin{{tabular}}{{{align}}}", r"\toprule",
             " & ".join(header) + r" \\", r"\midrule"]
    for row in rows:
        lines.append(" & ".join(str(c) for c in row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"  wrote table {path.name}")


def guard(name):
    """Decorator: log + skip an asset if its inputs are missing/malformed."""
    def deco(fn):
        def wrapped(*a, **k):
            try:
                fn(*a, **k)
            except FileNotFoundError as e:
                logger.warning(f"[skip] {name}: input missing ({e})")
            except Exception as e:
                logger.warning(f"[skip] {name}: {type(e).__name__}: {e}")
        return wrapped
    return deco


# --------------------------------------------------------------------------- #
#  Figures                                                                      #
# --------------------------------------------------------------------------- #
def ro_tokens(row):
    v = row.get("rank_ordering_set")
    if v:
        return set(v)
    return set(row.get("rank_ordering_tokens", []) or [])


def token_set(row, strat):
    if strat == "RO":
        return ro_tokens(row)
    return set(row.get(TOKEN_FIELD[strat], []) or [])


@guard("F1 pairwise heatmap")
def fig_F1(viz, df):
    calc = MetricsCalculator()
    cells = sorted(df["cell"].unique())
    # legacy Jaccard: mean of stored per-pair jaccard columns, per cell
    jac_rows = {}
    for a, b in PAIRS:
        col = f"jaccard_{a}_{b}"
        jac_rows[f"{a}_{b}"] = {c: df[df.cell == c][col].dropna().mean()
                                if col in df else np.nan for c in cells}
    jaccard_df = pd.DataFrame(jac_rows).T[cells]
    # adjusted-Jaccard paradigm components from stored ecs_adj_er/ep/rp, per cell
    aj_rows = {}
    for comp, col in [("er", "ecs_adj_er"), ("ep", "ecs_adj_ep"), ("rp", "ecs_adj_rp")]:
        aj_rows[comp] = {c: df[df.cell == c][col].dropna().mean()
                         if col in df else np.nan for c in cells}
    aj_df = pd.DataFrame(aj_rows).T[cells]
    viz.plot_pairwise_heatmap_by_cell(jaccard_df, aj_df)


@guard("F2 ecs-adj distributions")
def fig_F2(viz, df):
    sub = df[["dataset", "model_name", "ecs_adj", "ecs_adj_complete"]].rename(
        columns={"model_name": "model"})
    viz.plot_ecs_adj_distributions(sub)


@guard("F3 aj geometry stability")
def fig_F3(viz, sim_path: Path):
    d = json.load(open(sim_path, encoding="utf-8"))
    c1 = d["properties"]["c_geometry_stability"]["c1_ceiling_gate"]
    stds = {k: c1.get(k) for k in ("std_raw_j", "std_lift", "std_aj")}
    viz.plot_aj_geometry_stability(c1["rows"], stds=stds)


@guard("F4 erasure gap")
def fig_F4(viz, erasure_path: Path):
    agg = json.load(open(erasure_path, encoding="utf-8"))
    per_model = {}
    for mid, a in agg.get("per_model", {}).items():
        ov = a.get("overall", {})
        test = ov.get("cc3_vs_random_test", {})
        d = {}
        for op in ov.get("operators", []):
            d[op] = {
                "cc3": ov.get("cc3_flip_rate", {}).get(op),
                "random": ov.get("random_flip_rate", {}).get(op),
                "gap": ov.get("cc3_minus_random", {}).get(op),
                "err": None,
                "p_holm": test.get(op, {}).get("p_holm"),
            }
        per_model[mid] = d
    # optional tier panel from pooled by_ecs_lift_tier
    tier_rows = []
    pooled_tiers = agg.get("pooled", {}).get("by_ecs_lift_tier", {})
    for tier in ["low", "mid", "high"]:
        t = pooled_tiers.get(tier)
        if not t:
            continue
        for key, val in t.items():
            if key.startswith("gap_") and val is not None:
                tier_rows.append({"tier": tier, "operator": key[4:], "gap": val})
    viz.plot_erasure_gap(per_model, pd.DataFrame(tier_rows) if tier_rows else None)


@guard("F5 cf trade-off")
def fig_F5(viz, aidx):
    rows = []
    for (lvl, grp), e in aidx.items():
        if lvl != "model":
            continue
        for kind, vrate, mrate in [
            ("minimal", "cf_canonical_validity_rate", "mean_cf_canonical_minimality"),
            ("free", "cf_contrast_validity_rate", "mean_cf_contrast_minimality"),
        ]:
            v, m = e.get(vrate), e.get(mrate)
            if v is not None and m is not None:
                rows.append({"model": grp, "kind": kind, "validity": v, "edit_ratio": m})
    viz.plot_cf_tradeoff(pd.DataFrame(rows))


@guard("F6 cross-model contrast")
def fig_F6(viz, cross_model):
    rows = []
    for ds, e in cross_model.items():
        cm = e.get("cross_model_same_strategy_mean")
        wm = e.get("within_model_cross_strategy_mean_ecs")
        if cm is not None and wm is not None:
            rows.append({"dataset": ds, "delta": cm - wm})
    viz.plot_cross_model_contrast(pd.DataFrame(rows))


@guard("F7 confidence-ecs grid")
def fig_F7(viz, df, aidx):
    from scipy import stats
    sub = df[["dataset", "model_name", "confidence", "ecs_adj"]].rename(
        columns={"model_name": "model"})
    corr_by_cell = {}
    for (m, ds), g in sub.groupby(["model", "dataset"]):
        gg = g.dropna(subset=["confidence", "ecs_adj"])
        if len(gg) >= 3 and gg["confidence"].nunique() > 1 and gg["ecs_adj"].nunique() > 1:
            rho = stats.spearmanr(gg["confidence"], gg["ecs_adj"]).correlation
            tau = stats.kendalltau(gg["confidence"], gg["ecs_adj"], variant="b").correlation
            corr_by_cell[f"{m}_{ds}"] = SimpleNamespace(rho=float(rho), kendall_tau_b=float(tau))
    viz.plot_confidence_ecs_scatter_grid(sub, corr_by_cell)


@guard("F8 ablation robustness")
def fig_F8(viz, ablation_path: Path):
    d = json.load(open(ablation_path, encoding="utf-8"))
    # Preferred: a pre-flattened long frame (per_instance/rows with Variation + ECS_delta).
    rows = d.get("per_instance") or d.get("rows")
    if rows:
        df = pd.DataFrame(rows)
        value_col = "ECS_delta" if "ECS_delta" in df.columns else ("ECS" if "ECS" in df.columns else None)
        if value_col is None or "Variation" not in df.columns:
            raise ValueError("ablation frame lacks Variation/ECS_delta columns")
        viz.plot_robustness_analysis(df, value_col=value_col)
        return
    # Otherwise parse run_ablations.py's native schema: {dataset}_prompt ->
    # {strategy}_alt -> {deltas: [...]}. Pool datasets; x = strategy paraphrased,
    # y = per-instance ECS delta (baseline wording vs *_alt wording). Deltas
    # centred on 0 => the ECS metric is robust to the prompt rewording.
    long_rows = []
    for group, strategies in d.items():
        if not group.endswith("_prompt") or not isinstance(strategies, dict):
            continue
        for strat_key, payload in strategies.items():
            if not isinstance(payload, dict):
                continue
            strat = strat_key.replace("_alt", "")
            for delta in payload.get("deltas", []):
                if delta is not None:
                    long_rows.append({"Variation": strat, "ECS_delta": float(delta)})
    if not long_rows:
        raise ValueError("ablation JSON has no per-instance deltas to plot")
    viz.plot_robustness_analysis(pd.DataFrame(long_rows), value_col="ECS_delta")


# --------------------------------------------------------------------------- #
#  Tables + numbers                                                             #
# --------------------------------------------------------------------------- #
@guard("T2 coverage")
def table_T2(tdir, aidx):
    rows = []
    for (lvl, grp), e in sorted(aidx.items()):
        if lvl != "model_dataset":
            continue
        rows.append([cell_label(grp), e.get("n_instances", 0),
                     _fmt(e.get("highlighting_success_rate")),
                     _fmt(e.get("rationale_success_rate")),
                     _fmt(e.get("counterfactual_success_rate")),
                     _fmt(e.get("rank_ordering_success_rate")),
                     e.get("n_complete_cases", 0)])
    write_booktabs(tdir / "T2_coverage.tex",
                   "Per-strategy extraction success and complete-case counts, per model$\\times$dataset.",
                   "tab:coverage",
                   ["Cell", "N", "H", "R", "CF", "RO", "Complete"], rows)


@guard("T3 primary results")
def table_T3(tdir, aidx, min_n):
    rows = []
    for (lvl, grp), e in sorted(aidx.items()):
        if lvl != "model_dataset":
            continue
        n = e.get("n_ecs_adj_complete", 0)
        star = "*" if n < min_n else ""
        rows.append([cell_label(grp), f"{n}{star}",
                     _fmt(e.get("mean_ecs_adj_complete"), 4),
                     _fmt(e.get("ecs_adj_p_value"), 4),
                     _fmt(e.get("ecs_adj_p_holm"), 4),
                     _fmt(e.get("mean_ecs_adj"), 4),
                     _fmt(e.get("mean_ecs_complete"), 4),
                     _fmt(e.get("mean_ecs_lift"), 4)])
    write_booktabs(tdir / "T3_primary.tex",
                   ("Primary results: ECS-adj complete-case per cell with sign-flip $p$ "
                    "(raw + Holm). Available-component ECS-adj and the previously-defined "
                    "legacy ECS / ECS-lift shown for reference. * = below the $N{=}%d$ test floor."
                    % min_n),
                   "tab:primary",
                   ["Cell", "N", "ECS-adj (cc)", "$p$", "$p_{Holm}$",
                    "ECS-adj (avail)", "ECS (legacy)", "ECS-lift"], rows)


@guard("T4 paradigm components")
def table_T4(tdir, aidx):
    rows = []
    for (lvl, grp), e in sorted(aidx.items()):
        if lvl != "model_dataset":
            continue
        rows.append([cell_label(grp),
                     _fmt(e.get("mean_ecs_adj_er")), _fmt(e.get("mean_ecs_adj_ep")),
                     _fmt(e.get("mean_ecs_adj_rp"))])
    write_booktabs(tdir / "T4_paradigms.tex",
                   "Paradigm-component adjusted Jaccard: E--R, E--P, R--P per cell.",
                   "tab:paradigms",
                   ["Cell", "E--R", "E--P", "R--P"], rows)


@guard("T5 erasure")
def table_T5(tdir, erasure_path: Path):
    agg = json.load(open(erasure_path, encoding="utf-8"))
    rows = []
    for mid, a in sorted(agg.get("per_model", {}).items()):
        ov = a.get("overall", {})
        test = ov.get("cc3_vs_random_test", {})
        for op in ov.get("operators", []):
            rows.append([mid.split(".")[-1][:18], op,
                         _fmt(ov.get("cc3_flip_rate", {}).get(op)),
                         _fmt(ov.get("random_flip_rate", {}).get(op)),
                         _fmt(ov.get("cc3_minus_random", {}).get(op)),
                         _fmt(test.get(op, {}).get("p_holm"), 4)])
    write_booktabs(tdir / "T5_erasure.tex",
                   ("Consensus-core (CC3) erasure flip rate vs.\\ same-size random control, "
                    "per model per operator (family (b) sign-flip, Holm-corrected)."),
                   "tab:erasure",
                   ["Model", "Op", "CC3", "Random", "Gap", "$p_{Holm}$"], rows)


@guard("T6 cross-model")
def table_T6(tdir, cross_model):
    rows = []
    for ds, e in sorted(cross_model.items()):
        cm = e.get("cross_model_same_strategy_mean")
        wm = e.get("within_model_cross_strategy_mean_ecs")
        delta = (cm - wm) if (cm is not None and wm is not None) else None
        rows.append([ds, _fmt(cm), _fmt(wm), _fmt(delta),
                     e.get("n_instances_multi_model", 0)])
    write_booktabs(tdir / "T6_cross_model.tex",
                   ("Cross-model same-strategy agreement vs.\\ within-model cross-strategy "
                    "agreement, per dataset."),
                   "tab:crossmodel",
                   ["Dataset", "Cross-model", "Within-model", "$\\Delta$", "N"], rows)


@guard("T8 confidence")
def table_T8(tdir, aidx):
    rows = []
    for (lvl, grp), e in sorted(aidx.items()):
        if lvl != "model_dataset":
            continue
        rows.append([cell_label(grp),
                     _fmt(e.get("spearman_rho")),
                     _fmt(e.get("kendall_tau_b_confidence")),
                     _fmt(e.get("spearman_p_value"), 4),
                     e.get("n_confidence", 0)])
    write_booktabs(tdir / "T8_confidence.tex",
                   "Confidence$\\leftrightarrow$ECS association (Spearman $\\rho$, Kendall $\\tau_b$), per cell.",
                   "tab:confidence",
                   ["Cell", "$\\rho$", "$\\tau_b$", "$p$", "N"], rows)


def write_numbers(out: Path, aidx, cross_model, erasure_path):
    nums = {}
    overall = aidx.get(("overall", "overall")) or aidx.get(("overall", "all"))
    if overall is None:
        overall = next((e for (l, g), e in aidx.items() if l == "overall"), {})
    nums["overall"] = {
        "n_instances": overall.get("n_instances"),
        "mean_ecs_adj_complete": overall.get("mean_ecs_adj_complete"),
        "n_ecs_adj_complete": overall.get("n_ecs_adj_complete"),
        "mean_ecs_adj_available": overall.get("mean_ecs_adj"),
        "ecs_adj_p_value": overall.get("ecs_adj_p_value"),
        "ecs_adj_p_holm": overall.get("ecs_adj_p_holm"),
        "mean_ecs_adj_er": overall.get("mean_ecs_adj_er"),
        "mean_ecs_adj_ep": overall.get("mean_ecs_adj_ep"),
        "mean_ecs_adj_rp": overall.get("mean_ecs_adj_rp"),
        "legacy_mean_ecs_complete": overall.get("mean_ecs_complete"),
        "legacy_mean_ecs_lift": overall.get("mean_ecs_lift"),
    }
    nums["per_cell"] = {
        g: {"mean_ecs_adj_complete": e.get("mean_ecs_adj_complete"),
            "n": e.get("n_ecs_adj_complete"),
            "p_holm": e.get("ecs_adj_p_holm")}
        for (l, g), e in aidx.items() if l == "model_dataset"
    }
    nums["cross_model_delta"] = {
        ds: (e.get("cross_model_same_strategy_mean", 0) - e.get("within_model_cross_strategy_mean_ecs", 0))
        for ds, e in cross_model.items()
        if e.get("cross_model_same_strategy_mean") is not None
        and e.get("within_model_cross_strategy_mean_ecs") is not None
    }
    if erasure_path and Path(erasure_path).exists():
        agg = json.load(open(erasure_path, encoding="utf-8"))
        nums["erasure"] = {
            mid: {"cc3_minus_random": a.get("overall", {}).get("cc3_minus_random"),
                  "cc3_vs_random_test": a.get("overall", {}).get("cc3_vs_random_test")}
            for mid, a in agg.get("per_model", {}).items()
        }
    (out / "numbers.json").write_text(json.dumps(nums, indent=2), encoding="utf-8")
    logger.info(f"  wrote numbers.json ({len(nums)} sections)")


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", help="Frozen main-run output directory")
    ap.add_argument("--erasure-dir", help="Dir with aggregate_erasure.json (default: run_dir)")
    ap.add_argument("--ablation-dir", help="Dir with ablation_results.json (default: run_dir)")
    ap.add_argument("--sim-json", default="ECS_ADJ_SIMULATION_2026-07-06.json",
                    help="ECS-adj simulation JSON for figure F3")
    ap.add_argument("--out", default="paper", help="Output root (tables/, figures/, numbers.json)")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    erasure_dir = Path(args.erasure_dir) if args.erasure_dir else run_dir
    ablation_dir = Path(args.ablation_dir) if args.ablation_dir else run_dir
    out = Path(args.out)
    tdir, fdir = out / "tables", out / "figures"
    tdir.mkdir(parents=True, exist_ok=True)
    fdir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Loading run: {run_dir}")
    art = load_run(run_dir)
    df = instances_df(art["instances"], art["id2name"])
    aidx = agg_index(art["aggregate"])
    cross_model = art["cross_model"]

    # config knobs from snapshot (dpi, min_n) with safe defaults
    snap = run_dir / "config_snapshot.yaml"
    cfg = yaml.safe_load(open(snap, encoding="utf-8")) if snap.exists() else {}
    dpi = (cfg.get("output", {}) or {}).get("figure_dpi", 300)
    min_n = (cfg.get("metrics", {}) or {}).get("min_n_for_test", 6)

    viz = VisualizationGenerator(fdir, dpi=dpi)
    erasure_path = erasure_dir / "aggregate_erasure.json"
    ablation_path = ablation_dir / "ablation_results.json"
    sim_path = Path(args.sim_json)

    logger.info("Figures:")
    fig_F1(viz, df)
    fig_F2(viz, df)
    fig_F3(viz, sim_path)
    fig_F4(viz, erasure_path)
    fig_F5(viz, aidx)
    fig_F6(viz, cross_model)
    fig_F7(viz, df, aidx)
    fig_F8(viz, ablation_path)

    logger.info("Tables:")
    table_T2(tdir, aidx)
    table_T3(tdir, aidx, min_n)
    table_T4(tdir, aidx)
    table_T5(tdir, erasure_path)
    table_T6(tdir, cross_model)
    table_T8(tdir, aidx)

    logger.info("Numbers:")
    write_numbers(out, aidx, cross_model, erasure_path)

    logger.info(f"Done. Assets under {out}/  (tables/, figures/, numbers.json)")


if __name__ == "__main__":
    main()
