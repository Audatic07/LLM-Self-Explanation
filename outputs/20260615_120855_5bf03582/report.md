# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 12:09:08
- **Duration:** 540.5s (9.0m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 8153
- **Avg tokens per instance:** 302

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | — | 0.699 | 70% | 90% | 40% | 70% |
| mnli | 9 | — | 0.610 | 78% | 89% | 0% | 89% |
| ag_news | 8 | — | 0.587 | 88% | 100% | 25% | 100% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 10 | 10 | 1 |
| mnli | 10 | 9 | 1 |
| ag_news | 10 | 8 | 0 |
| **Total** | 30 | 27 | 2 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N={overall.n_short}) or medium-length (21–50 words, N={overall.n_medium}). ECS may partly reflect brevity.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N={overall.n_complete_cases})

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 21/27 | 78% |
| Rationale | 25/27 | 93% |
| Counterfactual | 6/27 | 22% |
| Rank Ordering | 23/27 | 85% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=27) | 0.6348 |
| Mean ECS (primary: H,CF,RO) | 0.6830 |
| Mean ECS (complete cases, N=4) | 0.5232 |
| Complete cases | 4/27 (15%) |
| Primary ECS pairs <3 | 18 instances |
  → sst2_validation_0000: 1 pair(s), ECS_primary=0.6667
  → sst2_validation_0002: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0003: 1 pair(s), ECS_primary=0.2500
  → sst2_validation_0004: 1 pair(s), ECS_primary=1.0000
  → sst2_validation_0008: 1 pair(s), ECS_primary=0.6000
  → ... and 13 more
| Std ECS | 0.2004 |
| Median ECS | 0.6345 |
| Spearman ρ (confidence vs ECS) | -0.0808 (p=0.7209) — no significant association |
| Mean CC3 size | 2.41 |
| Mean CC4 size | 2.00 |
| % instances with CC3 | 81.5% |
| % instances with CC4 | 81.5% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.6768 |
| H–CF | 0.3000 |
| H–RO | 0.7754 |
| R–CF | 0.2917 |
| R–RO | 0.6533 |
| CF–RO | 0.2700 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 21/27 (78%) | 21/27 (78%) |
| Rationale | 25/27 (93%) | 25/27 (93%) |
| Counterfactual | 6/27 (22%) | 6/27 (22%) |
| CF flip verified | 6/6 (100%) |
| Rank Ordering | 23/27 (85%) | 23/27 (85%) |
| All 4 valid | 4/27 |
| 3 valid (CC3 adjusted) | 18/27 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 7 | 0.6638 |
| Medium (21–50) | 14 | 0.6404 |
| Long (>50 words) | 1 | 0.3540 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.6348 | [0.5500, 0.7211] |
| Spearman ρ (self-reported confidence) | -0.0808 | [-0.4783, 0.2999] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 33 words
- **Raw response length:** 20 chars
- **Prompt hash:** `cb4f063c0376ab79`
- **ECS (full):** 0.6667
- **ECS (primary):** 0.6667
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
{"highlights":["no","hide","giant","achilles","heel"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `achilles`, `giant`, `heel`, `hide`, `no`

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
{"rationale":"The comment highlights the film's lack of story and a major flaw, indicating a negative assessment.","evidence":["giant","achilles","heel","hide","story"]}
```

**Rationale text:**
> The comment highlights the film's lack of story and a major flaw, indicating a negative assessment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `achilles`, `giant`, `heel`, `hide`, `story`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as positive instead of negative. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: positive>"}
```

**Response:**
```
{"counterfactual_text":"very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just great story , folks .","new_prediction":"positive"}
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
{"ranking":["no","achilles","hide","story","giant"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `no`(1), `achilles`(2), `hide`(3), `story`(4), `giant`(5)

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

### sst2_validation_0001

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `positive` ✗
- **Input length:** 6 words
- **Raw response length:** 20 chars

### sst2_validation_0002

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 20 chars
- **Prompt hash:** `2e2ef0e5cd8ece6c`
- **ECS (full):** 0.7778
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["holocaust","fear","exploits","cheap","tension"]}
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
{"rationale":"The text criticizes the work as manipulative and low-quality by highlighting its exploitation of fear and cheap tension.","evidence":["exploits","fear","nuclear","holocaust","cheap"]}
```

**Rationale text:**
> The text criticizes the work as manipulative and low-quality by highlighting its exploitation of fear and cheap tension.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploits`, `fear`, `holocaust`, `nuclear`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as positive instead of negative. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: positive>"}
```

**Response:**
```

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
{"ranking":["holocaust","fear","exploits","cheap","tension"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `holocaust`(1), `fear`(2), `exploits`(3), `cheap`(4), `tension`(5)

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

### sst2_validation_0003

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 20 chars
- **Prompt hash:** `62feda1e67645d47`
- **ECS (full):** 0.5000
- **ECS (primary):** 0.2500
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
{"rationale":"The description highlights the characters' \"fresh,\" \"quirky\" charm, indicating a positive assessment.","evidence":["fresh","quirky","charm","bring"]}
```

**Rationale text:**
> The description highlights the characters' "fresh," "quirky" charm, indicating a positive assessment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bring`, `charm`, `fresh`, `quirky`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as negative instead of positive. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: negative>"}
```

**Response:**
```
{"counterfactual_text":"neither parker nor donovan is a typical romantic lead , but they bring a stale , quirky charm to the formula .","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fresh`

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
{"ranking":["fresh","quirky","charm","bring"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fresh`(1), `quirky`(2), `charm`(3), `bring`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | 0.2500 |
| R–RO | 1.0000 |
| CF–RO | 0.2500 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### sst2_validation_0004

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

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
- **Confidence:** 75.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1f15d549cc74ae6d`
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["artist","control","improvise","jazzman","work"]}
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
{"rationale":"The sentence praises the artist's mastery and improvisational skill, indicating a positive view.","evidence":["control","improvise","jazzman","artist","work"]}
```

**Rationale text:**
> The sentence praises the artist's mastery and improvisational skill, indicating a positive view.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `jazzman`, `work`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as negative instead of positive. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: negative>"}
```

**Response:**
```
{"counterfactual_text":"it 's a work by an artist
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
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.4000 |
| Normalized τ | 0.7000 |

### sst2_validation_0005

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "what better message than ` love thyself ' could young women of any size receive ? "

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
- **Confidence:** 76.0%
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `ac9a9f698f4c0eba`
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
{"rationale":"The phrase \"love thyself\" promotes self‑acceptance, giving the text an overall positive tone.","evidence":["better","message","love","young","women"]}
```

**Rationale text:**
> The phrase "love thyself" promotes self‑acceptance, giving the text an overall positive tone.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `message`, `women`, `young`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as negative instead of positive. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: negative>"}
```

**Response:**
```
{"counterfactual_text":"what better message than ` hate thyself ' could young women of any size receive ? ","new_prediction":"negative"}
```

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
{"ranking":["love","better","message","young","women"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `better`(2), `message`(3), `young`(4), `women`(5)

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
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"negative"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 20 chars
- **Prompt hash:** `50f5b42b5c34d301`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 1
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

```

**Parsed tokens:**
- *Not parsed*

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
{"rationale":"The use of words like \"hack-artist\" and \"trick\" conveys a derogatory tone toward the filmmaker's methods, indicating a negative sentiment.","evidence":["hack-artist","trick","ooky-spookies"]}
```

**Rationale text:**
> The use of words like "hack-artist" and "trick" conveys a derogatory tone toward the filmmaker's methods, indicating a negative sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `ooky-spookies`, `trick`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as positive instead of negative. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: positive>"}
```

**Response:**
```

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
| H–R | — |
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
{"label":"positive or negative"}
```

#### 2. Classification Response
```
{"label":"positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 19 words
- **Raw response length:** 20 chars
- **Prompt hash:** `63718fc189536913`
- **ECS (full):** 0.6500
- **ECS (primary):** 0.5667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 4 | **CC4 size:** 2

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
{"rationale":"The description uses praise words like \"charming\" and highlights strong chemistry and affectionate relationships, indicating a positive sentiment.","evidence":["charming","chemistry","friends","lovers","leads"]}
```

**Rationale text:**
> The description uses praise words like "charming" and highlights strong chemistry and affectionate relationships, indicating a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`, `friends`, `leads`, `lovers`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as negative instead of positive. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: negative>"}
```

**Response:**
```
{"counterfactual_text":"as the two leads , lathan and diggs are repulsive and have tension both as friends and lovers .","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`

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
| H–CF | 0.4000 |
| H–RO | 0.8000 |
| R–CF | 0.4000 |
| R–RO | 0.8000 |
| CF–RO | 0.5000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### sst2_validation_0008

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b00a643964e1a260`
- **ECS (full):** 0.7333
- **ECS (primary):** 0.6000
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
{
  "rationale":"The passage conveys a negative tone by describing an unsettling, uncomfortable proximity to a bicycle thief.",
  "evidence":["uncomfortably","thief","close","treads","coasting"]
}
```

**Rationale text:**
> The passage conveys a negative tone by describing an unsettling, uncomfortable proximity to a bicycle thief.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `close`, `coasting`, `thief`, `treads`, `uncomfortably`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as positive instead of negative. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: positive>"}
```

**Response:**
```
{"counterfactual_text":"comes ... comfortably close to coasting in the treads of the bicycle thief . ","new_prediction":"positive"}
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
{"ranking":["uncomfortably","thief","close"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`(1), `thief`(2), `close`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.6000 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### sst2_validation_0009

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "one from the heart . "

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
- **Confidence:** 75.0%
- **Model refused:** No
- **Input length:** 5 words
- **Raw response length:** 20 chars
- **Prompt hash:** `741aee97f6968c27`
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
{"highlights":["heart","one","from","the","heart"]}
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
{"rationale":"The word \"heart\" conveys genuine, positive emotion, indicating a sentiment that is uplifting rather than negative.","evidence":["one","heart"]}
```

**Rationale text:**
> The word "heart" conveys genuine, positive emotion, indicating a sentiment that is uplifting rather than negative.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heart`, `one`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Replace exactly ONE or TWO individual words in the text such that the modified text WOULD be classified as negative instead of positive. The replacement words must come from outside the text. Do not change any other words, punctuation, or structure.

If no single-word or two-word replacement can plausibly flip the label, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 words changed>","new_prediction":"<one of: negative>"}
```

**Response:**
```
{"counterfactual_text":"one from the hell . ","new_prediction":"negative"}
```

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

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: It spoke of thousands of years, even before the times of the old empire.
Hypothesis: The old Empire is still ongoing.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 19 chars
- **Prompt hash:** `d5633a126ae8c423`
- **ECS (full):** 0.4222
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
{"highlights":["old","before","still","ongoing","thousands"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `old`, `ongoing`, `still`, `thousands`

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
{"rationale":"The premise only references a period before the old empire and does not provide information about whether the empire continues, so it neither entails nor contradicts the hypothesis.","evidence":["before","old","empire","thousands","years"]}
```

**Rationale text:**
> The premise only references a period before the old empire and does not provide information about whether the empire continues, so it neither entails nor contradicts the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `empire`, `old`, `thousands`, `years`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as entailment, contradiction instead of neutral. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: entailment, contradiction>"}
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
{"ranking":["before","old","empire","still","ongoing"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `old`(1), `empire`(2), `still`(3), `ongoing`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0001

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 26 words
- **Raw response length:** 24 chars
- **Prompt hash:** `9c46ed5be80cbed9`
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
{
  "highlights": ["only", "others", "protect", "went", "summons"]
}
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
  "rationale": "The premise only states that the summons concerns Dave Hanson and mentions three people arriving, but it gives no information about the others' intentions or actions toward Dave, so the hypothesis is not entailed nor contradicted.",
  "evidence": ["summons", "only", "Dave", "Hanson", "three"]
}
```

**Rationale text:**
> The premise only states that the summons concerns Dave Hanson and mentions three people arriving, but it gives no information about the others' intentions or actions toward Dave, so the hypothesis is not entailed nor contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dave`, `hanson`, `summons`, `three`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as entailment, contradiction instead of neutral. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: entailment, contradiction>"}
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
  "ranking": ["only", "others", "protect", "summons", "Dave"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `others`(1), `protect`(2), `summons`(3), `dave`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 22 chars
- **Prompt hash:** `3aaebb0a45f286c3`
- **ECS (full):** 0.6556
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

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
{"highlights":["good","sharing","no","profit","plan"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `no`, `plan`, `profit`, `sharing`

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
  "rationale":"The premise says there is a good profit‑sharing plan but no profit, which directly matches the hypothesis that it’s a good way of sharing money yet there’s no money.",
  "evidence":["good","profit","sharing","plan","just"]
}
```

**Rationale text:**
> The premise says there is a good profit‑sharing plan but no profit, which directly matches the hypothesis that it’s a good way of sharing money yet there’s no money.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `plan`, `profit`, `sharing`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as neutral, contradiction instead of entailment. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: neutral, contradiction>"}
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

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["profit","sharing","good","no","money"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `profit`(1), `sharing`(2), `good`(3), `no`(4), `money`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.8000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | -0.3333 |
| Normalized τ | 0.3333 |

### mnli_validation_matched_0003

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 25 chars
- **Prompt hash:** `9603de0e31d8f629`
- **ECS (full):** 0.7778
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["Positano","Amalfi","coast","south","far"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `coast`, `far`, `positano`, `south`

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
{"rationale":"The premise states that Positano is located on the Amalfi coast, so they are not far apart, contradicting the hypothesis.","evidence":["Positano","Amalfi","coast","south","villages"]}
```

**Rationale text:**
> The premise states that Positano is located on the Amalfi coast, so they are not far apart, contradicting the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `coast`, `positano`, `south`, `villages`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as entailment, neutral instead of contradiction. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: entailment, neutral>"}
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
{"ranking":["Positano","Amalfi","coast","far","south"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `positano`(1), `amalfi`(2), `coast`(3), `far`(4), `south`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### mnli_validation_matched_0004

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 22 chars
- **Prompt hash:** `2ca9e2aad190469d`
- **ECS (full):** 0.8333
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

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
{"highlights":["defeated","sadistic","mostly","when","aren't"]}
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
{"rationale":"The premise explicitly states that when his colleagues aren't sadistic, they are mostly defeated, which directly matches the hypothesis.","evidence":["colleagues","mostly","defeated","sadistic","when"]}
```

**Rationale text:**
> The premise explicitly states that when his colleagues aren't sadistic, they are mostly defeated, which directly matches the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleagues`, `defeated`, `mostly`, `sadistic`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as neutral, contradiction instead of entailment. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: neutral, contradiction>"}
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

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["defeated","mostly","sadistic","when","aren't"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defeated`(1), `sadistic`(2), `mostly`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.7500 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.7500 |
| CF–RO | — |
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
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 17 words
- **Raw response length:** 25 chars
- **Prompt hash:** `18b3b8ffa674b363`
- **ECS (full):** 0.6000
- **ECS (primary):** 1.0000
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
{"highlights":["look","compare","Don't","consider","before"]}
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
{"rationale":"The premise tells you to compare before buying, whereas the hypothesis tells you not to, which directly opposes the premise.","evidence":["look","compare","before","buying","sure"]}
```

**Rationale text:**
> The premise tells you to compare before buying, whereas the hypothesis tells you not to, which directly opposes the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buying`, `compare`, `look`, `sure`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as entailment, neutral instead of contradiction. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: entailment, neutral>"}
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
{"ranking":["don't","look","consider","compare","before"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `look`(1), `consider`(2), `compare`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 0.4000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### mnli_validation_matched_0006

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: It's come back? cried Julius excitedly.
Hypothesis: They thought it was gone forever.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 19 chars
- **Prompt hash:** `fba612cac83b9a15`
- **ECS (full):** 0.6190
- **ECS (primary):** 1.0000
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
{"highlights":["back","gone","forever","thought","excitedly"]}
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
{"rationale":"The premise only shows surprise at something returning, without indicating a prior belief that it was gone forever, so it neither entails nor contradicts the hypothesis.","evidence":["come","back","Julius","excitedly","gone"]}
```

**Rationale text:**
> The premise only shows surprise at something returning, without indicating a prior belief that it was gone forever, so it neither entails nor contradicts the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`, `come`, `excitedly`, `gone`, `julius`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as entailment, contradiction instead of neutral. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: entailment, contradiction>"}
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
{"ranking":["back","gone","forever","thought","excitedly"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `back`(1), `gone`(2), `forever`(3), `thought`(4), `excitedly`(5)

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

### mnli_validation_matched_0007

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving.

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 18 words
- **Raw response length:** 25 chars
- **Prompt hash:** `793a8d1dda9ca3e0`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
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

```

**Parsed tokens:**
- *Not parsed*

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
{"rationale":"The premise states that employers are still driving, directly opposing the hypothesis that they have refused to continue driving, thus they contradict each other.","evidence":["employers","still","driving","counts"]}
```

**Rationale text:**
> The premise states that employers are still driving, directly opposing the hypothesis that they have refused to continue driving, thus they contradict each other.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `counts`, `driving`, `employers`, `still`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as entailment, neutral instead of contradiction. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: entailment, neutral>"}
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
{"ranking":["still","refused","driving","continue","employers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `still`(1), `refused`(2), `driving`(3), `continue`(4), `employers`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0008

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `entailment`
- **Predicted:** `neutral` ✗
- **Input length:** 24 words
- **Raw response length:** 19 chars

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pharmaceuticals Inc."

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
- **Confidence:** 85.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d9cc2f1c2a401c2a`
- **ECS (full):** 0.3889
- **ECS (primary):** 0.2500
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{"highlights":["deal","buyout","shareholder","acquire","stock"]}
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
  "rationale":"The article discusses a dispute involving a major shareholder and a $4 billion acquisition, which are classic business‑related topics.",
  "evidence":["Icahn","CEO","Mylan","stock","buyout"]
}
```

**Rationale text:**
> The article discusses a dispute involving a major shareholder and a $4 billion acquisition, which are classic business‑related topics.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buyout`, `ceo`, `icahn`, `mylan`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as World, Sports, Sci/Tech instead of Business. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: World, Sports, Sci/Tech>"}
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
{"ranking":["Mylan","deal","Icahn","CEO","buyout"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mylan`(1), `deal`(2), `icahn`(3), `ceo`(4), `buyout`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 0.2500 |
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
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"World"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 93.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 17 chars
- **Prompt hash:** `34f8f0bbd178d7da`
- **ECS (full):** 0.3690
- **ECS (primary):** 0.4286
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
  "rationale":"The article discusses political controversy involving the Australian Prime Minister and a national incident, which falls under international/world news.",
  "evidence":["Australian","Prime","Minister","Howard","children"]
}
```

**Rationale text:**
> The article discusses political controversy involving the Australian Prime Minister and a national incident, which falls under international/world news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `children`, `howard`, `minister`, `prime`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as Sports, Business, Sci/Tech instead of World. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: Sports, Business, Sci/Tech>"}
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
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"World"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 17 chars
- **Prompt hash:** `d1c55024370f2e12`
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
{
  "rationale":"The article discusses an international legal action involving the United Nations war crimes prosecutor and Serbia, which is a global political matter.",
  "evidence":["U.N.","War","Court","Serbia","Reuters"]
}
```

**Rationale text:**
> The article discusses an international legal action involving the United Nations war crimes prosecutor and Serbia, which is a global political matter.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `court`, `reuters`, `serbia`, `u.n`, `war`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as Sports, Business, Sci/Tech instead of World. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: Sports, Business, Sci/Tech>"}
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
{"ranking":["U.N.","Serbia","court","War","Belgrade"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `u.n`(1), `serbia`(2), `court`(3), `war`(4), `belgrade`(5)

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
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 92.0%
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 20 chars
- **Prompt hash:** `362cc0a1227d48a0`
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
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
{
  "rationale":"The article discusses a Microsoft security patch and virus attacks on software, which are topics related to technology.",
  "evidence":["Microsoft","Security","patch","viruses","operating"]
}
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

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as World, Sports, Business instead of Sci/Tech. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: World, Sports, Business>"}
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
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Business"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 20 chars
- **Prompt hash:** `3aa17e5b8e6b2bae`
- **ECS (full):** 0.4889
- **ECS (primary):** 0.3556
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Sports`
- **CC3 size:** 4 | **CC4 size:** 1

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
{"highlights":["Bill","industry","tech","congressional","Members"]}
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
{"rationale":"The article discusses a legislative effort involving a bill and congressional members aimed at influencing the tech industry, which fits the Business topic.","evidence":["Bill","congressional","tech","industry","members"]}
```

**Rationale text:**
> The article discusses a legislative effort involving a bill and congressional members aimed at influencing the tech industry, which fits the Business topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bill`, `congressional`, `industry`, `members`, `tech`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as World, Sports, Sci/Tech instead of Business. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"counterfactual_text":"Boxer Begs Bush to Back Bum Bill Members of California's congressional team make one last effort to look good for the sports industry back home.","new_prediction":"Sports"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tech`

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
{"ranking":["tech","industry","Bill","congressional","California's"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tech`(1), `industry`(2), `bill`(3), `congressional`(4), `california's`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.2000 |
| H–RO | 0.6667 |
| R–CF | 0.2000 |
| R–RO | 0.6667 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### ag_news_test_0005

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "More Older People Turning to the Internet to Find Love Mary Bellis Waller, now 64, posted on two Internet dating sites during her search for a companion. Waller was a pioneer of online dating among people her age, and thousands of others age 60 and older are also turning to the Internet to find romance."

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
- **Confidence:** 65.0%
- **Model refused:** No
- **Input length:** 55 words
- **Raw response length:** 20 chars
- **Prompt hash:** `4bca8da7ad03dac3`
- **ECS (full):** 0.3540
- **ECS (primary):** 0.2762
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 1

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
{"highlights":["Internet","online","dating","sites","pioneer"]}
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
{"rationale":"The article discusses how older adults are using the Internet and online platforms for dating, which pertains to technology and its social applications, fitting the Sci/Tech category.","evidence":["Internet","dating","online","search","companion"]}
```

**Rationale text:**
> The article discusses how older adults are using the Internet and online platforms for dating, which pertains to technology and its social applications, fitting the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `companion`, `dating`, `internet`, `online`, `search`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as World, Sports, Business instead of Sci/Tech. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: World, Sports, Business>"}
```

**Response:**
```
{"counterfactual_text":"More Older People Turning to the Internet to Find Love Mary Bellis Waller, now 64, posted on two Internet sports sites during her search for a companion. Waller was a pioneer of online sports among people her age, and thousands of others age 60 and older are also turning to the Internet to find romance.","new_prediction":"Sports"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dating`

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
{"ranking":["Internet","online","dating","search","turning"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `internet`(1), `online`(2), `dating`(3), `search`(4), `turning`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | 0.2000 |
| H–RO | 0.4286 |
| R–CF | 0.2000 |
| R–RO | 0.6667 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0006

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "United States 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right."

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 18 chars
- **Prompt hash:** `1ed0148e7838e3a9`
- **ECS (full):** 0.5048
- **ECS (primary):** 0.8000
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
{"highlights":["fouls","turnovers","opponent","Sheryl","Swoopes"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `opponent`, `sheryl`, `swoopes`, `turnovers`

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
  "rationale":"The passage references game scores, fouls, turnovers, and a player, all characteristic of a sports report.",
  "evidence":["fouls","turnovers","Sheryl","Russia","United"]
}
```

**Rationale text:**
> The passage references game scores, fouls, turnovers, and a player, all characteristic of a sports report.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`, `russia`, `sheryl`, `turnovers`, `united`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as World, Business, Sci/Tech instead of Sports. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: World, Business, Sci/Tech>"}
```

**Response:**
```

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
{"ranking":["fouls,","turnovers","Swoopes","opponent,"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fouls`(1), `turnovers`(2), `swoopes`(3), `opponent`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4286 |
| H–CF | — |
| H–RO | 0.8000 |
| R–CF | — |
| R–RO | 0.2857 |
| CF–RO | — |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### ag_news_test_0007

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

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
- **Confidence:** 0.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 18 chars
- **Prompt hash:** `97373d2318f574eb`
- **ECS (full):** 1.0000
- **ECS (primary):** 1.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 5 | **CC4 size:** 5

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
{"rationale":"The article reports on a tennis match and tournament results, which are clearly sports content.","evidence":["Tennis","Canas","Novak","Shanghai","ATP"]}
```

**Rationale text:**
> The article reports on a tennis match and tournament results, which are clearly sports content.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `canas`, `novak`, `shanghai`, `tennis`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Replace exactly ONE or TWO topic-specific words (proper nouns, domain terms, named entities) so the article would be classified as World, Business, Sci/Tech instead of Sports. Keep all other words, punctuation, and structure identical.

If no single-word or two-word replacement can plausibly change the topic classification, return:
{"counterfactual_text": null, "new_prediction": null}

Otherwise, return only valid JSON:
{"counterfactual_text":"<modified text with only 1-2 topic words changed>","new_prediction":"<one of: World, Business, Sci/Tech>"}
```

**Response:**
```

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
{"ranking":["Tennis","ATP","Canas","Novak","Shanghai"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tennis`(1), `atp`(2), `canas`(3), `novak`(4), `shanghai`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | — |
| H–RO | 1.0000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### ag_news_test_0007 (ECS=1.0000)
- **Dataset:** ag_news
- **Text:** Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar A…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓
- **Confidence:** 0.0%

### ag_news_test_0003 (ECS=1.0000)
- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 92.0%

### sst2_validation_0004 (ECS=1.0000)
- **Dataset:** sst2
- **Text:** it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 75.0%


## Low-ECS Examples

### ag_news_test_0005 (ECS=0.3540)
- **Dataset:** ag_news
- **Text:** More Older People Turning to the Internet to Find Love Mary Bellis Waller, now 64, posted on two Internet dating sites during her search for a companion. Waller was a pioneer of online dating among pe…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 65.0%

### mnli_validation_matched_0001 (ECS=0.3587)
- **Dataset:** mnli
- **Text:** Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
- **Confidence:** 0.0%

### ag_news_test_0001 (ECS=0.3690)
- **Dataset:** ag_news
- **Text:** Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed …
- **Ground truth:** `World` → **Predicted:** `World` ✓
- **Confidence:** 93.0%
