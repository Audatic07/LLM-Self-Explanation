# Paper Drafting Session — Summary (2026-07-20)

**Scope.** Drafting the research paper from the completed N=200 campaign, then revising it
through two rounds of external review. Everything below is committed and pushed to `main`.

**Source of every number:** run of record `outputs/20260718_041618_eaa24e67`
(2,400 instances = 3 models × 4 datasets × 200, commit `670b928`). No number in the paper
was typed by hand without a machine check against that run's artifacts.

**Commits:** `89739f5` (initial draft + review round 1) → `845c70d` (review round 2).
Both on `main`, pushed to `github.com/Audatic07/LLM-Self-Explanation`.

---

## 1. What exists now

`paper/` — a complete ACL-format submission draft:

| File | What it is |
|---|---|
| `main.tex` (425 lines) | The paper: abstract → intro → related work → method → setup → 5 results sections → discussion → conclusion → limitations/ethics/reproducibility → 4 appendices |
| `main.pdf` | Built artifact: **18 pages**, content pp. 1–9, zero LaTeX errors, zero overfull boxes, all citations resolved |
| `references.bib` | 24 entries; 2 flagged `TODO-VERIFY` (author lists for arXiv:2407.14487, arXiv:2502.18156) |
| `acl.sty`, `acl_natbib.bst` | Official ACL style files (acl-org/acl-style-files) |
| `verify_numbers.py` | **240 executed checks + 8 structural assertions** against run artifacts; exits nonzero on mismatch |
| `figures/make_dumbbell.py` | Generates the body figure (observed → corrected agreement) from `disattenuated_agreement.json` |
| `tables/make_tables.py` | Regenerates appendix tables A1–A4 from the run's frozen booktabs output |
| `tables/A5_correctness.tex` | Correctness-split table (hand-built from computed values) |
| `README.md` | Build instructions, pre-submission TODOs, ranked page-trim options, the two open API runs |

`tests/test_disattenuation_recovery.py` (180 lines) — planted-agreement simulation
validating the disattenuation step; 4 tests, ~3 min runtime.

**Build:** `tectonic main.tex`. No system LaTeX exists on this machine; tectonic was
downloaded to the session scratchpad (re-fetch from tectonic-typesetting GitHub if needed).

---

## 2. The paper's argument

Title: *Do LLM Self-Explanations Tell One Story? A Chance-, Ceiling-, and
Reliability-Corrected Audit of Cross-Paradigm Agreement*.
Authors: Aditya Shrivastav, Aditya Kumar, Swathi Jagdale.

Five findings, in the order the paper makes them:

1. **Above-chance agreement everywhere.** Complete-case ECS-adj positive in all 12
   model×dataset cells (0.284–0.617; Holm *p* ≤ .0012 throughout), pooled 0.432.
2. **Structure by paradigm distance, sharpened by reliability correction.** Observed
   E–P 0.615 > E–R 0.395 > R–P 0.286. After disattenuation, extraction↔counterfactual
   pairs reach the ceiling (0.883, 0.956) — their divergence is mostly elicitation noise —
   while every rationale-involving pair stays far short (R–CF 0.391, CI [0.352, 0.429]),
   despite R being the *most reliable* instrument. **This is the headline.**
3. **Paradigm-shaped, not model-shaped.** Two models using one strategy agree more than
   one model using two strategies, on all four datasets.
4. **Consensus is causally load-bearing.** CC3 erasure flips predictions 2.0–2.7× more
   than matched random controls, all models, both operators.
5. **But it does not predict simulatability** (under explanation-independent
   perturbations) — a pre-registered null, reported as such.

---

## 3. Review round 1 — 14 items

**Errors fixed (their items 1–5).** Nova Pro was described as open-weight in three places
(it is proprietary/API-only, and the claim contradicted the Limitations line "no closed
frontier model"); an intro number matched no estimand; the disattenuation exclusion was
described as "two cells" when only one is excluded; "35 refusals, 1.5%" had an unstated
denominator; internal run-ID comments would have shipped in the arXiv source.

**Item 6 — disattenuation's soft spots.** Built the planted-agreement simulation the
reviewer asked for. Instruments observe latent evidence sets under size-preserving
replacement noise, scored with the study's own AJ estimator, 120 configurations. Results:
correction cuts recovery error ~4× (0.26 → 0.06); **essentially unbiased at rel ≥ 0.60**
(bias +0.009, max error 0.041 — the regime of every pooled pair); but acquires an
**upward bias near the 0.30 floor** (+0.072, up to +0.156). That last result *supports*
the reviewer's suspicion, so it is stated plainly and near-floor per-cell entries are
marked as upper bounds.

**Item 7 — simulatability construct.** Our perturbations are explanation-independent;
Chen et al.'s are explanation-derived. Every claim narrowed accordingly across abstract,
intro, §5.5, discussion, and conclusion.

**Items 8–13 + minors.** Cross-model label conditioning (93.9% of 8,074 pairs share a
predicted label; unconditioned comparison is conservative); erasure control scope stated;
MNLI complete-vs-available gap explained mechanically; weighted-null shift explained;
degeneracy counts by pair type with the ladder re-derived on 850 fully non-degenerate
cases (same ordering); correctness split added; OSF placeholder; notation, tie-breaking,
and test-conservativeness sentences.

**A claim I had to walk back mid-edit.** I wrote that the paradigm ordering survives under
both an overlap-coefficient and a Ruzicka graded-weight composite. The overlap version
verifies (E–P 0.786 > E–R 0.689 > R–P 0.526); the Ruzicka variant was Phase C of the plan
and is **not** in this run's outputs (`mean_ecs_lift_weighted` is the salience-weighted
null, a different quantity). The text now claims only the verified half.

---

## 4. Review round 2 — 7 items

Two of the reviewer's suspicions were correct, one was inverted in an important way, and
one analysis came out strongly in the paper's favour.

**Item 1 — pre-registration hygiene.** §5.6 said "six pre-registered sensitivity analyses"
and listed eight; items (vii) and (viii) were added in revision. Fixed, and the audit was
extended to every new analysis (overlap recombination, recovery simulation, correctness
split, per-token density), each now tagged post-hoc at its point of use, plus a global
statement in the Reproducibility Statement.

**Item 2 — CAD-IMDb mislabelled (worse than diagnosed).** Appendix D attributed all
degeneracy exclusions to short inputs. Checking every degenerate pair against both
mechanisms:

| Dataset | Exclusions | Small-V regime | Size-imbalance regime | Median V |
|---|---|---|---|---|
| CAD-IMDb | 398 | 0 | **398 (100%)** | 68 |
| AG News | 48 | 0 | 48 (100%) | 22 |
| MNLI | 289 | 41 | 248 | 12 |
| SST-2 | 213 | 65 | 148 | 10 |

CAD-IMDb has the study's *longest* inputs (median |H| = 30 vs |CF| = 11), and the
imbalance regime dominates everywhere. Appendix D rewritten around the two regimes.

**Item 3 — the k rule.** Code and registration both say `max(3, round(L/5))`, so v2 was
right and v1's ceiling notation was the error. But `L` counts non-punctuation whitespace
tokens, not content words as written — corrected, with both deviations from Huang et al.
(floor of 3 not 1; rounding not floor) disclosed.

**Item 4 — the reviewer's inference was inverted.** They suspected Qwen3/AG News couldn't
meet ceiling *n* ≥ 10 unless the cohort was validity-seeded. It does meet it (*n* = 13,
the study minimum) — but because the ceiling admits any CF that **parses**
(`skip_validation=True`, no flip verification), while the main analysis requires a
**verified flip**. The denominator's gate is *weaker* than the numerator's. Now disclosed
with its bias direction: the extra elicitations are failed flips, plausibly noisier, so
`rel_CF` is likely under-estimated, which **inflates** corrected CF pairs — the same
direction as the at-ceiling caveat.

**Item 5 — per-token density defuses the objection.** Raw flip rates appear to favour
whole strategy sets over the consensus core, which would hand a reviewer "consensus buys
nothing beyond salience." But those arms erase far more text. Per token erased:

| Arm | Mean size | Flip/token (mask) | Flip/token (delete) |
|---|---|---|---|
| **CC3** | 3.1 | **0.096** | **0.103** |
| CF | 6.2 | 0.072 | 0.079 |
| RO | 4.5 | 0.072 | 0.078 |
| R | 4.8 | 0.057 | 0.061 |
| H | 12.6 | 0.035 | 0.036 |
| random (size-matched) | 3.1 | 0.041 | 0.040 |

CC3 is the **densest** evidence per token destroyed — above every individual strategy and
~2.5× its control. Labelled post-hoc descriptive; the controlled like-sized baseline is
flagged as the outstanding gap.

**Items 6–7 — honesty about what wasn't run.** Removed the "roughly 5k further calls"
advertisement from the paraphrase limitation (inviting "why didn't you?" was the flagged
failure mode). Added the correlated-instrument-error caveat: the simulation models
*independent* noise, but the shared label anchor plausibly correlates errors across
paradigms, which inflates observed agreement without inflating self-consistency — again
hitting the at-ceiling claim specifically.

**Minors.** New body figure (observed → corrected dumbbell chart), offset by slimming the
now-duplicative Table 2 so the page count did not regress; E–R delta quantified (+0.056).

---

## 5. Verification infrastructure

Nothing in the results text is unchecked:

- **`paper/verify_numbers.py`** — 240 executed checks covering every cell of Tables 1–5,
  the pooled disattenuation values and CIs, cross-model contrasts, erasure rates and
  densities, simulatability gains, degeneracy rates by pair type and regime, the
  correctness split, and the headline prose values. Plus 8 structural assertions
  (e.g. regime counts must sum to 948; CC3 must be densest under both operators).
  **Run it after any edit to results text.**
- **`tests/test_disattenuation_recovery.py`** — 4 tests pinning every number in Appendix C.
- Both green as of this commit.

**Errors these caught during the session:** a rounding error in Table 1 (0.545 → 0.544),
the erasure ratio overstatement (2.4–2.9× → 2.0–2.7×), and the Ruzicka claim above.

---

## 6. Open items (author decisions, not defects)

**Blocking submission:**
1. Author affiliations and emails (placeholders in the author block).
2. OSF view-only pre-registration link (§3.4 footnote). Without it the pre-registration
   claim — the paper's main differentiator — is unverifiable at review time.
3. Verify the 2 `TODO-VERIFY` bib entries.
4. **Page limit: content runs to p. 9; ACL allows 8.** All cheap cuts are exhausted
   (figures moved to appendix, Related Work and Discussion compressed, simulation and
   degeneracy detail moved to appendices). Closing the last page requires cutting
   review-mandated substance — ranked options in `paper/README.md`.
5. Switch `[preprint]` → `[review]` for anonymous submission.

**Two API runs that would close the last methodological holes.** Neither is possible right
now — Bedrock credentials are not loaded and the campaign key was slated for rotation.
Both are specified in the text as not-run, with commands in `paper/README.md`:

- **Paraphrase expansion (~5k calls).** Two further paraphrases per strategy, turning each
  reliability ceiling into a distribution. This is the one thing that would move the
  "extraction↔CF at ceiling" claim from provisional to solid.
- **Erasure salience baseline (~4–5k calls).** CC3-sized top-TF-IDF or single-strategy-only
  token sets — the controlled version of the per-token density result.

---

## 7. Publication assessment

Asked whether the results support a top-tier venue, my honest read — consistent with the
external reviewer's independent estimate — is: **ACL/EMNLP main track is realistic but not
assured; Findings is a likely floor.**

What carries it: dated pre-registration with a reported null, 12/12 cells significant on a
chance- *and* ceiling-corrected estimand, and the disattenuation move, which converts the
field's standard caveat ("elicitation is noisy") into the headline finding. The
CAD-IMDb arm blunts the near-solved-benchmark objection, and the erasure axis is strong.

What a reviewer will press: it is a measurement/audit paper on English classification with
three mid-tier models (none frontier); the simulatability bridge is null, removing the
"and it matters downstream" pitch; label-conditioned elicitation caps claims at
consistency of post-hoc rationalizations; and the at-ceiling reading rests on
single-paraphrase reliabilities. Every one of these is now either closed or explicitly
bounded in the text — which is the most a draft can do without the two API runs above.

NeurIPS/ICLR are a poor fit; interpretability there skews mechanistic.
