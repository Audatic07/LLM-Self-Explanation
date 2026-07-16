"""Tests for prompt rendering and parser validation."""
from pathlib import Path


def load_prompt(filepath: str) -> str:
    path = Path(__file__).parent.parent / filepath
    return path.read_text(encoding='utf-8').strip()


def format_prompt(template: str, input_text: str, label_set) -> str:
    return template.format(input_text=input_text, label_set=", ".join(label_set))


def format_explain_prompt(template: str, predicted_label: str, input_text: str = "Some sample text",
                          other_labels: str = "World, Sports, Business",
                          other_labels_quoted: str = '"World" or "Sports" or "Business"') -> str:
    return template.format(predicted_label=predicted_label, input_text=input_text,
                           other_labels=other_labels, other_labels_quoted=other_labels_quoted)


def test_classification_prompt_no_unrendered_placeholders():
    text = "This movie was great."
    label_set = ["positive", "negative"]
    prompt = load_prompt("prompts/classification.txt")
    rendered = format_prompt(prompt, text, label_set)
    assert "{label_set}" not in rendered
    assert "{input_text}" not in rendered
    assert text in rendered


def test_classification_sst2_prompt_renders():
    text = "Great movie."
    label_set = ["positive", "negative"]
    prompt = load_prompt("prompts/classification_sst2.txt")
    rendered = format_prompt(prompt, text, label_set)
    assert "{input_text}" not in rendered
    assert text in rendered


def test_classification_mnli_prompt_renders():
    text = "Premise [SEP] Hypothesis"
    label_set = ["entailment", "neutral", "contradiction"]
    prompt = load_prompt("prompts/classification_mnli.txt")
    rendered = format_prompt(prompt, text, label_set)
    assert "{input_text}" not in rendered
    assert text in rendered


def test_classification_ag_news_prompt_renders():
    text = "Some news article text."
    label_set = ["World", "Sports", "Business", "Sci/Tech"]
    prompt = load_prompt("prompts/classification_ag_news.txt")
    rendered = format_prompt(prompt, text, label_set)
    assert "{input_text}" not in rendered


def test_highlighting_explain_prompt_renders():
    prompt = load_prompt("prompts/highlighting_explain.txt")
    rendered = format_explain_prompt(prompt, "positive")
    assert "{predicted_label}" not in rendered, f"Unrendered placeholder: {rendered}"
    assert "positive" in rendered


def test_rationale_explain_prompt_renders():
    prompt = load_prompt("prompts/rationale_explain.txt")
    rendered = format_explain_prompt(prompt, "entailment")
    assert "{predicted_label}" not in rendered
    assert "entailment" in rendered


def test_counterfactual_explain_prompt_renders():
    prompt = load_prompt("prompts/counterfactual_explain.txt")
    rendered = format_explain_prompt(prompt, "Sci/Tech")
    assert "{predicted_label}" not in rendered


def test_rank_ordering_explain_prompt_renders():
    prompt = load_prompt("prompts/rank_ordering_explain.txt")
    rendered = format_explain_prompt(prompt, "positive")
    assert "{predicted_label}" not in rendered
    assert "positive" in rendered


def test_all_explain_prompts_have_no_blank_labels():
    for name in ["highlighting_explain.txt", "rationale_explain.txt",
                  "counterfactual_explain.txt", "rank_ordering_explain.txt"]:
        prompt = load_prompt(f"prompts/{name}")
        rendered = format_explain_prompt(prompt, "positive")
        assert "{predicted_label}" not in rendered, f"Blank label in {name}"
        assert "positive" in rendered, f"Label not injected in {name}"


def test_classification_json_format_wanted():
    prompt = load_prompt("prompts/classification.txt")
    assert "JSON" in prompt


def test_highlighting_json_format_wanted():
    prompt = load_prompt("prompts/highlighting_explain.txt")
    assert "JSON" in prompt
    assert "salience" in prompt


def test_rationale_json_format_wanted():
    prompt = load_prompt("prompts/rationale_explain.txt")
    assert "JSON" in prompt
    assert "rationale" in prompt


def test_counterfactual_json_format_wanted():
    prompt = load_prompt("prompts/counterfactual_explain.txt")
    assert "JSON" in prompt
    assert "counterfactual_text" in prompt or "new_prediction" in prompt


def test_rank_ordering_json_format_wanted():
    prompt = load_prompt("prompts/rank_ordering_explain.txt")
    assert "JSON" in prompt
    assert "ranking" in prompt


# --- Paraphrase (*_alt.txt) prompts: guards for the self-consistency ceiling ---
# The ceiling AJ(base, alt) is only interpretable if the alt is a SURFACE paraphrase of
# its base (same task, reworded), and if it renders with no unrendered placeholders.
# Regressions here silently corrupt the ceiling (PROMPT_LITERATURE_VERIFICATION_2026-07-09.md).

_ALT_FILES = ["highlighting_alt.txt", "rationale_alt.txt",
              "counterfactual_alt.txt", "rank_ordering_alt.txt"]
_PLACEHOLDERS = ["{predicted_label}", "{input_text}", "{label_set}",
                 "{other_labels}", "{other_labels_quoted}"]


def test_alt_prompts_render_with_no_unrendered_placeholders():
    for name in _ALT_FILES:
        prompt = load_prompt(f"prompts/{name}")
        rendered = format_explain_prompt(prompt, "positive")
        for ph in _PLACEHOLDERS:
            assert ph not in rendered, f"Unrendered {ph} in {name}: {rendered}"
        assert "positive" in rendered, f"Label not injected in {name}"


def test_alt_prompts_do_not_reference_label_set():
    # {label_set} conditioning was a task change vs the base prompts (which condition on
    # {predicted_label}); all alts were rewritten to drop it.
    for name in _ALT_FILES:
        prompt = load_prompt(f"prompts/{name}")
        assert "{label_set}" not in prompt, f"{name} still references {{label_set}}"


def test_rank_ordering_uses_fixed_k_not_a_range():
    # Literature (Huang et al.) fixes k by protocol; a model-chosen range ("3-5") is
    # off-convention. Base and alt must request the SAME fixed count of WORDS.
    base = load_prompt("prompts/rank_ordering_explain.txt")
    alt = load_prompt("prompts/rank_ordering_alt.txt")
    for name, prompt in [("base", base), ("alt", alt)]:
        assert "3-5" not in prompt and "3 to 5" not in prompt, f"RO {name} must not request a range"
        assert "5 most important words" in prompt, f"RO {name} must request a fixed 5 words"
        assert "tokens" not in prompt, f"RO {name} must ask for words, not tokens"


def test_rationale_alt_is_rationale_only():
    # The alt must NOT request an 'evidence' array — parse_rationale never reads it, and
    # it drifts R toward feature-attribution. Evidence is POS-extracted from the prose in
    # BOTH arms, so base and alt differ only in surface wording.
    prompt = load_prompt("prompts/rationale_alt.txt")
    assert "rationale" in prompt
    assert "evidence" not in prompt, "R alt must not request an evidence list"


def test_counterfactual_alt_keeps_minimality_and_pinned_target():
    prompt = load_prompt("prompts/counterfactual_alt.txt")
    assert "third of the words" in prompt, "CF alt must keep the MiCE-style edit cap"
    assert "{other_labels_quoted}" in prompt, "CF alt must pin the target label(s)"
    assert "new_prediction" in prompt


def test_cad_imdb_prompt_resolution():
    """Move 2 (§2.3/2.4): create_prompt_map(config, "cad_imdb") resolves
    classification -> classification_cad_imdb.txt, CF -> the BINARY base
    counterfactual_explain.txt (2 labels => no multiclass variant is selected by
    build_baseline_explain_prompt), H/R/RO -> the shared bases; and every
    template formats without KeyError."""
    import sys
    ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(ROOT))
    from src.utils.config_loader import load_and_validate_config
    from scripts.run_experiment import create_prompt_map, format_prompt as fp
    from scripts.run_ablations import build_baseline_explain_prompt

    config = load_and_validate_config(config_dir=str(ROOT / "config"))
    prompts, sources = create_prompt_map(config, "cad_imdb")

    assert sources["classification"].endswith("classification_cad_imdb.txt")
    assert sources["CF_explain"].endswith("prompts/counterfactual_explain.txt")
    assert sources["H_explain"].endswith("prompts/highlighting_explain.txt")
    assert sources["R_explain"].endswith("prompts/rationale_explain.txt")
    assert sources["RO_explain"].endswith("prompts/rank_ordering_explain.txt")

    label_set = ["negative", "positive"]
    text = "The plot was engaging and the acting felt genuine throughout."
    rendered = fp(prompts["classification"], text, label_set)
    assert text in rendered and "{" not in rendered.replace('{"label"', "").replace('"}', "")
    for s in ("H", "R", "CF", "RO"):
        out = build_baseline_explain_prompt(s, prompts, "positive", text, label_set)
        assert text in out
        assert "{input_text}" not in out and "{predicted_label}" not in out
    # binary CF: the pinned target is the single other label
    cf = build_baseline_explain_prompt("CF", prompts, "positive", text, label_set)
    assert "negative" in cf
