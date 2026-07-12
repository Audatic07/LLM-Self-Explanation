# Prompt ↔ Literature Verification (2026-07-09)

**Prompted by:** the suspicion that "the ablation results have extremely wrong prompts, or our
own study prompts are extremely wrong from the existing scientific literature" — with rank
ordering and the rationale `_alt`'s evidence list as suspected examples.

**One-line verdict.** Both halves of the suspicion are confirmed, but they land differently:
the **base study prompts are defensible adaptations** of the cited literature (with citation-
hygiene issues, documented in §3), while the **ablation arm is genuinely broken at the
execution level** — its baseline prompts were sent to the model **unformatted**, with literal
`{predicted_label}` / `{input_text}` / `{other_labels_quoted}` placeholder braces (§1). Every
self-consistency ceiling and prompt-ablation delta computed to date compares an unformatted
baseline against a fully-formatted paraphrase and is **invalid as the designed quantity**. The
rationale-alt evidence-list complaint is also confirmed: the alt asks the model for an
`"evidence"` array that the parser **silently discards** (§4).

Verification tier: Huang, Madsen, MiCE, Tian, and Xiong quotes below were all checked against
the **papers' own PDFs** (downloaded 2026-07-09, text-extracted locally), not from memory or
secondary sources.

> **STATUS — fixes applied 2026-07-09 (same day).** The two code/prompt defects are fixed and
> verified offline; the re-run is in progress:
> - **§1 formatting bug — FIXED.** `run_ablations.py` now resolves and formats baseline prompts
>   through the main run's own path (`create_prompt_map` + `format_explain_prompt` + `pre_clean_text`,
>   CF multiclass variant + `other_labels*`). Acceptance check (offline, no API): the ablation
>   baseline explain prompt is now **byte-identical** to the main run's for all 3 datasets × 4
>   strategies, with no unrendered placeholders. New regression tests added; full suite **625 passed**.
> - **§4 alt paraphrases — FIXED.** All four `*_alt.txt` rewritten to true surface paraphrases of
>   their frozen bases (RO 3–5 words matched; R rationale-only, evidence field dropped; CF keeps the
>   ≤⅓ cap + pinned target; H drops `{label_set}`). Locked with tests.
> - **§3 base `*_explain.txt` prompts — one correction applied (RO), rest unchanged.** The RO base
>   `rank_ordering_explain.txt` was changed from the off-convention model-chosen range **"3-5 most
>   important words" → a fixed "5 most important words"** (with `rank_ordering_alt.txt` and its test
>   updated to match). This is the literature-faithful form (Huang fixes k by protocol; the value 5
>   is the study's protocol choice, matching `n_tokens: 5`). Done now because the production 200-run
>   has **not** happened yet — this is the correct window; the only cost is comparability with the
>   throwaway N=25 pilot. The parser (≥3 floor, no cap) and `n_tokens` (validated-positive only, not
>   a cap) both accommodate it with no code change. H/R/CF base prompts remain unchanged (their
>   deviations are documentation, not bugs). **Consequence for the numbers below:** the RO ceiling
>   (+0.747) was measured under the prior "3-5" wording; it will be re-measured under fixed-5 when the
>   production ablation runs (or on request).
> - **Re-run (§6.3) — DONE** (`outputs/20260709_153910/ablations/`, nova-pro, n≈48–50/dataset). Every
>   ceiling rose once the baseline was formatted correctly — the formatting bug had been suppressing
>   all four by 0.14–0.32:
>
>   | Strategy | Old (invalid) | **New (valid)** | sst2 / mnli / ag_news | n |
>   |---|---|---|---|---|
>   | R  (rationale)     | +0.821 | **+0.958** | 0.941 / 0.970 / 0.960 | 133 |
>   | RO (rank order)    | +0.465 | **+0.747** | 0.778 / 0.788 / 0.680 | 140 |
>   | H  (highlighting)  | +0.211 | **+0.527** | 0.490 / 0.549 / 0.541 | 145 |
>   | CF (counterfactual)| +0.088 | **+0.411** | 0.635 / 0.457 / 0.024 | 120 |
>
>   Key reads: **RO's ceiling (+0.747) now sits ABOVE the H–RO cross-strategy reference (+0.611)** —
>   the earlier "RO reproduces a different strategy better than itself" anomaly is gone; RO reproduces
>   itself best, as a valid ceiling must. **R's ceiling (+0.958)** confirms rationale paraphrase
>   stability and *strengthens* the extraction↔rationalization-gap argument (cross-method ECS-adj ≈
>   +0.44 sits far below it). **H (+0.527)** stays second-lowest — consistent with graded-salience
>   quantization being a *real* instability, not an artifact. **CF (+0.411)** rose from near-zero but
>   ag_news is still ~0 (small 1–2-token minimal edits over a 4-class news vocab) — CF divergence from
>   other methods is roughly within its own elicitation noise, a genuine property, not the bug.
>   The prompt-ablation ECS deltas are now all tiny (|mean_delta| < 0.02 in every cell), i.e. the
>   elicitations are robust to rewording — the intended F8 result, now validly measured.
> - **Citation hygiene (§6.4) — N/A yet:** no prose manuscript exists in the repo (only generated
>   tables); §3 is the citation guide for when the paper is drafted.

---

## 1. CRITICAL — the ablation baseline prompts were never formatted

### 1.1 The defect

In `scripts/run_ablations.py`, the baseline (step-1) explanation elicitation passes the raw
template string straight to the engine:

- `run_ablations.py:259` — `run_explain(engine, class_prompt, class_raw, strategy_prompts[s], ...)`
  where `strategy_prompts[s]` is the **unformatted file text** of `*_explain.txt`.
- `format_explain_prompt` (`run_ablations.py:93`) is defined but **never called**.
- The alt arm, by contrast, IS formatted: `format_alt_prompt(...)` at `run_ablations.py:295`
  substitutes the real `predicted_label`, `input_text`, and `label_set`.

The main run does this correctly: `run_experiment.py:85` formats every explain template with
`predicted_label=…, input_text=…, **kwargs` (call sites at lines 305/374/378).

### 1.2 Direct run evidence (not just code reading)

From the N=25 ablation run's own log
(`outputs/20260708_220033/ablations/logs/execution_20260708_220033.log`, line 244), the actual
Bedrock Converse request body for a baseline H elicitation:

> `"text": "The text was classified as: {predicted_label}\n\nText: \"{input_text}\"\n\nAnalyze
> the importance of each word for this classification. …"`

The model literally received placeholder braces. The instance text existed **only** in the
earlier classification turn of the conversation; the predicted label was never restated; and
for CF the target-label slots `{other_labels_quoted}` / `{other_labels}` were sent as braces —
the baseline CF model was never told the permitted target labels inline.

`git log -S` shows the defect is **original to the script** (present in the first version,
commit `7f0698e`), not a regression: even the since-removed highlighting-k arm only formatted
`predicted_label`, and the baseline loop never formatted anything.

### 1.3 Why nobody noticed

The elicitation still "works": the model resolves `{input_text}` from the classification turn
one message earlier, and the parser anchors output tokens against the *real* instance text, so
hallucinated tokens are filtered and outputs look sane. The damage is a **systematic condition
difference**, not visible garbage: baseline = text-in-context-only + unresolved braces;
alt = text restated inline + resolved label(s). Both smoke tests and the N=25 run produced
plausible numbers from a confounded comparison.

### 1.4 What this invalidates

- **All `self_consistency_aj_*` values** in `ablation_results.json` (RO +0.465, H +0.211,
  CF +0.088, R +0.821 pooled; all per-dataset cells). They measure
  *unformatted-vs-formatted + wording change*, not paraphrase stability. The R1 "ceiling" has
  not actually been measured yet.
- **All prompt-ablation ECS deltas** (`mean_delta`, `deltas`, and the F8
  robustness figure built from them) — same confound.
- The numeric table in `RANK_ORDERING_PROMPT_LITERATURE_CHECK_2026-07-09.md` §1 and the
  ceiling-vs-H–RO comparison built on it. That document's cardinality-confound mechanism (§2)
  is real (see §4 below) but is only *part* of the artifact; its "RO reproduces a different
  strategy better than itself" diagnostic may partly reflect this formatting confound instead.
- `ML_REVIEW_prompts_methods_2026-07-08.md` R1's status line "instrument built and smoked" —
  the instrument runs, but does not yet measure the claimed quantity.

**Not affected:** every main-run result (ECS-adj, erasure, W6 soft-match, confidence) — the
main pipeline formats prompts correctly and never touches `run_ablations.py`. CF's *base*
prompt file is also fine; only its ablation-time delivery was broken.

### 1.5 A second, smaller fidelity gap in the same script

`load_strategy_explain_prompts` (`run_ablations.py:105–107`) loads `config.prompt_file`
directly — the generic binary-form `counterfactual_explain.txt` — for **all** datasets. The
main run resolves dataset/multiclass variants via `create_prompt_map`
(`counterfactual_explain_multiclass.txt`, `_mnli`, `_ag_news`). So even after the formatting
fix, the ablation's CF baseline would not be the prompt the study actually runs on AG News and
MNLI. The ablation must reuse the main run's prompt-resolution path, not reimplement it.

---

## 2. What the cited papers' prompts actually are (verbatim, PDF-verified)

### 2.1 Huang et al. 2023, "Can Large Language Models Explain Themselves?" (arXiv:2310.11207)

The claimed anchor for H (full attribution) and RO (top-k). SST-2-style movie-review
sentiment, ChatGPT, single combined predict+explain turn (E-P and P-E orders).

**Full attribution (Table I, E-P system prompt):**

> "…you must analyze the importance of each word and punctuation in Python tuple format:
> (<word or punctuation>, <float importance>). Each word or punctuation is separated by a
> space. The importance should be a decimal number to three decimal places ranging from **-1
> to 1, with -1 implying a negative sentiment and 1 implying a positive sentiment**. Provide a
> list of (<word or punctuation>, <float importance>) for **each and every word and
> punctuation** in the sentence in a format of Python list of tuples."

**Top-k (Table IV, E-P):**

> "Your task is to identify the **top 3 most significant words, ranked from the most positive
> sentiment to the least positive sentiment**. … Only output the list of 3 words in the form
> of a comma separated list, with the prediction(as a number) and confidence following after,
> nothing more."

**How k is chosen (§III-B):**

> "The number k is chosen dynamically according to each input sentence as **min(1, ⌊L/5⌋)**,
> where L is the number of words in the sentence."

Note the paper literally prints **min** — an evident typo for **max**: as printed, k ≤ 1 for
every sentence, contradicting their own k=3 example (their example sentence has ~17 words;
⌊17/5⌋ = 3, matching the "top 3" prompt only under the max reading). The repo's earlier
rank-ordering check quoted this as `max(1, ⌊L/5⌋)` without noting the discrepancy — the
sensible reading, but a silent correction; the paper should be cited with a [sic].

### 2.2 Madsen et al. 2024, "Are self-explanations from LLMs faithful?" (ACL Findings 2024, arXiv:2401.07927)

IMDB-paragraph sentiment. All prompts single-turn, no label revealed beforehand.

**Counterfactual (Fig. 2):**

> "Edit the following paragraph such that the sentiment is "{opposite sentiment}". **Make as
> few edits as possible.** Do not explain the answer. Paragraph: {paragraph}"

(plus an implicit variant: "…becomes the opposite of what it currently is").

**Feature attribution (Fig. 3):**

> "List the most important words for determining the sentiment of the following paragraph,
> **such that without these words the sentiment can not be determined**. Do not explain the
> answer."

**Redaction (Fig. 4):**

> "Redact the most important words for determining the sentiment of the following paragraph,
> by replacing important words with [REDACTED], such that without these words the sentiment
> can not be determined. Do not explain the answer."

**Classification (Fig. 5, used before AND after every explanation):**

> "What is the sentiment of the following paragraph? **The paragraph can contain redacted
> words marked with [REDACTED].** Answer only "positive", "negative", "neutral", or
> "**unknown**". Do not explain the answer."

Note the two design features of Fig. 5 that exist *because of* the redaction/erasure check:
the model is told masked content may be present, and it is given an "unknown" escape so that
successful evidence-erasure can surface as "cannot classify" rather than a forced guess.

### 2.3 Ross et al. 2021, MiCE (arXiv:2012.13985)

Not a prompting paper (T5-based editor); it anchors the *minimality construct*:

- Contrastive edit = a modification that **changes the Predictor's output to a given target**
  (flip required by definition).
- Minimality metric = "**word-level Levenshtein distance** … a range from 0 to 1 — the
  Levenshtein distance divided by the number of words in the original input".
- No protocol-level hard cap: masking budget is binary-searched over **0%–55%**.
- Observed outcome: "**MiCE on average changes 17.3–33.1%** of the original tokens" (18.5–33.5%
  with gold labels).

### 2.4 Tian et al. 2023, "Just Ask for Calibration" (arXiv:2305.14975)

**Verb. 1S top-1 (Table 7):**

> "Provide your best guess and **the probability that it is correct (0.0 to 1.0)** for the
> following question. **Give ONLY the guess and probability, no other words or explanation.**"

Two-stage variant: "Provide the probability that your guess is correct. Give ONLY the
probability, no other words or explanation." Scale is **0.0–1.0** throughout.

### 2.5 Xiong et al. 2024, "Can LLMs Express Their Uncertainty?" (ICLR 2024, arXiv:2306.13063)

**Vanilla verbalized confidence (appendix prompt):**

> "Read the question, provide your answer and your confidence in this answer. **Note: The
> confidence indicates how likely you think your answer is true.** … Answer and Confidence
> **(0-100)**: [ONLY the number; … numerical number in the range of 0-100]%"

Scale is **0–100**.

---

## 3. Base study prompts vs the literature — strategy by strategy

Ordered by size of deviation. "Adapted" = defensible but must be cited as an adaptation, not
as "following" the source.

### 3.1 H — `highlighting_explain.txt` vs Huang full attribution: **adapted, 3 substantive changes**

| Dimension | Huang | This study |
|---|---|---|
| Scale | **signed −1…1**, 3 decimals (polarity + magnitude) | **unsigned 1–10 integers** (magnitude only) |
| Coverage | every word **and punctuation** | every word (punctuation dropped) |
| Turn structure | single combined predict+explain turn | separate turn, **predicted label revealed** |

The scale change is *motivated* — a sentiment-signed scale does not generalize to 3-class MNLI
or 4-class AG News, and integers parse robustly — but it changes the elicited object from a
directional attribution to a salience magnitude, and 10 integer levels (vs ~2000 float values)
produce heavy ties that interact with the dynamic top-k cutoff (the k-threshold sensitivity
already flagged as R5). The label-reveal point is ML_REVIEW R2. **Citation hygiene:** say
"adapted from Huang et al.'s per-word attribution: unsigned 1–10 integer salience, words only,
label-agnostic."

### 3.2 RO — `rank_ordering_explain.txt` vs Huang top-k: **adapted, 2 substantive changes**

- **Cardinality:** Huang's k is experimenter-set — fixed ("top 3") or length-proportional
  (⌊L/5⌋, misprinted as min(1,·)). The study's "**3-5**" hands the choice to the model — the
  non-standard range already documented in the rank-ordering check, and flatly mismatched to
  ~200-word MNLI inputs where Huang's formula would give k ≈ 40.
- **Ranking criterion:** Huang ranks "from the most positive sentiment to the least positive
  sentiment" (polarity order); the study ranks "from most to least important" (importance
  order). Since the pipeline consumes RO as an unordered set (Jaccard), this does not touch
  the metric, but the prompt form is not Huang's.

### 3.3 CF — `counterfactual_explain*.txt` vs Madsen Fig. 2 + MiCE: **well-aligned, best of the four**

- "Edit the text so that it is classified as X instead" ≈ Madsen's explicit-target template;
  "Make as few edits as possible" is **verbatim** Madsen.
- "change at most a third of the words" is in **neither** source as protocol: MiCE has no hard
  cap (binary-search to 55%); the ≤⅓ figure matches MiCE's **observed** edit fractions
  (17.3–33.5%). Defensible operationalization — cite as "cap chosen to match MiCE's reported
  edit-fraction range," not as MiCE's method.
- Flip requirement (validated `new_prediction`, parser-enforced edit-ratio) = MiCE's
  definition of a contrastive edit. ✅
- "do not add new sentences", "keep the original spacing and punctuation style" — study-specific
  parser-driven additions; harmless, but they are ours.

### 3.4 R — `rationale_explain.txt`: **no verbatim literature precedent — cite as construct, not form**

Neither Huang nor Madsen elicits a free-text rationale; project memory's "reworded to
Madsen/Huang forms" does not apply to R's *form*. The construct anchor is label-conditioned
free-text rationalization (Wiegreffe et al. 2021's "rationalizing" mode; the e-SNLI
"explain why" tradition). The **"In one sentence"** cap and the POS-based evidence extraction
are this study's own operationalizations (the one-sentence evidence-set compression is already
flagged as R5). Nothing here is *wrong* — but the paper must not imply the R prompt follows a
published template.

### 3.5 Confidence — `confidence_verbalized.txt` vs Tian/Xiong: **hybrid + one unsourced instruction**

- 0–100 scale = Xiong; "probability … correct" framing = Tian (who uses **0.0–1.0**); JSON-only
  output ≈ both papers' "Give ONLY the …" convention. Fine as a hybrid; cite both.
- "**Give your actual estimate, not a hedge toward 50**" has **no precedent in either paper**
  and is a leading instruction (nudges away from the middle of the scale). Pilot behaviour
  (109/225 at 0.95) matches Xiong's overconfidence clustering anyway, so it likely changed
  nothing — but a reviewer can ask why the elicitation editorializes. Flag in methods or drop
  at the next unfreezing point.

### 3.6 Classification + erasure re-classification vs Madsen Fig. 5: **construct deviation on the erasure leg**

The study's classification prompts (e.g. `classification_sst2.txt`) are plain forced-choice
JSON — reasonable for the main task. But the **erasure instrument**
(`scripts/run_validity_tests.py`) re-classifies `[MASK]`-ed/deleted text with that **same
forced-choice prompt**: no notice that the text may contain masked tokens, and **no
"unknown"/"neutral" escape**. Madsen's protocol includes both, precisely so that successful
evidence-removal can express itself as "cannot classify" instead of a coin flip. The study's
CC-minus-random differencing partially compensates (both arms face the same forced choice),
but the deviation should be stated in the limitations, and an unknown-aware re-classification
sensitivity (one extra prompt variant, offline re-run of the erasure arm) would close it.

---

## 4. Alt (paraphrase) prompts — audit against their own base

A paraphrase arm is only valid if the alt holds the task fixed and varies surface wording.
Deviations beyond wording, per strategy:

| Strategy | Task-level changes in `_alt` vs base | Severity |
|---|---|---|
| **R** | (1) requests an `"evidence": […]` array **that `parse_rationale` never reads** (parser.py:241 reads only `"rationale"`; evidence is POS-extracted from the prose — the requested list is discarded); (2) asks "why the text **belongs to one of these categories: {label_set}**" instead of "why … classified as {predicted_label}"; (3) "Focus on specific evidence tokens" drifts the elicitation toward Madsen's *feature-attribution* form — a different explanation type; (4) drops "In one sentence" from the instruction (survives only as a schema placeholder) | **High** — schema + question + type drift |
| **RO** | 3–5 **words** → exactly **5 tokens**; adds "into {label_set}" (documented 2026-07-09; confirmed) | **High** — cardinality is task spec |
| **CF** | drops the pinned target ("{other_labels_quoted} instead" → "a different category from these: {label_set}"); **drops the ≤⅓-words minimality cap**, the no-new-sentences and spacing constraints — i.e. the alt relaxes the MiCE minimality construct and sits closer to the *free*-CF variant than to base CF | **High** — minimality is the CF construct |
| **H** | "for this classification" → "contributed to classifying it into {label_set}" (conditioning drift); scale and every-word coverage matched | Low |

So three of four alts change the **task**, not the wording — and on top of that, all four
base-vs-alt comparisons executed to date carry the §1 formatting confound. The user's
"rationale alt evidence list is wrong" is confirmed twice over: the field is both a task
change *and* dead on arrival at the parser.

---

## 5. What survives, what doesn't

**Invalidated (must re-run after fixes):** every number in
`outputs/*/ablations/ablation_results.json` and `prompt_ablation_*.json` — self-consistency
ceilings AND ECS deltas; the F8 ablation-robustness figure; the ceiling-based interpretation
paragraphs in `N25_RUN_ANALYSIS_2026-07-08.md` and
`RANK_ORDERING_PROMPT_LITERATURE_CHECK_2026-07-09.md` §1/§4.

**Survives:** all main-run quantities (ECS-adj, per-pair AJ including the H–RO +0.611
reference, erasure results, W6 soft-match, confidence distribution) — collected by
`run_experiment.py`, which formats prompts correctly. The base prompts themselves are
literature-defensible adaptations (§3) needing citation hygiene, not rewrites. The R1
*argument* (a consistency paper needs a self-consistency ceiling) also survives — the ceiling
just hasn't validly been measured yet.

---

## 6. Recommended actions (ordered; respects the base-prompt freeze)

1. **Fix §1 in `run_ablations.py`** [code, no design change]: route baseline elicitation
   through the SAME prompt-resolution and formatting path as `run_experiment.py`
   (`create_prompt_map` + full kwargs, incl. `other_labels*` for CF and dataset/multiclass
   variants). Acceptance check: for one sampled instance, byte-diff the ablation's explain
   turn against the main run's — must be identical.
2. **Fix the four `_alt` files to true paraphrases** [ablation-only files, not frozen]:
   RO → "3-5 most important words" matched to base; R → keep one-sentence + {predicted_label}
   anchoring + `{"rationale": …}`-only schema, reword surface only (drop the evidence field —
   or, if kept, make the parser consume it in BOTH arms; dropping is cleaner); CF → keep
   pinned target + ≤⅓ cap + no-new-sentences, reword surface only; H → drop "{label_set}",
   keep "for this classification".
3. **Re-run the ablation arm** (nova-pro, same N as before) and re-quote ceilings in the N25
   analysis. Expect RO/H/CF ceilings to rise; treat pre-fix ceilings as void, not as lower
   bounds.
4. **Paper citation hygiene** (§3): "adapted from" language for H and RO (scale, punctuation,
   k-specification, ranking criterion), MiCE cited for the construct + observed-range cap (not
   protocol), R cited as label-conditioned rationalization (Wiegreffe / e-SNLI tradition) with
   the one-sentence cap as ours, confidence cited as Tian/Xiong hybrid (and reconsider the
   anti-hedge line at the next unfreezing point), erasure's forced-choice deviation from
   Madsen Fig. 5 stated in limitations (or closed with an unknown-aware sensitivity arm).
5. **Cite Huang's k-formula with [sic]** (paper prints min(1,⌊L/5⌋); the max reading is
   forced by their own k=3 example) — and amend the 2026-07-09 rank-ordering check, which
   silently corrected the formula and whose §1 numbers carry the §1 formatting confound.
6. **Do not change the frozen base `*_explain.txt` prompts before the 200-run** (ML_REVIEW R5
   freeze). All §3 deviations are documentation work, not mid-study prompt surgery.

---

## 7. Provenance

- Unformatted-baseline evidence: `scripts/run_ablations.py:93` (dead `format_explain_prompt`),
  `:259` (raw `strategy_prompts[s]`), `:295` (formatted alt);
  `outputs/20260708_220033/ablations/logs/execution_20260708_220033.log` line 244 (verbatim
  Converse request with literal braces); `git log -S format_explain_prompt` (defect present
  since `7f0698e`).
- Discarded evidence field: `src/parsing/parser.py:241` (`obj.get("rationale", "")`; no read
  of `"evidence"` anywhere in `parse_rationale`).
- Erasure forced-choice: `scripts/run_validity_tests.py` (`mask_token="[MASK]"`,
  re-classification via the standard `class_prompt`).
- Literature PDFs (downloaded + text-extracted 2026-07-09, session scratchpad):
  [Huang et al., arXiv:2310.11207](https://arxiv.org/abs/2310.11207) — Tables I/IV/V, §III-B ·
  [Madsen et al., arXiv:2401.07927 / ACL Findings 2024](https://aclanthology.org/2024.findings-acl.19/) — Figures 2–5 ·
  [Ross et al. (MiCE), arXiv:2012.13985](https://arxiv.org/abs/2012.13985) — §3/§4 minimality ·
  [Tian et al., arXiv:2305.14975](https://arxiv.org/abs/2305.14975) — Table 7 ·
  [Xiong et al., arXiv:2306.13063](https://arxiv.org/abs/2306.13063) — appendix prompt table.
