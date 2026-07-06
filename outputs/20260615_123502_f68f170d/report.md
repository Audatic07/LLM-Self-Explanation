# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 12:35:15
- **Duration:** 516.6s (8.6m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 8212
- **Avg tokens per instance:** 304

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | — | 0.626 | 80% | 90% | 40% | 80% |
| mnli | 9 | — | 0.554 | 89% | 89% | 22% | 89% |
| ag_news | 8 | — | 0.609 | 75% | 100% | 0% | 100% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 10 | 10 | 1 |
| mnli | 10 | 9 | 1 |
| ag_news | 10 | 8 | 0 |
| **Total** | 30 | 27 | 2 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=8) or medium-length (21–50 words, N=13). ECS may partly reflect brevity.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=5)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 22/27 | 81% |
| Rationale | 25/27 | 93% |
| Counterfactual | 6/27 | 22% |
| Rank Ordering | 24/27 | 89% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=27) | 0.5951 |
| Mean ECS (primary: H,CF,RO) | 0.6736 |
| Mean ECS (complete cases, N=5) | 0.5344 |
| Complete cases | 5/27 (19%) |
| Primary ECS pairs <3 | 17 instances |
  → sst2_validation_0000: 1 pair(s), ECS_primary=0.4286
  → sst2_validation_0002: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0003: 1 pair(s), ECS_primary=0.8000
  → sst2_validation_0006: 1 pair(s), ECS_primary=0.6000
  → sst2_validation_0008: 1 pair(s), ECS_primary=1.0000
  → ... and 12 more
| Std ECS | 0.1897 |
| Median ECS | 0.5556 |
| Spearman ρ (confidence vs ECS) | 0.0706 (p=0.7550) — no significant association |
| Mean CC3 size | 2.48 |
| Mean CC4 size | 1.93 |
| % instances with CC3 | 81.5% |
| % instances with CC4 | 81.5% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.6457 |
| H–CF | 0.2367 |
| H–RO | 0.7607 |
| R–CF | 0.2583 |
| R–RO | 0.5807 |
| CF–RO | 0.2200 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 22/27 (81%) | 22/27 (81%) |
| Rationale | 25/27 (93%) | 25/27 (93%) |
| Counterfactual | 6/27 (22%) | 6/27 (22%) |
| CF flip verified | 6/6 (100%) |
| Rank Ordering | 24/27 (89%) | 24/27 (89%) |
| All 4 valid | 5/27 |
| 3 valid (CC3 adjusted) | 17/27 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 8 | 0.6292 |
| Medium (21–50) | 13 | 0.5695 |
| Long (>50 words) | 1 | 0.6556 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.5951 | [0.5234, 0.6783] |
| Spearman ρ (self-reported confidence) | 0.0706 | [-0.2760, 0.4818] |

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
{"label":"negative","confidence":85}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 33 words
- **Raw response length:** 36 chars
- **Prompt hash:** `ebbb14848c53a1f0`
- **ECS (full):** 0.4048
- **ECS (primary):** 0.4286
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
{"highlights":["no","story","hide","achilles","heel"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `achilles`, `heel`, `hide`, `no`, `story`

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
{"rationale":"The review highlights the film's lack of story and calls its only redeeming feature an Achilles' heel, indicating a negative assessment.","evidence":["hide","giant","achilles","story","just"]}
```

**Rationale text:**
> The review highlights the film's lack of story and calls its only redeeming feature an Achilles' heel, indicating a negative assessment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `achilles`, `giant`, `hide`, `story`

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
{"ranking":["no","n't","heel","giant","hide"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `no`(1), `n't`(2), `heel`(3), `giant`(4), `hide`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | 0.2857 |
| CF–RO | — |
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
{"label":"negative","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 36 chars
- **Prompt hash:** `632f05c570eb9781`
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
{"highlights":["exploits","holocaust","fear","cheap","tension"]}
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
{"rationale":"The text criticizes the work as exploiting fear of nuclear disaster to create cheap, sensational tension, which conveys a negative judgment.","evidence":["exploits","fear","holocaust","cheap","tension"]}
```

**Rationale text:**
> The text criticizes the work as exploiting fear of nuclear disaster to create cheap, sensational tension, which conveys a negative judgment.

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
{"edits": [{"from": "exploits", "to": "celebrates"}], "new_prediction": "positive"}
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
{"ranking":["fear","holocaust","exploits","cheap","tension"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fear`(1), `holocaust`(2), `exploits`(3), `cheap`(4), `tension`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |

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
{"label":"positive","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 36 chars
- **Prompt hash:** `6d3cc2d0162fdf8d`
- **ECS (full):** 0.6556
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
{"highlights":["fresh","quirky","charm","bring","romantic"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bring`, `charm`, `fresh`, `quirky`, `romantic`

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
{"rationale":"The description uses positively‑valued adjectives such as \"fresh,\" \"quirky,\" and \"charm,\" indicating a favorable view.","evidence":["fresh","quirky","charm","romantic","lead"]}
```

**Rationale text:**
> The description uses positively‑valued adjectives such as "fresh," "quirky," and "charm," indicating a favorable view.

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
{"ranking":["charm","fresh","quirky","bring"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charm`(1), `fresh`(2), `quirky`(3), `bring`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

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
{"label":"positive","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 36 chars
- **Prompt hash:** `fe82006ca66ed1f5`
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
{"highlights":["control","improvise","artist","work","jazzman"]}
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
{"rationale":"The passage praises the artist’s mastery and improvisational skill, conveying a clearly positive sentiment.","evidence":["work","artist","control","improvise","jazzman"]}
```

**Rationale text:**
> The passage praises the artist’s mastery and improvisational skill, conveying a clearly positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `work`

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
{"edits": [{"from": "artist", "to": "charlatan"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> it 's a work by an charlatan so in control of both his medium and his message that he can improvise like a jazzman . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`

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
| H–R | 1.0000 |
| H–CF | 0.2000 |
| H–RO | 1.0000 |
| R–CF | 0.2000 |
| R–RO | 1.0000 |
| CF–RO | 0.2000 |
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
{"label":"positive","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 36 chars
- **Prompt hash:** `3fffe17d808c5583`
- **ECS (full):** 0.4889
- **ECS (primary):** 0.3556
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 4 | **CC4 size:** 1

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
{"highlights":["love","better","message","young","women"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `message`, `women`, `young`

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
{"rationale":"The text encourages self‑love and empowerment, which conveys a positive sentiment.","evidence":["love","better","message","young","women"]}
```

**Rationale text:**
> The text encourages self‑love and empowerment, which conveys a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `message`, `women`, `young`

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
{"edits": [{"from": "love", "to": "hate"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> what better message than ` hate thyself ' could young women of any size receive ? 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`

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
{"ranking":["love","better","young","women","any"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `better`(2), `young`(3), `women`(4), `receive`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.2000 |
| H–RO | 0.6667 |
| R–CF | 0.2000 |
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
{"label":"negative","confidence":70}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 70.0%
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 36 chars
- **Prompt hash:** `19716630de352c04`
- **ECS (full):** 0.3143
- **ECS (primary):** 0.6000
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
{"highlights":["trick","verbinski","implements","every","give"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `every`, `give`, `implements`, `trick`, `verbinski`

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
{"rationale":"The description calls the director's methods \"hack-artist\" and \"trick,\" which are derogatory terms indicating a negative assessment.","evidence":["hack-artist","trick","ooky-spookies"]}
```

**Rationale text:**
> The description calls the director's methods "hack-artist" and "trick," which are derogatory terms indicating a negative assessment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `ooky-spookies`, `trick`

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
{"edits":[{"from":"trick","to":"treat"}],"new_prediction":"positive"}
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
{"ranking":["trick","verbinski","implements"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `trick`(1), `verbinski`(2), `implements`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.2000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"positive","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 19 words
- **Raw response length:** 36 chars
- **Prompt hash:** `461ce7d654cf73ea`
- **ECS (full):** 0.5417
- **ECS (primary):** 0.4167
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 4 | **CC4 size:** 1

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
{"rationale":"The description praises the leads as charming with chemistry, emphasizing their positive relationship as friends and lovers.","evidence":["charming","chemistry","friends","lovers","leads"]}
```

**Rationale text:**
> The description praises the leads as charming with chemistry, emphasizing their positive relationship as friends and lovers.

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
{"ranking":["charming","chemistry","friends","lovers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`(1), `chemistry`(2), `friends`(3), `lovers`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.2000 |
| H–RO | 0.8000 |
| R–CF | 0.2000 |
| R–RO | 0.8000 |
| CF–RO | 0.2500 |
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
{"label":"negative", "confidence":85}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 37 chars
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
{"highlights":["uncomfortably","thief","close","treads","coasting"]}
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
{"rationale":"The words \"uncomfortably\" and \"thief\" convey a negative, uneasy feeling, justifying the negative label.","evidence":["uncomfortably","thief","close","treads","coasting"]}
```

**Rationale text:**
> The words "uncomfortably" and "thief" convey a negative, uneasy feeling, justifying the negative label.

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
{"ranking":["uncomfortably","thief","close","treads","coasting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`(1), `thief`(2), `close`(3), `treads`(4), `coasting`(5)

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

Identify the 5 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3","token4","token5"]}
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

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual SINGLE WORDS from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences. Do not include stopwords (like "the", "and", "it", "of").

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The word \"heart\" signals an emotional, sincere expression, which justifies a positive sentiment classification.","evidence":["one","heart"]}
```

**Rationale text:**
> The word "heart" signals an emotional, sincere expression, which justifies a positive sentiment classification.

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
{"edits": [{"from": "heart", "to": "hate"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> one from the hate . 

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
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | 0.5000 |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0000

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: It spoke of thousands of years, even before the times of the old empire.
Hypothesis: The old Empire is still ongoing.

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction", "confidence": <integer 0-100>}
```

#### 2. Classification Response
```
{
  "label": "neutral",
  "confidence": 90
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 44 chars
- **Prompt hash:** `ccd9492861a422f2`
- **ECS (full):** 0.5111
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

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
{
  "highlights": ["before", "thousands", "old", "empire.", "times"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `empire`, `old`, `thousands`, `times`

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
  "rationale": "The premise only references the old empire as a past period and does not state whether it continues, so it neither entails nor contradicts the hypothesis.",
  "evidence": ["thousands", "years", "before", "old", "empire"]
}
```

**Rationale text:**
> The premise only references the old empire as a past period and does not state whether it continues, so it neither entails nor contradicts the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `empire`, `old`, `thousands`, `years`

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
{
  "ranking": ["before", "old", "empire", "times", "spoke"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `old`(1), `empire`(2), `times`(3), `spoke`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
{"label":"neutral","confidence":90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Input length:** 26 words
- **Raw response length:** 35 chars
- **Prompt hash:** `5d436fd01abbdb0b`
- **ECS (full):** 0.6333
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["only","summons","others","protect","went"]}
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
  "rationale":"The premise only states that the summons was for Dave Hanson and does not indicate whether others acted to protect him, so it neither entails nor contradicts the hypothesis.",
  "evidence":["summons","Dave","Hanson","others","protect"]
}
```

**Rationale text:**
> The premise only states that the summons was for Dave Hanson and does not indicate whether others acted to protect him, so it neither entails nor contradicts the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dave`, `hanson`, `others`, `protect`, `summons`

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
{"ranking":["only","others","protect","summons","Dave"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `others`(1), `protect`(2), `summons`(3), `dave`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.8000 |
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
- **ECS (full):** 0.4861
- **ECS (primary):** 0.4167
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
{"highlights":["good","sharing","but","no","profit"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `no`, `profit`, `sharing`

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
{"rationale":"The premise says there is a good profit‑sharing plan but no profit, which directly matches the hypothesis that it is a good way of sharing money yet there is no money.","evidence":["good","profit","sharing","plan","no"]}
```

**Rationale text:**
> The premise says there is a good profit‑sharing plan but no profit, which directly matches the hypothesis that it is a good way of sharing money yet there is no money.

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
{"edits": [{"from": "good", "to": "bad"}], "new_prediction": "contradiction"}
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
{"ranking":["good","sharing","no","profit","money"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`(1), `sharing`(2), `no`(3), `profit`(4), `money`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.8000 |
| H–CF | 0.2500 |
| H–RO | 0.8000 |
| R–CF | 0.2000 |
| R–RO | 0.6667 |
| CF–RO | 0.2000 |
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
- **ECS (full):** 0.5556
- **ECS (primary):** 0.5000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["Positano","Amalfi","coast","south","spill"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `coast`, `positano`, `south`, `spill`

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
{"rationale":"The premise states that Positano is located on the Amalfi coast, so they are not far apart, contradicting the hypothesis.","evidence":["Positano","Amalfi","coast","spill","cliffs"]}
```

**Rationale text:**
> The premise states that Positano is located on the Amalfi coast, so they are not far apart, contradicting the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `cliffs`, `coast`, `positano`, `spill`

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
{"ranking":["Positano","Amalfi","coast","far","from"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `positano`(1), `amalfi`(2), `coast`(3), `far`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 0.5000 |
| R–CF | — |
| R–RO | 0.5000 |
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
{"label":"entailment","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 38 chars
- **Prompt hash:** `b34d47449d2d0db3`
- **ECS (full):** 0.5556
- **ECS (primary):** 0.4444
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
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
{"highlights":["defeated","mostly","when","aren't","sadistic"]}
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
{"rationale":"The premise explicitly says that when his colleagues aren't sadistic, they are mostly defeated, which matches the hypothesis.", "evidence":["colleagues","mostly","defeated","when","sadistic"]}
```

**Rationale text:**
> The premise explicitly says that when his colleagues aren't sadistic, they are mostly defeated, which matches the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`, `defeated`, `mostly`, `sadistic`

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
{"edits": [{"from": "mostly", "to": "never"}], "new_prediction": "contradiction"}
```

**Reconstructed text:**
> Premise: In America, his colleagues are never defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
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
{"ranking":["defeated","sadistic","mostly","when","colleagues"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defeated`(1), `mostly`(2), `sadistic`(3), `colleagues`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.7500 |
| H–CF | 0.3333 |
| H–RO | 0.7500 |
| R–CF | 0.2500 |
| R–RO | 1.0000 |
| CF–RO | 0.2500 |
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
{"label":"contradiction", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 17 words
- **Raw response length:** 42 chars
- **Prompt hash:** `2f89b9a7a4a49b69`
- **ECS (full):** 0.5222
- **ECS (primary):** 0.6667
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
{"highlights":["Don't","sure","look","consider","compare"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `compare`, `consider`, `look`, `sure`

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
{"rationale":"The premise tells you to compare before buying, whereas the hypothesis tells you not to consider and compare, directly opposing the premise.","evidence":["look","compare","before","buying","Don't"]}
```

**Rationale text:**
> The premise tells you to compare before buying, whereas the hypothesis tells you not to consider and compare, directly opposing the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buying`, `compare`, `look`

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
{"ranking":["Don't","Be","look","consider","compare"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sure`(1), `look`(2), `around`(3), `compare`(4), `buying`(5), `consider`(6)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.6667 |
| Normalized τ | 0.8333 |

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
{"label":"neutral","confidence":70}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 70.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 35 chars
- **Prompt hash:** `f92a3adae42b6d61`
- **ECS (full):** 0.5000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

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
{"highlights":["back","excitedly","thought","gone","forever"]}
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
{"rationale":"The premise only shows surprise at a return, without indicating any prior belief that it was gone forever, so it neither entails nor contradicts the hypothesis.","evidence":["come","back","cried","Julius","excitedly"]}
```

**Rationale text:**
> The premise only shows surprise at a return, without indicating any prior belief that it was gone forever, so it neither entails nor contradicts the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`, `come`, `cried`, `excitedly`, `julius`

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
{"ranking":["back?","gone","thought","excitedly","forever"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`(1), `gone`(2), `thought`(3), `excitedly`(4), `forever`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.2500 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |

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
- **ECS (full):** 0.6667
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["refused","still","continue","driving","employers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `continue`, `driving`, `employers`, `refused`, `still`

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
{"rationale":"The premise states that employers are still driving, directly opposing the hypothesis that they have refused to continue driving, making the statements contradictory.","evidence":["employers","still","driving","all","counts"]}
```

**Rationale text:**
> The premise states that employers are still driving, directly opposing the hypothesis that they have refused to continue driving, making the statements contradictory.

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
{"ranking":["refused","still","continue","driving","employers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `refused`(1), `still`(2), `continue`(3), `driving`(4), `employers`(5)

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

### mnli_validation_matched_0008

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `entailment`
- **Predicted:** `neutral` ✗
- **Input length:** 24 words
- **Raw response length:** 44 chars

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
{"label":"Business","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 36 chars
- **Prompt hash:** `6158484b6651713a`
- **ECS (full):** 0.5000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["deal","buyout","stock","shareholder","acquire"]}
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
  "rationale":"The article discusses a shareholder dispute over a corporate acquisition and stock buyout, which are topics of business news.",
  "evidence":["Icahn","CEO","Mylan","stock","deal"]
}
```

**Rationale text:**
> The article discusses a shareholder dispute over a corporate acquisition and stock buyout, which are topics of business news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ceo`, `deal`, `icahn`, `mylan`, `stock`

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
{"ranking":["stock","deal","buyout","shareholder","acquire"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `stock`(1), `deal`(2), `buyout`(3), `shareholder`(4), `acquire`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.2500 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.6000 |
| Normalized τ | 0.8000 |

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
{"label":"World", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 34 chars
- **Prompt hash:** `508b76f724cb3bc4`
- **ECS (full):** 0.2632
- **ECS (primary):** 0.4286
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

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
{"highlights":["Australian","PM","Howard","transcripts","rescue"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `howard`, `pm`, `rescue`, `transcripts`

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
{
  "rationale":"The article discusses political controversy surrounding a 2001 sea rescue and the Australian Prime Minister, which are matters of international and national affairs, fitting the World news category.",
  "evidence":["Australian","Prime","minister","controversial","rescue"]
}
```

**Rationale text:**
> The article discusses political controversy surrounding a 2001 sea rescue and the Australian Prime Minister, which are matters of international and national affairs, fitting the World news category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `controversial`, `minister`, `prime`, `rescue`

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
{"ranking":["Australian","PM","Howard","children","overboard"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`(1), `pm`(2), `howard`(3), `children`(4), `overboard`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | 0.1111 |
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
{"label":"World", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 34 chars
- **Prompt hash:** `8b17fb3cdddebeb7`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
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

```

**Parsed tokens:**
- *Not parsed*

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
{"rationale":"The article discusses a United Nations war crimes court transferring a case to Serbia, which is a matter of international affairs, fitting the World category.","evidence":["U.N.","War","court","Serbia","Reuters"]}
```

**Rationale text:**
> The article discusses a United Nations war crimes court transferring a case to Serbia, which is a matter of international affairs, fitting the World category.

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
{
  "edits": [
    {
      "from": "War",
      "to":
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
{"ranking":["War","Serbia","court","U.N.","Hague"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `war`(1), `serbia`(2), `court`(3), `u.n`(4), `hague`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
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
{"label":"Sci/Tech", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 37 chars
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
{"highlights":["Microsoft","Security","patch","viruses","operating"]}
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
{"rationale":"The article discusses a Microsoft security patch and virus attacks on software, which are topics related to technology.","evidence":["Microsoft","Security","patch","viruses","operating"]}
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
{
  "edits": [
    {
      "from": "patch",
      "to": "merger"
    }
  ],
  "new_prediction": "Business"
}
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
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{"label":"Business", "confidence":70}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 70.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 37 chars
- **Prompt hash:** `8a64396178009ff8`
- **ECS (full):** 0.6190
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 3 | **CC4 size:** 3

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
{"highlights":["Bill","tech","industry","congressional","Members"]}
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
  "rationale":"The article mentions a legislative bill and references the tech industry, indicating a focus on economic and policy matters rather than sports or science.",
  "evidence":["Bum","Bill","tech","industry","California"]
}
```

**Rationale text:**
> The article mentions a legislative bill and references the tech industry, indicating a focus on economic and policy matters rather than sports or science.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bill`, `bum`, `california`, `industry`, `tech`

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
{"edits": [{"from": "Bush", "to": "UN"}], "new_prediction": "World"}
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
{"ranking":["tech","industry","Bill","Members","congressional"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tech`(1), `industry`(2), `bill`(3), `members`(4), `congressional`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.4286 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
{
  "label": "Sci/Tech",
  "confidence": 70
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 70.0%
- **Model refused:** No
- **Input length:** 55 words
- **Raw response length:** 45 chars
- **Prompt hash:** `ce6a7f2c178e4783`
- **ECS (full):** 0.6556
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{
  "highlights": ["Internet", "online", "dating", "sites", "pioneer"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dating`, `internet`, `online`, `pioneer`, `sites`

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
{
  "rationale": "The article discusses how older adults are using Internet-based platforms and online technology to find romantic partners, which pertains to technology usage.",
  "evidence": ["Internet", "dating", "online", "search", "technology"]
}
```

**Rationale text:**
> The article discusses how older adults are using Internet-based platforms and online technology to find romantic partners, which pertains to technology usage.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dating`, `internet`, `online`, `search`

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
{
  "ranking": ["Internet", "online", "dating", "sites", "search"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `internet`(1), `online`(2), `dating`(3), `sites`(4), `search`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.8000 |
| CF–RO | — |
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
{"label":"Sports", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 35 chars
- **Prompt hash:** `265eb84f94f4d713`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `Sports`
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

```

**Parsed tokens:**
- *Not parsed*

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
{"rationale":"The article describes a competitive game between the United States and Russia, mentioning fouls, turnovers, and a player, which are typical elements of sports reporting.","evidence":["United","States","Russia","fouls","turnovers"]}
```

**Rationale text:**
> The article describes a competitive game between the United States and Russia, mentioning fouls, turnovers, and a player, which are typical elements of sports reporting.

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
{"ranking":["fouls","turnovers","Swoopes","Sheryl","opponent"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`(1), `turnovers`(2), `swoopes`(3), `sheryl`(4), `opponent`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | 0.2500 |
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
{"label":"Sports", "confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 35 chars
- **Prompt hash:** `41f4d8d8e7436a00`
- **ECS (full):** 0.6190
- **ECS (primary):** 0.4286
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
{"highlights":["Tennis","Canas","Novak","Shanghai","ATP"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `canas`, `novak`, `shanghai`, `tennis`

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
{
  "rationale": "The article discusses a tennis match and tournament results, which are clearly sports content.",
  "evidence": ["Tennis", "Canas", "Novak", "Shanghai", "ATP"]
}
```

**Rationale text:**
> The article discusses a tennis match and tournament results, which are clearly sports content.

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
{
  "edits": [
    {
      "from": "tournament",
      "to": "conference"
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

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Tennis","ATP","tournament","final","Shanghai"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tennis`(1), `atp`(2), `tournament`(3), `final`(4), `shanghai`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | 0.4286 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### ag_news_test_0003 (ECS=1.0000)
- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 95.0%

### sst2_validation_0008 (ECS=1.0000)
- **Dataset:** sst2
- **Text:** comes ... uncomfortably close to coasting in the treads of the bicycle thief . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 85.0%

### sst2_validation_0002 (ECS=1.0000)
- **Dataset:** sst2
- **Text:** k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 95.0%


## Low-ECS Examples

### ag_news_test_0001 (ECS=0.2632)
- **Dataset:** ag_news
- **Text:** Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed …
- **Ground truth:** `World` → **Predicted:** `World` ✓
- **Confidence:** 95.0%

### sst2_validation_0006 (ECS=0.3143)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 70.0%

### sst2_validation_0000 (ECS=0.4048)
- **Dataset:** sst2
- **Text:** very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 85.0%
