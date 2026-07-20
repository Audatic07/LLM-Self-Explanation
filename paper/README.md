# Paper draft — "Do LLM Self-Explanations Tell One Story?"

Draft of record built from run `outputs/20260718_041618_eaa24e67`.
Current build: **17 pages** (main content pp. 1–9, Limitations onward exempt),
zero LaTeX errors, zero overfull boxes, all citations resolved, `verify_numbers.py` green.

## Files

- `main.tex` — full paper (ACL format, `[preprint]` mode: named authors + page numbers).
  Switch to `\usepackage[review]{acl}` for anonymous *ACL submission.
- `references.bib` — two entries carry `TODO-VERIFY` notes on author lists
  (arXiv:2407.14487, arXiv:2502.18156); verify before submission.
- `acl.sty`, `acl_natbib.bst` — official ACL style files (acl-org/acl-style-files).
- `figures/` — vector PDFs copied from the run's `paper/figures/`.
- `tables/make_tables.py` — regenerates appendix tables A1–A4 from the run's frozen
  booktabs tables (prettified names only; numbers untouched). Run from repo root.
  `tables/A5_correctness.tex` is hand-written from the correctness computation.
- `verify_numbers.py` — cross-checks every number in Tables 1–5, the appendix additions,
  and the headline prose against the run artifacts (~180 checks). Run from repo root;
  exits nonzero on any mismatch. **Run this after any edit to results text.**
- `../tests/test_disattenuation_recovery.py` — planted-agreement simulation validating
  the Spearman correction on the AJ scale; backs every number in Appendix C.

## Build

```
tectonic main.tex
```

## Before submission

1. **Fill author affiliations + emails** (author block in `main.tex`).
2. **Insert the OSF view-only pre-registration link** — footnote in §3.4. The reviewer
   note is right that "pre-registered" is unverifiable at review time without it, and
   it is the paper's main differentiator.
3. **Verify the two TODO-VERIFY bib entries.**
4. **Page limit: content runs to p. 9; the ACL long-paper limit is 8.** Everything
   cheap has already been cut (Figures 1–2 moved to the appendix, Related Work and
   Discussion compressed, the simulation and degeneracy detail moved to Appendices C–D).
   Closing the last page requires an authorial call. Ranked options, least damaging first:
   - Cut Table 3 (cross-model) to two columns (Δ + CI only), keeping means in prose (~1/4 col).
   - Merge §6's three Discussion paragraphs into two (~1/3 col).
   - Move Table 5 (simulatability) to the appendix, keeping the null in prose (~1/2 col) —
     but this weakens the pre-registered-null framing, so it is listed last.
5. Switch to `[review]` mode.

## Known open items (flagged in the text, not defects)

- **Reliability ceilings rest on one paraphrase per strategy.** Adding 2–3 more
  (~5k API calls) would turn each ceiling into a distribution and directly harden the
  "extraction↔CF at ceiling" claim, which is the one result sensitive to it. Stated in
  Limitations as the highest-value extension.
- **Simulatability used explanation-independent perturbations**, not Chen et al.'s
  explanation-derived construct. All claims are narrowed accordingly; an
  explanation-derived arm is the natural follow-up.
- **Erasure control is matched-random only.** A like-sized non-consensus salient
  baseline (single-strategy or top-TF-IDF tokens) would be the sharper test; stated in §5.4.
