"""
01-hellmann-feynman.py
======================

The Hellmann-Feynman theorem: where DFT forces come from.

Every algebraic step is shown explicitly -- no skipped algebra.
Companion to chapter 04, section 4.7 (signs and formulas verified
against dft_notes/chapter_04/00-kohn-sham.md, lines 700-830).

Scene graph
-----------
1.  Title card.
2.  Setup: H(lambda), E(lambda) = <Psi|H|Psi>.
3.  Product rule: the total derivative splits into three terms.
4.  Terms (1) and (3) combine to E d<Psi|Psi>/dlambda = 0.
5.  The theorem, boxed: dE/dlambda = <dH/dlambda>.
6.  Force definition F_I = -dE/dR_I; only V_en and V_nn feel R_I.
7.  Their derivatives are classical electrostatics; final force.

Run from the repo root:
    manim -qm dft_notes/animations/chapter_04/01-hellmann-feynman.py HellmannFeynman
Writes to:
    dft_notes/animations/chapter_04/videos/... (see render pipeline in README)
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, VGroup, Write, Create, FadeIn, FadeOut,
    SurroundingRectangle, Line, UP, DOWN, ORIGIN, YELLOW,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # site accent 1
TEALC = "#5db8a6"     # site accent 2
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

WORK_X = -3.4         # working column centre
PANEL_X = 5.05        # facts panel centre
LABEL_Y = 2.48        # every section label lives here (title clears it)


def panel_row(tex_src, y):
    """A right-panel results row."""
    return MathTex(tex_src, color=INK, font_size=34).move_to(np.array([PANEL_X, y, 0.0]))


def work_tex(src, y, color=INK, size=40):
    return Tex(src, color=color, font_size=size).move_to(np.array([WORK_X, y, 0.0]))


def work_math(src, y, color=INK, size=38):
    return MathTex(src, color=color, font_size=size).move_to(np.array([WORK_X, y, 0.0]))


class HellmannFeynman(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex("The Hellmann--Feynman theorem",
                    color=INK, font_size=40).to_edge(UP, buff=0.45)
        subtitle = Tex("where DFT forces come from", color=DIM,
                       font_size=26).next_to(title, DOWN, buff=0.18)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(subtitle),
                  title.animate.scale(0.72).to_edge(UP, buff=0.25),
                  run_time=0.8)

        # ------------------------------------------------ 2. setup
        panel_title = Tex("key facts", color=DIM,
                          font_size=28).move_to(np.array([PANEL_X, 2.55, 0.0]))
        panel_rule = Line(np.array([3.15, 2.32, 0.0]), np.array([6.95, 2.32, 0.0]),
                          color=DIM, stroke_width=1)
        self.play(FadeIn(panel_title), Create(panel_rule), run_time=0.7)

        lbl0 = work_tex("setup:", LABEL_Y, color=TEALC, size=30)
        s0a = work_math(
            r"E(\lambda) = \Bigl\langle \Psi(\lambda)\Bigm|\hat H(\lambda)\Bigm|\Psi(\lambda)\Bigr\rangle",
            1.70, color=INK, size=36)
        s0b = work_tex(r"$\hat H(\lambda)$ depends on a parameter $\lambda$;",
                       0.92, color=DIM, size=26)
        s0c = work_tex(r"$\lambda$ could be a nuclear coordinate $R_{I\alpha}$",
                       0.44, color=DIM, size=26)
        self.play(Write(lbl0), run_time=0.8)
        self.play(Write(s0a), run_time=1.5)
        self.wait(0.9)
        self.play(FadeIn(s0b), run_time=0.7)
        self.play(FadeIn(s0c), run_time=0.7)
        self.wait(0.8)

        fact_norm_l = Tex("exact normalised ground state:", color=DIM,
                          font_size=23).move_to(np.array([PANEL_X, 2.02, 0.0]))
        fact_norm = panel_row(r"\langle\Psi(\lambda)|\Psi(\lambda)\rangle = 1", 1.66)
        self.play(FadeIn(fact_norm_l), FadeIn(fact_norm), run_time=0.6)
        self.wait(0.5)

        # ------------------------------------- 3. total derivative: 3 terms
        lbl1 = work_tex(r"differentiate $E(\lambda)$ -- product rule:",
                        LABEL_Y, color=CORAL, size=29)
        tag1 = Tex("(1)", color=CORAL, font_size=26).move_to(np.array([-5.62, 1.62, 0.0]))
        tag2 = Tex("(2)", color=TEALC, font_size=26).move_to(np.array([-5.62, 0.64, 0.0]))
        tag3 = Tex("(3)", color=CORAL, font_size=26).move_to(np.array([-5.62, -0.34, 0.0]))
        d1 = MathTex(
            r"\frac{dE}{d\lambda} \;=\;"
            r"\Bigl\langle \frac{\partial\Psi}{\partial\lambda}\Bigm|\hat H\Bigm|\Psi\Bigr\rangle",
            color=INK, font_size=36,
        ).move_to(np.array([-3.05, 1.62, 0.0]))
        d2 = MathTex(
            r"+\;\Bigl\langle \Psi\Bigm|\frac{\partial\hat H}{\partial\lambda}\Bigm|\Psi\Bigr\rangle",
            color=INK, font_size=36,
        ).move_to(np.array([WORK_X, 0.64, 0.0]))
        d3 = MathTex(
            r"+\;\Bigl\langle \Psi\Bigm|\hat H\Bigm|\frac{\partial\Psi}{\partial\lambda}\Bigr\rangle",
            color=INK, font_size=36,
        ).move_to(np.array([WORK_X, -0.34, 0.0]))

        self.play(FadeOut(VGroup(lbl0, s0a, s0b, s0c)), run_time=0.5)
        self.play(Write(lbl1), run_time=0.8)
        self.play(Write(d1), FadeIn(tag1), run_time=1.4)
        self.wait(0.8)
        self.play(Write(d2), FadeIn(tag2), run_time=1.3)
        self.wait(0.8)
        self.play(Write(d3), FadeIn(tag3), run_time=1.3)
        self.wait(1.0)

        fact_three = Tex(r"product rule $\Rightarrow$ three terms", color=DIM,
                         font_size=23).move_to(np.array([PANEL_X, 1.06, 0.0]))
        self.play(FadeIn(fact_three), run_time=0.6)
        self.wait(0.6)

        # --------------------------------------- 4. terms (1)+(3) combine
        lbl2 = work_tex("terms (1) and (3) combine:", LABEL_Y,
                        color=TEALC, size=29)
        c1 = MathTex(
            r"\Bigl\langle \frac{\partial\Psi}{\partial\lambda}\Bigm|\hat H\Bigm|\Psi\Bigr\rangle"
            r" + \Bigl\langle \Psi\Bigm|\hat H\Bigm|\frac{\partial\Psi}{\partial\lambda}\Bigr\rangle",
            color=INK, font_size=33,
        ).move_to(np.array([WORK_X, 1.55, 0.0]))
        c2 = MathTex(
            r"=\; E(\lambda)\,\frac{\partial}{\partial\lambda}\langle\Psi|\Psi\rangle",
            color=INK, font_size=36,
        ).move_to(np.array([WORK_X, 0.62, 0.0]))
        c3 = MathTex(r"=\; 0", color=YELLOW, font_size=44,
                     ).move_to(np.array([WORK_X, -0.31, 0.0]))
        why = work_tex(r"$\Psi$ is normalised at every $\lambda$", -1.05,
                       color=DIM, size=26)

        self.play(FadeOut(VGroup(lbl1, tag1, tag2, tag3, d1, d2, d3)), run_time=0.5)
        self.play(Write(lbl2), run_time=0.8)
        self.play(Write(c1), run_time=1.5)
        self.wait(0.8)
        self.play(Write(c2), run_time=1.5)
        self.wait(0.8)
        self.play(Write(c3), run_time=1.0)
        self.wait(0.6)
        self.play(FadeIn(why), run_time=0.7)
        self.wait(0.9)

        fact_zero = Tex(r"(1)$+$(3) $\to E\,\partial\langle\Psi|\Psi\rangle/\partial\lambda = 0$",
                        color=DIM, font_size=23).move_to(np.array([PANEL_X, 0.56, 0.0]))
        self.play(FadeIn(fact_zero), run_time=0.6)

        # ------------------------------------------- 5. the theorem, boxed
        res_hf = MathTex(
            r"\frac{dE}{d\lambda} = "
            r"\Bigl\langle \Psi(\lambda)\Bigm|\frac{\partial\hat H}{\partial\lambda}\Bigm|\Psi(\lambda)\Bigr\rangle",
            color=YELLOW, font_size=40,
        ).move_to(np.array([WORK_X, 0.45, 0.0]))

        self.play(FadeOut(VGroup(lbl2, c1, c2, c3, why)), run_time=0.5)
        self.play(Write(res_hf), run_time=1.8)
        self.wait(0.9)
        box_hf = SurroundingRectangle(res_hf, color=YELLOW, buff=0.16)
        self.play(Create(box_hf), run_time=0.7)
        self.wait(0.7)

        hf_group = VGroup(res_hf, box_hf)
        fact_hf_l = Tex("Hellmann--Feynman:", color=DIM,
                        font_size=23).move_to(np.array([PANEL_X, 0.10, 0.0]))
        self.play(hf_group.animate.scale(0.62).move_to(np.array([PANEL_X, -0.52, 0.0])),
                  FadeIn(fact_hf_l), run_time=1.0)
        self.wait(0.6)

        # ------------------------------------------------ 6. force on a nucleus
        lblF = work_tex("force on nucleus $I$:", LABEL_Y, color=CORAL, size=30)
        f_def = MathTex(
            r"\mathbf{F}_I = -\frac{\partial E}{\partial \mathbf{R}_I}",
            color=INK, font_size=42,
        ).move_to(np.array([WORK_X, 1.70, 0.0]))
        f_n1 = work_tex(r"Born--Oppenheimer surface $E(\mathbf R)$;",
                        0.95, color=DIM, size=26)
        f_n2 = work_tex(r"apply the theorem with $\lambda = R_{I\alpha}$.",
                        0.47, color=DIM, size=26)

        self.play(Write(lblF), run_time=0.8)
        self.play(Write(f_def), run_time=1.3)
        self.wait(0.9)
        self.play(FadeIn(f_n1), run_time=0.7)
        self.play(FadeIn(f_n2), run_time=0.7)
        self.wait(0.8)

        fact_force_l = Tex("force definition:", color=DIM,
                           font_size=23).move_to(np.array([PANEL_X, -1.28, 0.0]))
        fact_force = panel_row(r"\mathbf{F}_I = -\partial E/\partial \mathbf{R}_I", -1.63)
        self.play(FadeIn(fact_force_l), FadeIn(fact_force), run_time=0.6)
        self.wait(0.6)

        # ------------------------------------ 7. which pieces feel R_I?
        lblV = work_tex(r"only two pieces of $\hat H$ contain $\mathbf R_I$:",
                        LABEL_Y, color=TEALC, size=29)
        v1a = MathTex(
            r"\hat V_{en} = -\sum_{i,I} \frac{Z_I}{|\,\mathbf r_i - \mathbf R_I\,|}",
            color=INK, font_size=34,
        ).move_to(np.array([WORK_X, 1.62, 0.0]))
        v1b = MathTex(
            r"\hat V_{nn} = \frac{1}{2}\sum_{I \neq J} \frac{Z_I Z_J}{|\,\mathbf R_I - \mathbf R_J\,|}",
            color=INK, font_size=34,
        ).move_to(np.array([WORK_X, 0.70, 0.0]))
        v2 = work_tex(r"$\hat T_e$, $\hat V_{ee}$ never mention nuclei.", 0.00,
                      color=DIM, size=26)

        self.play(FadeOut(VGroup(lblF, f_def, f_n1, f_n2)), run_time=0.5)
        self.play(Write(lblV), run_time=0.8)
        self.play(Write(v1a), run_time=1.4)
        self.wait(0.7)
        self.play(Write(v1b), run_time=1.4)
        self.wait(0.7)
        self.play(FadeIn(v2), run_time=0.7)
        self.wait(0.9)

        # ------------------------------- 8. their R_I-derivatives
        dv_lbl = work_tex("differentiate those two:", LABEL_Y,
                          color=CORAL, size=29)
        dv_en = MathTex(
            r"\frac{\partial \hat V_{en}}{\partial \mathbf R_I}"
            r"= -\sum_i Z_I\,\frac{\mathbf r_i - \mathbf R_I}{|\,\mathbf r_i - \mathbf R_I\,|^3}",
            color=CORAL, font_size=30,
        ).move_to(np.array([WORK_X, 1.58, 0.0]))
        dv_nn = MathTex(
            r"\frac{\partial \hat V_{nn}}{\partial \mathbf R_I}"
            r"= -\sum_{J \neq I} Z_I Z_J\,"
            r"\frac{\mathbf R_I - \mathbf R_J}{|\,\mathbf R_I - \mathbf R_J\,|^3}",
            color=TEALC, font_size=30,
        ).move_to(np.array([WORK_X, 0.62, 0.0]))

        self.play(FadeOut(VGroup(lblV, v1a, v1b, v2)), run_time=0.5)
        self.play(Write(dv_lbl), run_time=0.8)
        self.play(Write(dv_en), run_time=1.6)
        self.wait(0.9)
        self.play(Write(dv_nn), run_time=1.6)
        self.wait(0.9)

        sign_note = work_tex(
            r"the minus in $\mathbf F_I = -\partial E / \partial\mathbf R_I$ flips both signs:",
            -0.18, color=DIM, size=26)
        self.play(FadeIn(sign_note), run_time=0.7)
        self.wait(0.9)

        # ------------------------------------------- 9. the force, assembled
        lblA = work_tex("assemble the force:", LABEL_Y, color=TEALC, size=29)
        g1 = MathTex(
            r"\mathbf F_I = +Z_I \int \rho(\mathbf r)\,"
            r"\frac{\mathbf r - \mathbf R_I}{|\,\mathbf r - \mathbf R_I\,|^3}\, d\mathbf r",
            color=INK, font_size=32,
        ).move_to(np.array([WORK_X, 1.50, 0.0]))
        g2 = MathTex(
            r"+\;\sum_{J \neq I} Z_I Z_J\,"
            r"\frac{\mathbf R_I - \mathbf R_J}{|\,\mathbf R_I - \mathbf R_J\,|^3}",
            color=INK, font_size=32,
        ).move_to(np.array([WORK_X + 0.6, 0.40, 0.0]))

        self.play(FadeOut(VGroup(dv_lbl, dv_en, dv_nn, sign_note)), run_time=0.5)
        self.play(Write(lblA), run_time=0.8)
        self.play(Write(g1), run_time=1.8)
        self.wait(0.9)
        self.play(Write(g2), run_time=1.5)
        self.wait(0.9)

        box_force = SurroundingRectangle(VGroup(g1, g2), color=YELLOW, buff=0.18)
        self.play(Create(box_force), run_time=0.8)
        interp = work_tex(r"classical Coulomb force on a charge $Z_I$ at $\mathbf R_I$:",
                          -0.78, color=DIM, size=25)
        self.play(FadeIn(interp), run_time=0.8)
        self.wait(1.0)

        fact_classical = Tex("electrons attract; other nuclei repel.", color=DIM,
                             font_size=23).move_to(np.array([PANEL_X, -2.18, 0.0]))
        self.play(FadeIn(fact_classical), run_time=0.6)
        self.wait(1.0)

        # ------------------------------------------------ 10. end card
        everything = VGroup(title, panel_title, panel_rule,
                            fact_norm_l, fact_norm, fact_three, fact_zero,
                            fact_hf_l, hf_group,
                            fact_force_l, fact_force, fact_classical,
                            lblA, g1, g2, box_force, interp)
        self.play(FadeOut(everything), run_time=0.9)
        end = Tex("The Hellmann--Feynman theorem:\\\\",
                  "nuclei move in the classical electrostatic field\\\\",
                  "of the electron density and the other nuclei.",
                  color=INK, font_size=32).move_to(ORIGIN)
        src = Tex("chapter 04, section 4.7  ·  complete basis set (no Pulay term yet)",
                  color=DIM, font_size=24).next_to(end, DOWN, buff=0.5)
        self.play(Write(end), run_time=1.5)
        self.play(FadeIn(src), run_time=0.8)
        self.wait(2.2)
