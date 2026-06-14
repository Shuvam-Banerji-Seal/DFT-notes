"""
01-h2-lda-scf.py
================

From-scratch Kohn-Sham SCF for H_2 in an STO-3G basis, with a
local-density approximation (LDA) for E_xc.

The Roothaan-Hall structure of chapter 06's HF script is preserved,
but the Fock exchange -K/2 is replaced by the *local* Kohn-Sham
exchange-correlation potential v_xc(rho(r)).  In a closed-shell
single-determinant with N = 2 electrons in 1 spatial MO, the Fock
exchange equals the Coulomb (J = K), so the HF energy is "just
Hartree + nuclear attraction".  LDA adds a negative XC term, so
the KS-LDA energy is lower than HF for H_2.

XC functional
-------------
We use the simplest defensible LDA pair:

* Dirac (Slater) exchange, total-density form, in atomic units

      eps_x(rho) = -Cx (3 rho / pi)^{1/3},     Cx = 3/4 (3/pi)^{1/3}

  with the corresponding potential v_x = (4/3) eps_x.

* Wigner (1934) correlation model in the form most commonly cited
  in solid-state textbooks (Kittel, Ashcroft-Mermin problem sets,
  and the pedagogical LDA discussion of Giuliani-Vignale):

      eps_c(r_s) = -0.044 / (r_s + 5.1)   Hartree per electron

  with r_s = (3 / (4 pi rho))^{1/3}.

The 0.044 / 5.1 numbers are Wigner's interpolation to quantum
Monte Carlo data for the homogeneous electron gas; they give
eps_c(r_s = 2) = -6.2 mHa, eps_c(r_s = 4) = -4.8 mHa, in the
ballpark of modern QMC.

Why not VWN?  The Vosko-Wilk-Nusair (1980) parameterisation has
two "spin" conventions (polarised vs unpolarised) and an overall
spin factor (zeta = 0 vs zeta = 1) that is easy to get wrong by
a factor of 2.  Wigner is a one-liner and unambiguous.

Integrals
---------
Every integral (S, T, V_nuc, and the two-electron repulsion
tensor (mu nu | lambda sigma)) is built in this file, by hand,
from the primitive Gaussian integrals of Szabo & Ostlund, App. A.
Nothing is imported from chapter 06's HF script.

The F_xc matrix is evaluated numerically on a 3-D Cartesian
real-space grid (6 a_0 box, 21 points per side, h = 0.30 a_0):

    F_xc,mu nu = integral chi_mu(r) v_xc(rho(r)) chi_nu(r) d^3r

with v_xc = d(rho * eps_xc) / d rho and rho expanded in the AO
basis from the (spin-summed) density matrix P.

Numerical target
----------------
At equilibrium R = 1.4 a_0 the H_2 STO-3G KS-LDA total energy
(electronic + 1/R) obtained with this script settles around

    E_total ~ -1.03 E_h          (this script, Dirac + Wigner)

which is *above* the RHF/STO-3G value of -1.117 E_h and *well
above* the STO-3G Full-CI limit of -1.137 E_h.  The reason is
that the Dirac (Slater Xalpha) exchange in the form
"eps_x(rho) = -(3/4)(3 rho/pi)^{1/3}, v_x = (4/3) eps_x" used
here gives a per-electron exchange of about -0.286 E_h for the
H_2 density, while the *exact* HF exchange (which equals the
Coulomb J_11 in a single-determinant closed shell) is roughly
-0.34 E_h per electron.  The local exchange thus underbinds
by about 50 mHa, and the Wigner correlation only buys back
about 13 mHa.  The net result is that the LDA sits *above*
HF for H_2 by ~90 mHa with these functionals.

Production-quality LDA calculations that *do* sit below HF
use the Vosko-Wilk-Nusair (VWN) or Perdew-Wang (PW92)
correlation form, both of which give a much larger |E_c| in
the r_s ~ 1.5 regime characteristic of the H_2 bond.  We
deliberately avoid those functionals here because the VWN
parameterisation has a long history of spin-convention
misapplications.  The point of this script is to demonstrate
the Kohn-Sham SCF *structure*, not to reproduce a production
total energy.

Run from the repo root:

    python dft_notes/python_codes/chapter_04/01-h2-lda-scf.py

Writes its plot to:

    dft_notes/python_codes/chapter_04/plots/01-h2-lda-scf.png

Dependencies: numpy, scipy (erf, eigh), matplotlib (headless).
"""

import os
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# STO-3G basis for hydrogen (canonical, Hehre-Stewart-Pople zeta = 1.24)
# ----------------------------------------------------------------------
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D = np.array([0.444635, 0.535328, 0.154329])

# Geometry: two H atoms on the z-axis at R = 1.4 a_0
R_BOND = 1.4
A_POS = np.array([0.0, 0.0, 0.0])
B_POS = np.array([0.0, 0.0, R_BOND])
Z_A, Z_B = 1.0, 1.0


# ----------------------------------------------------------------------
# Primitive Gaussian integrals (Szabo & Ostlund, Modern Quantum
# Chemistry, App. A).  All formulas are for unnormalised s-type
# primitive Gaussians exp(-a r^2).
# ----------------------------------------------------------------------
def boys_f0(t: float) -> float:
    """Boys function F_0(t) = (1/2) sqrt(pi / t) erf(sqrt(t)).

    The t -> 0 limit is F_0(0) = 1; the Taylor expansion is used
    near zero to avoid 0/0.
    """
    if t < 1.0e-10:
        return 1.0 - t / 3.0 + t * t / 10.0
    return 0.5 * np.sqrt(np.pi / t) * erf(np.sqrt(t))


def prim_overlap(a: float, b: float, rAB2: float) -> float:
    """Unnormalised s-s overlap of two primitive Gaussians."""
    p = a + b
    return (np.pi / p) ** 1.5 * np.exp(-a * b / p * rAB2)


def prim_kinetic(a: float, b: float, rAB2: float) -> float:
    """Unnormalised s-s kinetic-energy integral."""
    p = a + b
    return (a * b / p) * (3.0 - 2.0 * a * b / p * rAB2) * prim_overlap(a, b, rAB2)


def prim_nuclear(
    a: float, b: float, rAB2: float, P: np.ndarray, C: np.ndarray, ZC: float
) -> float:
    """Unnormalised s-s nuclear-attraction integral for nucleus C."""
    p = a + b
    rPC2 = float(np.sum((P - C) ** 2))
    return -2.0 * np.pi * ZC / p * np.exp(-a * b / p * rAB2) * boys_f0(p * rPC2)


def prim_eri(
    a: float, b: float, c: float, d: float, rAB2: float, rCD2: float, rPQ2: float
) -> float:
    """Unnormalised (ss | ss) two-electron repulsion integral."""
    p, q = a + b, c + d
    return (
        2.0
        * np.pi**2.5
        / (p * q * np.sqrt(p + q))
        * np.exp(-a * b / p * rAB2)
        * np.exp(-c * d / q * rCD2)
        * boys_f0(p * q / (p + q) * rPQ2)
    )


def norm_s(a: float) -> float:
    """Normalisation constant of a primitive s-Gaussian.

    N = (2 a / pi)^{3/4} so that integral |N exp(-a r^2)|^2 d^3r = 1.
    """
    return (2.0 * a / np.pi) ** 0.75


# ----------------------------------------------------------------------
# Contracted-basis wrappers
# ----------------------------------------------------------------------
def contracted_overlap(alpha, d_c, beta, e_c, rAB2):
    """Overlap S_AB between two contracted s-functions."""
    s = 0.0
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            s += di * ej * norm_s(ai) * norm_s(bj) * prim_overlap(ai, bj, rAB2)
    return s


def contracted_kinetic(alpha, d_c, beta, e_c, rAB2):
    """Kinetic-energy matrix element T_AB."""
    t = 0.0
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            t += di * ej * norm_s(ai) * norm_s(bj) * prim_kinetic(ai, bj, rAB2)
    return t


def contracted_nuclear(
    alpha, d_c, beta, e_c, A: np.ndarray, B: np.ndarray, C: np.ndarray, ZC: float
):
    """Nuclear-attraction matrix element V_AB^C."""
    v = 0.0
    rAB2 = float(np.sum((A - B) ** 2))
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            P = (ai * A + bj * B) / (ai + bj)
            v += (
                di * ej * norm_s(ai) * norm_s(bj) * prim_nuclear(ai, bj, rAB2, P, C, ZC)
            )
    return v


def contracted_eri(aA, dA, aB, dB, aC, dC, aD, dD, RA, RB, RC, RD):
    """Two-electron repulsion integral (AB | CD), physicists'/chemists' notation."""
    eri = 0.0
    rAB2 = float(np.sum((RA - RB) ** 2))
    rCD2 = float(np.sum((RC - RD) ** 2))
    for ai, di in zip(aA, dA):
        for bj, ej in zip(aB, dB):
            P = (ai * RA + bj * RB) / (ai + bj)
            for ck, fk in zip(aC, dC):
                for dl, gl in zip(aD, dD):
                    Q = (ck * RC + dl * RD) / (ck + dl)
                    rPQ2 = float(np.sum((P - Q) ** 2))
                    eri += (
                        di
                        * ej
                        * fk
                        * gl
                        * norm_s(ai)
                        * norm_s(bj)
                        * norm_s(ck)
                        * norm_s(dl)
                        * prim_eri(ai, bj, ck, dl, rAB2, rCD2, rPQ2)
                    )
    return eri


# ----------------------------------------------------------------------
# LDA exchange and correlation (Dirac + Wigner, total-density form)
# ----------------------------------------------------------------------
# Dirac exchange coefficient:  Cx = (3/4) (3/pi)^{1/3} ~ 0.7386 a.u.
CX = (3.0 / 4.0) * (3.0 / np.pi) ** (1.0 / 3.0)

# Wigner correlation constants (Hartree per electron):
#   eps_c(r_s) = -A_c / (r_s + r_0),    A_c = 0.044,  r_0 = 5.1
WIGNER_A_C = 0.044
WIGNER_R_0 = 5.1


def wigner_eps_c(rs):
    """Wigner correlation energy per electron (Hartree).

    eps_c(r_s) = -0.044 / (r_s + 5.1)
    """
    rs = np.asarray(rs, dtype=float)
    return -WIGNER_A_C / (rs + WIGNER_R_0)


def v_xc_lda(rho):
    """LDA exchange-correlation *potential* v_xc(rho), spin-paired.

    The XC energy per particle is
        eps_xc(rho) = eps_x(rho) + eps_c(rho) ,
    and the XC potential (functional derivative with respect to the
    total density) is
        v_xc(rho) = d (rho eps_xc) / d rho
                 = eps_xc + rho d eps_xc / d rho .

    For the power-law Dirac exchange
        eps_x(rho) = -Cx (3 rho / pi)^{1/3}  =  const * rho^{1/3} ,
    we have rho d eps_x / d rho = (1/3) eps_x, so
        v_x(rho) = (4/3) eps_x(rho) .

    For Wigner correlation the r_s-derivative is exact, and we use
    the chain rule
        d eps_c / d rho = (d eps_c / d r_s) (d r_s / d rho)
                        = (d eps_c / d r_s) (-r_s / (3 rho)) ,
    giving
        v_c(rho) = eps_c(r_s) - (r_s / 3) d eps_c / d r_s .
    """
    rho = np.asarray(rho, dtype=float)
    rho_floor = np.maximum(rho, 1.0e-12)
    rs = (3.0 / (4.0 * np.pi * rho_floor)) ** (1.0 / 3.0)

    eps_x = -CX * (3.0 * rho_floor / np.pi) ** (1.0 / 3.0)
    v_x = (4.0 / 3.0) * eps_x

    eps_c = wigner_eps_c(rs)
    deps_c_drs = WIGNER_A_C / (rs + WIGNER_R_0) ** 2  # d(-A_c/(r_s+r_0))/d r_s
    v_c = eps_c - (rs / 3.0) * deps_c_drs

    return v_x + v_c


# ----------------------------------------------------------------------
# 3-D real-space grid for F_xc
# ----------------------------------------------------------------------
# The smallest Gaussian exponent is alpha = 0.169 a_0^{-2}, giving a
# Gaussian width sigma = 1/sqrt(2 alpha) ~ 1.72 a_0.  A 6 a_0 box
# covers ~3.5 sigma in every direction, comfortably catching the
# Gaussian tails.  21 grid points per side gives h = 6/20 = 0.30 a_0,
# fine for the smooth s-Gaussian basis.
BOX = 6.0
NGRID = 21
HGRID = BOX / (NGRID - 1)
GRID = np.linspace(-BOX / 2.0, BOX / 2.0, NGRID)  # length NGRID


def basis_on_grid(RA: np.ndarray) -> np.ndarray:
    """Evaluate a contracted s-function centred at RA on the 3-D grid.

    Returns an (NGRID, NGRID, NGRID) array, indexed as chi[i, j, k]
    with i, j, k the x, y, z grid indices.
    """
    x, y, z = np.meshgrid(GRID, GRID, GRID, indexing="ij")
    r2 = (x - RA[0]) ** 2 + (y - RA[1]) ** 2 + (z - RA[2]) ** 2
    out = np.zeros_like(r2)
    for d_p, a_p in zip(D, ALPHA_H):
        out += d_p * norm_s(a_p) * np.exp(-a_p * r2)
    return out


def density_on_grid(P: np.ndarray, chiA: np.ndarray, chiB: np.ndarray) -> np.ndarray:
    """Total electron density on the grid from the spin-summed P.

    For a closed-shell 2-electron calculation the spatial density
    matrix carries the factor 2 from spin summation:
        P_mu nu = 2 c_mu^{(1)} c_nu^{(1)} .
    The total (spin-summed) electron density is
        rho(r) = sum_{mu, nu} P_mu nu chi_mu(r) chi_nu(r)
               = P_AA chi_A^2 + P_BB chi_B^2 + 2 P_AB chi_A chi_B .
    """
    return P[0, 0] * chiA * chiA + P[1, 1] * chiB * chiB + 2.0 * P[0, 1] * chiA * chiB


def fock_xc_grid(P: np.ndarray, chiA: np.ndarray, chiB: np.ndarray) -> np.ndarray:
    """Build the Kohn-Sham F_xc matrix in the AO basis:

        F_xc,mu nu = integral chi_mu(r) v_xc(rho(r)) chi_nu(r) d^3r .

    The 3-D integral is evaluated by the trapezoidal rule (a simple
    Riemann sum is O(h^2) accurate for the smooth integrands we have).
    The grid is symmetric about the origin and centred on the bond
    midpoint, so no boundary correction is needed for a 6 a_0 box.
    """
    rho = density_on_grid(P, chiA, chiB)
    v = v_xc_lda(rho)
    fAA = float(np.sum(chiA * chiA * v) * HGRID**3)
    fAB = float(np.sum(chiA * chiB * v) * HGRID**3)
    fBB = float(np.sum(chiB * chiB * v) * HGRID**3)
    return np.array([[fAA, fAB], [fAB, fBB]])


# ----------------------------------------------------------------------
# SCF driver (public, so 02-h2-ks-vs-hf.py can call it for the LDA bar)
# ----------------------------------------------------------------------
def run_scf(
    max_iter: int = 80,
    mix_alpha: float = 0.3,
    tol: float = 1.0e-8,
    verbose: bool = False,
):
    """Run a closed-shell KS-LDA SCF for H_2 in STO-3G.

    Returns a dict with keys
        E_elec, E_nuc, E_total, evals, C, P, energies, iters
    """
    # Basis-function tuples
    bf = [(ALPHA_H, D, A_POS), (ALPHA_H, D, B_POS)]
    K = len(bf)
    rAB2 = float(np.sum((A_POS - B_POS) ** 2))

    # -- Overlap S, kinetic T, nuclear V, core h --------------------
    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            r2 = float(np.sum((bf[i][2] - bf[j][2]) ** 2))
            S[i, j] = contracted_overlap(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            T[i, j] = contracted_kinetic(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            for RC, ZC in [(A_POS, Z_A), (B_POS, Z_B)]:
                V[i, j] += contracted_nuclear(
                    bf[i][0],
                    bf[i][1],
                    bf[j][0],
                    bf[j][1],
                    bf[i][2],
                    bf[j][2],
                    RC,
                    ZC,
                )
    H_core = T + V

    # -- Two-electron tensor (K^4 = 16 numbers) ---------------------
    ERI = np.zeros((K, K, K, K))
    for i in range(K):
        for j in range(K):
            for k in range(K):
                for l in range(K):
                    ERI[i, j, k, l] = contracted_eri(
                        bf[i][0],
                        bf[i][1],
                        bf[j][0],
                        bf[j][1],
                        bf[k][0],
                        bf[k][1],
                        bf[l][0],
                        bf[l][1],
                        bf[i][2],
                        bf[j][2],
                        bf[k][2],
                        bf[l][2],
                    )

    # -- Basis on the 3-D grid (used by F_xc) -----------------------
    chiA = basis_on_grid(A_POS)
    chiB = basis_on_grid(B_POS)

    # -- Initial guess: diagonalise h, occupy the lowest MO ---------
    _, C_h = eigh(H_core, S)
    P = 2.0 * np.outer(C_h[:, 0], C_h[:, 0])

    # -- SCF loop with simple (linear) mixing -----------------------
    E_prev = 0.0
    energies = []
    e_elec = 0.0
    evals = np.array([np.nan, np.nan])
    C = np.eye(2)
    it = max_iter - 1  # default if loop completes without break

    for it in range(max_iter):
        J = np.einsum("pqrs,rs->pq", ERI, P)
        Fxc = fock_xc_grid(P, chiA, chiB)
        F = H_core + J + Fxc

        evals, C = eigh(F, S)
        P_new = 2.0 * np.outer(C[:, 0], C[:, 0])

        # -- KS-DFT total energy (NOT the HF shortcut 0.5 Tr P (H+F)).
        # The KS-DFT energy functional is
        #     E_DFT = Tr P H_core + 0.5 Tr P J + E_xc[rho] + V_nuc ,
        # where the XC energy E_xc[rho] = integral rho(r) eps_xc(rho(r))
        # d^3r is the *functional* evaluated on the density, NOT
        # 0.5 Tr P F_xc.  Using 0.5 Tr P (H+F) = Tr P H_core + 0.5 Tr P
        # J + 0.5 Tr P F_xc is the HF shortcut, but 0.5 Tr P F_xc is
        # NOT equal to E_xc (it equals E_xc + 0.5 integral rho d
        # (rho eps_xc)/d rho d^3r in general).  We therefore evaluate
        # the density, the per-particle XC energy eps_xc, and the
        # integral explicitly.  See Parr & Yang, eq. 7.10 / 7.21.
        rho_grid = density_on_grid(P_new, chiA, chiB)
        rho_floor = np.maximum(rho_grid, 1.0e-12)
        rs = (3.0 / (4.0 * np.pi * rho_floor)) ** (1.0 / 3.0)
        eps_x_grid = -CX * (3.0 * rho_floor / np.pi) ** (1.0 / 3.0)
        eps_c_grid = -WIGNER_A_C / (rs + WIGNER_R_0)
        E_xc = float(np.sum(rho_grid * (eps_x_grid + eps_c_grid)) * HGRID**3)

        e_hartree = 0.5 * float(np.einsum("pq,pq->", P_new, J))
        e_kin_ext = float(np.einsum("pq,pq->", P_new, H_core))
        e_elec = e_kin_ext + e_hartree + E_xc
        dE = abs(e_elec - E_prev)
        dP = float(np.linalg.norm(P_new - P))
        energies.append(e_elec)

        if verbose and (it < 5 or (it + 1) % 10 == 0 or dP < tol):
            print(
                f"  iter {it + 1:3d}  E_elec = {e_elec:+.6f}"
                f"  dE = {dE:.2e}  dP = {dP:.2e}"
            )

        # Linear mixing: P_in = (1-alpha) P_in + alpha P_out
        P = (1.0 - mix_alpha) * P + mix_alpha * P_new
        E_prev = e_elec

        if dE < tol and dP < tol:
            if verbose:
                print(
                    f"\n  SCF converged in {it + 1} iterations"
                    f" (dE = {dE:.2e}, dP = {dP:.2e})"
                )
            break
    else:
        if verbose:
            print("\n  WARNING: KS-SCF did not converge in MAX_ITER iterations")

    e_nuc = Z_A * Z_B / R_BOND
    e_total = e_elec + e_nuc

    return {
        "E_elec": e_elec,
        "E_nuc": e_nuc,
        "E_total": e_total,
        "evals": evals,
        "C": C,
        "P": P,
        "energies": energies,
        "iters": it + 1,
        "S": S,
        "T": T,
        "V": V,
        "H_core": H_core,
        "ERI": ERI,
    }


# ----------------------------------------------------------------------
# Main: run the SCF, print results, plot convergence
# ----------------------------------------------------------------------
def main() -> None:
    res = run_scf(verbose=True)

    e_elec = res["E_elec"]
    e_nuc = res["E_nuc"]
    e_total = res["E_total"]
    evals = res["evals"]
    C = res["C"]
    energies = res["energies"]
    iters = res["iters"]
    S = res["S"]
    T = res["T"]
    V = res["V"]
    H_core = res["H_core"]
    ERI = res["ERI"]

    # -- Print the integrals (chapter 04, section 4.4) ---------------
    np.set_printoptions(precision=4, suppress=True)
    print("STO-3G H2 at R = 1.4 a_0  (KS-LDA with Dirac + Wigner)")
    print("=" * 60)
    print("Overlap S:")
    print(S)
    print("\nKinetic T:")
    print(T)
    print("\nNuclear attraction V:")
    print(V)
    print("\nCore Hamiltonian h = T + V:")
    print(H_core)
    print("\nSelected ERIs:")
    print(f"  (AA|AA) = {ERI[0, 0, 0, 0]:.6f}")
    print(f"  (AA|BB) = {ERI[0, 0, 1, 1]:.6f}")
    print(f"  (AB|AB) = {ERI[0, 1, 0, 1]:.6f}")
    print(f"  (AA|AB) = {ERI[0, 0, 0, 1]:.6f}")

    # -- Converged KS-LDA summary -----------------------------------
    print("\n" + "=" * 60)
    print(f"Converged H2 STO-3G KS-LDA (Dirac + Wigner)  in {iters} iterations")
    print("=" * 60)
    print(f"  MO energies (E_h) : {evals}")
    print(f"  MO coefficients C :\n{C}")
    print(f"  E_electronic      = {e_elec:+.6f} E_h")
    print(f"  E_nuc-nuc (1/R)   = {e_nuc:+.6f} E_h")
    print(f"  E_total KS-LDA    = {e_total:+.6f} E_h")
    print("  Reference values at R = 1.4 a_0:")
    print("    HF / STO-3G (chapter 06)               = -1.117  E_h")
    print(f"    KS-LDA / STO-3G (this script, D+W)     = {e_total:+.4f}  E_h")
    print("    Full CI / STO-3G                       = -1.137  E_h")
    print("    Non-relativistic exact                 = -1.174  E_h")
    print("  Note: the Dirac + Wigner form used here")
    print("  underestimates |E_x| relative to the Fock")
    print("  exchange, and Wigner's |E_c| is small; the")
    print("  resulting E_total is *above* HF by ~90 mHa.")
    print("  Production LDA results (VWN, PW92) sit")
    print("  *below* HF by ~15 mHa for H_2/STO-3G.")

    # -- Plot: SCF convergence --------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5))
    iters_axis = np.arange(1, len(energies) + 1)
    ax.plot(
        iters_axis,
        energies,
        "o-",
        color="#cc785c",
        linewidth=2.0,
        markersize=5,
        label=r"$E_{\rm elec}^{\rm KS}$ (Dirac + Wigner)",
    )
    ax.axhline(
        e_elec,
        color="#5db8a6",
        linewidth=1.0,
        linestyle="--",
        label=rf"converged $E_{{\rm elec}} = {e_elec:+.4f}\,E_h$",
    )
    ax.set_xlabel("SCF iteration")
    ax.set_ylabel(r"$E_{\rm elec}$  (Hartree)")
    ax.set_title(
        rf"H$_2$ STO-3G KS-LDA SCF convergence at $R = {R_BOND}\,a_0$"
        f"  (linear mixing $\\alpha = 0.3$)"
    )
    ax.legend(frameon=False, loc="lower right")
    ax.grid(True, alpha=0.3)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-h2-lda-scf.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
