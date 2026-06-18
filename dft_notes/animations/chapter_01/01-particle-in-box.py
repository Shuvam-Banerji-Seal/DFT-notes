"""
01-particle-in-box.py
=====================

The first four particle-in-a-box eigenfunctions, animated.

Scene graph
-----------
1.  Title at the top: "Particle in a box: the first four eigenstates".
2.  Subtitle (smaller, below the title):
        "ψ_n(x) = √(2/L) sin(nπx/L)  ·  E_n = n²·π²/(2mL²)"
3.  Draw the coordinate system and the infinite walls (red bars at
    x = 0 and x = L).  The x-axis runs from 0 to L + 0.4 with
    6 ticks; the y-axis runs from -1.4 to 1.4.
4.  For n = 1, 2, 3, 4 (sequenced):
      - Update the *info panel* in the top-left corner with the
        current state's badge ("n = 1"), the energy
        ("E_1 = 4.93 E_h"), and the number of nodes
        ("nodes: 0")
      - Plot ψ_n(x) on the axes in a distinct colour
      - Plot |ψ_n(x)|² underneath the ψ curve in the same
        colour at 0.5 opacity
      - Animate a "particle" dot moving along the ψ curve
        (it samples 0, 0.25, 0.5, 0.75, 1.0 of the arc length)
5.  Hold the last frame for a beat, then fade in a summary line at
    the bottom: "n² quantises the energy; the nodes sit at the walls."

Layout (why this version has no overlap)
----------------------------------------
The OLD script stacked the four equations on the right side of the
plot.  By state 4 the equation text reached y = -1.1, which is
*below* the x-axis (at y = -1.4) and overlapped with the
"x = 0" / "x = L" axis labels and the bottom-of-screen summary
text.  The hydrogen-orbital script had the same problem with
six energy labels stacking on the right.

This version uses a *single fixed info panel* in the top-left
corner.  The panel's content is updated for each state with
`Transform` so the text appears in the same place every time,
not stacked.  The plot is the only thing that changes between
states, so the eye is drawn to the new curve without having
to read a moving text block.

Why this animation lives in chapter 01's animations folder:
- it is the simplest non-trivial quantum-mechanical system
- it is the first eigenstate problem a chemistry student meets
- it sets the visual idiom (axes, wavefunctions drawn as curves) used
  by every later animation

Run from the repo root:
    manim -qm dft_notes/animations/chapter_01/01-particle-in-box.py ParticleInBox
Writes to:
    dft_notes/animations/chapter_01/videos/particle_in_box/720p30/ParticleInBox.mp4
    (a small post-process step renames to
    dft_notes/animations/chapter_01/videos/01-particle-in-box.mp4
    and captures the poster frame.)
"""

from manim import (
    Axes,
    BackgroundRectangle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    MoveAlongPath,
    Rectangle,
    ReplacementTransform,
    Scene,
    Text,
    Transform,
    VGroup,
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


# ---- Colour palette (matches the rest of the site) ----------------------
COLOR_BG = "#1a1814"  # warm dark (matches site theme)
COLOR_WALL = "#cc785c"  # poppy coral (accent)
COLOR_TITLE = "#e8e4d8"  # warm white
COLOR_SUBTITLE = "#a8a496"  # muted warm
COLOR_AXIS = "#7a7868"  # muted
COLOR_GRID = "#3a3830"  # subtle
COLORS_STATE = ["#5b9bd5", "#70ad47", "#ffc000", "#ed7d31"]  # 4 distinct hues
COLOR_PANEL = "#2a2820"  # dark panel
COLOR_PANEL_BORDER = "#4a4838"


def psi_n(n, x, L):
    """ψ_n(x) = √(2/L) sin(nπx/L) for a 1-D box of length L."""
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)


def E_n(n, L=1.0, m=1.0):
    """E_n = n²·π²/(2mL²) in Hartree atomic units.  With m = L = 1,
    E_1 = π²/2 ≈ 4.93 E_h."""
    return n * n * np.pi**2 / (2.0 * m * L**2)


class ParticleInBox(Scene):
    def construct(self):
        # ---- Configuration --------------------------------------------------
        L = 6.0  # length of the box (Manim units)
        x_max = L + 0.4
        y_max = 1.4
        n_states = 4
        E_first = E_n(1)  # used in the title and the first-state energy label

        # ---- Coordinate system ----------------------------------------------
        # The axes are placed centre-of-screen, but slightly offset to the
        # right so the info panel on the left has room.
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[-y_max, y_max, 0.5],
            x_length=7.0,
            y_length=4.0,
            tips=False,
            axis_config={
                "include_numbers": False,
                "stroke_width": 2,
                "color": COLOR_AXIS,
            },
        )
        axes.shift(RIGHT * 0.6 + DOWN * 0.3)

        # Boundary labels
        x0_label = MathTex("x = 0", font_size=26, color=COLOR_AXIS).next_to(
            axes.c2p(0, -y_max), DOWN, buff=0.2
        )
        xL_label = MathTex("x = L", font_size=26, color=COLOR_AXIS).next_to(
            axes.c2p(L, -y_max), DOWN, buff=0.2
        )

        # Infinite walls: two vertical bars at x = 0 and x = L
        wall_left = Rectangle(
            width=0.12,
            height=2 * y_max,
            fill_color=COLOR_WALL,
            fill_opacity=0.85,
            stroke_color=COLOR_WALL,
            stroke_width=0,
        ).move_to(axes.c2p(0, 0))
        wall_right = Rectangle(
            width=0.12,
            height=2 * y_max,
            fill_color=COLOR_WALL,
            fill_opacity=0.85,
            stroke_color=COLOR_WALL,
            stroke_width=0,
        ).move_to(axes.c2p(L, 0))

        # ---- Title + subtitle -----------------------------------------------
        title = Text(
            "Particle in a box: the first four eigenstates",
            font_size=32,
            color=COLOR_TITLE,
        ).to_edge(UP, buff=0.35)

        subtitle = MathTex(
            r"\psi_n(x) \;=\; \sqrt{\tfrac{2}{L}}\,\sin\!\left(\tfrac{n\pi x}{L}\right)"
            r"\,,\quad E_n \;=\; \frac{n^2 \pi^2}{2mL^2}",
            font_size=26,
            color=COLOR_SUBTITLE,
        ).next_to(title, DOWN, buff=0.18)

        # ---- Info panel (top-left, fixed position) ------------------------
        # The panel is a dark rounded rectangle that holds the state
        # badge, the energy, and the node count.  Its content is
        # *replaced* (via Transform) for each state, so the text never
        # stacks.  The panel itself stays put.
        panel = Rectangle(
            width=3.2,
            height=2.0,
            fill_color=COLOR_PANEL,
            fill_opacity=0.85,
            stroke_color=COLOR_PANEL_BORDER,
            stroke_width=1.5,
        ).to_corner(UL, buff=0.4)
        # Rounded corners for a softer look
        # (ManimCE's Rectangle doesn't have rounded_corners, but we
        # can use a simple RoundRect via the Create + Scale + pattern
        # if needed; the plain Rectangle is fine for now.)

        # The panel contents are stored as a list so we can Transform
        # between them.  The first one is for the "about to start"
        # state (no n selected).
        n_badge_template = MathTex("n = {n}", font_size=40, color=COLOR_TITLE)
        energy_template = MathTex(
            "E_{n} = {val:.2f}\\,E_h", font_size=28, color=COLOR_TITLE
        )
        nodes_template = MathTex("nodes: {k}", font_size=24, color=COLOR_SUBTITLE)

        # The "empty" state
        n_badge = MathTex("n = ?", font_size=40, color=COLOR_SUBTITLE)
        n_badge.move_to(panel.get_center() + UP * 0.55)
        energy_label = MathTex(
            "E_n = \\frac{\\pi^2}{2mL^2}", font_size=26, color=COLOR_SUBTITLE
        )
        energy_label.move_to(panel.get_center() + DOWN * 0.05)
        nodes_label = MathTex("k\\text{ nodes}", font_size=22, color=COLOR_SUBTITLE)
        nodes_label.move_to(panel.get_center() + DOWN * 0.65)

        # ---- Summary line (bottom) -----------------------------------------
        summary = Text(
            "n² quantises the energy;  the nodes sit at the walls.",
            font_size=24,
            color=COLOR_TITLE,
        ).to_edge(DOWN, buff=0.35)

        # ---- Animate the static elements ---------------------------------
        self.play(Write(title), run_time=1.0)
        self.play(Write(subtitle), run_time=1.0)
        self.play(
            Create(axes),
            Create(wall_left),
            Create(wall_right),
            Write(x0_label),
            Write(xL_label),
            run_time=1.5,
        )
        self.play(
            FadeIn(panel, scale=0.95),
            FadeIn(n_badge),
            FadeIn(energy_label),
            FadeIn(nodes_label),
            run_time=0.6,
        )
        self.wait(0.3)

        # ---- Per-state animation -----------------------------------------
        for n in range(1, n_states + 1):
            colour = COLORS_STATE[n - 1]
            # The ψ curve
            psi = axes.plot(
                lambda x: psi_n(n, x, L),
                x_range=[0.001, L - 0.001],
                color=colour,
                stroke_width=3.5,
                use_smoothing=True,
            )
            # The |ψ|² curve, drawn at half-height for clarity
            prob = axes.plot(
                lambda x: 0.5 * psi_n(n, x, L) ** 2,
                x_range=[0.001, L - 0.001],
                color=colour,
                stroke_width=1.5,
                use_smoothing=True,
            )

            # Update the panel: new badge, energy, node count.
            # The number of internal nodes is n - 1 (the wall nodes
            # at x=0 and x=L don't count as "nodes of the wavefunction"
            # in the chemistry convention).
            new_n_badge = MathTex(f"n = {n}", font_size=40, color=colour)
            new_n_badge.move_to(panel.get_center() + UP * 0.55)
            new_energy = MathTex(
                f"E_{{{n}}} = {E_n(n):.2f}\\,E_h", font_size=28, color=colour
            )
            new_energy.move_to(panel.get_center() + DOWN * 0.05)
            new_nodes = MathTex(
                f"{n - 1}\\,\\text{{nodes}}", font_size=24, color=COLOR_SUBTITLE
            )
            new_nodes.move_to(panel.get_center() + DOWN * 0.65)

            # Transform the panel content (replaces text in place, no
            # movement, no stacking)
            self.play(
                Transform(n_badge, new_n_badge),
                Transform(energy_label, new_energy),
                Transform(nodes_label, new_nodes),
                run_time=0.5,
            )

            # Draw the |ψ|² curve first (it's the "background" of the pair)
            self.play(Create(prob), run_time=0.6)
            # Then the ψ curve on top
            self.play(Create(psi), run_time=0.6)

            # Animate the "particle" dot along the ψ curve.
            # We sample 5 points along the curve (0, 0.25, 0.5, 0.75, 1.0)
            # and use MoveAlongPath for a smooth trace.
            from manim import MoveAlongPath

            dot = Dot(color=colour, radius=0.08).move_to(psi.point_from_proportion(0))
            self.play(FadeIn(dot, scale=0.5), run_time=0.2)
            self.play(MoveAlongPath(dot, psi), run_time=1.0, rate_func=lambda t: t)
            self.play(FadeOut(dot), run_time=0.2)

            # Pause briefly so the viewer can absorb the result
            self.wait(0.4)

        # ---- Summary -------------------------------------------------------
        self.play(Write(summary), run_time=1.5)
        self.wait(1.0)
