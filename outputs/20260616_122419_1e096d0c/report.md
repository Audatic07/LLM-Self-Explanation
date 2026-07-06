# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-16 12:25:50
- **Duration:** 219.6s (3.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 7
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 1575
- **Avg tokens per instance:** 225

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| mnli | 2 | 0/2 (0%) | 0.000 | 0% | 0% | 0% | 0% |
| ag_news | 5 | 3/5 (60%) | 0.196 | 60% | 40% | 0% | 60% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 0 | 0 | 0 |
| mnli | 0 | 0 | 0 |
| ag_news | 10 | 8 | 2 |
| **Total** | 10 | 8 | 2 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=0) or medium-length (21–50 words, N=2). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=0). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=0)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 3/7 | 43% |
| Rationale | 2/7 | 29% |
| Counterfactual | 0/7 | 0% |
| Rank Ordering | 3/7 | 43% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their Jaccard is excluded from ECS; agreement is measured via Kendall τ instead. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=7) | 0.1964 |
| Mean ECS (primary: H,CF,RO) | 0.0000 |
| Mean ECS (complete cases, N=0) | 0.0000 |
| Complete cases | 0/7 (0%) |
| Primary ECS pairs <3 | 2 instances |
  → ag_news_test_0001: 0 pair(s), ECS_primary=0.0000
  → ag_news_test_0002: 0 pair(s), ECS_primary=0.0000
| Std ECS | 0.1964 |
| Median ECS | 0.1964 |
| Confidence elicitation | Removed — does not proxy faithfulness |
| Mean CC3 size | 0.29 |
| Mean CC4 size | 0.29 |
| % instances with CC3 | 14.3% |
| % instances with CC4 | 14.3% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.1429 |
| H–CF | 0.0000 |
| H–RO | 0.3929 |
| R–CF | 0.0000 |
| R–RO | 0.2500 |
| CF–RO | 0.0000 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 3/7 (43%) | 3/7 (43%) |
| Rationale | 2/7 (29%) | 2/7 (29%) |
| Counterfactual | 0/7 (0%) | 0/7 (0%) |
| CF flip verified | 0/0 (0%) |
| Rank Ordering | 3/7 (43%) | 3/7 (43%) |
| All 4 valid | 0/7 |
| 3 valid (CC3 adjusted) | 2/7 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Kendall τ (rank correlation), not Jaccard.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 0 | 0.0000 |
| Medium (21–50) | 2 | 0.1964 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 2 | 0.1964 |
| Short vocab (≤20 unique tokens) | 0 | 0.0000 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.1964 | [0.0000, 0.3929] |

## Per-Instance Details

### mnli_validation_matched_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Input length:** 22 words
- **Raw response length:** 25 chars

### mnli_validation_matched_0006

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 14 words
- **Raw response length:** 22 chars

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
- **Model refused:** No
- **Input length:** 43 words
- **Raw response length:** 17 chars
- **Prompt hash:** `34f8f0bbd178d7da`
- **ECS (full):** 0.3929
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 2 | **CC4 size:** 2

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
"Revelations":6, 
"on":2, 
"children":8, 
"overboard":8, 
"incident":7, 
"put":4, 
"pressure":5, 
"on":2, 
"Australian":9, 
"PM":6, 
"AFP":3, 
"Australian":9, 
"Prime":6, 
"Minister":6, 
"John":5, 
"Howard":5, 
"was":2, 
"fighting":4, 
"to":2, 
"maintain":4, 
"his":2, 
"credibility":5, 
"after":3, 
"official":5, 
"transcripts":5, 
"backed":4, 
"up":2, 
"critics'":4, 
"claims":4, 
"about":3, 
"what":3, 
"he":2, 
"knew":4, 
"of":2, 
"a":2, 
"controversial":6, 
"2001":6, 
"sea":6, 
"rescue":6, 
"of":2, 
"boatpeople":8
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `boatpeople`, `children`, `incident`, `overboard`

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
{"rationale":"The text receives this classification because it discusses a political incident involving the Australian Prime Minister and a controversial sea rescue, which are topics of international news and current events typically found in the World category."}
```

**Rationale text:**
> The text receives this classification because it discusses a political incident involving the Australian Prime Minister and a controversial sea rescue, which are topics of international news and current events typically found in the World category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`, `controversial`, `incident`, `minister`

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
{"edits": [{"from": "Prime Minister", "to": "Coach"}], "new_prediction": "Sports"}
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
{"ranking":["Australian", "Prime", "Minister", "incident", "Howard"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `australian`(1), `prime`(2), `minister`(3), `incident`(4), `howard`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.2857 |
| H–CF | — |
| H–RO | 0.2500 |
| R–CF | — |
| R–RO | 0.5000 |
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
- **Model refused:** No
- **Input length:** 38 words
- **Raw response length:** 17 chars
- **Prompt hash:** `d1c55024370f2e12`
- **ECS (full):** 0.0000
- **ECS (primary):** 0.0000
- **ECS primary pairs:** 0
- **Valid strategies:** 3
- **CF flip verified:** No
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
"U.N.":8, 
"War":9, 
"Court":8, 
"Transfers":6, 
"First":5, 
"Case":7, 
"to":2, 
"Serbia":9, 
"BELGRADE":4, 
"(Reuters)":1, 
"-":1, 
"The":2, 
"U.N.":8, 
"war":9, 
"crimes":9, 
"prosecutor":8, 
"sent":4, 
"the":2, 
"first":5, 
"case":7, 
"to":2, 
"the":2, 
"Serbian":8, 
"judiciary":7, 
"Friday":3, 
"in":2, 
"a":2, 
"move":4, 
"that":2, 
"could":3, 
"warm":4, 
"ties":4, 
"between":4, 
"the":2, 
"Hague-based":6, 
"court":6, 
"and":2, 
"Belgrade":7
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `crimes`, `serbia`, `u.n`, `war`

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
{"rationale":"The text receives this classification because it discusses international relations and a significant event involving the U.N. war crimes prosecutor and a specific country, Serbia, which are all characteristic of global news and affairs."}
```

**Rationale text:**
> The text receives this classification because it discusses international relations and a significant event involving the U.N. war crimes prosecutor and a specific country, Serbia, which are all characteristic of global news and affairs.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `prosecutor`

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
{"edits": [{"from": "U.N.", "to": "NBA"}], "new_prediction": "Sports"}
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
{"ranking":["U.N.", "war", "Serbia", "court", "Belgrade"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `u.n`(1), `war`(2), `serbia`(3), `court`(4), `belgrade`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | 0.0000 |
| H–CF | — |
| H–RO | 0.5000 |
| R–CF | — |
| R–RO | 0.0000 |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |

### ag_news_test_0004

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Input length:** 25 words
- **Raw response length:** 20 chars

### ag_news_test_0005

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sci/Tech`
- **Predicted:** `World` ✗
- **Input length:** 55 words
- **Raw response length:** 17 chars

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
- **Model refused:** No
- **Input length:** 29 words
- **Raw response length:** 18 chars
- **Prompt hash:** `1ed0148e7838e3a9`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
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
{"salience":{
"United":8, 
"States":8, 
"66,":1, 
"Russia":8, 
"62":1, 
"Frustrated":4, 
"by":2, 
"fouls,":6, 
"turnovers":6, 
"and":2, 
"a":2, 
"feisty":4, 
"opponent,":4, 
"the":2, 
"desperately":4, 
"looked":4, 
"for":2, 
"help.":2, 
"Then":2, 
"along":2, 
"came":2, 
"Sheryl":9, 
"Swoopes":9, 
"to":2, 
"set":2, 
"things":2, 
"right.":2
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `russia`, `sheryl`, `states`, `swoopes`, `united`

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
{"rationale":"The text receives this classification because it describes a competitive event with a final score, mentions a specific player, and conveys a sense of action and tension, all of which are characteristic of a sports news report."}
```

**Parsed tokens:**
- *Not parsed*

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
{"edits": [{"from": "United States", "to": "Microsoft"}], "new_prediction": "Business"}
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
{"ranking":["United", "States", "Russia", "fouls", "turnovers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `united`(1), `states`(2), `russia`(3), `fouls`(4), `turnovers`(5)

#### 5. Pairwise Agreement (Jaccard)

| Pair | Jaccard |
|------|---------|
| H–R | — |
| H–CF | — |
| H–RO | 0.4286 |
| R–CF | — |
| R–RO | — |
| CF–RO | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |


## High-ECS Examples

### ag_news_test_0002 (ECS=0.0000)
- **Dataset:** ag_news
- **Text:** U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hagu…
- **Ground truth:** `World` → **Predicted:** `World` ✓

### ag_news_test_0001 (ECS=0.3929)
- **Dataset:** ag_news
- **Text:** Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed …
- **Ground truth:** `World` → **Predicted:** `World` ✓


## Low-ECS Examples

### ag_news_test_0002 (ECS=0.0000)
- **Dataset:** ag_news
- **Text:** U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hagu…
- **Ground truth:** `World` → **Predicted:** `World` ✓

### ag_news_test_0001 (ECS=0.3929)
- **Dataset:** ag_news
- **Text:** Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed …
- **Ground truth:** `World` → **Predicted:** `World` ✓
