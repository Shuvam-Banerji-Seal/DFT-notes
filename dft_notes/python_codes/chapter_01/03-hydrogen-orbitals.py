"""
03-hydrogen-orbitals.py
=======================
Hydrogen radial wavefunctions R_{n,ell}(r) for Z = 1, a_0 = 1,
and the radial probability density

    P_{n,ell}(r)  =  r^2 * |R_{n,ell}(r)|^2

for the six lowest states  1s, 2s, 2p, 3s, 3p, 3d.  The plot
also marks the mean radius

    <r>_{n,ell}  =  a_0 * (3 n^2 - ell (ell + 1)) / 2

expected for each state, and prints a small table comparing the
position of the maximum of P to <r>.

The normalised radial eigenfunctions are (Z = 1, a_0 = 1)

    R_{10}(r) = 2 e^{-r}
    R_{20}(r) = (1/(2 sqrt(2))) (2 - r) e^{-r/2}
    R_{21}(r) = (1/(2 sqrt(6))) r e^{-r/2}
    R_{30}(r) = (2/(81 sqrt(3))) (27 - 18 r + 2 r^2) e^{-r/3}
    R_{31}(r) = (4/(81 sqrt(6))) (6 - r) r e^{-r/3}
    R_{32}(r) = (4/(81 sqrt(30))) r^2 e^{-r/3}

and are coded explicitly below (no scipy.special, to keep the
script fully self-contained and to make the recursion visible).

Why this script lives in chapter 01's python_codes folder:

  - Chapter 01, section 1.10 ("The hydrogen atom") derives these
    eigenfunctions via the radial equation and the u = r R
    substitution.  The script makes the algebra concrete: the
    Laguerre polynomial structure of the analytic solution is
    hidden inside a polynomial, but the output is the same.
  - The 1s peak at r = a_0 is the "book cover" picture of
    quantum mechanics; the script prints the numerical peak
    position for verification.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_01/03-hydrogen-orbitals.py

Writes its plot to:

    dft_notes/python_codes/chapter_01/plots/03-hydrogen-orbitals.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless -- no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Closed-form radial eigenfunctions
# ---------------------------------------------------------------------------
# We hard-code the six lowest (n, ell) pairs.  Each R_{n,ell} is
# normalised so that int_0^infty |R_{n,ell}|^2 r^2 dr = 1, i.e.
# R_{n,ell} * Y_l^m is normalised to unity in 3D.
_R_FUNCS = {
    (1, 0): lambda r: 2.0 * np.exp(-r),
    (2, 0): lambda r: (1.0 / (2.0 * np.sqrt(2.0))) * (2.0 - r) * np.exp(-r / 2.0),
    (2, 1): lambda r: (1.0 / (2.0 * np.sqrt(6.0))) * r * np.exp(-r / 2.0),
    (3, 0): lambda r: (
        2.0 / (81.0 * np.sqrt(3.0)) * (27.0 - 18.0 * r + 2.0 * r**2) * np.exp(-r / 3.0)
    ),
    (3, 1): lambda r: (4.0 / (81.0 * np.sqrt(6.0)) * (6.0 - r) * r * np.exp(-r / 3.0)),
    (3, 2): lambda r: (4.0 / (81.0 * np.sqrt(30.0)) * r**2 * np.exp(-r / 3.0)),
}

# Pretty-print labels.
_LABELS = {
    (1, 0): "1s",
    (2, 0): "2s",
    (2, 1): "2p",
    (3, 0): "3s",
    (3, 1): "3p",
    (3, 2): "3d",
}

# Colour per state (consistent ordering for the legend).
_COLOURS = {
    "1s": "#cc785c",  # coral
    "2s": "#e8a55a",  # amber
    "2p": "#d99664",  # peach
    "3s": "#5db8a6",  # teal
    "3p": "#7c9b9a",  # muted teal
    "3d": "#a9583e",  # coral, active
}


def R_nl(n: int, ell: int, r: np.ndarray) -> np.ndarray:
    """Normalised hydrogen radial eigenfunction R_{n,ell}(r)."""
    return _R_FUNCS[(n, ell)](r)


def mean_radius(n: int, ell: int) -> float:
    """<r>_{n,ell} = a_0 * (3 n^2 - ell (ell + 1)) / 2, with a_0 = 1."""
    return (3.0 * n * n - ell * (ell + 1.0)) / 2.0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    STATES = [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]

    # --- Radial grid -------------------------------------------------
    # Avoid r = 0 exactly because r^2 R^2 -> 0 there for ell = 0
    # but the figure is more readable if we sample on a dense
    # grid.  30 a_0 is well past the last node of the 3d
    # eigenfunction (which is the slowest to decay).
    r = np.linspace(0.0, 30.0, 1201)

    # --- Print a small table -----------------------------------------
    print("Hydrogen radial eigenfunctions,  Z = 1,  a_0 = 1")
    print("=" * 64)
    print(f"  state   n   ell   E_n (E_h)       <r>  =  a_0 * (3n^2 - l(l+1)) / 2")
    for n, ell in STATES:
        E = -1.0 / (2.0 * n * n)
        mean_r = mean_radius(n, ell)
        print(
            f"  {(_LABELS[(n, ell)]):>3s}    {n}    {ell}    "
            f"{E:+.6f}      {mean_r:6.3f} a_0"
        )

    # --- Verify the 1s peak position ---------------------------------
    # R_{10} = 2 e^{-r}, so P_{10}(r) = r^2 * 4 e^{-2r}.
    # dP/dr = 8r e^{-2r} (1 - r)  =>  peak at r = a_0 = 1.
    r_peak_1s_analytic = 1.0
    r_dense = np.linspace(0.0, 5.0, 5001)
    P_1s_dense = r_dense**2 * R_nl(1, 0, r_dense) ** 2
    r_peak_1s_numeric = float(r_dense[np.argmax(P_1s_dense)])
    print(
        f"\n  1s peak:  analytic = {r_peak_1s_analytic:.6f} a_0,  "
        f"numeric = {r_peak_1s_numeric:.6f} a_0,  "
        f"|delta| = {abs(r_peak_1s_numeric - r_peak_1s_analytic):.2e} a_0"
    )

    # --- Plot the radial probability densities -----------------------
    fig, ax = plt.subplots(figsize=(8, 5.5))

    for n, ell in STATES:
        R = R_nl(n, ell, r)
        P = r**2 * R**2
        label = _LABELS[(n, ell)]
        ax.plot(
            r,
            P,
            color=_COLOURS[label],
            linewidth=2.0,
            label=rf"$P_{{{label}}}(r) = r^2 |R_{{{label}}}(r)|^2$",
        )
        # Mark the analytic mean radius.
        mean_r = mean_radius(n, ell)
        ax.axvline(
            mean_r,
            color=_COLOURS[label],
            linewidth=0.8,
            linestyle=":",
            alpha=0.7,
        )

    # Annotate the 1s peak explicitly, since it is the
    # "textbook" check.
    ax.annotate(
        rf"$r = a_0$ (1s peak)",
        xy=(1.0, 1.0 * (2.0 * np.exp(-1.0)) ** 2),
        xytext=(2.0, 0.55),
        arrowprops={"arrowstyle": "->", "color": "#3d3d3a", "lw": 0.8},
        fontsize=9,
        color="#3d3d3a",
    )

    ax.set_xlabel(r"$r$  (atomic units, $a_0$)")
    ax.set_ylabel(r"$P_{n\ell}(r) = r^2 |R_{n\ell}(r)|^2$")
    ax.set_title(
        "Hydrogen radial probability densities, "
        r"$Z = 1$, $a_0 = 1$  --  dotted: $\langle r \rangle_{n\ell}$"
    )
    ax.set_xlim(0.0, 25.0)
    ax.set_ylim(0.0, 0.6)
    ax.grid(True, alpha=0.2)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.tight_layout()

    # --- Write the plot ---------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "03-hydrogen-orbitals.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
