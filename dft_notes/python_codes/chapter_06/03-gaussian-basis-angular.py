"""
03-gaussian-basis-angular.py
============================
Visualisation of Cartesian Gaussian basis functions of
different angular momentum:

    s    :  g(r) = exp(-alpha r**2)
    p_x  :  g(r) = x exp(-alpha r**2)
    d_xy :  g(r) = x y exp(-alpha r**2)
    f_xyz:  g(r) = x y z exp(-alpha r**2)

These are the *unnormalised* Cartesian primitives that
underlie every contracted basis function we build in
chapter 06.  Plotting them as 2D contours makes the
angular structure visible: s is spherically symmetric, p
has one nodal plane, d has two, f has three.

All four functions are evaluated on a 2D grid in the xy
plane (z = 0).  The f_xyz function vanishes identically on
z = 0 (its third Cartesian factor is zero there), so for
that one panel we slice at z = z_offset = 0.5 a_0 to
expose the four lobes that survive when z != 0.

The exponent alpha is fixed at 0.5 a_0^-2 — small enough
that the Gaussian envelope is wide compared with the
angular polynomial, so the polynomial lobes are visible
inside the envelope.

Run from the repo root:
    python dft_notes/python_codes/chapter_06/03-gaussian-basis-angular.py

Writes its plot to:
    dft_notes/python_codes/chapter_06/plots/03-gaussian-basis-angular.png

Dependencies: numpy, matplotlib (headless via Agg).
"""

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")  # headless — no display required
import matplotlib.pyplot as plt


# ─── Parameters ────────────────────────────────────────────────────
ALPHA = 0.5  # Gaussian exponent, a_0^-2
GRID_HALF = 3.0  # plot range +/- GRID_HALF in each direction
NPTS = 301  # grid resolution per axis
Z_F_SLICE = 0.5  # z-offset for the f_xyz panel (a_0)


# ─── Cartesian Gaussian factories ─────────────────────────────────
def gauss_envelope(x, y, z, alpha):
    """Spherical Gaussian envelope exp(-alpha r**2)."""
    return np.exp(-alpha * (x * x + y * y + z * z))


def s_gauss(x, y, z, alpha):
    return gauss_envelope(x, y, z, alpha)


def px_gauss(x, y, z, alpha):
    return x * gauss_envelope(x, y, z, alpha)


def dxy_gauss(x, y, z, alpha):
    return x * y * gauss_envelope(x, y, z, alpha)


def fxyz_gauss(x, y, z, alpha):
    return x * y * z * gauss_envelope(x, y, z, alpha)


def main() -> None:
    # ─── Grid in the xy plane ─────────────────────────────────────
    xs = np.linspace(-GRID_HALF, GRID_HALF, NPTS)
    ys = np.linspace(-GRID_HALF, GRID_HALF, NPTS)
    X, Y = np.meshgrid(xs, ys, indexing="xy")

    # All four panels: (label, slice-z, function, has-sign)
    panels = [
        (r"$s$:  $\exp(-\alpha r^2)$", 0.0, s_gauss, False),
        (r"$p_x$:  $x\,\exp(-\alpha r^2)$", 0.0, px_gauss, True),
        (r"$d_{xy}$:  $x\,y\,\exp(-\alpha r^2)$", 0.0, dxy_gauss, True),
        (
            rf"$f_{{xyz}}$:  $x\,y\,z\,\exp(-\alpha r^2)$"
            rf"   (slice $z = {Z_F_SLICE}\,a_0$)",
            Z_F_SLICE,
            fxyz_gauss,
            True,
        ),
    ]

    # Evaluate each panel + report extrema.
    fields = []
    print(f"Gaussian basis functions, alpha = {ALPHA} a_0^-2")
    print(f"grid:  x, y in [-{GRID_HALF}, +{GRID_HALF}],  {NPTS} x {NPTS} points\n")
    print(f"{'panel':<48s} {'min':>12s} {'max':>12s}  {'nodal planes':>15s}")
    print("-" * 92)
    nodal_planes = {
        0: "0 (sign-definite)",
        1: "1 (x = 0)",
        2: "2 (x = 0, y = 0)",
        3: "3 (x = 0, y = 0, z = 0)",
    }
    for idx, (label, z0, func, _) in enumerate(panels):
        Z = func(X, Y, z0, ALPHA)
        fields.append(Z)
        plain = label.replace("$", "").replace("\\", "")
        # ASCII trim for the table
        short = plain.split(":")[0].strip()
        print(
            f"{short:<48s} {Z.min():>+12.4e} {Z.max():>+12.4e}  "
            f"{nodal_planes[idx]:>15s}"
        )

    # ─── Build the figure ─────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 9.0))
    axes = axes.ravel()

    # Use the same symmetric scale for sign-definite vs.
    # the absolute max for signed plots so colours mean the same
    # thing across panels.
    cmap_signed = "RdBu_r"  # blue = negative, red = positive
    cmap_pos = "viridis"  # for the s-function

    for ax, (label, z0, func, signed), Z in zip(axes, panels, fields):
        if signed:
            vmax = float(np.max(np.abs(Z)))
            if vmax == 0.0:
                vmax = 1.0
            levels = np.linspace(-vmax, vmax, 41)
            cf = ax.contourf(X, Y, Z, levels=levels, cmap=cmap_signed, extend="both")
            # zero-contour overlay
            ax.contour(
                X, Y, Z, levels=[0.0], colors="#3d3d3a", linewidths=0.8, linestyles="--"
            )
        else:
            vmax = float(Z.max())
            if vmax == 0.0:
                vmax = 1.0
            levels = np.linspace(0.0, vmax, 41)
            cf = ax.contourf(X, Y, Z, levels=levels, cmap=cmap_pos)

        ax.set_aspect("equal")
        ax.set_xlabel(r"$x$  (a$_0$)")
        ax.set_ylabel(r"$y$  (a$_0$)")
        ax.set_title(label, fontsize=11)
        ax.axhline(0.0, color="#3d3d3a", lw=0.5, alpha=0.4)
        ax.axvline(0.0, color="#3d3d3a", lw=0.5, alpha=0.4)
        ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
        ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
        cb = fig.colorbar(cf, ax=ax, shrink=0.85, pad=0.03)
        cb.ax.tick_params(labelsize=8)

    fig.suptitle(
        r"Cartesian Gaussian basis functions, "
        rf"$\alpha = {ALPHA}\,a_0^{{-2}}$",
        fontsize=13,
        y=1.00,
    )
    fig.tight_layout()

    here = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(here, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    out = os.path.join(plots_dir, "03-gaussian-basis-angular.png")
    fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
