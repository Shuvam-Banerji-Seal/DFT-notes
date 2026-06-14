"""
03-jacobs-ladder-cost-accuracy.py
==================================

"Jacob's ladder" of density-functional rungs, plotted as
computational cost (log scale, relative to LDA) vs typical
accuracy (mean absolute error on the G2 atomisation-energy
benchmark, in kcal/mol).  Each rung climbs the ladder at
the price of more compute, but the accuracy gain levels off
as the highest rungs approach the limits of single-reference
DFT.

Rungs (cost, MAE kcal/mol):
    LDA                :  (1,    90)
    GGA (PBE)          :  (1.5,  20)
    meta-GGA (SCAN)    :  (3,    8)
    hybrid (B3LYP)     :  (100,  5)
    RS-hybrid (wB97X)  :  (200,  3)
    double-hybrid (B2) :  (1000, 2)

References for the cost / accuracy numbers:
- MAE numbers are rounded eyeball-estimates of the G2
  atomisation-energy MAE as quoted in the DFT literature
  (e.g. Mardirossian & Head-Gordon, Mol. Phys. 115, 2315
  (2017), and references therein).  They are intended to
  illustrate the trend, not to be benchmark-precise.
- Cost numbers are relative wall-time estimates for a
  typical G2-sized organic molecule in a standard
  Gaussian-basis code (LDA = 1 by definition).

Why this lives in chapter 05:
    Section 5.6 ("the full zoo") and section 5.7 ("a short
    decision tree") summarise Jacob's ladder.  This plot
    is the visual summary of "why we keep climbing the
    ladder".

Run from the repo root:
    python dft_notes/python_codes/chapter_05/03-jacobs-ladder-cost-accuracy.py

Writes the plot to:
    dft_notes/python_codes/chapter_05/plots/03-jacobs-ladder-cost-accuracy.png

Dependencies: numpy, matplotlib (headless via Agg).
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ─── The data ──────────────────────────────────────────────────────
# (label, cost relative to LDA, MAE on G2 atomisation kcal/mol)
RUNGS = [
    ("LDA", 1, 90),
    ("GGA (PBE)", 1.5, 20),
    ("meta-GGA (SCAN)", 3, 8),
    ("hybrid (B3LYP)", 100, 5),
    ("RS-hybrid (wB97X)", 200, 3),
    ("double-hybrid (B2-PLYP)", 1000, 2),
]


# ─── Main ──────────────────────────────────────────────────────────
def main() -> None:
    names = [r[0] for r in RUNGS]
    costs = np.array([r[1] for r in RUNGS], dtype=float)
    maes = np.array([r[2] for r in RUNGS], dtype=float)

    # Print the data table to stdout (also a "Mermaid-style" data table).
    print("=" * 60)
    print("Jacob's ladder of DFT rungs")
    print("Cost (relative to LDA)  vs  G2 atomisation MAE (kcal/mol)")
    print("=" * 60)
    print(f"  {'Rung':<28s} {'Cost':>10s}  {'MAE':>6s}")
    print(f"  {'-' * 28} {'-' * 10}  {'-' * 6}")
    for name, cost, mae in RUNGS:
        print(f"  {name:<28s} {cost:>10.1f}  {mae:>6.1f}")

    # ─── Plot ──────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 6))

    palette = [
        "#cc785c",  # coral
        "#e8a55a",  # amber
        "#5db8a6",  # teal
        "#a9583e",  # rust
        "#7a8b99",  # slate
        "#3d3d3a",  # ink
    ]

    # Connect the points with a faint line so the eye can follow the
    # trend, but the main visual is the scatter + labels.
    ax.plot(costs, maes, color="#a09d96", linewidth=1.0, alpha=0.5, zorder=1)

    for (name, cost, mae), color in zip(RUNGS, palette):
        ax.scatter(
            cost,
            mae,
            s=160,
            color=color,
            edgecolor="white",
            linewidth=1.5,
            zorder=3,
        )
        # Label to the upper-right of the point.
        ax.annotate(
            name,
            xy=(cost, mae),
            xytext=(8, 8),
            textcoords="offset points",
            fontsize=11,
            color="#3d3d3a",
        )

    ax.set_xscale("log")
    ax.set_xlim(0.7, 2000)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Cost relative to LDA (log scale)")
    ax.set_ylabel("MAE on G2 atomisation energies (kcal/mol)")
    ax.set_title("Jacob's ladder: cost vs accuracy across the DFT rungs")
    ax.grid(True, which="both", alpha=0.25)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    # Annotate the two extremes for context.
    ax.annotate(
        "cheapest,\nleast accurate",
        xy=(1.0, 90),
        xytext=(0.8, 75),
        fontsize=9,
        color="#a09d96",
        ha="left",
    )
    ax.annotate(
        "most expensive,\nmost accurate",
        xy=(1000, 2),
        xytext=(400, 22),
        fontsize=9,
        color="#a09d96",
        ha="left",
    )

    fig.tight_layout()

    # ─── Save ──────────────────────────────────────────────────────
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "03-jacobs-ladder-cost-accuracy.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
