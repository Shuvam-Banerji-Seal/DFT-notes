# dft_notes/python_codes/chapter_11/01-graphene-bands.py
#
# Tight-binding band structure of graphene along Gamma - M - K - Gamma
# in the hexagonal Brillouin zone, with a single p_z orbital per
# carbon and a single nearest-neighbour hopping t.
#
# The two-atom basis gives a 2x2 Bloch Hamiltonian
#     H(k) = [[0, f(k)],
#             [f*(k), 0]]
# with f(k) = t (1 + e^{i k.a1} + e^{i k.a2}).
# The eigenvalues are eps_+/- (k) = +/- |f(k)|, the bonding (pi) and
# antibonding (pi*) bands.  The two bands touch at the K point with
# a linear, massless dispersion (the "Dirac cone").
#
# Run from the repository root:
#     python dft_notes/python_codes/chapter_11/01-graphene-bands.py
# The plot is written to plots/01-graphene-bands.png.
#
# Tested with Python 3.11, numpy 1.26, matplotlib 3.8.

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# --- Parameters --------------------------------------------------------
A = 2.46  # graphene lattice constant, Angstrom
T = -2.8  # nearest-neighbour pi hopping, eV (sign convention
# makes the pi band the lower band, the pi* band the
# upper band, and the centre of the pi-pi* pair at E=0)
N = 200  # k-points per path segment (total path is 3 segments
# of N points each, minus 1 for the shared endpoints)


# --- Reciprocal-lattice primitive vectors (Cartesian, 1/Angstrom) ----
#   a1 = A (1, 0)              a2 = A (1/2, sqrt(3)/2)
#   b1 = (2 pi / A) (1, -1/sqrt(3))
#   b2 = (2 pi / A) (0,  2/sqrt(3))
# We do not use b1, b2 directly; we sample the k-path in units of
# 1/A and convert to the phase e^{i k.a1}, e^{i k.a2} using
# k . a1 = 2 pi (k_x A),  k . a2 = 2 pi (k_x A/2 + k_y A sqrt(3)/2).


# --- High-symmetry points in the hexagonal BZ (Cartesian, 1/A) -------
Gamma = np.array([0.0, 0.0])
M = np.array([0.5, 0.0])
K = np.array([1.0 / 3.0, 1.0 / np.sqrt(3.0)])


# --- k-path helper ----------------------------------------------------
def kpath(points, n_per_segment):
    """Sample a piecewise-linear k-path.

    Parameters
    ----------
    points : list of (2,) array-like
        The k-path in Cartesian coordinates (units of 1/A).
    n_per_segment : int
        Number of samples per straight-line segment.

    Returns
    -------
    kpts : ndarray, shape (M, 2)
        The sampled k-points, in Cartesian coordinates (1/A).
    dist : ndarray, shape (M,)
        Cumulative arc length along the path, starting at 0.  The
        units are 1/A; the *relative* length is what matters for
        plotting.
    """
    pts = np.asarray(points, dtype=float)
    # Build the path two stages: first the full segments, then
    # strip duplicates at the seams.  This avoids the off-by-one
    # bug where the original code stripped a point from `seg` but
    # then derived `d` from the stripped seg (giving one fewer
    # d entry than klist has points).
    raw_klist = []
    raw_dlist = [0.0]  # cumulative distance starts at 0
    for i in range(len(pts) - 1):
        is_last = i == len(pts) - 2
        seg = np.linspace(pts[i], pts[i + 1], n_per_segment, endpoint=is_last)
        d = np.linalg.norm(np.diff(seg, axis=0), axis=1)
        raw_klist.append(seg)
        raw_dlist.extend((raw_dlist[-1] + np.cumsum(d)).tolist())
    # Now concatenate the full segments, dropping the duplicate
    # at each seam (the endpoint of seg i is the start of seg i+1).
    kpts = [raw_klist[0]]
    dist = [0.0]
    for i in range(1, len(raw_klist)):
        # raw_klist[i] starts with the same point that raw_klist[i-1]
        # ended with.  Drop the first point and corresponding
        # cumulative-distance entry to avoid duplication.
        kpts.append(raw_klist[i][1:])
        dist.extend(
            raw_dlist[
                1 + i * (n_per_segment - 1) + (1 if i < len(raw_klist) - 1 else 0) :
            ][: len(raw_klist[i]) - 1]
        )
    # Simpler: just recompute dist from kpts (numerical differences
    # are tiny, so the cost is negligible for a 600-point path).
    kpts_arr = np.vstack(kpts)
    dist_arr = np.zeros(len(kpts_arr))
    for i in range(1, len(kpts_arr)):
        dist_arr[i] = dist_arr[i - 1] + np.linalg.norm(kpts_arr[i] - kpts_arr[i - 1])
    return kpts_arr, dist_arr


# --- Build the k-path Gamma - M - K - Gamma ---------------------------
path_points = [Gamma, M, K, Gamma]
kpts, dist = kpath(path_points, N)
print(
    f"Sampled {kpts.shape[0]:d} k-points along the path "
    f"Gamma - M - K - Gamma (length = {dist[-1]:.4f} 1/A)."
)

# --- Structure factor f(k) -------------------------------------------
# f(k) = t (1 + e^{i k.a1} + e^{i k.a2})
#       = t (1 + exp(i 2 pi kx A) + exp(i pi kx A) exp(i pi ky A sqrt(3)))
#
# We compute in numpy vector form.  Note: kx, ky here are in 1/A, so
# kx * A is dimensionless.
kxA = kpts[:, 0] * A  # kx * a1.x  (k . a1 / (2 pi))
kyA = kpts[:, 1] * A  # ky * a1.y  (k . a2 components)

phase_1 = np.exp(1j * 2.0 * np.pi * kxA)
phase_2 = np.exp(1j * np.pi * (kxA + kyA * np.sqrt(3.0)))
f = T * (1.0 + phase_1 + phase_2)
f_abs = np.abs(f)

# --- Eigenvalues of the 2x2 Hamiltonian ------------------------------
#  H = [[0, f], [f*, 0]]  =>  eps_+/- = +/- |f|
eps_pi = -f_abs  # bonding (pi)    band
eps_pistar = +f_abs  # antibonding (pi*) band

# --- Locate the Dirac point on the path ------------------------------
# The K point of the path is at the third tick; find the closest
# sampled k-point and report the gap.
idx_K = int(np.argmin(np.linalg.norm(kpts - K, axis=1)))
gap_at_K = eps_pistar[idx_K] - eps_pi[idx_K]
print(
    f"At K (path index {idx_K:d}): "
    f"eps_pi = {eps_pi[idx_K]:+.6e} eV, "
    f"eps_pi* = {eps_pistar[idx_K]:+.6e} eV, "
    f"gap = {gap_at_K:.3e} eV (should be 0 to within round-off)."
)

# --- Fermi velocity at the Dirac point --------------------------------
# v_F = (3 |t| a) / (2 hbar).  In eV.Angstrom units, we report
# d eps / d k.  We estimate it by finite difference of the pi* band
# near K.
h = 3
slope = (eps_pistar[idx_K + h] - eps_pistar[idx_K - h]) / (
    dist[idx_K + h] - dist[idx_K - h]
)  # eV . Angstrom
# Convert d eps/dk (eV.Angstrom) to v_F (m/s):  v_F = (1/hbar) d eps/dk.
#   1 eV . Angstrom = 1.602e-19 J * 1e-10 m = 1.602e-29 J.m.
#   hbar = 1.055e-34 J.s.
hbar_SI = 1.054571817e-34
eV_to_J = 1.602176634e-19
Angstrom_to_m = 1.0e-10
v_F = (slope * eV_to_J * Angstrom_to_m) / hbar_SI
print(
    f"Fermi velocity at K (linear fit, +/-{h:d} samples): "
    f"v_F = {v_F:.3e} m/s  (experimental: ~1.0e6 m/s)."
)


# --- Plot -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.0))
ax.plot(dist, eps_pi, color="#1f6feb", lw=1.8, label=r"$\pi$")
ax.plot(dist, eps_pistar, color="#d97757", lw=1.8, label=r"$\pi^*$")
ax.axhline(0.0, color="#3d3d3a", lw=0.6, ls="--", alpha=0.6, label="Fermi level")

# tick marks at the high-symmetry points
tick_dists = [
    0.0,
    np.linalg.norm(M - Gamma),
    np.linalg.norm(M - Gamma) + np.linalg.norm(K - M),
    dist[-1],
]
tick_labels = [r"$\Gamma$", "$M$", "$K$", r"$\Gamma$"]
for d, lab in zip(tick_dists, tick_labels):
    ax.axvline(d, color="#3d3d3a", lw=0.5, ls=":", alpha=0.5)
    ax.text(d, 3.0 * abs(T) * 1.02, lab, ha="center", va="bottom", fontsize=11)

ax.set_xlim(0.0, dist[-1])
ax.set_ylim(-3.4 * abs(T), 3.4 * abs(T))
ax.set_xlabel("k-path  (cumulative arc length, $1/\\AA$)")
ax.set_ylabel(r"$\varepsilon_n(\mathbf{k})$  (eV)")
ax.set_title(
    r"Graphene tight-binding band structure: "
    r"$\Gamma$–$M$–$K$–$\Gamma$"
)
ax.legend(frameon=False, loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()

# --- Save -------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(here, "plots")
os.makedirs(plots_dir, exist_ok=True)
out = os.path.join(plots_dir, "01-graphene-bands.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"Wrote {out}")
