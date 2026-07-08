"""P0.4 smoke #3 — H long-input live smoke (PRE_200RUN_FIX_PLAN_2026-07-08.md).

The pilot's longest input was 70 words, but curated MNLI runs to 206 words; the
length-proportional H budget (12*n+200 = 2672 tokens at 206 words) is in the code but
no model has ever been asked for a 206-item salience list in this study. The failure
mode probed: malformed/truncated JSON on long salience lists -> length-correlated
MNAR missingness at scale.

Also runs each H elicitation TWICE with the identical prompt (temperature 0) — a
decoding-stability datapoint for the R1 test-retest review item (Qwen3-235B and
DeepSeek V3 are MoE models, where batching effects can make T=0 nondeterministic).

Usage: python outputs/smoke_h_long_20260708/h_long_smoke.py
Writes: outputs/smoke_h_long_20260708/h_long_smoke_results.json (+ raw responses)
"""
import asyncio
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from dotenv import load_dotenv
load_dotenv(REPO / ".env")

from src.load.dataset_loader import DatasetLoader
from src.inference.inference_engine import InferenceEngine
from src.parsing.parser import Parser
from src.normalization.normalizer import Normalizer
from src.metrics.metrics_calculator import MetricsCalculator
from scripts.run_experiment import pre_clean_text, format_prompt, format_explain_prompt, load_prompt

OUT_DIR = Path(__file__).resolve().parent
LABELS = ["entailment", "neutral", "contradiction"]

async def run_model(model_id: str, clean_text: str, class_prompt_t: str, h_prompt_t: str,
                    parser: Parser, normalizer: Normalizer) -> dict:
    n_words = len(clean_text.split())
    base = max(1024, 800)
    h_max = max(base * 2, 12 * n_words + 200)
    engine = InferenceEngine(model_name=model_id, max_retries=3, concurrent_requests=1)
    rec = {"model": model_id, "n_words": n_words, "h_max_tokens": h_max}

    class_prompt = format_prompt(class_prompt_t, clean_text, LABELS)
    cls = await engine.classify(class_prompt)
    try:
        label = parser.parse_classification(cls.raw_response, LABELS)
    except Exception as e:
        rec["classification"] = f"UNPARSEABLE: {e}"
        return rec
    rec["classification"] = label

    h_prompt = format_explain_prompt(h_prompt_t, label, input_text=clean_text)
    messages = [
        {"role": "user", "content": class_prompt},
        {"role": "assistant", "content": cls.raw_response},
        {"role": "user", "content": h_prompt},
    ]

    calc = MetricsCalculator()
    sets = []
    for attempt in ("base", "retest"):
        raw, usage = await engine.chat_with_usage(messages, max_tokens=h_max)
        entry = {"truncated": bool(usage.truncated),
                 "completion_tokens": usage.completion_tokens,
                 "finish_reason": usage.finish_reason}
        (OUT_DIR / f"raw_H_{model_id.replace(':','_').replace('.','_')}_{attempt}.txt").write_text(raw or "", encoding="utf-8")
        try:
            obj = parser._extract_json(raw)
            entry["json_parsed"] = obj is not None
            entry["salience_entries"] = len(obj.get("salience", [])) if obj else 0
            tokens = parser.parse_highlighting(raw, clean_text, normalizer)
            nset = set(tokens)
            entry["normalized_set_size"] = len(nset)
            entry["parse_ok"] = bool(nset)
            sets.append(nset)
        except Exception as e:
            entry["parse_ok"] = False
            entry["error"] = f"{type(e).__name__}: {str(e)[:200]}"
            sets.append(set())
        rec[attempt] = entry

    if len(sets) == 2 and sets[0] and sets[1]:
        rec["retest_jaccard"] = calc.compute_jaccard_similarity(sets[0], sets[1])
        rec["retest_identical"] = sets[0] == sets[1]
    return rec

async def main():
    loader = DatasetLoader(seed=42)
    instances = loader.load_curated(str(REPO / "data/processed/mnli_curated.jsonl"))
    longest = max(instances, key=lambda i: len(i.text.split()))
    clean_text = pre_clean_text(longest.text)
    print(f"Longest curated MNLI instance: {longest.instance_id} "
          f"({len(longest.text.split())} raw words, {len(clean_text.split())} clean words)")

    class_t = load_prompt(str(REPO / "prompts/classification_mnli.txt"))
    h_t = load_prompt(str(REPO / "prompts/highlighting_explain.txt"))
    parser = Parser()
    normalizer = Normalizer(use_lemmatization=True, remove_stopwords=True, lemmatizer="wordnet")

    results = {"instance_id": longest.instance_id, "gold_label": longest.label, "models": []}
    for mid in ["eu.amazon.nova-pro-v1:0", "qwen.qwen3-235b-a22b-2507-v1:0", "deepseek.v3-v1:0"]:
        print(f"--- {mid} ---")
        rec = await run_model(mid, clean_text, class_t, h_t, parser, normalizer)
        results["models"].append(rec)
        print(json.dumps(rec, indent=2))

    with open(OUT_DIR / "h_long_smoke_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved -> {OUT_DIR / 'h_long_smoke_results.json'}")

if __name__ == "__main__":
    asyncio.run(main())
