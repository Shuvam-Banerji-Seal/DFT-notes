"""
01-dft-u.py
===========

LDA+U: the penalty functional.

A two-orbital atom. With U = 0 the (spin-)levels are degenerate and the
energy is indifferent to how the electron is spread -- the LDA failure.
The penalty term E_U = (U_eff/2) sum_i n_i (1 - n_i) costs energy only
for *fractional* occupations, so its minimum sits at integer n, and on
the level diagram the same U_eff splits the degenerate pair into lower
and upper Hubbard bands: the Mott gap.

Scene graph
-----------
1.  Title card.
2.  The penalty formula, written large (persistent header).
3.  LEFT : f(n) = n(1-n) on small axes -- inverted parabola,
    zero at n = 0, 1; max 1/4 at n = 1/2.
4.  The two cases as dots on the parabola:
    LDA delocalised (1/2, 1/2) -> E_U = U_eff/4  (coral, apex)
    integer (1, 0)             -> E_U = 0        (teal, base)
5.  RIGHT: two-level diagram; U = 0 degenerate (metal) ->
    U ramps up, levels split by U_eff (LHB / UHB).
6.  End card.

Run from the repo root:
    manim -qm dft_notes/animations/chapter_13/01-dft-u.py DFTPlusU
Writes to:
    dft_notes/animations/chapter_13/videos/...
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, Text, VGroup, Write, Create, FadeIn, FadeOut,
    Dot, DashedLine, Axes, DoubleArrow, Arrow, GrowArrow, Line, ValueTracker,
    Indicate, config, UP, DOWN, LEFT, RIGHT, UL, UR, DR, ORIGIN,
    YELLOW, smooth,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # fractional / LDA accent
TEALC = "#5db8a6"     # integer / insulator accent
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

# ------------------------------------------------------- layout constants
LEFT_X  = -3.55       # left-panel centre
RIGHT_X = 3.95        # right-panel centre

EPS_Y   = -0.55       # U = 0 level energy (right panel)
SPAN    = 1.05        # half-split at U = 1  (upper +SPAN/2, lower -SPAN/2)
XA0, XA1 = 2.95, 3.80 # upper-orbital line span
XB0, XB1 = 4.10, 4.95 # lower-orbital line span


class DFTPlusU(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex("LDA+U: the penalty functional",
                    color=INK, font_size=40).to_edge(UP, buff=0.45)
        subtitle = Tex("why fractional occupations cost energy",
                       color=DIM, font_size=26).next_to(title, DOWN, buff=0.18)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(subtitle),
                  title.animate.scale(0.75).to_edge(UP, buff=0.25),
                  run_time=0.8)

        # ------------------------------------------- 2. the big formula
        formula = MathTex(
            r"E_U \;=\;",
            r"\frac{U_{\mathrm{eff}}}{2}",
            r"\sum_i\;",
            r"n_i\,(1-n_i)",
            font_size=52,
        ).move_to(np.array([0.0, 2.25, 0.0]))
        formula[0].set_color(INK)
        formula[1].set_color(TEALC)
        formula[2].set_color(DIM)
        formula[3].set_color(CORAL)
        self.play(Write(formula), run_time=2.2)
        self.wait(2.6)

        # --------------------------------------------- 3. LEFT: parabola
        left_lbl = Tex(r"penalty per orbital:  $f(n) = n(1-n)$",
                       color=DIM, font_size=27).move_to(np.array([LEFT_X, 1.15, 0.0]))
        self.play(FadeIn(left_lbl), run_time=0.7)

        axes = Axes(
            x_range=[0, 1.2, 1], y_range=[0, 0.32, 0.1],
            x_length=4.4, y_length=2.7,
            tips=True,
            axis_config={"stroke_width": 2, "include_ticks": False,
                         "tip_width": 0.14, "tip_height": 0.14},
        ).move_to(np.array([LEFT_X, -0.75, 0.0]))
        curve = axes.plot(lambda t: t * (1.0 - t), x_range=[0, 1],
                          color=CORAL, stroke_width=6)
        self.play(Create(axes), run_time=1.1)
        self.play(Create(curve), run_time=1.8)
        self.wait(1.0)

        xticks = VGroup(*[
            MathTex(s, color=DIM, font_size=26).next_to(axes.c2p(v, 0.0),
                                                        DOWN, buff=0.18)
            for v, s in [(0.0, "0"), (0.5, r"\tfrac12"), (1.0, "1")]
        ])
        ytick = MathTex(r"\tfrac14", color=DIM,
                        font_size=26).next_to(axes.c2p(0.0, 0.25), LEFT, buff=0.15)
        xlbl = MathTex("n", color=DIM, font_size=28).next_to(
            axes.c2p(1.2, 0.0), DR, buff=0.12)
        flbl = MathTex("f(n)", color=DIM, font_size=28).next_to(
            axes.c2p(0.0, 0.32), UP, buff=0.12)
        dash_v = DashedLine(axes.c2p(0.5, 0.0), axes.c2p(0.5, 0.25),
                            color=DIM, stroke_width=2)
        dash_h = DashedLine(axes.c2p(0.0, 0.25), axes.c2p(0.5, 0.25),
                            color=DIM, stroke_width=2)
        self.play(FadeIn(xticks), FadeIn(ytick), FadeIn(xlbl), FadeIn(flbl),
                  Create(dash_v), Create(dash_h), run_time=1.0)
        self.wait(1.0)

        # ------------------------------------- 4. the two cases as dots
        dot_lda = Dot(axes.c2p(0.5, 0.25), radius=0.09, color=CORAL)
        lda_lbl = MathTex(r"n=\tfrac12", color=CORAL, font_size=26)\
            .move_to(axes.c2p(0.76, 0.115))
        self.play(FadeIn(dot_lda, scale=2.2), run_time=0.9)
        self.play(FadeIn(lda_lbl), run_time=0.8)
        self.wait(0.9)

        dot_int1 = Dot(axes.c2p(0.0, 0.0), radius=0.09, color=TEALC)
        dot_int2 = Dot(axes.c2p(1.0, 0.0), radius=0.09, color=TEALC)
        int1_lbl = MathTex(r"n=0", color=TEALC, font_size=24)\
            .next_to(dot_int1, UL, buff=0.13)
        int2_lbl = MathTex(r"n=1", color=TEALC, font_size=24)\
            .next_to(dot_int2, UR, buff=0.13)
        self.play(FadeIn(dot_int1, scale=2.2), FadeIn(dot_int2, scale=2.2),
                  run_time=1.0)
        self.play(FadeIn(int1_lbl), FadeIn(int2_lbl), run_time=0.8)
        self.wait(1.4)

        row_lda = MathTex(
            r"\text{LDA } (\tfrac12,\tfrac12):\;\;",
            r"E_U = \frac{U_{\mathrm{eff}}}{2}\Bigl(\tfrac14+\tfrac14\Bigr) = \frac{U_{\mathrm{eff}}}{4}",
            color=CORAL, font_size=29,
        ).move_to(np.array([LEFT_X, -2.85, 0.0]))
        self.play(Write(row_lda), run_time=1.4)
        self.wait(2.2)

        row_int = MathTex(
            r"\text{integer } (1,0):\;\;",
            r"E_U",
            r"\;=\;",
            r"\frac{U_{\mathrm{eff}}}{2}\,(0+0)",
            r"\;=\;",
            r"0",
            color=TEALC, font_size=29,
        ).move_to(np.array([LEFT_X, -3.50, 0.0]))
        row_int[5].set_color(YELLOW)
        self.play(Write(row_int), run_time=1.3)
        self.wait(2.0)

        # ----------------------------------- 5. RIGHT: level diagram
        right_lbl = Tex(r"the same atom, energy levels:",
                        color=DIM, font_size=27).move_to(np.array([RIGHT_X, 1.15, 0.0]))

        utracker = ValueTracker(0.0)

        upper = Line(np.array([XA0, EPS_Y, 0]), np.array([XA1, EPS_Y, 0]),
                     color=INK, stroke_width=6)
        lower = Line(np.array([XB0, EPS_Y, 0]), np.array([XB1, EPS_Y, 0]),
                     color=INK, stroke_width=6)

        def upd_upper(m):
            y = EPS_Y + 0.5 * SPAN * utracker.get_value()
            m.put_start_and_end_on(np.array([XA0, y, 0]), np.array([XA1, y, 0]))

        def upd_lower(m):
            y = EPS_Y - 0.5 * SPAN * utracker.get_value()
            m.put_start_and_end_on(np.array([XB0, y, 0]), np.array([XB1, y, 0]))

        upper.add_updater(upd_upper)
        lower.add_updater(upd_lower)

        cap_metal = Tex("$U = 0$: degenerate levels $\\Rightarrow$ metal",
                        color=DIM, font_size=26)\
            .move_to(np.array([RIGHT_X, -2.35, 0.0]))

        self.play(FadeIn(right_lbl), run_time=0.7)
        self.play(FadeIn(upper), FadeIn(lower), run_time=1.1)
        self.play(FadeIn(cap_metal), run_time=0.9)
        self.wait(2.2)

        # --- ramp U up: one .animate only, everything else via updaters
        self.play(utracker.animate.set_value(1.0),
                  run_time=4.6, rate_func=smooth)
        self.wait(1.2)

        # gap bracket, built at the final split (arrows cannot be resized)
        gap_arrow = DoubleArrow(
            np.array([5.35, EPS_Y - 0.5 * SPAN, 0]),
            np.array([5.35, EPS_Y + 0.5 * SPAN, 0]),
            buff=0, stroke_width=3, tip_length=0.16, color=YELLOW)
        gap_lbl = MathTex(r"U_{\mathrm{eff}}", color=YELLOW, font_size=32)\
            .next_to(gap_arrow, RIGHT, buff=0.18)

        uhb = MathTex(r"\text{UHB}", color=CORAL, font_size=30)\
            .move_to(np.array([2.55, EPS_Y + SPAN * 0.5, 0]))
        lhb = MathTex(r"\text{LHB}", color=TEALC, font_size=30)\
            .move_to(np.array([2.55, EPS_Y - SPAN * 0.5, 0]))
        self.play(FadeIn(uhb), FadeIn(lhb), run_time=1.0)
        self.wait(0.6)
        self.play(FadeIn(gap_arrow), FadeIn(gap_lbl), run_time=1.0)
        self.play(Indicate(gap_lbl, color=YELLOW), run_time=0.9)

        cap_split = Tex("with $U_{\\mathrm{eff}}>0$ the manifold splits",
                        color=INK, font_size=26)\
            .move_to(np.array([RIGHT_X, -2.35, 0.0]))
        self.play(FadeOut(cap_metal), run_time=0.5)
        self.play(Write(cap_split), run_time=1.2)
        self.wait(1.4)

        cap_gap = Tex("gap $\\approx U_{\\mathrm{eff}}$ $\\Rightarrow$ Mott insulator",
                      color=YELLOW, font_size=28)\
            .move_to(np.array([RIGHT_X, -3.00, 0.0]))
        self.play(Write(cap_gap), run_time=1.4)
        self.wait(3.0)
        self.wait(0.8)

        # ------------------------------------------------ 6. end card
        everything = VGroup(
            title, formula,
            left_lbl, axes, curve, xticks, ytick, xlbl, flbl, dash_v, dash_h,
            dot_lda, lda_lbl, dot_int1, dot_int2, int1_lbl, int2_lbl,
            row_lda, row_int,
            right_lbl, upper, lower, gap_arrow, gap_lbl, uhb, lhb,
            cap_split, cap_gap,
        )
        self.play(FadeOut(everything), run_time=1.1)

        end1 = Tex("the penalty forces integer occupations",
                   color=INK, font_size=36).move_to(np.array([0.0, 1.15, 0.0]))
        end_arrow = Arrow(np.array([0.0, 0.55, 0]), np.array([0.0, -0.30, 0]),
                          buff=0, stroke_width=4, color=DIM)
        end2 = Tex("the Mott gap opens", color=YELLOW,
                   font_size=52).move_to(np.array([0.0, -1.00, 0.0]))
        src = Tex("chapter 13 · LDA+U · minimum of $n(1-n)$ is at integer filling",
                  color=DIM, font_size=24).next_to(end2, DOWN, buff=0.55)
        self.play(Write(end1), run_time=1.5)
        self.play(GrowArrow(end_arrow), run_time=0.7)
        self.play(Write(end2), run_time=1.2)
        self.play(FadeIn(src), run_time=0.8)
        self.wait(4.0)
