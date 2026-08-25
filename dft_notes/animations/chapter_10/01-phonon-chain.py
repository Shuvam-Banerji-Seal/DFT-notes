"""
01-phonon-chain.py
==================

Phonons of a diatomic chain: a row of masses on springs in which the
acoustic mode, the optical mode and the zone-boundary mode are animated
live as eigenmodes, with a small dispersion inset tracking the branch.

Companion to chapter 10 (lattice vibrations / phonons).

Run from the repo root:
    manim -qm --disable_caching dft_notes/animations/chapter_10/01-phonon-chain.py PhononChain
Writes to:
    dft_notes/animations/chapter_10/videos/01-phonon-chain.mp4
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, VGroup, VMobject, Write, Create, FadeIn, FadeOut,
    Circle, Dot, Line, Axes, ParametricFunction, Rectangle, ValueTracker,
    LaggedStart, UP, DOWN, RIGHT, UL, ORIGIN, PI, YELLOW, linear,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # light atoms M1
TEALC = "#5db8a6"     # heavy atoms M2
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

# ---------------------------------------------------------------- chain geometry
N_PAIRS = 8                     # 8 light + 8 heavy = 16 atoms
N_ATOMS = 2 * N_PAIRS
D       = 0.82                  # neighbour spacing
BASE_Y  = 0.75                  # chain height
X0      = np.array([-D * (N_ATOMS - 1) / 2 + i * D for i in range(N_ATOMS)])
RAD     = np.array([0.12 if i % 2 == 0 else 0.175 for i in range(N_ATOMS)])

# eigenvector sign patterns (displacement_i = sign_i * A * sin(om * t))
SIGN_AC = np.ones(N_ATOMS)                              # acoustic q->0 : all in phase
SIGN_OP = np.array([(-1.0) ** i for i in range(N_ATOMS)])  # optical q->0 : neighbours oppose
SIGN_ZB = np.array([1.0 if i % 2 == 0 else 0.0 for i in range(N_ATOMS)])  # q=pi/a : heavy still


def spring_pts(p1, p2, r1, r2, coils=4, amp=0.06):
    """Zigzag polyline between the rims of two atoms (a cartoon spring)."""
    dv = p2 - p1
    L = float(np.linalg.norm(dv))
    if L < 1e-6:
        return [p1.copy(), p2.copy()]
    u = dv / L
    nv = np.array([-u[1], u[0], 0.0])
    s = p1 + u * r1
    e = p2 - u * r2
    seg = L - r1 - r2
    pts = [s]
    n = coils * 2
    for k in range(1, n):
        off = amp if k % 2 == 1 else -amp
        pts.append(s + u * seg * (k / n) + nv * off)
    pts.append(e)
    return pts


class PhononChain(Scene):
    def construct(self):
        tau = ValueTracker(0.0)
        mode = {"amp": 0.0, "om": 1.6, "sign": SIGN_AC}

        def env():
            """Soft ramp-in so each mode starts smoothly from rest."""
            return float(np.clip(tau.get_value() / 1.2, 0.0, 1.0))

        def atom_x(i):
            return X0[i] + mode["sign"][i] * mode["amp"] * env() * np.sin(mode["om"] * tau.get_value())

        def make_atom_upd(i):
            def upd(m):
                m.move_to(np.array([atom_x(i), BASE_Y, 0.0]))
            return upd

        def make_spring_upd(j):
            def upd(m):
                p1 = np.array([atom_x(j), BASE_Y, 0.0])
                p2 = np.array([atom_x(j + 1), BASE_Y, 0.0])
                m.set_points_as_corners(spring_pts(p1, p2, RAD[j], RAD[j + 1]))
            return upd

        # ------------------------------------------------ 1. title card
        title = Tex("Phonons of a diatomic chain",
                    color=INK, font_size=40).to_edge(UP, buff=0.35)
        leg1 = VGroup(
            Circle(radius=0.07, color=CORAL, fill_opacity=1, stroke_width=0),
            Tex(r"$M_1$ = light atoms", color=INK, font_size=27),
        ).arrange(RIGHT, buff=0.16)
        leg2 = VGroup(
            Circle(radius=0.10, color=TEALC, fill_opacity=1, stroke_width=0),
            Tex(r"$M_2$ = heavy atoms", color=INK, font_size=27),
        ).arrange(RIGHT, buff=0.16)
        legend = VGroup(leg1, leg2).arrange(RIGHT, buff=0.8).next_to(title, DOWN, buff=0.22)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(legend), run_time=0.8)
        self.wait(1.5)

        # ------------------------------------------------ 2. the chain at rest
        baseline = Line(np.array([X0[0] - 0.7, BASE_Y, 0.0]),
                        np.array([X0[-1] + 0.7, BASE_Y, 0.0]),
                        stroke_color=DIM, stroke_width=1.5).set_opacity(0.35)
        springs = []
        for j in range(N_ATOMS - 1):
            sp = VMobject(stroke_color=DIM, stroke_width=2.5, fill_opacity=0)
            p1 = np.array([X0[j], BASE_Y, 0.0])
            p2 = np.array([X0[j + 1], BASE_Y, 0.0])
            sp.set_points_as_corners(spring_pts(p1, p2, RAD[j], RAD[j + 1]))
            springs.append(sp)
        atoms = [
            Circle(radius=RAD[i],
                   color=CORAL if i % 2 == 0 else TEALC,
                   fill_opacity=1, stroke_width=0
                   ).move_to(np.array([X0[i], BASE_Y, 0.0]))
            for i in range(N_ATOMS)
        ]
        self.play(Create(baseline), Create(VGroup(*springs)), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(a, scale=0.5) for a in atoms],
                              lag_ratio=0.06), run_time=1.5)
        self.wait(1.6)

        # live-motion plumbing (amp = 0, so the chain sits at equilibrium)
        for i, a in enumerate(atoms):
            a.add_updater(make_atom_upd(i))
        for j, sp in enumerate(springs):
            sp.add_updater(make_spring_upd(j))

        # ------------------------------------------------ 3. dispersion inset
        inset_frame = Rectangle(width=3.8, height=2.8).set_stroke(DIM, 1).set_fill(opacity=0)
        inset_frame.move_to(np.array([5.05, -2.35, 0.0]))
        axes = Axes(
            x_range=[0, 1, 1], y_range=[0, 1.05, 1],
            x_length=3.0, y_length=1.85,
            axis_config={"stroke_color": DIM, "stroke_width": 2,
                         "include_ticks": False, "include_tip": True,
                         "tip_width": 0.12, "tip_height": 0.12},
        ).move_to(np.array([4.93, -2.30, 0.0]))

        f_ac = lambda q: 0.66 * np.tanh(2.2 * q)          # acoustic branch
        g_op = lambda q: 0.88 - 0.16 * q * q               # optical branch
        cur_ac = ParametricFunction(lambda t: axes.c2p(t, f_ac(t)),
                                    t_range=(0, 1, 0.02),
                                    stroke_color=TEALC, stroke_width=3)
        cur_op = ParametricFunction(lambda t: axes.c2p(t, g_op(t)),
                                    t_range=(0, 1, 0.02),
                                    stroke_color=CORAL, stroke_width=3)
        tick0 = MathTex("0", color=DIM, font_size=24).next_to(axes.c2p(0, 0), DOWN, buff=0.14)
        tick1 = MathTex(r"\pi/a", color=DIM, font_size=24).next_to(axes.c2p(1, 0), DOWN, buff=0.14)
        ylab = MathTex(r"\omega", color=DIM, font_size=24).next_to(axes.c2p(0, 1.05), UL, buff=0.10)
        wtp = MathTex(r"\omega_+", color=CORAL, font_size=26)
        wtp.move_to(axes.c2p(0.30, g_op(0.30)) + UP * 0.16)
        wtm = MathTex(r"\omega_-", color=TEALC, font_size=26)
        wtm.move_to(axes.c2p(0.82, f_ac(0.82)) + DOWN * 0.22)

        self.play(FadeIn(inset_frame), run_time=0.5)
        self.play(Create(axes), run_time=0.9)
        self.play(Create(cur_ac), run_time=0.9)
        self.play(Create(cur_op), run_time=0.9)
        self.play(FadeIn(VGroup(tick0, tick1, ylab, wtp, wtm), lag_ratio=0.15),
                  run_time=0.8)
        self.wait(1.0)

        P_AC = axes.c2p(0.02, f_ac(0.02))     # acoustic  : q -> 0, lower branch
        P_OP = axes.c2p(0.02, g_op(0.02))     # optical   : q -> 0, upper branch
        P_ZB = axes.c2p(0.985, g_op(0.985))   # zone edge : upper branch end
        marker = Dot(radius=0.065, color=YELLOW).move_to(P_AC)

        # ------------------------------------------------ 4. acoustic mode
        lead_ac = Tex("acoustic:", color=TEALC, font_size=30)
        rest_ac = Tex(r"in phase -- $\omega \to 0$ as $q \to 0$",
                      color=INK, font_size=30)
        lbl_ac = VGroup(lead_ac, rest_ac).arrange(RIGHT, buff=0.22)
        lbl_ac.move_to(np.array([-1.6, -2.35, 0.0]))
        self.play(FadeIn(lbl_ac), run_time=0.9)
        self.wait(0.4)
        self.play(FadeIn(marker), run_time=0.5)

        mode.update(amp=0.26, om=1.6, sign=SIGN_AC)
        tau.set_value(0.0)
        self.play(tau.animate.set_value(7 * PI / 1.6),
                  run_time=7 * PI / 1.6, rate_func=linear)
        self.wait(0.5)

        # ------------------------------------------------ 5. optical mode
        # swap happens here: every atom sits exactly at equilibrium (t = k*pi/om),
        # so resetting the clock is invisible.
        mode.update(amp=0.19, om=3.4, sign=SIGN_OP)
        tau.set_value(0.0)
        lead_op = Tex("optical:", color=CORAL, font_size=30)
        rest_op = Tex(r"out of phase -- finite $\omega$ at $q \to 0$",
                      color=INK, font_size=30)
        lbl_op = VGroup(lead_op, rest_op).arrange(RIGHT, buff=0.22)
        lbl_op.move_to(np.array([-1.6, -2.35, 0.0]))
        self.play(FadeOut(lbl_ac), Write(lbl_op), run_time=0.9)
        self.play(marker.animate.move_to(P_OP), run_time=0.9)
        self.wait(0.4)
        self.play(tau.animate.set_value(10 * PI / 3.4),
                  run_time=10 * PI / 3.4, rate_func=linear)
        self.wait(0.5)

        # ------------------------------------------------ 6. zone boundary
        mode.update(amp=0.33, om=2.4, sign=SIGN_ZB)
        tau.set_value(0.0)
        heavy_grp = VGroup(*[atoms[i] for i in range(1, N_ATOMS, 2)])
        lead_zb = Tex(r"zone boundary $q = \pi/a$:", color=YELLOW, font_size=30)
        rest_zb = Tex("one sublattice stands still", color=INK, font_size=30)
        lbl_zb = VGroup(lead_zb, rest_zb).arrange(RIGHT, buff=0.22)
        lbl_zb.move_to(np.array([-1.6, -2.35, 0.0]))
        self.play(FadeOut(lbl_op), Write(lbl_zb), run_time=0.9)
        self.play(heavy_grp.animate.set_fill(opacity=0.45), run_time=0.6)
        self.play(marker.animate.move_to(P_ZB), run_time=0.9)
        self.wait(0.4)
        self.play(tau.animate.set_value(7 * PI / 2.4),
                  run_time=7 * PI / 2.4, rate_func=linear)
        self.wait(0.8)

        # ------------------------------------------------ 7. end card
        everything = VGroup(
            title, legend, baseline, VGroup(*springs), VGroup(*atoms),
            inset_frame, axes, cur_ac, cur_op,
            VGroup(tick0, tick1, ylab, wtp, wtm), marker, lbl_zb,
        )
        self.play(FadeOut(everything), run_time=0.9)
        line1 = MathTex(r"\text{acoustic}", r"\;\to\;", r"\text{sound}",
                        color=INK, font_size=42)
        line1[0].set_color(TEALC)
        line1[2].set_color(YELLOW)
        line2 = MathTex(r"\text{optical}", r"\;\to\;", r"\text{IR spectroscopy}",
                        color=INK, font_size=42)
        line2[0].set_color(CORAL)
        line2[2].set_color(YELLOW)
        end = VGroup(line1, line2).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        src = Tex("chapter 10 -- phonons: diatomic chain eigenmodes",
                  color=DIM, font_size=24).next_to(end, DOWN, buff=0.6)
        self.play(Write(line1), run_time=1.1)
        self.play(Write(line2), run_time=1.1)
        self.play(FadeIn(src), run_time=0.7)
        self.wait(3.0)
