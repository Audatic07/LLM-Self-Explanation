"""Salience-baseline arm (post-hoc erasure control, 2026-07-20).

The arm is only a controlled comparison if its samples are (a) drawn from genuinely
non-consensus tokens and (b) matched to CC3 on BOTH type count and destroyed-token
count. These tests pin both, plus determinism and the aggregation math.
"""
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.normalization.normalizer import Normalizer  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "run_salience_baseline", REPO / "scripts" / "run_salience_baseline.py")
sb = importlib.util.module_from_spec(spec)
sys.modules["run_salience_baseline"] = sb
spec.loader.exec_module(sb)

NORM = Normalizer(use_lemmatization=True, remove_stopwords=True, lemmatizer="wordnet")


def _inst(**kw):
    base = dict(
        instance_id="t1", dataset="sst2", model="m", text="the movie was dull and boring",
        highlighting_tokens=["dull", "boring", "movie"],
        rationale_tokens=["dull", "boring"],
        counterfactual_tokens=["dull"],
        rank_ordering_set=["dull", "boring", "movie"],
        cc3_tokens=["dull", "boring"],
        predicted_label="negative",
    )
    base.update(kw)
    return base


def test_single_strategy_pool_excludes_consensus_and_multi_strategy_tokens():
    """Only tokens named by EXACTLY one strategy qualify; CC3 tokens never do."""
    d = _inst()
    pool = sb.single_strategy_pool(d)
    assert "dull" not in pool and "boring" not in pool   # consensus
    assert "movie" not in pool                            # named by H and RO (count 2)
    # A token only H names is eligible.
    d2 = _inst(highlighting_tokens=["dull", "boring", "movie", "flat"])
    assert "flat" in sb.single_strategy_pool(d2)


def test_single_strategy_pool_is_deterministic():
    d = _inst(highlighting_tokens=["dull", "boring", "zeta", "alpha", "movie"])
    assert sb.single_strategy_pool(d) == sb.single_strategy_pool(d)
    assert sb.single_strategy_pool(d) == sorted(sb.single_strategy_pool(d))


def test_tfidf_pool_excludes_cc3_and_ranks_by_score():
    inst = [_inst(instance_id=f"i{i}", text=t) for i, t in enumerate([
        "the movie was dull and boring",
        "a rare and wonderful film",
        "the film was wonderful",
    ])]
    idf = sb.build_idf(inst, NORM)
    pool = sb.tfidf_pool(_inst(text="a rare and wonderful film", cc3_tokens=["film"]), NORM, idf)
    assert "film" not in pool                    # CC3 excluded
    assert pool, "pool must not be empty"
    # 'rare' appears in 1 of 3 docs, 'wonderful' in 2 -> rare scores higher
    if "rare" in pool and "wonderful" in pool:
        assert pool.index("rare") < pool.index("wonderful")


def test_matched_sample_matches_type_count():
    text = "alpha beta gamma delta epsilon"
    pool = ["alpha", "beta", "gamma", "delta", "epsilon"]
    s = sb.matched_sample(text, pool, n_types=3, target_occ=None, normalizer=NORM)
    assert len(s) == 3


def test_matched_sample_matches_destroyed_token_count():
    """With repeated words, matching on types alone under-destroys; the sample must
    keep taking until it destroys at least as many occurrences as CC3 did."""
    text = "bad bad bad good nice fine great"
    pool = ["good", "nice", "fine", "great"]
    s = sb.matched_sample(text, pool, n_types=1, target_occ=3, normalizer=NORM)
    assert sb.erased_token_count(text, s, NORM) >= 3
    assert len(s) >= 3   # needed >1 type to reach 3 destroyed occurrences


def test_matched_sample_stops_at_pool_exhaustion():
    text = "alpha beta"
    s = sb.matched_sample(text, ["alpha"], n_types=5, target_occ=99, normalizer=NORM)
    assert s == {"alpha"}


def test_matched_sample_is_deterministic():
    text = "alpha beta gamma delta"
    pool = ["alpha", "beta", "gamma", "delta"]
    a = sb.matched_sample(text, pool, 2, 2, NORM)
    b = sb.matched_sample(text, pool, 2, 2, NORM)
    assert a == b


def test_aggregate_paired_math():
    """mean_paired_diff is (CC3 flip - arm flip) averaged over instances where both
    are defined; a positive value means consensus erasure flips more."""
    recs = [
        {"instance_id": "a", "model": "m", "arms": {"ss1": {"mask": False}}},
        {"instance_id": "b", "model": "m", "arms": {"ss1": {"mask": False}}},
        {"instance_id": "c", "model": "m", "arms": {"ss1": {"mask": True}}},
    ]
    cc3 = {("a", "m"): {"mask": True}, ("b", "m"): {"mask": True}, ("c", "m"): {"mask": True}}
    agg = sb.aggregate(recs, cc3, ["mask"], ["ss1"], seed=42)
    e = agg["pooled"]["arms"]["ss1"]["mask"]
    assert e["arm_flip_rate"] == 1 / 3
    assert e["cc3_flip_rate_paired"] == 1.0
    assert abs(e["mean_paired_diff"] - (2 / 3)) < 1e-9
    assert e["n_paired"] == 3


def test_aggregate_skips_undefined_arms():
    recs = [{"instance_id": "a", "model": "m", "arms": {"ss1": {"mask": None}}}]
    agg = sb.aggregate(recs, {}, ["mask"], ["ss1"], seed=42)
    e = agg["pooled"]["arms"]["ss1"]["mask"]
    assert e["arm_flip_rate"] is None and e["n_paired"] == 0


def test_provenance_declares_post_hoc():
    agg = sb.aggregate([], {}, ["mask"], ["ss1"], seed=42)
    assert "POST-HOC" in agg["provenance"]["prereg"]


def test_matched_flag_detects_undermatched_arm():
    """A non-consensus pool smaller than CC3 leaves the arm under-matched; the flag
    must catch it so aggregation can exclude those instances."""
    text = "alpha beta gamma"
    # CC3 has 2 types / 2 occurrences, pool offers only 1 token.
    s = sb.matched_sample(text, ["alpha"], n_types=2, target_occ=2, normalizer=NORM)
    assert len(s) == 1
    assert not (len(s) >= 2 and sb.erased_token_count(text, s, NORM) >= 2)


def test_aggregate_reports_matched_only_subset():
    recs = [
        # under-matched, does not flip -> would drag the arm rate down unfairly
        {"instance_id": "a", "model": "m",
         "arms": {"ss1": {"mask": False, "matched": False, "n_types": 1}}},
        # properly matched, flips
        {"instance_id": "b", "model": "m",
         "arms": {"ss1": {"mask": True, "matched": True, "n_types": 3}}},
    ]
    cc3 = {("a", "m"): {"mask": True}, ("b", "m"): {"mask": True}}
    agg = sb.aggregate(recs, cc3, ["mask"], ["ss1"], seed=42)
    e = agg["pooled"]["arms"]["ss1"]["mask"]
    assert e["arm_flip_rate"] == 0.5           # both instances
    assert e["matched_only"]["arm_flip_rate"] == 1.0   # matched instance only
    assert e["matched_only"]["n_paired"] == 1
    assert e["pct_matched"] == 50.0
