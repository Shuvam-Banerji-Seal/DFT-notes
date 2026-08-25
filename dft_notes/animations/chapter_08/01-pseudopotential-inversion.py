"""
01-pseudopotential-inversion.py
===============================

Troullier-Martins pseudopotential inversion, sketched live.

The all-electron 1s orbital and its pseudo counterpart are drawn on top of
each other (upper panel): the true orbital carries the Coulomb cusp at the
nucleus, the pseudo orbital is smooth and nodeless, and the two curves are
identical beyond the cutoff radius r_c.  Below, the corresponding potentials:
the singular -Z/r versus a finite smooth pseudo-well, again coinciding
beyond r_c.

Companion to chapter 08.  All curves are analytic toy models built with
numpy (quintic Hermite match at r_c), meant to convey the *idea*, not
published TM parameters.

Run from the repo root:
    manim -qm dft_notes/animations/chapter_08/01-pseudopotential-inversion.py \
        PseudopotentialInversion
Writes to:
    dft_notes/animations/chapter_08/videos/... (see render pipeline in README)
"""

import numpy as np
from manim import (
    Scene, Axes, VGroup, Tex, MathTex, Line, DashedLine, Brace, Flash,
    Rectangle, Create, Write, FadeIn, FadeOut, DEGREES,
    UP, DOWN, LEFT, RIGHT, UR, ORIGIN, YELLOW,
)

# ---------------------------------------------------------------- palette
CORAL = "#cc785c"     # all-electron accent
TEALC = "#5db8a6"     # pseudo accent
INK   = "#e8e4de"     # warm off-white text
DIM   = "#9a958c"     # secondary text

# ---------------------------------------------------------------- physics
Z      = 2.0          # nuclear charge of the toy atom
RC     = 1.4          # cutoff radius (bohr)
R_MAX  = 5.0          # plot range
CLIP_V = -8.0         # display clip for -Z/r


def _tm_match(y0, yp0, ypp0, fe, fep, fepp, rc):
    """Quintic polynomial through interior conditions and a C2 match at rc."""
    A = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0],
        [1, rc, rc**2, rc**3, rc**4, rc**5],
        [0, 1, 2 * rc, 3 * rc**2, 4 * rc**3, 5 * rc**4],
        [0, 0, 2, 6 * rc, 12 * rc**2, 20 * rc**3],
    ])
    b = np.array([y0, yp0, ypp0, fe, fep, fepp])
    return np.linalg.solve(A, b)          # ascending powers c0 .. c5


_e_at_rc = np.exp(-Z * RC)
PSI_C = _tm_match(
    0.92, 0.0, -1.6,                   # smooth, flat top at the origin
    _e_at_rc, -Z * _e_at_rc, Z**2 * _e_at_rc,   # value/slope/curvature at rc
    RC,
)
V_C = _tm_match(
    -3.4, 0.0, 2.2,                    # finite smooth well bottom
    -Z / RC, Z / RC**2, -2 * Z / RC**3,
    RC,
)


def psi_ae(r):
    """All-electron 1s: exp(-Zr), cusp slope -Z at the nucleus."""
    return np.exp(-Z * r)


def psi_ps(r):
    """Pseudo 1s: smooth quintic inside rc, exact exp(-Zr) tail beyond."""
    return np.where(r < RC, np.polyval(PSI_C[::-1], r), np.exp(-Z * r))


def v_ae(r):
    """Nuclear attraction, clipped for display."""
    return np.maximum(-Z / r, CLIP_V)


def v_ps(r):
    """Pseudopotential: smooth well inside rc, exact -Z/r beyond."""
    return np.where(r < RC, np.polyval(V_C[::-1], r), -Z / r)


# ---------------------------------------------------------------- layout
AX_W   = 9.0                     # both plots share the same x mapping
AX_H   = 2.3
AX_CX  = -2.1                    # centre x -> left edge at -6.6
PSI_CY = 1.62                    # upper (wavefunction) axes centre
POT_CY = -1.62                   # lower (potential) axes centre
X_RC   = AX_CX - AX_W / 2 + AX_W * RC / R_MAX    # screen x of the cutoff


def legend_row(x, y, color, main_src, sub_src):
    """Colour swatch + name + one-line comment, parked right of the plots."""
    swatch = Line(np.array([x, y, 0.0]), np.array([x + 0.5, y, 0.0]),
                  stroke_width=6, color=color)
    main = Tex(main_src, color=color, font_size=28).next_to(swatch, RIGHT, buff=0.20)
    sub = Tex(sub_src, color=DIM, font_size=22).next_to(main, DOWN, buff=0.10)
    sub.align_to(main, LEFT)
    return VGroup(swatch, main, sub)


class PseudopotentialInversion(Scene):
    def construct(self):
        # ------------------------------------------------ 1. title card
        title = Tex("Pseudopotentials: smooth where it matters",
                    color=INK, font_size=40).to_edge(UP, buff=0.35)
        subtitle = Tex("smooth inside, exact outside -- the Troullier--Martins recipe",
                       color=DIM, font_size=26).next_to(title, DOWN, buff=0.16)
        self.play(Write(title), run_time=1.8)
        self.wait(1.0)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(subtitle),
                  title.animate.scale(0.72).to_edge(UP, buff=0.30),
                  run_time=0.9)

        # --------------------------------------- 2. upper axes (psi panel)
        axU = Axes(
            x_range=[0, R_MAX, 1], y_range=[0, 1.08, 0.5],
            x_length=AX_W, y_length=AX_H,
            axis_config={"stroke_color": DIM, "stroke_width": 2.0,
                         "include_ticks": False},
        ).move_to(np.array([AX_CX, PSI_CY, 0.0]))

        ylab_u = MathTex(r"\psi(r)", color=INK, font_size=30)
        ylab_u.rotate(90 * DEGREES).move_to(np.array([-6.88, PSI_CY, 0.0]))
        xlab_u = MathTex(r"r", color=INK, font_size=28)
        xlab_u.next_to(axU.x_axis.get_end(), DOWN, buff=0.15)

        self.play(Create(axU), run_time=2.0)
        self.play(FadeIn(ylab_u), FadeIn(xlab_u), run_time=0.7)
        self.wait(1.0)

        # ------------------------------------- 3. all-electron 1s (coral)
        ae_curve = axU.plot(psi_ae, x_range=[0, R_MAX],
                            color=CORAL, stroke_width=4)
        leg_ae = legend_row(2.9, 2.05, CORAL,
                            "all-electron 1s", "singular at $r=0$")
        self.play(Create(ae_curve), run_time=3.2)
        self.play(FadeIn(leg_ae, lag_ratio=0.25), run_time=1.0)
        self.wait(2.2)

        # ----------------------------------------- 4. pseudo 1s (teal)
        ps_curve = axU.plot(psi_ps, x_range=[0, R_MAX],
                            color=TEALC, stroke_width=4)
        leg_ps = legend_row(2.9, 1.10, TEALC,
                            "pseudo 1s", "nodeless, smooth top")
        self.play(Create(ps_curve), run_time=3.2)
        self.play(FadeIn(leg_ps, lag_ratio=0.25), run_time=1.0)
        self.wait(2.4)

        # --------------------------------- 5. cutoff radius r_c (dashed)
        rc_line = DashedLine(
            np.array([X_RC, POT_CY - AX_H / 2, 0.0]),
            np.array([X_RC, PSI_CY + AX_H / 2, 0.0]),
            dash_length=0.12, color=DIM, stroke_width=2.5,
        )
        rc_lbl = MathTex(r"r_c", color=INK, font_size=34)
        rc_lbl.next_to(rc_line.get_top(), UR, buff=0.12)
        self.play(Create(rc_line), run_time=1.2)
        self.play(FadeIn(rc_lbl), run_time=0.5)
        self.wait(2.0)

        # ----------------------------------- 6. lower axes (V panel)
        axL = Axes(
            x_range=[0, R_MAX, 1], y_range=[-8.0, 1.0, 2.0],
            x_length=AX_W, y_length=AX_H,
            axis_config={"stroke_color": DIM, "stroke_width": 2.0,
                         "include_ticks": False},
        ).move_to(np.array([AX_CX, POT_CY, 0.0]))

        ylab_l = MathTex(r"V(r)", color=INK, font_size=30)
        ylab_l.rotate(90 * DEGREES).move_to(np.array([-6.88, POT_CY, 0.0]))
        xlab_l = MathTex(r"r", color=INK, font_size=28)
        xlab_l.next_to(axL.x_axis.get_end(), DOWN, buff=0.15)

        self.play(Create(axL), run_time=1.8)
        self.play(FadeIn(ylab_l), FadeIn(xlab_l), run_time=0.7)
        self.wait(1.0)

        # ----------------------------- 7. nuclear potential -Z/r (coral)
        vae_curve = axL.plot(v_ae, x_range=[-Z / CLIP_V, R_MAX],
                             color=CORAL, stroke_width=4)
        leg_vae = legend_row(2.9, -1.10, CORAL,
                             "nucleus: $-Z/r$", "plunges to $-\\infty$")
        self.play(Create(vae_curve), run_time=3.2)
        self.play(FadeIn(leg_vae, lag_ratio=0.25), run_time=1.0)
        self.wait(2.2)

        # -------------------------------- 8. pseudopotential (teal)
        vps_curve = axL.plot(v_ps, x_range=[0, R_MAX],
                             color=TEALC, stroke_width=4)
        leg_vps = legend_row(2.9, -2.05, TEALC,
                             "pseudopotential", "finite, smooth well")
        self.play(Create(vps_curve), run_time=3.0)
        self.play(FadeIn(leg_vps, lag_ratio=0.25), run_time=1.0)
        self.wait(2.2)

        # ------------------------------------------------ 9. cusp beat
        brace_base = Line(axU.c2p(0, 0), axU.c2p(RC, 0))
        cusp_brace = Brace(brace_base, direction=DOWN, buff=0.10)
        cusp_brace.set_color(DIM)
        cusp_lbl = Tex("the Coulomb cusp", color=INK,
                       font_size=26).next_to(cusp_brace, DOWN, buff=0.12)
        self.play(Flash(axU.c2p(0, 1.0), color=CORAL, line_length=0.28,
                        flash_radius=0.25, num_lines=14), run_time=1.0)
        self.play(Create(cusp_brace), FadeIn(cusp_lbl), run_time=1.2)
        self.wait(2.4)
        self.play(FadeOut(cusp_brace), FadeOut(cusp_lbl), run_time=0.8)

        # -------------------------------------------- 10. matching beat
        x_l = X_RC - 0.15
        x_r = AX_CX + AX_W / 2 + 0.15
        match_rect = Rectangle(
            width=x_r - x_l, height=AX_H * 2 + 0.94,
            stroke_width=0, fill_color=YELLOW, fill_opacity=0.07,
        ).move_to(np.array([(x_l + x_r) / 2, 0.0, 0.0]))
        match_rect.set_z_index(-2)
        match_txt = Tex("identical beyond $r_c$", color=YELLOW,
                        font_size=30).move_to(np.array([1.0, 0.0, 0.0]))
        self.play(FadeIn(match_rect), run_time=1.0)
        self.play(Write(match_txt), run_time=1.2)
        self.wait(3.2)

        # ------------------------------------------------ 11. end card
        world = VGroup(
            title, axU, ylab_u, xlab_u, ae_curve, leg_ae,
            ps_curve, leg_ps, rc_line, rc_lbl,
            axL, ylab_l, xlab_l, vae_curve, leg_vae, vps_curve, leg_vps,
            match_rect, match_txt,
        )
        self.play(FadeOut(world), run_time=1.0)

        end1 = Tex("same scattering properties,", color=INK, font_size=42)
        end2 = Tex("no cusp $\\rightarrow$ smaller basis",
                   color=YELLOW, font_size=48)
        end2.next_to(end1, DOWN, buff=0.32)
        end_group = VGroup(end1, end2).move_to(np.array([0.0, 0.35, 0.0]))
        src = Tex("chapter 08  ·  Troullier--Martins pseudopotentials",
                  color=DIM, font_size=24).next_to(end_group, DOWN, buff=0.6)
        self.play(Write(end1), run_time=1.4)
        self.play(Write(end2), run_time=1.4)
        self.play(FadeIn(src), run_time=0.8)
        self.wait(3.4)
