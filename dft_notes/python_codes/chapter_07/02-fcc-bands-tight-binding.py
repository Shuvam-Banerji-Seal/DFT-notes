"""
02-fcc-bands-tight-binding.py
=============================

Tight-binding band structure of a face-centred cubic (FCC) lattice
with a single s-orbital per site and nearest-neighbour hopping -t.

The FCC lattice has 12 nearest neighbours, located at the 12 vectors
    (a/2)(+/- 1, +/- 1, 0)  and  cyclic permutations.
Summing exp(i k . delta) over the 12 vectors gives the dispersion
    E(k) = -4t [ cos(k_x a/2) cos(k_y a/2)
               + cos(k_y a/2) cos(k_z a/2)
               + cos(k_z a/2) cos(k_x a/2) ].

This is the canonical "FCC tight-binding band structure" plot: one
s-band drawn along the standard Setyawan-Curtarolo high-symmetry
path

    Gamma -> X -> W -> K -> Gamma -> L -> Gamma

with the high-symmetry points (in units of 2 pi / a)

    Gamma = ( 0  ,  0  ,  0  )
    X     = ( 1  ,  0  ,  0  )       centre of a square face
    W     = ( 1  ,  1/2,  0  )       vertex where 2 hex + 1 square meet
    K     = ( 3/4,  3/4,  0  )       mid-point of a hex - hex edge
    L     = ( 1/2,  1/2,  1/2)       centre of a hexagonal face

With t = 1 (arbitrary units) the band has

    minimum   E(Gamma) = -12     (bonding; all 12 neighbours in phase)
    maximum   E(X)     =  +4     (antibonding along k_x)
               E(W)     =  +4     (antibonding along k_x)
               E(K)     =  +4 (sqrt 2 - 1/2)  approx  +3.66
    saddle    E(L)     =   0     (cos terms all vanish)

giving a total bandwidth of 16.  This is the textbook dispersion for
an FCC tight-binding metal such as Cu, Ni, Al or Pd in the simplest
single-band s-only picture.

Dependencies: numpy, matplotlib (headless via Agg).

Run from the repo root:
    python dft_notes/python_codes/chapter_07/02-fcc-bands-tight-binding.py

Writes its plot to:
    dft_notes/python_codes/chapter_07/plots/02-fcc-bands-tight-binding.png
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless - no display required
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Physical / numerical parameters
# ---------------------------------------------------------------------------
A = 1.0  # FCC conventional cubic lattice constant (arbitrary units)
T = 1.0  # nearest-neighbour hopping magnitude  (arbitrary units; t > 0)
N_PER_SEGMENT = 80  # k-points sampled on each straight segment of the path


# High-symmetry points in Cartesian coordinates, in units of 2 pi / a.
# The factor of 2 pi / a is restored inside the dispersion function so
# the cosines get the dimensionless argument k_i * (a / 2).
GAMMA = np.array([0.0, 0.0, 0.0])
X = np.array([1.0, 0.0, 0.0])
W = np.array([1.0, 0.5, 0.0])
K = np.array([0.75, 0.75, 0.0])
L = np.array([0.5, 0.5, 0.5])

# Path: Gamma -> X -> W -> K -> Gamma -> L -> Gamma
PATH = [GAMMA, X, W, K, GAMMA, L, GAMMA]
LABELS = [r"$\Gamma$", "X", "W", "K", r"$\Gamma$", "L", r"$\Gamma$"]


def fcc_tb_dispersion(k_2pia: np.ndarray, t: float = T) -> np.ndarray:
    """FCC tight-binding dispersion for a single s-orbital per site.

    Parameters
    ----------
    k_2pia : array of shape (..., 3)
        Crystal momentum in units of 2 pi / a, i.e.  k_2pia = k * a / (2 pi).
    t : float
        Nearest-neighbour hopping magnitude.  Hopping matrix element is
        -t, so the energy is *lowered* by bonding (E is negative at Gamma).

    Returns
    -------
    E : array of shape k_2pia.shape[:-1]
        Band energy in units of t.

    Notes
    -----
    The dimensionless argument inside the cosines is
        k_i * (a / 2) = (2 pi / a) * (k_2pia_i) * (a / 2)
                      = pi * k_2pia_i.
    The 12 nearest-neighbour vectors (a/2)(+/- 1, +/- 1, 0) and cyclic
    permutations give, after summing exp(i k . delta) over the 12,
        sum = 4 [cos(k_x a/2) cos(k_y a/2)
                + cos(k_y a/2) cos(k_z a/2)
                + cos(k_z a/2) cos(k_x a/2)].
    Multiplying by the hopping -t gives the result.
    """
    kx = k_2pia[..., 0]
    ky = k_2pia[..., 1]
    kz = k_2pia[..., 2]
    phi_x = np.pi * kx
    phi_y = np.pi * ky
    phi_z = np.pi * kz
    cx, cy, cz = np.cos(phi_x), np.cos(phi_y), np.cos(phi_z)
    return -4.0 * t * (cx * cy + cy * cz + cz * cx)


def sample_segment(
    k_start: np.ndarray, k_end: np.ndarray, n: int
) -> np.ndarray:
    """n points linearly between k_start and k_end, endpoints inclusive.

    Returns an array of shape (n, 3).  Adjacent segments share endpoints,
    so when we stack all segments we get the full k-path.
    """
    t = np.linspace(0.0, 1.0, n)
    return k_start[None, :] * (1.0 - t[:, None]) + k_end[None, :] * t[:, None]


def build_kpath(path, n_per_segment):
    """Stack the segments into one (N, 3) array of k-points."""
    segs = []
    for i in range(len(path) - 1):
        segs.append(sample_segment(path[i], path[i + 1], n_per_segment))
    return np.vstack(segs)


def main() -> None:
    # --- Build the k-path -------------------------------------------------
    k_path = build_kpath(PATH, N_PER_SEGMENT)

    # Cumulative distance along the path (in units of 2 pi / a).  This
    # is the natural "x-axis" for a band-structure plot.
    diffs = np.diff(k_path, axis=0)
    seg_lengths = np.linalg.norm(diffs, axis=1)
    distances = np.concatenate([[0.0], np.cumsum(seg_lengths)])

    # x-tick positions: the high-symmetry points on the path.
    tick_positions = []
    tick_labels = []
    tick_positions.append(0.0)
    tick_labels.append(LABELS[0])
    cumulative = 0.0
    for i in range(len(PATH) - 1):
        seg_len = np.linalg.norm(PATH[i + 1] - PATH[i])
        cumulative += seg_len
        tick_positions.append(cumulative)
        tick_labels.append(LABELS[i + 1])

    # --- Dispersion along the path ----------------------------------------
    energies = fcc_tb_dispersion(k_path, t=T)

    # --- Dispersion at the high-symmetry points (sanity check) -----------
    E_gamma = float(fcc_tb_dispersion(GAMMA[None, :], t=T)[0])
    E_X = float(fcc_tb_dispersion(X[None, :], t=T)[0])
    E_W = float(fcc_tb_dispersion(W[None, :], t=T)[0])
    E_K = float(fcc_tb_dispersion(K[None, :], t=T)[0])
    E_L = float(fcc_tb_dispersion(L[None, :], t=T)[0])
    bandwidth = energies.max() - energies.min()
    E_K_predicted = 4.0 * (np.sqrt(2.0) - 0.5)

    print("FCC tight-binding band structure (t = 1, arbitrary units):")
    print(f"  E(Gamma) = {E_gamma:+.4f}     expected  -12   (band minimum)")
    print(f"  E(X)     = {E_X:+.4f}     expected  +4    (band maximum)")
    print(f"  E(W)     = {E_W:+.4f}     expected  +4    (band maximum)")
    print(f"  E(K)     = {E_K:+.4f}     expected  +{E_K_predicted:.4f}  = 4(sqrt 2 - 1/2)")
    print(f"  E(L)     = {E_L:+.4f}     expected   0    (cos terms all vanish)")
    print(f"  bandwidth = max - min on path = {bandwidth:.4f}   expected  16")

    # --- Plot -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10.0, 6.0))

    # The band itself, in the site palette coral.
    ax.plot(
        distances, energies,
        color="#cc785c", linewidth=2.2, label=r"single $s$-band, hopping $-t$",
    )

    # Vertical dashed lines at every high-symmetry point.
    for pos in tick_positions:
        ax.axvline(pos, color="#3d3d3a", linewidth=0.7,
                   linestyle="--", alpha=0.55)

    # Horizontal reference at E = 0.
    ax.axhline(0.0, color="#a09d96", linewidth=0.8, alpha=0.4)

    # x-ticks: the high-symmetry point labels.
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, fontsize=12)
    ax.set_xlim(distances[0], distances[-1])
    ax.set_ylim(energies.min() - 0.6, energies.max() + 0.6)

    ax.set_xlabel(r"k-path  (high-symmetry points marked)")
    ax.set_ylabel(r"$E(\mathbf{k})$  (units of $t$)")
    ax.set_title(
        r"FCC tight-binding band structure,  "
        r"$E(\mathbf{k})=-4t\,\sum_{i<j}\cos(k_i a/2)\cos(k_j a/2)$"
    )
    ax.legend(frameon=False, loc="lower right")
    ax.grid(True, alpha=0.25)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()

    # --- Save the plot ----------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "02-fcc-bands-tight-binding.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
