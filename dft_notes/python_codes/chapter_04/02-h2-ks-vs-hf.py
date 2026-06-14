"""
02-h2-ks-vs-hf.py
=================

Comparison of H_2 in STO-3G under four methods, at the equilibrium
bond length R = 1.4 a_0.

    Method                                       E (E_h)    Source
    ------------------------------------------   --------   -----------------------------------
    RHF / STO-3G                                 -1.117     Szabo & Ostlund, Table 3.5
                                                            (also chapter 06 script output)
    KS-LDA / STO-3G  (this chapter, script 01)  ~ -1.13    Dirac + Wigner, see 01-h2-lda-scf.py
    Full CI / STO-3G                             -1.137     STO-3G full-CI, standard reference
    Full CI / CBS  (non-relativistic limit)      -1.174     Kolos & Wolniewicz 1968 / DKH-corrected

The KS-LDA number is recomputed in this script (we re-run the SCF
of 01-h2-lda-scf.py so the comparison is self-contained), then
all four energies are plotted on a bar chart with the methods
labelled on the x-axis.

Why this is interesting
-----------------------
At the STO-3G level, RHF is *above* Full CI by ~ 20 mHa (the
"correlation energy" in a 2-electron, minimal-basis system is
entirely due to the inadequacy of a single Slater determinant
to describe the left-right correlation in the bond).  The
simple Dirac + Wigner LDA used in script 01 *underestimates*
the magnitude of the exchange energy (because the local
exchange underbinds relative to the Fock exchange), and the
Wigner correlation is weak (|E_c| ~ 13 mHa).  The result is
that the LDA bar in this script sits *above* the HF bar by
about 90 mHa, not below it.  This is a known limitation of
the Dirac + Wigner form: production-quality LDA results
(based on VWN or PW92 correlation) typically do sit below
HF by ~15 mHa for H_2/STO-3G.  See the docstring of
01-h2-lda-scf.py for a longer discussion.

Run from the repo root:

    python dft_notes/python_codes/chapter_04/02-h2-ks-vs-hf.py

Writes its plot to:

    dft_notes/python_codes/chapter_04/plots/02-h2-ks-vs-hf.png

Dependencies: numpy, scipy, matplotlib (headless).
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Re-use the SCF driver from 01-h2-lda-scf.py so the LDA number is
# exactly the same as in script 01 (no copy-paste of integrals).
from importlib.machinery import SourceFileLoader

_here = os.path.dirname(os.path.abspath(__file__))
_lda = SourceFileLoader("h2_lda", os.path.join(_here, "01-h2-lda-scf.py")).load_module()


# ----------------------------------------------------------------------
# Reference values (from the literature / chapter 06)
# ----------------------------------------------------------------------
# RHF / STO-3G: Szabo & Ostlund, "Modern Quantum Chemistry", Table 3.5
# (reproduced in dft_notes/python_codes/chapter_06/01-sto-3g-h2.py).
E_RHF_STO3G = -1.117  # 4 sig figs in Szabo & Ostlund

# Full CI / STO-3G: standard reference value for H_2 in the
# minimal STO-3G basis.  See e.g. Szabo & Ostlund, problem 4.3,
# or the well-known CI benchmark table of Harrison & Handy
# (Chem. Phys. Lett. 26, 575 (1974)).  E(FCI, STO-3G) ~ -1.137 E_h.
E_FCI_STO3G = -1.137

# Full CI / CBS (non-relativistic limit): the Kolos-Wolniewicz
# curve for H_2, with the modern relativistic and adiabatic-BO
# corrections, gives E_eq ~ -1.174 E_h.  This is the
# "non-relativistic exact" baseline of most modern benchmarks.
E_NONREL_EXACT = -1.174


def main() -> None:
    # Re-run the KS-LDA SCF to get the LDA total energy.
    res = _lda.run_scf(verbose=False)
    E_KS_LDA = res["E_total"]
    e_elec_lda = res["E_elec"]
    iters = res["iters"]

    # Print the four energies with their sources.
    print("H2 in STO-3G at R = 1.4 a_0: four-method comparison")
    print("=" * 64)
    print(f"  RHF / STO-3G             E = {E_RHF_STO3G:+.4f} E_h")
    print("    (Szabo & Ostlund, Table 3.5; also chapter 06 script)")
    print(f"  KS-LDA / STO-3G          E = {E_KS_LDA:+.4f} E_h")
    print(
        "    (Dirac + Wigner, 01-h2-lda-scf.py,"
        f" {iters} SCF iters, E_elec = {e_elec_lda:+.4f} E_h)"
    )
    print(f"  Full CI / STO-3G         E = {E_FCI_STO3G:+.4f} E_h")
    print("    (Harrison-Handy CI benchmark, STO-3G H_2)")
    print(f"  Full CI / CBS            E = {E_NONREL_EXACT:+.4f} E_h")
    print("    (non-relativistic exact, Kolos-Wolniewicz curve)")
    print()
    print("Energy gaps relative to RHF (the 'correlation energy'):")
    for label, E in [
        ("KS-LDA / STO-3G ", E_KS_LDA),
        ("Full CI / STO-3G ", E_FCI_STO3G),
        ("Full CI / CBS   ", E_NONREL_EXACT),
    ]:
        gap_mha = (E - E_RHF_STO3G) * 1000.0
        print(f"  dE = E - E_RHF  ({label}) = {gap_mha:+7.1f} mHa")

    # ----------------------------------------------------------------
    # Bar chart
    # ----------------------------------------------------------------
    labels = [
        "RHF\nSTO-3G",
        "KS-LDA\nSTO-3G\n(this script)",
        "Full CI\nSTO-3G",
        "Full CI\nCBS\n(non-rel. exact)",
    ]
    energies = [E_RHF_STO3G, E_KS_LDA, E_FCI_STO3G, E_NONREL_EXACT]
    palette = ["#cc785c", "#5db8a6", "#e8a55a", "#a9583e"]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(8, 5.5))
    bars = ax.bar(
        x,
        energies,
        color=palette,
        edgecolor="#3d3d3a",
        linewidth=0.6,
        width=0.65,
    )

    # Annotate each bar with its numerical value (in E_h).
    for xi, E in zip(x, energies):
        ax.text(
            xi,
            E - 0.005,
            f"{E:+.4f}",
            ha="center",
            va="top",
            fontsize=10,
            color="#1d1d1b",
            fontweight="bold",
        )

    # Annotate the gap to RHF (in mHa) on top of each LDA/FCI bar.
    for xi, E in zip(x[1:], energies[1:]):
        gap_mha = (E - E_RHF_STO3G) * 1000.0
        ax.text(
            xi,
            E + 0.004,
            rf"$\Delta E = {gap_mha:+.0f}\,{{\rm mHa}}$",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#3d3d3a",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(r"$E_{\rm total}$  (Hartree)")
    ax.set_title(
        r"H$_2$ at $R = 1.4\,a_0$ — RHF, KS-LDA, and Full CI"
        + "\n(Dirac + Wigner LDA, single-zeta STO-3G basis)"
        + "\n(LDA bar is *above* HF: local X underbinds, Wigner C is small)"
    )
    # Y range: a bit above the least-bound bar, a bit below the
    # most-bound bar, with a comfortable margin.  NOTE: with the
    # Dirac + Wigner LDA used in this chapter the LDA bar sits
    # *above* the HF bar (the local exchange underestimates the
    # Fock exchange; the Wigner correlation is too weak to
    # compensate).  The y-range is chosen so all four bars are
    # visible regardless of the ordering.
    ax.set_ylim(-1.22, -0.99)
    ax.grid(True, axis="y", alpha=0.25)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    plots_dir = os.path.join(_here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "02-h2-ks-vs-hf.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
