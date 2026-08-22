"""
01-h2-two-configuration.py
==========================

Full CI on H2: the two-configuration problem, solved live.

Every arithmetic step is shown explicitly -- no skipped algebra.
Companion to chapter 02, section 2.5 (all numbers verified against
PySCF and dft_notes/python_codes/chapter_02/03-h2-full-ci-toy.py).

Scene graph
-----------
1.  Title card.
2.  The two closed-shell determinants Phi1 = |gg> and Phi4 = |uu>.
3.  The MO integrals (h_gg, h_uu, J_gg, J_uu, K_gu) as a reference panel.
4.  Matrix elements, one substitution per line:
      H11 = 2 h_gg + J_gg = -1.8310
      H44 = 2 h_uu + J_uu = -0.2537
      H14 = K_gu          = +0.1813
5.  The 2x2 Hamiltonian block assembles itself from those numbers.
6.  The eigenvalue formula; each numeric substitution shown:
      mean -> half-difference -> squares -> sum -> root -> E0(el) -> E0(tot)
7.  Ground-state composition and correlation energy.

Run from the repo root:
    manim -qm dft_notes/animations/chapter_02/01-h2-two-configuration.py H2TwoConfiguration
Writes to:
    dft_notes/animations/chapter_02/videos/... (see render pipeline in README)
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, Text, VGroup, Write, Create, FadeIn, FadeOut,
    TransformMatchingTex, Transform, ReplacementTransform, Circle,
    Indicate, SurroundingRectangle, Rectangle, Line, Arrow, config, UP, DOWN,
    LEFT, RIGHT, UL, DR, ORIGIN, PI, RED, GREEN, BLUE, YELLOW, GREY, WHITE,
    TEAL, MAROON, PURPLE,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # site accent 1
TEALC = "#5db8a6"     # site accent 2
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

TITLE_Y = 3.35        # title baseline (frame half-height is 4)


def result_line(tex_src, y):
    """A right-panel results row."""
    return MathTex(tex_src, color=INK, font_size=38).move_to(np.array([5.05, y, 0.0]))


class H2TwoConfiguration(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex("Full CI on H$_2$: the two-configuration problem",
                    color=INK, font_size=40).to_edge(UP, buff=0.45)
        subtitle = Tex("every algebraic step shown", color=DIM,
                       font_size=26).next_to(title, DOWN, buff=0.18)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(subtitle),
                  title.animate.scale(0.72).to_edge(UP, buff=0.25),
                  run_time=0.8)

        # --------------------------------------------- 2. the two states
        phi1 = MathTex(r"\Phi_1 = |\sigma_g \bar\sigma_g\rangle",
                       color=TEALC, font_size=44).move_to(np.array([-3.4, 1.7, 0.0]))
        phi4 = MathTex(r"\Phi_4 = |\sigma_u \bar\sigma_u\rangle",
                       color=CORAL, font_size=44).move_to(np.array([-3.4, 0.85, 0.0]))
        note = Tex("both electrons in the bonding / antibonding MO",
                   color=DIM, font_size=26).next_to(phi4, DOWN, buff=0.35)
        self.play(Write(phi1), run_time=1.2)
        self.play(Write(phi4), run_time=1.2)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.2)

        # --------------------------------------- 3. integrals side panel
        panel_title = Tex("MO integrals ($E_h$)", color=DIM,
                          font_size=28).move_to(np.array([5.05, 2.55, 0.0]))
        panel_rule = Line([3.15, 2.32, 0], [6.95, 2.32, 0],
                          color=DIM, stroke_width=1)
        self.play(FadeIn(panel_title), Create(panel_rule), run_time=0.7)

        rows = VGroup(
            result_line(r"h_{gg} = -1.2528", 2.05),
            result_line(r"h_{uu} = -0.4756", 1.50),
            result_line(r"J_{gg} = 0.6746", 0.95),
            result_line(r"J_{uu} = 0.6975", 0.40),
            result_line(r"K_{gu} = 0.1813", -0.15),
            result_line(r"V_{NN} = 0.7143", -0.70),
        )
        self.play(FadeIn(rows, lag_ratio=0.12), run_time=1.6)
        self.wait(1.4)

        # ------------------------------------------------ 4. H11, step by step
        work_y = 1.7                      # top of the working column
        dy = -0.62                        # line spacing

        lbl1 = Tex("matrix element $H_{11}$:", color=TEALC,
                   font_size=30).move_to([-3.4, work_y, 0])
        s1a = MathTex(r"H_{11} = 2\,h_{gg} + J_{gg}",
                      color=INK, font_size=40).move_to([-3.4, work_y + dy, 0])
        s1b = MathTex(r"= 2\,(-1.2528) + 0.6746",
                      color=INK, font_size=40).move_to([-3.4, work_y + 2 * dy, 0])
        s1c = MathTex(r"= -2.5056\; + \;0.6746",
                      color=INK, font_size=40).move_to([-3.4, work_y + 3 * dy, 0])
        s1d = MathTex(r"= \;-1.8310",
                      color=YELLOW, font_size=44).move_to([-3.4, work_y + 4 * dy, 0])

        self.play(FadeOut(note), FadeOut(phi1), FadeOut(phi4), run_time=0.5)
        self.play(Write(lbl1), run_time=0.8)
        self.play(Write(s1a), run_time=1.2)
        self.wait(0.6)
        self.play(Write(s1b), run_time=1.2)
        self.wait(0.6)
        self.play(Write(s1c), run_time=1.0)
        self.wait(0.6)
        self.play(Write(s1d), run_time=0.9)
        self.wait(1.0)

        res_H11 = result_line(r"H_{11} = -1.8310", -1.25).set_color(YELLOW)
        box_H11 = SurroundingRectangle(res_H11, color=TEALC, buff=0.10)
        self.play(FadeOut(VGroup(lbl1, s1a, s1b, s1c)),
                  s1d.animate.move_to(res_H11),
                  run_time=0.8)
        self.play(FadeIn(box_H11), run_time=0.5)
        self.add(res_H11)
        self.remove(s1d)
        res_H11_row = VGroup(res_H11, box_H11)
        self.wait(0.6)

        # ------------------------------------------------ 5. H44
        work_y2 = 1.7
        lbl2 = Tex("matrix element $H_{44}$:", color=CORAL,
                   font_size=30).move_to([-3.4, work_y2, 0])
        s2a = MathTex(r"H_{44} = 2\,h_{uu} + J_{uu}",
                      color=INK, font_size=40).move_to([-3.4, work_y2 + dy, 0])
        s2b = MathTex(r"= 2\,(-0.4756) + 0.6975",
                      color=INK, font_size=40).move_to([-3.4, work_y2 + 2 * dy, 0])
        s2c = MathTex(r"= -0.9512\; + \;0.6975",
                      color=INK, font_size=40).move_to([-3.4, work_y2 + 3 * dy, 0])
        s2d = MathTex(r"= \;-0.2537",
                      color=YELLOW, font_size=44).move_to([-3.4, work_y2 + 4 * dy, 0])

        self.play(FadeOut(res_H11_row), run_time=0.4)
        self.play(Write(lbl2), run_time=0.8)
        self.play(Write(s2a), run_time=1.2)
        self.wait(0.6)
        self.play(Write(s2b), run_time=1.2)
        self.wait(0.6)
        self.play(Write(s2c), run_time=1.0)
        self.wait(0.6)
        self.play(Write(s2d), run_time=0.9)
        self.wait(1.0)

        # park H44 in the results panel next to H11
        res_H44_final = result_line(r"H_{44} = -0.2537", -1.80).set_color(YELLOW)
        self.play(FadeOut(VGroup(lbl2, s2a, s2b, s2c)),
                  s2d.animate.move_to(res_H44_final),
                  run_time=0.8)
        self.remove(s2d); self.add(res_H44_final)
        self.wait(0.5)

        # ------------------------------------------------ 6. H14
        lbl3 = Tex("coupling:", color=PURPLE,
                   font_size=30).move_to([-3.4, work_y2, 0])
        s3a = MathTex(r"H_{14} = K_{gu} = (\,gu \mid gu\,)",
                      color=INK, font_size=40).move_to([-3.4, work_y2 + dy, 0])
        s3b = Tex("direct term dies on spin orthogonality;",
                  color=DIM, font_size=27).move_to([-3.4, work_y2 + 2 * dy, 0])
        s3c = Tex("exchange survives.", color=DIM,
                  font_size=27).move_to([-3.4, work_y2 + 3 * dy, 0])
        s3d = MathTex(r"= \;+0.1813", color=YELLOW,
                      font_size=44).move_to([-3.4, work_y2 + 4 * dy, 0])

        self.play(Write(lbl3), run_time=0.7)
        self.play(Write(s3a), run_time=1.2)
        self.wait(0.7)
        self.play(FadeIn(s3b), run_time=0.7)
        self.play(FadeIn(s3c), run_time=0.7)
        self.wait(0.7)
        self.play(Write(s3d), run_time=0.9)
        self.wait(1.0)

        # both parked values now on the right, stacked
        res_H14 = result_line(r"H_{14} = +0.1813", -2.35).set_color(YELLOW)
        self.play(FadeOut(VGroup(lbl3, s3a, s3b, s3c)),
                  s3d.animate.move_to(res_H14),
                  FadeOut(res_H44_final),
                  run_time=0.8)
        self.add(res_H14); self.remove(s3d)
        self.wait(0.6)

        # ------------------------------------------------ 7. assemble matrix
        mat_label = Tex("the $2 \\times 2$ block:", color=INK,
                        font_size=30).move_to(np.array([-3.4, 1.7, 0.0]))
        mat = MathTex(
            r"\mathbf{H} \;=\;",
            r"\begin{pmatrix} -1.8310 & +0.1813 \\ +0.1813 & -0.2537 \end{pmatrix}",
            color=INK, font_size=44,
        ).move_to(np.array([-3.4, 0.35, 0.0]))
        mat[1][1:8].set_color(TEALC)       # -1.8310
        mat[1][16:23].set_color(CORAL)     # -0.2537
        self.play(Write(mat_label), run_time=0.7)
        self.play(Write(mat), run_time=1.8)
        self.wait(1.4)

        # ------------------------------------------------ 8. eigen formula
        eig_lbl = Tex("lower eigenvalue:", color=INK,
                      font_size=30).move_to(np.array([-3.4, -1.15, 0.0]))
        eig = MathTex(
            r"E_- = \frac{H_{11}+H_{44}}{2}"
            r" - \sqrt{\Bigl(\frac{H_{11}-H_{44}}{2}\Bigr)^{\!2} + H_{14}^2}",
            color=INK, font_size=36,
        ).move_to(np.array([-3.4, -1.95, 0.0]))
        self.play(FadeOut(mat_label), mat.animate.scale(0.78).to_edge(UP, buff=1.15),
                  run_time=0.7)
        self.play(Write(eig_lbl), run_time=0.7)
        self.play(Write(eig), run_time=2.0)
        self.wait(1.4)

        # ------------------------------------------------ 9. substitutions
        steps = [
            (r"\frac{H_{11}+H_{44}}{2} = \frac{-1.8310 + (-0.2537)}{2} = -1.0424",),
            (r"\frac{H_{11}-H_{44}}{2} = \frac{-1.8310 - (-0.2537)}{2} = -0.7886",),
            (r"\left(-0.7886\right)^2 = 0.6220, \qquad (0.1813)^2 = 0.0329",),
            (r"\sqrt{0.6220 + 0.0329} = \sqrt{0.6548} = 0.8092",),
        ]
        cur = eig
        for i, (src,) in enumerate(steps):
            nxt = MathTex(src, color=INK, font_size=34).move_to(eig)
            self.play(FadeOut(cur), Write(nxt), run_time=1.1)
            self.wait(1.0)
            cur = nxt

        # final energy chain
        e_el = MathTex(r"E_-(\mathrm{el}) = -1.0424 - 0.8092 = -1.8516",
                       color=INK, font_size=34).move_to(eig)
        self.play(FadeOut(cur), Write(e_el), run_time=1.1)
        self.wait(0.8)
        e_tot = MathTex(
            r"E_0 = -1.8516 + 0.7143 = \mathbf{-1.1373}\; E_h",
            color=YELLOW, font_size=42,
        ).move_to(eig)
        self.play(FadeOut(e_el), Write(e_tot), run_time=1.1)
        box_E = SurroundingRectangle(e_tot, color=YELLOW, buff=0.14)
        self.play(Create(box_E), run_time=0.7)
        self.wait(1.6)

        # ------------------------------------------------ 10. ground state
        gs_lbl = Tex("ground state:", color=INK,
                     font_size=30).move_to(np.array([-3.4, -0.55, 0.0]))
        gs = MathTex(
            r"\Psi_0 = 0.9936\,\Phi_1 \;-\; 0.1128\,\Phi_4",
            color=INK, font_size=40,
        ).move_to(np.array([-3.4, -1.30, 0.0]))
        wts = Tex("weights: 98.7% HF-like  +  1.3% doubly excited",
                  color=DIM, font_size=27).move_to(np.array([-3.4, -2.00, 0.0]))

        corr = MathTex(
            r"E_{\mathrm{corr}} = -1.1373 - (-1.1167) = -0.0206\;E_h",
            color=TEALC, font_size=36,
        ).move_to(np.array([-3.4, -2.75, 0.0]))

        self.play(FadeOut(VGroup(eig_lbl, box_E)), run_time=0.5)
        self.play(e_tot.animate.move_to(np.array([-3.4, -0.55, 0.0])).scale(0.8),
                  run_time=0.7)
        self.remove(gs_lbl)
        self.play(Write(gs), run_time=1.4)
        self.play(FadeIn(wts), run_time=0.7)
        self.wait(1.0)
        self.play(Write(corr), run_time=1.4)
        self.wait(1.6)

        # ------------------------------------------------ 11. end card
        everything = VGroup(title, panel_title, panel_rule, rows,
                            mat, e_tot, gs, wts, corr)
        self.play(FadeOut(everything), run_time=0.9)
        end = Tex("Left--right correlation:\\\\",
                  "the exact wavefunction mixes in the doubly excited configuration.",
                  color=INK, font_size=34).move_to(ORIGIN)
        src = Tex("chapter 02, section 2.5  ·  verified against PySCF",
                  color=DIM, font_size=24).next_to(end, DOWN, buff=0.5)
        self.play(Write(end), run_time=1.4)
        self.play(FadeIn(src), run_time=0.8)
        self.wait(2.2)
