"""F0: observed -> reliability-corrected pairwise agreement (Table 2's money shot).

Reads the run's disattenuated_agreement.json 'overall' block and renders a dumbbell
chart: each cross-paradigm pair as a segment from observed AJ to the disattenuated
value, with a bootstrap CI whisker on the corrected end. The same-paradigm H-RO
reference is drawn as a vertical marker for context (no registered correction).

Run from repo root:  python paper/figures/make_dumbbell.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RUN = Path("outputs/20260718_041618_eaa24e67")
OUT = Path("paper/figures/F0_observed_vs_corrected.pdf")

# ordered as in Table 2: E-P pairs, then E-R, then R-P.
# Labels use real en-dashes (U+2013); matplotlib renders text literally, so LaTeX
# "--" would appear as two hyphens in the figure.
EN = "–"
PAIRS = [
    ("RO_CF", f"RO{EN}CF", f"E{EN}P"),
    ("H_CF", f"H{EN}CF", f"E{EN}P"),
    ("H_R", f"H{EN}R", f"E{EN}R"),
    ("RO_R", f"RO{EN}R", f"E{EN}R"),
    ("R_CF", f"R{EN}CF", f"R{EN}P"),
]
COMP_COLOR = {f"E{EN}P": "#1b6ca8", f"E{EN}R": "#c8781b", f"R{EN}P": "#8c2f39"}

dis = json.loads((RUN / "disattenuated_agreement.json").read_text())
overall = dis["overall"]["pairs"]

# Sized for a single ACL column (~3.2in) so the rendered text is near 1:1 with
# the body font; do not enlarge without scaling the font sizes below.
fig, ax = plt.subplots(figsize=(3.35, 2.5))
ys = list(range(len(PAIRS)))[::-1]

for y, (key, label, comp) in zip(ys, PAIRS):
    p = overall[key]
    obs, corr = p["observed"], p["corrected"]
    lo, hi = p["ci_lower"], p["ci_upper"]
    c = COMP_COLOR[comp]
    ax.plot([obs, corr], [y, y], color=c, lw=2.2, alpha=0.5, zorder=2,
            solid_capstyle="round")
    ax.plot([lo, hi], [y, y], color=c, lw=1.1, alpha=0.9, zorder=3)
    for x in (lo, hi):
        ax.plot([x, x], [y - 0.15, y + 0.15], color=c, lw=1.1, zorder=3)
    ax.scatter([obs], [y], s=30, facecolor="white", edgecolor=c, lw=1.4,
               zorder=4, label="observed" if y == ys[0] else None)
    ax.scatter([corr], [y], s=38, color=c, zorder=5,
               label="corrected" if y == ys[0] else None)

ax.axvline(1.0, color="0.35", ls="--", lw=0.9, zorder=1)
ax.text(1.01, len(PAIRS) - 0.30, "ceiling", fontsize=7, color="0.35", va="center")

ax.set_yticks(ys)
ax.set_yticklabels([f"{lbl}  ({comp})" for _, lbl, comp in PAIRS], fontsize=8)
ax.set_xlabel("adjusted Jaccard  (0 = chance, 1 = ceiling)", fontsize=8)
ax.set_xlim(0.15, 1.18)
ax.set_ylim(-0.85, len(PAIRS) - 0.35)
ax.set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.grid(axis="x", color="0.9", lw=0.6)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=8)
ax.tick_params(axis="x", labelsize=7.5)
ax.legend(loc="lower left", frameon=False, fontsize=7.5, ncol=2,
          handletextpad=0.35, columnspacing=1.1, bbox_to_anchor=(-0.02, -0.055))

fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")
for key, _label, _ in PAIRS:
    p = overall[key]
    # ASCII-only console output: this repo's Windows console is cp1252.
    print(f"  {key}: obs {p['observed']:.3f} -> corr {p['corrected']:.3f} "
          f"[{p['ci_lower']:.3f}, {p['ci_upper']:.3f}]")
