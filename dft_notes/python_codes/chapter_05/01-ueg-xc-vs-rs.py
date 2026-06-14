"""
01-ueg-xc-vs-rs.py
==================

Uniform Electron Gas (UEG) exchange-correlation energy per
particle as a function of the Wigner-Seitz radius r_s.

This is the data on which every modern LDA functional is built.
The script compares three pieces:

  1.  The Dirac LDA exchange
           eps_x(r_s) = -0.458165 / r_s            (Hartree)

  2.  The Wigner interpolation
           eps_c(r_s) = -0.088 / (r_s + 7.8)

  3.  The Perdew-Zunger (1981) fit to the Ceperley-Alder
      quantum-Monte-Carlo data for the *unpolarized* UEG
      (J. P. Perdew and A. Zunger, Phys. Rev. B 23, 5048
      (1981), Table I):
           rs < 1  :  eps_c = B + A ln rs + D rs + C rs ln rs
           rs >= 1 :  eps_c = A_pz / (1 + B_pz sqrt(rs) + C_pz rs)
      with (A, B, C, D) = (0.0311, -0.0480, 0.0020, -0.0116) and
      (A_pz, B_pz, C_pz) = (-0.1423, 1.0529, 0.3334).

Plot: eps_x, eps_c (PZ81) and eps_xc = eps_x + eps_c for
r_s in [0.5, 10] bohr, with the r_s of typical simple metals
(Al, Na, Cs) marked.

Why this lives in chapter 05:
    Section 5.1 of chapter 05 (the uniform electron gas)
    introduces the UEG and the r_s parameter.  This script
    is the runnable counterpart of the formulas on that page.

Run from the repo root:
    python dft_notes/python_codes/chapter_05/01-ueg-xc-vs-rs.py

Writes the plot to:
    dft_notes/python_codes/chapter_05/plots/01-ueg-xc-vs-rs.png

Dependencies: numpy, matplotlib (headless via Agg).
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ─── Reference values ──────────────────────────────────────────────
# The Dirac-LDA exchange coefficient.  eps_x(r_s) = -Cx / r_s with
#   Cx = (3 / (4 pi)) * (9 pi / 4)^{1/3} = 0.45816519...
DIRAC_X_COEF = 0.458165

# Wigner interpolation: eps_c(r_s) = -A / (r_s + B)
WIGNER_A = 0.088
WIGNER_B = 7.8

# Perdew-Zunger (1981), Table I, unpolarized UEG.
# High-density branch: eps_c = B + A * ln(rs) + D * rs + C * rs * ln(rs)
PZ_HIGH_DENSITY = {
    "A": 0.0311,  # coefficient of ln r_s
    "B": -0.0480,  # constant term
    "C": 0.0020,  # coefficient of r_s * ln r_s
    "D": -0.0116,  # coefficient of r_s
}
# Low-density branch: eps_c = A_pz / (1 + B_pz * sqrt(rs) + C_pz * rs)
PZ_LOW_DENSITY = {
    "A": -0.1423,
    "B": 1.0529,
    "C": 0.3334,
}

# Typical r_s for jellium models of simple metals
RS_METALS = {
    "Al": 2.07,
    "Na": 3.93,
    "Cs": 5.62,
}


# ─── Energy formulas ───────────────────────────────────────────────
def dirac_exchange(rs):
    """LDA exchange per particle (Dirac, 1930) in Hartree.

    eps_x(r_s) = -Cx / r_s,   Cx = (3 / 4 pi) * (9 pi / 4)^{1/3}.
    """
    return -DIRAC_X_COEF / rs


def wigner_correlation(rs):
    """Wigner interpolation formula for the correlation energy
    per particle of the unpolarized UEG.  Approximate, but
    easy to remember and widely used in textbooks.
    """
    return -WIGNER_A / (rs + WIGNER_B)


def pz81_correlation_unpolarized(rs):
    """Perdew-Zunger (1981) fit to Ceperley-Alder QMC correlation
    energy per particle for the *unpolarized* UEG.

    Reference: J. P. Perdew and A. Zunger, Phys. Rev. B 23, 5048
    (1981), Table I (unpolarized case).

    Two regimes:
        r_s < 1  :  eps_c = B + A * ln(r_s) + D * r_s
                          + C * r_s * ln(r_s)
        r_s >= 1 :  eps_c = A_pz / (1 + B_pz * sqrt(r_s)
                                       + C_pz * r_s)
    """
    rs = np.asarray(rs, dtype=float)
    ec = np.empty_like(rs)

    mask_lo = rs < 1.0
    rs_lo = rs[mask_lo]
    c = PZ_HIGH_DENSITY
    ec[mask_lo] = (
        c["B"]
        + c["A"] * np.log(rs_lo)
        + c["D"] * rs_lo
        + c["C"] * rs_lo * np.log(rs_lo)
    )

    rs_hi = rs[~mask_lo]
    c = PZ_LOW_DENSITY
    ec[~mask_lo] = c["A"] / (1.0 + c["B"] * np.sqrt(rs_hi) + c["C"] * rs_hi)

    return ec


# ─── Main ──────────────────────────────────────────────────────────
def main() -> None:
    rs = np.linspace(0.5, 10.0, 500)

    ex = dirac_exchange(rs)
    ec_pz = pz81_correlation_unpolarized(rs)
    ec_wig = wigner_correlation(rs)
    exc = ex + ec_pz

    # Reference check at r_s = 2: PZ81 correlation ~ -0.0451 Eh
    # (textbook: ~ -0.0457 Eh; agreement within 0.001 Eh)
    rs_check = 2.0
    ex_at_2 = dirac_exchange(np.array([rs_check]))[0]
    ec_at_2 = pz81_correlation_unpolarized(np.array([rs_check]))[0]
    exc_at_2 = ex_at_2 + ec_at_2

    print("=" * 60)
    print("UEG exchange-correlation energy per particle")
    print("Perdew-Zunger (1981) fit to Ceperley-Alder QMC,")
    print("unpolarized UEG.")
    print("=" * 60)
    print(f"  At r_s = {rs_check:.2f} bohr:")
    print(f"    eps_x         = {ex_at_2:+.6f} E_h")
    print(f"    eps_c (PZ81)  = {ec_at_2:+.6f} E_h  (textbook: -0.0457)")
    print(f"    eps_xc        = {exc_at_2:+.6f} E_h")
    print()
    print("r_s values for typical simple metals (jellium model):")
    for name, r in RS_METALS.items():
        e_x = dirac_exchange(np.array([r]))[0]
        e_c = pz81_correlation_unpolarized(np.array([r]))[0]
        print(
            f"  {name:>2s}: r_s = {r:5.2f}  ->"
            f"  eps_x = {e_x:+.4f},"
            f" eps_c = {e_c:+.4f},"
            f" eps_xc = {e_x + e_c:+.4f} E_h"
        )

    # ─── Plot ──────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5.5))

    ax.plot(
        rs,
        ex,
        color="#cc785c",
        linewidth=2.0,
        label=r"Dirac exchange  $\varepsilon_x(r_s) = -0.4582/r_s$",
    )
    ax.plot(
        rs,
        ec_pz,
        color="#5db8a6",
        linewidth=2.0,
        label=r"PZ81 correlation  $\varepsilon_c^{\rm PZ81}(r_s)$",
    )
    ax.plot(
        rs,
        ec_wig,
        color="#e8a55a",
        linewidth=1.5,
        linestyle="--",
        label=r"Wigner  $-0.088/(r_s + 7.8)$",
    )
    ax.plot(
        rs,
        exc,
        color="#3d3d3a",
        linewidth=2.0,
        label=r"$\varepsilon_{xc}(r_s) = \varepsilon_x + \varepsilon_c$  (LDA)",
    )

    # Mark the typical r_s of Al, Na, Cs
    for name, r in RS_METALS.items():
        ax.axvline(r, color="#a09d96", linewidth=0.6, linestyle=":", alpha=0.7)
        ax.annotate(
            name,
            xy=(r, -0.5),
            xytext=(r + 0.15, -0.5),
            fontsize=10,
            color="#3d3d3a",
        )

    # Reference point at r_s = 2
    ax.plot(
        [2.0],
        [exc_at_2],
        "o",
        color="#a9583e",
        markersize=7,
        zorder=5,
        label=rf"$r_s=2$ check: $\varepsilon_{{xc}} = {exc_at_2:+.4f}\,E_h$",
    )

    ax.axhline(0.0, color="#a09d96", linewidth=0.6, alpha=0.5)
    ax.set_xlabel(r"Wigner-Seitz radius  $r_s$  (bohr)")
    ax.set_ylabel(r"$\varepsilon_{xc}(r_s)$  (Hartree / electron)")
    ax.set_title("Uniform electron gas: exchange and correlation")
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(0.5, 10.0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    # ─── Save ──────────────────────────────────────────────────────
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-ueg-xc-vs-rs.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
