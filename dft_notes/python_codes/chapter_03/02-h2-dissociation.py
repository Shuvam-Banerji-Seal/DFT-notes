"""
02-h2-dissociation.py
======================
H2 dissociation curve in the STO-3G basis at the restricted
Hartree–Fock level.  We run the from-scratch SCF of script
01-h2-sto3g-scf.py at a series of internuclear distances
R in [0.4, 6.0] a_0, and plot the total HF energy

    E_HF(R)  =  E_elec(R)  +  Z_A Z_B / R

The curve has the expected behaviour:

  *  A minimum near R_e ≈ 1.346 a_0 with a binding energy
     D_e = 2 E_H - E_HF(R_e) ≈ 0.131 E_h (≈ 3.6 eV).  The two
     reference numbers we use:
         E_H (exact)              = -0.500000 E_h
         E_H (STO-3G, RHF)        = -0.466582 E_h
     so the STO-3G "atomic limit" is -0.93316 E_h, while the
     true 2H atomic limit is -1.0 E_h.

  *  At large R the RHF curve plateaus *above* the correct
     limit  2 E_H = -1.0 E_h.  Restricted HF forces the two
     electrons to share a single doubly-occupied spatial
     orbital  (1 sigma_g),  which is a 50/50 mix of the ionic
     configurations H+H- and H-H+ together with H...H.  The
     ionic admixture costs roughly J - K = U_H / 2 at
     dissociation, so E_RHF(infty) > 2 E_H.  Multi-reference
     methods (CASSCF, FCI in two configurations) recover the
     correct -1.0 E_h limit, and unrestricted HF (UHF) gives
     the right limit at the price of breaking spin symmetry
     past the Coulson–Fischer point.  See Section 3.5 of the
     chapter.

Dependencies: numpy, scipy, matplotlib (Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_03/02-h2-dissociation.py

Writes its plot to:

    dft_notes/python_codes/chapter_03/plots/02-h2-dissociation.png
"""

from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")  # headless – no display required
import matplotlib.pyplot as plt


# ─── STO-3G H 1s contraction (same as script 01) ─────────────────
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D_H = np.array([0.444635, 0.535328, 0.154329])


# ─── Primitive-Gaussian integrals (verbatim from script 01) ──────
def boys_f0(t: float) -> float:
    if t < 1.0e-10:
        return 1.0 - t / 3.0 + t * t / 10.0
    return 0.5 * np.sqrt(np.pi / t) * erf(np.sqrt(t))


def norm_s(alpha: float) -> float:
    return (2.0 * alpha / np.pi) ** 0.75


def prim_overlap(a, b, rAB2):
    p = a + b
    return (np.pi / p) ** 1.5 * np.exp(-a * b / p * rAB2)


def prim_kinetic(a, b, rAB2):
    p = a + b
    return (a * b / p) * (3.0 - 2.0 * a * b / p * rAB2) * prim_overlap(a, b, rAB2)


def prim_nuclear(a, b, rAB2, P, C, ZC):
    p = a + b
    rPC2 = float(np.sum((P - C) ** 2))
    return -2.0 * np.pi * ZC / p * np.exp(-a * b / p * rAB2) * boys_f0(p * rPC2)


def prim_eri(a, b, c, d, rAB2, rCD2, rPQ2):
    p, q = a + b, c + d
    return (
        2.0
        * np.pi**2.5
        / (p * q * np.sqrt(p + q))
        * np.exp(-a * b / p * rAB2)
        * np.exp(-c * d / q * rCD2)
        * boys_f0(p * q / (p + q) * rPQ2)
    )


def build_integrals_h2(R: float):
    """Return (S, h, ERI, E_nn) for H2 with the two H atoms at
    z = 0 and z = R."""
    RA = np.array([0.0, 0.0, 0.0])
    RB = np.array([0.0, 0.0, R])
    basis = [(ALPHA_H, D_H, RA), (ALPHA_H, D_H, RB)]
    nuclei = [(RA, 1.0), (RB, 1.0)]
    K = len(basis)

    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    ERI = np.zeros((K, K, K, K))
    for i in range(K):
        ai, di, Ri = basis[i]
        for j in range(K):
            aj, dj, Rj = basis[j]
            rAB2 = float(np.sum((Ri - Rj) ** 2))
            S_ij = 0.0
            T_ij = 0.0
            for a, da in zip(ai, di):
                for b, db in zip(aj, dj):
                    n = norm_s(a) * norm_s(b)
                    S_ij += da * db * n * prim_overlap(a, b, rAB2)
                    T_ij += da * db * n * prim_kinetic(a, b, rAB2)
            S[i, j] = S_ij
            T[i, j] = T_ij

            V_ij = 0.0
            for RC, ZC in nuclei:
                for a, da in zip(ai, di):
                    for b, db in zip(aj, dj):
                        P = (a * Ri + b * Rj) / (a + b)
                        n = norm_s(a) * norm_s(b)
                        V_ij += da * db * n * prim_nuclear(a, b, rAB2, P, RC, ZC)
            V[i, j] = V_ij

            for k in range(K):
                ak, dk, Rk = basis[k]
                for l in range(K):
                    al, dl, Rl = basis[l]
                    rCD2 = float(np.sum((Rk - Rl) ** 2))
                    val = 0.0
                    for a, da in zip(ai, di):
                        for b, db in zip(aj, dj):
                            P = (a * Ri + b * Rj) / (a + b)
                            for c, dc in zip(ak, dk):
                                for d, dd_ in zip(al, dl):
                                    Q = (c * Rk + d * Rl) / (c + d)
                                    rPQ2 = float(np.sum((P - Q) ** 2))
                                    n = norm_s(a) * norm_s(b) * norm_s(c) * norm_s(d)
                                    val += (
                                        da
                                        * db
                                        * dc
                                        * dd_
                                        * n
                                        * prim_eri(a, b, c, d, rAB2, rCD2, rPQ2)
                                    )
                    ERI[i, j, k, l] = val

    h = T + V
    E_nn = 1.0 * 1.0 / R
    return S, h, ERI, E_nn


def scf_energy(S, h, ERI, n_occ=1, max_iter=128, tol=1e-9):
    """Plain Roothaan–Hall SCF with simple damping (alpha = 0.5)
    so that stretched-geometry runs do not oscillate.  Returns the
    converged electronic energy."""
    K = S.shape[0]
    P = np.zeros((K, K))
    E_prev = 0.0
    E_elec = 0.0
    for it in range(max_iter):
        J = np.einsum("pqrs,rs->pq", ERI, P)
        Kx = np.einsum("prqs,rs->pq", ERI, P)
        F = h + J - 0.5 * Kx
        eps, C = eigh(F, S)
        Cocc = C[:, :n_occ]
        P_new = 2.0 * Cocc @ Cocc.T
        E_elec = 0.5 * float(np.einsum("pq,pq->", P_new, h + F))
        dE = abs(E_elec - E_prev)
        # 50/50 damping for robustness at large R
        P = 0.5 * P + 0.5 * P_new
        E_prev = E_elec
        if dE < tol and float(np.linalg.norm(P_new - P)) < tol:
            break
    return E_elec


def main() -> None:
    # Reference atomic energies in STO-3G and "exact".
    # STO-3G H atom (one basis function) gives  E_atom = -1/2 alpha
    # only after integration; the value is the same  -0.466582  E_h
    # that Szabo & Ostlund quote for H STO-3G.
    E_H_stoG = -0.466582  # H atom in STO-3G
    E_H_exact = -0.5  # exact non-relativistic 1s

    # ─── Scan R ──────────────────────────────────────────────────
    R_vals = np.concatenate(
        [
            np.linspace(0.4, 1.2, 9),
            np.linspace(1.25, 2.0, 16),
            np.linspace(2.1, 4.0, 20),
            np.linspace(4.2, 6.0, 10),
        ]
    )

    E_tot = np.zeros_like(R_vals)
    for i, R in enumerate(R_vals):
        S, h, ERI, E_nn = build_integrals_h2(float(R))
        E_elec = scf_energy(S, h, ERI, n_occ=1)
        E_tot[i] = E_elec + E_nn

    # ─── Equilibrium: parabolic fit around the minimum ───────────
    i_min = int(np.argmin(E_tot))
    lo = max(0, i_min - 3)
    hi = min(len(R_vals), i_min + 4)
    coef = np.polyfit(R_vals[lo:hi], E_tot[lo:hi], 2)  # a x^2 + b x + c
    R_e = -coef[1] / (2.0 * coef[0])
    E_min = np.polyval(coef, R_e)
    D_e_basis = 2.0 * E_H_stoG - E_min  # vs basis-consistent atomic limit
    D_e_exact = 2.0 * E_H_exact - E_min  # vs exact non-relativistic 2 H limit
    D_e = D_e_basis  # value used in the plot annotation

    print("=== H2 / STO-3G RHF dissociation scan ===")
    print(f"  number of R points        : {R_vals.size}")
    print(f"  R range                   : [{R_vals.min():.2f}, {R_vals.max():.2f}] a_0")
    print(
        f"  E_HF at R = 1.4 a_0       = "
        f"{E_tot[int(np.argmin(np.abs(R_vals - 1.4)))]:+.6f} E_h"
        f"   (chapter value -1.117 E_h)"
    )
    print(f"  equilibrium R_e           = {R_e:.4f} a_0")
    print(f"  E_HF at R_e               = {E_min:+.6f} E_h")
    print(
        f"  D_e vs 2 E_H (STO-3G)     = {D_e_basis:+.4f} E_h  "
        f"(basis-consistent binding)"
    )
    print(f"  D_e vs 2 E_H (exact)      = {D_e_exact:+.4f} E_h  (target ≈ +0.13 E_h)")
    print(
        f"  E_HF at R = 6 a_0         = {E_tot[-1]:+.6f} E_h"
        f"  (target 2 E_H = -1.000 / 2*(-0.467) = -0.933 E_h)"
    )

    # ─── Plot ────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 6))
    palette = {"curve": "#cc785c", "mark": "#5db8a6", "ref": "#a09d96"}

    ax.plot(
        R_vals, E_tot, "-", color=palette["curve"], linewidth=2.2, label="RHF / STO-3G"
    )
    ax.plot(
        [R_e],
        [E_min],
        "o",
        color=palette["mark"],
        markersize=10,
        label=rf"$R_e = {R_e:.3f}\,a_0$, $E_\mathrm{{min}} = {E_min:+.4f}\,E_h$",
    )

    # Reference horizontal lines: 2 × STO-3G H atom, and 2 × exact H
    ax.axhline(
        2.0 * E_H_stoG,
        color=palette["ref"],
        linewidth=1.0,
        linestyle="--",
        alpha=0.7,
        label=r"$2\,E_H^\mathrm{STO-3G} = -0.933\,E_h$",
    )
    ax.axhline(
        2.0 * E_H_exact,
        color="#3d3d3a",
        linewidth=1.0,
        linestyle=":",
        alpha=0.7,
        label=r"$2\,E_H^\mathrm{exact} = -1.000\,E_h$",
    )

    # D_e arrow
    ax.annotate(
        "",
        xy=(R_e, E_min),
        xytext=(R_e, 2.0 * E_H_stoG),
        arrowprops=dict(arrowstyle="<->", color="#3d3d3a", lw=1.2),
    )
    ax.text(
        R_e + 0.15,
        0.5 * (E_min + 2.0 * E_H_stoG),
        rf"$D_e \approx {D_e:.3f}\,E_h$",
        fontsize=11,
    )

    ax.set_xlabel(r"internuclear distance  $R$  (a$_0$)")
    ax.set_ylabel(r"total HF energy  $E_\mathrm{HF}(R)$  (Hartree)")
    ax.set_title(r"H$_2$ dissociation curve at RHF/STO-3G")
    ax.legend(frameon=False, loc="lower right")
    ax.grid(True, alpha=0.25)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    here = Path(__file__).parent.resolve()
    plots_dir = here / "plots"
    plots_dir.mkdir(exist_ok=True)
    out = plots_dir / "02-h2-dissociation.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
