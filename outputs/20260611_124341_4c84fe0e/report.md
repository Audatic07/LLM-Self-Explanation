# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-11 12:43:50
- **Duration:** 43.2s (0.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 9
- **Model refusals:** 0 (0.0%)
- **Total tokens processed:** 3397
- **Avg tokens per instance:** 377

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 2/2 (100%) | 0.245 | 100% | 100% | 100% | 100% |
| mnli | 3 | 2/3 (67%) | 0.172 | 100% | 100% | 100% | 100% |
| ag_news | 4 | 4/4 (100%) | 0.276 | 100% | 100% | 100% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS | 0.2346 |
| Std ECS | 0.0758 |
| Median ECS | 0.2504 |
| Spearman ρ | 0.1386 (p=0.7221) |
| Mean CC3 size | 4.33 |
| Mean CC4 size | 1.44 |
| % instances with CC3 | 100.0% |
| % instances with CC4 | 77.8% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.1804 |
| H–CF | 0.1862 |
| H–RO | 0.5809 |
| R–CF | 0.1000 |
| R–RO | 0.1999 |
| CF–RO | 0.1602 |

### Parsing & Retention Rates

| Strategy | Success Rate |
|----------|-------------|
| Highlighting | 100.0% |
| Rationale | 100.0% |
| Counterfactual | 100.0% |
| Rank Ordering | 100.0% |
| All 4 parsed (CC possible) | 100.0% |

### Confidence Intervals

| Metric | Estimate | 95% CI |
|--------|----------|--------|
| Mean ECS | 0.2346 | [0.1842, 0.2776] |
| Spearman ρ | 0.1386 | [-0.6078, 0.8271] |

## Per-Instance Details

### sst2_validation_0000
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive`
- **Predicted:** `positive`
- **Confidence:** 100.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 207 + 78
- **Prompt hash:** `db6b904c6c3f3ed7`
- **ECS:** 0.2383
- **CC3 size:** 3 | **CC4 size:** 1

### sst2_validation_0001
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `negative`
- **Predicted:** `negative`
- **Confidence:** 90.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 201 + 144
- **Prompt hash:** `b6a5586d487bdc40`
- **ECS:** 0.2525
- **CC3 size:** 2 | **CC4 size:** 1

### mnli_validation_matched_0000
- **Dataset:** mnli
- **Text:** Jon's defense began to weaken and slow. [SEP] Jon began to lose his strength and defense.
- **Ground truth:** `entailment`
- **Predicted:** `entailment`
- **Confidence:** 95.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 222 + 217
- **Prompt hash:** `347eccb8984acac1`
- **ECS:** 0.2961
- **CC3 size:** 3 | **CC4 size:** 2

### mnli_validation_matched_0001
- **Dataset:** mnli
- **Text:** Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The …
- **Ground truth:** `neutral`
- **Predicted:** ``
- **Confidence:** 0.0%
- **Correct:** ✗
- **Model refused:** No
- **Tokens (prompt + response):** 231 + 268
- **Prompt hash:** `1a31c7dd0ca9cbe6`
- **ECS:** 0.0748
- **CC3 size:** 4 | **CC4 size:** 0

### mnli_validation_matched_0002
- **Dataset:** mnli
- **Text:** It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making e…
- **Ground truth:** `contradiction`
- **Predicted:** `contradiction`
- **Confidence:** 100.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 232 + 264
- **Prompt hash:** `5673d4a6e6c20529`
- **ECS:** 0.1438
- **CC3 size:** 4 | **CC4 size:** 1

### ag_news_test_0000
- **Dataset:** ag_news
- **Text:** Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zo…
- **Ground truth:** `World`
- **Predicted:** `World`
- **Confidence:** 100.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 230 + 100
- **Prompt hash:** `73c33850cfe93a36`
- **ECS:** 0.2605
- **CC3 size:** 3 | **CC4 size:** 2

### ag_news_test_0001
- **Dataset:** ag_news
- **Text:** Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s …
- **Ground truth:** `Sci/Tech`
- **Predicted:** `Sci/Tech`
- **Confidence:** 100.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 226 + 100
- **Prompt hash:** `c5d71843a1b5a727`
- **ECS:** 0.3475
- **CC3 size:** 8 | **CC4 size:** 4

### ag_news_test_0002
- **Dataset:** ag_news
- **Text:** Four players shoot opening-round 66 SEMMES, Ala. -- Grace Park, looking to clinch second place in the Player of the Year…
- **Ground truth:** `Sports`
- **Predicted:** `Sports`
- **Confidence:** 100.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 237 + 118
- **Prompt hash:** `ddfd45fe616b29b5`
- **ECS:** 0.2474
- **CC3 size:** 5 | **CC4 size:** 2

### ag_news_test_0003
- **Dataset:** ag_news
- **Text:** California employee pension fund tenders PeopleSoft shares to &lt;b&gt;...&lt;/b&gt; NOVEMBER 19, 2004 (IDG NEWS SERVICE…
- **Ground truth:** `Business`
- **Predicted:** `Business`
- **Confidence:** 100.0%
- **Correct:** ✓
- **Model refused:** No
- **Tokens (prompt + response):** 224 + 98
- **Prompt hash:** `e0d00644f7696b5e`
- **ECS:** 0.2504
- **CC3 size:** 7 | **CC4 size:** 0


## High-ECS Examples

### ag_news_test_0001 (ECS=0.3475)
- **Dataset:** ag_news
- **Text:** Microsoft #39;s big fix: Security patch now on the market For the past few years, viruses have attacked Microsoft #39;s operating system, Web browser or e-mail programs seemingly on a weekly basis.
- **Ground truth:** `Sci/Tech` → **Predicted:** `Sci/Tech` ✓
- **Confidence:** 100.0%

### mnli_validation_matched_0000 (ECS=0.2961)
- **Dataset:** mnli
- **Text:** Jon's defense began to weaken and slow. [SEP] Jon began to lose his strength and defense.
- **Ground truth:** `entailment` → **Predicted:** `entailment` ✓
- **Confidence:** 95.0%

### ag_news_test_0000 (ECS=0.2605)
- **Dataset:** ag_news
- **Text:** Israeli tank kills three Egyptian troops An Israeli tank has opened fire and killed three Egyptian troops in a border zone near the Gaza Strip after mistaking them for Palestinian arms smugglers, Isra…
- **Ground truth:** `World` → **Predicted:** `World` ✓
- **Confidence:** 100.0%


## Low-ECS Examples

### mnli_validation_matched_0001 (ECS=0.0748)
- **Dataset:** mnli
- **Text:** Respondents to the Board's question on whether the alternatives of presenting costs of Federal mission PP&amp [SEP] The board has bad history with presenting federal costs in the past.
- **Ground truth:** `neutral` → **Predicted:** `` ✗
- **Confidence:** 0.0%

### mnli_validation_matched_0002 (ECS=0.1438)
- **Dataset:** mnli
- **Text:** It is one of those rare cases in which I can please everyone. [SEP] It's one of those situations where I end up making everyone unhappy.
- **Ground truth:** `contradiction` → **Predicted:** `contradiction` ✓
- **Confidence:** 100.0%

### sst2_validation_0000 (ECS=0.2383)
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `positive` → **Predicted:** `positive` ✓
- **Confidence:** 100.0%
