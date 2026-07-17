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


class TestResolveModel:
    """--model override (STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md §1.1): resolve a config
    model NAME to its ModelConfig; unknown name is a hard error listing valid names."""

    @pytest.fixture(scope="class")
    def config(self):
        from types import SimpleNamespace
        return SimpleNamespace(models=[
            SimpleNamespace(name="nova-pro", model_id="eu.amazon.nova-pro-v1:0"),
            SimpleNamespace(name="qwen3-235b", model_id="qwen.qwen3-235b-a22b-2507-v1:0"),
            SimpleNamespace(name="deepseek-v3", model_id="deepseek.v3-v1:0"),
        ])

    def test_valid_name_resolves_to_model_id(self, config):
        from scripts.run_ablations import resolve_model
        assert resolve_model(config, "qwen3-235b").model_id == "qwen.qwen3-235b-a22b-2507-v1:0"
        assert resolve_model(config, "deepseek-v3").model_id == "deepseek.v3-v1:0"

    def test_none_defaults_to_first_model(self, config):
        from scripts.run_ablations import resolve_model
        assert resolve_model(config, None).name == "nova-pro"

    def test_unknown_name_raises_listing_valid(self, config):
        from scripts.run_ablations import resolve_model
        from src.utils.exceptions import ConfigurationError
        with pytest.raises(ConfigurationError) as exc:
            resolve_model(config, "gpt-4o")
        assert "qwen3-235b" in str(exc.value)


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


class TestResolveDatasets:
    """--datasets subset resolver (ceilings top-up passes for late-added dataset
    arms); mirrors the resolve_model contract: None = all, unknown = hard error."""

    @pytest.fixture(scope="class")
    def config(self):
        from types import SimpleNamespace
        return SimpleNamespace(datasets=[
            SimpleNamespace(name="sst2"),
            SimpleNamespace(name="mnli"),
            SimpleNamespace(name="ag_news"),
            SimpleNamespace(name="cad_imdb"),
        ])

    def test_valid_subset_resolves_in_given_order(self, config):
        from scripts.run_ablations import resolve_datasets
        out = resolve_datasets(config, ["cad_imdb", "sst2"])
        assert [d.name for d in out] == ["cad_imdb", "sst2"]

    def test_none_defaults_to_all_datasets(self, config):
        from scripts.run_ablations import resolve_datasets
        assert [d.name for d in resolve_datasets(config, None)] == [
            "sst2", "mnli", "ag_news", "cad_imdb"]

    def test_unknown_name_raises_listing_valid(self, config):
        from scripts.run_ablations import resolve_datasets
        from src.utils.exceptions import ConfigurationError
        with pytest.raises(ConfigurationError, match="imdb_full.*valid dataset names.*sst2"):
            resolve_datasets(config, ["cad_imdb", "imdb_full"])
