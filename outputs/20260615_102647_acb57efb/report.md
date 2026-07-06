# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 10:27:15
- **Duration:** 336.9s (5.6m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 8181
- **Avg tokens per instance:** 303

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | 10/10 (100%) | 0.522 | 100% | 100% | 40% | 90% |
| mnli | 9 | 7/9 (78%) | 0.534 | 78% | 78% | 44% | 67% |
| ag_news | 8 | 6/8 (75%) | 0.558 | 75% | 75% | 0% | 75% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 10 | 10 | 0 |
| mnli | 10 | 9 | 2 |
| ag_news | 10 | 8 | 2 |
| **Total** | 30 | 27 | 4 |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (full) | 0.5358 |
| Mean ECS (primary: H,CF,RO) | 0.4867 |
| Mean ECS (complete cases, N=8) | 0.4680 |
| Complete cases | 8/27 (30%) |
| Primary ECS pairs <3 | 13 instances |
  → sst2_validation_0000: 1 pair(s), ECS_primary=0.2500
  → sst2_validation_0001: 1 pair(s), ECS_primary=0.6667
  → sst2_validation_0002: 1 pair(s), ECS_primary=0.6000
  → sst2_validation_0003: 1 pair(s), ECS_primary=0.6000
  → sst2_validation_0004: 1 pair(s), ECS_primary=0.5000
  → ... and 8 more
| Std ECS | 0.1477 |
| Median ECS | 0.5333 |
| Spearman ρ | -0.3893 (p=0.0811) |
| Mean CC3 size | 2.11 |
| Mean CC4 size | 1.63 |
| % instances with CC3 | 77.8% |
| % instances with CC4 | 74.1% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.5533 |
| H–CF | 0.2780 |
| H–RO | 0.5728 |
| R–CF | 0.3334 |
| R–RO | 0.6840 |
| CF–RO | 0.2472 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 23/27 (85%) | 23/27 (85%) |
| Rationale | 23/27 (85%) | 23/27 (85%) |
| Counterfactual | 8/27 (30%) | 8/27 (30%) |
| CF flip verified | 8/8 (100%) |
| Rank Ordering | 21/27 (78%) | 21/27 (78%) |
| All 4 valid | 8/27 |
| 3 valid (CC3 adjusted) | 13/27 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 8 | 0.5664 |
| Medium (21–50) | 13 | 0.5170 |
| Long (>50 words) | 0 | 0.0000 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.5358 | [0.4674, 0.5972] |
| Spearman ρ (self-reported confidence) | -0.3893 | [-0.6917, 0.0798] |

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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 33 words
- **Raw response length:** 20 chars
- **Prompt hash:** `cb4f063c0376ab79`
- **ECS (full):** 0.2643
- **ECS (primary):** 0.2500
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["heel", "giant", "no"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `giant`, `heel`

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
{"rationale":"The classification is correct because the text criticizes the lack of story in the movie despite its special effects, indicating an overall negative opinion.","evidence":["special", "bold", "giant", "heel", "folks"]}
```

**Rationale text:**
> The classification is correct because the text criticizes the lack of story in the movie despite its special effects, indicating an overall negative opinion.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bold`, `folk`, `giant`, `heel`, `special`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: positive.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"very special effects , brilliantly bold colors and heightened reality can't hide the small achilles ' heel in `` stuart little 2 `` : there 's just a story , folks .","new_prediction":"positive"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["heel", "no", "hide", "just", "story"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `heel`(1), `hide`(2), `story`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | — |
| H–RO | 0.2500 |
| R–CF | — |
| R–RO | 0.1429 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "holden caulfield did it better . "

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 6 words
- **Raw response length:** 20 chars
- **Prompt hash:** `a447a2ee53afc6bc`
- **ECS (full):** 0.7778
- **ECS (primary):** 0.6667
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["better", "did", "holden"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `holden`

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
{"rationale":"The text is classified as negative because the phrase 'did it better' implies a comparison where the subject of the sentence is being outdone, which carries a negative connotation.","evidence":["holden","caulfield","better","did"]}
```

**Rationale text:**
> The text is classified as negative because the phrase 'did it better' implies a comparison where the subject of the sentence is being outdone, which carries a negative connotation.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `caulfield`, `holden`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: positive.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"holden caulfield did it worse","new_prediction":"positive"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["better", "did", "holden", "it", "caulfield"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `holden`(1), `caulfield`(2), `better`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 15 words
- **Raw response length:** 20 chars
- **Prompt hash:** `2e2ef0e5cd8ece6c`
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

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["fear", "cheap", "holocaust"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `fear`, `holocaust`

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
{"rationale":"The text is classified as negative because it uses words with negative connotations to describe the film's approach to generating tension.","evidence":["cheap", "fear", "holocaust", "exploits", "tension"]}
```

**Rationale text:**
> The text is classified as negative because it uses words with negative connotations to describe the film's approach to generating tension.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`, `exploit`, `fear`, `holocaust`, `tension`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: positive.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood excitement . ","new_prediction":"positive"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["cheap", "fear", "holocaust", "tension", "exploits"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cheap`(1), `fear`(2), `holocaust`(3), `tension`(4), `exploit`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 20 chars
- **Prompt hash:** `62feda1e67645d47`
- **ECS (full):** 0.7333
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["fresh", "quirky", "charm"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charm`, `fresh`, `quirky`

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
{"rationale":"The text is classified as positive because it describes the leads as bringing a 'fresh' and 'quirky charm' to the formula, indicating an appreciation for their unique qualities.","evidence":["fresh","quirky","charm","lead","romantic"]}
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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: negative.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"neither parker nor donovan is a typical romantic lead , but they bring a stale , quirky charm to the formula .","new_prediction":"negative"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

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
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 1.0000 |
| CF–RO | — |
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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1f15d549cc74ae6d`
- **ECS (full):** 0.3889
- **ECS (primary):** 0.5000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["control", "artist", "improvise"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`

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
{"rationale":"The classification is correct because the text uses language that implies a high level of skill and artistry, indicating a positive sentiment towards the artist's work.","evidence":["control", "jazzman", "improvise", "medium", "message"]}
```

**Rationale text:**
> The classification is correct because the text uses language that implies a high level of skill and artistry, indicating a positive sentiment towards the artist's work.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `control`, `improvise`, `jazzman`, `medium`, `message`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: negative.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"it 's a work by an artist so out of control of both his medium and his message that he can improvise like a jazzman .","new_prediction":"negative"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["control", "artist", "his", "message", "jazzman"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `control`(1), `artist`(2), `jazzman`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 0.5000 |
| R–CF | — |
| R–RO | 0.3333 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `ac9a9f698f4c0eba`
- **ECS (full):** 0.6111
- **ECS (primary):** 0.5556
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["love","better","young"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `young`

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
{"rationale":"The text is classified as positive because it implies that the message 'love thyself' is uplifting and beneficial for young women, conveying a sense of self-acceptance and empowerment.","evidence":["love", "better", "young", "women", "thyself"]}
```

**Rationale text:**
> The text is classified as positive because it implies that the message 'love thyself' is uplifting and beneficial for young women, conveying a sense of self-acceptance and empowerment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`, `thyself`, `woman`, `young`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: negative.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"what worse message than ` hate thyself ' could young women of any size receive ?","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `better`, `love`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["love", "better", "young", "women", "thyself"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `love`(1), `better`(2), `young`(3), `woman`(4), `thyself`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.6667 |
| H–RO | 0.6000 |
| R–CF | 0.4000 |
| R–RO | 1.0000 |
| CF–RO | 0.4000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 20 chars
- **Prompt hash:** `50f5b42b5c34d301`
- **ECS (full):** 0.2560
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["hack", "ooky", "trick"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack`, `ooky`, `trick`

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
{"rationale":"The text is classified as negative because it uses derogatory language to describe the artist's techniques, implying a lack of genuine skill or talent.","evidence":["hack-artist","ooky-spookies","trick","hacks","ooky"]}
```

**Rationale text:**
> The text is classified as negative because it uses derogatory language to describe the artist's techniques, implying a lack of genuine skill or talent.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `ooky`, `ooky-spookies`, `trick`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: positive.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"verbinski implements every great-artist trick to give us the ooky-spookies .","new_prediction":"positive"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["hack", "trick", "ooky", "spookies", "every"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack`(1), `trick`(2), `ooky`(3), `spookies`(4), `every`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | 0.0000 |
| H–RO | 0.6000 |
| R–CF | 0.2500 |
| R–RO | 0.2857 |
| CF–RO | 0.0000 |
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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 19 words
- **Raw response length:** 20 chars
- **Prompt hash:** `63718fc189536913`
- **ECS (full):** 0.4889
- **ECS (primary):** 0.3778
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["charming","chemistry","lovers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`, `lover`

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
{"rationale":"The classification is correct because the text uses positive adjectives to describe the leads, indicating a favorable sentiment.","evidence":["charming","chemistry","lovers","friends","leads"]}
```

**Rationale text:**
> The classification is correct because the text uses positive adjectives to describe the leads, indicating a favorable sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`, `chemistry`, `friend`, `lead`, `lover`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: negative.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"as the two leads , lathan and diggs are dull and have chemistry both as friends and lovers .","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["charming","chemistry","lovers","friends","leads"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `charming`(1), `chemistry`(2), `lover`(3), `friend`(4), `lead`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.3333 |
| H–RO | 0.6000 |
| R–CF | 0.2000 |
| R–RO | 1.0000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b00a643964e1a260`
- **ECS (full):** 0.4444
- **ECS (primary):** 0.3016
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["coasting", "uncomfortably", "thief"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `coasting`, `thief`, `uncomfortably`

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
{"rationale":"The text is classified as negative because it implies that the subject is unoriginal and lacking in creativity, as evidenced by words with negative connotations.","evidence":["uncomfortably","coasting","thief"]}
```

**Rationale text:**
> The text is classified as negative because it implies that the subject is unoriginal and lacking in creativity, as evidenced by words with negative connotations.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `coasting`, `thief`, `uncomfortably`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: positive.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"comes ... comfortably close to coasting in the treads of the bicycle thief .","new_prediction":"positive"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["coasting", "uncomfortably", "close", "thief", "in"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `come`(1), `uncomfortably`(2), `close`(3), `coasting`(4), `tread`(5), `bicycle`(6), `thief`(7)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.3333 |
| H–RO | 0.4286 |
| R–CF | 0.3333 |
| R–RO | 0.4286 |
| CF–RO | 0.1429 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 5 words
- **Raw response length:** 20 chars
- **Prompt hash:** `741aee97f6968c27`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["heart","one","the"]}
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
{"rationale":"The text is classified as positive because the phrase 'from the heart' is often associated with sincerity and genuine emotion, implying a positive sentiment.","evidence":["heart","one"]}
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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: negative.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"one from hell . ","new_prediction":"negative"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

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
| H–CF | — |
| H–RO | — |
| R–CF | — |
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
{"label":"contradiction"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 22 words
- **Raw response length:** 25 chars
- **Prompt hash:** ``
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 0
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```

```

**Response:**
```

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
{"label":"neutral"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 26 words
- **Raw response length:** 19 chars
- **Prompt hash:** `9c46ed5be80cbed9`
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

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["only", "three", "others"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `others`, `three`

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
{"rationale":"The classification is correct because the premise only mentions a summons for Dave Hanson, but does not provide information about the others' intentions or actions, making it neutral with respect to the hypothesis.","evidence":["summons", "sternly", "Perth", "Dave", "Hanson"]}
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

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: entailment, contradiction.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"The summons was only for John Hanson," Ser Perth said sternly as the three drew up to him.","new_prediction":"contradiction"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: neutral

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["only", "The", "to", "was", "as"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | — |
| R–CF | — |
| R–RO | — |
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
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 22 chars
- **Prompt hash:** `3aaebb0a45f286c3`
- **ECS (full):** 0.5012
- **ECS (primary):** 0.4167
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 4 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["profit", "good", "sharing"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `good`, `profit`, `sharing`

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
{"rationale":"The classification is correct because the premise explicitly states that there is a good profit sharing plan, but no profit, which directly supports the hypothesis.","evidence":["profit", "sharing", "plan", "good", "money"]}
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

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: neutral, contradiction.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"but like they always say you know got a good bonus plan just no profit","new_prediction":"neutral"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `always`, `good`, `got`, `hypothesis`, `know`, `like`, `money`, `plan`, `premise`, `profit`, `say`, `sharing`, `there's`, `way`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["profit", "good", "plan", "no", "sharing"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `profit`(1), `good`(2), `sharing`(3), `plan`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.2143 |
| H–RO | 0.7500 |
| R–CF | 0.3571 |
| R–RO | 0.8000 |
| CF–RO | 0.2857 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 40 words
- **Raw response length:** 25 chars
- **Prompt hash:** `9603de0e31d8f629`
- **ECS (full):** 0.3698
- **ECS (primary):** 0.2381
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 5 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["south", "Sorrento", "Positano"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `positano`, `sorrento`, `south`

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
{"rationale":"The classification is correct because the premise states that Positano is located on the Amalfi coast, which directly contradicts the hypothesis that the Amalfi coast is far from Positano.","evidence":["Sorrento", "Positano", "coast", "villages", "south"]}
```

**Rationale text:**
> The classification is correct because the premise states that Positano is located on the Amalfi coast, which directly contradicts the hypothesis that the Amalfi coast is far from Positano.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `coast`, `positano`, `sorrento`, `south`, `village`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: entailment, neutral.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Cote coast, justifiably tauted as one of the world's most beautiful drives.","new_prediction":"neutral"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `amalfi`, `beautiful`, `cliff`, `coast`, `craggy`, `drive`, `far`, `fishing`, `former`, `hypothesis`, `justifiably`, `one`, `positano`, `premise`, `serpentine`, `sorrento`, `south`, `spill`, `tauted`, `village`, `world's`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["south", "Positano", "coast", "Amalfi", "villages"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `south`(1), `positano`(2), `coast`(3), `amalfi`(4), `village`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.1429 |
| H–RO | 0.3333 |
| R–CF | 0.2381 |
| R–RO | 0.6667 |
| CF–RO | 0.2381 |
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
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 22 chars
- **Prompt hash:** `2ca9e2aad190469d`
- **ECS (full):** 0.4917
- **ECS (primary):** 0.4056
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 4 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["defeated", "sadistic", "mostly"]}
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
{"rationale":"The classification is correct because the premise directly states that when his colleagues aren't sadistic, they are mostly defeated, which is exactly what the hypothesis claims.","evidence":["defeated","sadistic","mostly","colleagues","disgust"]}
```

**Rationale text:**
> The classification is correct because the premise directly states that when his colleagues aren't sadistic, they are mostly defeated, which is exactly what the hypothesis claims.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `colleague`, `defeated`, `disgust`, `mostly`, `sadistic`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: neutral, contradiction.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"In Europe, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.","new_prediction":"neutral"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `america`, `colleague`, `defeated`, `disgust`, `early`, `first`, `hypothesis`, `job`, `miss`, `mostly`, `mudd`, `predecessor`, `premise`, `retired`, `sadistic`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["defeated", "colleagues", "sadistic", "mostly", "when"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defeated`(1), `colleague`(2), `sadistic`(3), `mostly`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.2000 |
| H–RO | 0.7500 |
| R–CF | 0.3333 |
| R–RO | 0.8000 |
| CF–RO | 0.2667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 17 words
- **Raw response length:** 25 chars
- **Prompt hash:** `18b3b8ffa674b363`
- **ECS (full):** 0.6389
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

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["before", "compare", "buying"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buying`, `compare`

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
{"rationale":"The classification is correct because the premise advises to compare before buying, while the hypothesis suggests not to, which are opposite actions.","evidence":["compare", "buying", "consider", "before", "buy"]}
```

**Rationale text:**
> The classification is correct because the premise advises to compare before buying, while the hypothesis suggests not to, which are opposite actions.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `buy`, `buying`, `compare`, `consider`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: entailment, neutral.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Premise: Be sure to look around and compare before selling. Hypothesis: Don't consider and compare before buying.","new_prediction":"neutral"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["before","compare","and","buying","consider"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `compare`(1), `buying`(2), `consider`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | — |
| H–RO | 0.6667 |
| R–CF | — |
| R–RO | 0.7500 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 22 chars
- **Prompt hash:** ``
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 0
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```

```

**Response:**
```

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
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 18 words
- **Raw response length:** 25 chars
- **Prompt hash:** `793a8d1dda9ca3e0`
- **ECS (full):** 0.5806
- **ECS (primary):** 0.5093
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 4 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["still", "refused", "driving"]}
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
{"rationale":"The classification is correct because the premise states that employers are still driving, which directly contradicts the hypothesis that employers have refused to continue driving.","evidence":["still", "driving", "refused", "employers", "counts"]}
```

**Rationale text:**
> The classification is correct because the premise states that employers are still driving, which directly contradicts the hypothesis that employers have refused to continue driving.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `count`, `driving`, `employer`, `refused`, `still`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: entailment, neutral.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"But employees are still driving, and that's all that counts.","new_prediction":"neutral"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `continue`, `count`, `driving`, `employer`, `hypothesis`, `premise`, `refused`, `still`, `that's`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["still", "refused", "driving", "employers", "have"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `still`(1), `refused`(2), `driving`(3), `employer`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.3333 |
| H–RO | 0.7500 |
| R–CF | 0.5556 |
| R–RO | 0.8000 |
| CF–RO | 0.4444 |
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
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{"label":"entailment"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 22 chars
- **Prompt hash:** `9f4a45e5e4e37481`
- **ECS (full):** 0.6222
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["earned", "Waters", "2000"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2000`, `earned`, `water`

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
{"rationale":"The classification is correct because the hypothesis is a paraphrased version of the premise, conveying the same information with slightly different wording.","evidence":["Waters", "earned", "65,000", "2000", "tax"]}
```

**Rationale text:**
> The classification is correct because the hypothesis is a paraphrased version of the premise, conveying the same information with slightly different wording.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2000`, `65,000`, `earned`, `tax`, `water`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: neutral, contradiction.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Tax records show Smith earned around $65,000 in 2000.", "new_prediction":"contradiction"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Waters","earned","2000","tax","records"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `water`(1), `earned`(2), `2000`(3), `tax`(4), `record`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d9cc2f1c2a401c2a`
- **ECS (full):** 0.4540
- **ECS (primary):** 0.3333
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Mylan", "billion", "shareholder"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `billion`, `mylan`, `shareholder`

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
{"rationale":"The text is classified as Business because it discusses a company's stock buyout offer, acquisition deal, and shareholder dispute, which are all typical business-related topics.","evidence":["Mylan", "CEO", "shareholder", "billion", "acquire"]}
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

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Sports, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Icahn blasts coach Coury after Nike rejects stock buyout offer The war of words between Nike and the company 's largest shareholder over Nike 's \$4 billion deal to acquire Adidas Inc.", "new_prediction":"Sports"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Mylan", "billion", "CEO", "stock", "deal"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `mylan`(1), `billion`(2), `ceo`(3), `stock`(4), `deal`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.3333 |
| R–CF | — |
| R–RO | 0.4286 |
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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 17 chars
- **Prompt hash:** `34f8f0bbd178d7da`
- **ECS (full):** 0.7333
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Prime", "Australian", "Minister"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `minister`, `prime`

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
{"rationale":"The text is classified as World because it discusses a political incident involving a country's prime minister, which is a typical topic in global news.","evidence":["Australian", "Prime", "Minister", "Howard", "incident"]}
```

**Rationale text:**
> The text is classified as World because it discusses a political incident involving a country's prime minister, which is a typical topic in global news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `howard`, `incident`, `minister`, `prime`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: Sports, Business, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Revelations on \"players overboard\" incident put pressure on Australian Coach (AFP) AFP - Australian Coach John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sea rescue of boatpeople.","new_prediction":"Sports"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

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
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 1.0000 |
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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 17 chars
- **Prompt hash:** `d1c55024370f2e12`
- **ECS (full):** 0.6222
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["U.N.", "War", "Serbia"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `serbia`, `u.n`, `war`

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
{"rationale":"The classification is correct because the article discusses international relations and a war crimes court, which are typical topics found in the World category.","evidence":["U.N.", "War", "Serbia", "Hague", "Belgrade"]}
```

**Rationale text:**
> The classification is correct because the article discusses international relations and a war crimes court, which are typical topics found in the World category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `belgrade`, `hague`, `serbia`, `u.n`, `war`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: Sports, Business, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"NBA Court Transfers First Case to Serbia  BELGRADE (Reuters) - The NBA prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade.","new_prediction":"Sports"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

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
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.6000 |
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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 20 chars
- **Prompt hash:** `362cc0a1227d48a0`
- **ECS (full):** 0.6167
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Microsoft", "viruses", "browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `microsoft`, `virus`

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
{"rationale":"The classification is correct because the text discusses Microsoft, operating systems, and security patches, which are all related to science and technology.", "evidence":["Microsoft", "viruses", "browser", "email", "patch"]}
```

**Rationale text:**
> The classification is correct because the text discusses Microsoft, operating systems, and security patches, which are all related to science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `microsoft`, `patch`, `virus`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Sports, Business.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Google's big fix: Security patch now on the market For the past few years, viruses have attacked Google's operating system, Web browser or e-mail programs seemingly on a weekly basis.","new_prediction":"Business"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Microsoft", "Security", "viruses", "operating", "browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `security`(2), `virus`(3), `operating`(4), `browser`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.7500 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
{"label":"Sci/Tech"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 25 words
- **Raw response length:** 20 chars
- **Prompt hash:** ``
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 0
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```

```

**Response:**
```

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
{"label":"World"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `World` ✗
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 55 words
- **Raw response length:** 17 chars
- **Prompt hash:** ``
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 0
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```

```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```

```

**Response:**
```

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
- **Confidence:** 79.0%
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 18 chars
- **Prompt hash:** `1ed0148e7838e3a9`
- **ECS (full):** 0.5333
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["United", "States", "Russia"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `russia`, `state`, `united`

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
- Tokens: `foul`, `russia`, `sheryl`, `swoopes`, `united`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Business, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"China 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the China desperately looked for help. Then along came Sheryl Swoopes to set things right.","new_prediction":"World"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["United", "States", "Russia", "Sheryl", "Swoopes"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `united`(1), `state`(2), `russia`(3), `sheryl`(4), `swoopes`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 0.6000 |
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
{"label":"World, Sports, Business, or Sci/Tech"}
```

#### 2. Classification Response
```
{"label":"Sports"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 97.0%
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 18 chars
- **Prompt hash:** `97373d2318f574eb`
- **ECS (full):** 0.3905
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the 3 most important individual SINGLE WORDS from the input text that support this classification. List them in order of importance. Each item must be a single word — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Tennis", "ATP", "final"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `atp`, `final`, `tennis`

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
{"rationale":"This classification is correct because the text specifically mentions a tennis tournament, which is a sports event, and includes terminology commonly used in the sports domain.","evidence":["Tennis", "Shanghai", "Guillermo", "Canas", "Open"]}
```

**Rationale text:**
> This classification is correct because the text specifically mentions a tennis tournament, which is a sports event, and includes terminology commonly used in the sports domain.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `canas`, `guillermo`, `open`, `shanghai`, `tennis`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Create a counterfactual: change no more than 2 words by substituting them with different words. Focus your changes on the most topic-specific words — proper nouns, domain terms, or named entities that identify the topic. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Business, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Golf: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open golf tournament against unheralded German Lars Burgsmuller.","new_prediction":"World"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Rank the 5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the input text — no phrases, no hyphenated compounds, no multi-word expressions.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Tennis", "ATP", "Open", "Shanghai", "final"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tennis`(1), `atp`(2), `open`(3), `shanghai`(4), `final`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.4286 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### sst2_validation_0001 (ECS=0.7778)
- **Dataset:** sst2
- **Text:** holden caulfield did it better . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 79.0%

### ag_news_test_0001 (ECS=0.7333)
- **Dataset:** ag_news
- **Text:** Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed …
- **Ground truth:** `World` → **Predicted:** `World` ✓
- **Confidence:** 79.0%

### sst2_validation_0003 (ECS=0.7333)
- **Dataset:** sst2
- **Text:** neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 79.0%


## Low-ECS Examples

### sst2_validation_0006 (ECS=0.2560)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 79.0%

### sst2_validation_0000 (ECS=0.2643)
- **Dataset:** sst2
- **Text:** very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 97.0%

### mnli_validation_matched_0003 (ECS=0.3698)
- **Dataset:** mnli
- **Text:** Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.…
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 97.0%
