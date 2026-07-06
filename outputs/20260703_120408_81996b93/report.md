# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-03 12:04:18
- **Duration:** 75.7s (1.3m)
- **Models (3):** nova-pro (`eu.amazon.nova-pro-v1:0`), qwen3-235b (`qwen.qwen3-235b-a22b-2507-v1:0`), deepseek-v3 (`deepseek.v3-v1:0`)
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 16155
- **Avg tokens per instance:** 1795

## Per-Dataset Summary

| Model | Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|-------|---------|-----------|----------|----------|---|---|------|---|
| nova-pro | sst2 | 1 | 0/1 (0%) | 0.575 | 100% | 100% | 0% | 100% |
| qwen3-235b | sst2 | 1 | 1/1 (100%) | 0.200 | 100% | 100% | 0% | 100% |
| deepseek-v3 | sst2 | 1 | 1/1 (100%) | 0.253 | 100% | 100% | 100% | 100% |
| nova-pro | mnli | 1 | 1/1 (100%) | 0.333 | 100% | 100% | 0% | 100% |
| qwen3-235b | mnli | 1 | 0/1 (0%) | 0.267 | 100% | 100% | 100% | 100% |
| deepseek-v3 | mnli | 1 | 0/1 (0%) | 0.500 | 100% | 100% | 0% | 100% |
| nova-pro | ag_news | 1 | 1/1 (100%) | 0.500 | 100% | 100% | 0% | 100% |
| qwen3-235b | ag_news | 1 | 1/1 (100%) | 0.500 | 100% | 100% | 0% | 100% |
| deepseek-v3 | ag_news | 1 | 1/1 (100%) | 0.437 | 100% | 100% | 0% | 100% |

## Sampling Log

| Model | Dataset | Requested | Sampled | Wrong Pred |
|-------|---------|-----------|---------|------------|
| nova-pro | sst2 | 1 | 1 | 1 |
| qwen3-235b | sst2 | 1 | 1 | 0 |
| deepseek-v3 | sst2 | 1 | 1 | 0 |
| nova-pro | mnli | 1 | 1 | 0 |
| qwen3-235b | mnli | 1 | 1 | 1 |
| deepseek-v3 | mnli | 1 | 1 | 1 |
| nova-pro | ag_news | 1 | 1 | 0 |
| qwen3-235b | ag_news | 1 | 1 | 0 |
| deepseek-v3 | ag_news | 1 | 1 | 0 |
| **Total** | | 9 | 9 | 3 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=3) or medium-length (21–50 words, N=6). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=3). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=2)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 9/9 | 100% |
| Rationale | 9/9 | 100% |
| Counterfactual | 2/9 | 22% |
| Rank Ordering | 9/9 | 100% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

> **Pooled across models and datasets — descriptive context only.** The primary reporting unit is the model×dataset cell (tables below): pooled numbers mix heterogeneous tasks and models, and their bootstrap CI resamples instance clusters (the same instance appears under every model). At scale, **complete-case ECS is the primary estimand** — partial-case ECS averages whichever pairs survived, which changes the construct per instance.

| Metric | Value |
|--------|-------|
| **Mean ECS (complete cases, N=2) — primary estimand** | 0.2600 |
| Complete cases | 2/9 (22%) |
| Mean ECS (all with ≥3 valid, N=9) | 0.3961 |
| Mean ECS-overlap (size-robust secondary, same pairs) | 0.7083 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.4124 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.3167 |
| Std ECS | 0.1349 |
| Median ECS | 0.4365 |
| **Mean ECS lift over chance** (ECS − uniform random) | +0.2956 |
| Mean ECS random baseline (uniform) | 0.1005 |
| Mean ECS lift over salience-weighted null (secondary, N=9) | +0.1468 |

> **Significance testing: pre-registered tests only.** Exactly two test families run (FIX_PLAN §P1.3): (a) sign-flip permutation on per-instance ECS-lift per model×dataset cell, Holm-corrected across cells — results in the table below; (b) CC-erasure vs random control in the separate erasure pass. Every other number in this report — strata, splits, contrasts — is descriptive, and cells below the configured minimum N report estimates without a test.

| Introduced-concept rate (R) | 0.725 |
| CF canonical (minimal) validity rate | 22% |
| CF canonical validity — first attempt (single-shot, uncoached) | 22% |
| CF valid only after correction loop (coached stratum) | 0 instances |
| RO required hallucination self-correction | 2 instances |
| CF contrast (free) validity rate | 78% |
| CF canonical (minimal) minimality (edits/len) | 0.135 |
| CF contrast (free) minimality (edits/len) | 0.412 |
| Verbalized confidence — mean (N=9) | 0.903 |
| Mean CC3 size | 2.00 |
| Mean CC4 size | 1.56 |
| % instances with CC3 | 100.0% |
| % instances with CC4 | 77.8% |

> The CF minimal-vs-free validity contrast replicates the validity–minimality trade-off of arXiv:2509.09396 (*LLMs Don't Know Their Own Decision Boundaries*): unconstrained rewrites flip reliably but over-edit; minimal edits often fail to flip. Single-shot rates are reported separately from the coached loop because the correction re-prompt makes headline rates multi-shot-search rates (not comparable to single-shot elicitation in Madsen et al. 2024 / MiCE).

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pre-registered test (a): mean ECS-lift > 0, per model×dataset cell

One-sided sign-flip permutation on per-instance (ECS − ECS_random) differences; Holm-corrected across this run's cells. `—` = cell below the configured minimum N for testing (estimate reported, test skipped).

| Model | Dataset | N (lift) | Mean lift | p (raw) | p (Holm) |
|-------|---------|----------|-----------|---------|----------|
| nova-pro | sst2 | 1 | +0.4719 | — | — |
| qwen3-235b | sst2 | 1 | +0.1204 | — | — |
| deepseek-v3 | sst2 | 1 | +0.1573 | — | — |
| nova-pro | mnli | 1 | +0.2549 | — | — |
| qwen3-235b | mnli | 1 | +0.1873 | — | — |
| deepseek-v3 | mnli | 1 | +0.3534 | — | — |
| nova-pro | ag_news | 1 | +0.4020 | — | — |
| qwen3-235b | ag_news | 1 | +0.3853 | — | — |
| deepseek-v3 | ag_news | 1 | +0.3275 | — | — |

### ECS by prediction correctness (per cell only)

Reported per model×dataset cell only — pooled, this contrast is confounded by cell composition. Descriptive; no test.

| Model | Dataset | Mean ECS correct (N) | Mean ECS incorrect (N) |
|-------|---------|----------------------|------------------------|
| nova-pro | sst2 | 0.0000 (0) | 0.5750 (1) |
| qwen3-235b | sst2 | 0.2000 (1) | 0.0000 (0) |
| deepseek-v3 | sst2 | 0.2533 (1) | 0.0000 (0) |
| nova-pro | mnli | 0.3333 (1) | 0.0000 (0) |
| qwen3-235b | mnli | 0.0000 (0) | 0.2667 (1) |
| deepseek-v3 | mnli | 0.0000 (0) | 0.5000 (1) |
| nova-pro | ag_news | 0.5000 (1) | 0.0000 (0) |
| qwen3-235b | ag_news | 0.5000 (1) | 0.0000 (0) |
| deepseek-v3 | ag_news | 0.4365 (1) | 0.0000 (0) |

### Verbalized confidence ↔ ECS (Spearman, per cell)

Association estimate with a seeded bootstrap CI (pre-registered as an estimate, not a hypothesis test). Confidence is the model's verbalized 0–100 probability that its classification is correct (Tian et al. 2023; Xiong et al. 2024).

| Model | Dataset | N pairs | Spearman ρ | 95% CI |
|-------|---------|---------|------------|--------|
| nova-pro | sst2 | 1 | 0.000 | [0.000, 0.000] |
| qwen3-235b | sst2 | 1 | 0.000 | [0.000, 0.000] |
| deepseek-v3 | sst2 | 1 | 0.000 | [0.000, 0.000] |
| nova-pro | mnli | 1 | 0.000 | [0.000, 0.000] |
| qwen3-235b | mnli | 1 | 0.000 | [0.000, 0.000] |
| deepseek-v3 | mnli | 1 | 0.000 | [0.000, 0.000] |
| nova-pro | ag_news | 1 | 0.000 | [0.000, 0.000] |
| qwen3-235b | ag_news | 1 | 0.000 | [0.000, 0.000] |
| deepseek-v3 | ag_news | 1 | 0.000 | [0.000, 0.000] |

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) | N instances |
|------|----------------------|----------------|-------------|
| H–R | 0.7778 | 0.4519 | 9 |
| H–CF | 0.8333 | 0.3667 | 2 |
| H–RO | 0.7056 | 0.5182 | 9 |
| R–CF | 0.0000 | 0.0000 | 2 |
| R–RO | 0.7056 | 0.3729 | 9 |
| CF–RO | 0.6667 | 0.2667 | 2 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.2070 |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — and its cross-paradigm mean is the `ECS-overlap` secondary composite. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking (both rankings live in the same normalized token space); Kendall τ provides a complementary rank correlation measure.

## Cross-Model Agreement (same strategy, different models)

For every instance run under ≥2 models: the Jaccard between DIFFERENT models' evidence sets for the SAME strategy, next to the within-model cross-strategy ECS of the same instances. If within-model consensus systematically exceeds cross-model same-strategy agreement, stated evidence tracks model-specific computation (privileged self-knowledge, arXiv:2602.02639); if not, it is closer to a generic task prior shared across models (cf. the cross-model explanation lottery, arXiv:2603.15821). Zero extra API calls; descriptive.

| Dataset | N instances | H | R | CF | RO | Cross-model mean | Within-model mean ECS |
|---------|-------------|---|---|----|----|------------------|------------------------|
| ag_news | 1 | 0.620 (3) | 0.514 (3) | — (0) | 0.444 (3) | 0.526 | 0.479 |
| mnli | 1 | 1.000 (3) | 0.556 (3) | — (0) | 0.667 (3) | 0.741 | 0.367 |
| sst2 | 1 | 0.333 (3) | 0.472 (3) | — (0) | 0.717 (3) | 0.507 | 0.343 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 9/9 (100%) | 9/9 (100%) |
| Rationale | 9/9 (100%) | 9/9 (100%) |
| Counterfactual (JSON parsed) | 8/9 (89%) |
| Counterfactual (rules compliant) | 3/9 (33%) |
| Counterfactual (flip verified) | 2/3 (67%) |
| Rank Ordering | 9/9 (100%) | 9/9 (100%) |
| All 4 valid | 2/9 |
| 3 valid (CC3 adjusted) | 7/9 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 3 | 0.3667 |
| Medium (21–50) | 6 | 0.4108 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 6 | 0.4108 |
| Short vocab (≤20 unique tokens) | 3 | 0.3667 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.3961 | [0.3428, 0.4788] |

## Per-Instance Details

### sst2_validation_000665 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

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
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 25 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.5750
- **ECS (extraction–rationale):** 0.5750
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["and", 2],
    ["if", 5],
    ["you", 7],
    ["'re", 3],
    ["not", 8],
    ["nearly", 6],
    ["moved", 9],
    ["to", 4],
    ["tears", 9],
    ["by", 4],
    ["a", 2],
    ["couple", 5],
    ["of", 3],
    ["scenes", 7],
    [",", 1],
    ["you", 7],
    ["'ve", 3],
    ["got", 5],
    ["ice", 6],
    ["water", 7],
    ["in", 4],
    ["your", 6],
    ["veins", 7],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `not`, `scene`, `tear`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text implies a strong negative judgment on someone's emotional response, suggesting they are unfeeling or cold if not moved to tears."
}
```

**Rationale text:**
> The text implies a strong negative judgment on someone's emotional response, suggesting they are unfeeling or cold if not moved to tears.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `not`, `tear`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "and if you're nearly moved to joy by a couple of scenes, you've got warm blood in your veins.",
  "new_prediction": "positive"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "tears",
    "moved",
    "water",
    "ice",
    "veins"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tear`(1), `move`(2), `water`(3), `ice`(4), `vein`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.7500 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.3333 |
| R–CF | — | — |
| R–RO | 0.6667 | 0.4000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2067 |

### sst2_validation_000665 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

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
- **Input length:** 24 words
- **Raw response length:** 20 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.2000
- **ECS (extraction–rationale):** 0.2000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["and", 2], ["if", 5], ["you", 6], ["'", 1], ["re", 4], ["not", 8], ["nearly", 7], ["moved", 9], ["to", 3], ["tears", 10], ["by", 2], ["a", 1], ["couple", 5], ["of", 2], ["scenes", 7], [",", 1], ["you", 6], ["'", 1], ["ve", 4], ["got", 5], ["ice", 8], ["water", 7], ["in", 3], ["your", 5], ["veins", 9]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `move`, `tear`, `vein`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses strong emotional praise for the scenes, implying they are profoundly moving and impactful."}
```

**Rationale text:**
> The text expresses strong emotional praise for the scenes, implying they are profoundly moving and impactful.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `scene`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "and if you're not nearly moved to tears by a couple of scenes, you've got ice water in your veins and no soul.", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["tears", "moved", "ice", "veins"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tear`(1), `move`(2), `ice`(3), `vein`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.2000 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3169 |

### sst2_validation_000665 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

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
- **Input length:** 24 words
- **Raw response length:** 20 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.2533
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** 0.3000
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["and", 1], ["if", 2], ["you", 1], ["'re", 1], ["not", 8], ["nearly", 3], ["moved", 7], ["to", 1], ["tears", 9], ["by", 1], ["a", 1], ["couple", 1], ["of", 1], ["scenes", 5], [",", 1], ["you", 1], ["'ve", 1], ["got", 1], ["ice", 10], ["water", 9], ["in", 1], ["your", 1], ["veins", 8], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `not`, `tear`, `water`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses a positive sentiment by strongly praising the emotional power of the scenes, suggesting that a normal, empathetic human reaction would be to be moved to tears."}
```

**Rationale text:**
> The text expresses a positive sentiment by strongly praising the emotional power of the scenes, suggesting that a normal, empathetic human reaction would be to be moved to tears.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `scene`, `tear`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "and if you 're not nearly moved to tears by a couple of scenes , you 've got a heart of gold .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> and if you 're not nearly moved to tears by a couple of scenes , you 've got a heart of gold .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `vein`, `water`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["tears", "moved", "ice"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tear`(1), `move`(2), `ice`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.1667 |
| H–CF | 0.6667 | 0.4000 |
| H–RO | 0.6667 | 0.4000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | 0.3333 | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1354 |

### mnli_validation_matched_007919 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "neutral"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Verbalized confidence:** 0.70
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 24 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 5],
    ["just", 3],
    ["look", 4],
    ["what", 5],
    ["we", 5],
    ["did", 6],
    ["to", 4],
    ["Iraq", 8],
    ["Hypothesis:", 5],
    ["Iraq", 8],
    ["was", 5],
    ["something", 6],
    ["that", 5],
    ["shouldn't", 8],
    ["have", 6],
    ["happened", 7]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happen`, `iraq`, `shouldn't`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise does not provide enough information to determine whether the actions taken in Iraq were right or wrong, thus it is neutral with respect to the hypothesis."
}
```

**Rationale text:**
> The premise does not provide enough information to determine whether the actions taken in Iraq were right or wrong, thus it is neutral with respect to the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: just look what we did to Iraq\nHypothesis: Iraq was something that should have happened",
  "new_prediction": "contradiction"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `neutral`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["Iraq", "did", "look", "just", "happened"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`(1), `look`(2), `happen`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.5000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1990 |

### mnli_validation_matched_007919 — qwen3-235b

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 22 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** 0.2667
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 3], ["just", 6], ["look", 5], ["what", 7], ["we", 4], ["did", 8], ["to", 3], ["Iraq", 9], ["Hypothesis:", 3], ["Iraq", 9], ["was", 5], ["something", 4], ["that", 4], ["shouldn't", 9], ["have", 5], ["happened", 8]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happen`, `iraq`, `shouldn't`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise implies a negative reflection on the actions taken against Iraq, which supports the hypothesis that the event was unjustified or wrong."}
```

**Rationale text:**
> The premise implies a negative reflection on the actions taken against Iraq, which supports the hypothesis that the event was unjustified or wrong.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: just look what we did to Iraq\nHypothesis: Iraq was something that should have happened", "new_prediction": "contradiction"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: just look what we did to Iraq
Hypothesis: Iraq was something that should have happened

**Parsed tokens:**
- Status: **Valid**
- Tokens: `shouldn't`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Iraq", "shouldn't", "happened", "look", "did"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`(1), `look`(2), `shouldn't`(3), `happen`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | 1.0000 | 0.3333 |
| H–RO | 0.6667 | 0.5000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2537 |

### mnli_validation_matched_007919 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 22 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** 0.5000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["just", 2], ["look", 3], ["what", 4], ["we", 5], ["did", 8], ["to", 1], ["Iraq", 10], ["Iraq", 10], ["was", 3], ["something", 4], ["that", 3], ["shouldn't", 8], ["have", 2], ["happened", 7]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happen`, `iraq`, `shouldn't`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise 'just look what we did to Iraq' implies a negative judgment of the actions taken, which directly supports the hypothesis that 'Iraq was something that shouldn't have happened'."}
```

**Rationale text:**
> The premise 'just look what we did to Iraq' implies a negative judgment of the actions taken, which directly supports the hypothesis that 'Iraq was something that shouldn't have happened'.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happen`, `iraq`, `look`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: just look what we did to Iraq\nHypothesis: Iraq was something that was completely justified", "new_prediction": "contradiction"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Iraq", "shouldn't", "happened"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`(1), `shouldn't`(2), `happen`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.5000 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2710 |

### ag_news_test_004983 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.5000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Nokia", 8], ["announces", 7], ["Near", 9], ["Field", 9], ["Communication", 9], ["products", 6], ["With", 5], ["the", 3], ["Nokia", 8], ["NFC", 10], ["(Near", 9], ["Field", 9], ["Communication)", 9], ["shell", 6], ["on", 4], ["their", 4], ["phone,", 6], ["consumers", 7], ["will", 5], ["be", 4], ["able", 5], ["to", 4], ["access", 7], ["a", 2], ["variety", 6], ["of", 3], ["services", 7], ["and", 4], ["exchange", 7], ["information", 8], ["with", 5], ["a", 2], ["simple", 6], ["touch", 7], ["gesture.", 6]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `access`, `communication`, `field`, `information`, `near`, `nfc`, `nokia`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses a technological advancement by Nokia involving Near Field Communication (NFC), which is a tech-related topic."}
```

**Rationale text:**
> The text discusses a technological advancement by Nokia involving Near Field Communication (NFC), which is a tech-related topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `nfc`, `nokia`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
For "World":
{"rewritten": "Nokia announces global expansion with Near Field Communication products. With the Nokia NFC (Near Field Communication) shell on their phone, consumers worldwide will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "World"}

For "Sports":
{"rewritten": "Nokia announces partnership with sports teams for Near Field Communication products. With the Nokia NFC (Near Field Communication) shell on their phone, sports fans will be able to access team services and exchange information with a simple touch gesture.", "new_prediction": "Sports"}

For "Business":
{"rewritten": "Nokia announces new business venture with Near Field Communication products. With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: No
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nokia", "NFC", "products", "consumers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nokia`(1), `nfc`(2), `product`(3), `consumer`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.7143 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.2222 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2857 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1382 |

### ag_news_test_004983 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.5000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Nokia", 8], ["announces", 6], ["Near", 10], ["Field", 10], ["Communication", 10], ["products", 7], ["With", 3], ["the", 1], ["Nokia", 8], ["NFC", 10], ["(", 2], ["Near", 10], ["Field", 10], ["Communication", 10], [")", 2], ["shell", 6], ["on", 2], ["their", 1], ["phone", 8], [",", 1], ["consumers", 5], ["will", 2], ["be", 1], ["able", 4], ["to", 1], ["access", 6], ["a", 1], ["variety", 4], ["of", 1], ["services", 7], ["and", 2], ["exchange", 6], ["information", 7], ["with", 2], ["a", 1], ["simple", 5], ["touch", 7], ["gesture", 6], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `information`, `near`, `nfc`, `nokia`, `phone`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses Nokia's announcement of Near Field Communication (NFC) technology, which is a technological innovation related to mobile devices and wireless data exchange."}
```

**Rationale text:**
> The text discusses Nokia's announcement of Near Field Communication (NFC) technology, which is a technological innovation related to mobile devices and wireless data exchange.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `exchange`, `field`, `near`, `nfc`, `nokia`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Nokia announces new business partnership to expand Near Field Communication services globally, boosting mobile commerce and payment solutions.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["NFC", "Nokia", "Communication", "products", "gesture"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `nokia`(2), `communication`(3), `product`(4), `gesture`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8333 | 0.6250 |
| H–CF | — | — |
| H–RO | 0.6000 | 0.3333 |
| R–CF | — | — |
| R–RO | 0.6000 | 0.3750 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1551 |

### ag_news_test_004983 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.4365
- **ECS (extraction–rationale):** 0.4365
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Nokia", 8], ["announces", 7], ["Near", 10], ["Field", 10], ["Communication", 10], ["products", 8], ["With", 2], ["the", 1], ["Nokia", 8], ["NFC", 10], ["(", 1], ["Near", 10], ["Field", 10], ["Communication", 10], [")", 1], ["shell", 6], ["on", 2], ["their", 1], ["phone", 7], [",", 1], ["consumers", 3], ["will", 2], ["be", 2], ["able", 2], ["to", 2], ["access", 4], ["a", 1], ["variety", 2], ["of", 1], ["services", 4], ["and", 2], ["exchange", 5], ["information", 5], ["with", 2], ["a", 1], ["simple", 3], ["touch", 4], ["gesture", 4], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `announce`, `communication`, `field`, `near`, `nfc`, `nokia`, `product`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text describes a new technological product (NFC shell) from a company (Nokia) that enables advanced communication and services, which falls under science and technology."}
```

**Rationale text:**
> The text describes a new technological product (NFC shell) from a company (Nokia) that enables advanced communication and services, which falls under science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `nfc`, `nokia`, `product`, `service`, `shell`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Nokia announces Near Field Communication products. With the Nokia NFC (Near Field Communication) shell on their phone, the company projects a significant increase in quarterly revenue.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["NFC", "Communication", "products", "phone"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `communication`(2), `product`(3), `phone`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.4444 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.3750 |
| R–CF | — | — |
| R–RO | 0.7500 | 0.4286 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1870 |


## High-ECS Examples

### sst2_validation_000665 (ECS=0.5750)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `negative` ✗

### ag_news_test_004983 (ECS=0.5000)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### ag_news_test_004983 (ECS=0.5000)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓


## Low-ECS Examples

### sst2_validation_000665 (ECS=0.2000)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_000665 (ECS=0.2533)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_007919 (ECS=0.2667)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗
