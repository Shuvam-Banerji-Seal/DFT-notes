"""
02-kohn-sham-mapping.py
=======================

The Hohenberg-Kohn mapping: V_ext(r) <-> rho(r).

The bijection that makes DFT possible, drawn as a forward/inverse arrow
diagram. Companion to chapter 04 (HK theorems section).

Scene graph
-----------
1.  Title card.
2.  Motivating question: can the density alone reconstruct the potential?
3.  Two boxes side by side: v_ext(r) with a well sketch, rho(r) with a
    density bump sketch.
4.  Forward arrow (trivial direction): Schroedinger equation -> unique rho.
5.  The theorem: reverse arrow in yellow, rho -> v_ext (up to a constant);
    the well visibly lifts by a constant.
6.  One-to-one correspondence highlighted around both boxes.
7.  Consequence chain: v_ext -> H -> Psi -> all observables.
8.  End card: all ground-state properties are functionals of rho.

Run from the repo root:
    manim -qm dft_notes/animations/chapter_04/02-kohn-sham-mapping.py KohnShamMapping
Writes to:
    dft_notes/animations/chapter_04/videos/... (see render pipeline in README)
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, VGroup, Write, Create, FadeIn, FadeOut,
    GrowArrow, Arrow, Line, ReplacementTransform, SurroundingRectangle,
    RoundedRectangle, ParametricFunction, LaggedStart,
    UP, DOWN, LEFT, RIGHT, ORIGIN, YELLOW,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # site accent 1  -> the potential side
TEALC = "#5db8a6"     # site accent 2  -> the density side
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

BOX_W = 4.0
BOX_H = 2.7
BOX_Y = 0.35
LX = -4.15            # left box centre x
RX = 4.15             # right box centre x


def box_at(cx, stroke_color):
    b = RoundedRectangle(
        corner_radius=0.12, width=BOX_W, height=BOX_H,
        stroke_color=stroke_color, stroke_width=2.5,
    )
    b.set_fill(stroke_color, opacity=0.05)
    b.move_to(np.array([cx, BOX_Y, 0.0]))
    return b


def r_axis(cx, y):
    """Tiny r-axis under a sketch."""
    ln = Line(np.array([cx - 1.45, y, 0.0]), np.array([cx + 1.45, y, 0.0]),
              color=DIM, stroke_width=2)
    lab = Tex("r", color=DIM, font_size=22).next_to(ln, RIGHT, buff=0.10)
    return VGroup(ln, lab)


class KohnShamMapping(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex("The Hohenberg--Kohn mapping",
                    color=INK, font_size=40).to_edge(UP, buff=0.45)
        subtitle = Tex("why DFT is possible", color=DIM,
                       font_size=26).next_to(title, DOWN, buff=0.18)
        self.play(Write(title), run_time=2.0)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(1.4)
        self.play(FadeOut(subtitle),
                  title.animate.scale(0.72).to_edge(UP, buff=0.25),
                  run_time=0.9)

        # ------------------------------------------------ 2. motivating question
        q = Tex("can the density alone reconstruct the potential?",
                color=DIM, font_size=27).move_to(np.array([0.0, 0.4, 0.0]))
        self.play(FadeIn(q), run_time=0.9)
        self.wait(1.8)
        self.play(FadeOut(q), run_time=0.7)

        # ------------------------------------------------ 3. the two boxes
        # left: external potential, drawn as a well
        box_l = box_at(LX, CORAL)
        lbl_l = MathTex(r"v_{\mathrm{ext}}(\mathbf{r})", color=CORAL,
                        font_size=40).move_to(np.array([LX, 1.22, 0.0]))
        desc_l = Tex("external potential", color=DIM,
                     font_size=20).move_to(np.array([LX, 0.90, 0.0]))
        base_l = r_axis(LX, 0.35)
        dip = ParametricFunction(
            lambda t: np.array([
                LX + t,
                0.35 - 0.85 * np.exp(-(t / 0.62) ** 2),
                0.0,
            ]),
            t_range=np.array([-1.45, 1.45, 0.04]),
            color=CORAL, stroke_width=3.5,
        )
        self.play(Create(box_l), run_time=1.5)
        self.play(Write(lbl_l), FadeIn(desc_l), run_time=1.0)
        self.play(Create(base_l), run_time=0.6)
        self.play(Create(dip), run_time=2.0)
        self.wait(1.6)

        # right: ground-state density, drawn as a bump
        box_r = box_at(RX, TEALC)
        lbl_r = MathTex(r"\rho(\mathbf{r})", color=TEALC,
                        font_size=40).move_to(np.array([RX, 1.22, 0.0]))
        desc_r = Tex("ground-state density", color=DIM,
                     font_size=20).move_to(np.array([RX, 0.90, 0.0]))
        base_r = r_axis(RX, -0.55)
        bump = ParametricFunction(
            lambda t: np.array([
                RX + t,
                -0.58 + 1.02 * np.exp(-(t / 0.55) ** 2),
                0.0,
            ]),
            t_range=np.array([-1.40, 1.40, 0.04]),
            color=TEALC, stroke_width=3.5,
        )
        bump.set_fill(TEALC, opacity=0.22)
        self.play(Create(box_r), run_time=1.5)
        self.play(Write(lbl_r), FadeIn(desc_r), run_time=1.0)
        self.play(Create(base_r), run_time=0.6)
        self.play(Create(bump), run_time=2.0)
        self.wait(1.6)

        # ------------------------------------------------ 4. forward arrow (trivial)
        fwd = Arrow(np.array([-1.95, 1.02, 0.0]), np.array([1.95, 1.02, 0.0]),
                    color=CORAL, stroke_width=6, buff=0.0)
        self.play(GrowArrow(fwd), run_time=1.4)

        mini = Arrow(ORIGIN, RIGHT * 0.45, color=CORAL, stroke_width=5,
                     buff=0.0, tip_length=0.16)
        cap_fwd = Tex("Schr\u00f6dinger equation $\\Rightarrow$ unique $\\rho$",
                      color=INK, font_size=27)
        cap_tag = Tex("(trivial direction)", color=DIM, font_size=22)
        cap_row = VGroup(mini, cap_fwd, cap_tag).arrange(RIGHT, buff=0.20)
        cap_row.move_to(np.array([0.0, -1.52, 0.0]))
        self.play(FadeIn(cap_row, lag_ratio=0.25), run_time=1.0)
        self.wait(2.2)

        # ------------------------------------------------ 5. the theorem (yellow)
        rev_ghost = Arrow(np.array([1.95, -0.33, 0.0]), np.array([-1.95, -0.33, 0.0]),
                          color=DIM, stroke_width=5, buff=0.0)
        self.play(GrowArrow(rev_ghost), run_time=1.5)
        self.wait(0.8)
        rev = Arrow(np.array([1.95, -0.33, 0.0]), np.array([-1.95, -0.33, 0.0]),
                    color=YELLOW, stroke_width=9, buff=0.0)
        self.play(ReplacementTransform(rev_ghost, rev), run_time=1.0)
        self.wait(0.9)

        cap_rev = MathTex(
            r"\rho \;\longrightarrow\; v_{\mathrm{ext}}"
            r"\;\; \text{(up to a constant)}",
            color=YELLOW, font_size=30,
        ).move_to(np.array([0.0, -2.18, 0.0]))
        self.play(Write(cap_rev), run_time=1.3)
        self.wait(1.1)

        cap_hk = Tex("HK theorem: the density determines the potential",
                     color=DIM, font_size=25).move_to(np.array([0.0, -2.76, 0.0]))
        self.play(FadeIn(cap_hk), run_time=0.9)
        self.wait(2.0)

        # "up to a constant", made visible: lift the well, put it back
        const_tag = MathTex(r"+\;\text{const}", color=DIM,
                            font_size=24).move_to(np.array([LX + 1.02, -0.10, 0.0]))
        self.play(FadeIn(const_tag), run_time=0.6)
        self.play(dip.animate.shift(UP * 0.22), run_time=0.8)
        self.play(dip.animate.shift(DOWN * 0.22), run_time=0.8)
        self.play(FadeOut(const_tag), run_time=0.5)
        self.wait(0.9)

        # ------------------------------------------------ 6. one-to-one highlight
        bij_rect = SurroundingRectangle(
            VGroup(box_l, box_r), color=TEALC, buff=0.18,
            stroke_width=2, corner_radius=0.15,
        )
        bij_lbl = Tex("one-to-one correspondence", color=TEALC,
                      font_size=26).next_to(bij_rect, UP, buff=0.14)
        self.play(Create(bij_rect), run_time=1.1)
        self.play(FadeIn(bij_lbl), run_time=0.9)
        self.wait(2.2)

        # ------------------------------------------------ 7. consequence chain
        self.play(FadeOut(bij_rect), FadeOut(bij_lbl), run_time=0.6)
        chain = VGroup(
            MathTex(r"v_{\mathrm{ext}}", color=CORAL, font_size=33),
            MathTex(r"\longrightarrow", color=DIM, font_size=30),
            MathTex(r"\hat{H}", color=INK, font_size=33),
            MathTex(r"\longrightarrow", color=DIM, font_size=30),
            MathTex(r"\Psi", color=INK, font_size=33),
            MathTex(r"\longrightarrow", color=DIM, font_size=30),
            MathTex(r"\text{all observables}", color=YELLOW, font_size=33),
        ).arrange(RIGHT, buff=0.34).move_to(np.array([0.0, -3.42, 0.0]))
        self.play(LaggedStart(*[Write(c) for c in chain], lag_ratio=0.32),
                  run_time=4.0)
        self.wait(2.4)

        # ------------------------------------------------ 8. end card
        self.wait(1.0)
        everything = VGroup(
            title, box_l, lbl_l, desc_l, base_l, dip,
            box_r, lbl_r, desc_r, base_r, bump,
            fwd, cap_row, rev, cap_rev, cap_hk, chain,
        )
        self.play(FadeOut(everything), run_time=1.3)
        end = Tex("all ground-state properties are ",
                  "functionals of $\\rho$",
                  font_size=38).move_to(ORIGIN)
        end[0].set_color(INK)
        end[1].set_color(YELLOW)
        end_box = SurroundingRectangle(end, color=YELLOW, buff=0.22,
                                       stroke_width=2.5, corner_radius=0.12)
        src = Tex("Hohenberg--Kohn theorem \u00b7 chapter 04",
                  color=DIM, font_size=22).next_to(end_box, DOWN, buff=0.45)
        self.play(Write(end), run_time=2.0)
        self.play(Create(end_box), run_time=0.9)
        self.play(FadeIn(src), run_time=0.8)
        self.wait(3.2)
