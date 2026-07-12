# Rank-Ordering Prompt & Self-Consistency Check (2026-07-09)

> **SUPERSEDED / CORRECTION (2026-07-09, later same day).** A follow-up audit
> ([PROMPT_LITERATURE_VERIFICATION_2026-07-09.md](PROMPT_LITERATURE_VERIFICATION_2026-07-09.md))
> found a larger, upstream defect: `run_ablations.py` sent every **baseline** explain prompt
> to the model **unformatted** — with literal `{predicted_label}` / `{input_text}` braces (proven
> in the run log). So every self-consistency ceiling quoted below (RO +0.465, etc.) compared an
> *unformatted baseline* against a *formatted paraphrase*, not two wordings of the same task.
> **The §1 numbers in this document are invalid and must not be quoted.** The
> cardinality-confound mechanism (§2) and the "3–5 vs literature" argument (§3) remain correct
> as *design* observations. Both defects (the formatting bug and the confounded `_alt` prompts)
> were **fixed and the ablation re-run** on 2026-07-09 (`outputs/20260709_153910/`). The corrected,
> valid ceilings: **RO +0.747** (was +0.465), R +0.958, H +0.527, CF +0.411. RO's ceiling now sits
> **above** the H–RO cross-strategy reference (+0.611) — the anomaly this document flagged is
> resolved, and RO's paraphrase stability was indeed being *underestimated*, exactly as §5 predicted.
>
> **RO base prompt corrected (2026-07-09):** the off-convention model-chosen range **"3–5 most
> important words" was replaced with a fixed "5 most important words"** in
> `rank_ordering_explain.txt` (alt + its test updated to match). Fixed-k is the literature-faithful
> form — Huang fixes k by protocol; 5 is the study's protocol choice, matching `n_tokens: 5`. Applied
> now because the production 200-run has not yet run (the correct window; the only cost is
> comparability with the N=25 pilot). This resolves §3.1's "range the model chooses" defect. The
> remaining §3.2 concern — a *flat* small k across very different input lengths (Huang's `k=⌊L/5⌋`
> would give ~40 on MNLI) — is a bigger design change (length-proportional k) still deferred as
> future work. The RO ceiling (+0.747) above was measured under the old "3–5" wording and will be
> re-measured under fixed-5 at the next ablation run.
>
> Also note: the Huang k-formula
> is printed in the paper as `min(1, ⌊L/5⌋)` (a typo — the `max` reading is forced by their own
> k=3 example); this document's `max(1, ⌊L/5⌋)` is the corrected form and should carry a [sic].

**Prompted by:** the suspicion that the self-consistency ("ceiling") numbers in the latest
pilot are *too low* to be believed, and that the **"3–5 most important words"** phrasing in the
rank-ordering (RO) prompt is wrong relative to the literature.

**One-line verdict.** Both suspicions are partly right, and they compound. The low RO ceiling
(+0.465 pooled, and **+0.177 on MNLI with many negative values**) is **not primarily decoding
noise — it is a measurement artifact**: RO's self-consistency is computed between a base prompt
that asks for **3–5 words** and a paraphrase (`_alt`) that asks for **exactly 5 tokens**, so the
"ceiling" conflates a deterministic *cardinality change* with paraphrase stability. Separately,
the **"3–5" range itself is non-standard**: the study's own cited precedent (Huang et al. 2023)
never hands the model a range — it uses a fixed `top-k` or a **length-proportional** `k =
max(1, ⌊L/5⌋)`. A flat 3–5 applied to 200-word MNLI inputs is exactly where the number collapses.

---

## 1. What the numbers actually are

Self-consistency ceiling = same-strategy adjusted-Jaccard between the base wording and the
paraphrased (`_alt`) wording, per strategy (source: `outputs/20260708_220033/ablations/ablation_results.json`,
computed by `scripts/run_ablations.py::compute_self_consistency_aj`).

| Strategy | Pooled AJ | sst2 | mnli | ag_news |
|---|---|---|---|---|
| R (rationale) | **+0.821** | 0.693 | 0.888 | 0.882 |
| RO (rank order) | **+0.465** | 0.681 | **+0.177** | 0.536 |
| H (highlighting) | +0.211 | 0.550 | **−0.279** | 0.362 |
| CF (counterfactual) | +0.088 | 0.327 | −0.118 | 0.055 |

Two things should already look wrong to a careful reader:

1. **RO agrees with a *different* strategy more than with its own paraphrase.** The paper's
   same-paradigm reference pair **H–RO is +0.611** (N25_RUN_ANALYSIS §2.5), but RO's *self*-
   consistency is only **+0.465**. A strategy that reproduces a *different* extraction method
   better than it reproduces itself under a reworded prompt is a signature of a **bad paraphrase**,
   not a noisy strategy. (H–RO uses both strategies' *base* prompts; RO-self uses base-vs-`_alt`.
   The only thing that changed is the `_alt` wording.)
2. **The collapse is localized to MNLI** (+0.177 for RO, −0.279 for H) — the long-input regime.
   That is the fingerprint of a *set-size / input-length* interaction, not of RO being intrinsically
   unstable.

---

## 2. Mechanism 1 — the paraphrase is confounded (this is the main story for RO)

The two prompts being compared:

- **Base** (`prompts/rank_ordering_explain.txt`):
  > "Identify the **3-5 most important words** for this classification, ranked from most to least
  > important. Each item must be a single **word** copied from the text."
- **Paraphrase** (`prompts/rank_ordering_alt.txt`, used as the self-consistency partner):
  > "list the **5 most important tokens** for classification into {label_set}, in decreasing order
  > of importance."

The `_alt` changes **three** things at once: (a) requested cardinality **3–5 → exactly 5**, (b)
**"words" → "tokens"**, (c) adds **"into {label_set}"**. A self-consistency *ceiling* is only
interpretable if the paraphrase holds the task fixed and varies **only surface wording**. Here the
task specification itself moves.

**The cardinality change is not hypothetical — it dominates the base output.** RO set sizes in the
main run (`instance_results.jsonl`, `rank_ordering_valid` instances, base prompt):

| Dataset | mean | size distribution |
|---|---|---|
| sst2 | 3.27 | **3:59, 4:8, 5:6** |
| mnli | 3.70 | 2:1, 3:39, 4:14, 5:19 |
| ag_news | 4.40 | 3:11, 4:23, 5:41 |
| **overall** | — | **3:109, 4:45, 5:66** (mode = the floor, 3) |

So on SST-2 the base returns **exactly 3 words 81% of the time**, while the `_alt` partner is
forced to return **5**. The self-consistency AJ is therefore measuring, in large part, "does a
3-word ranking nest inside an independently-drawn 5-token ranking," not "is the ranking stable."

### 2.1 How much does the AJ correction absorb this? (honest accounting)

The estimator is `AJ = (J − E[J]) / (J_max − E[J])` with `J_max = min(a,b)/max(a,b)`
(`metrics_calculator.py:186`). Because `J_max` is the size-mismatch ceiling, the correction **fully
removes the penalty when the smaller set nests perfectly** — base-3 ⊆ alt-5 gives `J = J_max = 0.6`
→ **AJ = 1.0**. This is visible in the data: 12 of 22 SST-2 RO values are exactly 1.0 (the nesting
cases), which is why SST-2 still averages a healthy 0.68.

What the correction does **not** remove is the **interaction of the mismatch with ranking noise**.
A 3-vs-5 comparison flips to low/negative AJ the moment one of the base's 3 words is *not* among the
alt's 5 (e.g. base picks a word the forced-5 ranking drops). That single-swap fragility is much
higher for 3-vs-5 than for a size-matched 5-vs-5 or 3-vs-3 paraphrase. On long MNLI inputs, where a
tiny set is drawn from a ~200-word vocabulary, non-nesting is the norm — hence the +0.177 with a
spread of negatives. **Net: the correction saves the easy (nesting) cases and lets the mismatch
punish the hard ones, which is exactly the wrong bias for a "ceiling."**

### 2.2 Why this is specific to RO

RO is the **only** strategy whose paraphrase changes the requested cardinality:

| Strategy | base cardinality spec | `_alt` cardinality spec | matched? |
|---|---|---|---|
| H | score **every** word | score **every** word | ✅ |
| R | one sentence → evidence | one sentence → evidence list | ✅ (approx) |
| CF | minimal edit that flips | minimal edit that flips | ✅ |
| **RO** | **3–5 words** | **exactly 5 tokens** | ❌ |

So RO's depressed ceiling is at least partly an artifact of an inconsistent `_alt` prompt, not a
property of rank-ordering. (H and CF are low for *other* reasons — graded-salience quantization and
1–2-token minimal edits — which the N25 analysis already discusses; those are not addressed here.)

---

## 3. Mechanism 2 — the "3–5 words" range vs. the literature

Even setting the paraphrase aside, the base prompt's **"3–5"** is a design outlier.

### 3.1 What the cited precedent does

The study cites Huang et al. for the rank-ordering / top-k design (project memory:
*"dynamic top-k (Huang)"*). The actual paper —
[**Huang et al., "Can Large Language Models Explain Themselves?" (arXiv:2310.11207)**](https://arxiv.org/abs/2310.11207)
— specifies the count in one of two ways, **never as a model-chosen range**:

- **Fixed k, stated explicitly:** the top-k prompt reads *"identify the **top 3 most significant
  words**, ranked from the most positive sentiment to the least positive sentiment."* — a single
  number, not "3–5."
- **Length-proportional k when it varies:** *"k is chosen dynamically … as `max(1, ⌊L/5⌋)`, where L
  is the number of words in the sentence."* The count is a **deterministic function of input
  length**, decided by the *experimenter*, not delegated to the model.

Both conventions share the property the study's prompt lacks: **the cardinality is fixed by the
protocol, not left to the model's discretion.** A range like "3–5" is precisely the thing these
designs avoid, because it makes the output length model- and instance-dependent, which (a) injects
uncontrolled variance across elicitations and (b) breaks comparability across models and prompts.

### 3.2 The length problem this exposes

Huang's `k = max(1, ⌊L/5⌋)` scales with input length: ~2 for a 10-word SST-2 sentence, but **~40
for a 200-word MNLI premise+hypothesis**. The study instead applies a **flat 3–5 to every dataset**.
On MNLI that means summarizing a ~200-word input's importance ranking in 3–5 tokens — a tiny,
high-variance sample of a large latent ranking. This is the mechanistic reason MNLI is the worst RO
cell (+0.177) and the worst H cell (−0.279): a flat small-k specification is mismatched to
long inputs. It is the same length-sensitivity the analysis already flagged for highlighting
("highlighting on MNLI" is the one paraphrase-brittle cell, §4.1).

### 3.3 Broader literature context (consistent direction, less direct)

- [Madsen et al., "Are self-explanations from LLMs faithful?" (ACL Findings 2024,
  arXiv:2401.07927)](https://aclanthology.org/2024.findings-acl.19/) build importance-measure and
  redaction explanations around a **per-word importance** notion and self-consistency (redact the
  words the model called important, check the prediction changes). Their construct is a *scored /
  selected subset determined by the model's own importance judgment*, not a fixed human-imposed
  "3–5." (Exact prompt cardinality not extractable from the HTML; this point is directional, not a
  verbatim quote.)
- Survey/empirical work on LLM self-explanations
  ([arXiv:2407.14487](https://arxiv.org/abs/2407.14487)) frames the two standard forms as **(i) full
  attribution — score every word** and **(ii) top-k — the few most important**, again with k as a
  protocol parameter. The study's "3–5 range" sits awkwardly between the two.

**Bottom line of the literature check:** the phrasing is not *nonsensical* — asking for a handful of
ranked words is a recognized "top-k" self-explanation. What is off-convention is (1) expressing k as
a **range the model chooses** rather than a fixed or formula-driven k, and (2) using a **flat small k
across wildly different input lengths**. Both are known to inject exactly the elicitation variance
that then shows up as a low self-consistency ceiling.

---

## 4. So: is the low number "wrong"?

Separating artifact from signal:

- **RO ceiling +0.465 is an *underestimate* of RO's true paraphrase stability.** It is depressed by
  the confounded `_alt` prompt (§2) and by the flat-k/long-input mismatch (§3.2). The clean
  diagnostic: RO reproduces a *different* strategy (H–RO +0.611) better than its own paraphrase
  (+0.465). A faithful ceiling should be *≥* the cross-strategy agreement, not below it.
- **The signal that survives:** R's ceiling (+0.82) is *not* affected by this (its `_alt` is
  cardinality-matched), so the paper's central R1 argument — "R-pairs at +0.44–0.46 sit genuinely
  below R's own +0.82 stability, so the extraction↔rationalization gap is real" — **still holds**.
  The RO artifact does not touch that conclusion.
- **What is genuinely low and not an artifact:** H and CF ceilings are low for independent reasons
  (graded-salience quantization; 1–2-token minimal edits over a large vocab). Those are correctly
  flagged in the N25 analysis and are *not* re-explained away here.

In short: the RO number is *too low for the wrong reasons* and should not be reported at face value
as "RO is only ~46% self-consistent." The H/CF numbers are low for real reasons.

---

## 5. Recommendations

Ordered by cost. Note the standing **prompt-freeze constraint** (ML_REVIEW R5: do **not** change the
*base* elicitation prompts before the 200-run, to preserve pilot↔production comparability and the
`prompt_manifest.json` freeze). That constraint applies to the base prompt, **not** to the `_alt`
paraphrase, which is an ablation-only artifact and has never entered the primary metric.

1. **Fix the RO `_alt` to be cardinality-matched (cheap, high-value, does not touch the base
   metric).** Change `prompts/rank_ordering_alt.txt` to request **3–5 words** (matching the base) so
   the self-consistency paraphrase varies *only* surface wording. Re-run only the ablation arm
   (`scripts/run_ablations.py`, nova-pro, ~zero risk to main results). Expectation: RO's ceiling
   rises toward the ~0.6–0.7 range its SST-2 cell already shows, and above H–RO — restoring the
   ceiling's interpretability. **This is the single change that most directly addresses the "too
   low" suspicion.** While there, align "tokens"→"words" and drop the extra `into {label_set}` clause
   so the paraphrase is a true reword.
2. **Report the RO ceiling with the artifact caveat, or re-run before quoting it.** Until the `_alt`
   is fixed, the paper should either omit RO's self-consistency number or footnote that the RO
   paraphrase changed the requested cardinality and the value is a lower bound.
3. **Consider (post-200-run, future design only) a length-proportional k for RO and H**, following
   Huang's `k = max(1, ⌊L/5⌋)`, instead of a flat 3–5. This is the principled fix for the MNLI
   collapse, but it is a base-prompt change and therefore **out of scope until after the frozen
   run** — flag it as future work, do not do it now.
4. **Do not change the base RO prompt now.** The "3–5" range is off-convention but it is frozen into
   the pilot and the 200-run design; changing it mid-study costs more (comparability) than it buys.
   State the range choice and its limitation plainly in the methods/limitations instead.

---

## 6. Provenance

- Self-consistency values: `outputs/20260708_220033/ablations/ablation_results.json`
  (`{dataset}_prompt → RO_alt → self_consistency_aj_*`).
- RO set-size distribution: `outputs/20260708_191145_0fe76508/instance_results.jsonl`,
  field `rank_ordering_set`, `rank_ordering_valid == true`.
- Estimator: `src/metrics/metrics_calculator.py:186` (`adjusted_jaccard`, `J_max = min/max`).
- Ceiling computation: `scripts/run_ablations.py:55` (`compute_self_consistency_aj`), prompts
  compared at lines 36–41 (`ALT_PROMPTS`).
- Prompts: `prompts/rank_ordering_explain.txt` (base), `prompts/rank_ordering_alt.txt` (paraphrase).
- Cross-strategy H–RO reference (+0.611): `N25_RUN_ANALYSIS_2026-07-08.md` §2.5.

**Sources (literature):**
- [Huang et al., *Can Large Language Models Explain Themselves?* arXiv:2310.11207](https://arxiv.org/abs/2310.11207) — fixed top-k / length-proportional `k = max(1, ⌊L/5⌋)`; the study's cited precedent.
- [Madsen et al., *Are self-explanations from LLMs faithful?* ACL Findings 2024 (arXiv:2401.07927)](https://aclanthology.org/2024.findings-acl.19/) — per-word importance + redaction self-consistency.
- [*Evaluating the Reliability of Self-Explanations in LLMs*, arXiv:2407.14487](https://arxiv.org/abs/2407.14487) — full-attribution vs top-k as the two standard forms.
