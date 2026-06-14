"""
03-scf-mixing-demo.py
======================
Convergence aids for the Roothaan–Hall SCF.

H2 in STO-3G is too small to exhibit the SCF pathologies that
mixing / DIIS were invented to fix: it is a 2-by-2 problem with a
single occupied orbital, so plain Roothaan–Hall converges
monotonically from any reasonable initial guess.  To show
something interesting we go one step up: a linear H4 chain
(4 H atoms equally spaced at d_HH = 1.4 a_0, on the z-axis) in
STO-3G.  This is a closed-shell singlet with 4 electrons and 4
basis functions; the HOMO/LUMO gap is small enough that plain
Roothaan–Hall struggles from a bad initial guess, and DIIS is
clearly faster.

Three flavours are compared:

  (a)  No mixing — plain Roothaan–Hall.  Each iteration's
       Fock matrix is built from the most recent density and
       diagonalised.  With a deliberately bad initial guess
       plain SCF takes many iterations to settle.

  (b)  Linear (Pulay-style) mixing of the *density*

           P_new  =  (1 - alpha) P_old  +  alpha P_built

       with alpha = 0.5.  Smooth, monotone-ish, but slow:
       linear convergence with rate 1 - alpha for the
       diagonalising eigenvalue.

  (c)  DIIS — Direct Inversion in the Iterative Subspace,
       Pulay 1980 / 1982.  At iteration k we have a history of
       Fock matrices  F_1, …, F_k  and their commutator-error
       vectors  e_i = S P_i F_i - F_i P_i S  (which vanish at
       convergence).  We choose coefficients  c_i  that
       minimise  ||sum c_i e_i||  subject to  sum c_i = 1,
       and use the extrapolated  F_extrap = sum c_i F_i  in
       the next diagonalisation.  Converges *much* faster
       once the history exceeds a couple of entries.

  (d)  Second-order / Newton–Raphson SCF — *not* implemented
       here.  See the chapter §3.8.4 for the algorithm; the
       three traces above already make the pedagogical point.

All three runs start from the *same* deliberately bad initial
density (a random orthogonal rotation of the core-Hamiltonian
orbitals) so the trajectories are directly comparable.

Dependencies: numpy, scipy, matplotlib (Agg).

Run from the repo root:

    python dft_notes/python_codes/chapter_03/03-scf-mixing-demo.py

Writes its plot to:

    dft_notes/python_codes/chapter_03/plots/03-scf-mixing-demo.png
"""

from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")  # headless – no display required
import matplotlib.pyplot as plt


# ─── STO-3G H 1s contraction (same as scripts 01 & 02) ───────────
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D_H = np.array([0.444635, 0.535328, 0.154329])
D_HH = 1.4  # nearest-neighbour H–H distance in the chain
N_ATOMS = 4  # H4 linear chain: 4 atoms, 4 electrons, 4 BFs


# ─── Primitive-Gaussian integrals (same set as script 01) ────────
def boys_f0(t):
    if t < 1.0e-10:
        return 1.0 - t / 3.0 + t * t / 10.0
    return 0.5 * np.sqrt(np.pi / t) * erf(np.sqrt(t))


def norm_s(a):
    return (2.0 * a / np.pi) ** 0.75


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


def build_integrals_chain(n_atoms: int, d: float):
    """STO-3G integrals for a linear H-chain on the z-axis.

    Returns S, h = T + V, ERI, and the nucleus–nucleus repulsion.
    """
    positions = [np.array([0.0, 0.0, i * d]) for i in range(n_atoms)]
    basis = [(ALPHA_H, D_H, R) for R in positions]
    nuclei = [(R, 1.0) for R in positions]
    K = n_atoms

    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    ERI = np.zeros((K, K, K, K))

    for i in range(K):
        ai, di, Ri = basis[i]
        for j in range(K):
            aj, dj, Rj = basis[j]
            rAB2 = float(np.sum((Ri - Rj) ** 2))
            for a, da in zip(ai, di):
                for b, db in zip(aj, dj):
                    nn = norm_s(a) * norm_s(b)
                    S[i, j] += da * db * nn * prim_overlap(a, b, rAB2)
                    T[i, j] += da * db * nn * prim_kinetic(a, b, rAB2)
            for RC, ZC in nuclei:
                for a, da in zip(ai, di):
                    for b, db in zip(aj, dj):
                        P = (a * Ri + b * Rj) / (a + b)
                        nn = norm_s(a) * norm_s(b)
                        V[i, j] += da * db * nn * prim_nuclear(a, b, rAB2, P, RC, ZC)
            for k in range(K):
                ak, dk, Rk = basis[k]
                for l in range(K):
                    al, dl, Rl = basis[l]
                    rCD2 = float(np.sum((Rk - Rl) ** 2))
                    for a, da in zip(ai, di):
                        for b, db in zip(aj, dj):
                            P = (a * Ri + b * Rj) / (a + b)
                            for c, dc in zip(ak, dk):
                                for d, dd_ in zip(al, dl):
                                    Q = (c * Rk + d * Rl) / (c + d)
                                    rPQ2 = float(np.sum((P - Q) ** 2))
                                    nn = norm_s(a) * norm_s(b) * norm_s(c) * norm_s(d)
                                    ERI[i, j, k, l] += (
                                        da
                                        * db
                                        * dc
                                        * dd_
                                        * nn
                                        * prim_eri(a, b, c, d, rAB2, rCD2, rPQ2)
                                    )

    h = T + V
    E_nn = 0.0
    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            E_nn += 1.0 / float(np.linalg.norm(positions[i] - positions[j]))
    return S, h, ERI, E_nn


# ─── Common SCF building blocks ──────────────────────────────────
def build_fock(h, ERI, P):
    """F = h + J - 0.5 K  given the density P."""
    J = np.einsum("pqrs,rs->pq", ERI, P)
    Kx = np.einsum("prqs,rs->pq", ERI, P)
    return h + J - 0.5 * Kx


def density_from_C(C, n_occ):
    return 2.0 * C[:, :n_occ] @ C[:, :n_occ].T


def electronic_energy(P, h, F):
    return 0.5 * float(np.einsum("pq,pq->", P, h + F))


def bad_initial_density(S, h, n_occ, seed=0):
    """A deliberately poor starting density: orthonormal MOs from
    a random orthogonal rotation of the core-Hamiltonian orbitals."""
    _, C0 = eigh(h, S)
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((C0.shape[1], C0.shape[1])))
    C = C0 @ Q
    return density_from_C(C, n_occ)


# ─── (a) Plain Roothaan–Hall ─────────────────────────────────────
def scf_plain(S, h, ERI, P0, n_occ, max_iter=80):
    P = P0.copy()
    history = []
    for it in range(max_iter):
        F = build_fock(h, ERI, P)
        _, C = eigh(F, S)
        P = density_from_C(C, n_occ)
        history.append(electronic_energy(P, h, F))
    return np.array(history)


# ─── (b) Linear mixing of the density ────────────────────────────
def scf_linear(S, h, ERI, P0, n_occ, alpha=0.3, max_iter=80):
    P = P0.copy()
    history = []
    for it in range(max_iter):
        F = build_fock(h, ERI, P)
        _, C = eigh(F, S)
        P_new = density_from_C(C, n_occ)
        history.append(electronic_energy(P_new, h, F))
        # P_{k+1} = (1 - alpha) P_k + alpha P_new
        P = (1.0 - alpha) * P + alpha * P_new
    return np.array(history)


# ─── (c) Pulay DIIS ──────────────────────────────────────────────
def scf_diis(S, h, ERI, P0, n_occ, max_iter=80, n_keep=6, n_warmup=2):
    """Pulay's DIIS.

    For the first `n_warmup` iterations we run plain Roothaan–Hall
    to build up an informative history; from iteration n_warmup+1
    onward we solve the constrained least-squares Pulay equations
    and use the extrapolated Fock matrix.
    """
    P = P0.copy()
    F_hist, e_hist = [], []
    history = []
    for it in range(max_iter):
        F_built = build_fock(h, ERI, P)
        # Commutator error e = S P F - F P S (AO basis)
        e = S @ P @ F_built - F_built @ P @ S

        F_hist.append(F_built.copy())
        e_hist.append(e.copy())
        if len(F_hist) > n_keep:
            F_hist.pop(0)
            e_hist.pop(0)

        if it >= n_warmup and len(F_hist) >= 2:
            n = len(F_hist)
            B = np.zeros((n + 1, n + 1))
            for i in range(n):
                for j in range(n):
                    B[i, j] = float(np.sum(e_hist[i] * e_hist[j]))
            B[n, :n] = -1.0
            B[:n, n] = -1.0
            rhs = np.zeros(n + 1)
            rhs[n] = -1.0
            try:
                c = np.linalg.solve(B, rhs)[:n]
                F_extrap = sum(ci * Fi for ci, Fi in zip(c, F_hist))
            except np.linalg.LinAlgError:
                F_extrap = F_built
        else:
            F_extrap = F_built

        _, C = eigh(F_extrap, S)
        P = density_from_C(C, n_occ)
        history.append(electronic_energy(P, h, F_built))
    return np.array(history)


def main() -> None:
    # ─── Build integrals once; reuse across all three runs ───────
    S, h, ERI, E_nn = build_integrals_chain(N_ATOMS, D_HH)
    K = S.shape[0]
    n_occ = N_ATOMS // 2  # closed-shell singlet: 2 doubly occupied MOs
    print(f"=== H{N_ATOMS} linear chain, d_HH = {D_HH} a_0, STO-3G ===")
    print(f"  basis size K           = {K}")
    print(f"  occupied MOs           = {n_occ}")
    print(f"  nuclear repulsion      = {E_nn:+.6f} E_h")

    # Bad initial guess shared by all three methods
    P0 = bad_initial_density(S, h, n_occ=n_occ, seed=2)

    # Reference: well-converged total electronic energy
    hist_ref = scf_linear(S, h, ERI, P0, n_occ=n_occ, alpha=0.3, max_iter=800)
    E_ref = hist_ref[-1]
    print(f"  reference E_elec       = {E_ref:+.8f} E_h (linear α=0.3, 800 iter)")
    print(f"  reference E_total      = {E_ref + E_nn:+.8f} E_h")

    # ─── Run the three methods ───────────────────────────────────
    n_iter = 60
    hist_plain = scf_plain(S, h, ERI, P0, n_occ=n_occ, max_iter=n_iter)
    hist_lin = scf_linear(S, h, ERI, P0, n_occ=n_occ, alpha=0.5, max_iter=n_iter)
    hist_diis = scf_diis(
        S, h, ERI, P0, n_occ=n_occ, max_iter=n_iter, n_keep=6, n_warmup=2
    )

    def first_below(hist, tol):
        err = np.abs(hist - E_ref)
        idx = np.where(err < tol)[0]
        return int(idx[0]) + 1 if idx.size else None

    print("\n  iterations to reach |E - E_ref| < 1e-6 E_h:")
    rows = [
        ("plain Roothaan–Hall", hist_plain),
        ("linear α=0.5      ", hist_lin),
        ("Pulay DIIS (k=6)  ", hist_diis),
    ]
    n_each = {}
    for name, hist in rows:
        n = first_below(hist, 1e-6)
        n_each[name] = n
        final_err = abs(hist[-1] - E_ref)
        tag = f"converged @ iter {n}" if n is not None else "NOT converged"
        print(f"    {name}: {tag}   (final |dE| = {final_err:.2e})")

    n_plain = n_each["plain Roothaan–Hall"]
    n_diis = n_each["Pulay DIIS (k=6)  "]
    if n_diis is not None and (n_plain is None or n_diis < n_plain):
        print("  ✓ DIIS converged in fewer iterations than plain SCF.")
    else:
        print("  ! note: DIIS did not strictly beat plain SCF on this problem.")

    # ─── Plot |E - E_ref| on a log axis ──────────────────────────
    fig, ax = plt.subplots(figsize=(8, 6))
    palette = {"plain": "#cc785c", "linear": "#e8a55a", "diis": "#5db8a6"}
    FLOOR = 1e-14

    def plot_err(hist, color, label):
        err = np.abs(hist - E_ref)
        err = np.where(err < FLOOR, FLOOR, err)
        ax.semilogy(
            np.arange(1, len(err) + 1),
            err,
            "o-",
            color=color,
            linewidth=2.0,
            markersize=5,
            label=label,
        )

    plot_err(hist_plain, palette["plain"], "(a) no mixing — plain Roothaan–Hall")
    plot_err(hist_lin, palette["linear"], r"(b) linear mixing of $P$,  $\alpha = 0.5$")
    plot_err(hist_diis, palette["diis"], r"(c) Pulay DIIS ($k \leq 6$, 2-iter warmup)")

    ax.axhline(
        1e-6,
        color="#a09d96",
        linewidth=0.8,
        linestyle=":",
        alpha=0.7,
        label=r"$10^{-6}\,E_h$ tolerance",
    )

    ax.set_xlabel("SCF iteration")
    ax.set_ylabel(
        r"$|E_\mathrm{elec}^{(k)} - E_\mathrm{elec}^\mathrm{ref}|$  (Hartree)"
    )
    ax.set_title(
        rf"SCF convergence aids on the H$_{N_ATOMS}$ chain "
        rf"($d_\mathrm{{HH}} = {D_HH}\,a_0$, STO-3G)"
    )
    ax.set_ylim(FLOOR, 5.0)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, loc="upper right")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    here = Path(__file__).parent.resolve()
    plots_dir = here / "plots"
    plots_dir.mkdir(exist_ok=True)
    out = plots_dir / "03-scf-mixing-demo.png"
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
