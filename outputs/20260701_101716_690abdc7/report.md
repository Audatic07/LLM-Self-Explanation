# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-01 10:17:34
- **Duration:** 723.6s (12.1m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 21
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 63540
- **Avg tokens per instance:** 3026

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 7 | 7/7 (100%) | 0.393 | 100% | 100% | 86% | 86% |
| mnli | 7 | 5/7 (71%) | 0.287 | 100% | 100% | 100% | 57% |
| ag_news | 7 | 5/7 (71%) | 0.380 | 100% | 100% | 14% | 100% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 7 | 7 | 0 |
| mnli | 7 | 7 | 2 |
| ag_news | 7 | 7 | 2 |
| **Total** | 21 | 21 | 4 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=4) or medium-length (21–50 words, N=17). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=6). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=10)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 21/21 | 100% |
| Rationale | 21/21 | 100% |
| Counterfactual | 14/21 | 67% |
| Rank Ordering | 17/21 | 81% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=21) | 0.3532 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.4377 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.3174 |
| Mean ECS (complete cases, N=10) | 0.3758 |
| Complete cases | 10/21 (48%) |
| ECS pairs <3 | 7 instances |
  → sst2_validation_000361: 1 pair(s), er=0.5000, ep=NA
  → ag_news_test_004983: 1 pair(s), er=0.3750, ep=NA
  → ag_news_test_001223: 1 pair(s), er=0.8571, ep=NA
  → ag_news_test_002300: 1 pair(s), er=0.1111, ep=NA
  → ag_news_test_000981: 1 pair(s), er=0.6667, ep=NA
  → ... and 2 more
| Std ECS | 0.1868 |
| Median ECS | 0.3056 |
| **Mean ECS lift over chance** (ECS − random) | +0.2534 |
| Mean ECS random baseline | 0.0997 |
| Mean ECS — correct preds (N=17) | 0.3520 |
| Mean ECS — incorrect preds (N=4) | 0.3580 |
| Introduced-concept rate (R) | 0.000 |
| CF canonical (minimal) validity rate | 67% |
| CF contrast (free) validity rate | 95% |
| CF canonical (minimal) minimality (edits/len) | 0.122 |
| CF contrast (free) minimality (edits/len) | 0.204 |
| Confidence elicitation | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size | 1.95 |
| Mean CC4 size | 1.10 |
| % instances with CC3 | 81.0% |
| % instances with CC4 | 66.7% |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.7528 | 0.4377 |
| H–CF | 0.6896 | 0.3174 |
| H–RO | 0.8627 | 0.4557 |
| R–CF | 0.5629 | 0.2666 |
| R–RO | 0.6569 | 0.3738 |
| CF–RO | 0.6667 | 0.3264 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.1779 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Overlap Coefficient is the primary pairwise metric (unlike Jaccard, it is not penalized by smaller salience sets). Jaccard is retained as a secondary reference. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 21/21 (100%) | 21/21 (100%) |
| Rationale | 21/21 (100%) | 21/21 (100%) |
| Counterfactual (JSON parsed) | 21/21 (100%) |
| Counterfactual (rules compliant) | 19/21 (90%) |
| Counterfactual (flip verified) | 14/19 (74%) |
| Rank Ordering | 17/21 (81%) | 17/21 (81%) |
| All 4 valid | 10/21 |
| 3 valid (CC3 adjusted) | 11/21 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs. Primary ECS averages H–CF and CF–RO (evidence-list methods). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 4 | 0.5758 |
| Medium (21–50) | 17 | 0.3008 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 15 | 0.3020 |
| Short vocab (≤20 unique tokens) | 6 | 0.4811 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.3532 | [0.2688, 0.4335] |

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
- **ECS (full):** 0.0422
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.1000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"and": 2, "if": 4, "you": 6, "re": 3, "not": 8, "nearly": 5, "moved": 9, "to": 4, "tears": 9, "by": 3, "a": 2, "couple": 5, "of": 2, "scenes": 7, "you": 6, "ve": 4, "got": 4, "ice": 8, "water": 8, "in": 3, "your": 6, "veins": 8}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ice`, `moved`, `not`, `tears`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as positive because it implies that the scenes are emotionally powerful and capable of evoking strong feelings, which is a complimentary sentiment."}
```

**Rationale text:**
> The text was classified as positive because it implies that the scenes are emotionally powerful and capable of evoking strong feelings, which is a complimentary sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `scenes`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "and if you 're not nearly moved to tears by a couple of scenes , you 've got a heart of stone .", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> and if you 're not nearly moved to tears by a couple of scenes , you 're a monster .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `got`, `ice`, `in`, `ve`, `veins`, `water`, `your`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["tears", "moved", "veins"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tears`(1), `moved`(2), `veins`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | 0.2500 | 0.1000 |
| H–RO | 0.6667 | 0.4000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.3333 | 0.1111 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1804 |

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
- **ECS (full):** 0.5967
- **ECS (extraction–rationale):** 0.7500
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"expect": 2, "the": 1, "same-old": 8, "lame-old": 9, "slasher": 6, "nonsense": 8, "just": 2, "with": 1, "different": 3, "scenery": 4}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`, `nonsense`, `same-old`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as negative because it uses strongly derogatory language, such as 'same-old', 'lame-old', and 'nonsense', to express disdain and disappointment with the expected content."}
```

**Rationale text:**
> The text was classified as negative because it uses strongly derogatory language, such as 'same-old', 'lame-old', and 'nonsense', to express disdain and disappointment with the expected content.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `expected`, `lame-old`, `nonsense`, `same-old`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "expect the same-old , great slasher fun , just with different scenery . ", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> expect the same-old , great slasher fun , just with different scenery . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`, `nonsense`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "expect the same-old , lame-old slasher nonsense , just with different scenery . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["lame-old", "nonsense", "slasher"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `lame-old`(1), `nonsense`(2), `slasher`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.7500 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 0.6667 | 0.5000 |
| R–CF | 1.0000 | 0.5000 |
| R–RO | 0.6667 | 0.4000 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1990 |

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
- **ECS (full):** 0.4167
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"a": 2, "very": 6, "long": 8, "movie": 4, "dull": 9, "in": 2, "stretches": 7, "with": 3, "entirely": 5, "too": 6, "much": 6, "focus": 4, "on": 2, "meal": 3, "preparation": 3, "and": 2, "igloo": 3, "construction": 3, "": 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `long`, `much`, `stretches`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as negative because it uses words and phrases with negative connotations, such as 'very long', 'dull', and 'entirely too much', to describe the movie, indicating an overall unfavorable opinion."}
```

**Rationale text:**
> The text was classified as negative because it uses words and phrases with negative connotations, such as 'very long', 'dull', and 'entirely too much', to describe the movie, indicating an overall unfavorable opinion.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`, `entirely`, `long`, `movie`, `much`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "a very long movie , engaging in stretches , with entirely too much focus on meal preparation and igloo construction .", "new_prediction": "positive"}
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

Text: "a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["dull", "long", "stretches"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `dull`(1), `long`(2), `stretches`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.5000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.7500 |
| R–CF | — | — |
| R–RO | 0.6667 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3257 |

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
- **ECS (full):** 0.3119
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** 0.1429
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"whether": 2, 
"writer-director": 4, 
"anne": 3, 
"fontaine": 3, 
"'s": 1, 
"film": 5, 
"is": 2, 
"a": 1, 
"ghost": 6, 
"story": 6, 
"an": 1, 
"account": 5, 
"of": 1, 
"a": 1, 
"nervous": 6, 
"breakdown": 6, 
"a": 1, 
"trip": 5, 
"down": 4, 
"memory": 7, 
"lane": 5, 
"all": 2, 
"three": 2, 
"or": 2, 
"none": 2, 
"of": 1, 
"the": 1, 
"above": 2, 
"it": 3, 
"is": 2, 
"as": 4, 
"seductive": 9, 
"as": 4, 
"it": 3, 
"is": 2, 
"haunting": 9
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `breakdown`, `ghost`, `haunting`, `memory`, `nervous`, `seductive`, `story`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as positive because it describes the film as 'seductive' and 'haunting', which are words that convey a sense of captivating beauty and emotional resonance, rather than criticism or negativity."}
```

**Rationale text:**
> The text was classified as positive because it describes the film as 'seductive' and 'haunting', which are words that convey a sense of captivating beauty and emotional resonance, rather than criticism or negativity.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `haunting`, `seductive`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as dull as it is haunting . ", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as dull as it is haunting . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `seductive`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "whether writer-director anne fontaine 's film is a ghost story , an account of a nervous breakdown , a trip down memory lane , all three or none of the above , it is as seductive as it is haunting . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["seductive", "haunting", "ghost"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `seductive`(1), `haunting`(2), `ghost`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.6667 | 0.2500 |
| H–CF | 1.0000 | 0.1429 |
| H–RO | 1.0000 | 0.4286 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 0.6667 | 0.5000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3903 |

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
- **ECS (full):** 0.5067
- **ECS (extraction–rationale):** 0.6000
- **ECS (extraction–perturbation):** 0.5000
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"it": 2, "provides": 6, "an": 1, "honest": 8, "look": 4, "at": 1, "a": 1, "community": 7, "striving": 9, "to": 1, "anchor": 5, "itself": 3, "in": 1, "new": 6, "grounds": 5, "." : 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `community`, `honest`, `striving`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

In one sentence, explain why the text was classified as positive.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as positive because it uses phrases with positive connotations, such as 'honest look' and 'striving to anchor itself', which imply a sense of hope and resilience in the community."}
```

**Rationale text:**
> The text was classified as positive because it uses phrases with positive connotations, such as 'honest look' and 'striving to anchor itself', which imply a sense of hope and resilience in the community.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `anchor`, `community`, `honest`, `look`, `striving`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Edit the text so that it is classified as "negative" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: negative>"}
```

**Response:**
```
{"rewritten": "it provides a dishonest look at a community struggling to anchor itself in new grounds . ", "new_prediction": "negative"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `negative`

**Reconstructed text:**
> it provides a dishonest look at a community struggling to anchor itself in new grounds . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `an`, `honest`, `striving`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: positive

Text: "it provides an honest look at a community striving to anchor itself in new grounds . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["honest", "striving", "community"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `honest`(1), `striving`(2), `community`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6000 |
| H–CF | 0.6667 | 0.5000 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.6667 | 0.3333 |
| R–RO | 1.0000 | 0.6000 |
| CF–RO | 0.6667 | 0.5000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1710 |

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
- **ECS (full):** 0.7333
- **ECS (extraction–rationale):** 0.6667
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 2 | **CC4 size:** 2

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"a": 2, "misogynistic": 10, "piece": 6, "of": 2, "filth": 10, "that": 4, "attempts": 6, "to": 2, "pass": 4, "itself": 4, "off": 2, "as": 2, "hip": 4, "young": 4, "adult": 4, "entertainment": 6, "." : 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `misogynistic`, `piece`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as negative because it uses strongly derogatory language, such as 'misogynistic' and 'filth', to express disdain and criticism for the subject."}
```

**Rationale text:**
> The text was classified as negative because it uses strongly derogatory language, such as 'misogynistic' and 'filth', to express disdain and criticism for the subject.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `misogynistic`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "a feminist piece of genius that attempts to pass itself off as hip , young adult entertainment .", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> a feminist piece of genius that attempts to pass itself off as hip , young adult entertainment .

**Parsed tokens:**
- Status: **Valid**
- Tokens: `filth`, `misogynistic`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["misogynistic", "filth", "attempts"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `misogynistic`(1), `filth`(2), `attempts`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 0.6667 | 0.5000 |
| R–CF | 1.0000 | 1.0000 |
| R–RO | 1.0000 | 0.6667 |
| CF–RO | 1.0000 | 0.6667 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.2440 |

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
- **ECS (full):** 0.1429
- **ECS (extraction–rationale):** 0.1429
- **ECS (extraction–perturbation):** 0.2857
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"care": 6, "deftly": 4, "captures": 5, "the": 1, "wonder": 3, "and": 1, "menace": 5, "of": 1, "growing": 3, "up": 2, "but": 8, "he": 2, "never": 9, "really": 7, "embraces": 8, "the": 1, "joy": 4, "of": 1, "fuhrman's": 3, "destructive": 6, "escapism": 5, "or": 1, "the": 1, "grace-in-rebellion": 6, "found": 4, "by": 1, "his": 2, "characters": 3}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `care`, `destructive`, `embraces`, `grace-in-rebellion`, `never`, `really`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

In one sentence, explain why the text was classified as negative.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as negative because although it acknowledges a positive aspect of 'care' capturing the wonder and menace of growing up, it ultimately criticizes 'care' for not embracing the joy and grace-in-rebellion found in the characters, implying a lack or shortfall."}
```

**Rationale text:**
> The text was classified as negative because although it acknowledges a positive aspect of 'care' capturing the wonder and menace of growing up, it ultimately criticizes 'care' for not embracing the joy and grace-in-rebellion found in the characters, implying a lack or shortfall.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capturing`, `care`, `characters`, `embracing`, `found`, `grace-in-rebellion`, `growing`, `joy`, `menace`, `wonder`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Edit the text so that it is classified as "positive" instead. Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: positive>"}
```

**Response:**
```
{"rewritten": "care deftly captures the wonder and menace of growing up , and he fully embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . ", "new_prediction": "positive"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `positive`

**Reconstructed text:**
> care deftly captures the wonder and menace of growing up , and he fully embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . 

**Parsed tokens:**
- Status: **Valid**
- Tokens: `but`, `never`, `really`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: negative

Text: "care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["never", "but", "menace"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.1429 |
| H–CF | 0.6667 | 0.2857 |
| H–RO | — | — |
| R–CF | 0.0000 | 0.0000 |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

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
- **ECS (full):** 0.4333
- **ECS (extraction–rationale):** 0.6667
- **ECS (extraction–perturbation):** 0.1667
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 3 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"In": 2, 
"1099": 4, 
"under": 2, 
"their": 2, 
"leaders": 3, 
"Godfrey": 1, 
"de": 1, 
"Bouillon": 1, 
"and": 2, 
"Tancred": 1, 
"the": 2, 
"Crusaders": 8, 
"captured": 9, 
"the": 2, 
"Holy": 6, 
"City": 6, 
"for": 2, 
"Christendom": 2, 
"by": 2, 
"slaughtering": 3, 
"both": 2, 
"Muslims": 2, 
"and": 2, 
"Jews": 2, 
"Hypothesis": 1, 
"The": 2, 
"Crusaders": 8, 
"captured": 9, 
"the": 2, 
"Holy": 6, 
"City": 6
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `1099`, `captured`, `city`, `crusaders`, `holy`, `leaders`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise directly states that the Crusaders captured the Holy City, which is exactly what the hypothesis asserts, making the premise a direct entailment of the hypothesis."}
```

**Rationale text:**
> The premise directly states that the Crusaders captured the Holy City, which is exactly what the hypothesis asserts, making the premise a direct entailment of the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `captured`, `city`, `crusaders`, `holy`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""neutral" or "contradiction"" instead of "entailment". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
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

Text: "Premise: In 1099, under their leaders Godfrey de Bouillon and Tancred, the Crusaders captured the Holy City for Christendom by slaughtering both Muslims and Jews.
Hypothesis: The Crusaders captured the Holy City."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Crusaders", "captured", "Holy"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `crusaders`(1), `captured`(2), `holy`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | 1.0000 | 0.1667 |
| H–RO | 1.0000 | 0.5000 |
| R–CF | 1.0000 | 0.2500 |
| R–RO | 1.0000 | 0.7500 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1132 |

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
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
  "Premise:": 1, 
  "we": 8, 
  "only": 10, 
  "have": 8, 
  "to": 6, 
  "get": 8, 
  "up": 8, 
  "for": 6, 
  "you": 2, 
  "know": 2, 
  "for": 6, 
  "the": 4, 
  "daytime": 10, 
  "feedings": 10, 
  "Hypothesis:": 1, 
  "We": 8, 
  "only": 10, 
  "have": 8, 
  "to": 6, 
  "get": 8, 
  "up": 8, 
  "for": 6, 
  "the": 4, 
  "daytime": 10, 
  "feedings": 10
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `feedings`, `get`, `know`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise and hypothesis are virtually identical in meaning, with the premise containing a minor filler phrase ('you know') that does not affect the overall logical relationship, thereby making the premise entail the hypothesis."}
```

**Rationale text:**
> The premise and hypothesis are virtually identical in meaning, with the premise containing a minor filler phrase ('you know') that does not affect the overall logical relationship, thereby making the premise entail the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `know`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""neutral" or "contradiction"" instead of "entailment". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: we only have to get up for you know for the daytime feedings\nHypothesis: We only have to get up for the nighttime feedings.", "new_prediction": "contradiction"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the nighttime feedings.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["daytime", "feedings", "only"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2500 |
| H–CF | 1.0000 | 0.2500 |
| H–RO | — | — |
| R–CF | 0.0000 | 0.0000 |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

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
- **ECS (full):** 0.1315
- **ECS (extraction–rationale):** 0.3077
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

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"If": 6, 
"necessary": 4, 
"to": 2, 
"meeting": 5, 
"the": 1, 
"restrictions": 8, 
"imposed": 3, 
"in": 1, 
"the": 1, 
"preceding": 5, 
"sentence": 5, 
"the": 1, 
"Administrator": 7, 
"shall": 6, 
"reduce": 9, 
"pro": 2, 
"rata": 2, 
"the": 1, 
"basic": 8, 
"Phase": 8, 
"II": 8, 
"allowance": 9, 
"allocations": 9, 
"for": 2, 
"each": 4, 
"unit": 7, 
"subject": 6, 
"to": 2, 
"the": 1, 
"requirements": 8, 
"of": 2, 
"section": 8, 
"414": 10, 
"Hypothesis:": 1, 
"Section": 8, 
"414": 10, 
"helps": 7, 
"balance": 8, 
"allowance": 9, 
"allocations": 9, 
"for": 2, 
"units": 7
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `414`, `allocations`, `allowance`, `basic`, `ii`, `phase`, `reduce`, `requirements`, `restrictions`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

In one sentence, explain why the text was classified as entailment.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise implies that section 414 has requirements that may necessitate reductions to balance allowance allocations, which directly supports the hypothesis that section 414 helps balance allowance allocations for units."}
```

**Rationale text:**
> The premise implies that section 414 has requirements that may necessitate reductions to balance allowance allocations, which directly supports the hypothesis that section 414 helps balance allowance allocations for units.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `414`, `allocations`, `allowance`, `balance`, `helps`, `requirements`, `section`, `units`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""neutral" or "contradiction"" instead of "entailment". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: neutral, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414. Hypothesis: Section 414 has no effect on allowance allocations for units.", "new_prediction": "contradiction"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414. Hypothesis: Section 414 has no effect on allowance allocations for units.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `balance`, `helps`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: entailment

Text: "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414.
Hypothesis: Section 414 helps balance allowance allocations for units."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["necessary", "reduce", "allocations"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `necessary`(1), `reduce`(2), `allocations`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.5000 | 0.3077 |
| H–CF | 0.0000 | 0.0000 |
| H–RO | 0.6667 | 0.2000 |
| R–CF | 1.0000 | 0.2500 |
| R–RO | 0.3333 | 0.1000 |
| CF–RO | 0.0000 | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1911 |

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
- **ECS (full):** 0.1019
- **ECS (extraction–rationale):** 0.0833
- **ECS (extraction–perturbation):** 0.2222
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 0 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"Premise:": 1,
"Favorite": 2,
"items": 4,
"that": 1,
"will": 2,
"help": 2,
"preserve": 2,
"your": 1,
"memories": 3,
"of": 1,
"the": 1,
"rugged": 2,
"Lakeland": 3,
"countryside": 3,
"are": 2,
"clothing": 6,
"or": 2,
"blankets": 6,
"made": 4,
"from": 2,
"the": 1,
"local": 4,
"Herdwick": 6,
"wool,": 6,
"coasters": 6,
"of": 1,
"polished": 4,
"slate,": 6,
"or": 2,
"walking": 6,
"sticks": 6,
"with": 2,
"ram's-horn": 6,
"handles.": 6,
"Hypothesis:": 1,
"They": 8,
"don't": 9,
"sell": 8,
"any": 8,
"souveineers.": 10,
"are": 2,
"will": 2,
"help": 2,
"preserve": 2,
"your": 1,
"memories": 3,
"of": 1,
"the": 1,
"rugged": 2,
"Lakeland": 3,
"countryside": 3
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `blankets`, `clothing`, `coasters`, `herdwick`, `sell`, `souveineers`, `wool`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

In one sentence, explain why the text was classified as contradiction.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise lists specific souvenir items that can help preserve memories, directly contradicting the hypothesis that they don't sell any souvenirs."}
```

**Rationale text:**
> The premise lists specific souvenir items that can help preserve memories, directly contradicting the hypothesis that they don't sell any souvenirs.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `help`, `items`, `memories`, `preserve`, `sell`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""entailment" or "neutral"" instead of "contradiction". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, neutral>"}
```

**Response:**
```
{"rewritten": "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles. Hypothesis: They sell souvenirs.", "new_prediction": "entailment"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**
> Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles. Hypothesis: They sell souvenirs.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `any`, `don't`, `souveineers`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: contradiction

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["are", "items", "souveineers"]}
```

**Parsed tokens:**
- *Not parsed*

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.2000 | 0.0833 |
| H–CF | 0.6667 | 0.2222 |
| H–RO | — | — |
| R–CF | 0.0000 | 0.0000 |
| R–RO | — | — |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | — |

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
- **ECS (full):** 0.3048
- **ECS (extraction–rationale):** 0.5385
- **ECS (extraction–perturbation):** 0.3636
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 5 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"The": 2, 
"Santa": 4, 
"Monica": 4, 
"Pier": 6, 
"is": 2, 
"the": 2, 
"coastal": 5, 
"setting": 5, 
"for": 3, 
"Twilight": 8, 
"Dance": 8, 
"Series": 8, 
"a": 1, 
"selection": 4, 
"of": 2, 
"free": 3, 
"summer": 4, 
"concerts": 6, 
"arranged": 4, 
"each": 3, 
"year": 3, 
"Hypothesis": 1, 
"The": 2, 
"Twilight": 8, 
"Dance": 8, 
"Series": 8, 
"also": 7, 
"hosts": 7, 
"events": 6, 
"directly": 9, 
"on": 9, 
"the": 2, 
"beach": 9, 
"near": 9, 
"the": 2, 
"pier": 6
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `dance`, `directly`, `hosts`, `near`, `series`, `twilight`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise only mentions that the Twilight Dance Series takes place at the Santa Monica Pier, but does not provide information about whether events are also hosted directly on the beach near the pier, making the hypothesis neither entailed nor contradicted."}
```

**Rationale text:**
> The premise only mentions that the Twilight Dance Series takes place at the Santa Monica Pier, but does not provide information about whether events are also hosted directly on the beach near the pier, making the hypothesis neither entailed nor contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `dance`, `directly`, `events`, `hosted`, `monica`, `near`, `pier`, `santa`, `series`, `twilight`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""entailment" or "contradiction"" instead of "neutral". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year. Hypothesis: The Twilight Dance Series is held directly on the Santa Monica Pier.", "new_prediction": "entailment"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `entailment`

**Reconstructed text:**
> Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year. Hypothesis: The Twilight Dance Series is held directly on the Santa Monica Pier.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `events`, `hosts`, `near`, `pier`, `the`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: The Santa Monica Pier is the coastal setting for the Twilight Dance Series, a selection of free summer concerts arranged each year.
Hypothesis: The Twilight Dance Series also hosts events directly on the beach near the pier."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["pier", "Series", "setting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `pier`(1), `series`(2), `setting`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8750 | 0.5385 |
| H–CF | 0.5714 | 0.3636 |
| H–RO | 0.3333 | 0.1000 |
| R–CF | 0.7143 | 0.3571 |
| R–RO | 0.6667 | 0.1538 |
| CF–RO | 0.3333 | 0.1111 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0000 |

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
- **ECS (full):** 0.2708
- **ECS (extraction–rationale):** 0.3750
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"Nokia": 8, 
"announces": 6, 
"Near": 9, 
"Field": 9, 
"Communication": 10, 
"products": 7, 
"With": 2, 
"the": 1, 
"Nokia": 5, 
"NFC": 10, 
"(Near": 3, 
"Field": 3, 
"Communication)": 3, 
"shell": 4, 
"on": 1, 
"their": 1, 
"phone": 8, 
"consumers": 6, 
"will": 2, 
"be": 1, 
"able": 2, 
"to": 1, 
"access": 6, 
"a": 1, 
"variety": 5, 
"of": 1, 
"services": 7, 
"and": 2, 
"exchange": 6, 
"information": 8, 
"with": 2, 
"a": 1, 
"simple": 4, 
"touch": 6, 
"gesture": 5
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `information`, `near`, `nfc`, `phone`, `products`, `services`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as Sci/Tech because it discusses a technological innovation, specifically Near Field Communication products and their applications, which falls under the category of science and technology."}
```

**Rationale text:**
> The text was classified as Sci/Tech because it discusses a technological innovation, specifically Near Field Communication products and their applications, which falls under the category of science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `products`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Nokia announces major investment in Near Field Communication products, a move expected to boost company profits and create new jobs.", "new_prediction": "Business"}
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
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["NFC", "Communication", "phone"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `communication`(2), `phone`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.3750 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.4286 |
| R–CF | — | — |
| R–RO | 0.3333 | 0.1667 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0488 |

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
- **ECS (full):** 0.6786
- **ECS (extraction–rationale):** 0.8571
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Business`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"Nikkei": 8, 
"hits": 4, 
"5-week": 6, 
"closing": 6, 
"high": 6, 
"on": 2, 
"upbeat": 7, 
"capital": 9, 
"spending": 9, 
"data": 8, 
"TOKYO": 3, 
"Japan": 5, 
"benchmark": 8, 
"stock": 9, 
"index": 8, 
"hit": 4, 
"a": 1, 
"five-week": 6, 
"closing": 6, 
"high": 6, 
"Monday": 3, 
"on": 2, 
"upbeat": 7, 
"capital": 9, 
"spending": 9, 
"figures": 8, 
"for": 2, 
"the": 1, 
"April-June": 6, 
"quarter": 6, 
"by": 2, 
"Japanese": 5, 
"companies": 8
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `benchmark`, `capital`, `data`, `index`, `nikkei`, `spending`, `stock`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as Business because it discusses stock market performance, specifically the Nikkei index, and capital spending data, which are key indicators of economic and financial activity."}
```

**Rationale text:**
> The text was classified as Business because it discusses stock market performance, specifically the Nikkei index, and capital spending data, which are key indicators of economic and financial activity.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capital`, `data`, `index`, `nikkei`, `spending`, `stock`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies, boosting Tokyo's global influence.", "new_prediction": "World"}
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

Text: "Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June quarter by Japanese companies."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nikkei", "stock", "spending"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nikkei`(1), `stock`(2), `spending`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.8571 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.4286 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1516 |

### ag_news_test_003283

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

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
- **Prompt hash:** `6b8688d9df4228aa`
- **ECS (full):** 0.2952
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** 0.5455
- **ECS primary pairs:** 2
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `Business`
- **CC3 size:** 5 | **CC4 size:** 0

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"Ailton": 8, 
"Weighs": 2, 
"Rising": 4, 
"Sun": 4, 
"Offer": 6, 
"Schalke": 9, 
"04": 9, 
"striker": 9, 
"Ailton": 8, 
"has": 1, 
"revealed": 2, 
"that": 1, 
"he": 1, 
"has": 1, 
"a": 1, 
"big": 2, 
"bucks": 2, 
"contract": 6, 
"waiting": 2, 
"for": 1, 
"him": 1, 
"in": 1, 
"Japan": 6, 
"(My": 1, 
"agent)": 3, 
"put": 1, 
"a": 1, 
"concrete": 3, 
"offer": 6, 
"from": 1, 
"Japan": 6, 
"in": 1, 
"front": 1, 
"of": 1, 
"me": 1, 
""": 1, 
"the": 1, 
"reigning": 5, 
"German": 8, 
"Footballer": 10, 
"of": 1, 
"the": 1, 
"Year": 5, 
"told": 2, 
"SportBild": 4, 
""": 1
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `04`, `ailton`, `contract`, `footballer`, `german`, `japan`, `offer`, `schalke`, `striker`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

In one sentence, explain why the text was classified as Sports.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as Sports because it discusses a professional soccer player, Ailton, and his potential contract offer, which are topics directly related to the sports industry."}
```

**Rationale text:**
> The text was classified as Sports because it discusses a professional soccer player, Ailton, and his potential contract offer, which are topics directly related to the sports industry.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ailton`, `contract`, `offer`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Edit the text so that it is classified as "World" or "Business" or "Sci/Tech" instead of "Sports". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Business, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "Ailton Weighs Rising Sun Investment Opportunity Ailton has revealed that he has a big bucks investment waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the renowned German entrepreneur of the Year told Bloomberg.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `Business`

**Reconstructed text:**
> Ailton Weighs Rising Sun Investment Opportunity Ailton has revealed that he has a big bucks investment waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the renowned German entrepreneur of the Year told Bloomberg.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `04`, `contract`, `footballer`, `offer`, `reigning`, `schalke`, `sportbild`, `striker`

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sports

Text: "Ailton Weighs Rising Sun Offer Schalke 04 striker Ailton has revealed that he has a big bucks contract waiting for him in Japan. (My agent) put a concrete offer from Japan in front of me, " the reigning German Footballer of the Year told SportBild."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Footballer", "striker", "Schalke"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `footballer`(1), `striker`(2), `schalke`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | 0.7500 | 0.5455 |
| H–RO | 1.0000 | 0.3333 |
| R–CF | 0.6667 | 0.2222 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 1.0000 | 0.3750 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0595 |

### ag_news_test_002300

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `World`
- **Predicted:** `Business` ✗
- **Input length:** 34 words
- **Raw response length:** 20 chars

### ag_news_test_000981

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

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
- **Input length:** 26 words
- **Raw response length:** 20 chars
- **Prompt hash:** `738fa585e9337bf6`
- **ECS (full):** 0.5833
- **ECS (extraction–rationale):** 0.6667
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `Sci/Tech`
- **CC3 size:** 3 | **CC4 size:** 3

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"Spammers": 8,
"use": 2,
"sender": 6,
"authentication": 9,
"too": 1,
"study": 4,
"says": 1,
"The": 1,
"technology": 8,
"hasn't": 2,
"been": 2,
"widely": 3,
"adopted": 5,
"but": 2,
"spammers": 8,
"are": 2,
"taking": 3,
"it": 2,
"up": 2,
"at": 2,
"a": 2,
"faster": 4,
"rate": 4,
"than": 2,
"legitimate": 6,
"e-mailers": 7
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `e-mailers`, `spammers`, `technology`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

In one sentence, explain why the text was classified as Sci/Tech.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as Sci/Tech because it discusses sender authentication technology and its adoption by spammers and legitimate e-mailers, which falls under the category of science and technology."}
```

**Rationale text:**
> The text was classified as Sci/Tech because it discusses sender authentication technology and its adoption by spammers and legitimate e-mailers, which falls under the category of science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `authentication`, `e-mailers`, `legitimate`, `sender`, `spammers`, `technology`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Edit the text so that it is classified as "World" or "Sports" or "Business" instead of "Sci/Tech". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Business>"}
```

**Response:**
```
{"rewritten": "Spammers use economic authentication too, study says The market hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate traders.", "new_prediction": "Business"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: No
- Actual label: `Sci/Tech`

**Parsed tokens:**
- *Not parsed*

#### 4. Rank Ordering Explanation

**Prompt:**
```
The text was classified as: Sci/Tech

Text: "Spammers use sender authentication too, study says The technology hasn't been widely adopted, but spammers are taking it up at a faster rate than legitimate e-mailers."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["technology", "spammers", "authentication"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `technology`(1), `spammers`(2), `authentication`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.6667 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.7500 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.5000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1480 |

### ag_news_test_003796

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `Business`
- **Predicted:** `Sci/Tech` ✗
- **Input length:** 39 words
- **Raw response length:** 20 chars

### ag_news_test_002873

#### 1. Classification Prompt
```
Categorize the following news article into the appropriate topic.

Article: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

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
- **Input length:** 34 words
- **Raw response length:** 20 chars
- **Prompt hash:** `1d2b82039e416b33`
- **ECS (full):** 0.2679
- **ECS (extraction–rationale):** 0.2857
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 1
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"August": 2, 
"chip": 8, 
"sales": 9, 
"up": 1, 
"Global": 3, 
"semiconductor": 9, 
"sales": 9, 
"rose": 4, 
"1.1": 6, 
"percent": 6, 
"to": 1, 
"$18.2": 8, 
"billion": 8, 
"in": 1, 
"August": 2, 
"from": 1, 
"the": 1, 
"previous": 5, 
"month": 5, 
"and": 1, 
"it": 1, 
"appears": 2, 
"as": 1, 
"though": 1, 
"chip": 8, 
"inventories": 7, 
"are": 1, 
"declining": 7, 
"an": 1, 
"industry": 8, 
"trade": 8, 
"group": 8, 
"said": 4, 
"Thursday": 2
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `18.2`, `billion`, `chip`, `industry`, `sales`, `semiconductor`, `trade`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

In one sentence, explain why the text was classified as Business.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The text was classified as Business because it discusses sales figures, revenue, and industry trends, which are all typical topics related to the business and financial sector."}
```

**Rationale text:**
> The text was classified as Business because it discusses sales figures, revenue, and industry trends, which are all typical topics related to the business and financial sector.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `industry`, `sales`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Edit the text so that it is classified as "World" or "Sports" or "Sci/Tech" instead of "Business". Make as few edits as possible.

Return only valid JSON:
{"rewritten": "<edited text>", "new_prediction": "<one of: World, Sports, Sci/Tech>"}
```

**Response:**
```
{"rewritten": "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group in Tokyo said Thursday.", "new_prediction": "World"}
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
The text was classified as: Business

Text: "August chip sales up Global semiconductor sales rose 1.1 percent to $18.2 billion in August from the previous month and it appears as though chip inventories are declining, an industry trade group said Thursday."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["sales", "billion", "semiconductor"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `sales`(1), `billion`(2), `semiconductor`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.2857 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.4286 |
| R–CF | — | — |
| R–RO | 0.5000 | 0.2500 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3271 |


## High-ECS Examples

### sst2_validation_000188 (ECS=0.7333)
- **Dataset:** sst2
- **Text:** a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### ag_news_test_001223 (ECS=0.6786)
- **Dataset:** ag_news
- **Text:** Nikkei hits 5-week closing high on upbeat capital spending data TOKYO - Japan 's benchmark Nikkei stock index hit a five-week closing high Monday on upbeat capital spending figures for the April-June …
- **Ground truth:** `Business` → **Predicted:** `Business` ✓

### sst2_validation_000657 (ECS=0.5967)
- **Dataset:** sst2
- **Text:** expect the same-old , lame-old slasher nonsense , just with different scenery . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓


## Low-ECS Examples

### sst2_validation_000665 (ECS=0.0422)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_006801 (ECS=0.1019)
- **Dataset:** mnli
- **Text:** Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking stic…
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓

### mnli_validation_matched_007556 (ECS=0.1315)
- **Dataset:** mnli
- **Text:** Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the req…
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
