---
layout: page
title: "03 — Kohn–Sham equations"
permalink: /notes/03-kohn-sham.html
description: >-
  The Kohn–Sham equations replace the interacting many-electron problem with an
  auxiliary system of non-interacting electrons moving in an effective
  potential. The only unknown is the exchange–correlation functional.
keywords: "Kohn Sham equations, self-consistent field, SCF, exchange correlation potential, auxiliary non-interacting system"
---

# 03 — Kohn–Sham equations

> Where the Hohenberg–Kohn theorems say *what* should exist, the **Kohn–Sham
> (KS) scheme** (1965) says *how to compute it*. The KS construction replaces
> the interacting many-body system by a fictitious, *non-interacting*
> reference system that reproduces the same density $\rho(\mathbf{r})$.

## 3.1 The idea

The exact interacting kinetic energy $T[\rho]$ is unknown and very hard to
approximate. Kohn and Sham's brilliant move: **don't approximate it at all**.
Instead, compute the kinetic energy of a *fictitious* non-interacting system
of electrons that yields the same density, and lump all the error into a
small correction term $E_\text{XC}[\rho]$.

We split the universal functional as

$$
F[\rho] = T_s[\rho] + E_H[\rho] + E_\text{XC}[\rho],
$$

where

- $T_s[\rho]$ — kinetic energy of the non-interacting KS system,
- $E_H[\rho] = \tfrac{1}{2}\iint \frac{\rho(\mathbf{r})\rho(\mathbf{r}')}{|\mathbf{r}-\mathbf{r}'|}\,d^3r\,d^3r'$ — classical Hartree self-repulsion,
- $E_\text{XC}[\rho]$ — **everything else**: exchange, correlation, and the
  self-interaction correction.

The total energy is

$$
E_\text{KS}[\rho]
= T_s[\rho] + \int v_\text{ext}(\mathbf{r})\rho(\mathbf{r})\,d^3r
+ E_H[\rho] + E_\text{XC}[\rho].
$$

## 3.2 The KS orbitals and equations

To handle the *non-interacting* kinetic energy $T_s[\rho]$, we introduce
**Kohn–Sham orbitals** $\{\phi_i(\mathbf{r})\}$ with

$$
\rho(\mathbf{r}) = \sum_{i=1}^{N} |\phi_i(\mathbf{r})|^2
\quad \text{(occupied orbitals only, spin-paired case)},
$$

and

$$
T_s = -\frac{1}{2}\sum_{i=1}^{N} \langle \phi_i | \nabla^2 | \phi_i \rangle.
$$

Imposing $\delta E_\text{KS}/\delta \phi_i^* = 0$ (subject to orthonormal
$\{\phi_i\}$) yields the **Kohn–Sham equations**:

$$
\boxed{\;
\left[-\frac{1}{2}\nabla^2 + v_\text{eff}(\mathbf{r})\right]\phi_i(\mathbf{r})
= \varepsilon_i\,\phi_i(\mathbf{r})
\;}
$$

with the **effective KS potential**

$$
v_\text{eff}(\mathbf{r})
= v_\text{ext}(\mathbf{r}) + v_H(\mathbf{r}) + v_\text{XC}(\mathbf{r}),
$$

where

- $v_H(\mathbf{r}) = \delta E_H/\delta\rho = \int \frac{\rho(\mathbf{r}')}{|\mathbf{r}-\mathbf{r}'|}\,d^3r'$,
- $v_\text{XC}(\mathbf{r}) = \delta E_\text{XC}/\delta\rho(\mathbf{r})$.

The KS equations have the form of a single-particle Schrödinger equation, but
$v_\text{eff}$ *depends on the orbitals* through $\rho$. They are therefore
solved **self-consistently** (the "SCF loop").

## 3.3 The self-consistent field (SCF) loop

<div class="note-box derivation">
<strong>Algorithm — single-point KS-DFT calculation</strong>
<ol>
<li>Start with an initial guess for the density $\rho^{(0)}(\mathbf{r})$.</li>
<li>Build $v_\text{eff}^{(k)}(\mathbf{r}) = v_\text{ext} + v_H[\rho^{(k)}] + v_\text{XC}[\rho^{(k)}]$.</li>
<li>Solve $\bigl[-\tfrac12\nabla^2 + v_\text{eff}^{(k)}\bigr]\phi_i^{(k+1)} = \varepsilon_i^{(k+1)}\phi_i^{(k+1)}$.</li>
<li>Compute the new density $\rho^{(k+1)}(\mathbf{r}) = \sum_i |\phi_i^{(k+1)}|^2$.</li>
<li>Mix $\rho^{(k+1)}$ with previous iterations to stabilize convergence.</li>
<li>Repeat from 2 until $|\rho^{(k+1)} - \rho^{(k)}| < \text{tol}$.</li>
</ol>
</div>

In practice, mixing schemes (Pulay, Broyden, Kerker) and preconditioners are
essential — naïve density mixing diverges for metallic systems.

## 3.4 What the orbital energies mean

For the exact functional, the **highest occupied KS eigenvalue** equals the
minus of the first ionization energy (Janak's theorem, plus the
*Perdew–Levy–Balduz* extension):

$$
\varepsilon_\text{HOMO} = -I.
$$

This is one of the very few exact statements we have. Other eigenvalues have
only approximate interpretations:

| Quantity | Approximate meaning |
| --- | --- |
| HOMO | $-I$ (ionization potential) — *exact* |
| LUMO | $-A$ (electron affinity) — exact for the *exact* functional with the derivative discontinuity |
| Gap $\varepsilon_\text{LUMO} - \varepsilon_\text{HOMO}$ | The **KS gap**, $\neq$ the *fundamental* gap. Always underestimated with semilocal functionals. |
| Lower occupied | Roughly minus binding energies from photoemission (Koopmans-like) |

## 3.5 What KS gets right and what it doesn't

<div class="note-box idea">
<strong>What works.</strong> Geometries, harmonic frequencies, dipole moments,
barriers, adsorption energies (with the right functional!), phase stability of
solids — for these, KS-DFT with a sensible GGA or hybrid is often within a
few percent of experiment.
</div>

<div class="note-box warn">
<strong>What fails badly.</strong>
<ul>
<li>Strongly correlated electrons (e.g. <em>Mott insulators</em>) — needs DFT+U, DMFT, or multireference methods.</li>
<li>Long-range charge-transfer excitations — needs long-range-corrected hybrids or range-separated functionals.</li>
<li>Van der Waals / dispersion — needs explicit dispersion corrections (D3, D4, nonlocal correlation, etc.) or many-body methods.</li>
<li>Self-interaction error — semilocal functionals delocalize electrons too much, producing too-small band gaps, over-delocalized polarons, etc.</li>
</ul>
</div>

## 3.6 Beyond KS

When KS-DFT isn't enough, several routes exist:

- **DFT+U** — add a Hubbard-like penalty on localized $d$/$f$ occupancies.
- **Hybrid functionals** — mix a fraction of exact (Hartree–Fock) exchange into $E_\text{XC}$.
- **Range-separated hybrids** — HF exchange only at long range.
- **DMFT** — embed a correlated impurity in a KS bath.
- **GW** — compute quasi-particle spectra on top of KS orbitals.

These are noted for context; details in dedicated notes later.

---

## See also

- Previous: **[Hohenberg–Kohn theorems](02-hohenberg-kohn.html)**
- Next: **[Exchange–correlation functionals](04-exchange-correlation.html)**
- [References](99-references.html) — Kohn–Sham (1965) original paper, Parr & Yang Ch. 7.

## Problems

1. Show that for a one-electron system, $E_H + E_\text{XC} = 0$ (no
   self-interaction).
2. Use Janak's theorem to show that the derivative of $E_\text{KS}$ with
   respect to orbital occupation $f_i$ is $\varepsilon_i$.
3. **In a real-space grid code, the most expensive step is almost always the
   Poisson solve for $v_H$. Why?**
