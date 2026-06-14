"""
02-pbe-vs-lda-atoms.py
======================

Perdew-Burke-Ernzerhof (PBE) GGA vs LDA for the helium and
beryllium atoms.  Uses simple Slater-type trial densities
(closed-shell spin-restricted) and computes the LDA and PBE
exchange-correlation energies by numerical integration.

The exchange-correlation energy of a closed-shell atom is

    E_xc[n] = \int n(r) * eps_xc(r; n, |grad n|) * d^3r

with the standard LDA / PBE ingredients:

    eps_x^{LDA}(n)   = -Cx * n^{1/3},    Cx = (3/4) (3/pi)^{1/3}
    eps_c^{LDA}(n)   = PZ81(r_s),         r_s = (3 / 4 pi n)^{1/3}
    s                = |grad n| / (2 k_F n),   k_F = (3 pi^2 n)^{1/3}
    F_x^{PBE}(s)     = 1 + kappa - kappa / (1 + mu s^2 / kappa)
    eps_x^{PBE}(n,s) = eps_x^{LDA}(n) * F_x^{PBE}(s)
    k_s              = (4 k_F / pi)^{1/2}
    t                = |grad n| / (2 k_s n)
    A                = beta / (gamma (exp(-eps_c^{LDA}/gamma) - 1))
    H                = gamma * ln[1 + (beta/gamma) t^2
                                 * (1 + A t^2)
                                 / (1 + A t^2 + (A t^2)^2)]
    eps_c^{PBE}(n,s) = eps_c^{LDA}(n) + H

with the PBE parameters
    kappa = 0.804,  mu = 0.21951,
    beta  = 0.066725,  gamma = 0.031091.

Reference: J. P. Perdew, K. Burke, M. Ernzerhof,
Phys. Rev. Lett. 77, 3865 (1996), and erratum 78, 1396 (1997).

Why this lives in chapter 05:
    Section 5.2 (GGA) introduces the PBE functional.  This
    script is the runnable counterpart of the formulas on
    that page and shows the standard PBE-vs-LDA effect on
    atomic exchange-correlation energies.

Run from the repo root:
    python dft_notes/python_codes/chapter_05/02-pbe-vs-lda-atoms.py

Writes the plot to:
    dft_notes/python_codes/chapter_05/plots/02-pbe-vs-lda-atoms.png

Dependencies: numpy, matplotlib (headless via Agg).
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ─── PBE parameters ───────────────────────────────────────────────
# Cx = (3/4) (3/pi)^{1/3},  the LDA exchange coefficient
CX = (3.0 / 4.0) * (3.0 / np.pi) ** (1.0 / 3.0)
KAPPA = 0.804
MU = 0.21951
BETA = 0.066725
GAMMA = 0.031091


# ─── Atomic densities (Slater-type, closed shell) ─────────────────
# He: variational exponent  Z_eff = Z - 5/16 = 1.6875
Z_HE = 1.6875
# Be (Slater rules):
#   zeta(1s) = Z - 0.30 = 3.7  (other 1s electron)
#   zeta(2s) = Z - 2*0.85 - 0.35 = 1.95
Z_BE_1S = 3.7
Z_BE_2S = 1.95


def he_density(r: np.ndarray):
    """He 1s^2 Slater density and its radial derivative.
    n(r) = 2 (Z^3/pi) * exp(-2 Z r)
    n'(r) = -2 Z * n(r)
    """
    n = 2.0 * (Z_HE**3 / np.pi) * np.exp(-2.0 * Z_HE * r)
    n_d = -2.0 * Z_HE * n
    return n, n_d


def be_density(r: np.ndarray):
    """Be 1s^2 2s^2 Slater density and its radial derivative.
    n(r) = 2 (zeta_1^3/pi) e^{-2 zeta_1 r}
         + 2 (zeta_2^5/(3 pi)) r^2 e^{-2 zeta_2 r}
    """
    z1, z2 = Z_BE_1S, Z_BE_2S
    n1 = 2.0 * (z1**3 / np.pi) * np.exp(-2.0 * z1 * r)
    n2 = 2.0 * (z2**5 / (3.0 * np.pi)) * r**2 * np.exp(-2.0 * z2 * r)
    n = n1 + n2
    n_d1 = -2.0 * z1 * n1
    # derivative of  r^2 e^{-2 z2 r}  is  (2 r - 2 z2 r^2) e^{-2 z2 r}
    # at r = 0 the limit is 0 (n2 ~ r^2, n_d2 ~ 4 r); we use np.where
    # so the 2/r piece is well behaved away from r = 0.
    n_d2 = np.where(r > 0.0, n2 * (2.0 / r - 2.0 * z2), 0.0)
    n_d = n_d1 + n_d2
    return n, n_d


# ─── Perdew-Zunger correlation (same as script 01) ───────────────
PZ_HIGH_DENSITY = {
    "A": 0.0311,
    "B": -0.0480,
    "C": 0.0020,
    "D": -0.0116,
}
PZ_LOW_DENSITY = {
    "A": -0.1423,
    "B": 1.0529,
    "C": 0.3334,
}


def pz81_correlation_unpolarized(rs: np.ndarray) -> np.ndarray:
    """Perdew-Zunger (1981) fit to Ceperley-Alder QMC, unpolarized."""
    rs = np.asarray(rs, dtype=float)
    ec = np.empty_like(rs)
    mask_lo = rs < 1.0
    rs_lo = rs[mask_lo]
    c = PZ_HIGH_DENSITY
    ec[mask_lo] = (
        c["B"]
        + c["A"] * np.log(rs_lo)
        + c["D"] * rs_lo
        + c["C"] * rs_lo * np.log(rs_lo)
    )
    rs_hi = rs[~mask_lo]
    c = PZ_LOW_DENSITY
    ec[~mask_lo] = c["A"] / (1.0 + c["B"] * np.sqrt(rs_hi) + c["C"] * rs_hi)
    return ec


# ─── PBE pieces ───────────────────────────────────────────────────
def lda_exchange_per_particle(n: np.ndarray) -> np.ndarray:
    """LDA exchange per particle, in Hartree:  -Cx n^{1/3}."""
    return -CX * n ** (1.0 / 3.0)


def pbe_exchange_enhancement(s: np.ndarray) -> np.ndarray:
    """F_x(s) = 1 + kappa - kappa / (1 + mu s^2 / kappa)."""
    return 1.0 + KAPPA - KAPPA / (1.0 + MU * s**2 / KAPPA)


def pbe_correlation_enhancement(eps_c_lda: np.ndarray, t: np.ndarray) -> np.ndarray:
    """H(eps_c_lda, t) from PBE 1996 eq. (8), unpolarized case.

    H = gamma * ln[ 1 + (beta/gamma) t^2 (1 + A t^2)
                                 / (1 + A t^2 + A^2 t^4) ]
    A = beta / (gamma (exp(-eps_c_lda/gamma) - 1))
    """
    A = BETA / (GAMMA * (np.exp(-eps_c_lda / GAMMA) - 1.0))
    H = GAMMA * np.log(
        1.0 + (BETA / GAMMA) * t**2 * (1.0 + A * t**2) / (1.0 + A * t**2 + A**2 * t**4)
    )
    return H


# ─── Main work: integrate over a radial grid ──────────────────────
def atom_energies(density_fn, r_max: float = 20.0, n_grid: int = 4000, label: str = ""):
    """Compute LDA and PBE exchange and correlation energies for an
    atom whose radial density is given by ``density_fn(r)``.

    Returns a dict with keys:
        Ex_lda, Ec_lda, Ex_pbe, Ec_pbe, Ex_pbe_ratio
    (all in Hartree).
    """
    # The radial grid: start just above r = 0 to avoid the 1/r in
    # the Be 2s derivative; the integrand is 4 pi r^2 n epsilon, so
    # the r -> 0 limit of the integrand is well-defined.
    r = np.linspace(1.0e-8, r_max, n_grid)

    n, n_d = density_fn(r)

    # Floors to avoid 0/0 in the enhancement factors.
    n_safe = np.maximum(n, 1.0e-20)
    grad_n = np.abs(n_d)

    # k_F = (3 pi^2 n)^{1/3}
    k_F = (3.0 * np.pi**2 * n_safe) ** (1.0 / 3.0)
    # s = |grad n| / (2 k_F n)
    s = grad_n / (2.0 * k_F * n_safe)

    # r_s = (3 / (4 pi n))^{1/3}
    rs = (3.0 / (4.0 * np.pi * n_safe)) ** (1.0 / 3.0)

    # k_s = (4 k_F / pi)^{1/2}
    k_s = np.sqrt(4.0 * k_F / np.pi)
    # t = |grad n| / (2 k_s n)
    t = grad_n / (2.0 * k_s * n_safe)

    # Energies per particle
    eps_x_lda = lda_exchange_per_particle(n_safe)
    eps_c_lda = pz81_correlation_unpolarized(rs)

    Fx = pbe_exchange_enhancement(s)
    eps_x_pbe = eps_x_lda * Fx

    H = pbe_correlation_enhancement(eps_c_lda, t)
    eps_c_pbe = eps_c_lda + H

    # Integrate  4 pi r^2 n(r) eps(r) dr  over r
    dV = 4.0 * np.pi * r**2
    Ex_lda = float(np.trapz(n_safe * eps_x_lda * dV, r))
    Ec_lda = float(np.trapz(n_safe * eps_c_lda * dV, r))
    Ex_pbe = float(np.trapz(n_safe * eps_x_pbe * dV, r))
    Ec_pbe = float(np.trapz(n_safe * eps_c_pbe * dV, r))

    return {
        "label": label,
        "Ex_lda": Ex_lda,
        "Ec_lda": Ec_lda,
        "Ex_pbe": Ex_pbe,
        "Ec_pbe": Ec_pbe,
        "Ex_pbe_ratio": Ex_pbe / Ex_lda,
    }


# ─── Main ──────────────────────────────────────────────────────────
def main() -> None:
    he = atom_energies(he_density, r_max=12.0, label="He")
    be = atom_energies(be_density, r_max=10.0, label="Be")

    print("=" * 60)
    print("PBE vs LDA exchange-correlation on He and Be")
    print("Hydrogenic / Slater-type trial densities, numerical integration.")
    print("=" * 60)
    for atom in (he, be):
        print(
            f"\n  {atom['label']}:\n"
            f"    E_x (LDA)  = {atom['Ex_lda']:+.6f} E_h\n"
            f"    E_x (PBE)  = {atom['Ex_pbe']:+.6f} E_h"
            f"   (PBE/LDA = {atom['Ex_pbe_ratio']:.4f})\n"
            f"    E_c (LDA)  = {atom['Ec_lda']:+.6f} E_h\n"
            f"    E_c (PBE)  = {atom['Ec_pbe']:+.6f} E_h"
        )

    # ─── Bar chart ────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=False)

    atoms_labels = [he["label"], be["label"]]
    x = np.arange(len(atoms_labels))
    width = 0.35

    palette = {"LDA": "#cc785c", "PBE": "#5db8a6"}

    # Exchange
    ax = axes[0]
    ax.bar(
        x - width / 2,
        [he["Ex_lda"], be["Ex_lda"]],
        width,
        color=palette["LDA"],
        label="LDA",
    )
    ax.bar(
        x + width / 2,
        [he["Ex_pbe"], be["Ex_pbe"]],
        width,
        color=palette["PBE"],
        label="PBE",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(atoms_labels)
    ax.set_ylabel(r"$E_x$  (Hartree)")
    ax.set_title("Exchange energy")
    ax.axhline(0.0, color="#a09d96", linewidth=0.6)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(frameon=False, loc="lower left")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    # Correlation
    ax = axes[1]
    ax.bar(
        x - width / 2,
        [he["Ec_lda"], be["Ec_lda"]],
        width,
        color=palette["LDA"],
        label="LDA",
    )
    ax.bar(
        x + width / 2,
        [he["Ec_pbe"], be["Ec_pbe"]],
        width,
        color=palette["PBE"],
        label="PBE",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(atoms_labels)
    ax.set_ylabel(r"$E_c$  (Hartree)")
    ax.set_title("Correlation energy")
    ax.axhline(0.0, color="#a09d96", linewidth=0.6)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(frameon=False, loc="lower left")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.suptitle("PBE vs LDA on closed-shell atoms (He, Be)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    # ─── Save ─────────────────────────────────────────────────────
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "02-pbe-vs-lda-atoms.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
