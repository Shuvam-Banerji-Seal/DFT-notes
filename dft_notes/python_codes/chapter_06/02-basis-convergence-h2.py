"""
02-basis-convergence-h2.py
==========================
Basis-set convergence of the Hartree-Fock energy of H2 at
R = 1.4 a_0, computed from scratch with the same primitive-
Gaussian machinery as 01-sto-3g-h2.py.

We run a closed-shell RHF SCF in seven s-only basis sets of
increasing size, all built from the textbook exponents and
contraction coefficients (EMSL Basis Set Exchange):

    Basis     K (bf for H2)   structure per H
    -------   -------------   ------------------------------
    STO-3G          2          1 CGTO from 3 prims
    3-21G           4          2 CGTOs (2 + 1) prims
    6-31G           4          2 CGTOs (3 + 1) prims
    6-311G          6          3 CGTOs (3 + 1 + 1) prims
    cc-pVDZ         4          2 CGTOs (s-only)
    cc-pVTZ         6          3 CGTOs (s-only)
    cc-pVQZ         8          4 CGTOs (s-only)

Polarisation (p on H for cc-pVDZ, p+d for cc-pVTZ, ...) is
*not* included: the goal here is the radial convergence of
the s-channel.  The chapter (section 6.6) discusses
polarisation separately.

Two extrapolations are computed:

  - Helgaker-style power-law in the number of basis functions
        E(K) = E_CBS + A / K**3                            (1)
    fitted to the three largest sets.  The user asked for K
    (total bf count), not the cardinal number.

  - Dunning-style two-point extrapolation on the cc-pVXZ
    family using the cardinal number X = 2, 3, 4:
        E(X) = E_CBS + B / X**3                            (2)
    fitted to (cc-pVTZ, cc-pVQZ) and to (cc-pVDZ, cc-pVTZ,
    cc-pVQZ) by least squares.

The accepted HF/CBS reference for H2 at R = 1.4 a_0 is
E_HF^CBS ~= -1.1336 E_h (Kolos & Roothaan 1960; modern
near-exact HF treatments).  We report how close each basis
gets and how the extrapolations compare.

Run from the repo root:
    python dft_notes/python_codes/chapter_06/02-basis-convergence-h2.py

Writes its plot to:
    dft_notes/python_codes/chapter_06/plots/02-basis-convergence-h2.png

Dependencies: numpy, scipy (eigh + erf), matplotlib (headless).
"""

import os
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")  # headless — no display required
import matplotlib.pyplot as plt


# ─── Geometry: two H atoms on the z-axis at R = 1.4 a_0 ───────────
R_BOND = 1.4
A_POS = np.array([0.0, 0.0, 0.0])
B_POS = np.array([0.0, 0.0, R_BOND])
Z_A, Z_B = 1.0, 1.0
E_HF_CBS_REF = -1.13363  # accepted near-CBS HF energy of H2 at 1.4 a_0


# ─── Basis-set library (s-only, EMSL values) ──────────────────────
# Each entry is the list of contractions for *one* hydrogen.  A
# contraction is (exps, coefs); the basis for H2 is two copies of
# the same list, one per atom.
H_BASES = {
    "STO-3G": [
        # 1s (HSP 1969, zeta = 1.24)
        ([0.168856, 0.623913, 3.425250], [0.444635, 0.535328, 0.154329]),
    ],
    "3-21G": [
        # inner 1s (2 prims)
        ([5.4471780, 0.8245470], [0.1562850, 0.9046910]),
        # outer 1s' (1 prim, uncontracted)
        ([0.1831920], [1.0]),
    ],
    "6-31G": [
        # inner 1s (3 prims)
        ([18.7311370, 2.8253944, 0.6401217], [0.0334946, 0.2347269, 0.8137573]),
        # outer 1s' (1 prim)
        ([0.1612778], [1.0]),
    ],
    "6-311G": [
        # inner 1s (3 prims)
        ([33.8650000, 5.0947900, 1.1587900], [0.0254938, 0.1903730, 0.8521610]),
        # middle 1s' (1 prim)
        ([0.3258400], [1.0]),
        # outer 1s'' (1 prim)
        ([0.1027410], [1.0]),
    ],
    "cc-pVDZ": [
        # 1s : general contraction over the 4 s-primitives
        (
            [13.0100000, 1.9620000, 0.4446000, 0.1220000],
            [0.0196850, 0.1379770, 0.4781480, 0.5012400],
        ),
        # 2s : diffuse primitive uncontracted
        ([0.1220000], [1.0]),
    ],
    "cc-pVTZ": [
        # 1s : general contraction over 5 s-primitives
        (
            [33.8700000, 5.0950000, 1.1590000, 0.3258000, 0.1027000],
            [0.0060680, 0.0453080, 0.2028220, 0.5039030, 0.3834210],
        ),
        # 2s : single uncontracted primitive
        ([0.3258000], [1.0]),
        # 3s : single uncontracted primitive
        ([0.1027000], [1.0]),
    ],
    "cc-pVQZ": [
        # 1s : general contraction over 6 s-primitives
        (
            [82.6400000, 12.4100000, 2.8240000, 0.7977000, 0.2581000, 0.0898900],
            [0.0020060, 0.0153430, 0.0755790, 0.2567500, 0.4978490, 0.2960770],
        ),
        # 2s, 3s, 4s : single uncontracted primitives
        ([0.7977000], [1.0]),
        ([0.2581000], [1.0]),
        ([0.0898900], [1.0]),
    ],
}

# Order in which we run / display the basis sets.
BASIS_ORDER = ["STO-3G", "3-21G", "6-31G", "6-311G", "cc-pVDZ", "cc-pVTZ", "cc-pVQZ"]

# Cardinal number for the Dunning family (used only for cc-pVXZ).
CARDINAL = {"cc-pVDZ": 2, "cc-pVTZ": 3, "cc-pVQZ": 4}


# ─── Primitive integrals (unnormalised s-Gaussians) ──────────────
# Same formulas as 01-sto-3g-h2.py (Szabo & Ostlund App. A).


def boys_f0(t: float) -> float:
    """Boys function F_0(t) = (1/2) sqrt(pi/t) erf(sqrt(t))."""
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
    """Normalisation constant of a primitive s-Gaussian."""
    return (2.0 * a / np.pi) ** 0.75


# ─── Contracted-basis wrappers ────────────────────────────────────
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


def contracted_nuclear(
    alpha, d_c, beta, e_c, A: np.ndarray, B: np.ndarray, C: np.ndarray, ZC: float
):
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


# ─── Build a basis for H2 from a per-H contraction list ───────────
def build_h2_basis(h_contractions):
    """Return a list of basis functions (alpha, coefs, centre)
    by replicating the per-H contraction list on both atoms."""
    bf = []
    for centre in (A_POS, B_POS):
        for exps, coefs in h_contractions:
            bf.append(
                (np.asarray(exps, dtype=float), np.asarray(coefs, dtype=float), centre)
            )
    return bf


# ─── RHF SCF in a generic s-only basis ────────────────────────────
def rhf_energy(bf, nuclei, verbose=False, max_iter=128, tol=1e-10):
    """Run RHF for 2 electrons in the closed-shell ground state.

    bf       : list of (alpha, coefs, centre) tuples
    nuclei   : list of (R, Z) tuples
    Returns  : E_total (E_h), E_elec, occupied-MO eigenvalue.
    """
    K = len(bf)
    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            r2 = float(np.sum((bf[i][2] - bf[j][2]) ** 2))
            S[i, j] = contracted_overlap(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            T[i, j] = contracted_kinetic(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            for RC, ZC in nuclei:
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

    # SCF iteration ------------------------------------------------
    P = np.zeros((K, K))
    E_prev = 0.0
    converged = False
    for it in range(max_iter):
        J = np.einsum("pqrs,rs->pq", ERI, P)
        Kx = np.einsum("prqs,rs->pq", ERI, P)
        F = Hcore + J - 0.5 * Kx
        evals, C = eigh(F, S)
        # closed shell: 2 electrons in the lowest MO
        P_new = 2.0 * np.outer(C[:, 0], C[:, 0])
        E_elec = 0.5 * float(np.einsum("pq,pq->", P_new, Hcore + F))
        dE = abs(E_elec - E_prev)
        dP = float(np.linalg.norm(P_new - P))
        P, E_prev = P_new, E_elec
        if dE < tol and dP < tol:
            converged = True
            break

    E_nuc = sum(
        Zi * Zj / np.linalg.norm(Ri - Rj)
        for i_, (Ri, Zi) in enumerate(nuclei)
        for j_, (Rj, Zj) in enumerate(nuclei)
        if j_ > i_
    )
    E_total = E_elec + E_nuc
    if verbose:
        status = "OK" if converged else "NOT CONVERGED"
        print(
            f"    SCF {status} in {it + 1} iters, "
            f"e_HOMO = {evals[0]:+.6f}, E_tot = {E_total:+.6f}"
        )
    return E_total, E_elec, evals[0], converged


# ─── Extrapolation helpers ────────────────────────────────────────
def fit_helgaker_K(Ks, Es):
    """Least-squares fit E(K) = E_CBS + A / K**3.

    With x = 1/K**3 the fit is linear: E = E_CBS + A x.
    Returns (E_CBS, A)."""
    x = 1.0 / np.asarray(Ks, dtype=float) ** 3
    y = np.asarray(Es, dtype=float)
    A_mat = np.vstack([np.ones_like(x), x]).T
    coefs, *_ = np.linalg.lstsq(A_mat, y, rcond=None)
    return float(coefs[0]), float(coefs[1])


def dunning_two_point(X1, E1, X2, E2):
    """Closed-form two-point extrapolation E(X) = E_CBS + B/X**3."""
    B = (E2 - E1) / (1.0 / X2**3 - 1.0 / X1**3)
    E_CBS = E1 - B / X1**3
    return E_CBS, B


def main() -> None:
    nuclei = [(A_POS, Z_A), (B_POS, Z_B)]

    # ─── Run every basis set ──────────────────────────────────────
    results = []  # list of (name, K, E_tot)
    print(f"\nH2 RHF energies at R = {R_BOND} a_0")
    print(
        f"{'basis':<10s} {'K':>3s}   {'E_tot (E_h)':>13s}   "
        f"{'e_HOMO (E_h)':>13s}   conv"
    )
    print("-" * 60)
    for name in BASIS_ORDER:
        bf = build_h2_basis(H_BASES[name])
        K = len(bf)
        E_tot, E_el, e_homo, ok = rhf_energy(bf, nuclei)
        results.append((name, K, E_tot))
        print(
            f"{name:<10s} {K:>3d}   {E_tot:>+13.6f}   "
            f"{e_homo:>+13.6f}   {'yes' if ok else 'NO'}"
        )

    # ─── Helgaker-style fit in K (uses all 7 points) ──────────────
    Ks_all = [r[1] for r in results]
    Es_all = [r[2] for r in results]
    # Use the three largest (6-311G, cc-pVTZ, cc-pVQZ) — small-K
    # points pollute a 1/K**3 law because their underlying angular
    # composition is wrong.  Sort by K then pick the three top.
    sorted_pairs = sorted(zip(Ks_all, Es_all))
    top3_K = [p[0] for p in sorted_pairs[-3:]]
    top3_E = [p[1] for p in sorted_pairs[-3:]]
    E_cbs_K, A_K = fit_helgaker_K(top3_K, top3_E)

    # ─── Dunning extrapolations on cc-pVXZ ────────────────────────
    cc = [(CARDINAL[r[0]], r[2]) for r in results if r[0] in CARDINAL]
    cc.sort()  # by X
    X_vals = np.array([p[0] for p in cc], dtype=float)
    E_cc = np.array([p[1] for p in cc])
    # Two-point (T,Q)
    E_cbs_TQ, B_TQ = dunning_two_point(X_vals[1], E_cc[1], X_vals[2], E_cc[2])
    # Three-point (D,T,Q) LSQ in 1/X**3
    x_cc = 1.0 / X_vals**3
    Amat = np.vstack([np.ones_like(x_cc), x_cc]).T
    coefs, *_ = np.linalg.lstsq(Amat, E_cc, rcond=None)
    E_cbs_DTQ, B_DTQ = float(coefs[0]), float(coefs[1])

    print()
    print("Extrapolations to the complete-basis-set HF limit:")
    print(f"  Helgaker 1/K^3 (top three K = {top3_K})")
    print(f"      E_CBS = {E_cbs_K:+.6f} E_h   (A = {A_K:+.4f})")
    print(f"  Dunning 1/X^3, two-point  (cc-pVTZ, cc-pVQZ)")
    print(f"      E_CBS = {E_cbs_TQ:+.6f} E_h   (B = {B_TQ:+.4f})")
    print(f"  Dunning 1/X^3, three-pt   (cc-pVDZ, cc-pVTZ, cc-pVQZ)")
    print(f"      E_CBS = {E_cbs_DTQ:+.6f} E_h   (B = {B_DTQ:+.4f})")
    print(f"  Reference HF/CBS for H2 (literature)")
    print(f"      E_CBS = {E_HF_CBS_REF:+.6f} E_h")

    # ─── Plot 1: E_HF vs K with 1/K^3 fit ─────────────────────────
    palette = {
        "pople": "#cc785c",  # coral
        "dunning": "#5db8a6",  # teal
        "fit": "#d4a72c",  # amber
        "ref": "#3d3d3a",  # ink
    }
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.0))

    ax = axes[0]
    pople_names = {"STO-3G", "3-21G", "6-31G", "6-311G"}
    for name, K, E in results:
        col = palette["pople"] if name in pople_names else palette["dunning"]
        marker = "o" if name in pople_names else "s"
        ax.plot(
            K,
            E,
            marker=marker,
            color=col,
            markersize=10,
            markeredgecolor="white",
            markeredgewidth=1.3,
            linestyle="none",
            zorder=4,
        )
        ax.annotate(
            name,
            xy=(K, E),
            xytext=(7, 4),
            textcoords="offset points",
            fontsize=9,
            color=col,
        )
    Kgrid = np.linspace(min(Ks_all) - 0.2, max(Ks_all) + 1.2, 200)
    ax.plot(
        Kgrid,
        E_cbs_K + A_K / Kgrid**3,
        color=palette["fit"],
        lw=1.6,
        ls="--",
        label=rf"$E(K) = E_{{\rm CBS}} + A/K^3$ (top 3)",
    )
    ax.axhline(
        E_cbs_K,
        color=palette["fit"],
        lw=0.8,
        ls=":",
        alpha=0.7,
        label=rf"$E_{{\rm CBS}}^{{1/K^3}} = {E_cbs_K:+.4f}$",
    )
    ax.axhline(
        E_HF_CBS_REF,
        color=palette["ref"],
        lw=0.8,
        ls="-.",
        alpha=0.8,
        label=rf"$E_{{\rm HF}}^{{\rm CBS}} \approx {E_HF_CBS_REF:+.4f}$ (lit.)",
    )
    # legend entries for marker shapes
    ax.plot(
        [],
        [],
        "o",
        color=palette["pople"],
        markeredgecolor="white",
        markeredgewidth=1.3,
        markersize=9,
        label="Pople sets",
    )
    ax.plot(
        [],
        [],
        "s",
        color=palette["dunning"],
        markeredgecolor="white",
        markeredgewidth=1.3,
        markersize=9,
        label="Dunning cc-pV$X$Z (s-only)",
    )
    ax.set_xlabel(r"Number of basis functions for H$_2$,  $K$")
    ax.set_ylabel(r"$E_{\rm HF}$  (E$_h$)")
    ax.set_title(r"(a)  $E_{\rm HF}$ versus $K$, Helgaker $1/K^3$ fit")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)
    ax.set_xlim(min(Ks_all) - 0.6, max(Ks_all) + 1.2)

    # ─── Plot 2: E vs cardinal X with Dunning extrap. ─────────────
    ax = axes[1]
    Xgrid = np.linspace(1.6, 6.5, 200)
    ax.plot(
        X_vals,
        E_cc,
        "s",
        color=palette["dunning"],
        markersize=11,
        markeredgecolor="white",
        markeredgewidth=1.3,
        zorder=4,
        label=r"cc-pV$X$Z (s-only)",
    )
    for Xi, Ei, nm in zip(X_vals, E_cc, ["cc-pVDZ", "cc-pVTZ", "cc-pVQZ"]):
        ax.annotate(
            nm,
            xy=(Xi, Ei),
            xytext=(7, 4),
            textcoords="offset points",
            fontsize=9,
            color=palette["dunning"],
        )
    ax.plot(
        Xgrid,
        E_cbs_TQ + B_TQ / Xgrid**3,
        color=palette["fit"],
        lw=1.6,
        ls="--",
        label=rf"$E_{{\rm CBS}}^{{TQ}} = {E_cbs_TQ:+.4f}$ (two-pt)",
    )
    ax.plot(
        Xgrid,
        E_cbs_DTQ + B_DTQ / Xgrid**3,
        color="#5784ba",
        lw=1.4,
        ls=":",
        label=rf"$E_{{\rm CBS}}^{{DTQ}} = {E_cbs_DTQ:+.4f}$ (three-pt)",
    )
    ax.axhline(
        E_HF_CBS_REF,
        color=palette["ref"],
        lw=0.8,
        ls="-.",
        alpha=0.8,
        label=rf"$E_{{\rm HF}}^{{\rm CBS}} \approx {E_HF_CBS_REF:+.4f}$ (lit.)",
    )
    ax.set_xlabel(r"Cardinal number  $X$  (D=2, T=3, Q=4)")
    ax.set_ylabel(r"$E_{\rm HF}$  (E$_h$)")
    ax.set_title(r"(b)  cc-pV$X$Z series, Dunning $1/X^3$ extrapolation")
    ax.grid(True, alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", fontsize=8.5, frameon=False)
    ax.set_xticks([2, 3, 4, 5, 6])
    ax.set_xlim(1.7, 6.3)

    fig.suptitle(
        r"H$_2$ Hartree–Fock convergence with basis-set size, "
        rf"$R = {R_BOND}\,a_0$",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "02-basis-convergence-h2.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
