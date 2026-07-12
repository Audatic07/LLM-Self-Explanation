"""Unit tests for the erasure pass (scripts/run_validity_tests.py) — the analysis
half only (no API calls): paired-difference construction, aggregate structure with
the pre-registered test family (b), and the erase() operator semantics."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "run_validity_tests", ROOT / "scripts" / "run_validity_tests.py")
rvt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rvt)

erase = rvt.erase
aggregate = rvt.aggregate
_paired_cc_random_diffs = rvt._paired_cc_random_diffs
_tier = rvt._tier
_rate = rvt._rate
_mean = rvt._mean

from src.normalization.normalizer import Normalizer


def _rec(iid, model, cc3_mask, rand_mask, ecs_lift=0.1, cc3_delete=None, rand_delete=None):
    return {
        "instance_id": iid,
        "dataset": "sst2",
        "model": model,
        "correct": True,
        "ecs": 0.3,
        "ecs_lift": ecs_lift,
        "original_prediction": "positive",
        "strategy_erasure": {"H": {"n": 3, "mask": True, "delete": True}},
        "cc3": {"size": 2, "mask": cc3_mask, "delete": cc3_delete},
        "cc4": {"size": 1, "mask": None, "delete": None},
        "random_cc3": {"n": 2, "mask_rate": rand_mask, "delete_rate": rand_delete},
        "cf_flip_heldout": None,
    }


class TestPairedDiffs:
    def test_pairing_is_within_instance(self):
        records = [
            _rec("a", "m1", True, 0.2),
            _rec("b", "m1", False, 0.5),
            _rec("c", "m1", None, 0.1),   # missing cc side -> excluded
            _rec("d", "m1", True, None),  # missing random side -> excluded
        ]
        diffs = _paired_cc_random_diffs(records, "mask")
        assert diffs == [pytest.approx(0.8), pytest.approx(-0.5)]


class TestAggregate:
    def test_structure_and_test_family(self):
        # 8 instances where CC erasure always flips and random rarely does ->
        # the pre-registered one-sided test should come out small.
        records = [_rec(f"i{k}", "m1", True, 0.1, ecs_lift=0.05 * k,
                        cc3_delete=True, rand_delete=0.2) for k in range(8)]
        agg = aggregate(records, ["mask", "delete"], n_permutations=500,
                        min_n_for_test=6, seed=1)
        o = agg["overall"]
        assert o["cc3_flip_rate"]["mask"] == 1.0
        assert o["random_flip_rate"]["mask"] == pytest.approx(0.1)
        assert o["cc3_minus_random"]["mask"] == pytest.approx(0.9)
        t = o["cc3_vs_random_test"]
        assert t["mask"]["n_paired"] == 8
        assert t["mask"]["p_raw"] is not None and t["mask"]["p_raw"] < 0.05
        assert t["mask"]["p_holm"] is not None
        # Holm within the operator family: adjusted >= raw.
        assert t["mask"]["p_holm"] >= t["mask"]["p_raw"]

    def test_below_min_n_skips_test_but_reports_estimate(self):
        records = [_rec(f"i{k}", "m1", True, 0.0) for k in range(3)]
        agg = aggregate(records, ["mask"], n_permutations=200, min_n_for_test=6, seed=1)
        t = agg["overall"]["cc3_vs_random_test"]["mask"]
        assert t["p_raw"] is None and t["p_holm"] is None
        assert agg["overall"]["cc3_minus_random"]["mask"] is not None

    def test_tier_breakdown_descriptive(self):
        records = [_rec(f"i{k}", "m1", k % 2 == 0, 0.1, ecs_lift=0.1 * k) for k in range(9)]
        agg = aggregate(records, ["mask"], n_permutations=100, min_n_for_test=6, seed=1)
        tiers = agg["by_ecs_lift_tier"]
        assert "_thresholds" in tiers
        assert set(tiers) >= {"low", "high", "_thresholds"}

    def test_heldout_rate_counted(self):
        records = [_rec("a", "m1", True, 0.0), _rec("b", "m1", True, 0.0)]
        records[0]["cf_flip_heldout"] = True
        records[1]["cf_flip_heldout"] = False
        agg = aggregate(records, ["mask"], n_permutations=100, min_n_for_test=6, seed=1)
        assert agg["overall"]["cf_flip_heldout_rate"] == pytest.approx(0.5)
        assert agg["overall"]["n_cf_heldout_checked"] == 2


class TestErase:
    def test_mask_and_delete_all_occurrences(self):
        text = "good food and good service"
        assert erase(text, {"good"}, "mask") == "[MASK] food and [MASK] service"
        assert erase(text, {"good"}, "delete") == "food and service"

    def test_lemma_aware_erasure(self):
        norm = Normalizer(use_lemmatization=True, remove_stopwords=True)
        # Evidence lemma "movie" must erase the inflected occurrence "movies".
        out = erase("great movies here", {"movie"}, "delete", normalizer=norm)
        assert "movies" not in out

    def test_tier_helper(self):
        assert _tier(None, 0.1, 0.2) is None
        assert _tier(0.05, 0.1, 0.2) == "low"
        assert _tier(0.15, 0.1, 0.2) == "mid"
        assert _tier(0.25, 0.1, 0.2) == "high"


class TestOccurrenceMatchedControl:
    """Audit F2 (RESEARCH_AUDIT_2026-07-10): the random control can match the CC3
    arm's destroyed-token count, not just its type count."""

    def test_erased_token_count_matches_erase(self):
        norm = Normalizer(use_lemmatization=True, remove_stopwords=True)
        text = "The movies were great and the movie score was great fun"
        tokens = {"movie", "great"}
        n = rvt.erased_token_count(text, tokens, norm)
        destroyed = len(text.split()) - len(erase(text, tokens, "delete", norm).split())
        assert n == destroyed
        assert n >= 4  # movies, movie, great, great (lemma fan-out counts occurrences)

    def test_type_matched_legacy_mode(self):
        norm = Normalizer(use_lemmatization=True, remove_stopwords=True)
        text = "alpha bravo charlie delta echo foxtrot golf hotel"
        samples = rvt.random_control_samples(text, n=3, trials=4, seed=7,
                                             normalizer=norm, match_occurrences=None)
        assert len(samples) == 4
        assert all(len(s) == 3 for s in samples)

    def test_occurrence_matched_mode_reaches_target(self):
        norm = Normalizer(use_lemmatization=True, remove_stopwords=True)
        # 'alpha' repeats: matching 3 occurrences may need fewer types than 3
        text = "alpha alpha alpha bravo charlie delta echo foxtrot"
        target = 3
        samples = rvt.random_control_samples(text, n=2, trials=6, seed=11,
                                             normalizer=norm, match_occurrences=target)
        assert len(samples) == 6
        # the pool (8 tokens over 6 types, 'alpha' x3) can always reach 3 occurrences
        for s in samples:
            assert rvt.erased_token_count(text, s, norm) >= target

    def test_occurrence_matched_is_deterministic(self):
        norm = Normalizer(use_lemmatization=True, remove_stopwords=True)
        text = "alpha bravo charlie delta echo foxtrot golf hotel india juliet"
        a = rvt.random_control_samples(text, 3, 5, seed=42, normalizer=norm, match_occurrences=4)
        b = rvt.random_control_samples(text, 3, 5, seed=42, normalizer=norm, match_occurrences=4)
        assert a == b


class TestUnknownArmAggregation:
    """Audit F12: unknown-escape sensitivity arm surfaces in aggregate() only when
    records carry it; 'unknown' answers are tracked separately from flips."""

    def test_aggregate_reports_unknown_arm(self):
        recs = []
        for i, (flip, unk, rflip, runk) in enumerate(
                [(True, False, 0.2, 0.4), (False, True, 0.0, 0.6), (None, None, 0.2, 0.2)]):
            r = _rec(f"i{i}", "m1", cc3_mask=True, rand_mask=0.2,
                     cc3_delete=False, rand_delete=0.0)
            r["unknown_arm"] = {"mask": {"cc3_flip": flip, "cc3_unknown": unk,
                                         "random_flip_rate": rflip,
                                         "random_unknown_rate": runk},
                                "delete": {"cc3_flip": False, "cc3_unknown": False,
                                           "random_flip_rate": 0.0,
                                           "random_unknown_rate": 0.0}}
            recs.append(r)
        agg = aggregate(recs, ["mask", "delete"], n_permutations=200, min_n_for_test=2)
        ua = agg["overall"]["unknown_arm"]["mask"]
        assert ua["n"] == 3
        assert ua["cc3_flip_rate"] == pytest.approx(0.5)      # True, False (None dropped)
        assert ua["cc3_unknown_rate"] == pytest.approx(0.5)
        assert ua["random_flip_rate"] == pytest.approx((0.2 + 0.0 + 0.2) / 3)
        assert agg["overall"]["random_control_match_mode"] == ["types"]

    def test_no_unknown_arm_key_when_absent(self):
        recs = [_rec("i0", "m1", cc3_mask=True, rand_mask=0.2,
                     cc3_delete=True, rand_delete=0.4),
                _rec("i1", "m1", cc3_mask=False, rand_mask=0.0,
                     cc3_delete=False, rand_delete=0.2)]
        agg = aggregate(recs, ["mask", "delete"], n_permutations=200, min_n_for_test=2)
        assert "unknown_arm" not in agg["overall"]
