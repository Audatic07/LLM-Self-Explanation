# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-03 12:48:55
- **Duration:** 754.8s (12.6m)
- **Models (3):** nova-pro (`eu.amazon.nova-pro-v1:0`), qwen3-235b (`qwen.qwen3-235b-a22b-2507-v1:0`), deepseek-v3 (`deepseek.v3-v1:0`)
- **Total instances:** 90
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 182868
- **Avg tokens per instance:** 2032

## Per-Dataset Summary

| Model | Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|-------|---------|-----------|----------|----------|---|---|------|---|
| nova-pro | sst2 | 10 | 10/10 (100%) | 0.409 | 100% | 90% | 0% | 100% |
| qwen3-235b | sst2 | 10 | 10/10 (100%) | 0.436 | 100% | 90% | 30% | 100% |
| deepseek-v3 | sst2 | 10 | 10/10 (100%) | 0.401 | 100% | 90% | 90% | 90% |
| nova-pro | mnli | 10 | 7/10 (70%) | 0.419 | 100% | 100% | 20% | 90% |
| qwen3-235b | mnli | 10 | 6/10 (60%) | 0.545 | 90% | 100% | 10% | 100% |
| deepseek-v3 | mnli | 10 | 5/10 (50%) | 0.368 | 100% | 100% | 40% | 90% |
| nova-pro | ag_news | 10 | 8/10 (80%) | 0.434 | 100% | 100% | 10% | 100% |
| qwen3-235b | ag_news | 10 | 8/10 (80%) | 0.404 | 100% | 100% | 10% | 100% |
| deepseek-v3 | ag_news | 10 | 8/10 (80%) | 0.364 | 100% | 100% | 40% | 100% |

## Sampling Log

| Model | Dataset | Requested | Sampled | Wrong Pred |
|-------|---------|-----------|---------|------------|
| nova-pro | sst2 | 10 | 10 | 0 |
| qwen3-235b | sst2 | 10 | 10 | 0 |
| deepseek-v3 | sst2 | 10 | 10 | 0 |
| nova-pro | mnli | 10 | 10 | 3 |
| qwen3-235b | mnli | 10 | 10 | 4 |
| deepseek-v3 | mnli | 10 | 10 | 5 |
| nova-pro | ag_news | 10 | 10 | 2 |
| qwen3-235b | ag_news | 10 | 10 | 2 |
| deepseek-v3 | ag_news | 10 | 10 | 2 |
| **Total** | | 90 | 90 | 18 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=22) or medium-length (21–50 words, N=61). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=28). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=22)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 89/90 | 99% |
| Rationale | 87/90 | 97% |
| Counterfactual | 25/90 | 28% |
| Rank Ordering | 87/90 | 97% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

> **Pooled across models and datasets — descriptive context only.** The primary reporting unit is the model×dataset cell (tables below): pooled numbers mix heterogeneous tasks and models, and their bootstrap CI resamples instance clusters (the same instance appears under every model). At scale, **complete-case ECS is the primary estimand** — partial-case ECS averages whichever pairs survived, which changes the construct per instance.

| Metric | Value |
|--------|-------|
| **Mean ECS (complete cases, N=22) — primary estimand** | 0.3509 |
| Complete cases | 22/90 (24%) |
| Mean ECS (all with ≥3 valid, N=90) | 0.4185 |
| Mean ECS-overlap (size-robust secondary, same pairs) | 0.7384 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.4317 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.3571 |
| Std ECS | 0.1985 |
| Median ECS | 0.3945 |
| **Mean ECS lift over chance** (ECS − uniform random) | +0.3066 |
| Mean ECS random baseline (uniform) | 0.1119 |
| Mean ECS lift over salience-weighted null (secondary, N=86) | +0.1841 |

> **Significance testing: pre-registered tests only.** Exactly two test families run (FIX_PLAN §P1.3): (a) sign-flip permutation on per-instance ECS-lift per model×dataset cell, Holm-corrected across cells — results in the table below; (b) CC-erasure vs random control in the separate erasure pass. Every other number in this report — strata, splits, contrasts — is descriptive, and cells below the configured minimum N report estimates without a test.

| Introduced-concept rate (R) | 0.642 |
| CF canonical (minimal) validity rate | 28% |
| CF canonical validity — first attempt (single-shot, uncoached) | 26% |
| CF valid only after correction loop (coached stratum) | 2 instances |
| RO required hallucination self-correction | 13 instances |
| CF contrast (free) validity rate | 82% |
| CF canonical (minimal) minimality (edits/len) | 0.095 |
| CF contrast (free) minimality (edits/len) | 0.346 |
| Verbalized confidence — mean (N=86) | 0.940 |
| Mean CC3 size | 2.07 |
| Mean CC4 size | 1.77 |
| % instances with CC3 | 87.8% |
| % instances with CC4 | 77.8% |

> The CF minimal-vs-free validity contrast replicates the validity–minimality trade-off of arXiv:2509.09396 (*LLMs Don't Know Their Own Decision Boundaries*): unconstrained rewrites flip reliably but over-edit; minimal edits often fail to flip. Single-shot rates are reported separately from the coached loop because the correction re-prompt makes headline rates multi-shot-search rates (not comparable to single-shot elicitation in Madsen et al. 2024 / MiCE).

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pre-registered test (a): mean ECS-lift > 0, per model×dataset cell

One-sided sign-flip permutation on per-instance (ECS − ECS_random) differences; Holm-corrected across this run's cells. `—` = cell below the configured minimum N for testing (estimate reported, test skipped).

| Model | Dataset | N (lift) | Mean lift | p (raw) | p (Holm) |
|-------|---------|----------|-----------|---------|----------|
| nova-pro | sst2 | 9 | +0.2598 | 0.0083 | 0.0108 |
| qwen3-235b | sst2 | 9 | +0.3132 | 0.0036 | 0.0108 |
| deepseek-v3 | sst2 | 10 | +0.2877 | 0.0013 | 0.0108 |
| nova-pro | mnli | 9 | +0.3139 | 0.0012 | 0.0108 |
| qwen3-235b | mnli | 9 | +0.4083 | 0.0012 | 0.0108 |
| deepseek-v3 | mnli | 10 | +0.2580 | 0.0013 | 0.0108 |
| nova-pro | ag_news | 10 | +0.3343 | 0.0013 | 0.0108 |
| qwen3-235b | ag_news | 10 | +0.3076 | 0.0013 | 0.0108 |
| deepseek-v3 | ag_news | 10 | +0.2837 | 0.0021 | 0.0108 |

### ECS by prediction correctness (per cell only)

Reported per model×dataset cell only — pooled, this contrast is confounded by cell composition. Descriptive; no test.

| Model | Dataset | Mean ECS correct (N) | Mean ECS incorrect (N) |
|-------|---------|----------------------|------------------------|
| nova-pro | sst2 | 0.4091 (9) | 0.0000 (0) |
| qwen3-235b | sst2 | 0.4362 (9) | 0.0000 (0) |
| deepseek-v3 | sst2 | 0.4012 (10) | 0.0000 (0) |
| nova-pro | mnli | 0.4525 (6) | 0.3509 (3) |
| qwen3-235b | mnli | 0.5150 (6) | 0.6038 (3) |
| deepseek-v3 | mnli | 0.4674 (5) | 0.2689 (5) |
| nova-pro | ag_news | 0.4266 (8) | 0.4654 (2) |
| qwen3-235b | ag_news | 0.4250 (8) | 0.3192 (2) |
| deepseek-v3 | ag_news | 0.3620 (8) | 0.3736 (2) |

### Verbalized confidence ↔ ECS (Spearman, per cell)

Association estimate with a seeded bootstrap CI (pre-registered as an estimate, not a hypothesis test). Confidence is the model's verbalized 0–100 probability that its classification is correct (Tian et al. 2023; Xiong et al. 2024).

| Model | Dataset | N pairs | Spearman ρ | 95% CI |
|-------|---------|---------|------------|--------|
| nova-pro | sst2 | 9 | 0.091 | [-0.558, 0.734] |
| qwen3-235b | sst2 | 9 | 0.585 | [-0.185, 0.964] |
| deepseek-v3 | sst2 | 10 | 0.604 | [0.140, 0.862] |
| nova-pro | mnli | 9 | 0.275 | [-0.732, 0.843] |
| qwen3-235b | mnli | 9 | 0.375 | [-0.485, 0.931] |
| deepseek-v3 | mnli | 10 | 0.413 | [-0.257, 0.866] |
| nova-pro | ag_news | 10 | 0.418 | [-0.177, 0.881] |
| qwen3-235b | ag_news | 10 | 0.453 | [-0.275, 0.887] |
| deepseek-v3 | ag_news | 10 | 0.201 | [-0.716, 0.869] |

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) | N instances |
|------|----------------------|----------------|-------------|
| H–R | 0.7333 | 0.4191 | 86 |
| H–CF | 0.9067 | 0.3416 | 25 |
| H–RO | 0.8312 | 0.5592 | 86 |
| R–CF | 0.6667 | 0.2800 | 24 |
| R–RO | 0.6942 | 0.4387 | 84 |
| CF–RO | 0.8043 | 0.3855 | 23 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.2604 |
| Kendall τ (H,RO) | 0.3622 |
| Normalized τ | 0.6811 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — and its cross-paradigm mean is the `ECS-overlap` secondary composite. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking (both rankings live in the same normalized token space); Kendall τ provides a complementary rank correlation measure.

## Cross-Model Agreement (same strategy, different models)

For every instance run under ≥2 models: the Jaccard between DIFFERENT models' evidence sets for the SAME strategy, next to the within-model cross-strategy ECS of the same instances. If within-model consensus systematically exceeds cross-model same-strategy agreement, stated evidence tracks model-specific computation (privileged self-knowledge, arXiv:2602.02639); if not, it is closer to a generic task prior shared across models (cf. the cross-model explanation lottery, arXiv:2603.15821). Zero extra API calls; descriptive.

| Dataset | N instances | H | R | CF | RO | Cross-model mean | Within-model mean ECS |
|---------|-------------|---|---|----|----|------------------|------------------------|
| ag_news | 10 | 0.616 (30) | 0.505 (30) | 0.500 (2) | 0.553 (30) | 0.557 | 0.401 |
| mnli | 10 | 0.720 (28) | 0.679 (30) | 0.667 (3) | 0.551 (26) | 0.654 | 0.441 |
| sst2 | 10 | 0.677 (30) | 0.626 (25) | 0.667 (3) | 0.663 (28) | 0.657 | 0.415 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 89/90 (99%) | 89/90 (99%) |
| Rationale | 87/90 (97%) | 87/90 (97%) |
| Counterfactual (JSON parsed) | 89/90 (99%) |
| Counterfactual (rules compliant) | 41/90 (46%) |
| Counterfactual (flip verified) | 25/41 (61%) |
| Rank Ordering | 87/90 (97%) | 87/90 (97%) |
| All 4 valid | 22/90 |
| 3 valid (CC3 adjusted) | 64/90 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 22 | 0.3906 |
| Medium (21–50) | 61 | 0.4262 |
| Long (>50 words) | 3 | 0.4690 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 58 | 0.4250 |
| Short vocab (≤20 unique tokens) | 28 | 0.4052 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.4185 | [0.3596, 0.4745] |

## Per-Instance Details

### sst2_validation_000665 — nova-pro

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
  "label": "positive"
}

Explanation: The text implies that the scenes are very emotionally impactful, suggesting a positive evaluation of the emotional depth and effectiveness of those scenes. The phrase "moved to tears" indicates a strong, positive emotional response, even though it's phrased in a slightly backhanded manner by suggesting that not being moved would indicate a lack of emotion ("ice water in your veins").
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 426 chars
- **Prompt hash:** `3c96c3fc1045fafc`
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
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["and", 1],
    ["if", 3],
    ["you", 6],
    ["'re", 4],
    ["not", 7],
    ["nearly", 8],
    ["moved", 9],
    ["to", 5],
    ["tears", 10],
    ["by", 5],
    ["a", 2],
    ["couple", 6],
    ["of", 3],
    ["scenes", 8],
    [",", 1],
    ["you", 6],
    ["'ve", 4],
    ["got", 5],
    ["ice", 7],
    ["water", 7],
    ["in", 4],
    ["your", 6],
    ["veins", 8],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `nearly`, `scene`, `tear`

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
{
  "rationale": "The text suggests that the scenes are profoundly moving, which is a positive evaluation of their emotional impact."
}
```

**Rationale text:**
> The text suggests that the scenes are profoundly moving, which is a positive evaluation of their emotional impact.

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
{
  "rewritten": "and if you're not nearly bored by a couple of scenes, you've got a high tolerance for dullness.",
  "new_prediction": "negative"
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
The text was classified as: positive

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
    "scenes",
    "couple",
    "ice"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tear`(1), `move`(2), `scene`(3), `couple`(4), `ice`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.5000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.6000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3380 |

### sst2_validation_000657 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

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
- **Input length:** 13 words
- **Raw response length:** 25 chars
- **Prompt hash:** `b68aba988a2aa373`
- **ECS (full):** 0.6000
- **ECS (extraction–rationale):** 0.6000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["expect", 5],
    ["the", 3],
    ["same-old", 9],
    [",", 1],
    ["lame-old", 9],
    ["slasher", 8],
    ["nonsense", 8],
    [",", 1],
    ["just", 4],
    ["with", 3],
    ["different", 6],
    ["scenery", 6],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`, `nonsense`, `same-old`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text uses derogatory terms like'same-old', 'lame-old', and 'nonsense', indicating a negative sentiment towards the subject."
}
```

**Rationale text:**
> The text uses derogatory terms like'same-old', 'lame-old', and 'nonsense', indicating a negative sentiment towards the subject.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame`, `lame-old`, `nonsense`, `old`, `same-old`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "enjoy fresh, exciting slasher thrills, just with new scenery.",
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

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["lame-old", "nonsense", "same-old", "slasher", "expect"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`(1), `nonsense`(2), `same-old`(3), `slasher`(4), `expect`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6000 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3200 |

### sst2_validation_000361 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Return only valid JSON:
{"label":"positive or negative"}
```

#### 2. Classification Response
```
```json
{
  "label": "negative"
}
```
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 21 words
- **Raw response length:** 37 chars
- **Prompt hash:** `53ae850b6f80a8dd`
- **ECS (full):** 0.3542
- **ECS (extraction–rationale):** 0.3542
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
  "salience": [
    ["a", 1],
    ["very", 8],
    ["long", 9],
    ["movie", 7],
    [",", 1],
    ["dull", 9],
    ["in", 3],
    ["stretches", 8],
    [",", 1],
    ["with", 4],
    ["entirely", 7],
    ["too", 8],
    ["much", 8],
    ["focus", 9],
    ["on", 5],
    ["meal", 6],
    ["preparation", 7],
    ["and", 2],
    ["igloo", 6],
    ["construction", 7],
    [".", 1]
  ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `focus`, `long`, `much`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
```json
{
  "rationale": "The text describes the movie as 'very long', 'dull in stretches', and criticizes its focus on'meal preparation and igloo construction', indicating dissatisfaction."
}
```
```

**Rationale text:**
> The text describes the movie as 'very long', 'dull in stretches', and criticizes its focus on'meal preparation and igloo construction', indicating dissatisfaction.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `construction`, `dull`, `focus`, `igloo`, `long`, `movie`, `preparation`, `stretch`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
```json
{
  "rewritten": "a very engaging movie, captivating in parts, with just enough focus on meal preparation and igloo construction.",
  "new_prediction": "positive"
}
```
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

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
```json
{
  "ranking": ["dull", "stretches", "long", "too"]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`(1), `stretch`(2), `long`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.3333 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.4000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.3750 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2354 |

### sst2_validation_000394 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

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
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 41 words
- **Raw response length:** 25 chars
- **Prompt hash:** `67a8763d00facc6b`
- **ECS (full):** 0.4762
- **ECS (extraction–rationale):** 0.4762
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["whether", 3],
    ["writer-director", 6],
    ["anne", 7],
    ["fontaine", 7],
    ["'s", 5],
    ["film", 8],
    ["is", 5],
    ["a", 4],
    ["ghost", 7],
    ["story", 7],
    [",", 2],
    ["an", 4],
    ["account", 7],
    ["of", 5],
    ["a", 4],
    ["nervous", 7],
    ["breakdown", 7],
    [",", 2],
    ["a", 4],
    ["trip", 7],
    ["down", 6],
    ["memory", 7],
    ["lane", 6],
    [",", 2],
    ["all", 6],
    ["three", 6],
    ["or", 5],
    ["none", 6],
    ["of", 5],
    ["the", 5],
    ["above", 6],
    [",", 2],
    ["it", 5],
    ["is", 5],
    ["as", 6],
    ["seductive", 9],
    ["as", 6],
    ["it", 5],
    ["is", 5],
    ["haunting", 9],
    [".", 2]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `account`, `anne`, `breakdown`, `film`, `fontaine`, `haunt`, `seductive`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text uses positive adjectives such as'seductive' and 'haunting' to describe the film, indicating a favorable impression."
}
```

**Rationale text:**
> The text uses positive adjectives such as'seductive' and 'haunting' to describe the film, indicating a favorable impression.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `haunt`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "whether writer-director anne fontaine's film is a ghost story, an account of a nervous breakdown, a trip down memory lane, all three or none of the above, it is as unappealing as it is dull.",
  "new_prediction": "negative"
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
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "seductive",
    "haunting",
    "film"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `seductive`(1), `haunt`(2), `film`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2857 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.4286 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3173 |

### sst2_validation_000228 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

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
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 25 chars
- **Prompt hash:** `121db9f475afa812`
- **ECS (full):** 0.2500
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["it", 3],
    ["provides", 9],
    ["an", 4],
    ["honest", 8],
    ["look", 7],
    ["at", 4],
    ["a", 3],
    ["community", 8],
    ["striving", 8],
    ["to", 4],
    ["anchor", 7],
    ["itself", 6],
    ["in", 4],
    ["new", 6],
    ["grounds", 7],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `community`, `honest`, `provide`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text was classified as positive because it describes the community in a constructive and supportive manner, highlighting their efforts to establish themselves in a new environment."
}
```

**Rationale text:**
> The text was classified as positive because it describes the community in a constructive and supportive manner, highlighting their efforts to establish themselves in a new environment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `community`, `new`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "it offers a bleak view of a community failing to establish itself in unfamiliar territory.",
  "new_prediction": "negative"
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
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["honest", "look", "community", "striving"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `honest`(1), `look`(2), `community`(3), `strive`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.2500 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0904 |

### sst2_validation_000188 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

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
- **Input length:** 18 words
- **Raw response length:** 25 chars
- **Prompt hash:** `6c16dd54d427ba05`
- **ECS (full):** 0.6667
- **ECS (extraction–rationale):** 0.6667
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["a", 2],
    ["misogynistic", 10],
    ["piece", 7],
    ["of", 3],
    ["filth", 9],
    ["that", 5],
    ["attempts", 8],
    ["to", 3],
    ["pass", 7],
    ["itself", 6],
    ["off", 5],
    ["as", 4],
    ["hip", 6],
    [",", 1],
    ["young", 6],
    ["adult", 6],
    ["entertainment", 8],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `attempt`, `filth`, `misogynistic`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text uses strongly derogatory language such as 'misogynistic' and 'filth', indicating a negative sentiment."
}
```

**Rationale text:**
> The text uses strongly derogatory language such as 'misogynistic' and 'filth', indicating a negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `misogynistic`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "a progressive and refreshing take that successfully presents itself as hip, young adult entertainment.",
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

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "misogynistic",
    "filth",
    "attempts",
    "off"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `misogynistic`(1), `filth`(2), `attempt`(3), `piece`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3257 |

### sst2_validation_000513 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

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
- **Verbalized confidence:** 0.80
- **Model refused:** No
- **Input length:** 31 words
- **Raw response length:** 25 chars
- **Prompt hash:** `66ffc0207e802d03`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["care", 7],
    ["deftly", 6],
    ["captures", 8],
    ["the", 3],
    ["wonder", 7],
    ["and", 3],
    ["menace", 7],
    ["of", 3],
    ["growing", 7],
    ["up", 5],
    [",", 1],
    ["but", 8],
    ["he", 5],
    ["never", 9],
    ["really", 7],
    ["embraces", 9],
    ["the", 3],
    ["joy", 7],
    ["of", 3],
    ["fuhrman", 6],
    ["'s", 3],
    ["destructive", 8],
    ["escapism", 8],
    ["or", 5],
    ["the", 3],
    ["grace-in-rebellion", 9],
    ["found", 7],
    ["by", 4],
    ["his", 5],
    ["characters", 7],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`, `destructive`, `embrace`, `escapism`, `grace-in-rebellion`, `never`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text was classified as negative because it highlights a shortcoming or limitation in the subject's approach, indicating a lack of full embracement of certain positive aspects."
}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "care deftly captures the wonder and charm of growing up, and he beautifully embraces the joy of fuhrman's adventurous spirit and the grace-in-rebellion found by his characters.",
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

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "never",
    "really",
    "embraces",
    "joy",
    "destructive"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `never`(1), `really`(2), `embrace`(3), `joy`(4), `destructive`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | 0.6000 | 0.3750 |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1593 |

### sst2_validation_000010 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

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
- **Input length:** 16 words
- **Raw response length:** 25 chars
- **Prompt hash:** `d9ae1018167dba5e`
- **ECS (full):** 0.1000
- **ECS (extraction–rationale):** 0.1000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["the", 3],
    ["mesmerizing", 9],
    ["performances", 8],
    ["of", 2],
    ["the", 3],
    ["leads", 7],
    ["keep", 6],
    ["the", 3],
    ["film", 5],
    ["grounded", 7],
    ["and", 2],
    ["keep", 6],
    ["the", 3],
    ["audience", 6],
    ["riveted", 8],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`, `performance`, `rivet`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text uses positive words like'mesmerizing', 'grounded', and 'riveted', indicating a favorable opinion of the film."
}
```

**Rationale text:**
> The text uses positive words like'mesmerizing', 'grounded', and 'riveted', indicating a favorable opinion of the film.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `grind`, `rivet`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "the uninspiring performances of the leads fail to ground the film and leave the audience bored.",
  "new_prediction": "negative"
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
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "mesmerizing",
    "performances",
    "keep",
    "riveted",
    "audience"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`(1), `performance`(2), `keep`(3), `rivet`(4), `audience`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.2000 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3380 |

### sst2_validation_000529 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

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
- **Input length:** 27 words
- **Raw response length:** 25 chars
- **Prompt hash:** `b04c96a0a49e1956`
- **ECS (full):** 0.5347
- **ECS (extraction–rationale):** 0.5347
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["for", 3],
    ["close", 5],
    ["to", 3],
    ["two", 5],
    ["hours", 6],
    ["the", 3],
    ["audience", 7],
    ["is", 3],
    ["forced", 8],
    ["to", 3],
    ["endure", 9],
    ["three", 6],
    ["terminally", 8],
    ["depressed", 9],
    [",", 1],
    ["mostly", 7],
    ["inarticulate", 8],
    [",", 1],
    ["hyper", 7],
    ["dysfunctional", 9],
    ["families", 8],
    ["for", 3],
    ["the", 3],
    ["price", 6],
    ["of", 3],
    ["one", 5],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`, `dysfunctional`, `endure`, `family`, `force`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text uses strongly negative words like 'forced to endure', 'terminally depressed', 'mostly inarticulate', and 'hyper dysfunctional', indicating a highly unfavorable view."
}
```

**Rationale text:**
> The text uses strongly negative words like 'forced to endure', 'terminally depressed', 'mostly inarticulate', and 'hyper dysfunctional', indicating a highly unfavorable view.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`, `dysfunctional`, `endure`, `force`, `hyper`, `inarticulate`, `mostly`, `terminally`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "for close to two hours the audience is delighted to enjoy three wonderfully vibrant, articulate, and functional families for the price of one.",
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

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "depressed",
    "dysfunctional",
    "inarticulate",
    "forced",
    "endure"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`(1), `dysfunctional`(2), `inarticulate`(3), `force`(4), `endure`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.4444 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.6667 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6250 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3329 |

### sst2_validation_000007 — nova-pro

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "or doing last year 's taxes with your ex-wife . "

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
- **Input length:** 10 words
- **Raw response length:** 25 chars
- **Prompt hash:** `bed5ce4a26311b72`
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
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["or", 3],
    ["doing", 8],
    ["last", 6],
    ["year", 5],
    ["'s", 4],
    ["taxes", 7],
    ["with", 5],
    ["your", 6],
    ["ex-wife", 10],
    [". ", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex-wife`, `last`, `tax`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text implies a stressful or unpleasant situation involving an ex-wife."
}
```

**Rationale text:**
> The text implies a stressful or unpleasant situation involving an ex-wife.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex`, `ex-wife`, `wife`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{
  "rewritten": "enjoying last year's tax refund with your best friend.",
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

Text: "or doing last year 's taxes with your ex-wife . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["ex-wife", "taxes", "doing", "last"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tax`(1), `ex-wife`(2), `last`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.2000 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 0.3333 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1710 |

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
- **ECS (full):** 0.3500
- **ECS (extraction–rationale):** 0.3500
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
{"salience": [["and", 2], ["if", 5], ["you", 6], ["'", 1], ["re", 4], ["not", 8], ["nearly", 7], ["moved", 9], ["to", 3], ["tears", 10], ["by", 2], ["a", 1], ["couple", 4], ["of", 2], ["scenes", 6], [",", 1], ["you", 6], ["'", 1], ["ve", 4], ["got", 5], ["ice", 8], ["water", 7], ["in", 3], ["your", 5], ["veins", 9]]}
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
{"ranking": ["tears", "moved", "scenes", "ice", "veins"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tear`(1), `move`(2), `scene`(3), `ice`(4), `vein`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.2000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.6000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3512 |

### sst2_validation_000657 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

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
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 13 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b68aba988a2aa373`
- **ECS (full):** 0.6000
- **ECS (extraction–rationale):** 0.6000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["expect", 3], ["the", 1], ["same-old", 8], [",", 1], ["lame-old", 9], ["slasher", 6], ["nonsense", 9], [",", 1], ["just", 3], ["with", 2], ["different", 4], ["scenery", 5], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`, `nonsense`, `same-old`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses disappointment and criticism by describing the content as unoriginal and dull, using negative terms like 'same-old,' 'lame-old,' and 'nonsense.'"}
```

**Rationale text:**
> The text expresses disappointment and criticism by describing the content as unoriginal and dull, using negative terms like 'same-old,' 'lame-old,' and 'nonsense.'

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame`, `lame-old`, `nonsense`, `old`, `same-old`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "expect the same-old, fun slasher excitement, just with fresh scenery.", "new_prediction": "positive"}
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

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["lame-old", "nonsense", "same-old", "slasher"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`(1), `nonsense`(2), `same-old`(3), `slasher`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6000 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3257 |

### sst2_validation_000361 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

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
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 21 words
- **Raw response length:** 20 chars
- **Prompt hash:** `53ae850b6f80a8dd`
- **ECS (full):** 0.1250
- **ECS (extraction–rationale):** 0.1250
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["a", 2], ["very", 6], ["long", 5], ["movie", 3], [",", 1], ["dull", 10], ["in", 2], ["stretches", 7], [",", 1], ["with", 2], ["entirely", 5], ["too", 6], ["much", 5], ["focus", 4], ["on", 2], ["meal", 3], ["preparation", 3], ["and", 2], ["igloo", 4], ["construction", 4], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `entirely`, `long`, `stretch`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text expresses criticism of the movie's length, pacing, and excessive focus on mundane activities, indicating a negative sentiment."}
```

**Rationale text:**
> The text expresses criticism of the movie's length, pacing, and excessive focus on mundane activities, indicating a negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `focus`, `movie`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "a beautifully crafted movie , engaging in parts , with delightful focus on meal preparation and igloo construction . ", "new_prediction": "positive"}
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

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["dull", "long", "too", "focus"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`(1), `long`(2), `focus`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.4000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2084 |

### sst2_validation_000394 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

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
- **Input length:** 41 words
- **Raw response length:** 20 chars
- **Prompt hash:** `67a8763d00facc6b`
- **ECS (full):** 0.6095
- **ECS (extraction–rationale):** 0.7143
- **ECS (extraction–perturbation):** 0.4762
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["whether", 3], ["writer-director", 5], ["anne", 6], ["fontaine", 7], ["'s", 4], ["film", 8], ["is", 5], ["a", 2], ["ghost", 6], ["story", 6], [",", 2], ["an", 2], ["account", 5], ["of", 3], ["a", 2], ["nervous", 7], ["breakdown", 7], [",", 2], ["a", 2], ["trip", 5], ["down", 4], ["memory", 6], ["lane", 6], [",", 2], ["all", 3], ["three", 3], ["or", 3], ["none", 4], ["of", 3], ["the", 2], ["above", 4], [",", 2], ["it", 5], ["is", 5], ["as", 6], ["seductive", 10], ["as", 6], ["it", 5], ["is", 5], ["haunting", 9], ["." , 2]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `anne`, `breakdown`, `film`, `fontaine`, `haunt`, `nervous`, `seductive`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as positive because it uses complimentary language such as 'seductive' and 'haunting' to convey an alluring and impactful impression of the film."}
```

**Rationale text:**
> The text was classified as positive because it uses complimentary language such as 'seductive' and 'haunting' to convey an alluring and impactful impression of the film.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `haunt`, `seductive`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as dull as it is confusing . ", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as dull as it is confusing . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `haunt`, `seductive`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["seductive", "haunting", "film"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `seductive`(1), `haunt`(2), `film`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.4286 |
| H–CF | 1.0000 | 0.2857 |
| H–RO | 1.0000 | 0.4286 |
| R–CF | 1.0000 | 0.6667 |
| R–RO | 1.0000 | 1.0000 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.4173 |

### sst2_validation_000228 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

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
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `121db9f475afa812`
- **ECS (full):** 0.2667
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["it", 3], ["provides", 6], ["an", 2], ["honest", 9], ["look", 5], ["at", 2], ["a", 2], ["community", 7], ["striving", 8], ["to", 2], ["anchor", 7], ["itself", 4], ["in", 3], ["new", 6], ["grounds", 5], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `anchor`, `honest`, `strive`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text conveys a respectful and hopeful portrayal of a community's effort to establish itself in a new environment, emphasizing honesty and resilience."}
```

**Rationale text:**
> The text conveys a respectful and hopeful portrayal of a community's effort to establish itself in a new environment, emphasizing honesty and resilience.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `community`, `new`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "it provides a bleak look at a community struggling to anchor itself in new grounds .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> it provides a bleak look at a community struggling to anchor itself in new grounds .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `honest`, `strive`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["honest", "striving", "anchor", "community"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `honest`(1), `strive`(2), `anchor`(3), `community`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3257 |

### sst2_validation_000188 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

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
- **Input length:** 18 words
- **Raw response length:** 20 chars
- **Prompt hash:** `6c16dd54d427ba05`
- **ECS (full):** 0.6667
- **ECS (extraction–rationale):** 0.6667
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["a", 3], ["misogynistic", 10], ["piece", 5], ["of", 2], ["filth", 9], ["that", 3], ["attempts", 6], ["to", 2], ["pass", 5], ["itself", 4], ["off", 4], ["as", 3], ["hip", 4], [",", 1], ["young", 5], ["adult", 4], ["entertainment", 3], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `attempt`, `filth`, `misogynistic`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses strongly derogatory language such as 'misogynistic' and 'filth' to criticize the content, indicating a clear negative sentiment."}
```

**Rationale text:**
> The text uses strongly derogatory language such as 'misogynistic' and 'filth' to criticize the content, indicating a clear negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `misogynistic`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "a progressive piece of art that attempts to pass itself off as hip, young adult entertainment.", "new_prediction": "positive"}
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

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["misogynistic", "filth", "attempts", "hip", "entertainment"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `misogynistic`(1), `filth`(2), `attempt`(3), `hip`(4), `entertainment`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3650 |

### sst2_validation_000513 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

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
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 31 words
- **Raw response length:** 20 chars
- **Prompt hash:** `66ffc0207e802d03`
- **ECS (full):** 0.0625
- **ECS (extraction–rationale):** 0.0625
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["care", 5], ["deftly", 6], ["captures", 7], ["the", 3], ["wonder", 6], ["and", 4], ["menace", 8], ["of", 2], ["growing", 5], ["up", 5], [",", 1], ["but", 9], ["he", 3], ["never", 9], ["really", 7], ["embraces", 8], ["the", 3], ["joy", 7], ["of", 2], ["fuhrman", 5], ["'", 1], ["s", 1], ["destructive", 8], ["escapism", 7], ["or", 5], ["the", 3], ["grace-in-rebellion", 6], ["found", 5], ["by", 3], ["his", 3], ["characters", 5], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`, `destructive`, `embrace`, `escapism`, `menace`, `never`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is classified as negative because it critiques the author for failing to fully embrace the positive aspects of the characters' rebellious experiences, despite acknowledging some strengths in the portrayal of growing up."}
```

**Rationale text:**
> The text is classified as negative because it critiques the author for failing to fully embrace the positive aspects of the characters' rebellious experiences, despite acknowledging some strengths in the portrayal of growing up.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `character`, `embrace`, `grow`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "care deftly captures the wonder and menace of growing up, and he fully embraces the joy of fuhrman's destructive escapism and the grace-in-rebellion found by his characters.", "new_prediction": "positive"}
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

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["never", "destructive", "menace"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `never`(1), `destructive`(2), `menace`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.1250 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3676 |

### sst2_validation_000010 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

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
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d9ae1018167dba5e`
- **ECS (full):** 0.4952
- **ECS (extraction–rationale):** 0.4286
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["the", 3], ["mesmerizing", 10], ["performances", 8], ["of", 2], ["the", 3], ["leads", 6], ["keep", 5], ["the", 3], ["film", 4], ["grounded", 7], ["and", 2], ["keep", 5], ["the", 3], ["audience", 6], ["riveted", 9], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`, `performance`, `rivet`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses positive language such as 'mesmerizing performances' and 'keep the audience riveted' to convey strong approval and admiration for the film's lead actors."}
```

**Rationale text:**
> The text uses positive language such as 'mesmerizing performances' and 'keep the audience riveted' to convey strong approval and admiration for the film's lead actors.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `audience`, `film`, `keep`, `lead`, `mesmerize`, `performance`, `rivet`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "the weak performances of the leads keep the film grounded and keep the audience bored.", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> the weak performances of the leads keep the film grounded and keep the audience bored.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`, `rivet`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["mesmerizing", "performances", "riveted", "grounded"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`(1), `performance`(2), `rivet`(3), `grind`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.4286 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 1.0000 | 0.2857 |
| R–RO | 1.0000 | 0.4286 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2807 |

### sst2_validation_000529 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

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
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 27 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b04c96a0a49e1956`
- **ECS (full):** 0.7500
- **ECS (extraction–rationale):** 0.7500
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["for", 2], ["close", 3], ["to", 2], ["two", 3], ["hours", 4], ["the", 1], ["audience", 5], ["is", 1], ["forced", 9], ["to", 2], ["endure", 10], ["three", 3], ["terminally", 9], ["depressed", 9], [",", 1], ["mostly", 6], ["inarticulate", 8], [",", 1], ["hyper", 7], ["dysfunctional", 8], ["families", 5], ["for", 2], ["the", 1], ["price", 3], ["of", 1], ["one", 2], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`, `dysfunctional`, `endure`, `force`, `terminally`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses strongly negative language such as 'forced to endure,' 'terminally depressed,' and 'hyper dysfunctional,' conveying a harshly critical view of the experience."}
```

**Rationale text:**
> The text uses strongly negative language such as 'forced to endure,' 'terminally depressed,' and 'hyper dysfunctional,' conveying a harshly critical view of the experience.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`, `dysfunctional`, `endure`, `force`, `hyper`, `terminally`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "for close to two hours the audience is invited to embrace three deeply sensitive, quietly expressive, uniquely human families for the price of one.", "new_prediction": "positive"}
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

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["forced", "depressed", "dysfunctional", "endure"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `force`(1), `depress`(2), `dysfunctional`(3), `endure`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.8333 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.8000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | -0.3333 |
| Normalized τ | 0.3333 |
| RBO (H,RO) | 0.2062 |

### sst2_validation_000007 — qwen3-235b

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "or doing last year 's taxes with your ex-wife . "

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
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 10 words
- **Raw response length:** 20 chars
- **Prompt hash:** `bed5ce4a26311b72`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["or", 2], ["doing", 5], ["last", 6], ["year", 5], ["'s", 5], ["taxes", 8], ["with", 3], ["your", 4], ["ex-wife", 10], [".", 2]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex-wife`, `last`, `tax`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text evokes a stressful and unpleasant situation involving both bureaucratic hassle and strained personal relationships."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "or enjoying a walk with your best friend.", "new_prediction": "positive"}
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

Text: "or doing last year 's taxes with your ex-wife . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["ex-wife", "taxes", "last", "doing"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex-wife`(1), `tax`(2), `last`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2710 |

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
- **ECS (full):** 0.1700
- **ECS (extraction–rationale):** 0.1250
- **ECS (extraction–perturbation):** 0.3000
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 0

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
{"salience": [["and", 1], ["if", 1], ["you", 1], ["'re", 1], ["not", 10], ["nearly", 3], ["moved", 8], ["to", 1], ["tears", 9], ["by", 1], ["a", 1], ["couple", 1], ["of", 1], ["scenes", 7], [",", 1], ["you", 1], ["'ve", 1], ["got", 1], ["ice", 9], ["water", 9], ["in", 1], ["your", 1], ["veins", 8], [".", 1]]}
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
{"rationale": "The text expresses a positive sentiment by strongly praising the emotional power of the scenes, suggesting that being moved by them is the expected and admirable human response."}
```

**Rationale text:**
> The text expresses a positive sentiment by strongly praising the emotional power of the scenes, suggesting that being moved by them is the expected and admirable human response.

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
| H–R | 0.0000 | 0.0000 |
| H–CF | 0.6667 | 0.4000 |
| H–RO | 0.6667 | 0.4000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.5000 | 0.2500 |
| CF–RO | 0.3333 | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0904 |

### sst2_validation_000657 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

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
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 13 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b68aba988a2aa373`
- **ECS (full):** 0.5267
- **ECS (extraction–rationale):** 0.4000
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["expect", 2], ["the", 1], ["same-old", 8], [",", 1], ["lame-old", 10], ["slasher", 7], ["nonsense", 9], [",", 1], ["just", 3], ["with", 1], ["different", 2], ["scenery", 3], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`, `nonsense`, `same-old`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses negative words like 'lame-old' and 'nonsense' to express a dismissive and critical opinion of the film."}
```

**Rationale text:**
> The text uses negative words like 'lame-old' and 'nonsense' to express a dismissive and critical opinion of the film.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame`, `lame-old`, `nonsense`, `old`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "expect the same-old , great-old slasher fun , just with different scenery .", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> expect the same-old , great-old slasher fun , just with different scenery .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`, `nonsense`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["lame-old", "nonsense", "same-old"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`(1), `nonsense`(2), `same-old`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.4000 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 1.0000 | 0.5000 |
| R–RO | 0.6667 | 0.4000 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2710 |

### sst2_validation_000361 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

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
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 21 words
- **Raw response length:** 20 chars
- **Prompt hash:** `53ae850b6f80a8dd`
- **ECS (full):** 0.3667
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** 0.2000
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["a", 1], ["very", 3], ["long", 7], ["movie", 1], [",", 1], ["dull", 10], ["in", 1], ["stretches", 6], [",", 1], ["with", 1], ["entirely", 4], ["too", 5], ["much", 4], ["focus", 3], ["on", 1], ["meal", 2], ["preparation", 2], ["and", 1], ["igloo", 2], ["construction", 2], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `entirely`, `long`, `stretch`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses negative descriptors like 'very long', 'dull', and 'entirely too much' to criticize the movie's pacing and boring content."}
```

**Rationale text:**
> The text uses negative descriptors like 'very long', 'dull', and 'entirely too much' to criticize the movie's pacing and boring content.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `entirely`, `long`, `movie`, `much`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "a very long movie , engaging in stretches , with entirely wonderful focus on meal preparation and igloo construction . ", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> a very long movie , engaging in stretches , with entirely wonderful focus on meal preparation and igloo construction . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `much`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["dull", "long", "too"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.5000 |
| H–CF | 0.5000 | 0.2000 |
| H–RO | — | — |
| R–CF | 1.0000 | 0.4000 |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### sst2_validation_000394 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

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
- **Input length:** 41 words
- **Raw response length:** 20 chars
- **Prompt hash:** `67a8763d00facc6b`
- **ECS (full):** 0.3476
- **ECS (extraction–rationale):** 0.4643
- **ECS (extraction–perturbation):** 0.2381
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["whether", 1], ["writer-director", 1], ["anne", 1], ["fontaine", 1], ["'s", 1], ["film", 1], ["is", 1], ["a", 1], ["ghost", 1], ["story", 1], [",", 1], ["an", 1], ["account", 1], ["of", 1], ["a", 1], ["nervous", 1], ["breakdown", 1], [",", 1], ["a", 1], ["trip", 1], ["down", 1], ["memory", 1], ["lane", 1], [",", 1], ["all", 1], ["three", 1], ["or", 1], ["none", 1], ["of", 1], ["the", 1], ["above", 1], [",", 1], ["it", 1], ["is", 10], ["as", 8], ["seductive", 10], ["as", 8], ["it", 1], ["is", 10], ["haunting", 9], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `account`, `all`, `anne`, `breakdown`, `film`, `haunt`, `seductive`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses strongly positive descriptors like 'seductive' and 'haunting' to praise the film's captivating and memorable quality."}
```

**Rationale text:**
> The text uses strongly positive descriptors like 'seductive' and 'haunting' to praise the film's captivating and memorable quality.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `haunt`, `seductive`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as dull as it is haunting .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as dull as it is haunting .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `seductive`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["seductive", "haunting", "trip"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `seductive`(1), `haunt`(2), `trip`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.4286 |
| H–CF | 1.0000 | 0.1429 |
| H–RO | 0.6667 | 0.2500 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3416 |

### sst2_validation_000228 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

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
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `121db9f475afa812`
- **ECS (full):** 0.6000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["it", 1], ["provides", 3], ["an", 1], ["honest", 9], ["look", 2], ["at", 1], ["a", 1], ["community", 3], ["striving", 8], ["to", 1], ["anchor", 7], ["itself", 2], ["in", 1], ["new", 4], ["grounds", 5], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `anchor`, `honest`, `strive`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is positive because it uses words like 'honest' and 'striving' which have a constructive and admirable connotation, portraying the community's efforts in a favorable light."}
```

**Rationale text:**
> The text is positive because it uses words like 'honest' and 'striving' which have a constructive and admirable connotation, portraying the community's efforts in a favorable light.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `community`, `honest`, `strive`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "it provides a dishonest look at a community failing to anchor itself in new grounds .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> it provides a dishonest look at a community failing to anchor itself in new grounds .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `honest`, `strive`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["honest", "striving", "anchor"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `honest`(1), `strive`(2), `anchor`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.5000 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 1.0000 | 0.6667 |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2710 |

### sst2_validation_000188 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

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
- **Input length:** 18 words
- **Raw response length:** 20 chars
- **Prompt hash:** `6c16dd54d427ba05`
- **ECS (full):** 0.5333
- **ECS (extraction–rationale):** 0.4667
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["a", 1], ["misogynistic", 10], ["piece", 2], ["of", 1], ["filth", 10], ["that", 1], ["attempts", 3], ["to", 1], ["pass", 4], ["itself", 1], ["off", 1], ["as", 1], ["hip", 5], [",", 1], ["young", 1], ["adult", 1], ["entertainment", 3], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `hip`, `misogynistic`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses highly negative and insulting language such as 'misogynistic', 'piece of filth', and implies deception with 'attempts to pass itself off' to express strong disapproval."}
```

**Rationale text:**
> The text uses highly negative and insulting language such as 'misogynistic', 'piece of filth', and implies deception with 'attempts to pass itself off' to express strong disapproval.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `attempt`, `filth`, `misogynistic`, `pa`, `piece`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "a fantastic piece of art that attempts to pass itself off as hip , young adult entertainment .", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> a fantastic piece of art that attempts to pass itself off as hip , young adult entertainment .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `misogynistic`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["misogynistic", "filth", "attempts"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `misogynistic`(1), `filth`(2), `attempt`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.3333 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 0.6667 | 0.5000 |
| R–CF | 1.0000 | 0.4000 |
| R–RO | 1.0000 | 0.6000 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1440 |

### sst2_validation_000513 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

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
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 31 words
- **Raw response length:** 20 chars
- **Prompt hash:** `66ffc0207e802d03`
- **ECS (full):** 0.2917
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.2917
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["care", 1], ["deftly", 1], ["captures", 1], ["the", 1], ["wonder", 3], ["and", 1], ["menace", 3], ["of", 1], ["growing", 1], ["up", 1], [",", 1], ["but", 8], ["he", 1], ["never", 9], ["really", 7], ["embraces", 8], ["the", 1], ["joy", 8], ["of", 1], ["fuhrman", 1], ["'s", 1], ["destructive", 1], ["escapism", 1], ["or", 1], ["the", 1], ["grace-in-rebellion", 8], ["found", 1], ["by", 1], ["his", 1], ["characters", 1], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `embrace`, `grace-in-rebellion`, `joy`, `menace`, `never`, `really`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is negative because it uses the conjunction 'but' to contrast a positive aspect with a stronger, overriding criticism about what the subject fails to do."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "care deftly captures the wonder and menace of growing up , and he wonderfully embraces the joy of fuhrman 's destructive escapism and the grace-in-rebellion found by his characters .", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> care deftly captures the wonder and menace of growing up , and he wonderfully embraces the joy of fuhrman 's destructive escapism and the grace-in-rebellion found by his characters .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `never`, `really`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["never", "destructive", "menace", "but"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `never`(1), `destructive`(2), `menace`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | 1.0000 | 0.3333 |
| H–RO | 0.6667 | 0.2857 |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | 0.5000 | 0.2500 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2230 |

### sst2_validation_000010 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

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
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d9ae1018167dba5e`
- **ECS (full):** 0.4000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["the", 1], ["mesmerizing", 10], ["performances", 9], ["of", 1], ["the", 1], ["leads", 8], ["keep", 3], ["the", 1], ["film", 2], ["grounded", 4], ["and", 1], ["keep", 3], ["the", 1], ["audience", 3], ["riveted", 10], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`, `performance`, `rivet`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses strongly positive adjectives like 'mesmerizing' and 'riveted' to describe the acting and its effect on the audience."}
```

**Rationale text:**
> The text uses strongly positive adjectives like 'mesmerizing' and 'riveted' to describe the acting and its effect on the audience.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `audience`, `mesmerize`, `rivet`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "the mediocre performances of the leads keep the film grounded and keep the audience riveted .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> the mesmerizing performances of the leads keep the film grounded and keep the audience bored .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `rivet`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["mesmerizing", "riveted", "grounded"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mesmerize`(1), `rivet`(2), `grind`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.5000 |
| H–CF | 1.0000 | 0.3333 |
| H–RO | 0.6667 | 0.5000 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2440 |

### sst2_validation_000529 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

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
- **Input length:** 27 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b04c96a0a49e1956`
- **ECS (full):** 0.6429
- **ECS (extraction–rationale):** 0.6429
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["for", 1], ["close", 2], ["to", 1], ["two", 2], ["hours", 3], ["the", 1], ["audience", 3], ["is", 1], ["forced", 9], ["to", 1], ["endure", 10], ["three", 2], ["terminally", 8], ["depressed", 9], [",", 1], ["mostly", 4], ["inarticulate", 8], [",", 1], ["hyper", 7], ["dysfunctional", 9], ["families", 5], ["for", 1], ["the", 1], ["price", 2], ["of", 1], ["one", 2], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`, `dysfunctional`, `endure`, `force`, `inarticulate`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text uses strongly negative words like 'forced to endure', 'terminally depressed', 'inarticulate', and 'hyper dysfunctional' to express a highly unfavorable view of the film."}
```

**Rationale text:**
> The text uses strongly negative words like 'forced to endure', 'terminally depressed', 'inarticulate', and 'hyper dysfunctional' to express a highly unfavorable view of the film.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `depress`, `dysfunctional`, `endure`, `force`, `hyper`, `inarticulate`, `terminally`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "for close to two hours the audience is treated to three deeply complex, mostly articulate, highly engaging families for the price of one.", "new_prediction": "positive"}
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

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["endure", "dysfunctional", "depressed", "inarticulate"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `endure`(1), `dysfunctional`(2), `depress`(3), `inarticulate`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.7143 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.8000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5714 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3332 |

### sst2_validation_000007 — deepseek-v3

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "or doing last year 's taxes with your ex-wife . "

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
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 10 words
- **Raw response length:** 20 chars
- **Prompt hash:** `bed5ce4a26311b72`
- **ECS (full):** 0.1333
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["or", 1], ["doing", 3], ["last", 2], ["year", 2], ["'s", 1], ["taxes", 4], ["with", 2], ["your", 2], ["ex-wife", 10], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex-wife`, `last`, `tax`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text is negative because it combines the universally stressful task of doing taxes with the emotional difficulty of interacting with an ex-spouse."}
```

**Rationale text:**
> The text is negative because it combines the universally stressful task of doing taxes with the emotional difficulty of interacting with an ex-spouse.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible — change at most a third of the words, and do not add new sentences.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "or doing last year 's taxes with your best friend .", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> or doing last year 's taxes with your best friend .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex-wife`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "or doing last year 's taxes with your ex-wife . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["ex-wife", "taxes", "last"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ex-wife`(1), `tax`(2), `last`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 1.0000 | 0.3333 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2710 |

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
- **Verbalized confidence:** 0.80
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 24 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 0 | **CC4 size:** 0

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
    ["we", 6],
    ["did", 7],
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
  "ranking": ["Iraq", "did", "just", "look"]
}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### mnli_validation_matched_008565 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "entailment"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 27 chars
- **Prompt hash:** `f71b2f7bec2f3b88`
- **ECS (full):** 0.8333
- **ECS (extraction–rationale):** 0.8333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 3],
    ["In", 5],
    ["1099,", 6],
    ["under", 5],
    ["their", 4],
    ["leaders", 6],
    ["Godfrey", 7],
    ["de", 6],
    ["Bouillon", 7],
    ["and", 5],
    ["Tancred,", 7],
    ["the", 4],
    ["Crusaders", 10],
    ["captured", 10],
    ["the", 4],
    ["Holy", 8],
    ["City", 8],
    ["for", 5],
    ["Christendom", 7],
    ["by", 5],
    ["slaughtering", 7],
    ["both", 5],
    ["Muslims", 6],
    ["and", 4],
    ["Jews.", 6],
    ["Hypothesis:", 3],
    ["The", 4],
    ["Crusaders", 10],
    ["captured", 10],
    ["the", 4],
    ["Holy", 8],
    ["City.", 8]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bouillon`, `capture`, `christendom`, `city`, `crusader`, `holy`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise directly states that the Crusaders captured the Holy City, which is exactly what the hypothesis claims."
}
```

**Rationale text:**
> The premise directly states that the Crusaders captured the Holy City, which is exactly what the hypothesis claims.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`, `city`, `crusader`, `holy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.\nHypothesis: The Crusaders failed to capture the Holy City.",
  "new_prediction": "contradiction"
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
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["Crusaders", "captured", "City", "Holy"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `crusader`(1), `capture`(2), `city`(3), `holy`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6667 |
| R–CF | — | — |
| R–RO | 1.0000 | 1.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3358 |

### mnli_validation_matched_009319 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "entailment"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 27 chars
- **Prompt hash:** `37f688ab6ac9c2c5`
- **ECS (full):** 0.4167
- **ECS (extraction–rationale):** 0.4167
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["and", 1],
    ["they", 5],
    ["have", 5],
    ["a", 1],
    ["bar", 4],
    ["also", 2],
    ["which", 3],
    ["is", 1],
    ["always", 3],
    ["crowded", 4],
    ["as", 1],
    ["can", 2],
    ["be", 2],
    ["but", 3],
    ["it's", 2],
    ["it's", 2],
    ["an", 1],
    ["specially", 4],
    ["fine", 5],
    ["restaurant", 6],
    ["and", 1],
    ["when", 3],
    ["you", 2],
    ["consider", 5],
    ["they", 5],
    ["take", 7],
    ["no", 8],
    ["plastic", 6],
    ["or", 4],
    ["checks", 6],
    ["Hypothesis:", 1],
    ["They", 5],
    ["only", 8],
    ["take", 7],
    ["cash,", 9],
    ["which", 3],
    ["can", 2],
    ["be", 2],
    ["inconvenient.", 6]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cash`, `check`, `consider`, `inconvenient`, `no`, `plastic`, `restaurant`, `take`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states that the restaurant does not accept plastic (credit cards) or checks, which logically entails that they only accept cash, as mentioned in the hypothesis."}
```

**Rationale text:**
> The premise states that the restaurant does not accept plastic (credit cards) or checks, which logically entails that they only accept cash, as mentioned in the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cash`, `check`, `plastic`, `restaurant`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks\nHypothesis: They accept plastic and checks, which is convenient.",
  "new_prediction": "contradiction"
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
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["plastic", "checks", "inconvenient", "take"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `plastic`(1), `check`(2), `inconvenient`(3), `take`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.5000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | -0.6667 |
| Normalized τ | 0.1667 |
| RBO (H,RO) | 0.1695 |

### mnli_validation_matched_007354 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "entailment"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 27 chars
- **Prompt hash:** `d03a6bac45bd33be`
- **ECS (full):** 0.5333
- **ECS (extraction–rationale):** 0.8750
- **ECS (extraction–perturbation):** 0.2917
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 1],
    ["we", 8],
    ["only", 10],
    ["have", 10],
    ["to", 10],
    ["get", 10],
    ["up", 10],
    ["for", 10],
    ["you", 2],
    ["know", 2],
    ["for", 10],
    ["the", 8],
    ["daytime", 10],
    ["feedings", 10],
    ["Hypothesis:", 1],
    ["We", 8],
    ["only", 10],
    ["have", 10],
    ["to", 10],
    ["get", 10],
    ["up", 10],
    ["for", 10],
    ["the", 8],
    ["daytime", 10],
    ["feedings.", 10]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `fee`, `get`, `know`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise directly supports the hypothesis by stating the same condition about getting up only for daytime feedings."
}
```

**Rationale text:**
> The premise directly supports the hypothesis by stating the same condition about getting up only for daytime feedings.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `fee`, `get`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: we only have to get up for you know for the daytime feedings\nHypothesis: We only have to get up for the nighttime feedings.",
  "new_prediction": "contradiction"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the nighttime feedings.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["get", "up", "daytime", "feedings"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `get`(1), `daytime`(2), `fee`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.7500 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | 1.0000 | 0.7500 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 1.0000 | 1.0000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1807 |

### mnli_validation_matched_007556 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units.

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
- **Ground truth:** `entailment`
- **Predicted:** `neutral` ✗
- **Verbalized confidence:** 0.70
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 24 chars
- **Prompt hash:** `b8619d83a5f459e3`
- **ECS (full):** 0.4028
- **ECS (extraction–rationale):** 0.4028
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 5],
    ["If", 7],
    ["necessary", 8],
    ["to", 5],
    ["meeting", 7],
    ["the", 4],
    ["restrictions", 8],
    ["imposed", 7],
    ["in", 4],
    ["the", 4],
    ["preceding", 6],
    ["sentence,", 6],
    ["the", 4],
    ["Administrator", 9],
    ["shall", 8],
    ["reduce,", 8],
    ["pro", 6],
    ["rata,", 6],
    ["the", 4],
    ["basic", 7],
    ["Phase", 7],
    ["II", 7],
    ["allowance", 9],
    ["allocations", 9],
    ["for", 6],
    ["each", 7],
    ["unit", 8],
    ["subject", 8],
    ["to", 5],
    ["the", 4],
    ["requirements", 9],
    ["of", 5],
    ["section", 9],
    ["414.", 9],
    ["Hypothesis:", 5],
    ["Section", 9],
    ["414", 9],
    ["helps", 8],
    ["balance", 9],
    ["allowance", 9],
    ["allocations", 9],
    ["for", 6],
    ["units.", 8]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `414`, `administrator`, `allocation`, `allowance`, `balance`, `help`, `necessary`, `requirement`, `section`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise describes a condition under which the Administrator may adjust allowance allocations, but it does not explicitly state that Section 414's purpose is to balance these allocations, hence the relationship is neutral."
}
```

**Rationale text:**
> The premise describes a condition under which the Administrator may adjust allowance allocations, but it does not explicitly state that Section 414's purpose is to balance these allocations, hence the relationship is neutral.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `administrator`, `allocation`, `allowance`, `balance`, `section`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.\nHypothesis: Section 414 mandates balancing allowance allocations for units.",
  "new_prediction": "entailment"
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

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["section", "allocations", "reduce", "necessary", "units"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `section`(1), `allocation`(2), `reduce`(3), `necessary`(4), `unit`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.5556 |
| H–CF | — | — |
| H–RO | 0.6000 | 0.2727 |
| R–CF | — | — |
| R–RO | 0.4000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1097 |

### mnli_validation_matched_006801 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "contradiction"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 30 chars
- **Prompt hash:** `a23647bceb96e5d0`
- **ECS (full):** 0.1875
- **ECS (extraction–rationale):** 0.1875
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 3],
    ["Favorite", 6],
    ["items", 7],
    ["that", 5],
    ["will", 5],
    ["help", 6],
    ["preserve", 7],
    ["your", 5],
    ["memories", 7],
    ["of", 4],
    ["the", 4],
    ["rugged", 6],
    ["Lakeland", 7],
    ["countryside", 7],
    ["are", 5],
    ["clothing", 7],
    ["or", 4],
    ["blankets", 7],
    ["made", 6],
    ["from", 5],
    ["the", 4],
    ["local", 6],
    ["Herdwick", 8],
    ["wool,", 6],
    ["coasters", 7],
    ["of", 4],
    ["polished", 6],
    ["slate,", 6],
    ["or", 4],
    ["walking", 7],
    ["sticks", 7],
    ["with", 5],
    ["ram's-horn", 8],
    ["handles.", 6],
    ["Hypothesis:", 3],
    ["They", 7],
    ["don't", 9],
    ["sell", 9],
    ["any", 8],
    ["souveineers.", 9]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `blanket`, `clothe`, `don't`, `herdwick`, `ram's-horn`, `sell`, `souveineers`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise lists specific souvenirs for sale, directly contradicting the hypothesis that no souvenirs are sold."
}
```

**Rationale text:**
> The premise lists specific souvenirs for sale, directly contradicting the hypothesis that no souvenirs are sold.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sell`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{
  "rewritten": "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.\nHypothesis: They sell various souvenirs.",
  "new_prediction": "neutral"
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
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["souveineers", "don't", "items", "sell"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `souveineers`(1), `don't`(2), `item`(3), `sell`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.1250 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.3333 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2633 |

### mnli_validation_matched_005549 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier.

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
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 24 chars
- **Prompt hash:** `573b8c907f1848b8`
- **ECS (full):** 0.2750
- **ECS (extraction–rationale):** 0.2750
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 10],
    ["The", 8],
    ["Santa", 9],
    ["Monica", 9],
    ["Pier", 9],
    ["is", 7],
    ["the", 8],
    ["coastal", 9],
    ["setting", 9],
    ["for", 8],
    ["the", 8],
    ["Twilight", 9],
    ["Dance", 9],
    ["Series,", 9],
    ["a", 6],
    ["selection", 9],
    ["of", 7],
    ["free", 9],
    ["summer", 9],
    ["concerts", 9],
    ["arranged", 9],
    ["each", 8],
    ["year.", 8],
    ["Hypothesis:", 10],
    ["The", 8],
    ["Twilight", 9],
    ["Dance", 9],
    ["Series", 9],
    ["also", 9],
    ["hosts", 9],
    ["events", 9],
    ["directly", 9],
    ["on", 8],
    ["the", 8],
    ["beach", 9],
    ["near", 8],
    ["the", 8],
    ["pier.", 8]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `arrange`, `beach`, `coastal`, `concert`, `dance`, `directly`, `event`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise does not provide information about events being hosted directly on the beach near the pier, so it neither confirms nor denies the hypothesis."
}
```

**Rationale text:**
> The premise does not provide information about events being hosted directly on the beach near the pier, so it neither confirms nor denies the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `beach`, `directly`, `event`, `host`, `pier`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.\nHypothesis: The Twilight Dance Series exclusively hosts events at the Santa Monica Pier.",
  "new_prediction": "contradiction"
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
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["Twilight", "Dance", "Series", "pier", "beach"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `twilight`(1), `dance`(2), `series`(3), `pier`(4), `beach`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6000 | 0.3000 |
| H–CF | — | — |
| H–RO | 0.4000 | 0.1818 |
| R–CF | — | — |
| R–RO | 0.4000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0599 |

### mnli_validation_matched_006492 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 19 chars
- **Prompt hash:** `aae0ec2710ab04a3`
- **ECS (full):** 0.3500
- **ECS (extraction–rationale):** 0.3500
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
"salience": [
["Premise:", 5],
["Hang", 7],
["it", 6],
["all!", 7],
["said", 8],
["Tommy", 9],
["indignantly.", 10],
["Hypothesis:", 5],
["Tommy", 9],
["did", 7],
["n't", 7],
["realize", 9],
["he", 7],
["was", 7],
["being", 7],
["indignant.", 10]
]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignant`, `indignantly`, `realize`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise describes Tommy's reaction as indignant, but it does not provide information on whether he was aware of his indignation, thus it is neutral to the hypothesis that he didn't realize it."}
```

**Rationale text:**
> The premise describes Tommy's reaction as indignant, but it does not provide information on whether he was aware of his indignation, thus it is neutral to the hypothesis that he didn't realize it.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignant`, `realize`, `tommy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: Hang it all! said Tommy indignantly.\nHypothesis: Tommy realized he was being indignant.", "new_prediction": "contradiction"}
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

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Tommy", "indignantly", "didn't"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tommy`(1), `indignantly`(2), `didn't`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.5000 |
| H–CF | — | — |
| H–RO | 0.3333 | 0.2000 |
| R–CF | — | — |
| R–RO | 0.3333 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0720 |

### mnli_validation_matched_009361 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. 

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "entailment"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 20 words
- **Raw response length:** 27 chars
- **Prompt hash:** `dde94c5611b7520a`
- **ECS (full):** 0.2333
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** 0.2500
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 5],
    ["I", 6],
    ["am", 6],
    ["glad", 9],
    ["she", 8],
    ["wasn't,", 9],
    ["said", 7],
    ["Jon.", 8],
    ["Hypothesis:", 5],
    ["Jon", 8],
    ["was", 7],
    ["happy", 9],
    ["that", 8],
    ["Jane", 8],
    ["was", 7],
    ["not", 9],
    ["going", 8],
    ["to", 6],
    ["the", 6],
    ["dance.", 8]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `glad`, `happy`, `not`, `wasn't`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise indicates Jon's happiness about a situation involving'she', which aligns with the hypothesis stating Jon was happy about Jane not going to the dance, suggesting the same sentiment."
}
```

**Rationale text:**
> The premise indicates Jon's happiness about a situation involving'she', which aligns with the hypothesis stating Jon was happy about Jane not going to the dance, suggesting the same sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dance`, `go`, `happy`, `jane`, `jon`, `not`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: I am glad she wasn't, said Jon. Hypothesis: Jon was indifferent about Jane not going to the dance.",
  "new_prediction": "neutral"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: I am glad she wasn't, said Jon. Hypothesis: Jon was indifferent about Jane not going to the dance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happy`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["glad", "wasn't", "happy", "not"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `glad`(1), `wasn't`(2), `happy`(3), `not`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.2500 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 1.0000 | 0.1667 |
| R–RO | 0.5000 | 0.2500 |
| CF–RO | 1.0000 | 0.2500 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.2719 |

### mnli_validation_matched_004122 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "contradiction"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 70 words
- **Raw response length:** 30 chars
- **Prompt hash:** `2e0f12cf98d38bf9`
- **ECS (full):** 0.5357
- **ECS (extraction–rationale):** 0.5357
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["oh", 1],
    ["you", 3],
    ["went", 6],
    ["to", 4],
    ["the", 5],
    ["dollar", 9],
    ["movie", 9],
    ["yeah", 2],
    ["yeah", 2],
    ["they", 7],
    ["show", 8],
    ["up", 4],
    ["at", 5],
    ["the", 5],
    ["dollar", 9],
    ["movie", 9],
    ["right", 6],
    ["after", 6],
    ["they", 7],
    ["get", 5],
    ["come", 5],
    ["out", 5],
    ["you", 3],
    ["know", 5],
    ["they're", 7],
    ["usually", 6],
    ["not", 7],
    ["not", 7],
    ["that", 5],
    ["great", 6],
    ["or", 5],
    ["didn't", 6],
    ["do", 5],
    ["that", 5],
    ["great", 6],
    ["anyway", 4],
    ["let", 4],
    ["me", 3],
    ["see", 5],
    ["let", 4],
    ["me", 3],
    ["see", 5],
    ["another", 5],
    ["movie", 6],
    ["i", 3],
    ["watched", 5],
    ["uh", 2],
    ["i", 3],
    ["want", 5],
    ["to", 4],
    ["see", 5],
    ["is", 4],
    ["uh", 2],
    ["that", 5],
    ["new", 5],
    ["one", 5],
    ["uh", 2],
    ["Hypothesis:", 1],
    ["they're", 7],
    ["never", 9],
    ["shown", 9],
    ["at", 5],
    ["the", 5],
    ["dollar", 9],
    ["movie", 9],
    ["theater", 8],
    ["at", 5],
    ["any", 7],
    ["point", 7]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `another`, `any`, `didn't`, `dollar`, `go`, `great`, `movie`, `never`, `not`, `point`, `right`, `show`, `theater`, `usually`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states that movies do appear at the dollar movie theater shortly after their release, which directly contradicts the hypothesis that they are never shown there at any point."}
```

**Rationale text:**
> The premise states that movies do appear at the dollar movie theater shortly after their release, which directly contradicts the hypothesis that they are never shown there at any point.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `dollar`, `movie`, `never`, `point`, `show`, `theater`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{
  "rewritten": "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh\nHypothesis: they're sometimes shown at the dollar movie theater after release.",
  "new_prediction": "neutral"
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
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["show", "dollar", "movie", "never"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `show`(1), `dollar`(2), `movie`(3), `never`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.5000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.2857 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5714 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |
| RBO (H,RO) | 0.3918 |

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

### mnli_validation_matched_008565 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 22 chars
- **Prompt hash:** `f71b2f7bec2f3b88`
- **ECS (full):** 0.7083
- **ECS (extraction–rationale):** 0.7083
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 1], ["In", 3], ["1099,", 7], ["under", 2], ["their", 1], ["leaders", 5], ["Godfrey", 6], ["de", 4], ["Bouillon", 6], ["and", 2], ["Tancred,", 6], ["the", 3], ["Crusaders", 10], ["captured", 10], ["the", 3], ["Holy", 9], ["City", 9], ["for", 2], ["Christendom", 6], ["by", 1], ["slaughtering", 5], ["both", 2], ["Muslims", 4], ["and", 2], ["Jews.", 4], ["Hypothesis:", 1], ["The", 3], ["Crusaders", 10], ["captured", 10], ["the", 3], ["Holy", 9], ["City.", 9]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `1099`, `bouillon`, `capture`, `city`, `crusader`, `holy`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise explicitly states that the Crusaders captured the Holy City in 1099, which directly supports the hypothesis."}
```

**Rationale text:**
> The premise explicitly states that the Crusaders captured the Holy City in 1099, which directly supports the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`, `city`, `crusader`, `holy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.\nHypothesis: The Crusaders failed to capture the Holy City.", "new_prediction": "contradiction"}
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

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["captured", "Crusaders", "City"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`(1), `crusader`(2), `city`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.5000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.7500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3946 |

### mnli_validation_matched_009319 — qwen3-235b

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient.

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
- **Input length:** 40 words
- **Raw response length:** 22 chars
- **Prompt hash:** `37f688ab6ac9c2c5`
- **ECS (full):** 0.7946
- **ECS (extraction–rationale):** 0.7946
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 5 | **CC4 size:** 5

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 3], ["and", 4], ["they", 6], ["have", 4], ["a", 2], ["bar", 3], ["also", 3], ["which", 5], ["is", 4], ["always", 5], ["crowded", 4], ["as", 3], ["can", 5], ["be", 4], ["but", 6], ["it's", 5], ["it's", 5], ["an", 2], ["specially", 6], ["fine", 6], ["restaurant", 7], ["and", 5], ["when", 5], ["you", 4], ["consider", 7], ["they", 6], ["take", 8], ["no", 9], ["plastic", 9], ["or", 7], ["checks", 9], ["Hypothesis:", 3], ["They", 6], ["only", 8], ["take", 8], ["cash,", 10], ["which", 5], ["can", 5], ["be", 4], ["inconvenient.", 7]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cash`, `check`, `consider`, `inconvenient`, `no`, `plastic`, `restaurant`, `take`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states the restaurant takes no plastic or checks, implying they only accept cash, which supports the hypothesis that this policy can be inconvenient."}
```

**Rationale text:**
> The premise states the restaurant takes no plastic or checks, implying they only accept cash, which supports the hypothesis that this policy can be inconvenient.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cash`, `check`, `inconvenient`, `no`, `plastic`, `restaurant`, `take`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks\nHypothesis: They accept all major credit cards, which is very convenient.", "new_prediction": "contradiction"}
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

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["plastic", "checks", "cash", "take", "inconvenient"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `plastic`(1), `check`(2), `cash`(3), `take`(4), `inconvenient`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.8750 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6250 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.7143 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |
| RBO (H,RO) | 0.3134 |

### mnli_validation_matched_007354 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 22 chars
- **Prompt hash:** `d03a6bac45bd33be`
- **ECS (full):** 0.8750
- **ECS (extraction–rationale):** 0.8750
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 5], ["we", 7], ["only", 10], ["have", 6], ["to", 8], ["get", 9], ["up", 9], ["for", 8], ["you", 3], ["know", 2], ["for", 8], ["the", 7], ["daytime", 10], ["feedings", 10], ["Hypothesis:", 5], ["We", 7], ["only", 10], ["have", 6], ["to", 8], ["get", 9], ["up", 9], ["for", 8], ["the", 7], ["daytime", 10], ["feedings", 10], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `fee`, `get`, `know`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise and hypothesis convey the same essential meaning, with the premise's informal phrasing ('you know') not altering the core claim that only daytime feedings require getting up."}
```

**Rationale text:**
> The premise and hypothesis convey the same essential meaning, with the premise's informal phrasing ('you know') not altering the core claim that only daytime feedings require getting up.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `fee`, `get`, `know`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: we only have to get up for you know for the daytime feedings\nHypothesis: We have to get up for both daytime and nighttime feedings.", "new_prediction": "contradiction"}
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

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["only", "get", "daytime", "feedings", "up"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `get`(1), `daytime`(2), `fee`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 1.0000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.7500 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.7500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1807 |

### mnli_validation_matched_007556 — qwen3-235b

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `neutral` ✗
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 19 chars
- **Prompt hash:** `b8619d83a5f459e3`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["The", 1], ["text", 2], ["was", 1], ["classified", 3], ["as", 1], [":", 1], ["neutral", 10], ["Text", 2], [":", 1], ["\"", 1], ["Premise", 8], [":", 1], ["If", 5], ["necessary", 7], ["to", 4], ["meeting", 6], ["the", 3], ["restrictions", 8], ["imposed", 7], ["in", 4], ["the", 3], ["preceding", 6], ["sentence", 6], [",", 1], ["the", 3], ["Administrator", 7], ["shall", 5], ["reduce", 9], [",", 1], ["pro", 6], ["rata", 7], [",", 1], ["the", 3], ["basic", 5], ["Phase", 6], ["II", 5], ["allowance", 8], ["allocations", 8], ["for", 4], ["each", 5], ["unit", 7], ["subject", 6], ["to", 4], ["the", 3], ["requirements", 8], ["of", 3], ["section", 7], ["414", 8], [".", 1], ["Hypothesis", 8], [":", 1], ["Section", 7], ["414", 8], ["helps", 7], ["balance", 7], ["allowance", 8], ["allocations", 8], ["for", 4], ["units", 7], ["."], 1], ["\""], 1]}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise describes a mechanism for reducing allowances under section 414 if needed, but does not explicitly state or imply that section 414's purpose or effect is to balance allocations, leaving the hypothesis neither confirmed nor contradicted."}
```

**Rationale text:**
> The premise describes a mechanism for reducing allowances under section 414 if needed, but does not explicitly state or imply that section 414's purpose or effect is to balance allocations, leaving the hypothesis neither confirmed nor contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `allocation`, `allowance`, `balance`, `reduce`, `section`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.\nHypothesis: Section 414 requires pro rata reductions of Phase II allowance allocations when necessary.", "new_prediction": "entailment"}
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
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Section", "balance", "allocations", "reduce", "requirements"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `section`(1), `balance`(2), `allocation`(3), `reduce`(4), `requirement`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | 0.8000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### mnli_validation_matched_006801 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 25 chars
- **Prompt hash:** `a23647bceb96e5d0`
- **ECS (full):** 0.2475
- **ECS (extraction–rationale):** 0.2475
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 3], ["Favorite", 6], ["items", 8], ["that", 4], ["will", 5], ["help", 7], ["preserve", 9], ["your", 5], ["memories", 9], ["of", 3], ["the", 2], ["rugged", 6], ["Lakeland", 7], ["countryside", 7], ["are", 5], ["clothing", 8], ["or", 4], ["blankets", 8], ["made", 6], ["from", 4], ["the", 2], ["local", 7], ["Herdwick", 8], ["wool,", 8], ["coasters", 8], ["of", 3], ["polished", 7], ["slate,", 8], ["or", 4], ["walking", 7], ["sticks", 8], ["with", 5], ["ram's-horn", 8], ["handles.", 8], ["Hypothesis:", 3], ["They", 4], ["don't", 9], ["sell", 9], ["any", 6], ["souveineers.", 10]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `blanket`, `clothe`, `coaster`, `don't`, `memory`, `preserve`, `sell`, `souveineers`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise lists specific items available for preserving memories of the Lakeland countryside, implying that souvenirs are sold, which directly contradicts the hypothesis stating that no souvenirs are sold."}
```

**Rationale text:**
> The premise lists specific items available for preserving memories of the Lakeland countryside, implying that souvenirs are sold, which directly contradicts the hypothesis stating that no souvenirs are sold.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `countryside`, `item`, `lakeland`, `memory`, `preserve`, `sell`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"rewritten": "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.\nHypothesis: They sell souvenirs.", "new_prediction": "entailment"}
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
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["souveniers", "items", "sell", "clothing", "blankets"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `item`(1), `sell`(2), `clothe`(3), `blanket`(4), `coaster`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.2727 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.4444 |
| R–CF | — | — |
| R–RO | 0.4000 | 0.2222 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.0795 |

### mnli_validation_matched_005549 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Verbalized confidence:** 0.92
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 19 chars
- **Prompt hash:** `573b8c907f1848b8`
- **ECS (full):** 0.4545
- **ECS (extraction–rationale):** 0.4545
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 5], ["The", 4], ["Santa", 8], ["Monica", 8], ["Pier", 8], ["is", 3], ["the", 4], ["coastal", 6], ["setting", 7], ["for", 3], ["the", 4], ["Twilight", 9], ["Dance", 8], ["Series,", 8], ["a", 2], ["selection", 5], ["of", 2], ["free", 5], ["summer", 6], ["concerts", 7], ["arranged", 5], ["each", 3], ["year.", 5], ["Hypothesis:", 5], ["The", 4], ["Twilight", 9], ["Dance", 8], ["Series", 8], ["also", 6], ["hosts", 6], ["events", 6], ["directly", 7], ["on", 4], ["the", 4], ["beach", 8], ["near", 5], ["the", 4], ["pier.", 7]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `beach`, `concert`, `dance`, `monica`, `pier`, `santa`, `series`, `twilight`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states that the Santa Monica Pier is the setting for the Twilight Dance Series but does not specify whether events are held directly on the beach near the pier, leaving the hypothesis neither confirmed nor contradicted."}
```

**Rationale text:**
> The premise states that the Santa Monica Pier is the setting for the Twilight Dance Series but does not specify whether events are held directly on the beach near the pier, leaving the hypothesis neither confirmed nor contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `beach`, `dance`, `directly`, `event`, `monica`, `pier`, `santa`, `series`, `set`, `twilight`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.\nHypothesis: The Twilight Dance Series hosts all events directly on the beach near the pier.", "new_prediction": "contradiction"}
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

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Pier", "beach", "hosts", "setting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `pier`(1), `beach`(2), `host`(3), `set`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8750 | 0.6364 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.2000 |
| R–CF | — | — |
| R–RO | 0.7500 | 0.2727 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1633 |

### mnli_validation_matched_006492 — qwen3-235b

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 25 chars
- **Prompt hash:** `aae0ec2710ab04a3`
- **ECS (full):** 0.7500
- **ECS (extraction–rationale):** 0.7500
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 3], ["Hang", 7], ["it", 4], ["all!", 8], ["said", 5], ["Tommy", 9], ["indignantly.", 10], ["Hypothesis:", 3], ["Tommy", 9], ["didnt", 10], ["realize", 9], ["he", 6], ["was", 5], ["being", 7], ["indignant.", 10]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignant`, `indignantly`, `realize`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise explicitly states that Tommy spoke indignantly, which implies awareness of his emotion, contradicting the hypothesis that he didn't realize he was being indignant."}
```

**Rationale text:**
> The premise explicitly states that Tommy spoke indignantly, which implies awareness of his emotion, contradicting the hypothesis that he didn't realize he was being indignant.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignant`, `indignantly`, `realize`, `tommy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"rewritten": "Premise: Hang it all! said Tommy indignantly.\nHypothesis: Tommy was being indignant.", "new_prediction": "entailment"}
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
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["indignantly", "Tommy", "realize", "Hang"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignantly`(1), `tommy`(2), `realize`(3), `hang`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.7500 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.5000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.7500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1354 |

### mnli_validation_matched_009361 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. 

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 20 words
- **Raw response length:** 19 chars
- **Prompt hash:** `dde94c5611b7520a`
- **ECS (full):** 0.2054
- **ECS (extraction–rationale):** 0.2054
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 3], ["I", 6], ["am", 4], ["glad", 9], ["she", 8], ["wasn't,", 8], ["said", 3], ["Jon.", 6], ["Hypothesis:", 3], ["Jon", 6], ["was", 4], ["happy", 9], ["that", 3], ["Jane", 7], ["was", 4], ["not", 8], ["going", 5], ["to", 3], ["the", 2], ["dance.", 6]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `glad`, `happy`, `not`, `wasn't`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise expresses Jon's relief about an unspecified event involving an unnamed female, but does not provide enough information to confirm that it refers to Jane not going to the dance."}
```

**Rationale text:**
> The premise expresses Jon's relief about an unspecified event involving an unnamed female, but does not provide enough information to confirm that it refers to Jane not going to the dance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dance`, `go`, `jane`, `jon`, `not`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: I am glad she wasn't, said Jon.\nHypothesis: Jon was glad that she wasn't going to the dance.", "new_prediction": "entailment"}
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
The text was classified as: neutral

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["glad", "she", "wasn't", "Jon", "dance"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `glad`(1), `wasn't`(2), `jon`(3), `dance`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.2500 | 0.1250 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.3333 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2857 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2084 |

### mnli_validation_matched_004122 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 70 words
- **Raw response length:** 25 chars
- **Prompt hash:** `2e0f12cf98d38bf9`
- **ECS (full):** 0.5992
- **ECS (extraction–rationale):** 0.5992
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 5 | **CC4 size:** 5

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Premise:", 3], ["oh", 1], ["you", 2], ["went", 3], ["to", 2], ["the", 2], ["dollar", 9], ["movie", 8], ["yeah", 1], ["yeah", 1], ["they", 8], ["show", 10], ["up", 5], ["at", 2], ["the", 2], ["dollar", 9], ["movie", 8], ["right", 6], ["after", 5], ["they", 5], ["get", 3], ["come", 4], ["out", 6], ["you", 2], ["know", 2], ["they're", 7], ["usually", 6], ["not", 5], ["not", 5], ["that", 3], ["great", 4], ["or", 3], ["didn't", 5], ["do", 3], ["that", 3], ["great", 4], ["anyway", 2], ["let", 1], ["me", 2], ["see", 3], ["let", 1], ["me", 2], ["see", 3], ["another", 3], ["movie", 5], ["i", 2], ["watched", 3], ["uh", 1], ["i", 2], ["want", 4], ["to", 2], ["see", 3], ["is", 2], ["uh", 1], ["that", 3], ["new", 4], ["one", 2], ["uh", 1], ["Hypothesis:", 3], ["they're", 8], ["never", 10], ["shown", 10], ["at", 2], ["the", 2], ["dollar", 9], ["movie", 8], ["theater", 7], ["at", 2], ["any", 5], ["point", 6]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `come`, `didn't`, `dollar`, `great`, `movie`, `never`, `new`, `not`, `point`, `right`, `show`, `theater`, `usually`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states that movies are shown at the dollar movie theater right after they come out, which directly contradicts the hypothesis that they are never shown there at any point."}
```

**Rationale text:**
> The premise states that movies are shown at the dollar movie theater right after they come out, which directly contradicts the hypothesis that they are never shown there at any point.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `come`, `dollar`, `movie`, `never`, `point`, `right`, `show`, `theater`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"rewritten": "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh\nHypothesis: they're sometimes shown at the dollar movie theater", "new_prediction": "entailment"}
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
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["never", "show", "dollar", "movie", "right"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `never`(1), `show`(2), `dollar`(3), `movie`(4), `right`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6429 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.3571 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5556 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |
| RBO (H,RO) | 0.5958 |

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
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 3 | **CC4 size:** 0

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
{
  "salience": [
    ["just", 2],
    ["look", 3],
    ["what", 3],
    ["we", 4],
    ["did", 7],
    ["to", 2],
    ["Iraq", 10],
    ["Iraq", 10],
    ["was", 2],
    ["something", 3],
    ["that", 2],
    ["shouldn't", 8],
    ["have", 2],
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
{"ranking": ["Iraq", "shouldn't", "happened", "did"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`(1), `shouldn't`(2), `happen`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.5000 |
| H–CF | 1.0000 | 0.3333 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2710 |

### mnli_validation_matched_008565 — deepseek-v3

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 22 chars
- **Prompt hash:** `f71b2f7bec2f3b88`
- **ECS (full):** 0.8333
- **ECS (extraction–rationale):** 0.8333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
  "salience": [
    ["In", 1],
    ["1099,", 1],
    ["under", 1],
    ["their", 1],
    ["leaders", 1],
    ["Godfrey", 1],
    ["de", 1],
    ["Bouillon", 1],
    ["and", 1],
    ["Tancred,", 1],
    ["the", 1],
    ["Crusaders", 10],
    ["captured", 10],
    ["the", 1],
    ["Holy", 10],
    ["City", 10],
    ["for", 1],
    ["Christendom", 1],
    ["by", 1],
    ["slaughtering", 1],
    ["both", 1],
    ["Muslims", 1],
    ["and", 1],
    ["Jews.", 1],
    ["The", 1],
    ["Crusaders", 10],
    ["captured", 10],
    ["the", 1],
    ["Holy", 10],
    ["City.", 10]
  ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `1099`, `bouillon`, `capture`, `city`, `crusader`, `holy`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise directly states that the Crusaders captured the Holy City, which is the exact claim made in the hypothesis."}
```

**Rationale text:**
> The premise directly states that the Crusaders captured the Holy City, which is the exact claim made in the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`, `city`, `crusader`, `holy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
```json
{
    "rewritten": "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.\nHypothesis: The Crusaders failed to capture the Holy City.",
    "new_prediction": "contradiction"
}
```
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

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["captured", "Crusaders", "Holy", "City"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`(1), `crusader`(2), `holy`(3), `city`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6667 |
| R–CF | — | — |
| R–RO | 1.0000 | 1.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.3638 |

### mnli_validation_matched_009319 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient.

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
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 22 chars
- **Prompt hash:** `37f688ab6ac9c2c5`
- **ECS (full):** 0.3961
- **ECS (extraction–rationale):** 0.3961
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["and", 1],
    ["they", 1],
    ["have", 1],
    ["a", 1],
    ["bar", 1],
    ["also", 1],
    ["which", 1],
    ["is", 1],
    ["always", 1],
    ["crowded", 1],
    ["as", 1],
    ["can", 1],
    ["be", 1],
    ["but", 1],
    ["it's", 1],
    ["it's", 1],
    ["an", 1],
    ["specially", 1],
    ["fine", 1],
    ["restaurant", 1],
    ["and", 1],
    ["when", 1],
    ["you", 1],
    ["consider", 1],
    ["they", 1],
    ["take", 10],
    ["no", 10],
    ["plastic", 10],
    ["or", 10],
    ["checks", 10]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `always`, `bar`, `check`, `consider`, `no`, `plastic`, `take`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states the restaurant 'takes no plastic or checks', which directly entails that they only accept cash, and the hypothesis correctly identifies this payment limitation as potentially inconvenient."}
```

**Rationale text:**
> The premise states the restaurant 'takes no plastic or checks', which directly entails that they only accept cash, and the hypothesis correctly identifies this payment limitation as potentially inconvenient.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cash`, `check`, `inconvenient`, `no`, `plastic`, `restaurant`, `take`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
```json
{
    "rewritten": "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks\nHypothesis: They only take cash, which is very convenient.",
    "new_prediction": "contradiction"
}
```
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

Text: "Premise: and they have a bar also which is always crowded as can be  but it's it's an specially fine restaurant and when you consider they take no plastic or checks
Hypothesis: They only take cash, which can be inconvenient."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["cash", "plastic", "checks"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cash`(1), `plastic`(2), `check`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5714 | 0.3636 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.2222 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.4286 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1635 |

### mnli_validation_matched_007354 — deepseek-v3

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 22 chars
- **Prompt hash:** `d03a6bac45bd33be`
- **ECS (full):** 0.5000
- **ECS (extraction–rationale):** 1.0000
- **ECS (extraction–perturbation):** 0.2500
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["we", 1],
    ["only", 10],
    ["have", 1],
    ["to", 1],
    ["get", 1],
    ["up", 1],
    ["for", 1],
    ["you", 1],
    ["know", 1],
    ["for", 1],
    ["the", 1],
    ["daytime", 10],
    ["feedings", 10],
    ["We", 1],
    ["only", 10],
    ["have", 1],
    ["to", 1],
    ["get", 1],
    ["up", 1],
    ["for", 1],
    ["the", 1],
    ["daytime", 10],
    ["feedings", 10]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `fee`, `get`, `know`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise and hypothesis express the same core proposition that getting up is only required for daytime feedings, with the premise's additional phrase 'you know' being a discourse marker that does not change the fundamental meaning."}
```

**Rationale text:**
> The premise and hypothesis express the same core proposition that getting up is only required for daytime feedings, with the premise's additional phrase 'you know' being a discourse marker that does not change the fundamental meaning.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `fee`, `get`, `know`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
```json
{
    "rewritten": "Premise: we only have to get up for you know for the daytime feedings\nHypothesis: We only have to get up for the nighttime feedings.",
    "new_prediction": "contradiction"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the nighttime feedings.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["daytime", "feedings", "only"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 1.0000 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | — | — |
| R–CF | 1.0000 | 0.2500 |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### mnli_validation_matched_007556 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `neutral` ✗
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 19 chars
- **Prompt hash:** `b8619d83a5f459e3`
- **ECS (full):** 0.2000
- **ECS (extraction–rationale):** 0.2000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
  "salience": [
    ["Premise:", 1],
    ["If", 3],
    ["necessary", 3],
    ["to", 1],
    ["meeting", 3],
    ["the", 1],
    ["restrictions", 4],
    ["imposed", 3],
    ["in", 1],
    ["the", 1],
    ["preceding", 4],
    ["sentence,", 1],
    ["the", 1],
    ["Administrator", 1],
    ["shall", 1],
    ["reduce,", 5],
    ["pro", 1],
    ["rata,", 1],
    ["the", 1],
    ["basic", 1],
    ["Phase", 1],
    ["II", 1],
    ["allowance", 6],
    ["allocations", 6],
    ["for", 1],
    ["each", 1],
    ["unit", 5],
    ["subject", 4],
    ["to", 1],
    ["the", 1],
    ["requirements", 6],
    ["of", 1],
    ["section", 7],
    ["414.", 7],
    ["Hypothesis:", 1],
    ["Section", 7],
    ["414", 7],
    ["helps", 5],
    ["balance", 5],
    ["allowance", 6],
    ["allocations", 6],
    ["for", 1],
    ["units.", 5]
  ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `414`, `allocation`, `allowance`, `balance`, `help`, `reduce`, `requirement`, `section`, `unit`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise describes a specific action the Administrator must take under section 414, but it does not state the purpose or effect of that section, so it neither supports nor contradicts the hypothesis that the section helps balance allocations."}
```

**Rationale text:**
> The premise describes a specific action the Administrator must take under section 414, but it does not state the purpose or effect of that section, so it neither supports nor contradicts the hypothesis that the section helps balance allocations.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `administrator`, `allocation`, `balance`, `help`, `section`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.\nHypothesis: Section 414 imposes restrictions that necessitate reducing allowance allocations for units.", "new_prediction": "entailment"}
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
The text was classified as: neutral

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["reduce", "restrictions", "requirements", "pro"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `reduce`(1), `restriction`(2), `requirement`(3), `pro`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.4000 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.1818 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0521 |

### mnli_validation_matched_006801 — deepseek-v3

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 25 chars
- **Prompt hash:** `a23647bceb96e5d0`
- **ECS (full):** 0.3429
- **ECS (extraction–rationale):** 0.3429
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Favorite", 1],
    ["items", 1],
    ["that", 1],
    ["will", 1],
    ["help", 1],
    ["preserve", 1],
    ["your", 1],
    ["memories", 1],
    ["of", 1],
    ["the", 1],
    ["rugged", 1],
    ["Lakeland", 1],
    ["countryside", 1],
    ["are", 1],
    ["clothing", 8],
    ["or", 1],
    ["blankets", 8],
    ["made", 1],
    ["from", 1],
    ["the", 1],
    ["local", 1],
    ["Herdwick", 1],
    ["wool", 1],
    [",", 1],
    ["coasters", 8],
    ["of", 1],
    ["polished", 1],
    ["slate", 1],
    [",", 1],
    ["or", 1],
    ["walking", 1],
    ["sticks", 8],
    ["with", 1],
    ["ram's-horn", 1],
    ["handles", 1],
    [".", 1],
    ["They", 1],
    ["don't", 10],
    ["sell", 10],
    ["any", 10],
    ["souveineers", 10],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `blanket`, `clothe`, `coaster`, `don't`, `sell`, `souveineers`, `stick`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise explicitly lists items for sale that are souvenirs (e.g., clothing, coasters, walking sticks), which directly contradicts the hypothesis claiming no souvenirs are sold."}
```

**Rationale text:**
> The premise explicitly lists items for sale that are souvenirs (e.g., clothing, coasters, walking sticks), which directly contradicts the hypothesis claiming no souvenirs are sold.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `clothe`, `coaster`, `item`, `sell`, `stick`, `walk`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"rewritten": "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.\nHypothesis: They sell many souvenirs.", "new_prediction": "entailment"}
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
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["souveineers", "items", "sell"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `souveineers`(1), `item`(2), `sell`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.4000 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.2222 |
| R–CF | — | — |
| R–RO | 0.6667 | 0.2857 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1365 |

### mnli_validation_matched_005549 — deepseek-v3

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Verbalized confidence:** 0.85
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 19 chars
- **Prompt hash:** `573b8c907f1848b8`
- **ECS (full):** 0.3889
- **ECS (extraction–rationale):** 0.3889
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["The", 1],
    ["Santa", 3],
    ["Monica", 3],
    ["Pier", 3],
    ["is", 1],
    ["the", 1],
    ["coastal", 4],
    ["setting", 4],
    ["for", 1],
    ["the", 1],
    ["Twilight", 5],
    ["Dance", 5],
    ["Series", 5],
    [",", 1],
    ["a", 1],
    ["selection", 1],
    ["of", 1],
    ["free", 1],
    ["summer", 1],
    ["concerts", 1],
    ["arranged", 1],
    ["each", 1],
    ["year", 1],
    [".", 1],
    ["The", 1],
    ["Twilight", 5],
    ["Dance", 5],
    ["Series", 5],
    ["also", 8],
    ["hosts", 6],
    ["events", 6],
    ["directly", 8],
    ["on", 7],
    ["the", 1],
    ["beach", 9],
    ["near", 7],
    ["the", 1],
    ["pier", 7],
    [".", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `dance`, `directly`, `event`, `host`, `near`, `pier`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states the concerts are held on the pier, but it does not provide any information about whether events are also held on the beach, so the hypothesis is neither confirmed nor denied."}
```

**Rationale text:**
> The premise states the concerts are held on the pier, but it does not provide any information about whether events are also held on the beach, so the hypothesis is neither confirmed nor denied.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `concert`, `event`, `pier`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "contradiction" instead of "neutral". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
```json
{
    "rewritten": "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.\nHypothesis: The Twilight Dance Series does not host events directly on the beach near the pier.",
    "new_prediction": "contradiction"
}
```
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

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["beach", "pier", "hosts"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `beach`(1), `pier`(2), `host`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.4444 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.3750 |
| R–CF | — | — |
| R–RO | 0.6667 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2769 |

### mnli_validation_matched_006492 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 25 chars
- **Prompt hash:** `aae0ec2710ab04a3`
- **ECS (full):** 0.3000
- **ECS (extraction–rationale):** 0.4000
- **ECS (extraction–perturbation):** 0.2500
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
    "salience": [
        ["Premise:", 1],
        ["Hang", 3],
        ["it", 1],
        ["all!", 3],
        ["said", 5],
        ["Tommy", 1],
        ["indignantly.", 10],
        ["Hypothesis:", 1],
        ["Tommy", 1],
        ["didn't", 10],
        ["realize", 10],
        ["he", 1],
        ["was", 1],
        ["being", 1],
        ["indignant.", 10]
    ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `didn't`, `indignant`, `indignantly`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise explicitly states that Tommy spoke indignantly, which directly contradicts the hypothesis that he did not realize he was being indignant."}
```

**Rationale text:**
> The premise explicitly states that Tommy spoke indignantly, which directly contradicts the hypothesis that he did not realize he was being indignant.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignant`, `indignantly`, `realize`, `tommy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"rewritten": "Premise: Hang it all! said Tommy indignantly.\nHypothesis: Tommy realized he was being indignant.", "new_prediction": "entailment"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**
> Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy realized he was being indignant.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `didn't`, `realize`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Hang it all! said Tommy indignantly.
Hypothesis: Tommy didn't realize he was being indignant."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["indignantly", "indignant", "didn't"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `indignantly`(1), `indignant`(2), `didn't`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.4000 |
| H–CF | 0.5000 | 0.2500 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.5000 | 0.2000 |
| R–RO | 0.6667 | 0.4000 |
| CF–RO | 0.5000 | 0.2500 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1260 |

### mnli_validation_matched_009361 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. 

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
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 20 words
- **Raw response length:** 22 chars
- **Prompt hash:** `dde94c5611b7520a`
- **ECS (full):** 0.1150
- **ECS (extraction–rationale):** 0.0625
- **ECS (extraction–perturbation):** 0.1250
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Premise:", 1],
    ["I", 10],
    ["am", 10],
    ["glad", 10],
    ["she", 8],
    ["wasn't,", 10],
    ["said", 1],
    ["Jon.", 1],
    ["Hypothesis:", 1],
    ["Jon", 1],
    ["was", 1],
    ["happy", 10],
    ["that", 1],
    ["Jane", 8],
    ["was", 1],
    ["not", 10],
    ["going", 1],
    ["to", 1],
    ["the", 1],
    ["dance.", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `glad`, `happy`, `not`, `wasn't`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise directly states Jon's gladness about 'she' not being something, which the hypothesis correctly identifies as happiness about Jane not going to the dance, making it a direct entailment."}
```

**Rationale text:**
> The premise directly states Jon's gladness about 'she' not being something, which the hypothesis correctly identifies as happiness about Jane not going to the dance, making it a direct entailment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dance`, `go`, `jane`, `jon`, `not`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "neutral" or "contradiction" instead of "entailment". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
```json
{
    "rewritten": "Premise: I am glad she wasn't, said Jon.\nHypothesis: Jon was happy that Jane was going to the dance.",
    "new_prediction": "contradiction"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `neutral`

**Reconstructed text:**
> Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was going to the dance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `not`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["glad", "wasn't", "happy"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `glad`(1), `wasn't`(2), `happy`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.2500 | 0.1250 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | 1.0000 | 0.7500 |
| R–CF | 1.0000 | 0.2000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.0000 | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2537 |

### mnli_validation_matched_004122 — deepseek-v3

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 70 words
- **Raw response length:** 25 chars
- **Prompt hash:** `2e0f12cf98d38bf9`
- **ECS (full):** 0.2719
- **ECS (extraction–rationale):** 0.2719
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["oh", 1],
    ["you", 1],
    ["went", 1],
    ["to", 1],
    ["the", 1],
    ["dollar", 10],
    ["movie", 10],
    ["yeah", 1],
    ["yeah", 1],
    ["they", 8],
    ["show", 9],
    ["up", 1],
    ["at", 1],
    ["the", 1],
    ["dollar", 10],
    ["movie", 10],
    ["right", 1],
    ["after", 1],
    ["they", 8],
    ["get", 1],
    ["come", 1],
    ["out", 1],
    ["you", 1],
    ["know", 1],
    ["they're", 8],
    ["usually", 5],
    ["not", 7],
    ["not", 7],
    ["that", 1],
    ["great", 1],
    ["or", 1],
    ["didn't", 1],
    ["do", 1],
    ["that", 1],
    ["great", 1],
    ["anyway", 1],
    ["let", 1],
    ["me", 1],
    ["see", 1],
    ["let", 1],
    ["me", 1],
    ["see", 1],
    ["another", 1],
    ["movie", 1],
    ["i", 1],
    ["watched", 1],
    ["uh", 1],
    ["i", 1],
    ["want", 1],
    ["to", 1],
    ["see", 1],
    ["is", 1],
    ["uh", 1],
    ["that", 1],
    ["new", 1],
    ["one", 1],
    ["uh", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `another`, `anyway`, `come`, `didn't`, `dollar`, `get`, `go`, `great`, `know`, `let`, `movie`, `not`, `show`, `usually`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise states that movies 'show up at the dollar movie right after they get come out', which directly contradicts the hypothesis that they are 'never shown at the dollar movie theater at any point'."}
```

**Rationale text:**
> The premise states that movies 'show up at the dollar movie right after they get come out', which directly contradicts the hypothesis that they are 'never shown at the dollar movie theater at any point'.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `come`, `dollar`, `movie`, `never`, `point`, `right`, `show`, `theater`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as "entailment" or "neutral" instead of "contradiction". Make as few edits as possible — change at most a third of the Hypothesis words — and keep the Premise unchanged.

Pick ONE target label. Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON (exactly one JSON object, one rewrite):
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
```json
{
    "rewritten": "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh\nHypothesis: they're sometimes shown at the dollar movie theater after they come out",
    "new_prediction": "entailment"
}
```
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
The text was classified as: contradiction

Text: "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["show", "dollar", "never"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `show`(1), `dollar`(2), `never`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.4444 | 0.2105 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.1333 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2454 |

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
- **ECS (full):** 0.3929
- **ECS (extraction–rationale):** 0.3929
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 1 | **CC4 size:** 1

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
{"salience": [["Nokia", 8], ["announces", 7], ["Near", 9], ["Field", 9], ["Communication", 9], ["products", 6], ["With", 5], ["the", 4], ["Nokia", 8], ["NFC", 10], ["Near", 9], ["Field", 9], ["Communication", 9], ["shell", 6], ["on", 4], ["their", 4], ["phone,", 6], ["consumers", 7], ["will", 5], ["be", 4], ["able", 5], ["to", 4], ["access", 7], ["a", 3], ["variety", 6], ["of", 4], ["services", 7], ["and", 4], ["exchange", 7], ["information", 8], ["with", 5], ["a", 3], ["simple", 6], ["touch", 7], ["gesture.", 6]]}
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
{"rationale": "The text discusses Nokia's announcement of new technology products related to Near Field Communication, which falls under the Sci/Tech category."}
```

**Rationale text:**
> The text discusses Nokia's announcement of new technology products related to Near Field Communication, which falls under the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `nokia`, `product`

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
{"rewritten": "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers in various countries will be able to access a variety of services and exchange information with a simple touch gesture, boosting global connectivity and trade.", "new_prediction": "World"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

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
| H–R | 0.8000 | 0.5000 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.2222 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2857 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1382 |

### ag_news_test_001223 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{
  "label": "Business"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 36 words
- **Raw response length:** 25 chars
- **Prompt hash:** `9d013e566f583003`
- **ECS (full):** 0.4500
- **ECS (extraction–rationale):** 0.4500
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Nikkei", 9],
    ["hits", 8],
    ["5-week", 7],
    ["closing", 7],
    ["high", 7],
    ["on", 3],
    ["upbeat", 8],
    ["capital", 9],
    ["spending", 9],
    ["data", 7],
    ["TOKYO", 6],
    ["-", 1],
    ["Japan", 8],
    ["'s", 3],
    ["benchmark", 8],
    ["Nikkei", 9],
    ["stock", 8],
    ["index", 8],
    ["hit", 8],
    ["a", 3],
    ["five-week", 7],
    ["closing", 7],
    ["high", 7],
    ["Monday", 5],
    ["on", 3],
    ["upbeat", 8],
    ["capital", 9],
    ["spending", 9],
    ["figures", 8],
    ["for", 5],
    ["the", 4],
    ["April-June", 6],
    ["quarter", 7],
    ["by", 5],
    ["Japanese", 7],
    ["companies", 8]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `benchmark`, `capital`, `company`, `figure`, `hit`, `nikkei`, `spend`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text discusses the performance of Japan's Nikkei stock index and capital spending by companies, which are economic and financial indicators relevant to the business sector."
}
```

**Rationale text:**
> The text discusses the performance of Japan's Nikkei stock index and capital spending by companies, which are economic and financial indicators relevant to the business sector.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capital`, `company`, `index`, `japan`, `nikkei`, `spend`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{
  "rewritten": "Global markets react to Nikkei's 5-week high driven by Japan's capital spending surge TOKYO - Global financial markets are closely watching as Japan's benchmark Nikkei stock index hit a five-week closing high Monday, driven by upbeat capital spending figures for the April-June quarter by Japanese companies.",
  "new_prediction": "World"
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
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "Nikkei",
    "spending",
    "companies",
    "capital",
    "high"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nikkei`(1), `spend`(2), `company`(3), `capital`(4), `high`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5714 | 0.4000 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.8000 | 0.5000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |
| RBO (H,RO) | 0.2759 |

### ag_news_test_003283 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{
  "label": "Sports"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 45 words
- **Raw response length:** 23 chars
- **Prompt hash:** `6b8688d9df4228aa`
- **ECS (full):** 0.1944
- **ECS (extraction–rationale):** 0.1944
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Ailton", 9],
    ["Weighs", 7],
    ["Rising", 6],
    ["Sun", 6],
    ["Offer", 8],
    ["Schalke", 8],
    ["04", 6],
    ["striker", 8],
    ["Ailton", 9],
    ["has", 5],
    ["revealed", 7],
    ["that", 5],
    ["he", 4],
    ["has", 5],
    ["a", 3],
    ["big", 6],
    ["bucks", 6],
    ["contract", 8],
    ["waiting", 7],
    ["for", 5],
    ["him", 5],
    ["in", 4],
    ["Japan.", 8],
    ["(My", 5],
    ["agent)", 6],
    ["put", 6],
    ["a", 3],
    ["concrete", 7],
    ["offer", 8],
    ["from", 6],
    ["Japan", 8],
    ["in", 4],
    ["front", 6],
    ["of", 4],
    ["me,", 5],
    ["\"", 3],
    ["the", 4],
    ["reigning", 7],
    ["German", 8],
    ["Footballer", 9],
    ["of", 4],
    ["the", 4],
    ["Year", 7],
    ["told", 6],
    ["SportBild.", 8]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ailton`, `contract`, `footballer`, `german`, `japan`, `offer`, `schalke`, `sportbild`, `striker`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

In one sentence, explain why the text was classified as Sports.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text discusses a football player's contract offer, which is a sports-related topic."
}
```

**Rationale text:**
> The text discusses a football player's contract offer, which is a sports-related topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `contract`, `offer`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Edit the text so that it is classified as "World" or "Business" or "Sci/Tech" instead of "Sports". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{
  "rewritten": "Ailton Weighs Rising Sun Offer: Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, \" the reigning German Footballer of the Year told SportBild. This move could significantly impact the global football market and player transfer dynamics.",
  "new_prediction": "World"
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
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "striker",
    "contract",
    "Japan",
    "Footballer",
    "revealed"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `striker`(1), `contract`(2), `japan`(3), `footballer`(4), `reveal`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2222 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.4000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.1667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | -0.6667 |
| Normalized τ | 0.1667 |
| RBO (H,RO) | 0.1922 |

### ag_news_test_002300 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `Business` ✗
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 20 chars
- **Prompt hash:** `35784201bb6c9372`
- **ECS (full):** 0.2364
- **ECS (extraction–rationale):** 0.2364
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Job-Loss", 9], ["Panic", 8], ["Rises", 7], ["in", 3], ["Western", 6], ["Europe", 6], ["Stephane", 5], ["Zervos", 5], ["first", 4], ["suspected", 7], ["his", 3], ["job", 9], ["was", 4], ["threatened", 8], ["when", 5], ["his", 3], ["bosses", 7], ["removed", 8], ["most", 5], ["of", 2], ["the", 3], ["heavy", 6], ["equipment", 7], ["from", 4], ["the", 3], ["car", 6], ["wheel", 6], ["factory", 7], ["where", 5], ["he'd", 4], ["worked", 7], ["for", 3], ["24", 4], ["years", 5]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bos`, `equipment`, `job`, `job-loss`, `panic`, `remove`, `threaten`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses job-loss panic in the context of a car wheel factory, which relates to employment and economic concerns, thus falling under the Business category."}
```

**Rationale text:**
> The text discusses job-loss panic in the context of a car wheel factory, which relates to employment and economic concerns, thus falling under the Business category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `car`, `factory`, `job`, `job-loss`, `loss`, `panic`, `wheel`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
For "World":
{"rewritten": "Job-Loss Panic Rises in Western Europe: A Global Concern. Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years, highlighting the growing issue of job insecurity across the continent.", "new_prediction": "World"}

For "Sports":
{"rewritten": "Job-Loss Panic Rises in Western Europe: Stephane Zervos, a veteran sports equipment factory worker, first suspected his job was threatened when his bosses removed most of the heavy equipment from the facility where he'd worked for 24 years, sparking concerns within the sports industry.", "new_prediction": "Sports"}

For "Sci/Tech":
{"rewritten": "Job-Loss Panic Rises in Western Europe: Stephane Zervos first suspected his job was threatened when his bosses removed most of the advanced robotics and automation equipment from the car wheel factory where he'd worked for 24 years, raising concerns about the impact of technological advancements on employment.", "new_prediction": "Sci/Tech"}
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
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Job-Loss", "Europe", "factory", "equipment", "suspected"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `job-loss`(1), `europe`(2), `factory`(3), `equipment`(4), `suspect`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.4286 | 0.2727 |
| H–CF | — | — |
| H–RO | 0.4000 | 0.2000 |
| R–CF | — | — |
| R–RO | 0.4000 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1284 |

### ag_news_test_000981 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

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
- **Input length:** 26 words
- **Raw response length:** 20 chars
- **Prompt hash:** `738fa585e9337bf6`
- **ECS (full):** 0.6250
- **ECS (extraction–rationale):** 0.6250
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Spammers", 9], ["use", 7], ["sender", 8], ["authentication", 9], ["too,", 5], ["study", 7], ["says", 6], ["The", 4], ["technology", 9], ["hasn't", 7], ["been", 7], ["widely", 7], ["adopted,", 7], ["but", 6], ["spammers", 9], ["are", 6], ["taking", 7], ["it", 5], ["up", 6], ["at", 5], ["a", 4], ["faster", 8], ["rate", 8], ["than", 7], ["legitimate", 8], ["e-mailers.", 8]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `e-mailers`, `fast`, `spammer`, `technology`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses a technology-related issue involving spammers and sender authentication, which falls under the Sci/Tech category."}
```

**Rationale text:**
> The text discusses a technology-related issue involving spammers and sender authentication, which falls under the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `sender`, `spammer`, `technology`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Global spam rates rise as sender authentication is adopted, study says. The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers.", "new_prediction": "World"}
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

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["spammers", "authentication", "technology"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `spammer`(1), `authentication`(2), `technology`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.5000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.7500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2650 |

### ag_news_test_003796 — nova-pro

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{
  "label": "Sci/Tech"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 39 words
- **Raw response length:** 25 chars
- **Prompt hash:** `d0f694ea81775b10`
- **ECS (full):** 0.6944
- **ECS (extraction–rationale):** 0.6944
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 5 | **CC4 size:** 5

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Diesels,", 8],
    ["Hybrids", 9],
    ["Fated", 6],
    ["to", 3],
    ["Wed", 6],
    ["Two", 5],
    ["leading", 7],
    ["technologies", 9],
    ["used", 6],
    ["in", 3],
    ["fuel-efficient", 8],
    ["vehicles", 8],
    ["seem", 5],
    ["destined", 7],
    ["to", 3],
    ["unite.", 6],
    ["Industry", 7],
    ["experts", 6],
    ["say", 5],
    ["joining", 8],
    ["hybrid", 9],
    ["motors", 7],
    ["with", 5],
    ["diesel", 9],
    ["engines", 8],
    ["would", 6],
    ["result", 7],
    ["in", 3],
    ["the", 4],
    ["greenest", 8],
    ["mainstream", 7],
    ["vehicles", 8],
    ["ever,", 5],
    ["and", 3],
    ["the", 4],
    ["initial", 6],
    ["tests", 7],
    ["are", 4],
    ["promising.", 7]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `diesel`, `engine`, `fuel-efficient`, `green`, `hybrid`, `join`, `technology`, `vehicle`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text discusses the technological advancements and innovations in vehicle technology, specifically the combination of diesel engines and hybrid motors, which falls under the Sci/Tech category."
}
```

**Rationale text:**
> The text discusses the technological advancements and innovations in vehicle technology, specifically the combination of diesel engines and hybrid motors, which falls under the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `diesel`, `engine`, `hybrid`, `motor`, `technology`, `vehicle`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{
  "rewritten": "Global Automakers Eye Greener Future with Diesel-Hybrid Fusion: Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising. This move is expected to significantly impact global emissions standards and the competitive landscape of the automotive industry.",
  "new_prediction": "World"
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
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "technologies",
    "vehicles",
    "engines",
    "hybrid",
    "diesel"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `technology`(1), `vehicle`(2), `engine`(3), `hybrid`(4), `diesel`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8333 | 0.5556 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6250 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.8333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | -0.6000 |
| Normalized τ | 0.2000 |
| RBO (H,RO) | 0.2338 |

### ag_news_test_002873 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{
  "label": "Business"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 25 chars
- **Prompt hash:** `1d2b82039e416b33`
- **ECS (full):** 0.3750
- **ECS (extraction–rationale):** 0.3750
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["August", 8],
    ["chip", 9],
    ["sales", 9],
    ["up", 6],
    ["Global", 7],
    ["semiconductor", 9],
    ["sales", 9],
    ["rose", 8],
    ["1.1", 7],
    ["percent", 7],
    ["to", 5],
    ["$18.2", 8],
    ["billion", 8],
    ["in", 5],
    ["August", 8],
    ["from", 6],
    ["the", 5],
    ["previous", 6],
    ["month", 6],
    ["and", 5],
    ["it", 5],
    ["appears", 7],
    ["as", 5],
    ["though", 7],
    ["chip", 9],
    ["inventories", 9],
    ["are", 6],
    ["declining,", 8],
    ["an", 5],
    ["industry", 7],
    ["trade", 7],
    ["group", 7],
    ["said", 7],
    ["Thursday.", 7]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `18.2`, `august`, `billion`, `chip`, `inventory`, `sale`, `semiconductor`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text discusses global semiconductor sales figures and trends in chip inventories, which are directly related to economic and business activities."
}
```

**Rationale text:**
> The text discusses global semiconductor sales figures and trends in chip inventories, which are directly related to economic and business activities.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `chip`, `global`, `inventory`, `sale`, `semiconductor`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{
  "rewritten": "Global semiconductor industry impacts world economy as August chip sales rise, signaling potential market shifts.",
  "new_prediction": "World"
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
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "sales",
    "billion",
    "semiconductor",
    "percent",
    "August"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sale`(1), `billion`(2), `semiconductor`(3), `percent`(4), `august`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.5000 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.4000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.1496 |

### ag_news_test_002291 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{
  "label": "Sci/Tech"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 25 chars
- **Prompt hash:** `7dfaf34897560923`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Briefly:", 1],
    ["T-Mobile", 8],
    ["sells", 6],
    ["Sidekick", 7],
    ["II", 5],
    ["roundup", 6],
    ["Plus:", 1],
    ["Spyware", 9],
    ["bill", 7],
    ["moves", 6],
    ["to", 2],
    ["Senate...", 8],
    ["Supercomputer", 9],
    ["center", 7],
    ["gets", 6],
    ["new", 5],
    ["No.", 4],
    ["2...", 3],
    ["MIT,", 8],
    ["Caltech", 8],
    ["offer", 7],
    ["low-tech", 7],
    ["voting", 6],
    ["advice.", 6]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `caltech`, `mit`, `spyware`, `supercomputer`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text discusses technology-related topics such as a mobile device sale, spyware legislation, supercomputer updates, and technical advice from prestigious institutions."
}
```

**Rationale text:**
> The text discusses technology-related topics such as a mobile device sale, spyware legislation, supercomputer updates, and technical advice from prestigious institutions.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `advice`, `mobile`, `spyware`, `supercomputer`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{
  "rewritten": "Briefly: T-Mobile sells Sidekick II roundup Plus: New trade agreement moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice.",
  "new_prediction": "Business"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["Supercomputer", "Spyware", "Sidekick", "Senate", "sells"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `supercomputer`(1), `spyware`(2), `sidekick`(3), `senate`(4), `sell`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.3333 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.3333 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2067 |

### ag_news_test_003454 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{
  "label": "World"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 22 chars
- **Prompt hash:** `3c62430b0a572f70`
- **ECS (full):** 0.6389
- **ECS (extraction–rationale):** 0.6389
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["For", 3],
    ["the", 3],
    ["First", 5],
    ["Time,", 5],
    ["an", 3],
    ["African", 8],
    ["Woman", 7],
    ["Wins", 8],
    ["the", 3],
    ["Nobel", 8],
    ["Peace", 7],
    ["Prize", 8],
    ["Wangari", 9],
    ["Maathai,", 9],
    ["a", 3],
    ["Kenyan", 8],
    ["who", 5],
    ["has", 5],
    ["worked", 6],
    ["tirelessly", 6],
    ["to", 4],
    ["protect", 7],
    ["the", 3],
    ["environment,", 7],
    ["improve", 7],
    ["the", 3],
    ["lives", 6],
    ["of", 4],
    ["women,", 7],
    ["and", 4],
    ["fight", 7],
    ["crime,", 6],
    ["Friday", 5],
    ["became", 7]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `african`, `kenyan`, `maathai`, `nobel`, `prize`, `wangari`, `win`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

In one sentence, explain why the text was classified as World.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The text discusses a significant global event involving an African woman winning the Nobel Peace Prize, which is a matter of international importance."
}
```

**Rationale text:**
> The text discusses a significant global event involving an African woman winning the Nobel Peace Prize, which is a matter of international importance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `african`, `nobel`, `peace`, `prize`, `win`, `woman`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Edit the text so that it is classified as "Sports" or "Business" or "Sci/Tech" instead of "World". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{
  "rewritten": "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to develop a groundbreaking environmental technology, improve the lives of women through entrepreneurship, and fight corporate crime, Friday became",
  "new_prediction": "Sci/Tech"
}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `World`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": [
    "African",
    "Woman",
    "Wins",
    "Nobel",
    "Prize"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `african`(1), `woman`(2), `win`(3), `nobel`(4), `prize`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.4444 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.5000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.8333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.1314 |

### ag_news_test_000788 — nova-pro

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1abb997e9f1de140`
- **ECS (full):** 0.4033
- **ECS (extraction–rationale):** 0.4833
- **ECS (extraction–perturbation):** 0.3250
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["GOP", 8], ["Jamboree", 7], ["Could", 6], ["Briefly", 7], ["Lift", 8], ["Stocks", 9], ["NEW", 3], ["YORK", 3], ["(Reuters)", 4], ["-", 1], ["Fasten", 5], ["your", 4], ["seatbelts.", 5], ["The", 6], ["Republicans", 8], ["are", 4], ["coming", 6], ["to", 3], ["town.", 5], ["If", 5], ["things", 6], ["go", 5], ["smoothly", 7], ["at", 4], ["the", 5], ["Republican", 8], ["National", 7], ["Convention,", 7], ["the", 5], ["stock", 8], ["market", 8], ["could", 7], ["get", 6], ["a", 3], ["brief", 7], ["boost", 8], ["next", 6], ["week,", 5], ["experts", 7], ["say.", 5]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `boost`, `brief`, `briefly`, `gop`, `lift`, `market`, `republican`, `stock`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses the potential impact of the Republican National Convention on the stock market, which is a business-related topic."}
```

**Rationale text:**
> The text discusses the potential impact of the Republican National Convention on the stock market, which is a business-related topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `convention`, `market`, `national`, `republican`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "GOP Jamboree Could Briefly Lift Global Markets NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, global markets could get a brief boost next week, experts say.", "new_prediction": "World"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `World`

**Reconstructed text:**
> GOP Jamboree Could Briefly Lift Global Tensions NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, global tensions could get a brief boost next week, experts say.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `market`, `stock`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["stocks", "market", "boost", "Republican", "Convention"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `stock`(1), `market`(2), `boost`(3), `republican`(4), `convention`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6000 | 0.3000 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | 0.8000 | 0.4444 |
| R–CF | 1.0000 | 0.4000 |
| R–RO | 0.8000 | 0.6667 |
| CF–RO | 1.0000 | 0.4000 |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3685 |

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
{"salience": [["Nokia", 8], ["announces", 6], ["Near", 10], ["Field", 10], ["Communication", 10], ["products", 7], ["With", 3], ["the", 1], ["Nokia", 8], ["NFC", 10], ["(Near", 10], ["Field", 10], ["Communication)", 10], ["shell", 6], ["on", 2], ["their", 1], ["phone", 8], [",", 1], ["consumers", 5], ["will", 2], ["be", 1], ["able", 4], ["to", 1], ["access", 6], ["a", 1], ["variety", 4], ["of", 1], ["services", 7], ["and", 3], ["exchange", 6], ["information", 7], ["with", 2], ["a", 1], ["simple", 5], ["touch", 7], ["gesture", 6], [".", 1]]}
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

### ag_news_test_001223 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 36 words
- **Raw response length:** 20 chars
- **Prompt hash:** `9d013e566f583003`
- **ECS (full):** 0.5143
- **ECS (extraction–rationale):** 0.5143
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Nikkei", 10], ["hits", 6], ["5-week", 8], ["closing", 8], ["high", 8], ["on", 3], ["upbeat", 9], ["capital", 10], ["spending", 10], ["data", 9], ["TOKYO", 5], ["-", 2], ["Japan", 7], ["'s", 2], ["benchmark", 7], ["Nikkei", 10], ["stock", 9], ["index", 9], ["hit", 6], ["a", 1], ["five-week", 8], ["closing", 8], ["high", 8], ["Monday", 4], ["on", 3], ["upbeat", 9], ["capital", 10], ["spending", 10], ["figures", 8], ["for", 2], ["the", 1], ["April-June", 7], ["quarter", 7], ["by", 2], ["Japanese", 6], ["companies", 7], ["." , 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capital`, `data`, `index`, `nikkei`, `spend`, `stock`, `upbeat`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses stock market performance and corporate capital spending data, which are key indicators in the business and financial sector."}
```

**Rationale text:**
> The text discusses stock market performance and corporate capital spending data, which are key indicators in the business and financial sector.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capital`, `spend`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Japan's Nikkei stadium hosts record-breaking marathon event TOKYO - A new national record was set Monday at the Nikkei stadium during a major international marathon, drawing athletes from over 50 countries.", "new_prediction": "Sports"}
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
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nikkei", "capital", "spending", "index", "stock"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nikkei`(1), `capital`(2), `spend`(3), `index`(4), `stock`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.4286 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.7143 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.8000 |
| Normalized τ | 0.9000 |
| RBO (H,RO) | 0.3653 |

### ag_news_test_003283 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sports"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 45 words
- **Raw response length:** 18 chars
- **Prompt hash:** `6b8688d9df4228aa`
- **ECS (full):** 0.2667
- **ECS (extraction–rationale):** 0.2667
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Ailton", 10], ["Weighs", 6], ["Rising", 3], ["Sun", 2], ["Offer", 8], ["Schalke", 10], ["04", 10], ["striker", 9], ["Ailton", 10], ["has", 2], ["revealed", 5], ["that", 1], ["he", 1], ["has", 2], ["a", 1], ["big", 3], ["bucks", 6], ["contract", 7], ["waiting", 4], ["for", 1], ["him", 1], ["in", 1], ["Japan", 5], ["(", 1], ["My", 1], ["agent", 6], [")", 1], ["put", 3], ["a", 1], ["concrete", 5], ["offer", 8], ["from", 2], ["Japan", 5], ["in", 1], ["front", 2], ["of", 1], ["me", 1], [",", 1], ["\"", 1], ["the", 1], ["reigning", 7], ["German", 8], ["Footballer", 10], ["of", 1], ["the", 1], ["Year", 9], ["told", 4], ["SportBild", 9], ["\"", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `04`, `ailton`, `footballer`, `german`, `offer`, `schalke`, `sportbild`, `striker`, `year`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

In one sentence, explain why the text was classified as Sports.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses a professional footballer considering a contract offer from a Japanese club, which is directly related to sports."}
```

**Rationale text:**
> The text discusses a professional footballer considering a contract offer from a Japanese club, which is directly related to sports.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `contract`, `footballer`, `offer`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Edit the text so that it is classified as "World" or "Business" or "Sci/Tech" instead of "Sports". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Ailton Considers Lucrative Business Venture in Japan; Schalke 04 striker revealed a major financial opportunity awaiting him abroad. 'My agent presented a concrete offer from Japan,' the reigning German Footballer of the Year told SportBild.", "new_prediction": "Business"}
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
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Ailton", "striker", "Footballer", "contract", "Japan"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ailton`(1), `striker`(2), `footballer`(3), `contract`(4), `japan`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.2000 |
| H–CF | — | — |
| H–RO | 0.6000 | 0.2727 |
| R–CF | — | — |
| R–RO | 0.6667 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2463 |

### ag_news_test_002300 — qwen3-235b

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `Business` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 20 chars
- **Prompt hash:** `35784201bb6c9372`
- **ECS (full):** 0.2611
- **ECS (extraction–rationale):** 0.2611
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Job-Loss", 10], ["Panic", 8], ["Rises", 7], ["in", 2], ["Western", 5], ["Europe", 6], ["Stephane", 3], ["Zervos", 3], ["first", 2], ["suspected", 7], ["his", 2], ["job", 9], ["was", 2], ["threatened", 9], ["when", 2], ["his", 2], ["bosses", 8], ["removed", 8], ["most", 3], ["of", 1], ["the", 1], ["heavy", 6], ["equipment", 8], ["from", 2], ["the", 1], ["car", 6], ["wheel", 5], ["factory", 8], ["where", 2], ["he'd", 2], ["worked", 8], ["for", 2], ["24", 3], ["years", 4]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bos`, `equipment`, `factory`, `job`, `job-loss`, `panic`, `threaten`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article discusses job losses and factory equipment removal in a car wheel manufacturing plant, which relates to economic activity and labor market concerns in the business sector."}
```

**Rationale text:**
> The article discusses job losses and factory equipment removal in a car wheel manufacturing plant, which relates to economic activity and labor market concerns in the business sector.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `car`, `equipment`, `factory`, `job`, `loss`, `wheel`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Job-Loss Panic Rises in Western Europe as Climate Protests Disrupt Transport Networks", "new_prediction": "World"}
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
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Job-Loss", "factory", "bosses", "work", "equipment"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `job-loss`(1), `factory`(2), `bos`(3), `work`(4), `equipment`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.3000 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.4000 | 0.2222 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.3176 |

### ag_news_test_000981 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

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
- **Input length:** 26 words
- **Raw response length:** 20 chars
- **Prompt hash:** `738fa585e9337bf6`
- **ECS (full):** 0.6000
- **ECS (extraction–rationale):** 0.6000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Spammers", 9], ["use", 5], ["sender", 8], ["authentication", 10], ["too", 4], ["study", 7], ["says", 3], ["The", 1], ["technology", 9], ["hasn't", 2], ["been", 1], ["widely", 6], ["adopted", 7], ["but", 2], ["spammers", 9], ["are", 1], ["taking", 4], ["it", 3], ["up", 3], ["at", 1], ["a", 1], ["faster", 6], ["rate", 5], ["than", 2], ["legitimate", 7], ["e-mailers", 8]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `e-mailers`, `sender`, `spammer`, `technology`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses sender authentication technology and its adoption by spammers, which pertains to cybersecurity and email technology, falling under the Sci/Tech category."}
```

**Rationale text:**
> The text discusses sender authentication technology and its adoption by spammers, which pertains to cybersecurity and email technology, falling under the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `spammer`, `technology`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Spammers use sender authentication too, study says. The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers, posing new challenges for global businesses.", "new_prediction": "Business"}
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

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Spammers", "sender", "authentication", "technology", "e-mailers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `spammer`(1), `sender`(2), `authentication`(3), `technology`(4), `e-mailers`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6000 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.6000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.2000 |
| Normalized τ | 0.6000 |
| RBO (H,RO) | 0.2193 |

### ag_news_test_003796 — qwen3-235b

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 39 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d0f694ea81775b10`
- **ECS (full):** 0.3773
- **ECS (extraction–rationale):** 0.3773
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Diesels", 9], ["Hybrids", 9], ["Fated", 4], ["to", 2], ["Wed", 6], ["Two", 3], ["leading", 6], ["technologies", 10], ["used", 5], ["in", 2], ["fuel-efficient", 10], ["vehicles", 8], ["seem", 3], ["destined", 5], ["to", 2], ["unite", 7], ["Industry", 6], ["experts", 7], ["say", 2], ["joining", 7], ["hybrid", 9], ["motors", 7], ["with", 2], ["diesel", 8], ["engines", 8], ["would", 3], ["result", 6], ["in", 2], ["the", 2], ["greenest", 9], ["mainstream", 5], ["vehicles", 7], ["ever", 4], ["and", 2], ["the", 2], ["initial", 5], ["tests", 7], ["are", 2], ["promising", 8]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `diesel`, `engine`, `fuel-efficient`, `green`, `hybrid`, `promise`, `technology`, `vehicle`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article discusses the technological integration of diesel engines and hybrid motors to create more fuel-efficient vehicles, which falls under scientific and technological advancements in automotive engineering."}
```

**Rationale text:**
> The article discusses the technological integration of diesel engines and hybrid motors to create more fuel-efficient vehicles, which falls under scientific and technological advancements in automotive engineering.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `diesel`, `efficient`, `engine`, `fuel`, `fuel-efficient`, `hybrid`, `motor`, `vehicle`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising, boosting investments and market competition among automakers.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Hybrids", "Diesels", "technologies", "vehicles", "greenest"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hybrid`(1), `diesel`(2), `technology`(3), `vehicle`(4), `green`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6250 | 0.4545 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6250 |
| R–CF | — | — |
| R–RO | 0.6000 | 0.3000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |
| RBO (H,RO) | 0.2426 |

### ag_news_test_002873 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1d2b82039e416b33`
- **ECS (full):** 0.1300
- **ECS (extraction–rationale):** 0.3250
- **ECS (extraction–perturbation):** 0.0000
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["August", 5], ["chip", 9], ["sales", 10], ["up", 6], ["Global", 5], ["semiconductor", 9], ["sales", 10], ["rose", 7], ["1.1", 6], ["percent", 6], ["to", 4], ["$18.2", 8], ["billion", 7], ["in", 3], ["August", 5], ["from", 3], ["the", 1], ["previous", 5], ["month", 5], ["and", 2], ["it", 1], ["appears", 4], ["as", 2], ["though", 3], ["chip", 9], ["inventories", 8], ["are", 1], ["declining", 7], ["an", 1], ["industry", 7], ["trade", 6], ["group", 5], ["said", 4], ["Thursday", 3]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `18.2`, `billion`, `chip`, `decline`, `inventory`, `sale`, `semiconductor`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text reports on global semiconductor sales figures and market trends, which are key indicators of economic activity in the technology sector, making it relevant to the Business category."}
```

**Rationale text:**
> The text reports on global semiconductor sales figures and market trends, which are key indicators of economic activity in the technology sector, making it relevant to the Business category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `global`, `sale`, `semiconductor`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday, highlighting advancements in semiconductor technology.", "new_prediction": "Sci/Tech"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Sci/Tech`

**Reconstructed text:**
> August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday, highlighting advancements in semiconductor technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `thursday`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["sales", "semiconductor", "billion", "chip"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sale`(1), `semiconductor`(2), `billion`(3), `chip`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.2500 |
| H–CF | 0.0000 | 0.0000 |
| H–RO | 1.0000 | 0.5714 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.6667 | 0.4000 |
| CF–RO | 0.0000 | 0.0000 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.3628 |

### ag_news_test_002291 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

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
- **Input length:** 22 words
- **Raw response length:** 20 chars
- **Prompt hash:** `7dfaf34897560923`
- **ECS (full):** 0.2500
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Briefly:", 3], ["T-Mobile", 7], ["sells", 4], ["Sidekick", 9], ["II", 6], ["roundup", 3], ["Plus:", 2], ["Spyware", 9], ["bill", 5], ["moves", 2], ["to", 1], ["Senate", 6], ["Supercomputer", 10], ["center", 6], ["gets", 2], ["new", 3], ["No.", 4], ["2", 4], ["MIT", 9], ["Caltech", 9], ["offer", 3], ["low-tech", 8], ["voting", 6], ["advice", 5]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `caltech`, `mit`, `sidekick`, `supercomputer`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as Sci/Tech because it covers technology-related topics such as mobile device sales, spyware legislation, supercomputing, and technical voting recommendations from MIT and Caltech."}
```

**Rationale text:**
> The text was classified as Sci/Tech because it covers technology-related topics such as mobile device sales, spyware legislation, supercomputing, and technical voting recommendations from MIT and Caltech.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `caltech`, `mit`, `mobile`, `spyware`, `tech`, `vote`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Briefly: T-Mobile sells Sidekick II in global markets amid rising demand...Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Sidekick", "Supercomputer", "MIT", "Caltech", "Spyware"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sidekick`(1), `supercomputer`(2), `mit`(3), `caltech`(4), `spyware`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.2500 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | -0.3333 |
| Normalized τ | 0.3333 |
| RBO (H,RO) | 0.2244 |

### ag_news_test_003454 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"World"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 17 chars
- **Prompt hash:** `3c62430b0a572f70`
- **ECS (full):** 0.5833
- **ECS (extraction–rationale):** 0.5833
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["For", 3], ["the", 2], ["First", 6], ["Time", 5], [",", 2], ["an", 2], ["African", 9], ["Woman", 8], ["Wins", 7], ["the", 2], ["Nobel", 10], ["Peace", 10], ["Prize", 9], ["Wangari", 8], ["Maathai", 9], [",", 2], ["a", 2], ["Kenyan", 8], ["who", 2], ["has", 2], ["worked", 4], ["tirelessly", 5], ["to", 2], ["protect", 5], ["the", 2], ["environment", 6], [",", 2], ["improve", 4], ["the", 2], ["lives", 5], ["of", 2], ["women", 7], [",", 2], ["and", 2], ["fight", 5], ["crime", 4], [",", 2], ["Friday", 4], ["became", 3]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `african`, `kenyan`, `maathai`, `nobel`, `peace`, `prize`, `wangari`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

In one sentence, explain why the text was classified as World.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as World because it reports on a significant international event—the Nobel Peace Prize being awarded to an African woman for her global impact on environmental and social issues."}
```

**Rationale text:**
> The text was classified as World because it reports on a significant international event—the Nobel Peace Prize being awarded to an African woman for her global impact on environmental and social issues.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `african`, `nobel`, `peace`, `prize`, `woman`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Edit the text so that it is classified as "Sports" or "Business" or "Sci/Tech" instead of "World". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "For the First Time, an African Woman Wins the Nobel Prize in Economics Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `World`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nobel", "Peace", "African", "Woman", "World"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nobel`(1), `peace`(2), `african`(3), `woman`(4), `kenyan`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.5000 |
| H–CF | — | — |
| H–RO | 0.8000 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.8000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |
| RBO (H,RO) | 0.4348 |

### ag_news_test_000788 — qwen3-235b

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.98
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1abb997e9f1de140`
- **ECS (full):** 0.5556
- **ECS (extraction–rationale):** 0.5556
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["GOP", 9], ["Jamboree", 6], ["Could", 4], ["Briefly", 5], ["Lift", 8], ["Stocks", 10], ["NEW", 2], ["YORK", 1], ["(Reuters)", 1], ["Fasten", 2], ["your", 1], ["seatbelts", 2], [".", 1], ["The", 1], ["Republicans", 7], ["are", 1], ["coming", 3], ["to", 1], ["town", 3], [".", 1], ["If", 2], ["things", 1], ["go", 2], ["smoothly", 5], ["at", 1], ["the", 1], ["Republican", 7], ["National", 6], ["Convention", 8], [",", 1], ["the", 1], ["stock", 9], ["market", 9], ["could", 4], ["get", 3], ["a", 1], ["brief", 5], ["boost", 8], ["next", 2], ["week", 4], [",", 1], ["experts", 5], ["say", 3], ["." ,1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `boost`, `convention`, `gop`, `jamboree`, `lift`, `market`, `republican`, `stock`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses the potential impact of the Republican National Convention on the stock market, which is a topic related to financial markets and economic activity."}
```

**Rationale text:**
> The text discusses the potential impact of the Republican National Convention on the stock market, which is a topic related to financial markets and economic activity.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `convention`, `market`, `national`, `republican`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "GOP Jamboree Draws Global Attention as World Leaders Monitor U.S. Political Shift NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, international markets and diplomats could see ripple effects, experts say.", "new_prediction": "World"}
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
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Stocks", "market", "boost", "Republican", "Convention"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `stock`(1), `market`(2), `boost`(3), `republican`(4), `convention`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.4444 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6250 |
| R–CF | — | — |
| R–RO | 0.8000 | 0.6667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.8000 |
| Normalized τ | 0.9000 |
| RBO (H,RO) | 0.4134 |

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
- **ECS (full):** 0.2286
- **ECS (extraction–rationale):** 0.2083
- **ECS (extraction–perturbation):** 0.1964
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Business`
- **CC3 size:** 1 | **CC4 size:** 1

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
{"salience": [["Nokia", 8], ["announces", 7], ["Near", 10], ["Field", 10], ["Communication", 10], ["products", 8], ["With", 2], ["the", 1], ["Nokia", 8], ["NFC", 10], ["(", 1], ["Near", 10], ["Field", 10], ["Communication", 10], [")", 1], ["shell", 6], ["on", 1], ["their", 1], ["phone", 7], [",", 1], ["consumers", 3], ["will", 2], ["be", 1], ["able", 2], ["to", 1], ["access", 4], ["a", 1], ["variety", 2], ["of", 1], ["services", 4], ["and", 1], ["exchange", 5], ["information", 5], ["with", 1], ["a", 1], ["simple", 2], ["touch", 3], ["gesture", 3], [".", 1]]}
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
{"rationale": "The text describes a new technological product (NFC shell) from a company, focusing on its innovative features and capabilities, which falls under science and technology."}
```

**Rationale text:**
> The text describes a new technological product (NFC shell) from a company, focusing on its innovative features and capabilities, which falls under science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`, `product`, `shell`

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
{"rewritten": "Nokia announces Near Field Communication products. The company's stock rose 5% on the news. With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Business`

**Reconstructed text:**
> Nokia announces Near Field Communication products. The company's stock rose 5% on the news. With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `product`

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
{"ranking": ["Nokia", "Communication", "products", "phone"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nokia`(1), `communication`(2), `product`(3), `phone`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.2500 |
| H–CF | 1.0000 | 0.1429 |
| H–RO | 0.7500 | 0.3750 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 0.3333 | 0.1667 |
| CF–RO | 1.0000 | 0.2500 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1688 |

### ag_news_test_001223 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.99
- **Model refused:** No
- **Input length:** 36 words
- **Raw response length:** 20 chars
- **Prompt hash:** `9d013e566f583003`
- **ECS (full):** 0.1429
- **ECS (extraction–rationale):** 0.1429
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Nikkei", 10], ["hits", 7], ["5-week", 5], ["closing", 6], ["high", 6], ["on", 1], ["upbeat", 8], ["capital", 9], ["spending", 9], ["data", 7], ["TOKYO", 3], ["-", 1], ["Japan", 4], ["'s", 1], ["benchmark", 6], ["Nikkei", 10], ["stock", 9], ["index", 8], ["hit", 7], ["a", 1], ["five-week", 5], ["closing", 6], ["high", 6], ["Monday", 4], ["on", 1], ["upbeat", 8], ["capital", 9], ["spending", 9], ["figures", 7], ["for", 1], ["the", 1], ["April-June", 4], ["quarter", 5], ["by", 1], ["Japanese", 4], ["companies", 7]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capital`, `company`, `index`, `nikkei`, `spend`, `stock`, `upbeat`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article reports on the performance of a major stock index and corporate investment data, which are core topics within the business and finance sector."}
```

**Rationale text:**
> The article reports on the performance of a major stock index and corporate investment data, which are core topics within the business and finance sector.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `index`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies, the World Bank reported.", "new_prediction": "World"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Business`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nikkei", "spending", "capital", "companies"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nikkei`(1), `spend`(2), `capital`(3), `company`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2857 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.5714 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |
| RBO (H,RO) | 0.3799 |

### ag_news_test_003283 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sports"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 45 words
- **Raw response length:** 18 chars
- **Prompt hash:** `6b8688d9df4228aa`
- **ECS (full):** 0.2497
- **ECS (extraction–rationale):** 0.2576
- **ECS (extraction–perturbation):** 0.3667
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Business`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Ailton", 7], ["Weighs", 3], ["Rising", 2], ["Sun", 2], ["Offer", 3], ["Schalke", 8], ["04", 8], ["striker", 9], ["Ailton", 7], ["has", 1], ["revealed", 1], ["that", 1], ["he", 1], ["has", 1], ["a", 1], ["big", 1], ["bucks", 1], ["contract", 4], ["waiting", 1], ["for", 1], ["him", 1], ["in", 1], ["Japan", 2], [".", 1], ["(", 1], ["My", 1], ["agent", 1], [")", 1], ["put", 1], ["a", 1], ["concrete", 1], ["offer", 3], ["from", 1], ["Japan", 2], ["in", 1], ["front", 1], ["of", 1], ["me", 1], [",", 1], ["", 1], ["the", 1], ["reigning", 6], ["German", 6], ["Footballer", 10], ["of", 1], ["the", 1], ["Year", 6], ["told", 1], ["SportBild", 8], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `04`, `ailton`, `footballer`, `german`, `reign`, `schalke`, `sportbild`, `striker`, `year`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

In one sentence, explain why the text was classified as Sports.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article focuses on a professional football (soccer) player, Ailton, discussing a contract offer related to his athletic career with Schalke 04."}
```

**Rationale text:**
> The article focuses on a professional football (soccer) player, Ailton, discussing a contract offer related to his athletic career with Schalke 04.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ailton`, `contract`, `offer`, `schalke`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Edit the text so that it is classified as "World" or "Business" or "Sci/Tech" instead of "Sports". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Ailton Weighs Rising Sun Offer Schalke 04 executive Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, \" the reigning German Businessman of the Year told a financial publication.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Business`

**Reconstructed text:**
> Ailton Weighs Rising Sun Offer Schalke 04 executive Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Businessman of the Year told a financial publication.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `footballer`, `sportbild`, `striker`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["striker", "Footballer", "contract", "Schalke"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `striker`(1), `footballer`(2), `contract`(3), `schalke`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.1818 |
| H–CF | 1.0000 | 0.3333 |
| H–RO | 0.7500 | 0.3000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.5000 | 0.3333 |
| CF–RO | 0.6667 | 0.4000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3226 |

### ag_news_test_002300 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `Business` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 20 chars
- **Prompt hash:** `35784201bb6c9372`
- **ECS (full):** 0.2250
- **ECS (extraction–rationale):** 0.2250
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Job-Loss", 10],
    ["Panic", 8],
    ["Rises", 7],
    ["in", 1],
    ["Western", 3],
    ["Europe", 3],
    ["Stephane", 1],
    ["Zervos", 1],
    ["first", 1],
    ["suspected", 2],
    ["his", 1],
    ["job", 10],
    ["was", 1],
    ["threatened", 9],
    ["when", 1],
    ["his", 1],
    ["bosses", 5],
    ["removed", 6],
    ["most", 1],
    ["of", 1],
    ["the", 1],
    ["heavy", 2],
    ["equipment", 4],
    ["from", 1],
    ["the", 1],
    ["car", 3],
    ["wheel", 3],
    ["factory", 6],
    ["where", 1],
    ["he'd", 1],
    ["worked", 4],
    ["for", 1],
    ["24", 1],
    ["years.", 1]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `factory`, `job`, `job-loss`, `panic`, `remove`, `rise`, `threaten`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article focuses on job losses and factory closures, which are core economic and employment issues falling under the Business category."}
```

**Rationale text:**
> The article focuses on job losses and factory closures, which are core economic and employment issues falling under the Business category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `factory`, `job`, `loss`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years, a situation now being monitored by the United Nations.", "new_prediction": "World"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Business`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Job-Loss Panic Rises in Western Europe Stephane Zervos first suspected his job was threatened when his bosses removed most of the heavy equipment from the car wheel factory where he'd worked for 24 years."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Job-Loss", "factory", "bosses"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `job-loss`(1), `factory`(2), `bos`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.2500 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.2500 |
| R–CF | — | — |
| R–RO | 0.3333 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1382 |

### ag_news_test_000981 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

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
- **Input length:** 26 words
- **Raw response length:** 20 chars
- **Prompt hash:** `738fa585e9337bf6`
- **ECS (full):** 0.7000
- **ECS (extraction–rationale):** 0.7000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
  "salience": [
    ["Spammers", 10],
    ["use", 3],
    ["sender", 8],
    ["authentication", 9],
    ["too,", 2],
    ["study", 7],
    ["says", 1],
    ["The", 1],
    ["technology", 9],
    ["hasn't", 1],
    ["been", 1],
    ["widely", 1],
    ["adopted,", 2],
    ["but", 1],
    ["spammers", 10],
    ["are", 1],
    ["taking", 2],
    ["it", 1],
    ["up", 1],
    ["at", 1],
    ["a", 1],
    ["faster", 2],
    ["rate", 2],
    ["than", 1],
    ["legitimate", 4],
    ["e-mailers.", 5]
  ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `sender`, `spammer`, `study`, `technology`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses the adoption of a specific email technology (sender authentication) by spammers, which is a topic related to technology and cybersecurity."}
```

**Rationale text:**
> The text discusses the adoption of a specific email technology (sender authentication) by spammers, which is a topic related to technology and cybersecurity.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `sender`, `spammer`, `technology`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers, impacting global business communications.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Spammers", "authentication", "technology", "e-mailers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `spammer`(1), `authentication`(2), `technology`(3), `e-mailers`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.8000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.5000 |
| R–CF | — | — |
| R–RO | 0.7500 | 0.6000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3650 |

### ag_news_test_003796 — deepseek-v3

> ⚠ **Wrong prediction** — included per D5 (incorrect-prediction stratum). Explanations below are elicited for the model's OWN (incorrect) label; ECS/erasure are defined relative to that prediction.

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 39 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d0f694ea81775b10`
- **ECS (full):** 0.5222
- **ECS (extraction–rationale):** 0.5222
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["Diesels", 8], [",", 1], ["Hybrids", 8], ["Fated", 2], ["to", 1], ["Wed", 2], ["Two", 1], ["leading", 3], ["technologies", 9], ["used", 3], ["in", 1], ["fuel-efficient", 7], ["vehicles", 7], ["seem", 1], ["destined", 2], ["to", 1], ["unite", 3], [".", 1], ["Industry", 4], ["experts", 5], ["say", 1], ["joining", 4], ["hybrid", 8], ["motors", 7], ["with", 1], ["diesel", 8], ["engines", 7], ["would", 1], ["result", 2], ["in", 1], ["the", 1], ["greenest", 6], ["mainstream", 4], ["vehicles", 7], ["ever", 2], [",", 1], ["and", 1], ["the", 1], ["initial", 3], ["tests", 5], ["are", 1], ["promising", 4], [".", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `diesel`, `engine`, `fuel-efficient`, `green`, `hybrid`, `motor`, `technology`, `vehicle`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article discusses the technological advancement of combining hybrid and diesel engine systems to create more fuel-efficient and environmentally friendly vehicles, which falls under science and technology."}
```

**Rationale text:**
> The article discusses the technological advancement of combining hybrid and diesel engine systems to create more fuel-efficient and environmentally friendly vehicles, which falls under science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `diesel`, `efficient`, `engine`, `fuel`, `fuel-efficient`, `hybrid`, `technology`, `vehicle`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts at a major automaker say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising for their market share.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Diesels, Hybrids Fated to Wed Two leading technologies used in fuel-efficient vehicles seem destined to unite. Industry experts say joining hybrid motors with diesel engines would result in the greenest mainstream vehicles ever, and the initial tests are promising."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Hybrids", "Diesel", "Engines", "Greenest", "Vehicles"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hybrid`(1), `diesel`(2), `engine`(3), `green`(4), `vehicle`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.6000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.6250 |
| R–CF | — | — |
| R–RO | 0.8000 | 0.4444 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 0.6000 |
| Normalized τ | 0.8000 |
| RBO (H,RO) | 0.2828 |

### ag_news_test_002873 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1d2b82039e416b33`
- **ECS (full):** 0.2771
- **ECS (extraction–rationale):** 0.3250
- **ECS (extraction–perturbation):** 0.2429
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["August", 2], ["chip", 8], ["sales", 9], ["up", 3], ["Global", 3], ["semiconductor", 9], ["sales", 9], ["rose", 7], ["1.1", 5], ["percent", 5], ["to", 1], ["$18.2", 7], ["billion", 7], ["in", 1], ["August", 2], ["from", 1], ["the", 1], ["previous", 1], ["month", 1], ["and", 1], ["it", 1], ["appears", 1], ["as", 1], ["though", 1], ["chip", 8], ["inventories", 7], ["are", 1], ["declining", 6], [",", 1], ["an", 1], ["industry", 8], ["trade", 8], ["group", 7], ["said", 1], ["Thursday", 2]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `18.2`, `billion`, `chip`, `industry`, `sale`, `semiconductor`, `trade`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text reports on financial performance and inventory trends within the semiconductor industry, which are core topics of business and economic news."}
```

**Rationale text:**
> The text reports on financial performance and inventory trends within the semiconductor industry, which are core topics of business and economic news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `industry`, `inventory`, `semiconductor`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
```json
{
    "rewritten": "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an international science and technology group said Thursday.",
    "new_prediction": "Sci/Tech"
}
```
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Sci/Tech`

**Reconstructed text:**
> August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an international science and technology group said Thursday.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `industry`, `trade`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["sales", "semiconductor", "chip", "industry"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sale`(1), `semiconductor`(2), `chip`(3), `industry`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.2500 |
| H–CF | 1.0000 | 0.2857 |
| H–RO | 1.0000 | 0.5714 |
| R–CF | 0.5000 | 0.2500 |
| R–RO | 0.6667 | 0.4000 |
| CF–RO | 0.5000 | 0.2000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |
| RBO (H,RO) | 0.4661 |

### ag_news_test_002291 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

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
- **Verbalized confidence:** 0.90
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 20 chars
- **Prompt hash:** `7dfaf34897560923`
- **ECS (full):** 0.1455
- **ECS (extraction–rationale):** 0.1455
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{
  "salience": [
    ["Briefly:", 1],
    ["T-Mobile", 7],
    ["sells", 6],
    ["Sidekick", 9],
    ["II", 8],
    ["roundup", 5],
    ["Plus:", 1],
    ["Spyware", 9],
    ["bill", 6],
    ["moves", 4],
    ["to", 1],
    ["Senate...", 4],
    ["Supercomputer", 10],
    ["center", 7],
    ["gets", 4],
    ["new", 3],
    ["No.", 5],
    ["2...", 5],
    ["MIT,", 9],
    ["Caltech", 9],
    ["offer", 5],
    ["low-tech", 8],
    ["voting", 6],
    ["advice.", 5]
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `caltech`, `mit`, `sidekick`, `supercomputer`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text discusses technology-related topics including a mobile device sale, a spyware bill, a supercomputer center, and tech-focused university voting advice."}
```

**Rationale text:**
> The text discusses technology-related topics including a mobile device sale, a spyware bill, a supercomputer center, and tech-focused university voting advice.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `advice`, `bill`, `center`, `mobile`, `spyware`, `supercomputer`, `tech`, `vote`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice.", "new_prediction": "Business"}
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

Text: "Briefly: T-Mobile sells Sidekick II roundup Plus: Spyware bill moves to Senate...Supercomputer center gets new No. 2...MIT, Caltech offer low-tech voting advice."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Supercomputer", "Spyware", "MIT", "Caltech", "T-Mobile"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `supercomputer`(1), `spyware`(2), `mit`(3), `caltech`(4), `t-mobile`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.2500 | 0.0909 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.6000 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2930 |

### ag_news_test_003454 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"World"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Verbalized confidence:** 1.00
- **Model refused:** No
- **Input length:** 34 words
- **Raw response length:** 17 chars
- **Prompt hash:** `3c62430b0a572f70`
- **ECS (full):** 0.5857
- **ECS (extraction–rationale):** 0.5857
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
{"salience": [["For", 1], ["the", 1], ["First", 8], ["Time,", 8], ["an", 1], ["African", 9], ["Woman", 8], ["Wins", 7], ["the", 1], ["Nobel", 10], ["Peace", 10], ["Prize", 10], ["Wangari", 7], ["Maathai,", 7], ["a", 1], ["Kenyan", 9], ["who", 1], ["has", 1], ["worked", 1], ["tirelessly", 1], ["to", 1], ["protect", 1], ["the", 1], ["environment,", 1], ["improve", 1], ["the", 1], ["lives", 1], ["of", 1], ["women,", 1], ["and", 1], ["fight", 1], ["crime,", 1], ["Friday", 6], ["became", 1]]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `african`, `first`, `kenyan`, `nobel`, `peace`, `prize`, `time`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

In one sentence, explain why the text was classified as World.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text reports on a significant international event, the awarding of the Nobel Peace Prize to a Kenyan activist, which is a matter of global affairs and human interest."}
```

**Rationale text:**
> The text reports on a significant international event, the awarding of the Nobel Peace Prize to a Kenyan activist, which is a matter of global affairs and human interest.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `kenyan`, `nobel`, `peace`, `prize`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Edit the text so that it is classified as "Sports" or "Business" or "Sci/Tech" instead of "World". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "For the First Time, an African Woman Wins the Nobel Prize in Economic Sciences Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `World`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Text: "For the First Time, an African Woman Wins the Nobel Peace Prize Wangari Maathai, a Kenyan who has worked tirelessly to protect the environment, improve the lives of women, and fight crime, Friday became"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nobel", "Peace", "Prize", "African"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nobel`(1), `peace`(2), `prize`(3), `african`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.5714 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.5714 |
| R–CF | — | — |
| R–RO | 0.7500 | 0.6000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |
| RBO (H,RO) | 0.4661 |

### ag_news_test_000788 — deepseek-v3

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Verbalized confidence:** 0.95
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1abb997e9f1de140`
- **ECS (full):** 0.5667
- **ECS (extraction–rationale):** 0.4583
- **ECS (extraction–perturbation):** 0.4583
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Sports`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text, in order. Include every occurrence, even repeated words.

Return only valid JSON:
{"salience": [["word", score], ["word", score], ...]}
```

**Response:**
```
```json
{
    "salience": [
        ["GOP", 3],
        ["Jamboree", 2],
        ["Could", 4],
        ["Briefly", 5],
        ["Lift", 7],
        ["Stocks", 10],
        ["NEW", 1],
        ["YORK", 1],
        ["Reuters", 1],
        ["Fasten", 1],
        ["your", 1],
        ["seatbelts", 1],
        ["The", 1],
        ["Republicans", 3],
        ["are", 1],
        ["coming", 1],
        ["to", 1],
        ["town", 1],
        ["If", 1],
        ["things", 1],
        ["go", 1],
        ["smoothly", 1],
        ["at", 1],
        ["the", 1],
        ["Republican", 3],
        ["National", 2],
        ["Convention", 2],
        ["the", 1],
        ["stock", 9],
        ["market", 9],
        ["could", 4],
        ["get", 1],
        ["a", 1],
        ["brief", 5],
        ["boost", 7],
        ["next", 1],
        ["week", 1],
        ["experts", 6],
        ["say", 1]
    ]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `boost`, `brief`, `briefly`, `could`, `expert`, `lift`, `market`, `stock`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The article discusses the potential impact of a political event on the stock market, which is a core topic of business and finance."}
```

**Rationale text:**
> The article discusses the potential impact of a political event on the stock market, which is a core topic of business and finance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `market`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "GOP Jamboree Could Briefly Lift Olympic Hopefuls NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the Olympic trials could get a brief boost next week, experts say.", "new_prediction": "Sports"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Sports`

**Reconstructed text:**
> GOP Jamboree Could Briefly Lift Olympic Hopefuls NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the Olympic trials could get a brief boost next week, experts say.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `market`, `stock`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Text: "GOP Jamboree Could Briefly Lift Stocks NEW YORK (Reuters) - Fasten your seatbelts. The Republicans are coming to town. If things go smoothly at the Republican National Convention, the stock market could get a brief boost next week, experts say."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["stocks", "market", "boost"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `stock`(1), `market`(2), `boost`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2500 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | 1.0000 | 0.3750 |
| R–CF | 1.0000 | 1.0000 |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.4353 |


## High-ECS Examples

### mnli_validation_matched_007354 (ECS=0.8750)
- **Dataset:** mnli
- **Text:** Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓

### mnli_validation_matched_008565 (ECS=0.8333)
- **Dataset:** mnli
- **Text:** Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured th…
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓

### mnli_validation_matched_008565 (ECS=0.8333)
- **Dataset:** mnli
- **Text:** Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured th…
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓


## Low-ECS Examples

### sst2_validation_000513 (ECS=0.0625)
- **Dataset:** sst2
- **Text:** care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_000010 (ECS=0.1000)
- **Dataset:** sst2
- **Text:** the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_009361 (ECS=0.1150)
- **Dataset:** mnli
- **Text:** Premise: I am glad she wasn't, said Jon.
Hypothesis: Jon was happy that Jane was not going to the dance. 
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗
