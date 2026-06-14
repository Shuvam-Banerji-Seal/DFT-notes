"""
01-free-electron-bands.py
==========================

Band structure of a 1-D periodic lattice with a cosine potential.

    V(x) = -0.5 cos(2 pi x / a),    a = 5.0 bohr

This is the textbook "nearly-free-electron" model: a free electron
perturbed by a weak periodic potential.  We expand in 21 plane waves
( G = m * 2pi/a  for m = -10, -9, ..., +9, +10 ) and diagonalise
the resulting 21 x 21 plane-wave Hamiltonian at 100 k-points
uniformly distributed in the 1st Brillouin zone [ -pi/a, +pi/a ].

The plot shows the first 4 bands as a function of k.  Two visual
sanity checks are visible in the figure:

  1.  At the BZ boundary  k = +/- pi/a,  the bands are split by
      the matrix element 2 * |V(2 pi / a)| = 0.5 Hartree.
  2.  The first Brillouin zone is the interval
       -pi/a <= k <= +pi/a,  marked by dashed vertical lines.

Why this script lives in the chapters python_codes folder:

  - Chapter 07 (Solids & PBC) inlines a copy of this script in
    Section 7.7 as the worked example.  The chapter is the
    readable narrative; the script is the source of truth.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_07/01-free-electron-bands.py

Writes its plot to:

    dft_notes/python_codes/chapter_07/plots/01-free-electron-bands.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
A = 5.0  # lattice constant, bohr
V0 = -0.5  # depth of the cosine potential, Hartree
N_PW = 21  # number of plane waves (must be odd, so G=0 is included)
N_K = 100  # number of k-points in the 1st Brillouin zone
B = 2.0 * np.pi / A  # reciprocal lattice constant in 1-D, bohr^-1

# Sanity check: 21 plane waves means m in -10..+10.
assert N_PW % 2 == 1, "N_PW must be odd so that G = 0 is included."


def fourier_coefficients(m_vals: np.ndarray) -> np.ndarray:
    """V_periodic(G_m' - G_m) for V(x) = V0 cos(2 pi x / a).

    V(x) = V0 * cos(2 pi x / a)
         = (V0 / 2) * e^{i 2 pi x / a}
         + (V0 / 2) * e^{-i 2 pi x / a}

    so the only non-zero Fourier coefficients on the reciprocal-
    lattice grid G = m * 2 pi / a are

        V_periodic(+/- 2 pi / a) = V0 / 2.

    The corresponding matrix element is
        V_periodic(G_m' - G_m) = V0 / 2  iff  m' - m = +/- 1,
    and zero otherwise (including m' - m = 0, because the
    average of V over one period is zero).

    Returns a real symmetric (N_PW, N_PW) matrix V[m', m].
    """
    N = m_vals.size
    V_mat = np.zeros((N, N), dtype=float)
    for i in range(N):
        for j in range(N):
            d = m_vals[i] - m_vals[j]
            if d == 1 or d == -1:
                V_mat[i, j] = V0 / 2.0
    return V_mat


def hamiltonian(k: float, G_vals: np.ndarray, V_mat: np.ndarray) -> np.ndarray:
    """Build the 21 x 21 plane-wave Hamiltonian at a single k-point.

    H_{m m'}(k) = (1/2) (k + G_m)^2  delta_{m m'}
                 + V_periodic(G_m' - G_m).
    """
    H_kin = 0.5 * (k + G_vals) ** 2  # diagonal kinetic term
    return np.diag(H_kin) + V_mat


def diagonalise_along_kpath(
    k_vals: np.ndarray, G_vals: np.ndarray, V_mat: np.ndarray
) -> np.ndarray:
    """Return a (len(k_vals), N_PW) array of band energies."""
    bands = np.zeros((k_vals.size, G_vals.size))
    for ik, k in enumerate(k_vals):
        H = hamiltonian(k, G_vals, V_mat)
        # eigvalsh: H is real symmetric; we want only the eigenvalues.
        bands[ik, :] = np.linalg.eigvalsh(H)
    return bands


def main() -> None:
    # --- Reciprocal lattice vectors in the plane-wave basis -------------
    m_vals = np.arange(-(N_PW // 2), N_PW // 2 + 1)  # -10, -9, ..., +9, +10
    G_vals = m_vals * B

    # --- k-mesh in the 1st Brillouin zone -------------------------------
    # Uniform mesh on [-pi/a, +pi/a).  endpoint=False is the
    # Monkhorst-Pack "open" convention; either open or closed is
    # fine for a band-structure plot.
    k_vals = np.linspace(-np.pi / A, np.pi / A, N_K, endpoint=False)

    # --- Build the potential matrix and diagonalise ---------------------
    V_mat = fourier_coefficients(m_vals)
    bands = diagonalise_along_kpath(k_vals, G_vals, V_mat)

    # --- Sanity check: the 2 x 2 gap at the BZ boundary -----------------
    # Pick the two k-points closest to k = +pi/a, take the lowest
    # two bands, and verify that the gap is approximately 0.5 Hartree.
    ik_bz = int(np.argmin(np.abs(k_vals - np.pi / A)))
    eps_lo = bands[ik_bz, 0]
    eps_hi = bands[ik_bz, 1]
    gap_predicted = 2.0 * abs(V0 / 2.0)  # = |V0| = 0.5 Hartree
    print(
        f"At k = +pi/a (ik = {ik_bz}, k = {k_vals[ik_bz]:+.5f} bohr^-1):"
        f"  eps_1 = {eps_lo:+.5f} E_h,"
        f"  eps_2 = {eps_hi:+.5f} E_h,"
        f"  gap = {eps_hi - eps_lo:+.5f} E_h"
        f"  (predicted {gap_predicted:+.5f} E_h)"
    )

    # --- Plot the first 4 bands ----------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    # Brand palette - same coral / amber / teal as the rest of the site.
    palette = ["#cc785c", "#e8a55a", "#5db8a6", "#a9583e"]
    for n in range(4):
        ax.plot(
            k_vals * A / np.pi,
            bands[:, n],
            color=palette[n],
            linewidth=2.0,
            label=rf"band {n + 1}",
        )

    # Free-electron parabolas in light grey for reference.  The first
    # BZ is mapped by G = m * b for m in Z, so the free-electron band
    # n in the reduced-zone scheme is 0.5 * (k + m * b)^2 for the
    # appropriate m.  We draw the four most relevant ones.
    for m, ls in zip((0, -1, 1, -2), (":", ":", ":", ":")):
        ax.plot(
            k_vals * A / np.pi,
            0.5 * (k_vals + m * B) ** 2,
            color="#a09d96",
            linewidth=0.7,
            alpha=0.45,
        )

    # Mark the BZ boundaries and zero of energy.
    ax.axvline(-1.0, color="#3d3d3a", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvline(+1.0, color="#3d3d3a", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axhline(0.0, color="#a09d96", linewidth=0.8, alpha=0.3)

    # Labels and cosmetics.
    ax.set_xlabel(r"$k a / \pi$")
    ax.set_ylabel(r"$\varepsilon_n(k)$  (Hartree)")
    ax.set_title("1-D band structure, $a = 5$ bohr, $V(x) = -0.5 \\cos(2\\pi x/a)$")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(-1.0, 1.0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    # --- Save the plot --------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-free-electron-bands.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
