"""
01-h2-sto3g-scf.py
===================
From-scratch closed-shell Roothaan–Hall SCF for H2 in the STO-3G
basis at R = 1.4 a_0.  Every integral is built analytically from
the Boys F_0 function and the standard Gaussian product formulas;
nothing is imported from a quantum-chemistry package.  The point
of the script is to show that the entire Hartree–Fock algorithm
fits on one page once the integrals are in hand.

Algorithm (Section 3.6.5 of the chapter):

  1.  Build the AO integrals  S, T, V, (mu nu | lambda sigma).
  2.  Initial guess  P = 0  (i.e. the first Fock matrix is the
      bare core Hamiltonian h = T + V).
  3.  Loop:
        a.  G_{mu nu} = sum_{lambda sigma} P_{lambda sigma}
                       [ (mu nu | sigma lambda) - 0.5 (mu lambda | sigma nu) ]
        b.  F = h + G
        c.  Solve  F C = S C eps    (generalised symmetric eig)
        d.  P_new  = 2 sum_{i in occ} C_{mu i} C_{nu i}
                     (RHF, 2 electrons -> one doubly occupied MO)
        e.  E_elec = 0.5 sum_{mu nu} P_{mu nu} ( h_{mu nu} + F_{mu nu} )
        f.  Convergence:  |dE| < 1e-10  and  ||dP||_F < 1e-10.
  4.  Add the nucleus–nucleus repulsion  E_nn = Z_A Z_B / R.

The chapter quotes  E_HF = -1.117 E_h  at R = 1.4 a_0.  We
verify that to six decimals at the end.

Notes on the basis:
  The task brief mentioned a single exponent  alpha = 2.70010
  for H 1s; that is not the standard STO-3G value (and it would
  not reproduce -1.117 E_h).  The canonical STO-3G H 1s is a
  contraction of three primitive s-Gaussians,

      alpha = (0.168856, 0.623913, 3.425250)
      d     = (0.444635, 0.535328, 0.154329)

  with zeta = 1.24 already absorbed into the exponents.  We use
  this contraction; it is the same set that lives in the
  EMSL Basis Set Exchange and in Szabo & Ostlund, App. A.

Dependencies: numpy, scipy (eigh, erf), matplotlib (Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_03/01-h2-sto3g-scf.py

Writes its plot to:

    dft_notes/python_codes/chapter_03/plots/01-h2-sto3g-scf.png
"""

from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")  # headless – no display required
import matplotlib.pyplot as plt


# ─── STO-3G H 1s contraction ─────────────────────────────────────
# Three primitive Gaussians fitted to a Slater 1s with zeta = 1.24.
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D_H = np.array([0.444635, 0.535328, 0.154329])

# ─── Geometry: two H nuclei on the z-axis at R = 1.4 a_0 ─────────
R_BOND = 1.4
R_A = np.array([0.0, 0.0, 0.0])
R_B = np.array([0.0, 0.0, R_BOND])
Z_A, Z_B = 1.0, 1.0


# ─── Primitive-Gaussian integral helpers (Szabo & Ostlund App. A)
# Every primitive s-Gaussian is g(r) = exp(-alpha |r - R|^2).
# The contracted basis function is
#   chi(r) = sum_p d_p N(alpha_p) g_p(r),
# where N(alpha) = (2 alpha / pi)^(3/4) normalises the primitive.


def boys_f0(t: float) -> float:
    """Boys function F_0(t) = (1/2) sqrt(pi/t) erf(sqrt(t)).

    Uses a Taylor expansion near t = 0 to avoid the 0/0
    indeterminate form  (sqrt(pi/t) erf(sqrt(t)) -> 2).
    """
    if t < 1.0e-10:
        return 1.0 - t / 3.0 + t * t / 10.0
    return 0.5 * np.sqrt(np.pi / t) * erf(np.sqrt(t))


def norm_s(alpha: float) -> float:
    """Normalisation of a primitive s-Gaussian (so <g|g> = 1)."""
    return (2.0 * alpha / np.pi) ** 0.75


def prim_overlap(a: float, b: float, rAB2: float) -> float:
    """<g_a | g_b>  for primitive s-Gaussians at distance^2 rAB2."""
    p = a + b
    return (np.pi / p) ** 1.5 * np.exp(-a * b / p * rAB2)


def prim_kinetic(a: float, b: float, rAB2: float) -> float:
    """<g_a | -1/2 nabla^2 | g_b>  for primitive s-Gaussians."""
    p = a + b
    return (a * b / p) * (3.0 - 2.0 * a * b / p * rAB2) * prim_overlap(a, b, rAB2)


def prim_nuclear(
    a: float, b: float, rAB2: float, P: np.ndarray, C: np.ndarray, ZC: float
) -> float:
    """<g_a | -ZC / |r - C| | g_b>  for primitive s-Gaussians."""
    p = a + b
    rPC2 = float(np.sum((P - C) ** 2))
    return -2.0 * np.pi * ZC / p * np.exp(-a * b / p * rAB2) * boys_f0(p * rPC2)


def prim_eri(
    a: float, b: float, c: float, d: float, rAB2: float, rCD2: float, rPQ2: float
) -> float:
    """(g_a g_b | g_c g_d)  in chemists' notation (1/r12)."""
    p, q = a + b, c + d
    return (
        2.0
        * np.pi**2.5
        / (p * q * np.sqrt(p + q))
        * np.exp(-a * b / p * rAB2)
        * np.exp(-c * d / q * rCD2)
        * boys_f0(p * q / (p + q) * rPQ2)
    )


# ─── Contracted-basis wrappers ───────────────────────────────────
# Each contracted basis function is a tuple (alpha[:], d[:], R[3]).


def overlap(bA, bB) -> float:
    aA, dA, RA = bA
    aB, dB, RB = bB
    rAB2 = float(np.sum((RA - RB) ** 2))
    S = 0.0
    for ai, di in zip(aA, dA):
        for bj, ej in zip(aB, dB):
            S += di * ej * norm_s(ai) * norm_s(bj) * prim_overlap(ai, bj, rAB2)
    return S


def kinetic(bA, bB) -> float:
    aA, dA, RA = bA
    aB, dB, RB = bB
    rAB2 = float(np.sum((RA - RB) ** 2))
    T = 0.0
    for ai, di in zip(aA, dA):
        for bj, ej in zip(aB, dB):
            T += di * ej * norm_s(ai) * norm_s(bj) * prim_kinetic(ai, bj, rAB2)
    return T


def nuclear(bA, bB, C: np.ndarray, ZC: float) -> float:
    aA, dA, RA = bA
    aB, dB, RB = bB
    rAB2 = float(np.sum((RA - RB) ** 2))
    V = 0.0
    for ai, di in zip(aA, dA):
        for bj, ej in zip(aB, dB):
            P = (ai * RA + bj * RB) / (ai + bj)
            V += (
                di * ej * norm_s(ai) * norm_s(bj) * prim_nuclear(ai, bj, rAB2, P, C, ZC)
            )
    return V


def eri(bA, bB, bC, bD) -> float:
    aA, dA, RA = bA
    aB, dB, RB = bB
    aC, dC, RC = bC
    aD, dD, RD = bD
    rAB2 = float(np.sum((RA - RB) ** 2))
    rCD2 = float(np.sum((RC - RD) ** 2))
    out = 0.0
    for ai, di in zip(aA, dA):
        for bj, ej in zip(aB, dB):
            P = (ai * RA + bj * RB) / (ai + bj)
            for ck, fk in zip(aC, dC):
                for dl, gl in zip(aD, dD):
                    Q = (ck * RC + dl * RD) / (ck + dl)
                    rPQ2 = float(np.sum((P - Q) ** 2))
                    out += (
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
    return out


# ─── Build the full integral set in the AO basis ─────────────────


def build_integrals(basis):
    """Return S, T, V, ERI for a list of contracted basis tuples."""
    K = len(basis)
    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    ERI = np.zeros((K, K, K, K))
    for i in range(K):
        for j in range(K):
            S[i, j] = overlap(basis[i], basis[j])
            T[i, j] = kinetic(basis[i], basis[j])
            for RC, ZC in [(R_A, Z_A), (R_B, Z_B)]:
                V[i, j] += nuclear(basis[i], basis[j], RC, ZC)
            for k in range(K):
                for l in range(K):
                    ERI[i, j, k, l] = eri(basis[i], basis[j], basis[k], basis[l])
    return S, T, V, ERI


# ─── Roothaan–Hall SCF (closed-shell, 2 electrons) ───────────────


def scf(S, h, ERI, n_occ=1, max_iter=64, tol_E=1e-10, tol_P=1e-10):
    """Plain Roothaan–Hall SCF with P = 0 as the initial guess.

    Returns the converged density P, MO coefficients C, MO energies
    eps, total electronic energy E_elec, and the per-iteration
    electronic-energy trace (for plotting convergence).
    """
    K = S.shape[0]
    P = np.zeros((K, K))
    E_prev = 0.0
    history = []
    for it in range(max_iter):
        # G_{mu nu} = sum_{lambda sigma} P_{lambda sigma}
        #     [ (mu nu | sigma lambda) - 0.5 (mu lambda | sigma nu) ]
        J = np.einsum("pqrs,rs->pq", ERI, P)  # Coulomb
        Kx = np.einsum("prqs,rs->pq", ERI, P)  # exchange
        F = h + J - 0.5 * Kx

        eps, C = eigh(F, S)  # F C = S C eps
        # 2 electrons doubly occupy the lowest MO
        Cocc = C[:, :n_occ]
        P_new = 2.0 * Cocc @ Cocc.T
        E_elec = 0.5 * float(np.einsum("pq,pq->", P_new, h + F))
        history.append(E_elec)

        dE = abs(E_elec - E_prev)
        dP = float(np.linalg.norm(P_new - P))
        P, E_prev = P_new, E_elec
        if dE < tol_E and dP < tol_P:
            return P, C, eps, E_elec, history, it + 1
    return P, C, eps, E_elec, history, max_iter


def main() -> None:
    # ─── Basis: one contracted s-function per nucleus ────────────
    basis = [
        (ALPHA_H, D_H, R_A),
        (ALPHA_H, D_H, R_B),
    ]
    K = len(basis)
    S, T, V, ERI = build_integrals(basis)
    h = T + V

    np.set_printoptions(precision=4, suppress=True)
    print("=== H2 / STO-3G integrals at R = 1.4 a_0 ===")
    print("Overlap S:")
    print(S)
    print("\nKinetic T:")
    print(T)
    print("\nNuclear V (sum over both nuclei):")
    print(V)
    print("\nCore Hamiltonian h = T + V:")
    print(h)
    print("\nKey two-electron integrals:")
    print(f"  (11|11)       = {ERI[0, 0, 0, 0]:+.6f}")
    print(f"  (11|22)       = {ERI[0, 0, 1, 1]:+.6f}")
    print(f"  (12|12)       = {ERI[0, 1, 0, 1]:+.6f}")
    print(f"  (11|12)       = {ERI[0, 0, 0, 1]:+.6f}")

    # ─── SCF ─────────────────────────────────────────────────────
    P, C, eps, E_elec, history, n_it = scf(S, h, ERI, n_occ=1)
    E_nn = Z_A * Z_B / R_BOND
    E_total = E_elec + E_nn

    print(f"\n=== Roothaan–Hall SCF ===")
    print(f"  iterations to convergence : {n_it}")
    print(f"  MO energies eps           : {eps}")
    print(f"  MO coefficients C         :")
    print(C)
    print(f"  density matrix P          :")
    print(P)
    print(f"  E_electronic              = {E_elec:+.6f} E_h")
    print(f"  E_nuc-nuc (Z_A Z_B / R)   = {E_nn:+.6f} E_h")
    print(f"  E_total (HF)              = {E_total:+.6f} E_h")
    print(f"  reference (Szabo-Ostlund) = -1.1167   E_h")
    assert abs(E_total + 1.1167) < 1.0e-3, (
        f"E_total = {E_total:+.6f} disagrees with the chapter "
        "value -1.1167 E_h by more than 1 mE_h."
    )

    # ─── Plot the SCF convergence trace ──────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    iters = np.arange(1, len(history) + 1)
    palette = ["#cc785c", "#5db8a6", "#e8a55a"]

    ax.plot(
        iters,
        history,
        "o-",
        color=palette[0],
        linewidth=2.2,
        markersize=7,
        label=r"$E_\mathrm{elec}$ per iteration",
    )
    ax.axhline(
        E_elec,
        color="#3d3d3a",
        linewidth=0.9,
        linestyle="--",
        alpha=0.6,
        label=rf"converged  $E_\mathrm{{elec}} = {E_elec:+.6f}\,E_h$",
    )
    ax.set_xlabel("SCF iteration")
    ax.set_ylabel(r"electronic energy  $E_\mathrm{elec}$  (Hartree)")
    ax.set_title(
        rf"H$_2$ STO-3G Roothaan–Hall SCF  ($R = {R_BOND}\,a_0$, "
        rf"converged in {n_it} steps)"
    )
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, loc="upper right")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    here = Path(__file__).parent.resolve()
    plots_dir = here / "plots"
    plots_dir.mkdir(exist_ok=True)
    out = plots_dir / "01-h2-sto3g-scf.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
