"""Semantic soft-matching sensitivity for ECS-adj (W6; ECS_ROBUSTNESS_PLAN §5).

A bounded SENSITIVITY analysis — never the headline metric. It answers review
finding R5/W6: how much of the depressed rationale-pair (R) agreement is *mere
lexical variation* ("terrible" vs "awful", which after lemmatization still miss
under exact-token identity) rather than genuine evidential disagreement?

Method (plan §5, pre-registered constants):

  * soft-Jaccard — unmatched tokens across two evidence sets may partially match
    via a pinned, offline embedding model (``en_core_web_md`` 3.8.0, GloVe 300d).
    Similarities enter a maximum-weight bipartite matching
    (``scipy.optimize.linear_sum_assignment``); a matched pair is credited its
    cosine similarity, but ONLY when cosine ≥ ``tau`` (pre-registered τ = 0.8).
    Exact-token matches always score 1.0. OOV tokens (no vector) can only match
    exactly.
  * chance correction — E[soft-J] is estimated by Monte-Carlo over random
    same-size token sets drawn without replacement from the instance vocabulary
    (the exact hypergeometric form is intractable for *soft* intersections; the
    plan explicitly permits MC with a reported SE for a sensitivity analysis).
  * ceiling — ``J_max = min(a,b)/max(a,b)`` is UNCHANGED from the hard estimator:
    bipartite matching is one-to-one, so the soft-intersection can never exceed
    ``min(a, b)``.
  * soft-AJ = ``(soft_J - E[soft_J]) / (J_max - E[soft_J])`` with the same
    degeneracy guard (``None`` when ``J_max - E[soft_J] < eps``) and the same
    paradigm-balanced ECS-adj aggregation (E-R / E-P / R-P, each 1/3) as the
    primary metric in :class:`MetricsCalculator`.

Design guarantees (asserted in ``tests/test_soft_match.py``):

  * with an embedder that gives distinct tokens cosine < τ, soft-J reduces to the
    hard Jaccard and soft-AJ to the hard adjusted Jaccard — the sensitivity never
    silently diverges from the primary metric when there is nothing to soft-match;
  * nested sets score soft-J = 1 and (given a non-degenerate geometry) soft-AJ = 1;
  * the embedder is injectable, so the estimator is testable without loading spaCy.
"""

import zlib
from functools import lru_cache
from typing import Dict, List, Optional, Sequence, Set, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment


class SpacyVectorEmbedder:
    """Pinned, offline static-vector embedder backed by a spaCy model's vector
    table. Loaded lazily; only the vector table is needed, so the tagger,
    parser, NER, lemmatizer and attribute-ruler pipes are disabled.

    Default model is ``en_core_web_lg`` — a FULL per-key vector table. The
    previous default ``en_core_web_md`` is a 34x PRUNED table (684,830 keys
    mapped onto 20,000 unique vectors, per the official release metadata),
    under which measured cosines are bucket identities, not semantics:
    'increase'/'decrease' share one vector row and 'good'/'bad' score 1.0000
    while the synonym pair 'good'/'great' scores 0.52 (RESEARCH_AUDIT_2026-07-10
    F7). A pruned table therefore credits antonyms at ANY tau and rejects
    synonyms at tau=0.8 — exactly backwards for sentiment evidence. md remains
    loadable for comparison but triggers the pruning warning below.

    Pinning: the resolved model package version IS the provenance — record
    :attr:`descriptor` (which now includes the measured keys/vectors shape) in
    the sensitivity output so the analysis is not a moving target.
    """

    MODEL = "en_core_web_lg"
    VERSION = "3.8.0"

    def __init__(self, model: Optional[str] = None) -> None:
        import spacy  # local import: the module must import without spaCy present

        self.model = model or self.MODEL
        self._nlp = spacy.load(
            self.model,
            disable=["tagger", "parser", "ner", "lemmatizer", "attribute_ruler", "tok2vec"],
        )
        self._vocab = self._nlp.vocab
        try:
            self.version = str(self._nlp.meta.get("version", self.VERSION))
        except Exception:
            self.version = self.VERSION
        vecs = self._vocab.vectors
        self.n_keys = int(len(vecs.key2row))
        self.n_unique_vectors = int(vecs.shape[0])
        self.pruned = self.n_unique_vectors < self.n_keys // 2
        if self.pruned:
            import warnings
            warnings.warn(
                f"{self.model} has a pruned vector table "
                f"({self.n_keys} keys -> {self.n_unique_vectors} unique vectors): "
                "cosines are bucket identities (antonyms can score 1.0). Soft-matching "
                "results under this table are not semantically interpretable (audit F7).",
                stacklevel=2,
            )

    @property
    def descriptor(self) -> str:
        table = f"{self.n_keys} keys/{self.n_unique_vectors} vectors"
        flag = ", PRUNED TABLE" if self.pruned else ""
        return f"{self.model}=={self.version} (static 300d vectors, {table}{flag})"

    def has_vector(self, token: str) -> bool:
        return bool(self._vocab.has_vector(token))

    def similarity(self, a: str, b: str) -> float:
        if a == b:
            return 1.0
        if not (self.has_vector(a) and self.has_vector(b)):
            return 0.0
        va = self._vocab.get_vector(a)
        vb = self._vocab.get_vector(b)
        na = float(np.linalg.norm(va))
        nb = float(np.linalg.norm(vb))
        if na == 0.0 or nb == 0.0:
            return 0.0
        return float(np.dot(va, vb) / (na * nb))


class DictEmbedder:
    """Deterministic embedder for tests: similarities from an explicit dict,
    keyed by frozenset({a, b}); identical tokens are 1.0, unknown pairs 0.0."""

    def __init__(self, sims: Optional[Dict[frozenset, float]] = None) -> None:
        self._sims = dict(sims or {})

    @property
    def descriptor(self) -> str:
        return "dict-embedder (test)"

    def has_vector(self, token: str) -> bool:  # every token is "known" for tests
        return True

    def similarity(self, a: str, b: str) -> float:
        if a == b:
            return 1.0
        return float(self._sims.get(frozenset((a, b)), 0.0))


# Paradigm-balanced ECS-adj aggregation (mirrors
# MetricsCalculator.compute_ecs_adjusted so the soft variant is a drop-in
# comparator on the SAME component structure).
_PAIR_KEYS: List[Tuple[str, str]] = [("H", "R"), ("RO", "R"), ("H", "CF"), ("RO", "CF"), ("R", "CF")]
_ER_PAIRS = [("H", "R"), ("RO", "R")]
_EP_PAIRS = [("H", "CF"), ("RO", "CF")]
_RP_PAIR = ("R", "CF")


class SoftMatcher:
    """Soft-matching ECS-adj sensitivity estimator.

    Parameters mirror the pre-registered constants; ``tau`` and ``eps`` default
    to the plan's values (0.8, 0.10). ``mc_draws`` is the Monte-Carlo sample size
    for the chance correction; ``seed`` fixes it for reproducibility.
    """

    def __init__(self, embedder, tau: float = 0.8, eps: float = 0.10,
                 mc_draws: int = 1000, seed: int = 42) -> None:
        self.embedder = embedder
        self.tau = float(tau)
        self.eps = float(eps)
        self.mc_draws = int(mc_draws)
        self.seed = int(seed)
        # (a, b) unordered similarity cache — MC draws repeat token pairs heavily.
        self._sim_cache: Dict[frozenset, float] = {}

    # ------------------------------------------------------------------ core
    def _sim(self, a: str, b: str) -> float:
        if a == b:
            return 1.0
        key = frozenset((a, b))
        cached = self._sim_cache.get(key)
        if cached is None:
            cached = float(self.embedder.similarity(a, b))
            self._sim_cache[key] = cached
        return cached

    def soft_intersection(self, set1: Sequence[str], set2: Sequence[str]) -> float:
        """Max-weight bipartite matching credit between two token sets, with
        below-τ similarities zeroed. Returns the summed matched credit
        (0 ≤ result ≤ min(|set1|, |set2|))."""
        a = list(dict.fromkeys(set1))  # dedupe, preserve order (sets are unordered anyway)
        b = list(dict.fromkeys(set2))
        if not a or not b:
            return 0.0
        # Credit matrix: similarity when ≥ τ, else 0. Exact matches -> 1.0 via _sim.
        credit = np.zeros((len(a), len(b)), dtype=float)
        for i, ta in enumerate(a):
            for j, tb in enumerate(b):
                s = self._sim(ta, tb)
                if s >= self.tau:
                    credit[i, j] = s
        if not credit.any():
            return 0.0
        # Maximise total credit -> minimise negative credit.
        rows, cols = linear_sum_assignment(-credit)
        return float(credit[rows, cols].sum())

    def soft_jaccard(self, set1: Sequence[str], set2: Sequence[str]) -> float:
        a = len(set(set1))
        b = len(set(set2))
        if a == 0 or b == 0:
            return 0.0
        inter = self.soft_intersection(set1, set2)
        union = a + b - inter
        return (inter / union) if union > 0 else 0.0

    def expected_soft_jaccard(self, size_a: int, size_b: int,
                              vocab_tokens: Sequence[str]) -> Tuple[float, float]:
        """Monte-Carlo E[soft-J] and its SE for two random same-size token sets
        drawn without replacement from ``vocab_tokens``. Soft-matching lifts
        chance agreement too, so this null is (correctly) ≥ the hard E[J]."""
        vocab = list(dict.fromkeys(vocab_tokens))
        V = len(vocab)
        a = min(int(size_a), V)
        b = min(int(size_b), V)
        if V <= 0 or a <= 0 or b <= 0:
            return 0.0, 0.0
        # Decorrelated, content-stable seeding (audit F8): re-seeding with the
        # SAME fixed seed on every call made every same-geometry pair reuse
        # identical draw patterns, so MC errors were shared across instances and
        # did not average out — the pooled soft-AJ mean swung ~±0.03 between
        # master seeds while each pair reported a tiny SE. Spawning a child seed
        # from (master seed, a, b, crc32 of the vocab contents) keeps runs
        # reproducible while making draws independent across pairs/instances.
        vocab_key = zlib.crc32("\x1f".join(vocab).encode("utf-8"))
        rng = np.random.default_rng(
            np.random.SeedSequence([self.seed, a, b, vocab_key]))
        idx = np.arange(V)
        vals = np.empty(self.mc_draws, dtype=float)
        for t in range(self.mc_draws):
            sa = [vocab[i] for i in rng.choice(idx, size=a, replace=False)]
            sb = [vocab[i] for i in rng.choice(idx, size=b, replace=False)]
            vals[t] = self.soft_jaccard(sa, sb)
        mean = float(vals.mean())
        se = float(vals.std(ddof=1) / np.sqrt(self.mc_draws)) if self.mc_draws > 1 else 0.0
        return mean, se

    def soft_adjusted_jaccard(self, set1: Sequence[str], set2: Sequence[str],
                              vocab_tokens: Sequence[str]) -> Tuple[Optional[float], bool, Dict[str, float]]:
        """Soft analogue of :meth:`MetricsCalculator.adjusted_jaccard`.

        Returns ``(value, degenerate, extras)`` where ``extras`` carries the
        diagnostic pieces (soft_j, e_soft_j, e_soft_j_se, j_max) so callers can
        report the MC SE. ``value`` is ``None`` when either set is empty or the
        geometry is degenerate (``J_max - E[soft_J] < eps``)."""
        a, b = len(set(set1)), len(set(set2))
        extras: Dict[str, float] = {}
        if a == 0 or b == 0 or not vocab_tokens:
            return None, True, extras
        soft_j = self.soft_jaccard(set1, set2)
        e_soft_j, e_se = self.expected_soft_jaccard(a, b, vocab_tokens)
        j_max = min(a, b) / max(a, b)
        denom = j_max - e_soft_j
        extras = {"soft_j": soft_j, "e_soft_j": e_soft_j, "e_soft_j_se": e_se, "j_max": j_max}
        if denom < self.eps:
            return None, True, extras
        return (soft_j - e_soft_j) / denom, False, extras

    def soft_ecs_adjusted(self, explanations: Dict[str, Set[str]],
                          vocab_tokens: Sequence[str]) -> Dict[str, object]:
        """Paradigm-balanced soft ECS-adj, structurally identical to
        :meth:`MetricsCalculator.compute_ecs_adjusted` but over soft-AJ pairs.

        Returns the same keys (``ecs_adj_er/ep/rp``, ``ecs_adj``,
        ``ecs_adj_n_components``, ``ecs_adj_complete``, ``n_degenerate_pairs``)
        plus ``pair_soft_aj`` (per-pair soft-AJ, ``None`` where degenerate/empty)."""
        aj: Dict[Tuple[str, str], float] = {}
        pair_soft_aj: Dict[str, Optional[float]] = {}
        n_degenerate = 0
        for (s1, s2) in _PAIR_KEYS:
            set1 = explanations.get(s1) or set()
            set2 = explanations.get(s2) or set()
            if not set1 or not set2:
                pair_soft_aj[f"{s1}_{s2}"] = None
                continue
            val, degenerate, _ = self.soft_adjusted_jaccard(set1, set2, vocab_tokens)
            if degenerate:
                n_degenerate += 1
            pair_soft_aj[f"{s1}_{s2}"] = val
            if val is not None:
                aj[(s1, s2)] = val

        def _mean_of(keys: List[Tuple[str, str]]) -> Optional[float]:
            vals = [aj[k] for k in keys if k in aj]
            return float(np.mean(vals)) if vals else None

        er = _mean_of(_ER_PAIRS)
        ep = _mean_of(_EP_PAIRS)
        rp = aj.get(_RP_PAIR)

        components = [c for c in (er, ep, rp) if c is not None]
        ecs_adj = float(np.mean(components)) if components else None
        complete = er is not None and ep is not None and rp is not None

        return {
            "ecs_adj_er": er,
            "ecs_adj_ep": ep,
            "ecs_adj_rp": rp,
            "ecs_adj": ecs_adj,
            "ecs_adj_n_components": len(components),
            "ecs_adj_complete": complete,
            "n_degenerate_pairs": n_degenerate,
            "pair_soft_aj": pair_soft_aj,
        }
