# Adversarial ML-Reviewer Review — Prompts & Method (2026-07-08, v2 literature-verified)

**Scope:** an ACL/EMNLP-caliber reviewer's read of the *prompts* and *measurement design*
(not the statistics — those were audited separately in `PRE_200RUN_FIX_PLAN_2026-07-08.md`
and are strong). The question asked: what would a tunnel-visioned team, deep in the metric
mechanics, MISS that gets the paper rejected or the results dismissed? The exposure is almost
entirely **construct validity and missing baselines** — the layer the ECS-adj work does not
touch. Findings are ordered by rejection risk. Each is tagged **[cheap]** (prompt/analysis
change, little/no new API) or **[scope]** (adds an experimental arm).

**v2 (same day):** every citation and factual claim below was verified against the
literature; R4's original claim was **wrong and is corrected** (e-SNLI covers SNLI, not
MNLI). R1 and R5 were **upgraded from hypotheses to measured pipeline properties** by the
2026-07-08 live smokes and pilot recomputes. A related-work positioning note was added.
Numbers are recomputed from pilot `20260707_223054_6c9bce68` (N=225) or measured in the
2026-07-08 smokes (`outputs/smoke_h_long_20260708/`, `outputs/20260708_150744/ablations/`).

---

## R1 — No within-strategy test–retest baseline: the ECS-adj number has no denominator. [scope→instrument now built, CRITICAL — and now MEASURED]

Every strategy is elicited **once, at temperature 0**. The study reports how much *different*
strategies agree (ECS-adj ≈ +0.44 complete-case), but not how much the *same* strategy agrees
**with itself** on re-elicitation. Without that ceiling, ECS-adj is uninterpretable:

- If same-strategy test–retest AJ ≈ 0.75, cross-method 0.44 is a real divergence between
  paradigms — an interesting result.
- If same-strategy test–retest AJ ≈ 0.45, cross-method 0.44 is **just elicitation noise**;
  the "cross-paradigm consistency" framing collapses.

**Literature (verified).** This is not a hypothetical reviewer preference: Parcalabescu &
Frank (ACL 2024, ["On Measuring Faithfulness or Self-consistency of Natural Language
Explanations"](https://aclanthology.org/2024.acl-long.329/)) argue that this family of tests
measures **self-consistency**, not faithfulness — which is this study's own framing — and
build their comparison suite around exactly such consistency measurements. A consistency
paper without a self-consistency ceiling invites the obvious question.

**And temperature 0 does not give you determinism.** The Thinking Machines batch-invariance
study (["Defeating Nondeterminism in LLM Inference"](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/),
2025) showed **Qwen3-235B — one of this study's three models** — produced 80 distinct
completions in 1,000 greedy (T=0) samples due to batch-variant kernels; MoE routing makes this
worse, and **DeepSeek V3 and Qwen3-235B are both MoE**. So the single T=0 draw is a sample
from a distribution the study never characterizes.

**Measured on this very pipeline (2026-07-08 H-long smoke):** the same H prompt sent twice at
T=0 to the same model on the same 206-word MNLI instance reproduced the evidence set
**exactly zero times out of three models** — retest Jaccard **0.907 (nova-pro), 0.822
(qwen3-235b), 0.907 (deepseek-v3)**; even the salience-entry counts changed (196→211 on
qwen). The same-elicitation noise floor is real and ~0.82–0.91 raw Jaccard (n=1 instance;
needs scale).

**Resolution (implemented 2026-07-08, zero extra API):** the prompt-paraphrase ablation
already elicits every strategy under a second wording — `run_ablations.py` now computes
**same-strategy AJ(base, alt)** with a support-closed instance vocabulary
(`compute_self_consistency_aj`) and persists it per strategy per dataset
(`self_consistency_aj_*` in `ablation_results.json`). This is the paraphrase-stability
ceiling. Smoked live (n=2/dataset): values range −0.81 to +1.0 — noisy at n=2, as expected,
but the instrument works. **Action:** run the full 50-instance ablation (already in the
launch sequence) and report the ceiling next to ECS-adj; optionally add an identical-prompt
retest arm (~200 calls, one model×dataset) to separate decoding noise from paraphrase
brittleness. The paper's headline should be stated as a fraction of the achievable ceiling.

## R2 — The predicted label is revealed in every explanation prompt → you are measuring consistency of *post-hoc rationalizations*, and the anchor can inflate agreement. [cheap framing + optional control]

All four explanation prompts, plus confidence, open with `The text was classified as:
{predicted_label}`. The model is never introspecting a computation — it is **justifying a
label it is handed**. Two consequences:

1. **Claim ceiling.** This is consistency of *label-conditioned rationalization*, the
   confabulation-prone regime: Turpin et al. (NeurIPS 2023, ["Language Models Don't Always
   Say What They Think"](https://arxiv.org/abs/2305.04388)) showed models' explanations
   systematically omit the actual drivers of their predictions; Wiegreffe et al. (EMNLP 2021,
   ["Measuring Association Between Labels and Free-Text
   Rationales"](https://aclanthology.org/2021.emnlp-main.804/)) established that
   label-conditioned ("rationalizing") generation is a different object from
   jointly-produced reasoning. The paper must not drift into language implying the model
   reveals its own reasoning. (The repo is disciplined about "not faithfulness" — good — but
   the label-anchor point is a distinct, sharper caveat and should be stated explicitly.)
2. **Agreement inflation.** Handing every strategy the same label can anchor them all to the
   same obvious cue token(s), manufacturing agreement that would not survive if each strategy
   had to commit to a label itself. This biases ECS-adj **upward** and is a confound the
   chance/ceiling adjustment does **not** remove.

**Cheap:** state the post-hoc/anchor framing as a first-class limitation. **Optional control
[scope]:** a no-label condition on a subset to bound the anchoring effect.

## R3 — Counterfactual evidence is a different KIND of object than H/R/RO; low E-P / R-P agreement may be *definitional*, not an inconsistency. [cheap framing, important]

H/RO/R identify tokens that **support** the current label; CF identifies tokens that, when
**changed**, **flip** it. These diverge for principled reasons (in "not good," the flip
hinges on "not" while the salient sentiment token is "good"). The XAI literature treats these
as answers to *different questions*: Kommiya Mothilal et al. (AIES 2021, ["Towards Unifying
Feature Attribution and Counterfactual Explanations"](https://arxiv.org/abs/2011.04917))
formalize attribution as (roughly) **sufficiency**-oriented and counterfactuals as
**necessity**-oriented, and show the two disagree by construction on many inputs. Forcing
both into one token-set Jaccard and calling the gap "inconsistency" is a category issue that
paradigm-balancing redistributes but does not resolve.

**Pilot evidence this matters:** per-pair AJ means — H–CF **+0.64**, RO–CF **+0.52**, but
R–CF **+0.29**, the lowest of all pairs; and CF's median evidence set is **2 tokens with 36%
of valid CFs at ≤1 token**, so CF-pair Jaccard is heavily quantized. The paper needs either
an explicit argument that minimal-edit sets and attribution sets *should* coincide on these
tasks, or to frame the E-P/R-P components as measuring **attribution↔intervention
divergence** — an expected structural gap whose *size* is the finding, not a model failure.

## R4 — No anchor to gold human rationales. [CORRECTED in v2: e-SNLI covers SNLI, NOT MNLI]

**Correction:** v1 of this review claimed e-SNLI human highlights were "directly comparable
… on the MNLI arm." That was **wrong**: [e-SNLI (Camburu et al., NeurIPS
2018)](https://arxiv.org/abs/1812.01193) annotates **SNLI only**; **MNLI has no gold
rationale annotations** (only tiny ad-hoc research samples exist). The corrected options:

- **(a) Recommended:** a small **SNLI side-arm** (~50 curated instances × 3 models, ~1.3k
  calls) scored against e-SNLI highlight tokens — reports "H/RO evidence recovers X% of
  human-annotated rationale tokens," converting "the methods agree with each other" into
  "…and they overlap with human rationales to degree X." Post-200-run annex; does not gate
  launch.
- **(b) Alternative:** the ERASER benchmark's Movies rationales (long-document sentiment) —
  heavier, but would also exercise the long-input regime (R7).
- **(c) Minimum:** state plainly that no gold-rationale anchor exists for the three chosen
  datasets and agreement ≠ correctness (all methods may converge on the same shortcut).

Risk downgraded from Med-High to **Medium** (the "available and unused" charge was wrong for
MNLI), but option (a) remains cheap and high-value.

## R5 — Prompt design shapes the metric: one-sentence R and score-every-word H. [cheap — and the W6 gate has now FIRED]

- **R is capped at one sentence**, structurally forcing a small evidence set (pilot median 4
  content words) extracted from free prose by an unexamined spaCy step, then compared under
  **exact-token identity after lemmatization** ("awful" ≠ "terrible"). Plan §5 (W6) gated
  the semantic soft-matching sensitivity on whether R-pairs look depressed. **Measured
  2026-07-08: they are.** R-containing pairs average AJ **+0.46** vs **+0.58** for
  CF–extraction pairs and **+0.64** for the same-paradigm H–RO reference. The pre-registered
  gate fires: the **W6 soft-match sensitivity (pinned local embedder, cosine τ = 0.8, as
  pre-registered) must run** (offline, post-collection is fine) to bound how much of the E-R
  and R-P gap is lexical variation rather than evidential disagreement.
- **H scores every word 1–10**, then dynamic top-k turns the graded vector into a set; the
  cutoff does hidden work. The 2026-07-08 long-input smoke retires the *truncation* worry
  (206-word instance → valid ~196–211-entry salience lists on all 3 models, no truncation at
  the 2672-token budget), but a k-threshold sensitivity note remains worth one paragraph.

**Also cheap:** consider allowing R up to 2–3 sentences in a *future* design; do NOT change
the prompt now — the pilot/200-run comparability and the prompt manifest freeze matter more.

## R6 — The verbalized-confidence RQ is effectively dead at temperature 0. [cheap — cut or reframe; literature-consistent]

Pilot: **109/225 answers are exactly 0.95**; top three values (0.95/0.98/0.85) cover most of
the sample; range 0.70–1.00. This replicates the known verbalized-confidence pathology —
Xiong et al. (ICLR 2024, ["Can LLMs Express Their
Uncertainty?"](https://arxiv.org/abs/2306.13063)) document exactly this overconfident
clustering at high round values — so the finding is *consistent with the literature*, but it
means the confidence↔ECS association cannot be estimated from this design (restricted range,
massive ties). Recommend: **drop it from the headline** and report one line — "verbalized
confidence is non-informative under greedy decoding on these tasks, consistent with Xiong et
al. (2024)" — rather than a correlation table that invites "your confidence variable is a
constant."

## R7 — Datasets are near-solved and single-cue-dominated; the interesting regime is under-sampled. [scope / framing]

SST-2, AG News, and (largely) MNLI are high-accuracy for these models; many instances carry
one decisive token, on which all methods trivially agree (the post-P0.1 `short_vocab` mass —
majority of SST-2/MNLI — is the symptom). The multi-feature regime where paradigms *could*
meaningfully diverge is thin. At minimum, report ECS-adj stratified by a difficulty proxy
(input length / content-cue count — confidence is dead per R6); the length-strata machinery
added in P1.2 already covers part of this. A harder or longer-input task (e.g., ERASER
Movies, which would also serve R4b) is the structural fix, post-200-run.

## R8 — MNAR from CF validity makes the complete-case estimand a ~30% selected subsample. [known; biggest external-validity threat]

CF validity is **43%** overall (97/225), far lower on multiclass cells, so the complete-case
primary estimand rests on instances where a minimal flip was *easy to find*. The free-CF AJ
sensitivity (P0.3: complete-case +0.4047, n=114, positive in all 9 cells) mitigates but does
not eliminate this — free-CF is still gated on the rewrite flipping. Lead with the
availability-vs-complete dual reporting (P0.1 structure already does this); state the
selection direction explicitly in the limitations.

---

## Related-work positioning (added in v2 — not scoops, must be cited)

The scoop-check found adjacent 2024–2025 work that the paper must position against, none of
which does the multi-paradigm × multi-model, chance- AND ceiling-corrected design here:

- [Parcalabescu & Frank, ACL 2024](https://aclanthology.org/2024.acl-long.329/) — frames
  these tests as self-consistency, not faithfulness; closest conceptual neighbor, and
  supports this study's framing.
- ["Evaluating the Reliability of Self-Explanations in Large Language
  Models"](https://arxiv.org/abs/2407.14487) — ChatGPT feature-importance vs LIME/occlusion
  disagreement on sentiment; single-model, no chance correction.
- ["Can LLMs Explain Themselves Counterfactually?"](https://arxiv.org/abs/2502.18156) —
  LLM-generated counterfactual explanations studied in isolation.
- ["Aligning What LLMs Do and Say: Towards Self-Consistent
  Explanations"](https://arxiv.org/pdf/2506.07523) — intervention to *improve* do/say
  consistency; this study measures it across paradigms.

---

## Priority summary (v2)

| # | Issue | Rejection risk | Cost | Status / recommendation |
|---|-------|----------------|------|--------------------------|
| R1 | No test–retest ceiling; T=0 retest J = 0.82–0.91 **measured** | **Highest** | instrument built, zero extra API | Ceiling instrument implemented + smoked; run at 50-inst scale with ablation; report ECS-adj vs ceiling |
| R2 | Label anchor → post-hoc rationalization + inflation | High | cheap framing (+optional control) | State plainly (Turpin 2023; Wiegreffe 2021); optional no-label subset |
| R3 | CF flip-set ≠ attribution support-set | High | cheap framing | Frame E-P/R-P as attribution↔intervention divergence (Mothilal 2021); R–CF +0.29 is the datapoint |
| R5 | R-pair depression **measured** (+0.46 vs +0.58/+0.64) | Med-High (was Med) | offline analysis | **W6 gate fired** — run pre-registered soft-match sensitivity (τ=0.8) |
| R4 | No gold-rationale anchor (**corrected**: e-SNLI ≠ MNLI) | Medium | ~1.3k calls post-run | SNLI/e-SNLI side-arm annex, or state absence plainly |
| R6 | Confidence RQ dead at T=0 (109/225 = 0.95) | Medium | cheap | Cut from headline; one-line null consistent with Xiong 2024 |
| R7 | Easy single-cue datasets | Medium | framing now, scope later | Difficulty-stratify (P1.2 partially covers); harder task post-run |
| R8 | CF-MNAR ~30% selection | Structural | none (framing) | Lead with dual reporting; state selection direction |

**One-line verdict (v2):** metric and statistics are publication-grade after the P0/P1
fixes; the design now has a *built and smoked* answer to its biggest hole (R1 — report the
self-consistency ceiling), one fired pre-registered gate to execute (R5/W6 soft-match), two
framing exposures to write honestly (R2, R3), and one corrected factual claim (R4). Nothing
here blocks the 200-run launch; R1's ceiling and R5's sensitivity are computed from the
already-planned ablation arm and offline rescoring.

**Sources checked (2026-07-08):**
[ACL Anthology — Parcalabescu & Frank 2024](https://aclanthology.org/2024.acl-long.329/) ·
[arXiv:2305.04388 Turpin et al.](https://arxiv.org/abs/2305.04388) ·
[ACL Anthology — Wiegreffe et al. 2021](https://aclanthology.org/2021.emnlp-main.804/) ·
[arXiv:2011.04917 Kommiya Mothilal et al.](https://arxiv.org/abs/2011.04917) ·
[arXiv:1812.01193 Camburu et al. e-SNLI](https://arxiv.org/abs/1812.01193) ·
[arXiv:2306.13063 Xiong et al.](https://arxiv.org/abs/2306.13063) ·
[Thinking Machines — Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) ·
[arXiv:2407.14487](https://arxiv.org/abs/2407.14487) ·
[arXiv:2502.18156](https://arxiv.org/abs/2502.18156) ·
[arXiv:2506.07523](https://arxiv.org/pdf/2506.07523)
