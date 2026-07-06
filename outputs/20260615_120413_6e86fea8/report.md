# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-15 12:04:21
- **Duration:** 51.7s (0.9m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 2127
- **Avg tokens per instance:** 79

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 10 | — | 0.000 | 0% | 0% | 0% | 0% |
| mnli | 9 | — | 0.000 | 0% | 0% | 0% | 0% |
| ag_news | 8 | — | 0.694 | 25% | 38% | 0% | 38% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 0 | 0 | 0 |
| mnli | 0 | 0 | 0 |
| ag_news | 10 | 8 | 5 |
| **Total** | 10 | 8 | 5 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N={overall.n_short}) or medium-length (21–50 words, N={overall.n_medium}). ECS may partly reflect brevity.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N={overall.n_complete_cases})

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 2/27 | 7% |
| Rationale | 3/27 | 11% |
| Counterfactual | 0/27 | 0% |
| Rank Ordering | 3/27 | 11% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=27) | 0.6944 |
| Mean ECS (primary: H,CF,RO) | 0.6250 |
| Mean ECS (complete cases, N=0) | 0.0000 |
| Complete cases | 0/27 (0%) |
| Primary ECS pairs <3 | 2 instances |
  → ag_news_test_0000: 1 pair(s), ECS_primary=0.2500
  → ag_news_test_0003: 1 pair(s), ECS_primary=1.0000
| Std ECS | 0.3056 |
| Median ECS | 0.6944 |
| Spearman ρ (confidence vs ECS) | 0.0000 (p=1.0000) — no significant association |
| Mean CC3 size | 0.22 |
| Mean CC4 size | 0.22 |
| % instances with CC3 | 7.4% |
| % instances with CC4 | 7.4% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.6250 |
| H–CF | 0.0000 |
| H–RO | 0.6250 |
| R–CF | 0.0000 |
| R–RO | 0.7778 |
| CF–RO | 0.0000 |

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 2/27 (7%) | 2/27 (7%) |
| Rationale | 3/27 (11%) | 3/27 (11%) |
| Counterfactual | 0/27 (0%) | 0/27 (0%) |
| CF flip verified | 0/0 (0%) |
| Rank Ordering | 3/27 (11%) | 3/27 (11%) |
| All 4 valid | 0/27 |
| 3 valid (CC3 adjusted) | 2/27 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. Primary ECS averages H–CF, H–RO, CF–RO (evidence-list methods). Full ECS includes all 6 pairwise Jaccards.

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 0 | 0.0000 |
| Medium (21–50) | 2 | 0.6944 |
| Long (>50 words) | 0 | 0.0000 |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.6944 | [0.3889, 1.0000] |
| Spearman ρ (self-reported confidence) | 0.0000 | [0.0000, 0.0000] |

## Per-Instance Details

### sst2_validation_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `` ✗
- **Input length:** 33 words
- **Raw response length:** 0 chars

### sst2_validation_0001

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `` ✗
- **Input length:** 6 words
- **Raw response length:** 0 chars

### sst2_validation_0002

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `` ✗
- **Input length:** 15 words
- **Raw response length:** 0 chars

### sst2_validation_0003

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `positive`
- **Predicted:** `` ✗
- **Input length:** 22 words
- **Raw response length:** 0 chars

### sst2_validation_0004

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `positive`
- **Predicted:** `` ✗
- **Input length:** 25 words
- **Raw response length:** 0 chars

### sst2_validation_0005

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `positive`
- **Predicted:** `` ✗
- **Input length:** 16 words
- **Raw response length:** 0 chars

### sst2_validation_0006

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `` ✗
- **Input length:** 11 words
- **Raw response length:** 0 chars

### sst2_validation_0007

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `positive`
- **Predicted:** `` ✗
- **Input length:** 19 words
- **Raw response length:** 0 chars

### sst2_validation_0008

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `negative`
- **Predicted:** `` ✗
- **Input length:** 14 words
- **Raw response length:** 0 chars

### sst2_validation_0009

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `positive`
- **Predicted:** `` ✗
- **Input length:** 5 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `` ✗
- **Input length:** 22 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0001

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `` ✗
- **Input length:** 26 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0002

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `entailment`
- **Predicted:** `` ✗
- **Input length:** 29 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0003

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `contradiction`
- **Predicted:** `` ✗
- **Input length:** 40 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0004

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `entailment`
- **Predicted:** `` ✗
- **Input length:** 35 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0005

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `contradiction`
- **Predicted:** `` ✗
- **Input length:** 17 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0006

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `` ✗
- **Input length:** 14 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0007

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `contradiction`
- **Predicted:** `` ✗
- **Input length:** 18 words
- **Raw response length:** 0 chars

### mnli_validation_matched_0008

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `entailment`
- **Predicted:** `` ✗
- **Input length:** 24 words
- **Raw response length:** 0 chars

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
- **Confidence:** 0.0%
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
  "rationale":"The article discusses a shareholder dispute over a corporate acquisition and stock buyout, which are topics of business news.",
  "evidence":["Icahn","CEO","Mylan","stock","deal"]
}
```

**Rationale text:**
> The article discusses a shareholder dispute over a corporate acquisition and stock buyout, which are topics of business news.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ceo`, `deal`, `icahn`, `mylan`, `stock`

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

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `World`
- **Predicted:** `` ✗
- **Input length:** 43 words
- **Raw response length:** 0 chars

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
{"ranking":["U.N.","Serbia","War","Court","Belgrade"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `u.n`(1), `serbia`(2), `war`(3), `court`(4), `belgrade`(5)

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
- **Confidence:** 76.0%
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

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Business`
- **Predicted:** `` ✗
- **Input length:** 25 words
- **Raw response length:** 0 chars

### ag_news_test_0005

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sci/Tech`
- **Predicted:** `` ✗
- **Input length:** 55 words
- **Raw response length:** 0 chars

### ag_news_test_0006

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sports`
- **Predicted:** `` ✗
- **Input length:** 29 words
- **Raw response length:** 0 chars

### ag_news_test_0007

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sports`
- **Predicted:** `` ✗
- **Input length:** 43 words
- **Raw response length:** 0 chars


## High-ECS Examples

### ag_news_test_0000 (ECS=0.3889)
- **Dataset:** ag_news
- **Text:** Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pha…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 0.0%

### ag_news_test_0003 (ECS=1.0000)
- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 76.0%


## Low-ECS Examples

### ag_news_test_0000 (ECS=0.3889)
- **Dataset:** ag_news
- **Text:** Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pha…
- **Ground truth:** `Business` → **Predicted:** `Business` ✓
- **Confidence:** 0.0%

### ag_news_test_0003 (ECS=1.0000)
- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 76.0%
