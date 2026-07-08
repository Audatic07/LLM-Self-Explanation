"""Tests for the W6 semantic soft-matching sensitivity estimator
(src/metrics/soft_match.py; ECS_ROBUSTNESS_PLAN §5).

The estimator is a bounded sensitivity, so the invariants that matter are:
  * it REDUCES to the hard metric when there is nothing to soft-match (no silent
    divergence from the primary ECS-adj);
  * soft credit only flows above the pre-registered τ;
  * bipartite matching is 1-to-1 (soft-intersection ≤ min(|a|,|b|));
  * the chance null rises under soft-matching (soft E[J] ≥ hard E[J]);
  * paradigm-balanced aggregation matches compute_ecs_adjusted's structure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from src.metrics.soft_match import DictEmbedder, SoftMatcher
from src.metrics.metrics_calculator import MetricsCalculator


@pytest.fixture
def calc():
    return MetricsCalculator()


# --------------------------------------------------------------- soft_jaccard
def test_exact_sets_soft_jaccard_is_one():
    sm = SoftMatcher(DictEmbedder(), tau=0.8)
    assert sm.soft_jaccard({"a", "b"}, {"a", "b"}) == pytest.approx(1.0)


def test_disjoint_no_similarity_soft_jaccard_is_zero():
    sm = SoftMatcher(DictEmbedder(), tau=0.8)
    assert sm.soft_jaccard({"a", "b"}, {"c", "d"}) == pytest.approx(0.0)


def test_synonym_credited_only_above_tau():
    # "awful"~"terrible" at cosine 0.85 is credited at τ=0.8 but not at τ=0.9.
    emb = DictEmbedder({frozenset(("awful", "terrible")): 0.85})
    below = SoftMatcher(emb, tau=0.8)
    above = SoftMatcher(emb, tau=0.9)
    # both sets size 2: exact "bad" (1.0) + soft "awful"~"terrible" (0.85) ->
    # inter = 1.85, union = 2 + 2 - 1.85 = 2.15
    j_soft = below.soft_jaccard({"bad", "awful"}, {"bad", "terrible"})
    assert j_soft == pytest.approx(1.85 / 2.15)
    # at τ=0.9 the synonym drops out -> reduces to hard Jaccard (1 shared of 3)
    j_hard = above.soft_jaccard({"bad", "awful"}, {"bad", "terrible"})
    assert j_hard == pytest.approx(1.0 / 3.0)


def test_reduces_to_hard_jaccard_when_all_below_tau(calc):
    # distinct tokens all below τ -> soft-J must equal the exact-token Jaccard.
    emb = DictEmbedder({frozenset(("x", "y")): 0.5, frozenset(("p", "q")): 0.1})
    sm = SoftMatcher(emb, tau=0.8)
    s1, s2 = {"x", "p", "shared"}, {"y", "q", "shared"}
    assert sm.soft_jaccard(s1, s2) == pytest.approx(calc.compute_jaccard_similarity(s1, s2))


def test_soft_intersection_bounded_by_smaller_set():
    # everything mutually similar, but 1-to-1 matching caps credit at min(|a|,|b|).
    pairs = {frozenset((a, b)): 0.99 for a in ("a", "b", "c") for b in ("x", "y") if a != b}
    sm = SoftMatcher(DictEmbedder(pairs), tau=0.8)
    inter = sm.soft_intersection({"a", "b", "c"}, {"x", "y"})
    assert inter <= 2.0 + 1e-9  # min(3, 2)


def test_empty_set_soft_jaccard_is_zero():
    sm = SoftMatcher(DictEmbedder(), tau=0.8)
    assert sm.soft_jaccard(set(), {"a"}) == 0.0


# ----------------------------------------------------- chance / adjusted forms
def test_soft_null_geq_hard_null(calc):
    # With pervasive soft similarity, MC E[soft-J] must exceed the exact hard E[J].
    vocab = [f"t{i}" for i in range(10)]
    pairs = {frozenset((a, b)): 0.9 for a in vocab for b in vocab if a < b}
    sm = SoftMatcher(DictEmbedder(pairs), tau=0.8, mc_draws=300, seed=7)
    e_soft, se = sm.expected_soft_jaccard(3, 3, vocab)
    e_hard = calc.expected_jaccard_exact(3, 3, len(vocab))
    assert e_soft > e_hard
    assert se >= 0.0


def test_soft_aj_reduces_to_hard_aj_when_nothing_matches(calc):
    # No cross-token similarity -> soft-AJ must equal hard adjusted_jaccard.
    vocab = [f"t{i}" for i in range(20)]
    sm = SoftMatcher(DictEmbedder(), tau=0.8, mc_draws=400, seed=1)
    s1, s2 = {"t0", "t1", "t2"}, {"t0", "t3", "t4"}
    soft_val, soft_deg, _ = sm.soft_adjusted_jaccard(s1, s2, vocab)
    hard_val, hard_deg = calc.adjusted_jaccard(s1, s2, vocab_size=len(vocab))
    assert soft_deg == hard_deg
    # MC null vs exact null: allow small MC tolerance.
    assert soft_val == pytest.approx(hard_val, abs=0.05)


def test_degeneracy_guard_triggers_on_tight_geometry():
    # 1-vs-5 with a small vocab: J_max - E[soft-J] < eps -> None, degenerate.
    vocab = [f"t{i}" for i in range(6)]
    sm = SoftMatcher(DictEmbedder(), tau=0.8, eps=0.10, mc_draws=200)
    val, degenerate, extras = sm.soft_adjusted_jaccard({"t0"}, {"t0", "t1", "t2", "t3", "t4"}, vocab)
    assert degenerate is True
    assert val is None
    assert "j_max" in extras


# ------------------------------------------------------------- ecs aggregation
def test_soft_ecs_adjusted_structure_and_completeness():
    vocab = [f"t{i}" for i in range(30)]
    sm = SoftMatcher(DictEmbedder(), tau=0.8, mc_draws=200, seed=3)
    explanations = {
        "H": {"t0", "t1", "t2"},
        "R": {"t0", "t3", "t4"},
        "CF": {"t1", "t5"},
        "RO": {"t0", "t2", "t6"},
    }
    res = sm.soft_ecs_adjusted(explanations, vocab)
    assert set(res).issuperset({"ecs_adj_er", "ecs_adj_ep", "ecs_adj_rp",
                                "ecs_adj", "ecs_adj_complete", "n_degenerate_pairs",
                                "pair_soft_aj"})
    assert res["ecs_adj_complete"] == (res["ecs_adj_er"] is not None
                                       and res["ecs_adj_ep"] is not None
                                       and res["ecs_adj_rp"] is not None)


def test_soft_ecs_adjusted_matches_hard_when_no_soft_credit(calc):
    # Injectable no-similarity embedder -> soft ECS-adj must equal hard ECS-adj
    # (same MC-vs-exact tolerance on each surviving component).
    vocab_size = 40
    vocab = [f"t{i}" for i in range(vocab_size)]
    sm = SoftMatcher(DictEmbedder(), tau=0.8, mc_draws=600, seed=11)
    explanations = {
        "H": {"t0", "t1", "t2", "t3"},
        "R": {"t0", "t4", "t5"},
        "CF": {"t1", "t6", "t7"},
        "RO": {"t0", "t2", "t8"},
    }
    soft = sm.soft_ecs_adjusted(explanations, vocab)
    hard = calc.compute_ecs_adjusted(explanations, vocab_size)
    assert soft["ecs_adj_complete"] == hard["ecs_adj_complete"]
    if soft["ecs_adj"] is not None and hard["ecs_adj"] is not None:
        assert soft["ecs_adj"] == pytest.approx(hard["ecs_adj"], abs=0.06)
