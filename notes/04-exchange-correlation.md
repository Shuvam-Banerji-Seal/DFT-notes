---
layout: page
title: "04 — Exchange–correlation functionals"
permalink: /notes/04-exchange-correlation.html
description: >-
  A guided tour of the exchange–correlation (XC) zoo: LDA, GGA, meta-GGA,
  hybrid, range-separated, and nonlocal correlation. Jacob's ladder of DFT
  functionals, with practical guidance on which functional to use for which
  problem.
keywords: "exchange correlation functional, LDA, GGA, PBE, B3LYP, SCAN, hybrid functional, Jacob's ladder"
---

# 04 — Exchange–correlation functionals

> All of practical DFT lives or dies by the choice of $E_\text{XC}[\rho]$.
> The Hohenberg–Kohn theorems guarantee it *exists* and is *universal*; the
> Kohn–Sham scheme isolates it as the *only* term we still have to approximate.
> This note is a guided tour of the most important approximations.

## 4.1 The shape of the problem

Recall the splitting of the universal functional:

$$
F[\rho] = T_s[\rho] + E_H[\rho] + E_\text{XC}[\rho].
$$

The XC functional must absorb three things at once:

1. The exchange energy of the interacting system.
2. The correlation energy (everything missing from Hartree–Fock).
3. The difference $T - T_s$ between the true interacting kinetic energy and the
   non-interacting KS kinetic energy.

This is the reason XC is hard: it has to model **both** a many-body quantum
effect (exchange, correlation) and a *kinetic* correction. There is no known
exact closed form.

## 4.2 Jacob's ladder

Perdew's famous **"Jacob's ladder"** of DFT functionals ranks approximations by
the *amount of local information* they use:

| Rung | Functional class | Inputs |
| --- | --- | --- |
| 0 | Hartree world (no XC) | — |
| 1 | LDA — Local Density Approximation | $\rho(\mathbf{r})$ |
| 2 | GGA — Generalized Gradient Approximation | $\rho$, $\nabla\rho$ |
| 3 | meta-GGA | $\rho$, $\nabla\rho$, $\nabla^2\rho$, kinetic-energy density $\tau$ |
| 4 | Hybrid | adds a fraction of *exact (HF) exchange* |
| 5 | Double hybrids, RPA, … | adds correlation from MP2 / RPA |

The metaphor: each rung is closer to "chemical heaven" — but every rung has
its place.

## 4.3 Rung 1: Local Density Approximation (LDA)

The simplest approximation. Replace the unknown $E_\text{XC}[\rho]$ by the XC
energy of a **uniform electron gas** (jellium) of the *same local density*:

$$
E_\text{XC}^\text{LDA}[\rho]
= \int \rho(\mathbf{r})\,\varepsilon_\text{xc}^\text{unif}\bigl(\rho(\mathbf{r})\bigr)\,d^3r.
$$

The function $\varepsilon_\text{xc}^\text{unif}(\rho)$ is **known exactly** for
exchange ($\varepsilon_x = -\frac{3}{4}\bigl(\frac{3\rho}{\pi}\bigr)^{1/3}$) and
to arbitrary precision for correlation (Quantum Monte Carlo, Ceperley–Alder,
1980).

**When LDA works surprisingly well:**

- Bond lengths (∼ 1% accuracy).
- Phonon frequencies in simple metals.
- Crystalline structure ranking of many solids.

**Where LDA fails:**

- Strongly correlated electrons.
- Systems with rapidly varying density (atoms, surfaces).
- Reaction barriers (huge underestimates).
- Band gaps (typically 30–50% too small).

## 4.4 Rung 2: GGA

Add information about the local density gradient:

$$
E_\text{XC}^\text{GGA}[\rho]
= \int f\bigl(\rho(\mathbf{r}), \nabla\rho(\mathbf{r})\bigr)\,d^3r.
$$

### PBE

The **Perdew–Burke–Ernzerhof (PBE)** functional (1996) is the canonical
non-empirical GGA. Its enhancement factor satisfies as many exact constraints
of the uniform gas as possible: the LDA linear response, sum rules, and the
correct uniform-gas limit.

### Other popular GGAs

| Functional | Notes |
| --- | --- |
| **PBE** | The default GGA for solids. Non-empirical. |
| **PBEsol** | PBE re-tuned for solids (better lattice constants, worse atomization). |
| **BLYP** | Becke 88 exchange + Lee–Yang–Parr correlation. Historical, popular in chemistry. |
| **B97-D** | Grimme's dispersion-aware GGA. |
| **revPBE** | Re-fit PBE exchange; better for molecular adsorption. |

## 4.5 Rung 3: meta-GGA

A meta-GGA depends on the **kinetic-energy density**

$$
\tau(\mathbf{r}) = \frac{1}{2}\sum_i^\text{occ} |\nabla\phi_i(\mathbf{r})|^2,
$$

in addition to $\rho$ and $\nabla\rho$. This adds genuine non-local
information: $\tau$ discriminates single-orbital regions (covalent bonds,
slowly-varying density) from many-orbital regions (tails, near-nucleus).

### SCAN

The **Strongly Constrained and Appropriately Normed (SCAN)** meta-GGA
(Sun, Ruzsinszky, Perdew, 2015) satisfies **17 known exact constraints** of the
XC functional. SCAN is currently the best non-empirical meta-GGA for
general-purpose use: it is competitive with hybrids for geometries, formation
energies, and many solids — at GGA cost.

| Functional | Cost | Strength | Weakness |
| --- | --- | --- | --- |
| **SCAN** | meta-GGA | Robust generalist; good for solids & molecules | Mild overbinding in some cases |
| **TPSS** | meta-GGA | Earlier meta-GGA, well-tested | Mostly superseded by SCAN |
| **r²SCAN** | meta-GGA | Regularized SCAN — better numerics | Slightly less accurate than SCAN on some tests |

## 4.6 Rung 4: hybrids

A hybrid functional mixes a fraction of **exact Hartree–Fock exchange** into
the GGA/meta-GGA exchange. The intuition: HF exchange is *self-interaction
free*, which corrects one of the worst LDA/GGA errors.

### B3LYP

The most-used functional in computational chemistry:

$$
E_\text{XC}^\text{B3LYP}
= (1 - a_0)\,E_x^\text{LDA} + a_0\,E_x^\text{HF}
+ a_x\,\Delta E_x^\text{B88} + (1 - a_c)\,E_c^\text{VWN} + a_c\,E_c^\text{LYP},
$$

with $a_0 = 0.20$, $a_x = 0.72$, $a_c = 0.81$ — fitted to a set of
molecular atomization energies.

### PBE0

A non-empirical hybrid mixing 25% of HF exchange into PBE:

$$
E_\text{XC}^\text{PBE0}
= \tfrac{1}{4}E_x^\text{HF} + \tfrac{3}{4}E_x^\text{PBE} + E_c^\text{PBE}.
$$

PBE0 is the default in VASP for solid-state work and is dramatically more
accurate than PBE for band gaps, defect levels, and barrier heights.

### Range-separated hybrids

Split exchange into short- and long-range parts with an error function:

$$
\frac{1}{r} = \underbrace{\frac{1 - \operatorname{erf}(\omega r)}{r}}_{\text{SR}}
            + \underbrace{\frac{\operatorname{erf}(\omega r)}{r}}_{\text{LR}}.
$$

The short-range part is treated at the GGA level; the long-range part uses
exact (HF) exchange. This fixes the wrong long-range behavior of semilocal
exchange and is essential for:

- Charge-transfer excitations (use $\omega$ tuned per system, e.g. LC-$\omega$PBE).
- Excitation energies (TDDFT).
- Polarizabilities of long chains.

## 4.7 Dispersion: the missing rung

Standard semilocal DFT cannot describe London dispersion — the long-range
$1/r^6$ tail of the correlation energy between well-separated fragments.
Workarounds:

| Method | Idea |
| --- | --- |
| **DFT-D3 / D4** (Grimme) | Empirical $C_6/r^6$ pairwise (and three-body) terms on top of any functional |
| **vdW-DF** (Dion et al.) | Nonlocal correlation functional of $\rho$, $\nabla\rho$ |
| **VV10 / rVV10** | Similar in spirit, smoother numerics |
| **Many-body dispersion (MBD)** | Treats fragments as coupled dipoles |

> **Practical rule of thumb.** For molecular non-covalent interactions and
> layered materials, **always add a dispersion correction** unless you have
> a good reason not to. PBE-D3(BJ) is a strong default.

## 4.8 What to use for what

| Problem | Recommended functional | Why |
| --- | --- | --- |
| Geometry of a small molecule | B3LYP-D3, PBE0-D3, SCAN-D3 | Hybrid or SCAN gives 0.01 Å accuracy |
| Bulk solid phase stability | PBE, PBEsol, SCAN | Non-empirical; good lattice constants |
| Band gap of a solid | HSE06, PBE0, GW | Semilocal underestimates; hybrid or GW is needed |
| Defect formation energy | SCAN, HSE06, DFT+U | Localization is critical |
| Catalysis (transition metals) | PBE-D3, BEEF-vdW | Good balance + uncertainty quantification |
| Long-range charge transfer | LC-$\omega$PBE, CAM-B3LYP | Long-range HF exchange required |
| Weakly bound complexes | PBE-D3, B97-D, SCAN-D3 | Dispersion is essential |
| Strongly correlated oxides | DFT+U, DMFT | Beyond pure DFT |

---

## See also

- Previous: **[Kohn–Sham equations](03-kohn-sham.html)**
- [References](99-references.html) — original Kohn–Sham paper, PBE (1996),
  SCAN (2015), B3LYP (1993).

## Problems

1. **Show that LDA exchange is exact for the uniform electron gas** by
   computing $E_x$ explicitly from the Slater determinant of plane waves.
2. The enhancement factor $F_x(s)$ of PBE exchange satisfies $F_x(0) = 1$
   and certain high-density-gradient limits. Why are these *physically
   necessary*?
3. The B3LYP parameters were fitted to atomization energies of a small
   molecule set. Why might this *hurt* predictions of solid-state properties?
4. *Conceptual.* If a functional is exact for the uniform gas, the
   one-electron atom, and the two-electron closed shell, must it be exact for
   all systems? Why or why not?
