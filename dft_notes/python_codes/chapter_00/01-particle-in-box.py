"""
01-particle-in-box.py
=====================
Plots the first four eigenfunctions of the 1-D particle in a box
of length L, plus the corresponding probability densities.  This
is the "hello world" of quantum mechanics — the simplest system
that has the structure (quantised energy levels, nodes,
orthonormal basis) that every later chapter will build on.

Why this script lives in the chapters python_codes folder:
  - Chapter 01 (Schrödinger equation) inlines a discretised
    version of this in Section 1.3 — but the *closed-form*
    analytic version is the right place to start.  The
    inlined numpy.linalg.eigh version is the "from-scratch"
    path; this one is the "use the known answer" path.
  - Chapter 02 (Many-body) reuses `sin(n*pi*x/L)` as the
    one-electron basis.
  - The plot here is the canonical visual for "what a bound
    state looks like", which every later chapter will
    reference.

Dependencies: numpy, matplotlib (headless via `Agg`).

Run from the repo root:
    python dft_notes/python_codes/chapter_00/01-particle-in-box.py

Writes its plot to:
    dft_notes/python_codes/chapter_00/plots/01-particle-in-box.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless — no display required
import matplotlib.pyplot as plt


def psi_n(n: int, x: np.ndarray, L: float) -> np.ndarray:
    """The n-th eigenfunction of the 1-D particle in a box.

    ψ_n(x) = sqrt(2/L) * sin(n * pi * x / L),   for 0 < x < L,
    ψ_n(0) = ψ_n(L) = 0,    normalisation ∫|ψ|² dx = 1.
    """
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)


def energy_n(n: int, L: float) -> float:
    """The n-th eigenvalue in atomic units (ħ²/m_e = 1).

    E_n = (n² π²) / (2 L²).
    """
    return (n * n * np.pi * np.pi) / (2.0 * L * L)


def main() -> None:
    # --- Parameters --------------------------------------------------
    L = 1.0  # box length (atomic units)
    N_POINTS = 401  # sampling grid inside the box
    LEVELS = (1, 2, 3, 4)  # the four states to plot

    # The x grid.  We avoid exactly x = 0 and x = L because the
    # wavefunctions are zero at the boundaries and we'd just be
    # plotting zeros.
    x = np.linspace(0.0, L, N_POINTS)

    # --- Figure: 2 rows × 1 column -----------------------------------
    #   top    : wavefunctions ψ_n(x) for n = 1..4
    #   bottom : probability densities |ψ_n(x)|² for the same n
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(7, 5),
        sharex=True,
        gridspec_kw={"height_ratios": (2, 2)},
    )

    # Brand palette — same coral / amber / teal as the site.
    # Pulled into RGB tuples so matplotlib (which wants 0–1 floats)
    # can use them.
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
            label=rf"$\psi_{n}(x)$, $E_{n} = {E:.3f}$ E$_h$",
        )
        axes[1].plot(
            x,
            psi * psi,
            color=palette[n],
            linewidth=2.0,
            label=rf"$|\psi_{n}(x)|^{{2}}$",
        )

    # --- Cosmetics ---------------------------------------------------
    axes[0].axhline(0, color="#a09d96", linewidth=0.8, alpha=0.5)
    axes[0].set_ylabel(r"$\psi_n(x)$")
    axes[0].legend(loc="upper right", frameon=False, fontsize=9)
    axes[0].set_title("Particle in a box — the simplest bound quantum system")

    axes[1].set_xlabel(r"$x$  (atomic units)")
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

    # --- Write the plot ----------------------------------------------
    # Resolve the output path relative to THIS file, not the
    # current working directory — the script is meant to be
    # runnable from anywhere in the repo.
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-particle-in-box.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
