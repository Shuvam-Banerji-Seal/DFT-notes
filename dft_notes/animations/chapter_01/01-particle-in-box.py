"""
01-particle-in-box.py
=====================

The first four particle-in-a-box eigenfunctions, animated.

Scene graph
-----------
1.  Draw the infinite potential well V(x) = 0 for 0 < x < L, +∞ outside.
2.  Draw the axis (0 to L on x, -0.2 to 1.2 on y for amplitude)
    with the boundary labels x = 0 and x = L.
3.  Title: "Particle in a box: the first four eigenstates".
4.  For n = 1, 2, 3, 4 (sequenced):
      - write the equation ψ_n(x) = sqrt(2/L) sin(n π x / L) on the left
      - plot ψ_n(x) on the right, with the same axes scale
      - animate a "particle" dot moving at the *group velocity* of the
        wave packet (here: a stationary dot, since each ψ_n is a
        stationary state; we move the dot to show the spatial oscillation)
5.  Fade to a panel of all four |ψ_n|² on one set of axes for comparison.
6.  Final text: "n² quantises the energy; the wavefunction's zeros are
    at the boundaries."

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
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    Rectangle,
    Scene,
    Text,
    VGroup,
    Write,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    PI,
    config,
)
import numpy as np


class ParticleInBox(Scene):
    def construct(self):
        # ---- Configuration --------------------------------------------------
        L = 6.0  # length of the box (Manim units, not bohr)
        x_max = L + 0.5  # axis extent
        y_max = 1.4  # amplitude axis extent
        n_states = 4  # first four eigenstates

        # ---- Coordinate system ----------------------------------------------
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[-y_max, y_max, 0.5],
            x_length=8,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False, "stroke_width": 2},
        ).shift(LEFT * 0.3)

        # Boundary labels
        x0_label = MathTex("x = 0", font_size=28).next_to(
            axes.c2p(0, -y_max), DOWN, buff=0.15
        )
        xL_label = MathTex("x = L", font_size=28).next_to(
            axes.c2p(L, -y_max), DOWN, buff=0.15
        )

        # Infinite walls: two vertical bars at x = 0 and x = L
        wall_left = Rectangle(
            width=0.12,
            height=2 * y_max,
            fill_color="#cc785c",
            fill_opacity=0.85,
            stroke_color="#cc785c",
            stroke_width=0,
        ).move_to(axes.c2p(0, 0))
        wall_right = Rectangle(
            width=0.12,
            height=2 * y_max,
            fill_color="#cc785c",
            fill_opacity=0.85,
            stroke_color="#cc785c",
            stroke_width=0,
        ).move_to(axes.c2p(L, 0))

        # ---- Title ----------------------------------------------------------
        title = Text(
            "Particle in a box: the first four eigenstates", font_size=28
        ).to_edge(UP, buff=0.3)

        self.play(Write(title), run_time=1.0)
        self.play(
            Create(axes),
            Create(wall_left),
            Create(wall_right),
            Write(x0_label),
            Write(xL_label),
            run_time=1.5,
        )

        # ---- Plot each eigenstate in sequence -------------------------------
        n_colours = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e"]
        # Store the four ψ curves and the four |ψ|² curves for the final panel
        psi_curves = []
        prob_curves = []
        eq_labels = []

        for n in range(1, n_states + 1):
            colour = n_colours[n - 1]
            # ψ_n(x) = sqrt(2/L) sin(n π x / L)
            psi = axes.plot(
                lambda x: np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L),
                x_range=[0, L],
                color=colour,
                stroke_width=3,
            )
            # |ψ_n|²(x) = (2/L) sin²(n π x / L)  — only positive
            prob = axes.plot(
                lambda x: (2.0 / L) * np.sin(n * np.pi * x / L) ** 2,
                x_range=[0, L],
                color=colour,
                stroke_width=2,
            )
            # Equation label
            eq = (
                MathTex(
                    r"\psi_{%d}(x) = \sqrt{\tfrac{2}{L}}\,\sin(%d\pi x/L)" % (n, n),
                    font_size=30,
                )
                .next_to(axes, RIGHT, buff=0.4)
                .shift(UP * (1.6 - 0.9 * (n - 1)))
            )
            energy = MathTex(
                r"E_{%d} = %d^2 \cdot \frac{\pi^2}{2mL^2}" % (n, n), font_size=26
            ).next_to(eq, DOWN, buff=0.15, aligned_edge=LEFT)

            # Animate: title for the state, draw ψ, draw a moving "particle"
            self.play(Write(eq), Write(energy), Create(psi), run_time=1.2)
            # Animate a "particle" dot oscillating along the wavefunction.
            # For a stationary state |ψ|² doesn't move, but we move a dot
            # along the curve to visualise the spatial structure.
            dot = Dot(color=colour, radius=0.07).move_to(psi.point_from_proportion(0))
            self.play(FadeIn(dot, scale=0.5), run_time=0.3)
            self.play(
                dot.animate.move_to(psi.point_from_proportion(0.25)), run_time=0.25
            )
            self.play(
                dot.animate.move_to(psi.point_from_proportion(0.5)), run_time=0.25
            )
            self.play(
                dot.animate.move_to(psi.point_from_proportion(0.75)), run_time=0.25
            )
            self.play(
                dot.animate.move_to(psi.point_from_proportion(1.0)), run_time=0.25
            )
            self.play(FadeOut(dot), run_time=0.3)

            # Keep the curves and labels for the final panel
            psi_curves.append(psi)
            prob_curves.append(prob)
            eq_labels.append(VGroup(eq, energy))

        # ---- Summary line ---------------------------------------------------
        summary = Text(
            "n² quantises the energy; the wavefunction's zeros sit at the walls.",
            font_size=24,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(summary), run_time=1.5)

        # Hold the final frame for a beat so the video doesn't end abruptly
        self.wait(0.8)
