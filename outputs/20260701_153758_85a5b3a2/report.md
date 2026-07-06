# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-01 15:38:08
- **Duration:** 285.2s (4.8m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 11
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 26153
- **Avg tokens per instance:** 2378

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 7 | 7/7 (100%) | 0.356 | 100% | 100% | 86% | 86% |
| mnli | 4 | 2/4 (50%) | 0.201 | 100% | 100% | 100% | 50% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 7 | 7 | 0 |
| mnli | 7 | 7 | 2 |
| **Total** | 14 | 14 | 2 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=4) or medium-length (21–50 words, N=7). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=6). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=7)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 11/11 | 100% |
| Rationale | 11/11 | 100% |
| Counterfactual | 10/11 | 91% |
| Rank Ordering | 8/11 | 73% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=11) | 0.3001 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.2914 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.3363 |
| Mean ECS (complete cases, N=7) | 0.3368 |
| Complete cases | 7/11 (64%) |
| Std ECS | 0.1921 |
| Median ECS | 0.2400 |
| **Mean ECS lift over chance** (ECS − random) | +0.1929 |
| Mean ECS random baseline | 0.1071 |

> **No significance testing applied.** The lift, correct-vs-incorrect split, length/vocab strata, and any other comparison above are point estimates (plus the bootstrap CI on mean ECS where shown) — no hypothesis test or multiple-comparison correction has been run, regardless of what `config/experiment.yaml` declares. At this pilot N, treat every comparison in this report as descriptive.

| Mean ECS — correct preds (N=9) | 0.3234 |
| Mean ECS — incorrect preds (N=2) | 0.1950 |
| Introduced-concept rate (R) | 0.721 |
| CF canonical (minimal) validity rate | 91% |
| CF contrast (free) validity rate | 82% |
| CF canonical (minimal) minimality (edits/len) | 0.126 |
| CF contrast (free) minimality (edits/len) | 0.208 |
| Confidence elicitation | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size | 1.45 |
| Mean CC4 size | 0.91 |
| % instances with CC3 | 72.7% |
| % instances with CC4 | 63.6% |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.6364 | 0.3075 |
| H–CF | 0.7167 | 0.3262 |
| H–RO | 0.8750 | 0.5567 |
| R–CF | 0.4333 | 0.2393 |
| R–RO | 0.5417 | 0.2982 |
| CF–RO | 0.7619 | 0.3968 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.2574 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported here as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — for interpreting individual pairs, not for the headline number. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 11/11 (100%) | 11/11 (100%) |
| Rationale | 11/11 (100%) | 11/11 (100%) |
| Counterfactual (JSON parsed) | 11/11 (100%) |
| Counterfactual (rules compliant) | 11/11 (100%) |
| Counterfactual (flip verified) | 10/11 (91%) |
| Rank Ordering | 8/11 (73%) | 8/11 (73%) |
| All 4 valid | 7/11 |
| 3 valid (CC3 adjusted) | 4/11 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 4 | 0.4339 |
| Medium (21–50) | 7 | 0.2236 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 5 | 0.1997 |
| Short vocab (≤20 unique tokens) | 6 | 0.3837 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.3001 | [0.2090, 0.4222] |

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
> and if you 're not nearly moved to tears by a couple of scenes , you 're utterly despicable .

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
{"salience": {"a": 2, "very": 6, "long": 8, "movie": 4, "dull": 9, "in": 2, "stretches": 7, "with": 3, "entirely": 5, "too": 6, "much": 6, "focus": 4, "on": 2, "meal": 4, "preparation": 4, "and": 2, "igloo": 4, "construction": 4, "": 1}}
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
{"salience": {"whether": 2, "writer-director": 4, "anne": 3, "fontaine": 3, "s": 1, "film": 5, "is": 1, "a": 1, "ghost": 6, "story": 6, "an": 1, "account": 5, "of": 1, "a": 1, "nervous": 6, "breakdown": 6, "a": 1, "trip": 5, "down": 4, "memory": 7, "lane": 6, "all": 2, "three": 2, "or": 2, "none": 2, "of": 1, "the": 1, "above": 2, "it": 1, "is": 1, "as": 8, "seductive": 9, "as": 8, "it": 1, "is": 1, "haunting": 9}}
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
- **ECS (full):** 0.3619
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** 0.5000
- **ECS primary pairs:** 4
- **Valid strategies:** 4
- **CF flip verified:** Yes
- **CF actual label:** `negative`
- **CC3 size:** 3 | **CC4 size:** 1

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
- Tokens: `anchor`, `community`, `honest`, `look`, `strive`

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
| H–R | 0.6667 | 0.3333 |
| H–CF | 0.6667 | 0.5000 |
| H–RO | 1.0000 | 1.0000 |
| R–CF | 0.3333 | 0.1429 |
| R–RO | 0.6667 | 0.3333 |
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
{"rationale": "The text was classified as negative because it uses strongly derogatory language, such as 'misogynistic' and 'filth', to express intense disapproval and disgust towards the subject."}
```

**Rationale text:**
> The text was classified as negative because it uses strongly derogatory language, such as 'misogynistic' and 'filth', to express intense disapproval and disgust towards the subject.

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
- **ECS (full):** 0.2262
- **ECS (extraction–rationale):** 0.1429
- **ECS (extraction–perturbation):** 0.2857
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** Yes
- **CF actual label:** `positive`
- **CC3 size:** 1 | **CC4 size:** 1

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
"care": 4, 
"deftly": 3, 
"captures": 5, 
"the": 1, 
"wonder": 6, 
"and": 2, 
"menace": 6, 
"of": 1, 
"growing": 5, 
"up": 4, 
"but": 8, 
"he": 3, 
"never": 9, 
"really": 7, 
"embraces": 8, 
"the": 1, 
"joy": 6, 
"of": 1, 
"fuhrman": 2, 
"'s": 1, 
"destructive": 7, 
"escapism": 6, 
"or": 2, 
"the": 1, 
"grace-in-rebellion": 6, 
"found": 5, 
"by": 2, 
"his": 3, 
"characters": 4
}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `destructive`, `embraces`, `menace`, `never`, `really`, `wonder`

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
{"rationale": "The text was classified as negative because although it starts with a positive statement, it ultimately expresses a criticism that the subject 'never really embraces' a key aspect of the work, implying a limitation or shortfall."}
```

**Rationale text:**
> The text was classified as negative because although it starts with a positive statement, it ultimately expresses a criticism that the subject 'never really embraces' a key aspect of the work, implying a limitation or shortfall.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `embrace`, `really`

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
| H–R | 0.5000 | 0.1429 |
| H–CF | 0.6667 | 0.2857 |
| H–RO | — | — |
| R–CF | 0.5000 | 0.2500 |
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
"Godfrey": 2, 
"de": 1, 
"Bouillon": 2, 
"and": 2, 
"Tancred": 2, 
"the": 2, 
"Crusaders": 8, 
"captured": 9, 
"the": 2, 
"Holy": 6, 
"City": 6, 
"for": 2, 
"Christendom": 4, 
"by": 2, 
"slaughtering": 3, 
"both": 2, 
"Muslims": 3, 
"and": 2, 
"Jews": 3, 
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
- Tokens: `1099`, `captured`, `christendom`, `city`, `crusaders`, `holy`

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
{"rationale": "The premise and hypothesis are virtually identical in meaning, with the premise's informal phrase 'you know' being the only difference, which does not affect the overall logical relationship between the two statements."}
```

**Rationale text:**
> The premise and hypothesis are virtually identical in meaning, with the premise's informal phrase 'you know' being the only difference, which does not affect the overall logical relationship between the two statements.

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

### mnli_validation_matched_007919 (ECS=0.1500)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗

### mnli_validation_matched_007354 (ECS=0.1500)
- **Dataset:** mnli
- **Text:** Premise: we only have to get up for you know for the daytime feedings
Hypothesis: We only have to get up for the daytime feedings.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
