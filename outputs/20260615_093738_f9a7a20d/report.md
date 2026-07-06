# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 09:37:51
- **Duration:** 115.4s (1.9m)
- **Model:** llama-3.1-8b-instant
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 2450
- **Avg tokens per instance:** 272

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 1/2 (50%) | 0.511 | 50% | 50% | 0% | 50% |
| mnli | 3 | 3/3 (100%) | 0.426 | 100% | 100% | 100% | 100% |
| ag_news | 4 | 4/4 (100%) | 0.547 | 100% | 100% | 0% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (full) | 0.4972 |
| Mean ECS (primary: H,CF,RO) | 0.4342 |
| Primary ECS pairs <3 | 5 instances |
  → sst2_validation_0000: 1 pair(s), ECS_primary=0.3333
  → ag_news_test_0000: 1 pair(s), ECS_primary=0.4000
  → ag_news_test_0001: 1 pair(s), ECS_primary=0.6000
  → ag_news_test_0002: 1 pair(s), ECS_primary=0.6000
  → ag_news_test_0003: 1 pair(s), ECS_primary=0.3333
| Std ECS | 0.0983 |
| Median ECS | 0.5056 |
| Spearman ρ | 0.3293 (p=0.4258) |
| Mean CC3 size | 2.56 |
| Mean CC4 size | 2.00 |
| % instances with CC3 | 88.9% |
| % instances with CC4 | 88.9% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.5167 |
| H–CF | 0.2534 |
| H–RO | 0.4938 |
| R–CF | 0.2981 |
| R–RO | 0.6062 |
| CF–RO | 0.3920 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 8/9 (89%) | 8/9 (89%) |
| Rationale | 8/9 (89%) | 8/9 (89%) |
| Counterfactual | 3/9 (33%) | 3/9 (33%) |
| Rank Ordering | 8/9 (89%) | 8/9 (89%) |
| All 4 valid | 3/9 |
| 3 valid (CC3 adjusted) | 5/9 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.4972 | [0.4255, 0.5618] |
| Spearman ρ | 0.3293 | [-0.5748, 0.8771] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's great escapist fun that recreates a place and time that will never happen again . "

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"positive or negative","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"positive","confidence":8.5}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `8f7d9cf2630f205e`
- **ECS (full):** 0.5111
- **ECS (primary):** 0.3333
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CC3 size:** 2 | **CC4 size:** 2

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
 "evidence":["great","fun","recreates","happen","again"]}
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
{"counterfactual_text":"it's great deprecating fun that recreates a place and time that will never happen again .","new_prediction":"negative"}
```

**Parsed tokens:**
- *Not parsed*

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
{"ranking":["great","fun","recreates","never","happen"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`(1), `fun`(2), `recreates`(3), `never`(4), `happen`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | — |
| H–RO | 0.3333 |
| R–CF | — |
| R–RO | 0.8000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "verbinski implements every hack-artist trick to give us the ooky-spookies . "

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"positive or negative","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"positive","confidence":8.2}
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

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"entailment, neutral, or contradiction","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"entailment", "confidence":7.8}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 62.0%
- **Model refused:** No
- **Prompt hash:** `1a3d0d43bf23eaa5`
- **ECS (full):** 0.5583
- **ECS (primary):** 0.4667
- **ECS primary pairs:** 3
- **Valid strategies:** 4
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
{"highlights":["Jon's","defense","weaken"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `jon's`, `weaken`

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
{"rationale":"The premise directly implies that Jon's defense is weakening, which is a key aspect of losing strength and defense, making the hypothesis a logical consequence.", "evidence":["Jon's","defense","weaken","slow","defense"]}
```

**Rationale text:**
> The premise directly implies that Jon's defense is weakening, which is a key aspect of losing strength and defense, making the hypothesis a logical consequence.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `jon's`, `slow`, `weaken`

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
{"ranking":["weaken", "slow", "defense", "Jon's", "began"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `weaken`(1), `slow`(2), `defense`(3), `jon's`(4), `began`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.7500 |
| H–CF | 0.3000 |
| H–RO | 0.6000 |
| R–CF | 0.4000 |
| R–RO | 0.8000 |
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

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"entailment, neutral, or contradiction","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"neutral", "confidence":7.8}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Confidence:** 52.0%
- **Model refused:** No
- **Prompt hash:** `7296da0bb0db7ae9`
- **ECS (full):** 0.3326
- **ECS (primary):** 0.2778
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CC3 size:** 3 | **CC4 size:** 2

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
"evidence":["Respondents", "question", "alternatives", "presenting", "past"]}
```

**Rationale text:**
> The premise does not provide any information about the board's past history, making it neutral to the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `alternative`, `past`, `presenting`, `question`, `respondent`

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
{"counterfactual_text":"Respondents to the Commission's question on whether the alternatives of presenting costs of State mission PP&H","new_prediction":"contradiction"}
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
{"ranking":["past","federal","question","board","history"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `past`(1), `federal`(2), `question`(3), `board`(4), `history`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.1875 |
| H–RO | 0.3333 |
| R–CF | 0.3125 |
| R–RO | 0.2500 |
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

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"entailment, neutral, or contradiction","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"contradiction", "confidence": 8.5}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `b140cb50b73eff64`
- **ECS (full):** 0.3864
- **ECS (primary):** 0.4621
- **ECS primary pairs:** 3
- **Valid strategies:** 4
- **CC3 size:** 4 | **CC4 size:** 1

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
{"highlights":["rare", "please", "unhappy"]}
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
"evidence":["everyone","pleased","everyone","unhappy"]}
```

**Rationale text:**
> The premise states that everyone is pleased, while the hypothesis states that everyone is unhappy, making them mutually exclusive claims.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `everyone`, `unhappy`

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
{"counterfactual_text": "It is one of those rare cases in which I can displease everyone.", "new_prediction": "entailment"}
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
{"ranking":["everyone", "happily", "unhappy", "please", "rare"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `everyone`(1), `please`(2), `rare`(3), `unhappy`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | 0.2727 |
| H–RO | 0.7500 |
| R–CF | 0.1818 |
| R–RO | 0.5000 |
| CF–RO | 0.3636 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Israeli security sources say."

Choose from: World, Sports, Business, Sci/Tech

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"World","confidence":8.7}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `3213a8463d1fb713`
- **ECS (full):** 0.5000
- **ECS (primary):** 0.4000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CC3 size:** 2 | **CC4 size:** 2

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
{"highlights":["Israeli","Egyptian","Gaza"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `egyptian`, `gaza`, `israeli`

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
{"rationale":"The classification is correct because the article discusses a geopolitical event involving a country and its border.", 
 "evidence":["Israeli","Egyptian","tank","Gaza","Strip"]}
```

**Rationale text:**
> The classification is correct because the article discusses a geopolitical event involving a country and its border.

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
{"ranking":["Israeli","Egyptian","tank","Israeli","Gaza"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `israeli`(1), `tank`(2), `egyptian`(3), `troop`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.4000 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis."

Choose from: World, Sports, Business, Sci/Tech

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"Sci/Tech","confidence":8.5}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `97c96526e8341585`
- **ECS (full):** 0.6222
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CC3 size:** 3 | **CC4 size:** 3

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
{"highlights":["Microsoft","patch","virus"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`, `patch`, `virus`

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
"evidence":["Microsoft","patch","virus","browser","programs"]}
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
- *Not parsed*

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
{"ranking":["Microsoft","patch","Security","virus","browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `patch`(2), `security`(3), `virus`(4), `browser`(5)

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

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions."

Choose from: World, Sports, Business, Sci/Tech

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"Sports", "confidence":8.5}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `0b567880791095e0`
- **ECS (full):** 0.6222
- **ECS (primary):** 0.6000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CC3 size:** 3 | **CC4 size:** 3

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
 "evidence":["Tournament", "Champions", "birdied", "Player", "place"]}
```

**Rationale text:**
> The text mentions a golf tournament and a player's performance, indicating a sports-related event.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `birdied`, `champion`, `place`, `player`, `tournament`

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
- *Not parsed*

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

Article: "California employee pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees ' Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc."

Choose from: World, Sports, Business, Sci/Tech

Rate your confidence on a scale from 1 to 10 (1=total guess, 10=certain). Do not use round numbers.

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<1-10>}
```

#### 2. Classification Response
```
{"label":"Business", "confidence":8.7}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 72.0%
- **Model refused:** No
- **Prompt hash:** `e086952844d4a2f6`
- **ECS (full):** 0.4444
- **ECS (primary):** 0.3333
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CC3 size:** 2 | **CC4 size:** 2

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
{"rationale":"The classification is correct because the text discusses a specific company and a financial transaction involving a pension fund.", "evidence":["Calpers", "shares", "PeopleSoft", "Inc", "tendering"]}
```

**Rationale text:**
> The classification is correct because the text discusses a specific company and a financial transaction involving a pension fund.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `calpers`, `inc`, `peoplesoft`, `share`, `tendering`

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
- *Not parsed*

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
{"ranking":["Calpers","PeopleSoft","shares","tendering","pension"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `calpers`(1), `peoplesoft`(2), `share`(3), `tendering`(4), `pension`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | — |
| H–RO | 0.3333 |
| R–CF | — |
| R–RO | 0.6667 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### ag_news_test_0002 (ECS=0.6222)
- **Dataset:** ag_news
- **Text:** Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the fir…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓
- **Confidence:** 72.0%

### ag_news_test_0001 (ECS=0.6222)
- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 72.0%

### mnli_validation_matched_0000 (ECS=0.5583)
- **Dataset:** mnli
- **Text:** Premise: Jon's defense began to weaken and slow.
Hypothesis: Jon began to lose his strength and defense.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 62.0%


## Low-ECS Examples

### mnli_validation_matched_0001 (ECS=0.3326)
- **Dataset:** mnli
- **Text:** Premise: Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&
Hypothesis: The board has bad history with presenting federal costs in the past.
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
- **Confidence:** 52.0%

### mnli_validation_matched_0002 (ECS=0.3864)
- **Dataset:** mnli
- **Text:** Premise: It is one of those rare cases in which I can please everyone.
Hypothesis: It's one of those situations where I end up making everyone unhappy.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 72.0%

### ag_news_test_0003 (ECS=0.4444)
- **Dataset:** ag_news
- **Text:** California employee pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees ' Retirement System (Calpers) is tendering its 1.5 million PeopleSoft …
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 72.0%
