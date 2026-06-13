---
layout: page
title: "01 — Many-body quantum mechanics primer"
permalink: /notes/01-many-body-qm.html
description: >-
  A concise primer on the many-body quantum mechanics underlying Density
  Functional Theory. Born–Oppenheimer approximation, the electronic Hamiltonian,
  and the Hartree–Fock limit.
keywords: "many-body quantum mechanics, electronic Hamiltonian, Born-Oppenheimer, second quantization, DFT prerequisites"
---

# 01 — Many-body quantum mechanics primer

> **Prerequisites for everything in this knowledge base.** If you already know
> the electronic Hamiltonian and the Born–Oppenheimer approximation cold, you
> can skim this note and move on to the [Hohenberg–Kohn theorems](02-hohenberg-kohn.html).

## 1.1 The full molecular Hamiltonian

Consider a system of $N$ electrons and $M$ nuclei with charges $\{Z_I\}$ and
positions $\{\mathbf{R}_I\}$. The full non-relativistic Hamiltonian (in atomic
units) is

$$
\hat{H}
= \underbrace{-\sum_{i=1}^{N}\frac{1}{2}\nabla_i^2}_{\hat{T}_e}
\;\;
\underbrace{-\sum_{I=1}^{M}\frac{1}{2M_I}\nabla_I^2}_{\hat{T}_n}
\;\;
\underbrace{-\sum_{i,I}\frac{Z_I}{|\mathbf{r}_i-\mathbf{R}_I|}}_{\hat{V}_{en}}
\;\;
\underbrace{+\sum_{i<j}\frac{1}{|\mathbf{r}_i-\mathbf{r}_j|}}_{\hat{V}_{ee}}
\;\;
\underbrace{+\sum_{I<J}\frac{Z_I Z_J}{|\mathbf{R}_I-\mathbf{R}_J|}}_{\hat{V}_{nn}}.
$$

Five terms: electronic kinetic energy $\hat T_e$, nuclear kinetic energy
$\hat T_n$, electron–nucleus attraction $\hat V_{en}$, electron–electron
repulsion $\hat V_{ee}$, and nuclear–nuclear repulsion $\hat V_{nn}$.

> **Atomic units** mean $\hbar = m_e = e = 4\pi\varepsilon_0 = 1$, so all
> quantities are dimensionless and energies are in hartree ($E_h \approx 27.21\,\text{eV}$).

## 1.2 Born–Oppenheimer approximation

Nuclei are 3–5 orders of magnitude heavier than electrons, so they move on a
much slower timescale. The standard **Born–Oppenheimer (BO) approximation**
freezes the nuclei at fixed positions $\{\mathbf{R}_I\}$ and treats them as an
*external potential* acting on the electrons. The electronic Hamiltonian
becomes

$$
\hat{H}_\text{el}
= -\sum_{i=1}^{N}\frac{1}{2}\nabla_i^2
- \sum_{i,I}\frac{Z_I}{|\mathbf{r}_i-\mathbf{R}_I|}
+ \sum_{i<j}\frac{1}{|\mathbf{r}_i-\mathbf{r}_j|},
$$

and the full BO energy is $E_\text{tot} = E_\text{el} + V_{nn}$ with
$V_{nn} = \sum_{I<J} Z_I Z_J / |\mathbf{R}_I - \mathbf{R}_J|$ a constant
(classical, geometry-dependent) shift.

<div class="note-box derivation">
<strong>Why this matters for DFT.</strong> The BO separation means DFT operates
on an <em>electronic</em> problem with a parametric dependence on the nuclear
coordinates. The output of a DFT calculation is the electronic energy
$E_\text{el}[\{\mathbf{R}_I\}]$, which is then used to scan geometries, find
minima, compute forces, and run molecular dynamics.
</div>

## 1.3 The electronic wavefunction

The exact ground state of $\hat H_\text{el}$ is an antisymmetric
$N$-electron wavefunction $\Psi(\mathbf{x}_1, \dots, \mathbf{x}_N)$, where
$\mathbf{x}_i = (\mathbf{r}_i, \sigma_i)$ is a combined space–spin coordinate.
Antisymmetry under exchange is the entire reason we have the Pauli principle,
Fermi statistics, exchange energy, and ultimately the *shape* of the
exchange–correlation functional.

> The dimensionality of the problem grows exponentially with $N$. A naive
> grid-based representation of a 10-electron wavefunction in 3D already requires
> storing a 30-dimensional antisymmetric tensor — infeasible for any
> $N \gtrsim 5$. **Density functional theory replaces the wavefunction by the
> density $\rho(\mathbf{r})$, a 3-dimensional object.**

## 1.4 Hartree–Fock: the starting point for everything

The simplest variational ansatz for $\Psi$ is a single Slater determinant of
$N$ orthonormal spin-orbitals $\{\phi_i(\mathbf{x})\}$:

$$
\Psi(\mathbf{x}_1, \dots, \mathbf{x}_N)
= \frac{1}{\sqrt{N!}}
\begin{vmatrix}
\phi_1(\mathbf{x}_1) & \cdots & \phi_N(\mathbf{x}_1) \\
\vdots              & \ddots & \vdots              \\
\phi_1(\mathbf{x}_N) & \cdots & \phi_N(\mathbf{x}_N)
\end{vmatrix}.
$$

The Hartree–Fock energy functional is obtained by evaluating
$\langle \Psi | \hat H_\text{el} | \Psi \rangle$:

$$
E_\text{HF}[\{\phi_i\}]
= \sum_i \langle \phi_i | \hat h | \phi_i \rangle
+ \frac{1}{2}\sum_{i,j}\bigl(J_{ij} - K_{ij}\bigr),
$$

where $\hat h$ is the one-electron part, $J_{ij}$ is the **Coulomb
(self-)interaction** of the two charge densities $|\phi_i|^2$ and $|\phi_j|^2$,
and $K_{ij}$ is the **exchange** integral — a quantum, spin-resolved
correction that has no classical analogue.

<div class="note-box warn">
<strong>Hartree–Fock misses electron correlation.</strong> A single Slater
determinant cannot represent the cusp in the wavefunction at electron–electron
coalescence. The missing piece is called <em>correlation energy</em>:
$E_\text{corr} = E_\text{exact} - E_\text{HF}$. DFT's modern strength is that
carefully designed exchange–correlation functionals recover a large fraction of
$E_\text{corr}$ at a cost much lower than post-HF methods.
</div>

## 1.5 The electronic density

For our purposes the central observable is the **spin-summed electron
density**:

$$
\rho(\mathbf{r})
= N \sum_{\sigma_1,\dots,\sigma_N}
\int
\bigl|\Psi(\mathbf{x}_1, \dots, \mathbf{x}_N)\bigr|^2
\, d^3 r_2 \cdots d^3 r_N,
$$

with $\mathbf{x}_1 = (\mathbf{r}, \sigma_1)$.

Two properties are crucial:

- $\rho(\mathbf{r}) \geq 0$ everywhere.
- $\int \rho(\mathbf{r})\,d^3r = N$ (normalization to the number of electrons).

The astonishing claim of the Hohenberg–Kohn theorems (next note) is that
*this 3-dimensional scalar field* is in one-to-one correspondence with the
external potential — and therefore with every observable of the system.

---

## See also

- Next: **[Hohenberg–Kohn theorems](02-hohenberg-kohn.html)**
- [References](99-references.html) — Parr & Yang, Dreizler & Gross, Burke's "ABC of DFT".

## Problems

1. Verify the antisymmetry of a Slater determinant under exchange of two rows.
2. Show that the Hartree–Fock energy is *self-interaction free*: a
   one-electron system has $E_\text{HF}$ equal to the exact energy. (Hint: $K_{11} = J_{11}$.)
3. In atomic units, what is the BO energy of two protons at infinite separation
   with no electrons? Why is this a meaningful limiting case?
