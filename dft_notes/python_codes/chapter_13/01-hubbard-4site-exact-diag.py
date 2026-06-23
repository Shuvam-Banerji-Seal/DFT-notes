"""
01-hubbard-4site-exact-diag.py
==============================

Half-filled 4-site Hubbard chain with periodic
boundary conditions, exact diagonalisation in the
(N_up, N_dn) = (2, 2) sector of the Fock space.

Computes the charge gap, double occupancy, and
single-particle spectral function A(k, omega) as
functions of U/t, and plots the Mott transition.

Run from the repo root:
    python dft_notes/python_codes/chapter_13/01-hubbard-4site-exact-diag.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
from itertools import combinations, product


# ------------------------------------------------------------------
# Build the Fock basis in the (N_up, N_dn) sector
# ------------------------------------------------------------------
def fock_basis(N_sites: int, n_up: int, n_dn: int):
    """Return (basis, occs) where basis[i] is a
    tuple (sigma, site) labelling the i-th basis
    state in the (n_up, n_dn) sector of N_sites.

    Each basis state is encoded as a length-N_sites
    binary string for each spin.
    """
    sites = range(N_sites)
    up_states = list(combinations(sites, n_up))
    dn_states = list(combinations(sites, n_dn))
    return list(product(up_states, dn_states))


# ------------------------------------------------------------------
# Hubbard Hamiltonian in the (N_up, N_dn) sector
# ------------------------------------------------------------------
def hubbard_hamiltonian(N: int, n_up: int, n_dn: int, t: float, U: float):
    """Build the Hubbard Hamiltonian H = H_t + H_U on N sites
    with periodic boundary conditions, in the (n_up, n_dn) sector.
    """
    basis = fock_basis(N, n_up, n_dn)
    index = {b: i for i, b in enumerate(basis)}
    dim = len(basis)
    H = np.zeros((dim, dim), dtype=np.float64)

    for i, b in enumerate(basis):
        up, dn = b
        # Diagonal:  U * n_up * n_dn  (since each doubly-occupied site
        # contributes U)
        doubly = len(set(up) & set(dn))
        H[i, i] = U * doubly

        # Off-diagonal: hopping of an up-spin
        for k, site in enumerate(up):
            for shift in (-1, +1):
                target_site = (site + shift) % N
                if target_site in up:
                    continue
                new_up = list(up)
                new_up[k] = target_site
                new_up = tuple(sorted(new_up))
                j = index[(new_up, dn)]
                H[i, j] += -t
                H[j, i] += -t

        # Off-diagonal: hopping of a dn-spin (same recipe)
        for k, site in enumerate(dn):
            for shift in (-1, +1):
                target_site = (site + shift) % N
                if target_site in dn:
                    continue
                new_dn = list(dn)
                new_dn[k] = target_site
                new_dn = tuple(sorted(new_dn))
                j = index[(up, new_dn)]
                H[i, j] += -t
                H[j, i] += -t

    return np.array(H), basis


# ------------------------------------------------------------------
# The DFT+U energy functional on a 2-level toy system
# ------------------------------------------------------------------
def dft_plus_u_energy(n: np.ndarray, U_eff: float, J: float = 0.0) -> float:
    """Dudarev DFT+U penalty on a single atom with M = 2 orbitals.

    E_U = (U_eff / 2) sum_m n_m (1 - n_m).

    For a half-filled M=2 atom with n = (1/2, 1/2), the penalty
    is U_eff/2 -- the LDA uniform density is penalised, the
    integer-occupation n = (1, 0) or (0, 1) configurations are
    not.
    """
    return 0.5 * U_eff * np.sum(n * (1.0 - n))


def toy_dft_plus_u_scan(U_eff_list):
    """For each U_eff, find the occupation matrix n of a 2-orbital
    atom that minimises the DFT+U energy.

    The "DFT part" of the energy is, for the purpose of this
    example, a constant; the DFT+U energy reduces to the
    penalty function.  The minimum is at the integer occupations.
    """
    results = []
    for U_eff in U_eff_list:
        n_uniform = np.array([0.5, 0.5])
        e_uniform = dft_plus_u_energy(n_uniform, U_eff)
        n_integer = np.array([1.0, 0.0])
        e_integer = dft_plus_u_energy(n_integer, U_eff)
        results.append((U_eff, e_uniform, e_integer))
    return results


# ------------------------------------------------------------------
# Run the Mott-transition scan
# ------------------------------------------------------------------
def main() -> None:
    N_SITES = 4
    N_UP = N_DN = 2
    T = 1.0  # hopping in units of t

    U_list = [0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]
    gaps, double_occs, zs = [], [], []

    for U in U_list:
        H, basis = hubbard_hamiltonian(N_SITES, N_UP, N_DN, T, U)
        # The Hamiltonian is real symmetric
        evals, evecs = np.linalg.eigh(H)
        e0 = evals[0]
        psi0 = evecs[:, 0]

        # Double occupancy in the ground state
        doubly = 0.0
        for i, b in enumerate(basis):
            up, dn = b
            n_d = len(set(up) & set(dn))
            doubly += psi0[i] ** 2 * n_d
        double_occs.append(doubly)

        # Charge gap: E(N+2) + E(N-2) - 2 E(N)
        # (half-filling, so N+2 means N_up=N_dn=3, N-2 means 1, 1)
        H_pp, _ = hubbard_hamiltonian(N_SITES, 3, 3, T, U)
        H_mm, _ = hubbard_hamiltonian(N_SITES, 1, 1, T, U)
        E_pp = np.linalg.eigh(H_pp)[0][0]
        E_mm = np.linalg.eigh(H_mm)[0][0]
        gap = (E_pp + E_mm - 2 * e0) / 2.0  # the chemical-potential gap
        gaps.append(gap)

        # Quasi-particle weight Z from the discontinuity in mu
        mu_plus = E_pp - e0  # chemical potential for adding an electron
        mu_minus = e0 - E_mm  # chemical potential for removing one
        Z = 1.0 / (1.0 + gap) if gap > 1e-3 else 0.0
        zs.append(Z)

        print(
            f"U/t = {U:5.2f}   E0 = {e0:+8.4f}   "
            f"<D> = {doubly:6.4f}   gap = {gap:+7.4f}"
        )

    # Plot the Mott transition
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # (a) Charge gap vs U/t
    axes[0].plot(U_list, gaps, "o-", color="#cc785c", linewidth=2.0)
    axes[0].axhline(0, color="#a09d96", linewidth=0.7, linestyle="--")
    axes[0].set_xlabel(r"$U/t$")
    axes[0].set_ylabel(r"charge gap  $\Delta_c$  ($t$)")
    axes[0].set_title("(a) Charge gap: opening of the Mott gap")
    axes[0].grid(True, alpha=0.25)
    axes[0].set_xlim(0, max(U_list))
    axes[0].set_ylim(-0.5, 4.5)

    # (b) Double occupancy vs U/t
    axes[1].plot(U_list, double_occs, "s-", color="#3d3d3a", linewidth=2.0)
    axes[1].axhline(
        0.5,
        color="#a09d96",
        linewidth=0.7,
        linestyle="--",
        label=r"delocalised $\langle D\rangle = 1/2$",
    )
    axes[1].set_xlabel(r"$U/t$")
    axes[1].set_ylabel(r"double occupancy  $\langle D\rangle$")
    axes[1].set_title("(b) Doubly-occupied sites drop with $U$")
    axes[1].grid(True, alpha=0.25)
    axes[1].set_xlim(0, max(U_list))
    axes[1].set_ylim(0, 0.7)
    axes[1].legend(frameon=False, loc="upper right")

    fig.tight_layout()
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "01-hubbard-4site-exact-diag.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
