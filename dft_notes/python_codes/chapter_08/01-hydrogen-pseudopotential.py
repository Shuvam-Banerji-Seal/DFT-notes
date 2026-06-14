"""
01-hydrogen-pseudopotential.py
==============================

Construct a Troullier-Martins norm-conserving pseudopotential for
hydrogen (Z = 1) in the s-channel (l = 0) with cutoff r_c = 0.5 a_0.

The recipe is the one in Section 8.4 / 8.8 of chapter 08.  We:

  1. Compute the all-electron 1s wavefunction and its value, slope,
     and curvature at r_c.
  2. Parameterise the pseudo-wavefunction inside r_c as
        phi(r) = r * exp(c_0 + c_1 r^2 + c_2 r^4 + c_3 r^6)
     and enforce four matching conditions at r_c:  value,
     first derivative, second derivative, norm conservation.
  3. The first condition sets c_0; the other three give a 3 x 3
     nonlinear system for (c_1, c_2, c_3), solved with
     scipy.optimize.fsolve.
  4. Invert the radial Schroedinger equation to obtain V_ps(r) for
     r <= r_c, set V_ps(r) = -1/r for r > r_c.
  5. Plot the all-electron 1s and the pseudo wavefunction on the
     same axes (left panel), and the all-electron and pseudo
     potentials (right panel).

The script writes its plot to:

    dft_notes/python_codes/chapter_08/plots/01-hydrogen-pseudopotential.png

Run from the repo root:

    python dft_notes/python_codes/chapter_08/01-hydrogen-pseudopotential.py
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless -- no display required
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import fsolve


# ---------------------------------------------------------------------------
# All-electron reference (hydrogen 1s, atomic units)
# ---------------------------------------------------------------------------

# u_0(r) = 2 r exp(-r),  E_0 = -1/2 Hartree
E_0 = -0.5
R_C = 0.5  # cutoff in a_0


def u_ae(r):
    """All-electron radial wavefunction for hydrogen 1s."""
    return 2.0 * r * np.exp(-r)


def u_ae_prime(r):
    """First derivative of u_ae."""
    return 2.0 * (1.0 - r) * np.exp(-r)


def u_ae_double_prime(r):
    """Second derivative of u_ae."""
    return -2.0 * (2.0 - r) * np.exp(-r)


# Sanity check: the radial equation at a few test points.
for r_test in (0.1, 0.5, 1.0, 2.0):
    lhs = -0.5 * u_ae_double_prime(r_test) - (1.0 / r_test) * u_ae(r_test)
    rhs = E_0 * u_ae(r_test)
    assert abs(lhs - rhs) < 1e-12, f"radial check failed at r={r_test}"


# Value / derivative / curvature / log-derivative at r_c.
u_at_rc = u_ae(R_C)
u_prime_at_rc = u_ae_prime(R_C)
u_dd_at_rc = u_ae_double_prime(R_C)
log_deriv_at_rc = u_prime_at_rc / u_at_rc  # D_0(E_0) = 1/r_c - 1

# Core charge:  Q_0^{ae} = int_0^{r_c} u_ae^2 dr
# Closed form (verify by differentiation):
#   d/dr [-(r^2/2) e^{-2r}] = -(r - r^2) e^{-2r}
#   int r^2 e^{-2r} dr = -(e^{-2r}/2)(r^2 + r + 1/2)
# so  Q_0^{ae} = 1 - 2 e^{-2 r_c}(r_c^2 + r_c + 1/2).
Q_ae = 1.0 - 2.0 * np.exp(-2.0 * R_C) * (R_C**2 + R_C + 0.5)
# Numerical check via quadrature.
Q_ae_num, _ = quad(lambda r: u_ae(r) ** 2, 0.0, R_C)
assert abs(Q_ae - Q_ae_num) < 1e-12, "closed-form core charge disagrees with quadrature"


# ---------------------------------------------------------------------------
# Pseudo-wavefunction ansatz
# ---------------------------------------------------------------------------
#
#   phi(r) = r * exp(p(r)),   p(r) = c_0 + c_1 r^2 + c_2 r^4 + c_3 r^6
#
# The four conditions at r = r_c are
#
#   (1) value:    phi(r_c)     = u_ae(r_c)     ->  sets c_0
#   (2) 1st deriv: phi'(r_c)  = u_ae'(r_c)
#   (3) 2nd deriv: phi''(r_c) = u_ae''(r_c)   ->  continuous V_ps at r_c
#   (4) norm:      int_0^{r_c} phi^2 dr       =  Q_ae
#
# Conditions (2)-(4) are three equations in the three unknowns
# (c_1, c_2, c_3).  They are nonlinear (condition (3) is quadratic in
# the c's, condition (4) is transcendental) and we solve them with
# fsolve starting from the linear-only solution (c_3 = 0).


def phi_value_condition(c):
    """c_0 + c_1 r_c^2 + c_2 r_c^4 + c_3 r_c^6 - (ln 2 - r_c) = 0
    Implemented as:  return c_0 such that condition (1) holds."""
    c1, c2, c3 = c
    return np.log(2.0) - R_C - c1 * R_C**2 - c2 * R_C**4 - c3 * R_C**6


def phi_first_deriv_condition(c):
    """2 c_1 r_c + 4 c_2 r_c^3 + 6 c_3 r_c^5 + 1 = 0
    (since the 1/r_c terms cancel and the right-hand side is -1)."""
    c1, c2, c3 = c
    return 2.0 * c1 * R_C + 4.0 * c2 * R_C**3 + 6.0 * c3 * R_C**5 + 1.0


def phi_second_deriv_condition(c):
    """2 p'(r_c)/r_c + p'(r_c)^2 + p''(r_c) - u_dd/u_at_rc = 0."""
    c1, c2, c3 = c
    p_prime = 2.0 * c1 * R_C + 4.0 * c2 * R_C**3 + 6.0 * c3 * R_C**5
    p_dd = 2.0 * c1 + 12.0 * c2 * R_C**2 + 30.0 * c3 * R_C**4
    return 2.0 * p_prime / R_C + p_prime**2 + p_dd - (u_dd_at_rc / u_at_rc)


def phi_norm_condition(c):
    """int_0^{r_c} phi^2 dr - Q_ae = 0."""
    c1, c2, c3 = c
    c0 = phi_value_condition(c)

    def integrand(r):
        return (r**2) * np.exp(
            2.0 * c0 + 2.0 * c1 * r**2 + 2.0 * c2 * r**4 + 2.0 * c3 * r**6
        )

    Q_ps, _ = quad(integrand, 0.0, R_C, limit=200)
    return Q_ps - Q_ae


def system(c):
    """Stack the three nonlinear conditions on (c_1, c_2, c_3)."""
    return [
        phi_first_deriv_condition(c),
        phi_second_deriv_condition(c),
        phi_norm_condition(c),
    ]


# Initial guess from the linear-only (3-parameter) solution:
#   c_1 = -1.5,  c_2 = +1,  c_3 = 0.
c_init = np.array([-1.5, 1.0, 0.0])
c_sol, info, ier, msg = fsolve(system, c_init, full_output=True, xtol=1e-14)
assert ier == 1, f"fsolve did not converge: {msg}"

c1, c2, c3 = c_sol
c0 = phi_value_condition(c_sol)

# Sanity checks.
residual = np.array(system(c_sol))
assert np.max(np.abs(residual)) < 1e-9, f"residual too large: {residual}"

print("Troullier-Martins pseudopotential for hydrogen 1s (l=0, r_c=0.5 a_0)")
print("=" * 66)
print(f"  c_0 = {c0:+.6f}")
print(f"  c_1 = {c1:+.6f}")
print(f"  c_2 = {c2:+.6f}")
print(f"  c_3 = {c3:+.6f}")
print(f"  residual (max |f_i|) = {np.max(np.abs(residual)):.2e}")
print()
print(f"  All-electron  u_0(r_c)  = {u_at_rc:.6f}")
print(
    f"  Pseudo        phi(r_c)  = {R_C * np.exp(c0 + c1 * R_C**2 + c2 * R_C**4 + c3 * R_C**6):.6f}"
)
print(f"  All-electron  Q_0       = {Q_ae:.8f}  (closed form)")
Q_ps_num, _ = quad(
    lambda r: (r**2)
    * np.exp(2.0 * c0 + 2.0 * c1 * r**2 + 2.0 * c2 * r**4 + 2.0 * c3 * r**6),
    0.0,
    R_C,
)
print(f"  Pseudo        Q_0^ps    = {Q_ps_num:.8f}  (quadrature)")
print(f"  Log-deriv     D_0(r_c)  = {log_deriv_at_rc:.6f} a_0^-1")


# ---------------------------------------------------------------------------
# Pseudo-wavefunction and pseudo-potential
# ---------------------------------------------------------------------------


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


def v_pseudo(r):
    """Pseudo-potential, valid for all r > 0.

    For r <= r_c:  V_ps(r) = E_0 + (1/2) [ 2 p'(r)/r + p'(r)^2 + p''(r) ]
    For r >  r_c:  V_ps(r) = -1/r  (the all-electron Coulomb tail).

    Note: at r exactly equal to 0 we use the analytic limit (3 c_1 + E_0).
    """
    r = np.asarray(r, dtype=float)
    out = np.empty_like(r)
    inside = r <= R_C
    outside = ~inside
    r_in = r[inside]
    out[inside] = _v_ps_inside(r_in)
    # If r_in contains a zero, _v_ps_inside will return Inf or NaN for
    # the 2 p'(r)/r term; replace those entries with the analytic limit.
    zero_mask_inside = r_in <= 0.0
    if zero_mask_inside.any():
        out[inside][zero_mask_inside] = E_0 + 3.0 * c1
    out[outside] = -1.0 / r[outside]
    return out


def _v_ps_inside(r):
    """Pseudo-potential at r > 0 inside r_c (no r=0 handling)."""
    p_prime = 2.0 * c1 * r + 4.0 * c2 * r**3 + 6.0 * c3 * r**5
    p_dd = 2.0 * c1 + 12.0 * c2 * r**2 + 30.0 * c3 * r**4
    return E_0 + 0.5 * (2.0 * p_prime / r + p_prime**2 + p_dd)


# Verify continuity at r_c.
v_inside_at_rc = float(_v_ps_inside(np.array([R_C])))
v_outside_at_rc = -1.0 / R_C
print(
    f"  V_ps(r_c^-)  = {v_inside_at_rc:+.6f}  "
    f"V_ps(r_c^+) = {v_outside_at_rc:+.6f}  "
    f"diff = {v_inside_at_rc - v_outside_at_rc:+.2e}"
)
print(
    f"  V_ps(0)      = {E_0 + 3.0 * c1:+.6f}  (analytic limit, all-electron diverges)"
)
print()


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

# Use a grid that starts just above r = 0 to avoid the 1/r divergence
# of the all-electron potential.  We use 1000 points to make the
# transition at r_c visible.
r_grid = np.linspace(1e-3, 4.0, 1000)

u_vals = u_ae(r_grid)
phi_vals = phi_pseudo(r_grid)
v_ae_vals = -1.0 / r_grid
v_ps_vals = v_pseudo(r_grid)

# 2-panel figure:  wavefunctions (left),  potentials (right).
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# Brand palette (same as chapter 00 / 04 for consistency).
COLOR_AE = "#3d3d3a"  # warm dark grey for all-electron
COLOR_PS = "#cc785c"  # coral (primary) for pseudo
COLOR_RC = "#a09d96"  # muted for the cutoff marker
GRID_ALPHA = 0.2

# ----- left panel: wavefunctions -----
ax = axes[0]
ax.plot(
    r_grid,
    u_vals,
    color=COLOR_AE,
    linewidth=2.0,
    label=r"All-electron $u_{1s}(r) = 2r\,e^{-r}$",
)
ax.plot(
    r_grid,
    phi_vals,
    color=COLOR_PS,
    linewidth=2.0,
    label=r"Pseudo $\phi_{ps}(r)$ (TM, $r_c=0.5\,a_0$)",
)
ax.axvline(
    R_C,
    color=COLOR_RC,
    linestyle="--",
    linewidth=0.9,
    alpha=0.7,
    label=r"$r_c = 0.5\,a_0$",
)
ax.set_xlabel(r"$r\;[a_0]$")
ax.set_ylabel(r"$\phi(r)$")
ax.set_title("Hydrogen 1s: all-electron vs pseudo wavefunction")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.set_xlim(0.0, 4.0)
ax.set_ylim(0.0, 0.85)
ax.grid(True, alpha=GRID_ALPHA)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

# ----- right panel: potentials -----
ax = axes[1]
# Clip the all-electron potential so it doesn't blow up the y-axis
# (it diverges at the origin, but that's the point of the figure).
clip = 5.0
v_ae_plot = np.clip(v_ae_vals, -clip, clip)
ax.plot(
    r_grid, v_ae_plot, color=COLOR_AE, linewidth=2.0, label=r"All-electron $V = -1/r$"
)
ax.plot(r_grid, v_ps_vals, color=COLOR_PS, linewidth=2.0, label=r"Pseudo $V_{ps}(r)$")
ax.axvline(R_C, color=COLOR_RC, linestyle="--", linewidth=0.9, alpha=0.7)
ax.set_xlabel(r"$r\;[a_0]$")
ax.set_ylabel(r"$V(r)\;[\mathrm{E_h}]$")
ax.set_title(r"Pseudo-potential (finite at $r = 0$)")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.set_xlim(0.0, 4.0)
ax.set_ylim(-10.0, 5.0)
ax.grid(True, alpha=GRID_ALPHA)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.suptitle(
    "Troullier-Martins pseudopotential, hydrogen 1s, "
    r"$l=0$, $r_c = 0.5\,a_0$",
    fontsize=12,
)
fig.tight_layout()

# Save with an absolute path under the script's own directory.
here = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(here, "plots")
os.makedirs(plots_dir, exist_ok=True)
out = os.path.join(plots_dir, "01-hydrogen-pseudopotential.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"Wrote {out}")
