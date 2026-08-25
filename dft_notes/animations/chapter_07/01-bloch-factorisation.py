"""
01-bloch-factorisation.py
=========================

Bloch's theorem in one dimension: a Bloch state factorised into a plane
wave times a cell-periodic part,  psi(x) = e^{ikx} u(x).

Scene graph
-----------
1.  Title card (the master identity).
2.  Top band:    V(x), a row of identical wells, lattice constant a marked.
3.  Middle band: the plane-wave factor e^{ikx} with a sliding k-arrow.
4.  Bottom band: u(x) -- same periodicity as V;  u(x+a) = u(x).
5.  Product band: psi(x) = e^{ikx} u(x) as a modulated wave whose envelope
    is exactly +-u(x).
6.  k varies live (ValueTracker + always_redraw): wavelength changes,
    the envelope stays fixed.
7.  End card: the Bloch condition psi(x+a) = e^{ika} psi(x).

Run from the repo root:
    manim -qm --disable_caching dft_notes/animations/chapter_07/01-bloch-factorisation.py BlochFactorisation
Writes to:
    dft_notes/animations/chapter_07/videos/01-bloch-factorisation.mp4
"""

import numpy as np
from manim import (
    Scene, MathTex, Tex, VGroup, Write, Create, FadeIn, FadeOut, Indicate,
    Line, DashedLine, Arrow, DoubleArrow, GrowArrow, ParametricFunction,
    Dot, ValueTracker, always_redraw, LaggedStart,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI, YELLOW, linear,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # potential / wavevector accents
TEALC = "#5db8a6"     # cell-periodic u(x)
INK   = "#e8e4de"     # warm off-white text / plane wave
DIM   = "#9a958c"     # secondary text, baselines

# ---------------------------------------------------------------- geometry
A_SCR   = 4.0                       # lattice constant on screen
CX0, CX1 = -5.4, 5.4                # curve x-extent
B0, B1   = -5.55, 5.55              # baseline x-extent
Y_V      = 1.90                     # top band    : V(x)
Y_P      = 0.30                     # mid band    : e^{ikx}
Y_U     = -1.30                     # lower band  : u(x)
Y_PS    = -2.98                     # bottom band : psi
A_V      = 0.42                     # V well depth
A_P      = 0.30                     # plane-wave amplitude
LABEL_X  = -6.42                    # left label column
READ_X   = 6.28                     # live k readout (right)


def v_f(t):
    """Periodic potential: identical wells at x = n*A_SCR."""
    return Y_V - A_V * np.cos(PI * t / A_SCR) ** 2


def u_amp(t):
    """Cell-periodic amplitude, period A_SCR, peaks at well centres."""
    return 0.44 * (0.68 + 0.32 * np.cos(PI * t / A_SCR))


def curve(y_of_t, c, w=3.5):
    return ParametricFunction(
        lambda t: np.array([t, y_of_t(t), 0.0]),
        t_range=(CX0, CX1, 0.02), stroke_color=c, stroke_width=w,
    )


def baseline(y):
    return Line(np.array([B0, y, 0.0]), np.array([B1, y, 0.0]),
                stroke_color=DIM, stroke_width=1.5).set_opacity(0.5)


class BlochFactorisation(Scene):
    def construct(self):
        ktr = ValueTracker(0.80)                 # k in units of pi/a
        clock = {"t": 0.0}                       # scene clock for the slide

        ticker = Dot(radius=0.001).set_opacity(0)

        def _tick(_m, dt):
            clock["t"] += dt

        ticker.add_updater(_tick)
        self.add(ticker)

        # ------------------------------------------------ 1. title card
        title = MathTex(
            r"\text{Bloch's theorem: }\;\;",
            r"\psi(x) \;=\;", r"e^{ikx}", r"\;", r"u(x)",
            font_size=36,
        ).to_edge(UP, buff=0.30)
        title[0].set_color(INK)
        title[1].set_color(INK)
        title[2].set_color(CORAL)
        title[4].set_color(TEALC)
        self.play(Write(title), run_time=2.0)
        self.wait(2.2)

        # ------------------------------------------------ 2. V(x): the lattice
        v_lbl = MathTex(r"V(x)", color=CORAL, font_size=28)
        v_lbl.move_to(np.array([LABEL_X, Y_V - 0.20, 0.0]))
        v_base = baseline(Y_V)
        v_curve = curve(v_f, CORAL)

        self.play(FadeIn(v_lbl), run_time=0.8)
        self.play(Create(v_base), Create(v_curve), run_time=2.2)
        self.wait(0.6)

        lat_guides = VGroup(
            DashedLine(np.array([-A_SCR, Y_V - A_V - 0.04, 0.0]),
                       np.array([-A_SCR, Y_V - A_V - 0.24, 0.0]),
                       stroke_color=DIM, stroke_width=2),
            DashedLine(np.array([0.0, Y_V - A_V - 0.04, 0.0]),
                       np.array([0.0, Y_V - A_V - 0.24, 0.0]),
                       stroke_color=DIM, stroke_width=2),
        )
        lat_arrow = DoubleArrow(
            np.array([-A_SCR, Y_V - A_V - 0.32, 0.0]),
            np.array([0.0, Y_V - A_V - 0.32, 0.0]),
            buff=0, stroke_color=CORAL, stroke_width=3,
            tip_length=0.18,
        )
        lat_lbl = MathTex(r"a", color=CORAL, font_size=28)
        lat_lbl.move_to(np.array([-A_SCR / 2, Y_V - A_V - 0.62, 0.0]))
        self.play(LaggedCreate(lat_guides, lat_arrow, lat_lbl), run_time=1.6)
        self.wait(2.0)

        # ------------------------------------------------ 3. plane wave e^{ikx}
        re_lbl = MathTex(r"\mathrm{Re}\,[\,e^{ikx}\,]", color=INK, font_size=24)
        re_lbl.move_to(np.array([LABEL_X, Y_P, 0.0]))

        def make_pw():
            ks = ktr.get_value() * PI / A_SCR
            return curve(lambda t: Y_P + A_P * np.cos(ks * t), INK)

        p_base = baseline(Y_P)
        pw_static = make_pw()
        self.play(FadeIn(re_lbl), run_time=0.8)
        self.play(Create(p_base), Create(pw_static), run_time=2.2)

        pw_live = always_redraw(make_pw)
        self.remove(pw_static)
        self.add(pw_live)

        def make_karrow():
            xc = -4.5 + 0.14 * min(clock["t"], 64.0)
            kd = ktr.get_value()
            L = 0.60 + 0.85 * kd
            arr = Arrow(np.array([xc - L / 2, Y_P - A_P - 0.56, 0.0]),
                        np.array([xc + L / 2, Y_P - A_P - 0.56, 0.0]),
                        buff=0, color=CORAL, stroke_width=5,
                        max_tip_length_to_length_ratio=0.25)
            lab = MathTex(r"k", color=CORAL, font_size=30)
            lab.next_to(arr.get_end(), RIGHT, buff=0.12)
            return VGroup(arr, lab)

        karr_static = make_karrow()
        ticker.clear_updaters()
        self.play(GrowArrow(karr_static[0]), FadeIn(karr_static[1]),
                  run_time=1.0)
        ticker.add_updater(_tick)

        karr_live = always_redraw(make_karrow)
        self.remove(karr_static[0], karr_static[1])
        self.add(karr_live)
        self.wait(3.6)                      # arrow slides along

        # ------------------------------------------------ 4. u(x): same period
        u_eq = MathTex(r"u(x+a) \;=\; u(x)",
                       color=TEALC, font_size=34).move_to(np.array([0.0, 3.02, 0.0]))
        self.play(Write(u_eq), Indicate(title[4], color=TEALC), run_time=1.4)
        self.wait(1.2)

        u_lbl = MathTex(r"u(x)", color=TEALC, font_size=28)
        u_lbl.move_to(np.array([LABEL_X, Y_U, 0.0]))
        u_base = baseline(Y_U)
        u_curve = curve(lambda t: Y_U + u_amp(t), TEALC)

        self.play(FadeIn(u_lbl), run_time=0.8)
        self.play(Create(u_base), Create(u_curve), run_time=2.2)
        self.wait(0.6)

        u_guides = VGroup(
            DashedLine(np.array([0.0, Y_U + 0.10, 0.0]),
                       np.array([0.0, Y_U - 0.14, 0.0]),
                       stroke_color=DIM, stroke_width=2),
            DashedLine(np.array([A_SCR, Y_U + 0.10, 0.0]),
                       np.array([A_SCR, Y_U - 0.14, 0.0]),
                       stroke_color=DIM, stroke_width=2),
        )
        u_arrow = DoubleArrow(
            np.array([0.0, Y_U - 0.22, 0.0]),
            np.array([A_SCR, Y_U - 0.22, 0.0]),
            buff=0, stroke_color=TEALC, stroke_width=3, tip_length=0.18,
        )
        u_per_lbl = MathTex(r"a", color=TEALC, font_size=28)
        u_per_lbl.move_to(np.array([A_SCR / 2, Y_U - 0.44, 0.0]))
        self.play(LaggedCreate(u_guides, u_arrow, u_per_lbl), run_time=1.5)
        dim_grp = VGroup(u_guides, u_arrow, u_per_lbl)
        self.play(Indicate(dim_grp, color=YELLOW), run_time=1.0)
        self.wait(2.0)

        # ------------------------------------------------ 5. product psi(x)
        ps_lbl = MathTex(r"\psi(x)", color=YELLOW, font_size=28)
        ps_lbl.move_to(np.array([LABEL_X, Y_PS, 0.0]))

        def make_prod():
            ks = ktr.get_value() * PI / A_SCR
            return curve(lambda t: Y_PS + u_amp(t) * np.cos(ks * t), YELLOW)

        ps_base = baseline(Y_PS)
        prod_static = make_prod()
        self.play(FadeIn(ps_lbl), run_time=0.8)
        self.play(Create(ps_base), Create(prod_static), run_time=2.4)

        prod_live = always_redraw(make_prod)
        self.remove(prod_static)
        self.add(prod_live)
        self.wait(2.6)

        # ------------------------------------------------ 6. vary k live
        caption = Tex("vary $k$: the plane wave rescales, the envelope $u(x)$ is fixed",
                      color=DIM, font_size=24).move_to(np.array([0.0, -3.74, 0.0]))
        read_static = make_readout(ktr)
        self.play(FadeIn(caption), FadeIn(read_static), run_time=0.9)

        read_live = always_redraw(lambda: make_readout(ktr))
        self.remove(read_static)
        self.add(read_live)

        self.play(ktr.animate.set_value(1.60), run_time=3.6, rate_func=linear)
        self.wait(1.4)
        self.play(ktr.animate.set_value(0.40), run_time=3.8, rate_func=linear)
        self.wait(1.4)
        self.play(ktr.animate.set_value(0.90), run_time=2.8, rate_func=linear)
        self.wait(1.8)

        # ------------------------------------------------ 7. end card
        for m in (pw_live, karr_live, prod_live, read_live, ticker):
            m.clear_updaters()
        everything = VGroup(
            title, u_eq,
            v_lbl, v_base, v_curve, lat_guides, lat_arrow, lat_lbl,
            re_lbl, p_base, pw_live, karr_live,
            u_lbl, u_base, u_curve, u_guides, u_arrow, u_per_lbl,
            ps_lbl, ps_base, prod_live,
            read_live, caption,
        )
        self.wait(1.0)
        self.play(FadeOut(everything), run_time=1.0)

        end1 = MathTex(r"\psi(x+a) \;=\; e^{ika}\,\psi(x)",
                       color=YELLOW, font_size=52).move_to(np.array([0.0, 0.60, 0.0]))
        end2 = Tex("the Bloch condition", color=INK,
                   font_size=32).next_to(end1, DOWN, buff=0.45)
        src = Tex(r"chapter 07 · solids \& periodic boundary conditions",
                  color=DIM, font_size=24).next_to(end2, DOWN, buff=0.55)
        self.play(Write(end1), run_time=1.6)
        self.play(FadeIn(end2), run_time=0.8)
        self.play(FadeIn(src), run_time=0.7)
        self.wait(4.0)


def LaggedCreate(*mobs, **kw):
    """LaggedStart of Create over the given mobjects."""
    return LaggedStart(*[Create(m) for m in mobs],
                       lag_ratio=float(kw.pop("lag_ratio", 0.35)))


def make_readout(tracker):
    return MathTex(
        rf"k = {tracker.get_value():.2f}\;\pi/a",
        color=CORAL, font_size=24,
    ).move_to(np.array([READ_X, Y_P, 0.0]))
