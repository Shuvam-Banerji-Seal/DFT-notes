"""
03-h2-full-ci-toy.py
====================

Full configuration interaction (FCI) on a *toy* 2-electron, 2-orbital
H_2 model in the canonical STO-3G minimal basis.

The spin-free singlet configuration state function (CSF) basis for
two electrons distributed over two spatial MOs {g, u} is

    |Phi_1> = |gg>          (closed shell: 2 electrons in g)
    |Phi_2> = |uu>          (closed shell: 2 electrons in u)
    |Phi_3> = |(gu) S=0>    (open-shell singlet, both MOs singly occ.)

The 3x3 Hamiltonian in this basis follows from the Slater-Condon
rules (Szabo & Ostlund, *Modern Quantum Chemistry*, table 4.4) and
the 8-fold permutational symmetry of the spatial MOs:

    H_11 = 2 h_g + J_gg                          (RHF / |gg> alone)
    H_22 = 2 h_u + J_uu                          (|uu> alone)
    H_33 = h_g + h_u + J_gu + K_gu               (open-shell singlet)
    H_12 = H_21 = K_gu                            (double-excitation coup)
    H_13 = H_31 = sqrt(2) * <g | h | u>           (Brillouin: 0 in HF MOs)
    H_23 = H_32 = sqrt(2) * <u | h | g>           (Brillouin: 0 in HF MOs)

For *HF* (canonical) MOs the off-diagonals involving |(gu)S=0> vanish
by Brillouin's theorem, and the lowest eigenvalue of the 2x2
{|gg>, |uu>} block is the FCI ground state.  The triplet state
|S=1, M_S=0> has the same spatial part as the open-shell singlet
but with K_gu subtracted:

    E_T(R) = h_g + h_u + J_gu - K_gu.

Total energy curves include the nuclear repulsion 1 / R.

What this script does:

  1.  At each H-H distance R in [0.6, 4.0] a_0, builds the STO-3G
      AOs (3-Gaussian fit to a 1s STO, zeta = 1.24 from
      Hehre-Stewart-Pople 1969) centred on the two protons.
  2.  Computes S, T, V_nuc, and the 2-electron (ij|kl) tensor.
  3.  Runs RHF (closed-shell, 1 doubly-occupied MO) until the
      density is self-consistent.
  4.  Transforms the spatial one- and two-electron integrals to
      the MO basis {g, u}.
  5.  Builds the 3x3 singlet CI matrix, diagonalises, and takes
      the lowest eigenvalue as the FCI energy.
  6.  Plots E_FCI(R), E_T(R), and E_RHF(R) (the energy of |gg>
      alone) on the same axes.
  7.  Prints the energies at R = 0.6, 1.0, 1.4, 2.0, 3.0, 4.0 a_0.

Why this script lives in chapter 02:

    Section 2.x (the many-body problem) introduces the e-e
    repulsion 1/r_12 as the *correlation* term.  FCI is the
    "exact" solution in a given one-electron basis, and
    H_2 in the minimal STO-3G basis is the simplest system where
    FCI can be worked out by hand (3 CSFs, 3x3 matrix).  The plot
    shows the FCI-RHF gap as a function of R, the dissociation
    pathology of RHF (it goes to -infinity too fast on
    dissociation), and the correct covalent dissociation of FCI
    into two neutral H atoms.

Dependencies: numpy, scipy (eigh + erf), matplotlib (headless via Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_02/03-h2-full-ci-toy.py

Writes its plot to:

    dft_notes/python_codes/chapter_02/plots/03-h2-full-ci-toy.png
"""

import os
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ─── STO-3G parameters for hydrogen (Hehre-Stewart-Pople, 1969) ─────────
# 3-Gaussian fit to a 1s STO with zeta = 1.24, the molecular value
# optimised for H in molecules (not the atomic value zeta = 1).
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D = np.array([0.444635, 0.535328, 0.154329])

R_GRID = np.linspace(0.6, 4.0, 35)
R_PRINT = np.array([0.6, 1.0, 1.4, 2.0, 3.0, 4.0])
Z_A, Z_B = 1.0, 1.0


# ─── Primitive (unnormalised s-Gaussian) integral formulas ──────────────
# Szabo & Ostlund, *Modern Quantum Chemistry*, App. A.


def boys_f0(t: float) -> float:
    """Boys function F_0(t) = (1/2) sqrt(pi / t) erf(sqrt(t))."""
    if t < 1.0e-10:
        return 1.0 - t / 3.0 + t * t / 10.0
    return 0.5 * np.sqrt(np.pi / t) * erf(np.sqrt(t))


def prim_overlap(a: float, b: float, rAB2: float) -> float:
    p = a + b
    return (np.pi / p) ** 1.5 * np.exp(-a * b / p * rAB2)


def prim_kinetic(a: float, b: float, rAB2: float) -> float:
    p = a + b
    return (a * b / p) * (3.0 - 2.0 * a * b / p * rAB2) * prim_overlap(a, b, rAB2)


def prim_nuclear(
    a: float, b: float, rAB2: float, P: np.ndarray, C: np.ndarray, ZC: float
) -> float:
    p = a + b
    rPC2 = float(np.sum((P - C) ** 2))
    return -2.0 * np.pi * ZC / p * np.exp(-a * b / p * rAB2) * boys_f0(p * rPC2)


def prim_eri(
    a: float, b: float, c: float, d: float, rAB2: float, rCD2: float, rPQ2: float
) -> float:
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
    """Normalisation of a primitive s-Gaussian: N = (2a/pi)^(3/4)."""
    return (2.0 * a / np.pi) ** 0.75


# ─── Contracted-basis wrappers ──────────────────────────────────────────


def contracted_overlap(alpha, d_c, beta, e_c, rAB2):
    S = 0.0
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            S += di * ej * norm_s(ai) * norm_s(bj) * prim_overlap(ai, bj, rAB2)
    return S


def contracted_kinetic(alpha, d_c, beta, e_c, rAB2):
    T = 0.0
    for ai, di in zip(alpha, d_c):
        for bj, ej in zip(beta, e_c):
            T += di * ej * norm_s(ai) * norm_s(bj) * prim_kinetic(ai, bj, rAB2)
    return T


def contracted_nuclear(alpha, d_c, beta, e_c, A, B, C, ZC):
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


# ─── Single-point: AO integrals, RHF, MO integrals, CI ─────────────────


def run_rhf_and_ci(R: float):
    """Return (E_RHF, E_FCI, E_T, c_g) for H_2 at bond length R (a_0).

    E_RHF : total RHF energy (|gg> alone), a.u.
    E_FCI : lowest singlet eigenvalue of the 3x3 CI matrix, a.u.
    E_T   : lowest triplet energy, a.u.
    c_g   : (1,) MO coefficient of AO A in the g MO, for the snapshot.
    """
    A = np.array([0.0, 0.0, 0.0])
    B = np.array([0.0, 0.0, R])
    bf = [(ALPHA_H, D, A), (ALPHA_H, D, B)]
    K = 2  # two basis functions

    # AO integrals
    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            r2 = float(np.sum((bf[i][2] - bf[j][2]) ** 2))
            S[i, j] = contracted_overlap(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            T[i, j] = contracted_kinetic(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            for RC, ZC in [(A, Z_A), (B, Z_B)]:
                V[i, j] += contracted_nuclear(
                    bf[i][0], bf[i][1], bf[j][0], bf[j][1], bf[i][2], bf[j][2], RC, ZC
                )
    Hcore = T + V

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

    # RHF loop (closed-shell, 2 electrons, 1 doubly-occupied MO)
    P = np.zeros((K, K))
    E_prev = 0.0
    for it in range(64):
        J = np.einsum("pqrs,rs->pq", ERI, P)
        Kx = np.einsum("prqs,rs->pq", ERI, P)
        F = Hcore + J - 0.5 * Kx
        evals, C = eigh(F, S)
        P_new = 2.0 * np.outer(C[:, 0], C[:, 0])
        E_elec = 0.5 * float(np.einsum("pq,pq->", P_new, Hcore + F))
        if abs(E_elec - E_prev) < 1e-12 and float(np.linalg.norm(P_new - P)) < 1e-12:
            break
        P, E_prev = P_new, E_elec
    E_nuc = Z_A * Z_B / R
    E_rhf = E_elec + E_nuc

    # Transform one- and two-electron integrals to the MO basis
    # (2 MOs, ordered as C[:, 0] = g, C[:, 1] = u).
    h_mo = C.T @ Hcore @ C  # (2, 2)
    # (pq|rs)_MO in chemists' notation
    eri_mo = np.einsum("pi,qj,rk,sl,pqrs->ijkl", C, C, C, C, ERI)
    h_g, h_u = h_mo[0, 0], h_mo[1, 1]
    J_gg = eri_mo[0, 0, 0, 0]
    J_uu = eri_mo[1, 1, 1, 1]
    J_gu = eri_mo[0, 0, 1, 1]
    K_gu = eri_mo[0, 1, 0, 1]
    h_gu = h_mo[0, 1]  # one-electron off-diagonal in MO basis

    # 3x3 singlet CI matrix in the { |gg>, |uu>, |(gu)S=0> } basis
    H_ci = np.zeros((3, 3))
    H_ci[0, 0] = 2.0 * h_g + J_gg
    H_ci[1, 1] = 2.0 * h_u + J_uu
    H_ci[2, 2] = h_g + h_u + J_gu + K_gu
    H_ci[0, 1] = H_ci[1, 0] = K_gu
    H_ci[0, 2] = H_ci[2, 0] = np.sqrt(2.0) * h_gu
    H_ci[1, 2] = H_ci[2, 1] = np.sqrt(2.0) * h_gu
    ci_evals = np.linalg.eigvalsh(H_ci)
    E_fci_elec = float(ci_evals[0])
    E_fci = E_fci_elec + E_nuc

    # Triplet (g, u) with one electron in each
    E_T = h_g + h_u + J_gu - K_gu + E_nuc

    return E_rhf, E_fci, E_T, C[:, 0], h_gu, K_gu


# ─── Main ───────────────────────────────────────────────────────────────


def main() -> None:
    E_rhf_arr = np.zeros_like(R_GRID)
    E_fci_arr = np.zeros_like(R_GRID)
    E_t_arr = np.zeros_like(R_GRID)
    h_gu_arr = np.zeros_like(R_GRID)
    K_gu_arr = np.zeros_like(R_GRID)
    for i, R in enumerate(R_GRID):
        E_rhf_arr[i], E_fci_arr[i], E_t_arr[i], _, h_gu_arr[i], K_gu_arr[i] = (
            run_rhf_and_ci(float(R))
        )

    # --- Print energies at the requested bond lengths ------------------
    print("H_2 full-CI toy: 3x3 singlet CI in the STO-3G minimal basis")
    print("  (energies include 1/R nuclear repulsion)")
    print(
        f"  {'R (a_0)':>10s}  {'E_RHF':>12s}  {'E_FCI':>12s}  "
        f"{'E_T':>12s}  {'E_FCI-E_RHF':>14s}  {'<g|h|u>':>10s}"
    )
    for R in R_PRINT:
        i = int(np.argmin(np.abs(R_GRID - R)))
        dE = E_fci_arr[i] - E_rhf_arr[i]
        print(
            f"  {R_GRID[i]:10.2f}  {E_rhf_arr[i]:+12.6f}  "
            f"{E_fci_arr[i]:+12.6f}  {E_t_arr[i]:+12.6f}  "
            f"{dE:+14.6f}  {h_gu_arr[i]:+10.2e}"
        )

    # Sanity: at R = 1.4 the FCI should be slightly below RHF,
    # and the triplet should be well above both.
    i14 = int(np.argmin(np.abs(R_GRID - 1.4)))
    print()
    print("  Equilibrium check at R = 1.4 a_0:")
    print(f"    E_RHF = {E_rhf_arr[i14]:+.6f}  (Szabo-Ostlund table 3.5: -1.117)")
    print(f"    E_FCI = {E_fci_arr[i14]:+.6f}  (FCI in minimal STO-3G: ~ -1.13)")
    print(f"    E_T   = {E_t_arr[i14]:+.6f}  (open-shell triplet)")
    print(
        f"    correlation correction = E_FCI - E_RHF = "
        f"{E_fci_arr[i14] - E_rhf_arr[i14]:+.6f} Ha"
    )
    print(
        f"    Brillouin check: <g | h | u> = {h_gu_arr[i14]:+.2e}  "
        "(should be ~ 0 for HF canonical MOs)"
    )

    # --- Plot ----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5.5))

    palette = ["#cc785c", "#5db8a6", "#e8a55a"]  # coral FCI, teal RHF, amber triplet
    ax.plot(
        R_GRID,
        E_fci_arr,
        color=palette[0],
        linewidth=2.4,
        label=r"FCI  (lowest 3$\times$3 singlet eigenvalue)",
    )
    ax.plot(
        R_GRID,
        E_rhf_arr,
        color=palette[1],
        linewidth=2.0,
        linestyle="-",
        label=r"RHF  ($E[|gg\rangle] = 2h_g + J_{gg}$)",
    )
    ax.plot(
        R_GRID,
        E_t_arr,
        color=palette[2],
        linewidth=2.0,
        linestyle="--",
        label=r"Triplet  ($h_g + h_u + J_{gu} - K_{gu}$)",
    )

    # Mark the equilibrium (minimum of E_FCI)
    i_min = int(np.argmin(E_fci_arr))
    ax.plot(
        R_GRID[i_min],
        E_fci_arr[i_min],
        marker="o",
        markersize=8,
        color=palette[0],
        markeredgecolor="#3d3d3a",
        markeredgewidth=1.0,
        zorder=5,
    )
    ax.annotate(
        rf"FCI min at $R \approx {R_GRID[i_min]:.2f}\,a_0$",
        xy=(R_GRID[i_min], E_fci_arr[i_min]),
        xytext=(R_GRID[i_min] + 0.4, E_fci_arr[i_min] + 0.15),
        fontsize=10,
        color="#3d3d3a",
        arrowprops=dict(arrowstyle="->", color="#3d3d3a", lw=1.0),
    )

    # Reference line: two neutral H atoms (each at -0.5 Ha)
    ax.axhline(
        -1.0,
        color="#a09d96",
        linewidth=0.8,
        linestyle=":",
        alpha=0.7,
        label=r"dissociation limit  $2\,E({\rm H}) = -1\,E_h$",
    )

    ax.set_xlabel(r"$R$  (H–H distance, $a_0$)")
    ax.set_ylabel(r"$E$  (Hartree)")
    ax.set_title(r"H$_2$ full-CI toy: 3$\times$3 singlet CI in STO-3G minimal basis")
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(R_GRID[0], R_GRID[-1])
    ax.set_ylim(-1.3, 0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "03-h2-full-ci-toy.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
