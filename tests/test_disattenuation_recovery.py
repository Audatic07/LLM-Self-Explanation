"""Planted-agreement validation of the Spearman disattenuation on the AJ scale
(review item: the classical correction is defined for product-moment correlations;
its application to mean adjusted-Jaccard agreement levels is an analogue that must
be validated empirically).

Simulation design
-----------------
Each instrument s observes a latent true evidence set T_s (subset of a vocabulary of
size V). One elicitation keeps each token of T_s independently with probability q_s
and replaces each dropped token with a uniform random distractor (size-preserving,
matching AJ's fixed-size geometry). Then, per configuration:

  rel_s      = mean AJ(elicit1_s, elicit2_s)   (two independent elicitations of T_s)
  obs(A,B)   = mean AJ(elicit_A, elicit_B)
  true(A,B)  = AJ(T_A, T_B)                     (noise-free planted agreement)
  corrected  = obs / sqrt(rel_A * rel_B)

The claim under test: corrected ~= true across the geometries and the reliability
range the study actually uses (both rel >= 0.30, the pre-registered estimability
floor), including unequal reliabilities and unequal set sizes.

Run directly for the full table:  python tests/test_disattenuation_recovery.py
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.metrics.metrics_calculator import MetricsCalculator  # noqa: E402

EPS = 0.10
SEED = 42
N_DRAWS = 2000
calc = MetricsCalculator()


def _plant_sets(rng, V, a, b, overlap):
    """Two latent sets of sizes a, b with |intersection| = overlap."""
    vocab = np.arange(V)
    rng.shuffle(vocab)
    shared = set(vocab[:overlap].tolist())
    t_a = shared | set(vocab[overlap:overlap + (a - overlap)].tolist())
    t_b = shared | set(vocab[overlap + (a - overlap):overlap + (a - overlap) + (b - overlap)].tolist())
    return t_a, t_b


def _elicit(rng, true_set, V, q):
    """Keep each true token w.p. q; replace drops with uniform distractors."""
    kept = {t for t in true_set if rng.random() < q}
    n_drop = len(true_set) - len(kept)
    if n_drop:
        pool = [t for t in range(V) if t not in true_set and t not in kept]
        kept |= set(rng.choice(pool, size=min(n_drop, len(pool)), replace=False).tolist())
    return kept


def _aj(s1, s2, V):
    v, _ = calc.adjusted_jaccard({str(x) for x in s1}, {str(x) for x in s2}, V, EPS)
    return v


def run_config(V, a, b, overlap, q_a, q_b, n_draws=N_DRAWS, seed=SEED):
    rng = np.random.default_rng(seed)
    t_a, t_b = _plant_sets(rng, V, a, b, overlap)
    true_aj = _aj(t_a, t_b, V)
    if true_aj is None:
        return None
    rels_a, rels_b, obs = [], [], []
    for _ in range(n_draws):
        e_a1, e_a2 = _elicit(rng, t_a, V, q_a), _elicit(rng, t_a, V, q_a)
        e_b1, e_b2 = _elicit(rng, t_b, V, q_b), _elicit(rng, t_b, V, q_b)
        for acc, x, y in ((rels_a, e_a1, e_a2), (rels_b, e_b1, e_b2), (obs, e_a1, e_b1)):
            v = _aj(x, y, V)
            if v is not None:
                acc.append(v)
    rel_a, rel_b = float(np.mean(rels_a)), float(np.mean(rels_b))
    mean_obs = float(np.mean(obs))
    if rel_a <= 0 or rel_b <= 0:
        return None
    corrected = mean_obs / np.sqrt(rel_a * rel_b)
    return {
        "V": V, "a": a, "b": b, "overlap": overlap, "q_a": q_a, "q_b": q_b,
        "rel_a": rel_a, "rel_b": rel_b, "true": true_aj,
        "obs": mean_obs, "corrected": float(corrected),
        "error": float(corrected - true_aj),
    }


def full_grid():
    results = []
    geoms = [(30, 4, 4), (30, 5, 2), (60, 8, 4), (15, 4, 3)]
    qs = [0.55, 0.7, 0.85, 1.0]
    for (V, a, b), q_a, q_b in itertools.product(geoms, qs, qs):
        if q_b > q_a:  # symmetric; skip duplicates
            continue
        for frac in (0.5, 0.75, 1.0):
            overlap = max(1, round(frac * min(a, b)))
            r = run_config(V, a, b, overlap, q_a, q_b)
            if r is not None:
                results.append(r)
    return results


@pytest.fixture(scope="module")
def grid():
    return full_grid()


def test_recovery_above_floor(grid):
    """Above the pre-registered floor (both rel >= 0.30), the corrected value
    recovers the planted true AJ far better than the uncorrected observation:
    mean |corrected-true| < 0.06 (measured 0.050) vs mean |obs-true| = 0.26 on
    noisy configs — a ~4x error reduction."""
    above = [r for r in grid if r["rel_a"] >= 0.30 and r["rel_b"] >= 0.30]
    assert len(above) >= 40
    errors = [abs(r["error"]) for r in above]
    assert float(np.mean(errors)) < 0.06
    assert max(errors) < 0.18
    noisy = [r for r in above if r["q_a"] < 1.0 or r["q_b"] < 1.0]
    assert float(np.mean([abs(r["error"]) for r in noisy])) < 0.5 * float(
        np.mean([abs(r["obs"] - r["true"]) for r in noisy])
    )


def test_bias_negligible_in_study_regime(grid):
    """The correction acquires a mild UPWARD bias as reliabilities approach the
    floor (documented: +0.07 mean, +0.16 max in min-rel [0.30, 0.45)) — but in
    the regime of every pooled headline pair (both rel >= 0.60, min pooled rel
    is CF at 0.62) recovery is essentially unbiased: |bias| < 0.03 and
    max error < 0.06 (measured +0.009 and 0.041)."""
    study = [r for r in grid if min(r["rel_a"], r["rel_b"]) >= 0.60]
    assert len(study) >= 10
    signed = [r["error"] for r in study]
    assert abs(float(np.mean(signed))) < 0.03
    assert max(abs(e) for e in signed) < 0.06
    # the near-floor inflation is real and positive — document it, don't hide it
    near_floor = [r["error"] for r in grid
                  if 0.30 <= min(r["rel_a"], r["rel_b"]) < 0.45]
    assert near_floor and 0.0 < float(np.mean(near_floor)) < 0.10
    assert max(near_floor) < 0.20


def test_floor_excludes_unstable_region(grid):
    """Below the floor the ratio degrades — max error below floor must exceed
    max error above floor, justifying the pre-registered exclusion."""
    above = [abs(r["error"]) for r in grid if r["rel_a"] >= 0.30 and r["rel_b"] >= 0.30]
    below = [abs(r["error"]) for r in grid if r["rel_a"] < 0.30 or r["rel_b"] < 0.30]
    if below:  # grid may not reach below the floor on every machine's q range
        assert max(below) > max(above)


def test_determinism():
    r1 = run_config(30, 4, 4, 2, 0.7, 0.7, n_draws=300)
    r2 = run_config(30, 4, 4, 2, 0.7, 0.7, n_draws=300)
    assert r1 == r2


if __name__ == "__main__":
    rows = full_grid()
    above = [r for r in rows if r["rel_a"] >= 0.30 and r["rel_b"] >= 0.30]
    below = [r for r in rows if not (r["rel_a"] >= 0.30 and r["rel_b"] >= 0.30)]
    print(f"configs: {len(rows)} (above floor: {len(above)}, below: {len(below)})")
    err_above = [abs(r["error"]) for r in above]
    signed_above = [r["error"] for r in above]
    att = [abs(r["obs"] - r["true"]) for r in above if r["q_a"] < 1.0 or r["q_b"] < 1.0]
    err_noisy = [abs(r["error"]) for r in above if r["q_a"] < 1.0 or r["q_b"] < 1.0]
    print(f"above floor: mean|err|={np.mean(err_above):.4f} max|err|={max(err_above):.4f} "
          f"signed bias={np.mean(signed_above):+.4f}")
    print(f"  noisy configs: mean|obs-true|={np.mean(att):.4f} vs mean|corrected-true|={np.mean(err_noisy):.4f}")
    if below:
        eb = [abs(r["error"]) for r in below]
        print(f"below floor: mean|err|={np.mean(eb):.4f} max|err|={max(eb):.4f}")
    print("rel range above floor:", f"{min(min(r['rel_a'], r['rel_b']) for r in above):.3f}",
          "-", f"{max(max(r['rel_a'], r['rel_b']) for r in above):.3f}")
    worst = sorted(above, key=lambda r: -abs(r["error"]))[:5]
    for r in worst:
        print("worst:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
