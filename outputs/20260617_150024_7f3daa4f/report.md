# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-17 15:00:35
- **Duration:** 860.5s (14.3m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 27
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 13168
- **Avg tokens per instance:** 488

## Per-Dataset Summary

| Dataset | Instances | Accuracy     | Mean ECS | H    | R   | CF   | RO   |
| ------- | --------- | ------------ | -------- | ---- | --- | ---- | ---- |
| sst2    | 10        | 10/10 (100%) | 0.253    | 100% | 80% | 80%  | 90%  |
| mnli    | 9         | 7/9 (78%)    | 0.249    | 100% | 67% | 100% | 67%  |
| ag_news | 8         | 6/8 (75%)    | 0.150    | 88%  | 75% | 50%  | 100% |

## Sampling Log

| Dataset         | Requested | Sampled | Wrong Pred |
| --------------- | --------- | ------- | ---------- |
| sst2            | 10        | 10      | 0          |
| mnli            | 10        | 9       | 2          |
| ag_news         | 10        | 8       | 2          |
| **Total** | 30        | 27      | 4          |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=8) or medium-length (21–50 words, N=13). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=11). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=14)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy       | Valid / Total | Rate |
| -------------- | ------------- | ---- |
| Highlighting   | 26/27         | 96%  |
| Rationale      | 20/27         | 74%  |
| Counterfactual | 21/27         | 78%  |
| Rank Ordering  | 23/27         | 85%  |

Coverage varies dramatically.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).

## Overall Metrics

| Metric                                                       | Value                                                                      |
| ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Mean ECS (all, N=27)                                         | 0.2283                                                                     |
| Mean ECS (extraction–rationale: H,R,RO)                     | 0.2578                                                                     |
| Mean ECS (extraction–perturbation: H,CF,RO)                 | 0.2049                                                                     |
| Mean ECS (complete cases, N=14)                              | 0.2012                                                                     |
| Complete cases                                               | 14/27 (52%)                                                                |
| ECS pairs <3                                                 | 6 instances                                                                |
| → sst2_validation_0001: 1 pair(s), er=0.3333, ep=NA         |                                                                            |
| → sst2_validation_0004: 1 pair(s), er=0.5000, ep=NA         |                                                                            |
| → sst2_validation_0006: 1 pair(s), er=NA, ep=0.2000         |                                                                            |
| → mnli_validation_matched_0006: 1 pair(s), er=NA, ep=0.4000 |                                                                            |
| → mnli_validation_matched_0007: 1 pair(s), er=NA, ep=0.3333 |                                                                            |
| → ... and 1 more                                            |                                                                            |
| Std ECS                                                      | 0.0965                                                                     |
| Median ECS                                                   | 0.2133                                                                     |
| **Mean ECS lift over chance** (ECS − random)          | +0.1329                                                                    |
| Mean ECS random baseline                                     | 0.0953                                                                     |
| Mean ECS — correct preds (N=18)                             | 0.2194                                                                     |
| Mean ECS — incorrect preds (N=4)                            | 0.2681                                                                     |
| Introduced-concept rate (R)                                  | 0.717                                                                      |
| CF-free validity rate                                        | 78%                                                                        |
| CF-minimal validity rate                                     | 41%                                                                        |
| CF-free minimality (edits/len)                               | 0.094                                                                      |
| CF-minimal minimality (edits/len)                            | 0.072                                                                      |
| Confidence elicitation                                       | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size                                                | 1.30                                                                       |
| Mean CC4 size                                                | 0.33                                                                       |
| % instances with CC3                                         | 70.4%                                                                      |
| % instances with CC4                                         | 25.9%                                                                      |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair   | Overlap Coeff (mean) | Jaccard (mean) |
| ------ | -------------------- | -------------- |
| H–R   | 0.6184               | 0.2578         |
| H–CF  | 0.6198               | 0.2092         |
| H–RO  | 0.7205               | 0.5745         |
| R–CF  | 0.1146               | 0.0490         |
| R–RO  | 0.7287               | 0.2983         |
| CF–RO | 0.6843               | 0.2364         |

### Rank-Based Agreement (H vs RO)

| Metric            | Value  |
| ----------------- | ------ |
| RBO (H,RO)        | 0.1719 |
| Kendall τ (H,RO) | 0.4667 |
| Normalized τ     | 0.7333 |

> Overlap Coefficient is the primary pairwise metric (unlike Jaccard, it is not penalized by smaller salience sets). Jaccard is retained as a secondary reference. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy                         | Parsed      | Valid       |
| -------------------------------- | ----------- | ----------- |
| Highlighting                     | 26/27 (96%) | 26/27 (96%) |
| Rationale                        | 20/27 (74%) | 20/27 (74%) |
| Counterfactual (JSON parsed)     | 26/27 (96%) |             |
| Counterfactual (rules compliant) | 26/27 (96%) |             |
| Counterfactual (flip verified)   | 21/26 (81%) |             |
| Rank Ordering                    | 23/27 (85%) | 23/27 (85%) |
| All 4 valid                      | 14/27       |             |
| 3 valid (CC3 adjusted)           | 8/27        |             |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length             | N  | Mean ECS |
| ------------------ | -- | -------- |
| Short (≤20 words) | 8  | 0.2448   |
| Medium (21–50)    | 13 | 0.2150   |
| Long (>50 words)   | 1  | 0.2686   |

### ECS by Vocabulary Size

| Vocab Bucket                     | N  | Mean ECS |
| -------------------------------- | -- | -------- |
| Normal vocab (>20 unique tokens) | 11 | 0.2210   |
| Short vocab (≤20 unique tokens) | 11 | 0.2356   |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric   | Estimate | 95% CI           |
| -------- | -------- | ---------------- |
| Mean ECS | 0.2283   | [0.1902, 0.2685] |

## Per-Instance Details

### sst2_validation_0000

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

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
- **Input length:** 33 words
- **Raw response length:** 20 chars
- **Prompt hash:** `cb4f063c0376ab79`
- **ECS (full):** 0.2067
- **ECS (extraction–rationale):** 0.2000
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"very": 4, 
"special": 4, 
"effects": 4, 
"brilliantly": 4, 
"bold": 4, 
"colors": 4, 
"and": 2, 
"heightened": 4, 
"reality": 4, 
"ca": 1, 
"n't": 2, 
"hide": 6, 
"the": 2, 
"giant": 8, 
"achilles": 8, 
"heel": 8, 
"in": 2, 
"stuart": 6, 
"little": 6, 
"2": 6, 
"there's": 6, 
"just": 6, 
"no": 10, 
"story": 10, 
"folks": 4
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `achilles`, `giant`, `heel`, `no`, `story`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because, despite acknowledging some impressive technical aspects of the movie, the criticism of a fundamental flaw, specifically the lack of a story, outweighs these positives and dominates the overall sentiment."}
```

**Rationale text:**

> The text receives a negative classification because, despite acknowledging some impressive technical aspects of the movie, the criticism of a fundamental flaw, specifically the lack of a story, outweighs these positives and dominates the overall sentiment.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `story`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

Rewrite the text so a classifier would instead predict one of: positive.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: positive>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "very special effects , brilliantly bold colors and heightened reality are perfectly complemented by the giant strength in `` stuart little 2 `` : there 's a wonderfully engaging story , folks .", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> very special effects , brilliantly bold colors and heightened reality are perfectly complemented by the giant strength in ``stuart little 2`` : there 's a wonderfully engaging story , folks .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `achilles`, `ca`, `heel`, `hide`, `just`, `n't`, `no`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"very special effects , brilliantly bold colors and heightened reality ca n't hide the giant achilles ' heel in `` stuart little 2 `` : there 's just no story , folks . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["no", "heel", "ca", "n't", "folks"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `no`(1), `heel`(2), `ca`(3), `n't`(4), `folks`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.2000  |
| H–CF             | 0.6000        | 0.3333  |
| H–RO             | 0.4000        | 0.2500  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.0000        | 0.0000  |
| CF–RO            | 0.8000        | 0.5000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2165        |         |

### sst2_validation_0001

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "holden caulfield did it better . "

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
- **Input length:** 6 words
- **Raw response length:** 20 chars
- **Prompt hash:** `a447a2ee53afc6bc`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"holden caulfield did it better . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"holden":8, "caulfield":8, "did":6, "it":4, "better":9, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `better`, `caulfield`, `holden`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"holden caulfield did it better . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because it implies that the subject being referred to is inferior to Holden Caulfield, a character known for his rebellious and critical nature, suggesting a comparison that diminishes the subject's value or accomplishment."}
```

**Rationale text:**

> The text receives a negative classification because it implies that the subject being referred to is inferior to Holden Caulfield, a character known for his rebellious and critical nature, suggesting a comparison that diminishes the subject's value or accomplishment.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `caulfield`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"holden caulfield did it better . "

Rewrite the text so a classifier would instead predict one of: positive.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: positive>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "holden caulfield didn't do it better . ", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `negative`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"holden caulfield did it better . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["better","did","it","holden","caulfield"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `holden`(1), `caulfield`(2), `better`(3)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.3333  |
| H–CF             | —            | —      |
| H–RO             | 1.0000        | 1.0000  |
| R–CF             | —            | —      |
| R–RO             | 1.0000        | 0.3333  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2200        |         |

### sst2_validation_0002

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

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
- **Input length:** 15 words
- **Raw response length:** 20 chars
- **Prompt hash:** `2e2ef0e5cd8ece6c`
- **ECS (full):** 0.1533
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.1667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"k-19":8, "exploits":9, "our":2, "substantial":6, "collective":6, "fear":8, "of":1, "nuclear":7, "holocaust":8, "to":1, "generate":5, "cheap":4, "hollywood":3, "tension":5, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `exploits`, `fear`, `holocaust`, `k-19`, `nuclear`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because it describes the film's method of generating tension as exploitative and cheap, implying a criticism of the film's approach to evoking emotions from its audience."}
```

**Rationale text:**

> The text receives a negative classification because it describes the film's method of generating tension as exploitative and cheap, implying a criticism of the film's approach to evoking emotions from its audience.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `tension`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

Rewrite the text so a classifier would instead predict one of: positive.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: positive>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "k-19 harnesses our substantial collective fear of nuclear holocaust to generate gripping hollywood tension . ", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> k-19 harnesses our substantial collective fear of nuclear holocaust to generate gripping hollywood tension .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `cheap`, `exploits`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"k-19 exploits our substantial collective fear of nuclear holocaust to generate cheap hollywood tension . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["cheap", "fear", "exploits", "tension", "holocaust"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `cheap`(1), `fear`(2), `exploits`(3), `tension`(4), `holocaust`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | 0.5000        | 0.1667  |
| H–RO             | 0.6000        | 0.4286  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.2000  |
| CF–RO            | 1.0000        | 0.4000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1298        |         |

### sst2_validation_0003

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

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
- **Input length:** 22 words
- **Raw response length:** 20 chars
- **Prompt hash:** `62feda1e67645d47`
- **ECS (full):** 0.2200
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.4000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"neither":6, 
"parker":8, 
"nor":6, 
"donovan":8, 
"is":4, 
"a":2, 
"typical":7, 
"romantic":7, 
"lead":7, 
"but":5, 
"they":5, 
"bring":9, 
"a":2, 
"fresh":9, 
"quirky":9, 
"charm":9, 
"to":3, 
"the":2, 
"formula":6, 
"(":1, 
")":1 
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `bring`, `charm`, `fresh`, `parker`, `quirky`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because it frames the unconventional nature of the romantic leads as a strength, emphasizing the unique and charming qualities they bring to the story, which suggests an overall appreciation and enthusiasm for their portrayal."}
```

**Rationale text:**

> The text receives a positive classification because it frames the unconventional nature of the romantic leads as a strength, emphasizing the unique and charming qualities they bring to the story, which suggests an overall appreciation and enthusiasm for their portrayal.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `lead`, `romantic`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

Rewrite the text so a classifier would instead predict one of: negative.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: negative>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "neither parker nor donovan is a typical romantic lead , but they bring a stale , quirky charmlessness to the formula . ", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> neither parker nor donovan is a typical romantic lead , but they bring a stale , quirky charmlessness to the formula .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `charm`, `fresh`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"neither parker nor donovan is a typical romantic lead , but they bring a fresh , quirky charm to the formula . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["fresh", "charm", "quirky", "but", "lead"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `fresh`(1), `charm`(2), `quirky`(3), `lead`(4)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | 1.0000        | 0.4000  |
| H–RO             | 0.7500        | 0.5000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.5000        | 0.2000  |
| CF–RO            | 1.0000        | 0.5000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1930        |         |

### sst2_validation_0004

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

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
- **Input length:** 25 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1f15d549cc74ae6d`
- **ECS (full):** 0.5000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"it":2, "s":1, "a":2, "work":6, "by":2, "an":2, "artist":8, "so":4, "in":3, "control":9, "of":3, "both":5, "his":4, "medium":8, "and":4, "his":4, "message":8, "that":4, "he":4, "can":6, "improvise":8, "like":5, "a":2, "jazzman":7, "":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `artist`, `control`, `improvise`, `medium`, `message`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because it describes the artist as being in control of their medium and message, implying a high level of skill and mastery, and also makes a favorable comparison to a jazzman, which is often associated with creativity and expertise."}
```

**Rationale text:**

> The text receives a positive classification because it describes the artist as being in control of their medium and message, implying a high level of skill and mastery, and also makes a favorable comparison to a jazzman, which is often associated with creativity and expertise.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `artist`, `control`, `jazzman`, `medium`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

Rewrite the text so a classifier would instead predict one of: negative.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: negative>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "it 's a work by an artist so out of control of both his medium and his message that he can improvise like a jazzman . ", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `positive`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["artist", "control", "improvise", "jazzman", "work"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `artist`(1), `control`(2), `improvise`(3), `jazzman`(4), `work`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.7500        | 0.5000  |
| H–CF             | —            | —      |
| H–RO             | 0.6000        | 0.4286  |
| R–CF             | —            | —      |
| R–RO             | 0.7500        | 0.5000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2198        |         |

### sst2_validation_0005

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "what better message than ` love thyself ' could young women of any size receive ? "

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
- **Input length:** 16 words
- **Raw response length:** 20 chars
- **Prompt hash:** `ac9a9f698f4c0eba`
- **ECS (full):** 0.1800
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** 0.2000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"what better message than ` love thyself ' could young women of any size receive ? "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"what":6, "better":8, "message":7, "than":4, "love":10, "thyself":10, "could":5, "young":8, "women":9, "of":3, "any":6, "size":7, "receive":8}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `better`, `love`, `thyself`, `women`, `young`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"what better message than ` love thyself ' could young women of any size receive ? "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because it presents the message of self-love as a universally beneficial and uplifting idea, particularly for young women of any size, implying a supportive and empowering tone."}
```

**Rationale text:**

> The text receives a positive classification because it presents the message of self-love as a universally beneficial and uplifting idea, particularly for young women of any size, implying a supportive and empowering tone.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `love`, `message`, `receive`, `size`, `young`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"what better message than ` love thyself ' could young women of any size receive ? "

Rewrite the text so a classifier would instead predict one of: negative.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: negative>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "what worse message than ` love thyself ' could young women of any size receive ?", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> what worse message than ` love thyself ' could young women of any size receive ?

**Parsed tokens:**

- Status: **Valid**
- Tokens: `better`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"what better message than ` love thyself ' could young women of any size receive ? "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["love","better","thyself","young","women"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `love`(1), `better`(2), `thyself`(3), `young`(4), `women`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.4000        | 0.2500  |
| H–CF             | 1.0000        | 0.2000  |
| H–RO             | 1.0000        | 1.0000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.4000        | 0.2500  |
| CF–RO            | 1.0000        | 0.2000  |
| Kendall τ (H,RO) | 0.4000        |         |
| Normalized τ     | 0.7000        |         |
| RBO (H,RO)        | 0.3193        |         |

### sst2_validation_0006

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
- **ECS (full):** 0.2000
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.2000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"verbinski":6, "implements":4, "every":3, "hack-artist":8, "trick":5, "to":2, "give":2, "us":2, "the":2, "ooky-spookies":7}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `hack-artist`, `implements`, `ooky-spookies`, `trick`, `verbinski`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because the phrase as a whole implies that the filmmaker is relying on cheap or unoriginal techniques to create a certain atmosphere, suggesting a lack of genuine skill or creativity."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

Rewrite the text so a classifier would instead predict one of: positive.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: positive>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "verbinski implements every masterful trick to give us the ooky-spookies . ", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> verbinski implements every masterful trick to give us the ooky-spookies .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `hack-artist`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"verbinski implements every hack-artist trick to give us the ooky-spookies . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["hack-artist","trick","ooky-spookies","every","implements"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `hack-artist`(1), `trick`(2), `ooky-spookies`(3), `every`(4), `implements`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 1.0000        | 0.2000  |
| H–RO             | 0.8000        | 0.6667  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | 1.0000        | 0.2000  |
| Kendall τ (H,RO) | 0.6667        |         |
| Normalized τ     | 0.8333        |         |
| RBO (H,RO)        | 0.3062        |         |

### sst2_validation_0007

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . "

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
- **Input length:** 19 words
- **Raw response length:** 20 chars
- **Prompt hash:** `63718fc189536913`
- **ECS (full):** 0.2933
- **ECS (extraction–rationale):** 0.4000
- **ECS (extraction–perturbation):** 0.1667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"as":2, "the":2, "two":4, "leads":6, "lathan":8, "and":3, "diggs":8, "are":5, "charming":9, "and":3, "have":5, "chemistry":9, "both":4, "as":2, "friends":6, "and":3, "lovers":6, "":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `charming`, `chemistry`, `diggs`, `lathan`, `leads`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because it describes the leads as having a desirable and appealing on-screen relationship, with the description of them being charming and having chemistry conveying a sense of warmth and enthusiasm."}
```

**Rationale text:**

> The text receives a positive classification because it describes the leads as having a desirable and appealing on-screen relationship, with the description of them being charming and having chemistry conveying a sense of warmth and enthusiasm.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `charming`, `chemistry`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . "

Rewrite the text so a classifier would instead predict one of: negative.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: negative>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "as the two leads , lathan and diggs are uncharming and lack chemistry both as friends and lovers . ", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> as the two leads , lathan and diggs are uncharming and lack chemistry both as friends and lovers .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `charming`, `have`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"as the two leads , lathan and diggs are charming and have chemistry both as friends and lovers . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["charming","chemistry","lovers","leads","friends"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `charming`(1), `chemistry`(2), `lovers`(3), `leads`(4), `friends`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.4000  |
| H–CF             | 0.5000        | 0.1667  |
| H–RO             | 0.6000        | 0.4286  |
| R–CF             | 0.5000        | 0.3333  |
| R–RO             | 1.0000        | 0.4000  |
| CF–RO            | 0.5000        | 0.1667  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.3198        |         |

### sst2_validation_0008

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
- **ECS (full):** 0.1933
- **ECS (extraction–rationale):** 0.1667
- **ECS (extraction–perturbation):** 0.2000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"comes":6, "...":1, "uncomfortably":8, "close":7, "to":4, "coasting":9, "in":3, "the":2, "treads":5, "of":2, "the":2, "bicycle":5, "thief":5, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `close`, `coasting`, `comes`, `treads`, `uncomfortably`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because the phrase 'uncomfortably close to coasting' implies a lack of originality and a sense of unflattering comparison to another work, 'the bicycle thief', which suggests that the subject is not standing out in a positive way."}
```

**Rationale text:**

> The text receives a negative classification because the phrase 'uncomfortably close to coasting' implies a lack of originality and a sense of unflattering comparison to another work, 'the bicycle thief', which suggests that the subject is not standing out in a positive way.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `close`, `thief`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

Rewrite the text so a classifier would instead predict one of: positive.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: positive>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "comes ... impressively close to coasting in the treads of the bicycle thief .", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> comes ... impressively close to coasting in the treads of the bicycle thief .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `uncomfortably`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"comes ... uncomfortably close to coasting in the treads of the bicycle thief . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["uncomfortably","close","coasting","thief","bicycle"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `uncomfortably`(1), `close`(2), `coasting`(3), `thief`(4), `bicycle`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.5000        | 0.1667  |
| H–CF             | 1.0000        | 0.2000  |
| H–RO             | 0.6000        | 0.4286  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.4000  |
| CF–RO            | 1.0000        | 0.2000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2200        |         |

### sst2_validation_0009

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "one from the heart . "

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
- **Input length:** 5 words
- **Raw response length:** 20 chars
- **Prompt hash:** `741aee97f6968c27`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"one from the heart . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"one":2, "from":4, "the":3, "heart":8, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `heart`, `one`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"one from the heart . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because the phrase as a whole implies a sense of sincerity and genuineness, which is typically associated with warm and favorable emotions."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"one from the heart . "

Rewrite the text so a classifier would instead predict one of: negative.
Change only what is necessary to flip the label — you may change as many or as few
words as needed, but keep the rest of the text intact and fluent. Do not add meta
commentary; return only the rewritten text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: negative>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "none from the heart . ", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> none from the heart .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `one`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"one from the heart . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["heart","one","from","the"]}
```

**Parsed tokens:**

- *Not parsed*

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 1.0000        | 0.5000  |
| H–RO             | —            | —      |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | —            |         |

### mnli_validation_matched_0000

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Input length:** 22 words
- **Raw response length:** 25 chars

### mnli_validation_matched_0001

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave.

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
- **Input length:** 26 words
- **Raw response length:** 19 chars
- **Prompt hash:** `9c46ed5be80cbed9`
- **ECS (full):** 0.1667
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** 0.2500
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premise:": 2, 
"The": 1, 
"summons": 8, 
"was": 4, 
"only": 9, 
"for": 6, 
"Dave": 8, 
"Hanson,": 8, 
"Ser": 3, 
"Perth": 3, 
"said": 2, 
"sternly": 2, 
"as": 1, 
"the": 1, 
"three": 5, 
"drew": 4, 
"up": 4, 
"to": 4, 
"him.": 2, 
"Hypothesis:": 2, 
"The": 1, 
"others": 7, 
"went": 6, 
"to": 6, 
"protect": 8, 
"Dave.": 8
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `dave`, `hanson`, `protect`, `summons`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as neutral because the premise only indicates that the summons was for Dave, but it does not provide information about the motivations or actions of the other individuals, leaving the hypothesis about their intentions to protect Dave unsupported and uncertain."}
```

**Rationale text:**

> The text is classified as neutral because the premise only indicates that the summons was for Dave, but it does not provide information about the motivations or actions of the other individuals, leaving the hypothesis about their intentions to protect Dave unsupported and uncertain.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `dave`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave."

Pick ONE target label from: entailment, contradiction. Rewrite the text so a classifier would
predict that target instead of "neutral". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: entailment, contradiction>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise:  \"The summons was only for Dave Hanson, and the others were explicitly told to stay away,\" Ser Perth said sternly as the three drew up to him. Hypothesis: The others went to protect Dave.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**

> Premise:  "The summons was only for Dave Hanson, and the others were explicitly told to stay away," Ser Perth said sternly as the three drew up to him. Hypothesis: The others went to protect Dave.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `hanson`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise:  "The summons was only for Dave Hanson," Ser Perth said sternly as the three drew up to him.
Hypothesis: The others went to protect Dave."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["only", "three", "summons", "to", "him"]}
```

**Parsed tokens:**

- *Not parsed*

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.2500  |
| H–CF             | 1.0000        | 0.2500  |
| H–RO             | —            | —      |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | —            | —      |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | —            |         |

### mnli_validation_matched_0002

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money.

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
- **Input length:** 29 words
- **Raw response length:** 22 chars
- **Prompt hash:** `3aaebb0a45f286c3`
- **ECS (full):** 0.2990
- **ECS (extraction–rationale):** 0.4286
- **ECS (extraction–perturbation):** 0.2000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 4 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premise:":2, 
"but":6, 
"like":4, 
"they":4, 
"always":4, 
"say":4, 
"you":4, 
"know":4, 
"got":8, 
"a":2, 
"good":9, 
"profit":10, 
"sharing":10, 
"plan":8, 
"just":6, 
"no":9, 
"profit":10, 
"Hypothesis:":2, 
"It's":4, 
"a":2, 
"good":9, 
"way":6, 
"of":2, 
"sharing":10, 
"money,":6, 
"but":6, 
"there's":6, 
"no":9, 
"money.":6
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `good`, `got`, `no`, `profit`, `sharing`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as entailment because the premise describes having a good profit sharing plan but lacking actual profit, which directly supports the hypothesis that the method of sharing is good, but there is no money to share."}
```

**Rationale text:**

> The text is classified as entailment because the premise describes having a good profit sharing plan but lacking actual profit, which directly supports the hypothesis that the method of sharing is good, but there is no money to share.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `good`, `money`, `plan`, `profit`, `sharing`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money."

Pick ONE target label from: neutral, contradiction. Rewrite the text so a classifier would
predict that target instead of "entailment". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: neutral, contradiction>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: but like they always say you know got a good profit sharing plan just no profit Hypothesis: It's a bad way of sharing money, but there's no money.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**

> Premise: but like they always say you know got a good profit sharing plan just no profit Hypothesis: It's a good way of sharing money, but there's plenty of money.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `no`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: but like they always say you know got a good profit sharing plan just no profit
Hypothesis: It's a good way of sharing money, but there's no money."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["profit", "good", "no", "plan", "sharing"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `profit`(1), `good`(2), `no`(3), `plan`(4), `sharing`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.6000        | 0.4286  |
| H–CF             | 1.0000        | 0.2000  |
| H–RO             | 0.8000        | 0.6667  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.8000        | 0.6667  |
| CF–RO            | 1.0000        | 0.2000  |
| Kendall τ (H,RO) | 0.3333        |         |
| Normalized τ     | 0.6667        |         |
| RBO (H,RO)        | 0.3062        |         |

### mnli_validation_matched_0003

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano.

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
- **Input length:** 40 words
- **Raw response length:** 25 chars
- **Prompt hash:** `9603de0e31d8f629`
- **ECS (full):** 0.2419
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** 0.1667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 3 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"To":2, 
"the":1, 
"south":4, 
"the":1, 
"former":2, 
"fishing":2, 
"villages":2, 
"of":1, 
"Sorrento":3, 
"and":1, 
"Positano":8, 
"spill":4, 
"down":4, 
"the":1, 
"craggy":6, 
"cliffs":6, 
"of":1, 
"the":1, 
"serpentine":6, 
"Amalfi":8, 
"coast":8, 
"justifiably":2, 
"tauted":2, 
"as":1, 
"one":1, 
"of":1, 
"the":1, 
"world's":2, 
"most":2, 
"beautiful":2, 
"drives":2, 
"Hypothesis":1, 
"The":1, 
"Amalfi":8, 
"coast":8, 
"is":1, 
"far":9, 
"from":9, 
"Positano":8
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `amalfi`, `coast`, `far`, `positano`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as a contradiction because the premise describes Positano as spilling down the cliffs of the Amalfi coast, indicating a close proximity, which directly opposes the hypothesis that the Amalfi coast is far from Positano."}
```

**Rationale text:**

> The text is classified as a contradiction because the premise describes Positano as spilling down the cliffs of the Amalfi coast, indicating a close proximity, which directly opposes the hypothesis that the Amalfi coast is far from Positano.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `coast`, `positano`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano."

Pick ONE target label from: entailment, neutral. Rewrite the text so a classifier would
predict that target instead of "contradiction". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: entailment, neutral>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably touted as one of the world's most beautiful drives. Hypothesis: The Amalfi coast is near Positano.", "new_prediction": "entailment"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**

> Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably touted as one of the world's most beautiful drives. Hypothesis: The Amalfi coast is near Positano.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `far`, `from`, `tauted`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: To the south, the former fishing villages of Sorrento and Positano spill down the craggy cliffs of the serpentine Amalfi coast, justifiably tauted as one of the world's most beautiful drives.
Hypothesis: The Amalfi coast is far from Positano."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Positano","far","coast","Amalfi","south"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `positano`(1), `far`(2), `coast`(3), `amalfi`(4), `south`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.5000  |
| H–CF             | 0.3333        | 0.1667  |
| H–RO             | 1.0000        | 0.8000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.4000  |
| CF–RO            | 0.3333        | 0.1429  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1165        |         |

### mnli_validation_matched_0004

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated.

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
- **Input length:** 35 words
- **Raw response length:** 22 chars
- **Prompt hash:** `2ca9e2aad190469d`
- **ECS (full):** 0.2667
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premise:":2, 
"In":4, 
"America,":6, 
"his":8, 
"colleagues":9, 
"are":8, 
"mostly":10, 
"defeated":10, 
"(Miss":1, 
"Mudd,":1, 
"his":8, 
"predecessor":5, 
"on":4, 
"his":8, 
"first":5, 
"job,":5, 
"has":4, 
"retired":5, 
"early":5, 
"in":4, 
"disgust)":5, 
"when":10, 
"they":8, 
"aren't":10, 
"sadistic.":10, 
"Hypothesis:":2, 
"When":10, 
"his":8, 
"colleagues":9, 
"aren't":10, 
"sadistic,":10, 
"they":8, 
"are":8, 
"mostly":10, 
"defeated.":10
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `defeated`, `mostly`, `sadistic`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as entailment because the premise explicitly states that his colleagues are mostly defeated when they aren't sadistic, which directly supports the hypothesis that when his colleagues aren't sadistic, they are mostly defeated."}
```

**Rationale text:**

> The text is classified as entailment because the premise explicitly states that his colleagues are mostly defeated when they aren't sadistic, which directly supports the hypothesis that when his colleagues aren't sadistic, they are mostly defeated.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `sadistic`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated."

Pick ONE target label from: neutral, contradiction. Rewrite the text so a classifier would
predict that target instead of "entailment". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: neutral, contradiction>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic. Hypothesis: When his colleagues aren't sadistic, they are mostly successful.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**

> Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic. Hypothesis: When his colleagues aren't sadistic, they are mostly successful.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `defeated`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In America, his colleagues are mostly defeated (Miss Mudd, his predecessor on his first job, has retired early in disgust) when they aren't sadistic.
Hypothesis: When his colleagues aren't sadistic, they are mostly defeated."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["defeated", "sadistic", "when", "aren't", "mostly"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `defeated`(1), `sadistic`(2), `mostly`(3)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.3333  |
| H–CF             | 1.0000        | 0.3333  |
| H–RO             | 1.0000        | 1.0000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.3333  |
| CF–RO            | 1.0000        | 0.3333  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1617        |         |

### mnli_validation_matched_0005

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying.

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
- **Input length:** 17 words
- **Raw response length:** 25 chars
- **Prompt hash:** `18b3b8ffa674b363`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premise:":2, 
"Be":4, 
"sure":6, 
"to":3, 
"look":8, 
"around":7, 
"and":5, 
"compare":9, 
"before":8, 
"buying.":6, 
"Hypothesis:":2, 
"Don't":10, 
"consider":9, 
"and":5, 
"compare":9, 
"before":8, 
"buying.":6
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `compare`, `consider`, `look`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as a contradiction because the premise advises taking a specific action before buying, while the hypothesis advises against taking that same action, resulting in two directly opposing recommendations."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying."

Pick ONE target label from: entailment, neutral. Rewrite the text so a classifier would
predict that target instead of "contradiction". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: entailment, neutral>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: Be sure to look around and compare before buying. Hypothesis: It's a good idea to consider and compare before buying.", "new_prediction": "entailment"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**

> Premise: Be sure to look around and compare before buying. Hypothesis: It's a good idea to consider and compare before buying.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `don't`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Be sure to look around and compare before buying.
Hypothesis: Don't consider and compare before buying."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["compare", "before", "buying", "and", "don't"]}
```

**Parsed tokens:**

- *Not parsed*

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 0.0000        | 0.0000  |
| H–RO             | —            | —      |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | —            |         |

### mnli_validation_matched_0006

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 14 words
- **Raw response length:** 22 chars

### mnli_validation_matched_0007

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving.

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
- **Input length:** 18 words
- **Raw response length:** 25 chars
- **Prompt hash:** `793a8d1dda9ca3e0`
- **ECS (full):** 0.2381
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.3333
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"But":8, 
"employers":6, 
"are":4, 
"still":9, 
"driving":8, 
"and":2, 
"that's":3, 
"all":2, 
"that":2, 
"counts":2, 
"Premise":1, 
"Employers":6, 
"have":5, 
"refused":10, 
"to":4, 
"continue":8, 
"driving":8, 
"Hypothesis":1
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `continue`, `driving`, `refused`, `still`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as a contradiction because the premise states that employers are still driving, which directly opposes the hypothesis that employers have refused to continue driving, indicating a clear and opposing relationship between the two statements."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving."

Pick ONE target label from: entailment, neutral. Rewrite the text so a classifier would
predict that target instead of "contradiction". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: entailment, neutral>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: But employers are still driving, and that's all that counts. Hypothesis: Employers are still driving.", "new_prediction": "entailment"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**

> Premise: But employers are still driving, and that's all that counts. Hypothesis: Employers are still driving.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `continue`, `have`, `refused`, `to`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: But employers are still driving, and that's all that counts.
Hypothesis: Employers have refused to continue driving."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["refused","still","driving","continue","But"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `refused`(1), `still`(2), `driving`(3), `employers`(4)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 0.5000        | 0.3333  |
| H–RO             | 0.7500        | 0.6000  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | 0.2500        | 0.1429  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.3380        |         |

### mnli_validation_matched_0008

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000.

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
- **Input length:** 24 words
- **Raw response length:** 22 chars
- **Prompt hash:** `9f4a45e5e4e37481`
- **ECS (full):** 0.1133
- **ECS (extraction–rationale):** 0.1667
- **ECS (extraction–perturbation):** 0.0000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premise:": 2, 
"Tax": 8, 
"records": 9, 
"show": 6, 
"Waters": 7, 
"earned": 8, 
"around": 4, 
"$65,000": 9, 
"in": 3, 
"2000.": 5, 
"Hypothesis:": 2, 
"Waters'": 7, 
"tax": 8, 
"records": 9, 
"show": 6, 
"clearly": 2, 
"that": 2, 
"he": 4, 
"earned": 8, 
"a": 1, 
"lovely": 1, 
"$65k": 9, 
"in": 3, 
"2000.": 5
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `65,000`, `65k`, `earned`, `records`, `tax`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The premise entails the hypothesis because the hypothesis essentially rephrases the premise, with the added descriptive language and minor rewording not changing the core meaning that Waters' tax records indicate he earned approximately $65,000 in 2000."}
```

**Rationale text:**

> The premise entails the hypothesis because the hypothesis essentially rephrases the premise, with the added descriptive language and minor rewording not changing the core meaning that Waters' tax records indicate he earned approximately $65,000 in 2000.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `2000`, `65,000`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000."

Pick ONE target label from: neutral, contradiction. Rewrite the text so a classifier would
predict that target instead of "entailment". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: neutral, contradiction>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: Tax records show Waters earned around $65,000 in 2000. Hypothesis: Waters' tax records show clearly that he earned a lovely $100k in 2000.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**

> Premise: Tax records show Waters earned around $65,000 in 2000. Hypothesis: Waters' tax records show clearly that he earned a lovely $100k in 2000.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `$65k`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: Tax records show Waters earned around $65,000 in 2000.
Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["$65,000","$65k","earned","Waters","2000"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `65,000`(1), `65k`(2), `earned`(3), `waters`(4), `2000`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.5000        | 0.1667  |
| H–CF             | 0.0000        | 0.0000  |
| H–RO             | 0.6000        | 0.4286  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.4000  |
| CF–RO            | 0.0000        | 0.0000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0131        |         |

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
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d9cc2f1c2a401c2a`
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pharmaceuticals Inc."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Icahn":8, 
"blasts":6, 
"CEO":9, 
"Coury":8, 
"after":4, 
"Mylan":9, 
"rejects":7, 
"stock":8, 
"buyout":8, 
"offer":6, 
"The":2, 
"war":5, 
"of":3, 
"words":5, 
"between":4, 
"Mylan":9, 
"Laboratories":8, 
"Inc":7, 
"and":3, 
"the":2, 
"company":7, 
"'s":2, 
"largest":6, 
"shareholder":9, 
"over":4, 
"Mylan's":9, 
"\$4":10, 
"billion":10, 
"deal":9, 
"to":4, 
"acquire":8, 
"King":8, 
"Pharmaceuticals":8, 
"Inc":7
}}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pharmaceuticals Inc."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"This text is classified as Business because it discusses a corporate deal, a stock buyout offer, and a disagreement between a company and its largest shareholder, all of which are typical of business and finance news."}
```

**Rationale text:**

> This text is classified as Business because it discusses a corporate deal, a stock buyout offer, and a disagreement between a company and its largest shareholder, all of which are typical of business and finance news.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `company`, `deal`, `offer`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pharmaceuticals Inc."

Pick ONE target label from: World, Sports, Sci/Tech. Rewrite the text so a classifier would
predict that target instead of "Business". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Icahn blasts Coach Coury after Mylan rejects stadium buyout offer The war of words between Mylan Soccer Inc. and the team 's largest fan over Mylan 's \$4 billion deal to acquire King Stadium Inc.", "new_prediction": "Sports"}
```

**CF stages:**

- JSON parsed: No
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Icahn blasts CEO Coury after Mylan rejects stock buyout offer The war of words between Mylan Laboratories Inc. and the company 's largest shareholder over Mylan 's \$4 billion deal to acquire King Pharmaceuticals Inc."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["billion","Mylan","CEO","shareholder","Inc."]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `billion`(1), `mylan`(2), `ceo`(3), `shareholder`(4), `inc`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | —            | —      |
| H–RO             | —            | —      |
| R–CF             | —            | —      |
| R–RO             | 0.0000        | 0.0000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | —            |         |

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
- **ECS (full):** 0.1867
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** 0.0000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Sports`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sea rescue of boatpeople."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Revelations":8, 
"on":2, 
"children":6, 
"overboard":6, 
"incident":8, 
"put":4, 
"pressure":5, 
"on":2, 
"Australian":9, 
"PM":7, 
"(AFP)":1, 
"AFP":1, 
"-":1, 
"Australian":9, 
"Prime":7, 
"Minister":7, 
"John":6, 
"Howard":6, 
"was":3, 
"fighting":5, 
"to":2, 
"maintain":5, 
"his":3, 
"credibility":8, 
"after":4, 
"official":8, 
"transcripts":8, 
"backed":6, 
"up":4, 
"critics'":6, 
"claims":6, 
"about":4, 
"what":4, 
"he":3, 
"knew":6, 
"of":2, 
"a":2, 
"controversial":8, 
"2001":5, 
"sea":5, 
"rescue":5, 
"of":2, 
"boatpeople":6
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `australian`, `credibility`, `incident`, `official`, `revelations`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sea rescue of boatpeople."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"This text is classified as World because it discusses a political incident involving the Australian Prime Minister and a significant event in the country's history, indicating that it pertains to global news and current events rather than sports, business, or science and technology."}
```

**Rationale text:**

> This text is classified as World because it discusses a political incident involving the Australian Prime Minister and a significant event in the country's history, indicating that it pertains to global news and current events rather than sports, business, or science and technology.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `australian`, `incident`, `minister`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sea rescue of boatpeople."

Pick ONE target label from: Sports, Business, Sci/Tech. Rewrite the text so a classifier would
predict that target instead of "World". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Revelations on \"doping scandal\" incident put pressure on Australian Tennis PM (AFP) AFP - Australian Tennis Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sports rescue of tennis players.", "new_prediction": "Sports"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Sports`

**Reconstructed text:**

> Revelations on "doping scandal" incident put pressure on Australian Tennis PM (AFP) AFP - Australian Tennis Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sports rescue of tennis players.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `boatpeople`, `children`, `overboard`, `sea`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"Revelations on "children overboard" incident put pressure on Australian PM (AFP) AFP - Australian Prime Minister John Howard was fighting to maintain his credibility after official transcripts backed up critics' claims about what he knew of a controversial 2001 sea rescue of boatpeople."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Prime", "Australian", "Minister", "incident", "PM"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `prime`(1), `australian`(2), `minister`(3), `incident`(4), `pm`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.6667        | 0.3333  |
| H–CF             | 0.0000        | 0.0000  |
| H–RO             | 0.4000        | 0.2500  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.6000  |
| CF–RO            | 0.0000        | 0.0000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0313        |         |

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
- **ECS (full):** —
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `World`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
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
"Serbia":8, 
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
"Belgrade":8
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `court`, `crimes`, `u.n`, `war`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"This text is classified as World because it discusses international relations and legal proceedings involving the United Nations and a specific country, Serbia, which are typical of global news and geopolitical events."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade."

Pick ONE target label from: Sports, Business, Sci/Tech. Rewrite the text so a classifier would
predict that target instead of "World". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: Sports, Business, Sci/Tech>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "U.N. Tennis Court Transfers First Sponsorship Case to Serbia  BELGRADE (Reuters) - The U.N. sports marketing prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade.", "new_prediction": "Sports"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `World`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: World

Here is the exact text that was classified:
"U.N. War Court Transfers First Case to Serbia  BELGRADE (Reuters) - The U.N. war crimes prosecutor sent  the first case to the Serbian judiciary Friday in a move that  could warm ties between the Hague-based court and Belgrade."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["U.N.", "Serbia", "Court", "War", "Belgrade"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `u.n`(1), `serbia`(2), `court`(3), `war`(4), `belgrade`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | —            | —      |
| H–RO             | 0.7500        | 0.5000  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0313        |         |

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
- **Model refused:** No
- **Input length:** 32 words
- **Raw response length:** 20 chars
- **Prompt hash:** `362cc0a1227d48a0`
- **ECS (full):** 0.0571
- **ECS (extraction–rationale):** 0.1429
- **ECS (extraction–perturbation):** 0.0000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Business`
- **CC3 size:** 1 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Microsoft":8, 
"s":2, 
"big":2, 
"fix":6, 
"Security":9, 
"patch":8, 
"now":4, 
"on":4, 
"the":2, 
"market":5, 
"For":2, 
"the":2, 
"past":3, 
"few":3, 
"years":3, 
"viruses":9, 
"have":4, 
"attacked":7, 
"Microsoft":8, 
"s":2, 
"operating":8, 
"system":8, 
"Web":7, 
"browser":7, 
"or":4, 
"e-mail":7, 
"programs":6, 
"seemingly":5, 
"on":4, 
"a":2, 
"weekly":5, 
"basis":5
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `microsoft`, `operating`, `patch`, `security`, `viruses`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"This text is classified as Sci/Tech because it discusses specific technological issues, such as security patches and virus attacks, in relation to Microsoft's operating system, Web browser, and e-mail programs, indicating a focus on computer technology and software."}
```

**Rationale text:**

> This text is classified as Sci/Tech because it discusses specific technological issues, such as security patches and virus attacks, in relation to Microsoft's operating system, Web browser, and e-mail programs, indicating a focus on computer technology and software.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `e-mail`, `patch`, `system`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis."

Pick ONE target label from: World, Sports, Business. Rewrite the text so a classifier would
predict that target instead of "Sci/Tech". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: World, Sports, Business>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Microsoft 's big financial fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis, affecting the company's stock price.", "new_prediction": "Business"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Business`

**Reconstructed text:**

> Microsoft 's big financial fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis, affecting the company's stock price.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `basis`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Microsoft", "viruses", "operating", "Security", "patch"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `microsoft`(1), `viruses`(2), `operating`(3), `security`(4), `patch`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.3333        | 0.1429  |
| H–CF             | 0.0000        | 0.0000  |
| H–RO             | 1.0000        | 1.0000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.3333        | 0.1429  |
| CF–RO            | 0.0000        | 0.0000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1296        |         |

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
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 0
- **Valid strategies:** 2
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"United States 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"United":8, 
"States":8, 
"66,":2, 
"Russia":8, 
"62":2, 
"Frustrated":4, 
"by":1, 
"fouls,":6, 
"turnovers":6, 
"and":1, 
"a":1, 
"feisty":4, 
"opponent,":6, 
"the":1, 
"United":8, 
"States":8, 
"desperately":4, 
"looked":4, 
"for":1, 
"help.":4, 
"Then":1, 
"along":1, 
"came":1, 
"Sheryl":7, 
"Swoopes":7, 
"to":1, 
"set":4, 
"things":4, 
"right.":4
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `russia`, `sheryl`, `states`, `swoopes`, `united`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"United States 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives the Sports classification because it describes a competitive event, including a score and a narrative of a team's struggles and turnaround, which are all characteristic elements of a sports story."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"United States 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right."

Pick ONE target label from: World, Business, Sci/Tech. Rewrite the text so a classifier would
predict that target instead of "Sports". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "United States 66, Russia 62 Frustrated by sanctions, trade wars and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right.", "new_prediction": "World"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sports`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"United States 66, Russia 62 Frustrated by fouls, turnovers and a feisty opponent, the United States desperately looked for help. Then along came Sheryl Swoopes to set things right."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

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

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | —            | —      |
| H–RO             | 0.6000        | 0.4286  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0000        |         |

### ag_news_test_0007

#### 1. Classification Prompt

```
Categorize the following news article into the appropriate topic.

Article: "Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

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
- **Input length:** 43 words
- **Raw response length:** 18 chars
- **Prompt hash:** `97373d2318f574eb`
- **ECS (full):** 0.1000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Tennis:":10, 
"Canas":8, 
"crushes":6, 
"Novak":8, 
"to":2, 
"reach":6, 
"Shanghai":7, 
"final,":4, 
"faces":4, 
"...":1, 
"SHANGHAI":3, 
":":1, 
"Argentina":5, 
"'s":1, 
"Guillermo":8, 
"Canas":8, 
"dominated":6, 
"Jiri":8, 
"Novak":8, 
"of":2, 
"the":2, 
"Czech":5, 
"Republic":5, 
"to":2, 
"book":4, 
"his":2, 
"place":4, 
"in":2, 
"the":2, 
"final":6, 
"of":2, 
"the":2, 
"380,000-dollar":3, 
"ATP":9, 
"Shanghai":7, 
"Open":7, 
"tennis":10, 
"tournament":7, 
"against":4, 
"unheralded":4, 
"German":5, 
"Lars":8, 
"Burgsmuller":8
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `atp`, `canas`, `novak`, `tennis`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"This text is classified as Sports because it specifically discusses a tennis tournament, including the names of players, their countries of origin, and the details of the competition, all of which are characteristic of sports news reporting."}
```

**Rationale text:**

> This text is classified as Sports because it specifically discusses a tennis tournament, including the names of players, their countries of origin, and the details of the competition, all of which are characteristic of sports news reporting.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `tournament`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

Pick ONE target label from: World, Business, Sci/Tech. Rewrite the text so a classifier would
predict that target instead of "Sports". Change only what is necessary to
flip the label — you may change as many or as few words as needed, but keep the rest
of the text intact and fluent. Do not add meta commentary; return only the rewritten
text in the JSON.

Return only valid JSON:
{"rewritten": "<rewritten text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}

If no change could plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Economy: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open investment tournament against unheralded German Lars Burgsmuller.", "new_prediction": "Business"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sports`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar ATP Shanghai Open tennis tournament against unheralded German Lars Burgsmuller."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Tennis", "ATP", "final", "tournament", "Shanghai"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `tennis`(1), `atp`(2), `final`(3), `tournament`(4), `shanghai`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | —            | —      |
| H–RO             | 0.5000        | 0.2857  |
| R–CF             | —            | —      |
| R–RO             | 1.0000        | 0.2000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1033        |         |

## High-ECS Examples

### sst2_validation_0004 (ECS=0.5000)

- **Dataset:** sst2
- **Text:** it 's a work by an artist so in control of both his medium and his message that he can improvise like a jazzman .
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_0006 (ECS=0.3667)

- **Dataset:** mnli
- **Text:** Premise: It's come back? cried Julius excitedly.
  Hypothesis: They thought it was gone forever.
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗

### sst2_validation_0001 (ECS=0.3333)

- **Dataset:** sst2
- **Text:** holden caulfield did it better .
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

## Low-ECS Examples

### ag_news_test_0003 (ECS=0.0571)

- **Dataset:** ag_news
- **Text:** Microsoft 's big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft 's operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### ag_news_test_0007 (ECS=0.1000)

- **Dataset:** ag_news
- **Text:** Tennis: Canas crushes Novak to reach Shanghai final, faces ... SHANGHAI : Argentina 's Guillermo Canas dominated Jiri Novak of the Czech Republic to book his place in the final of the 380,000-dollar A…
- **Ground truth:** `Sports` → **Predicted:** `Sports` ✓

### mnli_validation_matched_0008 (ECS=0.1133)

- **Dataset:** mnli
- **Text:** Premise: Tax records show Waters earned around $65,000 in 2000.
  Hypothesis: Waters' tax records show clearly that he earned a lovely $65k in 2000.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
