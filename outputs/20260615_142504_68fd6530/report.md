# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 14:25:14
- **Duration:** 280.6s (4.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 8117
- **Avg tokens per instance:** 301

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | 10/10 (100%) | 0.685 | 100% | 100% | 50% | 90% |
| mnli | 9 | 7/9 (78%) | 0.696 | 78% | 78% | 11% | 78% |
| ag_news | 8 | 6/8 (75%) | 0.669 | 75% | 75% | 0% | 75% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 10 | 10 | 0 |
| mnli | 10 | 9 | 2 |
| ag_news | 10 | 8 | 2 |
| **Total** | 30 | 27 | 4 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=9) or medium-length (21–50 words, N=14). ECS may partly reflect brevity.

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
| Mean ECS (all, N=27) | 0.6840 |
| Mean ECS (primary: H,CF,RO) | 0.7150 |
| Mean ECS (complete cases, N=5) | 0.4717 |
| Complete cases | 5/27 (19%) |
| Primary ECS pairs <3 | 18 instances |
  → sst2_validation_0000: 1 pair(s), ECS_primary=0.8000
  → sst2_validation_0001: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0003: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0004: 1 pair(s), ECS_primary=0.6667
  → sst2_validation_0007: 1 pair(s), ECS_primary=1.0000
  → ... and 13 more
| Std ECS | 0.2135 |
| Median ECS | 0.6667 |
| Spearman ρ (confidence vs ECS) | 0.1282 (p=0.5598) — no significant association |
| Mean CC3 size | 2.81 |
| Mean CC4 size | 2.30 |
| % instances with CC3 | 85.2% |
| % instances with CC4 | 81.5% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.7170 |
| H–CF | 0.2194 |
| H–RO | 0.8361 |
| R–CF | 0.2583 |
| R–RO | 0.7159 |
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
| Short (≤20 words) | 9 | 0.6855 |
| Medium (21–50) | 14 | 0.6830 |
| Long (>50 words) | 0 | 0.0000 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.6840 | [0.6017, 0.7614] |
| Spearman ρ (self-reported confidence) | 0.1282 | [-0.3216, 0.6073] |

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
{"label": "negative", "confidence": 90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 33 words
- **Raw response length:** 39 chars
- **Prompt hash:** `ebbb14848c53a1f0`
- **ECS (full):** 0.5762
- **ECS (primary):** 0.8000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale": "The text is classified as negative because it states that the special effects and colors cannot hide the major flaw of the movie, which is the lack of a story.", "evidence": ["heel", "giant", "bold", "special", "hide"]}
```

**Rationale text:**
> The text is classified as negative because it states that the special effects and colors cannot hide the major flaw of the movie, which is the lack of a story.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bold`, `giant`, `heel`, `hide`, `special`

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
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.4286 |
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
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 3

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as negative because the phrase 'did it better' implies a comparison where the subject being referred to is inferior to Holden Caulfield.", "evidence":["better", "holden", "caulfield", "did"]}
```

**Rationale text:**
> The text is classified as negative because the phrase 'did it better' implies a comparison where the subject being referred to is inferior to Holden Caulfield.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `caulfield`, `holden`

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
{"ranking":["better", "holden", "did", "it", "caulfield"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`(1), `holden`(2), `caulfield`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
- **ECS (full):** 0.6000
- **ECS (primary):** 0.4667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 5 | **CC4 size:** 1

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
{"highlights":["fear", "cheap", "holocaust", "tension", "exploits"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploits`, `fear`, `holocaust`, `tension`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as negative because it uses words with negative connotations to describe the movie's approach to generating tension.", "evidence":["exploits", "fear", "cheap", "holocaust", "tension"]}
```

**Rationale text:**
> The text is classified as negative because it uses words with negative connotations to describe the movie's approach to generating tension.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploits`, `fear`, `holocaust`, `tension`

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
| H–R | 1.0000 |
| H–CF | 0.2000 |
| H–RO | 1.0000 |
| R–CF | 0.2000 |
| R–RO | 1.0000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.8000 |
| Normalized τ | 0.9000 |

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
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 5 | **CC4 size:** 5

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as positive because it describes the leads as bringing a 'fresh' and 'quirky charm' to the formula, indicating an appreciation for their unique qualities.", "evidence":["fresh", "quirky", "charm", "lead", "romantic"]}
```

**Rationale text:**
> The text is classified as positive because it describes the leads as bringing a 'fresh' and 'quirky charm' to the formula, indicating an appreciation for their unique qualities.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charm`, `fresh`, `lead`, `quirky`, `romantic`

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
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
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
- **ECS (full):** 0.6667
- **ECS (primary):** 0.6667
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
{"highlights":["control", "artist", "message", "jazzman", "improvise"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `message`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as positive because it describes the artist as being in control and able to improvise, implying a high level of skill and mastery.", "evidence":["control", "jazzman", "medium", "message", "improvise"]}
```

**Rationale text:**
> The text is classified as positive because it describes the artist as being in control and able to improvise, implying a high level of skill and mastery.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `control`, `improvise`, `jazzman`, `medium`, `message`

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
{"ranking":["artist", "control", "jazzman", "medium", "message"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`(1), `control`(2), `jazzman`(3), `medium`(4), `message`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

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
- **ECS (full):** 0.6000
- **ECS (primary):** 0.4667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 1

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as positive because it implies that the message 'love thyself' is beneficial and uplifting for young women, conveying a sense of self-acceptance and empowerment.","evidence":["love", "better", "young", "women", "thyself"]}
```

**Rationale text:**
> The text is classified as positive because it implies that the message 'love thyself' is beneficial and uplifting for young women, conveying a sense of self-acceptance and empowerment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `thyself`, `women`, `young`

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
| H–R | 1.0000 |
| H–CF | 0.2000 |
| H–RO | 1.0000 |
| R–CF | 0.2000 |
| R–RO | 1.0000 |
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
- **ECS (full):** 0.1944
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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as negative because it uses derogatory language to describe the artist's techniques, implying a lack of genuine skill or talent.", "evidence":["hack-artist", "ooky-spookies", "trick", "verbinski", "hacks"]}
```

**Rationale text:**
> The text is classified as negative because it uses derogatory language to describe the artist's techniques, implying a lack of genuine skill or talent.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `ooky-spookies`, `trick`, `verbinski`

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
| H–R | 0.1250 |
| H–CF | 0.0000 |
| H–RO | 0.6667 |
| R–CF | 0.2500 |
| R–RO | 0.1250 |
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
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 5 | **CC4 size:** 5

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as positive because it describes the leads as charming and having chemistry, which are desirable traits in a performance.","evidence":["charming","chemistry","lovers","leads","friends"]}
```

**Rationale text:**
> The text is classified as positive because it describes the leads as charming and having chemistry, which are desirable traits in a performance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`, `friends`, `leads`, `lovers`

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
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
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
- **ECS (full):** 0.5417
- **ECS (primary):** 0.4167
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 4 | **CC4 size:** 1

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
{"highlights":["coasting", "uncomfortably", "close", "thief", "in"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `close`, `coasting`, `thief`, `uncomfortably`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as negative because it implies that the subject is unoriginal and lacking in creativity, as evidenced by the use of words with negative connotations.", "evidence":["uncomfortably", "coasting", "thief", "close", "bicycle"]}
```

**Rationale text:**
> The text is classified as negative because it implies that the subject is unoriginal and lacking in creativity, as evidenced by the use of words with negative connotations.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bicycle`, `close`, `coasting`, `thief`, `uncomfortably`

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
| H–R | 0.8000 |
| H–CF | 0.2500 |
| H–RO | 0.8000 |
| R–CF | 0.2000 |
| R–RO | 1.0000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"highlights":["heart", "one", "from", "the", "one"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heart`, `one`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as positive because the phrase 'from the heart' is often associated with sincerity and genuine emotion, implying a positive sentiment.", "evidence":["heart", "one", "from"]}
```

**Rationale text:**
> The text is classified as positive because the phrase 'from the heart' is often associated with sincerity and genuine emotion, implying a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heart`, `one`

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
| H–R | 1.0000 |
| H–CF | 0.5000 |
| H–RO | — |
| R–CF | 0.5000 |
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
- **ECS (full):** 0.3476
- **ECS (primary):** 0.4000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 1 | **CC4 size:** 1

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the premise only mentions a summons for Dave Hanson, but does not provide information about the others' intentions or actions, making it neutral with respect to the hypothesis.", "evidence":["summons", "sternly", "Perth", "Dave", "Hanson"]}
```

**Rationale text:**
> The classification is correct because the premise only mentions a summons for Dave Hanson, but does not provide information about the others' intentions or actions, making it neutral with respect to the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dave`, `hanson`, `perth`, `sternly`, `summons`

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
| H–R | 0.1429 |
| H–CF | — |
| H–RO | 0.4000 |
| R–CF | — |
| R–RO | 0.5000 |
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
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `entailment`
- **CC3 size:** 5 | **CC4 size:** 5

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the premise explicitly states that there is a good profit sharing plan, but no profit, which directly supports the hypothesis.", "evidence":["profit", "sharing", "plan", "good", "money"]}
```

**Rationale text:**
> The classification is correct because the premise explicitly states that there is a good profit sharing plan, but no profit, which directly supports the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `money`, `plan`, `profit`, `sharing`

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
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
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
- **ECS (full):** 0.7778
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `contradiction`
- **CC3 size:** 4 | **CC4 size:** 4

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the premise states that Positano is located on the Amalfi coast, which directly contradicts the hypothesis that the Amalfi coast is far from Positano.", "evidence":["Sorrento", "Positano", "coast", "villages", "south"]}
```

**Rationale text:**
> The classification is correct because the premise states that Positano is located on the Amalfi coast, which directly contradicts the hypothesis that the Amalfi coast is far from Positano.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `coast`, `positano`, `sorrento`, `south`, `villages`

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
{"ranking":["south", "Positano", "coast", "of", "to"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `south`(1), `positano`(2), `coast`(3), `sorrento`(4), `amalfi`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.6667 |
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
{"label":"entailment", "confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 40 chars
- **Prompt hash:** `b34d47449d2d0db3`
- **ECS (full):** 0.7556
- **ECS (primary):** 0.8000
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
{"highlights":["defeated", "colleagues", "sadistic", "mostly", "when"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`, `defeated`, `mostly`, `sadistic`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the premise directly states that when his colleagues aren't sadistic, they are mostly defeated, which is exactly what the hypothesis claims.", "evidence":["defeated", "sadistic", "mostly", "colleagues", "disgust"]}
```

**Rationale text:**
> The classification is correct because the premise directly states that when his colleagues aren't sadistic, they are mostly defeated, which is exactly what the hypothesis claims.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`, `defeated`, `disgust`, `mostly`, `sadistic`

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
{"ranking":["defeated", "colleagues", "sadistic", "mostly", "when"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`(1), `sadistic`(2), `defeated`(3), `mostly`(4), `america`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.8000 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

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
- **ECS (full):** 1.0000
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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the premise advises to compare before buying, while the hypothesis suggests not to, which are opposite actions.", "evidence":["compare", "buying", "consider", "before", "don't"]}
```

**Rationale text:**
> The classification is correct because the premise advises to compare before buying, while the hypothesis suggests not to, which are opposite actions.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buying`, `compare`, `consider`

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
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
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
- **ECS (full):** 0.5667
- **ECS (primary):** 0.5000
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
{"highlights":["still", "refused", "driving", "are", "but"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `driving`, `refused`, `still`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the premise states that employers are still driving, which directly contradicts the hypothesis that employers have refused to continue driving.", "evidence":["still", "refused", "driving", "employers", "counts"]}
```

**Rationale text:**
> The classification is correct because the premise states that employers are still driving, which directly contradicts the hypothesis that employers have refused to continue driving.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `counts`, `driving`, `employers`, `refused`, `still`

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
- Tokens: `still`(1), `driving`(2), `employers`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.5000 |
| R–CF | — |
| R–RO | 0.6000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **ECS (full):** 0.4222
- **ECS (primary):** 0.4444
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 3 | **CC4 size:** 1

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the hypothesis is a paraphrased version of the premise, conveying the same information about Waters' earnings in 2000.", "evidence":["Waters", "earned", "65,000", "2000", "Waters'"]}
```

**Rationale text:**
> The classification is correct because the hypothesis is a paraphrased version of the premise, conveying the same information about Waters' earnings in 2000.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2000`, `65,000`, `earned`, `waters`

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
{"ranking":["Waters", "earned", "tax", "records", "2000"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `waters`(1), `earned`(2), `tax`(3), `records`(4), `2000`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | 0.1667 |
| H–RO | 1.0000 |
| R–CF | 0.2000 |
| R–RO | 0.5000 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"Business", "confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 38 chars
- **Prompt hash:** `6158484b6651713a`
- **ECS (full):** 0.7778
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 4 | **CC4 size:** 4

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as Business because it discusses a company's stock buyout offer, acquisition deal, and shareholder dispute, which are all typical business-related topics.", "evidence":["Mylan", "CEO", "shareholder", "acquire", "billion"]}
```

**Rationale text:**
> The text is classified as Business because it discusses a company's stock buyout offer, acquisition deal, and shareholder dispute, which are all typical business-related topics.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `acquire`, `billion`, `ceo`, `mylan`, `shareholder`

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
{"edits": [{"from": "Mylan", "to": "NASA"}, {"from": "King", "to": "CERN"}], "new_prediction": "Sci/Tech"}
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
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.6667 |
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
- **ECS (full):** 0.6667
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 3

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as World because it discusses a political incident involving a country's prime minister, which is a typical topic in global news.", "evidence":["Australian", "Prime", "Minister", "Howard", "transcripts"]}
```

**Rationale text:**
> The text is classified as World because it discusses a political incident involving a country's prime minister, which is a typical topic in global news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `howard`, `minister`, `prime`, `transcripts`

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
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.6667 |
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
{"label":"World", "confidence": 100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 36 chars
- **Prompt hash:** `8b17fb3cdddebeb7`
- **ECS (full):** 0.7778
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 4 | **CC4 size:** 4

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as World because it discusses international relations and a U.N. war crimes court, which are typical topics of global news.", "evidence":["U.N.", "Serbia", "Hague", "Belgrade", "Court"]}
```

**Rationale text:**
> The text is classified as World because it discusses international relations and a U.N. war crimes court, which are typical topics of global news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `belgrade`, `court`, `hague`, `serbia`, `u.n`

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
{"edits": [{"from": "U.N.", "to": "NBA"}, {"from": "war", "to": "championship"}], "new_prediction": "Sports"}
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
{"ranking":["U.N.", "war", "Serbia", "court", "Belgrade"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `u.n`(1), `war`(2), `serbia`(3), `court`(4), `belgrade`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.6667 |
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
- **ECS (full):** 0.6667
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 3 | **CC4 size:** 3

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as Sci/Tech because it discusses Microsoft, operating systems, and viruses, which are all related to technology and computing.", "evidence":["Microsoft", "viruses", "browser", "email", "patch"]}
```

**Rationale text:**
> The text is classified as Sci/Tech because it discusses Microsoft, operating systems, and viruses, which are all related to technology and computing.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `microsoft`, `patch`, `viruses`

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
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.5000 |
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
- **ECS (full):** 0.5079
- **ECS (primary):** 0.4286
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["United", "States", "Russia", "fouls", "turnovers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `russia`, `states`, `turnovers`, `united`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as Sports because it mentions a competition with scores and a player's name, indicating a sporting event.","evidence":["United", "Russia", "Sheryl", "Swoopes", "fouls"]}
```

**Rationale text:**
> The text is classified as Sports because it mentions a competition with scores and a player's name, indicating a sporting event.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `russia`, `sheryl`, `swoopes`, `united`

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
{"ranking":["United", "States", "Russia", "Sheryl", "Swoopes"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `united`(1), `states`(2), `russia`(3), `sheryl`(4), `swoopes`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | 0.6667 |
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
- **ECS (full):** 0.6190
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 3 | **CC4 size:** 3

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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text is classified as Sports because it mentions a tennis tournament and specific players, indicating a focus on athletic competition.","evidence":["Tennis", "Shanghai", "Guillermo", "Canas", "ATP"]}
```

**Rationale text:**
> The text is classified as Sports because it mentions a tennis tournament and specific players, indicating a focus on athletic competition.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `canas`, `guillermo`, `shanghai`, `tennis`

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
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.4286 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### mnli_validation_matched_0005 (ECS=1.0000)
- **Dataset:** mnli
- **Text:** Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%

### mnli_validation_matched_0002 (ECS=1.0000)
- **Dataset:** mnli
- **Text:** Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 90.0%

### sst2_validation_0007 (ECS=1.0000)
- **Dataset:** sst2
- **Text:** as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 90.0%


## Low-ECS Examples

### sst2_validation_0006 (ECS=0.1944)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 80.0%

### mnli_validation_matched_0001 (ECS=0.3476)
- **Dataset:** mnli
- **Text:** Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
- **Confidence:** 80.0%

### mnli_validation_matched_0008 (ECS=0.4222)
- **Dataset:** mnli
- **Text:** Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 100.0%
