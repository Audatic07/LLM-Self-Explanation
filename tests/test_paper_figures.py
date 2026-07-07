"""Smoke tests for the paper figures F1–F8 (PAPER_DATA_VIZ_PLAN §B2).

One test per new VisualizationGenerator method: build a synthetic frame in the
shape generate_paper_assets.py passes, call the method, assert both the PDF and
PNG exist and are non-trivial. No pixel assertions — mirrors test_visualization.py.
"""
import numpy as np
import pandas as pd
import pytest
from types import SimpleNamespace

from src.plots.visualization_generator import VisualizationGenerator


@pytest.fixture
def viz(tmp_path):
    return VisualizationGenerator(tmp_path, dpi=72)


def _nonempty(tmp_path, stem):
    for ext in ("pdf", "png"):
        p = tmp_path / f"{stem}.{ext}"
        assert p.exists(), f"{p} missing"
        assert p.stat().st_size > 500, f"{p} looks empty"


def test_F1_pairwise_heatmap(viz, tmp_path):
    cells = ["nova-pro/sst2", "qwen3-235b/mnli"]
    jaccard_df = pd.DataFrame(
        np.random.rand(6, 2),
        index=["H_R", "H_CF", "H_RO", "R_CF", "R_RO", "CF_RO"], columns=cells)
    aj_df = pd.DataFrame(np.random.rand(3, 2), index=["er", "ep", "rp"], columns=cells)
    viz.plot_pairwise_heatmap_by_cell(jaccard_df, aj_df)
    _nonempty(tmp_path, "F1_pairwise_heatmap")


def test_F2_ecs_adj_distributions(viz, tmp_path):
    rows = []
    for ds in ["sst2", "mnli"]:
        for m in ["nova-pro", "qwen3-235b"]:
            for i in range(8):
                rows.append({"dataset": ds, "model": m, "ecs_adj": np.random.rand(),
                             "ecs_adj_complete": bool(i % 2)})
    viz.plot_ecs_adj_distributions(pd.DataFrame(rows))
    _nonempty(tmp_path, "F2_ecs_adj_distributions")


def test_F2_empty(viz, tmp_path):
    viz.plot_ecs_adj_distributions(pd.DataFrame())
    _nonempty(tmp_path, "F2_ecs_adj_distributions")


def test_F3_aj_geometry_stability(viz, tmp_path):
    rows = [{"a": 2, "b": b, "k": 2, "raw_j": 2 / b, "lift": 2 / b - 0.1, "aj": 1.0}
            for b in (2, 4, 6, 8, 10)]
    viz.plot_aj_geometry_stability(rows, stds={"std_raw_j": 0.3, "std_lift": 0.3, "std_aj": 0.0})
    _nonempty(tmp_path, "F3_aj_geometry_stability")


def test_F4_erasure_gap(viz, tmp_path):
    per_model = {
        "amazon.nova-pro": {"mask": {"cc3": 0.6, "random": 0.3, "gap": 0.3, "err": 0.08, "p_holm": 0.01},
                            "delete": {"cc3": 0.5, "random": 0.35, "gap": 0.15, "err": 0.1, "p_holm": 0.2}},
        "deepseek.v3": {"mask": {"cc3": 0.55, "random": 0.4, "gap": 0.15, "err": 0.09, "p_holm": 0.3},
                        "delete": {"cc3": 0.45, "random": 0.4, "gap": 0.05, "err": 0.1, "p_holm": 0.7}},
    }
    tiers = pd.DataFrame([{"tier": t, "operator": op, "gap": np.random.rand() * 0.3}
                          for t in ("low", "mid", "high") for op in ("mask", "delete")])
    viz.plot_erasure_gap(per_model, tiers)
    _nonempty(tmp_path, "F4_erasure_gap")


def test_F5_cf_tradeoff(viz, tmp_path):
    rows = pd.DataFrame([
        {"model": "nova-pro", "kind": "minimal", "validity": 0.8, "edit_ratio": 0.15},
        {"model": "nova-pro", "kind": "free", "validity": 0.9, "edit_ratio": 0.4},
        {"model": "deepseek-v3", "kind": "minimal", "validity": 0.7, "edit_ratio": 0.2},
        {"model": "deepseek-v3", "kind": "free", "validity": 0.85, "edit_ratio": 0.5},
    ])
    viz.plot_cf_tradeoff(rows)
    _nonempty(tmp_path, "F5_cf_tradeoff")


def test_F6_cross_model_contrast(viz, tmp_path):
    rows = pd.DataFrame([
        {"dataset": "sst2", "delta": 0.24, "ci_lower": 0.1, "ci_upper": 0.38},
        {"dataset": "mnli", "delta": 0.12, "ci_lower": -0.02, "ci_upper": 0.26},
        {"dataset": "ag_news", "delta": 0.30, "ci_lower": 0.18, "ci_upper": 0.42},
    ])
    viz.plot_cross_model_contrast(rows)
    _nonempty(tmp_path, "F6_cross_model_contrast")


def test_F6_no_ci(viz, tmp_path):
    rows = pd.DataFrame([{"dataset": "sst2", "delta": 0.2}, {"dataset": "mnli", "delta": 0.1}])
    viz.plot_cross_model_contrast(rows)
    _nonempty(tmp_path, "F6_cross_model_contrast")


def test_F7_confidence_ecs_grid(viz, tmp_path):
    rows, corr = [], {}
    for ds in ["sst2", "mnli"]:
        for m in ["nova-pro", "qwen3-235b"]:
            for _ in range(10):
                rows.append({"dataset": ds, "model": m,
                             "confidence": np.random.rand() * 100, "ecs_adj": np.random.rand()})
            corr[f"{m}_{ds}"] = SimpleNamespace(rho=0.3, kendall_tau_b=0.2)
    viz.plot_confidence_ecs_scatter_grid(pd.DataFrame(rows), corr)
    _nonempty(tmp_path, "F7_confidence_ecs_grid")
