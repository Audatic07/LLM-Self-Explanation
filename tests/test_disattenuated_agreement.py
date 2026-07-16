"""Unit tests for scripts/run_disattenuated_agreement.py (Move 1,
STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md §1.4): Spearman disattenuation algebra,
the pre-registered estimability floor, the at-ceiling flag, the
paradigm-balanced composite, and CI determinism. Offline — no API."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "run_disattenuated_agreement", ROOT / "scripts" / "run_disattenuated_agreement.py")
rda = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rda)


def _rel(mean, n=50, values=None):
    if values is None:
        values = [mean] * n
    return {"mean": mean, "n": n, "values": values}


class TestDisattenuationAlgebra:
    def test_known_algebra(self):
        # obs=0.45, rel_a=rel_b=0.9 -> 0.45/sqrt(0.81) = 0.45/0.9 = 0.50 exactly.
        assert rda.disattenuate(0.45, 0.9, 0.9) == pytest.approx(0.50)

    def test_pair_entry_uses_the_formula(self):
        e = rda.build_pair_entry([0.45] * 20, _rel(0.9), _rel(0.9), "H", "R",
                                 n_bootstrap=50)
        assert e["estimable"] is True
        assert e["observed"] == pytest.approx(0.45)
        assert e["corrected"] == pytest.approx(0.50)
        assert e["at_or_above_ceiling"] is False
        assert e["reason"] is None


class TestReliabilityFloor:
    def test_below_floor_gates_the_pair(self):
        e = rda.build_pair_entry([0.4] * 20, _rel(0.9), _rel(0.29), "H", "CF")
        assert e["estimable"] is False
        assert e["corrected"] is None
        assert "reliability_below_floor:CF" in e["reason"]
        # observed is still reported (excluded, never silenced)
        assert e["observed"] == pytest.approx(0.4)

    def test_low_ceiling_n_gates_the_pair(self):
        e = rda.build_pair_entry([0.4] * 20, _rel(0.9), _rel(0.9, n=9), "RO", "CF")
        assert e["estimable"] is False
        assert "ceiling_n_below_10:CF" in e["reason"]

    def test_missing_reliability_gates_the_pair(self):
        e = rda.build_pair_entry([0.4] * 20, _rel(0.9), None, "H", "R")
        assert e["estimable"] is False
        assert "reliability_missing:R" in e["reason"]

    def test_no_instances_gates_the_pair(self):
        e = rda.build_pair_entry([], _rel(0.9), _rel(0.9), "H", "R")
        assert e["estimable"] is False
        assert e["reason"] == "no_observed_instances"


class TestCeilingFlag:
    def test_corrected_above_one_flagged_not_truncated(self):
        # obs=0.5, rels=0.49 -> 0.5/0.49 ~= 1.0204 > 1
        e = rda.build_pair_entry([0.5] * 20, _rel(0.49), _rel(0.49), "H", "R",
                                 n_bootstrap=50)
        assert e["estimable"] is True
        assert e["corrected"] == pytest.approx(0.5 / 0.49)
        assert e["corrected"] > 1.0
        assert e["at_or_above_ceiling"] is True


class TestComposite:
    def _pair(self, corrected):
        return {"corrected": corrected, "estimable": corrected is not None}

    def test_missing_rp_component(self):
        pairs = {
            "H_R": self._pair(0.5), "RO_R": self._pair(0.7),
            "H_CF": self._pair(0.4), "RO_CF": self._pair(0.6),
            "R_CF": self._pair(None),
        }
        c = rda.composite(pairs)
        assert c["er_star"] == pytest.approx(0.6)
        assert c["ep_star"] == pytest.approx(0.5)
        assert c["rp_star"] is None
        assert c["n_components"] == 2
        assert c["ecs_adj_disattenuated"] == pytest.approx((0.6 + 0.5) / 2)

    def test_component_defined_with_one_estimable_pair(self):
        pairs = {
            "H_R": self._pair(0.5), "RO_R": self._pair(None),
            "H_CF": self._pair(None), "RO_CF": self._pair(None),
            "R_CF": self._pair(None),
        }
        c = rda.composite(pairs)
        assert c["er_star"] == pytest.approx(0.5)
        assert c["ep_star"] is None
        assert c["n_components"] == 1
        assert c["ecs_adj_disattenuated"] == pytest.approx(0.5)


class TestDeterminism:
    def test_same_inputs_same_seed_identical_cis(self):
        aj = [0.3, 0.5, 0.45, 0.6, 0.4, 0.55, 0.35, 0.5, 0.42, 0.48]
        ra = [0.85, 0.9, 0.95, 0.88, 0.92, 0.87, 0.91, 0.9, 0.93, 0.89, 0.9]
        rb = [0.5, 0.6, 0.55, 0.65, 0.58, 0.52, 0.61, 0.57, 0.59, 0.54, 0.56]
        c1 = rda.bootstrap_ci(aj, ra, rb, n_bootstrap=200, seed=42)
        c2 = rda.bootstrap_ci(aj, ra, rb, n_bootstrap=200, seed=42)
        assert c1 == c2
        assert c1["ci_lower"] is not None and c1["ci_lower"] < c1["ci_upper"]
        assert c1["n_bad_replicates"] == 0
        assert c1["ci_unstable"] is False


class TestPerInstancePairAj:
    def test_matches_metrics_calculator(self):
        from src.metrics.metrics_calculator import MetricsCalculator
        calc = MetricsCalculator()
        rec = {
            "vocab_size": 20,
            "highlighting_tokens": ["a", "b", "c"],
            "rationale_tokens": ["b", "c", "d"],
            "counterfactual_tokens": [],
            "rank_ordering_set": ["a", "c"],
        }
        out = rda.per_instance_pair_aj([rec], calc)
        expected, _ = calc.adjusted_jaccard({"a", "b", "c"}, {"b", "c", "d"}, 20, 0.10)
        assert out["H_R"] == [pytest.approx(expected)]
        # empty CF set -> CF pairs skipped, not zero
        assert out["H_CF"] == []
        assert out["R_CF"] == []

    def test_zero_vocab_skipped(self):
        from src.metrics.metrics_calculator import MetricsCalculator
        rec = {"vocab_size": 0, "highlighting_tokens": ["a"], "rationale_tokens": ["a"],
               "counterfactual_tokens": ["a"], "rank_ordering_set": ["a"]}
        out = rda.per_instance_pair_aj([rec], MetricsCalculator())
        assert all(v == [] for v in out.values())
