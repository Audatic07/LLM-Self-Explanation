# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-16 13:10:14
- **Duration:** 271.5s (4.5m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 11
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 4908
- **Avg tokens per instance:** 446

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 4 | 4/4 (100%) | 0.150 | 100% | 50% | 75% | 100% |
| mnli | 3 | 3/3 (100%) | 0.194 | 67% | 100% | 67% | 100% |
| ag_news | 4 | 4/4 (100%) | 0.184 | 100% | 100% | 25% | 100% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 5 | 4 | 0 |
| mnli | 5 | 3 | 0 |
| ag_news | 5 | 4 | 0 |
| **Total** | 15 | 11 | 0 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=3) or medium-length (21–50 words, N=6). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=3). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=4)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 10/11 | 91% |
| Rationale | 9/11 | 82% |
| Counterfactual | 6/11 | 55% |
| Rank Ordering | 11/11 | 100% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their Jaccard is excluded from ECS; agreement is measured via Kendall τ instead. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=11) | 0.1766 |
| Mean ECS (primary: H,CF,RO) | 0.0867 |
| Mean ECS (complete cases, N=4) | 0.1842 |
| Complete cases | 4/11 (36%) |
| Primary ECS pairs <3 | 5 instances |
  → mnli_validation_matched_0001: 1 pair(s), ECS_primary=0.2000
  → mnli_validation_matched_0002: 0 pair(s), ECS_primary=0.0000
  → ag_news_test_0001: 0 pair(s), ECS_primary=0.0000
  → ag_news_test_0002: 0 pair(s), ECS_primary=0.0000
  → ag_news_test_0003: 0 pair(s), ECS_primary=0.0000
| Std ECS | 0.0781 |
| Median ECS | 0.1704 |
| Confidence elicitation | Removed — does not proxy faithfulness |
| Mean CC3 size | 0.55 |
| Mean CC4 size | 0.27 |
| % instances with CC3 | 54.5% |
| % instances with CC4 | 27.3% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.2708 |
| H–CF | 0.1533 |
| H–RO | 0.2986 |
| R–CF | 0.1000 |
| R–RO | 0.1869 |
| CF–RO | 0.1278 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 10/11 (91%) | 10/11 (91%) |
| Rationale | 9/11 (82%) | 9/11 (82%) |
| Counterfactual | 6/11 (55%) | 6/11 (55%) |
| CF flip verified | 6/6 (100%) |
| Rank Ordering | 11/11 (100%) | 11/11 (100%) |
| All 4 valid | 4/11 |
| 3 valid (CC3 adjusted) | 6/11 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Kendall τ (rank correlation), not Jaccard.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 3 | 0.1900 |
| Medium (21–50) | 6 | 0.1758 |
| Long (>50 words) | 1 | 0.1407 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 7 | 0.1708 |
| Short vocab (≤20 unique tokens) | 3 | 0.1900 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.1766 | [0.1313, 0.2271] |

## Per-Instance Details

### sst2_validation_0000

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
- **Model refused:** No
- **Input length:** 14 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b00a643964e1a260`
- **ECS (full):** 0.2000
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"comes":2, "uncomfortably":8, "close":6, "to":1, "coasting":7, "in":1, "the":1, "treads":4, "of":1, "the":1, "bicycle":4, "thief":4}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `bicycle`, `close`, `coasting`, `treads`, `uncomfortably`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives a negative classification because it implies that the subject is unoriginal and lacking in creativity, suggesting that it is simply following in the footsteps of something else, which is a criticism."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to positive.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
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

**Reconstructed text:**
> comes ... comfortably close to coasting in the treads of the bicycle thief . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`

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
{"ranking":["uncomfortably", "coasting", "close", "thief", "in"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `uncomfortably`(1), `coasting`(2), `close`(3), `thief`(4), `comes`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | 0.2000 |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | — |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | 1.0000 |
| Normalized τ | 1.0000 |

### sst2_validation_0001

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . "

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
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 20 chars
- **Prompt hash:** `9aba917cfb5449c7`
- **ECS (full):** 0.1200
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"what's":2, "surprising":6, "about":4, "full":8, "frontal":8, "is":2, "that":2, "despite":4, "its":2, "overt":6, "self-awareness":6, "parts":4, "of":2, "the":2, "movie":8, "still":6, "manage":6, "to":2, "break":6, "past":4, "the":2, "artifice":6, "and":2, "thoroughly":8, "engage":8, "you":2}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `engage`, `frontal`, `full`, `movie`, `thoroughly`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives a positive classification because it mentions that parts of the movie are able to break past its artificial nature and thoroughly engage the viewer, implying an overall effective and impactful film."}
```

**Rationale text:**
> The text receives a positive classification because it mentions that parts of the movie are able to break past its artificial nature and thoroughly engage the viewer, implying an overall effective and impactful film.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `movie`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to negative.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "engage", "to": "alienate"}], "new_prediction": "negative"}
```

**Reconstructed text:**
> what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly alienate you . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `engage`

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
{"ranking":["engage", "surprising", "thoroughly", "despite", "still"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `engage`(1), `surprising`(2), `thoroughly`(3), `despite`(4), `still`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2000 |
| H–CF | 0.2000 |
| H–RO | 0.2500 |
| R–CF | 0.0000 |
| R–RO | 0.0000 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### sst2_validation_0002

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
- **Model refused:** No
- **Input length:** 11 words
- **Raw response length:** 20 chars
- **Prompt hash:** `50f5b42b5c34d301`
- **ECS (full):** 0.1300
- **ECS (primary):** 0.1000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"verbinski":6, "implements":4, "every":3, "hack-artist":8, "trick":5, "to":2, "give":3, "us":2, "the":2, "ooky-spookies":9}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`, `implements`, `ooky-spookies`, `trick`, `verbinski`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives a negative classification because the tone is dismissive and mocking, implying that the filmmaker's use of techniques to create a spooky atmosphere is unoriginal and reliant on cheap tricks."}
```

**Rationale text:**
> The text receives a negative classification because the tone is dismissive and mocking, implying that the filmmaker's use of techniques to create a spooky atmosphere is unoriginal and reliant on cheap tricks.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `trick`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to positive.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
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

**Reconstructed text:**
> verbinski implements every visionary trick to give us the ooky-spookies . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack-artist`

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
{"ranking":["hack", "trick", "ooky", "spookies", "us"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hack`(1), `trick`(2), `ooky`(3), `spookies`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2000 |
| H–CF | 0.2000 |
| H–RO | 0.1250 |
| R–CF | 0.0000 |
| R–RO | 0.2500 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### sst2_validation_0003

#### 1. Classification Prompt
```
Analyze the sentiment expressed in the following text.

Text: "it 's an offbeat treat that pokes fun at the democratic exercise while also examining its significance for those who take part . "

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
- **Model refused:** No
- **Input length:** 23 words
- **Raw response length:** 20 chars
- **Prompt hash:** `fd4efe262a8ab2d5`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"it":2, "s":1, "an":2, "offbeat":8, "treat":7, "that":3, "pokes":6, "fun":6, "at":1, "the":1, "democratic":5, "exercise":5, "while":2, "also":2, "examining":4, "its":2, "significance":9, "for":2, "those":3, "who":2, "take":2, "part":3}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `fun`, `offbeat`, `pokes`, `significance`, `treat`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives a positive classification because it describes the subject as a unique and engaging experience, using phrases that convey a sense of playful curiosity and thoughtful examination, which overall suggests an appreciative and admiring tone."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Identify the word(s) most responsible for this classification. Replace 1-2 of them with words that would change the classifier's output to negative.

A good replacement changes the semantic direction of the text. In sentiment, replace a strongly positive word with a negative one (or vice versa). In topic classification, replace a topic-defining word with one from a different category.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text
- Replaced words must be content words (nouns, verbs, adjectives, adverbs)

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: negative>"}

Example — if the text is "This film is terrible" and was classified as negative, return:
{"edits": [{"from": "terrible", "to": "amazing"}], "new_prediction": "positive"}
```

**Response:**
```
{"edits": [{"from": "treat", "to": "disaster"}], "new_prediction": "negative"}
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
{"ranking":["treat", "significance", "fun", "exercise", "part"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `treat`(1), `significance`(2), `fun`(3), `exercise`(4), `part`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ | 0.6667 |

### mnli_validation_matched_0000

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: Not yourself.
Hypothesis: Someone else

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
- **Model refused:** No
- **Input length:** 6 words
- **Raw response length:** 22 chars
- **Prompt hash:** `bd36af1ff07e9a2a`
- **ECS (full):** 0.2400
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `neutral`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"Determine":4, "the":2, "logical":6, "relationship":8, "between":4, "the":2, "premise":9, "and":3, "the":2, "hypothesis":9, "Premise":8, "Not":5, "yourself":7, "Hypothesis":8, "Someone":6, "else":6, "Does":4, "the":2, "premise":9, "entail":8, "the":2, "hypothesis":9, "contradict":5, "it":3, "or":2, "is":2, "it":3, "neutral":4}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hypothesis`, `premise`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The premise 'Not yourself' implies that the subject is referring to another individual, which directly supports the hypothesis 'Someone else', establishing a logical relationship of entailment between the two statements."}
```

**Rationale text:**
> The premise 'Not yourself' implies that the subject is referring to another individual, which directly supports the hypothesis 'Someone else', establishing a logical relationship of entailment between the two statements.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hypothesis`, `premise`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to neutral, contradiction.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "yourself", "to": "city"}], "new_prediction": "neutral"}
```

**Reconstructed text:**
> Premise: Not city.
Hypothesis: Someone else

**Parsed tokens:**
- Status: **Valid**
- Tokens: `yourself`

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
{"ranking":["yourself", "else", "Not", "Someone", "hypothesis"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `else`(1), `not`(2), `someone`(3), `hypothesis`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 1.0000 |
| H–CF | 0.0000 |
| H–RO | 0.2000 |
| R–CF | 0.0000 |
| R–RO | 0.2000 |
| CF–RO | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0001

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: 36 AC usage nationally for mercury control from power plants should be roughly proportional to the total MWe of coal-fired facilities that are equipped with the technology (this assumes an average capacity factor of 85 percent and other assumptions of Tables 4-4 and 4-5).
Hypothesis: Power plants' mercury control AC usage is higher than total MWe from coal facilities.

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
- **Model refused:** No
- **Input length:** 60 words
- **Raw response length:** 25 chars
- **Prompt hash:** `57b403d5df0447cc`
- **ECS (full):** 0.1407
- **ECS (primary):** 0.2000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{
"Determine":2, 
"the":1, 
"logical":3, 
"relationship":4, 
"between":2, 
"the":1, 
"premise":8, 
"and":2, 
"the":1, 
"hypothesis":8, 
"Premise":6, 
"36":5, 
"AC":5, 
"usage":5, 
"nationally":4, 
"for":2, 
"mercury":7, 
"control":7, 
"from":2, 
"power":6, 
"plants":6, 
"should":3, 
"be":2, 
"roughly":4, 
"proportional":6, 
"to":2, 
"the":1, 
"total":5, 
"MWe":5, 
"of":2, 
"coal-fired":6, 
"facilities":6, 
"that":2, 
"are":2, 
"equipped":4, 
"with":2, 
"the":1, 
"technology":6, 
"this":2, 
"assumes":3, 
"an":2, 
"average":4, 
"capacity":5, 
"factor":5, 
"of":2, 
"85":3, 
"percent":3, 
"and":2, 
"other":2, 
"assumptions":4, 
"of":2, 
"Tables":3, 
"4-4":2, 
"and":2, 
"4-5":2, 
"Hypothesis":6, 
"Power":6, 
"plants'":6, 
"mercury":7, 
"control":7, 
"AC":5, 
"usage":5, 
"is":2, 
"higher":8, 
"than":4, 
"total":5, 
"MWe":5, 
"from":2, 
"coal":6, 
"facilities":6, 
"Does":2, 
"the":1, 
"premise":8, 
"entail":4, 
"the":1, 
"hypothesis":8, 
"contradict":8, 
"it":2, 
"or":2, 
"is":2, 
"neutral":
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The premise suggests a proportional relationship between AC usage and total MWe of coal-fired facilities, which implies that the AC usage should be roughly equivalent to the total MWe, not higher, thereby contradicting the hypothesis that power plants' mercury control AC usage is higher than total MWe from coal facilities."}
```

**Rationale text:**
> The premise suggests a proportional relationship between AC usage and total MWe of coal-fired facilities, which implies that the AC usage should be roughly equivalent to the total MWe, not higher, thereby contradicting the hypothesis that power plants' mercury control AC usage is higher than total MWe from coal facilities.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hypothesis`, `mwe`, `premise`, `proportional`, `total`, `usage`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to entailment, neutral.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"edits": [{"from": "higher", "to": "similar"}], "new_prediction": "entailment"}
```

**Reconstructed text:**
> Premise: 36 AC usage nationally for mercury control from power plants should be roughly proportional to the total MWe of coal-fired facilities that are equipped with the technology (this assumes an average capacity factor of 85 percent and other assumptions of Tables 4-4 and 4-5).
Hypothesis: Power plants' mercury control AC usage is similar than total MWe from coal facilities.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `higher`

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
{"ranking":["proportional", "roughly", "higher", "mercury", "total"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `proportional`(1), `roughly`(2), `higher`(3), `mercury`(4), `total`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | — |
| R–CF | 0.0000 |
| R–RO | 0.2222 |
| CF–RO | 0.2000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### mnli_validation_matched_0002

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: In general, six elements appear  purpose, type of data collected, method of data collection, design, method of data analysis, and reporting.
Hypothesis: Breaking it down into 6 elements has always been helpful for students and professionals.

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
- **Model refused:** No
- **Input length:** 37 words
- **Raw response length:** 19 chars
- **Prompt hash:** `b00ef8ce8bce925d`
- **ECS (full):** 0.2000
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{
"Determine":8, 
"the":2, 
"logical":8, 
"relationship":8, 
"between":4, 
"the":2, 
"premise":9, 
"and":3, 
"the":2, 
"hypothesis":9, 
"Premeise":1, 
"In":2, 
"general":5, 
"six":6, 
"elements":7, 
"appear":6, 
"purpose":6, 
"type":6, 
"of":2, 
"data":6, 
"collected":6, 
"method":6, 
"of":2, 
"collection":6, 
"design":6, 
"method":6, 
"analysis":6, 
"reporting":6, 
"Hypothesis":1, 
"Breaking":4, 
"it":2, 
"down":4, 
"into":4, 
"has":4, 
"always":4, 
"been":4, 
"helpful":4, 
"for":2, 
"students":4, 
"and":3, 
"professionals":4, 
"Does":8, 
"the":2, 
"premise":9, 
"entail":8, 
"the":2, 
"hypothesis":9, 
"contradict":8, 
"it":2, 
"or":2, 
"is":2, 
"neutral":8
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `appear`, `elements`, `hypothesis`, `premise`, `six`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives a neutral classification because the premise simply states the typical components involved in a process, while the hypothesis makes a claim about the usefulness of breaking it down into these components, without any direct logical connection between the two statements."}
```

**Rationale text:**
> The text receives a neutral classification because the premise simply states the typical components involved in a process, while the hypothesis makes a claim about the usefulness of breaking it down into these components, without any direct logical connection between the two statements.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `hypothesis`, `premise`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to entailment, contradiction.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"edits": [{"from": "helpful", "to": "essential"}], "new_prediction": "entailment"}
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
{"ranking":["general", "elements", "appear", "data", "always"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `general`(1), `elements`(2), `appear`(3), `data`(4), `always`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.4000 |
| H–CF | — |
| H–RO | 0.2500 |
| R–CF | — |
| R–RO | 0.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0000

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Mark Cuban prompts dot-com redux reporteri 's notebook SAN FRANCISCO--Hope and cynicism sparred to a draw on Tuesday at the glitzy opening banquet of Web 2.0 conference here, as serial entrepreneur and reality TV show host Mark Cuban took the stage to talk about what 's next for the 10-year "

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
- **Model refused:** No
- **Input length:** 50 words
- **Raw response length:** 20 chars
- **Prompt hash:** `2d5cb1e4d9eca6c0`
- **ECS (full):** 0.2467
- **ECS (primary):** 0.1667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Business`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{
"Mark":6, 
"Cuban":6, 
"prompts":4, 
"dot-com":8, 
"redux":5, 
"reporteri":2, 
"'s":1, 
"notebook":3, 
"SAN":2, 
"FRANCISCO--Hope":2, 
"and":1, 
"cynicism":2, 
"sparred":2, 
"to":1, 
"a":1, 
"draw":2, 
"on":1, 
"Tuesday":2, 
"at":1, 
"the":1, 
"glitzy":2, 
"opening":2, 
"banquet":2, 
"of":1, 
"Web":9, 
"2.0":9, 
"conference":7, 
"here,":1, 
"as":1, 
"serial":4, 
"entrepreneur":6, 
"and":1, 
"reality":4, 
"TV":4, 
"show":4, 
"host":4, 
"took":2, 
"the":1, 
"stage":2, 
"to":1, 
"talk":2, 
"about":1, 
"what":1, 
"'s":1, 
"next":2, 
"for":1, 
"the":1, 
"10-year":2
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `2.0`, `conference`, `dot-com`, `mark`, `web`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives this classification because it discusses a Web 2.0 conference, a reality TV show host's thoughts on the future of the industry, and the overall tone suggests a focus on technology and innovation, which are all characteristic of the Sci/Tech topic."}
```

**Rationale text:**
> The text receives this classification because it discusses a Web 2.0 conference, a reality TV show host's thoughts on the future of the industry, and the overall tone suggests a focus on technology and innovation, which are all characteristic of the Sci/Tech topic.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `conference`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to World, Sports, Business.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"edits": [{"from": "Web", "to": "Olympic"}, {"from": "conference", "to": "championship"}], "new_prediction": "Sports"}
```

**Reconstructed text:**
> Mark Cuban prompts dot-com redux reporteri 's notebook SAN FRANCISCO--Hope and cynicism sparred to a draw on Tuesday at the glitzy opening banquet of Olympic 2.0 championship here, as serial entrepreneur and reality TV show host Mark Cuban took the stage to talk about what 's next for the 10-year 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `Web`, `conference`

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
{"ranking":["Web", "conference", "TV", "stage", "banquet"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `web`(1), `conference`(2), `tv`(3), `stage`(4), `banquet`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2000 |
| H–CF | 0.1667 |
| H–RO | 0.2500 |
| R–CF | 0.5000 |
| R–RO | 0.2000 |
| CF–RO | 0.1667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, preserving a 6-5 come-from-behind win over the San Diego Padres. "

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
- **Model refused:** No
- **Input length:** 46 words
- **Raw response length:** 18 chars
- **Prompt hash:** `fbbe5e525705be07`
- **ECS (full):** 0.0833
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{"Braves":8, "6,":1, "Padres":8, "5":1, "Andruw":6, "Jones":6, "hit":4, "a":1, "two-run":5, "homer":7, "off":2, "Trevor":6, "Hoffman":6, "in":2, "the":1, "ninth":5, "inning":5, "and":1, "the":1, "Atlanta":8, "Braves":8, "threw":4, "out":4, "the":1, "potential":3, "tying":3, "run":4, "at":2, "the":1, "plate":4, "for":2, "the":1, "final":3, "out":4, "Wednesday":2, "night,":1, "preserving":3, "a":1, "6-5":1, "come-from-behind":3, "win":4, "over":2, "the":1, "San":6, "Diego":6, "Padres":8}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `andruw`, `atlanta`, `braves`, `homer`, `padres`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives this classification because it describes a specific baseball game, including the score, teams involved, and key events such as a home run and a final out, which are all characteristic elements of a sports news report."}
```

**Rationale text:**
> The text receives this classification because it describes a specific baseball game, including the score, teams involved, and key events such as a home run and a final out, which are all characteristic elements of a sports news report.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `final`, `run`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to World, Business, Sci/Tech.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "Braves", "to": "Diplomats"}], "new_prediction": "World"}
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
{"ranking":["Braves", "homer", "Padres", "run", "win"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `braves`(1), `homer`(2), `padres`(3), `run`(4), `win`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | 0.1667 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a powerbase for radical cleric Moqtada al-Sadr,  the military said."

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
- **Model refused:** No
- **Input length:** 42 words
- **Raw response length:** 17 chars
- **Prompt hash:** `77b3e5eec9068618`
- **ECS (full):** 0.0714
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{
"U.S.":8, 
"Forces":9, 
"Kill":9, 
"50":6, 
"Sadr":8, 
"Militia":9, 
"in":4, 
"Baghdad":8, 
"Suburb":6, 
"BAGHDAD":5, 
"(Reuters)":2, 
"-":1, 
"U.S.":8, 
"forces":9, 
"killed":9, 
"more":5, 
"than":5, 
"50":6, 
"Shi'ite":8, 
"militiamen":9, 
"on":4, 
"Wednesday":5, 
"in":4, 
"a":4, 
"significant":7, 
"advance":7, 
"into":4, 
"a":4, 
"Baghdad":8, 
"suburb":6, 
"that":4, 
"is":4, 
"a":4, 
"powerbase":7, 
"for":4, 
"radical":7, 
"cleric":7, 
"Moqtada":8, 
"al-Sadr,":8, 
"the":4, 
"military":8, 
"said.":4
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `forces`, `kill`, `killed`, `militia`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: World

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives this classification because it reports on a significant military event involving U.S. forces and a radical cleric in a specific location, Baghdad, which are all indicators of a news story about global events and geopolitics."}
```

**Rationale text:**
> The text receives this classification because it reports on a significant military event involving U.S. forces and a radical cleric in a specific location, Baghdad, which are all indicators of a news story about global events and geopolitics.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `military`, `radical`, `significant`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to Sports, Business, Sci/Tech.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: Sports, Business, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "militiamen", "to": "quarterbacks"}], "new_prediction": "Sports"}
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
{"ranking":["Forces", "Baghdad", "militiamen", "military", "cleric"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `forces`(1), `baghdad`(2), `militiamen`(3), `military`(4), `cleric`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.1250 |
| R–CF | — |
| R–RO | 0.1429 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans to expand in Indianapolis, a move that will knock rival ATA Airlines from its No."

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
- **Model refused:** No
- **Input length:** 46 words
- **Raw response length:** 20 chars
- **Prompt hash:** `0b86c33802b9ddb3`
- **ECS (full):** 0.3333
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

For EACH word in the input text, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in the text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the input text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```
{"salience":{
"Steenland:":2, 
"Northwest":8, 
"Joins":4, 
"Southwest":6, 
"In":2, 
"Raiding":6, 
"Bankrupt":8, 
"ATA":8, 
"Turf":4, 
"Gnawed":4, 
"by":2, 
"Northwest":8, 
"Airlines":9, 
"(nasdaq:":1, 
"NWAC":3, 
"-":1, 
"news":1, 
"-":1, 
"people":1, 
")":1, 
"on":2, 
"Tuesday":2, 
"said":4, 
"it":2, 
"plans":6, 
"to":2, 
"expand":6, 
"in":2, 
"Indianapolis,":4, 
"a":2, 
"move":6, 
"that":2, 
"will":4, 
"knock":4, 
"rival":6, 
"ATA":8, 
"Airlines":9, 
"from":2, 
"its":2, 
"No":2, 
"1":2, 
".":1
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `airlines`, `ata`, `bankrupt`, `northwest`, `southwest`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The text receives a Business classification because it discusses the strategic expansion plans of Northwest Airlines, its impact on a rival airline, and the dynamics of the airline industry, all of which are characteristic of business and market trends."}
```

**Rationale text:**
> The text receives a Business classification because it discusses the strategic expansion plans of Northwest Airlines, its impact on a rival airline, and the dynamics of the airline industry, all of which are characteristic of business and market trends.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `airlines`, `rival`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Identify the most important word(s) driving this classification. Replace 1-2 topic-defining words (proper nouns, domain terms, named entities) with words from a different category that would flip the classifier's output to World, Sports, Sci/Tech.

For news classification: replace a word specific to one topic (e.g., "basketball", "stocks", "election", "NASA") with a word from a different topic.

Rules:
- Replace exactly 1-2 individual words from the original text
- Each replacement word must NOT appear in the original text

Return only valid JSON. If no single-word or two-word edit can plausibly flip the label, return:
{"edits": null, "new_prediction": null}

Otherwise, return:
{"edits": [{"from": "original_word", "to": "replacement"}], "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"edits": [{"from": "Airlines", "to": "Teams"}], "new_prediction": "Sports"}
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
{"ranking":["Airlines", "Northwest", "Bankrupt", "Rival", "Expands"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `airlines`(1), `northwest`(2), `bankrupt`(3), `rival`(4)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.1667 |
| H–CF | — |
| H–RO | 0.5000 |
| R–CF | — |
| R–RO | 0.5000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### ag_news_test_0003 (ECS=0.3333)
- **Dataset:** ag_news
- **Text:** Steenland: Northwest Joins Southwest In Raiding Bankrupt ATA Turf Gnawed by Northwest. Joining an apparent feeding frenzy, Northwest Airlines (nasdaq: NWAC - news - people ) on Tuesday said it plans t…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓

### ag_news_test_0000 (ECS=0.2467)
- **Dataset:** ag_news
- **Text:** Mark Cuban prompts dot-com redux reporteri 's notebook SAN FRANCISCO--Hope and cynicism sparred to a draw on Tuesday at the glitzy opening banquet of Web 2.0 conference here, as serial entrepreneur an…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### mnli_validation_matched_0000 (ECS=0.2400)
- **Dataset:** mnli
- **Text:** Premise: Not yourself.
Hypothesis: Someone else
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓


## Low-ECS Examples

### ag_news_test_0002 (ECS=0.0714)
- **Dataset:** ag_news
- **Text:** U.S. Forces Kill 50 Sadr Militia in Baghdad Suburb  BAGHDAD (Reuters) - U.S. forces killed more than 50 Shi'ite  militiamen on Wednesday in a significant advance into a Baghdad  suburb that is a power…
- **Ground truth:** `World` → **Predicted:** `World` ✓

### ag_news_test_0001 (ECS=0.0833)
- **Dataset:** ag_news
- **Text:** Braves 6, Padres 5 Andruw Jones hit a two-run homer off Trevor Hoffman in the ninth inning and the Atlanta Braves threw out the potential tying run at the plate for the final out Wednesday night, pres…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓

### sst2_validation_0001 (ECS=0.1200)
- **Dataset:** sst2
- **Text:** what 's surprising about full frontal is that despite its overt self-awareness , parts of the movie still manage to break past the artifice and thoroughly engage you . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
