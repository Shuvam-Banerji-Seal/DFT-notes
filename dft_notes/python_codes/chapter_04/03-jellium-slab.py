"""
03-jellium-slab.py
==================

1-D jellium slab: a slab of constant positive background charge
(the "jellium") inside a 1-D box, with N = 10 electrons that
form a 1-D uniform-density slab of width L and density
n = N / L = 1 a_0^{-1} (i.e. r_s = 1 a_0).

Setup
-----
* Box length    L_box = 20 a_0
* Jellium slab  [x_c - L/2, x_c + L/2] = [5, 15] a_0
* Slab width    L = 10 a_0
* Electron count N = 10
* Background density n_+ = N / L = 1 a_0^{-1}
* Real-space grid: 200 points uniformly spaced, h = 20/199 ~ 0.10 a_0
* Dirichlet boundary conditions: psi(0) = psi(L_box) = 0

1-D Poisson equation
--------------------
The "1-D Coulomb" interaction that gives a finite, well-behaved
kernel is the Green's function of the 1-D Poisson equation

    d^2 V / dx^2 = -rho(x)   with   V(0) = V(L_box) = 0 ,

namely  G(x, x') = -|x - x'| / 2.  The corresponding potential
is

    V(x) = - integral |x - x'| / 2 * source(x') dx' .

For a positive source this is *negative* (attractive for an
electron) and *finite* (no 1/|x-x'| divergence at the source
point).  We adopt this convention here, which is the one used
in most pedagogical 1-D DFT codes (e.g. the well-known jellium
slab exercise of various computational-physics textbooks).

KS equations on a real-space grid
---------------------------------
The KS equation is solved on the grid with the finite-difference
Laplacian (3-point stencil):

    -(1/2) (psi_{i+1} - 2 psi_i + psi_{i-1}) / h^2 + V_KS(x_i) psi_i
        = epsilon psi_i .

We build the (NGRID-2) x (NGRID-2) matrix (interior points only,
the boundary values are fixed to zero) and diagonalise.

The density is built from the lowest N/2 = 5 spatial orbitals
with the standard spin factor 2:

    rho(x) = 2 sum_{n=1}^{N/2} |psi_n(x)|^2 .

XC functional (1-D analogues of the 3-D Dirac + Wigner pair)
------------------------------------------------------------
We use the same *formulas* as in 01-h2-lda-scf.py, but with a
1-D exchange coefficient of 1/3 (the simplest 1-D local-exchange
convention; the 3-D Dirac form has v_x = (4/3) eps_x, the 1-D
analogue has v_x = (1/3) eps_x):

    eps_x(rho) = -Cx (3 rho / pi)^{1/3} ,    v_x(rho) = (1/3) eps_x
    eps_c(r_s) = -0.044 / (r_s + 5.1) ,
    v_c(rho)   = eps_c(r_s) - (r_s / 3) d eps_c / d r_s ,
    r_s        = (3 / (4 pi rho))^{1/3} .

The 1-D / 3-D factor of 1/4 between the v_x coefficients is the
standard result of reducing the exchange hole to one dimension;
see e.g. Helbig et al., "Density-functional theory for the
non-interacting electron gas in 1, 2, and 3 dimensions" (2011)
for a careful discussion.

External potential: jellium background
--------------------------------------
V_jellium(x) is computed by solving the 1-D Poisson equation
for the source n_+(x) = n_0 for x in [5, 15] and 0 elsewhere,
with the same Dirichlet boundary conditions as the Hartree
potential.  The Hartree potential is computed in the same way
from rho(x).

In the converged self-consistent solution rho(x) -> n_+(x) in
the slab, so the total classical potential V_H + V_jellium
tends to zero there (perfect neutralisation); outside the
slab the residual V_H - V_jellium falls off linearly with
distance.

Plots
-----
A 2 x 2 subplot grid:

    (a) the self-consistent density rho(x)               (should be
        ~ uniform = 1 a.u.^-1 in [5, 15] and ~ 0 outside)
    (b) the Hartree potential V_H(x)                      (positive,
        parabolic in the slab, falling off linearly outside)
    (c) the total KS potential V_KS(x) = V_H + V_xc + V_jel
    (d) the first 4 KS eigenvalues as horizontal lines, with
        |psi_1|^2 overlaid to show the lowest orbital localised
        in the slab

Run from the repo root:

    python dft_notes/python_codes/chapter_04/03-jellium-slab.py

Writes its plot to:

    dft_notes/python_codes/chapter_04/plots/03-jellium-slab.png

Dependencies: numpy, scipy (eigh), matplotlib (headless).
"""

import os
import numpy as np
from scipy.linalg import eigh
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# Physical / numerical parameters
# ----------------------------------------------------------------------
L_BOX = 20.0  # box length, bohr
L = 10.0  # jellium-slab width, bohr
N_ELEC = 10  # total number of electrons
N_OCC = N_ELEC // 2  # doubly-occupied spatial orbitals
X_C = L_BOX / 2.0  # centre of the slab
A_LEFT = X_C - L / 2.0  # 5.0
A_RIGHT = X_C + L / 2.0  # 15.0
N_PLUS = N_ELEC / L  # background density inside the slab
NGRID = 200
HGRID = L_BOX / (NGRID - 1)  # grid spacing
MAX_ITER = 200
MIX_ALPHA = 0.2
TOL = 1.0e-8

# Dirac exchange coefficient (3-D, but reused as the prefactor in the
# 1-D formula; the conversion factor lives in v_x below).
CX = (3.0 / 4.0) * (3.0 / np.pi) ** (1.0 / 3.0)

# Wigner correlation
WIGNER_A_C = 0.044
WIGNER_R_0 = 5.1


# ----------------------------------------------------------------------
# Real-space grid helpers
# ----------------------------------------------------------------------
def v_xc_1d(rho):
    """1-D LDA exchange-correlation potential v_xc(rho).

    Same *structure* as the 3-D Dirac + Wigner form in
    01-h2-lda-scf.py, but with the 1-D exchange coefficient
    (1/3) eps_x in place of the 3-D one (4/3) eps_x.
    """
    rho = np.asarray(rho, dtype=float)
    rho_floor = np.maximum(rho, 1.0e-12)
    rs = (3.0 / (4.0 * np.pi * rho_floor)) ** (1.0 / 3.0)

    # Exchange
    eps_x = -CX * (3.0 * rho_floor / np.pi) ** (1.0 / 3.0)
    v_x = (1.0 / 3.0) * eps_x  # 1-D coefficient

    # Correlation (Wigner), exact r_s derivative
    eps_c = -WIGNER_A_C / (rs + WIGNER_R_0)
    deps_c_drs = WIGNER_A_C / (rs + WIGNER_R_0) ** 2
    v_c = eps_c - (rs / 3.0) * deps_c_drs

    return v_x + v_c


def poisson_1d_solve(rho: np.ndarray) -> np.ndarray:
    """Solve the 1-D Poisson equation

        d^2 V / dx^2 = -rho(x)  ,  V(0) = V(L_box) = 0

    on the uniform grid by direct inversion of the tridiagonal
    finite-difference Laplacian (NGRID-2 interior points, Dirichlet
    BCs on the boundary).  This is the discretised Green's function
    -|x - x'|/2 with the sign convention V_H > 0 for positive source.

    Returns V(x) on the full NGRID grid (boundary points are zero).
    """
    # 3-point finite-difference Laplacian:  V_{i+1} - 2 V_i + V_{i-1} = -h^2 rho_i
    # Tridiagonal matrix on the (NGRID - 2) interior points.
    N_int = NGRID - 2
    diag = -2.0 * np.ones(N_int)
    off = np.ones(N_int - 1)
    A = np.diag(diag) + np.diag(off, k=1) + np.diag(off, k=-1)
    # Right-hand side: -h^2 * rho at interior points.
    b = -(HGRID**2) * rho[1:-1]
    V_int = np.linalg.solve(A, b)
    V = np.zeros(NGRID)
    V[1:-1] = V_int
    return V


def coulomb_1d_potential(rho: np.ndarray) -> np.ndarray:
    """1-D Hartree potential V_H(x) felt by an electron.

    Sign convention: V_H > 0 for positive rho (repulsive between
    like charges -- the test electron is repelled by the other
    electrons).  The 1-D Poisson equation

        d^2 phi / dx^2 = -rho,  phi(0) = phi(L_box) = 0

    has the unique solution phi > 0 in the interior for rho > 0;
    this is the "positive-test-charge" potential.  For a *test
    electron* interacting with a *positive* source (the other
    electrons), the energy in v_eff is +phi, so we set V_H = phi
    directly.  (Equivalently: the "source" and the "test charge"
    are both negative, so the interaction is repulsive.)
    """
    return poisson_1d_solve(rho)


def jellium_potential() -> np.ndarray:
    """External potential of the positive jellium background,
    as *felt by an electron*.

    Sign convention: V_jel < 0 for positive n_+ (the jellium
    attracts the test electron).  The 1-D Poisson equation with
    source n_+ > 0 has phi > 0 in the interior; for a *test
    electron* interacting with a *positive* source, the energy
    in v_eff is -phi.  (The "source" and the "test charge" have
    opposite signs, so the interaction is attractive.)
    """
    x = np.linspace(0.0, L_BOX, NGRID)
    n_plus = np.where((x >= A_LEFT) & (x <= A_RIGHT), N_PLUS, 0.0)
    return -poisson_1d_solve(n_plus)


def build_ks_hamiltonian(V_KS: np.ndarray) -> np.ndarray:
    """Build the (NGRID - 2) x (NGRID - 2) finite-difference KS matrix
    with Dirichlet boundary conditions at x = 0 and x = L_box.
    """
    N_int = NGRID - 2  # interior grid points
    diag_kin = np.ones(N_int) * (1.0 / HGRID**2)  # -1/2 * (-2) / h^2
    off_kin = np.ones(N_int - 1) * (-0.5 / HGRID**2)
    H = np.diag(diag_kin + V_KS[1:-1]) + np.diag(off_kin, k=1) + np.diag(off_kin, k=-1)
    return H


def solve_ks(V_KS: np.ndarray) -> tuple:
    """Diagonalise the KS Hamiltonian, return (eps_all, psi) where
    psi is a (NGRID, N_OCC) array with the interior values of the
    lowest N_OCC eigenvectors (boundary points set to 0).
    """
    H = build_ks_hamiltonian(V_KS)
    # We need at least N_OCC eigenvalues; ask for the NGRID//2 lowest
    # for safety (a (NGRID-2) matrix has only NGRID-2 eigenvalues,
    # and we want the lowest N_OCC of them).
    n_eig = min(N_OCC, H.shape[0])
    eps, vecs = eigh(H, subset_by_index=(0, n_eig - 1))
    psi = np.zeros((NGRID, n_eig))
    psi[1:-1, :] = vecs
    # Normalise each orbital on the grid (trapezoidal)
    for k in range(n_eig):
        norm2 = np.sum(psi[:, k] ** 2) * HGRID
        psi[:, k] /= np.sqrt(norm2)
    return eps[:n_eig], psi


def density_from_orbitals(psi: np.ndarray) -> np.ndarray:
    """rho(x) = 2 sum_{n=1}^{N_OCC} |psi_n(x)|^2 .

    psi is (NGRID, N_OCC); returns a (NGRID,) array.
    """
    return 2.0 * np.sum(psi**2, axis=1)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main() -> None:
    x = np.linspace(0.0, L_BOX, NGRID)

    # Pre-compute the jellium potential (does not change during SCF).
    V_jel = jellium_potential()

    # Initial guess for the density: uniform in the slab, zero outside.
    rho = np.where((x >= A_LEFT) & (x <= A_RIGHT), N_PLUS, 0.0)

    print("1-D jellium slab, real-space KS-DFT")
    print("=" * 60)
    print(
        f"  L_box = {L_BOX} a_0,  L = {L} a_0,"
        f"  N = {N_ELEC} electrons,  n_+ = {N_PLUS:.4f} a_0^-1"
    )
    print(f"  NGRID = {NGRID}, h = {HGRID:.4f} a_0,  N_OCC = {N_OCC}")
    print(f"  r_s = (1 / n_+) = {1.0 / N_PLUS:.4f} a_0")
    print(f"  XC: 1-D Dirac + Wigner,  mixing alpha = {MIX_ALPHA},  tol = {TOL:.1e}")

    # SCF loop
    E_prev = 0.0
    energies = []
    eps = np.array([])
    psi = np.zeros((NGRID, N_OCC))
    E_total = 0.0
    it = 0

    for it in range(MAX_ITER):
        V_H = coulomb_1d_potential(rho)
        V_xc = v_xc_1d(rho)
        # V_jel is the potential felt by the electron -- negative
        # (attractive) for the positive jellium.  It enters V_KS
        # directly, with a PLUS sign (it is part of v_eff).
        V_KS = V_H + V_xc + V_jel

        eps, psi = solve_ks(V_KS)
        rho_new = density_from_orbitals(psi)

        # Total KS-DFT energy:
        #     E_DFT = T + V_ext + V_H + E_xc + V_jel_jel
        # with
        #     T          = 2 sum_n <psi_n|T|psi_n>
        #                 = sum_n integral |d psi_n/dx|^2 dx     (parts)
        #     V_ext      = integral rho(x) V_jel(x) dx          (negative;
        #                 the electron-jellium interaction is attractive)
        #     V_H        = 0.5 integral rho(x) V_H(x) dx        (Hartree
        #                 double-counted)
        #     E_xc       = integral rho(x) eps_xc(rho) dx
        #     V_jel_jel  = 0.5 integral n_+(x) V_jel(x) dx       (jellium
        #                 self-energy; negative for the attractive
        #                 jellium-jellium interaction in this convention)
        # We compute T by integration by parts on the 1-D Laplacian,
        # evaluated as a trapezoidal sum of |d psi / dx|^2 with the
        # 3-point finite-difference derivative.
        T = 0.0
        for n in range(psi.shape[1]):
            dpsi = (psi[1:, n] - psi[:-1, n]) / HGRID
            T += float(np.sum(dpsi**2)) * HGRID
        T *= 0.5  # the kinetic operator is -1/2 d^2/dx^2

        V_ext = float(np.sum(rho * V_jel) * HGRID)
        V_H_e = 0.5 * float(np.sum(rho * V_H) * HGRID)
        rho_floor = np.maximum(rho, 1.0e-12)
        rs = (3.0 / (4.0 * np.pi * rho_floor)) ** (1.0 / 3.0)
        eps_x = -CX * (3.0 * rho_floor / np.pi) ** (1.0 / 3.0)
        eps_c = -WIGNER_A_C / (rs + WIGNER_R_0)
        E_xc = float(np.sum(rho * (eps_x + eps_c)) * HGRID)
        n_plus = np.where((x >= A_LEFT) & (x <= A_RIGHT), N_PLUS, 0.0)
        V_jel_jel = 0.5 * float(np.sum(n_plus * V_jel) * HGRID)

        E_total = T + V_ext + V_H_e + E_xc + V_jel_jel

        dE = abs(E_total - E_prev)
        dR = float(np.linalg.norm(rho_new - rho))
        energies.append(E_total)

        if it < 5 or (it + 1) % 10 == 0 or dR < TOL:
            print(
                f"  iter {it + 1:3d}  E_tot = {E_total:+.6f}  "
                f"T = {T:+.6f}  dE = {dE:.2e}  dR = {dR:.2e}"
            )

        # Linear mixing
        rho = (1.0 - MIX_ALPHA) * rho + MIX_ALPHA * rho_new
        E_prev = E_total

        if dE < TOL and dR < TOL:
            print(
                f"\n  SCF converged in {it + 1} iterations"
                f" (dE = {dE:.2e}, dR = {dR:.2e})"
            )
            break
    else:
        print("\n  WARNING: KS-SCF did not converge in MAX_ITER iterations")

    # Verify the density integrates to N_ELEC.
    n_electrons = float(np.sum(rho) * HGRID)
    print("\n" + "=" * 60)
    print("Converged 1-D jellium slab results")
    print("=" * 60)
    print(f"  Converged E_total        = {E_total:+.6f} E_h")
    print(f"  Lowest 4 KS eigenvalues  = {eps[:4]}")
    print(f"  integral rho(x) dx       = {n_electrons:.4f}  (should be {N_ELEC})")
    print(
        f"  max(rho) in slab         = {rho[(x >= A_LEFT) & (x <= A_RIGHT)].max():.4f}"
    )
    print(
        f"  min(rho) in slab         = {rho[(x >= A_LEFT) & (x <= A_RIGHT)].min():.4f}"
    )

    # ----------------------------------------------------------------
    # Plot 2 x 2 grid
    # ----------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5))

    palette = ["#cc785c", "#5db8a6", "#e8a55a", "#a9583e"]
    slab_color = "#a09d96"

    # (a) Self-consistent density
    ax = axes[0, 0]
    ax.fill_between(x, rho, color=palette[0], alpha=0.35)
    ax.plot(x, rho, color=palette[0], linewidth=2.0, label=r"$\rho_{\rm SCF}(x)$")
    ax.axvspan(
        A_LEFT,
        A_RIGHT,
        color=slab_color,
        alpha=0.12,
        label=f"jellium  $n_+ = {N_PLUS:.2f}\\,a_0^{{-1}}$",
    )
    ax.axhline(N_PLUS, color=palette[0], linestyle=":", linewidth=1.0, alpha=0.7)
    ax.set_xlabel(r"$x$  (a$_0$)")
    ax.set_ylabel(r"$\rho(x)$  (a$_0^{-1}$)")
    ax.set_title(
        f"(a) Self-consistent density   "
        rf"$\int \rho\,dx = {n_electrons:.3f}$"
    )
    ax.set_xlim(0, L_BOX)
    ax.set_ylim(0, max(1.4, rho.max() * 1.1))
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    # (b) Hartree potential V_H
    ax = axes[0, 1]
    V_H = coulomb_1d_potential(rho)
    ax.plot(x, V_H, color=palette[1], linewidth=2.0, label=r"$V_H(x)$")
    ax.axhline(0, color="#3d3d3a", linewidth=0.6, alpha=0.5)
    ax.axvspan(A_LEFT, A_RIGHT, color=slab_color, alpha=0.12)
    ax.set_xlabel(r"$x$  (a$_0$)")
    ax.set_ylabel(r"$V_H(x)$  (Hartree)")
    ax.set_title("(b) Hartree potential")
    ax.set_xlim(0, L_BOX)
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    # (c) Total KS potential
    ax = axes[1, 0]
    V_xc = v_xc_1d(rho)
    V_KS = V_H + V_xc + V_jel
    ax.plot(x, V_H, color=palette[1], linewidth=1.2, label=r"$V_H$", alpha=0.7)
    ax.plot(x, V_xc, color=palette[2], linewidth=1.2, label=r"$V_{\rm xc}$", alpha=0.7)
    ax.plot(
        x, V_jel, color=palette[3], linewidth=1.2, label=r"$V_{\rm jellium}$", alpha=0.7
    )
    ax.plot(x, V_KS, color="#3d3d3a", linewidth=2.0, label=r"$V_{\rm KS}$")
    ax.axhline(0, color="#3d3d3a", linewidth=0.6, alpha=0.5)
    ax.axvspan(A_LEFT, A_RIGHT, color=slab_color, alpha=0.12)
    ax.set_xlabel(r"$x$  (a$_0$)")
    ax.set_ylabel(r"$V(x)$  (Hartree)")
    ax.set_title("(c) Kohn-Sham potential")
    ax.set_xlim(0, L_BOX)
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    # (d) Eigenvalues as horizontal lines, with |psi_1|^2 overlaid
    ax = axes[1, 1]
    # Overlay |psi_1|^2 on the same panel, rescaled to fit the y range.
    psi1_sq = psi[:, 0] ** 2
    scale = 0.4 * (eps[3] - eps[0]) / max(psi1_sq.max(), 1.0e-12)
    ax.fill_between(x, eps[0] + psi1_sq * scale, eps[0], color=palette[0], alpha=0.30)
    ax.plot(
        x,
        eps[0] + psi1_sq * scale,
        color=palette[0],
        linewidth=1.5,
        label=r"$|\psi_1|^2$  (rescaled)",
    )
    # Eigenvalues as horizontal lines
    for n in range(min(4, len(eps))):
        ax.axhline(
            eps[n],
            color=palette[n],
            linewidth=2.0,
            linestyle="--",
            label=rf"$\varepsilon_{n + 1} = {eps[n]:+.4f}\,E_h$",
        )
    ax.axvspan(A_LEFT, A_RIGHT, color=slab_color, alpha=0.12)
    ax.set_xlabel(r"$x$  (a$_0$)")
    ax.set_ylabel(r"$\varepsilon$  (Hartree)")
    ax.set_title("(d) Lowest KS eigenvalues + $|\\psi_1|^2$")
    ax.set_xlim(0, L_BOX)
    ax.set_ylim(eps[0] - 0.05, eps[3] + 0.05)
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    fig.suptitle(
        f"1-D jellium slab: $L_{{\\rm box}} = {L_BOX:.0f}\\,a_0$,"
        f" $L = {L:.0f}\\,a_0$,"
        f" $N = {N_ELEC}$,"
        f" $r_s = 1\\,a_0$"
        f"   (Dirac + Wigner, 1-D)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "03-jellium-slab.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
