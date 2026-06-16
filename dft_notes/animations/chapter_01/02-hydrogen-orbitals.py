"""
02-hydrogen-orbitals.py
========================

The first nine hydrogen atomic orbitals (n=1..3), animated.

Scene graph
-----------
1.  Title: "Hydrogen atom: the first nine orbitals".
2.  Draw a radial axis (r in a.u., from 0 to 20 a0) and a vertical
    energy axis (in Hartree, from -1.0 to 0).
3.  For each (n, l) in [(1,0), (2,0), (2,1), (3,0), (3,1), (3,2)]:
      - write the radial function R_{nl}(r) and the energy E_n
      - plot R_{nl}(r) and r * R_{nl}(r) (which is the radial
        amplitude of the wavefunction when squared)
      - add a vertical line at the average radius <r>_{nl}
4.  Final panel: all six |R_{nl}(r)|² on one set of axes, with
    a label "E_n = -1/(2n²) Hartree".

Why this animation lives in chapter 01's animations folder:
- the hydrogen atom is the only analytically-solvable
  multi-electron-free problem, and its orbitals are the building
  block of every chemistry argument from hybridisation to
  crystal-field theory
- it complements the particle-in-box animation (same idiom, one
  dimension higher)

Run from the repo root:
    manim -qm dft_notes/animations/chapter_01/02-hydrogen-orbitals.py HydrogenOrbitals
"""

from manim import (Axes, Create, Dot, FadeIn, FadeOut, MathTex,
                   Rectangle, Scene, Text, VGroup, Write,
                   UP, DOWN, LEFT, RIGHT, ORIGIN, PI, config)
import numpy as np
from scipy.special import genlaguerre, factorial


def R_nl(n, l, r):
    """Hydrogen radial wavefunction R_{nl}(r) in atomic units."""
    # rho = 2r / n
    rho = 2.0 * r / n
    # Normalisation: sqrt((2/n)^3 (n-l-1)! / (2n (n+l)!))
    norm = np.sqrt((2.0 / n) ** 3 * factorial(n - l - 1) / (2.0 * n * factorial(n + l)))
    # Laguerre polynomial L_{n-l-1}^{2l+1}(rho)
    L = genlaguerre(n - l - 1, 2 * l + 1)
    return norm * np.exp(-rho / 2.0) * rho ** l * L(rho)


def mean_r(n, l):
    """Mean radius <r>_{nl} = a0 * (3n^2 - l(l+1)) / 2."""
    return (3.0 * n * n - l * (l + 1)) / 2.0


class HydrogenOrbitals(Scene):
    def construct(self):
        # ---- Configuration --------------------------------------------------
        r_max = 20.0
        y_max = 0.5  # amplitude scale

        # ---- Coordinate system ----------------------------------------------
        axes = Axes(
            x_range=[0, r_max, 5],
            y_range=[-y_max, y_max, 0.1],
            x_length=9,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": False, "stroke_width": 2},
        ).shift(LEFT * 0.3)

        # x label
        x_label = MathTex("r \;(a_0)", font_size=28).next_to(
            axes.x_axis, RIGHT, buff=0.2
        )

        # ---- Title ----------------------------------------------------------
        title = Text(
            "Hydrogen atom: the first nine orbitals",
            font_size=28
        ).to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), Write(x_label), run_time=1.5)

        # ---- Orbitals (n, l) -----------------------------------------------
        nls = [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]
        n_colours = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf", "#bcbd22"]

        # We accumulate the curves and labels for the final panel
        all_curves = VGroup()

        for (n, l), colour in zip(nls, n_colours):
            # The radial function R_{nl}(r)
            R = axes.plot(
                lambda r: R_nl(n, l, r) if r > 0 else (0 if l > 0 else 2 * (1.0 ** 1.5) * np.exp(-1.0)),
                x_range=[0.001, r_max],
                color=colour, stroke_width=2.5,
            )
            # Vertical line at the mean radius
            mean_r_val = mean_r(n, l)
            mean_line = axes.plot(
                lambda r: 0,
                x_range=[mean_r_val, mean_r_val],
                color=colour, stroke_width=1, use_smoothing=False,
            )
            mean_dot = Dot(axes.c2p(mean_r_val, 0), color=colour, radius=0.06)
            mean_label = MathTex(
                r"\langle r\rangle_{%d,%d} = %.1f\,a_0" % (n, l, mean_r_val),
                font_size=22, color=colour
            ).next_to(mean_dot, UP, buff=0.15)

            # Energy label
            energy = -1.0 / (2 * n * n)
            energy_text = MathTex(
                r"E_{%d} = -\frac{1}{2\cdot %d^2} = %.4f\,E_h" % (n, n, energy),
                font_size=22
            ).next_to(axes, RIGHT, buff=0.4).shift(UP * (1.6 - 0.45 * (nls.index((n, l)))))

            # Orbital label
            orb_label = MathTex(
                r"|%d, %d\rangle" % (n, l),
                font_size=28, color=colour
            ).next_to(energy_text, DOWN, buff=0.1, aligned_edge=LEFT)

            self.play(
                Write(orb_label), Write(energy_text),
                Create(R),
                run_time=1.2
            )

            if n > 1:  # only show mean radius for n > 1 to avoid clutter
                self.play(
                    Create(mean_line), FadeIn(mean_dot, scale=0.5),
                    Write(mean_label),
                    run_time=0.8
                )

            all_curves.add(R.copy())

        # ---- Summary --------------------------------------------------------
        summary = Text(
            "Energy:  E_n = -1/(2n²) Hartree  ·  Mean radius:  ⟨r⟩_{nl} = (3n² - ℓ(ℓ+1))/2 · a₀",
            font_size=20
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(summary), run_time=2.0)

        # Hold the final frame
        self.wait(1.0)
