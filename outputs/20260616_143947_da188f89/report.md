# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-16 14:40:03
- **Duration:** 269.7s (4.5m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 11
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 4005
- **Avg tokens per instance:** 364

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 4 | — | 0.183 | 0% | 50% | 100% | 100% |
| mnli | 3 | — | 0.333 | 33% | 33% | 0% | 67% |
| ag_news | 4 | — | 0.000 | 0% | 0% | 0% | 0% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 5 | 4 | 0 |
| mnli | 5 | 3 | 1 |
| ag_news | 0 | 0 | 0 |
| **Total** | 10 | 7 | 1 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=2) or medium-length (21–50 words, N=1). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=2). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=0)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 1/11 | 9% |
| Rationale | 5/11 | 45% |
| Counterfactual | 4/11 | 36% |
| Rank Ordering | 9/11 | 82% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their Jaccard is excluded from ECS; agreement is measured via Kendall τ instead. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=11) | 0.2333 |
| Mean ECS (primary: H,CF,RO) | 0.0667 |
| Mean ECS (complete cases, N=0) | 0.0000 |
| Complete cases | 0/11 (0%) |
| Primary ECS pairs <3 | 3 instances |
  → sst2_validation_0002: 1 pair(s), ECS_primary=0.0000
  → sst2_validation_0003: 1 pair(s), ECS_primary=0.2000
  → mnli_validation_matched_0000: 0 pair(s), ECS_primary=0.0000
| Std ECS | 0.1656 |
| Median ECS | 0.3333 |
| Confidence elicitation | Removed — does not proxy faithfulness |
| Mean CC3 size | 0.18 |
| Mean CC4 size | 0.18 |
| % instances with CC3 | 18.2% |
| % instances with CC4 | 18.2% |

### Pairwise Jaccard Similarity

| Pair | Jaccard (mean) | Overlap Coeff (mean) |
|------|----------------|----------------------|
| H–R | 0.3333 | 1.0000 |
| H–CF | 0.0000 | 0.0000 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.2500 | 0.5000 |
| R–RO | 0.2133 | 0.5333 |
| CF–RO | 0.2000 | 0.7500 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 1/11 (9%) | 1/11 (9%) |
| Rationale | 5/11 (45%) | 5/11 (45%) |
| Counterfactual | 4/11 (36%) | 4/11 (36%) |
| CF flip verified | 4/4 (100%) |
| Rank Ordering | 9/11 (82%) | 9/11 (82%) |
| All 4 valid | 0/11 |
| 3 valid (CC3 adjusted) | 3/11 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Kendall τ (rank correlation), not Jaccard.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 2 | 0.1667 |
| Medium (21–50) | 1 | 0.3667 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 1 | 0.3667 |
| Short vocab (≤20 unique tokens) | 2 | 0.1667 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2333 | [0.0000, 0.3667] |

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
- **CF flip verified:** Yes
- **CF actual label:** `positive`
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

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The passage conveys a sense of unease and discomfort by describing an unsettling proximity to a threatening figure, which creates a negative emotional tone."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to positive.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: positive>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{
  "edits": [
    {"from": "uncomfortably", "to": "pleasantly"},
    {"from": "thief", "to": "friend"}
  ],
  "new_prediction": "positive"
}
```

**Reconstructed text:**
> comes ... pleasantly close to coasting in the treads of the bicycle friend . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `thief`, `uncomfortably`

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
{"ranking":["uncomfortably","thief","close","treads","coasting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`(1), `thief`(2), `close`(3), `treads`(4), `coasting`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | — |
| CF–RO | 0.4000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
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

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The passage highlights that, despite the film's self‑conscious style, it succeeds in transcending its artificiality and genuinely engaging the viewer, which conveys a positive assessment."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to negative.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "engage", "to": "bore"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly bore you . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `engage`

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

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | — |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **ECS (full):** 0.0000
- **ECS (primary):** 0.0000
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
    "hack
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text criticizes Verbinski's approach by calling his techniques hackneyed and describing the result as merely 'ooky-spookies,' indicating a disapproving tone toward the film's quality."}
```

**Rationale text:**
> The text criticizes Verbinski's approach by calling his techniques hackneyed and describing the result as merely 'ooky-spookies,' indicating a disapproving tone toward the film's quality.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ooky`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to positive.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: positive>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "hack-artist", "to": "visionary"}], "new_prediction": "positive"}
```

**Reconstructed text:**
> verbinski implements every visionary trick to give us the ooky-spookies . 

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
{"ranking":["trick","verbinski","implements","every","give"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `trick`(1), `verbinski`(2), `implements`(3), `every`(4), `give`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | 0.0000 |
| R–RO | 0.0000 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **ECS (full):** 0.3667
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

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

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text praises the work as an offbeat treat that humorously critiques democracy while also thoughtfully exploring its importance to participants, conveying an overall appreciative and favorable tone."}
```

**Rationale text:**
> The text praises the work as an offbeat treat that humorously critiques democracy while also thoughtfully exploring its importance to participants, conveying an overall appreciative and favorable tone.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `offbeat`, `treat`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to negative.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "treat", "to": "disaster"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> it 's an offbeat disaster that pokes fun at the democratic exercise while also examining its significance for those who take part . 

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

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | 0.5000 |
| R–RO | 0.4000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **ECS (full):** 0.3333
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

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
{
  "salience": {
    "Premise:": 2,
    "Not": 9,
    "yourself.": 9,
    "Hypothesis:": 2,
    "Someone": 8,
    "else": 8
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `else`, `not`, `someone`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The premise states that the referent is not you, which directly implies that it must be another person, thereby supporting the hypothesis that it is someone else."}
```

**Rationale text:**
> The premise states that the referent is not you, which directly implies that it must be another person, thereby supporting the hypothesis that it is someone else.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `someone`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to neutral, contradiction.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

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
- Tokens: `not`(2), `someone`(4), `else`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Valid strategies:** 1
- **CF flip verified:** No
- **CF actual label:** `neutral`
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

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The premise merely lists six elements without asserting any evaluative claim, while the hypothesis adds a subjective benefit claim about those elements, so the premise neither confirms nor denies the hypothesis, making the relationship neutral."}
```

**Rationale text:**
> The premise merely lists six elements without asserting any evaluative claim, while the hypothesis adds a subjective benefit claim about those elements, so the premise neither confirms nor denies the hypothesis, making the relationship neutral.

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to entailment, contradiction.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "purpose", "to": "burden"}], "new_prediction": "contradiction"}
```

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

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **CF actual label:** `Sports`
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

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article describes a baseball game, detailing specific players, scoring actions, and a defensive play, which are characteristic elements of sports reporting."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to World, Business, Sci/Tech.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{
  "edits": [
    {
      "from": "homer",
      "to": "satellite"
    }
  ],
  "new_prediction": "Sci/Tech"
}
```

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

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article reports on a U.S. military operation resulting in the deaths of militia members in a Baghdad suburb, focusing on international conflict and political actors, which aligns with the World news category."}
```

**Rationale text:**
> The article reports on a U.S. military operation resulting in the deaths of militia members in a Baghdad suburb, focusing on international conflict and political actors, which aligns with the World news category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `military`, `suburb`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to Sports, Business, Sci/Tech.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{"edits":[{"from":"militiamen","to":"players"}],"new_prediction":"Sports"}
```

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
{"ranking":["Baghdad","U.S.","Sadr","militia","forces"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `baghdad`(1), `u.s`(2), `sadr`(3), `militia`(4), `forces`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | 0.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article discusses airline companies' strategic expansion and competition, mentioning corporate actions such as Northwest Airlines' plans to grow in Indianapolis and the impact on rival ATA Airlines, which are clearly business-related topics."}
```

**Rationale text:**
> The article discusses airline companies' strategic expansion and competition, mentioning corporate actions such as Northwest Airlines' plans to grow in Indianapolis and the impact on rival ATA Airlines, which are clearly business-related topics.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `airlines`, `indianapolis`, `rival`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to World, Sports, Sci/Tech.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"edits":[{"from":"bankrupt","to":"tournament"}],"new_prediction":"Sports"}
```

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
{"ranking":["Northwest","Airlines","expand","rival","Nasdaq"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `northwest`(1), `airlines`(2), `expand`(3), `rival`(4), `nasdaq`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### sst2_validation_0003 (ECS=0.3667)
- **Dataset:** sst2
- **Text:** it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_0000 (ECS=0.3333)
- **Dataset:** mnli
- **Text:** Premise: Not yourself.
Hypothesis: Someone else
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓

### sst2_validation_0002 (ECS=0.0000)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓


## Low-ECS Examples

### sst2_validation_0002 (ECS=0.0000)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### mnli_validation_matched_0000 (ECS=0.3333)
- **Dataset:** mnli
- **Text:** Premise: Not yourself.
Hypothesis: Someone else
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓

### sst2_validation_0003 (ECS=0.3667)
- **Dataset:** sst2
- **Text:** it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
