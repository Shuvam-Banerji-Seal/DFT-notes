"""
02-pseudopotential-transferability.py
======================================

Construct a Troullier-Martins norm-conserving pseudopotential for a
fictitious 1-D "atom" with Z = 4 in the l = 0 channel with cutoff
r_c = 1.5 a_0, then test transferability via a box-eigenvalue test
and a logarithmic-derivative test.

The all-electron reference is the 1s-like orbital of a fictitious
1-D hydrogenic atom:

    u_ae(r) = 2 Z^{3/2} r e^{-Z r} = 16 r e^{-4 r}
    E_0     = -Z^2 / 2          = -8     E_h

The Troullier-Martins pseudo-wavefunction is

    phi(r) = r * exp(c_0 + c_1 r^2 + c_2 r^4 + c_3 r^6)    for r <= r_c

with c_0 set by value-matching at r_c, and (c_1, c_2, c_3) chosen so
that the slope, curvature, and integrated norm match the all-electron
wavefunction at r_c.  The pseudo-potential is then obtained by
inverting the radial equation inside r_c, with V_ps(r) = -Z/r stitched
on for r > r_c.

Transferability tests:

  1. Box-eigenvalue test.  Solve the pseudo-eigenvalue problem on a
     cell-centered finite-difference grid (h = 0.02 a_0, Dirichlet BC
     at r = 0 and r = L) for L = 10 a_0 and L = 20 a_0 with
     scipy.linalg.eigh_tridiagonal.  The two lowest eigenvalues must
     agree to better than 1 mE_h.

  2. Logarithmic-derivative test.  Compute D_l(E; r_c) = u'(r_c)/u(r_c)
     as a function of energy by Numerov integration, and check that
     the AE and PS curves overlap.

Run from the repo root:

    python dft_notes/python_codes/chapter_08/02-pseudopotential-transferability.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless -- no display required
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import fsolve
from scipy.linalg import eigh_tridiagonal


# ---------------------------------------------------------------------------
# Constants (atomic units)
# ---------------------------------------------------------------------------
Z = 4
R_C = 1.5
E_0 = -(Z**2) / 2.0  # = -8 E_h


# ---------------------------------------------------------------------------
# All-electron reference
# ---------------------------------------------------------------------------


def u_ae(r):
    """All-electron radial wavefunction u_0(r) = 16 r e^{-4 r}."""
    return 16.0 * r * np.exp(-Z * r)


def u_ae_prime(r):
    """First derivative of u_ae:  u_ae'(r) = 16 (1 - Z r) e^{-Z r}."""
    return 16.0 * (1.0 - Z * r) * np.exp(-Z * r)


def u_ae_double_prime(r):
    """Second derivative of u_ae:  u_ae''(r) = -16 Z (2 - Z r) e^{-Z r}."""
    return -16.0 * (2.0 - Z * r) * Z * np.exp(-Z * r)


# Sanity check:  radial equation at a few test points.
for r_test in (0.1, 0.5, 1.0, 1.5, 2.0):
    lhs = -0.5 * u_ae_double_prime(r_test) - (Z / r_test) * u_ae(r_test)
    rhs = E_0 * u_ae(r_test)
    assert abs(lhs - rhs) < 1e-12, f"radial check failed at r={r_test}"

# Properties at r_c.
u_at_rc = u_ae(R_C)
u_prime_at_rc = u_ae_prime(R_C)
u_dd_at_rc = u_ae_double_prime(R_C)
log_deriv_at_rc = u_prime_at_rc / u_at_rc  # = 1/r_c - Z

# Closed form for Q_ae = int_0^{r_c} u_ae^2 dr.
#   int r^2 e^{-alpha r} dr = -(e^{-alpha r}/alpha)(r^2 + 2r/alpha + 2/alpha^2)
# With alpha = 2Z = 8:
#   int_0^{r_c} r^2 e^{-8r} dr = 1/256 - e^{-8 r_c}(r_c^2/8 + r_c/32 + 1/256)
#   Q_ae = 256 * (above) = 1 - e^{-8 r_c}(32 r_c^2 + 8 r_c + 1)
alpha = 2.0 * Z
Q_ae = 1.0 - np.exp(-alpha * R_C) * (32.0 * R_C**2 + 8.0 * R_C + 1.0)
Q_ae_num, _ = quad(lambda r: u_ae(r) ** 2, 0.0, R_C)
assert abs(Q_ae - Q_ae_num) < 1e-10, (
    f"Q_ae closed form vs quadrature mismatch: {Q_ae} vs {Q_ae_num}"
)


# ---------------------------------------------------------------------------
# Troullier-Martins pseudo-wavefunction
# ---------------------------------------------------------------------------
#
#   phi(r) = r * exp(p(r)),   p(r) = c_0 + c_1 r^2 + c_2 r^4 + c_3 r^6
#
# Conditions at r_c (Z = 4):
#   (1) value:  p(r_c)         = ln(16) - 4 r_c         -> sets c_0
#   (2) slope:  1/r_c + p'(r_c) = 1/r_c - 4             -> p'(r_c) = -4
#   (3) curv.:  2 p'(r_c)/r_c + p'(r_c)^2 + p''(r_c) = u''/u(r_c) = 16 - 8/r_c
#   (4) norm:   int_0^{r_c} phi^2 dr = Q_ae
#
# (2), (3), (4) are three equations in (c_1, c_2, c_3); (4) is
# transcendental and the only nonlinear one.  Solved with fsolve
# starting from the linear-only solution (c_3 = 0).


def phi_value_condition(c):
    """c_0 such that phi(r_c) = u_ae(r_c)."""
    c1, c2, c3 = c
    return np.log(16.0) - Z * R_C - c1 * R_C**2 - c2 * R_C**4 - c3 * R_C**6


def phi_first_deriv_condition(c):
    """p'(r_c) + Z = 0  (i.e., p'(r_c) = -Z = -4)."""
    c1, c2, c3 = c
    return 2.0 * c1 * R_C + 4.0 * c2 * R_C**3 + 6.0 * c3 * R_C**5 + Z


def phi_second_deriv_condition(c):
    """2 p'(r_c)/r_c + p'(r_c)^2 + p''(r_c) = u''/u(r_c)."""
    c1, c2, c3 = c
    p_prime = 2.0 * c1 * R_C + 4.0 * c2 * R_C**3 + 6.0 * c3 * R_C**5
    p_dd = 2.0 * c1 + 12.0 * c2 * R_C**2 + 30.0 * c3 * R_C**4
    u_dd_over_u = u_dd_at_rc / u_at_rc
    return 2.0 * p_prime / R_C + p_prime**2 + p_dd - u_dd_over_u


def phi_norm_condition(c):
    """int_0^{r_c} phi^2 dr - Q_ae = 0."""
    c1, c2, c3 = c
    c0 = phi_value_condition(c)

    def integrand(r):
        return r**2 * np.exp(
            2.0 * c0 + 2.0 * c1 * r**2 + 2.0 * c2 * r**4 + 2.0 * c3 * r**6
        )

    Q_ps, _ = quad(integrand, 0.0, R_C, limit=200)
    return Q_ps - Q_ae


def system(c):
    return [
        phi_first_deriv_condition(c),
        phi_second_deriv_condition(c),
        phi_norm_condition(c),
    ]


# Initial guess: linear solution (c_3 = 0) of (2) and (3):
#   c_1 = -6 c_2 r_c^2,  c_2 = 1/(2 r_c^3).
c_init = np.array([-2.0, 1.0 / (2.0 * R_C**3), 0.0])
c_sol, info, ier, msg = fsolve(system, c_init, full_output=True, xtol=1e-14)
# fsolve may return ier=3 ("no further improvement in the approximate
# solution is possible") once it has converged to machine precision
# but the requested xtol is tighter than that.  Treat any ier in {1, 3}
# as convergence; the residual check below is the real acceptance test.
assert ier in (1, 3), f"fsolve did not converge: ier={ier}, msg={msg}"

c1, c2, c3 = c_sol
c0 = phi_value_condition(c_sol)
residual = np.array(system(c_sol))
assert np.max(np.abs(residual)) < 1e-7, f"residual too large: {residual}"


def phi_pseudo(r):
    """Pseudo-wavefunction, valid for all r > 0."""
    r = np.asarray(r, dtype=float)
    out = np.empty_like(r)
    inside = r <= R_C
    outside = ~inside
    out[inside] = r[inside] * np.exp(
        c0 + c1 * r[inside] ** 2 + c2 * r[inside] ** 4 + c3 * r[inside] ** 6
    )
    out[outside] = u_ae(r[outside])
    return out


def _v_ps_inside(r):
    """Pseudo-potential at r > 0 inside r_c (no r=0 handling)."""
    p_prime = 2.0 * c1 * r + 4.0 * c2 * r**3 + 6.0 * c3 * r**5
    p_dd = 2.0 * c1 + 12.0 * c2 * r**2 + 30.0 * c3 * r**4
    return E_0 + 0.5 * (2.0 * p_prime / r + p_prime**2 + p_dd)


def v_pseudo(r):
    """Pseudo-potential, valid for all r > 0.

    For r <= r_c:  V_ps(r) = E_0 + 1/2 [ 2 p'(r)/r + p'(r)^2 + p''(r) ]
    For r >  r_c:  V_ps(r) = -Z/r  (the all-electron Coulomb tail).
    At r = 0 we use the analytic limit (E_0 + 3 c_1).
    """
    r = np.asarray(r, dtype=float)
    out = np.empty_like(r)
    inside = r <= R_C
    outside = ~inside
    r_in = r[inside]
    # Compute the inside branch, guarding r=0 against division by zero
    # by substituting a safe value and overwriting the r=0 entries
    # with the analytic limit after the fact.  We must assign into
    # `out` directly with a combined boolean mask -- `out[inside][...]`
    # would modify a temporary copy and be lost.
    r_safe = np.where(r_in <= 0.0, 1.0, r_in)
    p_prime = 2.0 * c1 * r_safe + 4.0 * c2 * r_safe**3 + 6.0 * c3 * r_safe**5
    p_dd = 2.0 * c1 + 12.0 * c2 * r_safe**2 + 30.0 * c3 * r_safe**4
    val = E_0 + 0.5 * (2.0 * p_prime / r_safe + p_prime**2 + p_dd)
    val = np.where(r_in <= 0.0, E_0 + 3.0 * c1, val)
    out[inside] = val
    out[outside] = -Z / r[outside]
    return out


# Verify continuity of V_ps at r_c.
v_in_at_rc = float(_v_ps_inside(np.array([R_C])).item())
v_out_at_rc = -Z / R_C


# ---------------------------------------------------------------------------
# Print key numerical results
# ---------------------------------------------------------------------------

print("Troullier-Martins pseudopotential, fictitious 1-D atom (Z=4, l=0)")
print("=" * 72)
print(f"  Z             = {Z}")
print(f"  r_c           = {R_C} a_0")
print(f"  E_0           = {E_0} E_h")
print()
print(f"  c_0           = {c0:+.6f}")
print(f"  c_1           = {c1:+.6f}")
print(f"  c_2           = {c2:+.6f}")
print(f"  c_3           = {c3:+.6f}")
print(f"  residual      = {np.max(np.abs(residual)):.2e}")
print()
print(f"  V_ps(r_c^-)   = {v_in_at_rc:+.6f}")
print(f"  V_ps(r_c^+)   = {v_out_at_rc:+.6f}")
print(f"  diff          = {v_in_at_rc - v_out_at_rc:+.2e}")
print(f"  V_ps(0) lim   = {E_0 + 3.0 * c1:+.6f}")
print()


# ---------------------------------------------------------------------------
# Test 1: box-eigenvalue test (L = 10 a_0 vs L = 20 a_0, h = 0.02 a_0)
# ---------------------------------------------------------------------------


def box_lowest_eig(L, h, v_func):
    """Lowest eigenvalue of H = -1/2 d^2/dr^2 + V on [0, L] with
    Dirichlet BCs, on a cell-centered grid with spacing h.

    Cell-centered grid: r_i = (i + 1/2) h, i = 0, ..., N-1, N = L/h.
    Ghost points at r = 0 and r = L carry u = 0; the FD stencil at
    the boundary cells reduces to a regular tridiagonal row.
    """
    N = int(round(L / h))
    r = (np.arange(N) + 0.5) * h
    V = v_func(r)
    diag = V + 1.0 / h**2
    off = -1.0 / (2.0 * h**2) * np.ones(N - 1)
    eigvals = eigh_tridiagonal(diag, off, eigvals_only=True)
    return float(eigvals[0])


H_GRID = 0.02
eig_10 = box_lowest_eig(10.0, H_GRID, v_pseudo)
eig_20 = box_lowest_eig(20.0, H_GRID, v_pseudo)
eig_diff_mEh = (eig_20 - eig_10) * 1000.0  # mE_h

print("Box-eigenvalue test (lowest eigenvalue on [0, L] with Dirichlet BCs)")
print("-" * 72)
print(f"  h             = {H_GRID} a_0")
print(f"  L = 10 a_0    :  eps = {eig_10:+.8f} E_h")
print(f"  L = 20 a_0    :  eps = {eig_20:+.8f} E_h")
print(f"  |eps(20) - eps(10)| = {abs(eig_diff_mEh):.4f} mE_h")
assert abs(eig_diff_mEh) < 1.0, "box-eigenvalue test FAILED: diff > 1 mE_h"
print("  --> pass (diff < 1 mE_h)")
print()


# ---------------------------------------------------------------------------
# Test 2: logarithmic derivative via Numerov
# ---------------------------------------------------------------------------


def log_deriv(E, r_c_target, V_eff, h=0.001):
    """D_l(E; r_c_target) = u'(r_c_target)/u(r_c_target) via Numerov.

    Schr: u'' = -k^2 u with k^2 = 2(E - V_eff).  BC: u(0) = 0,
    u(h) = h (linear near r=0 for l=0).
    """
    N = int(round(r_c_target / h))
    if N < 2:
        raise ValueError("grid too small for Numerov")
    r = np.arange(N + 1) * h
    k2 = 2.0 * (E - V_eff(r))
    u = np.zeros(N + 1)
    u[0] = 0.0
    u[1] = h
    prefac = h**2 / 12.0
    for n in range(1, N):
        num = 2.0 * u[n] * (1.0 - 5.0 * prefac * k2[n]) - u[n - 1] * (
            1.0 + prefac * k2[n - 1]
        )
        den = 1.0 + prefac * k2[n + 1]
        u[n + 1] = num / den
    return (u[N] - u[N - 1]) / (h * u[N])


def v_ae_eff(r):
    """AE effective potential for l=0:  -Z/r, regularised at r=0."""
    r = np.asarray(r, dtype=float)
    out = np.empty_like(r)
    nz = r > 0
    out[nz] = -Z / r[nz]
    out[~nz] = -Z / 1e-3
    return out


def v_ps_eff(r):
    """Pseudo effective potential for l=0 (no centrifugal term)."""
    return v_pseudo(r)


E_grid = np.linspace(E_0 - 0.5, E_0 + 0.5, 201)
D_ae = np.array([log_deriv(E, R_C, v_ae_eff, h=0.001) for E in E_grid])
D_ps = np.array([log_deriv(E, R_C, v_ps_eff, h=0.001) for E in E_grid])

i0 = np.argmin(np.abs(E_grid - E_0))
print(f"Logarithmic-derivative test at r_c = {R_C} a_0")
print("-" * 72)
print(f"  D_0^ae(E_0)   = {D_ae[i0]:+.6f} a_0^-1")
print(f"  D_0^ps(E_0)   = {D_ps[i0]:+.6f} a_0^-1")
print(f"  analytic      = {log_deriv_at_rc:+.6f} a_0^-1  (u_ae'/u_ae at r_c)")
print()


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

r_grid = np.linspace(1e-3, 6.0, 1000)
u_vals = u_ae(r_grid)
phi_vals = phi_pseudo(r_grid)
v_ae_vals = -Z / r_grid
v_ps_vals = v_pseudo(r_grid)

# Brand palette (same as chapter 00 / 04 / 08.01 for consistency).
COLOR_AE = "#3d3d3a"  # warm dark grey for all-electron
COLOR_PS = "#cc785c"  # coral (primary) for pseudo
COLOR_RC = "#a09d96"  # muted for the cutoff marker
GRID_ALPHA = 0.2

fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2], hspace=0.32, wspace=0.25)

# ----- top-left: wavefunctions -----
ax = fig.add_subplot(gs[0, 0])
ax.plot(
    r_grid,
    u_vals,
    color=COLOR_AE,
    linewidth=2.0,
    label=r"All-electron $u_{1s}(r) = 16\,r\,e^{-4r}$",
)
ax.plot(
    r_grid,
    phi_vals,
    color=COLOR_PS,
    linewidth=2.0,
    label=r"Pseudo $\phi_{ps}(r)$ (TM, $r_c=1.5\,a_0$)",
)
ax.axvline(
    R_C,
    color=COLOR_RC,
    linestyle="--",
    linewidth=0.9,
    alpha=0.7,
    label=r"$r_c = 1.5\,a_0$",
)
ax.set_xlabel(r"$r\;[a_0]$")
ax.set_ylabel(r"$\phi(r)$")
ax.set_title("Wavefunction")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.set_xlim(0.0, 6.0)
ax.set_ylim(0.0, None)
ax.grid(True, alpha=GRID_ALPHA)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

# ----- top-right: potentials -----
ax = fig.add_subplot(gs[0, 1])
clip = 5.0
v_ae_plot = np.clip(v_ae_vals, -clip, clip)
ax.plot(
    r_grid,
    v_ae_plot,
    color=COLOR_AE,
    linewidth=2.0,
    label=r"All-electron $V = -4/r$",
)
ax.plot(r_grid, v_ps_vals, color=COLOR_PS, linewidth=2.0, label=r"Pseudo $V_{ps}(r)$")
ax.axvline(R_C, color=COLOR_RC, linestyle="--", linewidth=0.9, alpha=0.7)
ax.set_xlabel(r"$r\;[a_0]$")
ax.set_ylabel(r"$V(r)\;[\mathrm{E_h}]$")
ax.set_title("Potential")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.set_xlim(0.0, 6.0)
ax.grid(True, alpha=GRID_ALPHA)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

# ----- bottom (wide): logarithmic derivative -----
ax = fig.add_subplot(gs[1, :])
ax.plot(
    E_grid,
    D_ae,
    color=COLOR_AE,
    linewidth=2.0,
    label=r"All-electron $D_0(E; r_c)$",
)
ax.plot(
    E_grid,
    D_ps,
    color=COLOR_PS,
    linewidth=2.0,
    label=r"Pseudo $D_0(E; r_c)$",
)
ax.axvline(
    E_0,
    color=COLOR_RC,
    linestyle="--",
    linewidth=0.9,
    alpha=0.7,
    label=rf"$E_0 = {E_0}\,E_h$",
)
ax.set_xlabel(r"$E\;[\mathrm{E_h}]$")
ax.set_ylabel(r"$D_0(E; r_c)\;[a_0^{-1}]$")
ax.set_title(r"Logarithmic derivative at $r_c$ (transferability test)")
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.grid(True, alpha=GRID_ALPHA)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.suptitle(
    "Troullier-Martins pseudopotential transferability, "
    rf"fictitious 1-D atom $Z=4$, $l=0$, $r_c = {R_C}\,a_0$",
    fontsize=12,
)

# Save with an absolute path under the script's own directory.
here = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(here, "plots")
os.makedirs(plots_dir, exist_ok=True)
out = os.path.join(plots_dir, "02-pseudopotential-transferability.png")
fig.savefig(out, dpi=120, bbox_inches="tight")
plt.close(fig)
print(f"Wrote {out}")
