"""
02-hydrogen-orbitals.py
========================

The first six hydrogen-atom radial eigenfunctions, animated.

Scene graph
-----------
1.  Title at the top: "Hydrogen atom: the first nine orbitals".
2.  Subtitle: "R_{nℓ}(r) for (n,ℓ) = (1,0), (2,0), (2,1), (3,0), (3,1), (3,2)".
3.  Draw the coordinate system (r on x-axis, R(r) on y-axis) and a
    horizontal reference line at R = 0.
4.  For each (n, ℓ) in the list above (sequenced):
      - Update the *info panel* in the top-left corner with the
        current orbital's name ("1s", "2s", "2p", "3s", "3p", "3d"),
        its quantum numbers, the energy E_n = -1/(2n²) E_h, and
        the mean radius ⟨r⟩_{nℓ} in bohr.
      - Plot R_{nℓ}(r) in a distinct colour
      - Draw a vertical line at the mean radius ⟨r⟩_{nℓ}, with a
        small label "⟨r⟩ = X.X a_0" placed *above* the line at a
        fixed height (so the label never moves position between
        orbitals and never collides with the x-axis labels).
      - Animate a "particle" dot moving along the radial function
5.  Final panel: show the energy formula and a short summary at
    the bottom.

Layout (why this version has no overlap)
----------------------------------------
The OLD script stacked six energy+orbital labels on the right side
of the plot, plus a mean-radius label that moved with the radius
position.  By orbital 3d the right side had 7 text bands packed
into 270px of vertical space, with the mean-radius label (which
moves to larger r for higher n) overlapping the orbital labels.

This version uses:
- A *single fixed info panel* in the top-left corner.  The
  panel's content is replaced (via Transform) for each orbital,
  so the text never stacks.
- A small, fixed-position "⟨r⟩" label at a *fixed x* (4 a_0)
  for every orbital.  The line itself is at r_mean (so the line
  moves correctly), but the label never moves.
- The 6 curves are plotted one at a time, in the centre of the
  screen, with no text on the right side of the plot.

Why this animation lives in chapter 01's animations folder:
- the hydrogen atom is the only analytically-solvable
  many-body-free system, and its orbitals are the building
  block of every chemistry argument from hybridisation to
  crystal-field theory
- it complements the particle-in-box animation (same idiom, one
  dimension higher)

Run from the repo root:
    manim -qm dft_notes/animations/chapter_01/02-hydrogen-orbitals.py HydrogenOrbitals
Writes to:
    dft_notes/animations/chapter_01/videos/hydrogen_orbitals/720p30/HydrogenOrbitals.mp4
    (a small post-process step renames to
    dft_notes/animations/chapter_01/videos/02-hydrogen-orbitals.mp4
    and captures the poster frame.)
"""

from manim import (
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    MoveAlongPath,
    Rectangle,
    Scene,
    Text,
    Transform,
    Write,
    UL,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    config,
)
import numpy as np
from scipy.special import genlaguerre, factorial


# ---- Colour palette (matches the rest of the site) ----------------------
COLOR_BG = "#1a1814"
COLOR_TITLE = "#e8e4d8"
COLOR_SUBTITLE = "#a8a496"
COLOR_AXIS = "#7a7868"
COLOR_GRID = "#3a3830"
COLOR_PANEL = "#2a2820"
COLOR_PANEL_BORDER = "#4a4838"
COLORS_ORBITAL = ["#5b9bd5", "#70ad47", "#ffc000", "#ed7d31", "#a5a5a5", "#264478"]


def R_nl(n, l, r):
    """Hydrogen radial wavefunction R_{nℓ}(r) in atomic units.

    R_{nℓ}(r) = (2/n)² * sqrt((n-ℓ-1)! / (2n(n+ℓ)!)) * exp(-r/n) *
                (2r/n)^ℓ * L_{n-ℓ-1}^{2ℓ+1}(2r/n)
    """
    rho = 2.0 * r / n
    norm = np.sqrt((2.0 / n) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    L = genlaguerre(n - l - 1, 2 * l + 1)
    # At r = 0, R_{nℓ} is non-zero only for ℓ = 0
    if l > 0:
        return np.where(r > 0, norm * np.exp(-rho / 2.0) * rho**l * L(rho), 0.0)
    else:
        return np.where(
            r > 0, norm * np.exp(-rho / 2.0) * L(rho), 2.0 * (1.0 / n) ** 1.5
        )


def mean_r(n, l):
    """Mean radius ⟨r⟩_{nℓ} = a₀ · (3n² - ℓ(ℓ+1)) / 2."""
    return (3.0 * n * n - l * (l + 1)) / 2.0


def orbital_label(n, l):
    """The chemistry label for the orbital: 1s, 2s, 2p, 3s, 3p, 3d, ..."""
    s = ["s", "p", "d", "f", "g", "h"][l]
    return f"{n}{s}"


class HydrogenOrbitals(Scene):
    def construct(self):
        # ---- Configuration --------------------------------------------------
        r_max = 20.0
        y_max = 0.6  # amplitude scale (R_max ≈ 0.6 for 1s)
        orbitals = [
            (1, 0),  # 1s
            (2, 0),  # 2s
            (2, 1),  # 2p
            (3, 0),  # 3s
            (3, 1),  # 3p
            (3, 2),  # 3d
        ]

        # Fixed position for the mean-radius label (in DATA coordinates
        # of the r axis).  Placing it at r = 4 a_0 keeps it in the
        # left half of the plot, well clear of the r-axis label at
        # the right end.  The label TEXT is at this fixed x; the
        # VERTICAL LINE that indicates the mean radius is at the
        # actual r_mean (so the line moves but the label doesn't).
        MEAN_LABEL_X = 4.0

        # ---- Coordinate system ----------------------------------------------
        axes = Axes(
            x_range=[0, r_max, 5],
            y_range=[-y_max, y_max, 0.2],
            x_length=7.5,
            y_length=4.0,
            tips=False,
            axis_config={
                "include_numbers": False,
                "stroke_width": 2,
                "color": COLOR_AXIS,
            },
        )
        axes.shift(RIGHT * 0.4 + DOWN * 0.2)

        # x label
        x_label = MathTex("r \\;(a_0)", font_size=28, color=COLOR_AXIS).next_to(
            axes.x_axis, RIGHT, buff=0.2
        )

        # Zero line
        zero_line = axes.plot(
            lambda r: 0,
            x_range=[0, r_max],
            color=COLOR_GRID,
            stroke_width=1,
            use_smoothing=False,
        )

        # ---- Title + subtitle -----------------------------------------------
        title = Text(
            "Hydrogen atom: the first nine orbitals",
            font_size=32,
            color=COLOR_TITLE,
        ).to_edge(UP, buff=0.35)
        # Short subtitle on a single line.  The full list of orbitals
        # is shown in the info panel; the subtitle just announces
        # what's being plotted.
        subtitle = Text(
            "radial eigenfunctions  R_{nℓ}(r)  for  n = 1, 2, 3  and  ℓ = 0, 1, 2",
            font_size=22,
            color=COLOR_SUBTITLE,
        ).next_to(title, DOWN, buff=0.2)

        # ---- Info panel (top-left, fixed position) ------------------------
        panel = Rectangle(
            width=3.2,
            height=2.4,
            fill_color=COLOR_PANEL,
            fill_opacity=0.85,
            stroke_color=COLOR_PANEL_BORDER,
            stroke_width=1.5,
        ).to_corner(UL, buff=0.4)

        # The "empty" / start state of the panel
        header_text = MathTex("|n,\\ell\\rangle", font_size=28, color=COLOR_SUBTITLE)
        header_text.move_to(panel.get_center() + UP * 0.85)
        name_text = MathTex("?", font_size=48, color=COLOR_SUBTITLE)
        name_text.move_to(panel.get_center() + UP * 0.2)
        energy_text = MathTex(
            "E_n = -\\tfrac{1}{2n^2}\\,E_h", font_size=22, color=COLOR_SUBTITLE
        )
        energy_text.move_to(panel.get_center() + DOWN * 0.35)
        radius_text = MathTex(
            "\\langle r\\rangle = \\tfrac{3n^2 - \\ell(\\ell+1)}{2}\\,a_0",
            font_size=20,
            color=COLOR_SUBTITLE,
        )
        radius_text.move_to(panel.get_center() + DOWN * 0.95)

        # ---- Summary line (bottom) -----------------------------------------
        summary = Text(
            "E_n = -1/(2n²) Hartree  ·  ⟨r⟩_{nℓ} = (3n² - ℓ(ℓ+1))/2 · a₀",
            font_size=22,
            color=COLOR_TITLE,
        ).to_edge(DOWN, buff=0.35)

        # ---- Animate the static elements ---------------------------------
        self.play(Write(title), run_time=1.0)
        self.play(Write(subtitle), run_time=0.8)
        self.play(
            Create(axes),
            Create(zero_line),
            Write(x_label),
            run_time=1.2,
        )
        self.play(
            FadeIn(panel, scale=0.95),
            FadeIn(header_text),
            FadeIn(name_text),
            FadeIn(energy_text),
            FadeIn(radius_text),
            run_time=0.6,
        )
        self.wait(0.3)

        # ---- Per-orbital animation ----------------------------------------
        for idx, (n, l) in enumerate(orbitals):
            colour = COLORS_ORBITAL[idx]
            r_mean = mean_r(n, l)
            energy = -1.0 / (2 * n * n)

            # The radial function R_{nℓ}(r)
            curve = axes.plot(
                lambda r: R_nl(n, l, r),
                x_range=[0.001, r_max],
                color=colour,
                stroke_width=3.5,
                use_smoothing=True,
            )
            # |R_{nℓ}|² (probability density), drawn at half-scale
            prob = axes.plot(
                lambda r: 0.5 * R_nl(n, l, r) ** 2,
                x_range=[0.001, r_max],
                color=colour,
                stroke_width=1.5,
                use_smoothing=True,
            )

            # Mean-radius vertical line at the actual r_mean
            mean_line = axes.plot(
                lambda r: 0,
                x_range=[r_mean, r_mean],
                color=colour,
                stroke_width=1.2,
                use_smoothing=False,
            )
            # Small dot at the bottom of the line
            mean_dot = Dot(axes.c2p(r_mean, 0), color=colour, radius=0.05)
            # The mean-radius LABEL goes at FIXED x = MEAN_LABEL_X,
            # placed ABOVE the x-axis.  It never moves between orbitals
            # (only the value changes), so it can't collide with the
            # axis labels or the right-side info.
            mean_label = MathTex(
                f"\\langle r\\rangle = {r_mean:.1f}\\,a_0",
                font_size=20,
                color=colour,
            )
            mean_label.move_to(axes.c2p(MEAN_LABEL_X, y_max - 0.15))

            # Update the panel: new header, name, energy, radius.
            # All Transform() so they stay put (no stacking).
            new_header = MathTex(f"|{n},{l}\\rangle", font_size=28, color=colour)
            new_header.move_to(panel.get_center() + UP * 0.85)
            new_name = MathTex(
                f"\\text{{{orbital_label(n, l)}}}",
                font_size=48,
                color=colour,
            )
            new_name.move_to(panel.get_center() + UP * 0.2)
            new_energy = MathTex(
                f"E_{{{n}}} = {energy:.4f}\\,E_h", font_size=22, color=colour
            )
            new_energy.move_to(panel.get_center() + DOWN * 0.35)
            new_radius = MathTex(
                f"\\langle r\\rangle = {r_mean:.1f}\\,a_0", font_size=20, color=colour
            )
            new_radius.move_to(panel.get_center() + DOWN * 0.95)

            self.play(
                Transform(header_text, new_header),
                Transform(name_text, new_name),
                Transform(energy_text, new_energy),
                Transform(radius_text, new_radius),
                run_time=0.5,
            )

            # Draw the |R|² curve first (background)
            self.play(Create(prob), run_time=0.6)
            # Then the R curve
            self.play(Create(curve), run_time=0.6)
            # Then the mean-radius indicator (line + dot + label at
            # fixed x position)
            self.play(
                Create(mean_line),
                FadeIn(mean_dot, scale=0.5),
                Write(mean_label),
                run_time=0.4,
            )

            # Animate a "particle" dot moving along the radial function
            dot = Dot(color=colour, radius=0.08).move_to(curve.point_from_proportion(0))
            self.play(FadeIn(dot, scale=0.5), run_time=0.2)
            self.play(MoveAlongPath(dot, curve), run_time=0.9, rate_func=lambda t: t)
            self.play(FadeOut(dot), run_time=0.2)

            self.wait(0.3)

        # ---- Summary -------------------------------------------------------
        self.play(Write(summary), run_time=1.5)
        self.wait(1.0)
