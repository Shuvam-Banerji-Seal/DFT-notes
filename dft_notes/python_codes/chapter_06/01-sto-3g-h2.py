"""
01-sto-3g-h2.py
================
STO-3G basis for H2 at R = 1.4 a_0.  Build the overlap S, the
one-electron core Hamiltonian h, and the Fock matrix F.  Solve the
Roothaan-Hall equations FC = SCE.  Print the matrices and total
energy; plot the two molecular orbitals along the bond axis.

The basis is the canonical STO-3G three-primitive contraction
fitted to a Slater 1s orbital with zeta = 1.24 (the value
optimised by Hehre, Stewart & Pople 1969 for the H atom in
molecules).  Two contracted s-functions, one centred on each
hydrogen, give a 2 x 2 problem that can be solved in closed form
in a single SCF iteration once the integrals are built (in
practice we iterate until the density is self-consistent).

Why this script lives in chapter 06:
  - Section 6.9 (worked example) walks through exactly these
    numbers.  The script is the source of truth for the matrix
    elements quoted in the chapter; if the chapter and the
    script disagree, the script wins.
  - The plot illustrates the two MOs: the bonding sigma_g
    (positive linear combination of the two atomic functions)
    and the antibonding sigma_u^* (negative combination, with a
    node at the midpoint).

Dependencies: numpy, scipy (eigh + erf), matplotlib (headless).

Run from the repo root:
    python dft_notes/python_codes/chapter_06/01-sto-3g-h2.py

Writes its plot to:
    dft_notes/python_codes/chapter_06/plots/01-sto-3g-h2.png
"""

import os
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")  # headless — no display required
import matplotlib.pyplot as plt


# ─── STO-3G parameters for hydrogen ──────────────────────────────
# Canonical STO-3G H 1s basis from the EMSL Basis Set Exchange.
# These exponents already incorporate the Hehre-Stewart-Pople
# molecular value zeta = 1.24 for hydrogen (the underlying
# zeta = 1.0 fit has exponents smaller by a factor of 1.24**2 =
# 1.5376; e.g. alpha_1^{zeta=1.0} = 0.10982 -> 0.16886 when
# scaled).  The contraction coefficients d_p multiply the
# *normalised* primitive Gaussians and are independent of zeta.
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D = np.array([0.444635, 0.535328, 0.154329])

# Geometry: two H atoms on the z-axis at R = 1.4 a_0 ------------
R_BOND = 1.4
A_POS = np.array([0.0, 0.0, 0.0])
B_POS = np.array([0.0, 0.0, R_BOND])
Z_A, Z_B = 1.0, 1.0


# ─── Primitive integrals (unnormalised s-Gaussians) ──────────────
# Formulas: Szabo & Ostlund, *Modern Quantum Chemistry*, App. A.


def boys_f0(t: float) -> float:
    """Boys function F_0(t) = (1/2) sqrt(pi/t) erf(sqrt(t)).

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
    """Unnormalised (ss|ss) two-electron repulsion integral."""
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

    N = (2 alpha / pi) ** (3/4) so that integral |N exp(-a r**2)|**2 = 1.
    """
    return (2.0 * a / np.pi) ** 0.75


# ─── Contracted-basis wrappers ────────────────────────────────────
def contracted_overlap(alpha, d_c, beta, e_c, rAB2):
    """Overlap S_AB between two contracted s-functions."""
    S = 0.0
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            S += di * ej * norm_s(ai) * norm_s(bj) * prim_overlap(ai, bj, rAB2)
    return S


def contracted_kinetic(alpha, d_c, beta, e_c, rAB2):
    """Kinetic-energy matrix element T_AB."""
    T = 0.0
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            T += di * ej * norm_s(ai) * norm_s(bj) * prim_kinetic(ai, bj, rAB2)
    return T


def contracted_nuclear(
    alpha, d_c, beta, e_c, A: np.ndarray, B: np.ndarray, C: np.ndarray, ZC: float
):
    """Nuclear-attraction matrix element V_AB^C."""
    V = 0.0
    rAB2 = float(np.sum((A - B) ** 2))
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            P = (ai * A + bj * B) / (ai + bj)
            V += (
                di * ej * norm_s(ai) * norm_s(bj) * prim_nuclear(ai, bj, rAB2, P, C, ZC)
            )
    return V


def contracted_eri(aA, dA, aB, dB, aC, dC, aD, dD, RA, RB, RC, RD):
    """Two-electron integral (AB|CD) in physicists' chemists' notation."""
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


def main() -> None:
    # ─── Geometry & basis tuples ─────────────────────────────────
    # Each basis function is a triple (exponents, coefficients, centre).
    bf = [(ALPHA_H, D, A_POS), (ALPHA_H, D, B_POS)]
    K = len(bf)  # K = 2 basis functions
    rAB2 = float(np.sum((A_POS - B_POS) ** 2))

    # ─── Overlap matrix S (K x K) ────────────────────────────────
    S = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            r2 = float(np.sum((bf[i][2] - bf[j][2]) ** 2))
            S[i, j] = contracted_overlap(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)

    # ─── Kinetic-energy matrix T ────────────────────────────────
    T = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            r2 = float(np.sum((bf[i][2] - bf[j][2]) ** 2))
            T[i, j] = contracted_kinetic(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)

    # ─── Nuclear-attraction matrix V (sum over both nuclei) ────
    V = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            for RC, ZC in [(A_POS, Z_A), (B_POS, Z_B)]:
                V[i, j] += contracted_nuclear(
                    bf[i][0], bf[i][1], bf[j][0], bf[j][1], bf[i][2], bf[j][2], RC, ZC
                )
    Hcore = T + V

    # ─── Two-electron integral tensor (K**4) ────────────────────
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

    # ─── Print the integrals ─────────────────────────────────────
    np.set_printoptions(precision=4, suppress=True)
    print("Overlap S:")
    print(S)
    print("\nKinetic T:")
    print(T)
    print("\nNuclear attraction V:")
    print(V)
    print("\nCore Hamiltonian h = T + V:")
    print(Hcore)
    print("\nSelected ERIs (chemists' notation [ij|kl]):")
    print(f"  [11|11] = (AA|AA) = {ERI[0, 0, 0, 0]:.6f}")
    print(f"  [11|22] = (AA|BB) = {ERI[0, 0, 1, 1]:.6f}")
    print(f"  [12|12] = (AB|AB) = {ERI[0, 1, 0, 1]:.6f}")
    print(f"  [11|12] = (AA|AB) = {ERI[0, 0, 0, 1]:.6f}")

    # ─── SCF loop (closed-shell, 2 electrons in 1 occupied MO) ───
    P = np.zeros((K, K))  # initial density: zero (uses h as F)
    E_prev = 0.0
    for it in range(64):
        J = np.einsum("pqrs,rs->pq", ERI, P)
        Kx = np.einsum("prqs,rs->pq", ERI, P)
        F = Hcore + J - 0.5 * Kx
        evals, C = eigh(F, S)
        # 2 electrons go in the lowest MO (closed shell)
        P_new = 2.0 * np.outer(C[:, 0], C[:, 0])
        E_elec = 0.5 * float(np.einsum("pq,pq->", P_new, Hcore + F))
        dE = abs(E_elec - E_prev)
        dP = float(np.linalg.norm(P_new - P))
        P, E_prev = P_new, E_elec
        if dE < 1e-10 and dP < 1e-10:
            print(
                f"\nSCF converged in {it + 1} iterations (dE = {dE:.2e}, dP = {dP:.2e})"
            )
            break
    else:
        print("\nWARNING: SCF did not converge")

    E_nuc = Z_A * Z_B / R_BOND
    E_total = E_elec + E_nuc
    print(f"\n*** Converged H2 STO-3G HF energy ***")
    print(f"  MO energies (E_h) : {evals}")
    print(f"  MO coefficients C :\n{C}")
    print(f"  E_electronic      = {E_elec:+.6f} E_h")
    print(f"  E_nuc-nuc (1/R)   = {E_nuc:+.6f} E_h")
    print(f"  E_total HF        = {E_total:+.6f} E_h")
    print(f"  (Szabo & Ostlund table 3.5 quote -1.1167  E_h)")

    # ─── Plot the two MOs along the bond axis ──────────────────
    z = np.linspace(-2.5, R_BOND + 2.5, 401)

    def chi(z_array: np.ndarray, R_atom: float) -> np.ndarray:
        """Contracted s-function centred at R_atom, sampled along z."""
        out = np.zeros_like(z_array)
        for d_p, a_p in zip(D, ALPHA_H):
            out += d_p * norm_s(a_p) * np.exp(-a_p * (z_array - R_atom) ** 2)
        return out

    chiA = chi(z, 0.0)
    chiB = chi(z, R_BOND)

    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

    palette = ["#cc785c", "#5db8a6"]  # coral, teal
    labels = [
        rf"$\psi_1 = \sigma_g$    ($\varepsilon_1 = {evals[0]:+.4f}\,E_h$)",
        rf"$\psi_2 = \sigma_u^*$ ($\varepsilon_2 = {evals[1]:+.4f}\,E_h$)",
    ]
    for k in range(2):
        psi_mo = C[0, k] * chiA + C[1, k] * chiB
        axes[k].plot(z, psi_mo, color=palette[k], linewidth=2.2, label=labels[k])
        axes[k].axhline(0, color="#a09d96", lw=0.6, alpha=0.5)
        axes[k].axvline(0.0, color="#3d3d3a", lw=0.8, alpha=0.4, linestyle=":")
        axes[k].axvline(R_BOND, color="#3d3d3a", lw=0.8, alpha=0.4, linestyle=":")
        axes[k].set_ylabel(r"$\psi(z)$  (a$_0^{-3/2}$)")
        axes[k].legend(loc="upper right", frameon=False, fontsize=10)
        axes[k].grid(True, alpha=0.2)
        axes[k].spines["top"].set_visible(False)
        axes[k].spines["right"].set_visible(False)
    axes[1].set_xlabel(r"$z$  (atomic units, along bond axis)")
    axes[0].set_title(rf"H$_2$ STO-3G molecular orbitals at $R = {R_BOND}\,a_0$")
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-sto-3g-h2.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
