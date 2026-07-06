# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-11 15:21:51
- **Duration:** 75.9s (1.3m)
- **Model:** llama-3.1-8b-instant
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 2681
- **Avg tokens per instance:** 298

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 1/2 (50%) | 0.396 | 100% | 100% | 100% | 100% |
| mnli | 3 | 2/3 (67%) | 0.172 | 67% | 100% | 100% | 67% |
| ag_news | 4 | 4/4 (100%) | 0.309 | 100% | 100% | 100% | 75% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (full) | 0.2825 |
| Mean ECS (primary: H,CF,RO) | 0.2272 |
| Std ECS | 0.1274 |
| Median ECS | 0.3389 |
| Spearman ρ | -0.4140 (p=0.2679) |
| Mean CC3 size | 1.78 |
| Mean CC4 size | 0.44 |
| % instances with CC3 | 77.8% |
| % instances with CC4 | 44.4% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.4992 |
| H–CF | 0.1887 |
| H–RO | 0.4619 |
| R–CF | 0.1493 |
| R–RO | 0.4737 |
| CF–RO | 0.1037 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 8/9 (89%) | 8/9 (89%) |
| Rationale | 9/9 (100%) | 9/9 (100%) |
| Counterfactual | 9/9 (100%) | 9/9 (100%) |
| Rank Ordering | 7/9 (78%) | 7/9 (78%) |
| All 4 parsed (CC possible) | 77.8% |

ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2825 | [0.1951, 0.3588] |
| Spearman ρ | -0.4140 | [-0.8393, 0.1058] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's great escapist fun that recreates a place and time that will never happen again . "

Return only valid JSON:
{"label":"positive or negative","confidence":<0-100>}
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
- **Prompt hash:** `8922c915481edfbc`
- **ECS (full):** 0.4028
- **ECS (primary):** 0.3389
- **CC3 size:** 2 | **CC4 size:** 1

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

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The text expresses a positive sentiment because it describes the experience as 'great' and 'fun', indicating a high level of enjoyment.", "evidence":["great", "fun"]}
```

**Rationale text:**
> The text expresses a positive sentiment because it describes the experience as 'great' and 'fun', indicating a high level of enjoyment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fun`, `great`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"it's terrible escapist fun that recreates a place and time that will never happen again . ","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`, `terrible`

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
{"ranking":["great","escapist","fun","recreates","never"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`(1), `escapist`(2), `fun`(3), `recreates`(4), `never`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | 0.2500 |
| H–RO | 0.6000 |
| R–CF | 0.3333 |
| R–RO | 0.4000 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "verbinski implements every hack-artist trick to give us the ooky-spookies . "

Return only valid JSON:
{"label":"positive or negative","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"positive","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `positive` ✗
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `5576f165fb33daa6`
- **ECS (full):** 0.3889
- **ECS (primary):** 0.2500
- **CC3 size:** 2 | **CC4 size:** 1

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
{"highlights":["ooky-spookies","us","give"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `give`, `ooky-spookies`, `u`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The text expresses enthusiasm and approval for the film's use of horror elements, indicating a positive sentiment.", "evidence":["us", "give", "ooky-spookies"]}
```

**Rationale text:**
> The text expresses enthusiasm and approval for the film's use of horror elements, indicating a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `give`, `ooky-spookies`, `u`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"verbinski implements every hack-artist trick to give us the boring-spookies . ","new_prediction":"negative"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `boring-spookies`, `ooky-spookies`

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
{"ranking":["ooky-spookies","hack-artist","trick","us","verbinski"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ooky-spookies`(1), `hack-artist`(2), `trick`(3), `u`(4), `verbinski`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.2500 |
| H–RO | 0.3333 |
| R–CF | 0.2500 |
| R–RO | 0.3333 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### mnli_validation_matched_0000

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise [SEP] Hypothesis: "Jon's defense began to weaken and slow. [SEP] Jon began to lose his strength and defense."

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction","confidence":<0-100>}
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
- **Prompt hash:** `60c2ea0b81b59b67`
- **ECS (full):** 0.3389
- **ECS (primary):** 0.2000
- **CC3 size:** 3 | **CC4 size:** 0

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
{"highlights":["weaken", "lose", "defense"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `lose`, `weaken`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The classification as entailment is correct because the premise provides a specific description of Jon's defense weakening, which logically leads to the conclusion that he began to lose his strength and defense, as described in the hypothesis.", "evidence":["weaken", "slow", "lose", "strength", "defense"]}
```

**Rationale text:**
> The classification as entailment is correct because the premise provides a specific description of Jon's defense weakening, which logically leads to the conclusion that he began to lose his strength and defense, as described in the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `lose`, `slow`, `strength`, `weaken`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Jon's defense began to weaken and speed. [SEP] Jon began to lose his strength and defense.","new_prediction":"contradiction"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `slow`, `speed`

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
{"ranking":["weaken", "lose", "defense", "began", "strength"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `weaken`(1), `lose`(2), `defense`(3), `began`(4), `strength`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.0000 |
| H–RO | 0.6000 |
| R–CF | 0.1667 |
| R–RO | 0.6667 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0001

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise [SEP] Hypothesis: "Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has bad history with presenting federal costs in the past."

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"entailment", "confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `9b509fc51c0943e8`
- **ECS (full):** 0.1778
- **ECS (primary):** 0.1667
- **CC3 size:** 2 | **CC4 size:** 0

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
{"highlights":["past","has","bad"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bad`, `past`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The premise entails the hypothesis because it provides a specific reason for the board's potential issue with presenting federal costs, implying that the bad history is a contributing factor to the current problem.", "evidence":["The board has bad history with presenting federal costs in the past", "Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP"]}
```

**Rationale text:**
> The premise entails the hypothesis because it provides a specific reason for the board's potential issue with presenting federal costs, implying that the bad history is a contributing factor to the current problem.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `alternative`, `bad`, `board`, `board's`, `cost`, `federal`, `history`, `mission`, `past`, `pp`, `presenting`, `question`, `respondent`, `whether`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp The board has good history with presenting federal costs in the past.", "new_prediction":"contradiction"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bad`, `good`

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
{"ranking":["past","federal","board","history","presenting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `past`(1), `federal`(2), `board`(3), `history`(4), `presenting`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1429 |
| H–CF | 0.3333 |
| H–RO | 0.1667 |
| R–CF | 0.0667 |
| R–RO | 0.3571 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise [SEP] Hypothesis: "It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone unhappy."

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"contradiction","confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `127df198b63a92cb`
- **ECS (full):** 0.0000
- **ECS (primary):** 0.0000
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
{"highlights":["everyone","unhappy","happily"]}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The text is classified as a contradiction because it presents two mutually exclusive statements that cannot be true at the same time, indicating a logical contradiction between the premise and the hypothesis.",
 "evidence":["I", "can", "please", "everyone", "I", "end", "up", "making", "everyone", "unhappy"]}
```

**Rationale text:**
> The text is classified as a contradiction because it presents two mutually exclusive statements that cannot be true at the same time, indicating a logical contradiction between the premise and the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `end`, `everyone`, `making`, `please`, `unhappy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone equally unhappy.",
"new_prediction":"entailment"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `equally`

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
{"ranking":["everyone","unhappy","please","rare","happily"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | 0.0000 |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Israeli security sources say."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"World","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `b156d7f3a79ce82c`
- **ECS (full):** 0.3778
- **ECS (primary):** 0.3333
- **CC3 size:** 0 | **CC4 size:** 0

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

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The classification as 'World' is correct because the article mentions a specific geographic location (the Gaza Strip) and a country (Egypt) and a military action involving a tank, indicating a global event.", "evidence":["Israeli", "Egyptian", "Gaza", "Strip", "tank"]}
```

**Rationale text:**
> The classification as 'World' is correct because the article mentions a specific geographic location (the Gaza Strip) and a country (Egypt) and a military action involving a tank, indicating a global event.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `egyptian`, `gaza`, `israeli`, `strip`, `tank`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Israeli tank kills three Israeli troops An Israeli tank has opened fire and killed three Israeli troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Israeli security sources say.",
"new_prediction":"Sports"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `egyptian`

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
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.3333 |
| H–RO | — |
| R–CF | 0.2000 |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"Sci/Tech","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `1eb9278ea1e99466`
- **ECS (full):** 0.2561
- **ECS (primary):** 0.2421
- **CC3 size:** 2 | **CC4 size:** 1

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
{"highlights":["Microsoft","patch","operating"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`, `operating`, `patch`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The classification is correct because the text mentions specific computer-related components and a security patch, indicating a focus on technology and computing.", "evidence":["Microsoft", "operating system", "Web browser", "e-mail programs", "viruses", "patch"]}
```

**Rationale text:**
> The classification is correct because the text mentions specific computer-related components and a security patch, indicating a focus on technology and computing.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `e-mail`, `microsoft`, `operating`, `patch`, `program`, `system`, `virus`, `web`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Microsoft's big fix: Economic patch now on the market For the past few years, viruses have attacked Microsoft's operating system, Web browser or e-mail programs seemingly on a weekly basis.",
"new_prediction":"Business"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `39;s`, `economic`, `microsoft`, `microsoft's`, `security`

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
| H–R | 0.3333 |
| H–CF | 0.1429 |
| H–RO | 0.3333 |
| R–CF | 0.0769 |
| R–RO | 0.4000 |
| CF–RO | 0.2500 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"Sports","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `ba8c190006964532`
- **ECS (full):** 0.3893
- **ECS (primary):** 0.3143
- **CC3 size:** 3 | **CC4 size:** 1

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

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The text was classified as Sports because it mentions a specific golf tournament and the Player of the Year race, indicating a focus on a competitive athletic event.",
"evidence":["Tournament", "Champions", "Player", "Year", "birdied", "hole", "round"]}
```

**Rationale text:**
> The text was classified as Sports because it mentions a specific golf tournament and the Player of the Year race, indicating a focus on a competitive athletic event.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `birdied`, `champion`, `hole`, `player`, `round`, `tournament`, `year`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the World Cup race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions.",
"new_prediction":"World"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cup`, `player`, `year`

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
| H–R | 0.4286 |
| H–CF | 0.2000 |
| H–RO | 0.6000 |
| R–CF | 0.2500 |
| R–RO | 0.7143 |
| CF–RO | 0.1429 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "California employee pension fund tenders PeopleSoft shares to &lt;b&gt;...&lt;/b&gt; NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc."

Choose from: World, Sports, Business, Sci/Tech

Return only valid JSON:
{"label":"World, Sports, Business, or Sci/Tech","confidence":<0-100>}
```

#### 2. Classification Response
```
{"label":"Business", "confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `acbf1338eaa356c1`
- **ECS (full):** 0.2111
- **ECS (primary):** 0.2000
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

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The classification as Business is correct because the text mentions a specific company (PeopleSoft Inc.) and a financial institution (California Employees' Retirement System) in the context of a financial transaction (tendering shares).",
 "evidence":["PeopleSoft", "Inc", "California", "Employees", "Retirement", "System", "tendering", "shares"]}
```

**Rationale text:**
> The classification as Business is correct because the text mentions a specific company (PeopleSoft Inc.) and a financial institution (California Employees' Retirement System) in the context of a financial transaction (tendering shares).

**Parsed tokens:**
- Status: **Valid**
- Tokens: `california`, `employee`, `inc`, `peoplesoft`, `retirement`, `share`, `system`, `tendering`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"California employee pension fund tenders PeopleSoft shares to a World leader NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc.",
"new_prediction":"World"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `b>...</b`, `leader`

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
| H–R | 0.2222 |
| H–CF | 0.0000 |
| H–RO | 0.6000 |
| R–CF | 0.0000 |
| R–RO | 0.4444 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |


## High-ECS Examples

### sst2_validation_0000 (ECS=0.4028)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 80.0%

### ag_news_test_0002 (ECS=0.3893)
- **Dataset:** ag_news
- **Text:** Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the fir…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓
- **Confidence:** 80.0%

### sst2_validation_0001 (ECS=0.3889)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `positive` ✗
- **Confidence:** 80.0%


## Low-ECS Examples

### mnli_validation_matched_0002 (ECS=0.0000)
- **Dataset:** mnli
- **Text:** It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone unhappy.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%

### mnli_validation_matched_0001 (ECS=0.1778)
- **Dataset:** mnli
- **Text:** Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has bad history with presenting federal costs in the past.
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗
- **Confidence:** 80.0%

### ag_news_test_0003 (ECS=0.2111)
- **Dataset:** ag_news
- **Text:** California employee pension fund tenders PeopleSoft shares to &lt;b&gt;...&lt;/b&gt; NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 80.0%
