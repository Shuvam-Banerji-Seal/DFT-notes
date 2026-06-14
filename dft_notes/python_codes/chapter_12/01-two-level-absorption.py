"""
01-two-level-absorption.py
==========================

Absorption spectrum of a two-level system by two equivalent
routes:

    (A) the Casida eigenvalue problem (linear-response TD-DFT,
        section 12.7 of chapter 12) and

    (B) real-time propagation of the time-dependent
        Schroedinger equation with a delta-kick perturbation
        (section 12.8 of chapter 12) followed by a
        Fourier transform of the time-dependent dipole
        moment.

The two routes must agree on the position and width of the
absorption peak (a finite-width peak is produced by the
Fourier uncertainty principle, with a damping constant eta
that controls the linewidth).

Model Hamiltonian (atomic units):

    H_0 = diag(0, omega_12)        ground state |1>, excited |2>
    d   = d_12 * sigma_x           dipole operator

A "delta-kick" of strength k rotates the ground state into a
coherent superposition |1> + i*k*d_12 |2> at t=0+; the dipole
moment then oscillates at the *dressed* excitation frequency
omega_exc = sqrt(omega_12 * (omega_12 + 2 K)) where K is the
single Casida coupling-matrix element.  We expose the effect
of the kernel by running the script for K = 0 (bare KS) and
for a representative K = +0.2 E_h.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_12/01-two-level-absorption.py

Writes its plot to:

    dft_notes/python_codes/chapter_12/plots/01-two-level-absorption.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
OMEGA_12 = 1.0  # KS excitation energy of the bare 2-level system (E_h)
D12 = 1.0  # dipole matrix element <2|d|1>  (e a_0)
KICK = 0.01  # strength of the delta-kick perturbation
ETA = 0.05  # exponential damping of the time signal (E_h)
T_MAX = 200.0  # total propagation time (E_h^-1)
N_STEPS = 16384  # number of time steps; dt = T_MAX / N_STEPS

# Casida coupling matrix element K (one number for the 1x1 system).
# K = 0 reproduces the bare KS result; K = +0.2 E_h gives a
# representative "with kernel" dressed excitation.
K_CASIDA = 0.2  # E_h

# Brand palette - same coral / amber / teal as the rest of the site.
PALETTE_RT = "#cc785c"
PALETTE_LORENTZ = "#3d3d3a"
PALETTE_CASIDA = "#5db8a6"


# ---------------------------------------------------------------------------
# Casida linear-response calculation
# ---------------------------------------------------------------------------
def casida_2level(omega_12: float, K: float, d12: float) -> tuple:
    """Return (omega_exc, f_osc) for a 2-level system.

    The Casida matrix in the 1-transition space is 2x2:

        M = ((A, B), (B, A)),   with A = omega_12 + K, B = K.

    The positive eigenvalue is sqrt(A^2 - B^2) = sqrt(omega_12 *
    (omega_12 + 2 K)).  The eigenvectors (X, Y) satisfy
    (X + Y) / (X - Y) = sqrt((omega_12 + K - omega_exc) /
                              (omega_12 + K + omega_exc));
    we use them to compute the dipole-oscillator strength in
    the length gauge,

        f_osc = (2/3) omega_exc d12^2 (X + Y)^2 .
    """
    A = omega_12 + K
    B = K
    omega_exc = float(np.sqrt(A * A - B * B))

    # Eigenvector of M (positive eigenvalue omega_exc).
    #   M (X, Y)^T = omega_exc (X, -Y)^T
    #   => (A - omega_exc) X + B Y = 0  =>  Y/X = -(A - omega_exc)/B
    # Normalise so that X^2 - Y^2 = 1.
    if abs(B) < 1e-14:
        X = 1.0
        Y = 0.0
    else:
        Y_over_X = -(A - omega_exc) / B
        X = 1.0 / np.sqrt(1.0 - Y_over_X**2)
        Y = Y_over_X * X
    f_osc = (2.0 / 3.0) * omega_exc * d12**2 * (X + Y) ** 2
    return omega_exc, float(f_osc)


# ---------------------------------------------------------------------------
# Real-time propagation
# ---------------------------------------------------------------------------
def propagate_2level(
    omega_12: float,
    d12: float,
    kick: float,
    t_max: float,
    n_steps: int,
    eta: float,
) -> tuple:
    """Time-propagate the 2-level density matrix after a delta-kick.

    Returns
    -------
    t : (n_steps+1,) ndarray   time grid, E_h^-1
    mu : (n_steps+1,) ndarray   dipole moment <Psi(t)|d|Psi(t)>, real
    """
    t = np.linspace(0.0, t_max, n_steps + 1)
    # Initial state: ground state |1>.
    c1 = 1.0 + 0.0j
    c2 = 0.0 + 0.0j
    # Apply the delta-kick:  c -> exp(-i k d) c  with
    # d = d_12 (|1><2| + |2><1|).  This rotates |1> into
    # |1> - i k d_12 |2> + O(k^2).
    c1 = np.cos(kick * d12) * c1 - 1j * np.sin(kick * d12) * 0.0
    c2 = np.cos(kick * d12) * c2 - 1j * np.sin(kick * d12) * 1.0
    # Time evolution at time t>0 with energy splitting omega_12:
    #   c1(t) = c1(0+)
    #   c2(t) = c2(0+) exp(-i omega_12 t) exp(-eta t)
    phase = np.exp(-1j * omega_12 * t) * np.exp(-eta * t)
    c2_t = c2 * phase
    # Dipole moment  mu(t) = <Psi|hat d|Psi> = 2 d_12 Re(c1* c2)
    # (the factor 2 is the closed-shell Kramers-paired factor).
    mu = 2.0 * d12 * np.real(np.conj(c1) * c2_t)
    return t, mu


def fourier_absorbtion(t: np.ndarray, mu: np.ndarray, n_freq: int = 4096) -> tuple:
    """Fourier transform of mu(t) for the absorption spectrum.

    Returns (omega, |mu(omega)|**2) on a positive-frequency grid.
    """
    dt = t[1] - t[0]
    # Pad to the next power of two to make the FFT efficient
    # and to get a fine frequency grid.
    n_fft = int(2 ** np.ceil(np.log2(max(len(t), n_freq))))
    freqs_full = 2.0 * np.pi * np.fft.fftfreq(n_fft, d=dt)
    # Window to suppress the Gibbs phenomenon from the abrupt
    # end of the time signal.  An exponential damping
    # exp(-eta t) is already in mu(t), so we use a flat-top
    # window here to avoid double-damping.
    window = np.ones_like(mu)
    mu_windowed = mu * window
    mu_padded = np.zeros(n_fft)
    mu_padded[: len(mu)] = mu_windowed
    mu_omega = np.fft.fft(mu_padded)
    # Return only the positive frequencies.
    mask = freqs_full >= 0
    return freqs_full[mask], np.abs(mu_omega[mask]) ** 2


# ---------------------------------------------------------------------------
# Sanity-check: analytic Lorentzian
# ---------------------------------------------------------------------------
def lorentzian(omega: np.ndarray, omega_0: float, gamma: float) -> np.ndarray:
    """A normalised Lorentzian L(omega) = (1/pi) gamma / ((omega-omega_0)^2 + gamma^2)."""
    return (1.0 / np.pi) * gamma / ((omega - omega_0) ** 2 + gamma**2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # ---- (A) Casida ------------------------------------------------------
    omega_exc_bare, f_bare = casida_2level(OMEGA_12, 0.0, D12)
    omega_exc_dressed, f_dressed = casida_2level(OMEGA_12, K_CASIDA, D12)

    print("--- Casida (linear-response) calculation ---")
    print(f"  Bare KS excitation energy (K=0):   omega_exc = {omega_exc_bare:.4f} E_h")
    print(
        f"  K = {K_CASIDA:+.3f} E_h  ->  omega_exc = "
        f"{omega_exc_dressed:.4f} E_h"
        f"   ( = sqrt({OMEGA_12:.2f} * ({OMEGA_12:.2f} + 2*{K_CASIDA:.2f}))"
        f"  = {np.sqrt(OMEGA_12 * (OMEGA_12 + 2 * K_CASIDA)):.4f} )"
    )
    print(f"  Oscillator strength (K=0):   f_osc = {f_bare:.4f}")
    print(f"  Oscillator strength (K={K_CASIDA:+.2f}): f_osc = {f_dressed:.4f}")

    # ---- (B) Real-time propagation ---------------------------------------
    t, mu = propagate_2level(OMEGA_12, D12, KICK, T_MAX, N_STEPS, ETA)
    omega_grid, spec = fourier_absorbtion(t, mu, n_freq=8192)

    # Find the peak of the spectrum in a window around omega_exc.
    window_lo = 0.5 * OMEGA_12
    window_hi = 1.5 * OMEGA_12
    mask = (omega_grid > window_lo) & (omega_grid < window_hi)
    peak_idx = np.argmax(spec[mask])
    omega_peak = float(omega_grid[mask][peak_idx])

    # Half-width at half-maximum: find the two points where the
    # spectrum is half of its peak value.
    peak_value = spec[mask][peak_idx]
    half = 0.5 * peak_value
    above = spec[mask] >= half
    edges = np.where(np.diff(above.astype(int)) != 0)[0]
    if edges.size >= 2:
        i_lo = edges[0]
        i_hi = edges[-1]
        omega_lo = omega_grid[mask][i_lo]
        omega_hi = omega_grid[mask][i_hi]
        fwhm = float(omega_hi - omega_lo)
    else:
        fwhm = float("nan")

    print("--- Real-time propagation ---")
    print(f"  Kick strength k = {KICK}")
    print(f"  Damping eta = {ETA} E_h")
    print(
        f"  Propagation T = {T_MAX} E_h^-1,  "
        f"n_steps = {N_STEPS},  dt = {T_MAX / N_STEPS:.4e} E_h^-1"
    )
    print(
        f"  Peak of |mu(omega)|^2 at omega = {omega_peak:.4f} E_h"
        f"   (Casida prediction: {omega_exc_dressed:.4f} E_h)"
    )
    print(
        f"  Width (FWHM) = {fwhm:.4f} E_h   (Fourier limit 2*eta = {2.0 * ETA:.4f} E_h)"
    )

    # ---- (C) Plot --------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))

    # Real-time spectrum (smoothed slightly by the FWHM of the peak).
    ax.plot(
        omega_grid[mask],
        spec[mask],
        color=PALETTE_RT,
        linewidth=1.6,
        label=r"real-time TD-DFT,"
        r"  $|\tilde\mu(\omega)|^2$",
    )

    # Reference Lorentzian centred on the Casida peak with FWHM 2*eta.
    omega_fine = np.linspace(window_lo, window_hi, 600)
    L_peak = lorentzian(omega_peak, omega_peak, ETA)
    L_norm = spec[mask][peak_idx] / L_peak * lorentzian(omega_fine, omega_peak, ETA)
    ax.plot(
        omega_fine,
        L_norm,
        color=PALETTE_LORENTZ,
        linewidth=1.4,
        linestyle="--",
        alpha=0.7,
        label=(r"Lorentzian,  $\omega_0 = $ Casida,  $\gamma = \eta$"),
    )

    # Vertical line at the Casida prediction.
    ax.axvline(
        omega_exc_dressed,
        color=PALETTE_CASIDA,
        linewidth=1.5,
        linestyle="-",
        alpha=0.85,
        label=rf"Casida $\omega_{{\rm exc}} = {omega_exc_dressed:.3f}\,E_h$",
    )

    # Vertical line at the bare-KS prediction.
    ax.axvline(
        omega_exc_bare,
        color="#a09d96",
        linewidth=1.0,
        linestyle=":",
        alpha=0.6,
        label=rf"bare KS, $\omega_{{12}} = {omega_exc_bare:.3f}\,E_h$",
    )

    ax.set_xlabel(r"$\omega \ \ (E_h)$")
    ax.set_ylabel(r"$|\tilde\mu(\omega)|^2$   (arbitrary units)")
    ax.set_title(
        r"Two-level absorption:  real-time vs. Casida  "
        rf"($k={KICK}$, $\eta={ETA}\,E_h$, $T={T_MAX:.0f}\,E_h^{{-1}}$)"
    )
    ax.legend(frameon=False, loc="upper right")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(window_lo, window_hi)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-two-level-absorption.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
