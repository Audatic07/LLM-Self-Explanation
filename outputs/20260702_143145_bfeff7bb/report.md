# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-07-02 14:31:54
- **Duration:** 174.9s (2.9m)
- **Models (2):** nova-pro (`eu.amazon.nova-pro-v1:0`), qwen3-235b (`qwen.qwen3-235b-a22b-2507-v1:0`)
- **Total instances:** 6
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 14397
- **Avg tokens per instance:** 2400

## Per-Dataset Summary

| Model | Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|-------|---------|-----------|----------|----------|---|---|------|---|
| claude-haiku-4.5 | sst2 | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| nova-pro | sst2 | 1 | 0/1 (0%) | 0.000 | 0% | 0% | 0% | 0% |
| qwen3-235b | sst2 | 1 | 1/1 (100%) | 0.000 | 100% | 100% | 0% | 100% |
| claude-haiku-4.5 | mnli | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| nova-pro | mnli | 1 | 1/1 (100%) | 0.333 | 100% | 100% | 0% | 100% |
| qwen3-235b | mnli | 1 | 1/1 (100%) | 0.333 | 100% | 100% | 0% | 100% |
| claude-haiku-4.5 | ag_news | 0 | — | 0.000 | 0% | 0% | 0% | 0% |
| nova-pro | ag_news | 1 | 1/1 (100%) | 0.396 | 100% | 100% | 0% | 100% |
| qwen3-235b | ag_news | 1 | 1/1 (100%) | 0.500 | 100% | 100% | 0% | 100% |

## Sampling Log

| Model | Dataset | Requested | Sampled | Wrong Pred |
|-------|---------|-----------|---------|------------|
| claude-haiku-4.5 | sst2 | 0 | 0 | 0 |
| nova-pro | sst2 | 0 | 0 | 0 |
| qwen3-235b | sst2 | 1 | 1 | 0 |
| claude-haiku-4.5 | mnli | 0 | 0 | 0 |
| nova-pro | mnli | 1 | 1 | 0 |
| qwen3-235b | mnli | 1 | 1 | 0 |
| claude-haiku-4.5 | ag_news | 0 | 0 | 0 |
| nova-pro | ag_news | 1 | 1 | 0 |
| qwen3-235b | ag_news | 1 | 1 | 0 |
| **Total** | | 5 | 5 | 0 |

**Note:** No long inputs (>50 words) were sampled. All instances are short (≤20 words, N=2) or medium-length (21–50 words, N=3). ECS may partly reflect brevity.

**Short-vocab filter:** Instances with ≤20 unique normalized tokens are flagged `short_vocab` (N=2). These degenerate inputs yield inflated/trivial ECS via near-identical evidence across strategies. Compare filtered results below.

## Overview — Two Analysis Regimes

### Analysis A: Complete Cases (all 4 strategies valid, N=0)

This is the clean statistical analysis: instances where Highlighting, Rationale, Counterfactual, and Rank Ordering all produced valid evidence.

### Analysis B: Coverage

| Strategy | Valid / Total | Rate |
|----------|---------------|------|
| Highlighting | 6/6 | 100% |
| Rationale | 5/6 | 83% |
| Counterfactual | 0/6 | 0% |
| Rank Ordering | 6/6 | 100% |

Coverage varies dramatically — Counterfactual is the least reliable method. This is itself a finding: explanation methods differ substantially in reliability.

**Design note:** H (graded salience) and RO (ranked selection) belong to the same extraction-based paradigm. Their pairwise agreement is excluded from ECS; overlap is measured via Overlap Coefficient, rank agreement via Kendall τ and RBO. The three genuinely distinct paradigms are: extraction (H/RO), rationalization (R), and perturbation (CF).


## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS (all, N=6) | 0.3125 |
| Mean ECS (extraction–rationale: H,R,RO) | 0.3125 |
| Mean ECS (extraction–perturbation: H,CF,RO) | 0.0000 |
| Mean ECS (complete cases, N=0) | 0.0000 |
| Complete cases | 0/6 (0%) |
| Std ECS | 0.1875 |
| Median ECS | 0.3333 |
| **Mean ECS lift over chance** (ECS − random) | +0.2241 |
| Mean ECS random baseline | 0.0884 |

> **No significance testing applied.** The lift, correct-vs-incorrect split, length/vocab strata, and any other comparison above are point estimates (plus the bootstrap CI on mean ECS where shown) — no hypothesis test or multiple-comparison correction has been run, regardless of what `config/experiment.yaml` declares. At this pilot N, treat every comparison in this report as descriptive.

| Mean ECS — correct preds (N=5) | 0.3125 |
| Mean ECS — incorrect preds (N=0) | 0.0000 |
| Introduced-concept rate (R) | 0.769 |
| CF canonical (minimal) validity rate | 0% |
| CF contrast (free) validity rate | 50% |
| CF canonical (minimal) minimality (edits/len) | 0.000 |
| CF contrast (free) minimality (edits/len) | 0.359 |
| Confidence elicitation | Removed — logprobs unsupported on this model; does not proxy faithfulness |
| Mean CC3 size | 1.00 |
| Mean CC4 size | 1.00 |
| % instances with CC3 | 66.7% |
| % instances with CC4 | 66.7% |

> **Framing.** ECS is an inter-method **consistency** measure, reported as **lift over a random baseline** (raw overlap is confounded by set size and vocabulary). It is **not** a faithfulness score. The erasure pass (`aggregate_erasure.json`, run separately via `run_validity_tests.py`) is a **second consistency axis** (comprehensiveness-style, stated-vs-revealed input sensitivity) — not ground truth; its headline is Consensus-Core erasure vs. a same-size random control, by ECS-lift tier.

### Pairwise Agreement (Overlap Coefficient)

| Pair | Overlap Coeff (mean) | Jaccard (mean) |
|------|----------------------|----------------|
| H–R | 0.7267 | 0.3917 |
| H–CF | 0.0000 | 0.0000 |
| H–RO | 0.6278 | 0.4643 |
| R–CF | 0.0000 | 0.0000 |
| R–RO | 0.5700 | 0.2333 |
| CF–RO | 0.0000 | 0.0000 |

### Rank-Based Agreement (H vs RO)

| Metric | Value |
|--------|-------|
| RBO (H,RO) | 0.0766 |
| Kendall τ (H,RO) | 0.0000 |
| Normalized τ | 0.0000 |

> Jaccard is what feeds the headline ECS and ECS-lift (both computed from Jaccard pairwise agreement, never Overlap Coefficient). Overlap Coefficient is reported here as a size-robust complement — unlike Jaccard, it is not penalized by smaller salience sets — for interpreting individual pairs, not for the headline number. RBO measures top-weighted rank agreement between H's graded salience order and RO's selected ranking; Kendall τ provides a complementary rank correlation measure.

### Validation Rates (strict)

| Strategy | Parsed | Valid |
|----------|--------|-------|
| Highlighting | 6/6 (100%) | 6/6 (100%) |
| Rationale | 5/6 (83%) | 5/6 (83%) |
| Counterfactual (JSON parsed) | 5/6 (83%) |
| Counterfactual (rules compliant) | 1/6 (17%) |
| Counterfactual (flip verified) | 0/1 (0%) |
| Rank Ordering | 6/6 (100%) | 6/6 (100%) |
| All 4 valid | 0/6 |
| 3 valid (CC3 adjusted) | 5/6 |

CC is computed over valid strategies only. When CF is missing, CC3-of-3 replaces CC4-of-4.
ECS is computed using validated outputs only. The H–RO pair is excluded (same paradigm family). Full ECS averages the 5 remaining cross-paradigm pairs (all Jaccard). Primary ECS is two composites: extraction–rationale averages (H,R) and (R,RO); extraction–perturbation averages (H,CF) and (CF,RO). H–RO agreement is measured via Overlap Coefficient (set), Kendall τ (rank correlation), and RBO (top-weighted rank).

### ECS by Input Length

| Length | N | Mean ECS |
|--------|---|----------|
| Short (≤20 words) | 2 | 0.3333 |
| Medium (21–50) | 3 | 0.2986 |
| Long (>50 words) | 0 | 0.0000 |


### ECS by Vocabulary Size

| Vocab Bucket | N | Mean ECS |
|--------------|---|----------|
| Normal vocab (>20 unique tokens) | 3 | 0.2986 |
| Short vocab (≤20 unique tokens) | 2 | 0.3333 |

> The normal-vocab column gives a more conservative, reliable ECS estimate by excluding degenerate instances.

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.3125 | [0.1458, 0.4333] |

## Per-Instance Details

### sst2_validation_000665 — nova-pro

> **SKIPPED**: Wrong prediction — no explanation strategies elicited, no ECS computed.

- **Ground truth:** `positive`
- **Predicted:** `negative` ✗
- **Input length:** 24 words
- **Raw response length:** 25 chars

### sst2_validation_000665 — qwen3-235b

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
{"salience": {"and": 2, "if": 5, "you": 6, "'re": 4, "not": 8, "nearly": 6, "moved": 9, "to": 5, "tears": 9, "by": 3, "a": 2, "couple": 4, "of": 2, "scenes": 7, ",": 1, "you": 6, "'ve": 4, "got": 5, "ice": 7, "water": 6, "in": 3, "your": 5, "veins": 7, ".": 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `moved`, `not`, `scenes`, `tears`

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
{"rationale": "The text expresses strong emotional praise for the scenes, implying they are profoundly moving and impactful."}
```

**Rationale text:**
> The text expresses strong emotional praise for the scenes, implying they are profoundly moving and impactful.

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
{"rewritten": "and if you're not nearly moved to tears by a couple of scenes, you've got ice water in your veins—what a disappointment.", "new_prediction": "negative"}
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
{"ranking": ["tears", "moved", "ice", "veins"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `tears`(1), `moved`(2), `ice`(3), `veins`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.0000 | 0.0000 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.3333 |
| R–CF | — | — |
| R–RO | 0.0000 | 0.0000 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.1804 |

### mnli_validation_matched_007919 — nova-pro

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened

Does the premise entail the hypothesis, contradict it, or is it neutral?

Return only valid JSON:
{"label":"entailment, neutral, or contradiction"}
```

#### 2. Classification Response
```
{
  "label": "neutral"
}
```

#### 3. Ground Truth & Prediction
- **Ground truth:** `neutral`
- **Predicted:** `neutral` ✓
- **Model refused:** No
- **Input length:** 16 words
- **Raw response length:** 24 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CF actual label:** `neutral`
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{
  "salience": {
    "just": 3,
    "look": 4,
    "what": 5,
    "we": 6,
    "did": 7,
    "to": 5,
    "Iraq": 10,
    "Hypothesis:": 6,
    "Iraq": 10,
    "was": 6,
    "something": 7,
    "that": 6,
    "shouldn't": 8,
    "have": 7,
    "happened": 9
  }
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happened`, `iraq`, `something`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{
  "rationale": "The premise does not provide enough information to determine whether the actions taken in Iraq were right or wrong, thus it is neutral with respect to the hypothesis."
}
```

**Rationale text:**
> The premise does not provide enough information to determine whether the actions taken in Iraq were right or wrong, thus it is neutral with respect to the hypothesis.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""entailment" or "contradiction"" instead of "neutral". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{
  "rewritten": "Premise: just look what we did to Iraq\nHypothesis: Iraq was something that should have happened",
  "new_prediction": "contradiction"
}
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

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{
  "ranking": ["Iraq", "did", "look", "happened"]
}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`(1), `look`(2), `happened`(3), `something`(6)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | — | — |
| H–RO | 0.6667 | 0.5000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0634 |

### mnli_validation_matched_007919 — qwen3-235b

#### 1. Classification Prompt
```
Determine the logical relationship between the premise and the hypothesis.

Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened

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
- **Input length:** 16 words
- **Raw response length:** 19 chars
- **Prompt hash:** `82c03589065d7755`
- **ECS (full):** 0.3333
- **ECS (extraction–rationale):** 0.3333
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 1 | **CC4 size:** 1

#### 4. Highlighting Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Analyze the importance of each word for this classification. Give every word an importance score from 1 (irrelevant) to 10 (decisive), using each word exactly as it appears in the text.

Return only valid JSON:
{"salience": {"word": score, ...}}
```

**Response:**
```
{"salience": {"Premise": 5, "just": 6, "look": 5, "what": 7, "we": 4, "did": 8, "to": 3, "Iraq": 9, "Hypothesis": 5, "was": 3, "something": 5, "that": 3, "shouldn't": 9, "have": 4, "happened": 8}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `happened`, `iraq`, `look`

#### 4. Rationale Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

In one sentence, explain why the text was classified as neutral.

Return only valid JSON:
{"rationale": "<one-sentence explanation>"}
```

**Response:**
```
{"rationale": "The premise expresses a reflection on actions taken regarding Iraq but does not explicitly state a judgment about whether those actions should or should not have occurred, leaving the hypothesis neither confirmed nor contradicted."}
```

**Rationale text:**
> The premise expresses a reflection on actions taken regarding Iraq but does not explicitly state a judgment about whether those actions should or should not have occurred, leaving the hypothesis neither confirmed nor contradicted.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`

#### 4. Counterfactual Explanation

**Prompt:**
```
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

The text has a Premise and a Hypothesis. Edit only the Hypothesis so that the relationship is classified as ""entailment" or "contradiction"" instead of "neutral". Make as few edits as possible, and keep the Premise unchanged.

Return the full text (unchanged Premise, edited Hypothesis) in the JSON.

Return only valid JSON:
{"rewritten": "<full text with edited Hypothesis>", "new_prediction": "<one of: entailment, contradiction>"}
```

**Response:**
```
{"rewritten": "Premise: just look what we did to Iraq\nHypothesis: The Iraq intervention was a mistake that should not have happened", "new_prediction": "entailment"}
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
The text was classified as: neutral

Text: "Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened"

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Iraq", "shouldn't", "happened", "look", "did"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `iraq`(1), `look`(2), `happened`(3)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 1.0000 | 0.3333 |
| H–CF | — | — |
| H–RO | 1.0000 | 1.0000 |
| R–CF | — | — |
| R–RO | 1.0000 | 0.3333 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0540 |

### ag_news_test_004983 — nova-pro

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
- **ECS (full):** 0.3958
- **ECS (extraction–rationale):** 0.3958
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
{"salience": {"Nokia": 8, "announces": 7, "Near": 9, "Field": 9, "Communication": 9, "products": 6, "With": 5, "the": 4, "Nokia": 8, "NFC": 10, "(Near": 9, "Field": 9, "Communication)": 9, "shell": 7, "on": 4, "their": 4, "phone,": 6, "consumers": 6, "will": 5, "be": 4, "able": 5, "to": 4, "access": 7, "a": 3, "variety": 6, "of": 4, "services": 7, "and": 4, "exchange": 7, "information": 8, "with": 5, "a": 3, "simple": 6, "touch": 7, "gesture.": 5}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `near`, `nfc`, `nokia`

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
{"rationale": "The text discusses Nokia's announcement of new technology products related to Near Field Communication, which is a scientific and technological advancement."}
```

**Rationale text:**
> The text discusses Nokia's announcement of new technology products related to Near Field Communication, which is a scientific and technological advancement.

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
For "World":
{"rewritten": "Nokia announces Near Field Communication products expansion globally. With the Nokia NFC (Near Field Communication) shell on their phone, consumers worldwide will be able to access a variety of services and exchange information with a simple touch gesture.", "new_prediction": "World"}

For "Sports":
{"rewritten": "Nokia announces Near Field Communication products partnership with major sports leagues. With the Nokia NFC (Near Field Communication) shell on their phone, sports fans will be able to access exclusive content and exchange information with a simple touch gesture.", "new_prediction": "Sports"}

For "Business":
{"rewritten": "Nokia announces Near Field Communication products with a new business model. With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture, enhancing user experience and driving sales.", "new_prediction": "Business"}
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
The text was classified as: Sci/Tech

Text: "Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information with a simple touch gesture."

Identify the 3-5 most important words for this classification, ranked from most to least important. Each item must be a single word copied from the text.

Return only valid JSON:
{"ranking": ["word1", "word2", "word3"]}
```

**Response:**
```
{"ranking": ["Nokia", "NFC", "products", "consumers"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nokia`(1), `nfc`(2), `products`(3), `consumers`(4)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8000 | 0.6667 |
| H–CF | — | — |
| H–RO | 0.5000 | 0.2857 |
| R–CF | — | — |
| R–RO | 0.2500 | 0.1250 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0000 |

### ag_news_test_004983 — qwen3-235b

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
- **ECS (full):** 0.5000
- **ECS (extraction–rationale):** 0.5000
- **ECS (extraction–perturbation):** —
- **ECS primary pairs:** 2
- **Valid strategies:** 3
- **CF flip verified:** No
- **CC3 size:** 3 | **CC4 size:** 3

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
{"salience": {"Nokia": 8, "announces": 6, "Near": 10, "Field": 10, "Communication": 10, "products": 7, "With": 2, "the": 1, "NFC": 10, "(": 1, ")": 1, "shell": 7, "on": 1, "their": 1, "phone": 8, ",": 1, "consumers": 5, "will": 2, "be": 1, "able": 4, "to": 1, "access": 6, "a": 1, "variety": 3, "of": 1, "services": 6, "and": 2, "exchange": 7, "information": 8, "with": 2, "a": 1, "simple": 5, "touch": 7, "gesture": 6, ".": 1}}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `field`, `information`, `near`, `nfc`, `nokia`, `phone`

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
{"rationale": "The text discusses Nokia's announcement of Near Field Communication (NFC) technology, which is a technological innovation related to mobile devices and wireless data exchange."}
```

**Rationale text:**
> The text discusses Nokia's announcement of Near Field Communication (NFC) technology, which is a technological innovation related to mobile devices and wireless data exchange.

**Parsed tokens:**
- Status: **Valid**
- Tokens: `communication`, `exchange`, `field`, `near`, `nfc`, `nokia`

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
{"rewritten": "Nokia announces new business partnership to expand Near Field Communication services globally, enhancing mobile transactions and corporate collaborations.", "new_prediction": "Business"}
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
{"ranking": ["NFC", "Nokia", "Communication", "products", "gesture"]}
```

**Parsed tokens:**
- Status: **Valid**
- Tokens: `nfc`(1), `nokia`(2), `communication`(3), `products`(4), `gesture`(5)

#### 5. Pairwise Agreement

| Pair | Overlap Coeff | Jaccard |
|------|---------------|---------|
| H–R | 0.8333 | 0.6250 |
| H–CF | — | — |
| H–RO | 0.6000 | 0.3333 |
| R–CF | — | — |
| R–RO | 0.6000 | 0.3750 |
| CF–RO | — | — |
| Kendall τ (H,RO) | — |
| Normalized τ | — |
| RBO (H,RO) | 0.0000 |


## High-ECS Examples

### ag_news_test_004983 (ECS=0.5000)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### ag_news_test_004983 (ECS=0.3958)
- **Dataset:** ag_news
- **Text:** Nokia announces Near Field Communication products With the Nokia NFC (Near Field Communication) shell on their phone, consumers will be able to access a variety of services and exchange information wi…
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓

### mnli_validation_matched_007919 (ECS=0.3333)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓


## Low-ECS Examples

### sst2_validation_000665 (ECS=0.0000)
- **Dataset:** sst2
- **Text:** and if you 're not nearly moved to tears by a couple of scenes , you 've got ice water in your veins . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓

### mnli_validation_matched_007919 (ECS=0.3333)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓

### mnli_validation_matched_007919 (ECS=0.3333)
- **Dataset:** mnli
- **Text:** Premise: just look what we did to Iraq
Hypothesis: Iraq was something that shouldn't have happened
- **Ground truth:** `neutral` → **Predicted:** `neutral` ✓
