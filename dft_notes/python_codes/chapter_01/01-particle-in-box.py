"""
01-particle-in-box.py
=====================
Particle in a 1-D infinite well (the "particle in a box") of
length L = 1 a_0.

Plots the first four eigenfunctions

    psi_n(x) = sqrt(2 / L) * sin(n * pi * x / L),    0 < x < L,

and the corresponding probability densities |psi_n(x)|^2.
The first four eigenvalues in atomic units (hbar^2 / m_e = 1)
are

    E_n = (pi^2 / 2) * n^2,

so for L = 1 the ground-state energy is
E_1 = pi^2 / 2 = 4.93480 Hartree.

Why this script lives in chapter 01's python_codes folder:

  - Chapter 01 (Schroedinger equation), section 1.3 ("A minimal
    example: the particle in a box") introduces the analytic
    eigenfunctions and quotes the eigenvalues.  This script is
    the source of truth for the numbers; the chapter copy is
    inlined for reading.
  - The plot is the canonical "what a bound state looks like"
    visual that every later chapter (basis sets, solids) refers
    back to.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_01/01-particle-in-box.py

Writes its plot to:

    dft_notes/python_codes/chapter_01/plots/01-particle-in-box.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless -- no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Analytic solution
# ---------------------------------------------------------------------------
def psi_n(n: int, x: np.ndarray, L: float) -> np.ndarray:
    """Normalised n-th eigenfunction of the 1-D particle in a box.

    psi_n(x) = sqrt(2 / L) * sin(n * pi * x / L),   0 < x < L,
    psi_n(0) = psi_n(L) = 0,    int_0^L |psi_n|^2 dx = 1.
    """
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)


def energy_n(n: int, L: float) -> float:
    """The n-th eigenvalue in atomic units (hbar^2 / m_e = 1).

    E_n = n^2 * pi^2 / (2 L^2).
    """
    return (n * n * np.pi * np.pi) / (2.0 * L * L)


def main() -> None:
    # --- Parameters ----------------------------------------------------
    L = 1.0  # box length, atomic units
    N_POINTS = 401  # sampling grid inside the box
    LEVELS = (1, 2, 3, 4)  # the four states to plot

    # The x grid.  Avoid exactly x = 0 and x = L because the
    # wavefunctions vanish there; we sample just inside the
    # walls.  The mid-points of the box are where the lobes peak.
    x = np.linspace(0.0, L, N_POINTS)

    # --- Verify the energies against the analytic formula --------------
    print("Particle in a box (L = 1 a_0)")
    print("=" * 38)
    print(f"  E_1 analytic = pi^2 / 2 = {0.5 * np.pi**2:.6f} E_h")
    print(f"  E_1 numeric  = {energy_n(1, L):.6f} E_h")
    print()
    print("  n   E_n analytic (E_h)   E_n = n^2 pi^2 / 2  (exact)")
    for n in LEVELS:
        E = energy_n(n, L)
        exact = n * n * np.pi**2 / 2.0
        delta = E - exact
        print(f"  {n}   {E:18.6f}   {exact:18.6f}   delta = {delta:+.2e}")

    # --- Figure: 2 rows x 1 column -------------------------------------
    #   top    : wavefunctions psi_n(x) for n = 1..4
    #   bottom : probability densities |psi_n(x)|^2 for the same n
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(7, 5),
        sharex=True,
        gridspec_kw={"height_ratios": (2, 2)},
    )

    # Brand palette -- same coral / amber / teal as the rest of the site.
    palette = {
        1: "#cc785c",  # coral   (primary)
        2: "#e8a55a",  # amber
        3: "#5db8a6",  # teal
        4: "#a9583e",  # coral, active
    }
    for n in LEVELS:
        psi = psi_n(n, x, L)
        E = energy_n(n, L)
        axes[0].plot(
            x,
            psi,
            color=palette[n],
            linewidth=2.0,
            label=rf"$\psi_{n}(x)$, $E_{n} = {E:.3f}\ E_h$",
        )
        axes[1].plot(
            x,
            psi * psi,
            color=palette[n],
            linewidth=2.0,
            label=rf"$|\psi_{n}(x)|^{{2}}$",
        )

    # --- Cosmetics -----------------------------------------------------
    axes[0].axhline(0, color="#a09d96", linewidth=0.8, alpha=0.5)
    axes[0].set_ylabel(r"$\psi_n(x)$")
    axes[0].legend(loc="upper right", frameon=False, fontsize=9)
    axes[0].set_title(rf"Particle in a box, $L = 1\,a_0$  --  $E_n = n^2 \pi^2 / 2$")

    axes[1].set_xlabel(r"$x$  (atomic units, $a_0$)")
    axes[1].set_ylabel(r"$|\psi_n(x)|^{2}$")
    axes[1].legend(loc="upper right", frameon=False, fontsize=9)

    for ax in axes:
        ax.grid(True, alpha=0.2)
        # Mark the box walls.
        ax.axvline(0, color="#3d3d3a", linewidth=0.8, alpha=0.5)
        ax.axvline(L, color="#3d3d3a", linewidth=0.8, alpha=0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()

    # --- Write the plot -----------------------------------------------
    # Resolve the output path relative to THIS file, not the
    # current working directory -- the script is meant to be
    # runnable from anywhere in the repo.
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-particle-in-box.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
