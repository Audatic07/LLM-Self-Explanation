# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-16 15:05:32
- **Duration:** 58.4s (1.0m)
- **Model:** openai/gpt-oss-120b
- **Total instances:** 4
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 1486
- **Avg tokens per instance:** 372

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| ag_news | 4 | — | 0.190 | 0% | 50% | 25% | 50% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| ag_news | 5 | 4 | 1 |
| **Total** | 5 | 4 | 1 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=0) or medium-length (21–50 words, N=1). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=0). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=0)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 0/4 | 0% |
| Rationale | 2/4 | 50% |
| Counterfactual | 1/4 | 25% |
| Rank Ordering | 2/4 | 50% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=4) | 0.1905 |
| Mean ECS (primary: H,CF,RO) | 0.4286 |
| Mean ECS (complete cases, N=0) | 0.0000 |
| Complete cases | 0/4 (0%) |
| Primary ECS pairs <3 | 1 instances |
  → ag_news_test_0001: 1 pair(s), ECS_primary=0.4286
| Std ECS | 0.0000 |
| Median ECS | 0.1905 |
| Confidence elicitation | Removed — does not proxy faithfulness |
| Mean CC3 size | 0.00 |
| Mean CC4 size | 0.00 |
| % instances with CC3 | 0.0% |
| % instances with CC4 | 0.0% |

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 0.0000 | 0.0000 |
| H–RO | 0.0000 | 0.0000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.3333 | 0.3333 |
| CF–RO | 0.6000 | 0.4286 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | — |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Overlap Coefficient is the primary pairwise metric (unlike Jaccard, it is not penalized by smaller salience sets). Jaccard is retained as a secondary reference. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 0/4 (0%) | 0/4 (0%) |
| Rationale | 2/4 (50%) | 2/4 (50%) |
| Counterfactual | 1/4 (25%) | 1/4 (25%) |
| CF flip verified | 1/1 (100%) |
| Rank Ordering | 2/4 (50%) | 2/4 (50%) |
| All 4 valid | 0/4 |
| 3 valid (CC3 adjusted) | 1/4 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 0 | 0.0000 |
| Medium (21–50) | 1 | 0.1905 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 1 | 0.1905 |
| Short vocab (≤20 unique tokens) | 0 | 0.0000 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.1905 | [0.0000, 0.0000] |

## Per-Instance Details

### ag_news_test_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Sci/Tech`
- **Predicted:** `Business` ✗
- **Input length:** 19 words
- **Raw response length:** 20 chars

### ag_news_test_0001

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, saying any reform would be one-sided if new members did not have veto power."

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
- **Prompt hash:** `a7f51cfce14b864b`
- **ECS (full):** 0.1905
- **ECS (primary):** 0.4286
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `Sports`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: World

Here is the exact text that was classified:
"Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, saying any reform would be one-sided if new members did not have veto power."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
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

Here is the exact text that was classified:
"Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, saying any reform would be one-sided if new members did not have veto power."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article discusses a political decision by Russian President Vladimir Putin regarding United Nations Security Council reform, which is an international diplomatic issue, placing it squarely in the World news category."}
```

**Rationale text:**
> The article discusses a political decision by Russian President Vladimir Putin regarding United Nations Security Council reform, which is an international diplomatic issue, placing it squarely in the World news category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `putin`, `reform`, `russian`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: World

Here is the exact text that was classified:
"Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, saying any reform would be one-sided if new members did not have veto power."

Rewrite the text above with MINIMAL changes to flip the classifier's output to Sports, Business, Sci/Tech. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: Sports, Business, Sci/Tech

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a FIFA panel on expanding the UN Security Council, saying any reform would be one-sided if new members did not have veto power.", "new_prediction":"Sports"}
```

**Reconstructed text:**
> Putin backs veto for members of expanded World Cup Russian President Vladimir Putin yesterday rejected a key recommendation of a FIFA panel on expanding the World Cup, saying any reform would be one-sided if new members did not have veto power.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `council`, `nations`, `security`, `un`, `united`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: World

Here is the exact text that was classified:
"Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, saying any reform would be one-sided if new members did not have veto power."

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Putin","Security","Council","veto","UN"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `putin`(1), `security`(2), `council`(3), `veto`(4), `un`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.3333 | 0.1429 |
| CF–RO | 0.6000 | 0.4286 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### ag_news_test_0002

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Dollar Holds Above Record Low Vs Euro  LONDON (Reuters) - The dollar held almost a cent above its  record low against the euro on Tuesday, winning a respite after  heavy selling as European officials warned about a strong euro  and investors grew wary ahead of U.S. trade data."

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
- **Input length:** 48 words
- **Raw response length:** 20 chars
- **Prompt hash:** `99c601d06d130b30`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 1
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Dollar Holds Above Record Low Vs Euro  LONDON (Reuters) - The dollar held almost a cent above its  record low against the euro on Tuesday, winning a respite after  heavy selling as European officials warned about a strong euro  and investors grew wary ahead of U.S. trade data."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Dollar Holds Above Record Low Vs Euro  LONDON (Reuters) - The dollar held almost a cent above its  record low against the euro on Tuesday, winning a respite after  heavy selling as European officials warned about a strong euro  and investors grew wary ahead of U.S. trade data."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The article discusses currency movements, the dollar‑euro exchange rate, and investor reactions to trade data, all of which are core topics of financial markets and economics, placing it squarely in the Business category."}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Dollar Holds Above Record Low Vs Euro  LONDON (Reuters) - The dollar held almost a cent above its  record low against the euro on Tuesday, winning a respite after  heavy selling as European officials warned about a strong euro  and investors grew wary ahead of U.S. trade data."

Rewrite the text above with MINIMAL changes to flip the classifier's output to World, Sports, Sci/Tech. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: World, Sports, Sci/Tech

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"Dollar Holds Above Record Low Vs Euro  LONDON (Reuters) - The dollar held almost a cent above its  record low against the euro on Tuesday, winning a respite after  heavy selling as European officials warned about a strong euro  and investors grew wary ahead of U.S. election data.","new_prediction":"World"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Business

Here is the exact text that was classified:
"Dollar Holds Above Record Low Vs Euro  LONDON (Reuters) - The dollar held almost a cent above its  record low against the euro on Tuesday, winning a respite after  heavy selling as European officials warned about a strong euro  and investors grew wary ahead of U.S. trade data."

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```
{"ranking":["Dollar","Euro","trade","investors","record"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dollar`(1), `euro`(2), `trade`(3), `investors`(4), `record`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

### ag_news_test_0003

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Today in Athens Leontien Zijlaard-van Moorsel of the Netherlands wipes a tear after winning the gold medal in the women 's road cycling individual time trial at the Vouliagmeni Olympic Centre in Athens on Wednesday. "

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
- **Input length:** 35 words
- **Raw response length:** 18 chars
- **Prompt hash:** `499246307c2c4512`
- **ECS (full):** —
- **ECS (primary):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 1
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Today in Athens Leontien Zijlaard-van Moorsel of the Netherlands wipes a tear after winning the gold medal in the women 's road cycling individual time trial at the Vouliagmeni Olympic Centre in Athens on Wednesday. "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Today in Athens Leontien Zijlaard-van Moorsel of the Netherlands wipes a tear after winning the gold medal in the women 's road cycling individual time trial at the Vouliagmeni Olympic Centre in Athens on Wednesday. "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**
```
{"rationale":"The passage describes an athlete winning a gold medal in a women's road cycling time trial at the Olympic Games, focusing on a specific sporting event and competitor, which clearly identifies it as sports content."}
```

**Rationale text:**
> The passage describes an athlete winning a gold medal in a women's road cycling time trial at the Olympic Games, focusing on a specific sporting event and competitor, which clearly identifies it as sports content.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `medal`, `trial`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Today in Athens Leontien Zijlaard-van Moorsel of the Netherlands wipes a tear after winning the gold medal in the women 's road cycling individual time trial at the Vouliagmeni Olympic Centre in Athens on Wednesday. "

Rewrite the text above with MINIMAL changes to flip the classifier's output to World, Business, Sci/Tech. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: World, Business, Sci/Tech

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**
```
{"rewritten":"Today in Athens Leontien Zijlaard-van Moorsel of the Netherlands wipes a tear after winning the gold medal in the women 's road cycling individual time trial at the Vouliagmeni UN Centre in Athens on Wednesday.", "new_prediction":"World"}
```

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Here is the exact text that was classified:
"Today in Athens Leontien Zijlaard-van Moorsel of the Netherlands wipes a tear after winning the gold medal in the women 's road cycling individual time trial at the Vouliagmeni Olympic Centre in Athens on Wednesday. "

Rank the 3-5 most important individual SINGLE WORDS for this classification, from most important to least important. Each item must be a single word copied verbatim from the original text — no phrases, no hyphenated compounds, no multi-word expressions. Use fewer than 5 only if there genuinely aren't 5 informative words.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**
```

```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | — | — |
| H–CF | — | — |
| H–RO | — | — |
| R–CF | — | — |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |


## High-ECS Examples

### ag_news_test_0001 (ECS=0.1905)
- **Dataset:** ag_news
- **Text:** Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, sayin…
- **Ground truth:** `World` → **Predicted:** `World` ✓


## Low-ECS Examples

### ag_news_test_0001 (ECS=0.1905)
- **Dataset:** ag_news
- **Text:** Putin backs veto for members of expanded Security Council Russian President Vladimir Putin yesterday rejected a key recommendation of a United Nations panel on expanding the UN Security Council, sayin…
- **Ground truth:** `World` → **Predicted:** `World` ✓
