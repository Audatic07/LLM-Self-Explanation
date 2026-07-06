# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 13:09:12
- **Duration:** 829.9s (13.8m)
- **Model:** openai/gpt-oss-120b:free
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 8030
- **Avg tokens per instance:** 297

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | — | 0.656 | 90% | 90% | 40% | 70% |
| mnli | 9 | — | 0.467 | 78% | 78% | 44% | 78% |
| ag_news | 8 | — | 0.568 | 100% | 100% | 12% | 100% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 10 | 10 | 1 |
| mnli | 10 | 9 | 2 |
| ag_news | 10 | 8 | 0 |
| **Total** | 30 | 27 | 3 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=8) or medium-length (21–50 words, N=14). ECS may partly reflect brevity.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=8)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 24/27 | 89% |
| Rationale | 24/27 | 89% |
| Counterfactual | 9/27 | 33% |
| Rank Ordering | 22/27 | 81% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=27) | 0.5678 |
| Mean ECS (primary: H,CF,RO) | 0.5603 |
| Mean ECS (complete cases, N=8) | 0.4463 |
| Complete cases | 8/27 (30%) |
| Primary ECS pairs <3 | 15 instances |
  → sst2_validation_0002: 1 pair(s), ECS_primary=0.6667
  → sst2_validation_0003: 1 pair(s), ECS_primary=0.8000
  → sst2_validation_0004: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0008: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0009: 1 pair(s), ECS_primary=0.5000
  → ... and 10 more
| Std ECS | 0.1867 |
| Median ECS | 0.5444 |
| Spearman ρ (confidence vs ECS) | -0.0465 (p=0.8333) — no significant association |
| Mean CC3 size | 2.74 |
| Mean CC4 size | 1.78 |
| % instances with CC3 | 85.2% |
| % instances with CC4 | 70.4% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.6751 |
| H–CF | 0.1648 |
| H–RO | 0.7065 |
| R–CF | 0.1593 |
| R–RO | 0.6750 |
| CF–RO | 0.1096 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 24/27 (89%) | 24/27 (89%) |
| Rationale | 24/27 (89%) | 24/27 (89%) |
| Counterfactual | 9/27 (33%) | 9/27 (33%) |
| CF flip verified | 9/9 (100%) |
| Rank Ordering | 22/27 (81%) | 22/27 (81%) |
| All 4 valid | 8/27 |
| 3 valid (CC3 adjusted) | 15/27 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 8 | 0.6336 |
| Medium (21–50) | 14 | 0.5438 |
| Long (>50 words) | 1 | 0.3778 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.5678 | [0.4978, 0.6473] |
| Spearman ρ (self-reported confidence) | -0.0465 | [-0.5244, 0.3702] |

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
{"label":"negative", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 33 words
- **Raw response length:** 37 chars
- **Prompt hash:** `ebbb14848c53a1f0`
- **ECS (full):** 0.4861
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
{"highlights":["no","achilles","heel","just","story"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `achilles`, `heel`, `no`, `story`

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
{"rationale":"The reviewer criticizes the film for lacking a story, calling its main flaw a 'giant Achilles' heel', which conveys a negative sentiment.","evidence":["no","story","giant","achilles","heel"]}
```

**Rationale text:**
> The reviewer criticizes the film for lacking a story, calling its main flaw a 'giant Achilles' heel', which conveys a negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `achilles`, `giant`, `heel`, `no`, `story`

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
{"edits": [{"from": "no", "to": "great"}], "new_prediction": "positive"}
```

**Reconstructed text:**
> very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just great story , folks . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `no`

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
{"ranking":["no","story","achilles","heel","can't"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `no`(1), `story`(2), `achilles`(3), `heel`(4), `n't`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.8000 |
| H–CF | 0.2500 |
| H–RO | 0.8000 |
| R–CF | 0.2000 |
| R–RO | 0.6667 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### sst2_validation_0001

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `positive` ✗
- **Input length:** 6 words
- **Raw response length:** 36 chars

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
{"label":"negative", "confidence": 92}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 38 chars
- **Prompt hash:** `632f05c570eb9781`
- **ECS (full):** 0.7778
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 4 | **CC4 size:** 4

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
{"highlights":["exploits","fear","holocaust","cheap","nuclear"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploits`, `fear`, `holocaust`, `nuclear`

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
{"rationale":"The text criticizes K-19 for using fear of nuclear disaster to create low-quality tension, conveying a negative judgment.","evidence":["exploits","fear","nuclear","holocaust","cheap"]}
```

**Rationale text:**
> The text criticizes K-19 for using fear of nuclear disaster to create low-quality tension, conveying a negative judgment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploits`, `fear`, `holocaust`, `nuclear`

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
{"edits": [{"from": "exploits", "to": "highlights"}], "new_prediction": "positive"}
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
{"ranking":["fear","holocaust","cheap","tension","nuclear"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fear`(1), `holocaust`(2), `cheap`(3), `tension`(4), `nuclear`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"positive", "confidence":90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 37 chars
- **Prompt hash:** `6d3cc2d0162fdf8d`
- **ECS (full):** 0.5762
- **ECS (primary):** 0.8000
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
{"highlights":["fresh","quirky","charm","bring","fresh"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bring`, `charm`, `fresh`, `quirky`

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
{"rationale":"The description highlights the actors' \"fresh\" and \"quirky\" charm, which conveys a positive appraisal despite noting they are not typical romantic leads.","evidence":["fresh","quirky","charm","typical","formula"]}
```

**Rationale text:**
> The description highlights the actors' "fresh" and "quirky" charm, which conveys a positive appraisal despite noting they are not typical romantic leads.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charm`, `formula`, `fresh`, `quirky`, `typical`

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
{"ranking":["fresh","quirky","charm","bring","positive"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fresh`(1), `quirky`(2), `charm`(3), `bring`(4), `lead`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.4286 |
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
{"label":"positive", "confidence":85}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 37 chars
- **Prompt hash:** `fe82006ca66ed1f5`
- **ECS (full):** 0.7778
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
{"highlights":["control","improvise","jazzman","artist","work"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `work`

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
{"rationale":"The description praises the artist's mastery and creative freedom, using positive language like 'control' and 'improvise', which conveys a favorable sentiment.","evidence":["artist","control","improvise","jazzman","medium"]}
```

**Rationale text:**
> The description praises the artist's mastery and creative freedom, using positive language like 'control' and 'improvise', which conveys a favorable sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `medium`

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
{"ranking":["control","improvise","jazzman","artist","work"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `control`(1), `improvise`(2), `jazzman`(3), `artist`(4), `work`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"positive","confidence":85}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 36 chars
- **Prompt hash:** `3fffe17d808c5583`
- **ECS (full):** 0.3611
- **ECS (primary):** 0.2333
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
{"highlights":["love","thyself","young","any","size"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`, `size`, `thyself`, `young`

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
{"rationale":"The phrase encourages self‑love, which conveys an uplifting and supportive sentiment toward women of any size.","evidence":["love","thyself","young","women","size"]}
```

**Rationale text:**
> The phrase encourages self‑love, which conveys an uplifting and supportive sentiment toward women of any size.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`, `size`, `thyself`, `women`, `young`

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
{"ranking":["love","thyself","better","young","women"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `thyself`(2), `better`(3), `young`(4), `women`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.8000 |
| H–CF | 0.0000 |
| H–RO | 0.5000 |
| R–CF | 0.0000 |
| R–RO | 0.6667 |
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
{"label":"negative", "confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 37 chars
- **Prompt hash:** `19716630de352c04`
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

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"highlights":["trick","implements","every","give","us"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `every`, `give`, `implements`, `trick`

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
{"rationale":"The wording conveys criticism by highlighting manipulative 'hack-artist' tricks and describing the result as 'ooky-spookies', indicating a negative view.","evidence":["hack-artist","trick","ooky-spookies","implements","every"]}
```

**Rationale text:**
> The wording conveys criticism by highlighting manipulative 'hack-artist' tricks and describing the result as 'ooky-spookies', indicating a negative view.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `every`, `hack-artist`, `implements`, `ooky-spookies`, `trick`

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
{"ranking":["trick"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
{"label":"positive", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 19 words
- **Raw response length:** 37 chars
- **Prompt hash:** `461ce7d654cf73ea`
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
{"highlights":["charming","chemistry","friends","lovers","leads"]}
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
{"rationale":"The description uses positive adjectives and highlights attractive interpersonal dynamics, indicating a favorable view.","evidence":["charming","chemistry","friends","lovers","leads"]}
```

**Rationale text:**
> The description uses positive adjectives and highlights attractive interpersonal dynamics, indicating a favorable view.

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
{"edits": [{"from": "charming", "to": "boring"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> as the two leads , lathan and diggs are boring and have chemistry both as friends and lovers . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`

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
{"ranking":["charming","chemistry","friends","lovers","leads"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`(1), `chemistry`(2), `friends`(3), `lovers`(4), `leads`(5)

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
{"label":"negative", "confidence": 82}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 82.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 38 chars
- **Prompt hash:** `68ac624bb5647ef1`
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 5 | **CC4 size:** 5

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
{"highlights":["uncomfortably","thief","close","coasting","treads"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `close`, `coasting`, `thief`, `treads`, `uncomfortably`

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
{"rationale":"The phrase uses negative descriptors like 'uncomfortably' and suggests an invasive, unsettling proximity, indicating a negative sentiment.","evidence":["uncomfortably","close","coasting","treads","thief"]}
```

**Rationale text:**
> The phrase uses negative descriptors like 'uncomfortably' and suggests an invasive, unsettling proximity, indicating a negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `close`, `coasting`, `thief`, `treads`, `uncomfortably`

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
{"ranking":["uncomfortably","thief","close","coasting","treads"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`(1), `thief`(2), `close`(3), `coasting`(4), `treads`(5)

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
{"label":"positive","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Input length:** 5 words
- **Raw response length:** 36 chars
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
{"highlights":["heart","one","from","the","one"]}
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
{
  "rationale":"The phrase conveys affection by referencing something that comes directly from the heart, which is inherently positive.",
  "evidence":["one","heart"]
}
```

**Rationale text:**
> The phrase conveys affection by referencing something that comes directly from the heart, which is inherently positive.

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
{"edits": [{"from": "heart", "to": "pain"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> one from the pain . 

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
{"ranking":["heart","one","from","the"]}
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
- **Raw response length:** 42 chars

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
{"label":"neutral", "confidence":85}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 26 words
- **Raw response length:** 36 chars
- **Prompt hash:** `5d436fd01abbdb0b`
- **ECS (full):** 0.3587
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["only","others","protect","went","summons"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `others`, `protect`, `summons`, `went`

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
{
  "rationale":"The premise states that only Dave Hanson was summoned, but it gives no information about the others' intentions, so it neither supports nor contradicts the hypothesis that they went to protect him.",
  "evidence":["summons","only","Dave","Hanson","three"]
}
```

**Rationale text:**
> The premise states that only Dave Hanson was summoned, but it gives no information about the others' intentions, so it neither supports nor contradicts the hypothesis that they went to protect him.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dave`, `hanson`, `summons`, `three`

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
{"edits": null, "new_prediction": null}
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
{"ranking":["only","others","summons","Dave","protect"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `summons`(1), `others`(2), `protect`(3), `dave`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | -0.3333 |
| Normalized τ | 0.3333 |

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
{"label":"entailment", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 39 chars
- **Prompt hash:** `ed542e8118eca549`
- **ECS (full):** 0.4889
- **ECS (primary):** 0.3556
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 4 | **CC4 size:** 1

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
{"highlights":["good","sharing","no","profit","money"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `money`, `no`, `profit`, `sharing`

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
{
  "rationale":"Both sentences state that the profit‑sharing arrangement is good but lacks any actual profit or money, so the hypothesis follows from the premise.",
  "evidence":["good","profit","sharing","plan","no"]
}
```

**Rationale text:**
> Both sentences state that the profit‑sharing arrangement is good but lacks any actual profit or money, so the hypothesis follows from the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `no`, `plan`, `profit`, `sharing`

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
{"edits": [{"from": "good", "to": "bad"}], "new_prediction": "neutral"}
```

**Reconstructed text:**
> Premise: but like they always say you know got a bad profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`

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
{"ranking":["good","profit","sharing","no","plan"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`(1), `profit`(2), `sharing`(3), `no`(4), `plan`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | 0.2000 |
| H–RO | 0.6667 |
| R–CF | 0.2000 |
| R–RO | 1.0000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

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
{"label":"contradiction", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 42 chars
- **Prompt hash:** `fd7769715006e52e`
- **ECS (full):** 0.3889
- **ECS (primary):** 0.2222
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 4 | **CC4 size:** 0

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
{"highlights":["Positano","Amalfi","coast","villages","south"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `coast`, `positano`, `south`, `villages`

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
{
  "rationale":"The premise states that Positano is located on the Amalfi coast, directly contradicting the hypothesis that the Amalfi coast is far from Positano.",
  "evidence":["Positano","Amalfi","coast","villages","south"]
}
```

**Rationale text:**
> The premise states that Positano is located on the Amalfi coast, directly contradicting the hypothesis that the Amalfi coast is far from Positano.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `coast`, `positano`, `south`, `villages`

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
{"edits": [{"from": "far", "to": "near"}], "new_prediction": "entailment"}
```

**Reconstructed text:**
> Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is near from Positano.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `far`

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
{"ranking":["Positano","Amalfi","coast","south","spill"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `positano`(1), `amalfi`(2), `coast`(3), `south`(4), `spill`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.0000 |
| H–RO | 0.6667 |
| R–CF | 0.0000 |
| R–RO | 0.6667 |
| CF–RO | 0.0000 |
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
{"label":"entailment", "confidence": 95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 40 chars
- **Prompt hash:** `b34d47449d2d0db3`
- **ECS (full):** 0.3675
- **ECS (primary):** 0.2137
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
{"highlights":["mostly","defeated","sadistic","when","aren't"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defeated`, `mostly`, `sadistic`

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
{
  "rationale":"The premise states that when colleagues aren't sadistic, they are mostly defeated, which directly matches the hypothesis.",
  "evidence":["mostly","defeated","sadistic","aren't","when"]
}
```

**Rationale text:**
> The premise states that when colleagues aren't sadistic, they are mostly defeated, which directly matches the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defeated`, `mostly`, `sadistic`

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
{
  "edits": [
    {
      "from": "mostly",
      "to": "sometimes"
    }
  ],
  "new_prediction": "neutral"
}
```

**Reconstructed text:**
> Premise: In America, his colleagues are sometimes defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mostly`

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
{"ranking":["defeated","sadistic","mostly","when","aren’t"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `america`(1), `colleagues`(2), `mostly`(3), `defeated`(4), `miss`(5), `mudd`(6), `predecessor`(7), `first`(8), `job`(9), `retired`(10), `early`(11), `disgust`(12), `sadistic`(13)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.3333 |
| H–RO | 0.2308 |
| R–CF | 0.3333 |
| R–RO | 0.2308 |
| CF–RO | 0.0769 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"contradiction", "confidence": 95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 17 words
- **Raw response length:** 43 chars
- **Prompt hash:** `2f89b9a7a4a49b69`
- **ECS (full):** 0.5000
- **ECS (primary):** 0.3333
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 3 | **CC4 size:** 0

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
{"highlights":["look","compare","before","Don't","consider"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `compare`, `consider`, `look`

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
{
  "rationale":"The premise advises looking and comparing before buying, while the hypothesis advises not to consider and compare, directly opposing the premise.",
  "evidence":["look","compare","before","Don't","consider"]
}
```

**Rationale text:**
> The premise advises looking and comparing before buying, while the hypothesis advises not to consider and compare, directly opposing the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `compare`, `consider`, `look`

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
{
  "edits": [
    {
      "from": "Don't",
      "to": "Do"
    }
  ],
  "new_prediction": "entailment"
}
```

**Reconstructed text:**
> Premise: Be sure to look around and compare before buying.
Hypothesis: Do consider and compare before buying.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `Don't`

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
{"ranking":["don't","look","compare","consider"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `look`(1), `compare`(2), `consider`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.0000 |
| H–RO | 1.0000 |
| R–CF | 0.0000 |
| R–RO | 1.0000 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0006

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: It's come back? cried Julius excitedly.
Hypothesis: They thought it was gone forever.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"neutral","confidence":85}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 35 chars
- **Prompt hash:** `f92a3adae42b6d61`
- **ECS (full):** 0.6190
- **ECS (primary):** 0.4286
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 3 | **CC4 size:** 3

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
{"highlights":["back","gone","forever","excitedly","thought"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`, `excitedly`, `forever`, `gone`, `thought`

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
{
  "rationale":"The premise only shows surprise at something returning, without indicating any prior belief that it was gone forever, so the hypothesis is not entailed nor contradicted.",
  "evidence":["excitedly","Julius","cried","back","gone"]
}
```

**Rationale text:**
> The premise only shows surprise at something returning, without indicating any prior belief that it was gone forever, so the hypothesis is not entailed nor contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`, `cried`, `excitedly`, `gone`, `julius`

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
{"edits": [{"from": "excitedly", "to": "relieved"}], "new_prediction": "entailment"}
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
{"ranking":["back","gone","excitedly","cried","Julius"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`(1), `gone`(2), `excitedly`(3), `cried`(4), `julius`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"contradiction", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 18 words
- **Raw response length:** 42 chars
- **Prompt hash:** `728037a82366269d`
- **ECS (full):** 0.5444
- **ECS (primary):** 0.8000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["still","driving","refused","continue","all"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `continue`, `driving`, `refused`, `still`

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
{
  "rationale":"The premise states that employers are still driving, which directly opposes the hypothesis that they have refused to continue driving.",
  "evidence":["employers","still","driving","counts"]
}
```

**Rationale text:**
> The premise states that employers are still driving, which directly opposes the hypothesis that they have refused to continue driving.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `counts`, `driving`, `employers`, `still`

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
{"edits": [{"from": "still", "to": "no longer"}], "new_prediction": "entailment"}
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
{"ranking":["still","refused","continue","driving","employers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `still`(1), `refused`(2), `continue`(3), `driving`(4), `employers`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### mnli_validation_matched_0008

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `entailment`
- **Predicted:** `neutral` ✗
- **Input length:** 24 words
- **Raw response length:** 36 chars

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
{"label":"Business", "confidence": 92}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 38 chars
- **Prompt hash:** `6158484b6651713a`
- **ECS (full):** 0.2917
- **ECS (primary):** 0.2500
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 1 | **CC4 size:** 1

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
{"highlights":["stock","buyout","shareholder","deal","acquire"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `acquire`, `buyout`, `deal`, `shareholder`, `stock`

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
{
  "rationale": "The article discusses a shareholder dispute over a multi‑billion‑dollar corporate acquisition, which is a business‑related topic.",
  "evidence": ["Icahn","CEO","Mylan","buyout","acquisition"]
}
```

**Rationale text:**
> The article discusses a shareholder dispute over a multi‑billion‑dollar corporate acquisition, which is a business‑related topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buyout`, `ceo`, `icahn`, `mylan`

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
{"edits": [{"from": "Mylan", "to": "FIFA"}], "new_prediction": "Sports"}
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
{"ranking":["Mylan","Icahn","Coury","buyout","deal"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mylan`(1), `icahn`(2), `coury`(3), `buyout`(4), `deal`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1250 |
| H–CF | — |
| H–RO | 0.2500 |
| R–CF | — |
| R–RO | 0.5000 |
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
{"label":"World", "confidence": 92}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 35 chars
- **Prompt hash:** `508b76f724cb3bc4`
- **ECS (full):** 0.5079
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
{"highlights":["Australian","Howard","children","overboard","pressure"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `children`, `howard`, `overboard`, `pressure`

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
{"rationale":"The article discusses political controversy involving the Australian Prime Minister and a national rescue incident, which falls under international or domestic political news, a subcategory of World news.","evidence":["Australian","Prime","Minister","Howard","children"]}
```

**Rationale text:**
> The article discusses political controversy involving the Australian Prime Minister and a national rescue incident, which falls under international or domestic political news, a subcategory of World news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `children`, `howard`, `minister`, `prime`

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
{"edits": [{"from": "Australian", "to": "NBA"}], "new_prediction": "Sports"}
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
{"ranking":["Australian","children","overboard","rescue","Howard"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`(1), `children`(2), `overboard`(3), `rescue`(4), `howard`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.4286 |
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
{"label":"World", "confidence": 92}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 35 chars
- **Prompt hash:** `8b17fb3cdddebeb7`
- **ECS (full):** 0.5873
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
{"highlights":["war","court","Serbia","prosecutor","Hague"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `court`, `hague`, `prosecutor`, `serbia`, `war`

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
{"rationale":"The article discusses a United Nations war crimes court transferring a case to Serbia, which is an international political/legal matter, fitting the World news category.","evidence":["U.N.","War","Court","Serbia","Reuters"]}
```

**Rationale text:**
> The article discusses a United Nations war crimes court transferring a case to Serbia, which is an international political/legal matter, fitting the World news category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `court`, `reuters`, `serbia`, `u.n`, `war`

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
{"edits": [{"from": "War", "to": "Championship"}], "new_prediction": "Sports"}
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
{"ranking":["U.N.","War","Court","Serbia","Hague"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `u.n`(1), `war`(2), `court`(3), `serbia`(4), `hague`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 0.6667 |
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
{"label":"Sci/Tech", "confidence": 92}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 38 chars
- **Prompt hash:** `1662f7e986ec19ce`
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 5 | **CC4 size:** 5

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
{"highlights":["Microsoft","Security","patch","operating","viruses"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`, `operating`, `patch`, `security`, `viruses`

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
{"rationale":"The article discusses a Microsoft security patch and virus attacks on software, which are topics related to technology.", "evidence":["Microsoft","Security","patch","viruses","operating"]}
```

**Rationale text:**
> The article discusses a Microsoft security patch and virus attacks on software, which are topics related to technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`, `operating`, `patch`, `security`, `viruses`

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
{"edits": [{"from": "Microsoft", "to": "UN"}], "new_prediction": "World"}
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
{"ranking":["Microsoft","Security","patch","viruses","operating"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `security`(2), `patch`(3), `viruses`(4), `operating`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### ag_news_test_0004

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Boxer Begs Bush to Back Bum Bill Members of California's congressional team make one last effort to look good for the tech industry back home."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{
  "label": "Business",
  "confidence": 70
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 70.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 45 chars
- **Prompt hash:** `8a64396178009ff8`
- **ECS (full):** 0.4484
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 2 | **CC4 size:** 2

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
{
  "highlights": ["tech", "industry", "bill", "members", "congressional"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bill`, `congressional`, `industry`, `members`, `tech`

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
{
  "rationale": "The article mentions a legislative \"Bum Bill\" and references the tech industry, indicating a focus on political and economic issues rather than sports or science.",
  "evidence": ["Boxer","Bush","Bum","Bill","tech"]
}
```

**Rationale text:**
> The article mentions a legislative "Bum Bill" and references the tech industry, indicating a focus on political and economic issues rather than sports or science.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bill`, `boxer`, `bum`, `bush`, `tech`

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
{
  "edits": [
    {
      "from": "Boxer",
      "to": "Athlete"
    }
  ],
  "new_prediction": "Sports"
}
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
{
  "ranking": ["Bill", "tech", "industry", "congressional", "Bush"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bill`(1), `tech`(2), `industry`(3), `congressional`(4), `bush`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.4286 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### ag_news_test_0005

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "More Older People Turning to the Internet to Find Love Mary Bellis Waller, now 64, posted on two Internet dating sites during her search for a companion. Waller was a pioneer of online dating among people her age, and thousands of others age 60 and older are also turning to the Internet to find romance."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{"label":"Sci/Tech", "confidence":70}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 70.0%
- **Model refused:** No
- **Input length:** 55 words
- **Raw response length:** 37 chars
- **Prompt hash:** `ce6a7f2c178e4783`
- **ECS (full):** 0.3778
- **ECS (primary):** 0.2667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `World`
- **CC3 size:** 4 | **CC4 size:** 0

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
{"highlights":["Internet","online","dating","search","technology"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dating`, `internet`, `online`, `search`

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
{"rationale":"The article discusses how seniors are using digital platforms for dating, which pertains to technology and its societal impact, fitting the Sci/Tech category.","evidence":["Internet","dating","online","search","romance"]}
```

**Rationale text:**
> The article discusses how seniors are using digital platforms for dating, which pertains to technology and its societal impact, fitting the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dating`, `internet`, `online`, `romance`, `search`

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
{"edits": [{"from": "Internet", "to": "Olympics"}], "new_prediction": "Sports"}
```

**Reconstructed text:**
> More Older People Turning to the Olympics to Find Love Mary Bellis Waller, now 64, posted on two Internet dating sites during her search for a companion. Waller was a pioneer of online dating among people her age, and thousands of others age 60 and older are also turning to the Internet to find romance.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `Internet`

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
{"ranking":["Internet","online","dating","search","people"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `internet`(1), `online`(2), `dating`(3), `search`(4), `people`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.8000 |
| H–CF | 0.0000 |
| H–RO | 0.8000 |
| R–CF | 0.0000 |
| R–RO | 0.6667 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"Sports", "confidence": 92}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 36 chars
- **Prompt hash:** `265eb84f94f4d713`
- **ECS (full):** 0.6667
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 4 | **CC4 size:** 4

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
{"highlights":["fouls","turnovers","opponent","United","Russia"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `opponent`, `russia`, `turnovers`, `united`

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
{"rationale":"The article mentions a scoreline between two nations, fouls, turnovers, and a basketball star, all of which are typical elements of a sports report.", "evidence":["United","States","Russia","fouls","turnovers"]}
```

**Rationale text:**
> The article mentions a scoreline between two nations, fouls, turnovers, and a basketball star, all of which are typical elements of a sports report.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `russia`, `states`, `turnovers`, `united`

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
{"edits": [{"from": "fouls", "to": "sanctions"}], "new_prediction": "World"}
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
{"ranking":["fouls","turnovers","United","Russia","Swoopes"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`(1), `turnovers`(2), `united`(3), `russia`(4), `swoopes`(5)

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
{"label":"Sports", "confidence": 99}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 99.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 36 chars
- **Prompt hash:** `41f4d8d8e7436a00`
- **ECS (full):** 0.6667
- **ECS (primary):** 0.6667
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
{"highlights":["Tennis","Canas","Novak","ATP","final"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `canas`, `final`, `novak`, `tennis`

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
{"rationale":"The article reports on a tennis match result and the players advancing to the final of an ATP tournament, which is clearly a sports topic.","evidence":["Tennis","Canas","Novak","Shanghai","ATP"]}
```

**Rationale text:**
> The article reports on a tennis match result and the players advancing to the final of an ATP tournament, which is clearly a sports topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `canas`, `novak`, `shanghai`, `tennis`

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
{"edits": [{"from": "ATP", "to": "stock"}], "new_prediction": "Business"}
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
{"ranking":["Canas","Novak","Shanghai","final","tennis"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `canas`(1), `novak`(2), `shanghai`(3), `final`(4), `tennis`(5)

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


## High-ECS Examples

### ag_news_test_0003 (ECS=1.0000)
- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 92.0%

### sst2_validation_0008 (ECS=1.0000)
- **Dataset:** sst2
- **Text:** comes ... uncomfortably close to coasting in the treads of the bicycle thief . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 82.0%

### sst2_validation_0004 (ECS=0.7778)
- **Dataset:** sst2
- **Text:** it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 85.0%


## Low-ECS Examples

### ag_news_test_0000 (ECS=0.2917)
- **Dataset:** ag_news
- **Text:** Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pha…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 92.0%

### mnli_validation_matched_0001 (ECS=0.3587)
- **Dataset:** mnli
- **Text:** Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
- **Confidence:** 85.0%

### sst2_validation_0005 (ECS=0.3611)
- **Dataset:** sst2
- **Text:** what better message than ` love thyself ' could young women of any size receive ? 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 85.0%
