"""Unit tests for scripts/run_simulatability.py (Move 3,
STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md §3.4): perturbation determinism + tie-break,
skip rules, prompt rendering, aggregation math (Holm family size, red-flag P/R),
and the checkpoint skip. Offline — mock engines only, no API."""
import asyncio
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "run_simulatability", ROOT / "scripts" / "run_simulatability.py")
rs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rs)

from src.normalization.normalizer import Normalizer
from src.parsing.parser import Parser


@pytest.fixture(scope="module")
def normalizer():
    return Normalizer(use_lemmatization=True, remove_stopwords=True, lemmatizer="wordnet")


class TestPerturbations:
    def test_deterministic_across_calls(self, normalizer):
        text = ("The brilliant ensemble cast delivers a moving portrait of resilience "
                "and the direction stays sharp throughout the entire film.")
        a, da = rs.build_perturbations("sst2_validation_000123", text, normalizer)
        b, db = rs.build_perturbations("sst2_validation_000123", text, normalizer)
        assert a == b and da == db
        assert [p["kind"] for p in a] == ["P1", "P2", "P3"]
        # different instance_id -> different random draws (P1/P2 seeded by crc32(id)^42)
        c, _ = rs.build_perturbations("sst2_validation_000999", text, normalizer)
        assert [p["kind"] for p in c] == ["P1", "P2", "P3"]

    def test_p2_masks_p1_deletes(self, normalizer):
        text = ("The brilliant ensemble cast delivers a moving portrait of resilience "
                "and the direction stays sharp throughout the entire film.")
        perts, _ = rs.build_perturbations("id_x", text, normalizer)
        by_kind = {p["kind"]: p["text"] for p in perts}
        assert "[MASK]" in by_kind["P2"]
        assert "[MASK]" not in by_kind["P1"]
        assert len(by_kind["P1"].split()) < len(text.split())

    def test_p3_top_frequency_with_alphabetical_tiebreak(self, normalizer):
        # zebra appears 3x; apple and mango 2x each (tie) -> alphabetical picks
        # apple before mango; k=3 -> {zebra, apple, mango}.
        text = "zebra zebra zebra apple apple mango mango kiwi banana"
        top = rs.top_frequency_types(text, normalizer, k=3)
        assert top == ["zebra", "apple", "mango"]
        # k=2 drops mango via the tie-break
        assert rs.top_frequency_types(text, normalizer, k=2) == ["zebra", "apple"]

    def test_small_pool_uses_all_available(self, normalizer):
        # Only 2 content types survive normalization (stopwords removed).
        text = "the zebra and the mango"
        pool = rs.content_type_pool(text, normalizer)
        assert len(pool) == 2
        perts, _ = rs.build_perturbations("id_y", text, normalizer)
        p3 = next(p for p in perts if p["kind"] == "P3")
        # both content words destroyed
        assert "zebra" not in p3["text"] and "mango" not in p3["text"]

    def test_noop_perturbation_dropped_and_counted(self, normalizer):
        # No content words at all -> pool empty -> P1/P2 have no samples and P3 has
        # no types: zero perturbations, nothing counted as a noop drop.
        perts, dropped = rs.build_perturbations("id_z", "the and of", normalizer)
        assert perts == [] and dropped == 0
        # Monkeypatch erase to a no-op to force the perturbed==original branch.
        orig_erase = rs.erase
        try:
            rs.erase = lambda text, tokens, op, norm: text
            text = "zebra apple mango kiwi banana melon grape peach plum"
            perts, dropped = rs.build_perturbations("id_w", text, normalizer)
            assert perts == [] and dropped == 3
        finally:
            rs.erase = orig_erase


REC = {
    "instance_id": "sst2_validation_000001",
    "model": "eu.amazon.nova-pro-v1:0",
    "dataset": "sst2",
    "text": "The zebra apple mango was brilliant and moving throughout.",
    "predicted_label": "positive",
    "ecs_adj": 0.4,
    "ecs_adj_complete": True,
    "highlighting_tokens": ["brilliant", "moving"],
    "rationale_text": "The review praises the film warmly.",
    "cf_counterfactual_text": "The zebra apple mango was dull and boring throughout.",
    "cf_flip_verified": True,
    "rank_ordering_tokens": [["brilliant", 1], ["moving", 2]],
}


class TestPromptRendering:
    def test_all_arms_format_without_keyerror(self):
        sim = (ROOT / "prompts/simulatability_predict.txt").read_text(encoding="utf-8")
        base = (ROOT / "prompts/simulatability_predict_baseline.txt").read_text(encoding="utf-8")
        labels = ["negative", "positive"]
        out_base = rs.format_sim_prompt(base, REC, "modified text", labels)
        assert "modified text" in out_base and REC["text"] in out_base
        for s in rs.STRATEGY_ARMS:
            expl, reason = rs.render_explanation(s, REC)
            assert reason is None
            out = rs.format_sim_prompt(sim, REC, "modified text", labels, explanation=expl)
            assert expl in out and "{" not in out.replace('{"label"', "").replace(">"+'"}', "")

    def test_baseline_contains_no_explanation_substring(self):
        base = (ROOT / "prompts/simulatability_predict_baseline.txt").read_text(encoding="utf-8")
        assert "explanation" not in base.lower()

    def test_cf_arm_skipped_without_verified_flip(self):
        rec = dict(REC, cf_flip_verified=False)
        expl, reason = rs.render_explanation("CF", rec)
        assert expl is None and reason == "no verified flip"

    def test_missing_evidence_skips_arm(self):
        rec = dict(REC, highlighting_tokens=[], rationale_text="")
        assert rs.render_explanation("H", rec) == (None, "no highlighting evidence")
        assert rs.render_explanation("R", rec) == (None, "no rationale text")

    def test_ro_renders_in_rank_order(self):
        expl, _ = rs.render_explanation("RO", REC)
        assert expl == "Words ranked by importance: brilliant, moving"


def _sim_rec(iid, model, ecs, target, arms_per_pert):
    """Synthetic simulatability_instances row: arms_per_pert is a list of arm
    dicts, one per perturbation, all sharing `target` as the target label."""
    return {
        "instance_id": iid, "model": model, "simulator": "sim", "dataset": "sst2",
        "ecs_adj": ecs, "ecs_adj_complete": True,
        "perturbations": [{"kind": f"P{i+1}", "target_label": target, "arms": a}
                          for i, a in enumerate(arms_per_pert)],
        "n_perturbations": len(arms_per_pert), "n_dropped_noop": 0, "skipped_arms": {},
    }


class TestAggregation:
    def test_instance_arm_stats_hand_computed(self):
        # 2 perturbations, target "pos". baseline: 1/2 correct. H: 2/2. R: None both.
        rec = _sim_rec("a", "m1", 0.5, "pos", [
            {"baseline": "pos", "H": "pos", "R": None, "CF": "neg", "RO": "pos"},
            {"baseline": "neg", "H": "pos", "R": None, "CF": "pos", "RO": "neg"},
        ])
        st = rs.instance_arm_stats(rec)
        assert st["sim_acc"]["baseline"] == pytest.approx(0.5)
        assert st["sim_acc"]["H"] == pytest.approx(1.0)
        assert st["sim_acc"]["R"] is None
        assert st["sim_acc"]["CF"] == pytest.approx(0.5)
        assert st["gain"]["H"] == pytest.approx(0.5)
        assert "R" not in st["gain"]
        assert st["mean_gain"] == pytest.approx((0.5 + 0.0 + 0.0) / 3)  # H, CF, RO

    def test_null_target_perturbation_excluded(self):
        rec = _sim_rec("a", "m1", 0.5, "pos", [
            {"baseline": "pos", "H": "pos", "R": "pos", "CF": "pos", "RO": "pos"},
        ])
        rec["perturbations"].append(
            {"kind": "P2", "target_label": None,
             "arms": {"baseline": "pos", "H": "neg", "R": "neg", "CF": "neg", "RO": "neg"}})
        st = rs.instance_arm_stats(rec)
        assert st["sim_acc"]["H"] == pytest.approx(1.0)  # null-target row ignored

    def test_aggregate_holm_family_size_counts_non_none(self):
        # Model m1 has enough rows to test; m2 has too few (n<3 -> rho None).
        arms_good = {"baseline": "neg", "H": "pos", "R": "pos", "CF": "pos", "RO": "pos"}
        arms_bad = {"baseline": "pos", "H": "neg", "R": "neg", "CF": "neg", "RO": "neg"}
        records = []
        for i in range(9):
            ecs = i / 10
            records.append(_sim_rec(f"i{i}", "m1", ecs, "pos",
                                    [arms_good if i >= 5 else arms_bad] * 3))
        records.append(_sim_rec("j0", "m2", 0.5, "pos", [arms_good] * 3))
        agg = rs.aggregate(records, ["m1", "m2"], n_permutations=200, seed=42)
        m1, m2 = agg["per_model"]["m1"], agg["per_model"]["m2"]
        assert m1["c1_spearman"]["p_value"] is not None
        assert m2["c1_spearman"]["rho"] is None  # n<3
        # Holm family = only the non-None test -> adjusted equals raw for m1.
        assert m1["c1_spearman"]["p_holm"] == pytest.approx(m1["c1_spearman"]["p_value"])
        assert m2["c1_spearman"]["p_holm"] is None
        # positive association built in -> tercile diff > 0
        assert m1["c2_tercile"]["observed_diff"] > 0

    def test_red_flag_precision_recall_on_toy(self):
        # 4 instances: ecs [0.1, 0.2, 0.8, 0.9] -> median 0.5 -> flagged = first two.
        # "bad" (best strategy < baseline): make instances 0 and 2 bad.
        def row(ecs, bad):
            sim_acc = ({"baseline": 1.0, "H": 0.0, "R": 0.0, "CF": 0.0, "RO": 0.0}
                       if bad else
                       {"baseline": 0.0, "H": 1.0, "R": 1.0, "CF": 1.0, "RO": 1.0})
            return {"stats": {"sim_acc": sim_acc}}
        ecs = [0.1, 0.2, 0.8, 0.9]
        rows = [row(0.1, True), row(0.2, False), row(0.8, True), row(0.9, False)]
        rf = rs.red_flag_stats(ecs, rows)
        # flagged = {0,1}; bad = {0,2}; tp = {0} -> precision 1/2, recall 1/2
        assert rf["precision"] == pytest.approx(0.5)
        assert rf["recall"] == pytest.approx(0.5)
        assert rf["n_flagged"] == 2 and rf["n_bad"] == 2


class MockEngine:
    """Counts calls; returns a fixed JSON label."""
    def __init__(self, label="positive"):
        self.calls = 0
        self.label = label

    async def _make_request(self, prompt, max_tokens=50):
        self.calls += 1
        return json.dumps({"label": self.label})


class TestCheckpointSkip:
    def test_preseeded_row_not_recollected(self, tmp_path, normalizer):
        out_path = tmp_path / "simulatability_instances.jsonl"
        seeded = _sim_rec(REC["instance_id"], REC["model"], 0.4, "positive", [
            {"baseline": "positive", "H": "positive", "R": "positive",
             "CF": "positive", "RO": "positive"}])
        out_path.write_text(json.dumps(seeded) + "\n", encoding="utf-8")

        done = rs.load_done(out_path)
        assert (REC["instance_id"], REC["model"]) in done

        rec2 = dict(REC, instance_id="sst2_validation_000002")
        todo = rs.filter_todo([REC, rec2], done)
        assert [r["instance_id"] for r in todo] == ["sst2_validation_000002"]

        # Collect only the todo row with mock engines: the engine is called for
        # rec2 but never for the pre-seeded REC.
        target, sim = MockEngine(), MockEngine()
        parser = Parser()
        sim_prompt = (ROOT / "prompts/simulatability_predict.txt").read_text(encoding="utf-8")
        base_prompt = (ROOT / "prompts/simulatability_predict_baseline.txt").read_text(encoding="utf-8")
        class_prompt = (ROOT / "prompts/classification_sst2.txt").read_text(encoding="utf-8")
        for r in todo:
            out = asyncio.run(rs.process_instance_sim(
                r, target, sim, "sim-model", parser, class_prompt,
                sim_prompt, base_prompt, ["negative", "positive"], normalizer))
            assert out["instance_id"] == "sst2_validation_000002"
            assert out["n_perturbations"] >= 1
        n_perts = out["n_perturbations"]
        assert target.calls == n_perts          # one target label per perturbation
        assert sim.calls == n_perts * 5          # 5 arms per perturbation (all valid)
