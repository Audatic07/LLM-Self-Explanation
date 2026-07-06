# Experiment Report: llm-explanation-agreement-study-pilot

- **Date:** 2026-06-11 11:06:48
- **Duration:** 43.5s (0.7m)
- **Model:** llama-3.3-70b-versatile
- **Total instances:** 9

## Per-Dataset Summary

| Dataset | Instances | Accuracy | Mean ECS | H | R | CF | RO |
|---------|-----------|----------|----------|---|---|------|---|
| sst2 | 2 | 0/2 (0%) | 0.261 | 100% | 100% | 100% | 100% |
| mnli | 3 | 0/3 (0%) | 0.253 | 100% | 100% | 100% | 100% |
| ag_news | 4 | 0/4 (0%) | 0.233 | 100% | 100% | 100% | 100% |

## Overall Metrics

| Metric | Value |
|--------|-------|
| Mean ECS | 0.2459 |
| Std ECS | 0.0307 |
| Median ECS | 0.2525 |
| Spearman ρ | 0.0100 (p=0.9797) |
| Mean CC3 size | 4.67 |
| Mean CC4 size | 1.11 |
| % instances with CC3 | 100.0% |
| % instances with CC4 | 77.8% |

### Pairwise Jaccard Similarity

| Pair | Mean |
|------|------|
| H–R | 0.1908 |
| H–CF | 0.1920 |
| H–RO | 0.6436 |
| R–CF | 0.0708 |
| R–RO | 0.1929 |
| CF–RO | 0.1854 |

## Per-Instance Details

### sst2_validation_0000
- **Dataset:** sst2
- **Text:** it 's great escapist fun that recreates a place and time that will never happen again . 
- **Ground truth:** `1`
- **Predicted:** `positive`
- **Confidence:** 1.0%
- **Correct:** ✗
- **ECS:** 0.2705
- **CC3 size:** 3 | **CC4 size:** 1

### sst2_validation_0001
- **Dataset:** sst2
- **Text:** verbinski implements every hack-artist trick to give us the ooky-spookies . 
- **Ground truth:** `0`
- **Predicted:** `negative`
- **Confidence:** 0.9%
- **Correct:** ✗
- **ECS:** 0.2525
- **CC3 size:** 2 | **CC4 size:** 1

### mnli_validation_matched_0000
- **Dataset:** mnli
- **Text:** FEC Chairman Scott Thomas, a Democrat who was also at the conference, noted that the Federal Election Campaign Act of 19…
- **Ground truth:** `1`
- **Predicted:** `entailment`
- **Confidence:** 1.0%
- **Correct:** ✗
- **ECS:** 0.2768
- **CC3 size:** 8 | **CC4 size:** 2

### mnli_validation_matched_0001
- **Dataset:** mnli
- **Text:** oh well yeah that's all i have to say thank you [SEP] Good riddance is all I have to say.
- **Ground truth:** `2`
- **Predicted:** `contradiction`
- **Confidence:** 0.9%
- **Correct:** ✗
- **ECS:** 0.2734
- **CC3 size:** 4 | **CC4 size:** 1

### mnli_validation_matched_0002
- **Dataset:** mnli
- **Text:** okay and and i think we just hang up i don't think we have to do anything else [SEP] We don't have to do anything else b…
- **Ground truth:** `0`
- **Predicted:** `entailment`
- **Confidence:** 0.9%
- **Correct:** ✗
- **ECS:** 0.2099
- **CC3 size:** 5 | **CC4 size:** 1

### ag_news_test_0000
- **Dataset:** ag_news
- **Text:** Seagate to Ship 400 GB HDD SL: Seagate Technology has announced that it will begin shipping the world #39;s highest capa…
- **Ground truth:** `3`
- **Predicted:** `Sci/Tech`
- **Confidence:** 1.0%
- **Correct:** ✗
- **ECS:** 0.2117
- **CC3 size:** 5 | **CC4 size:** 0

### ag_news_test_0001
- **Dataset:** ag_news
- **Text:** US team stumbles Marion Jones, the queen of Sydney who finished those 2000 Olympics with a record five track-and-field m…
- **Ground truth:** `1`
- **Predicted:** `Sports`
- **Confidence:** 1.0%
- **Correct:** ✗
- **ECS:** 0.2485
- **CC3 size:** 3 | **CC4 size:** 3

### ag_news_test_0002
- **Dataset:** ag_news
- **Text:** Oil Prices Don #39;t Deter Shoppers; Consumer Confidence Index Up Consumers shrugged off record oil prices to increase s…
- **Ground truth:** `2`
- **Predicted:** `Business`
- **Confidence:** 1.0%
- **Correct:** ✗
- **ECS:** 0.2764
- **CC3 size:** 7 | **CC4 size:** 1

### ag_news_test_0003
- **Dataset:** ag_news
- **Text:** India #39;s Offer for Peace Talks on Kashmir Is Sweetened With Aid India #39;s prime minister, Manmohan Singh, came to K…
- **Ground truth:** `0`
- **Predicted:** `World`
- **Confidence:** 1.0%
- **Correct:** ✗
- **ECS:** 0.1937
- **CC3 size:** 5 | **CC4 size:** 0
