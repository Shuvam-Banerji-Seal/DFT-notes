---
layout: page
title: "Chapter 00 — Welcome"
permalink: /dft-notes/chapter-00/
description: >-
  How to read these notes, the notation we use, the prerequisites, and
  what's deliberately out of scope.
keywords: "DFT, introduction, notation, prerequisites, reading guide"
---

# Chapter 00 — Welcome

> This chapter has no equations. That's the only one. Everything after
> this is math.

These notes are an attempt to write down, in one place, the *minimum
viable theory* of Density Functional Theory — enough to read a modern
DFT paper, set up a calculation, and know which approximations you are
making and why they might be wrong.

## How to read

Each chapter follows the same template:

1. **The claim** — the result or definition, stated precisely.
2. **The proof (or derivation)** — short, with the load-bearing steps
   called out in a callout box.
3. **The code** — a minimal implementation that produces the result.
4. **The catch** — what the formula *doesn't* tell you, and the regime
   where it breaks.

> **Tip.** If you're reading on a phone, the code blocks are
> horizontal-scrollable. If you're reading on the e-reader surface (see
> the [design spec]({{ "/design.md" | relative_url }})), use the font
> slider if the math is too small.

## Prerequisites

- **Linear algebra.** Vector spaces, inner products, eigendecomposition,
  spectral theorem. We assume comfort with bra-ket notation.
- **Calculus of several variables.** Jacobian, divergence, curl, line
  and surface integrals. Green's theorem.
- **Probability.** Expectation values, joint distributions, marginals.
- **Quantum mechanics, undergraduate level.** The postulates, the
  harmonic oscillator, the hydrogen atom. If you have never seen the
  Schrödinger equation before, start with
  [chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}).

## Notation

We use the following conventions consistently. When a chapter deviates,
it says so at the top.

| Symbol            | Meaning                                                |
|:------------------|:-------------------------------------------------------|
| $\mathbf r$       | Position vector in $\mathbb R^3$                       |
| $\hat H$          | Hamiltonian operator                                  |
| $\psi$            | Wavefunction                                          |
| $\Psi$            | Many-body wavefunction                                |
| $\rho$            | One-particle density                                  |
| $\lvert \phi \rangle$ | State in a Hilbert space (ket)                      |
| $\langle \phi \rvert \psi \rangle$ | Inner product                     |
| $\int d\mathbf r$ | Volume integral over all of $\mathbb R^3$             |
| $\nabla$          | Gradient                                              |
| $\nabla^2$        | Laplacian                                             |

Atomic units ($\hbar = m_e = e = 1$) are used throughout unless a
chapter is explicitly working in SI or eV.

## What is *not* in scope

These notes deliberately stop at the Kohn–Sham equations and the
practical zoo of exchange–correlation functionals. The following are
either out of scope or sketched only briefly:

- **Relativistic DFT.** Spin-orbit coupling, the Dirac equation, four-
  component methods.
- **Strong correlation.** DFT+U, DMFT, multireference methods, quantum
  Monte Carlo.
- **Time-dependent DFT.** The Runge–Gross theorem, the linear-response
  regime, excitons.
- **Embedding.** ONIOM, QM/MM, subsystem DFT.
- **Materials-specific machinery.** Phonons, electron-phonon coupling,
  Wannier functions, Berry-phase quantities.

Each of those is a separate knowledge base.

## A short reading list

| Resource                           | Use it for                                               |
|:-----------------------------------|:---------------------------------------------------------|
| Parr & Yang, *Density-Functional Theory of Atoms and Molecules* (1989) | The classical text. Dense but complete. |
| Engel & Dreizler, *Density Functional Theory* (2011) | A gentler, more modern alternative. |
| Burke, *The ABC of DFT* ([ABC of DFT](https://dft.uci.edu/doc/ABC_of_DFT.pdf)) | A 40-page primer. Read this first. |
| Koch & Holthausen, *A Chemist's Guide to DFT* (2nd ed., 2001) | For the chemistry-oriented practitioner. |
| Mardirossian & Head-Gordon, *Thirty Years of Density Functional Theory* (2017) | The modern XC-functional landscape. |

## What's next

[Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) — the
Schrödinger equation and the postulates we'll be building on.

> **Disclaimer.** These notes are a personal study aid. They are
> correct to the best of the author's knowledge, but they are *not* a
> substitute for a textbook. Cite primary sources, not these notes.
