"""Tests for the R1 self-consistency ceiling added to the ablation arm (2026-07-08):
same-strategy AJ(base_set, alt_set) with a support-closed instance vocabulary — the
paraphrase-stability ceiling against which cross-strategy ECS-adj is read."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from scripts.run_ablations import compute_self_consistency_aj
from src.metrics.metrics_calculator import MetricsCalculator
from src.normalization.normalizer import Normalizer


@pytest.fixture(scope="module")
def calc():
    return MetricsCalculator()


@pytest.fixture(scope="module")
def normalizer():
    return Normalizer(use_lemmatization=True, remove_stopwords=True, lemmatizer="wordnet")


TEXT = "The brilliant ensemble cast delivers a moving, unforgettable portrait of resilience."


class TestSelfConsistencyAj:
    def test_identical_sets_score_one(self, calc, normalizer):
        s = {"brilliant", "moving", "unforgettable"}
        aj, degen = compute_self_consistency_aj(s, set(s), TEXT, normalizer, calc)
        assert not degen
        assert aj == pytest.approx(1.0)

    def test_disjoint_sets_score_at_or_below_zero(self, calc, normalizer):
        base = {"brilliant", "moving"}
        alt = {"resilience", "portrait"}
        aj, degen = compute_self_consistency_aj(base, alt, TEXT, normalizer, calc)
        assert not degen
        # J=0 < E[J] -> below chance -> negative (or 0 in the measure-zero E[J]=0 case).
        assert aj is not None and aj <= 0.0

    def test_empty_set_is_missing_not_degenerate(self, calc, normalizer):
        aj, degen = compute_self_consistency_aj(set(), {"moving"}, TEXT, normalizer, calc)
        assert aj is None
        assert degen is False  # missing evidence, not a degenerate geometry

    def test_support_closure_covers_out_of_vocab_evidence(self, calc, normalizer):
        # Evidence tokens absent from the input text must still be inside the urn
        # (support closure mirrors run_experiment P1.1) — the call must not blow up
        # and must return a defined AJ for overlapping sets.
        base = {"zzzunseen", "moving"}
        alt = {"zzzunseen", "moving"}
        aj, degen = compute_self_consistency_aj(base, alt, TEXT, normalizer, calc)
        assert not degen
        assert aj == pytest.approx(1.0)

    def test_partial_overlap_between_zero_and_one(self, calc, normalizer):
        base = {"brilliant", "moving", "portrait"}
        alt = {"brilliant", "moving", "resilience"}
        aj, degen = compute_self_consistency_aj(base, alt, TEXT, normalizer, calc)
        assert not degen
        assert aj is not None and 0.0 < aj < 1.0


class TestEcsAdjFromTokenSets:
    """Audit F10 (RESEARCH_AUDIT_2026-07-10): paraphrase deltas are also reported on
    the primary metric's (ECS-adj) scale via compute_ecs_adj_from_token_sets."""

    def test_identical_strategy_sets_score_positive(self, calc, normalizer):
        from scripts.run_ablations import compute_ecs_adj_from_token_sets
        s = {"brilliant", "moving", "unforgettable"}
        sets = {"H": set(s), "R": set(s), "CF": set(s), "RO": set(s)}
        val = compute_ecs_adj_from_token_sets(sets, TEXT, normalizer, calc)
        assert val is not None
        assert val == pytest.approx(1.0)

    def test_empty_sets_give_none(self, calc, normalizer):
        from scripts.run_ablations import compute_ecs_adj_from_token_sets
        sets = {"H": set(), "R": set(), "CF": set(), "RO": set()}
        assert compute_ecs_adj_from_token_sets(sets, TEXT, normalizer, calc) is None
