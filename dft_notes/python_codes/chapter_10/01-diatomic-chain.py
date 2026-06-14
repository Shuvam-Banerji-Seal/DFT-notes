"""
01-diatomic-chain.py
====================

Phonon dispersion of a 1-D diatomic chain.

    M_1 = 12 amu,  M_2 = 16 amu,  K = 10 eV/Å^2,  a = 5 Å

The unit cell contains two atoms; the Brillouin zone is
[-π/a, +π/a] = [-0.628, +0.628] bohr^-1.  We sample 401 wave-
vectors uniformly in the irreducible BZ [0, π/a] and evaluate
the dispersion relation (chapter 10, eq. 10.62)

    ω_±^2(q) = K (1/M_1 + 1/M_2) ± K sqrt( (1/M_1 + 1/M_2)^2
                                        - 4 sin^2(q a / 2) / (M_1 M_2) )

The acoustic branch ω_-(q) starts at zero at q = 0 and rises
with the speed of sound v_s = (a/2) sqrt(K/μ) where
μ = M_1 M_2 / (M_1 + M_2) is the reduced mass.  The optical
branch ω_+(q) starts at sqrt(2K/μ) at q = 0.  At the BZ
boundary q = π/a the branches are ω_- = sqrt(2K/M_2) and
ω_+ = sqrt(2K/M_1), separated by a gap of

    Δ(ω^2) = 2K (1/M_1 - 1/M_2).

For the parameters above:

    v_s       ≈ 8.96 × 10^4 m/s
    ω_+(0)    ≈ 25.5 THz
    ω_-(π/a)  ≈ 24.7 THz
    ω_+(π/a)  ≈ 28.4 THz

The script:

  1.  Sets the physical parameters.
  2.  Converts the force constant K to SI units.
  3.  Builds a 401-point mesh in [0, π/a].
  4.  Evaluates the dispersion relation at every q.
  5.  Plots the two branches, with the BZ boundary marked.
  6.  Saves the plot to plots/01-diatomic-chain.png.

Why this script lives in the chapters python_codes folder:

  - Chapter 10 (Phonons & vibrations) inlines a copy of this
    script in Section 10.9 as the worked example.  The chapter
    is the readable narrative; the script is the source of
    truth.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_10/01-diatomic-chain.py

Writes its plot to:

    dft_notes/python_codes/chapter_10/plots/01-diatomic-chain.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
M1 = 12.0  # mass of atom 1, amu
M2 = 16.0  # mass of atom 2, amu
K = 10.0  # nearest-neighbour force constant, eV/Å^2
A = 5.0  # lattice constant, Å

# Unit conversions to SI.
eV_to_J = 1.602176634e-19  # 1 eV  in J
A_to_m = 1.0e-10  # 1 Å   in m
amu_to_kg = 1.66053906660e-27  # 1 amu in kg
THz_to_Hz = 1.0e12  # 1 THz in Hz

K_SI = K * eV_to_J / A_to_m**2  # 160.2 N/m = 160.2 kg/s^2
M1_SI = M1 * amu_to_kg  # 1.993e-26 kg
M2_SI = M2 * amu_to_kg  # 2.657e-26 kg


def dispersion(q_vals, K, M1, M2, A):
    """Evaluate the two branches of the diatomic-chain dispersion.

    Parameters
    ----------
    q_vals : np.ndarray
        Phonon wavevector in 1/m, shape (N,).
    K : float
        Force constant in kg/s^2 (i.e. N/m).
    M1, M2 : float
        Atomic masses in kg.
    A : float
        Lattice constant in m.

    Returns
    -------
    omega_minus, omega_plus : np.ndarray
        Acoustic and optical branches in rad/s, shape (N,).
    """
    sum_inv = 1.0 / M1 + 1.0 / M2
    diff_inv = 4.0 * np.sin(q_vals * A / 2.0) ** 2 / (M1 * M2)
    inside = sum_inv**2 - diff_inv
    # Guard against tiny negative round-off near q = 0
    inside = np.maximum(inside, 0.0)
    omega_sq_plus = K * (sum_inv + np.sqrt(inside))
    omega_sq_minus = K * (sum_inv - np.sqrt(inside))
    return np.sqrt(omega_sq_minus), np.sqrt(omega_sq_plus)


def main() -> None:
    # --- Wavevector mesh in the 1st BZ -----------------------------------
    N_Q = 401
    q_frac = np.linspace(0.0, 1.0, N_Q)
    q_vals = q_frac * np.pi / A  # m^-1

    # --- Dispersion ------------------------------------------------------
    omega_minus, omega_plus = dispersion(q_vals, K_SI, M1_SI, M2_SI, A)

    # Convert to THz for plotting: ν = ω / (2π) in Hz, then /1e12.
    nu_minus_THz = omega_minus / (2.0 * np.pi * THz_to_Hz)
    nu_plus_THz = omega_plus / (2.0 * np.pi * THz_to_Hz)

    # --- Sanity checks against analytical limits ------------------------
    mu = M1_SI * M2_SI / (M1_SI + M2_SI)  # reduced mass
    v_s = (A / 2.0) * np.sqrt(K_SI / mu)  # speed of sound
    nu_optical_at_0 = np.sqrt(2.0 * K_SI / mu) / (2.0 * np.pi * THz_to_Hz)
    nu_lower_at_bz = np.sqrt(2.0 * K_SI / M2_SI) / (2.0 * np.pi * THz_to_Hz)
    nu_upper_at_bz = np.sqrt(2.0 * K_SI / M1_SI) / (2.0 * np.pi * THz_to_Hz)

    print(
        f"Speed of sound     v_s       = {v_s:+.4e} m/s\n"
        f"Optical at q = 0   ν_+(0)    = {nu_optical_at_0:+.4f} THz\n"
        f"Acoustic at q = π/a ν_-(π/a) = {nu_lower_at_bz:+.4f} THz\n"
        f"Optical at q = π/a  ν_+(π/a) = {nu_upper_at_bz:+.4f} THz"
    )

    # --- Plot the two branches ------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    # Brand palette - same coral / teal as the rest of the site.
    ax.plot(
        q_frac,
        nu_minus_THz,
        color="#cc785c",
        linewidth=2.2,
        label=r"acoustic  $\omega_-(q)$",
    )
    ax.plot(
        q_frac,
        nu_plus_THz,
        color="#5db8a6",
        linewidth=2.2,
        label=r"optical   $\omega_+(q)$",
    )

    # Mark the BZ boundary and the zero of frequency.
    ax.axvline(1.0, color="#3d3d3a", linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axhline(0.0, color="#a09d96", linewidth=0.8, alpha=0.3)

    # Annotate the optical frequency at q = 0.
    ax.annotate(
        rf"$\omega_+(0) \approx {nu_optical_at_0:.1f}$ THz",
        xy=(0.05, nu_optical_at_0 - 1.0),
        color="#5db8a6",
        fontsize=10,
    )

    ax.set_xlabel(r"$q\, a\,/\,\pi$")
    ax.set_ylabel(r"$\nu$ (THz)")
    ax.set_title(
        r"1-D diatomic chain:  $M_1 = 12$ amu, $M_2 = 16$ amu, "
        r"$K = 10$ eV/Å$^2$, $a = 5$ Å"
    )
    ax.legend(frameon=False, loc="lower right")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(0.0, 1.0)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    # --- Save the plot --------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-diatomic-chain.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
