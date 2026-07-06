# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-16 15:23:49
- **Duration:** 303.4s (5.1m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 11
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 4199
- **Avg tokens per instance:** 382

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 4 | — | 0.171 | 50% | 100% | 75% | 100% |
| mnli | 3 | — | 0.500 | 33% | 67% | 33% | 67% |
| ag_news | 4 | — | 0.000 | 0% | 0% | 0% | 0% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 5 | 4 | 0 |
| mnli | 5 | 3 | 1 |
| ag_news | 0 | 0 | 0 |
| **Total** | 10 | 7 | 1 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=2) or medium-length (21–50 words, N=2). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=2). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=3)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 3/11 | 27% |
| Rationale | 8/11 | 73% |
| Counterfactual | 4/11 | 36% |
| Rank Ordering | 9/11 | 82% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=11) | 0.2533 |
| Mean ECS (primary: H,CF,RO) | 0.2917 |
| Mean ECS (complete cases, N=3) | 0.2933 |
| Complete cases | 3/11 (27%) |
| Primary ECS pairs <3 | 1 instances |
  → sst2_validation_0001: 1 pair(s), ECS_primary=0.2000
| Std ECS | 0.1791 |
| Median ECS | 0.2367 |
| Confidence elicitation | Removed — does not proxy faithfulness |
| Mean CC3 size | 0.36 |
| Mean CC4 size | 0.18 |
| % instances with CC3 | 18.2% |
| % instances with CC4 | 18.2% |

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.6667 | 0.2444 |
| H–CF | 1.0000 | 0.3556 |
| H–RO | 0.8000 | 0.6984 |
| R–CF | 0.5000 | 0.2500 |
| R–RO | 0.7708 | 0.7708 |
| CF–RO | 0.7500 | 0.2667 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.1224 |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |

> Overlap Coefficient is the primary pairwise metric (unlike Jaccard, it is not penalized by smaller salience sets). Jaccard is retained as a secondary reference. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 3/11 (27%) | 3/11 (27%) |
| Rationale | 8/11 (73%) | 8/11 (73%) |
| Counterfactual (JSON parsed) | 7/11 (64%) |
| Counterfactual (rules compliant) | 7/11 (64%) |
| Counterfactual (flip verified) | 4/7 (57%) |
| Rank Ordering | 9/11 (82%) | 9/11 (82%) |
| All 4 valid | 3/11 |
| 3 valid (CC3 adjusted) | 1/11 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 2 | 0.2700 |
| Medium (21–50) | 2 | 0.2367 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 2 | 0.2367 |
| Short vocab (≤20 unique tokens) | 2 | 0.2700 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2533 | [0.0867, 0.4200] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

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
- **Input length:** 14 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b00a643964e1a260`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{
  "salience": {
    "comes": 2,
    "...": 1,
    "uncomfortably": 10,
    "close": 7,
    "to":
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The phrase conveys a sense of unease and discomfort by describing something as \"uncomfortably close\" to a negative, unsettling image of \"coasting in the treads of the bicycle thief,\" which together create a negative sentiment."}
```

**Rationale text:**
> The phrase conveys a sense of unease and discomfort by describing something as "uncomfortably close" to a negative, unsettling image of "coasting in the treads of the bicycle thief," which together create a negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `close`, `thief`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

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
{"rewritten":"comes ... comfortably close to coasting in the treads of the bicycle thief .","new_prediction":"positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `negative`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["uncomfortably","thief","close","comes","coasting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`(1), `thief`(2), `close`(3), `comes`(4), `coasting`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | 1.0000 | 0.4000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . "

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
- **Input length:** 29 words
- **Raw response length:** 20 chars
- **Prompt hash:** `9aba917cfb5449c7`
- **ECS (full):** 0.1333
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text praises the film for unexpectedly transcending its self‑aware style and genuinely engaging the viewer, highlighting surprising depth that conveys a positive assessment."}
```

**Rationale text:**
> The text praises the film for unexpectedly transcending its self‑aware style and genuinely engaging the viewer, highlighting surprising depth that conveys a positive assessment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `surprising`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . "

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
{"rewritten":"what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still fail to break past the artifice and thoroughly engage you .","new_prediction":"negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still fail to break past the artifice and thoroughly engage you .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `manage`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["engage","thoroughly","manage","surprising","break"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `engage`(1), `thoroughly`(2), `manage`(3), `surprising`(4), `break`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 1.0000 | 0.2000 |
| CF–RO | 1.0000 | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### sst2_validation_0002

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
- **ECS (full):** 0.0400
- **ECS (primary):** 0.1000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
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
{"salience":{"verbinski":3,"implements":4,"every":2,"hack-artist":9,"trick":8,"to":1,"give":2,"us":1,"the":1,"ooky-spookies":9,".":1}}
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
{"ranking":["trick","implement","verbinski","every","give"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `trick`(1), `implements`(2), `verbinski`(3), `every`(4), `give`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 1.0000 | 0.2000 |
| H–RO | 0.6000 | 0.4286 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.0000 | 0.0000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |
| RBO (H,RO) | 0.1028 |

### sst2_validation_0003

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . "

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
- **Input length:** 23 words
- **Raw response length:** 20 chars
- **Prompt hash:** `fd4efe262a8ab2d5`
- **ECS (full):** 0.3400
- **ECS (primary):** 0.2000
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
"it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{
  "salience": {
    "it": 1,
    "'s": 1,
    "an": 1,
    "offbeat": 8,
    "treat": 8,
    "that": 1,
    "pokes": 6,
    "fun": 9,
    "at": 1,
    "the": 1,
    "democratic": 2,
    "exercise": 2,
    "while": 1,
    "also": 3,
    "examining": 4,
    "its": 1,
    "significance": 5,
    "for": 1,
    "those": 1,
    "who": 1,
    "take": 1,
    "part": 1,
    ".": 1
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fun`, `offbeat`, `pokes`, `significance`, `treat`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The passage conveys a light‑hearted, appreciative tone by describing the work as an \"offbeat treat\" that humorously critiques democracy while also thoughtfully exploring its importance to participants, indicating a generally favorable view."}
```

**Rationale text:**
> The passage conveys a light‑hearted, appreciative tone by describing the work as an "offbeat treat" that humorously critiques democracy while also thoughtfully exploring its importance to participants, indicating a generally favorable view.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `offbeat`, `treat`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . "

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
{"rewritten":"it 's an offbeat travesty that pokes fun at the democratic exercise while also examining its significance for those who take part .","new_prediction":"negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> it 's an offbeat travesty that pokes fun at the democratic exercise while also examining its significance for those who take part .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `treat`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Here is the exact text that was classified:
"it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["treat","fun","offbeat","significance","examining"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `treat`(1), `fun`(2), `offbeat`(3), `significance`(4), `examining`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.4000 |
| H–CF | 1.0000 | 0.2000 |
| H–RO | 0.8000 | 0.6667 |
| R–CF | 1.0000 | 0.5000 |
| R–RO | 1.0000 | 0.4000 |
| CF–RO | 1.0000 | 0.2000 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |
| RBO (H,RO) | 0.2332 |

### mnli_validation_matched_0000

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Not yourself.
Hypothesis: Someone else

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
- **Model refused:** No
- **Input length:** 6 words
- **Raw response length:** 22 chars
- **Prompt hash:** `bd36af1ff07e9a2a`
- **ECS (full):** 0.5000
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Not yourself.
Hypothesis: Someone else"

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"Premise:":2,"Not":9,"yourself.":9,"Hypothesis:":2,"Someone":8,"else":8}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `else`, `not`, `someone`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Not yourself.
Hypothesis: Someone else"

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The premise \"Not yourself\" directly implies that the referent is a different person, which matches the hypothesis that it refers to \"someone else,\" making the hypothesis logically entailed by the premise."}
```

**Rationale text:**
> The premise "Not yourself" directly implies that the referent is a different person, which matches the hypothesis that it refers to "someone else," making the hypothesis logically entailed by the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `someone`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Not yourself.
Hypothesis: Someone else"

Rewrite the text above with MINIMAL changes to flip the classifier's output to neutral, contradiction. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: neutral, contradiction

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: neutral, contradiction>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"Premise: Not yourself.\nHypothesis: Yourself","new_prediction":"contradiction"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: Not yourself.
Hypothesis: Yourself

**Parsed tokens:**
- Status: **Valid**
- Tokens: `else`, `someone`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Not yourself.
Hypothesis: Someone else"

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Not","yourself","Someone","else"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `not`(1), `someone`(2), `else`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 1.0000 | 0.5000 |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0313 |

### mnli_validation_matched_0001

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `contradiction`
- **Predicted:** `neutral` ✗
- **Input length:** 60 words
- **Raw response length:** 19 chars

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.
Hypothesis: Breaking it down into 6 elements has always been helpful for students and professionals.

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
- **Input length:** 37 words
- **Raw response length:** 19 chars
- **Prompt hash:** `b00ef8ce8bce925d`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.
Hypothesis: Breaking it down into 6 elements has always been helpful for students and professionals."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.
Hypothesis: Breaking it down into 6 elements has always been helpful for students and professionals."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The premise merely lists six elements without evaluating their usefulness, while the hypothesis asserts that breaking them down is helpful, so the premise neither confirms nor denies the hypothesis, making the relationship neutral."}
```

**Rationale text:**
> The premise merely lists six elements without evaluating their usefulness, while the hypothesis asserts that breaking them down is helpful, so the premise neither confirms nor denies the hypothesis, making the relationship neutral.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `helpful`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.
Hypothesis: Breaking it down into 6 elements has always been helpful for students and professionals."

Rewrite the text above with MINIMAL changes to flip the classifier's output to entailment, contradiction. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: entailment, contradiction

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: entailment, contradiction>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{
  "rewritten": "Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.\nHypothesis: Breaking it down into 6 elements has been helpful for students and professionals.",
  "new_prediction": "ent
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
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.
Hypothesis: Breaking it down into 6 elements has always been helpful for students and professionals."

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["six","elements","helpful","students","professionals"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `six`(1), `elements`(2), `helpful`(3), `students`(4), `professionals`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | 1.0000 | 0.2000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### ag_news_test_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sci/Tech`
- **Predicted:** `Business` ✗
- **Input length:** 50 words
- **Raw response length:** 20 chars

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, preserving a 6-5 come-from-behind win over the San Diego Padres. "

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
- **Model refused:** No
- **Input length:** 46 words
- **Raw response length:** 18 chars
- **Prompt hash:** `fbbe5e525705be07`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 1
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, preserving a 6-5 come-from-behind win over the San Diego Padres. "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, preserving a 6-5 come-from-behind win over the San Diego Padres. "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The passage describes a baseball game, mentioning teams, players, a home run, and a defensive play that determined the outcome, which are all characteristic details of sports reporting."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, preserving a 6-5 come-from-behind win over the San Diego Padres. "

Rewrite the text above with MINIMAL changes to flip the classifier's output to World, Business, Sci/Tech. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: World, Business, Sci/Tech

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```

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
The text was classified as: Sports

Here is the exact text that was classified:
"Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, preserving a 6-5 come-from-behind win over the San Diego Padres. "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Braves","Padres","homer","run","Andruw"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `braves`(1), `padres`(2), `homer`(3), `run`(4), `andruw`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said."

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
- **Model refused:** No
- **Input length:** 42 words
- **Raw response length:** 17 chars
- **Prompt hash:** `77b3e5eec9068618`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Here is the exact text that was classified:
"U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Here is the exact text that was classified:
"U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article reports on a U.S. military operation and casualties involving Shi'ite militia in Baghdad, focusing on international conflict and political actors, which are characteristic of World news."}
```

**Rationale text:**
> The article reports on a U.S. military operation and casualties involving Shi'ite militia in Baghdad, focusing on international conflict and political actors, which are characteristic of World news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `baghdad`, `military`, `militia`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Here is the exact text that was classified:
"U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said."

Rewrite the text above with MINIMAL changes to flip the classifier's output to Sports, Business, Sci/Tech. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: Sports, Business, Sci/Tech

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"Lakers Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - Lakers killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said.","new_prediction":"Sports"}
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

Here is the exact text that was classified:
"U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said."

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Baghdad","U.S.","militia","Sadr","forces"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `baghdad`(1), `u.s`(2), `militia`(3), `sadr`(4), `forces`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | 0.6667 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Airlines from its No."

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
- **Model refused:** No
- **Input length:** 46 words
- **Raw response length:** 20 chars
- **Prompt hash:** `0b86c33802b9ddb3`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Airlines from its No."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Airlines from its No."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article discusses airline companies, mentions a NASDAQ ticker, and focuses on corporate expansion and competition between Northwest and ATA, all of which are characteristic of business news."}
```

**Rationale text:**
> The article discusses airline companies, mentions a NASDAQ ticker, and focuses on corporate expansion and competition between Northwest and ATA, all of which are characteristic of business news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `news`, `northwest`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Airlines from its No."

Rewrite the text above with MINIMAL changes to flip the classifier's output to World, Sports, Sci/Tech. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: World, Sports, Sci/Tech

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Warriors (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Warriors from its No.","new_prediction":"Sports"}
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

Here is the exact text that was classified:
"Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Airlines from its No."

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Northwest","Airlines","nasdaq","expand","rival"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `northwest`(1), `airlines`(2), `nasdaq`(3), `expand`(4), `rival`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | 0.5000 | 0.1667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |


## High-ECS Examples

### mnli_validation_matched_0000 (ECS=0.5000)
- **Dataset:** mnli
- **Text:** Premise: Not yourself.
Hypothesis: Someone else
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓

### sst2_validation_0003 (ECS=0.3400)
- **Dataset:** sst2
- **Text:** it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_0001 (ECS=0.1333)
- **Dataset:** sst2
- **Text:** what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓


## Low-ECS Examples

### sst2_validation_0002 (ECS=0.0400)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_0001 (ECS=0.1333)
- **Dataset:** sst2
- **Text:** what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_0003 (ECS=0.3400)
- **Dataset:** sst2
- **Text:** it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
