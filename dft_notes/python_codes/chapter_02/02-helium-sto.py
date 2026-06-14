"""
02-helium-sto.py
================

Variational ground-state energy of the helium atom in a
*minimal* Slater-type-orbital (STO) basis: one normalised 1s STO

    phi(r) = (zeta^3 / pi)^(1/2) exp(-zeta r)

for each of the two electrons.  The two electrons are paired in a
single spatial orbital, forming a closed-shell singlet.  The
spatial part of the wavefunction is therefore simply the product
phi(r_1) phi(r_2), and the only variational parameter is zeta.

The Hamiltonian is

    H = -1/2 nabla_1^2 - 1/2 nabla_2^2
        - Z / r_1 - Z / r_2
        + 1 / r_12

with Z = 2 for helium.  The closed-shell singlet expectation value
of H in the single-orbital ansatz is (Slater, "Quantum Theory of
Atomic Structure", vol. 1, ch. 8)

    E(zeta) = 2 h_11(zeta) + J_11(zeta)

where, for a normalised 1s STO with exponent zeta on a nucleus of
charge Z,

    h_11(zeta) = <1s | -1/2 nabla^2 - Z/r | 1s>
               = zeta^2 / 2 - Z * zeta                (a.u.)

    J_11(zeta) = <1s 1s | 1/r_12 | 1s 1s> = 5 zeta / 8   (a.u.)

For Z = 2 this gives

    E(zeta) = zeta^2 - 4 zeta + 5 zeta / 8 = zeta^2 - (27/8) zeta.

The minimum is at dE/dzeta = 0 -> zeta* = 27/16 = 1.6875, with

    E_min = E(zeta*) = -729 / 256 = -2.84766 Hartree.

The "exact" non-relativistic helium ground-state energy is
-2.86168 Hartree (Hylleraas 1929; the modern value is
-2.90372... once relativistic + QED corrections are added, but
the variational reference is the non-relativistic Hylleraas
number).  The 0.014 Ha gap is the *missing correlation energy*
in this minimal basis: a single Slater determinant built from
one STO cannot describe the instantaneous electron-electron
cusp.

What this script does:

  1.  Plots E(zeta) for zeta in [0.5, 3.0] Hartree.
  2.  Marks the variational minimum with a coral dot.
  3.  Draws a horizontal dashed line at the Hylleraas reference
      E = -2.8617 Ha, so the missing correlation energy is
      immediately readable off the figure.
  4.  Prints the optimum, E_min, and the missing correlation
      energy (E_min - E_Hylleraas).

Why this script lives in chapter 02:

    Section 2.x (the many-body problem) introduces the electron-
    electron repulsion 1/r_12 as the source of "correlation", the
    effect absent from mean-field / single-determinant pictures.
    Helium in one STO is the simplest closed-shell 2-electron
    problem where 1/r_12 contributes a non-zero, zeta-dependent
    matrix element, and where the variational optimum is
    computable by hand.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_02/02-helium-sto.py

Writes its plot to:

    dft_notes/python_codes/chapter_02/plots/02-helium-sto.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
Z_NUC = 2  # helium nuclear charge
Z_RANGE = (0.5, 3.0)  # STO exponent grid
N_Z = 601  # grid points
E_HYLLERAAS = -2.86168  # Ha, the non-relativistic "exact" helium ground state


def h_11(zeta: np.ndarray) -> np.ndarray:
    """One-electron integral h_11(zeta) = zeta^2/2 - Z*zeta.

    This is <1s| -1/2 nabla^2 - Z/r |1s> for a normalised 1s STO.
    """
    return 0.5 * zeta**2 - Z_NUC * zeta


def J_11(zeta: np.ndarray) -> np.ndarray:
    """Coulomb self-repulsion J_11(zeta) = 5 zeta / 8.

    Derivation: <1s 1s | 1/r_12 | 1s 1s> with a normalised 1s STO.
    Standard Slater integral (Slater, QTAS vol. 1, table 8-1).
    """
    return 5.0 / 8.0 * zeta


def energy(zeta: np.ndarray) -> np.ndarray:
    """Closed-shell singlet variational energy in the 1-STO basis."""
    return 2.0 * h_11(zeta) + J_11(zeta)


def main() -> None:
    zeta = np.linspace(*Z_RANGE, N_Z)
    E = energy(zeta)

    # Closed-form optimum (parabola minimum)
    # E(zeta) = zeta^2 - 2Z*zeta + 5 zeta / 8 = (zeta - (Z - 5/16))^2 - (Z - 5/16)^2
    zeta_opt = Z_NUC - 5.0 / 16.0  # = 27/16 = 1.6875 for Z = 2
    E_min = -((16.0 * Z_NUC - 5.0) ** 2) / 256.0  # = -729/256 = -2.84766 Ha for Z=2
    dE_corr = E_min - E_HYLLERAAS  # positive = missing correlation

    print("Helium 1-STO variational calculation (Z = 2, closed-shell singlet)")
    print(f"  E(zeta) = zeta^2 - 4 zeta + 5 zeta / 8")
    print(
        f"  Optimum zeta*             = {zeta_opt:.6f}   "
        f"(analytic 27/16 = {27.0 / 16.0:.6f})"
    )
    print(
        f"  E_min = E(zeta*)          = {E_min:+.6f} Ha  "
        f"(analytic -729/256 = {-729.0 / 256.0:+.6f})"
    )
    print(f"  Hylleraas reference       = {E_HYLLERAAS:+.6f} Ha")
    print(
        f"  Missing correlation energy= {dE_corr:+.6f} Ha "
        f"( = {dE_corr * 1000:+.3f} mHa )"
    )

    # --- Plot ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5.2))

    palette = ["#cc785c", "#5db8a6", "#3d3d3a"]

    # E(zeta) curve
    ax.plot(
        zeta,
        E,
        color=palette[0],
        linewidth=2.4,
        label=r"$E(\zeta) = \zeta^2 - 4\zeta + \frac{5}{8}\,\zeta$",
    )

    # Hylleraas reference
    ax.axhline(
        E_HYLLERAAS,
        color=palette[1],
        linewidth=1.6,
        linestyle="--",
        alpha=0.9,
        label=rf"Hylleraas: $E = {E_HYLLERAAS:+.4f}\,E_h$  "
        rf"(non-relativistic exact)",
    )

    # Variational minimum
    ax.plot(
        zeta_opt,
        E_min,
        marker="o",
        markersize=9,
        color=palette[0],
        markeredgecolor=palette[2],
        markeredgewidth=1.2,
        zorder=5,
        label=rf"Variational minimum  "
        rf"($\zeta^* = {zeta_opt:.4f}$, "
        rf"$E = {E_min:+.4f}\,E_h$)",
    )

    # Vertical guide from x-axis to the minimum
    ax.axvline(zeta_opt, color=palette[2], lw=0.7, alpha=0.4, linestyle=":")
    ax.axhline(0.0, color="#a09d96", lw=0.7, alpha=0.5)

    # Annotate the correlation gap
    ax.annotate(
        rf"missing correlation" "\n" rf"$\Delta E = {dE_corr * 1000:+.1f}$ mHa",
        xy=(zeta_opt + 0.12, (E_min + E_HYLLERAAS) / 2.0),
        xytext=(zeta_opt + 0.7, (E_min + E_HYLLERAAS) / 2.0 + 0.10),
        fontsize=10,
        color=palette[2],
        arrowprops=dict(arrowstyle="->", color=palette[2], lw=1.0),
    )

    ax.set_xlabel(r"$\zeta$  (STO exponent, a.u.)")
    ax.set_ylabel(r"$E(\zeta)$  (Hartree)")
    ax.set_title(
        r"Helium atom in a single 1s STO: variational optimum "
        r"and the missing correlation energy"
    )
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(*Z_RANGE)
    ax.set_ylim(-3.4, 0.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "02-helium-sto.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
