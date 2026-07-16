#!/usr/bin/env python
"""Fetch CAD-IMDb (counterfactually-augmented IMDb, Kaushik, Hovy & Lipton,
ICLR 2020, arXiv:1909.12434) — Move 2 of STRONG_ACCEPT_MOVES_SPEC_2026-07-13.md.

Downloads the REVISED (counterfactual) sentiment dev+test splits from the
authors' repository (github.com/acmi-lab/counterfactually-augmented-data,
license: Apache-2.0) and writes data/raw/cad_imdb/candidates_raw.jsonl, one row
per review: {"text", "label" ("positive"|"negative"), "source_split"
("dev"|"test")}. Only the revised splits are ingested — the point is
shortcut-broken text; originals would also re-introduce ~85%-overlap
original/revised near-dup pairs by design.

Deterministic: rows are sorted by sha1(text) before writing. Network-only —
zero Bedrock calls.
"""
import csv
import hashlib
import html
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

BASE = ("https://raw.githubusercontent.com/acmi-lab/"
        "counterfactually-augmented-data/master/sentiment/new")
SPLITS = ["dev", "test"]  # revised-only; train excluded for eval-split hygiene
OUT_PATH = Path("data/raw/cad_imdb/candidates_raw.jsonl")


def clean_review_text(text: str) -> str:
    """HTML cleanup mirroring the pipeline's pre_clean_text/clean_text:
    unescape entities, <br /> (and any tag) -> space, collapse whitespace."""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_split(split: str):
    url = f"{BASE}/{split}.tsv"
    print(f"Fetching {url} ...")
    with urllib.request.urlopen(url) as resp:
        raw = resp.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw), delimiter="\t")
    rows = []
    for row in reader:
        label = (row.get("Sentiment") or "").strip().lower()
        text = clean_review_text(row.get("Text") or "")
        if label not in ("positive", "negative") or not text:
            print(f"  skipped a row (label={label!r}, empty={not text})")
            continue
        rows.append({"text": text, "label": label, "source_split": split})
    print(f"  {split}: {len(rows)} rows")
    return rows


def main():
    rows = []
    for split in SPLITS:
        rows.extend(fetch_split(split))
    # Deterministic order: stable sha1-of-text key.
    rows.sort(key=lambda r: hashlib.sha1(r["text"].encode("utf-8")).hexdigest())
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    n_pos = sum(1 for r in rows if r["label"] == "positive")
    print(f"Wrote {len(rows)} rows ({n_pos} positive, {len(rows) - n_pos} negative) -> {OUT_PATH}")


if __name__ == "__main__":
    main()
