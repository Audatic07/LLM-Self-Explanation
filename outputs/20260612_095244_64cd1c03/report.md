# Experiment Report: review_fixes_pilot

- **Date:** 2026-06-12 09:52:52
- **Duration:** 96.5s (1.6m)
- **Model:** llama-3.1-8b-instant
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 2670
- **Avg tokens per instance:** 297

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 1/2 (50%) | 0.282 | 100% | 100% | 100% | 100% |
| mnli | 3 | 3/3 (100%) | 0.537 | 100% | 100% | 0% | 100% |
| ag_news | 4 | 4/4 (100%) | 0.411 | 100% | 100% | 100% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (full) | 0.4245 |
| Mean ECS (primary: H,CF,RO) | 0.3957 |
| Std ECS | 0.1728 |
| Median ECS | 0.3778 |
| Spearman ρ | -0.2126 (p=0.5829) |
| Mean CC3 size | 1.56 |
| Mean CC4 size | 0.00 |
| % instances with CC3 | 66.7% |
| % instances with CC4 | 0.0% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.5122 |
| H–CF | 0.1333 |
| H–RO | 0.5000 |
| R–CF | 0.0400 |
| R–RO | 0.5902 |
| CF–RO | 0.1300 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 9/9 (100%) | 9/9 (100%) |
| Rationale | 9/9 (100%) | 9/9 (100%) |
| Counterfactual | 6/9 (67%) | 6/9 (67%) |
| Rank Ordering | 9/9 (100%) | 9/9 (100%) |
| All 4 parsed (CC possible) | 66.7% |

ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.4245 | [0.3255, 0.5519] |
| Spearman ρ | -0.2126 | [-0.8875, 0.5939] |

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
- **Confidence:** 85.0%
- **Model refused:** No
- **Prompt hash:** `8f7d9cf2630f205e`
- **ECS (full):** 0.3111
- **ECS (primary):** 0.2222
- **CC3 size:** 2 | **CC4 size:** 0

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
- Status: **Valid**
- Tokens: `escapist`

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
| H–CF | 0.3333 |
| H–RO | 0.3333 |
| R–CF | 0.0000 |
| R–RO | 0.8000 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
- **Confidence:** 82.0%
- **Model refused:** No
- **Prompt hash:** `d719c8a1feab36a1`
- **ECS (full):** 0.2528
- **ECS (primary):** 0.1500
- **CC3 size:** 1 | **CC4 size:** 0

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
{"highlights":["ooky-spookies","give","us"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `give`, `ooky-spookies`

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
{"rationale":"The text expresses enthusiasm and approval for the filmmaker's use of horror elements, indicated by the playful and affectionate tone.", 
 "evidence":["ooky-spookies", "us", "give", "trick", "us"]}
```

**Rationale text:**
> The text expresses enthusiasm and approval for the filmmaker's use of horror elements, indicated by the playful and affectionate tone.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `give`, `ooky-spookies`, `trick`

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
{"counterfactual_text":"verbinski implements every boring-artist trick to give us the ooky-spookies . ","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`

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
{"ranking":["ooky-spookies","hack-artist","trick","us","implements"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ooky-spookies`(1), `hack-artist`(2), `trick`(3), `implement`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | 0.0000 |
| H–RO | 0.2000 |
| R–CF | 0.0000 |
| R–RO | 0.4000 |
| CF–RO | 0.2500 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

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
- **Confidence:** 78.0%
- **Model refused:** No
- **Prompt hash:** `1a3d0d43bf23eaa5`
- **ECS (full):** 0.7167
- **ECS (primary):** 0.6000
- **CC3 size:** 0 | **CC4 size:** 0

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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: neutral, contradiction.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Jon's offense began to weaken and slow.","new_prediction":"contradiction"}
```

**Parsed tokens:**
- *Not parsed*

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
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.8000 |
| CF–RO | — |
| Kendall τ (H,RO) | -1.0000 |
| Normalized τ | 0.0000 |

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
- **Confidence:** 78.0%
- **Model refused:** No
- **Prompt hash:** `7296da0bb0db7ae9`
- **ECS (full):** 0.3944
- **ECS (primary):** 0.3333
- **CC3 size:** 0 | **CC4 size:** 0

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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: entailment, contradiction.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission problems","new_prediction":"contradiction"}
```

**Parsed tokens:**
- *Not parsed*

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
| H–CF | — |
| H–RO | 0.3333 |
| R–CF | — |
| R–RO | 0.2500 |
| CF–RO | — |
| Kendall τ (H,RO) | -1.0000 |
| Normalized τ | 0.0000 |

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
- **Confidence:** 85.0%
- **Model refused:** No
- **Prompt hash:** `b140cb50b73eff64`
- **ECS (full):** 0.5000
- **ECS (primary):** 0.7500
- **CC3 size:** 0 | **CC4 size:** 0

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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: entailment, neutral.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"It is one of those rare cases in which I can make everyone happy.", "new_prediction":"entailment"}
```

**Parsed tokens:**
- *Not parsed*

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
- Tokens: `everyone`(1), `unhappy`(2), `please`(3), `rare`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | — |
| H–RO | 0.7500 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | -1.0000 |
| Normalized τ | 0.0000 |

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
- **Confidence:** 87.0%
- **Model refused:** No
- **Prompt hash:** `3213a8463d1fb713`
- **ECS (full):** 0.7167
- **ECS (primary):** 0.7500
- **CC3 size:** 3 | **CC4 size:** 0

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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: Sports, Business, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian soldiers in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Israeli security sources say.",
"new_prediction":"Sports"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: 

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
- Tokens: `israeli`(1), `egyptian`(2), `tank`(3), `gaza`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | — |
| H–RO | 0.7500 |
| R–CF | — |
| R–RO | 0.8000 |
| CF–RO | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis."

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
- **Confidence:** 85.0%
- **Model refused:** No
- **Prompt hash:** `52a00be7254081bc`
- **ECS (full):** 0.3778
- **ECS (primary):** 0.2667
- **CC3 size:** 4 | **CC4 size:** 0

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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Sports, Business.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Microsoft #39;s big fix: Security patch now on the market For the past few years, bugs have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis.",
"new_prediction":"Business"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `virus`

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
{"ranking":["Microsoft","patch","Security","browser","virus"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `patch`(2), `security`(3), `browser`(4), `virus`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.0000 |
| H–RO | 0.6000 |
| R–CF | 0.2000 |
| R–RO | 0.6667 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

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
- **Confidence:** 85.0%
- **Model refused:** No
- **Prompt hash:** `0b567880791095e0`
- **ECS (full):** 0.3111
- **ECS (primary):** 0.2000
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

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Business, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Four players shoot opening-round 65 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions.",
"new_prediction":"Business"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `66`

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
| R–RO | 0.6667 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "California employee pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc."

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
- **Confidence:** 87.0%
- **Model refused:** No
- **Prompt hash:** `4f7abba953b122c1`
- **ECS (full):** 0.2397
- **ECS (primary):** 0.2889
- **CC3 size:** 1 | **CC4 size:** 0

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
{"rationale":"The classification is correct because the text discusses a specific company and a financial transaction involving a pension fund.", "evidence":["California", "Pension", "Fund", "Shares", "Inc"]}
```

**Rationale text:**
> The classification is correct because the text discusses a specific company and a financial transaction involving a pension fund.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `california`, `fund`, `inc`, `pension`, `share`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Create a minimal-edit counterfactual: change no more than 2 words by substituting them with different words. Do not insert new words or delete existing words — only substitute. Do not modify punctuation, numbers, or HTML-encoded characters. The new_prediction must be one of: World, Sports, Sci/Tech.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"California employee pension fund tenders Oracle shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1.5 million Oracle Inc.",
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
{"ranking":["Pension", "Fund", "Shares", "PeopleSoft", "Calpers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `pension`(1), `fund`(2), `share`(3), `peoplesoft`(4), `calpers`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | 0.3333 |
| H–RO | 0.3333 |
| R–CF | 0.0000 |
| R–RO | 0.4286 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |


## High-ECS Examples

### ag_news_test_0000 (ECS=0.7167)
- **Dataset:** ag_news
- **Text:** Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Isra…
- **Ground truth:** `World` → **Predicted:** `World` ✓
- **Confidence:** 87.0%

### mnli_validation_matched_0000 (ECS=0.7167)
- **Dataset:** mnli
- **Text:** Premise: Jon's defense began to weaken and slow.
Hypothesis: Jon began to lose his strength and defense.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 78.0%

### mnli_validation_matched_0002 (ECS=0.5000)
- **Dataset:** mnli
- **Text:** Premise: It is one of those rare cases in which I can please everyone.
Hypothesis: It's one of those situations where I end up making everyone unhappy.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 85.0%


## Low-ECS Examples

### ag_news_test_0003 (ECS=0.2397)
- **Dataset:** ag_news
- **Text:** California employee pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1.5 million PeopleSo…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 87.0%

### sst2_validation_0001 (ECS=0.2528)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `positive` ✗
- **Confidence:** 82.0%

### sst2_validation_0000 (ECS=0.3111)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 85.0%
