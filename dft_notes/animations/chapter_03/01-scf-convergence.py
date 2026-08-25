"""
01-scf-convergence.py
=====================

The SCF loop: an iterative cycle that almost diverges, then converges.

Left: the total energy E_k oscillates with decaying amplitude and settles
on the Hartree-Fock value.  Right: the density change max|dP| falls down a
log-scale staircase and crosses the 10^-6 threshold at iteration 12.
Numbers are the standard H2 / STO-3G-like values used throughout these
notes (E_HF = -1.1167 E_h); energies follow
    E_k = -1.1167 + (-1)^k * 0.35 exp(-0.9 k) + 0.02 exp(-1.4 k).

Run from the repo root:
    manim -qm dft_notes/animations/chapter_03/01-scf-convergence.py SCFConvergence
Writes to:
    dft_notes/animations/chapter_03/videos/... (see render pipeline in README)
"""

import numpy as np
from manim import (
    Scene, Tex, MathTex, VGroup, Dot, Line, DashedLine, Arrow, Axes,
    Create, Write, FadeIn, FadeOut, SurroundingRectangle,
    UP, DOWN, LEFT, RIGHT, DEGREES, YELLOW,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # site accent 1  -> density-change trace
TEALC = "#5db8a6"     # site accent 2  -> energy trace
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

# ---------------------------------------------------------------- data
K_ITERS = np.arange(13)
ENERGIES = -1.1167 + (-1.0) ** K_ITERS * 0.35 * np.exp(-0.9 * K_ITERS) \
    + 0.02 * np.exp(-1.4 * K_ITERS)
LOG_DP = np.array(
    [-0.50, -0.62, -0.55, -0.70, -0.80, -0.96, -1.28,
     -1.70, -2.20, -2.80, -3.44, -4.92, -6.25]
)
DP_VALS = 10.0 ** LOG_DP

RE_POS = np.array([5.25, 1.45, 0.0])     # live energy readout anchor
RP_POS = np.array([5.25, -1.75, 0.0])    # live density-change readout


def sci(val):
    """5.6e-07 -> '5.60\\times10^{-7}'"""
    mant, exp = f"{float(val):.2e}".split("e")
    return rf"{mant}\times 10^{{{int(exp)}}}"


class SCFConvergence(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex("The SCF loop", color=INK,
                    font_size=40).to_edge(UP, buff=0.35)
        subtitle = Tex("guess a density -- rebuild it -- repeat until it "
                       "agrees with itself",
                       color=DIM, font_size=26).next_to(title, DOWN, buff=0.18)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(subtitle),
                  title.animate.scale(0.75).to_edge(UP, buff=0.25),
                  run_time=0.8)
        self.wait(0.5)

        # --------------------------------------- 2. the five loop steps
        steps = VGroup(
            Tex("1.  guess a density ", "$P$", font_size=32),
            Tex("2.  build the Fock matrix ", "$F[P]$", font_size=32),
            Tex("3.  diagonalise ", r"$F \rightarrow C,\ \epsilon$",
                font_size=32),
            Tex("4.  form the new density ", "$P'$", font_size=32),
            Tex("5.  restart until ",
                r"$\max|P' - P| < 10^{-6}$", font_size=32),
        )
        for s in steps:
            s.set_color(INK)
        steps[0][1].set_color(CORAL)
        steps[1][1].set_color(TEALC)
        steps[2][1].set_color(TEALC)
        steps[3][1].set_color(CORAL)
        step_ys = [2.05, 1.27, 0.49, -0.29, -1.07]
        for s, y in zip(steps, step_ys):
            s.move_to(np.array([-2.2, y, 0.0]))

        for s in steps:
            self.play(Write(s), run_time=1.35)
            self.wait(0.7)

        elbow = VGroup(
            Line(np.array([0.45, -1.07, 0.0]), np.array([3.35, -1.07, 0.0])),
            Line(np.array([3.35, -1.07, 0.0]), np.array([3.35, 1.27, 0.0])),
            Arrow(np.array([3.35, 1.27, 0.0]), np.array([0.30, 1.27, 0.0]),
                  buff=0.08, stroke_width=3),
        ).set_color(TEALC)
        elbow_lbl = Tex("repeat", color=DIM,
                        font_size=24).rotate(90 * DEGREES)
        elbow_lbl.move_to(np.array([3.80, 0.10, 0.0]))
        self.play(Create(elbow), run_time=1.0)
        self.play(FadeIn(elbow_lbl), run_time=0.5)
        self.wait(2.4)
        self.play(FadeOut(VGroup(steps, elbow, elbow_lbl)), run_time=0.7)

        # ------------------------------------------ 3. the two plot frames
        e_ax = Axes(
            x_range=[0, 12, 2], y_range=[-1.4, -0.6, 0.2],
            x_length=8.0, y_length=2.5, tips=False,
            axis_config={"font_size": 20, "stroke_width": 2},
        ).move_to(np.array([-0.9, 1.45, 0.0]))
        e_ax.add_coordinates(font_size=20, color=DIM)
        t_e = Tex("total energy $E_k$  ($E_h$)", color=DIM,
                  font_size=28).next_to(e_ax, UP, buff=0.12)
        t_e.align_to(e_ax, LEFT)

        p_ax = Axes(
            x_range=[0, 12, 2], y_range=[-7, 0, 1],
            x_length=8.0, y_length=2.5, tips=False,
            axis_config={"font_size": 20, "stroke_width": 2},
        ).move_to(np.array([-0.9, -1.95, 0.0]))
        p_ax.x_axis.add_numbers(font_size=20, color=DIM)
        power_labels: dict = {
            float(v): MathTex(rf"10^{{{v}}}", font_size=22, color=DIM)
            for v in range(0, -7, -1)
        }
        p_ax.y_axis.add_labels(power_labels, font_size=22)
        t_p = Tex(r"density change $\max|\Delta P|$  ($\log_{10}$)",
                  color=DIM, font_size=28).next_to(p_ax, UP, buff=0.15)
        t_p.align_to(p_ax, LEFT)
        iter_lbl = Tex("iteration", color=DIM, font_size=24)
        iter_lbl.next_to(p_ax, DOWN, buff=0.28).align_to(p_ax, RIGHT)

        self.play(Create(e_ax), run_time=1.8)
        self.play(FadeIn(t_e), run_time=0.6)
        self.play(Create(p_ax), run_time=1.8)
        self.play(FadeIn(t_p), FadeIn(iter_lbl), run_time=0.7)
        self.wait(1.0)

        # ------------------------------- 4. convergence threshold marker
        thr_line = DashedLine(p_ax.c2p(0, -6), p_ax.c2p(12, -6),
                              dash_length=0.12, color=CORAL, stroke_width=2.5)
        thr_lbl = MathTex(r"\text{threshold}\; 10^{-6}", color=CORAL,
                          font_size=24).move_to(p_ax.c2p(3.2, -5.30))
        self.play(Create(thr_line), run_time=0.9)
        self.play(FadeIn(thr_lbl), run_time=0.6)
        self.wait(0.8)

        # -------------------------------------- 5. live data, iteration 0
        edot = Dot(e_ax.c2p(0, ENERGIES[0]), radius=0.085, color=TEALC)
        pdot = Dot(p_ax.c2p(0, LOG_DP[0]), radius=0.085, color=CORAL)
        re_out = MathTex(rf"k=0:\ E = {ENERGIES[0]:+.4f}\ E_h",
                         font_size=30, color=INK).move_to(RE_POS)
        rp_out = MathTex(rf"\max|\Delta P| = {sci(DP_VALS[0])}",
                         font_size=30, color=INK).move_to(RP_POS)
        self.play(FadeIn(VGroup(edot, pdot)), FadeIn(re_out), FadeIn(rp_out),
                  run_time=0.9)
        self.wait(1.4)

        # --------------------------------- 6. iterate: dots chase settling
        seg_e_all, seg_p_all = [], []
        for k in range(1, 13):
            if k == 5:
                note = Tex("charge sloshes between atoms: ",
                           "$F[P]$ lags behind the density",
                           font_size=26, color=DIM)
                note.move_to(np.array([-0.9, 2.05, 0.0]))
                note[1].set_color(TEALC)
                self.play(FadeIn(note), run_time=0.7)
                self.wait(1.8)
                self.play(FadeOut(note), run_time=0.6)

            seg_e = Line(e_ax.c2p(k - 1, ENERGIES[k - 1]),
                         e_ax.c2p(k, ENERGIES[k]),
                         color=TEALC, stroke_width=3)
            seg_p = Line(p_ax.c2p(k - 1, LOG_DP[k - 1]),
                         p_ax.c2p(k, LOG_DP[k]),
                         color=CORAL, stroke_width=3)
            re_new = MathTex(rf"k={k}:\ E = {ENERGIES[k]:+.4f}\ E_h",
                             font_size=30, color=INK).move_to(RE_POS)
            rp_new = MathTex(rf"\max|\Delta P| = {sci(DP_VALS[k])}",
                             font_size=30, color=INK).move_to(RP_POS)
            step_rt = 1.3 if k >= 10 else 0.8
            self.play(
                edot.animate.move_to(e_ax.c2p(k, ENERGIES[k])),
                pdot.animate.move_to(p_ax.c2p(k, LOG_DP[k])),
                Create(seg_e), Create(seg_p),
                FadeOut(re_out), FadeIn(re_new),
                FadeOut(rp_out), FadeIn(rp_new),
                run_time=step_rt,
            )
            seg_e_all.append(seg_e)
            seg_p_all.append(seg_p)
            re_out, rp_out = re_new, rp_new
        self.wait(0.8)

        # ------------------------------------------- 7. settle + callouts
        self.play(edot.animate.set_color(YELLOW),
                  pdot.animate.set_color(YELLOW),
                  run_time=0.7)
        re_fin = MathTex(rf"k=12:\ E = {ENERGIES[12]:+.4f}\ E_h",
                         font_size=30, color=YELLOW).move_to(RE_POS)
        rp_fin = MathTex(rf"\max|\Delta P| = {sci(DP_VALS[12])}",
                         font_size=30, color=YELLOW).move_to(RP_POS)
        self.play(FadeOut(re_out), FadeIn(re_fin),
                  FadeOut(rp_out), FadeIn(rp_fin),
                  run_time=0.5)
        box_e = SurroundingRectangle(edot, color=YELLOW, buff=0.07)
        ehf = MathTex(r"E_{\mathrm{HF}} = -1.1167\ E_h",
                      font_size=30, color=YELLOW).move_to(
                          np.array([5.25, 1.00, 0.0]))
        self.play(Create(box_e), FadeIn(ehf), run_time=0.9)
        below = Tex("below threshold", color=YELLOW, font_size=24)
        below.move_to(p_ax.c2p(9.0, -5.35))
        self.play(FadeIn(below),
                  thr_line.animate.set_color(YELLOW),
                  thr_lbl.animate.set_color(YELLOW),
                  run_time=0.8)
        self.wait(2.4)
        self.wait(1.0)

        # ---------------------------------------------------- 8. end card
        outro = VGroup(title, t_e, e_ax, t_p, p_ax, iter_lbl,
                       thr_line, thr_lbl, edot, pdot,
                       *seg_e_all, *seg_p_all,
                       re_fin, rp_fin, box_e, ehf, below)
        self.play(FadeOut(outro), run_time=0.9)

        end = Tex("Converged in 12 iterations", "  ·  ",
                  r"$\Delta E < 10^{-6}$", font_size=40)
        end[0].set_color(INK)
        end[1].set_color(DIM)
        end[2].set_color(YELLOW)
        src = Tex(r"H$_2$ / STO-3G-like · chapter 03 · self-consistent field",
                  color=DIM, font_size=24).next_to(end, DOWN, buff=0.5)
        self.play(Write(end), run_time=1.7)
        self.play(FadeIn(src), run_time=0.7)
        self.wait(3.4)
