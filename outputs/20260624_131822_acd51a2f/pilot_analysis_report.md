# Pilot Analysis Report — LLM Explanation-Agreement Study

**Run ID:** `20260624_131822_acd51a2f`  ·  **Date:** 2026-06-24 13:18–13:33
**Model:** `llama-3.3-70b-versatile` (Groq, on-demand free tier) · temperature 0, top‑p 1, seed 42
**Data:** frozen hand-vetted curated sets (`data/processed/*_curated.jsonl`), N=10 requested per dataset
**Strategies elicited per instance:** Highlighting (H), Rationale (R), Counterfactual (CF), Rank Ordering (RO)

> This is an analyst-written companion to the auto-generated [`report.md`](report.md). It keeps the headline tables, adds interpretation, and — importantly — corrects a completeness issue the auto-report's Sampling Log hides (see §1). The full per-instance transcripts remain in `report.md`; the raw records are in `instance_results.jsonl`.

---

## 1. Run integrity — read this first

**The run did not finish the full N=30 matrix.** It stopped gracefully partway through AG News when the **Groq free-tier daily token budget (100K tokens/day, TPD) was exhausted** (used 99,471 / 100,000). The engine correctly detected a *daily* 429 and halted rather than burning retries.

| Dataset | Requested | **Actually analysed** | Status |
|---------|-----------|----------------------|--------|
| sst2    | 10 | **10** | ✅ complete |
| mnli    | 10 | **10** | ✅ complete |
| ag_news | 10 | **3**  | ⚠️ truncated — daily TPD quota hit at instance 4/10 |
| **Total** | 30 | **23** | partial |

> ⚠️ **Caveat that the auto-report obscures.** `report.md`'s "Sampling Log" prints `ag_news … sampled=10, wrong_pred=0`. That reflects what was *sampled from disk*, not what was *processed* — only 3 AG News instances ever reached the model. **All AG News numbers below are N=3 and are not interpretable;** treat them as a smoke test, not a result. sst2 and mnli are the only datasets that ran to their intended N=10.

**Why it happened:** each instance costs ~3,400 tokens (classification + 4 strategies + CF flip-verification re-classifications + CF-free contrast + redaction passes). 23 instances ≈ 79K tokens, and the per-strategy CF correction loops push a handful of instances well above average. At ~3.4K tokens/instance the 100K/day ceiling is reached at roughly instance 28–29 of the matrix.

**To complete AG News** you need one of: (a) wait for the daily quota to reset and re-run with `--datasets ag_news`; (b) move to a paid Groq tier; or (c) trim per-instance cost (e.g. disable the CF-free contrast or the redaction passes for pilots). The daily window does **not** refill enough within minutes to finish today.

---

## 2. Headline results (sst2 + mnli, N=20 reliable; overall N=23)

| Metric | Overall (N=23) | sst2 (N=10) | mnli (N=10) | ag_news (N=3 ⚠️) |
|--------|----------------|-------------|-------------|------------------|
| Classification accuracy | 19/23 (83%) | 10/10 (100%) | 6/10 (60%) | 3/3 |
| **Mean ECS** | **0.258** | 0.134 | 0.292 | 0.553 |
| 95% CI (bootstrap) | [0.170, 0.350] | [0.057, 0.222] | [0.188, 0.400] | [0.333, 0.857] |
| Mean random baseline | 0.090 | 0.087 | 0.095 | 0.085 |
| **ECS lift over chance** | **+0.167** | +0.047 | +0.197 | +0.469 |
| Complete cases (all 4 valid) | 5/23 (22%) | — | — | — |

**Reading it:** ECS is an inter-method **consistency** measure reported as **lift over a set-size/vocabulary-matched random baseline** — *not* a faithfulness score. The whole-corpus lift of **+0.167** says the four self-explanation methods agree meaningfully more than chance, but the absolute agreement is low: the methods point at overlapping-but-different tokens far more often than they converge. On the one task with a wide vocabulary and full N (mnli), lift is a healthy **+0.197**; on sst2 it collapses to **+0.047** — barely above chance.

---

## 3. Strategy coverage — reliability differs sharply by method

| Strategy | Parsed / Valid | Rate | Note |
|----------|----------------|------|------|
| Highlighting (H) | 23/23 | **100%** | always produced a usable salience set |
| Rank Ordering (RO) | 20/23 | 87% | occasional stopword-only / hallucinated tokens |
| Rationale (R) | 19/23 | 83% | failures are "all tokens unanchored" — pure free-text with no input words |
| **Counterfactual (CF)** | 12/23 | **52%** | JSON parses 100%, but only **12/22 (55%) actually flip the label** |

**Coverage is itself a finding.** CF is the bottleneck and the reason complete-case analysis only retains **5/23 (22%)** instances. The model frequently *claims* a flip that the classifier rejects: e.g. rewriting *"dull in stretches"* → *"engaging in stretches"* still scored **negative**; *"misogynistic"* → *"feminist"* still scored **negative**. Self-reported counterfactuals are unreliable without the verification loop this pipeline runs — a concrete validity argument for keeping flip-verification in the design.

The unconstrained **CF-free** variant flips far more often (74% valid overall, **100% on mnli**) but at **1.6× the edit size** (minimality 0.120 vs 0.077 edits/word). This is exactly the minimality↔validity trade-off from the MiCE/Mayne framing: you can have minimal edits or reliable flips, not both for free.

---

## 4. Paradigm structure — who agrees with whom

Mean **Overlap Coefficient** across all valid instances:

| Pair | Overlap | Paradigm relationship |
|------|---------|-----------------------|
| H–RO | **0.80** | same paradigm (extraction) — highest, as expected; excluded from ECS |
| H–CF | 0.72 | extraction ↔ perturbation |
| CF–RO | 0.65 | perturbation ↔ extraction |
| H–R | 0.55 | extraction ↔ rationalization |
| R–RO | 0.44 | rationalization ↔ extraction |
| **R–CF** | **0.25** | rationalization ↔ perturbation — **lowest** |

The ordering is the story: **agreement decays with paradigm distance.** The two extraction methods (H, RO) agree most; the two genuinely distinct *reasoning* paradigms — free-text rationale (R) and counterfactual perturbation (CF) — agree least (0.25 overall, and **exactly 0.00 on mnli**). Rationales and counterfactuals are nominally explaining the same prediction yet nominate almost disjoint evidence. This is the disagreement problem reproduced *within a single model's own self-explanations*.

Rank agreement between H and RO (the same-paradigm pair) is only moderate: Kendall τ = 0.33, RBO = 0.18 overall — they pick similar *sets* (overlap 0.80) but order them differently.

---

## 5. Secondary signals

- **Rationales are mostly post-hoc.** Introduced-concept rate (R) = **0.75** overall (0.86 on sst2) — three-quarters of the concepts a rationale invokes have **no anchor** in the input text. R reads as plausible narrative, not token-grounded evidence.
- **Higher agreement on *wrong* predictions.** ECS = 0.379 on the 4 misclassified instances vs 0.232 on the 19 correct ones. All 4 misclassifications are from mnli. Small N, but the direction is notable: when the model is wrong, its explanation methods are *more* mutually consistent, not less — consistency ≠ correctness.
- **Consensus cores are thin.** Mean CC3 = 1.35 tokens, CC4 = 0.87. Few tokens survive as agreed-upon across ≥3 methods, consistent with the low absolute ECS.
- **Erasure (redaction) faithfulness** is low where measured: H = 0.22 (N=21), RO = 0.18 (N=17) — removing the top-ranked tokens often fails to flip the prediction, a second (separate) consistency axis pointing the same way as ECS.

---

## 6. Per-dataset notes

**sst2 (N=10, full).** Cleanest run (100% accuracy) but **lowest agreement** — ECS lift only +0.047. H–R overlap is just 0.17: on short sentiment sentences, highlighting and rationale barely nominate the same words. R coverage is also weakest here (60%). Interpretation: short, low-vocabulary inputs give the methods little to converge on, and ECS is dominated by the random-baseline floor.

**mnli (N=10, full).** **The most informative dataset.** Wider vocabulary (premise + hypothesis), real misclassifications (6/10 correct), and the strongest lift (+0.197). It also shows the sharpest paradigm split: R–CF overlap = 0.00 and Kendall τ(H,RO) = 0.00. NLI is where self-explanation methods diverge most.

**ag_news (N=3, ⚠️ not interpretable).** ECS looks high (0.553) but this is an artifact of tiny label-token sets over 3 instances; overlaps saturate near 1.0 and Kendall τ even goes negative (−0.33). **Ignore for any conclusion** — needs a full N=10+ re-run after quota reset.

---

## 7. What to do next

1. **Finish AG News.** Re-run after the daily Groq quota resets: `python scripts/run_experiment.py --datasets ag_news`. The curated set and seed make this reproducible and additive.
2. **Budget the token cost up front.** At ~3.4K tokens/instance, the free 100K TPD caps a full single-model run at ~29 instances/day. For the planned 200/dataset study this is the binding constraint — size the tier (or prune CF-free + redaction for pilots) before scaling.
3. **Treat N=20 (sst2+mnli) as the pilot's real evidence.** It already supports the paper's core claims — methods agree above chance but weakly, agreement decays with paradigm distance, CF is the least reliable modality, and rationales are largely unanchored.
4. **Don't over-read absolute ECS.** Report lift-over-chance and the per-pair overlap gradient; those are robust to set-size confounds in a way the raw mean is not.

---

### Reproducibility footer

| | |
|---|---|
| Config | `config/experiment.yaml` (seed 42, temp 0), curated sets `data/processed/*_curated.jsonl` |
| Artifacts | `instance_results.jsonl`, `aggregate_metrics.json`, `instance_metrics.csv`, `config_snapshot.yaml`, `environment_snapshot.json` |
| Wall time | 926 s (15.4 min); analysed-instance time 853 s; ~79.2K tokens, avg 3,443/instance |
| Stop reason | Groq daily TPD (100K) exhausted at `ag_news_test_002300` (instance 4/10) — partial output checkpointed |
| Auto-report | [`report.md`](report.md) — full per-instance prompt/response transcripts |
