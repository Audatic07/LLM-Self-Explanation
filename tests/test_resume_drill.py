"""Kill/resume drill (pre-flight checklist item, IMPROVEMENT_PLAN_2026-07-04.md #9):
interrupt a run mid-flight and confirm checkpoint resume produces IDENTICAL results
to an uninterrupted run.

Bedrock is unavailable for a live drill (account-level quota exhaustion at the time
this was written), so `process_instance` is replaced with a deterministic fake that
returns a distinct, real InstanceResult per instance_id — this exercises the actual
orchestration surface (CheckpointManager file I/O, _load_checkpointed_results,
_run_model_on_dataset's skip/merge logic) rather than re-testing process_instance's
own parsing logic, which is already covered elsewhere (test_parser.py etc.).
"""
import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.utils.config import InferenceConfig, OutputConfig, ModelConfig, DatasetConfig
from src.utils.data_models import InstanceResult

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_spec = importlib.util.spec_from_file_location(
    "run_experiment_mod", ROOT / "scripts" / "run_experiment.py")
rx = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rx)


def _instances(n):
    from types import SimpleNamespace
    return [SimpleNamespace(instance_id=f"sst2_{k:03d}") for k in range(n)]


def _config():
    return __import__("types").SimpleNamespace(
        inference=InferenceConfig(concurrent_requests=4, max_retries=1),
        output=OutputConfig(checkpoint_frequency=1),  # flush after every instance
    )


def _dataset(n):
    return DatasetConfig(name="sst2", huggingface_id="hf", split="validation",
                         sample_size=n, labels=["negative", "positive"])


def _deterministic_result(instance_id, model="nova-pro"):
    """A fixed, content-addressed InstanceResult — same instance_id always produces
    byte-identical field values, so two independent runs can be compared exactly."""
    correct = hash(instance_id) % 2 == 0
    return InstanceResult(
        instance_id=instance_id, dataset="sst2", model=model, timestamp=datetime(2026, 7, 4, 12, 0, 0),
        text=f"text for {instance_id}", ground_truth_label="positive",
        predicted_label="positive" if correct else "negative", correct=correct,
        prompt_tokens=42, response_tokens=17,
    )


async def test_resume_after_simulated_kill_matches_uninterrupted_run(tmp_path):
    all_four = _instances(4)

    # --- CONTROL: one uninterrupted pass over all 4 instances ---
    control_dir = tmp_path / "control_run"
    control_dir.mkdir()

    async def fake_pi_full(instance, engine, *args, **kwargs):
        return _deterministic_result(instance.instance_id)

    with patch.object(rx, "InferenceEngine", MagicMock(return_value=MagicMock(
            total_prompt_tokens=0, total_completion_tokens=0, n_truncated=0,
            total_requests=0, total_requests_failed=0, requests_by_category={}))), \
         patch.object(rx, "process_instance", fake_pi_full):
        control_bundle = await rx._run_model_on_dataset(
            ModelConfig(name="nova-pro", model_id="id", context_window=1000),
            all_four, {}, _dataset(4),
            MagicMock(), MagicMock(), MagicMock(), _config(), control_dir,
        )
    control_results = {r.instance_id: r for r in control_bundle["results"]}
    assert set(control_results) == {"sst2_000", "sst2_001", "sst2_002", "sst2_003"}

    # --- INTERRUPTED: process only the first 2 instances, THEN THE PROCESS DIES ---
    # (simulated by simply never calling run_experiment's tail-end file writes —
    # _run_model_on_dataset itself already flushed a checkpoint for these 2 via its
    # final _flush_checkpoint(), which is exactly what survives a kill.)
    resume_dir = tmp_path / "interrupted_run"
    resume_dir.mkdir()

    async def fake_pi_first_two(instance, engine, *args, **kwargs):
        return _deterministic_result(instance.instance_id)

    with patch.object(rx, "InferenceEngine", MagicMock(return_value=MagicMock(
            total_prompt_tokens=0, total_completion_tokens=0, n_truncated=0,
            total_requests=0, total_requests_failed=0, requests_by_category={}))), \
         patch.object(rx, "process_instance", fake_pi_first_two):
        first_bundle = await rx._run_model_on_dataset(
            ModelConfig(name="nova-pro", model_id="id", context_window=1000),
            all_four[:2], {}, _dataset(4),  # only 2 of the 4 instances "reach" this process
            MagicMock(), MagicMock(), MagicMock(), _config(), resume_dir,
        )
    assert len(first_bundle["results"]) == 2

    # Checkpoint file must be on disk now (this is what a killed process leaves behind).
    cp_path = resume_dir / "checkpoint_sst2_nova-pro.jsonl"
    assert cp_path.exists()
    with open(cp_path, encoding="utf-8") as f:
        checkpointed_lines = [l for l in f if l.strip()]
    assert len(checkpointed_lines) == 2

    # --- RESUME: a fresh process picks up the SAME output dir ---
    existing = rx._load_checkpointed_results(resume_dir, "sst2", "nova-pro")
    assert {r.instance_id for r in existing} == {"sst2_000", "sst2_001"}

    async def fake_pi_remaining(instance, engine, *args, **kwargs):
        return _deterministic_result(instance.instance_id)

    with patch.object(rx, "InferenceEngine", MagicMock(return_value=MagicMock(
            total_prompt_tokens=0, total_completion_tokens=0, n_truncated=0,
            total_requests=0, total_requests_failed=0, requests_by_category={}))), \
         patch.object(rx, "process_instance", fake_pi_remaining):
        resumed_bundle = await rx._run_model_on_dataset(
            ModelConfig(name="nova-pro", model_id="id", context_window=1000),
            all_four, {}, _dataset(4),   # the FULL sample is reconstructed (same seed/config)
            MagicMock(), MagicMock(), MagicMock(), _config(), resume_dir,
            existing_results=existing,
        )
    resumed_results = {r.instance_id: r for r in resumed_bundle["results"]}

    # Core guarantee: resume produces the SAME 4 results as the uninterrupted control.
    assert set(resumed_results) == set(control_results)
    for iid in control_results:
        c, r = control_results[iid], resumed_results[iid]
        assert c.to_dict() == r.to_dict(), f"{iid} diverged between control and resumed runs"

    # And the checkpoint file on disk now has all 4 (no duplicates from the 2 seeded ones).
    with open(cp_path, encoding="utf-8") as f:
        final_lines = [l for l in f if l.strip()]
    assert len(final_lines) == 4


async def test_force_restart_after_kill_reprocesses_everything(tmp_path):
    """--force-restart on a resume must discard the interrupted checkpoint entirely,
    not merge it — used when the operator wants a clean slate instead of continuing."""
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    attempted = []

    async def fake_pi(instance, engine, *args, **kwargs):
        attempted.append(instance.instance_id)
        return _deterministic_result(instance.instance_id)

    with patch.object(rx, "InferenceEngine", MagicMock(return_value=MagicMock(
            total_prompt_tokens=0, total_completion_tokens=0, n_truncated=0,
            total_requests=0, total_requests_failed=0, requests_by_category={}))), \
         patch.object(rx, "process_instance", fake_pi):
        await rx._run_model_on_dataset(
            ModelConfig(name="nova-pro", model_id="id", context_window=1000),
            _instances(2), {}, _dataset(4),
            MagicMock(), MagicMock(), MagicMock(), _config(), run_dir,
        )

    existing = rx._load_checkpointed_results(run_dir, "sst2", "nova-pro")
    assert len(existing) == 2

    attempted.clear()
    with patch.object(rx, "InferenceEngine", MagicMock(return_value=MagicMock(
            total_prompt_tokens=0, total_completion_tokens=0, n_truncated=0,
            total_requests=0, total_requests_failed=0, requests_by_category={}))), \
         patch.object(rx, "process_instance", fake_pi):
        restarted_bundle = await rx._run_model_on_dataset(
            ModelConfig(name="nova-pro", model_id="id", context_window=1000),
            _instances(4), {}, _dataset(4),
            MagicMock(), MagicMock(), MagicMock(), _config(), run_dir,
            existing_results=existing, force_restart=True,
        )

    assert attempted == ["sst2_000", "sst2_001", "sst2_002", "sst2_003"]
    assert len(restarted_bundle["results"]) == 4
