"""
02-finite-square-well.py
========================
Particle in a 1-D finite square well of width L = 2 a_0 and
depth V_0 = 10 E_h.

The potential is

    V(x) = -V_0   for  |x| < L/2,
    V(x) =  0     for  |x| > L/2.

Bound states have energies E in (-V_0, 0).  The transcendental
equations (matching the wavefunction and its derivative at the
walls) are, in atomic units (hbar = m = 1),

    z * tan(z)  =  sqrt(z_0^2 - z^2)    (even parity)
    -z * cot(z) =  sqrt(z_0^2 - z^2)    (odd parity)

with  z = k * L / 2,   k = sqrt(2 (E + V_0)),  and
z_0 = L * sqrt(V_0 / 2).  For (L, V_0) = (2, 10) the
dimensionless depth is z_0 = 2 sqrt(5) = 4.4721.  Bound
states exist for n = 1, 2, 3, ..., N where (N - 1/2) pi < z_0,
so this well supports 3 bound states: n = 1 (even, ground),
n = 2 (odd), n = 3 (even, highest).

The script:

  1. solves the two transcendental equations with
     `scipy.optimize.brentq`;
  2. converts back to energies E_n = 2 z_n^2 / L^2 - V_0;
  3. plots the three eigenfunctions on top of the potential,
     offset by their eigen-energies (the "ladder" plot).

Why this script lives in chapter 01's python_codes folder:

  - It is a direct numerical illustration of the matching
    procedure in section 1.3 -- the particle in a box is the
    infinite-V_0 limit of this problem.
  - The figure is the textbook "finite square well" picture
    that reappears in every quantum-mechanics course.

Dependencies: numpy, scipy (brentq), matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_01/02-finite-square-well.py

Writes its plot to:

    dft_notes/python_codes/chapter_01/plots/02-finite-square-well.png
"""

import os
import numpy as np
from scipy.optimize import brentq
import matplotlib

matplotlib.use("Agg")  # headless -- no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Transcendental equations
# ---------------------------------------------------------------------------
def f_even(z: float, z0: float) -> float:
    """Even-parity equation multiplied by cos(z) to remove the pole.

    Original equation: z * tan(z) = sqrt(z_0^2 - z^2)
    Stable form:        z * sin(z) - cos(z) * sqrt(z_0^2 - z^2) = 0

    The stable form is finite everywhere and changes sign at
    the (n - 1/2) * pi crossings.
    """
    if z >= z0:
        # RHS is imaginary past z_0; no bound state lives there.
        return 1.0
    return z * np.sin(z) - np.cos(z) * np.sqrt(z0**2 - z**2)


def f_odd(z: float, z0: float) -> float:
    """Odd-parity equation multiplied by sin(z) to remove the pole.

    Original equation: -z * cot(z) = sqrt(z_0^2 - z^2)
    Stable form:        -z * cos(z) - sin(z) * sqrt(z_0^2 - z^2) = 0
    """
    if z >= z0:
        return 1.0
    return -z * np.cos(z) - np.sin(z) * np.sqrt(z0**2 - z**2)


def solve_z(z0: float) -> list:
    """Return the dimensionless momenta z_n for all bound states.

    The roots alternate: (0, pi/2) is the first even, (pi/2, pi)
    is the first odd, (pi, 3pi/2) is the second even, and so on.
    The number of bound states is N = floor(2 z_0 / pi) + 1.
    """
    N = int(np.floor(2.0 * z0 / np.pi)) + 1
    roots = []
    for n in range(1, N + 1):
        if n % 2 == 1:
            # even state: bracket in ((n - 1) pi / 2,  n pi / 2)
            lo = (n - 1) * np.pi / 2.0 + 1.0e-6
            hi = n * np.pi / 2.0 - 1.0e-6
            f = f_even
            parity = "even"
        else:
            # odd state: bracket in ((n - 1) pi / 2,  n pi / 2)
            lo = (n - 1) * np.pi / 2.0 + 1.0e-6
            hi = n * np.pi / 2.0 - 1.0e-6
            f = f_odd
            parity = "odd"
        # Clip the upper bracket to z_0 -- beyond that the
        # bound-state solution does not exist.
        hi = min(hi, z0 - 1.0e-6)
        # Guard against the bracketing interval collapsing.
        if hi <= lo:
            break
        z_n = brentq(f, lo, hi, args=(z0,))
        roots.append((n, parity, z_n))
    return roots


# ---------------------------------------------------------------------------
# Wavefunctions
# ---------------------------------------------------------------------------
def wavefunction(n: int, parity: str, z_n: float, x: np.ndarray, L: float, V0: float):
    """Build the normalised n-th eigenfunction on the grid x.

    The matching conditions at |x| = L / 2 determine the
    relative amplitudes inside and outside the well.
    """
    half = L / 2.0
    E = 2.0 * z_n**2 / L**2 - V0  # negative (bound)
    k = np.sqrt(2.0 * (E + V0))  # inside,  oscillatory
    kap = np.sqrt(-2.0 * E)  # outside, exponential decay

    psi = np.zeros_like(x)

    if parity == "even":
        # psi = A * cos(kx)        for |x| < half
        # psi = B * exp(-kap |x|) for |x| > half
        A_inside = 1.0
        B_outside = A_inside * np.cos(k * half) / np.exp(-kap * half)
        inside = np.abs(x) < half
        outside = ~inside
        psi[inside] = A_inside * np.cos(k * x[inside])
        sign = np.where(x >= 0.0, 1.0, 1.0)  # even
        psi[outside] = B_outside * np.exp(-kap * np.abs(x[outside]))
    else:
        # odd: psi = A * sin(kx)                       for |x| < half
        #      psi = sign(x) * B * exp(-kap |x|)       for |x| > half
        A_inside = 1.0
        B_outside = A_inside * np.sin(k * half) / np.exp(-kap * half)
        inside = np.abs(x) < half
        outside = ~inside
        psi[inside] = A_inside * np.sin(k * x[inside])
        psi[outside] = (
            B_outside * np.sign(x[outside]) * np.exp(-kap * np.abs(x[outside]))
        )

    # Normalise: int_{-infty}^{infty} |psi|^2 dx = 1.
    norm = np.sqrt(np.trapz(psi**2, x))
    psi /= norm
    return psi, E


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # --- Parameters --------------------------------------------------
    L = 2.0  # well width, a_0
    V0 = 10.0  # well depth, E_h
    z0 = L * np.sqrt(V0 / 2.0)  # dimensionless depth

    # --- Predict the number of bound states --------------------------
    N_predicted = int(np.floor(2.0 * z0 / np.pi)) + 1
    print(
        f"Finite square well:  L = {L:.4f} a_0,  "
        f"V_0 = {V0:.4f} E_h,  z_0 = L * sqrt(V_0 / 2) = {z0:.6f}"
    )
    print(
        f"Predicted number of bound states:  N = floor(2 z_0 / pi) + 1 = {N_predicted}"
    )
    print()

    # --- Solve the transcendental equations -------------------------
    roots = solve_z(z0)
    print(f"  n   parity     z_n              E_n (E_h)         |psi(0)|^2 inside")
    print(f"  --  ---------- ----------------  ----------------  ----------------")
    for n, parity, z_n in roots:
        E = 2.0 * z_n**2 / L**2 - V0
        print(f"  {n}   {parity:10s} {z_n:14.6f}   {E:14.6f}   --")
    print(f"\n  *** {len(roots)} bound state(s) found ***")
    print(
        f"  *** ground-state energy  E_1 = {2.0 * roots[0][2] ** 2 / L**2 - V0:.6f} E_h ***"
    )

    # --- Build the figure: ladder plot ------------------------------
    # x grid wide enough to show the exponential tails.
    x = np.linspace(-3.0 * L / 2.0, 3.0 * L / 2.0, 1201)
    # Potential (a step from -V_0 to 0 at the walls).
    V = np.where(np.abs(x) < L / 2.0, -V0, 0.0)

    fig, ax = plt.subplots(figsize=(8, 5.5))

    # Brand palette.
    palette = ["#cc785c", "#e8a55a", "#5db8a6", "#a9583e"]

    # Plot the potential as a filled step, going from -V_0 up to
    # each E_n.  The convention is "potential at the bottom,
    # wavefunctions above the well floor".
    xstep = np.linspace(-3.0 * L / 2.0, 3.0 * L / 2.0, 2001)
    Vstep = np.where(np.abs(xstep) < L / 2.0, -V0, 0.0)
    ax.fill_between(xstep, Vstep, -V0 - 1.5, color="#e8e6e1", alpha=0.7, zorder=1)
    ax.plot(
        xstep, Vstep, color="#3d3d3a", linewidth=2.0, zorder=2, label=r"$V(x)$ (well)"
    )

    # Dotted eigen-energy levels.
    for n, parity, z_n in roots:
        E = 2.0 * z_n**2 / L**2 - V0
        ax.axhline(
            E, color="#a09d96", linewidth=0.8, linestyle=":", alpha=0.7, zorder=2
        )

    # Plot each wavefunction, offset to its own energy, with a
    # small vertical scale so they don't overlap.
    SCALE = 0.7
    for idx, (n, parity, z_n) in enumerate(roots):
        psi, E = wavefunction(n, parity, z_n, x, L, V0)
        label = (
            rf"$\psi_{{{n}}}^{{({parity[0]})}}$, "
            rf"$E_{{{n}}} = {E:+.3f}\,E_h$"
        )
        ax.plot(
            x,
            E + SCALE * psi,
            color=palette[idx % len(palette)],
            linewidth=2.0,
            label=label,
            zorder=3,
        )

    ax.axhline(0.0, color="#3d3d3a", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvline(-L / 2.0, color="#3d3d3a", linewidth=0.8, alpha=0.5)
    ax.axvline(+L / 2.0, color="#3d3d3a", linewidth=0.8, alpha=0.5)
    ax.set_xlabel(r"$x$  (atomic units, $a_0$)")
    ax.set_ylabel(r"$E$  (Hartree)")
    ax.set_title(
        rf"Finite square well:  $L = {L:.0f}\,a_0$,  $V_0 = {V0:.0f}\,E_h$,  "
        rf"{len(roots)} bound state(s)"
    )
    ax.set_xlim(-3.0 * L / 2.0, 3.0 * L / 2.0)
    ax.set_ylim(-V0 - 1.0, 0.6)
    ax.grid(True, alpha=0.2)
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.tight_layout()

    # --- Write the plot ---------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "02-finite-square-well.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
