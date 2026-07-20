"""Stratified re-analysis of the simulatability arm (POST-HOC, 2026-07-21).

WHY THIS EXISTS
---------------
The pre-registered family (c) estimand is raw simulator accuracy gain,
``gain_s = acc_s - acc_baseline``, aggregated over all perturbations. On this data that
estimand is close to uninformative, and the "explanations barely help" reading it
produced is misleading. Two facts, both computed below:

  1. **Severe class imbalance.** Only ~14% of the explanation-independent perturbations
     actually change the target model's label. A constant "predict no change" strategy
     therefore scores ~86%, and every arm (79-86%) sits at or BELOW that trivial
     baseline. There is almost no headroom for an explanation to move the metric.

  2. **Opposing effects that cancel.** Split by whether the label changed, the arms are
     not null at all. Extraction-style explanations (H, RO) HELP on unchanged
     perturbations (~+2.5pp) and HURT on changed ones (-11pp / -10pp): they anchor the
     simulator to the original prediction. CF is the mirror image (hurts unchanged,
     helps changed), consistent with its construct. Weighted 86/14 these wash out to
     ~0, which is the pre-registered null.

The defensible finding is therefore NOT "agreement does not predict simulatability" but
"the registered estimand is underpowered by construction, and stratified, extraction
explanations degrade prediction of behaviour CHANGE."

STATUS: post-hoc. This does not replace family (c); it explains why family (c)'s result
cannot bear the interpretation originally placed on it. Report both.

USAGE
  python scripts/analyze_simulatability_stratified.py --results-dir outputs/<run>
Writes ``<run>/simulatability_stratified.json``.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.statistics.statistical_tests import sign_flip_permutation_test  # noqa: E402

ARMS = ("baseline", "H", "R", "CF", "RO")
STRATEGIES = ("H", "R", "CF", "RO")
MODEL_NAME = {
    "eu.amazon.nova-pro-v1:0": "nova-pro",
    "qwen.qwen3-235b-a22b-2507-v1:0": "qwen3-235b",
    "deepseek.v3-v1:0": "deepseek-v3",
}
SEED = 42
N_PERM = 10000


def load(run: Path):
    orig = {}
    with (run / "instance_results.jsonl").open(encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            orig[(d["instance_id"], d["model"])] = d.get("predicted_label")
    rows = [json.loads(l) for l in
            (run / "simulatability_instances.jsonl").open(encoding="utf-8") if l.strip()]
    return orig, rows


def _rate(c, n):
    return (c / n) if n else None


def headroom(orig, rows) -> Dict[str, Any]:
    """How often the perturbation actually changed the target model's label — the
    ceiling on how much any explanation could possibly matter."""
    by_kind = defaultdict(lambda: [0, 0])
    by_ds = defaultdict(lambda: [0, 0])
    changed = total = unparsed = 0
    for r in rows:
        o = orig.get((r["instance_id"], r["model"]))
        for p in r["perturbations"]:
            t = p.get("target_label")
            if t is None:
                unparsed += 1
                continue
            total += 1
            by_kind[p["kind"]][1] += 1
            by_ds[r["dataset"]][1] += 1
            if t != o:
                changed += 1
                by_kind[p["kind"]][0] += 1
                by_ds[r["dataset"]][0] += 1
    return {
        "n_perturbations_scored": total,
        "n_unparsed_target": unparsed,
        "change_rate": _rate(changed, total),
        "constant_predictor_accuracy": _rate(total - changed, total),
        "change_rate_by_kind": {k: _rate(c, n) for k, (c, n) in sorted(by_kind.items())},
        "change_rate_by_dataset": {k: _rate(c, n) for k, (c, n) in sorted(by_ds.items())},
    }


def stratified_accuracy(orig, rows, model: str = None) -> Dict[str, Any]:
    """Per-arm accuracy split by whether the target's label changed."""
    acc = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for r in rows:
        if model and r["model"] != model:
            continue
        o = orig.get((r["instance_id"], r["model"]))
        for p in r["perturbations"]:
            t = p.get("target_label")
            if t is None:
                continue
            sub = "changed" if t != o else "unchanged"
            for arm, pred in p.get("arms", {}).items():
                if pred is None:
                    continue
                acc[sub][arm][1] += 1
                if pred == t:
                    acc[sub][arm][0] += 1
    out: Dict[str, Any] = {}
    for sub in ("unchanged", "changed"):
        base = _rate(*acc[sub]["baseline"])
        out[sub] = {}
        for arm in ARMS:
            c, n = acc[sub][arm]
            a = _rate(c, n)
            out[sub][arm] = {"accuracy": a, "n": n,
                             "gain_vs_baseline": (a - base) if (a is not None and base is not None) else None}
    # Balanced accuracy: mean of the two class recalls, so the 86% majority cannot
    # dominate the estimand the way raw accuracy does.
    out["balanced_accuracy"] = {}
    base_bal = None
    for arm in ARMS:
        ch, un = out["changed"][arm]["accuracy"], out["unchanged"][arm]["accuracy"]
        bal = 0.5 * (ch + un) if (ch is not None and un is not None) else None
        if arm == "baseline":
            base_bal = bal
        out["balanced_accuracy"][arm] = {
            "value": bal,
            "gain_vs_baseline": (bal - base_bal) if (bal is not None and base_bal is not None) else None,
        }
    return out


def paired_changed_subset_test(orig, rows) -> Dict[str, Any]:
    """Per-instance paired test restricted to CHANGED perturbations — the only cases
    where an explanation can demonstrate it conveys behaviour change. Two-sided
    reported as both one-sided p's (the suite exposes a one-sided test)."""
    out = {}
    for arm in STRATEGIES:
        diffs: List[float] = []
        for r in rows:
            o = orig.get((r["instance_id"], r["model"]))
            bc = bn = ac = an = 0
            for p in r["perturbations"]:
                t = p.get("target_label")
                if t is None or t == o:
                    continue
                bp, ap = p["arms"].get("baseline"), p["arms"].get(arm)
                if bp is not None:
                    bn += 1
                    bc += (bp == t)
                if ap is not None:
                    an += 1
                    ac += (ap == t)
            if bn and an:
                diffs.append(ac / an - bc / bn)
        entry = {"n_instances": len(diffs),
                 "mean_diff": (sum(diffs) / len(diffs)) if diffs else None}
        if len(diffs) >= 6:
            entry["p_helps"] = sign_flip_permutation_test(
                diffs, n_permutations=N_PERM, seed=SEED, alternative="greater")
            entry["p_hurts"] = sign_flip_permutation_test(
                [-d for d in diffs], n_permutations=N_PERM, seed=SEED, alternative="greater")
        out[arm] = entry
    return out


def run(run_dir: Path) -> Dict[str, Any]:
    orig, rows = load(run_dir)
    result = {
        "provenance": {
            "prereg": "POST-HOC (2026-07-21). Diagnostic for pre-registered family (c); "
                      "does not replace it.",
            "seed": SEED,
            "n_permutations": N_PERM,
            "n_instances": len(rows),
        },
        "headroom": headroom(orig, rows),
        "pooled": stratified_accuracy(orig, rows),
        "per_model": {MODEL_NAME.get(m, m): stratified_accuracy(orig, rows, model=m)
                      for m in MODEL_NAME},
        "paired_changed_subset_test": paired_changed_subset_test(orig, rows),
    }
    # Integrity guard: the simulator must never be the target model.
    result["provenance"]["n_simulator_equals_target"] = sum(
        1 for r in rows if r.get("simulator") == r.get("model"))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--results-dir", type=Path, required=True)
    args = ap.parse_args()
    res = run(args.results_dir)
    out = args.results_dir / "simulatability_stratified.json"
    out.write_text(json.dumps(res, indent=2), encoding="utf-8")

    h = res["headroom"]
    print(f"simulator==target (must be 0): {res['provenance']['n_simulator_equals_target']}")
    print(f"label-change rate: {100*h['change_rate']:.1f}%  "
          f"=> constant predictor scores {100*h['constant_predictor_accuracy']:.1f}%")
    print("  by kind:   " + "  ".join(f"{k}={100*v:.1f}%" for k, v in h["change_rate_by_kind"].items()))
    print("  by dataset:" + "  ".join(f" {k}={100*v:.1f}%" for k, v in h["change_rate_by_dataset"].items()))
    for sub in ("unchanged", "changed"):
        print(f"\n[{sub}] accuracy (gain vs baseline):")
        for arm in ARMS:
            e = res["pooled"][sub][arm]
            if e["accuracy"] is None:
                continue
            print(f"   {arm:8s} {100*e['accuracy']:5.1f}%  ({e['gain_vs_baseline']*100:+5.1f} pp)  n={e['n']}")
    print("\n[balanced accuracy]")
    for arm in ARMS:
        e = res["balanced_accuracy"] if False else res["pooled"]["balanced_accuracy"][arm]
        if e["value"] is not None:
            print(f"   {arm:8s} {100*e['value']:5.1f}%  ({e['gain_vs_baseline']*100:+5.1f} pp)")
    print("\n[paired test, CHANGED perturbations only]")
    for arm, e in res["paired_changed_subset_test"].items():
        if e.get("mean_diff") is None:
            continue
        print(f"   {arm:3s} mean={e['mean_diff']:+.3f} n={e['n_instances']:3d} "
              f"p(helps)={e.get('p_helps')} p(hurts)={e.get('p_hurts')}")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
