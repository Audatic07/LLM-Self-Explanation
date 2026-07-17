# Experiment Report: llm-explanation-agreement-study

- **Date:** 2026-07-16 21:03:54
- **Instance processing span:** 97.9s (1.6m) — first-to-last instance timestamp; see execution_summary.txt for total run wall-clock
- **Models (3):** nova-pro (`eu.amazon.nova-pro-v1:0`), qwen3-235b (`qwen.qwen3-235b-a22b-2507-v1:0`), deepseek-v3 (`deepseek.v3-v1:0`)
- **Total instances:** 15
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 81780
- **Avg tokens per instance:** 5452

## Per-Dataset Summary

| Model | Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|-------|---------|-----------|----------|----------|---|---|------|---|
| nova-pro | cad_imdb | 5 | 4/5 (80%) | 0.223 | 100% | 100% | 100% | 100% |
| qwen3-235b | cad_imdb | 5 | 5/5 (100%) | 0.266 | 80% | 100% | 100% | 100% |
| deepseek-v3 | cad_imdb | 5 | 5/5 (100%) | 0.315 | 100% | 100% | 100% | 100% |

*H/R/CF/RO columns are validity rates (parsed AND passed validation), not raw parse rates.*

### Complete-Case ECS-adj by Cell (N=6 minimum — PRIMARY estimand)

Chance- and ceiling-adjusted, paradigm-balanced ECS-adj over instances where all three paradigm components are defined, per model×dataset cell. This is the primary estimand at scale; the pooled number mixes cells whose complete-case membership can differ by an order of magnitude, so pooling alone is not a safe substitute for it.

| Model | Dataset | Complete cases | Mean ECS-adj (complete) |
|-------|---------|-----------------|--------------------------|
| nova-pro | cad_imdb | 4/5 (below N=6) | 0.2742* |
| qwen3-235b | cad_imdb | 5/5 (below N=6) | 0.4791* |
| deepseek-v3 | cad_imdb | 5/5 (below N=6) | 0.5323* |

*Estimate shown, not a well-powered cell (fewer than 6 complete cases).*

### Complete-Case ECS by Cell (N=6 minimum — legacy ECS, DEPRECATED)

Legacy flat 5-pair-mean ECS over instances where H, R, CF, and RO all produced valid evidence, per model×dataset cell. **Deprecated** (superseded by the ECS-adj table above); retained for comparison with earlier reports only.

| Model | Dataset | Complete cases | Mean ECS (complete) |
|-------|---------|-----------------|----------------------|
| nova-pro | cad_imdb | 5/5 (below N=6) | 0.2228* |
| qwen3-235b | cad_imdb | 4/5 (below N=6) | 0.2929* |
| deepseek-v3 | cad_imdb | 5/5 (below N=6) | 0.3146* |

*Estimate shown, not a well-powered cell (fewer than 6 complete cases).*

## Sampling Log

| Model | Dataset | Requested | Sampled | Wrong Pred |
|-------|---------|-----------|---------|------------|
| nova-pro | cad_imdb | 5 | 5 | 1 |
| qwen3-235b | cad_imdb | 5 | 5 | 0 |
| deepseek-v3 | cad_imdb | 5 | 5 | 0 |
| **Total** | | 15 | 15 | 1 |

**Note:** Instances with a defined ECS (N=15 of 15 sampled), by length: short (≤20 words) N=0; medium (21–50) N=3; long (>50) N=12. Legacy (raw) ECS may partly reflect brevity; the primary ECS-adj strata below test whether that confound survives the chance+ceiling adjustment (P1.2).

**Short-vocab flag (provenance, not a filter — P1.2):** 0 instances have ≤20 unique normalized tokens (`short_vocab`). In raw ECS these degenerate inputs yield inflated/trivial agreement via near-identical evidence across strategies — a confound the ECS-adj chance+ceiling adjustment is designed to remove. The flag is retained for provenance/auditing, but it is NOT a "conservative-estimate" filter: post-P0.1 the normalized-vocab threshold of 20 flags the majority of SST-2 and MNLI instances (median normalized vocab there is ~9–11), so filtering on it would be an AG-News-only estimate wearing a robustness costume. The vocab strata below are reported on the primary (ECS-adj) scale, and the continuous vocab↔ECS-adj relationship is the honest presentation.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=14)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

**Sensitivity analysis — free-CF ECS (N=14):** 0.2506. Minimal-CF ECS (above) is the primary estimand because minimality is part of the CF construct (MiCE) — this is a robustness check, recomputed with the unconstrained/free CF rewrite (`cf_contrast_tokens`, substantially higher validity than the minimal-edit gate) substituted for CF's evidence, over instances where H, R, and RO are valid and the free CF also produced evidence. Pure post-processing of already-collected data — zero additional API cost. Missingness in the primary (minimal-CF) analysis is MNAR (validity depends on how easy a minimal edit is to find), which is precisely why this sensitivity analysis exists: it shows whether the ECS-level conclusions survive when the perturbation paradigm isn't gated by the minimal-edit constraint.

**Sensitivity analysis — free-CF ECS-adj (PRIMARY scale, P0.3):** complete-case +0.4380 (N=10); available-component +0.3759 (N=14). Because ECS-adj is now the primary estimand (Decision D1), the plan §3.4 MNAR robustness check must also exist on the chance- AND ceiling-corrected scale, not only on the deprecated flat ECS above. Same substitution (free CF rewrite for the minimal-CF evidence), scored with the AJ estimator. Zero additional API cost; descriptive robustness check, not NHST-tested. A positive complete-case value here means the primary conclusion survives removing the minimal-edit gate.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 14/15 | 93% |
| Rationale | 15/15 | 100% |
| Counterfactual | 15/15 | 100% |
| Rank Ordering | 15/15 | 100% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

> **Pooled across models and datasets — descriptive context only.** The primary reporting unit is the model×dataset cell (tables below): pooled numbers mix heterogeneous tasks and models, and their bootstrap CI resamples instance clusters (the same instance appears under every model). At scale, **complete-case ECS-adj is the primary estimand** (Decision D1); legacy ECS below is **deprecated**, retained for comparison. Partial-case composites average whichever pairs survived, which changes the construct per instance.

| Metric | Value |
|--------|-------|
| Mean ECS (complete cases, N=14) — DEPRECATED (legacy) | 0.2756 |
| Complete cases | 14/15 (93%) |
| Mean ECS (all with ≥3 valid, N=15) | 0.2678 |
| Mean ECS-overlap (size-robust secondary, same pairs) | 0.6656 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.2060 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.3760 |
| Std ECS | 0.1734 |
| Median ECS | 0.2192 |
| Mean ECS lift over chance (ECS − uniform random) — DEPRECATED (legacy) | +0.1791 |
| Mean ECS random baseline (uniform) | 0.0887 |
| Mean ECS lift over salience-weighted null (legacy secondary, N=14) | +0.1557 |

> **ECS-adj** (ECS_ROBUSTNESS_PLAN_2026-07-05.md) — the **PRIMARY** consensus estimand (Decision D1, 2026-07-07): chance- AND ceiling-adjusted, paradigm-balanced, replacing the deprecated flat 5-pair-mean ECS above. 0 = chance, 1 = maximum agreement achievable given each pair's set sizes. Adopted after its validation gates passed (planted-agreement simulation, pilot rescore, property tests — plan §6).

| Metric | Value |
|--------|-------|
| **Mean ECS-adj (complete cases, N=14) — PRIMARY estimand** | 0.4396 |
| Mean ECS-adj (available-component, N=15) | 0.4508 |
| Mean ECS-adj E-R (extraction-rationalization) | 0.3261 |
| Mean ECS-adj E-P (extraction-perturbation) | 0.7166 |
| Mean ECS-adj R-P (rationalization-perturbation) | 0.2883 |

> **Non-nested Ns (P2):** legacy ECS is defined for N=15 rows (≥3 valid strategies) and available-component ECS-adj for N=15 rows — these populations OVERLAP but are NOT nested. ECS-adj degrades gracefully per component, so it can be defined below the ≥3-valid gate; conversely an all-degenerate instance loses ECS-adj while keeping legacy ECS. The two counts are therefore not expected to reconcile.

> **Component-subset caveat (P2):** the available-component E-R / E-P / R-P means above are each computed over a DIFFERENT subset of instances (E-P and R-P exist only where a valid CF was elicited — a heavily selected minority; E-R exists far more often). Do not compare the E-R vs E-P *available* means directly as if within-instance. The complete-case ECS-adj table is the clean within-instance comparison across all three paradigm pairs.
| Degenerate pairs (J_max - E[J] < eps) | 8 |

> **AJ floor & test conservativeness (P1.4).** AJ is NOT bounded below by −1: the floor is −E[J]/(J_max−E[J]), asymmetric by design (pilot minimum pair value ≈ −1.5). So the AJ null distribution is left-skewed — bounded above at +1 with a long negative tail — which makes the one-sided sign-flip test for `mean > 0` **conservative** (a documented property of the estimator, not a discovered one). Consequently a **negative cell mean** (which can occur in tiny-N cells) must never be read as a "below-chance magnitude": the floor asymmetry means negative values are not on the same scale as positive ones. Report negative cell means as "not above chance at this N", never as a signed effect size.

> **Significance testing: pre-registered tests only.** The pre-registered families: (a) PRIMARY — sign-flip permutation on per-instance ECS-adj > 0 (null=0 by construction, plan §3.5) on the **complete-case** population per model×dataset cell, Holm-corrected across cells (Decision D1; the estimand/test population was aligned in the 2026-07-08 P0.1 amendment); (a2) SENSITIVITY — the same test on the available-component pool (wider N, but >half its rows are a single-paradigm-pair statement); (b) CC-erasure vs random control in the separate erasure pass. Both (a) and (a2) tables are below. Every other number in this report — strata, splits, contrasts — is descriptive, and cells below the configured minimum N report estimates without a test. The legacy sign-flip test on mean ECS-lift > 0 is **deprecated**, retained below for comparison with earlier reports only.

| Metric | Value |
|--------|-------|
| Introduced-concept rate (R) | 0.656 |
| CF canonical (minimal) validity rate | 100% |
| CF canonical validity — first attempt (single-shot, uncoached) | 100% |
| CF valid only after correction loop (coached stratum) | 0 instances |
| RO required hallucination self-correction | 0 instances |
| CF contrast (free) validity rate | 100% |
| CF canonical (minimal) minimality (edits/len) | 0.106 |
| CF contrast (free) minimality (edits/len) | 0.203 |
| Verbalized confidence — mean (ECS-paired, N=15) | 0.905 |
| Mean CC3 size | 4.47 |
| Mean CC4 size | 1.73 |
| % instances with CC3 | 93.3% |
| % instances with CC4 | 60.0% |

> The CF minimal-vs-free validity contrast replicates the validity–minimality trade-off of arXiv:2509.09396 (*LLMs Don't Know Their Own Decision Boundaries*): unconstrained rewrites flip reliably but over-edit; minimal edits often fail to flip. Single-shot rates are reported separately from the coached loop because the correction re-prompt makes headline rates multi-shot-search rates (not comparable to single-shot elicitation in Madsen et al. 2024 / MiCE).

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Legacy test (DEPRECATED): mean ECS-lift > 0, per model×dataset cell

One-sided sign-flip permutation on per-instance (ECS − ECS_random) differences; Holm-corrected across this run's cells. `—` = cell below the configured minimum N for testing (estimate reported, test skipped). **Deprecated** — superseded by the ECS-adj test below (Decision D1); retained for comparison with earlier reports only.

| Model | Dataset | N (lift) | Mean lift | p (raw) | p (Holm) |
|-------|---------|----------|-----------|---------|----------|
| nova-pro | cad_imdb | 5 | +0.1338 | — | — |
| qwen3-235b | cad_imdb | 5 | +0.1877 | — | — |
| deepseek-v3 | cad_imdb | 5 | +0.2160 | — | — |

### Pre-registered test (a): mean ECS-adj > 0 on COMPLETE CASES, per cell (PRIMARY)

The PRIMARY pre-registered test (Decision D1; estimand/test alignment fixed in the 2026-07-08 P0.1 amendment): one-sided sign-flip permutation applied directly to per-instance ECS-adj on the **complete-case** population (all three paradigm components defined) — the same population as the primary estimand. AJ's null is 0 by construction (plan §3.5), so no baseline subtraction is needed. Holm-corrected across this run's cells; `—` = cell below the configured minimum N.

| Model | Dataset | N (complete) | Mean ECS-adj (complete) | p (raw) | p (Holm) |
|-------|---------|--------------|--------------------------|---------|----------|
| nova-pro | cad_imdb | 4 | +0.2742 | — | — |
| qwen3-235b | cad_imdb | 5 | +0.4791 | — | — |
| deepseek-v3 | cad_imdb | 5 | +0.5323 | — | — |

*Complete-case = all 3 paradigm components defined; this does NOT mean degeneracy-free: 6/14 complete-case instances contain ≥1 degeneracy-guarded pair (a component rested on its other pair). This is by design (ECS_ROBUSTNESS_PLAN §3.4, corrected in the 2026-07-08 amendment).*

### Sensitivity test (a2): mean ECS-adj > 0 on AVAILABLE components, per cell

The wider-N robustness companion to (a): the same one-sided sign-flip test on the **available-component** ECS-adj (every row with a defined ECS-adj, regardless of how many components survived). This has larger N but, for more than half its rows, is a statement about above-chance agreement across *whichever* paradigm pairs were elicitable (predominantly extraction↔rationalization) — not the full three-paradigm construct. Reported as sensitivity, never as the headline. Holm-corrected as its own family; `—` = cell below the configured minimum N.

| Model | Dataset | N (available) | Mean ECS-adj (available) | p (raw) | p (Holm) |
|-------|---------|---------------|---------------------------|---------|----------|
| nova-pro | cad_imdb | 5 | +0.3410 | — | — |
| qwen3-235b | cad_imdb | 5 | +0.4791 | — | — |
| deepseek-v3 | cad_imdb | 5 | +0.5323 | — | — |

### ECS by prediction correctness (per cell only)

Reported per model×dataset cell only — pooled, this contrast is confounded by cell composition. Descriptive; no test.

| Model | Dataset | Mean ECS correct (N) | Mean ECS incorrect (N) |
|-------|---------|----------------------|------------------------|
| nova-pro | cad_imdb | 0.2680 (4) | 0.0420 (1) |
| qwen3-235b | cad_imdb | 0.2661 (5) | — (0) |
| deepseek-v3 | cad_imdb | 0.3146 (5) | — (0) |

### Verbalized confidence ↔ ECS (Spearman, per cell)

Association estimate with a seeded bootstrap CI (pre-registered as an estimate, not a hypothesis test). Confidence is the model's verbalized 0–100 probability that its classification is correct (Tian et al. 2023; Xiong et al. 2024).

**Restricted range / heavy ties (P2):** verbalized confidence is severely range-restricted — a large share of instances answer exactly 0.95 and the observed range is roughly 0.7–1.0. This is an expected-null descriptive association under heavy ties, NOT a calibration finding; τ-b (tie-robust) is reported precisely because ρ is fragile under this concentration. Do not interpret the sign of ρ as evidence that confidence tracks consistency.
Kendall τ-b is a tie-robust companion to Spearman ρ (review P2.2) — descriptive, pre-specified alongside ρ, not a replacement or a separate test. Confidence concentrates heavily near {0.9–1.0}, so heavy ties make ρ (and its CI) fragile; τ-b corrects for ties directly rather than treating them as ordinary rank gaps.

| Model | Dataset | N pairs | Spearman ρ | 95% CI | Kendall τ-b |
|-------|---------|---------|------------|--------|-------------|
| nova-pro | cad_imdb | 5 | 0.000 | [0.000, 0.000] | — |
| qwen3-235b | cad_imdb | 5 | 0.872 | [0.111, 1.000] | 0.738 |
| deepseek-v3 | cad_imdb | 5 | 0.632 | [-0.968, 1.000] | 0.447 |

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) | N instances |
|------|----------------------|----------------|-------------|
| H–R | 0.8193 | 0.1734 | 14 |
| H–CF | 0.8066 | 0.3721 | 14 |
| H–RO | 0.9714 | 0.2245 | 14 |
| R–CF | 0.4639 | 0.1764 | 15 |
| R–RO | 0.3956 | 0.2501 | 15 |
| CF–RO | 0.8800 | 0.3825 | 15 |

### Rank-Based Agreement (H vs RO)

| Metric | Value | N |
|--------|-------|---|
| RBO (H,RO) | 0.3557 | 14 |
| Kendall τ (H,RO) | 0.2381 | 14 |
| Normalized τ | 0.6190 | 14 |

*Kendall τ requires ≥4 overlapping ranked tokens (undefined below that, see per-instance tables); N here is the count of instances where it was defined, not the full sample.*

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — and its cross-paradigm mean is the `ECS-overlap` secondary composite. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking (both rankings live in the same normalized token space); Kendall τ provides a complementary rank correlation measure.

## Cross-Model Agreement (same strategy, different models)

For every instance run under ≥2 models: the agreement between DIFFERENT models' evidence sets for the SAME strategy, next to the within-model cross-strategy consensus of the same instances. If within-model consensus systematically exceeds cross-model same-strategy agreement, stated evidence tracks model-specific computation (privileged self-knowledge, arXiv:2602.02639); if not, it is closer to a generic task prior shared across models (cf. the cross-model explanation lottery, arXiv:2603.15821). Zero extra API calls; descriptive.

> **Scale (P0.2, 2026-07-08):** the HEADLINE contrast is on the **adjusted (AJ)** scale — the same chance- AND ceiling-corrected estimator ECS-adj uses. The raw-Jaccard table further below is a set-size-confounded **descriptive companion only**: same-strategy pairs have similar set sizes and a high Jaccard ceiling, while the within-model cross-paradigm pairs have dissimilar sizes and a structurally capped ceiling, so part of the raw gap is geometry rather than agreement. Under AJ the pilot gap roughly halves and at least one dataset's paired CI includes 0.

### Adjusted (AJ) — headline

| Dataset | N instances | H | R | CF | RO | Cross-model mean (AJ) | Within-model mean ECS-adj |
|---------|-------------|---|---|----|----|------------------------|----------------------------|
| cad_imdb | 5 | +0.348 (13) | +0.663 (14) | +0.787 (15) | +0.484 (15) | +0.577 | +0.451 |

#### Paired Per-Instance Contrast (AJ) — headline

Δ = (instance's own cross-model same-strategy mean AJ) − (that same instance's own within-model mean ECS-adj), paired within-instance and bootstrapped. Descriptive pre-specified estimate, not a hypothesis test.

| Dataset | N | Mean Δ (AJ) | 95% CI | Direction |
|---------|---|-------------|--------|-----------|
| cad_imdb | 5 | +0.1296 | [+0.0344, +0.2130] | Cross-model exceeds within-model |

**Observed direction (AJ):** on the adjusted scale, cross-model same-strategy agreement exceeds within-model cross-strategy ECS-adj in every dataset (Δ CI entirely above 0) — evidence for a generic task prior shared across models over privileged self-knowledge (cf. the cross-model explanation lottery, arXiv:2603.15821). The raw-Jaccard companion below overstates this gap (~2×); read the adjusted numbers as the effect.

### Raw Jaccard — descriptive companion (set-size confounded; DEPRECATED comparator)

Raw Jaccard for the cross-model side against the **deprecated** legacy ECS for the within side. Retained for comparison with earlier reports; the AJ table above is the honest contrast. Do not cite these numbers as the effect size.

| Dataset | N instances | H | R | CF | RO | Cross-model mean | Within-model mean ECS |
|---------|-------------|---|---|----|----|------------------|------------------------|
| cad_imdb | 5 | 0.538 (13) | 0.411 (15) | 0.661 (15) | 0.504 (15) | 0.528 | 0.268 |

| Dataset | N | Mean Δ (raw) | 95% CI | Direction |
|---------|---|-------------|--------|-----------|
| cad_imdb | 5 | +0.2574 | [+0.2192, +0.2955] | Cross-model exceeds within-model |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 14/15 (93%) | 14/15 (93%) |
| Rationale | 15/15 (100%) | 15/15 (100%) |
| Counterfactual (JSON parsed) | 15/15 (100%) |
| Counterfactual (rules compliant) | 15/15 (100%) |
| Counterfactual (flip verified) | 15/15 (100%) |
| Rank Ordering | 15/15 (100%) | 15/15 (100%) |
| All 4 valid | 14/15 |
| 3 valid (CC3 adjusted) | 1/15 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

Primary (ECS-adj) alongside legacy (raw ECS). The **legacy** column is where the brevity confound lives (short inputs score high on raw agreement); the **ECS-adj** column is the primary scale, where the chance+ceiling adjustment removes that confound. If the raw gradient (short highest) does not reproduce under ECS-adj, the old "ECS may reflect brevity" caveat describes the deprecated metric only (P1.2).

| Length | N (ECS-adj) | Mean ECS-adj | N (legacy) | Mean ECS (legacy) |
|--------|-------------|--------------|------------|-------------------|
| Short (≤20 words) | 0 | +0.0000 | 0 | 0.0000 |
| Medium (21–50) | 3 | +0.6997 | 3 | 0.5773 |
| Long (>50 words) | 12 | +0.3886 | 12 | 0.1905 |


### ECS by Vocabulary Size

Primary (ECS-adj) alongside legacy (raw ECS). Raw ECS is inflated for short-vocab instances (chance and ceiling nearly coincide there); ECS-adj corrects exactly that. The short-vocab flag is a provenance marker, not a conservative-estimate filter (see the note above) — do not read the normal-vocab column as "the conservative estimate" (P1.2).

| Vocab Bucket | N (ECS-adj) | Mean ECS-adj | N (legacy) | Mean ECS (legacy) |
|--------------|-------------|--------------|------------|-------------------|
| Normal vocab (>20 unique tokens) | 15 | +0.4508 | 15 | 0.2678 |
| Short vocab (≤20 unique tokens) | 0 | +0.0000 | 0 | 0.0000 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2678 | [0.1615, 0.4239] |

## Per-Instance Details

### cad_imdb_dev_000284 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{
  "label": "positive"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 110 words
- **Raw response length:** 25 chars
- **Prompt hash:** `973c726ddbbfd9e7`
- **ECS (full):** 0.1870
- **ECS (extraction–rationale):** 0.0217
- **ECS (extraction–perturbation):** 0.4457
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 0

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{
  "confidence": 95
}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Well,", 3],
    ["what", 3],
    ["can", 3],
    ["it", 3],
    ["be", 3],
    ["said", 3],
    ["about", 3],
    ["this", 5],
    ["fabulous", 8],
    ["thing?", 5],
    ["I", 5],
    ["watched", 6],
    ["it", 3],
    ["because", 5],
    ["it", 3],
    ["aired", 5],
    ["on", 3],
    ["cable.", 3],
    ["I", 5],
    ["loved", 8],
    ["it.", 3],
    ["The", 5],
    ["creature", 8],
    ["is", 3],
    ["the", 3],
    ["scariest", 8],
    ["you", 3],
    ["can", 3],
    ["get!", 5],
    ["Please,", 3],
    ["you", 3],
    ["need", 5],
    ["to", 3],
    ["be", 3],
    ["very", 6],
    ["generous", 8],
    ["not", 5],
    ["to", 3],
    ["get", 5],
    ["scared", 8],
    ["by", 3],
    ["the", 3],
    ["amazing", 8],
    ["Halloween", 6],
    ["costume.", 5],
    ["Oh", 3],
    ["well,", 3],
    ["there", 5],
    ["are", 3],
    ["also", 5],
    ["displays", 6],
    ["of", 3],
    ["great", 8],
    ["acting,", 6],
    ["f/x,", 6],
    ["and", 3],
    ["dialogues.", 5],
    ["The", 5],
    ["confrontation", 8],
    ["with", 5],
    ["the", 3],
    ["creature", 8],
    ["is", 3],
    ["unbelievable,", 8],
    ["you", 3],
    ["can't", 5],
    ["get", 5],
    ["a", 3],
    ["more", 6],
    ["amazing", 8],
    ["scene.", 5],
    ["This", 5],
    ["is", 3],
    ["the", 3],
    ["best", 8],
    ["you", 3],
    ["can", 3],
    ["get", 5],
    ["from", 5],
    ["direct", 6],
    ["to", 3],
    ["video", 6],
    ["flicks.", 5],
    ["\"", 3],
    ["Creature", 8],
    ["Unknown", 8],
    ["\"", 3],
    ["makes", 6],
    ["FULL", 8],
    ["MOON", 8],
    ["PICTURES", 8],
    ["movies", 6],
    ["look", 6],
    ["like", 5],
    ["\"", 3],
    ["Halloween", 8],
    ["\".", 3],
    ["I", 5],
    ["recommend", 8],
    ["at", 3],
    ["all", 5],
    ["costs,", 5],
    ["please.", 5],
    ["The", 5],
    ["only", 6],
    ["\"", 3],
    ["negative", 8],
    ["\"", 3],
    ["thing", 6],
    ["about", 5],
    ["this", 5],
    ["great", 8],
    ["movie", 8],
    ["are", 3],
    ["the", 3],
    ["women.", 5]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `amaze`, `best`, `confrontation`, `creature`, `direct`, `display`, `f/x`, `fabulous`, `full`, `generous`, `great`, `halloween`, `love`, `moon`, `movie`, `picture`, `recommend`, `scar`, `scary`, `unbelievable`, `unknown`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text contains overwhelmingly positive language and enthusiastic recommendations about the movie, despite a minor critique about the women in it."
}
```

**Rationale text:**
> The text contains overwhelmingly positive language and enthusiastic recommendations about the movie, despite a minor critique about the women in it.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `movie`, `woman`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "Well, what can it be said about this dreadful thing? I watched it because it aired on cable. I hated it. The creature is the least scary you can get! Please, you need to be very critical not to be bored by the terrible Halloween costume. Oh well, there are also displays of poor acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more disappointing scene. This is the worst you can get from direct to video flicks. \"Creature Unknown\" makes FULL MOON PICTURES movies look like \"Halloween\". I discourage at all costs, please. The only \"negative\" thing about this awful movie are the women.",
  "new_prediction": "negative"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> Well, what can it be said about this dreadful thing? I watched it because it aired on cable. I hated it. The creature is the least scary you can get! Please, you need to be very critical not to be bored by the terrible Halloween costume. Oh well, there are also displays of poor acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more disappointing scene. This is the worst you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I discourage at all costs, please. The only "negative" thing about this awful movie are the women.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amaze`, `best`, `fabulous`, `generous`, `get`, `great`, `love`, `recommend`, `scar`, `scary`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{
  "ranking": [
    "loved",
    "amazing",
    "great",
    "recommend",
    "scariest"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `amaze`(2), `great`(3), `recommend`(4), `scary`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.0435 |
| H–CF | 0.9000 | 0.3913 |
| H–RO | 1.0000 | 0.2273 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 1.0000 | 0.5000 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.6000 |
| Normalized τ | 0.8000 |
| RBO (H,RO) | 0.2204 |

### cad_imdb_test_000501 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{
  "label": "positive"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 190 words
- **Raw response length:** 25 chars
- **Prompt hash:** `ebd4951c603a1d3d`
- **ECS (full):** 0.1489
- **ECS (extraction–rationale):** 0.0263
- **ECS (extraction–perturbation):** 0.3127
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 0

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{
  "confidence": 95
}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["This", 5],
    ["film", 9],
    ["is", 5],
    ["the", 4],
    ["best", 8],
    ["motion", 7],
    ["picture", 7],
    ["I", 5],
    ["have", 6],
    ["EVER", 8],
    ["seen.", 7],
    ["To", 5],
    ["begin,", 5],
    ["I'd", 5],
    ["like", 5],
    ["to", 4],
    ["say", 5],
    ["the", 4],
    ["the", 4],
    ["front", 6],
    ["cover", 6],
    ["of", 4],
    ["this", 5],
    ["film", 8],
    ["is", 5],
    ["great,", 7],
    ["if", 5],
    ["you", 5],
    ["think", 6],
    ["you", 5],
    ["are", 5],
    ["about", 6],
    ["to", 4],
    ["see", 6],
    ["a", 4],
    ["truly", 7],
    ["scary", 7],
    ["horror", 7],
    ["film", 8],
    ["with", 5],
    ["a", 4],
    ["monster", 7],
    ["clown,", 7],
    ["you", 5],
    ["are", 5],
    ["soooo", 8],
    ["right.", 7],
    ["In", 5],
    ["fact", 6],
    ["the", 4],
    ["killers", 7],
    ["face", 6],
    ["looks", 6],
    ["exactly", 7],
    ["like", 6],
    ["the", 4],
    ["front", 6],
    ["cover,", 6],
    ["it's", 6],
    ["just", 6],
    ["an", 5],
    ["image", 7],
    ["they", 6],
    ["must", 6],
    ["have", 6],
    ["found", 7],
    ["on", 5],
    ["Google", 7],
    ["and", 5],
    ["thought", 7],
    ["it", 5],
    ["looked", 6],
    ["cool.", 6],
    ["Speaking", 6],
    ["of", 4],
    ["things", 6],
    ["they", 6],
    ["found", 7],
    ["and", 5],
    ["thought", 7],
    ["it", 5],
    ["looked", 6],
    ["cool,", 6],
    ["there", 6],
    ["is", 5],
    ["a", 4],
    ["scene", 7],
    ["in", 5],
    ["this", 5],
    ["film", 8],
    ["where", 6],
    ["some", 6],
    ["of", 4],
    ["the", 4],
    ["gang", 6],
    ["are", 5],
    ["searching", 7],
    ["for", 6],
    ["the", 4],
    ["friend", 7],
    ["in", 5],
    ["the", 4],
    ["old", 6],
    ["woods,", 7],
    ["then", 6],
    ["suddenly", 7],
    ["the", 4],
    ["screen", 7],
    ["chops", 7],
    ["to", 4],
    ["a", 4],
    ["scene", 7],
    ["where", 6],
    ["there", 6],
    ["is", 5],
    ["a", 4],
    ["mother", 7],
    ["deer", 7],
    ["nurturing", 8],
    ["it's", 6],
    ["young", 7],
    ["in", 5],
    ["a", 4],
    ["glisten", 7],
    ["of", 4],
    ["sunlight...", 8],
    ["I", 5],
    ["mean", 6],
    ["seriously", 8],
    ["awesome!!!", 9],
    ["It's", 7],
    ["so", 6],
    ["relevant", 8],
    ["to", 4],
    ["the", 4],
    ["dark", 7],
    ["woods", 7],
    ["they", 6],
    ["are", 5],
    ["wandering", 7],
    ["through?", 7],
    ["I", 5],
    ["bought", 7],
    ["this", 5],
    ["film", 8],
    ["from", 6],
    ["a", 4],
    ["man", 6],
    ["at", 5],
    ["a", 4],
    ["market", 7],
    ["hoping", 7],
    ["it", 5],
    ["would", 6],
    ["be", 5],
    ["entertaining,", 8],
    ["if", 5],
    ["it", 5],
    ["wasn't", 7],
    ["horror", 7],
    ["then", 6],
    ["at", 5],
    ["least", 6],
    ["it", 5],
    ["would", 6],
    ["be", 5],
    ["funny", 7],
    ["right?", 7],
    ["RIGHT!", 8],
    ["The", 6],
    ["next", 6],
    ["day", 6],
    ["I", 5],
    ["GAVE", 8],
    ["it", 5],
    ["to", 4],
    ["my", 5],
    ["work", 6],
    ["colleague", 7],
    ["because", 7],
    ["I", 5],
    ["had", 6],
    ["to", 4],
    ["share.", 7],
    ["Bottom", 7],
    ["line", 7],
    ["is:", 6],
    ["SEE", 9],
    ["THIS", 9],
    ["FILM!!!", 9]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`, `best`, `bottom`, `buy`, `chop`, `clown`, `colleague`, `dark`, `deer`, `entertain`, `ever`, `exactly`, `film`, `find`, `friend`, `funny`, `give`, `glisten`, `google`, `great`, `hop`, `horror`, `image`, `killer`, `line`, `market`, `monster`, `mother`, `motion`, `nurture`, `picture`, `relevant`, `right`, `scary`, `see`, `seriously`, `soooo`, `sunlight`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text expresses strong enthusiasm and praise for the film, highlighting various aspects the author found impressive and enjoyable."
}
```

**Rationale text:**
> The text expresses strong enthusiasm and praise for the film, highlighting various aspects the author found impressive and enjoyable.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `find`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "This film is the worst motion picture I have EVER seen. To begin, I'd like to say the front cover of this film is terrible, if you think you are about to see a truly scary horror film with a monster clown, you are soooo wrong. In fact the killer's face looks nothing like the front cover, it's just an image they must have found on Google and thought it looked awful. Speaking of things they found and thought it looked awful, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing its young in a glisten of sunlight... I mean seriously boring!!! It's so irrelevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? WRONG! The next day I THREW it away because I had to forget. Bottom line is: AVOID THIS FILM!!!",
  "new_prediction": "negative"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> This film is the worst motion picture I have EVER seen. To begin, I'd like to say the front cover of this film is terrible, if you think you are about to see a truly scary horror film with a monster clown, you are soooo wrong. In fact the killer's face looks nothing like the front cover, it's just an image they must have found on Google and thought it looked awful. Speaking of things they found and thought it looked awful, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing its young in a glisten of sunlight... I mean seriously boring!!! It's so irrelevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? WRONG! The next day I THREW it away because I had to forget. Bottom line is: AVOID THIS FILM!!!

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`, `best`, `colleague`, `cool`, `exactly`, `film`, `give`, `great`, `killer`, `relevant`, `right`, `see`, `share`, `work`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{
  "ranking": [
    "awesome",
    "great",
    "right",
    "cool",
    "best"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`(1), `great`(2), `right`(3), `cool`(4), `best`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.0526 |
| H–CF | 0.7857 | 0.2683 |
| H–RO | 0.8000 | 0.1026 |
| R–CF | 0.5000 | 0.0667 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 1.0000 | 0.3571 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |
| RBO (H,RO) | 0.3461 |

### cad_imdb_dev_000699 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{
  "label": "positive"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 166 words
- **Raw response length:** 25 chars
- **Prompt hash:** `e4542f4cd92447dd`
- **ECS (full):** 0.2276
- **ECS (extraction–rationale):** 0.2135
- **ECS (extraction–perturbation):** 0.3138
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 2

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{
  "confidence": 95
}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["For", 3],
    ["the", 2],
    ["first", 5],
    ["forty", 5],
    ["minutes,", 4],
    ["Empire", 8],
    ["really", 6],
    ["shapes", 6],
    ["itself", 6],
    ["up:", 4],
    ["it", 3],
    ["is", 3],
    ["a", 2],
    ["strong,", 7],
    ["confident,", 7],
    ["though", 5],
    ["relatively", 6],
    ["unknown", 6],
    ["gangster", 8],
    ["flick.", 5],
    ["At", 3],
    ["the", 2],
    ["time", 4],
    ["I", 3],
    ["didn't", 5],
    ["know", 6],
    ["why", 5],
    ["I", 3],
    ["knew", 6],
    ["it", 3],
    ["was", 4],
    ["good-", 6],
    ["but", 4],
    ["now", 5],
    ["I", 3],
    ["do.", 4],
    ["One", 5],
    ["of", 3],
    ["the", 2],
    ["main", 6],
    ["strong", 8],
    ["points", 7],
    ["with", 5],
    ["this", 5],
    ["film", 7],
    ["is", 3],
    ["that", 4],
    ["it", 3],
    ["is", 3],
    ["purely", 7],
    ["and", 5],
    ["utterly", 7],
    ["classy", 8],
    ["and", 5],
    ["tasteful.", 8],
    ["I", 3],
    ["don't", 5],
    ["mind", 6],
    ["films", 6],
    ["with", 5],
    ["psychos", 7],
    ["and", 5],
    ["things,", 6],
    ["to", 3],
    ["prove", 6],
    ["a", 2],
    ["point-", 6],
    ["take", 6],
    ["Jackie", 7],
    ["Brown,", 7],
    ["for", 4],
    ["example-", 6],
    ["but", 4],
    ["they're", 6],
    ["all", 5],
    ["so", 5],
    ["terrifically", 8],
    ["meaningful", 8],
    ["in", 3],
    ["this", 5],
    ["and", 5],
    ["that", 4],
    ["is", 3],
    ["obviously", 7],
    ["included", 7],
    ["for", 4],
    ["entertainment.", 7],
    ["You", 5],
    ["literally", 7],
    ["feel", 6],
    ["a", 2],
    ["knot", 7],
    ["of", 3],
    ["excitement", 8],
    ["in", 3],
    ["your", 5],
    ["stomach.", 6],
    ["Another", 7],
    ["major", 7],
    ["strong", 8],
    ["point", 7],
    ["is", 3],
    ["the", 2],
    ["protagonist.", 8],
    ["He", 6],
    ["is", 3],
    ["not", 5],
    ["smug", 7],
    ["or", 4],
    ["arrogant", 7],
    ["and", 5],
    ["-", 2],
    ["expectedly", 7],
    ["-", 2],
    ["not", 5],
    ["that", 4],
    ["bad.", 6],
    ["He", 6],
    ["seems", 6],
    ["just", 6],
    ["right", 7],
    ["to", 3],
    ["be", 4],
    ["a", 2],
    ["drug-dealing", 8],
    ["woman", 7],
    ["killer.", 7],
    ["The", 5],
    ["fact", 6],
    ["is,", 3],
    ["at", 3],
    ["the", 2],
    ["end", 5],
    ["of", 3],
    ["the", 2],
    ["day,", 5],
    ["this", 5],
    ["film", 7],
    ["is", 3],
    ["completely", 8],
    ["perfect.", 8],
    ["Slick,", 8],
    ["clever,", 8],
    ["never", 7],
    ["dull,", 7],
    ["and", 5],
    ["always", 7],
    ["meaningful", 8],
    ["-", 2],
    ["this", 5],
    ["incredible", 8],
    ["masterpiece", 9],
    ["should", 7],
    ["be", 4],
    ["applauded", 8],
    ["at", 3],
    ["all", 5],
    ["times.", 6],
    ["*****", 8],
    ["out", 5],
    ["of", 3],
    ["*****", 8],
    ["(5", 6],
    ["out", 5],
    ["of", 3],
    ["5)", 6]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `always`, `another`, `applaud`, `arrogant`, `brown`, `classy`, `clever`, `completely`, `confident`, `drug-dealing`, `dull`, `empire`, `entertainment`, `excitement`, `expectedly`, `film`, `gangster`, `include`, `incredible`, `jackie`, `killer`, `knot`, `literally`, `major`, `masterpiece`, `meaningful`, `perfect`, `protagonist`, `slick`, `strong`, `tasteful`, `terrifically`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text praises the film with strong positive adjectives and a perfect rating, indicating a highly favorable sentiment."
}
```

**Rationale text:**
> The text praises the film with strong positive adjectives and a perfect rating, indicating a highly favorable sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `perfect`, `strong`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "For the first forty minutes, Empire really disappoints: it is a weak, uncertain, and relatively unknown gangster flick. At the time I didn't know why I knew it was bad- but now I do. One of the main weak points with this film is that it is purely and utterly tasteless and dull. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terribly pointless in this and that is obviously included for poor entertainment. You literally feel a pit of boredom in your stomach. Another major weak point is the protagonist. He is smug or arrogant and - unexpectedly - very bad. He seems completely wrong to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely flawed. Clumsy, uninspired, always dull, and never meaningful - this terrible failure should be forgotten at all times. * out of ***** (1 out of 5)",
  "new_prediction": "negative"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> For the first forty minutes, Empire really disappoints: it is a weak, uncertain, and relatively unknown gangster flick. At the time I didn't know why I knew it was bad- but now I do. One of the main weak points with this film is that it is purely and utterly tasteless and dull. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terribly pointless in this and that is obviously included for poor entertainment. You literally feel a pit of boredom in your stomach. Another major weak point is the protagonist. He is smug or arrogant and - unexpectedly - very bad. He seems completely wrong to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely flawed. Clumsy, uninspired, always dull, and never meaningful - this terrible failure should be forgotten at all times. * out of ***** (1 out of 5)

**Parsed tokens:**
- Status: **Valid**
- Tokens: `5`, `always`, `applaud`, `classy`, `clever`, `confident`, `excitement`, `expectedly`, `good`, `incredible`, `knot`, `masterpiece`, `meaningful`, `never`, `not`, `perfect`, `right`, `shape`, `slick`, `strong`, `tasteful`, `terrifically`, `though`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{
  "ranking": [
    "perfect",
    "masterpiece",
    "incredible",
    "applauded",
    "strong"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `perfect`(1), `masterpiece`(2), `incredible`(3), `applaud`(4), `strong`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.0938 |
| H–CF | 0.6957 | 0.4103 |
| H–RO | 1.0000 | 0.1562 |
| R–CF | 0.6667 | 0.0833 |
| R–RO | 0.6667 | 0.3333 |
| CF–RO | 1.0000 | 0.2174 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.2000 |
| Normalized τ | 0.6000 |
| RBO (H,RO) | 0.2876 |

### cad_imdb_dev_000531 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{
  "label": "negative"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `negative` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 275 words
- **Raw response length:** 25 chars
- **Prompt hash:** `6d0a18e2e553b3d6`
- **ECS (full):** 0.0420
- **ECS (extraction–rationale):** 0.0172
- **ECS (extraction–perturbation):** 0.0877
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: negative

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{
  "confidence": 95
}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["I", 3],
    ["really", 7],
    ["don't", 7],
    ["get", 6],
    ["how", 5],
    ["people", 6],
    ["made", 6],
    ["this", 6],
    ["film", 7],
    ["and", 3],
    ["thought", 6],
    ["it", 4],
    ["wasn't", 7],
    ["worth", 7],
    ["all", 5],
    ["the", 4],
    ["work", 6],
    ["they", 5],
    ["put", 5],
    ["into", 5],
    ["it.", 3],
    ["Even", 6],
    ["more", 5],
    ["puzzling", 7],
    ["are", 4],
    ["those", 5],
    ["who", 5],
    ["watched", 6],
    ["this", 6],
    ["film", 7],
    ["without", 6],
    ["feeling", 6],
    ["content", 6],
    ["about", 5],
    ["the", 4],
    ["88", 5],
    ["minutes", 5],
    ["of", 3],
    ["doing", 5],
    ["something", 6],
    ["relaxing", 6],
    ["and", 3],
    ["not", 5],
    ["cleaning", 6],
    ["under", 5],
    ["the", 4],
    ["couch", 5],
    ["or", 3],
    ["reading", 6],
    ["Leviticus.", 6],
    ["First", 5],
    ["of", 3],
    ["all,", 3],
    ["they", 5],
    ["had", 5],
    ["real", 6],
    ["Irish", 6],
    ["people,", 5],
    ["and", 3],
    ["some", 5],
    ["good-looking", 7],
    ["women", 6],
    ["who", 5],
    ["could", 6],
    ["deliver", 6],
    ["their", 5],
    ["lines", 5],
    ["better", 6],
    ["than", 5],
    ["the", 4],
    ["stunning,", 6],
    ["talented", 6],
    ["porn", 8],
    ["stars", 6],
    ["sprinkled", 6],
    ["throughout", 6],
    ["this", 6],
    ["film.", 6],
    ["Granted,", 5],
    ["the", 4],
    ["gore", 6],
    ["works-", 6],
    ["but", 5],
    ["strangely,", 6],
    ["it's", 5],
    ["not", 5],
    ["as", 4],
    ["troubling", 7],
    ["as", 4],
    ["you", 5],
    ["might", 5],
    ["think", 6],
    ["to", 3],
    ["see", 5],
    ["organs", 6],
    ["yanked", 6],
    ["out", 5],
    ["of", 3],
    ["the", 4],
    ["porn", 8],
    ["stars'", 6],
    ["hot,", 5],
    ["tight", 6],
    ["bodies", 6],
    ["left", 5],
    ["and", 3],
    ["right.", 5],
    ["Probably", 6],
    ["has", 5],
    ["something", 6],
    ["to", 3],
    ["do", 5],
    ["with", 5],
    ["the", 4],
    ["fact", 5],
    ["that", 5],
    ["after", 5],
    ["their", 5],
    ["brilliant", 7],
    ["acting", 6],
    ["you", 5],
    ["just", 5],
    ["want", 6],
    ["them", 5],
    ["to", 3],
    ["die", 6],
    ["in", 4],
    ["pain.", 6],
    ["So,", 4],
    ["if", 4],
    ["you", 5],
    ["care", 5],
    ["at", 4],
    ["all", 5],
    ["about", 5],
    ["the", 4],
    ["following:", 5],
    ["-", 3],
    ["acting", 6],
    ["(seriously,", 6],
    ["everyone", 6],
    ["was", 5],
    ["outstanding.", 7],
    ["I've", 5],
    ["never", 6],
    ["witnessed", 6],
    ["this", 6],
    ["before.", 5],
    ["EVERYONE.", 7],
    ["-", 3],
    ["plot", 6],
    ["(some", 5],
    ["crappy", 6],
    ["horror", 6],
    ["movies", 6],
    ["are", 4],
    ["remotely", 6],
    ["linear,", 6],
    ["or", 3],
    ["at", 4],
    ["the", 4],
    ["very", 5],
    ["least", 5],
    ["surprising.", 6],
    ["This", 6],
    ["movie", 6],
    ["makes", 6],
    ["perfect", 6],
    ["sense", 6],
    ["unless", 6],
    ["you're", 5],
    ["trashed.", 6],
    ["-", 3],
    ["theme", 6],
    ["(Lots", 6],
    ["to", 3],
    ["learn", 6],
    ["from", 5],
    ["this", 6],
    ["film.", 6],
    ["So", 5],
    ["much", 5],
    ["to", 3],
    ["be", 4],
    ["scared", 6],
    ["about", 5],
    ["in", 4],
    ["bed", 5],
    ["at", 4],
    ["night,", 5],
    ["to", 3],
    ["contemplate", 6],
    ["or", 3],
    ["grasp,", 5],
    ["and", 3],
    ["explain", 6],
    ["to", 3],
    ["others).", 5],
    ["-", 3],
    ["soundtrack", 6],
    ["(Wow,", 6],
    ["Music", 6],
    ["as", 4],
    ["bewitching", 7],
    ["as", 4],
    ["the", 4],
    ["script).", 6],
    ["-", 3],
    ["scenery", 6],
    ["(Could", 6],
    ["have", 5],
    ["been", 5],
    ["this", 6],
    ["film's", 6],
    ["saving", 6],
    ["downfall,", 6],
    ["but", 5],
    ["no...", 5],
    ["nothing", 6],
    ["missing", 6],
    ["here.", 5],
    ["Even", 6],
    ["the", 4],
    ["rocks", 6],
    ["are", 4],
    ["real).", 5],
    ["So,", 4],
    ["yeah.", 5],
    ["If", 4],
    ["you", 5],
    ["care", 5],
    ["about", 5],
    ["that", 5],
    ["or", 3],
    ["you're", 5],
    ["just", 5],
    ["a", 3],
    ["horny", 7],
    ["teen", 6],
    ["with", 5],
    ["good", 6],
    ["taste", 6],
    ["in", 4],
    ["music", 6],
    ["and", 3],
    ["\"", 3],
    ["women,", 6],
    ["\"", 3],
    ["this", 6],
    ["movie", 6],
    ["is", 4],
    ["for", 5],
    ["you.", 5],
    ["Other", 6],
    ["comments:", 5],
    ["interesting", 7],
    ["cinematography", 8],
    ["at", 4],
    ["times.", 5],
    ["Very", 6],
    ["realistic", 7],
    ["gore.", 6],
    ["But", 5],
    ["the", 4],
    ["intestines", 7],
    ["scene", 6],
    ["is", 4],
    ["classic.", 6],
    ["I", 3],
    ["agree", 6],
    ["with", 5],
    ["the", 4],
    ["mutant-", 6],
    ["disembowelment", 8],
    ["solves", 7],
    ["the", 4],
    ["fake", 6],
    ["accent", 6],
    ["problem.", 6]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `accent`, `act`, `agree`, `bewitch`, `body`, `brilliant`, `cinematography`, `classic`, `clean`, `contemplate`, `content`, `could`, `crappy`, `deliver`, `die`, `disembowelment`, `don't`, `downfall`, `even`, `everyone`, `fake`, `feel`, `film`, `film's`, `get`, `good`, `good-looking`, `gore`, `horny`, `horror`, `interest`, `intestine`, `irish`, `learn`, `leviticus`, `linear`, `lot`, `make`, `miss`, `movie`, `music`, `mutant`, `never`, `nothing`, `organ`, `outstanding`, `porn`, `puzzle`, `realistic`, `really`, `solve`, `trouble`, `wasn't`, `worth`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text uses sarcastic and critical language to express dissatisfaction with the film, highlighting perceived flaws in acting, plot, theme, soundtrack, and scenery."
}
```

**Rationale text:**
> The text uses sarcastic and critical language to express dissatisfaction with the film, highlighting perceived flaws in acting, plot, theme, soundtrack, and scenery.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `film`, `plot`, `scenery`, `soundtrack`, `theme`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "I really get how people made this film and thought it was worth all the work they put into it. Even more impressive are those who watched this film feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented actors sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the actors' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want the story to continue. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some great horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving grace, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a fan with good taste in music and \"cinema,\" this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the director- disembowelment solves the fake accent problem.",
  "new_prediction": "positive"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> I really get how people made this film and thought it was worth all the work they put into it. Even more impressive are those who watched this film feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented actors sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the actors' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want the story to continue. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some great horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving grace, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a fan with good taste in music and "cinema," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the director- disembowelment solves the fake accent problem.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `crappy`, `die`, `downfall`, `horny`, `mutant`, `n't`, `pain`, `porn`, `puzzle`, `star`, `teen`, `without`, `woman`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{
  "ranking": [
    "crappy",
    "troubling",
    "trashed",
    "disembowelment",
    "realistic"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `crappy`(1), `trouble`(2), `trash`(3), `disembowelment`(4), `realistic`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.0345 |
| H–CF | 0.5385 | 0.1167 |
| H–RO | 0.8000 | 0.0727 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.2000 | 0.0588 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | -0.6667 |
| Normalized τ | 0.1667 |
| RBO (H,RO) | 0.1023 |

### cad_imdb_dev_000220 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{
  "label": "negative"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 50 words
- **Raw response length:** 25 chars
- **Prompt hash:** `c831d668eac72d2d`
- **ECS (full):** 0.5083
- **ECS (extraction–rationale):** 0.4583
- **ECS (extraction–perturbation):** 0.5625
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 5 | **CC4 size:** 4

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{
  "confidence": 95
}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["I", 3],
    ["think", 5],
    ["Via", 8],
    ["Satellite", 8],
    ["is", 5],
    ["one", 6],
    ["of", 4],
    ["the", 5],
    ["lamest", 9],
    ["New", 7],
    ["Zealand", 7],
    ["made", 6],
    ["movies", 7],
    ["around.", 5],
    ["I", 3],
    ["detested", 9],
    ["the", 5],
    ["way", 6],
    ["the", 5],
    ["movie", 7],
    ["delt", 6],
    ["with", 5],
    ["all", 5],
    ["the", 5],
    ["characters", 7],
    ["within", 6],
    ["the", 5],
    ["entire", 6],
    ["movie.", 6],
    ["It", 5],
    ["was", 5],
    ["rubbish,", 9],
    ["and", 4],
    ["a", 3],
    ["pitiful", 8],
    ["movie.", 6],
    ["A", 3],
    ["feeble", 8],
    ["movie,", 6],
    ["one", 6],
    ["which", 6],
    ["I", 3],
    ["will", 5],
    ["always", 6],
    ["remember", 7],
    ["poorly,", 8],
    ["and", 4],
    ["never", 7],
    ["watch", 7],
    ["again.", 6]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `character`, `detest`, `feeble`, `lame`, `movie`, `pitiful`, `poorly`, `rubbish`, `satellite`, `via`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text contains strong negative language and criticism towards the movie, such as 'lamest', 'detested', 'rubbish', 'pitiful', 'feeble', and a vow to never watch it again."
}
```

**Rationale text:**
> The text contains strong negative language and criticism towards the movie, such as 'lamest', 'detested', 'rubbish', 'pitiful', 'feeble', and a vow to never watch it again.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `detest`, `feeble`, `movie`, `never`, `pitiful`, `rubbish`, `watch`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "I think Via Satellite is one of the finest New Zealand made movies around. I appreciated the way the movie handled all the characters within the entire movie. It was excellent, and a remarkable movie. A strong movie, one which I will always remember fondly, and might watch again.",
  "new_prediction": "positive"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> I think Via Satellite is one of the finest New Zealand made movies around. I appreciated the way the movie handled all the characters within the entire movie. It was excellent, and a remarkable movie. A strong movie, one which I will always remember fondly, and might watch again.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `delt`, `detest`, `feeble`, `lame`, `never`, `pitiful`, `poorly`, `rubbish`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{
  "ranking": [
    "detested",
    "rubbish",
    "pitiful",
    "feeble",
    "lamest"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `detest`(1), `rubbish`(2), `pitiful`(3), `feeble`(4), `lame`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7143 | 0.4167 |
| H–CF | 0.7500 | 0.5000 |
| H–RO | 1.0000 | 0.5000 |
| R–CF | 0.7143 | 0.5000 |
| R–RO | 0.8000 | 0.5000 |
| CF–RO | 1.0000 | 0.6250 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.2000 |
| Normalized τ | 0.6000 |
| RBO (H,RO) | 0.4796 |

### cad_imdb_dev_000284 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 110 words
- **Raw response length:** 20 chars
- **Prompt hash:** `973c726ddbbfd9e7`
- **ECS (full):** 0.1691
- **ECS (extraction–rationale):** 0.0909
- **ECS (extraction–perturbation):** 0.3318
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 98}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Well,", 2], ["what", 3], ["can", 4], ["it", 5], ["be", 3], ["said", 4], ["about", 3], ["this", 6], ["fabulous", 9], ["thing?", 5], ["I", 5], ["watched", 4], ["it", 5], ["because", 3], ["it", 5], ["aired", 4], ["on", 2], ["cable.", 3], ["I", 5], ["loved", 10], ["it.", 6], ["The", 3], ["creature", 8], ["is", 3], ["the", 2], ["scariest", 9], ["you", 4], ["can", 4], ["get!", 6], ["Please,", 3], ["you", 4], ["need", 4], ["to", 2], ["be", 3], ["very", 5], ["generous", 5], ["not", 3], ["to", 2], ["get", 4], ["scared", 7], ["by", 2], ["the", 2], ["amazing", 8], ["Halloween", 6], ["costume.", 6], ["Oh", 2], ["well,", 2], ["there", 3], ["are", 2], ["also", 3], ["displays", 6], ["of", 2], ["great", 8], ["acting,", 7], ["f/x,", 7], ["and", 2], ["dialogues.", 6], ["The", 3], ["confrontation", 8], ["with", 3], ["the", 2], ["creature", 8], ["is", 3], ["unbelievable,", 9], ["you", 4], ["can't", 4], ["get", 4], ["a", 2], ["more", 5], ["amazing", 8], ["scene.", 7], ["This", 5], ["is", 3], ["the", 2], ["best", 10], ["you", 4], ["can", 4], ["get", 4], ["from", 3], ["direct", 5], ["to", 2], ["video", 5], ["flicks.", 6], ["Creature", 8], ["Unknown", 7], ["makes", 5], ["FULL", 5], ["MOON", 5], ["PICTURES", 5], ["movies", 6], ["look", 5], ["like", 4], ["Halloween", 6], [".", 2], ["I", 5], ["recommend", 10], ["at", 4], ["all", 5], ["costs,", 7], ["please.", 4], ["The", 3], ["only", 4], ["\"negative\"", 3], ["thing", 4], ["about", 3], ["this", 6], ["great", 8], ["movie", 7], ["are", 3], ["the", 2], ["women.", 2]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `amaze`, `best`, `confrontation`, `cost`, `costume`, `creature`, `dialogue`, `display`, `f/x`, `fabulous`, `flick`, `get`, `great`, `love`, `movie`, `recommend`, `scar`, `scary`, `scene`, `unbelievable`, `unknown`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses enthusiastic praise for the movie's creature, acting, effects, dialogue, and overall quality, with only a minor, sarcastically framed criticism, indicating a strongly positive sentiment."}
```

**Rationale text:**
> The text expresses enthusiastic praise for the movie's creature, acting, effects, dialogue, and overall quality, with only a minor, sarcastically framed criticism, indicating a strongly positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `creature`, `dialogue`, `movie`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "Well, what can it be said about this awful thing? I watched it because it aired on cable. I hated it. The creature is the lamest you can get! Please, you need to be very generous not to laugh at the ridiculous Halloween costume. Oh well, there are also displays of bad acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more stupid scene. This is the worst you can get from direct to video flicks. \"Creature Unknown\" makes FULL MOON PICTURES movies look like \"Halloween\". I recommend at all costs, please. The only \"positive\" thing about this terrible movie are the women.", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> Well, what can it be said about this awful thing? I watched it because it aired on cable. I hated it. The creature is the lamest you can get! Please, you need to be very generous not to laugh at the ridiculous Halloween costume. Oh well, there are also displays of bad acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more stupid scene. This is the worst you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "positive" thing about this terrible movie are the women.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amaze`, `best`, `fabulous`, `get`, `great`, `love`, `scar`, `scary`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["loved", "fabulous", "amazing", "unbelievable", "recommend"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `fabulous`(2), `amaze`(3), `unbelievable`(4), `recommend`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.1818 |
| H–CF | 1.0000 | 0.3636 |
| H–RO | 1.0000 | 0.2273 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.6000 | 0.3000 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.2000 |
| Normalized τ | 0.6000 |
| RBO (H,RO) | 0.3840 |

### cad_imdb_test_000501 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 190 words
- **Raw response length:** 20 chars
- **Prompt hash:** `ebd4951c603a1d3d`
- **ECS (full):** 0.1587
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 95}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["This", 6], ["film", 8], ["is", 4], ["the", 3], ["best", 10], ["motion", 6], ["picture", 7], ["I", 5], ["have", 4], ["EVER", 9], ["seen", 6], [".", 2], ["To", 3], ["begin", 5], [","], ["I'd", 4], ["like", 5], ["to", 3], ["say", 5], ["the", 3], ["the", 3], ["front", 6], ["cover", 7], ["of", 3], ["this", 6], ["film", 8], ["is", 4], ["great", 8], [","], ["if", 4], ["you", 5], ["think", 6], ["you", 5], ["are", 4], ["about", 5], ["to", 3], ["see", 6], ["a", 3], ["truly", 7], ["scary", 7], ["horror", 7], ["film", 8], ["with", 4], ["a", 3], ["monster", 8], ["clown", 7], [","], ["you", 5], ["are", 4], ["soooo", 8], ["right", 7], ["."], ["In", 4], ["fact", 5], ["the", 3], ["killers", 7], ["face", 6], ["looks", 6], ["exactly", 7], ["like", 5], ["the", 3], ["front", 6], ["cover", 7], [","], ["it's", 4], ["just", 5], ["an", 3], ["image", 6], ["they", 5], ["must", 5], ["have", 4], ["found", 6], ["on", 4], ["Google", 7], ["and", 4], ["thought", 6], ["it", 5], ["looked", 6], ["cool", 7], ["."], ["Speaking", 6], ["of", 4], ["things", 5], ["they", 5], ["found", 6], ["and", 4], ["thought", 6], ["it", 5], ["looked", 6], ["cool", 7], [","], ["there", 4], ["is", 4], ["a", 3], ["scene", 7], ["in", 4], ["this", 6], ["film", 8], ["where", 5], ["some", 5], ["of", 4], ["the", 3], ["gang", 6], ["are", 4], ["searching", 7], ["for", 4], ["the", 3], ["friend", 6], ["in", 4], ["the", 3], ["old", 5], ["woods", 6], [","], ["then", 5], ["suddenly", 7], ["the", 3], ["screen", 7], ["chops", 8], ["to", 3], ["a", 3], ["scene", 7], ["where", 5], ["there", 4], ["is", 4], ["a", 3], ["mother", 7], ["deer", 7], ["nurturing", 8], ["it's", 5], ["young", 6], ["in", 4], ["a", 3], ["glisten", 7], ["of", 4], ["sunlight", 8], ["..."], ["I", 5], ["mean", 6], ["seriously", 8], ["awesome", 10], ["!!!"], ["It's", 5], ["so", 6], ["relevant", 3], ["to", 3], ["the", 3], ["dark", 6], ["woods", 6], ["they", 5], ["are", 4], ["wandering", 7], ["through", 5], ["?"], ["I", 5], ["bought", 6], ["this", 6], ["film", 8], ["from", 4], ["a", 3], ["man", 5], ["at", 4], ["a", 3], ["market", 6], ["hoping", 6], ["it", 5], ["would", 5], ["be", 4], ["entertaining", 8], [","], ["if", 4], ["it", 5], ["wasn't", 5], ["horror", 7], ["then", 5], ["at", 4], ["least", 6], ["it", 5], ["would", 5], ["be", 4], ["funny", 7], ["right", 7], ["?"], ["RIGHT", 9], ["!"], ["The", 4], ["next", 5], ["day", 5], ["I", 5], ["GAVE", 8], ["it", 5], ["to", 3], ["my", 5], ["work", 5], ["colleague", 7], ["because", 5], ["I", 5], ["had", 5], ["to", 3], ["share", 8], ["."], ["Bottom", 6], ["line", 6], ["is", 4], [":"], ["SEE", 9], ["THIS", 7], ["FILM", 9], ["!!!"]]}}
```

**Parsed tokens:**
- *Not parsed*

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses enthusiastic praise and excitement for the film, using exaggerated positive language and a strong recommendation to watch it, despite apparent irony and criticism."}
```

**Rationale text:**
> The text expresses enthusiastic praise and excitement for the film, using exaggerated positive language and a strong recommendation to watch it, despite apparent irony and criticism.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "This film is the worst motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is terrible, if you think you are about to see a truly scary horror film with a monster clown, you are soooo wrong. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awful!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? WRONG! The next day I GAVE it to my work colleague because I had to get rid of it. Bottom line is: AVOID THIS FILM!!!", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> This film is the worst motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is terrible, if you think you are about to see a truly scary horror film with a monster clown, you are soooo wrong. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awful!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? WRONG! The next day I GAVE it to my work colleague because I had to get rid of it. Bottom line is: AVOID THIS FILM!!!

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`, `best`, `film`, `great`, `right`, `see`, `share`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["best", "awesome", "SEE", "GAVE", "entertaining"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `best`(1), `awesome`(2), `see`(3), `give`(4), `entertain`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | 1.0000 | 0.1429 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.6000 | 0.3333 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### cad_imdb_dev_000699 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 166 words
- **Raw response length:** 20 chars
- **Prompt hash:** `e4542f4cd92447dd`
- **ECS (full):** 0.2495
- **ECS (extraction–rationale):** 0.2135
- **ECS (extraction–perturbation):** 0.3602
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 2

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 100}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["For", 2], ["the", 1], ["first", 3], ["forty", 2], ["minutes", 3], [",", 1], ["Empire", 6], ["really", 5], ["shapes", 3], ["itself", 2], ["up", 2], [":", 1], ["it", 2], ["is", 2], ["a", 1], ["strong", 8], [",", 1], ["confident", 8], [",", 1], ["though", 2], ["relatively", 3], ["unknown", 4], ["gangster", 5], ["flick", 4], [".", 1], ["At", 2], ["the", 1], ["time", 3], ["I", 2], ["did", 1], ["n't", 1], ["know", 3], ["why", 3], ["I", 2], ["knew", 4], ["it", 2], ["was", 2], ["good", 9], ["-", 1], ["but", 3], ["now", 3], ["I", 2], ["do", 2], [".", 1], ["One", 3], ["of", 1], ["the", 1], ["main", 4], ["strong", 8], ["points", 4], ["with", 2], ["this", 3], ["film", 5], ["is", 2], ["that", 2], ["it", 2], ["is", 2], ["purely", 6], ["and", 2], ["utterly", 7], ["classy", 8], ["and", 2], ["tasteful", 8], [".", 1], ["I", 2], ["don't", 2], ["mind", 4], ["films", 3], ["with", 2], ["psychos", 5], ["and", 2], ["things", 3], [",", 1], ["to", 2], ["prove", 4], ["a", 1], ["point", 4], ["-", 1], ["take", 3], ["Jackie", 4], ["Brown", 4], [",", 1], ["for", 2], ["example", 3], ["-", 1], ["but", 3], ["they're", 2], ["all", 3], ["so", 3], ["terrifically", 7], ["meaningful", 8], ["in", 2], ["this", 3], ["and", 2], ["that", 2], ["is", 2], ["obviously", 5], ["included", 4], ["for", 2], ["entertainment", 6], [".", 1], ["You", 2], ["literally", 5], ["feel", 5], ["a", 1], ["knot", 6], ["of", 1], ["excitement", 9], ["in", 2], ["your", 2], ["stomach", 5], [".", 1], ["Another", 3], ["major", 4], ["strong", 8], ["point", 4], ["is", 2], ["the", 1], ["protagonist", 7], [".", 1], ["He", 2], ["is", 2], ["not", 3], ["smug", 5], ["or", 2], ["arrogant", 6], ["and", 2], ["-", 1], ["expectedly", 4], ["-", 1], ["not", 3], ["that", 2], ["bad", 5], [".", 1], ["He", 2], ["seems", 4], ["just", 4], ["right", 5], ["to", 2], ["be", 2], ["a", 1], ["drug-dealing", 6], ["woman", 3], ["killer", 5], [".", 1], ["The", 2], ["fact", 3], ["is", 2], [",", 1], ["at", 2], ["the", 1], ["end", 4], ["of", 1], ["the", 1], ["day", 3], [",", 1], ["this", 3], ["film", 5], ["is", 2], ["completely", 6], ["perfect", 10], [".", 1], ["Slick", 8], [",", 1], ["clever", 8], [",", 1], ["never", 5], ["dull", 5], [",", 1], ["and", 2], ["always", 5], ["meaningful", 8], ["-", 1], ["this", 3], ["incredible", 9], ["masterpiece", 10], ["should", 3], ["be", 2], ["applauded", 7], ["at", 2], ["all", 3], ["times", 4], [".", 1], ["*****", 9], ["out", 3], ["of", 1], ["*****", 9], ["(", 1], ["5", 4], ["out", 3], ["of", 1], ["5", 4], [")", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `always`, `applaud`, `arrogant`, `bad`, `classy`, `clever`, `completely`, `confident`, `drug-dealing`, `dull`, `empire`, `entertainment`, `excitement`, `feel`, `film`, `gangster`, `good`, `incredible`, `killer`, `knot`, `literally`, `masterpiece`, `meaningful`, `never`, `perfect`, `protagonist`, `purely`, `slick`, `strong`, `tasteful`, `terrifically`, `utterly`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses enthusiastic praise for the film, highlighting its strengths, quality, and emotional impact, culminating in a perfect rating and description as a 'masterpiece.'"}
```

**Rationale text:**
> The text expresses enthusiastic praise for the film, highlighting its strengths, quality, and emotional impact, culminating in a perfect rating and description as a 'masterpiece.'

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `masterpiece`, `perfect`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "For the first forty minutes, Empire really shapes itself up: it is a weak, unconfident, though relatively unknown gangster flick. At the time I didn't know why I knew it was bad- but now I do. One of the main weak points with this film is that it is purely and utterly classless and tasteless. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terribly meaningless in this and that is obviously included for boredom. You literally feel a knot of disappointment in your stomach. Another major weak point is the protagonist. He is smug and arrogant and - unexpectedly - that bad. He seems just wrong to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely flawed. Sloppy, dull, always boring, and never meaningful - this incredible failure should be criticized at all times. ***** out of ***** (5 out of 5)", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> For the first forty minutes, Empire really shapes itself up: it is a weak, unconfident, though relatively unknown gangster flick. At the time I didn't know why I knew it was bad- but now I do. One of the main weak points with this film is that it is purely and utterly classless and tasteless. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terribly meaningless in this and that is obviously included for boredom. You literally feel a knot of disappointment in your stomach. Another major weak point is the protagonist. He is smug and arrogant and - unexpectedly - that bad. He seems just wrong to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely flawed. Sloppy, dull, always boring, and never meaningful - this incredible failure should be criticized at all times. ***** out of ***** (5 out of 5)

**Parsed tokens:**
- Status: **Valid**
- Tokens: `always`, `applaud`, `classy`, `clever`, `confident`, `entertainment`, `excitement`, `expectedly`, `good`, `masterpiece`, `meaningful`, `never`, `not`, `perfect`, `right`, `slick`, `strong`, `tasteful`, `terrifically`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["perfect", "masterpiece", "strong", "classy", "excitement"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `perfect`(1), `masterpiece`(2), `strong`(3), `classy`(4), `excitement`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.0938 |
| H–CF | 0.8421 | 0.4571 |
| H–RO | 1.0000 | 0.1562 |
| R–CF | 0.6667 | 0.1000 |
| R–RO | 0.6667 | 0.3333 |
| CF–RO | 1.0000 | 0.2632 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.2000 |
| Normalized τ | 0.6000 |
| RBO (H,RO) | 0.4460 |

### cad_imdb_dev_000531 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 275 words
- **Raw response length:** 20 chars
- **Prompt hash:** `6d0a18e2e553b3d6`
- **ECS (full):** 0.1187
- **ECS (extraction–rationale):** 0.0370
- **ECS (extraction–perturbation):** 0.2597
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 0

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 95}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["I", 3], ["really", 5], ["don't", 4], ["get", 2], ["how", 2], ["people", 3], ["made", 3], ["this", 6], ["film", 6], ["and", 2], ["thought", 3], ["it", 3], ["wasn't", 5], ["worth", 7], ["all", 4], ["the", 3], ["work", 5], ["they", 3], ["put", 4], ["into", 3], ["it", 3], [".", 1], ["Even", 3], ["more", 3], ["puzzling", 6], ["are", 2], ["those", 2], ["who", 2], ["watched", 4], ["this", 6], ["film", 6], ["without", 4], ["feeling", 5], ["content", 7], ["about", 3], ["the", 3], ["88", 3], ["minutes", 4], ["of", 2], ["doing", 2], ["something", 2], ["relaxing", 6], ["and", 2], ["not", 4], ["cleaning", 3], ["under", 3], ["the", 3], ["couch", 2], ["or", 2], ["reading", 3], ["Leviticus", 3], [".", 1], ["First", 3], ["of", 2], ["all", 4], [",", 1], ["they", 3], ["had", 3], ["real", 6], ["Irish", 5], ["people", 3], [",", 1], ["and", 2], ["some", 3], ["good-looking", 6], ["women", 5], ["who", 2], ["could", 3], ["deliver", 4], ["their", 3], ["lines", 5], ["better", 6], ["than", 4], ["the", 3], ["stunning", 7], [",", 1], ["talented", 6], ["porn", 4], ["stars", 5], ["sprinkled", 5], ["throughout", 4], ["this", 6], ["film", 6], [".", 1], ["Granted", 4], [",", 1], ["the", 3], ["gore", 7], ["works", 6], ["-", 1], ["but", 3], ["strangely", 5], [",", 1], ["it's", 3], ["not", 4], ["as", 3], ["troubling", 5], ["as", 3], ["you", 2], ["might", 3], ["think", 3], ["to", 2], ["see", 4], ["organs", 5], ["yanked", 6], ["out", 3], ["of", 2], ["the", 3], ["porn", 4], ["stars'", 5], ["hot", 5], [",", 1], ["tight", 5], ["bodies", 4], ["left", 3], ["and", 2], ["right", 3], [".", 1], ["Probably", 3], ["has", 3], ["something", 2], ["to", 2], ["do", 2], ["with", 3], ["the", 3], ["fact", 3], ["that", 3], ["after", 3], ["their", 3], ["brilliant", 7], ["acting", 7], ["you", 2], ["just", 3], ["want", 5], ["them", 3], ["to", 2], ["die", 6], ["in", 3], ["pain", 6], [".", 1], ["So", 3], [",", 1], ["if", 3], ["you", 2], ["care", 5], ["at", 3], ["all", 4], ["about", 3], ["the", 3], ["following", 3], [":", 1], ["-", 2], ["acting", 7], ["(", 1], ["seriously", 6], [",", 1], ["everyone", 6], ["was", 4], ["outstanding", 8], [".", 1], ["I've", 3], ["never", 4], ["witnessed", 5], ["this", 6], ["before", 4], [".", 1], ["EVERYONE", 8], [".", 1], ["-", 2], ["plot", 6], ["(", 1], ["some", 3], ["crappy", 3], ["horror", 4], ["movies", 4], ["are", 2], ["remotely", 4], ["linear", 5], [",", 1], ["or", 2], ["at", 3], ["the", 3], ["very", 3], ["least", 3], ["surprising", 5], [".", 1], ["This", 5], ["movie", 5], ["makes", 5], ["perfect", 7], ["sense", 5], ["unless", 4], ["you're", 3], ["trashed", 4], [".", 1], ["-", 2], ["theme", 6], ["(", 1], ["Lots", 5], ["to", 2], ["learn", 5], ["from", 3], ["this", 6], ["film", 6], [".", 1], ["So", 3], ["much", 4], ["to", 2], ["be", 3], ["scared", 6], ["about", 3], ["in", 3], ["bed", 3], ["at", 3], ["night", 4], [",", 1], ["to", 2], ["contemplate", 5], ["or", 2], ["grasp", 5], [",", 1], ["and", 2], ["explain", 4], ["to", 2], ["others", 4], [")", 1], [".", 1], ["-", 2], ["soundtrack", 7], ["(", 1], ["Wow", 7], [",", 1], ["Music", 6], ["as", 3], ["bewitching", 7], ["as", 3], ["the", 3], ["script", 6], [")", 1], [".", 1], ["-", 2], ["scenery", 6], ["(", 1], ["Could", 4], ["have", 3], ["been", 3], ["this", 6], ["film's", 5], ["saving", 4], ["downfall", 3], [",", 1], ["but", 3], ["no", 3], ["...", 1], ["nothing", 4], ["missing", 6], ["here", 4], [".", 1], ["Even", 5], ["the", 3], ["rocks", 5], ["are", 2], ["real", 6], [")", 1], [".", 1], ["So", 3], [",", 1], ["yeah", 3], [".", 1], ["If", 3], ["you", 2], ["care", 5], ["about", 3], ["that", 3], ["or", 2], ["you're", 3], ["just", 3], ["a", 2], ["horny", 4], ["teen", 3], ["with", 3], ["good", 6], ["taste", 5], ["in", 3], ["music", 5], ["and", 2], ["\"", 1], ["women", 5], ["\"", 1], [",", 1], ["this", 6], ["movie", 5], ["is", 3], ["for", 3], ["you", 2], [".", 1], ["Other", 3], ["comments", 4], [":", 1], ["interesting", 6], ["cinematography", 6], ["at", 3], ["times", 4], [".", 1], ["Very", 5], ["realistic", 6], ["gore", 7], [".", 1], ["But", 4], ["the", 3], ["intestines", 7], ["scene", 6], ["is", 3], ["classic", 8], [".", 1], ["I", 3], ["agree", 5], ["with", 3], ["the", 3], ["mutant", 5], ["-", 1], ["disembowelment", 7], ["solves", 5], ["the", 3], ["fake", 5], ["accent", 5], ["problem", 5], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `accent`, `act`, `agree`, `bewitch`, `brilliant`, `care`, `cinematography`, `classic`, `contemplate`, `content`, `die`, `disembowelment`, `even`, `everyone`, `fake`, `feel`, `film`, `film's`, `good`, `good-looking`, `gore`, `grasp`, `hot`, `interest`, `intestine`, `irish`, `learn`, `line`, `linear`, `lot`, `make`, `miss`, `music`, `outstanding`, `pain`, `perfect`, `plot`, `puzzle`, `real`, `realistic`, `relax`, `scar`, `scene`, `scenery`, `script`, `seriously`, `soundtrack`, `stun`, `talented`, `theme`, `work`, `worth`, `wow`, `yank`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses sarcastic praise to mock the film's poor acting, plot, and casting, but the overall tone and exaggerated criticism indicate a negative sentiment, making the initial 'positive' classification incorrect."}
```

**Rationale text:**
> The text uses sarcastic praise to mock the film's poor acting, plot, and casting, but the overall tone and exaggerated criticism indicate a negative sentiment, making the initial 'positive' classification incorrect.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `film`, `make`, `plot`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "I really don't get how people made this film and thought it was worth all the work they put into it. Even more puzzling are those who watched this film without feeling annoyed about the 88 minutes of doing something pointless and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines worse than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their terrible acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was awful. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes no sense unless you're trashed. - theme (Nothing to learn from this film. So little to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as boring as the script). - scenery (Could have been this film's saving grace, but no...everything missing here. Even the rocks are fake). So, yeah. If you care about that or you're just a horny teen with bad taste in music and \"women,\" this movie is for you. Other comments: dull cinematography at times. Very fake gore. But the intestines scene is laughable. I agree with the mutant- disembowelment solves the fake accent problem.", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> I really don't get how people made this film and thought it was worth all the work they put into it. Even more puzzling are those who watched this film without feeling annoyed about the 88 minutes of doing something pointless and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines worse than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their terrible acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was awful. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes no sense unless you're trashed. - theme (Nothing to learn from this film. So little to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as boring as the script). - scenery (Could have been this film's saving grace, but no...everything missing here. Even the rocks are fake). So, yeah. If you care about that or you're just a horny teen with bad taste in music and "women," this movie is for you. Other comments: dull cinematography at times. Very fake gore. But the intestines scene is laughable. I agree with the mutant- disembowelment solves the fake accent problem.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bewitch`, `brilliant`, `classic`, `content`, `downfall`, `good`, `interest`, `lot`, `much`, `n't`, `nothing`, `outstanding`, `perfect`, `real`, `realistic`, `relax`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["outstanding", "perfect", "brilliant", "bewitching", "realistic"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `outstanding`(1), `perfect`(2), `brilliant`(3), `bewitch`(4), `realistic`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.0741 |
| H–CF | 0.7500 | 0.2069 |
| H–RO | 1.0000 | 0.0926 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 1.0000 | 0.3125 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |
| RBO (H,RO) | 0.2508 |

### cad_imdb_dev_000220 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"negative"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Verbalized confidence:** 0.99
- **Model refused:** No
- **Input length:** 50 words
- **Raw response length:** 20 chars
- **Prompt hash:** `c831d668eac72d2d`
- **ECS (full):** 0.6345
- **ECS (extraction–rationale):** 0.6439
- **ECS (extraction–perturbation):** 0.6299
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 5 | **CC4 size:** 5

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 99}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["I", 3], ["think", 4], ["Via", 2], ["Satellite", 2], ["is", 2], ["one", 2], ["of", 1], ["the", 1], ["lamest", 10], ["New", 2], ["Zealand", 2], ["made", 3], ["movies", 5], ["around", 2], [".", 1], ["I", 3], ["detested", 10], ["the", 1], ["way", 3], ["the", 1], ["movie", 4], ["delt", 5], ["with", 2], ["all", 3], ["the", 1], ["characters", 6], ["within", 3], ["the", 1], ["entire", 4], ["movie", 4], [".", 1], ["It", 3], ["was", 2], ["rubbish", 9], [",", 1], ["and", 2], ["a", 1], ["pitiful", 9], ["movie", 4], [".", 1], ["A", 1], ["feeble", 8], ["movie", 4], [",", 1], ["one", 2], ["which", 2], ["I", 3], ["will", 2], ["always", 5], ["remember", 6], ["poorly", 7], [",", 1], ["and", 2], ["never", 6], ["watch", 4], ["again", 5], ["." ,1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `always`, `character`, `detest`, `feeble`, `lame`, `never`, `pitiful`, `poorly`, `remember`, `rubbish`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses strong disapproval and criticism of the movie using negative language such as 'lamest,' 'detested,' 'rubbish,' 'pitiful,' and 'feeble,' indicating a clearly negative sentiment."}
```

**Rationale text:**
> The text expresses strong disapproval and criticism of the movie using negative language such as 'lamest,' 'detested,' 'rubbish,' 'pitiful,' and 'feeble,' indicating a clearly negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `detest`, `feeble`, `lame`, `movie`, `pitiful`, `rubbish`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "I think Via Satellite is one of the finest New Zealand made movies around. I loved the way the movie dealt with all the characters within the entire movie. It was brilliant, and a remarkable movie. A strong movie, one which I will always remember fondly, and never watch again.", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> I think Via Satellite is one of the finest New Zealand made movies around. I loved the way the movie dealt with all the characters within the entire movie. It was brilliant, and a remarkable movie. A strong movie, one which I will always remember fondly, and never watch again.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `delt`, `detest`, `feeble`, `lame`, `pitiful`, `poorly`, `rubbish`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["detested", "rubbish", "lamest", "pitiful", "feeble"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `detest`(1), `rubbish`(2), `lame`(3), `pitiful`(4), `feeble`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8333 | 0.4545 |
| H–CF | 0.8571 | 0.5455 |
| H–RO | 1.0000 | 0.5000 |
| R–CF | 0.8333 | 0.6250 |
| R–RO | 1.0000 | 0.8333 |
| CF–RO | 1.0000 | 0.7143 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.6000 |
| Normalized τ | 0.8000 |
| RBO (H,RO) | 0.4979 |

### cad_imdb_dev_000284 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 110 words
- **Raw response length:** 20 chars
- **Prompt hash:** `973c726ddbbfd9e7`
- **ECS (full):** 0.2192
- **ECS (extraction–rationale):** 0.0956
- **ECS (extraction–perturbation):** 0.4167
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 1

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 95}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
    "salience": [
        ["Well", 2],
        ["what", 1],
        ["can", 1],
        ["it", 1],
        ["be", 1],
        ["said", 1],
        ["about", 1],
        ["this", 3],
        ["fabulous", 9],
        ["thing?", 1],
        ["I", 1],
        ["watched", 1],
        ["it", 1],
        ["because", 1],
        ["it", 1],
        ["aired", 1],
        ["on", 1],
        ["cable.", 1],
        ["I", 1],
        ["loved", 10],
        ["it.", 1],
        ["The", 1],
        ["creature", 3],
        ["is", 1],
        ["the", 1],
        ["scariest", 8],
        ["you", 1],
        ["can", 1],
        ["get!", 1],
        ["Please,", 1],
        ["you", 1],
        ["need", 1],
        ["to", 1],
        ["be", 1],
        ["very", 1],
        ["generous", 1],
        ["not", 1],
        ["to", 1],
        ["get", 1],
        ["scared", 1],
        ["by", 1],
        ["the", 1],
        ["amazing", 8],
        ["Halloween", 1],
        ["costume.", 1],
        ["Oh", 1],
        ["well,", 1],
        ["there", 1],
        ["are", 1],
        ["also", 1],
        ["displays", 1],
        ["of", 1],
        ["great", 9],
        ["acting,", 1],
        ["f/x,", 1],
        ["and", 1],
        ["dialogues.", 1],
        ["The", 1],
        ["confrontation", 1],
        ["with", 1],
        ["the", 1],
        ["creature", 1],
        ["is", 1],
        ["unbelievable,", 8],
        ["you", 1],
        ["can't", 1],
        ["get", 1],
        ["a", 1],
        ["more", 1],
        ["amazing", 8],
        ["scene.", 1],
        ["This", 1],
        ["is", 1],
        ["the", 1],
        ["best", 10],
        ["you", 1],
        ["can", 1],
        ["get", 1],
        ["from", 1],
        ["direct", 1],
        ["to", 1],
        ["video", 1],
        ["flicks.", 1],
        ["\"Creature", 1],
        ["Unknown\"", 1],
        ["makes", 1],
        ["FULL", 1],
        ["MOON", 1],
        ["PICTURES", 1],
        ["movies", 1],
        ["look", 1],
        ["like", 1],
        ["\"Halloween\".", 1],
        ["I", 1],
        ["recommend", 10],
        ["at", 1],
        ["all", 1],
        ["costs,", 1],
        ["please.", 1],
        ["The", 1],
        ["only", 1],
        ["\"negative\"", 1],
        ["thing", 1],
        ["about", 1],
        ["this", 1],
        ["great", 9],
        ["movie", 1],
        ["are", 1],
        ["the", 1],
        ["women.", 1]
    ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `air`, `all`, `also`, `amaze`, `best`, `cable`, `can't`, `confrontation`, `cost`, `costume`, `creature`, `dialogue`, `direct`, `display`, `fabulous`, `great`, `love`, `recommend`, `scary`, `unbelievable`, `well`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is overwhelmingly positive, praising the movie's scariness, acting, effects, and scenes, with the single negative comment about the women being downplayed as the only flaw in a 'great movie'."}
```

**Rationale text:**
> The text is overwhelmingly positive, praising the movie's scariness, acting, effects, and scenes, with the single negative comment about the women being downplayed as the only flaw in a 'great movie'.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `great`, `movie`, `scene`, `woman`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
```json
{
    "rewritten": "Well, what can it be said about this terrible thing? I watched it because it aired on cable. I hated it. The creature is the lamest you can get! Please, you need to be very generous not to be bored by the awful Halloween costume. Oh well, there are also displays of terrible acting, f/x, and dialogues. The confrontation with the creature is ridiculous, you can't get a more disappointing scene. This is the worst you can get from direct to video flicks. \"Creature Unknown\" makes FULL MOON PICTURES movies look like \"Halloween\". I do not recommend at all, please. The only \"negative\" thing about this awful movie are the women.",
    "new_prediction": "negative"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> Well, what can it be said about this terrible thing? I watched it because it aired on cable. I hated it. The creature is the lamest you can get! Please, you need to be very generous not to be bored by the awful Halloween costume. Oh well, there are also displays of terrible acting, f/x, and dialogues. The confrontation with the creature is ridiculous, you can't get a more disappointing scene. This is the worst you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I do not recommend at all, please. The only "negative" thing about this awful movie are the women.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amaze`, `best`, `cost`, `fabulous`, `get`, `great`, `love`, `scar`, `scary`, `unbelievable`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scared by the amazing Halloween costume. Oh well, there are also displays of great acting, f/x, and dialogues. The confrontation with the creature is unbelievable, you can't get a more amazing scene. This is the best you can get from direct to video flicks. "Creature Unknown" makes FULL MOON PICTURES movies look like "Halloween". I recommend at all costs, please. The only "negative" thing about this great movie are the women."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["loved", "best", "great", "amazing", "fabulous"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `best`(2), `great`(3), `amaze`(4), `fabulous`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.4000 | 0.0800 |
| H–CF | 0.8000 | 0.3333 |
| H–RO | 1.0000 | 0.2273 |
| R–CF | 0.2000 | 0.0714 |
| R–RO | 0.2000 | 0.1111 |
| CF–RO | 1.0000 | 0.5000 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |
| RBO (H,RO) | 0.4790 |

### cad_imdb_test_000501 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.05
- **Model refused:** No
- **Input length:** 190 words
- **Raw response length:** 20 chars
- **Prompt hash:** `ebd4951c603a1d3d`
- **ECS (full):** 0.2806
- **ECS (extraction–rationale):** 0.2548
- **ECS (extraction–perturbation):** 0.3134
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 7 | **CC4 size:** 2

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 5}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
    "salience": [
        ["This", 2],
        ["film", 8],
        ["is", 3],
        ["the", 1],
        ["best", 10],
        ["motion", 5],
        ["picture", 5],
        ["I", 3],
        ["have", 3],
        ["EVER", 10],
        ["seen", 5],
        [".", 1],
        ["To", 2],
        ["begin", 2],
        [",", 1],
        ["I", 3],
        ["'d", 2],
        ["like", 3],
        ["to", 2],
        ["say", 3],
        ["the", 1],
        ["the", 1],
        ["front", 4],
        ["cover", 4],
        ["of", 1],
        ["this", 2],
        ["film", 8],
        ["is", 3],
        ["great", 8],
        [",", 1],
        ["if", 2],
        ["you", 2],
        ["think", 3],
        ["you", 2],
        ["are", 2],
        ["about", 2],
        ["to", 2],
        ["see", 5],
        ["a", 1],
        ["truly", 6],
        ["scary", 6],
        ["horror", 6],
        ["film", 8],
        ["with", 2],
        ["a", 1],
        ["monster", 5],
        ["clown", 5],
        [",", 1],
        ["you", 2],
        ["are", 2],
        ["soooo", 9],
        ["right", 6],
        [".", 1],
        ["In", 2],
        ["fact", 3],
        ["the", 1],
        ["killers", 4],
        ["face", 4],
        ["looks", 4],
        ["exactly", 6],
        ["like", 3],
        ["the", 1],
        ["front", 4],
        ["cover", 4],
        [",", 1],
        ["it", 3],
        ["'s", 3],
        ["just", 3],
        ["an", 1],
        ["image", 4],
        ["they", 3],
        ["must", 3],
        ["have", 3],
        ["found", 4],
        ["on", 2],
        ["Google", 4],
        ["and", 1],
        ["thought", 4],
        ["it", 3],
        ["looked", 4],
        ["cool", 6],
        [".", 1],
        ["Speaking", 3],
        ["of", 1],
        ["things", 3],
        ["they", 3],
        ["found", 4],
        ["and", 1],
        ["thought", 4],
        ["it", 3],
        ["looked", 4],
        ["cool", 6],
        [",", 1],
        ["there", 2],
        ["is", 3],
        ["a", 1],
        ["scene", 5],
        ["in", 2],
        ["this", 2],
        ["film", 8],
        ["where", 3],
        ["some", 2],
        ["of", 1],
        ["the", 1],
        ["gang", 4],
        ["are", 2],
        ["searching", 4],
        ["for", 2],
        ["the", 1],
        ["friend", 4],
        ["in", 2],
        ["the", 1],
        ["old", 3],
        ["woods", 4],
        [",", 1],
        ["then", 2],
        ["suddenly", 4],
        ["the", 1],
        ["screen", 4],
        ["chops", 4],
        ["to", 2],
        ["a", 1],
        ["scene", 5],
        ["where", 3],
        ["there", 2],
        ["is", 3],
        ["a", 1],
        ["mother", 4],
        ["deer", 4],
        ["nurturing", 5],
        ["it", 3],
        ["'s", 3],
        ["young", 4],
        ["in", 2],
        ["a", 1],
        ["glisten", 5],
        ["of", 1],
        ["sunlight", 5],
        ["...", 3],
        ["I", 3],
        ["mean", 4],
        ["seriously", 7],
        ["awesome", 10],
        ["!!!", 8],
        ["It", 3],
        ["'s", 3],
        ["so", 7],
        ["relevant", 5],
        ["to", 2],
        ["the", 1],
        ["dark", 4],
        ["woods", 4],
        ["they", 3],
        ["are", 2],
        ["wandering", 4],
        ["through", 3],
        ["?", 3],
        ["I", 3],
        ["bought", 3],
        ["this", 2],
        ["film", 8],
        ["from", 2],
        ["a", 1],
        ["man", 2],
        ["at", 2],
        ["a", 1],
        ["market", 3],
        ["hoping", 4],
        ["it", 3],
        ["would", 3],
        ["be", 3],
        ["entertaining", 7],
        [",", 1],
        ["if", 2],
        ["it", 3],
        ["was", 3],
        ["n't", 3],
        ["horror", 6],
        ["then", 2],
        ["at", 2],
        ["least", 4],
        ["it", 3],
        ["would", 3],
        ["be", 3],
        ["funny", 7],
        ["right", 6],
        ["?", 3],
        ["RIGHT", 8],
        ["!", 5],
        ["The", 2],
        ["next", 3],
        ["day", 3],
        ["I", 3],
        ["GAVE", 9],
        ["it", 3],
        ["to", 2],
        ["my", 3],
        ["work", 4],
        ["colleague", 4],
        ["because", 4],
        ["I", 3],
        ["had", 3],
        ["to", 2],
        ["share", 8],
        [".", 1],
        ["Bottom", 4],
        ["line", 4],
        ["is", 3],
        [":", 2],
        ["SEE", 10],
        ["THIS", 8],
        ["FILM", 10],
        ["!!!", 10]
    ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`, `best`, `bottom`, `chop`, `clown`, `colleague`, `cool`, `cover`, `dark`, `deer`, `entertain`, `ever`, `exactly`, `face`, `film`, `find`, `friend`, `front`, `funny`, `gang`, `give`, `glisten`, `great`, `horror`, `monster`, `motion`, `nurture`, `picture`, `relevant`, `right`, `scary`, `scene`, `see`, `seriously`, `share`, `soooo`, `sunlight`, `truly`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is overwhelmingly positive because the author uses extreme praise like 'best motion picture I have EVER seen' and 'seriously awesome', enthusiastically recommends others see it, and shares the film with a colleague."}
```

**Rationale text:**
> The text is overwhelmingly positive because the author uses extreme praise like 'best motion picture I have EVER seen' and 'seriously awesome', enthusiastically recommends others see it, and shares the film with a colleague.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`, `colleague`, `ever`, `film`, `motion`, `picture`, `see`, `seriously`, `share`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
```json
{
    "rewritten": "This film is the worst motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is misleading, if you think you are about to see a truly scary horror film with a monster clown, you are soooo wrong. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cheap. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awful!!! It's so irrelevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? WRONG! The next day I DUMPED it on my work colleague because I had to get rid of it. Bottom line is: AVOID THIS FILM!!!",
    "new_prediction": "negative"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> This film is the worst motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is misleading, if you think you are about to see a truly scary horror film with a monster clown, you are soooo wrong. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cheap. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awful!!! It's so irrelevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? WRONG! The next day I DUMPED it on my work colleague because I had to get rid of it. Bottom line is: AVOID THIS FILM!!!

**Parsed tokens:**
- Status: **Valid**
- Tokens: `awesome`, `best`, `cool`, `film`, `give`, `great`, `relevant`, `right`, `see`, `share`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster clown, you are soooo right. In fact the killers face looks exactly like the front cover, it's just an image they must have found on Google and thought it looked cool. Speaking of things they found and thought it looked cool, there is a scene in this film where some of the gang are searching for the friend in the old woods, then suddenly the screen chops to a scene where there is a mother deer nurturing it's young in a glisten of sunlight... I mean seriously awesome!!! It's so relevant to the dark woods they are wandering through? I bought this film from a man at a market hoping it would be entertaining, if it wasn't horror then at least it would be funny right? RIGHT! The next day I GAVE it to my work colleague because I had to share. Bottom line is: SEE THIS FILM!!!"

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["best", "awesome", "great", "SEE", "EVER"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `best`(1), `awesome`(2), `great`(3), `see`(4), `ever`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2368 |
| H–CF | 1.0000 | 0.2632 |
| H–RO | 1.0000 | 0.1316 |
| R–CF | 0.4444 | 0.2667 |
| R–RO | 0.6000 | 0.2727 |
| CF–RO | 0.8000 | 0.3636 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.2000 |
| Normalized τ | 0.6000 |
| RBO (H,RO) | 0.4760 |

### cad_imdb_dev_000699 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
```json
{"label":"positive"}
```
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 166 words
- **Raw response length:** 32 chars
- **Prompt hash:** `e4542f4cd92447dd`
- **ECS (full):** 0.2891
- **ECS (extraction–rationale):** 0.2924
- **ECS (extraction–perturbation):** 0.3434
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 6 | **CC4 size:** 3

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 100}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
  "salience": [
    ["For", 1],
    ["the", 1],
    ["first", 1],
    ["forty", 1],
    ["minutes", 1],
    [",", 1],
    ["Empire", 3],
    ["really", 2],
    ["shapes", 2],
    ["itself", 1],
    ["up", 1],
    [":", 1],
    ["it", 1],
    ["is", 1],
    ["a", 1],
    ["strong", 8],
    [",", 1],
    ["confident", 8],
    [",", 1],
    ["though", 1],
    ["relatively", 1],
    ["unknown", 1],
    ["gangster", 1],
    ["flick", 1],
    [".", 1],
    ["At", 1],
    ["the", 1],
    ["time", 1],
    ["I", 1],
    ["didn't", 1],
    ["know", 1],
    ["why", 1],
    ["I", 1],
    ["knew", 1],
    ["it", 1],
    ["was", 1],
    ["good", 9],
    ["-", 1],
    ["but", 1],
    ["now", 1],
    ["I", 1],
    ["do", 1],
    [".", 1],
    ["One", 1],
    ["of", 1],
    ["the", 1],
    ["main", 1],
    ["strong", 8],
    ["points", 1],
    ["with", 1],
    ["this", 1],
    ["film", 1],
    ["is", 1],
    ["that", 1],
    ["it", 1],
    ["is", 1],
    ["purely", 7],
    ["and", 1],
    ["utterly", 7],
    ["classy", 9],
    ["and", 1],
    ["tasteful", 9],
    [".", 1],
    ["I", 1],
    ["don't", 1],
    ["mind", 1],
    ["films", 1],
    ["with", 1],
    ["psychos", 1],
    ["and", 1],
    ["things", 1],
    [",", 1],
    ["to", 1],
    ["prove", 1],
    ["a", 1],
    ["point", 1],
    ["-", 1],
    ["take", 1],
    ["Jackie", 1],
    ["Brown", 1],
    [",", 1],
    ["for", 1],
    ["example", 1],
    ["-", 1],
    ["but", 1],
    ["they're", 1],
    ["all", 1],
    ["so", 1],
    ["terrifically", 8],
    ["meaningful", 8],
    ["in", 1],
    ["this", 1],
    ["and", 1],
    ["that", 1],
    ["is", 1],
    ["obviously", 1],
    ["included", 1],
    ["for", 1],
    ["entertainment", 1],
    [".", 1],
    ["You", 1],
    ["literally", 1],
    ["feel", 1],
    ["a", 1],
    ["knot", 1],
    ["of", 1],
    ["excitement", 9],
    ["in", 1],
    ["your", 1],
    ["stomach", 1],
    [".", 1],
    ["Another", 1],
    ["major", 1],
    ["strong", 8],
    ["point", 1],
    ["is", 1],
    ["the", 1],
    ["protagonist", 1],
    [".", 1],
    ["He", 1],
    ["is", 1],
    ["not", 1],
    ["smug", 1],
    ["or", 1],
    ["arrogant", 1],
    ["and", 1],
    ["-", 1],
    ["expectedly", 1],
    ["-", 1],
    ["not", 1],
    ["that", 1],
    ["bad", 1],
    [".", 1],
    ["He", 1],
    ["seems", 1],
    ["just", 1],
    ["right", 1],
    ["to", 1],
    ["be", 1],
    ["a", 1],
    ["drug-dealing", 1],
    ["woman", 1],
    ["killer", 1],
    [".", 1],
    ["The", 1],
    ["fact", 1],
    ["is", 1],
    [",", 1],
    ["at", 1],
    ["the", 1],
    ["end", 1],
    ["of", 1],
    ["the", 1],
    ["day", 1],
    [",", 1],
    ["this", 1],
    ["film", 1],
    ["is", 1],
    ["completely", 8],
    ["perfect", 10],
    [".", 1],
    ["Slick", 9],
    [",", 1],
    ["clever", 9],
    [",", 1],
    ["never", 1],
    ["dull", 1],
    [",", 1],
    ["and", 1],
    ["always", 1],
    ["meaningful", 8],
    ["-", 1],
    ["this", 1],
    ["incredible", 10],
    ["masterpiece", 10],
    ["should", 1],
    ["be", 1],
    ["applauded", 9],
    ["at", 1],
    ["all", 1],
    ["times", 1],
    [".", 1],
    ["*****", 10],
    ["out", 1],
    ["of", 1],
    ["*****", 10],
    ["(", 1],
    ["5", 10],
    ["out", 1],
    ["of", 1],
    ["5", 10],
    [")", 1]
  ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `5`, `all`, `always`, `another`, `applaud`, `arrogant`, `bad`, `brown`, `classy`, `clever`, `completely`, `confident`, `day`, `didn't`, `don't`, `drug-dealing`, `dull`, `empire`, `excitement`, `good`, `incredible`, `masterpiece`, `meaningful`, `perfect`, `purely`, `really`, `shape`, `slick`, `strong`, `tasteful`, `terrifically`, `utterly`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is overwhelmingly positive, using effusive praise like 'completely perfect,' 'incredible masterpiece,' and a 5/5 rating to express strong approval."}
```

**Rationale text:**
> The text is overwhelmingly positive, using effusive praise like 'completely perfect,' 'incredible masterpiece,' and a 5/5 rating to express strong approval.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `completely`, `incredible`, `masterpiece`, `perfect`, `strong`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
```json
{
  "rewritten": "For the first forty minutes, Empire really falls apart: it is a weak, uncertain, and relatively unknown gangster flick. At the time I didn't know why I knew it was bad- but now I do. One of the main weak points with this film is that it is purely and utterly tacky and tasteless. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terribly meaningless in this and that is obviously included for boredom. You literally feel a knot of dread in your stomach. Another major weak point is the protagonist. He is smug and arrogant and - expectedly - that bad. He seems just wrong to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely flawed. Sloppy, stupid, always dull, and never meaningful - this terrible disaster should be criticized at all times. * out of ***** (1 out of 5)",
  "new_prediction": "negative"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> For the first forty minutes, Empire really falls apart: it is a weak, uncertain, and relatively unknown gangster flick. At the time I didn't know why I knew it was bad- but now I do. One of the main weak points with this film is that it is purely and utterly tacky and tasteless. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terribly meaningless in this and that is obviously included for boredom. You literally feel a knot of dread in your stomach. Another major weak point is the protagonist. He is smug and arrogant and - expectedly - that bad. He seems just wrong to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely flawed. Sloppy, stupid, always dull, and never meaningful - this terrible disaster should be criticized at all times. * out of ***** (1 out of 5)

**Parsed tokens:**
- Status: **Valid**
- Tokens: `5`, `always`, `applaud`, `classy`, `clever`, `confident`, `entertainment`, `excitement`, `good`, `incredible`, `masterpiece`, `meaningful`, `never`, `not`, `perfect`, `right`, `shape`, `slick`, `strong`, `tasteful`, `terrifically`, `though`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of the main strong points with this film is that it is purely and utterly classy and tasteful. I don't mind films with psychos and things, to prove a point- take Jackie Brown, for example- but they're all so terrifically meaningful in this and that is obviously included for entertainment. You literally feel a knot of excitement in your stomach. Another major strong point is the protagonist. He is not smug or arrogant and - expectedly - not that bad. He seems just right to be a drug-dealing woman killer. The fact is, at the end of the day, this film is completely perfect. Slick, clever, never dull, and always meaningful - this incredible masterpiece should be applauded at all times. ***** out of ***** (5 out of 5)"

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
```json
{"ranking": ["perfect", "masterpiece", "incredible", "applauded", "excitement"]}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `perfect`(1), `masterpiece`(2), `incredible`(3), `applaud`(4), `excitement`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.1562 |
| H–CF | 0.7727 | 0.4595 |
| H–RO | 1.0000 | 0.1562 |
| R–CF | 0.8000 | 0.1739 |
| R–RO | 0.6000 | 0.4286 |
| CF–RO | 1.0000 | 0.2273 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |
| RBO (H,RO) | 0.4020 |

### cad_imdb_dev_000531 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 275 words
- **Raw response length:** 20 chars
- **Prompt hash:** `6d0a18e2e553b3d6`
- **ECS (full):** 0.1954
- **ECS (extraction–rationale):** 0.2091
- **ECS (extraction–perturbation):** 0.2218
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 3

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 95}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
    "salience": [
        ["I", 1],
        ["really", 2],
        ["don't", 1],
        ["get", 1],
        ["how", 1],
        ["people", 1],
        ["made", 1],
        ["this", 1],
        ["film", 1],
        ["and", 1],
        ["thought", 1],
        ["it", 1],
        ["wasn't", 1],
        ["worth", 1],
        ["all", 1],
        ["the", 1],
        ["work", 1],
        ["they", 1],
        ["put", 1],
        ["into", 1],
        ["it.", 1],
        ["Even", 1],
        ["more", 1],
        ["puzzling", 1],
        ["are", 1],
        ["those", 1],
        ["who", 1],
        ["watched", 1],
        ["this", 1],
        ["film", 1],
        ["without", 1],
        ["feeling", 1],
        ["content", 3],
        ["about", 1],
        ["the", 1],
        ["88", 1],
        ["minutes", 1],
        ["of", 1],
        ["doing", 1],
        ["something", 1],
        ["relaxing", 3],
        ["and", 1],
        ["not", 1],
        ["cleaning", 1],
        ["under", 1],
        ["the", 1],
        ["couch", 1],
        ["or", 1],
        ["reading", 1],
        ["Leviticus.", 1],
        ["First", 1],
        ["of", 1],
        ["all,", 1],
        ["they", 1],
        ["had", 1],
        ["real", 4],
        ["Irish", 1],
        ["people,", 1],
        ["and", 1],
        ["some", 1],
        ["good-looking", 4],
        ["women", 1],
        ["who", 1],
        ["could", 1],
        ["deliver", 1],
        ["their", 1],
        ["lines", 1],
        ["better", 4],
        ["than", 1],
        ["the", 1],
        ["stunning,", 1],
        ["talented", 1],
        ["porn", 1],
        ["stars", 1],
        ["sprinkled", 1],
        ["throughout", 1],
        ["this", 1],
        ["film.", 1],
        ["Granted,", 1],
        ["the", 1],
        ["gore", 1],
        ["works-", 1],
        ["but", 1],
        ["strangely,", 1],
        ["it's", 1],
        ["not", 1],
        ["as", 1],
        ["troubling", 1],
        ["as", 1],
        ["you", 1],
        ["might", 1],
        ["think", 1],
        ["to", 1],
        ["see", 1],
        ["organs", 1],
        ["yanked", 1],
        ["out", 1],
        ["of", 1],
        ["the", 1],
        ["porn", 1],
        ["stars'", 1],
        ["hot,", 1],
        ["tight", 1],
        ["bodies", 1],
        ["left", 1],
        ["and", 1],
        ["right.", 1],
        ["Probably", 1],
        ["has", 1],
        ["something", 1],
        ["to", 1],
        ["do", 1],
        ["with", 1],
        ["the", 1],
        ["fact", 1],
        ["that", 1],
        ["after", 1],
        ["their", 1],
        ["brilliant", 8],
        ["acting", 8],
        ["you", 1],
        ["just", 1],
        ["want", 1],
        ["them", 1],
        ["to", 1],
        ["die", 1],
        ["in", 1],
        ["pain.", 1],
        ["So,", 1],
        ["if", 1],
        ["you", 1],
        ["care", 1],
        ["at", 1],
        ["all", 1],
        ["about", 1],
        ["the", 1],
        ["following:", 1],
        ["-", 1],
        ["acting", 9],
        ["(", 1],
        ["seriously,", 1],
        ["everyone", 1],
        ["was", 1],
        ["outstanding.", 9],
        ["I've", 1],
        ["never", 1],
        ["witnessed", 1],
        ["this", 1],
        ["before.", 1],
        ["EVERYONE.", 1],
        ["-plot", 9],
        ["(", 1],
        ["some", 1],
        ["crappy", 1],
        ["horror", 1],
        ["movies", 1],
        ["are", 1],
        ["remotely", 1],
        ["linear,", 1],
        ["or", 1],
        ["at", 1],
        ["the", 1],
        ["very", 1],
        ["least", 1],
        ["surprising.", 1],
        ["This", 1],
        ["movie", 1],
        ["makes", 1],
        ["perfect", 8],
        ["sense", 8],
        ["unless", 1],
        ["you're", 1],
        ["trashed.", 1],
        ["-", 1],
        ["theme", 9],
        ["(", 1],
        ["Lots", 1],
        ["to", 1],
        ["learn", 8],
        ["from", 1],
        ["this", 1],
        ["film.", 1],
        ["So", 1],
        ["much", 1],
        ["to", 1],
        ["be", 1],
        ["scared", 1],
        ["about", 1],
        ["in", 1],
        ["bed", 1],
        ["at", 1],
        ["night,", 1],
        ["to", 1],
        ["contemplate", 1],
        ["or", 1],
        ["grasp,", 1],
        ["and", 1],
        ["explain", 1],
        ["to", 1],
        ["others).", 1],
        ["-", 1],
        ["soundtrack", 9],
        ["(", 1],
        ["Wow,", 1],
        ["Music", 1],
        ["as", 1],
        ["bewitching", 8],
        ["as", 1],
        ["the", 1],
        ["script).", 1],
        ["-", 1],
        ["scenery", 9],
        ["(", 1],
        ["Could", 1],
        ["have", 1],
        ["been", 1],
        ["this", 1],
        ["film's", 1],
        ["saving", 1],
        ["downfall,", 1],
        ["but", 1],
        ["no...nothing", 1],
        ["missing", 1],
        ["here.", 1],
        ["Even", 1],
        ["the", 1],
        ["rocks", 1],
        ["are", 1],
        ["real).", 1],
        ["So,", 1],
        ["yeah.", 1],
        ["If", 1],
        ["you", 1],
        ["care", 1],
        ["about", 1],
        ["that", 1],
        ["or", 1],
        ["you're", 1],
        ["just", 1],
        ["a", 1],
        ["horny", 1],
        ["teen", 1],
        ["with", 1],
        ["good", 1],
        ["taste", 1],
        ["in", 1],
        ["music", 1],
        ["and", 1],
        ["\"women,\"", 1],
        ["this", 1],
        ["movie", 1],
        ["is", 1],
        ["for", 1],
        ["you.", 1],
        ["Other", 1],
        ["comments:", 1],
        ["interesting", 7],
        ["cinematography", 7],
        ["at", 1],
        ["times.", 1],
        ["Very", 1],
        ["realistic", 6],
        ["gore.", 1],
        ["But", 1],
        ["the", 1],
        ["intestines", 1],
        ["scene", 1],
        ["is", 1],
        ["classic.", 7],
        ["I", 1],
        ["agree", 1],
        ["with", 1],
        ["the", 1],
        ["mutant-", 1],
        ["disembowelment", 1],
        ["solves", 1],
        ["the", 1],
        ["fake", 1],
        ["accent", 1],
        ["problem.", 1]
    ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `88`, `accent`, `act`, `agree`, `all`, `bed`, `bewitch`, `body`, `brilliant`, `care`, `cinematography`, `classic`, `clean`, `comment`, `contemplate`, `content`, `couch`, `could`, `crappy`, `deliver`, `die`, `disembowelment`, `don't`, `downfall`, `even`, `everyone`, `fact`, `fake`, `feel`, `film`, `film's`, `first`, `follow`, `get`, `good`, `good-looking`, `gore`, `grant`, `grasp`, `horny`, `horror`, `interest`, `learn`, `outstanding`, `perfect`, `plot`, `real`, `realistic`, `really`, `relax`, `scenery`, `sense`, `soundtrack`, `theme`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is classified as positive because the author uses sarcastic praise to enthusiastically recommend the film, highlighting its outstanding acting, coherent plot, bewitching soundtrack, and realistic scenery as reasons to watch it."}
```

**Rationale text:**
> The text is classified as positive because the author uses sarcastic praise to enthusiastically recommend the film, highlighting its outstanding acting, coherent plot, bewitching soundtrack, and realistic scenery as reasons to watch it.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `act`, `bewitch`, `film`, `outstanding`, `plot`, `realistic`, `scenery`, `soundtrack`, `watch`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
```json
{
    "rewritten": "I really don't get how people made this film and thought it was worth all the work they put into it. Even more puzzling are those who watched this film without feeling bored about the 88 minutes of doing something tedious and not cleaning under the couch or reading Leviticus. First of all, they had fake Irish people, and some unattractive women who could deliver their lines worse than the stunning, untalented porn stars sprinkled throughout this film. Granted, the gore fails- but strangely, it's more troubling than you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their terrible acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was awful. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes no sense unless you're trashed. - theme (Nothing to learn from this film. So little to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Ugh, Music as dull as the script). - scenery (Could have been this film's saving downfall, but no...everything missing here. Even the rocks are fake). So, yeah. If you care about that or you're just a horny teen with bad taste in music and \"women,\" this movie is for you. Other comments: boring cinematography at times. Very unrealistic gore. But the intestines scene is forgettable. I agree with the mutant- disembowelment solves the fake accent problem.",
    "new_prediction": "negative"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> I really don't get how people made this film and thought it was worth all the work they put into it. Even more puzzling are those who watched this film without feeling bored about the 88 minutes of doing something tedious and not cleaning under the couch or reading Leviticus. First of all, they had fake Irish people, and some unattractive women who could deliver their lines worse than the stunning, untalented porn stars sprinkled throughout this film. Granted, the gore fails- but strangely, it's more troubling than you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their terrible acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was awful. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes no sense unless you're trashed. - theme (Nothing to learn from this film. So little to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Ugh, Music as dull as the script). - scenery (Could have been this film's saving downfall, but no...everything missing here. Even the rocks are fake). So, yeah. If you care about that or you're just a horny teen with bad taste in music and "women," this movie is for you. Other comments: boring cinematography at times. Very unrealistic gore. But the intestines scene is forgettable. I agree with the mutant- disembowelment solves the fake accent problem.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bewitch`, `brilliant`, `classic`, `content`, `good`, `good-looking`, `interest`, `lot`, `much`, `n't`, `not`, `nothing`, `outstanding`, `perfect`, `real`, `realistic`, `relax`, `talented`, `work`, `wow`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes of doing something relaxing and not cleaning under the couch or reading Leviticus. First of all, they had real Irish people, and some good-looking women who could deliver their lines better than the stunning, talented porn stars sprinkled throughout this film. Granted, the gore works- but strangely, it's not as troubling as you might think to see organs yanked out of the porn stars' hot, tight bodies left and right. Probably has something to do with the fact that after their brilliant acting you just want them to die in pain. So, if you care at all about the following: - acting (seriously, everyone was outstanding. I've never witnessed this before. EVERYONE. -plot (some crappy horror movies are remotely linear, or at the very least surprising. This movie makes perfect sense unless you're trashed. - theme (Lots to learn from this film. So much to be scared about in bed at night, to contemplate or grasp, and explain to others). - soundtrack (Wow, Music as bewitching as the script). - scenery (Could have been this film's saving downfall, but no...nothing missing here. Even the rocks are real). So, yeah. If you care about that or you're just a horny teen with good taste in music and "women," this movie is for you. Other comments: interesting cinematography at times. Very realistic gore. But the intestines scene is classic. I agree with the mutant- disembowelment solves the fake accent problem."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["outstanding", "bewitching", "classic", "relaxing", "realistic"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `outstanding`(1), `bewitch`(2), `classic`(3), `relax`(4), `realistic`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8889 | 0.1455 |
| H–CF | 0.6000 | 0.1935 |
| H–RO | 1.0000 | 0.0926 |
| R–CF | 0.3333 | 0.1154 |
| R–RO | 0.6000 | 0.2727 |
| CF–RO | 1.0000 | 0.2500 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | 0.8000 |
| Normalized τ | 0.9000 |
| RBO (H,RO) | 0.2286 |

### cad_imdb_dev_000220 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"negative"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 50 words
- **Raw response length:** 20 chars
- **Prompt hash:** `c831d668eac72d2d`
- **ECS (full):** 0.5889
- **ECS (extraction–rationale):** 0.5152
- **ECS (extraction–perturbation):** 0.7071
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 5 | **CC4 size:** 4

#### 4. Confidence Elicitation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

State how confident you are that this classification is correct, as a probability from 0 (certainly wrong) to 100 (certainly correct).

Return only valid JSON:
{"confidence": <0-100>}
```

**Response:**
```
{"confidence": 100}
```

#### 5. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["I", 1], ["think", 2], ["Via", 7], ["Satellite", 7], ["is", 1], ["one", 3], ["of", 1], ["the", 1], ["lamest", 10], ["New", 5], ["Zealand", 5], ["made", 1], ["movies", 5], ["around", 1], [".", 1], ["I", 1], ["detested", 10], ["the", 1], ["way", 2], ["the", 1], ["movie", 6], ["delt", 7], ["with", 1], ["all", 1], ["the", 1], ["characters", 5], ["within", 1], ["the", 1], ["entire", 1], ["movie", 6], [".", 1], ["It", 1], ["was", 1], ["rubbish", 10], [",", 1], ["and", 1], ["a", 1], ["pitiful", 10], ["movie", 6], [".", 1], ["A", 1], ["feeble", 10], ["movie", 6], [",", 1], ["one", 1], ["which", 1], ["I", 1], ["will", 1], ["always", 1], ["remember", 3], ["poorly", 8], [",", 1], ["and", 1], ["never", 8], ["watch", 3], ["again", 3], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `delt`, `detest`, `feeble`, `lame`, `never`, `pitiful`, `poorly`, `rubbish`, `satellite`, `via`

#### 6. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses strongly negative words like 'lamest', 'detested', 'rubbish', 'pitiful', and 'feeble' to express a harshly critical opinion of the movie."}
```

**Rationale text:**
> The text uses strongly negative words like 'lamest', 'detested', 'rubbish', 'pitiful', and 'feeble' to express a harshly critical opinion of the movie.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `detest`, `feeble`, `movie`, `pitiful`, `rubbish`

#### 7. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences. Keep the original spacing and punctuation style; only change the words you edit.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "I think Via Satellite is one of the finest New Zealand made movies around. I adored the way the movie delt with all the characters within the entire movie. It was brilliant, and a wonderful movie. A fantastic movie, one which I will always remember fondly, and always watch again.", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> I think Via Satellite is one of the finest New Zealand made movies around. I adored the way the movie delt with all the characters within the entire movie. It was brilliant, and a wonderful movie. A fantastic movie, one which I will always remember fondly, and always watch again.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `detest`, `feeble`, `lame`, `never`, `pitiful`, `poorly`, `rubbish`

#### 8. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A feeble movie, one which I will always remember poorly, and never watch again."

Identify the 5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3", "word4", "word5"]}
```

**Response:**
```
{"ranking": ["rubbish", "detested", "lamest", "pitiful", "feeble"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `rubbish`(1), `detest`(2), `lame`(3), `pitiful`(4), `feeble`(5)

#### 9. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.3636 |
| H–CF | 1.0000 | 0.7000 |
| H–RO | 1.0000 | 0.5000 |
| R–CF | 0.8000 | 0.5000 |
| R–RO | 0.8000 | 0.6667 |
| CF–RO | 1.0000 | 0.7143 |

Rank-based agreement (H vs RO):

| Metric | Value |
|--------|-------|
| Kendall τ (H,RO) | -0.2000 |
| Normalized τ | 0.4000 |
| RBO (H,RO) | 0.3796 |


## High-ECS Examples

### cad_imdb_dev_000220 — qwen3-235b (ECS=0.6345)
- **Dataset:** cad_imdb
- **Text:** I think Via Satellite is one of the lamest New Zealand made movies around. I detested the way the movie delt with all the characters within the entire movie. It was rubbish, and a pitiful movie. A fee…
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### cad_imdb_dev_000699 — deepseek-v3 (ECS=0.2891)
- **Dataset:** cad_imdb
- **Text:** For the first forty minutes, Empire really shapes itself up: it is a strong, confident, though relatively unknown gangster flick. At the time I didn't know why I knew it was good- but now I do. One of…
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### cad_imdb_test_000501 — deepseek-v3 (ECS=0.2806)
- **Dataset:** cad_imdb
- **Text:** This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster c…
- **Ground truth:** `positive` → **Predicted:** `positive` ✓


## Low-ECS Examples

### cad_imdb_dev_000531 — nova-pro (ECS=0.0420)
- **Dataset:** cad_imdb
- **Text:** I really don't get how people made this film and thought it wasn't worth all the work they put into it. Even more puzzling are those who watched this film without feeling content about the 88 minutes …
- **Ground truth:** `positive` → **Predicted:** `negative` ✗

### cad_imdb_test_000501 — nova-pro (ECS=0.1489)
- **Dataset:** cad_imdb
- **Text:** This film is the best motion picture I have EVER seen. To begin, I'd like to say the the front cover of this film is great, if you think you are about to see a truly scary horror film with a monster c…
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### cad_imdb_dev_000284 — qwen3-235b (ECS=0.1691)
- **Dataset:** cad_imdb
- **Text:** Well, what can it be said about this fabulous thing? I watched it because it aired on cable. I loved it. The creature is the scariest you can get! Please, you need to be very generous not to get scare…
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
