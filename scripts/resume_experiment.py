"""Resume an interrupted experiment run from its existing output directory.

Usage:
    python scripts/resume_experiment.py 20260703_124843_013dd120
    python scripts/resume_experiment.py outputs/20260703_124843_013dd120
    python scripts/resume_experiment.py 20260703_124843_013dd120 --force-restart

Reads the run's OWN config_snapshot.yaml (written near the start of run_experiment.py,
before any API calls) rather than the live config/ directory, which may have changed
since the original run started — resuming MUST use the exact seed/sample_size/models
that produced the existing checkpoints, or the reconstructed instance sample would
silently diverge from the one partially processed so far.

Already-checkpointed (dataset, model) instances are skipped; only unfinished
instances are (re-)processed. Whether this call finishes the run or stops early again
(e.g. renewed rate-limiting), ALL output artifacts (instance_results.jsonl,
aggregate_metrics.json, report.md, instance_metrics.csv, execution_summary.txt, ...)
are recalculated from the full merged instance set (old + newly completed) and
overwritten in place in the SAME directory — run_experiment.py's save_* calls always
write fresh, complete files, never append.
"""
import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from src.utils.config_loader import load_config_from_snapshot, ConfigValidator
import run_experiment as re_mod


def resolve_run_dir(name_or_path: str, default_base: str = "outputs") -> Path:
    """Accept either a full/relative path or a bare output-folder name."""
    p = Path(name_or_path)
    if p.exists():
        return p
    candidate = Path(default_base) / name_or_path
    if candidate.exists():
        return candidate
    raise FileNotFoundError(
        f"Could not find run directory '{name_or_path}' (also tried '{candidate}'). "
        "Pass either the full path or the folder name under outputs/."
    )


def main():
    load_dotenv()
    p = argparse.ArgumentParser(description="Resume an interrupted experiment run")
    p.add_argument("run_dir", type=str,
                   help="Output folder name (e.g. 20260703_124843_013dd120) or full path")
    p.add_argument("--force-restart", action="store_true",
                   help="Ignore existing checkpoints in this directory and reprocess every instance")
    cli_args = p.parse_args()

    run_dir = resolve_run_dir(cli_args.run_dir)
    snapshot_path = run_dir / "config_snapshot.yaml"
    if not snapshot_path.exists():
        raise FileNotFoundError(
            f"{snapshot_path} not found — this run has no saved config to resume with. "
            "Only runs started after the resume feature was added write config_snapshot.yaml "
            "at launch (previously it was written only on successful completion, so an "
            "interrupted older run has no snapshot to recover)."
        )
    config = load_config_from_snapshot(snapshot_path)
    ConfigValidator().validate(config)

    print(f"Resuming '{config.experiment.name}' (v{config.experiment.version}) at {run_dir}")
    for ds in config.datasets:
        for m in config.models:
            existing = re_mod._load_checkpointed_results(run_dir, ds.name, m.name)
            print(f"  {m.name}/{ds.name}: {len(existing)}/{ds.sample_size} instances already checkpointed")

    args = argparse.Namespace(resume_dir=str(run_dir), force_restart=cli_args.force_restart)
    asyncio.run(re_mod.run_experiment(config, args))


if __name__ == "__main__":
    main()
