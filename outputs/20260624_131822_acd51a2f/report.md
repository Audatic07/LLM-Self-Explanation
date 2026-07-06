# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-24 13:18:35
- **Duration:** 853.4s (14.2m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 23
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 79194
- **Avg tokens per instance:** 3443

## Per-Dataset Summary

| Dataset | Instances | Accuracy     | Mean ECS | H    | R    | CF  | RO   |
| ------- | --------- | ------------ | -------- | ---- | ---- | --- | ---- |
| sst2    | 10        | 10/10 (100%) | 0.134    | 100% | 60%  | 60% | 90%  |
| mnli    | 10        | 6/10 (60%)   | 0.292    | 100% | 100% | 50% | 80%  |
| ag_news | 3         | 3/3 (100%)   | 0.553    | 100% | 100% | 33% | 100% |

## Sampling Log

| Dataset         | Requested | Sampled | Wrong Pred |
| --------------- | --------- | ------- | ---------- |
| sst2            | 10        | 10      | 0          |
| mnli            | 10        | 10      | 4          |
| ag_news         | 10        | 10      | 0          |
| **Total** | 30        | 30      | 4          |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=8) or medium-length (21–50 words, N=14). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=10). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=5)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy       | Valid / Total | Rate |
| -------------- | ------------- | ---- |
| Highlighting   | 23/23         | 100% |
| Rationale      | 19/23         | 83%  |
| Counterfactual | 12/23         | 52%  |
| Rank Ordering  | 20/23         | 87%  |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).

## Overall Metrics

| Metric                                                 | Value                                                                      |
| ------------------------------------------------------ | -------------------------------------------------------------------------- |
| Mean ECS (all, N=23)                                   | 0.2578                                                                     |
| Mean ECS (extraction–rationale: H,R,RO)               | 0.3478                                                                     |
| Mean ECS (extraction–perturbation: H,CF,RO)           | 0.2626                                                                     |
| Mean ECS (complete cases, N=5)                         | 0.3071                                                                     |
| Complete cases                                         | 5/23 (22%)                                                                 |
| ECS pairs <3                                           | 15 instances                                                               |
| → sst2_validation_000665: 1 pair(s), er=NA, ep=0.0000 |                                                                            |
| → sst2_validation_000657: 1 pair(s), er=NA, ep=0.3333 |                                                                            |
| → sst2_validation_000361: 1 pair(s), er=0.1250, ep=NA |                                                                            |
| → sst2_validation_000394: 1 pair(s), er=NA, ep=0.1429 |                                                                            |
| → sst2_validation_000188: 1 pair(s), er=0.0000, ep=NA |                                                                            |
| → ... and 10 more                                     |                                                                            |
| Std ECS                                                | 0.2129                                                                     |
| Median ECS                                             | 0.2076                                                                     |
| **Mean ECS lift over chance** (ECS − random)    | +0.1674                                                                    |
| Mean ECS random baseline                               | 0.0904                                                                     |
| Mean ECS — correct preds (N=19)                       | 0.2323                                                                     |
| Mean ECS — incorrect preds (N=4)                      | 0.3787                                                                     |
| Introduced-concept rate (R)                            | 0.748                                                                      |
| CF canonical (minimal) validity rate                   | 52%                                                                        |
| CF contrast (free) validity rate                       | 74%                                                                        |
| CF canonical (minimal) minimality (edits/len)          | 0.077                                                                      |
| CF contrast (free) minimality (edits/len)              | 0.120                                                                      |
| Confidence elicitation                                 | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size                                          | 1.35                                                                       |
| Mean CC4 size                                          | 0.87                                                                       |
| % instances with CC3                                   | 60.9%                                                                      |
| % instances with CC4                                   | 47.8%                                                                      |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair   | Overlap Coeff (mean) | Jaccard (mean) |
| ------ | -------------------- | -------------- |
| H–R   | 0.5516               | 0.3478         |
| H–CF  | 0.7222               | 0.2626         |
| H–RO  | 0.8017               | 0.5332         |
| R–CF  | 0.2500               | 0.1354         |
| R–RO  | 0.4365               | 0.2634         |
| CF–RO | 0.6481               | 0.2225         |

### Rank-Based Agreement (H vs RO)

| Metric            | Value  |
| ----------------- | ------ |
| RBO (H,RO)        | 0.1761 |
| Kendall τ (H,RO) | 0.3333 |
| Normalized τ     | 0.6667 |

> Overlap Coefficient is the primary pairwise metric (unlike Jaccard, it is not penalized by smaller salience sets). Jaccard is retained as a secondary reference. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy                         | Parsed       | Valid        |
| -------------------------------- | ------------ | ------------ |
| Highlighting                     | 23/23 (100%) | 23/23 (100%) |
| Rationale                        | 19/23 (83%)  | 19/23 (83%)  |
| Counterfactual (JSON parsed)     | 23/23 (100%) |              |
| Counterfactual (rules compliant) | 22/23 (96%)  |              |
| Counterfactual (flip verified)   | 12/22 (55%)  |              |
| Rank Ordering                    | 20/23 (87%)  | 20/23 (87%)  |
| All 4 valid                      | 5/23         |              |
| 3 valid (CC3 adjusted)           | 18/23        |              |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length             | N  | Mean ECS |
| ------------------ | -- | -------- |
| Short (≤20 words) | 8  | 0.2283   |
| Medium (21–50)    | 14 | 0.2782   |
| Long (>50 words)   | 1  | 0.2076   |

### ECS by Vocabulary Size

| Vocab Bucket                     | N  | Mean ECS |
| -------------------------------- | -- | -------- |
| Normal vocab (>20 unique tokens) | 13 | 0.2963   |
| Short vocab (≤20 unique tokens) | 10 | 0.2076   |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric   | Estimate | 95% CI           |
| -------- | -------- | ---------------- |
| Mean ECS | 0.2578   | [0.1701, 0.3497] |

## Per-Instance Details

### sst2_validation_000665

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

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
- **Input length:** 24 words
- **Raw response length:** 20 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.0000
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"and":2, "if":4, "you":6, "re":2, "not":3, "nearly":5, "moved":8, "to":2, "tears":8, "by":2, "a":1, "couple":5, "of":1, "scenes":7, "you":6, "ve":2, "got":2, "ice":6, "water":6, "in":2, "your":4, "veins":6}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `moved`, `scenes`, `tears`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because the speaker implies that the scenes are emotionally powerful and capable of evoking strong feelings, suggesting that the work has a profound impact on the viewer, which is a complimentary sentiment."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to negative. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: negative

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: negative>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "and if you 're nearly moved to tears by a couple of scenes , you 've got ice water in your veins .", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> and if you 're nearly moved to tears by a couple of scenes , you 've got ice water in your veins .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `not`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["tears","scenes","veins","ice","moved"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `tears`(1), `scenes`(2), `veins`(3), `ice`(4), `moved`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 0.0000        | 0.0000  |
| H–RO             | 0.6667        | 0.4000  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | 0.0000        | 0.0000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1748        |         |

### sst2_validation_000657

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

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
- **Input length:** 13 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b68aba988a2aa373`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.3333
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
"expect the same-old , lame-old slasher nonsense , just with different scenery . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"expect":6, "the":2, "same-old":8, "lame-old":9, "slasher":7, "nonsense":8, "just":3, "with":2, "different":4, "scenery":4, "(":1, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `lame-old`, `nonsense`, `same-old`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"expect the same-old , lame-old slasher nonsense , just with different scenery . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because it expresses a dismissive and unenthusiastic tone, implying that the subject is unoriginal and lacking in substance, with the use of phrases that convey a sense of monotony and disappointment."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"expect the same-old , lame-old slasher nonsense , just with different scenery . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "expect the same-old , great slasher nonsense , just with different scenery . ", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> expect the same-old , great slasher nonsense , just with different scenery .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `lame-old`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"expect the same-old , lame-old slasher nonsense , just with different scenery . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["nonsense", "lame-old", "same-old", "slasher", "lame"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `nonsense`(1), `lame-old`(2), `same-old`(3), `slasher`(4), `lame`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 1.0000        | 0.3333  |
| H–RO             | 1.0000        | 1.0000  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | 1.0000        | 0.3333  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2200        |         |

### sst2_validation_000361

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

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
- **Input length:** 21 words
- **Raw response length:** 20 chars
- **Prompt hash:** `53ae850b6f80a8dd`
- **ECS (full):** 0.2500
- **ECS (extraction–rationale):** 0.1250
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
"a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"a":2, "very":8, "long":9, "movie":6, "dull":10, "in":4, "stretches":8, "with":3, "entirely":8, "too":9, "much":8, "focus":5, "on":4, "meal":6, "preparation":6, "and":4, "igloo":6, "construction":6, "":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `dull`, `long`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because it describes the movie as lengthy and dull, and also criticizes its focus on seemingly mundane and irrelevant details, such as meal preparation and igloo construction, which suggests that the reviewer found the film to be unengaging and poorly paced."}
```

**Rationale text:**

> The text receives a negative classification because it describes the movie as lengthy and dull, and also criticizes its focus on seemingly mundane and irrelevant details, such as meal preparation and igloo construction, which suggests that the reviewer found the film to be unengaging and poorly paced.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `construction`, `dull`, `focus`, `igloo`, `meal`, `movie`, `preparation`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "a very long movie , engaging in stretches , with entirely too much focus on meal preparation and igloo construction . ", "new_prediction": "positive"}
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
"a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["dull", "long", "too", "movie", "construction"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `dull`(1), `long`(2), `movie`(3), `construction`(4)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.5000        | 0.1250  |
| H–CF             | —            | —      |
| H–RO             | 1.0000        | 0.5000  |
| R–CF             | —            | —      |
| R–RO             | 0.7500        | 0.3750  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2804        |         |

### sst2_validation_000394

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

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
- **Input length:** 41 words
- **Raw response length:** 20 chars
- **Prompt hash:** `67a8763d00facc6b`
- **ECS (full):** 0.1714
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.1429
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"whether":2, "writer-director":4, "anne":3, "fontaine":3, "'s":1, "film":6, "is":2, "a":1, "ghost":5, "story":5, "an":1, "account":5, "of":1, "a":1, "nervous":5, "breakdown":5, "a":1, "trip":5, "down":2, "memory":5, "lane":5, "all":2, "three":2, "or":2, "none":2, "of":1, "the":1, "above":2, "it":2, "is":2, "as":3, "seductive":8, "as":3, "it":2, "is":2, "haunting":9}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `account`, `film`, `ghost`, `haunting`, `nervous`, `seductive`, `story`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because the description of the film as being "as seductive as it is haunting" implies a captivating and emotionally resonant quality, suggesting that the speaker holds the film in high regard."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to negative. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: negative

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: negative>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as repulsive as it is haunting . ", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as repulsive as it is haunting .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `seductive`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["seductive", "haunting", "ghost", "nervous", "memory"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `seductive`(1), `haunting`(2), `ghost`(3), `nervous`(4), `memory`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 1.0000        | 0.1429  |
| H–RO             | 0.8000        | 0.5000  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | 1.0000        | 0.2000  |
| Kendall τ (H,RO) | 0.6667        |         |
| Normalized τ     | 0.8333        |         |
| RBO (H,RO)        | 0.2979        |         |

### sst2_validation_000228

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

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
- **Prompt hash:** `121db9f475afa812`
- **ECS (full):** 0.0833
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.2500
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it provides an honest look at a community striving to anchor itself in new grounds . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"it":2, "provides":6, "an":1, "honest":8, "look":4, "at":1, "a":1, "community":7, "striving":9, "to":1, "anchor":8, "itself":3, "in":1, "new":5, "grounds":5, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `anchor`, `honest`, `striving`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it provides an honest look at a community striving to anchor itself in new grounds . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because it describes the community's efforts in a neutral yet supportive light, framing their struggles as a noble endeavor to establish themselves, which implies a sense of admiration and appreciation for their resilience."}
```

**Rationale text:**

> The text receives a positive classification because it describes the community's efforts in a neutral yet supportive light, framing their struggles as a noble endeavor to establish themselves, which implies a sense of admiration and appreciation for their resilience.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `community`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it provides an honest look at a community striving to anchor itself in new grounds . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to negative. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: negative

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: negative>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "it provides a dishonest look at a community striving to anchor itself in new grounds . ", "new_prediction": "negative"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**

> it provides a dishonest look at a community striving to anchor itself in new grounds .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `an`, `honest`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"it provides an honest look at a community striving to anchor itself in new grounds . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["honest", "community", "it", "an", "itself"]}
```

**Parsed tokens:**

- *Not parsed*

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | 0.5000        | 0.2500  |
| H–RO             | —            | —      |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | —            | —      |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | —            |         |

### sst2_validation_000188

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

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
- **Input length:** 18 words
- **Raw response length:** 20 chars
- **Prompt hash:** `6c16dd54d427ba05`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"a":2, "misogynistic":10, "piece":6, "of":1, "filth":9, "that":1, "attempts":4, "to":1, "pass":4, "itself":2, "off":2, "as":2, "hip":3, "young":3, "adult":3, "entertainment":5, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `filth`, `misogynistic`, `piece`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because it uses strongly derogatory language to describe the subject, indicating a intense dislike and disapproval of its perceived attitude towards women and its attempt to masquerade as something appealing to a young audience."}
```

**Rationale text:**

> The text receives a negative classification because it uses strongly derogatory language to describe the subject, indicating a intense dislike and disapproval of its perceived attitude towards women and its attempt to masquerade as something appealing to a young audience.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `young`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "a feminist piece of filth that attempts to pass itself off as hip , young adult entertainment . ", "new_prediction": "positive"}
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
"a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["filth","misogynistic","entertainment","attempts","misogynistic"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `filth`(1), `misogynistic`(2), `entertainment`(3), `attempts`(4)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | —            | —      |
| H–RO             | 0.6667        | 0.5000  |
| R–CF             | —            | —      |
| R–RO             | 0.0000        | 0.0000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1804        |         |

### sst2_validation_000513

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

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
- **Input length:** 31 words
- **Raw response length:** 20 chars
- **Prompt hash:** `66ffc0207e802d03`
- **ECS (full):** 0.1833
- **ECS (extraction–rationale):** —
- **ECS (extraction–perturbation):** 0.1667
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
"care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"care":6, "deftly":4, "captures":5, "the":2, "wonder":8, "and":2, "menace":8, "of":2, "growing":7, "up":3, "but":9, "he":4, "never":10, "really":8, "embraces":9, "the":2, "joy":7, "of":2, "fuhrman's":5, "destructive":8, "escapism":6, "or":2, "the":2, "grace-in-rebellion":8, "found":5, "by":3, "his":4, "characters":6, "":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `embraces`, `menace`, `never`, `really`, `wonder`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because although it acknowledges a positive aspect of the subject's work, it immediately undermines this praise by stating that the subject fails to fully embrace the more uplifting and redeeming qualities of the material, ultimately focusing on what is lacking."}
```

**Parsed tokens:**

- *Not parsed*

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "care deftly captures the wonder and menace of growing up , and he always really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . ", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> care deftly captures the wonder and menace of growing up , and he always really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `but`, `never`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["but","never","menace","deftly","escapism"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `never`(1), `menace`(2), `deftly`(3), `escapism`(4)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | —            | —      |
| H–CF             | 0.5000        | 0.1667  |
| H–RO             | 0.5000        | 0.2857  |
| R–CF             | —            | —      |
| R–RO             | —            | —      |
| CF–RO            | 0.5000        | 0.2000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2362        |         |

### sst2_validation_000010

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

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
- **Prompt hash:** `d9ae1018167dba5e`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `positive`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"the":2, "mesmerizing":9, "performances":8, "of":1, "the":2, "leads":6, "keep":4, "the":2, "film":5, "grounded":7, "and":3, "keep":4, "the":2, "audience":6, "riveted":8, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `mesmerizing`, `performances`, `riveted`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a positive classification because it describes the performances of the leads as having a powerful and captivating effect on both the film and the audience, indicating a strong appreciation for the actors' work."}
```

**Rationale text:**

> The text receives a positive classification because it describes the performances of the leads as having a powerful and captivating effect on both the film and the audience, indicating a strong appreciation for the actors' work.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `audience`, `film`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: positive

Here is the exact text that was classified:
"the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to negative. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: negative

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: negative>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "the underwhelming performances of the leads keep the film grounded and keep the audience riveted . ", "new_prediction": "negative"}
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
"the mesmerizing performances of the leads keep the film grounded and keep the audience riveted . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["mesmerizing","riveted","grounded","performances","leads"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `mesmerizing`(1), `riveted`(2), `grounded`(3), `performances`(4), `leads`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | —            | —      |
| H–RO             | 0.6667        | 0.5000  |
| R–CF             | —            | —      |
| R–RO             | 0.0000        | 0.0000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2930        |         |

### sst2_validation_000529

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

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
- **Input length:** 27 words
- **Raw response length:** 20 chars
- **Prompt hash:** `b04c96a0a49e1956`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"for":2, 
"close":3, 
"to":2, 
"two":3, 
"hours":4, 
"the":1, 
"audience":6, 
"is":2, 
"forced":8, 
"to":2, 
"endure":9, 
"three":3, 
"terminally":10, 
"depressed":10, 
"mostly":5, 
"inarticulate":9, 
"hyper":8, 
"dysfunctional":10, 
"families":7, 
"for":2, 
"the":1, 
"price":4, 
"of":2, 
"one":3
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `depressed`, `dysfunctional`, `endure`, `inarticulate`, `terminally`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because it describes the audience's experience using phrases that convey a sense of imposition and suffering, implying that the subject matter is unpleasant and potentially distressing to watch."}
```

**Rationale text:**

> The text receives a negative classification because it describes the audience's experience using phrases that convey a sense of imposition and suffering, implying that the subject matter is unpleasant and potentially distressing to watch.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `audience`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "for close to two hours the audience is treated to three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . ", "new_prediction": "positive"}
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
"for close to two hours the audience is forced to endure three terminally depressed , mostly inarticulate , hyper dysfunctional families for the price of one . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["depressed", "forced", "dysfunctional", "inarticulate", "endure"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `depressed`(1), `forced`(2), `dysfunctional`(3), `inarticulate`(4), `endure`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | —            | —      |
| H–RO             | 0.8000        | 0.6667  |
| R–CF             | —            | —      |
| R–RO             | 0.0000        | 0.0000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | 0.6667        |         |
| Normalized τ     | 0.8333        |         |
| RBO (H,RO)        | 0.1879        |         |

### sst2_validation_000007

#### 1. Classification Prompt

```
Analyze the sentiment expressed in the following text.

Text: "or doing last year 's taxes with your ex-wife . "

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
- **Input length:** 10 words
- **Raw response length:** 20 chars
- **Prompt hash:** `bed5ce4a26311b72`
- **ECS (full):** 0.3233
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** 0.5000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"or doing last year 's taxes with your ex-wife . "

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"or":2, "doing":4, "last":3, "year":3, "s":1, "taxes":6, "with":4, "your":5, "ex-wife":10, ".":1}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `ex-wife`, `taxes`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"or doing last year 's taxes with your ex-wife . "

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a negative classification because the scenario it presents, doing taxes with an ex-wife, implies a potentially awkward, stressful, or uncomfortable situation, which is typically associated with negative emotions or experiences."}
```

**Rationale text:**

> The text receives a negative classification because the scenario it presents, doing taxes with an ex-wife, implies a potentially awkward, stressful, or uncomfortable situation, which is typically associated with negative emotions or experiences.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `ex`, `ex-wife`, `wife`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"or doing last year 's taxes with your ex-wife . "

Rewrite the text above with MINIMAL changes to flip the classifier's output to positive. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: positive

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: positive>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "or doing last year 's taxes with your wife . ", "new_prediction": "positive"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**

> or doing last year 's taxes with your wife .

**Parsed tokens:**

- Status: **Valid**
- Tokens: `ex-wife`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: negative

Here is the exact text that was classified:
"or doing last year 's taxes with your ex-wife . "

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["ex-wife","taxes","last","year's","or"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `ex-wife`(1), `taxes`(2), `last`(3)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.5000        | 0.2500  |
| H–CF             | 1.0000        | 0.5000  |
| H–RO             | 1.0000        | 0.6667  |
| R–CF             | 1.0000        | 0.3333  |
| R–RO             | 0.3333        | 0.2000  |
| CF–RO            | 1.0000        | 0.3333  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2440        |         |

### mnli_validation_matched_007919

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 16 words
- **Raw response length:** 22 chars

### mnli_validation_matched_008565

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City.

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
- **Input length:** 32 words
- **Raw response length:** 22 chars
- **Prompt hash:** `f71b2f7bec2f3b88`
- **ECS (full):** 0.3600
- **ECS (extraction–rationale):** 0.7500
- **ECS (extraction–perturbation):** 0.2500
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
"Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premeise:": 1, 
"In": 2, 
"1099,": 4, 
"under": 3, 
"their": 3, 
"leaders": 6, 
"Godfrey": 5, 
"de": 5, 
"Bouillon": 5, 
"and": 3, 
"Tancred,": 5, 
"the": 8, 
"Crusaders": 9, 
"captured": 10, 
"the": 8, 
"Holy": 8, 
"City": 8, 
"for": 4, 
"Christendom": 6, 
"by": 4, 
"slaughtering": 4, 
"both": 4, 
"Muslims": 4, 
"and": 3, 
"Jews.':": 4, 
"Hypothesis:": 1, 
"The": 8, 
"Crusaders": 9, 
"captured": 10, 
"the": 8, 
"Holy": 8, 
"City.": 8
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `captured`, `city`, `crusaders`, `holy`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as entailment because the premise explicitly states that the Crusaders captured the Holy City, which directly supports and confirms the hypothesis that they did so, making the hypothesis a logical and unavoidable consequence of the premise."}
```

**Rationale text:**

> The text is classified as entailment because the premise explicitly states that the Crusaders captured the Holy City, which directly supports and confirms the hypothesis that they did so, making the hypothesis a logical and unavoidable consequence of the premise.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `city`, `crusaders`, `holy`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

The input has a Premise and a Hypothesis. Rewrite ONLY the Hypothesis, changing as few words as possible, so the relationship is classified as neutral, contradiction instead of "entailment". Keep the Premise and the "Premise:"/"Hypothesis:" structure identical, and change as little of the Hypothesis as you can.

Return the FULL text (the unchanged Premise and the minimally edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with a minimally edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews. Hypothesis: The Crusaders did not capture the Holy City.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**

> Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews. Hypothesis: The Crusaders did not capture the Holy City.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `captured`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Crusaders","captured","City","Holy","Godfrey"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `crusaders`(1), `captured`(2), `city`(3), `holy`(4), `godfrey`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.7500  |
| H–CF             | 1.0000        | 0.2500  |
| H–RO             | 1.0000        | 0.8000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 1.0000        | 0.6000  |
| CF–RO            | 1.0000        | 0.2000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1132        |         |

### mnli_validation_matched_009319

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 40 words
- **Raw response length:** 22 chars

### mnli_validation_matched_007354

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings.

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
- **Input length:** 25 words
- **Raw response length:** 22 chars
- **Prompt hash:** `d03a6bac45bd33be`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"Premise:":1, "we":8, "only":9, "have":8, "to":6, "get":8, "up":8, "for":6, "you":4, "know":4, "for":6, "the":6, "daytime":10, "feedings":10, "Hypothesis:":1, "We":8, "only":9, "have":8, "to":6, "get":8, "up":8, "for":6, "the":6, "daytime":10, "feedings":10}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `daytime`, `feedings`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as entailment because the premise and hypothesis convey the same meaning, with the premise's informal phrase 'you know' being the only difference, which does not affect the overall logical relationship between the two statements."}
```

**Rationale text:**

> The text is classified as entailment because the premise and hypothesis convey the same meaning, with the premise's informal phrase 'you know' being the only difference, which does not affect the overall logical relationship between the two statements.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `know`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

The input has a Premise and a Hypothesis. Rewrite ONLY the Hypothesis, changing as few words as possible, so the relationship is classified as neutral, contradiction instead of "entailment". Keep the Premise and the "Premise:"/"Hypothesis:" structure identical, and change as little of the Hypothesis as you can.

Return the FULL text (the unchanged Premise and the minimally edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with a minimally edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: we only have to get up for you know for the daytime feedings\nHypothesis: We don't only have to get up for the daytime feedings.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: No
- Flip verified: No

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["get", "up", "for", "daytime", "feedings"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `get`(1), `daytime`(2), `feedings`(3)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.0000        | 0.0000  |
| H–CF             | —            | —      |
| H–RO             | 1.0000        | 0.6667  |
| R–CF             | —            | —      |
| R–RO             | 0.0000        | 0.0000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1617        |         |

### mnli_validation_matched_007556

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units.

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
- **Input length:** 43 words
- **Raw response length:** 22 chars
- **Prompt hash:** `b8619d83a5f459e3`
- **ECS (full):** 0.1409
- **ECS (extraction–rationale):** 0.1818
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `entailment`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premeise:": 1, 
"If": 8, 
"necessary": 6, 
"to": 4, 
"meeting": 6, 
"the": 2, 
"restrictions": 8, 
"imposed": 6, 
"in": 4, 
"the": 2, 
"preceding": 6, 
"sentence,": 4, 
"the": 2, 
"Administrator": 8, 
"shall": 6, 
"reduce,": 9, 
"pro": 5, 
"rata,": 5, 
"the": 2, 
"basic": 7, 
"Phase": 7, 
"II": 7, 
"allowance": 9, 
"allocations": 9, 
"for": 4, 
"each": 6, 
"unit": 7, 
"subject": 6, 
"to": 4, 
"the": 2, 
"requirements": 8, 
"of": 4, 
"section": 8, 
"414.": 9, 
"Hypothesis:": 1, 
"Section": 8, 
"414": 9, 
"helps": 7, 
"balance": 8, 
"allowance": 9, 
"allocations": 9, 
"for": 4, 
"units.": 7
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `414`, `administrator`, `allocations`, `allowance`, `reduce`, `requirements`, `restrictions`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as entailment because the premise describes a specific action taken by the Administrator to adjust allowance allocations for units subject to section 414, which directly supports the hypothesis that section 414 plays a role in balancing these allocations."}
```

**Rationale text:**

> The text is classified as entailment because the premise describes a specific action taken by the Administrator to adjust allowance allocations for units subject to section 414, which directly supports the hypothesis that section 414 plays a role in balancing these allocations.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `administrator`, `allowance`, `balance`, `section`, `subject`, `unit`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

The input has a Premise and a Hypothesis. Rewrite ONLY the Hypothesis, changing as few words as possible, so the relationship is classified as neutral, contradiction instead of "entailment". Keep the Premise and the "Premise:"/"Hypothesis:" structure identical, and change as little of the Hypothesis as you can.

Return the FULL text (the unchanged Premise and the minimally edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with a minimally edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414. Hypothesis: Section 414 hinders balance of allowance allocations for units.", "new_prediction": "contradiction"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `entailment`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: entailment

Here is the exact text that was classified:
"Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["necessary", "reduce", "allocations", "section", "requirements"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `necessary`(1), `reduce`(2), `allocations`(3), `section`(4), `requirements`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.3333        | 0.1818  |
| H–CF             | —            | —      |
| H–RO             | 0.6000        | 0.3333  |
| R–CF             | —            | —      |
| R–RO             | 0.2000        | 0.1000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0913        |         |

### mnli_validation_matched_006801

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers.

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
- **Prompt hash:** `a23647bceb96e5d0`
- **ECS (full):** 0.1757
- **ECS (extraction–rationale):** 0.1429
- **ECS (extraction–perturbation):** 0.2857
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premise:": 2, 
"Favorite": 4, 
"items": 6, 
"that": 3, 
"will": 3, 
"help": 4, 
"preserve": 5, 
"your": 2, 
"memories": 5, 
"of": 2, 
"the": 2, 
"rugged": 4, 
"Lakeland": 4, 
"countryside": 4, 
"are": 3, 
"clothing": 6, 
"or": 2, 
"blankets": 6, 
"made": 4, 
"from": 2, 
"the": 2, 
"local": 4, 
"Herdwick": 6, 
"wool,": 6, 
"coasters": 6, 
"of": 2, 
"polished": 4, 
"slate,": 6, 
"or": 2, 
"walking": 6, 
"sticks": 6, 
"with": 2, 
"ram's-horn": 6, 
"handles.": 6, 
"Hypothesis:": 2, 
"They": 8, 
"don't": 9, 
"sell": 9, 
"any": 8, 
"souveineers.": 10
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `any`, `blankets`, `clothing`, `items`, `sell`, `souveineers`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The premise explicitly mentions specific items that can be purchased to preserve memories, which directly contradicts the hypothesis that they don't sell any souvenirs, indicating a clear contradiction between the two statements."}
```

**Rationale text:**

> The premise explicitly mentions specific items that can be purchased to preserve memories, which directly contradicts the hypothesis that they don't sell any souvenirs, indicating a clear contradiction between the two statements.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `preserve`, `sell`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

The input has a Premise and a Hypothesis. Rewrite ONLY the Hypothesis, changing as few words as possible, so the relationship is classified as entailment, neutral instead of "contradiction". Keep the Premise and the "Premise:"/"Hypothesis:" structure identical, and change as little of the Hypothesis as you can.

Return the FULL text (the unchanged Premise and the minimally edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with a minimally edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles. Hypothesis: They might sell some souvenirs.", "new_prediction": "neutral"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**

> Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles. Hypothesis: They might sell some souvenirs.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `any`, `don't`, `souveineers`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["are","sell","souveineers","items","don't"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `sell`(1), `souveineers`(2), `items`(3)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.5000        | 0.1429  |
| H–CF             | 0.6667        | 0.2857  |
| H–RO             | 1.0000        | 0.5000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.5000        | 0.2500  |
| CF–RO            | 0.3333        | 0.2000  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1052        |         |

### mnli_validation_matched_005549

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier.

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
- **Input length:** 38 words
- **Raw response length:** 19 chars
- **Prompt hash:** `573b8c907f1848b8`
- **ECS (full):** 0.5253
- **ECS (extraction–rationale):** 0.7778
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Premeise":1, 
"The":1, 
"Santa":2, 
"Monica":2, 
"Pier":6, 
"is":1, 
"the":1, 
"coastal":4, 
"setting":4, 
"for":1, 
"the":1, 
"Twilight":8, 
"Dance":8, 
"Series":8, 
"a":1, 
"selection":3, 
"of":1, 
"free":3, 
"summer":3, 
"concerts":3, 
"arranged":2, 
"each":2, 
"year":2, 
"Hypothesis":1, 
"The":1, 
"Twilight":8, 
"Dance":8, 
"Series":8, 
"also":2, 
"hosts":2, 
"events":2, 
"directly":2, 
"on":2, 
"the":1, 
"beach":4, 
"near":4, 
"the":1, 
"pier":6
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `beach`, `coastal`, `dance`, `pier`, `series`, `setting`, `twilight`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as neutral because the premise only mentions that the Santa Monica Pier is the coastal setting for the Twilight Dance Series, but it does not provide any information about the specific location of the events, such as whether they are held on the pier itself or on the beach near the pier, which is what the hypothesis is claiming."}
```

**Rationale text:**

> The text is classified as neutral because the premise only mentions that the Santa Monica Pier is the coastal setting for the Twilight Dance Series, but it does not provide any information about the specific location of the events, such as whether they are held on the pier itself or on the beach near the pier, which is what the hypothesis is claiming.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `beach`, `coastal`, `dance`, `monica`, `pier`, `santa`, `series`, `setting`, `twilight`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

The input has a Premise and a Hypothesis. Rewrite ONLY the Hypothesis, changing as few words as possible, so the relationship is classified as entailment, contradiction instead of "neutral". Keep the Premise and the "Premise:"/"Hypothesis:" structure identical, and change as little of the Hypothesis as you can.

Return the FULL text (the unchanged Premise and the minimally edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with a minimally edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year. Hypothesis: The Twilight Dance Series only hosts events on the Santa Monica Pier.", "new_prediction": "entailment"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `neutral`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: neutral

Here is the exact text that was classified:
"Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["pier", "Series", "beach", "near", "also"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `pier`(1), `series`(2), `beach`(3), `near`(4), `also`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.7778  |
| H–CF             | —            | —      |
| H–RO             | 0.6000        | 0.3333  |
| R–CF             | —            | —      |
| R–RO             | 0.6000        | 0.2727  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0425        |         |

### mnli_validation_matched_006492

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `contradiction` ✗
- **Input length:** 15 words
- **Raw response length:** 25 chars

### mnli_validation_matched_009361

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 20 words
- **Raw response length:** 22 chars

### mnli_validation_matched_004122

#### 1. Classification Prompt

```
Determine the logical relationship between the premise and the hypothesis.

Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point

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
- **Input length:** 70 words
- **Raw response length:** 25 chars
- **Prompt hash:** `2e0f12cf98d38bf9`
- **ECS (full):** 0.2076
- **ECS (extraction–rationale):** 0.4545
- **ECS (extraction–perturbation):** 0.2222
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 2 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"oh":2, 
"you":2, 
"went":3, 
"to":2, 
"the":2, 
"dollar":8, 
"movie":9, 
"yeah":1, 
"yeah":1, 
"they":6, 
"show":8, 
"up":4, 
"at":2, 
"the":2, 
"dollar":8, 
"movie":9, 
"right":5, 
"after":5, 
"they":6, 
"get":4, 
"come":4, 
"out":4, 
"you":2, 
"know":3, 
"they're":6, 
"usually":4, 
"not":4, 
"not":4, 
"that":3, 
"great":5, 
"or":3, 
"didn't":5, 
"do":5, 
"that":3, 
"great":5, 
"anyway":2, 
"let":1, 
"me":1, 
"see":1, 
"let":1, 
"me":1, 
"see":1, 
"another":3, 
"movie":6, 
"I":2, 
"watched":3, 
"uh":1, 
"I":2, 
"want":3, 
"to":2, 
"see":3, 
"is":2, 
"uh":1, 
"that":3, 
"new":4, 
"one":3, 
"uh":1, 
"Hypothesis:":1, 
"they're":6, 
"never":9, 
"shown":8, 
"at":2, 
"the":2, 
"dollar":8, 
"movie":9, 
"theater":7, 
"at":2, 
"any":5, 
"point":5
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `any`, `dollar`, `great`, `movie`, `never`, `right`, `show`, `shown`, `theater`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as a contradiction because the premise states that movies are shown at the dollar movie right after they come out, which directly opposes the hypothesis that they are never shown at the dollar movie theater at any point."}
```

**Rationale text:**

> The text is classified as a contradiction because the premise states that movies are shown at the dollar movie right after they come out, which directly opposes the hypothesis that they are never shown at the dollar movie theater at any point.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `come`, `dollar`, `movie`, `point`, `right`, `show`, `theater`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

The input has a Premise and a Hypothesis. Rewrite ONLY the Hypothesis, changing as few words as possible, so the relationship is classified as entailment, neutral instead of "contradiction". Keep the Premise and the "Premise:"/"Hypothesis:" structure identical, and change as little of the Hypothesis as you can.

Return the FULL text (the unchanged Premise and the minimally edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with a minimally edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh\nHypothesis: they're usually shown at the dollar movie theater at some point", "new_prediction": "neutral"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**

> Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
> Hypothesis: they're usually shown at the dollar movie theater at some point

**Parsed tokens:**

- Status: **Valid**
- Tokens: `any`, `never`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: contradiction

Here is the exact text that was classified:
"Premise: oh you went to the dollar movie yeah yeah they show up at the dollar movie right after they get come out you know they're usually not not that great or didn't do that great anyway let me see let me see another movie i watched uh i want to see is uh that new one uh
Hypothesis: they're never shown at the dollar movie theater at any point"

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["yeah", "they", "never", "show", "at"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `yeah`(1), `never`(2), `show`(3)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 0.7143        | 0.4545  |
| H–CF             | 1.0000        | 0.2222  |
| H–RO             | 0.6667        | 0.2000  |
| R–CF             | 0.0000        | 0.0000  |
| R–RO             | 0.3333        | 0.1111  |
| CF–RO            | 0.5000        | 0.2500  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.2184        |         |

### ag_news_test_004983

#### 1. Classification Prompt

```
Categorize the following news article into the appropriate topic.

Article: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

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
- **Input length:** 35 words
- **Raw response length:** 20 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.4690
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Business`
- **CC3 size:** 4 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Nokia":8, 
"announces":6, 
"Near":9, 
"Field":9, 
"Communication":10, 
"products":5, 
"With":2, 
"the":1, 
"Nokia":8, 
"NFC":10, 
"(Near":4, 
"Field":9, 
"Communication)":10, 
"shell":7, 
"on":2, 
"their":2, 
"phone":8, 
"consumers":4, 
"will":3, 
"be":2, 
"able":3, 
"to":2, 
"access":6, 
"a":1, 
"variety":5, 
"of":2, 
"services":6, 
"and":2, 
"exchange":6, 
"information":7, 
"with":2, 
"a":1, 
"simple":4, 
"touch":7, 
"gesture":5
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `nfc`, `nokia`, `phone`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text receives a Sci/Tech classification because it discusses a specific technological innovation, namely Near Field Communication products, and explains its application and functionality in a consumer electronics context."}
```

**Rationale text:**

> The text receives a Sci/Tech classification because it discusses a specific technological innovation, namely Near Field Communication products, and explains its application and functionality in a consumer electronics context.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `communication`, `field`, `near`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Rewrite the text above with MINIMAL changes to flip the classifier's output to World, Sports, Business. Change as few words as possible — ideally 1-3 words. Keep the rest identical.

For news articles: replace a topic-defining word (like a sports team name, company name, country name, or technical term) with a word from a different category.

Rules:
- Change as few words as possible
- The rewritten text must be a minimal variation of the original
- The label must change to one of: World, Sports, Business

Return only valid JSON:
{"rewritten": "<minimally changed text>", "new_prediction": "<one of: World, Sports, Business>"}

If no minimal change can plausibly flip the label, return:
{"rewritten": null, "new_prediction": null}
```

**Response:**

```
{"rewritten": "Nokia announces Financial products With the Nokia Financial (Finance) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "Business"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Business`

**Reconstructed text:**

> Nokia announces Financial products With the Nokia Financial (Finance) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `nfc`

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: Sci/Tech

Here is the exact text that was classified:
"Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["NFC", "Communication", "phone", "products", "services"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `nfc`(1), `communication`(2), `phone`(3), `products`(4), `services`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.5000  |
| H–CF             | 1.0000        | 0.6667  |
| H–RO             | 0.6000        | 0.3750  |
| R–CF             | 1.0000        | 0.7500  |
| R–RO             | 0.3333        | 0.1429  |
| CF–RO            | 0.5000        | 0.2857  |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.0076        |         |

### ag_news_test_001223

#### 1. Classification Prompt

```
Categorize the following news article into the appropriate topic.

Article: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

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
- **Input length:** 36 words
- **Raw response length:** 20 chars
- **Prompt hash:** `9d013e566f583003`
- **ECS (full):** 0.8571
- **ECS (extraction–rationale):** 0.7143
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 5 | **CC4 size:** 5

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{
"Nikkei":8, 
"hits":4, 
"5-week":6, 
"closing":6, 
"high":6, 
"on":2, 
"upbeat":7, 
"capital":9, 
"spending":9, 
"data":5, 
"TOKYO":3, 
"Japan":5, 
"'s":1, 
"benchmark":8, 
"Nikkei":8, 
"stock":9, 
"index":8, 
"hit":4, 
"a":1, 
"five-week":6, 
"closing":6, 
"high":6, 
"Monday":3, 
"on":2, 
"upbeat":7, 
"capital":9, 
"spending":9, 
"figures":7, 
"for":2, 
"the":1, 
"April-June":6, 
"quarter":6, 
"by":2, 
"Japanese":5, 
"companies":8
}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `benchmark`, `capital`, `companies`, `index`, `nikkei`, `spending`, `stock`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"This text is classified as Business because it discusses financial market performance, specifically the Nikkei stock index and capital spending data, which are key indicators of economic activity and are typically of interest to investors and business professionals."}
```

**Rationale text:**

> This text is classified as Business because it discusses financial market performance, specifically the Nikkei stock index and capital spending data, which are key indicators of economic activity and are typically of interest to investors and business professionals.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `capital`, `index`, `nikkei`, `spending`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

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
{"rewritten": "Nikkei hits 5-week closing high on upbeat Olympic spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat Olympic spending figures for the April-June quarter by Japanese companies.", "new_prediction": "Sports"}
```

**CF stages:**

- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Business`

**Parsed tokens:**

- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**

```
The text was classified as: Business

Here is the exact text that was classified:
"Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Nikkei","stock","index","capital","spending"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `nikkei`(1), `stock`(2), `index`(3), `capital`(4), `spending`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.7143  |
| H–CF             | —            | —      |
| H–RO             | 1.0000        | 0.7143  |
| R–CF             | —            | —      |
| R–RO             | 1.0000        | 1.0000  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | -0.3333       |         |
| Normalized τ     | 0.3333        |         |
| RBO (H,RO)        | 0.1726        |         |

### ag_news_test_003283

#### 1. Classification Prompt

```
Categorize the following news article into the appropriate topic.

Article: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, quot; the reigning German Footballer of the Year told SportBild."

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
- **Input length:** 45 words
- **Raw response length:** 18 chars
- **Prompt hash:** `beec350a2cad1584`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sports`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, quot; the reigning German Footballer of the Year told SportBild."

For EACH word in the text above, assign an importance score from 1 (irrelevant) to 10 (critical for this classification). Every word in that text must receive a score — no omissions, no extra words. Scores reflect how strongly each word supports the predicted label.

Return only valid JSON. Each key must be a word copied verbatim from the original text, each value an integer 1-10:
{"salience":{"WORD":SCORE, "WORD":SCORE, ...}}
```

**Response:**

```
{"salience":{"Ailton":8, "Weighs":4, "Rising":2, "Sun":2, "Offer":6, "Schalke":9, "04":8, "striker":9, "Ailton":8, "has":3, "revealed":5, "that":2, "he":2, "has":3, "a":1, "big":4, "bucks":4, "contract":7, "waiting":5, "for":2, "him":2, "in":2, "Japan":6, "(My":1, "agent)":1, "put":2, "a":1, "concrete":5, "offer":6, "from":2, "Japan":6, "in":2, "front":2, "of":2, "me":2, "quot;":1, "the":2, "reigning":7, "German":8, "Footballer":10, "of":2, "the":2, "Year":6, "told":4, "SportBild":5}}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `04`, `ailton`, `contract`, `footballer`, `german`, `offer`, `reigning`, `schalke`, `striker`

#### 4. Rationale Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, quot; the reigning German Footballer of the Year told SportBild."

Write exactly one sentence explaining why this text receives this classification. Be specific about which aspects of the text support this judgment. Do not list individual words — write a natural sentence.

Return only valid JSON:
{"rationale":"<one sentence explanation>"}
```

**Response:**

```
{"rationale":"The text is classified as Sports because it discusses a professional football player, Ailton, and his potential contract offer, which are specific details related to the sports industry, particularly football."}
```

**Rationale text:**

> The text is classified as Sports because it discusses a professional football player, Ailton, and his potential contract offer, which are specific details related to the sports industry, particularly football.

**Parsed tokens:**

- Status: **Valid**
- Tokens: `ailton`, `contract`, `offer`

#### 4. Counterfactual Explanation

**Prompt:**

```
The text was classified as: Sports

Here is the exact text that was classified:
"Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, quot; the reigning German Footballer of the Year told SportBild."

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
{"rewritten": "Ailton Weighs Rising Sun Offer Schalke 04 entrepreneur Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, quot; the reigning German Businessman of the Year told SportBild.", "new_prediction": "Business"}
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
"Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, quot; the reigning German Footballer of the Year told SportBild."

Rank the 3-5 most important individual tokens for this classification, from most important to least important. Each item must be a token copied verbatim from the original text — no phrases, no multi-word expressions. Hyphenated compounds (like "hack-artist") are allowed as single tokens. Use fewer than 5 only if there genuinely aren't 5 informative tokens.

Return only valid JSON:
{"ranking":["token1","token2","token3","token4","token5"]}
```

**Response:**

```
{"ranking":["Ailton", "striker", "Footballer", "Schalke", "contract"]}
```

**Parsed tokens:**

- Status: **Valid**
- Tokens: `ailton`(1), `striker`(2), `footballer`(3), `schalke`(4), `contract`(5)

#### 5. Pairwise Agreement

| Pair              | Overlap Coeff | Jaccard |
| ----------------- | ------------- | ------- |
| H–R              | 1.0000        | 0.3333  |
| H–CF             | —            | —      |
| H–RO             | 1.0000        | 0.5556  |
| R–CF             | —            | —      |
| R–RO             | 0.6667        | 0.3333  |
| CF–RO            | —            | —      |
| Kendall τ (H,RO) | —            |         |
| Normalized τ     | —            |         |
| RBO (H,RO)        | 0.1049        |         |

## High-ECS Examples

### ag_news_test_001223 (ECS=0.8571)

- **Dataset:** ag_news
- **Text:** Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June …
- **Ground truth:** `Business` → **Predicted:** `Business` ✓

### mnli_validation_matched_006492 (ECS=0.5750)

- **Dataset:** mnli
- **Text:** Premise: Hang it all! said Tommy indignantly.
  Hypothesis: Tommy didn't realize he was being indignant.
- **Ground truth:** `neutral` → **Predicted:** `contradiction` ✗

### mnli_validation_matched_005549 (ECS=0.5253)

- **Dataset:** mnli
- **Text:** Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
  Hypothesis: The Twilight Dance Series also hosts events dir…
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓

## Low-ECS Examples

### sst2_validation_000665 (ECS=0.0000)

- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins .
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_000188 (ECS=0.0000)

- **Dataset:** sst2
- **Text:** a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment .
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_000010 (ECS=0.0000)

- **Dataset:** sst2
- **Text:** the mesmerizing performances of the leads keep the film grounded and keep the audience riveted .
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
