"""
dft_notes/python_codes/chapter_04/01-diis-scf.py

DIIS SCF on a 2x2 Kohn-Sham toy Hamiltonian.  Compares linear
mixing, Pulay's DIIS, and Broyden's method (good Broyden).

Run from the repo root:
    python dft_notes/python_codes/chapter_04/01-diis-scf.py

Output:
    plots/01-diis-scf.png   convergence plot (energy vs iter)
"""

import os
import numpy as np
import scipy.linalg
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# Toy model
# -------------------------------------------------------------------------
H_core = np.array([[-1.0, -0.5], [-0.5, -1.0]])
S = np.eye(2)
ALPHA = 0.3  # XC coupling (toy)
MIX = 0.5  # linear mixing parameter
TOL = 1e-10
N_OCC = 1  # one doubly-occupied MO


def v_xc(P):
    """Spin-paired toy XC: diagonal in the basis, linear in diag(P)."""
    return ALPHA * np.diag(np.diag(P))


def ks_step(P):
    """One KS step.  Returns P_new, residual, energy."""
    F = H_core + v_xc(P)
    eps, C = scipy.linalg.eigh(F, S)
    Cocc = C[:, :N_OCC]
    P_new = 2.0 * Cocc @ Cocc.T
    residual = (P_new - P).flatten()
    # KS energy: 0.5 * Tr P (H_core + F)
    E = 0.5 * np.trace(P @ (H_core + F))
    return P_new, residual, E


def inner(R):
    """Flat Euclidean inner product on the flattened residual."""
    return float(R @ R)


# -------------------------------------------------------------------------
# Linear mixing
# -------------------------------------------------------------------------
def scf_linear(max_iter=200, alpha=MIX):
    P = np.zeros_like(H_core)
    hist = []
    for it in range(max_iter):
        P_new, R, E = ks_step(P)
        hist.append((E, inner(R)))
        if inner(R) < TOL:
            break
        P = (1.0 - alpha) * P + alpha * P_new
    return hist


# -------------------------------------------------------------------------
# DIIS
# -------------------------------------------------------------------------
def diis_coefficients(R_list):
    m = len(R_list)
    B = np.zeros((m + 1, m + 1))
    for i in range(m):
        for j in range(m):
            B[i, j] = R_list[i] @ R_list[j]
    B[-1, :m] = 1.0
    B[:m, -1] = 1.0
    rhs = np.zeros(m + 1)
    rhs[-1] = 1.0
    sol = np.linalg.solve(B, rhs)
    return sol[:m]


def scf_diis(max_iter=200, m_max=6, alpha=1.0):
    P = np.zeros_like(H_core)
    P_hist, R_hist = [], []
    hist = []
    for it in range(max_iter):
        P_new, R, E = ks_step(P)
        hist.append((E, inner(R)))
        if inner(R) < TOL:
            break
        P_hist.append(P_new)
        R_hist.append(R)
        if len(P_hist) >= 2:
            m = min(len(P_hist), m_max)
            cs = diis_coefficients(R_hist[-m:])
            P_extrap = sum(cs[i] * P_hist[-(m - i)] for i in range(m))
            # next step: use extrapolated P, do a pure step (alpha=1)
            P = (1.0 - alpha) * P + alpha * P_extrap
        else:
            P = P_new
    return hist


# -------------------------------------------------------------------------
# Good Broyden
# -------------------------------------------------------------------------
def scf_broyden(max_iter=200, alpha=0.5):
    P = np.zeros_like(H_core)
    G = -alpha * np.eye(4)  # approx inverse Jacobian
    hist = []
    r_old = np.zeros(4)
    for it in range(max_iter):
        P_new, R, E = ks_step(P)
        hist.append((E, inner(R)))
        if inner(R) < TOL:
            break
        # Broyden step:  dP = -G r
        dP = -G @ R
        P_broy = P + dP.reshape(2, 2)
        # Re-normalize: diagonalize F(P_broy) and build physical P
        F_broy = H_core + v_xc(P_broy)
        _, C_broy = scipy.linalg.eigh(F_broy, S)
        Cocc_broy = C_broy[:, :N_OCC]
        P = 2.0 * Cocc_broy @ Cocc_broy.T
        # Update G using the actual change in P and R
        delta_x = (P - P_new).flatten()
        delta_r = R - r_old
        denom = delta_x @ delta_x
        if denom > 1e-30:
            G = G + np.outer(delta_x - G @ delta_r, delta_x) / denom
        r_old = R
    return hist


# -------------------------------------------------------------------------
# Run and plot
# -------------------------------------------------------------------------
def plot_convergence(all_hist, out_path):
    fig, (axE, axR) = plt.subplots(1, 2, figsize=(11, 4))
    for label, hist in all_hist.items():
        Es = [e for e, r in hist]
        Rs = [r for e, r in hist]
        iters = np.arange(len(Es))
        axE.plot(iters, Es - Es[-1] + 1e-16, "o-", label=label, ms=3)
        axR.semilogy(iters, Rs, "o-", label=label, ms=3)
    axE.set_xlabel("SCF iteration")
    axE.set_ylabel("$E^{(n)} - E_\\mathrm{conv}$  [Ha]")
    axE.set_yscale("log")
    axE.legend()
    axE.set_title("Energy convergence")
    axR.set_xlabel("SCF iteration")
    axR.set_ylabel("$\\|\\rho_\\mathrm{out} - \\rho_\\mathrm{in}\\|$")
    axR.set_title("Residual convergence")
    axR.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    print(f"  Plot saved to {out_path}")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    print("Running SCF: linear mixing ...")
    h_lin = scf_linear()
    print(f"  converged in {len(h_lin)} iters, E = {h_lin[-1][0]:.12f}")

    print("Running SCF: DIIS (m_max=6) ...")
    h_diis = scf_diis()
    print(f"  converged in {len(h_diis)} iters, E = {h_diis[-1][0]:.12f}")

    print("Running SCF: Broyden (good) ...")
    h_broy = scf_broyden()
    print(f"  converged in {len(h_broy)} iters, E = {h_broy[-1][0]:.12f}")

    out = os.path.join(plots_dir, "01-diis-scf.png")
    plot_convergence(
        {"linear": h_lin, "DIIS (m=6)": h_diis, "Broyden": h_broy},
        out,
    )
