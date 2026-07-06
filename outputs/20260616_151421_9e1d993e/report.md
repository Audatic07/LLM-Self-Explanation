# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-16 15:14:34
- **Duration:** 27.1s (0.5m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 2
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 879
- **Avg tokens per instance:** 440

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | — | 0.243 | 100% | 100% | 100% | 50% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 3 | 2 | 0 |
| **Total** | 3 | 2 | 0 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=2) or medium-length (21–50 words, N=0). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=2). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=1)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 2/2 | 100% |
| Rationale | 2/2 | 100% |
| Counterfactual | 2/2 | 100% |
| Rank Ordering | 1/2 | 50% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=2) | 0.2433 |
| Mean ECS (primary: H,CF,RO) | 0.2333 |
| Mean ECS (complete cases, N=1) | 0.4200 |
| Complete cases | 1/2 (50%) |
| Primary ECS pairs <3 | 1 instances |
  → sst2_validation_0001: 1 pair(s), ECS_primary=0.2000
| Std ECS | 0.1767 |
| Median ECS | 0.2433 |
| Confidence elicitation | Removed — does not proxy faithfulness |
| Mean CC3 size | 1.00 |
| Mean CC4 size | 0.50 |
| % instances with CC3 | 50.0% |
| % instances with CC4 | 50.0% |

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.5000 | 0.2000 |
| H–CF | 1.0000 | 0.2000 |
| H–RO | 1.0000 | 0.6000 |
| R–CF | 0.5000 | 0.2500 |
| R–RO | 1.0000 | 1.0000 |
| CF–RO | 1.0000 | 0.3333 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.3650 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

> Overlap Coefficient is the primary pairwise metric (unlike Jaccard, it is not penalized by smaller salience sets). Jaccard is retained as a secondary reference. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 2/2 (100%) | 2/2 (100%) |
| Rationale | 2/2 (100%) | 2/2 (100%) |
| Counterfactual (JSON parsed) | 2/2 (100%) |
| Counterfactual (rules compliant) | 2/2 (100%) |
| Counterfactual (flip verified) | 2/2 (100%) |
| Rank Ordering | 1/2 (50%) | 1/2 (50%) |
| All 4 valid | 1/2 |
| 3 valid (CC3 adjusted) | 1/2 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 2 | 0.2433 |
| Medium (21–50) | 0 | 0.0000 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 0 | 0.0000 |
| Short vocab (≤20 unique tokens) | 2 | 0.2433 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2433 | [0.0667, 0.4200] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's great escapist fun that recreates a place and time that will never happen again . "

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
- **Model refused:** No
- **Input length:** 17 words
- **Raw response length:** 20 chars
- **Prompt hash:** `26dd26288e7734de`
- **ECS (full):** 0.4200
- **ECS (primary):** 0.2667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's great escapist fun that recreates a place and time that will never happen again . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{
  "salience": {
    "it": 2,
    "'s": 2,
    "great": 9,
    "escapist": 7,
    "fun": 9,
    "that": 2,
    "recreates": 5,
    "a": 1,
    "place": 4,
    "and": 1,
    "time": 4,
    "will": 1,
    "never": 3,
    "happen": 3,
    "again": 3,
    ".": 1
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `escapist`, `fun`, `great`, `place`, `recreates`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's great escapist fun that recreates a place and time that will never happen again . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text conveys a positive judgment by describing the experience as enjoyable and valuable, emphasizing its great, escapist fun and the unique, cherished nature of the recreated setting."}
```

**Rationale text:**
> The text conveys a positive judgment by describing the experience as enjoyable and valuable, emphasizing its great, escapist fun and the unique, cherished nature of the recreated setting.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fun`, `great`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's great escapist fun that recreates a place and time that will never happen again . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to negative. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: negative

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: negative>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"it 's bad escapist fun that recreates a place and time that will never happen again .","new_prediction":"negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> it 's bad escapist fun that recreates a place and time that will never happen again .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's great escapist fun that recreates a place and time that will never happen again . "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["great","fun","escapist"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`(1), `fun`(2), `escapist`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.4000 |
| H–CF | 1.0000 | 0.2000 |
| H–RO | 1.0000 | 0.6000 |
| R–CF | 1.0000 | 0.5000 |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |
| RBO (H,RO) | 0.3650 |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "verbinski implements every hack-artist trick to give us the ooky-spookies . "

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
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 20 chars
- **Prompt hash:** `50f5b42b5c34d301`
- **ECS (full):** 0.0667
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{
  "salience": {
    "verbinski": 5,
    "implements": 3,
    "every": 2,
    "hack-artist": 9,
    "trick": 8,
    "to": 1,
    "give": 2,
    "us": 1,
    "the": 1,
    "ooky-spookies": 9,
    ".": 1
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `implements`, `ooky-spookies`, `trick`, `verbinski`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The description calls the filmmaker's methods \"hack-artist tricks\" and the result \"ooky-spookies,\" using disparaging language that conveys a critical, unfavorable view."}
```

**Rationale text:**
> The description calls the filmmaker's methods "hack-artist tricks" and the result "ooky-spookies," using disparaging language that conveys a critical, unfavorable view.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ooky`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"verbinski implements every artistic trick to give us the ooky-spookies .","new_prediction":"positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> verbinski implements every artistic trick to give us the ooky-spookies .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["trick"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 1.0000 | 0.2000 |
| H–RO | — | — |
| R–CF | 0.0000 | 0.0000 |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |


## High-ECS Examples

### sst2_validation_0001 (ECS=0.0667)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_0000 (ECS=0.4200)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓


## Low-ECS Examples

### sst2_validation_0001 (ECS=0.0667)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_0000 (ECS=0.4200)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
