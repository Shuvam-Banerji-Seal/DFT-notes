"""
01-h2-bond-relaxation.py
========================
Relax the H2 bond length in the STO-3G basis using analytical
Hellmann-Feynman forces and steepest descent.

The script:
  1. Builds the STO-3G basis for H2 at arbitrary bond length R
     (the ch06 integrals are generalised to a single parameter
     R controlling the position of the second hydrogen).
  2. Runs closed-shell HF at five fixed bond lengths
     R = 1.0, 1.2, 1.4, 1.6, 2.0 a_0 and tabulates E(R).
  3. Computes the Hellmann-Feynman force on each nucleus at each R
     by numerical quadrature of the classical Coulomb force
     exerted by the SCF density on each nucleus (plus the
     nuclear-nuclear repulsion).
  4. Computes the true gradient dE/dR by central finite
     differences of E(R), and shows that the Hellmann-Feynman
     forces (on both nuclei) recover this gradient up to the
     Pulay correction.
  5. Uses steepest descent in the 1-D coordinate R to relax
     the bond from R = 2.0 a_0 to the STO-3G minimum, with a
     backtracking line search.
  6. Plots the potential energy curve and the trajectory on a
     single two-panel figure.

Why this script lives in chapter 09:
  - Section 9.10 (worked example) walks through the same
    calculation.  The numbers in the chapter come from this
    script; if they disagree, the script wins.
  - The plot shows the potential well, the gradient, and the
    relaxation trajectory on the same axes.

Dependencies: numpy, scipy (eigh + erf), matplotlib (headless).

Run from the repo root:
    python dft_notes/python_codes/chapter_09/01-h2-bond-relaxation.py

Writes its plot to:
    dft_notes/python_codes/chapter_09/plots/01-h2-bond-relaxation.png
"""

import os
import numpy as np
from scipy.linalg import eigh
from scipy.special import erf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ─── STO-3G parameters for hydrogen (zeta = 1.24) ───────────────
# Canonical EMSL Basis Set Exchange entry; the underlying
# zeta = 1.0 Hehre-Stewart-Pople fit has been scaled by
# zeta^2 = 1.5376 to give the molecular-H exponents.  See
# chapter 06 (00-basis-sets.md) section 6.4 for the origin.
ALPHA_H = np.array([0.168856, 0.623913, 3.425250])
D = np.array([0.444635, 0.535328, 0.154329])

Z_H = 1.0  # nuclear charge


# ─── Primitive integrals (unnormalised s-Gaussians) ──────────────
# Formulas: Szabo & Ostlund, *Modern Quantum Chemistry*, App. A.


def boys_f0(t: float) -> float:
    """Boys function F_0(t) = (1/2) sqrt(pi/t) erf(sqrt(t)).
    Series near t = 0 to avoid 0/0.
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
    """Normalisation constant of a primitive s-Gaussian."""
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
    """Two-electron integral (AB|CD) in chemists' notation."""
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


# ─── HF at a fixed bond length ────────────────────────────────────


def run_hf(R: float):
    """Run closed-shell HF for H2 at bond length R.

    Returns a dict with E_total, E_elec, E_nuc, the AO basis
    arrays, the SCF density matrix P, the MOs C, and the
    orbital energies.
    """
    A = np.array([0.0, 0.0, 0.0])
    B = np.array([0.0, 0.0, R])
    bf = [(ALPHA_H, D, A), (ALPHA_H, D, B)]
    K = 2

    # ─── Overlap, kinetic, nuclear attraction ─────────────────
    S = np.zeros((K, K))
    T = np.zeros((K, K))
    V = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            r2 = float(np.sum((bf[i][2] - bf[j][2]) ** 2))
            S[i, j] = contracted_overlap(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            T[i, j] = contracted_kinetic(bf[i][0], bf[i][1], bf[j][0], bf[j][1], r2)
            for RC, ZC in [(A, Z_H), (B, Z_H)]:
                V[i, j] += contracted_nuclear(
                    bf[i][0], bf[i][1], bf[j][0], bf[j][1], bf[i][2], bf[j][2], RC, ZC
                )
    Hcore = T + V

    # ─── Two-electron integral tensor ─────────────────────────
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

    # ─── SCF loop (closed shell, 2 electrons in 1 occupied MO) ─
    P = np.zeros((K, K))
    E_prev = 0.0
    evals = None
    C = None
    E_elec = None
    for it in range(64):
        J = np.einsum("pqrs,rs->pq", ERI, P)
        Kx = np.einsum("prqs,rs->pq", ERI, P)
        F = Hcore + J - 0.5 * Kx
        evals, C = eigh(F, S)
        P_new = 2.0 * np.outer(C[:, 0], C[:, 0])
        E_elec = 0.5 * float(np.einsum("pq,pq->", P_new, Hcore + F))
        dP = float(np.linalg.norm(P_new - P))
        P, E_prev = P_new, E_elec
        if dP < 1e-10:
            break

    E_nuc = Z_H * Z_H / R
    E_total = E_elec + E_nuc
    return {
        "R": R,
        "A": A,
        "B": B,
        "S": S,
        "Hcore": Hcore,
        "F": F,
        "C": C,
        "P": P,
        "ERI": ERI,
        "evals": evals,
        "E_elec": E_elec,
        "E_nuc": E_nuc,
        "E_total": E_total,
    }


# ─── Hellmann-Feynman force on each nucleus ───────────────────────


def density_on_grid(X, Y, Z, A, B, P):
    """Evaluate the SCF density rho(r) = sum_mu_nu P_munu chi_mu chi_nu
    on a Cartesian grid (X, Y, Z) with the two H atoms at A and B.
    """
    rho = np.zeros_like(X)
    for mu, (R_atom_mu) in enumerate([A, B]):
        r2_mu = (
            (X - R_atom_mu[0]) ** 2 + (Y - R_atom_mu[1]) ** 2 + (Z - R_atom_mu[2]) ** 2
        )
        chi_mu = np.zeros_like(X)
        for d_p, a_p in zip(D, ALPHA_H):
            chi_mu += d_p * norm_s(a_p) * np.exp(-a_p * r2_mu)
        for nu, (R_atom_nu) in enumerate([A, B]):
            r2_nu = (
                (X - R_atom_nu[0]) ** 2
                + (Y - R_atom_nu[1]) ** 2
                + (Z - R_atom_nu[2]) ** 2
            )
            chi_nu = np.zeros_like(X)
            for d_p, a_p in zip(D, ALPHA_H):
                chi_nu += d_p * norm_s(a_p) * np.exp(-a_p * r2_nu)
            rho += P[mu, nu] * chi_mu * chi_nu
    return rho


def hf_force_on_nuclei(R, A, B, P, n_per_axis=50, L=6.0):
    """Compute the Hellmann-Feynman force on each H nucleus.

    F_I = -Z_I * int rho(r) (r - R_I) / |r - R_I|^3 dr
          + Z_I * Z_J * (R_J - R_I) / |R_I - R_J|^3
    (the second term is the nuclear-nuclear repulsion, with the
    sign convention that positive F means "pushed in the
    positive-z direction").

    The grid is centred on the bond midpoint and extends
    L a_0 in each Cartesian direction, with n_per_axis points
    per axis (so n_per_axis^3 grid points in total).  A
    soft-core regularisation r_safe = max(r, 1e-3) is used in
    the 1/r^3 kernel to keep the integral finite at the
    nucleus.
    """
    # Build 3-D grid (Cartesian).
    x = np.linspace(-L, L, n_per_axis)
    y = np.linspace(-L, L, n_per_axis)
    z = np.linspace(-L, L, n_per_axis)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    dV = (x[1] - x[0]) * (y[1] - y[0]) * (z[1] - z[0])

    # Shift grid so the bond midpoint is at the origin in z.
    # This is not strictly necessary but makes the grid
    # allocation symmetric about the molecule.
    Z = Z - 0.5 * R

    rho = density_on_grid(X, Y, Z, A, B, P)

    # Force on A (vector).
    rxA = X - A[0]
    ryA = Y - A[1]
    rzA = Z - A[2]
    rA = np.sqrt(rxA**2 + ryA**2 + rzA**2)
    rA_safe = np.maximum(rA, 1.0e-3)
    F_A_electronic = -Z_H * np.array(
        [
            np.sum(rho * rxA / rA_safe**3) * dV,
            np.sum(rho * ryA / rA_safe**3) * dV,
            np.sum(rho * rzA / rA_safe**3) * dV,
        ]
    )

    # Force on B (vector).
    rxB = X - B[0]
    ryB = Y - B[1]
    rzB = Z - B[2]
    rB = np.sqrt(rxB**2 + ryB**2 + rzB**2)
    rB_safe = np.maximum(rB, 1.0e-3)
    F_B_electronic = -Z_H * np.array(
        [
            np.sum(rho * rxB / rB_safe**3) * dV,
            np.sum(rho * ryB / rB_safe**3) * dV,
            np.sum(rho * rzB / rB_safe**3) * dV,
        ]
    )

    # Nuclear-nuclear repulsion.  The Hellmann-Feynman force on
    # nucleus I is F_I^nuc = +Z_I Z_J (R_I - R_J) / |R_I - R_J|^3
    # (Coulomb's law, in the convention that "force on I from J"
    # points from J to I for like charges, i.e. away from J).
    AB = B - A
    ABmag = np.sqrt(np.sum(AB**2))
    F_A_nuc = Z_H * Z_H * (A - B) / ABmag**3
    F_B_nuc = Z_H * Z_H * (B - A) / ABmag**3

    F_A = F_A_electronic + F_A_nuc
    F_B = F_B_electronic + F_B_nuc
    return F_A, F_B


# ─── Steepest descent in 1-D R ────────────────────────────────────


def steepest_descent_relax(
    R0: float,
    alpha0: float = 0.5,
    E_tol: float = 1.0e-8,
    F_tol: float = 1.0e-5,
    max_steps: int = 64,
):
    """Relax the bond length R from R0 using steepest descent with
    backtracking line search on the central-difference gradient.

    R_new = R_old - alpha_k * dE/dR

    Initial step alpha_0 = alpha0 a_0/E_h.  Halve alpha if the
    energy increases.  Stop when |dE/dR| < F_tol and
    |E_new - E_old| < E_tol.
    """
    R = R0
    traj_R = [R]
    traj_E = [run_hf(R)["E_total"]]
    traj_grad = [None]
    alpha = alpha0

    for step in range(max_steps):
        h = 1.0e-4
        E_plus = run_hf(R + h)["E_total"]
        E_minus = run_hf(R - h)["E_total"]
        dE_dR = (E_plus - E_minus) / (2.0 * h)
        traj_grad[-1] = dE_dR
        if abs(dE_dR) < F_tol and step > 0:
            break

        # Steepest descent step with backtracking.
        E_old = traj_E[-1]
        for _backtrack in range(16):
            R_new = R - alpha * dE_dR
            if R_new < 0.5:  # avoid collapse
                alpha *= 0.5
                continue
            E_new = run_hf(R_new)["E_total"]
            if E_new < E_old:
                break
            alpha *= 0.5
        else:
            # Could not find a downhill step; stop.
            break

        R = R_new
        traj_R.append(R)
        traj_E.append(E_new)
        traj_grad.append(None)
        if abs(E_new - E_old) < E_tol:
            traj_grad[-1] = (E_new - E_old) / (alpha * 1.0)
            break

    # Final gradient at the converged R.
    h = 1.0e-4
    dE_dR_final = (run_hf(R + h)["E_total"] - run_hf(R - h)["E_total"]) / (2.0 * h)
    traj_grad[-1] = dE_dR_final
    return np.array(traj_R), np.array(traj_E), np.array(traj_grad)


# ─── Main ──────────────────────────────────────────────────────────


def main() -> None:
    # ─── 1. Energy curve on a grid of bond lengths ──────────────
    R_grid = np.array([1.0, 1.2, 1.4, 1.6, 2.0])
    E_grid = []
    hf_at_R = []
    for R in R_grid:
        out = run_hf(float(R))
        E_grid.append(out["E_total"])
        hf_at_R.append(out)
    E_grid = np.array(E_grid)

    # ─── 2. Hellmann-Feynman force on each nucleus ──────────────
    print("\n=== Hellmann-Feynman forces on each nucleus ===")
    print("     R (a_0)    F_A^HF (E_h/a_0)    F_B^HF (E_h/a_0)")
    hf_forces = []
    for R, hf in zip(R_grid, hf_at_R):
        F_A, F_B = hf_force_on_nuclei(
            float(R), hf["A"], hf["B"], hf["P"], n_per_axis=40, L=6.0
        )
        hf_forces.append((F_A, F_B))
        print(f"     {R:5.2f}     {F_A[2]:+10.4f}            {F_B[2]:+10.4f}")

    # ─── 3. Central-difference gradient dE/dR ───────────────────
    print("\n=== Gradient dE/dR by central finite differences ===")
    print("     R (a_0)    dE/dR (E_h/a_0)    (F_A^HF - F_B^HF)/2")
    grad_grid = []
    for R, (F_A, F_B) in zip(R_grid, hf_forces):
        h = 1.0e-4
        E_plus = run_hf(float(R + h))["E_total"]
        E_minus = run_hf(float(R - h))["E_total"]
        dE_dR = (E_plus - E_minus) / (2.0 * h)
        grad_grid.append(dE_dR)
        asym = (F_A[2] - F_B[2]) / 2.0
        print(f"     {R:5.2f}     {dE_dR:+10.4f}            {asym:+10.4f}")
    grad_grid = np.array(grad_grid)

    # ─── 4. Dense potential-energy curve (for the plot) ─────────
    R_dense = np.linspace(0.9, 2.5, 41)
    E_dense = np.array([run_hf(float(R))["E_total"] for R in R_dense])

    # ─── 5. Steepest-descent relaxation from R = 2.0 a_0 ────────
    print("\n=== Steepest-descent relaxation starting at R = 2.0 a_0 ===")
    print("     step      R (a_0)        E (E_h)        dE/dR (E_h/a_0)")
    R_traj, E_traj, G_traj = steepest_descent_relax(R0=2.0, alpha0=0.5)
    for k, (R, E, G) in enumerate(zip(R_traj, E_traj, G_traj)):
        g_str = f"{G:+10.4f}" if G is not None else "      ---  "
        print(f"     {k:3d}      {R:8.4f}      {E:+10.6f}      {g_str}")
    R_star = R_traj[-1]
    E_min = E_traj[-1]
    print(
        f"\nConverged bond length R* = {R_star:.4f} a_0  (~ {R_star * 0.529177:.3f} Angstrom)"
    )
    print(f"Minimum energy        E* = {E_min:.6f} E_h")

    # ─── 6. Plot ─────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 1, figsize=(7, 7.5), sharex=True)

    palette = ["#cc785c", "#5db8a6", "#3d3d3a"]
    # Top panel: potential energy curve + relaxation trajectory.
    axes[0].plot(
        R_dense,
        E_dense,
        color=palette[0],
        lw=2.0,
        label=r"$E_\text{HF}(R)$  (STO-3G H$_2$)",
    )
    axes[0].scatter(
        R_traj,
        E_traj,
        color=palette[1],
        s=42,
        zorder=5,
        edgecolor=palette[2],
        linewidth=0.8,
        label=r"Steepest-descent trajectory (from $R = 2.0\,a_0$)",
    )
    axes[0].axvline(
        R_star,
        color=palette[1],
        ls="--",
        lw=0.8,
        alpha=0.6,
        label=rf"Converged $R^\star = {R_star:.3f}\,a_0$",
    )
    axes[0].axhline(
        E_min,
        color=palette[1],
        ls=":",
        lw=0.7,
        alpha=0.4,
    )
    axes[0].set_ylabel(r"$E_\text{HF}(R)$  ($E_h$)")
    axes[0].set_title(
        r"H$_2$ STO-3G geometry relaxation: potential curve and steepest-descent path"
    )
    axes[0].legend(loc="lower left", frameon=False, fontsize=9)
    axes[0].grid(True, alpha=0.2)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # Bottom panel: gradient dE/dR (force on the bond) vs R.
    dE_dR_dense = np.gradient(E_dense, R_dense)
    axes[1].plot(
        R_dense,
        dE_dR_dense,
        color=palette[0],
        lw=2.0,
        label=r"$dE/dR$  (numerical, from $E(R)$)",
    )
    axes[1].axhline(0, color="#a09d96", lw=0.6, alpha=0.5)
    axes[1].axvline(
        R_star,
        color=palette[1],
        ls="--",
        lw=0.8,
        alpha=0.6,
        label=rf"$dE/dR = 0$ at $R^\star = {R_star:.3f}\,a_0$",
    )
    axes[1].set_xlabel(r"$R$  (bond length, $a_0$)")
    axes[1].set_ylabel(r"$dE/dR$  ($E_h / a_0$)")
    axes[1].legend(loc="upper right", frameon=False, fontsize=9)
    axes[1].grid(True, alpha=0.2)
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)

    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-h2-bond-relaxation.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
