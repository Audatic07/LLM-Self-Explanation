# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-11 12:59:07
- **Duration:** 44.9s (0.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 3382
- **Avg tokens per instance:** 376

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 2/2 (100%) | 0.261 | 100% | 100% | 100% | 100% |
| mnli | 3 | 2/3 (67%) | 0.185 | 100% | 100% | 100% | 100% |
| ag_news | 4 | 4/4 (100%) | 0.255 | 100% | 100% | 100% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS | 0.2329 |
| Std ECS | 0.0699 |
| Median ECS | 0.2525 |
| Spearman ρ | 0.2277 (p=0.5557) |
| Mean CC3 size | 4.33 |
| Mean CC4 size | 1.56 |
| % instances with CC3 | 100.0% |
| % instances with CC4 | 77.8% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.1790 |
| H–CF | 0.1994 |
| H–RO | 0.5655 |
| R–CF | 0.1030 |
| R–RO | 0.1943 |
| CF–RO | 0.1565 |

### Parsing & Retention Rates

| Strategy | Success Rate |
|----------|-------------|
| Highlighting | 100.0% |
| Rationale | 100.0% |
| Counterfactual | 100.0% |
| Rank Ordering | 100.0% |
| All 4 parsed (CC possible) | 100.0% |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2329 | [0.1864, 0.2775] |
| Spearman ρ | 0.2277 | [-0.5451, 0.7956] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's great escapist fun that recreates a place and time that will never happen again . "

Respond with:
Prediction: [positive or negative]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: positive
Confidence: 100
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `db6b904c6c3f3ed7`
- **ECS:** 0.2705
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. great
2. escapist fun
3. it's
```

**Parsed tokens:**
- `escapist`, `fun`, `great`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The classification as positive is correct because the text describes the experience as "great escapist fun", which is a strongly affirmative phrase that indicates a highly enjoyable and entertaining experience.
```

**Parsed tokens:**
- `affirmative`, `classification`, `correct`, `describes`, `enjoyable`, `entertaining`, `escapist`, `experience`, `fun`, `great`, `highly`, `indicates`, `phrase`, `positive`, `strongly`, `text`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: positive
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: positive
Counterfactual Text: "it 's terrible escapist fun that recreates a place and time that will never happen again . "
Counterfactual Prediction: negative
```

**Parsed tokens:**
- `great`, `terrible`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. great
2. fun
3. escapist
4. recreates
5. again
```

**Parsed tokens:**
- `great`(1), `fun`(2), `escapist`(3), `recreates`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1875 |
| H–CF | 0.2500 |
| H–RO | 0.7500 |
| R–CF | 0.0588 |
| R–RO | 0.1765 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "verbinski implements every hack-artist trick to give us the ooky-spookies . "

Respond with:
Prediction: [positive or negative]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: Negative
Confidence: 90

The text uses the term "hack-artist trick", which has a negative connotation, implying that the director is using unoriginal or cheap techniques. The tone of the sentence also seems to be sarcast
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `negative`
- **Predicted:** `negative` ✓
- **Confidence:** 90.0%
- **Model refused:** No
- **Prompt hash:** `b6a5586d487bdc40`
- **ECS:** 0.2525
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. "hack-artist trick" 
2. "ooky-spookies" 
3. "implements every"
```

**Parsed tokens:**
- `every`, `hack-artist`, `implement`, `ooky-spookies`, `trick`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The classification of the text as negative is correct because the phrase "hack-artist trick" is a pejorative expression that implies a lack of originality or skill, indicating a dismissive and critical tone towards the director's methods.
```

**Parsed tokens:**
- `classification`, `correct`, `critical`, `director`, `dismissive`, `expression`, `hack-artist`, `implies`, `indicating`, `lack`, `method`, `negative`, `originality`, `pejorative`, `phrase`, `skill`, `text`, `tone`, `trick`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: negative
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: negative
Counterfactual Text: "verbinski implements every masterful trick to give us the ooky-spookies . "
Counterfactual Prediction: positive

In this counterfactual, I changed the word "hack-artist" to "masterful", which has a strongly positive connotation, implying skill and expertise. This minimal edit flips the sentiment of the text from negative to positive.
```

**Parsed tokens:**
- `hack-artist`, `masterful`, `verbinski`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. hack-artist
2. trick
3. ooky-spookies
4. implements
5. every
```

**Parsed tokens:**
- `hack-artist`(1), `trick`(2), `ooky-spookies`(3), `implement`(4), `every`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0909 |
| H–CF | 0.1429 |
| H–RO | 1.0000 |
| R–CF | 0.0476 |
| R–RO | 0.0909 |
| CF–RO | 0.1429 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### mnli_validation_matched_0000

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise [SEP] Hypothesis: "Jon's defense began to weaken and slow. [SEP] Jon began to lose his strength and defense."

Does the premise entail the hypothesis, contradict it, or is it neutral?

Respond with:
Prediction: [entailment, neutral, or contradiction]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: entailment
Confidence: 95

The premise states that "Jon's defense began to weaken and slow," which implies a decline in his defensive capabilities. The hypothesis states that "Jon began to lose his strength and defense," which is
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `entailment`
- **Predicted:** `entailment` ✓
- **Confidence:** 95.0%
- **Model refused:** No
- **Prompt hash:** `347eccb8984acac1`
- **ECS:** 0.2961
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. "weaken" 
2. "defense" 
3. "began to" 

These tokens support the classification of entailment because they indicate a decline or reduction in Jon's defensive capabilities, which is further elaborated in the hypothesis as "lose his strength and defense". The word "weaken" is the most important token as it directly implies a loss of strength or ability, making the hypothesis a logical consequence of the premise.
```

**Parsed tokens:**
- `began`, `defense`, `weaken`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The classification as entailment is correct because the premise that "Jon's defense began to weaken and slow" directly implies the hypothesis that "Jon began to lose his strength and defense", as a weakening defense is a clear indicator of losing strength and defensive capabilities.
```

**Parsed tokens:**
- `began`, `capability`, `classification`, `clear`, `correct`, `defense`, `defensive`, `directly`, `entailment`, `hypothesis`, `implies`, `indicator`, `jon`, `lose`, `losing`, `premise`, `slow`, `strength`, `weaken`, `weakening`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: entailment
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: entailment
Counterfactual Text: "Jon's defense began to strengthen and slow. [SEP] Jon began to lose his strength and defense."
Counterfactual Prediction: contradiction
```

**Parsed tokens:**
- `defense`, `jon's`, `strengthen`, `weaken`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. weaken
2. defense
3. began
4. lose
5. strength
```

**Parsed tokens:**
- `weaken`(1), `defense`(2), `began`(3), `lose`(4), `strength`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1500 |
| H–CF | 0.4000 |
| H–RO | 0.6000 |
| R–CF | 0.0909 |
| R–RO | 0.2500 |
| CF–RO | 0.2857 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### mnli_validation_matched_0001

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise [SEP] Hypothesis: "Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has bad history with presenting federal costs in the past."

Does the premise entail the hypothesis, contradict it, or is it neutral?

Respond with:
Prediction: [entailment, neutral, or contradiction]
Confidence: [0-100]
```

#### 2. Classification Response
```
To determine the logical relationship between the premise and the hypothesis, let's analyze them step by step.

1. **Premise**: The premise discusses respondents' views on whether alternatives for presenting costs of Federal mission PP&amp; are considered by the Board.

```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `` ✗
- **Confidence:** 0.0%
- **Model refused:** No
- **Prompt hash:** `1a31c7dd0ca9cbe6`
- **ECS:** 0.1130
- **CC3 size:** 7 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: 

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
Based on the given text, the classification seems to be related to the relationship between a premise and a hypothesis, specifically in the context of a board's history with presenting federal costs. The most important tokens that support this classification are:

1. "The board has bad history" - This phrase suggests a prior issue or problem, which is crucial for understanding the context of the hypothesis.
2. "presenting federal costs" - This phrase directly relates to the action or topic being discussed, indicating that the hypothesis is about the board's past performance regarding federal cost presentation.
3. "in the past" - This phrase provides a temporal context, implying that the hypothesis is based on historical information or previous experiences with the board's handling of federal costs.
```

**Parsed tokens:**
- `action`, `bad`, `based`, `board`, `board's`, `context`, `cost`, `crucial`, `directly`, `discussed`, `experience`, `federal`, `handling`, `historical`, `history`, `hypothesis`, `implying`, `indicating`, `information`, `issue`, `past`, `performance`, `phrase`, `presentation`, `presenting`, `previous`, `prior`, `problem`, `provides`, `regarding`, `relates`, `suggests`, `temporal`, `topic`, `understanding`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: 

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The classification is correct because the premise implies that the Board is currently considering or has considered alternatives for presenting federal costs, which suggests a potential improvement or change from past practices, thereby supporting the hypothesis that the Board has had bad history with presenting federal costs in the past.
```

**Parsed tokens:**
- `alternative`, `bad`, `board`, `change`, `classification`, `considered`, `considering`, `correct`, `cost`, `currently`, `federal`, `history`, `hypothesis`, `implies`, `improvement`, `past`, `potential`, `practice`, `premise`, `presenting`, `suggests`, `supporting`, `thereby`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: 

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: 
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: Neutral

Counterfactual Text: "Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has good history with presenting federal costs in the past."

Counterfactual Prediction: Entailment
```

**Parsed tokens:**
- `bad`, `good`, `past`, `respondent`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: 

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
Based on the given text, the classification, and the context provided, here's a ranking of the most important tokens:

1. Board
2. Federal
3. Costs
4. Presenting
5. History
```

**Parsed tokens:**
- `board`(1), `federal`(2), `cost`(3), `presenting`(4), `history`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1837 |
| H–CF | 0.0541 |
| H–RO | 0.1429 |
| R–CF | 0.0800 |
| R–RO | 0.2174 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise [SEP] Hypothesis: "It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone unhappy."

Does the premise entail the hypothesis, contradict it, or is it neutral?

Respond with:
Prediction: [entailment, neutral, or contradiction]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: contradiction
Confidence: 100

The premise states that it's a rare case where everyone can be pleased, implying a positive outcome. The hypothesis, on the other hand, states that it's a situation where everyone ends up unhappy,
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `5673d4a6e6c20529`
- **ECS:** 0.1448
- **CC3 size:** 4 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. "please everyone" 
2. "making everyone unhappy"
3. "rare cases" 

These tokens are crucial in establishing the contradiction between the premise and the hypothesis. The phrase "please everyone" implies a positive outcome, while "making everyone unhappy" implies a negative one. The phrase "rare cases" highlights the unexpected nature of the situation, making the contrast between the premise and hypothesis more pronounced.
```

**Parsed tokens:**
- `case`, `everyone`, `making`, `please`, `rare`, `unhappy`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The classification as a contradiction is correct because the premise explicitly states that it's a rare case where everyone can be pleased, which directly opposes the hypothesis that everyone ends up unhappy, indicating a clear and absolute opposition between the two statements.
```

**Parsed tokens:**
- `absolute`, `case`, `classification`, `clear`, `contradiction`, `correct`, `directly`, `end`, `everyone`, `explicitly`, `hypothesis`, `indicating`, `opposes`, `opposition`, `pleased`, `premise`, `rare`, `state`, `statement`, `unhappy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: contradiction
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: contradiction
Counterfactual Text: "It is one of those rare cases in which I can please everyone. It's one of those situations where I end up making everyone happy."
Counterfactual Prediction: entailment
```

**Parsed tokens:**
- `happy`, `sep`, `unhappy`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. everyone (in the premise and hypothesis, with opposite outcomes)
2. please (implies a positive outcome in the premise)
3. unhappy (implies a negative outcome in the hypothesis)
4. rare cases (sets up an expectation of a positive exception in the premise)
5. end up (indicates an outcome or result in the hypothesis, contrasting with the premise)
```

**Parsed tokens:**
- `everyone`(1), `premise`(1), `hypothesis`(1), `opposite`(1), `outcome`(1), `please`(2), `implies`(2), `positive`(2), `outcome`(2), `premise`(2), `unhappy`(3), `implies`(3), `negative`(3), `outcome`(3), `hypothesis`(3), `rare`(4), `case`(4), `set`(4), `expectation`(4), `positive`(4), `exception`(4), `premise`(4), `end`(5), `indicates`(5), `outcome`(5), `result`(5), `hypothesis`(5), `contrasting`(5), `premise`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1818 |
| H–CF | 0.1250 |
| H–RO | 0.2500 |
| R–CF | 0.0455 |
| R–RO | 0.2188 |
| CF–RO | 0.0476 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Israeli security sources say."

Choose from: World, Sports, Business, Sci/Tech

Respond with:
Prediction: [category]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: World
Confidence: 100
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `World`
- **Predicted:** `World` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `73c33850cfe93a36`
- **ECS:** 0.2605
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. Israeli
2. Egyptian troops
3. Gaza Strip
```

**Parsed tokens:**
- `egyptian`, `gaza`, `israeli`, `strip`, `troop`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The article is classified as "World" because it reports on a geopolitical incident involving the death of Egyptian troops by an Israeli tank, which is a significant international news event.
```

**Parsed tokens:**
- `article`, `classified`, `death`, `egyptian`, `event`, `geopolitical`, `incident`, `international`, `involving`, `israeli`, `news`, `report`, `significant`, `tank`, `troop`, `world`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: World
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: World
Counterfactual Text: "Israeli soccer team kills three Egyptian fans An Israeli soccer team has opened fire and killed three Egyptian fans in a stadium zone near the Gaza Strip after mistaking them for Palestinian soccer hooligans, Israeli sports sources say."
Counterfactual Prediction: Sports
```

**Parsed tokens:**
- `arm`, `border`, `fan`, `hooligan`, `israeli`, `say`, `security`, `smuggler`, `soccer`, `sport`, `stadium`, `tank`, `team`, `troop`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. Israeli
2. Egyptian
3. troops
4. Gaza Strip
5. border
```

**Parsed tokens:**
- `israeli`(1), `egyptian`(2), `troop`(3), `gaza`(4), `strip`(4), `border`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1667 |
| H–CF | 0.1176 |
| H–RO | 0.8333 |
| R–CF | 0.1111 |
| R–RO | 0.1579 |
| CF–RO | 0.1765 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis."

Choose from: World, Sports, Business, Sci/Tech

Respond with:
Prediction: [category]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: Sci/Tech
Confidence: 100
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `c5d71843a1b5a727`
- **ECS:** 0.3492
- **CC3 size:** 7 | **CC4 size:** 4

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. Microsoft
2. operating system
3. Security patch
```

**Parsed tokens:**
- `microsoft`, `operating`, `patch`, `security`, `system`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The classification as Sci/Tech is correct because the text specifically mentions technical topics such as Microsoft's operating system, Web browser, e-mail programs, and security patches, which are all related to science and technology.
```

**Parsed tokens:**
- `browser`, `classification`, `correct`, `e-mail`, `mention`, `microsoft`, `operating`, `patch`, `program`, `related`, `sci/tech`, `science`, `security`, `specifically`, `system`, `technical`, `technology`, `text`, `topic`, `web`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: Sci/Tech
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: Sci/Tech
Counterfactual Text: "Microsoft's big fix: Financial patch now on the market For the past few years, losses have attacked Microsoft's profits, stocks or investments seemingly on a weekly basis."
Counterfactual Prediction: Business
```

**Parsed tokens:**
- `39;s`, `basis`, `browser`, `e-mail`, `financial`, `investment`, `loss`, `microsoft`, `microsoft's`, `operating`, `profit`, `program`, `security`, `stock`, `system`, `virus`, `web`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. Microsoft
2. operating system
3. Security patch
4. viruses
5. Web browser
```

**Parsed tokens:**
- `microsoft`(1), `operating`(2), `system`(2), `security`(3), `patch`(3), `virus`(4), `web`(5), `browser`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | 0.2222 |
| H–RO | 0.6250 |
| R–CF | 0.2759 |
| R–RO | 0.3333 |
| CF–RO | 0.3889 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the first round of the Tournament of Champions."

Choose from: World, Sports, Business, Sci/Tech

Respond with:
Prediction: [category]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: Sports
Confidence: 100
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sports`
- **Predicted:** `Sports` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `ddfd45fe616b29b5`
- **ECS:** 0.1952
- **CC3 size:** 5 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. Tournament of Champions
2. Player of the Year
3. birdied the final hole
```

**Parsed tokens:**
- `birdied`, `champion`, `final`, `hole`, `player`, `tournament`, `year`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The text is classified as Sports because it mentions specific golf terminology, such as "birdied" and "opening-round 66", and references a golf tournament, the "Tournament of Champions", indicating that the article is about a sporting event.
```

**Parsed tokens:**
- `article`, `birdied`, `champion`, `classified`, `event`, `golf`, `indicating`, `mention`, `opening-round`, `reference`, `specific`, `sport`, `sporting`, `terminology`, `text`, `tournament`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: Sports
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: Sports
Counterfactual Text: "Four CEOs shoot opening-round profits SEMMES, Ala. -- Grace Park, looking to clinch second place in the Market race, closed a major deal on the final day Thursday to gain a share of the lead after the first quarter of the Business of Champions."
Counterfactual Prediction: Business
```

**Parsed tokens:**
- `66`, `birdied`, `business`, `ceo`, `champion`, `closed`, `day`, `deal`, `four`, `hole`, `major`, `market`, `player`, `profit`, `quarter`, `round`, `tournament`, `year`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. Tournament of Champions
2. Player of the Year
3. birdied
4. lead
5. golf (implied by "shoot" and "opening-round", but not explicitly mentioned, however "shoot" is the fifth most important token in this context) 

Revised to include the actual word:
1. Tournament of Champions
2. Player of the Year
3. birdied
4. lead
5. shoot
```

**Parsed tokens:**
- `tournament`(1), `champion`(1), `player`(2), `year`(2), `birdied`(3), `lead`(4), `golf`(5), `implied`(5), `shoot`(5), `opening-round`(5), `explicitly`(5), `mentioned`(5), `however`(5), `shoot`(5), `fifth`(5), `important`(5), `token`(5), `context`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1500 |
| H–CF | 0.3158 |
| H–RO | 0.2632 |
| R–CF | 0.0968 |
| R–RO | 0.1786 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "California employee pension fund tenders PeopleSoft shares to &lt;b&gt;...&lt;/b&gt; NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Employees #39; Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc."

Choose from: World, Sports, Business, Sci/Tech

Respond with:
Prediction: [category]
Confidence: [0-100]
```

#### 2. Classification Response
```
Prediction: Business
Confidence: 100
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Business`
- **Predicted:** `Business` ✓
- **Confidence:** 100.0%
- **Model refused:** No
- **Prompt hash:** `e0d00644f7696b5e`
- **ECS:** 0.2144
- **CC3 size:** 5 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Identify the 3 most important tokens (words or phrases) that support this classification. List them in order of importance.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
```

**Response:**
```
1. Pension fund
2. Shares
3. Calpers (California Employees' Retirement System)
```

**Parsed tokens:**
- `california`, `calpers`, `employee`, `fund`, `pension`, `retirement`, `share`, `system`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Provide a one-sentence rationale explaining why this classification is correct. Focus on the key evidence in the text.

Format your response as:
Rationale: [one sentence explanation]
```

**Response:**
```
Rationale: The text is classified as Business because it discusses a significant financial transaction involving the California Employees' Retirement System (Calpers) and a company's shares, specifically PeopleSoft Inc., which is a clear indication of a business-related event.
```

**Parsed tokens:**
- `business`, `business-related`, `california`, `calpers`, `classified`, `clear`, `company`, `discusses`, `employee`, `event`, `financial`, `inc`, `indication`, `involving`, `peoplesoft`, `retirement`, `share`, `significant`, `specifically`, `system`, `text`, `transaction`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Create a minimal-edit counterfactual: modify the text as little as possible to change the classification to a different category. Only change the words that are most critical to the classification.

Format your response as:
Original Prediction: Business
Counterfactual Text: [the minimally modified text]
Counterfactual Prediction: [the predicted label for the counterfactual]
```

**Response:**
```
Original Prediction: Business
Counterfactual Text: "California athlete pension fund tenders PeopleSoft shares to ... NOVEMBER 19, 2004 (IDG NEWS SERVICE) - The California Athletes' Retirement System (Calpers) is tendering its 1.5 million PeopleSoft Inc."
Counterfactual Prediction: Sports
```

**Parsed tokens:**
- `39`, `athlete`, `california`, `employee`, `inc`, `lt;b&gt;...&lt;/b&gt`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Rank the 5 most important tokens (words or phrases) for this classification, from most important to least important.

Format your response as:
1. [most important token]
2. [second most important token]
3. [third most important token]
4. [fourth most important token]
5. [fifth most important token]
```

**Response:**
```
1. Pension
2. Fund
3. Shares
4. Retirement
5. Calpers
```

**Parsed tokens:**
- `pension`(1), `fund`(2), `share`(3), `retirement`(4), `calpers`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2500 |
| H–CF | 0.1667 |
| H–RO | 0.6250 |
| R–CF | 0.1200 |
| R–RO | 0.1250 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.5000 |


## High-ECS Examples

### ag_news_test_0001 (ECS=0.3492)
- **Dataset:** ag_news
- **Text:** Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 100.0%

### mnli_validation_matched_0000 (ECS=0.2961)
- **Dataset:** mnli
- **Text:** Jon's defense began to weaken and slow. [SEP] Jon began to lose his strength and defense.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 95.0%

### sst2_validation_0000 (ECS=0.2705)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 100.0%


## Low-ECS Examples

### mnli_validation_matched_0001 (ECS=0.1130)
- **Dataset:** mnli
- **Text:** Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has bad history with presenting federal costs in the past.
- **Ground truth:** `neutral` → **Predicted:** `` ✗
- **Confidence:** 0.0%

### mnli_validation_matched_0002 (ECS=0.1448)
- **Dataset:** mnli
- **Text:** It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone unhappy.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%

### ag_news_test_0002 (ECS=0.1952)
- **Dataset:** ag_news
- **Text:** Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year race, birdied the final hole Thursday to gain a share of the lead after the fir…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓
- **Confidence:** 100.0%
