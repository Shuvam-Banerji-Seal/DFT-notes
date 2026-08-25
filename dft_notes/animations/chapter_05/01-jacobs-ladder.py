"""
01-jacobs-ladder.py
===================

Jacob's ladder of density functional approximations (Perdew 2001).

A small figure climbs five ascending rungs -- LDA, GGA, meta-GGA,
hybrid, RPA -- while accuracy and cost bar charts grow on the right
at every rung reached.

Run from the repo root:
    manim -qm dft_notes/animations/chapter_05/01-jacobs-ladder.py JacobsLadder
Writes to:
    dft_notes/animations/chapter_05/videos/
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, Text, VGroup, VMobject, Write, Create, FadeIn,
    FadeOut, GrowFromEdge, MoveAlongPath, Indicate, Rectangle, Line,
    Circle, Triangle, UP, DOWN, RIGHT, ORIGIN, PI, YELLOW,
)

CORAL = "#cc785c"
TEALC = "#5db8a6"
INK = "#e8e4de"
DIM = "#9a958c"

NAMES = ["LDA", "GGA", "meta-GGA", "hybrid", "RPA"]
INGS = [
    r"\rho",
    r"\rho,\ \nabla\rho",
    r"\rho,\ \nabla\rho,\ \tau",
    r"+\ E_x^{\mathrm{HF}}",
]
ING_TEX = [
    MathTex(INGS[0], color=DIM, font_size=26),
    MathTex(INGS[1], color=DIM, font_size=26),
    MathTex(INGS[2], color=DIM, font_size=26),
    MathTex(INGS[3], color=DIM, font_size=26),
    Tex("+ unoccupied orbitals", color=DIM, font_size=24),
]
COST_REL = [1, 3, 6, 20, 100]


def cost_height(v):
    return 0.60 + 0.78 * np.log10(v)


class JacobsLadder(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex(
            "Jacob's ladder of density functional approximations",
            color=INK, font_size=38,
        ).to_edge(UP, buff=0.40)
        sub = Tex("five rungs, five physical ingredients",
                  color=DIM, font_size=26).next_to(title, DOWN, buff=0.18)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(3.6)
        self.play(FadeOut(sub), run_time=0.6)

        # ------------------------------------------------ 2. staircase
        dx, dy, t, w, g = 1.7, 1.2, 0.14, 1.48, 0.22
        xs = np.array([-6.7 + dx * i for i in range(5)])
        ys = np.array([-2.8 + dy * i for i in range(5)])

        steps = []
        names = []
        ings = []
        for i in range(5):
            tread = (
                Rectangle(width=w, height=t)
                .set_fill(CORAL, 1.0)
                .set_stroke(INK, 1.0)
                .move_to(np.array([xs[i] + w / 2, ys[i], 0.0]))
            )
            step = VGroup(tread)
            if i > 0:
                riser = (
                    Rectangle(width=g, height=dy)
                    .set_fill(CORAL, 1.0)
                    .set_stroke(INK, 1.0)
                    .move_to(np.array([xs[i] - g / 2, ys[i] + t - dy / 2, 0.0]))
                )
                step.add(riser)
            name = Text(
                NAMES[i], font_size=30, color=INK, weight="BOLD"
            ).move_to(np.array([xs[i] + 0.95, ys[i] - 0.42, 0.0]))
            ing = ING_TEX[i].move_to(np.array([xs[i] + 1.15, ys[i] - 0.85, 0.0]))
            steps.append(step)
            names.append(name)
            ings.append(ing)
            self.play(Create(step), FadeIn(name), FadeIn(ing), run_time=1.1)
            self.wait(1.5)

        # ------------------------------------------------ 3. right panel
        cx = np.array([4.05 + 0.62 * i for i in range(5)])
        axis = Line(
            np.array([3.5, -3.0, 0.0]),
            np.array([7.0, -3.0, 0.0]),
            color=DIM, stroke_width=2,
        )
        ticks = VGroup(*[
            Text(str(i + 1), font_size=18, color=DIM).move_to(
                np.array([cx[i], -3.32, 0.0])
            )
            for i in range(5)
        ])
        chip_a = Rectangle(width=0.16, height=0.16).set_fill(TEALC, 1.0)
        tex_a = Tex("accuracy $\\uparrow$", color=DIM, font_size=22)
        leg_a = VGroup(chip_a, tex_a).arrange(RIGHT, buff=0.12).move_to(
            np.array([4.45, 0.12, 0.0])
        )
        chip_b = Rectangle(width=0.16, height=0.16).set_fill(CORAL, 1.0)
        tex_b = Tex("cost (rel.)", color=DIM, font_size=22)
        leg_b = VGroup(chip_b, tex_b).arrange(RIGHT, buff=0.12).move_to(
            np.array([6.35, 0.12, 0.0])
        )
        self.play(
            Create(axis), FadeIn(ticks), FadeIn(leg_a), FadeIn(leg_b),
            run_time=1.0,
        )
        self.wait(0.8)

        # ------------------------------------------------ 4. the climber
        dot = (
            Circle(radius=0.14)
            .set_fill(TEALC, 1.0)
            .set_stroke(INK, 1.5)
            .move_to(np.array([xs[0] + w / 2, ys[0] + t / 2 + 0.14, 0.0]))
        )
        self.play(FadeIn(dot), run_time=0.7)
        self.wait(0.8)

        bars_acc = []
        bars_cost = []
        cost_lbls = []

        def arrive(i, hold):
            ha = 0.50 * (i + 1)
            hc = cost_height(COST_REL[i])
            bar_a = (
                Rectangle(width=0.24, height=ha)
                .set_fill(TEALC, 1.0)
                .move_to(np.array([cx[i] - 0.19, -3.0 + ha / 2, 0.0]))
            )
            bar_c = (
                Rectangle(width=0.24, height=hc)
                .set_fill(CORAL, 1.0)
                .move_to(np.array([cx[i] + 0.19, -3.0 + hc / 2, 0.0]))
            )
            lbl = MathTex(
                r"\times\," + str(COST_REL[i]), color=DIM, font_size=20
            ).move_to(np.array([cx[i], -3.0 + max(ha, hc) + 0.22, 0.0]))
            bars_acc.append(bar_a)
            bars_cost.append(bar_c)
            cost_lbls.append(lbl)
            self.play(
                GrowFromEdge(bar_a, DOWN),
                GrowFromEdge(bar_c, DOWN),
                FadeIn(lbl),
                run_time=0.8,
            )
            self.play(names[i].animate.set_color(TEALC), run_time=0.4)
            self.play(Indicate(ings[i]), run_time=1.0)
            self.wait(hold)

        arrive(0, 1.8)

        # ------------------------------------------------ 5. climb
        for i in range(4):
            p0 = np.array([xs[i] + w / 2, ys[i] + t / 2 + 0.14, 0.0])
            p1 = np.array([xs[i + 1] + w / 2, ys[i + 1] + t / 2 + 0.14, 0.0])
            apex_y = min(max(p0[1], p1[1]) + 1.2, 2.8)
            path = VMobject().set_points_smoothly(
                [p0, np.array([(p0[0] + p1[0]) / 2, apex_y, 0.0]), p1]
            )
            self.play(MoveAlongPath(dot, path), run_time=1.35)
            arrive(i + 1, 2.4 if i + 1 >= 3 else 1.8)

        # ------------------------------------------------ 6. summit flag
        pole = Line(
            np.array([xs[4] + w, ys[4] + t, 0.0]),
            np.array([xs[4] + w, ys[4] + 0.68, 0.0]),
            color=DIM, stroke_width=2.5,
        )
        flag = (
            Triangle(radius=0.15)
            .rotate(-PI / 2)
            .set_fill(YELLOW, 1.0)
            .set_stroke(width=0)
            .move_to(np.array([xs[4] + w + 0.16, ys[4] + 0.68, 0.0]))
        )
        self.play(Create(pole), Create(flag), run_time=0.8)
        self.play(Indicate(dot, scale_factor=1.6), run_time=0.8)
        self.wait(2.6)

        # ------------------------------------------------ 7. end card
        everything = VGroup(
            title,
            *steps, *names, *ings,
            dot, axis, ticks, leg_a, leg_b,
            *bars_acc, *bars_cost, *cost_lbls,
            pole, flag,
        )
        self.wait(1.0)
        self.play(FadeOut(everything), run_time=0.9)

        line1 = Tex(
            "every rung adds one physical ingredient",
            color=INK, font_size=34,
        )
        line2 = Tex(
            r"heaven = chemical accuracy ($1\ \mathrm{kcal/mol}$)",
            color=YELLOW, font_size=42,
        )
        card = VGroup(line1, line2).arrange(DOWN, buff=0.55).move_to(
            np.array([0.0, 0.3, 0.0])
        )
        src = Tex(
            "Perdew, Schmidt, AIP Conf. Proc. 577, 1 (2001)",
            color=DIM, font_size=24,
        ).next_to(card, DOWN, buff=0.7)
        self.play(Write(line1), run_time=1.5)
        self.wait(1.0)
        self.play(Write(line2), run_time=1.5)
        self.play(FadeIn(src), run_time=0.8)
        self.wait(3.6)
