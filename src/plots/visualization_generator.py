"""Figure generation for the LLM explanation-agreement study.

Two layers live here:

* The original generic helpers (``plot_agreement_heatmap``, ``plot_ecs_distributions``,
  ``plot_confidence_ecs_scatter``, ``plot_flip_rate_comparison``, ``plot_robustness_analysis``)
  — kept verbatim; ``tests/test_visualization.py`` pins their signatures.
* The paper figures F1–F8 (``plot_*_by_cell`` / ``plot_ecs_adj_*`` / ``plot_erasure_gap`` / …),
  added per ``PAPER_DATA_VIZ_PLAN_2026-07-07.md`` §B2. Each accepts an already-shaped
  DataFrame/dict so it is unit-testable on synthetic data; all artifact I/O lives in
  ``scripts/generate_paper_assets.py``.

Every figure is written as both PDF (vector, for LaTeX) and PNG via ``_save``.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from src.statistics.statistical_tests import CorrelationResult

# Study-wide display constants (single source of truth for labels/colours).
STRATEGY_LABELS = {"H": "Highlighting", "R": "Rationale",
                   "CF": "Counterfactual", "RO": "Rank-ordering"}
PARADIGM_LABELS = {"er": "E–R\n(extract–rationalize)",
                   "ep": "E–P\n(extract–perturb)",
                   "rp": "R–P\n(rationalize–perturb)"}
PAIR_ORDER = ["H_R", "H_CF", "H_RO", "R_CF", "R_RO", "CF_RO"]


class VisualizationGenerator:
    def __init__(self, output_dir, dpi=72):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.figure_dpi = dpi
        self._setup_style()

    def _setup_style(self):
        """Colourblind-safe palette + >=10pt fonts, applied globally (plan §B2).

        Only touches rcParams/palette — existing figures are unaffected in content,
        so the pinned visualization tests still pass."""
        try:
            sns.set_theme(style="whitegrid", palette="colorblind")
        except Exception:
            pass
        plt.rcParams.update({
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "figure.dpi": self.figure_dpi,
            "savefig.dpi": self.figure_dpi,
            "pdf.fonttype": 42,   # TrueType — editable text in the vector PDF
            "ps.fonttype": 42,
        })

    def _save(self, fig, filename):
        filepath_pdf = self.output_dir / f"{filename}.pdf"
        filepath_png = self.output_dir / f"{filename}.png"
        fig.savefig(filepath_pdf, dpi=self.figure_dpi, bbox_inches="tight")
        fig.savefig(filepath_png, dpi=self.figure_dpi, bbox_inches="tight")
        plt.close(fig)

    # ------------------------------------------------------------------ #
    #  Original generic helpers (signatures pinned by tests — do not edit) #
    # ------------------------------------------------------------------ #
    def plot_agreement_heatmap(self, data: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(data, annot=True, fmt=".3f", cmap="YlOrRd", vmin=0, vmax=1, ax=ax)
        ax.set_title("Mean Pairwise Jaccard Similarity")
        self._save(fig, "agreement_heatmap")

    def plot_ecs_distributions(self, ecs_by_dataset: Dict[str, List[float]],
                                ecs_by_model: Dict[str, List[float]]):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        for idx, (data, title) in enumerate([
            (ecs_by_dataset, "ECS by Dataset"),
            (ecs_by_model, "ECS by Model")
        ]):
            rows = []
            for group, values in data.items():
                for v in values:
                    rows.append({"Group": group, "ECS": v})
            df = pd.DataFrame(rows)
            if not df.empty:
                sns.boxplot(data=df, x="Group", y="ECS", ax=axes[idx])
                sns.stripplot(data=df, x="Group", y="ECS", color="black", alpha=0.3, size=3, ax=axes[idx])
            axes[idx].set_title(title)
        plt.tight_layout()
        self._save(fig, "ecs_distributions")

    def plot_confidence_ecs_scatter(self, confidences: List[float], ecs_values: List[float],
                                     correlation: CorrelationResult):
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(confidences, ecs_values, alpha=0.5)
        ax.set_xlabel("Confidence")
        ax.set_ylabel("ECS")
        ax.set_title(f"Confidence vs ECS (rho={correlation.rho:.3f}, p={correlation.p_value:.4f})")
        self._save(fig, "confidence_ecs_scatter")

    def plot_flip_rate_comparison(self, cc_rates: Dict[str, float], random_rates: Dict[str, float]):
        fig, ax = plt.subplots(figsize=(6, 5))
        categories = list(cc_rates.keys())
        cc_values = [cc_rates[k] for k in categories]
        random_values = [random_rates.get(k, 0) for k in categories]
        x = range(len(categories))
        width = 0.35
        ax.bar([i - width / 2 for i in x], cc_values, width, label="CC", color="#e74c3c", alpha=0.8)
        ax.bar([i + width / 2 for i in x], random_values, width, label="Random", color="#3498db", alpha=0.8)
        ax.set_ylabel("Flip Rate")
        ax.set_title("Prediction Flip Rates After Token Removal")
        ax.set_xticks(list(x))
        ax.set_xticklabels(categories)
        ax.legend()
        self._save(fig, "flip_rate_comparison")

    def plot_robustness_analysis(self, data: pd.DataFrame, value_col: str = "ECS"):
        fig, ax = plt.subplots(figsize=(8, 5))
        if not data.empty:
            sns.boxplot(data=data, x="Variation", y=value_col, ax=ax)
            sns.stripplot(data=data, x="Variation", y=value_col, color="black", alpha=0.3, size=3, ax=ax)
        ax.set_title("Robustness Analysis")
        self._save(fig, "robustness_analysis")

    # ------------------------------------------------------------------ #
    #  Paper figures F1–F8                                                #
    # ------------------------------------------------------------------ #
    def plot_pairwise_heatmap_by_cell(self, jaccard_df: pd.DataFrame,
                                      aj_df: pd.DataFrame, filename: str = "F1_pairwise_heatmap"):
        """F1 — two heatmaps side by side: adjusted-Jaccard paradigm components
        (primary) and legacy pairwise Jaccard (as previously defined), each over
        the model×dataset cells.

        ``aj_df``: rows = paradigm component (er/ep/rp), cols = cell label.
        ``jaccard_df``: rows = strategy pair (H_R … CF_RO), cols = cell label."""
        fig, axes = plt.subplots(1, 2, figsize=(max(10, 1.1 * jaccard_df.shape[1]), 6),
                                 gridspec_kw={"width_ratios": [1, 1]})
        aj_plot = aj_df.rename(index={k: v.replace("\n", " ") for k, v in PARADIGM_LABELS.items()})
        sns.heatmap(aj_plot, annot=True, fmt=".2f", cmap="viridis", vmin=0, vmax=1,
                    cbar_kws={"label": "Adjusted Jaccard"}, ax=axes[0])
        axes[0].set_title("(a) ECS-adj components — PRIMARY")
        axes[0].set_xlabel("")
        jac_plot = jaccard_df.rename(index=lambda p: p.replace("_", "–"))
        sns.heatmap(jac_plot, annot=True, fmt=".2f", cmap="viridis", vmin=0, vmax=1,
                    cbar_kws={"label": "Jaccard"}, ax=axes[1])
        axes[1].set_title("(b) Pairwise Jaccard — as previously defined")
        axes[1].set_xlabel("")
        plt.tight_layout()
        self._save(fig, filename)

    def plot_ecs_adj_distributions(self, df: pd.DataFrame, filename: str = "F2_ecs_adj_distributions"):
        """F2 — ECS-adj distributions faceted dataset (col) × model (row).

        ``df`` columns: ``dataset``, ``model``, ``ecs_adj`` (available-component),
        ``ecs_adj_complete`` (bool). Complete-case points are drawn dark; the
        available-component-only rows are drawn in a lighter shade behind them."""
        if df.empty:
            fig, ax = plt.subplots(figsize=(6, 4)); ax.set_title("ECS-adj (no data)")
            self._save(fig, filename); return
        datasets = sorted(df["dataset"].unique())
        models = sorted(df["model"].unique())
        fig, axes = plt.subplots(len(models), len(datasets),
                                 figsize=(3.2 * len(datasets), 2.6 * len(models)),
                                 squeeze=False, sharey=True)
        for i, m in enumerate(models):
            for j, ds in enumerate(datasets):
                ax = axes[i][j]
                cell = df[(df["model"] == m) & (df["dataset"] == ds)].dropna(subset=["ecs_adj"])
                if not cell.empty:
                    sns.violinplot(y=cell["ecs_adj"], color="#cfd8e3", cut=0,
                                   inner=None, ax=ax)
                    comp = cell[cell["ecs_adj_complete"] == True]
                    avail = cell[cell["ecs_adj_complete"] != True]
                    ax.scatter(np.random.uniform(-0.08, 0.08, len(avail)), avail["ecs_adj"],
                               s=10, color="#9aa7b8", alpha=0.5, label="available-comp.")
                    ax.scatter(np.random.uniform(-0.08, 0.08, len(comp)), comp["ecs_adj"],
                               s=14, color="#1f3a5f", alpha=0.8, label="complete-case")
                    ax.axhline(cell["ecs_adj"].mean(), color="#e4572e", lw=1.2, ls="--")
                ax.set_ylim(-0.05, 1.05)
                if i == 0:
                    ax.set_title(ds)
                ax.set_ylabel(m if j == 0 else "")
                ax.set_xlabel(""); ax.set_xticks([])
        fig.suptitle("ECS-adj by model × dataset (dashed = cell mean)", y=1.01)
        plt.tight_layout()
        self._save(fig, filename)

    def plot_aj_geometry_stability(self, rows: List[Dict], stds: Optional[Dict] = None,
                                   filename: str = "F3_aj_geometry_stability"):
        """F3 — the justification figure: at a FIXED planted agreement (the smaller
        set fully nested, k = min(a,b)), sweep the set-size geometry and show that
        adjusted Jaccard stays pinned at the ceiling while raw Jaccard and raw
        lift swing widely (plan property (c); source: ECS_ADJ_SIMULATION rows).

        ``rows``: list of ``{a, b, k, raw_j, lift, aj}``. ``stds`` (optional):
        ``{std_raw_j, std_lift, std_aj}`` for the annotation."""
        if not rows:
            fig, ax = plt.subplots(figsize=(6, 4)); ax.set_title("AJ geometry stability (no data)")
            self._save(fig, filename); return
        rows = sorted(rows, key=lambda r: (r.get("b", 0), r.get("a", 0)))
        x = list(range(len(rows)))
        xlabels = [f"{r['a']}:{r['b']}" for r in rows]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, [r["aj"] for r in rows], marker="o", lw=2, color="#1f3a5f",
                label="Adjusted Jaccard (ECS-adj)")
        ax.plot(x, [r["raw_j"] for r in rows], marker="s", ls="--", color="#e4572e",
                alpha=0.85, label="raw Jaccard")
        ax.plot(x, [r["lift"] for r in rows], marker="^", ls=":", color="#3a7d44",
                alpha=0.85, label="raw Jaccard-lift")
        ax.set_xticks(x); ax.set_xticklabels(xlabels, rotation=45, ha="right")
        ax.set_xlabel("Set-size geometry  (|smaller| : |larger|)")
        ax.set_ylabel("Agreement score at fixed (maximal) planted overlap")
        title = "Why ECS-adj replaces the flat mean:\nAJ is geometry-stable; raw Jaccard / lift are not"
        if stds:
            title += (f"\nσ: AJ={stds.get('std_aj',0):.3f}  "
                      f"rawJ={stds.get('std_raw_j',0):.3f}  lift={stds.get('std_lift',0):.3f}")
        ax.set_title(title)
        ax.legend(fontsize=9)
        plt.tight_layout()
        self._save(fig, filename)

    def plot_erasure_gap(self, per_model: Dict[str, Dict], tier_rows: Optional[pd.DataFrame] = None,
                         filename: str = "F4_erasure_gap"):
        """F4 — CC3-vs-random flip gap per model, grouped by operator (mask/delete).

        ``per_model``: ``{model: {op: {"cc3": r, "random": r, "gap": g,
        "err": half_ci_or_None, "p_holm": p}}}``. Optional second panel: gap by
        ECS-lift tier (labelled descriptive) via ``tier_rows`` with columns
        ``tier``, ``operator``, ``gap``."""
        two = tier_rows is not None and not tier_rows.empty
        fig, axes = plt.subplots(1, 2 if two else 1, figsize=(12 if two else 7, 5), squeeze=False)
        ax = axes[0][0]
        models = list(per_model.keys())
        operators = sorted({op for m in per_model.values() for op in m})
        palette = sns.color_palette("colorblind", n_colors=max(2, len(operators)))
        width = 0.8 / max(1, len(operators))
        x = np.arange(len(models))
        for oi, op in enumerate(operators):
            gaps = [per_model[m].get(op, {}).get("gap") or 0.0 for m in models]
            errs = [per_model[m].get(op, {}).get("err") or 0.0 for m in models]
            bars = ax.bar(x + oi * width, gaps, width, yerr=errs, capsize=3,
                          color=palette[oi], alpha=0.85, label=f"{op}")
            for xi, m in zip(x, models):
                p = per_model[m].get(op, {}).get("p_holm")
                if p is not None and p < 0.05:
                    g = per_model[m].get(op, {}).get("gap") or 0.0
                    ax.text(xi + oi * width, g + (errs[list(models).index(m)] or 0) + 0.01,
                            "*", ha="center", va="bottom", fontsize=13)
        ax.axhline(0, color="black", lw=0.8)
        ax.set_xticks(x + width * (len(operators) - 1) / 2)
        ax.set_xticklabels(models, rotation=15, ha="right")
        ax.set_ylabel("CC3 flip rate − random control")
        ax.set_title("(a) Consensus-core erasure gap (per model)\n* = Holm p<0.05")
        ax.legend(title="operator")
        if two:
            ax2 = axes[0][1]
            sns.barplot(data=tier_rows, x="tier", y="gap", hue="operator",
                        order=["low", "mid", "high"], ax=ax2)
            ax2.axhline(0, color="black", lw=0.8)
            ax2.set_title("(b) Gap by ECS-lift tier (descriptive)")
            ax2.set_ylabel("CC3 − random")
        plt.tight_layout()
        self._save(fig, filename)

    def plot_cf_tradeoff(self, rows: pd.DataFrame, filename: str = "F5_cf_tradeoff"):
        """F5 — CF validity vs edit ratio, minimal vs free, one marker per model.

        ``rows`` columns: ``model``, ``kind`` ('minimal'|'free'), ``validity``,
        ``edit_ratio``. Replication picture for arXiv:2509.09396."""
        if rows.empty:
            fig, ax = plt.subplots(figsize=(6, 5)); ax.set_title("CF trade-off (no data)")
            self._save(fig, filename); return
        fig, ax = plt.subplots(figsize=(7, 5))
        models = sorted(rows["model"].unique())
        palette = dict(zip(models, sns.color_palette("colorblind", n_colors=len(models))))
        markers = {"minimal": "o", "free": "s"}
        for _, r in rows.iterrows():
            ax.scatter(r["edit_ratio"], r["validity"], s=90,
                       marker=markers.get(r["kind"], "o"),
                       color=palette[r["model"]], edgecolor="black", linewidth=0.5)
        # connect minimal→free per model
        for m in models:
            sub = rows[rows["model"] == m].set_index("kind")
            if {"minimal", "free"}.issubset(sub.index):
                ax.plot([sub.loc["minimal", "edit_ratio"], sub.loc["free", "edit_ratio"]],
                        [sub.loc["minimal", "validity"], sub.loc["free", "validity"]],
                        color=palette[m], alpha=0.4, lw=1)
        model_handles = [plt.Line2D([], [], marker="o", ls="", color=palette[m], label=m) for m in models]
        kind_handles = [plt.Line2D([], [], marker=markers[k], ls="", color="gray", label=k)
                        for k in ["minimal", "free"]]
        ax.legend(handles=model_handles + kind_handles, fontsize=8, ncol=2)
        ax.set_xlabel("Mean edit ratio (fraction of tokens changed)")
        ax.set_ylabel("CF validity rate (verified label flip)")
        ax.set_title("Counterfactual validity–minimality trade-off")
        plt.tight_layout()
        self._save(fig, filename)

    def plot_cross_model_contrast(self, rows: pd.DataFrame, filename: str = "F6_cross_model_contrast"):
        """F6 — forest plot of the paired Δ (cross-model same-strategy − within-model
        cross-strategy) per dataset, with 95% CI and a vertical zero line.

        ``rows`` columns: ``dataset``, ``delta``, ``ci_lower``, ``ci_upper``
        (CI columns optional → drawn as points only)."""
        if rows.empty:
            fig, ax = plt.subplots(figsize=(6, 4)); ax.set_title("Cross-model Δ (no data)")
            self._save(fig, filename); return
        fig, ax = plt.subplots(figsize=(7, max(3, 0.9 * len(rows) + 2)))
        y = np.arange(len(rows))
        deltas = rows["delta"].values
        has_ci = {"ci_lower", "ci_upper"}.issubset(rows.columns)
        if has_ci:
            xerr = np.vstack([deltas - rows["ci_lower"].values, rows["ci_upper"].values - deltas])
            ax.errorbar(deltas, y, xerr=np.abs(xerr), fmt="o", color="#1f3a5f",
                        capsize=4, markersize=8)
        else:
            ax.scatter(deltas, y, color="#1f3a5f", s=80)
        ax.axvline(0, color="#e4572e", ls="--", lw=1.2)
        ax.set_yticks(y); ax.set_yticklabels(rows["dataset"].values)
        ax.set_xlabel("Δ = cross-model same-strategy − within-model cross-strategy agreement")
        ax.set_title("Same explanation type across models agrees more\nthan different types within a model?")
        ax.invert_yaxis()
        plt.tight_layout()
        self._save(fig, filename)

    def plot_confidence_ecs_scatter_grid(self, df: pd.DataFrame, corr_by_cell: Dict[str, CorrelationResult],
                                         filename: str = "F7_confidence_ecs_grid"):
        """F7 — confidence vs ECS-adj scatter, one panel per model×dataset cell,
        with ρ / τ-b annotated.

        ``df`` columns: ``dataset``, ``model``, ``confidence``, ``ecs_adj``.
        ``corr_by_cell`` keyed by ``f"{model}_{dataset}"``."""
        if df.empty:
            fig, ax = plt.subplots(figsize=(6, 4)); ax.set_title("Confidence↔ECS (no data)")
            self._save(fig, filename); return
        datasets = sorted(df["dataset"].unique())
        models = sorted(df["model"].unique())
        fig, axes = plt.subplots(len(models), len(datasets),
                                 figsize=(3.2 * len(datasets), 2.8 * len(models)),
                                 squeeze=False, sharex=True, sharey=True)
        for i, m in enumerate(models):
            for j, ds in enumerate(datasets):
                ax = axes[i][j]
                cell = df[(df["model"] == m) & (df["dataset"] == ds)].dropna(subset=["confidence", "ecs_adj"])
                ax.scatter(cell["confidence"], cell["ecs_adj"], alpha=0.5, s=14, color="#1f3a5f")
                cr = corr_by_cell.get(f"{m}_{ds}")
                if cr is not None:
                    tau = getattr(cr, "kendall_tau_b", None)
                    txt = f"ρ={cr.rho:.2f}"
                    if tau is not None:
                        txt += f"\nτb={tau:.2f}"
                    ax.text(0.05, 0.92, txt, transform=ax.transAxes, va="top", fontsize=8,
                            bbox=dict(boxstyle="round", fc="white", alpha=0.7))
                if i == 0:
                    ax.set_title(ds)
                ax.set_ylabel(m if j == 0 else "")
                ax.set_xlabel("confidence" if i == len(models) - 1 else "")
                ax.set_ylim(-0.05, 1.05)
        fig.suptitle("Verbalized confidence vs ECS-adj", y=1.01)
        plt.tight_layout()
        self._save(fig, filename)
