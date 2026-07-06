# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-01 15:55:25
- **Duration:** 409.7s (6.8m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 14
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 37378
- **Avg tokens per instance:** 2670

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 7 | 7/7 (100%) | 0.332 | 100% | 100% | 86% | 86% |
| mnli | 7 | 5/7 (71%) | 0.198 | 86% | 100% | 86% | 57% |
| ag_news | 0 | — | 0.000 | 0% | 0% | 0% | 0% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 7 | 7 | 0 |
| mnli | 7 | 7 | 2 |
| ag_news | 0 | 0 | 0 |
| **Total** | 14 | 14 | 2 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=4) or medium-length (21–50 words, N=9). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=6). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=8)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 13/14 | 93% |
| Rationale | 14/14 | 100% |
| Counterfactual | 12/14 | 86% |
| Rank Ordering | 10/14 | 71% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=14) | 0.2699 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.2676 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.3273 |
| Mean ECS (complete cases, N=8) | 0.3250 |
| Complete cases | 8/14 (57%) |
| Std ECS | 0.1893 |
| Median ECS | 0.2606 |
| **Mean ECS lift over chance** (ECS − random) | +0.1563 |
| Mean ECS random baseline | 0.1136 |

> **No significance testing applied.** The lift, correct-vs-incorrect split, length/vocab strata, and any other comparison above are point estimates (plus the bootstrap CI on mean ECS where shown) — no hypothesis test or multiple-comparison correction has been run, regardless of what `config/experiment.yaml` declares. At this pilot N, treat every comparison in this report as descriptive.

| Mean ECS — correct preds (N=11) | 0.2795 |
| Mean ECS — incorrect preds (N=2) | 0.2169 |
| Introduced-concept rate (R) | 0.626 |
| CF canonical (minimal) validity rate | 86% |
| CF contrast (free) validity rate | 86% |
| CF canonical (minimal) minimality (edits/len) | 0.127 |
| CF contrast (free) minimality (edits/len) | 0.155 |
| Confidence elicitation | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size | 1.36 |
| Mean CC4 size | 0.64 |
| % instances with CC3 | 57.1% |
| % instances with CC4 | 42.9% |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.5745 | 0.2959 |
| H–CF | 0.7035 | 0.3296 |
| H–RO | 0.7667 | 0.4654 |
| R–CF | 0.3552 | 0.1933 |
| R–RO | 0.5000 | 0.2552 |
| CF–RO | 0.7083 | 0.3611 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.2127 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported here as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — for interpreting individual pairs, not for the headline number. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 13/14 (93%) | 13/14 (93%) |
| Rationale | 14/14 (100%) | 14/14 (100%) |
| Counterfactual (JSON parsed) | 14/14 (100%) |
| Counterfactual (rules compliant) | 14/14 (100%) |
| Counterfactual (flip verified) | 12/14 (86%) |
| Rank Ordering | 10/14 (71%) | 10/14 (71%) |
| All 4 valid | 8/14 |
| 3 valid (CC3 adjusted) | 5/14 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 4 | 0.4185 |
| Medium (21–50) | 9 | 0.2039 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 7 | 0.1812 |
| Short vocab (≤20 unique tokens) | 6 | 0.3734 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2699 | [0.1795, 0.3828] |

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
- **ECS (extraction–perturbation):** 0.1056
- **ECS primary pairs:** 4
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
- Tokens: `scene`

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
- **ECS (full):** 0.4905
- **ECS (extraction–rationale):** 0.3929
- **ECS (extraction–perturbation):** 0.6667
- **ECS primary pairs:** 4
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
{"rationale": "The text was classified as negative because it uses strongly derogatory language, such as 'same-old', 'lame-old', and 'nonsense', to express disappointment and disdain for the expected content."}
```

**Rationale text:**
> The text was classified as negative because it uses strongly derogatory language, such as 'same-old', 'lame-old', and 'nonsense', to express disappointment and disdain for the expected content.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `expect`, `lame`, `lame-old`, `nonsense`, `old`, `same-old`

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
| H–R | 1.0000 | 0.5000 |
| H–CF | 1.0000 | 0.6667 |
| H–RO | 0.6667 | 0.5000 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 0.6667 | 0.2857 |
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
- **ECS (extraction–rationale):** 0.4167
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
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
- **ECS (full):** 0.2241
- **ECS (extraction–rationale):** 0.1556
- **ECS (extraction–perturbation):** 0.2381
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 1 | **CC4 size:** 1

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
{"salience": {"whether": 2, "writer-director": 4, "anne": 3, "fontaine": 3, "s": 1, "film": 5, "is": 1, "a": 1, "ghost": 6, "story": 6, "an": 1, "account": 5, "of": 1, "a": 1, "nervous": 6, "breakdown": 6, "a": 1, "trip": 5, "down": 4, "memory": 7, "lane": 7, "all": 2, "three": 2, "or": 1, "none": 2, "of": 1, "the": 1, "above": 2, "it": 1, "is": 1, "as": 3, "seductive": 9, "as": 3, "it": 1, "is": 1, "haunting": 8}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `ghost`, `haunting`, `lane`, `memory`, `nervous`, `seductive`, `story`

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
{"rationale": "The text was classified as positive because it describes the film as 'seductive' and 'haunting', which are words that convey a sense of captivating and emotional depth, implying a compelling and effective cinematic experience."}
```

**Rationale text:**
> The text was classified as positive because it describes the film as 'seductive' and 'haunting', which are words that convey a sense of captivating and emotional depth, implying a compelling and effective cinematic experience.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `film`, `haunt`, `seductive`

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
| H–R | 0.3333 | 0.1111 |
| H–CF | 1.0000 | 0.1429 |
| H–RO | 1.0000 | 0.4286 |
| R–CF | 1.0000 | 0.3333 |
| R–RO | 0.3333 | 0.2000 |
| CF–RO | 1.0000 | 0.3333 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3721 |

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
- **ECS (full):** 0.3000
- **ECS (extraction–rationale):** 0.1667
- **ECS (extraction–perturbation):** 0.5000
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 2 | **CC4 size:** 1

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
{"rationale": "The text was classified as positive because it uses phrases with positive connotations, such as 'honest look' and 'striving to anchor itself', which imply a sense of hope and resilience."}
```

**Rationale text:**
> The text was classified as positive because it uses phrases with positive connotations, such as 'honest look' and 'striving to anchor itself', which imply a sense of hope and resilience.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `anchor`, `honest`, `look`, `strive`

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
| H–R | 0.3333 | 0.1667 |
| H–CF | 0.6667 | 0.5000 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.3333 | 0.1667 |
| R–RO | 0.3333 | 0.1667 |
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
- **ECS primary pairs:** 4
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
{"rationale": "The text was classified as negative because it uses strongly derogatory language, including 'misogynistic' and 'filth', to express intense disapproval and disdain for the subject."}
```

**Rationale text:**
> The text was classified as negative because it uses strongly derogatory language, including 'misogynistic' and 'filth', to express intense disapproval and disdain for the subject.

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
{"rewritten": "a feminist piece of genius that attempts to pass itself off as hip , young adult entertainment . ", "new_prediction": "positive"}
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
- **ECS (full):** 0.1148
- **ECS (extraction–rationale):** 0.0588
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
{"salience": {
"care": 6, 
"deftly": 4, 
"captures": 5, 
"the": 1, 
"wonder": 3, 
"and": 1, 
"menace": 3, 
"of": 1, 
"growing": 3, 
"up": 2, 
"but": 8, 
"he": 2, 
"never": 9, 
"really": 7, 
"embraces": 8, 
"the": 1, 
"joy": 4, 
"of": 1, 
"fuhrman": 2, 
"'s": 1, 
"destructive": 5, 
"escapism": 5, 
"or": 1, 
"the": 1, 
"grace-in-rebellion": 5, 
"found": 4, 
"by": 1, 
"his": 2, 
"characters": 3
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `captures`, `care`, `destructive`, `embraces`, `never`, `really`

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
- Tokens: `capture`, `care`, `character`, `embrace`, `find`, `grace`, `grace-in`, `grow`, `joy`, `menace`, `rebellion`, `wonder`

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
| H–R | 0.1667 | 0.0588 |
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
- **ECS (full):** 0.2657
- **ECS (extraction–rationale):** 0.4143
- **ECS (extraction–perturbation):** 0.2500
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `contradiction`
- **CC3 size:** 3 | **CC4 size:** 0

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
"Christendom": 3, 
"by": 2, 
"slaughtering": 4, 
"both": 2, 
"Muslims": 3, 
"and": 2, 
"Jews": 3, 
"Premise": 1, 
"Premise": 1, 
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
- Tokens: `1099`, `captured`, `city`, `crusaders`, `holy`, `slaughtering`

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
{"rationale": "The premise directly states that the Crusaders captured the Holy City, which is exactly what the hypothesis claims, making the hypothesis a logical and direct consequence of the premise."}
```

**Rationale text:**
> The premise directly states that the Crusaders captured the Holy City, which is exactly what the hypothesis claims, making the hypothesis a logical and direct consequence of the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `capture`, `city`, `crusaders`, `holy`

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
| H–R | 0.7500 | 0.4286 |
| H–CF | 1.0000 | 0.1667 |
| H–RO | 1.0000 | 0.5000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.6667 | 0.4000 |
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
- **ECS (full):** 0.1500
- **ECS (extraction–rationale):** 0.2500
- **ECS (extraction–perturbation):** 0.2000
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
  "Premise:": 2, 
  "we": 8, 
  "only": 9, 
  "have": 8, 
  "to": 6, 
  "get": 8, 
  "up": 8, 
  "for": 6, 
  "you": 4, 
  "know": 2, 
  "for": 6, 
  "the": 5, 
  "daytime": 10, 
  "feedings": 10, 
  "Hypothesis:": 2, 
  "We": 8, 
  "only": 9, 
  "have": 8, 
  "to": 6, 
  "get": 8, 
  "up": 8, 
  "for": 6, 
  "the": 5, 
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
{"rewritten": "Premise: we only have to get up for you know for the daytime feedings\nHypothesis: We have to get up for the nighttime feedings.", "new_prediction": "contradiction"}
```

**CF stages:**
- JSON parsed: Yes
- Rules compliant: Yes
- Flip verified: Yes
- Actual label: `contradiction`

**Reconstructed text:**
> Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We have to get up for the nighttime feedings.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `daytime`, `only`

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
| H–CF | 0.5000 | 0.2000 |
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
- **ECS (full):** 0.0769
- **ECS (extraction–rationale):** 0.0769
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `entailment`
- **CC3 size:** 0 | **CC4 size:** 0

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
  "If": 2, 
  "necessary": 6, 
  "to": 1, 
  "meeting": 4, 
  "the": 1, 
  "restrictions": 8, 
  "imposed": 3, 
  "in": 1, 
  "the": 1, 
  "preceding": 5, 
  "sentence": 3, 
  "the": 1, 
  "Administrator": 4, 
  "shall": 2, 
  "reduce": 7, 
  "pro": 2, 
  "rata": 2, 
  "the": 1, 
  "basic": 6, 
  "Phase": 8, 
  "II": 8, 
  "allowance": 9, 
  "allocations": 9, 
  "for": 1, 
  "each": 3, 
  "unit": 6, 
  "subject": 5, 
  "to": 1, 
  "the": 1, 
  "requirements": 8, 
  "of": 1, 
  "section": 8, 
  "414": 10, 
  "Hypothesis": 1, 
  "Section": 8, 
  "414": 10, 
  "helps": 6, 
  "balance": 8, 
  "allowance": 9, 
  "allocations": 9, 
  "for": 1, 
  "units": 6
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `414`, `allocations`, `allowance`, `ii`, `phase`, `requirements`, `restrictions`, `section`

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
- Tokens: `allocation`, `allowance`, `balance`, `help`, `requirement`, `section`, `unit`

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
{"rewritten": "Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the requirements of section 414. Hypothesis: Section 414 hinders balance in allowance allocations for units.", "new_prediction": "contradiction"}
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
| H–R | 0.2857 | 0.1538 |
| H–CF | — | — |
| H–RO | 0.3333 | 0.1000 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0865 |

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

Text: "Premise: Favorite items that will help preserve your memories of the rugged Lakeland countryside are clothing or blankets made from the local Herdwick wool, coasters of polished slate, or walking sticks with ram's-horn handles.
Hypothesis: They don't sell any souveineers."

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {
"Premise:": 2, 
"Favorite": 4, 
"items": 6, 
"that": 2, 
"will": 2, 
"help": 4, 
"preserve": 4, 
"your": 2, 
"memories": 6, 
"of": 2, 
"the": 2, 
"rugged": 4, 
"Lakeland": 6, 
"countryside": 6, 
"are": 4, 
"clothing": 8, 
"or": 2, 
"blankets": 8, 
"made": 4, 
"from": 2, 
"the": 2, 
"local": 6, 
"Herdwick": 8, 
"wool,": 8, 
"coasters": 8, 
"of": 2, 
"polished": 6, 
"slate,": 8, 
"or": 2, 
"walking": 8, 
"sticks": 8, 
"with": 2, 
"ram's-horn": 8, 
"handles.": 6, 
"Hypothesis:": 2, 
"They": 6, 
"don't": 10, 
"sell": 10, 
"any": 8, 
"souveineers.": 10, 
"Text:": 1, 
"Premise:": 1, 
"Favorite": 1, 
"items": 1, 
"that": 1, 
"will": 1, 
"help": 1, 
"preserve": 1, 
"your": 1, 
"memories": 1, 
"of": 1, 
"the": 1, 
"rugged": 1, 
"Lakeland": 1, 
"countryside": 1, 
"are": 1, 
"clothing": 1, 
"or": 1, 
"blankets": 1, 
"made": 1, 
"from": 1, 
"the": 1, 
"local": 1, 
"Herdwick": 1, 
"wool,": 1, 
"coasters": 1, 
"of": 1, 
"polished": 1, 
"slate,": 1, 
"or": 1, 
"walking": 1, 
"sticks": 1, 
"with": 1, 
"ram's-horn": 1, 
"handles.": 1, 
"Hypothesis:": 1, 
"They": 1, 
"don't": 1, 
"sell": 1, 
"any": 1, 
"souveineers.": 1, 
"Analyze": 1, 
"the": 1, 
"importance": 1, 
"of": 1, 
"each": 1, 
"word": 1, 
"for": 1, 
"this": 1, 
"classification.": 1, 
"Give": 1, 
"every": 1, 
"word": 1, 
"an": 1, 
"importance": 1, 
"score": 1, 
"from": 1, 
"1": 1, 
"(irrelevant)": 1, 
"to": 1, 
"10": 1, 
"(decisive),": 1, 
"using": 1, 
"each": 1, 
"word": 1, 
"exactly": 1, 
"as": 1, 
"it": 1, 
"appears": 1, 
"in": 1, 
"the": 1, 
"text.": 1, 
"Return": 1, 
"only": 1, 
"valid": 1, 
"JSON:": 1, 
"{"salience":": 1, 
"{": 1, 
"word":": 1, 
"score,": 1, 
"...}": 1, 
"}": 1
}}
```

**Parsed tokens:**
- *Not parsed*

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
- Tokens: `help`, `item`, `memory`, `preserve`, `sell`

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
| H–R | — | — |
| H–CF | — | — |
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
- **ECS (full):** 0.2606
- **ECS (extraction–rationale):** 0.3141
- **ECS (extraction–perturbation):** 0.2374
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `entailment`
- **CC3 size:** 4 | **CC4 size:** 0

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
"Pier": 6, 
"Premise": 2, 
"The": 1, 
"Santa": 4, 
"Monica": 4, 
"is": 3, 
"the": 1, 
"coastal": 5, 
"setting": 5, 
"for": 3, 
"Twilight": 8, 
"Dance": 8, 
"Series": 8, 
"a": 2, 
"selection": 4, 
"of": 2, 
"free": 4, 
"summer": 4, 
"concerts": 6, 
"arranged": 4, 
"each": 3, 
"year": 3, 
"Hypothesis": 2, 
"also": 7, 
"hosts": 7, 
"events": 7, 
"directly": 9, 
"on": 9, 
"beach": 9, 
"near": 6, 
"the": 1, 
"pier": 6
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `dance`, `directly`, `events`, `hosts`, `series`, `twilight`

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
{"rationale": "The premise only mentions that the Twilight Dance Series takes place at the Santa Monica Pier, but does not provide information about whether events are also hosted directly on the beach near the pier, making the hypothesis neither entailed nor contradicted by the premise."}
```

**Rationale text:**
> The premise only mentions that the Twilight Dance Series takes place at the Santa Monica Pier, but does not provide information about whether events are also hosted directly on the beach near the pier, making the hypothesis neither entailed nor contradicted by the premise.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `also`, `beach`, `dance`, `directly`, `event`, `host`, `monica`, `pier`, `santa`, `series`, `twilight`

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
{"ranking": ["pier", "series", "setting"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `pier`(1), `series`(2), `setting`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.7500 | 0.4615 |
| H–CF | 0.5714 | 0.3636 |
| H–RO | 0.3333 | 0.1000 |
| R–CF | 0.4286 | 0.2000 |
| R–RO | 0.6667 | 0.1667 |
| CF–RO | 0.3333 | 0.1111 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0000 |


## High-ECS Examples

### sst2_validation_000188 (ECS=0.7333)
- **Dataset:** sst2
- **Text:** a misogynistic piece of filth that attempts to pass itself off as hip , young adult entertainment . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_000657 (ECS=0.4905)
- **Dataset:** sst2
- **Text:** expect the same-old , lame-old slasher nonsense , just with different scenery . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓

### sst2_validation_000361 (ECS=0.4167)
- **Dataset:** sst2
- **Text:** a very long movie , dull in stretches , with entirely too much focus on meal preparation and igloo construction . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓


## Low-ECS Examples

### sst2_validation_000665 (ECS=0.0422)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_007556 (ECS=0.0769)
- **Dataset:** mnli
- **Text:** Premise: If necessary to meeting the restrictions imposed in the preceding sentence, the Administrator shall reduce, pro rata, the basic Phase II allowance allocations for each unit subject to the req…
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓

### sst2_validation_000513 (ECS=0.1148)
- **Dataset:** sst2
- **Text:** care deftly captures the wonder and menace of growing up , but he never really embraces the joy of fuhrman 's destructive escapism or the grace-in-rebellion found by his characters . 
- **Ground truth:** `negative` → **Predicted:** `negative` ✓
