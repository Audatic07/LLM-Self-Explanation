# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 09:49:57
- **Duration:** 85.0s (1.4m)
- **Model:** llama-3.1-8b-instant
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 2295
- **Avg tokens per instance:** 255

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 1/2 (50%) | 0.508 | 50% | 50% | 50% | 50% |
| mnli | 3 | 3/3 (100%) | 0.417 | 100% | 100% | 100% | 100% |
| ag_news | 4 | 4/4 (100%) | 0.413 | 100% | 100% | 75% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (full) | 0.4264 |
| Mean ECS (primary: H,CF,RO) | 0.4135 |
| Primary ECS pairs <3 | 1 instances |
  → ag_news_test_0000: 1 pair(s), ECS_primary=0.6000
| Std ECS | 0.1233 |
| Median ECS | 0.4417 |
| Spearman ρ | 0.0261 (p=0.9511) |
| Mean CC3 size | 2.89 |
| Mean CC4 size | 1.56 |
| % instances with CC3 | 88.9% |
| % instances with CC4 | 66.7% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.4625 |
| H–CF | 0.2324 |
| H–RO | 0.6354 |
| R–CF | 0.2770 |
| R–RO | 0.5295 |
| CF–RO | 0.2878 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 8/9 (89%) | 8/9 (89%) |
| Rationale | 8/9 (89%) | 8/9 (89%) |
| Counterfactual | 7/9 (78%) | 7/9 (78%) |
| CF flip verified | 1/7 (14%) |
| Rank Ordering | 8/9 (89%) | 8/9 (89%) |
| All 4 valid | 7/9 |
| 3 valid (CC3 adjusted) | 1/9 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.4264 | [0.3437, 0.5073] |
| Spearman ρ | 0.0261 | [-0.8948, 0.7309] |

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
- **Confidence:** 75.0%
- **Model refused:** No
- **Prompt hash:** `26dd26288e7734de`
- **ECS (full):** 0.5083
- **ECS (primary):** 0.5833
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["great","escapist","fun"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `escapist`, `fun`, `great`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text expresses enthusiasm and appreciation for the experience, indicating a positive sentiment.", 
 "evidence":["great", "fun", "recreates", "happen", "again"]}
```

**Rationale text:**
> The text expresses enthusiasm and appreciation for the experience, indicating a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fun`, `great`, `happen`, `recreates`

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
{"counterfactual_text":"it's great frustrating fun that recreates a place and time that will never happen again .","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `escapist`, `fun`, `great`, `happen`, `never`, `place`, `recreates`, `time`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["great","escapist","fun","recreates","positive"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`(1), `escapist`(2), `fun`(3)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | 0.3750 |
| H–RO | 1.0000 |
| R–CF | 0.5000 |
| R–RO | 0.4000 |
| CF–RO | 0.3750 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
{"label": "positive"}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `positive` ✗
- **Confidence:** 75.0%
- **Model refused:** No
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

### mnli_validation_matched_0000

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Jon's defense began to weaken and slow.
Hypothesis: Jon began to lose his strength and defense.

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
- **Confidence:** 75.0%
- **Model refused:** No
- **Prompt hash:** `06e98be6668ed303`
- **ECS (full):** 0.5278
- **ECS (primary):** 0.4667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** No
- **CF actual label:** `entailment`
- **CC3 size:** 4 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["defense","weaken","slow"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `slow`, `weaken`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The premise directly implies that Jon's defense is weakening, which is a key aspect of the hypothesis that he is losing strength and defense.", 
 "evidence":["Jon's", "weaken", "slow", "lose", "defense"]}
```

**Rationale text:**
> The premise directly implies that Jon's defense is weakening, which is a key aspect of the hypothesis that he is losing strength and defense.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `jon's`, `lose`, `slow`, `weaken`

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
{"counterfactual_text":"Mike's defense began to weaken and slow.","new_prediction":"contradiction"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `began`, `defense`, `hypothesis`, `jon`, `jon's`, `lose`, `premise`, `slow`, `strength`, `weaken`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["weaken","slow","defense","lose","strength"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `weaken`(1), `slow`(2), `defense`(3), `lose`(4), `strength`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.3000 |
| H–RO | 0.6000 |
| R–CF | 0.5000 |
| R–RO | 0.6667 |
| CF–RO | 0.5000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0001

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&
Hypothesis: The board has bad history with presenting federal costs in the past.

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
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `40670994e88e99cc`
- **ECS (full):** 0.2650
- **ECS (primary):** 0.2778
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["question","alternatives","past"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `alternative`, `past`, `question`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The premise does not provide any information about the board's past history, making it neutral to the hypothesis.", 
 "evidence":["Respondents", "question", "whether", "alternatives", "costs"]}
```

**Rationale text:**
> The premise does not provide any information about the board's past history, making it neutral to the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `alternative`, `cost`, `question`, `respondent`, `whether`

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
{"counterfactual_text":"Respondents to the Board's question on whether the alternatives of presenting costs of State mission PP&H","new_prediction":"contradiction"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `alternative`, `bad`, `board`, `board's`, `cost`, `federal`, `history`, `hypothesis`, `mission`, `past`, `pp`, `premise`, `presenting`, `question`, `respondent`, `whether`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: neutral

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["past","federal","question","presenting","history"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `past`(1), `federal`(2), `question`(3), `presenting`(4), `history`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | 0.1875 |
| H–RO | 0.3333 |
| R–CF | 0.3125 |
| R–RO | 0.1111 |
| CF–RO | 0.3125 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: It is one of those rare cases in which I can please everyone.
Hypothesis: It's one of those situations where I end up making everyone unhappy.

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
- **Confidence:** 95.0%
- **Model refused:** No
- **Prompt hash:** `12aa5c3f6d10e094`
- **ECS (full):** 0.4583
- **ECS (primary):** 0.4621
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 4 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["rare","please","unhappy"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `please`, `rare`, `unhappy`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The premise states that everyone is pleased, while the hypothesis states that everyone is unhappy, making them mutually exclusive claims.",
"evidence":["everyone","please","hypothesis","unhappy","everyone"]}
```

**Rationale text:**
> The premise states that everyone is pleased, while the hypothesis states that everyone is unhappy, making them mutually exclusive claims.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `everyone`, `hypothesis`, `please`, `unhappy`

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
{"counterfactual_text":"It is one of those rare cases in which I can displease everyone.",
"new_prediction":"entailment"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `case`, `end`, `everyone`, `hypothesis`, `making`, `one`, `please`, `premise`, `rare`, `situation`, `unhappy`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["rare","everyone","happily","unhappy","please"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `rare`(1), `everyone`(2), `unhappy`(3), `please`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | 0.2727 |
| H–RO | 0.7500 |
| R–CF | 0.3636 |
| R–RO | 0.6000 |
| CF–RO | 0.3636 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Israeli security sources say."

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
- **Confidence:** 75.0%
- **Model refused:** No
- **Prompt hash:** `b4839c59bc60cbb1`
- **ECS (full):** 0.6222
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Israeli","Egyptian","tank"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `egyptian`, `israeli`, `tank`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the article discusses a geopolitical event involving a country (Israel) and its border with another country (Egypt).",
"evidence":["Israeli","Egyptian","tank","Gaza","Strip"]}
```

**Rationale text:**
> The classification is correct because the article discusses a geopolitical event involving a country (Israel) and its border with another country (Egypt).

**Parsed tokens:**
- Status: **Valid**
- Tokens: `egyptian`, `gaza`, `israeli`, `strip`, `tank`

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
{"counterfactual_text":"Israeli tank kills three Egyptian soldiers An Israeli tank has opened fire and killed three Egyptian soldiers in a border zone near the Sinai Peninsula after mistaking them for Palestinian arms smugglers, Israeli security sources say.",
"new_prediction":"World"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Israeli","Egyptian","tank","Israeli","troops"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `israeli`(1), `tank`(2), `egyptian`(3), `troop`(4), `gaza`(5)

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

### ag_news_test_0001

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
- **Confidence:** 95.0%
- **Model refused:** No
- **Prompt hash:** `362cc0a1227d48a0`
- **ECS (full):** 0.4251
- **ECS (primary):** 0.3404
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 4 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Microsoft","patch","browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `microsoft`, `patch`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the text discusses a specific software-related issue and its solution, indicating a focus on technology.", 
 "evidence":["Microsoft", "patch", "virus", "browser", "programs"]}
```

**Rationale text:**
> The classification is correct because the text discusses a specific software-related issue and its solution, indicating a focus on technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `microsoft`, `patch`, `program`, `virus`

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
{"counterfactual_text":"Google's big fix: Security patch now on the market For the past few years, viruses have attacked Google's operating system, Web browser or e-mail programs seemingly on a weekly basis.",
"new_prediction":"Business"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `attacked`, `basis`, `big`, `browser`, `e-mail`, `fix`, `market`, `microsoft`, `operating`, `past`, `patch`, `program`, `security`, `seemingly`, `system`, `virus`, `web`, `weekly`, `year`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Microsoft","Security","patch","viruses","browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `security`(2), `patch`(3), `virus`(4), `browser`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.1579 |
| H–RO | 0.6000 |
| R–CF | 0.2632 |
| R–RO | 0.6667 |
| CF–RO | 0.2632 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions."

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
- **Confidence:** 95.0%
- **Model refused:** No
- **Prompt hash:** `cb67ba467aeb6bbd`
- **ECS (full):** 0.3667
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["Tournament", "Player", "Champions"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `champion`, `player`, `tournament`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The text mentions a golf tournament and a player's performance, indicating a sports-related event.", 
"evidence":["Tournament", "Champions", "birdied", "Player", "round"]}
```

**Rationale text:**
> The text mentions a golf tournament and a player's performance, indicating a sports-related event.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `birdied`, `champion`, `player`, `round`, `tournament`

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
{"counterfactual_text":"Four players shoot opening-round 66 Seminole, Fla. -- Grace Kim, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions.",
"new_prediction":"World"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ala`, `park`, `semmes`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Tournament", "Player", "Champions", "round", "birdied"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tournament`(1), `player`(2), `champion`(3), `round`(4), `birdied`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.0000 |
| H–RO | 0.6000 |
| R–CF | 0.0000 |
| R–RO | 1.0000 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "California employee pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees ' Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc."

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
- **Confidence:** 75.0%
- **Model refused:** No
- **Prompt hash:** `2a2bc5cfe80380f3`
- **ECS (full):** 0.2375
- **ECS (primary):** 0.3778
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["California", "PeopleSoft", "Calpers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `california`, `calpers`, `peoplesoft`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Provide a one-sentence rationale explaining why this classification is correct. Then list no more than 5 individual single words from the input text that serve as evidence. Each evidence item must be a single word copied verbatim from the input — no phrases, no clauses, no sentences.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word","word","word","word","word"]}
```

**Response:**
```
{"rationale":"The classification is correct because the text discusses a financial transaction involving a pension fund and a company's shares, indicating a business-related topic.",
"evidence":["California", "pension", "fund", "shares", "Business"]}
```

**Rationale text:**
> The classification is correct because the text discusses a financial transaction involving a pension fund and a company's shares, indicating a business-related topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `california`, `fund`, `pension`, `share`

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
{"counterfactual_text":"California employee pension fund tenders Oracle shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees ' Retirement System (Calpers) is tendering its 1.5 million Oracle Inc.",
"new_prediction":"Sci/Tech"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `peoplesoft`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["California", "PeopleSoft", "Calpers", "Retirement", "System"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `california`(1), `peoplesoft`(2), `calpers`(3), `retirement`(4), `system`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1667 |
| H–CF | 0.3333 |
| H–RO | 0.6000 |
| R–CF | 0.0000 |
| R–RO | 0.1250 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### ag_news_test_0000 (ECS=0.6222)
- **Dataset:** ag_news
- **Text:** Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Isra…
- **Ground truth:** `World` → **Predicted:** `World` ✓
- **Confidence:** 75.0%

### mnli_validation_matched_0000 (ECS=0.5278)
- **Dataset:** mnli
- **Text:** Premise: Jon's defense began to weaken and slow.
Hypothesis: Jon began to lose his strength and defense.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 75.0%

### sst2_validation_0000 (ECS=0.5083)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 75.0%


## Low-ECS Examples

### ag_news_test_0003 (ECS=0.2375)
- **Dataset:** ag_news
- **Text:** California employee pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees ' Retirement System (Calpers) is tendering its 1.5 million PeopleSoft …
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 75.0%

### mnli_validation_matched_0001 (ECS=0.2650)
- **Dataset:** mnli
- **Text:** Premise: Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&
Hypothesis: The board has bad history with presenting federal costs in the past.
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
- **Confidence:** 72.0%

### ag_news_test_0002 (ECS=0.3667)
- **Dataset:** ag_news
- **Text:** Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the fir…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓
- **Confidence:** 95.0%
