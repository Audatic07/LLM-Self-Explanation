# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-02 10:36:51
- **Duration:** 20.7s (0.3m)
- **Model:** us.meta.llama3-3-70b-instruct-v1:0
- **Total instances:** 6
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 13413
- **Avg tokens per instance:** 2236

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 1 | — | 0.050 | 100% | 100% | 100% | 100% |
| sst2 | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| sst2 | 1 | — | 0.000 | 100% | 100% | 0% | 100% |
| mnli | 1 | — | 0.150 | 100% | 100% | 100% | 0% |
| mnli | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| mnli | 1 | — | 0.000 | 0% | 0% | 0% | 0% |
| ag_news | 1 | — | 0.171 | 100% | 100% | 0% | 100% |
| ag_news | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| ag_news | 1 | — | 0.062 | 100% | 100% | 0% | 100% |

## Sampling Log

| Dataset | Requested | Sampled | Wrong Pred |
|---------|-----------|---------|------------|
| sst2 | 1 | 1 | 0 |
| sst2 | 0 | 0 | 0 |
| sst2 | 1 | 1 | 0 |
| mnli | 1 | 1 | 1 |
| mnli | 0 | 0 | 0 |
| mnli | 0 | 0 | 0 |
| ag_news | 1 | 1 | 0 |
| ag_news | 0 | 0 | 0 |
| ag_news | 1 | 1 | 0 |
| **Total** | 5 | 5 | 1 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=1) or medium-length (21–50 words, N=4). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=1). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=1)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 6/6 | 100% |
| Rationale | 6/6 | 100% |
| Counterfactual | 2/6 | 33% |
| Rank Ordering | 4/6 | 67% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=6) | 0.0868 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.0968 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.1625 |
| Mean ECS (complete cases, N=1) | 0.0500 |
| Complete cases | 1/6 (17%) |
| Std ECS | 0.0718 |
| Median ECS | 0.0625 |
| **Mean ECS lift over chance** (ECS − random) | +0.0023 |
| Mean ECS random baseline | 0.0845 |

> **No significance testing applied.** The lift, correct-vs-incorrect split, length/vocab strata, and any other comparison above are point estimates (plus the bootstrap CI on mean ECS where shown) — no hypothesis test or multiple-comparison correction has been run, regardless of what `config/experiment.yaml` declares. At this pilot N, treat every comparison in this report as descriptive.

| Mean ECS — correct preds (N=4) | 0.0710 |
| Mean ECS — incorrect preds (N=1) | 0.1500 |
| Introduced-concept rate (R) | 0.778 |
| CF canonical (minimal) validity rate | 33% |
| CF contrast (free) validity rate | 83% |
| CF canonical (minimal) minimality (edits/len) | 0.115 |
| CF contrast (free) minimality (edits/len) | 0.367 |
| Confidence elicitation | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size | 0.17 |
| Mean CC4 size | 0.17 |
| % instances with CC3 | 16.7% |
| % instances with CC4 | 16.7% |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.2889 | 0.1375 |
| H–CF | 0.6667 | 0.2250 |
| H–RO | 0.7917 | 0.4643 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0833 | 0.0357 |
| CF–RO | 0.0000 | 0.0000 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.1495 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported here as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — for interpreting individual pairs, not for the headline number. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 6/6 (100%) | 6/6 (100%) |
| Rationale | 6/6 (100%) | 6/6 (100%) |
| Counterfactual (JSON parsed) | 5/6 (83%) |
| Counterfactual (rules compliant) | 2/6 (33%) |
| Counterfactual (flip verified) | 2/2 (100%) |
| Rank Ordering | 4/6 (67%) | 4/6 (67%) |
| All 4 valid | 1/6 |
| 3 valid (CC3 adjusted) | 4/6 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 1 | 0.1500 |
| Medium (21–50) | 4 | 0.0710 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 4 | 0.0710 |
| Short vocab (≤20 unique tokens) | 1 | 0.1500 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.0868 | [0.0325, 0.1411] |

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
- **ECS (full):** 0.0500
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** 0.1250
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
{"salience": {"and": 2, "if": 4, "you": 6, "re": 3, "not": 8, "nearly": 5, "moved": 9, "to": 4, "tears": 9, "by": 4, "a": 2, "couple": 5, "of": 2, "scenes": 7, "you": 6, "ve": 3, "got": 4, "ice": 8, "water": 8, "in": 4, "your": 6, "veins": 8}}
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
| H–CF | 1.0000 | 0.2500 |
| H–RO | 0.6667 | 0.4000 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | 0.0000 | 0.0000 |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1804 |

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
```json
{
  "label": "positive"
}
```
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `positive`
- **Predicted:** `positive` ✓
- **Model refused:** No
- **Input length:** 24 words
- **Raw response length:** 37 chars
- **Prompt hash:** `3c96c3fc1045fafc`
- **ECS (full):** 0.0000
- **ECS (extraction–rationale):** 0.0000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
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
```json
{
  "salience": {
    "and": 1,
    "if": 2,
    "you": 3,
    "'re": 3,
    "not": 8,
    "nearly": 7,
    "moved": 10,
    "to": 4,
    "tears": 9,
    "by": 3,
    "a": 2,
    "couple": 4,
    "of": 2,
    "scenes": 6,
    ",": 1,
    "you": 3,
    "'ve": 3,
    "got": 5,
    "ice": 8,
    "water": 6,
    "in": 3,
    "your": 3,
    "veins": 7,
    ".": 1
  }
}
```
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
```json
{
  "rationale": "The text conveys strong emotional engagement and admiration, implying that the scenes are deeply moving and impactful, which reflects a positive sentiment."
}
```
```

**Rationale text:**
> The text conveys strong emotional engagement and admiration, implying that the scenes are deeply moving and impactful, which reflects a positive sentiment.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `move`, `scene`

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
```json
{
  "rewritten": "and if you're not nearly repulsed by a couple of scenes, you've got ice water in your veins.",
  "new_prediction": "negative"
}
```
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
The text was classified as: positive

Text: "and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . "

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
```json
{
  "ranking": ["moved", "tears", "ice", "veins", "scenes"]
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `moved`(1), `tears`(2), `ice`(3), `veins`(4), `scenes`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.6000 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.3380 |

### mnli_validation_matched_007919

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 16 words
- **Raw response length:** 22 chars

### mnli_validation_matched_007919

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `neutral`
- **Predicted:** `entailment` ✗
- **Input length:** 16 words
- **Raw response length:** 34 chars

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
- **ECS (full):** 0.1714
- **ECS (extraction–rationale):** 0.1714
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
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
"Nokia": 4, 
"NFC": 10, 
"(Near": 3, 
"Field": 3, 
"Communication)": 3, 
"shell": 5, 
"on": 2, 
"their": 2, 
"phone": 8, 
"consumers": 4, 
"will": 2, 
"be": 1, 
"able": 2, 
"to": 1, 
"access": 6, 
"a": 1, 
"variety": 4, 
"of": 1, 
"services": 7, 
"and": 2, 
"exchange": 6, 
"information": 8, 
"with": 2, 
"a": 1, 
"simple": 5, 
"touch": 7, 
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
{"rationale": "The text was classified as Sci/Tech because it discusses a technological innovation, specifically Nokia's Near Field Communication products and their applications, which falls under the category of science and technology."}
```

**Rationale text:**
> The text was classified as Sci/Tech because it discusses a technological innovation, specifically Nokia's Near Field Communication products and their applications, which falls under the category of science and technology.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `nokia`, `product`

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
{"rewritten": "Nokia announces major investment in new factory, creating hundreds of jobs, with the introduction of Near Field Communication products", "new_prediction": "Business"}
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
{"ranking": ["NFC", "phone", "Communication"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `phone`(2), `communication`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.4000 | 0.2000 |
| H–CF | — | — |
| H–RO | 1.0000 | 0.4286 |
| R–CF | — | — |
| R–RO | 0.3333 | 0.1429 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0488 |

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
```json
{"label":"Sci/Tech"}
```
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech` ✓
- **Model refused:** No
- **Input length:** 35 words
- **Raw response length:** 32 chars
- **Prompt hash:** `d090938e39303f01`
- **ECS (full):** 0.0625
- **ECS (extraction–rationale):** 0.0625
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 0 | **CC4 size:** 0

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
```json
{
  "salience": {
    "Nokia": 8,
    "announces": 6,
    "Near": 5,
    "Field": 5,
    "Communication": 9,
    "products": 7,
    "With": 2,
    "the": 1,
    "NFC": 10,
    "(Near": 4,
    "Field": 5,
    "Communication)": 9,
    "shell": 6,
    "on": 2,
    "their": 2,
    "phone,": 7,
    "consumers": 5,
    "will": 3,
    "be": 2,
    "able": 3,
    "to": 2,
    "access": 6,
    "a": 1,
    "variety": 4,
    "of": 2,
    "services": 6,
    "and": 2,
    "exchange": 7,
    "information": 7,
    "with": 2,
    "simple": 4,
    "touch": 6,
    "gesture.": 5
  }
}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `exchange`, `nfc`, `nokia`, `phone`, `products`

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
```json
{"rationale": "The text discusses a technological innovation (Near Field Communication) in mobile devices, which falls under the Sci/Tech category."}
```
```

**Rationale text:**
> The text discusses a technological innovation (Near Field Communication) in mobile devices, which falls under the Sci/Tech category.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `near`

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
```json
{
  "rewritten": "Nokia expands global partnerships with Near Field Communication products. With the Nokia NFC shell on their phone, consumers worldwide will benefit from enhanced connectivity in financial transactions and public services.",
  "new_prediction": "Business"
}
```
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
```json
{"ranking": ["NFC", "Communication", "products", "phone", "technology"]}
```
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `products`(2), `phone`(3), `services`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.3333 | 0.1250 |
| H–CF | — | — |
| H–RO | 0.7500 | 0.4286 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0306 |


## High-ECS Examples

### ag_news_test_004983 (ECS=0.1714)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### mnli_validation_matched_007919 (ECS=0.1500)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `entailment` ✗

### ag_news_test_004983 (ECS=0.0625)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓


## Low-ECS Examples

### sst2_validation_000665 (ECS=0.0000)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### sst2_validation_000665 (ECS=0.0500)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### ag_news_test_004983 (ECS=0.0625)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
