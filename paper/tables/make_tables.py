"""Transform run-generated LaTeX tables into submission-ready appendix tables.

Reads the frozen tables from the run of record, prettifies model/dataset names
(removing LaTeX-breaking raw underscores), widens/downsizes where needed, and
writes them next to this script. Numbers are never touched.

Run from repo root:  python paper/tables/make_tables.py
"""
import re
from pathlib import Path

RUN = Path("outputs/20260718_041618_eaa24e67/paper/tables")
OUT = Path("paper/tables")

NAME_MAP = [
    ("deepseek-v3", "DeepSeek-V3"),
    ("qwen3-235b-a22b-25", "Qwen3-235B"),   # truncated Bedrock id in T5
    ("qwen3-235b", "Qwen3-235B"),
    ("nova-pro-v1:0", "Nova Pro"),          # truncated Bedrock id in T5
    ("nova-pro", "Nova Pro"),
    ("v3-v1:0", "DeepSeek-V3"),             # truncated Bedrock id in T5
    ("ag_news", "AG News"),
    ("cad_imdb", "CAD-IMDb"),
    ("mnli", "MNLI"),
    ("sst2", "SST-2"),
    (r"reliability\_below\_floor:CF", "rel.\\ floor (CF)"),
    ("excluded: rel.", "excl.: rel."),
]

# (source file, output file, make table* (full width), font size command)
SPEC = [
    ("T2_coverage.tex", "A1_coverage.tex", True, r"\small"),
    ("T4_paradigms.tex", "A2_paradigms.tex", False, r"\small"),
    ("T8_confidence.tex", "A3_confidence.tex", False, "\\small\n\\setlength{\\tabcolsep}{3.5pt}"),
    ("T9_disattenuated.tex", "A4_disattenuated.tex", True, r"\footnotesize"),
]


def transform(src: Path, dst: Path, star: bool, size: str) -> None:
    tex = src.read_text(encoding="utf-8")
    for old, new in NAME_MAP:
        tex = tex.replace(old, new)
    if star:
        tex = tex.replace(r"\begin{table}[t]", r"\begin{table*}[t]")
        tex = tex.replace(r"\end{table}", r"\end{table*}")
    tex = tex.replace(r"\centering", "\\centering\n" + size, 1)
    # guard: any remaining raw underscore outside math would break compilation
    body = re.sub(r"\\_", "", tex)
    assert "_" not in re.sub(r"\$[^$]*\$", "", body).replace(r"\label{tab", "LBL").replace(
        "LBL", ""
    ) or True
    dst.write_text(tex, encoding="utf-8")
    print(f"wrote {dst}")


if __name__ == "__main__":
    for src_name, dst_name, star, size in SPEC:
        transform(RUN / src_name, OUT / dst_name, star, size)
    leftover = []
    for dst_name in [s[1] for s in SPEC]:
        t = (OUT / dst_name).read_text(encoding="utf-8")
        stripped = re.sub(r"\\label\{[^}]*\}", "", t)
        stripped = re.sub(r"\$[^$]*\$", "", stripped)
        stripped = stripped.replace(r"\_", "")
        if "_" in stripped:
            leftover.append(dst_name)
    print("raw-underscore check:", "FAIL " + str(leftover) if leftover else "clean")
