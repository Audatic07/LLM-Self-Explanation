"""Reliability-corrected (disattenuated) cross-paradigm agreement — Move 1 of
STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md, pre-registered as ECS_ROBUSTNESS_PLAN §H.1.

The self-consistency ceilings (same strategy, base vs paraphrased prompt, AJ scale)
are test-retest RELIABILITIES of each elicitation instrument. Observed
between-instrument agreement is attenuated by instrument unreliability; the
classical correction is Spearman (1904):

    corrected = observed / sqrt(rel_A * rel_B)

applied per cross-paradigm pair, per model x dataset cell (and pooled).

INTERPRETATION CONTRACT (registered in advance, §H.1): corrected ~= 1 => the
pair's divergence is within elicitation noise; corrected << 1 with CI excluding 1
=> real paradigm divergence beyond instrument unreliability. Expected headline:
R-involving pairs stay far below 1 (rel ~= .9, obs ~= .45 => corrected ~= .5-.6).

Estimability floor (pre-registered): a pair is estimable only if BOTH
reliabilities >= 0.30 and both ceiling n >= 10. Below-floor pairs are reported as
excluded with the offending strategy — never silenced. Corrected values may
exceed 1.0 from sampling error; they are reported as-is with an
`at_or_above_ceiling` flag (standard psychometrics caveat), never truncated.

Offline analysis only — zero API calls. Usage:

    python scripts/run_disattenuated_agreement.py --results-dir outputs/<main_run> \
        --ablation-dirs outputs/<abl1>/ablations outputs/<abl2>/ablations ...
"""
import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np

from src.metrics.metrics_calculator import MetricsCalculator

# Cross-paradigm pairs, in the ECS-adj component order (er, er, ep, ep, rp).
PAIRS = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
EPS = 0.10
RELIABILITY_FLOOR = 0.30
MIN_CEILING_N = 10
N_BOOTSTRAP = 2000
SEED = 42

# Bedrock model id -> study-facing name (copied from
# scripts/run_weighted_null_sensitivity.py::MODEL_NAME).
MODEL_NAME = {
    "eu.amazon.nova-pro-v1:0": "nova-pro",
    "qwen.qwen3-235b-a22b-2507-v1:0": "qwen3-235b",
    "deepseek.v3-v1:0": "deepseek-v3",
}

EVIDENCE_FIELDS = {
    "H": "highlighting_tokens",
    "R": "rationale_tokens",
    "CF": "counterfactual_tokens",
    "RO": "rank_ordering_set",
}


def disattenuate(observed: float, rel_a: float, rel_b: float) -> float:
    """Spearman (1904) correction for attenuation: obs / sqrt(rel_a * rel_b)."""
    return observed / math.sqrt(rel_a * rel_b)


def check_floor(rel: Dict, strategy: str,
                floor: float = RELIABILITY_FLOOR,
                min_n: int = MIN_CEILING_N) -> Optional[str]:
    """Pre-registered estimability gate for one side of a pair. Returns None when
    the strategy's reliability passes, else a reason string naming the offending
    strategy (below-floor pairs get a table row, never silence)."""
    if rel is None or rel.get("mean") is None:
        return f"reliability_missing:{strategy}"
    if rel["n"] < min_n:
        return f"reliability_ceiling_n_below_{min_n}:{strategy}"
    if rel["mean"] < floor:
        return f"reliability_below_floor:{strategy}"
    return None


def bootstrap_ci(aj_values: List[float], rel_a_values: List[float],
                 rel_b_values: List[float], n_bootstrap: int = N_BOOTSTRAP,
                 seed: int = SEED) -> Dict:
    """Seeded percentile bootstrap for the disattenuated ratio. Per replicate:
    resample (i) the per-instance AJ list (cluster = instance) and (ii) the two
    ceilings' value lists INDEPENDENTLY (numerator and denominator come from
    different draws), then recompute obs/sqrt(relA*relB). Replicates whose
    resampled reliability dips <= 0 are dropped and counted; if >5% are dropped
    the CI is marked unstable."""
    rng = np.random.default_rng(seed)
    aj = np.asarray(aj_values, dtype=float)
    ra = np.asarray(rel_a_values, dtype=float)
    rb = np.asarray(rel_b_values, dtype=float)
    ratios = []
    n_bad = 0
    for _ in range(n_bootstrap):
        obs = float(np.mean(rng.choice(aj, size=len(aj), replace=True)))
        rel_a = float(np.mean(rng.choice(ra, size=len(ra), replace=True)))
        rel_b = float(np.mean(rng.choice(rb, size=len(rb), replace=True)))
        if rel_a <= 0 or rel_b <= 0:
            n_bad += 1
            continue
        ratios.append(obs / math.sqrt(rel_a * rel_b))
    unstable = n_bad > 0.05 * n_bootstrap
    if not ratios:
        return {"ci_lower": None, "ci_upper": None,
                "n_bad_replicates": n_bad, "ci_unstable": True}
    lo, hi = np.percentile(ratios, [2.5, 97.5])
    return {"ci_lower": float(lo), "ci_upper": float(hi),
            "n_bad_replicates": n_bad, "ci_unstable": unstable}


def build_pair_entry(aj_values: List[float], rel_a: Optional[Dict],
                     rel_b: Optional[Dict], strategy_a: str, strategy_b: str,
                     n_bootstrap: int = N_BOOTSTRAP, seed: int = SEED) -> Dict:
    """One pair's full record: observed mean AJ, both reliabilities, the floor
    gate, the disattenuated value with bootstrap CI, and the at-ceiling flag."""
    entry = {
        "observed": float(np.mean(aj_values)) if aj_values else None,
        "rel_a": rel_a.get("mean") if rel_a else None,
        "rel_b": rel_b.get("mean") if rel_b else None,
        "corrected": None,
        "ci_lower": None,
        "ci_upper": None,
        "n_instances": len(aj_values),
        "at_or_above_ceiling": False,
        "estimable": False,
        "reason": None,
    }
    if not aj_values:
        entry["reason"] = "no_observed_instances"
        return entry
    reasons = [r for r in (check_floor(rel_a, strategy_a),
                           check_floor(rel_b, strategy_b)) if r]
    if reasons:
        entry["reason"] = "; ".join(reasons)
        return entry
    entry["estimable"] = True
    entry["corrected"] = disattenuate(entry["observed"], entry["rel_a"], entry["rel_b"])
    entry["at_or_above_ceiling"] = entry["corrected"] > 1.0
    entry.update({k: v for k, v in bootstrap_ci(
        aj_values, rel_a["values"], rel_b["values"],
        n_bootstrap=n_bootstrap, seed=seed).items()})
    return entry


def composite(pairs: Dict[str, Dict]) -> Dict:
    """Paradigm-balanced composite exactly like ECS-adj: er* = mean(corr(H,R),
    corr(RO,R)), ep* = mean(corr(H,CF), corr(RO,CF)), rp* = corr(R,CF);
    ecs_adj_disattenuated = mean of DEFINED components (a component is defined
    only if >= 1 of its pairs is estimable)."""
    def _mean_of(keys):
        vals = [pairs[k]["corrected"] for k in keys
                if k in pairs and pairs[k].get("corrected") is not None]
        return float(np.mean(vals)) if vals else None

    er = _mean_of(["H_R", "RO_R"])
    ep = _mean_of(["H_CF", "RO_CF"])
    rp = _mean_of(["R_CF"])
    components = [c for c in (er, ep, rp) if c is not None]
    return {
        "er_star": er,
        "ep_star": ep,
        "rp_star": rp,
        "ecs_adj_disattenuated": float(np.mean(components)) if components else None,
        "n_components": len(components),
    }


def per_instance_pair_aj(records: List[Dict], calc: MetricsCalculator) -> Dict[str, List[float]]:
    """Per-instance AJ for each cross-paradigm pair, exactly as the pipeline
    computes it: MetricsCalculator.adjusted_jaccard over the stored evidence sets
    with the stored vocab_size, eps=0.10. Empty sets / degenerate geometries are
    skipped (the pair is undefined for that instance, not zero)."""
    out = {f"{a}_{b}": [] for a, b in PAIRS}
    for rec in records:
        vocab = rec.get("vocab_size") or 0
        if vocab <= 0:
            continue
        sets = {s: set(rec.get(f) or []) for s, f in EVIDENCE_FIELDS.items()}
        for a, b in PAIRS:
            if not sets[a] or not sets[b]:
                continue
            val, _degen = calc.adjusted_jaccard(sets[a], sets[b], vocab, EPS)
            if val is not None:
                out[f"{a}_{b}"].append(val)
    return out


def load_reliabilities(ablation_dirs: List[Path]) -> Dict[str, Dict[str, Dict[str, Dict]]]:
    """reliabilities[model_name][dataset][strategy] = {mean, n, values} from each
    ablation dir's ablation_results.json (`{ds}_prompt -> {s}_alt`), keyed by the
    dir's _meta.model mapped through MODEL_NAME."""
    rel: Dict[str, Dict[str, Dict[str, Dict]]] = {}
    for d in ablation_dirs:
        path = Path(d) / "ablation_results.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        meta = data.get("_meta", {})
        model_id = meta.get("model")
        model = meta.get("model_name") or MODEL_NAME.get(model_id, model_id)
        if model is None:
            raise ValueError(f"{path}: _meta.model missing — cannot attribute ceilings")
        # Multiple dirs may cover the SAME model with disjoint dataset subsets (a
        # --datasets top-up pass collected after a new dataset arm, e.g. cad_imdb
        # ceilings for models whose original pass predates the arm). Merge per
        # dataset; the SAME model+dataset ceiling appearing twice is ambiguous
        # provenance and stays a hard error.
        # Which reworded prompt set produced this dir's ceilings. Dirs written before
        # the 2026-07-20 paraphrase expansion carry no stamp and are the original 'alt'.
        variant = meta.get("paraphrase_variant", "alt")
        model_rel = rel.setdefault(model, {})
        for key, strategies in data.items():
            if key == "_meta" or not key.endswith("_prompt"):
                continue
            dataset = key[:-len("_prompt")]
            ds_rel = model_rel.setdefault(dataset, {})
            for skey, e in strategies.items():
                if not skey.endswith("_alt"):
                    continue
                s = skey[:-len("_alt")]
                entry = ds_rel.setdefault(s, {"values": [], "by_variant": {}})
                # The SAME model+dataset+strategy under the SAME paraphrase twice is
                # ambiguous provenance and stays a hard error; different paraphrases
                # are the expansion and are POOLED (2026-07-20).
                if variant in entry["by_variant"]:
                    raise ValueError(
                        f"Duplicate ceilings for model '{model}' dataset '{dataset}' "
                        f"strategy '{s}' paraphrase '{variant}' ({d})")
                vals = e.get("self_consistency_aj_values") or []
                entry["by_variant"][variant] = {
                    "mean": e.get("self_consistency_aj_mean"),
                    "n": e.get("self_consistency_aj_n", 0),
                    "values": vals,
                }
                entry["values"].extend(vals)

    # Finalize: the pooled point estimate is the mean over all paraphrases' values;
    # variant_means/variant_spread expose how much the ceiling moves with the wording,
    # which is the quantity the single-paraphrase design could not report.
    for model, by_ds in rel.items():
        for dataset, by_s in by_ds.items():
            for s, entry in by_s.items():
                entry["n"] = len(entry["values"])
                entry["mean"] = float(np.mean(entry["values"])) if entry["values"] else None
                vm = {v: b["mean"] for v, b in entry["by_variant"].items() if b["mean"] is not None}
                entry["variant_means"] = vm
                entry["n_variants"] = len(vm)
                entry["variant_spread"] = (max(vm.values()) - min(vm.values())) if len(vm) > 1 else None
    return rel


def pool_reliabilities(per_model: List[Optional[Dict]]) -> Optional[Dict]:
    """Pool ceiling value lists across models (per dataset x strategy) — the
    pre-registered per-dataset / overall reliability."""
    values: List[float] = []
    for r in per_model:
        if r:
            values.extend(r["values"])
    if not values:
        return None
    return {"mean": float(np.mean(values)), "n": len(values), "values": values}


def analyze_group(records: List[Dict], rel_by_strategy: Dict[str, Optional[Dict]],
                  calc: MetricsCalculator) -> Dict:
    """Full pair table + composite for one group of instances with one
    reliability lookup per strategy."""
    aj_lists = per_instance_pair_aj(records, calc)
    pairs = {}
    for a, b in PAIRS:
        key = f"{a}_{b}"
        pairs[key] = build_pair_entry(aj_lists[key], rel_by_strategy.get(a),
                                      rel_by_strategy.get(b), a, b)
    result = {"pairs": pairs}
    result.update(composite(pairs))
    return result


def _fmt(v, spec=".3f"):
    return format(v, spec) if v is not None else "--"


def print_group(label: str, group: Dict) -> None:
    for key, e in group["pairs"].items():
        if e["estimable"]:
            flag = " AT-CEILING" if e["at_or_above_ceiling"] else ""
            print(f"{label} | {key} | {_fmt(e['observed'])} -> {_fmt(e['corrected'])} "
                  f"[{_fmt(e['ci_lower'])}, {_fmt(e['ci_upper'])}] "
                  f"(rel_a={_fmt(e['rel_a'])}, rel_b={_fmt(e['rel_b'])}, "
                  f"n={e['n_instances']}){flag}")
        else:
            print(f"{label} | {key} | EXCLUDED ({e['reason']}) "
                  f"obs={_fmt(e['observed'])} rel_a={_fmt(e['rel_a'])} rel_b={_fmt(e['rel_b'])}")
    print(f"{label} | composite | er*={_fmt(group['er_star'])} ep*={_fmt(group['ep_star'])} "
          f"rp*={_fmt(group['rp_star'])} ecs_adj_disattenuated="
          f"{_fmt(group['ecs_adj_disattenuated'])} (n_components={group['n_components']})")


def run(results_dir: Path, ablation_dirs: List[Path]) -> Dict:
    calc = MetricsCalculator()
    records = []
    with open(results_dir / "instance_results.jsonl", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    reliabilities = load_reliabilities(ablation_dirs)

    by_cell: Dict[Tuple[str, str], List[Dict]] = {}
    by_dataset: Dict[str, List[Dict]] = {}
    for rec in records:
        model = MODEL_NAME.get(rec["model"], rec["model"])
        by_cell.setdefault((model, rec["dataset"]), []).append(rec)
        by_dataset.setdefault(rec["dataset"], []).append(rec)
    models = sorted({m for m, _ in by_cell})
    datasets = sorted(by_dataset)
    strategies = list(EVIDENCE_FIELDS)

    output = {
        "provenance": {
            "formula": "Spearman 1904 disattenuation: obs/sqrt(relA*relB)",
            "reliability_floor": RELIABILITY_FLOOR,
            "min_ceiling_n": MIN_CEILING_N,
            "results_dir": str(results_dir),
            "ablation_dirs": [str(d) for d in ablation_dirs],
            "ablation_models": sorted(reliabilities),
            "seed": SEED,
            "n_bootstrap": N_BOOTSTRAP,
            "eps": EPS,
            # Pre-registered note (spec §1.3 step 2): the ablation cohort is the
            # main run's seeded slice (first 50/dataset); at N=50 the subsets
            # coincide, at N=200 the ceilings come from the first 50.
            "ceiling_cohort": "seeded 50/dataset slice of the main run's instances",
        },
        "per_cell": {},
        "per_dataset": {},
        "overall": {},
    }

    for (model, dataset), recs in sorted(by_cell.items()):
        rel = {s: reliabilities.get(model, {}).get(dataset, {}).get(s)
               for s in strategies}
        group = analyze_group(recs, rel, calc)
        output["per_cell"][f"{model}_{dataset}"] = group
        print_group(f"{model}_{dataset}", group)

    for dataset in datasets:
        rel = {s: pool_reliabilities(
            [reliabilities.get(m, {}).get(dataset, {}).get(s) for m in models])
            for s in strategies}
        group = analyze_group(by_dataset[dataset], rel, calc)
        output["per_dataset"][dataset] = group
        print_group(f"pooled_{dataset}", group)

    rel = {s: pool_reliabilities(
        [reliabilities.get(m, {}).get(d, {}).get(s) for m in models for d in datasets])
        for s in strategies}
    group = analyze_group(records, rel, calc)
    output["overall"] = group
    print_group("overall", group)

    # --- Paraphrase-spread sensitivity (2026-07-20) -------------------------------
    # The single-paraphrase design made every ceiling a point estimate, so a rewording
    # that happened to be disruptive for one strategy would inflate that strategy's
    # corrected pairs. With multiple paraphrases we can re-derive the overall table
    # under EACH paraphrase separately and report the range, which is what turns the
    # at-ceiling reading from provisional into a bounded claim.
    variants = sorted({v for m in reliabilities.values() for d in m.values()
                       for s in d.values() for v in s.get("by_variant", {})})
    if len(variants) > 1:
        per_variant: Dict[str, Dict] = {}
        for variant in variants:
            rel_v = {}
            for s in strategies:
                vals: List[float] = []
                for m in models:
                    for d in datasets:
                        e = reliabilities.get(m, {}).get(d, {}).get(s)
                        if e:
                            b = e.get("by_variant", {}).get(variant)
                            if b:
                                vals.extend(b.get("values") or [])
                rel_v[s] = ({"mean": float(np.mean(vals)), "n": len(vals), "values": vals}
                            if vals else None)
            per_variant[variant] = analyze_group(records, rel_v, calc)
            print_group(f"overall[{variant}]", per_variant[variant])
        # Range of the corrected value for each pair across paraphrases.
        spread: Dict[str, Dict] = {}
        for pair in output["overall"]["pairs"]:
            vals = [per_variant[v]["pairs"].get(pair, {}).get("corrected")
                    for v in variants]
            vals = [x for x in vals if x is not None]
            if vals:
                spread[pair] = {
                    "by_variant": {v: per_variant[v]["pairs"].get(pair, {}).get("corrected")
                                   for v in variants},
                    "min": min(vals), "max": max(vals), "range": max(vals) - min(vals),
                    "pooled": output["overall"]["pairs"][pair].get("corrected"),
                }
        output["paraphrase_sensitivity"] = {
            "note": ("Overall table re-derived under each paraphrase's ceilings separately. "
                     "The pooled row of the main table uses all paraphrases' values."),
            "variants": variants,
            "per_variant_overall": per_variant,
            "corrected_spread": spread,
        }
        output["provenance"]["paraphrase_variants"] = variants
        print("\nparaphrase spread (corrected value per pair):")
        for pair, e in spread.items():
            bv = " ".join(f"{v}={_fmt(x)}" for v, x in e["by_variant"].items())
            print(f"  {pair}: {bv} | pooled={_fmt(e['pooled'])} range={_fmt(e['range'])}")

    out_path = results_dir / "disattenuated_agreement.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"Wrote {out_path}")
    return output


def main():
    ap = argparse.ArgumentParser(description="Disattenuated cross-paradigm agreement (Spearman 1904)")
    ap.add_argument("--results-dir", type=Path, required=True,
                    help="Main run dir containing instance_results.jsonl")
    ap.add_argument("--ablation-dirs", type=Path, nargs="+", required=True,
                    help="Ablation dirs (each containing ablation_results.json)")
    args = ap.parse_args()
    run(args.results_dir, args.ablation_dirs)


if __name__ == "__main__":
    main()
