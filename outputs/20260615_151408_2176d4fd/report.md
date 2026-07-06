# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 15:14:18
- **Duration:** 281.3s (4.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 8273
- **Avg tokens per instance:** 306

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | 10/10 (100%) | 0.456 | 100% | 100% | 50% | 90% |
| mnli | 9 | 7/9 (78%) | 0.378 | 78% | 78% | 11% | 78% |
| ag_news | 8 | 6/8 (75%) | 0.357 | 75% | 75% | 0% | 75% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 10 | 10 | 0 |
| mnli | 10 | 9 | 2 |
| ag_news | 10 | 8 | 2 |
| **Total** | 30 | 27 | 4 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=9) or medium-length (21–50 words, N=14). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=11). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=5)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 23/27 | 85% |
| Rationale | 23/27 | 85% |
| Counterfactual | 6/27 | 22% |
| Rank Ordering | 22/27 | 81% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=27) | 0.4063 |
| Mean ECS (primary: H,CF,RO) | 0.7148 |
| Mean ECS (complete cases, N=5) | 0.2994 |
| Complete cases | 5/27 (19%) |
| Primary ECS pairs <3 | 18 instances |
  → sst2_validation_0000: 1 pair(s), ECS_primary=0.8000
  → sst2_validation_0001: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0003: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0004: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0007: 1 pair(s), ECS_primary=1.0000
  → ... and 13 more
| Std ECS | 0.1741 |
| Median ECS | 0.3333 |
| Spearman ρ (confidence vs ECS) | -0.1685 (p=0.4421) — no significant association |
| Mean CC3 size | 1.37 |
| Mean CC4 size | 1.07 |
| % instances with CC3 | 63.0% |
| % instances with CC4 | 51.9% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.2302 |
| H–CF | 0.2194 |
| H–RO | 0.8360 |
| R–CF | 0.2333 |
| R–RO | 0.2437 |
| CF–RO | 0.1533 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 23/27 (85%) | 23/27 (85%) |
| Rationale | 23/27 (85%) | 23/27 (85%) |
| Counterfactual | 6/27 (22%) | 6/27 (22%) |
| CF flip verified | 6/6 (100%) |
| Rank Ordering | 22/27 (81%) | 22/27 (81%) |
| All 4 valid | 5/27 |
| 3 valid (CC3 adjusted) | 18/27 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 9 | 0.4366 |
| Medium (21–50) | 14 | 0.3869 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 12 | 0.3780 |
| Short vocab (≤20 unique tokens) | 11 | 0.4373 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.4063 | [0.3362, 0.4747] |
| Spearman ρ (self-reported confidence) | -0.1685 | [-0.5833, 0.2103] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"negative", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 33 words
- **Raw response length:** 38 chars
- **Prompt hash:** `ebbb14848c53a1f0`
- **ECS (full):** 0.3143
- **ECS (primary):** 0.8000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["heel", "giant", "hide", "just", "no"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `giant`, `heel`, `hide`, `no`

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
{"rationale":"The text receives a negative classification because it states that the impressive visual elements of the movie cannot compensate for its major flaw, which is the lack of a compelling story, indicating an overall unfavorable opinion of the film."}
```

**Rationale text:**
> The text receives a negative classification because it states that the impressive visual elements of the movie cannot compensate for its major flaw, which is the lack of a compelling story, indicating an overall unfavorable opinion of the film.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heighten`, `little`, `story`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Specify exactly ONE or TWO individual word replacements that would flip the classification to positive instead of negative. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: positive>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "hide", "to": "show"}, {"from": "can't", "to": "can"}], "new_prediction": "positive"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["heel", "no", "hide", "giant", "story"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heel`(1), `no`(2), `hide`(3), `giant`(4), `story`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.1429 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "holden caulfield did it better . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"negative", "confidence": 80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 6 words
- **Raw response length:** 38 chars
- **Prompt hash:** `ba03e9c7e06ebe6b`
- **ECS (full):** 0.5556
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["better", "did", "holden", "it", "caulfield"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `caulfield`, `holden`

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
{"rationale":"The text receives a negative classification because it implies that the current subject is being compared unfavorably to Holden Caulfield, suggesting that the speaker believes the subject has done something worse or less effectively than Caulfield."}
```

**Rationale text:**
> The text receives a negative classification because it implies that the current subject is being compared unfavorably to Holden Caulfield, suggesting that the speaker believes the subject has done something worse or less effectively than Caulfield.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `caulfield`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Specify exactly ONE or TWO individual word replacements that would flip the classification to positive instead of negative. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: positive>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "better", "to": "worse"}], "new_prediction": "positive"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["better", "did", "holden", "it", "caulfield"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`(1), `caulfield`(2), `holden`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### sst2_validation_0002

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"negative", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 38 chars
- **Prompt hash:** `632f05c570eb9781`
- **ECS (full):** 0.4095
- **ECS (primary):** 0.4667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["fear", "cheap", "tension", "holocaust", "exploits"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploits`, `fear`, `holocaust`, `tension`

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
{"rationale":"The text receives a negative classification because it criticizes the film's method of creating tension, implying that it relies on a cheap and exploitative tactic to evoke fear, which suggests a disapproving tone towards the film's approach."}
```

**Rationale text:**
> The text receives a negative classification because it criticizes the film's method of creating tension, implying that it relies on a cheap and exploitative tactic to evoke fear, which suggests a disapproving tone towards the film's approach.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `fear`, `generate`, `substantial`, `tension`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Specify exactly ONE or TWO individual word replacements that would flip the classification to positive instead of negative. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: positive>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "cheap", "to": "gripping"}], "new_prediction": "positive"}
```

**Reconstructed text:**
> k-19 exploits our substantial collective fear of nuclear holocaust to generate gripping hollywood tension . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["cheap", "fear", "holocaust", "tension", "exploits"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`(1), `fear`(2), `holocaust`(3), `tension`(4), `exploits`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | 0.2000 |
| H–RO | 1.0000 |
| R–CF | 0.2000 |
| R–RO | 0.4286 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.6000 |
| Normalized τ | 0.8000 |

### sst2_validation_0003

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"positive", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 38 chars
- **Prompt hash:** `6d3cc2d0162fdf8d`
- **ECS (full):** 0.5833
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["fresh", "charm", "quirky", "romantic", "lead"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charm`, `fresh`, `lead`, `quirky`, `romantic`

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
{"rationale":"The text receives a positive classification because it describes the leads as bringing a unique and appealing quality to the formula, implying that their unconventional nature is a refreshing asset rather than a liability."}
```

**Rationale text:**
> The text receives a positive classification because it describes the leads as bringing a unique and appealing quality to the formula, implying that their unconventional nature is a refreshing asset rather than a liability.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `formula`, `fresh`, `lead`, `neither`, `romantic`, `typical`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Specify exactly ONE or TWO individual word replacements that would flip the classification to negative instead of positive. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "fresh", "to": "stale"}], "new_prediction": "negative"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["fresh", "charm", "quirky", "romantic", "lead"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fresh`(1), `charm`(2), `quirky`(3), `romantic`(4), `lead`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3750 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.3750 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### sst2_validation_0004

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"positive", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 38 chars
- **Prompt hash:** `fe82006ca66ed1f5`
- **ECS (full):** 0.7143
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["control", "artist", "message", "jazzman", "improvise"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `message`

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
{"rationale":"The text receives a positive classification because it describes the artist as being in control of their medium and message, implying a high level of skill and mastery, and also makes a favorable comparison to a jazzman, which is often associated with creative genius and improvisational expertise."}
```

**Rationale text:**
> The text receives a positive classification because it describes the artist as being in control of their medium and message, implying a high level of skill and mastery, and also makes a favorable comparison to a jazzman, which is often associated with creative genius and improvisational expertise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `like`, `medium`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Specify exactly ONE or TWO individual word replacements that would flip the classification to negative instead of positive. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "control", "to": "chaos"}], "new_prediction": "negative"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["artist", "control", "jazzman", "message", "improvise"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`(1), `control`(2), `jazzman`(3), `message`(4), `improvise`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5714 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.5714 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.6000 |
| Normalized τ | 0.8000 |

### sst2_validation_0005

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "what better message than ` love thyself ' could young women of any size receive ? "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"positive", "confidence": 95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 38 chars
- **Prompt hash:** `3fffe17d808c5583`
- **ECS (full):** 0.3167
- **ECS (primary):** 0.4667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["love", "better", "young", "women", "thyself"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `thyself`, `women`, `young`

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
{"rationale":"The text receives a positive classification because it presents a supportive and uplifting message, implying that self-love is a valuable and beneficial concept, particularly for young women, which conveys an overall tone of encouragement and empowerment."}
```

**Rationale text:**
> The text receives a positive classification because it presents a supportive and uplifting message, implying that self-love is a valuable and beneficial concept, particularly for young women, which conveys an overall tone of encouragement and empowerment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`, `message`, `receive`, `woman`, `young`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Specify exactly ONE or TWO individual word replacements that would flip the classification to negative instead of positive. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "better", "to": "worse"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> what worse message than ` love thyself ' could young women of any size receive ? 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["love", "better", "young", "women", "thyself"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `better`(2), `young`(3), `women`(4), `thyself`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | 0.2000 |
| H–RO | 1.0000 |
| R–CF | 0.0000 |
| R–RO | 0.2500 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### sst2_validation_0006

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "verbinski implements every hack-artist trick to give us the ooky-spookies . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"negative", "confidence": 80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 38 chars
- **Prompt hash:** `19716630de352c04`
- **ECS (full):** 0.1905
- **ECS (primary):** 0.2222
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["hack", "ooky", "spookies", "every", "trick"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `every`, `hack`, `ooky`, `spookies`, `trick`

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
{"rationale":"The text receives a negative classification because the tone is dismissive and mocking, implying that the filmmaker's use of techniques to create a spooky atmosphere is unoriginal and lacking in genuine artistry."}
```

**Rationale text:**
> The text receives a negative classification because the tone is dismissive and mocking, implying that the filmmaker's use of techniques to create a spooky atmosphere is unoriginal and lacking in genuine artistry.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `give`, `ooky`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Specify exactly ONE or TWO individual word replacements that would flip the classification to positive instead of negative. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
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

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["hack", "trick", "ooky", "spookies", "artist"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack`(1), `trick`(2), `ooky`(3), `spookies`(4), `artist`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | 0.0000 |
| H–RO | 0.6667 |
| R–CF | 0.0000 |
| R–RO | 0.3333 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### sst2_validation_0007

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"positive", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 19 words
- **Raw response length:** 38 chars
- **Prompt hash:** `461ce7d654cf73ea`
- **ECS (full):** 0.5238
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["charming", "chemistry", "lovers", "friends", "leads"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`, `friends`, `leads`, `lovers`

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
{"rationale":"The text receives a positive classification because it describes the two leads as charming and having chemistry, which implies a strong and enjoyable on-screen presence that contributes to a favorable impression."}
```

**Rationale text:**
> The text receives a positive classification because it describes the two leads as charming and having chemistry, which implies a strong and enjoyable on-screen presence that contributes to a favorable impression.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`, `lead`, `lover`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Specify exactly ONE or TWO individual word replacements that would flip the classification to negative instead of positive. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "charming", "to": "awkward"}], "new_prediction": "negative"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["charming", "chemistry", "lovers", "leads", "friends"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`(1), `chemistry`(2), `lovers`(3), `leads`(4), `friends`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2857 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.2857 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.8000 |
| Normalized τ | 0.9000 |

### sst2_validation_0008

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"negative", "confidence": 80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 38 chars
- **Prompt hash:** `68ac624bb5647ef1`
- **ECS (full):** 0.2833
- **ECS (primary):** 0.4167
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["uncomfortably", "coasting", "close", "thief", "in"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `close`, `coasting`, `thief`, `uncomfortably`

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
{"rationale":"The text receives a negative classification because it implies that the subject is unoriginal and lacking in creativity, by suggesting that it is simply following in the footsteps of another work, 'the bicycle thief', without adding anything new or innovative."}
```

**Rationale text:**
> The text receives a negative classification because it implies that the subject is unoriginal and lacking in creativity, by suggesting that it is simply following in the footsteps of another work, 'the bicycle thief', without adding anything new or innovative.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `thief`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Specify exactly ONE or TWO individual word replacements that would flip the classification to positive instead of negative. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: positive>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "uncomfortably", "to": "comfortably"}], "new_prediction": "positive"}
```

**Reconstructed text:**
> comes ... comfortably close to coasting in the treads of the bicycle thief . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["coasting", "uncomfortably", "close", "thief", "bicycle"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `coasting`(1), `uncomfortably`(2), `close`(3), `thief`(4), `bicycle`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | 0.2500 |
| H–RO | 0.8000 |
| R–CF | 0.0000 |
| R–RO | 0.2000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |

### sst2_validation_0009

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "one from the heart . "

Return only valid JSON:
{"label":"positive or negative", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"positive", "confidence": 80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 5 words
- **Raw response length:** 38 chars
- **Prompt hash:** `0e78d798fc6c570a`
- **ECS (full):** 0.6667
- **ECS (primary):** 0.5000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["heart", "one", "from", "the"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heart`, `one`

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
{"rationale":"The text receives a positive classification because the phrase as a whole implies a sense of sincerity and genuineness, which is typically associated with favorable emotions and intentions."}
```

**Rationale text:**
> The text receives a positive classification because the phrase as a whole implies a sense of sincerity and genuineness, which is typically associated with favorable emotions and intentions.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heart`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Specify exactly ONE or TWO individual word replacements that would flip the classification to negative instead of positive. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "heart", "to": "nightmare"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> one from the nightmare . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heart`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["heart", "one", "from", "the"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | 0.5000 |
| H–RO | — |
| R–CF | 1.0000 |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Input length:** 22 words
- **Raw response length:** 44 chars

### mnli_validation_matched_0001

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"neutral", "confidence": 80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 26 words
- **Raw response length:** 37 chars
- **Prompt hash:** `5d436fd01abbdb0b`
- **ECS (full):** 0.1889
- **ECS (primary):** 0.4000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["said", "only", "three", "Dave", "to"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dave`, `said`, `three`

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
{"rationale":"The text receives a neutral classification because it only mentions that the summons was specifically for Dave Hanson, without providing any information about the actions or intentions of the other individuals involved, leaving their motivations and behaviors uncertain."}
```

**Rationale text:**
> The text receives a neutral classification because it only mentions that the summons was specifically for Dave Hanson, without providing any information about the actions or intentions of the other individuals involved, leaving their motivations and behaviors uncertain.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hanson`, `sternly`, `summon`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to entailment, contradiction instead of neutral. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "Perth", "to": "Bodyguard"}], "new_prediction": "entailment"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: neutral

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["only", "Dave", "summons", "Hanson", "three"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `summons`(1), `dave`(2), `hanson`(3), `three`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.4000 |
| R–CF | — |
| R–RO | 0.1667 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"entailment", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 40 chars
- **Prompt hash:** `ed542e8118eca549`
- **ECS (full):** 0.6667
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `entailment`
- **CC3 size:** 4 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["profit", "good", "plan", "sharing", "money"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `money`, `plan`, `profit`, `sharing`

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
{"rationale":"The text receives this classification because the premise describes a situation where a profit sharing plan exists, but there is no profit to share, which directly supports the hypothesis that it's a good way of sharing money, but there's no money, thereby establishing a logical entailment between the two statements."}
```

**Rationale text:**
> The text receives this classification because the premise describes a situation where a profit sharing plan exists, but there is no profit to share, which directly supports the hypothesis that it's a good way of sharing money, but there's no money, thereby establishing a logical entailment between the two statements.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `hypothesis`, `money`, `plan`, `premise`, `profit`, `way`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to neutral, contradiction instead of entailment. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "profit", "to": "loss"}], "new_prediction": "contradiction"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["profit", "good", "plan", "sharing", "money"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `profit`(1), `good`(2), `plan`(3), `sharing`(4), `money`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0003

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"contradiction", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 44 chars
- **Prompt hash:** `fd7769715006e52e`
- **ECS (full):** 0.3333
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `contradiction`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["south", "Sorrento", "Positano", "coast", "Amalfi"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `coast`, `positano`, `sorrento`, `south`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives this classification because it describes Positano as one of the former fishing villages that spill down the craggy cliffs of the Amalfi coast, indicating a close proximity between the two, which directly contradicts the hypothesis that the Amalfi coast is far from Positano."}
```

**Rationale text:**
> The text receives this classification because it describes Positano as one of the former fishing villages that spill down the craggy cliffs of the Amalfi coast, indicating a close proximity between the two, which directly contradicts the hypothesis that the Amalfi coast is far from Positano.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cliff`, `coast`, `craggy`, `drive`, `former`, `hypothesis`, `one`, `positano`, `village`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to entailment, neutral instead of contradiction. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"edits": [{"from": "south", "to": "north"}], "new_prediction": "neutral"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["south", "Positano", "coast", "Amalfi", "villages"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `south`(1), `positano`(2), `coast`(3), `amalfi`(4), `villages`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1667 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.1667 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0004

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"entailment", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 41 chars
- **Prompt hash:** `b34d47449d2d0db3`
- **ECS (full):** 0.1788
- **ECS (primary):** 0.3077
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `entailment`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["defeated", "colleagues", "sadistic", "mostly", "when"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`, `defeated`, `mostly`, `sadistic`

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
{"rationale":"The text receives this classification because the premise directly states that his colleagues are mostly defeated when they aren't sadistic, which is a clear and direct affirmation of the hypothesis, indicating a logical entailment relationship between the two statements."}
```

**Rationale text:**
> The text receives this classification because the premise directly states that his colleagues are mostly defeated when they aren't sadistic, which is a clear and direct affirmation of the hypothesis, indicating a logical entailment relationship between the two statements.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleague`, `early`, `hypothesis`, `premise`, `retire`, `sadistic`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to neutral, contradiction instead of entailment. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "America", "to": "Utopia"}], "new_prediction": "contradiction"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["defeated", "sadistic", "colleagues", "mostly", "when"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`(1), `mostly`(2), `defeated`(3), `sadistic`(4), `america`(5), `retired`(6), `early`(7), `disgust`(8), `first`(9), `job`(10), `predecessor`(11), `miss`(12), `mudd`(13)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1111 |
| H–CF | — |
| H–RO | 0.3077 |
| R–CF | — |
| R–RO | 0.1176 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### mnli_validation_matched_0005

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"contradiction", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 17 words
- **Raw response length:** 44 chars
- **Prompt hash:** `2f89b9a7a4a49b69`
- **ECS (full):** 0.7333
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `contradiction`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["before", "compare", "buying", "consider", "and"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buying`, `compare`, `consider`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives this classification because the premise advises to compare before buying, which directly opposes the hypothesis that suggests not considering and comparing before making a purchase, indicating a clear contradictory relationship between the two statements."}
```

**Rationale text:**
> The text receives this classification because the premise advises to compare before buying, which directly opposes the hypothesis that suggests not considering and comparing before making a purchase, indicating a clear contradictory relationship between the two statements.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buying`, `compare`, `consider`, `hypothesis`, `premise`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to entailment, neutral instead of contradiction. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"edits": [{"from": "before", "to": "after"}], "new_prediction": "entailment"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["before", "compare", "buying", "consider", "and"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `compare`(1), `buying`(2), `consider`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.6000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0006

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 14 words
- **Raw response length:** 40 chars

### mnli_validation_matched_0007

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"contradiction", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 18 words
- **Raw response length:** 44 chars
- **Prompt hash:** `728037a82366269d`
- **ECS (full):** 0.2500
- **ECS (primary):** 0.7500
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `contradiction`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["still", "refused", "driving", "are", "but"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `driving`, `refused`, `still`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text is classified as a contradiction because the premise states that employers are still driving, which directly opposes the hypothesis that employers have refused to continue driving, indicating a clear and opposing relationship between the two statements."}
```

**Rationale text:**
> The text is classified as a contradiction because the premise states that employers are still driving, which directly opposes the hypothesis that employers have refused to continue driving, indicating a clear and opposing relationship between the two statements.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `continue`, `employer`, `hypothesis`, `premise`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to entailment, neutral instead of contradiction. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"edits": [{"from": "refused", "to": "agreed"}, {"from": "employers", "to": "employees"}], "new_prediction": "neutral"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["still", "refused", "driving", "employers", "have"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `still`(1), `refused`(2), `driving`(3), `employers`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.7500 |
| R–CF | — |
| R–RO | 0.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0008

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"entailment", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 41 chars
- **Prompt hash:** `7596e1e223125816`
- **ECS (full):** 0.2972
- **ECS (primary):** 0.4444
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["Waters", "earned", "tax", "records", "2000"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2000`, `earned`, `records`, `tax`, `waters`

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
{"rationale":"The premise and hypothesis are classified as entailment because the hypothesis is a paraphrased version of the premise, conveying the same information about Waters' earnings in 2000, with the only difference being the tone and wording used to express the information."}
```

**Rationale text:**
> The premise and hypothesis are classified as entailment because the hypothesis is a paraphrased version of the premise, conveying the same information about Waters' earnings in 2000, with the only difference being the tone and wording used to express the information.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2000`, `earn`, `hypothesis`, `premise`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to neutral, contradiction instead of entailment. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "Waters", "to": "Johnson"}, {"from": "2000", "to": "2010"}], "new_prediction": "neutral"}
```

**Reconstructed text:**
> Premise: Tax records show Johnson earned around $65,000 in 2010.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2000`, `Waters`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Waters", "earned", "2000", "tax", "records"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `waters`(1), `earned`(2), `2000`(3), `tax`(4), `records`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1250 |
| H–CF | 0.1667 |
| H–RO | 1.0000 |
| R–CF | 0.2000 |
| R–RO | 0.1250 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pharmaceuticals Inc."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"Business", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 39 chars
- **Prompt hash:** `6158484b6651713a`
- **ECS (full):** 0.2593
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["Mylan", "billion", "CEO", "shareholder", "acquire"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `acquire`, `billion`, `ceo`, `mylan`, `shareholder`

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
{"rationale":"The text receives this classification because it discusses a corporate deal, a stock buyout offer, and a disagreement between a company and its largest shareholder, all of which are typical of business and finance news."}
```

**Rationale text:**
> The text receives this classification because it discusses a corporate deal, a stock buyout offer, and a disagreement between a company and its largest shareholder, all of which are typical of business and finance news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `company`, `deal`, `laboratories`, `large`, `offer`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to World, Sports, Sci/Tech instead of Business. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "Mylan", "to": "NASA"}, {"from": "King", "to": "SpaceX"}], "new_prediction": "Sci/Tech"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Mylan", "billion", "CEO", "shareholder", "deal"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mylan`(1), `billion`(2), `ceo`(3), `shareholder`(4), `deal`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.1111 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sea rescue of boatpeople."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"World", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 36 chars
- **Prompt hash:** `508b76f724cb3bc4`
- **ECS (full):** 0.3704
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["Australian", "Prime", "Minister", "incident", "transcripts"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `incident`, `minister`, `prime`, `transcripts`

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
{"rationale":"The text receives a World classification because it discusses a significant political event involving the Australian Prime Minister and a controversial sea rescue, which are typical topics covered in international news and global affairs."}
```

**Rationale text:**
> The text receives a World classification because it discusses a significant political event involving the Australian Prime Minister and a controversial sea rescue, which are typical topics covered in international news and global affairs.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `controversial`, `critic`, `minister`, `official`, `transcript`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to Sports, Business, Sci/Tech instead of World. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "Prime", "to": "Coach"}, {"from": "Minister", "to": "MVP"}], "new_prediction": "Sports"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Australian", "Prime", "Minister", "incident", "Howard"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`(1), `prime`(2), `minister`(3), `incident`(4), `howard`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2222 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.2222 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"World", "confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 35 chars
- **Prompt hash:** `8b17fb3cdddebeb7`
- **ECS (full):** 0.3333
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["U.N.", "War", "Court", "Serbia", "Belgrade"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `belgrade`, `court`, `serbia`, `u.n`, `war`

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
{"rationale":"The text receives this classification because it discusses a significant international event involving the United Nations and a specific country, Serbia, which are typical subjects of world news."}
```

**Rationale text:**
> The text receives this classification because it discusses a significant international event involving the United Nations and a specific country, Serbia, which are typical subjects of world news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `crime`, `prosecutor`, `send`, `transfers`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to Sports, Business, Sci/Tech instead of World. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "Court", "to": "Stadium"}], "new_prediction": "Sports"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["U.N.", "war", "court", "Serbia", "Belgrade"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `u.n`(1), `war`(2), `court`(3), `serbia`(4), `belgrade`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"Sci/Tech", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 38 chars
- **Prompt hash:** `1662f7e986ec19ce`
- **ECS (full):** 0.5000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["Microsoft", "viruses", "operating", "system", "browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `microsoft`, `operating`, `system`, `viruses`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives this classification because it discusses specific technology-related issues, such as viruses attacking Microsoft's operating system, Web browser, and e-mail programs, which are all core components of the tech industry."}
```

**Rationale text:**
> The text receives this classification because it discusses specific technology-related issues, such as viruses attacking Microsoft's operating system, Web browser, and e-mail programs, which are all core components of the tech industry.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `market`, `microsoft`, `security`, `system`, `virus`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to World, Sports, Business instead of Sci/Tech. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"edits": [{"from": "Microsoft", "to": "Government"}], "new_prediction": "Business"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Microsoft", "viruses", "operating", "system", "browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `viruses`(2), `operating`(3), `system`(4), `browser`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.2500 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### ag_news_test_0004

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Input length:** 25 words
- **Raw response length:** 38 chars

### ag_news_test_0005

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sci/Tech`
- **Predicted:** `World` ✗
- **Input length:** 55 words
- **Raw response length:** 35 chars

### ag_news_test_0006

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "United States 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"Sports", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 37 chars
- **Prompt hash:** `265eb84f94f4d713`
- **ECS (full):** 0.2222
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["United", "States", "Russia", "fouls", "turnovers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `russia`, `states`, `turnovers`, `united`

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
{"rationale":"The text receives this classification because it describes a competitive event with a final score, mentions a specific player, and conveys a sense of urgency and teamwork, all of which are characteristic of a sports game."}
```

**Rationale text:**
> The text receives this classification because it describes a competitive event with a final score, mentions a specific player, and conveys a sense of urgency and teamwork, all of which are characteristic of a sports game.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `along`, `desperately`, `feisty`, `frustrate`, `swoopes`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to World, Business, Sci/Tech instead of Sports. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "United States", "to": "Microsoft"}, {"from": "Russia", "to": "Google"}], "new_prediction": "Business"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["United", "States", "Russia", "Sheryl", "fouls"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `united`(1), `states`(2), `russia`(3), `sheryl`(4), `fouls`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0007

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"Sports", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 37 chars
- **Prompt hash:** `41f4d8d8e7436a00`
- **ECS (full):** 0.4545
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["Tennis", "Shanghai", "Open", "ATP", "final"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `final`, `open`, `shanghai`, `tennis`

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
{"rationale":"The text receives this classification because it specifically mentions a tennis tournament, including the names of players and the details of the competition, which are all characteristic elements of a sports news report."}
```

**Rationale text:**
> The text receives this classification because it specifically mentions a tennis tournament, including the names of players and the details of the competition, which are all characteristic elements of a sports news report.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `argentina`, `dominate`, `german`, `open`, `place`, `reach`, `tennis`, `tournament`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Specify exactly ONE or TWO topic-specific word replacements (proper nouns, domain terms, named entities) that would flip the classification to World, Business, Sci/Tech instead of Sports. Each replacement: (1) must replace a single word from the original text, and (2) the replacement word must come from outside the text.

Return only valid JSON. If no single-word or two-word replacement can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "Tennis", "to": "Economy"}], "new_prediction": "Business"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Tennis", "Shanghai", "Open", "ATP", "final"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tennis`(1), `shanghai`(2), `open`(3), `atp`(4), `final`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1818 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.1818 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### mnli_validation_matched_0005 (ECS=0.7333)
- **Dataset:** mnli
- **Text:** Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%

### sst2_validation_0004 (ECS=0.7143)
- **Dataset:** sst2
- **Text:** it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 90.0%

### mnli_validation_matched_0002 (ECS=0.6667)
- **Dataset:** mnli
- **Text:** Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 90.0%


## Low-ECS Examples

### mnli_validation_matched_0004 (ECS=0.1788)
- **Dataset:** mnli
- **Text:** Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sa…
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 100.0%

### mnli_validation_matched_0001 (ECS=0.1889)
- **Dataset:** mnli
- **Text:** Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
- **Confidence:** 80.0%

### sst2_validation_0006 (ECS=0.1905)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 80.0%
