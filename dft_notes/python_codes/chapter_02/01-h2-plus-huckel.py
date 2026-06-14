"""
01-h2-plus-huckel.py
====================

H_2^+ in the Huckel (tight-binding) approximation.

The 2x2 Huckel Hamiltonian for the two 1s AOs (one per proton) is

        H = [ alpha   beta  ]
            [ beta    alpha ]

with alpha = 0, beta = -1 (atomic units; only relative energies matter
since the diagonal cancels in symmetric problems).  The overlap
between two 1s STOs separated by R is

        S(R) = <1s_A | 1s_B> = exp(-R / a_0) = exp(-R)   (a_0 = 1 a.u.)

so the 2x2 generalised eigenvalue problem H C = S C E has the
closed-form solutions

        E_pm(R) = (alpha pm beta) / (1 pm S(R))
        c_pm(R) = 1 / sqrt(2 (1 pm S(R)))      (MO coefficient of 1s_A)

This is the "textbook" picture of the covalent bond: a bonding
sigma_g (E_- in [-1/2, 0]) and an antibonding sigma_u^* (E_+ in
[+1/2, +infinity)) that diverge as the two AOs decouple at large R.

What this script does:

  1.  Plots E_pm(R) and c_pm(R) on [0.5, 5.0] a_0.
  2.  Plots the two MOs psi_pm(z) along the bond axis at R = 2 a_0
      using 3-D 1s STOs with zeta = 1 centred on the two protons.
  3.  Prints the energies and coefficients at R = 1 a_0 as a
      numerical sanity check (E_- = -1/(1+e^-1) = -0.7310 a.u.).

Why this script lives in chapter 02:

    Section 2.x (the many-body problem) introduces the model
    Hamiltonian H = h_1 + h_2 + 1/r_12 as the building block of
    quantum chemistry.  The Huckel limit of H_2^+ (one electron,
    one orbital per atom, S != I, no e-e interaction) is the
    simplest example that exhibits bonding, antibonding, and
    basis-set non-orthogonality in a single 2x2 problem.  It is
    also the limiting case of a single-determinant FCI in the
    minimal basis (one electron, no correlation).

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_02/01-h2-plus-huckel.py

Writes its plot to:

    dft_notes/python_codes/chapter_02/plots/01-h2-plus-huckel.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
ALPHA = 0.0  # diagonal Huckel matrix element (a.u.)
BETA = -1.0  # off-diagonal Huckel matrix element (a.u.)
R_RANGE = (0.5, 5.0)  # a_0
N_R = 401  # grid points for E(R) and c(R)
R_SNAP = 2.0  # a_0, the bond length for the psi_pm snapshot
ZETA_STO = 1.0  # 1s STO exponent for H


def overlap_1s_1s(R):
    """S(R) = <1s_A | 1s_B> for two unit-exponent 1s STOs.

    In atomic units a_0 = 1 the well-known result is exp(-R).
    Accepts both a scalar and a numpy array.
    """
    return np.exp(-R)


def energies_coeffs(R: np.ndarray) -> tuple:
    """Return (E_plus, E_minus, c_plus, c_minus) on a grid of R.

    Bonding (sigma_g, E_-) and antibonding (sigma_u^*, E_+) branches
    of the Huckel spectrum, with alpha = 0 and beta = -1:

        E_-(R) = (alpha + beta) / (1 + S)   < 0  (bonding)
        E_+(R) = (alpha - beta) / (1 - S)   > 0  (antibonding)

        c_-(R) = 1 / sqrt(2 (1 + S))        (1s_A coefficient in sigma_g)
        c_+(R) = 1 / sqrt(2 (1 - S))        (1s_A coefficient in sigma_u^*)
    """
    S = overlap_1s_1s(R)
    E_minus = (ALPHA + BETA) / (1.0 + S)  # bonding branch
    E_plus = (ALPHA - BETA) / (1.0 - S)  # antibonding branch
    c_minus = 1.0 / np.sqrt(2.0 * (1.0 + S))  # sigma_g MO coefficient
    c_plus = 1.0 / np.sqrt(2.0 * (1.0 - S))  # sigma_u^* MO coefficient
    return E_plus, E_minus, c_plus, c_minus


def main() -> None:
    R = np.linspace(*R_RANGE, N_R)
    E_plus, E_minus, c_plus, c_minus = energies_coeffs(R)

    # Snapshot grid along the bond axis (z), with the two protons
    # at z = -R_SNAP/2 and z = +R_SNAP/2.
    z = np.linspace(-R_SNAP - 2.5, R_SNAP + 2.5, 601)
    zA = -R_SNAP / 2.0
    zB = +R_SNAP / 2.0
    # 3-D 1s STO with exponent zeta: phi(r) = (zeta^3/pi)^(1/2) exp(-zeta r)
    norm_3d = (ZETA_STO**3 / np.pi) ** 0.5
    phiA = norm_3d * np.exp(-ZETA_STO * np.abs(z - zA))
    phiB = norm_3d * np.exp(-ZETA_STO * np.abs(z - zB))
    S_snap = overlap_1s_1s(R_SNAP)
    c_m = 1.0 / np.sqrt(2.0 * (1.0 + S_snap))  # sigma_g (bonding) coefficient
    c_p = 1.0 / np.sqrt(2.0 * (1.0 - S_snap))  # sigma_u^* (antibonding) coefficient
    psi_plus = c_p * (phiA - phiB)  # antibonding: opposite sign, node at mid
    psi_minus = c_m * (phiA + phiB)  # bonding: same sign, no node

    # --- Sanity check at R = 1 a_0 -----------------------------------
    R_chk = 1.0
    S_chk = overlap_1s_1s(R_chk)
    E_p_chk = (ALPHA - BETA) / (1.0 - S_chk)
    E_m_chk = (ALPHA + BETA) / (1.0 + S_chk)
    c_p_chk = 1.0 / np.sqrt(2.0 * (1.0 - S_chk))
    c_m_chk = 1.0 / np.sqrt(2.0 * (1.0 + S_chk))
    print("H_2^+ in the Huckel approximation (alpha = 0, beta = -1 a.u.)")
    print(f"  S(R=1)              = {S_chk:.6f}")
    print(
        f"  E_-(R=1) bonding    = {E_m_chk:+.6f} a.u.   "
        f"(analytic: -1/(1+e^-1) = {-1.0 / (1.0 + np.exp(-1.0)):+.6f})"
    )
    print(
        f"  E_+(R=1) antibonding= {E_p_chk:+.6f} a.u.   "
        f"(analytic: +1/(1-e^-1) = {1.0 / (1.0 - np.exp(-1.0)):+.6f})"
    )
    print(
        f"  c_-(R=1)            = {c_m_chk:.6f}        "
        f"(-> 1/sqrt(2) = {1.0 / np.sqrt(2.0):.6f} as R -> infinity)"
    )
    print(f"  c_+(R=1)            = {c_p_chk:.6f}")
    print(f"  Dissociation limit: E_pm -> 0, c_pm -> 1/sqrt(2)")

    # --- Plot ---------------------------------------------------------
    fig, axes = plt.subplots(3, 1, figsize=(7.5, 10))

    palette = ["#cc785c", "#5db8a6"]  # coral = antibonding, teal = bonding
    label_p = r"$\sigma_u^* = E_+$  (antibonding)"
    label_m = r"$\sigma_g = E_-$  (bonding)"

    # (a) energies
    axes[0].plot(R, E_plus, color=palette[0], linewidth=2.2, label=label_p)
    axes[0].plot(R, E_minus, color=palette[1], linewidth=2.2, label=label_m)
    axes[0].axhline(0.0, color="#a09d96", lw=0.7, alpha=0.5)
    axes[0].axvline(1.0, color="#3d3d3a", lw=0.7, alpha=0.4, linestyle=":")
    axes[0].set_ylabel(r"$E_\pm(R)$  (Hartree)")
    axes[0].set_title(
        r"$H_2^+$ in the H\"uckel approximation "
        r"($\alpha = 0,\;\beta = -1$ a.u.)"
    )
    axes[0].legend(loc="upper right", frameon=False, fontsize=10)
    axes[0].grid(True, alpha=0.25)
    axes[0].set_xlim(*R_RANGE)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # (b) MO coefficients
    axes[1].plot(
        R,
        c_plus,
        color=palette[0],
        linewidth=2.2,
        label=r"$c_+(R) = \langle 1s_A | \sigma_u^* \rangle$",
    )
    axes[1].plot(
        R,
        c_minus,
        color=palette[1],
        linewidth=2.2,
        label=r"$c_-(R) = \langle 1s_A | \sigma_g \rangle$",
    )
    axes[1].axhline(
        1.0 / np.sqrt(2.0),
        color="#3d3d3a",
        lw=0.8,
        linestyle="--",
        alpha=0.6,
        label=r"$1/\sqrt{2}$  (atomic limit)",
    )
    axes[1].set_ylabel(r"$c_\pm(R)$")
    axes[1].legend(loc="upper right", frameon=False, fontsize=10)
    axes[1].grid(True, alpha=0.25)
    axes[1].set_xlim(*R_RANGE)
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    # (c) MOs at R = 2 a_0
    axes[2].plot(
        z,
        psi_plus,
        color=palette[0],
        linewidth=2.2,
        label=rf"$\psi_+ = (\phi_A - \phi_B)/\sqrt{{2(1-S)}}$, "
        rf"$E_+ = {E_plus[np.argmin(np.abs(R - R_SNAP))]:+.4f}\,E_h$",
    )
    axes[2].plot(
        z,
        psi_minus,
        color=palette[1],
        linewidth=2.2,
        label=rf"$\psi_- = (\phi_A + \phi_B)/\sqrt{{2(1+S)}}$, "
        rf"$E_- = {E_minus[np.argmin(np.abs(R - R_SNAP))]:+.4f}\,E_h$",
    )
    axes[2].plot(
        z,
        +phiA,
        color="#a09d96",
        lw=1.0,
        alpha=0.6,
        label=r"$\phi_A,\;\phi_B$ (atomic 1s STO)",
    )
    axes[2].plot(z, +phiB, color="#a09d96", lw=1.0, alpha=0.6)
    axes[2].axhline(0.0, color="#a09d96", lw=0.6, alpha=0.5)
    axes[2].axvline(zA, color="#3d3d3a", lw=0.8, alpha=0.4, linestyle=":")
    axes[2].axvline(zB, color="#3d3d3a", lw=0.8, alpha=0.4, linestyle=":")
    axes[2].set_xlabel(r"$z$  (atomic units, along bond axis)")
    axes[2].set_ylabel(r"$\psi(z)$  (a.u.)")
    axes[2].set_title(
        rf"Molecular orbitals at $R = {R_SNAP}\,a_0$"
        rf"  ($S = {S_snap:.4f}$)"
    )
    axes[2].legend(loc="upper right", frameon=False, fontsize=9)
    axes[2].grid(True, alpha=0.25)
    axes[2].spines["top"].set_visible(False)
    axes[2].spines["right"].set_visible(False)

    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-h2-plus-huckel.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
