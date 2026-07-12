# Research Audit — 2026-07-10

**Scope.** Full literature-grounded audit of the study on branch `w6-softmatch-n25` (prompts, methodology, metric mathematics, statistics, code, datasets, claims, novelty), as requested: *"verify the prompts, the methodologies, the code, the dataset … everything is on the table for change … you may find errors in the scientific papers themselves."*
**Evidence base.** The N=25 run `outputs/20260708_191145_0fe76508` (225 instances), post-fix ablation `outputs/20260709_153910`, the working tree as of 2026-07-10 (625 tests green), six audit scripts under `audit/2026-07-10/` (all seeded, all offline), and 20+ primary sources fetched this session. **Zero Bedrock calls were made.**
**Method.** Every headline number was recomputed with implementations written independently for this audit (nothing imported from `src/` for the arithmetic checks); every literature anchor was re-verified against the source, not the repo's prior verification docs; design choices with no literature answer were probed by simulation.

---

## 0. Verdict in one paragraph

The pipeline's **computations are correct**: all 225 instances × ~12 metric fields, all 48 aggregate statistics, all three pre-registered test families, the full erasure aggregate, and the cross-model contrast reproduce **bit-exactly** under independent reimplementation, and the exact hypergeometric null was validated against Monte-Carlo. The metric construction (ECS-adj) is a textbook Hubert–Arabie chance-and-ceiling correction applied to Jaccard, on firmer ground than its classical antecedents. The pre-registered sign-flip test is empirically **conservative** under its skewed null, as the spec claimed. The prompt-literature verification of 2026-07-09 survives independent spot-checks verbatim, including its identification of a genuine misprint in Huang et al. **No P0 (run-invalidating) defect was found.** The audit found **12 P1 findings** — the most consequential: the primary results table quotes p-values from the wrong test family (F1); the erasure random control is occurrence-unmatched, though the erasure effect demonstrably survives the confound (F2); the cross-model headline is partly a composition artifact (F3); and the W6 soft-matching instrument is built on a pruned vector table that scores antonyms at cosine 1.0 (F7) with a correlated-noise Monte-Carlo null (F8) — its conclusion happens to survive both. All P1 fixes are applied in this session (see §6) except those requiring API re-runs, which ship as code + a validation recipe.

---

## 1. What was verified sound (V1–V13)

| # | Component | Verdict | Evidence |
|---|-----------|---------|----------|
| V1 | Per-instance metrics (legacy ECS, all AJ pairs/components, complete flags, degeneracy counts) | ✓ bit-exact, 0/225 mismatches | `audit/2026-07-10/01_recompute_headlines.py` (A) |
| V2 | Aggregates (9 cells + 3 datasets + 3 models + overall × 3 stats) and all three NHST families incl. `min_n_for_test=6` gating and Holm | ✓ 0/48 mismatches; p-values bit-exact; n=2/3/4 cells correctly untested | 01 (B, C) |
| V3 | Erasure aggregates (strategy/CC3/CC4/random rates, gaps, family-(b) p's, held-out CF rates) | ✓ 0 mismatches | `02_erasure_recompute.py` (A) |
| V4 | Cross-model contrast (per-strategy AJ, cross/within means, paired Δ + bootstrap CIs) | ✓ 0 mismatches | `03_crossmodel_recompute.py` (A) |
| V5 | AJ mathematics: exact E[J]=Σ pmf(k;V,a,b)·k/(a+b−k); J_max=min/max; AJ=(J−E)/(J_max−E) | ✓ exact-vs-MC max diff 0.0039 ≈ MC error; construction = [Hubert & Arabie 1985](https://link.springer.com/article/10.1007/BF01908075)'s (Index−E)/(Max−E) under a hypergeometric null — the same null family ARI uses. The classical treatment ([Albatineh et al. 2006](https://link.springer.com/article/10.1007/s00357-006-0017-z)) had to *approximate* E[Jaccard]; this study's fixed-size finite-vocab setting admits the exact form. | 01 (D); fetched sources |
| V6 | Sign-flip permutation test on skewed AJ values | ✓ empirically conservative: type-I 0.025–0.048 at α=0.05 across all testable cells (H0 simulated through each cell's real (a,b,V) geometry, skew +0.3…+1.0); +1 correction per Phipson & Smyth 2010 implemented as documented; Holm valid with None-exclusion | `05_stats_probes.py` (A) |
| V7 | Complete-case selection (R8/MNAR) — observable bias | ✓ none detected: complete vs incomplete instances indistinguishable on er-component AJ (0.475 vs 0.492, MW p=0.86), text length, vocab, evidence sizes, accuracy | 05 (B) |
| V8 | Vocabulary/urn integrity | ✓ support closure holds in 225/225 (V ≥ |∪ evidence|); vocab reconstruction through the production normalizer matches stored `vocab_size` 225/225 | 01 (F), `04_null_sensitivity.py` |
| V9 | W6 top-line conclusion ("R-pair gap is evidential, not lexical") | ✓ survives and **strengthens under the repaired instrument** (F7/F8 fix, artifact regenerated this session with en_core_web_lg + 1000-draw decorrelated null): semantic credit flows to CF pairs (H-CF +0.025, R-CF +0.024) while R pairs stay flat (−0.006), so the E-P↔R gap *widens* slightly under soft matching — lexical share −0.12 / −0.09 / +0.01 at τ=0.7/0.8/0.9 | regenerated `soft_match_sensitivity.json`; `06_softmatch_probe.py` |
| V10 | PROMPT_LITERATURE_VERIFICATION_2026-07-09 verbatim claims | ✓ independently confirmed against sources: Huang §III-B prints "min(1,⌊L/5⌋)" (see §4); Table I signed −1…1 incl. punctuation; Table IV "top 3 … most positive sentiment to the least"; Madsen Fig 2 "Make as few edits as possible" verbatim; Fig 5 `[REDACTED]`+"unknown" protocol; MiCE minimality = "Levenshtein distance divided by the number of words in the original input", observed edits "17.3–33.1%", binary search "0%–55%", flip-to-target definitional; Xiong "Answer and Confidence (0-100)" | ar5iv/ACL fetches this session |
| V11 | On-disk 07-09 fixes match their doc | ✓ RO base+alt fixed-5; `rationale_alt` evidence field dropped; ablation baseline routed through `create_prompt_map`+`format_explain_prompt` | file reads + `tests/test_prompts.py` |
| V12 | Erasure/faithfulness framing | ✓ "second consistency axis, NOT faithfulness" is exactly [Parcalabescu & Frank ACL 2024](https://aclanthology.org/2024.acl-long.329/): "these faithfulness tests do not measure faithfulness to the models' inner workings – but rather their self-consistency at output level"; deletion-operator precedent = ERASER comprehensiveness ([DeYoung et al. 2020](https://aclanthology.org/2020.acl-main.408/): "comprehensiveness = m(xᵢ)ⱼ − m(xᵢ\rᵢ)ⱼ"); OOD caveat = [Hase et al. 2021](https://arxiv.org/abs/2106.00786); held-out CF verification matches [arXiv:2505.13972](https://arxiv.org/abs/2505.13972) ("judge models with an independent, non-fine-tuned relationship to the generator model provide the most reliable label flipping evaluations") | fetched sources |
| V13 | Datasets | ✓ frozen curated 200/dataset, balanced (SST-2 100/100; AG News 4×50; MNLI 67/67/66 + genre strata), datasheets account for every drop, deterministic seed-42 slicing; splits are the standard eval splits | data/processed/* + loader code |

Two failed internal-audit suspicions worth recording (the audit tried and could not break them): the per-cell test gating **is** enforced (the "significant everywhere" impression traces to F1, not to a gating bug), and MNAR selection has **no** observable signature at N=25 (V7).

---

## 2. Findings — defects and required changes (F1–F12 = P1; F13–F16 = P2)

### F1 (P1) — Primary results table quotes the wrong test family
`scripts/generate_paper_assets.py` builds `T3_primary.tex` (L306-320) and `numbers.json` `per_cell` (L409-414) with `ecs_adj_p_value`/`ecs_adj_p_holm` — the **available-component (a2 sensitivity) family** — next to complete-case estimates, under a caption that promises "ECS-adj complete-case per cell with sign-flip p". The correct fields (`ecs_adj_complete_p_*`) exist and are populated.
**Impact:** the primary family's true picture at N=25 is: significant after Holm in deepseek-sst2 (0.0006), nova-sst2 (0.016), qwen-sst2 (0.016), deepseek-ag_news (0.026); **not** significant in deepseek-mnli (0.060) and qwen-mnli (0.079); untestable (n<6) in 3 cells. The shipped table reads "≈0.0009 everywhere".
**Evidence:** `01_results.json` §G — every `numbers.json` per-cell p matches the a2 family bit-exactly.
**Fix (applied):** T3 now prints the complete-case p's in the primary columns and the a2 p's in explicitly-labelled companion columns; `numbers.json` carries both keys (`p_holm_complete`, `p_holm_available`).

### F2 (P1) — Erasure random control is type-matched but occurrence-unmatched; effect survives anyway
CC3 evidence tokens are fixed-point lemmas whose 3-tier matching in `erase()` fans out to multiple surface variants; the random control samples surface types. Both erase k=|CC3| **types**, but CC3 destroys **14.5% more actual tokens** (mean 3.28 vs 2.81; excess +0.76 ag_news, +0.64 mnli, ≈0 sst2; sign-flip p≈1e-4).
**Decisive probes:** the paired CC3−random gap **survives in the no-advantage subsample** (excess≤0: mask +0.098, p=4e-4, n=106; delete +0.133, p=1e-4, n=102 — delete shows zero attenuation), and there is **no dose-response** (Spearman r≈0.01–0.02). So the erasure effect is real; the mask-arm point estimate carries a modest upward bias (+0.129 full vs +0.098 no-advantage).
**Fix (applied):** `random_flip_rate` gains an occurrence-matched sampling mode (matches expected destroyed-token count, not just type count), default-on for future runs; **needs re-run** for production numbers; the N=25 numbers stand with the subsample-robustness evidence above quoted in the paper.
**Evidence:** `02_results.json` §B. Literature: matched perturbation controls are the standard remedy for removal-based evaluation confounds (ERASER-style deletion; OOD critique [Hase et al. 2021](https://arxiv.org/abs/2106.00786) — both arms stay equally OOD only if destruction is matched).

### F3 (P1) — "Cross-model exceeds within-model" is partly composition
The paired Δ_aj compares a cross side averaged over whichever same-strategy pairs parsed (CF nearly absent: 0.5% of cross pairs on ag_news, 8.8% mnli, 13.7% sst2) against a within side where CF-bearing components hold a fixed 2/3 weight. Under a **strategy-matched contrast** ({H,R,RO} cross pairs vs the within er-component), the direction is significant in **1 of 3 datasets** (sst2 +0.230 [+0.042,+0.448]; ag_news +0.100 [−0.008,+0.216]; mnli +0.054 [−0.054,+0.196]).
**Also learned:** R is by far the most cross-model-stable evidence (AJ 0.75–0.82) — models share rationale vocabulary more than any within-model cross-paradigm pair agrees. This strengthens the "generic task prior" reading (cf. the Explanation Lottery, [arXiv:2603.15821](https://arxiv.org/abs/2603.15821)) for R specifically.
**Fix (applied):** `compute_cross_model_agreement` now also emits `paired_contrast_aj_matched` (same-support contrast); claim language in the drafting map softened to the matched result.
**Evidence:** `03_results.json` §B.

### F4 (P1) — Uniform-draw null is mildly anti-conservative; conclusions robust
AJ centres pairs at E[J] under uniform draws from the instance vocabulary. Under a **frequency-weighted null** (types drawn ∝ occurrence count — explanations plausibly gravitate to repeated tokens), pooled complete-case ECS-adj moves 0.4867 → 0.4635 (−0.023); worst cell deepseek-mnli −0.086; **every cell stays clearly positive**.
**Fix (applied):** productionized as `scripts/run_weighted_null_sensitivity.py` (from audit 04) + a limitations sentence. The legacy pipeline already had this instinct (salience-weighted `ecs_lift_weighted`); this extends it to the primary estimand's scale.
**Evidence:** `04_results.json`.

### F5 (P1, doc) — MNAR robustness evidence should ship with the paper
V7's negative probe (complete-case ≈ incomplete on every observable, most importantly er-AJ p=0.86) is the strongest available answer to R8 and belongs in the limitations text alongside the a2 sensitivity — with the honest caveat that MNAR on *unobservables* remains possible (Little & Rubin's distinction; complete-case unbiasedness requires missingness ⊥ outcome given observables).
**Fix (applied):** limitations paragraph updated (§7 below), probe script retained under audit/.

### F6 (P1, must land pre-launch) — One cell of the 200-run is structurally underpowered
Projected complete-case n at N=200 from N=25 CF-validity: nova-ag_news ≈ **16** (cc rate 0.08; n=2 at N=25 — mean/sd unprojectable), qwen-ag_news ≈ 32 (power 0.82 at the Bonferroni-9 floor), all other cells ≥ 48 with power ≈ 1.0.
**Fix (applied):** dated pre-registration amendment (§G in `ECS_ROBUSTNESS_PLAN_2026-07-05.md`): per-dataset complete-case family added as **co-primary** (3 tests, Holm), per-cell retained as granular secondary; nova-ag_news pre-declared expected-underpowered.
**Evidence:** `05_results.json` §C.

### F7 (P1) — The soft-matching embedder cannot do its stated job
`en_core_web_md==3.8.0` packs **684,830 keys into 20,000 unique vectors** ([official release metadata](https://github.com/explosion/spacy-models/releases/tag/en_core_web_md-3.8.0)) — a 34× pruned table. Measured with the pipeline's own embedder: `increase/decrease` **share vector row 9986** (cosine 1.0000); `good/bad`, `positive/negative`, `love/hate` all cosine 1.0000 on duplicate rows — while the true synonym `good/great` scores 0.522 and is **rejected** at τ=0.8. The instrument credits antonyms at any threshold and rejects synonyms — backwards for sentiment data. The W6 conclusion (V9) survives *incidentally*, because the MC null absorbs bucket collisions symmetrically, but "τ=0.8 = strict semantic matching" is not a supportable description, and `tests/test_soft_match.py`'s "synonyms credited only above τ" premise is hollow under this table.
**Fix (applied):** embedder switched to `en_core_web_lg` (full per-key vector table), W6 re-run offline, artifact + numbers regenerated; md kept only as an explicitly-labelled fallback.

### F8 (P1) — Soft-null Monte-Carlo noise is correlated across the whole run
`expected_soft_jaccard` re-seeds `default_rng(self.seed)` **inside every call**, so all same-geometry pairs across all instances share identical draw patterns: MC errors do not average out. Measured: the pooled H-R soft-AJ mean swings **±0.031 between seeds 42→43** (0.4295→0.4610, n identical) — the same magnitude as the soft-vs-hard deltas being interpreted, and the per-pair SE the artifact reports understates aggregate uncertainty because errors are shared.
**Fix (applied):** per-call decorrelated child seeds (SeedSequence spawned per call), `mc_draws` 200→1000, and a seed-repeat line in the sensitivity report.

### F9 (P1, doc) — The "consistency ladder" has one separated rung at N=25
Cluster-bootstrap CIs (2000 resamples over instances): E-P 0.589 [0.491,0.685] > E-R 0.478 [0.411,0.544] > R-P 0.382 [0.229,0.532]; differences: **E-P>R-P separated** (+0.208 [+0.056,+0.361]); E-P>E-R (+0.110 [−0.005,+0.230]) and E-R>R-P (+0.098 [−0.049,+0.239]) **not separated**. The ladder narrative must be presented as a point-estimate ordering with one CI-separated contrast until N=200.
**Fix (applied):** caveat added to the N25 analysis and the drafting map. Evidence: `06_results.json` §C.

### F10 (P1) — Ablation reports mix scales and hide scope
`run_ablations.py` computes paraphrase deltas on the **legacy raw-Jaccard ECS** while its self-consistency ceilings are **AJ** — two scales in one report/figure (F8) — and the single-model scope (nova-pro only) is not stamped into the output.
**Fix (applied):** AJ-scale deltas recorded alongside legacy (needs re-run to populate for production); output JSON now carries `model` and `scales` metadata; F8 axis label states the scale.

### F11 (P1) — Confidence elicitation: unsourced leading instruction + degenerate measurement
"Give your actual estimate, not a hedge toward 50" has no precedent in either anchor (verified: [Tian et al.](https://arxiv.org/abs/2305.14975) — 0.0–1.0 scale, "Give ONLY the guess and probability"; [Xiong et al.](https://arxiv.org/abs/2306.13063) — "Answer and Confidence (0-100)"), and at T=0 the elicitation is degenerate anyway (109/225 = 0.95; ρ(conf,ECS)=0.0004). Note also the repo doc cites Tian "Table 7"; the prompt is in **Table 6 / Appendix C**.
**Fix (applied):** the anti-hedge sentence is dropped from `prompts/confidence_verbalized.txt` (same pre-200-run unfreezing rationale as the 07-09 RO fix; the N=25 comparability cost is nil — the distribution is one atom at 0.95); confidence claims descoped to descriptive in the drafting map. **Validation recipe** (when quota allows): re-run confidence on 20 instances × 1 model; expect the 0.95 atom to persist (Xiong's overconfidence clustering), confirming the line changed nothing.

### F12 (P1) — Erasure re-classification deviates from its anchor protocol
Madsen Fig 5 (verified verbatim) tells the model masked content may be present and offers an "unknown" escape, so successful evidence-removal can surface as "cannot classify" rather than a forced coin-flip. The study's erasure leg re-classifies with the plain forced-choice JSON prompt. The CC−random differencing neutralizes the *level* effect (both arms forced-choice) but not any *interaction* (consensus-erased texts may be differentially "unknowable").
**Fix (applied):** unknown-aware re-classification variant added behind `validity.unknown_escape_sensitivity` (default off; prompt appends the Madsen-style notice + unknown option; unknown counted as non-flip in the primary and reported separately). **Needs re-run** to produce numbers; ships as a sensitivity arm, not a headline change.

### P2 register (specified, not implemented)
- **F13**: `[MASK]` vs Madsen's `[REDACTED]` (cosmetic for instruction LLMs; document); erasure leg's separate prompt-format path and `max_tokens=50` are fine today (label JSON ≤ ~15 tokens) but should share the main run's formatting helper eventually.
- **F14**: "H-RO" name collision — collection-time H-RO is rank-agreement (Kendall τ needs ≥4 shared tokens and is usually None; RBO p=0.9 with asymmetric depths), soft-match "H_RO" is a set-overlap AJ reference. Rename one in outputs (e.g. `H_RO_rank` vs `H_RO_set`).
- **F15**: citation hygiene — cite Huang's k-formula **with [sic]** (§4); Tian Table 6 not 7; "privileged self-knowledge" is the repo's gloss on [arXiv:2602.02639](https://arxiv.org/abs/2602.02639) ("A Positive Case for Faithfulness…"), not the paper's term; add dataset-paper citations (Socher et al. 2013; Zhang et al. 2015; Williams et al. 2018) to the datasheets.
- **F16**: dead/drifting bits — vestigial `InstanceResult.ecs_complete` never populated in the main path; `ValidityConfig` default `n_random_baseline_trials=10` vs yaml 5; the documented pair-key ordering trap between `compute_ecs_primary` and `compute_ecs_adjusted`.

---

## 3. Statistics: what the 200-run's evidence will look like (from `05_results.json`)

| cell | cc-rate (N=25) | projected n_cc @200 | power @α=.05 | power @α=.05/9 |
|---|---|---|---|---|
| deepseek-sst2 | 0.68 | 136 | 1.00 | 1.00 |
| qwen-sst2 | 0.52 | 104 | 1.00 | 1.00 |
| nova-sst2 | 0.32 | 64 | 1.00 | 1.00 |
| deepseek-mnli | 0.32 | 64 | 1.00 | 1.00 |
| qwen-mnli | 0.24 | 48 | 1.00 | 1.00 |
| nova-mnli | 0.12 | 24 | 0.98 | 0.87 |
| deepseek-ag_news | 0.28 | 56 | 1.00 | 1.00 |
| qwen-ag_news | 0.16 | 32 | 0.96 | 0.82 |
| **nova-ag_news** | **0.08** | **~16** | — unprojectable (n=2 at N=25) | — |

Hence amendment §G (F6): per-dataset co-primary family; nova-ag_news pre-declared underpowered.

---

## 4. Errors found in the scientific literature itself

1. **Huang et al., arXiv:2310.11207, §III-B** — the paper prints: *"The number k is chosen dynamically according to each input sentence as min(1,⌊L/5⌋), where L is the number of words in the sentence."* (verified in the ar5iv full text this session). As printed, k≤1 for every sentence, contradicting the paper's own top-3 prompt and its ~17-word/k=3 example. The intended reading is max(1,⌊L/5⌋). **Cite with [sic].** The repo's rank-ordering check had silently corrected the formula; the 07-09 verification doc caught the discrepancy — this audit confirms it from the source.
2. **ERASER (DeYoung et al. 2020)** presents comprehensiveness/sufficiency without acknowledging the OOD confound of token removal (checked: no distribution-shift discussion attaches to the metric definitions) — the gap later formalized by [Hase et al. 2021](https://arxiv.org/abs/2106.00786). Not an error in this study; a known weakness of the anchor to note when citing.
3. **spaCy `en_core_web_md` as a "semantic vector" source** — the official release metadata advertises "684830 keys, 20000 unique vectors" without flagging the behavioral consequence measured here (antonym pairs at cosine 1.0). Any study using md-class pruned tables for word-level semantic matching inherits F7; treat this as a community-level pitfall.

## 5. Novelty assessment (2025–2026 sweep)

No found work measures **chance-and-ceiling-corrected cross-paradigm agreement across four self-explanation forms with an erasure cross-check and a cross-model contrast**. Nearest neighbors, all to be cited:
- [arXiv:2606.01148](https://arxiv.org/abs/2606.01148) (Jun 2026) — compares **two** forms (verbalized attributions vs rationales) under counterfactual **simulatability**: each form's usefulness separately, not inter-form agreement.
- [Can LLMs Explain Themselves Counterfactually?](https://arxiv.org/abs/2502.18156) (EMNLP 2025) — CF self-explanations only.
- Huang et al. 2023 — attribution vs top-k on sentiment, raw agreement, no chance correction.
- Madsen et al. 2024 — per-form faithfulness, no cross-form agreement.
- Krishna et al. 2022 — the Disagreement Problem for **post-hoc explainers**, not self-explanations.
- "Mind the gap: from plausible to valid self-explanations" (Machine Learning, 2025) — validity of single forms.
The differentiators (exact hypergeometric chance correction, paradigm-balanced aggregation, pre-registered families, erasure axis, cross-model contrast) appear genuinely novel in combination.

## 6. Fix log (this session)

All fixes below are applied AND the full suite is green post-fix: **634 passed** (625 baseline + 9 new tests). Paper assets for the N=25 run were regenerated and re-verified: the audit's provenance check now tags every per-cell p in `numbers.json` as the complete-case family (None where untestable).

| Finding | Change | Where | Status |
|---|---|---|---|
| F1 | T3/numbers.json complete-case p's + labelled a2 companions | `scripts/generate_paper_assets.py` | applied; **verified** on regenerated assets (provenance check: 9/9 cells → complete family) |
| F2 | occurrence-matched random control (`validity.occurrence_matched_control: true`) | `scripts/run_validity_tests.py`, config, +4 tests | applied; **needs re-run** for production numbers |
| F3 | `paired_contrast_aj_matched` in cross-model analysis | `src/metrics/metrics_calculator.py`, +1 test | applied (future runs emit it natively; the N=25 matched values live in `audit/2026-07-10/03_results.json`) |
| F4 | weighted-null sensitivity driver | `scripts/run_weighted_null_sensitivity.py` (new) | applied; artifact written to the N=25 run dir (reproduces audit 04 exactly: 0.4867→0.4635) |
| F6 | pre-registration amendment §G (per-dataset co-primary; nova-ag_news declared; instrument fixes recorded) | `ECS_ROBUSTNESS_PLAN_2026-07-05.md` | applied |
| F7+F8 | full-vector `en_core_web_lg` (+pruning guard/warning), decorrelated per-call SeedSequence, draws 200→1000 | `src/metrics/soft_match.py`, `scripts/run_soft_match_sensitivity.py` | applied; **W6 artifact regenerated** — see V9 for the strengthened result |
| F10 | AJ-scale ablation deltas (`mean_delta_aj`) + `_meta` scope/scale stamp | `scripts/run_ablations.py`, +2 tests | applied; AJ deltas **need re-run** to populate |
| F11 | anti-hedge line dropped; confidence descoped to descriptive | `prompts/confidence_verbalized.txt`, drafting map | applied |
| F12 | unknown-escape erasure arm (`validity.unknown_escape_sensitivity`, default off) + prompt | `scripts/run_validity_tests.py`, config, `prompts/classification_erasure_unknown.txt`, +2 tests | applied; **needs re-run** (sensitivity arm) |
| F5, F9, F15 partial | limitations + ladder caveat + [sic] + claim-language corrections | `N25_RUN_ANALYSIS_2026-07-08.md` (audit banner), `PAPER_READINESS_PLAN_2026-07-08.md` (audit banner) | applied |

**Needs re-run (when quota allows, before/with the 200-run):** erasure arm (F2 occurrence-matched control + F12 unknown-escape sensitivity — one combined pass), ablation arm (F10 AJ-scale deltas; also re-measures the RO ceiling under the fixed-5 prompt, already noted in the 07-09 doc), optional 20-instance confidence probe (F11).

## 7. Limitations text ready for the paper (drop-in)

> Complete-case ECS-adj conditions on counterfactual validity (39.6% at N=25). We find no observable selection: complete and incomplete instances are indistinguishable on the agreement components measurable for both (er-component AJ 0.475 vs 0.492, Mann-Whitney p=0.86), text length, vocabulary size, evidence-set sizes, and accuracy; the available-component estimand differs from the complete-case one by <0.01 pooled. Selection on unobservables cannot be excluded. Our chance correction assumes uniform draws from the instance vocabulary; under a frequency-weighted null the pooled estimate decreases by 0.023 and every cell remains positive. The erasure control matches erased token types; occurrence-matched re-analysis (§F2) shows the consensus-core effect survives in the subsample with no destruction advantage under both operators. Erasure re-classification is forced-choice, unlike Madsen et al.'s unknown-escape protocol; an unknown-aware sensitivity arm is pre-specified. All datasets predate the models' training cutoffs and are plausibly contaminated ([Sainz et al. 2023](https://aclanthology.org/2023.findings-emnlp.722/)); per-cell accuracy is 76–96%, so our consistency estimates describe explanations of largely easy, possibly memorized predictions — consistency on harder or held-out-era data is untested. Verbalized confidence is degenerate at temperature 0 (95% of responses = 0.95) and is reported descriptively only.

## 8. Audit reproducibility

`audit/2026-07-10/01_recompute_headlines.py` … `06_softmatch_probe.py` — all seeded, offline, self-contained (independent reimplementations except where the *design's own behavior* was the measurand: 02-B, 04, 06 import the production `erase`/`Normalizer`/`SoftMatcher` deliberately). Result JSONs sit beside the scripts. Baseline suite: 625 passed (pre-fix); post-fix: **634 passed** (9 new tests covering F2, F3, F10, F12).

**Primary sources fetched this session:** Huang [2310.11207](https://arxiv.org/abs/2310.11207) (ar5iv full text); Madsen [2401.07927](https://aclanthology.org/2024.findings-acl.19/) (ar5iv); MiCE [2012.13985](https://arxiv.org/abs/2012.13985) (ar5iv); Tian [2305.14975](https://arxiv.org/abs/2305.14975); Xiong [2306.13063](https://arxiv.org/abs/2306.13063); [Hubert & Arabie 1985](https://link.springer.com/article/10.1007/BF01908075) (form via secondary restatements); [Albatineh et al. 2006](https://link.springer.com/article/10.1007/s00357-006-0017-z); [Vinh et al. 2010](https://jmlr.csail.mit.edu/papers/volume11/vinh10a/vinh10a.pdf); [DeYoung et al. 2020](https://aclanthology.org/2020.acl-main.408/) (ar5iv); [Jacovi & Goldberg 2020](https://aclanthology.org/2020.acl-main.386/); [Parcalabescu & Frank 2024](https://aclanthology.org/2024.acl-long.329/); [Hase et al. 2021](https://arxiv.org/abs/2106.00786); [Sainz et al. 2023](https://aclanthology.org/2023.findings-emnlp.722/); [Kaushik et al. 2020](https://arxiv.org/abs/1909.12434); [spaCy en_core_web_md-3.8.0 release](https://github.com/explosion/spacy-models/releases/tag/en_core_web_md-3.8.0); [2602.02639](https://arxiv.org/abs/2602.02639); [2603.15821](https://arxiv.org/abs/2603.15821); [2505.13972](https://arxiv.org/abs/2505.13972); [2606.01148](https://arxiv.org/abs/2606.01148); [2502.18156](https://arxiv.org/abs/2502.18156).
