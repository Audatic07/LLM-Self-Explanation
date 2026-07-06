# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-11 14:27:31
- **Duration:** 40.2s (0.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 2721
- **Avg tokens per instance:** 302

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 2/2 (100%) | 0.410 | 100% | 100% | 100% | 50% |
| mnli | 3 | 2/3 (67%) | 0.349 | 100% | 100% | 100% | 67% |
| ag_news | 4 | 4/4 (100%) | 0.371 | 100% | 100% | 75% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (full) | 0.3721 |
| Mean ECS (primary: H,CF,RO) | 0.2966 |
| Std ECS | 0.0838 |
| Median ECS | 0.4083 |
| Spearman ρ | -0.1063 (p=0.7855) |
| Mean CC3 size | 1.78 |
| Mean CC4 size | 0.33 |
| % instances with CC3 | 66.7% |
| % instances with CC4 | 33.3% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.5343 |
| H–CF | 0.1562 |
| H–RO | 0.5238 |
| R–CF | 0.1711 |
| R–RO | 0.6218 |
| CF–RO | 0.1210 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 9/9 (100%) | 9/9 (100%) |
| Rationale | 9/9 (100%) | 9/9 (100%) |
| Counterfactual | 8/9 (89%) | 8/9 (89%) |
| Rank Ordering | 7/9 (78%) | 7/9 (78%) |
| All 4 parsed (CC possible) | 66.7% |

ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.3721 | [0.3144, 0.4219] |
| Spearman ρ | -0.1063 | [-0.7536, 0.6670] |

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
{"label":"positive","confidence":90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 90.0%
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
{"highlights":["great","fun","escapist"]}
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
{"rationale":"The text is classified as positive because it describes the experience as 'great escapist fun', which implies an enjoyable and entertaining experience.","evidence":["great","fun"]}
```

**Rationale text:**
> The text is classified as positive because it describes the experience as 'great escapist fun', which implies an enjoyable and entertaining experience.

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
{"counterfactual_text":"it 's terrible escapist fun that recreates a place and time that will never happen again .","new_prediction":"negative"}
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
{"ranking":["great","fun","escapist","place","time"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `great`(1), `fun`(2), `escapist`(3), `place`(4), `time`(5)

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
{"label":"negative","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `5576f165fb33daa6`
- **ECS (full):** 0.4167
- **ECS (primary):** 0.2500
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 3 most important single tokens (words) from the input text that support this classification. List them in order of importance.

Return only valid JSON — each token must be copied verbatim from the input text:
{"highlights":["token1","token2","token3"]}
```

**Response:**
```
{"highlights":["hack-artist","ooky-spookies","trick"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `ooky-spookies`, `trick`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Provide a one-sentence rationale explaining why this classification is correct, and list the specific evidence tokens (individual words from the input text) that support it.

Return only valid JSON:
{"rationale":"<one sentence explanation>","evidence":["word1","word2","..."]}
```

**Response:**
```
{"rationale":"The text is classified as negative because it uses derogatory language to describe the artist's techniques, implying a lack of genuine skill or talent.","evidence":["hack-artist","ooky-spookies"]}
```

**Rationale text:**
> The text is classified as negative because it uses derogatory language to describe the artist's techniques, implying a lack of genuine skill or talent.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `ooky-spookies`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: modify as few words as possible to change the classification to a different category. Change only the words most critical to the classification.

Return only valid JSON:
{"counterfactual_text":"<the minimally modified text>","new_prediction":"<flipped label>"}
```

**Response:**
```
{"counterfactual_text":"verbinski implements every skilled-artist trick to give us the ooky-spookies .","new_prediction":"positive"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `skilled-artist`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important single tokens (individual words) for this classification, from most important to least important. Each token must be a single word copied verbatim from the input text.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["hack-artist","ooky-spookies","trick","every","hacks" is not present, so "to" is the next best choice, but actually "hack" is part of "hack-artist" so the next best is "ooky" is part of "ooky-spookies" so the next best is "trick" is already used so the next is "every" is already used so the next is "to" is already mentioned so the next is "us" is not as strong as "to" so the next is actually "hack" is not present alone so "ooky" is not present alone so the next best is actually "give" no, "to" is a better choice than "give" or "us": "to"]} 

However a better answer is 
{"ranking":["hack-artist","ooky-spookies","trick","every","to"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | 0.2500 |
| H–RO | — |
| R–CF | 0.3333 |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

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
{"label":"entailment","confidence":95}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Prompt hash:** `60c2ea0b81b59b67`
- **ECS (full):** 0.4083
- **ECS (primary):** 0.3389
- **CC3 size:** 3 | **CC4 size:** 1

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
{"highlights":["weaken", "defense", "strength"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `defense`, `strength`, `weaken`

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
{"rationale":"The classification is correct because the premise describes Jon's defense weakening and slowing, which logically leads to the hypothesis that Jon began to lose his strength and defense","evidence":["weaken", "slow", "lose", "strength", "defense"]}
```

**Rationale text:**
> The classification is correct because the premise describes Jon's defense weakening and slowing, which logically leads to the hypothesis that Jon began to lose his strength and defense

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
{"counterfactual_text":"Jon's defense began to strengthen and slow. [SEP] Jon began to lose his strength and defense.","new_prediction":"contradiction"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `strengthen`, `weaken`

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
{"ranking":["began","weaken","lose","strength","defense"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `began`(1), `weaken`(2), `lose`(3), `strength`(4), `defense`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.2500 |
| H–RO | 0.6000 |
| R–CF | 0.1667 |
| R–RO | 0.6667 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

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
{"label":"entailment","confidence":80}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Confidence:** 80.0%
- **Model refused:** No
- **Prompt hash:** `9b509fc51c0943e8`
- **ECS (full):** 0.2222
- **ECS (primary):** 0.1111
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
{"highlights":["Board's", "Federal", "costs"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `board's`, `cost`, `federal`

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
{"rationale":"The classification is correct because the premise implies that the board has experience with presenting federal costs, which suggests a history of doing so, thereby supporting the hypothesis that the board has a bad history with presenting federal costs in the past.","evidence":["history","past","presenting","federal","costs"]}
```

**Rationale text:**
> The classification is correct because the premise implies that the board has experience with presenting federal costs, which suggests a history of doing so, thereby supporting the hypothesis that the board has a bad history with presenting federal costs in the past.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `cost`, `federal`, `history`, `past`, `presenting`

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
{"counterfactual_text":"Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has good history with presenting federal costs in the past.","new_prediction":"contradiction"}
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
{"ranking":["past","history","costs","federal","board"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `past`(1), `history`(2), `cost`(3), `federal`(4), `board`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3333 |
| H–CF | 0.0000 |
| H–RO | 0.3333 |
| R–CF | 0.0000 |
| R–RO | 0.6667 |
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
- **ECS (full):** 0.4167
- **ECS (primary):** 0.3333
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
{"highlights":["everyone","everyone","unhappy"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `everyone`, `unhappy`

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
{"rationale":"The classification is correct because the premise states that it's a rare case where everyone is pleased, which directly contradicts the hypothesis that everyone ends up unhappy.","evidence":["everyone","please","unhappy"]}
```

**Rationale text:**
> The classification is correct because the premise states that it's a rare case where everyone is pleased, which directly contradicts the hypothesis that everyone ends up unhappy.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `everyone`, `please`, `unhappy`

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
{"counterfactual_text":"It is one of those rare cases in which I can please everyone. It's one of those situations where I end up making everyone happy.","new_prediction":"entailment"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happy`, `unhappy`

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
{"ranking":["everyone","unhappy","everyone","please","those"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6667 |
| H–CF | 0.3333 |
| H–RO | — |
| R–CF | 0.2500 |
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
{"label":"World","confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `b156d7f3a79ce82c`
- **ECS (full):** 0.4143
- **ECS (primary):** 0.2476
- **CC3 size:** 5 | **CC4 size:** 0

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
{"highlights":["Israeli", "Egyptian", "Gaza"]}
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
{"rationale":"The text is classified as World because it reports on a geopolitical event involving two countries, Israel and Egypt, which is a typical topic in international news.","evidence":["Israeli","Egyptian","Gaza","border","troops"]}
```

**Rationale text:**
> The text is classified as World because it reports on a geopolitical event involving two countries, Israel and Egypt, which is a typical topic in international news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `border`, `egyptian`, `gaza`, `israeli`, `troop`

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
{"counterfactual_text":"Israeli soccer team kills three Egyptian fans An Israeli soccer team has opened fire and killed three Egyptian fans in a stadium zone near the Gaza Strip after mistaking them for Palestinian soccer hooligans, Israeli sports sources say.","new_prediction":"Sports"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `arm`, `border`, `fan`, `hooligan`, `security`, `smuggler`, `soccer`, `stadium`, `tank`, `team`, `troop`

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
{"ranking":["Israeli", "Egyptian", "troops", "Gaza", "border"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `israeli`(1), `egyptian`(2), `troop`(3), `gaza`(4), `border`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.6000 |
| H–CF | 0.0000 |
| H–RO | 0.6000 |
| R–CF | 0.1429 |
| R–RO | 1.0000 |
| CF–RO | 0.1429 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

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
{"label":"Sci/Tech","confidence":90}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Prompt hash:** `1eb9278ea1e99466`
- **ECS (full):** 0.4731
- **ECS (primary):** 0.6000
- **CC3 size:** 0 | **CC4 size:** 0

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
{"highlights":["Microsoft", "viruses", "operating"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`, `operating`, `virus`

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
{"rationale":"The text is classified as Sci/Tech because it discusses Microsoft's operating system, Web browser, and e-mail programs, which are all related to technology and computing.","evidence":["Microsoft", "operating", "system", "Web", "browser", "e-mail", "programs", "viruses"]}
```

**Rationale text:**
> The text is classified as Sci/Tech because it discusses Microsoft's operating system, Web browser, and e-mail programs, which are all related to technology and computing.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `browser`, `e-mail`, `microsoft`, `operating`, `program`, `system`, `virus`, `web`

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
{"counterfactual_text":"Microsoft's big fix: Financial patch now on the market For the past few years, economic downturns have attacked Microsoft's financial reports, stock prices or investor programs seemingly on a weekly basis.","new_prediction":"Business"}
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
{"ranking":["Microsoft", "Security", "viruses", "operating", "browser"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `microsoft`(1), `security`(2), `virus`(3), `operating`(4), `browser`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.3750 |
| H–CF | — |
| H–RO | 0.6000 |
| R–CF | — |
| R–RO | 0.4444 |
| CF–RO | — |
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
{"label":"Sports","confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `ba8c190006964532`
- **ECS (full):** 0.3724
- **ECS (primary):** 0.2972
- **CC3 size:** 2 | **CC4 size:** 1

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
{"highlights":["Tournament", "Champions", "Player"]}
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
{"rationale":"The text is classified as Sports because it contains language and terminology commonly used in the context of golf tournaments, such as 'opening-round', 'birdied', and 'Player of the Year race'.","evidence":["players", "birdied", "Tournament", "Player", "round"]}
```

**Rationale text:**
> The text is classified as Sports because it contains language and terminology commonly used in the context of golf tournaments, such as 'opening-round', 'birdied', and 'Player of the Year race'.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `birdied`, `player`, `round`, `tournament`

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
{"counterfactual_text":"Four investors shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Market race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions.","new_prediction":"Business"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `investor`, `market`, `player`, `year`

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
{"ranking":["Champions", "Tournament", "Players", "round", "birdied"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `champion`(1), `tournament`(2), `player`(3), `round`(4), `birdied`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | 0.1667 |
| H–RO | 0.6000 |
| R–CF | 0.1429 |
| R–RO | 0.8000 |
| CF–RO | 0.1250 |
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
{"label":"Business","confidence":100}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `acbf1338eaa356c1`
- **ECS (full):** 0.2222
- **ECS (primary):** 0.1528
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
{"highlights":["pension", "fund", "shares"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fund`, `pension`, `share`

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
{"rationale":"This classification is correct because the text discusses a financial transaction involving a pension fund and a company's shares, which is a typical business-related activity.","evidence":["pension", "fund", "shares", "Calpers", "PeopleSoft", "tendering"]}
```

**Rationale text:**
> This classification is correct because the text discusses a financial transaction involving a pension fund and a company's shares, which is a typical business-related activity.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `calpers`, `fund`, `pension`, `peoplesoft`, `share`, `tendering`

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
{"counterfactual_text":"California athlete pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Athletes' Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc.","new_prediction":"Sports"}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `39`, `athlete`, `b>...</b`, `employee`

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
{"ranking":["pension", "fund", "Calpers", "Employees", "Retirement"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `pension`(1), `fund`(2), `calpers`(3), `employee`(4), `retirement`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.5000 |
| H–CF | 0.0000 |
| H–RO | 0.3333 |
| R–CF | 0.0000 |
| R–RO | 0.3750 |
| CF–RO | 0.1250 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |


## High-ECS Examples

### ag_news_test_0001 (ECS=0.4731)
- **Dataset:** ag_news
- **Text:** Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 90.0%

### mnli_validation_matched_0002 (ECS=0.4167)
- **Dataset:** mnli
- **Text:** It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone unhappy.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%

### sst2_validation_0001 (ECS=0.4167)
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
- **Confidence:** 80.0%


## Low-ECS Examples

### mnli_validation_matched_0001 (ECS=0.2222)
- **Dataset:** mnli
- **Text:** Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has bad history with presenting federal costs in the past.
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗
- **Confidence:** 80.0%

### ag_news_test_0003 (ECS=0.2222)
- **Dataset:** ag_news
- **Text:** California employee pension fund tenders PeopleSoft shares to &lt;b&gt;...&lt;/b&gt; NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 100.0%

### ag_news_test_0002 (ECS=0.3724)
- **Dataset:** ag_news
- **Text:** Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the fir…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓
- **Confidence:** 100.0%
