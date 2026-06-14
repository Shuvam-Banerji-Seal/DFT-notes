"""
03-monkhorst-pack-convergence.py
================================

Convergence of the Brillouin-zone integral of a simple-cubic (SC)
tight-binding dispersion as a function of the Monkhorst-Pack (MP)
k-point grid density.

Model: single s-orbital per site on a simple cubic lattice with
nearest-neighbour hopping -t.  The dispersion is

    E(k) = -2t [ cos(k_x a) + cos(k_y a) + cos(k_z a) ].

We use the *centered* (shifted) MP mesh

    k_i = (2 m - n - 1) / (2 n)  in units of 2 pi / a,  m = 1, ..., n,

which is symmetric around k = 0 and is the form used in most modern
solid-state codes (VASP, Quantum ESPRESSO, CASTEP).  The "total energy
per unit cell" is the uniform average over the BZ:

    E_tot / N  =  (1 / n^3)  sum_{k in MP(n x n x n)}  E(k).

We compute this for n in {2, 4, 6, 8, 10, 12, 16, 20} and plot the
absolute error versus the n = 20 result on a log-y axis.

A mathematical observation worth noting in the plot and the report:

  For *general* smooth integrands the MP error scales as
  O(1/n^2) in 1-D and O(1/n^{2/3}) in 3-D (chapter 7, eq. 7.21).
  But for the specific integrand used here, the dispersion is a sum
  of three cosine terms, and each cosine is *itself* a single Fourier
  mode of the BZ.  The centered MP mesh samples these modes with
  *exact* zero mean for all even n >= 2 (the mesh is symmetric about
  k = 0, and the cosine is even, so the positive-k contributions
  cancel the negative-k contributions by symmetry).  In exact
  arithmetic the discrete sum is 0; in floating point it is at the
  machine-precision floor (~1e-15 for double precision).

  So the convergence of THIS particular integrand is faster than the
  textbook 1/n^2 prediction; the plot shows this with a C/n^2
  reference line for visual comparison.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:
    python dft_notes/python_codes/chapter_07/03-monkhorst-pack-convergence.py

Writes its plot to:
    dft_notes/python_codes/chapter_07/plots/03-monkhorst-pack-convergence.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
A = 1.0  # simple cubic lattice constant (arbitrary units)
T = 1.0  # nearest-neighbour hopping magnitude  (arbitrary units; t > 0)
N_VALUES = [2, 4, 6, 8, 10, 12, 16, 20]


def mp_offsets_1d(n: int) -> np.ndarray:
    """Return the n centered Monkhorst-Pack mesh offsets in units of 2 pi / a.

    The mesh is symmetric around k = 0:
        k_i = (2 m - n - 1) / (2 n),  m = 1, 2, ..., n.
    For n = 4 this gives the offsets {-3/8, -1/8, +1/8, +3/8} (in 2 pi / a);
    for n = 3 it gives {-1/3, 0, +1/3} (the Gamma point is included).
    """
    m = np.arange(1, n + 1, dtype=float)
    return (2.0 * m - n - 1.0) / (2.0 * n)


def sc_tb_dispersion(k_2pia: np.ndarray, t: float = T) -> np.ndarray:
    """Simple-cubic tight-binding dispersion for a single s-orbital.

    Parameters
    ----------
    k_2pia : array of shape (..., 3)
        Crystal momentum in units of 2 pi / a.
    t : float
        Nearest-neighbour hopping magnitude.

    Returns
    -------
    E : array of shape k_2pia.shape[:-1]
        Band energy in units of t.

    Notes
    -----
    The dimensionless argument inside the cosines is
        k_i * a = (2 pi / a) * (k_2pia_i) * a = 2 pi * k_2pia_i.
    The 6 nearest-neighbour vectors are +/- a e_i, i = 1, 2, 3; summing
    exp(i k . delta) gives 2 [cos(k_x a) + cos(k_y a) + cos(k_z a)],
    and multiplying by the hopping -t gives the result.
    """
    kx = k_2pia[..., 0]
    ky = k_2pia[..., 1]
    kz = k_2pia[..., 2]
    return -2.0 * t * (
        np.cos(2.0 * np.pi * kx)
        + np.cos(2.0 * np.pi * ky)
        + np.cos(2.0 * np.pi * kz)
    )


def total_energy_per_cell(n: int, t: float = T) -> float:
    """Compute the MP-averaged total energy per unit cell for an n x n x n mesh.

    E_tot / N  =  (1 / n^3)  sum_k  E(k).
    """
    k_1d = mp_offsets_1d(n)
    kx, ky, kz = np.meshgrid(k_1d, k_1d, k_1d, indexing="ij")
    k_3d = np.stack([kx, ky, kz], axis=-1)
    E = sc_tb_dispersion(k_3d, t=t)
    return float(np.mean(E))


def main() -> None:
    # --- Compute E_tot/N for each n --------------------------------------
    energies = [total_energy_per_cell(n) for n in N_VALUES]
    E_ref = energies[-1]  # the n = 20 result, used as the "converged" reference
    errors = [abs(e - E_ref) for e in energies]

    # --- Print the table -------------------------------------------------
    print("Monkhorst-Pack convergence for SC tight-binding (t = 1):")
    print(f"  Analytic BZ integral of E(k) is 0  (sum of cosines on a period).")
    print()
    print(f"  {'n':>4s}  {'N_k = n^3':>10s}  {'E_tot / N':>16s}  "
          f"{'|error vs n=20|':>20s}")
    for n, E, err in zip(N_VALUES, energies, errors):
        print(f"  {n:>4d}  {n ** 3:>10d}  {E:>16.6e}  {err:>20.6e}")
    print()
    print(f"  Reference (n = 20):  E_tot / N = {E_ref:+.6e}")
    print(f"  All n values are even, so the centered MP mesh has perfect k -> -k")
    print(f"  symmetry, and the discrete sum is at machine precision.")
    print(f"  This is the classical 'trapezoidal rule on a periodic domain' result:")
    print(f"  for any finite Fourier series of the period the rule is *exact*.")

    # --- Plot -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.0, 6.0))

    n_arr = np.array(N_VALUES, dtype=float)
    err_arr = np.array(errors)

    # Floor the error at machine precision for the log scale (the actual
    # values are 0 to floating-point, and log(0) is -inf).
    plot_err = np.maximum(err_arr, 1.0e-16)

    # Actual |error| on the MP grid.
    ax.loglog(
        n_arr, plot_err,
        marker="o", color="#cc785c", linewidth=2.0, markersize=8.0,
        markerfacecolor="#cc785c", markeredgecolor="#3d3d3a",
        label=r"$|E_\mathrm{tot}/N(n) - E_\mathrm{tot}/N(20)|$",
    )

    # 1/n^2 reference line, scaled to pass through the (n=2) point.
    # For this particular integrand the actual error is at the machine
    # floor, but the textbook rate is 1/n^2 in 1-D (chapter 7.6.2).
    C = plot_err[0] * n_arr[0] ** 2
    ax.loglog(
        n_arr, C / n_arr ** 2,
        linestyle="--", color="#3d3d3a", linewidth=1.5,
        label=r"$\propto 1/n^{2}$ reference (1-D textbook rate)",
    )

    ax.set_xlabel(r"$n$  (mesh points per direction)")
    ax.set_ylabel(r"$|E_\mathrm{tot}/N(n) - E_\mathrm{tot}/N(20)|$")
    ax.set_title(
        "Monkhorst-Pack convergence — simple cubic tight-binding"
    )
    ax.legend(frameon=False, loc="upper right")
    ax.grid(True, which="both", alpha=0.25)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    # --- Save the plot ----------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "03-monkhorst-pack-convergence.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
