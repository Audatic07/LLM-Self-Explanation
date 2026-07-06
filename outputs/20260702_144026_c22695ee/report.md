# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-02 14:40:35
- **Duration:** 168.7s (2.8m)
- **Models (3):** nova-pro (`eu.amazon.nova-pro-v1:0`), qwen3-235b (`qwen.qwen3-235b-a22b-2507-v1:0`), deepseek-v3 (`deepseek.v3-v1:0`)
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 20460
- **Avg tokens per instance:** 2273

## Per-Dataset Summary

| Model | Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|-------|---------|-----------|----------|----------|---|---|------|---|
| nova-pro | sst2 | 1 | 1/1 (100%) | 0.000 | 100% | 100% | 0% | 100% |
| qwen3-235b | sst2 | 1 | 1/1 (100%) | 0.000 | 100% | 100% | 0% | 100% |
| deepseek-v3 | sst2 | 1 | 1/1 (100%) | 0.054 | 100% | 100% | 100% | 100% |
| nova-pro | mnli | 1 | 1/1 (100%) | 0.333 | 100% | 100% | 0% | 100% |
| qwen3-235b | mnli | 1 | 1/1 (100%) | 0.333 | 100% | 100% | 0% | 100% |
| deepseek-v3 | mnli | 1 | 0/1 (0%) | 0.233 | 100% | 100% | 100% | 0% |
| nova-pro | ag_news | 1 | 1/1 (100%) | 0.476 | 100% | 100% | 0% | 100% |
| qwen3-235b | ag_news | 1 | 1/1 (100%) | 0.500 | 100% | 100% | 0% | 100% |
| deepseek-v3 | ag_news | 1 | 1/1 (100%) | 0.163 | 100% | 100% | 0% | 100% |

## Sampling Log

| Model | Dataset | Requested | Sampled | Wrong Pred |
|-------|---------|-----------|---------|------------|
| nova-pro | sst2 | 1 | 1 | 0 |
| qwen3-235b | sst2 | 1 | 1 | 0 |
| deepseek-v3 | sst2 | 1 | 1 | 0 |
| nova-pro | mnli | 1 | 1 | 0 |
| qwen3-235b | mnli | 1 | 1 | 0 |
| deepseek-v3 | mnli | 1 | 1 | 1 |
| nova-pro | ag_news | 1 | 1 | 0 |
| qwen3-235b | ag_news | 1 | 1 | 0 |
| deepseek-v3 | ag_news | 1 | 1 | 0 |
| **Total** | | 9 | 9 | 1 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=3) or medium-length (21–50 words, N=6). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=3). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=1)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 9/9 | 100% |
| Rationale | 9/9 | 100% |
| Counterfactual | 2/9 | 22% |
| Rank Ordering | 8/9 | 89% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=9) | 0.2325 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.2562 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.1670 |
| Mean ECS (complete cases, N=1) | 0.0536 |
| Complete cases | 1/9 (11%) |
| Std ECS | 0.1925 |
| Median ECS | 0.2333 |
| **Mean ECS lift over chance** (ECS − random) | +0.1368 |
| Mean ECS random baseline | 0.0957 |

> **No significance testing applied.** The lift, correct-vs-incorrect split, length/vocab strata, and any other comparison above are point estimates (plus the bootstrap CI on mean ECS where shown) — no hypothesis test or multiple-comparison correction has been run, regardless of what `config/experiment.yaml` declares. At this pilot N, treat every comparison in this report as descriptive.

| Mean ECS — correct preds (N=8) | 0.2324 |
| Mean ECS — incorrect preds (N=1) | 0.2333 |
| Introduced-concept rate (R) | 0.737 |
| CF canonical (minimal) validity rate | 22% |
| CF contrast (free) validity rate | 56% |
| CF canonical (minimal) minimality (edits/len) | 0.198 |
| CF contrast (free) minimality (edits/len) | 0.409 |
| Confidence elicitation | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size | 0.89 |
| Mean CC4 size | 0.78 |
| % instances with CC3 | 66.7% |
| % instances with CC4 | 55.6% |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.5222 | 0.2954 |
| H–CF | 0.2917 | 0.1625 |
| H–RO | 0.7208 | 0.5354 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.4188 | 0.1815 |
| CF–RO | 0.3333 | 0.1429 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.1314 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported here as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — for interpreting individual pairs, not for the headline number. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 9/9 (100%) | 9/9 (100%) |
| Rationale | 9/9 (100%) | 9/9 (100%) |
| Counterfactual (JSON parsed) | 8/9 (89%) |
| Counterfactual (rules compliant) | 3/9 (33%) |
| Counterfactual (flip verified) | 2/3 (67%) |
| Rank Ordering | 8/9 (89%) | 8/9 (89%) |
| All 4 valid | 1/9 |
| 3 valid (CC3 adjusted) | 8/9 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 3 | 0.3000 |
| Medium (21–50) | 6 | 0.1987 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 6 | 0.1987 |
| Short vocab (≤20 unique tokens) | 3 | 0.3000 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2325 | [0.1060, 0.3513] |

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

**Explanation:** 
The text implies that the scenes are very emotionally impactful, suggesting a high level of quality or effectiveness in evoking emotion. This is a positive sentiment towards the scenes being described.
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 246 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{
  "salience": {
    "and": 1,
    "if": 3,
    "you": 7,
    "'re": 3,
    "not": 6,
    "nearly": 8,
    "moved": 9,
    "to": 4,
    "tears": 9,
    "by": 5,
    "a": 2,
    "couple": 6,
    "of": 3,
    "scenes": 9,
    ",": 1,
    "you": 7,
    "'ve": 3,
    "got": 6,
    "ice": 7,
    "water": 7,
    "in": 4,
    "your": 6,
    "veins": 7,
    ".": 1
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `moved`, `nearly`, `scenes`, `tears`

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
  "rationale": "The text praises the emotional impact of the scenes, suggesting they are profoundly moving, which is a positive sentiment."
}
```

**Rationale text:**
> The text praises the emotional impact of the scenes, suggesting they are profoundly moving, which is a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `scene`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{
  "rewritten": "if you're not nearly moved to tears by a couple of scenes, they completely missed the mark.",
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
    "moved",
    "tears",
    "scenes",
    "couple"
  ]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `moved`(1), `tears`(2), `scenes`(3), `couple`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.6000 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3257 |

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
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 20 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"and": 2, "if": 5, "you": 6, "'re": 4, "not": 8, "nearly": 6, "moved": 9, "to": 3, "tears": 10, "by": 2, "a": 1, "couple": 3, "of": 1, "scenes": 7, ",": 1, "you": 6, "'ve": 4, "got": 5, "ice": 8, "water": 6, "in": 2, "your": 4, "veins": 7, ".": 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `moved`, `not`, `tears`

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

Edit the text so that it is classified as "negative" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "and if you're not nearly moved to tears by a couple of scenes, you've got ice water in your veins—what a cold, lifeless experience.", "new_prediction": "negative"}
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
- Tokens: `tears`(1), `moved`(2), `scenes`(3), `ice`(4), `veins`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.6000 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3380 |

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
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 20 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.0536
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.1339
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

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"and": 1, "if": 1, "you": 1, "'re": 1, "not": 1, "nearly": 3, "moved": 8, "to": 1, "tears": 9, "by": 1, "a": 1, "couple": 1, "of": 1, "scenes": 7, ",": 1, "you": 1, "'ve": 1, "got": 1, "ice": 6, "water": 6, "in": 1, "your": 1, "veins": 6, ".": 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `moved`, `scenes`, `tears`

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
{"rationale": "The text expresses a positive sentiment by strongly implying that the scenes are emotionally powerful and moving, suggesting a positive quality."}
```

**Rationale text:**
> The text expresses a positive sentiment by strongly implying that the scenes are emotionally powerful and moving, suggesting a positive quality.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `scene`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "and if you 're not nearly moved to tears by a couple of scenes , you 've got a heart .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> and if you 're not nearly moved to tears by a couple of scenes , you 've got a heart .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `in`, `veins`, `water`, `your`

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
- Tokens: `tears`(1), `moved`(2), `ice`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 0.2500 | 0.1250 |
| H–RO | 1.0000 | 0.7500 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.3333 | 0.1429 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2987 |

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
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{
  "salience": {
    "just": 3,
    "look": 4,
    "what": 5,
    "we": 6,
    "did": 7,
    "to": 5,
    "Iraq": 10,
    "Hypothesis:": 2,
    "Iraq": 10,
    "was": 6,
    "something": 7,
    "that": 6,
    "shouldn't": 8,
    "have": 7,
    "happened": 8
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happened`, `iraq`, `something`

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

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""entailment" or "contradiction"" instead of "neutral". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: just look what we did to Iraq\nHypothesis: We should not have done what we did to Iraq",
  "new_prediction": "entailment"
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
- Tokens: `iraq`(1), `look`(2), `happened`(3)

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
| RBO (H,RO) | 0.0270 |

### mnli_validation_matched_007919 — qwen3-235b

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
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 19 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"Premise": 5, "just": 6, "look": 5, "what": 7, "we": 4, "did": 8, "to": 3, "Iraq": 9, "Hypothesis": 5, "was": 3, "something": 5, "that": 3, "shouldn't": 9, "have": 4, "happened": 8}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happened`, `iraq`, `look`

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
{"rationale": "The premise expresses a reflection on actions taken regarding Iraq but does not explicitly state whether those actions were right or wrong, leaving the judgment in the hypothesis unsupported or contradicted."}
```

**Rationale text:**
> The premise expresses a reflection on actions taken regarding Iraq but does not explicitly state whether those actions were right or wrong, leaving the judgment in the hypothesis unsupported or contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""entailment" or "contradiction"" instead of "neutral". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: just look what we did to Iraq\nHypothesis: The action against Iraq was a mistake and should not have happened", "new_prediction": "entailment"}
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
- Tokens: `iraq`(1), `look`(2), `happened`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0540 |

### mnli_validation_matched_007919 — deepseek-v3

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 16 words
- **Raw response length:** 22 chars

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
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.4762
- **ECS (extraction–rationale):** 0.4762
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"Nokia": 8, "announces": 7, "Near": 9, "Field": 9, "Communication": 9, "products": 6, "With": 5, "the": 4, "Nokia": 8, "NFC": 10, "(Near": 9, "Field": 9, "Communication)": 9, "shell": 7, "on": 5, "their": 5, "phone,": 7, "consumers": 7, "will": 6, "be": 6, "able": 7, "to": 5, "access": 8, "a": 3, "variety": 7, "of": 5, "services": 8, "and": 5, "exchange": 8, "information": 9, "with": 6, "simple": 7, "touch": 8, "gesture.": 6}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `information`, `near`, `nfc`

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
{"rewritten": "Nokia announces Near Field Communication products, sparking a global conversation about the future of mobile technology. With the Nokia NFC (Near Field Communication) shell on their phone, consumers around the world will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "World"}

For "Sports":
{"rewritten": "Nokia announces Near Field Communication products, aiming to revolutionize fan engagement at sports events. With the Nokia NFC (Near Field Communication) shell on their phone, sports fans will be able to access exclusive content and exchange information with a simple touch gesture.", "new_prediction": "Sports"}

For "Business":
{"rewritten": "Nokia announces Near Field Communication products, expanding their market reach and revenue streams. With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture, boosting Nokia's competitive edge in the tech industry.", "new_prediction": "Business"}
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
{"ranking": ["Nokia", "Communication", "products", "consumers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nokia`(1), `communication`(2), `products`(3), `consumers`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.6667 |
| H–CF | — | — |
| H–RO | 0.2500 | 0.1250 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2857 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0000 |

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

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"Nokia": 8, "announces": 6, "Near": 10, "Field": 10, "Communication": 10, "products": 5, "With": 2, "the": 1, "NFC": 10, "(": 1, ")": 1, "shell": 6, "on": 1, "their": 1, "phone": 7, ",": 1, "consumers": 4, "will": 2, "be": 1, "able": 3, "to": 1, "access": 5, "a": 1, "variety": 3, "of": 1, "services": 5, "and": 2, "exchange": 6, "information": 7, "with": 2, "a": 1, "simple": 4, "touch": 6, "gesture": 5, ".": 1}}
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
{"rewritten": "Nokia announces new business partnership to expand Near Field Communication products, boosting global market reach and mobile payment solutions.", "new_prediction": "Business"}
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
- Tokens: `nfc`(1), `nokia`(2), `communication`(3), `products`(4), `gesture`(5)

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
| RBO (H,RO) | 0.0000 |

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
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.1625
- **ECS (extraction–rationale):** 0.1625
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

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
```json
{
  "salience": {
    "Nokia": 7,
    "announces": 6,
    "Near": 9,
    "Field": 9,
    "Communication": 9,
    "products": 5,
    "With": 1,
    "the": 1,
    "NFC": 9,
    "(": 1,
    "Near": 9,
    "Field": 9,
    "Communication": 9,
    ")": 1,
    "shell": 4,
    "on": 1,
    "their": 1,
    "phone,": 4,
    "consumers": 2,
    "will": 1,
    "be": 1,
    "able": 1,
    "to": 1,
    "access": 3,
    "a": 1,
    "variety": 1,
    "of": 1,
    "services": 3,
    "and": 1,
    "exchange": 3,
    "information": 3,
    "with": 1,
    "a": 1,
    "simple": 2,
    "touch": 3,
    "gesture.": 2
  }
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `announces`, `communication`, `field`, `near`, `nfc`, `nokia`, `products`

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
{"rationale": "The text describes a new technological product (NFC shell) from a company (Nokia) that enables advanced digital services, which falls under science and technology."}
```

**Rationale text:**
> The text describes a new technological product (NFC shell) from a company (Nokia) that enables advanced digital services, which falls under science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`, `nokia`, `product`, `service`, `shell`

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
{"rewritten": "Nokia announces new business strategy with Near Field Communication products. With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "Business"}
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
{"ranking": ["NFC", "Communication", "products", "phone"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `communication`(2), `products`(3), `phone`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.4000 | 0.2000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.3750 |
| R–CF | — | — |
| R–RO | 0.2500 | 0.1250 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0076 |


## High-ECS Examples

### ag_news_test_004983 (ECS=0.5000)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### ag_news_test_004983 (ECS=0.4762)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### mnli_validation_matched_007919 (ECS=0.3333)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓


## Low-ECS Examples

### sst2_validation_000665 (ECS=0.0000)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_000665 (ECS=0.0000)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_000665 (ECS=0.0536)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
