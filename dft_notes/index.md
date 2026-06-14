---
layout: page
title: "Chapters — DFT Notes"
permalink: /dft-notes/
description: >-
  Reader-first knowledge base on Density Functional Theory, organised
  as a progressive walk through the foundations, methods, and
  practice of DFT.
---

# DFT Notes

> A reader-first knowledge base on Density Functional Theory —
> the standard workhorse of modern quantum chemistry and
> computational materials science.

These notes are organised as a **progressive walk** through DFT.
Each chapter builds on the last, but every chapter is also
self-contained enough to be read in isolation. Math is rendered
inline (MathJax 3, with AMS environments loaded); code samples
are Python unless otherwise noted; tables and figures are inline
rather than appendix-pinned.

## Chapters

| #  | Chapter                                       | Topic                                                       |
|:---|:----------------------------------------------|:------------------------------------------------------------|
| 0  | [Welcome]({{ site.baseurl }}/dft-notes/chapter-00/)              | How to read these notes, notation, and prerequisites        |
| 1  | [Schrödinger equation]({{ site.baseurl }}/dft-notes/chapter-01/) | The postulates, the Hamiltonian, and what $\psi$ means     |
| 2  | [The many-body problem]({{ site.baseurl }}/dft-notes/chapter-02/) | Why a single Slater determinant isn't enough, and why       |
| 3  | [Hartree–Fock]({{ site.baseurl }}/dft-notes/chapter-03/)         | Mean-field theory, the Fock operator, and the SCF loop      |
| 4  | [Kohn–Sham DFT]({{ site.baseurl }}/dft-notes/chapter-04/)        | Hohenberg–Kohn existence + Kohn–Sham practical map          |
| 5  | [XC functionals]({{ site.baseurl }}/dft-notes/chapter-05/)       | Jacob's ladder: LDA, GGA, hybrids, range-separated          |

> **Status:** these are *sample* notes — real prose, real math,
> real code, but not yet encyclopaedic. They exist to exercise
> every rendering feature of the future e-reader (see
> [`design.md`]({{ site.baseurl }}/design.md) at the root of
> the repo).

## Reading order

If you're new to DFT, read top-to-bottom. If you're returning to
brush up on a specific topic, each chapter is internally
cross-referenced and the section headers follow the same
template:

1. **The claim** — the result or definition, stated precisely.
2. **The proof (or derivation)** — short, with the load-bearing
   steps called out.
3. **The code** — a minimal implementation that produces the
   result.
4. **The catch** — what the formula *doesn't* tell you, and the
   regime where it breaks.

## Notation

A short, opinionated list — see [chapter 00]({{ site.baseurl }}/dft-notes/chapter-00/) for the full
table.

| Symbol              | Meaning                                                |
|:--------------------|:-------------------------------------------------------|
| $\psi$              | Many-body wavefunction                                 |
| $\rho$              | One-particle density $\rho(\mathbf r) = N \sum_{\sigma} \int \lvert \Psi \rvert^2\, d\mathbf r'$ |
| $\hat H$            | Electronic Hamiltonian                                |
| $E_\text{xc}$       | Exchange–correlation energy                            |
| $v_\text{xc}(\mathbf r)$ | Exchange–correlation potential                    |
| $\phi_i$            | Kohn–Sham orbital                                      |
| $\varepsilon_i$     | Kohn–Sham eigenvalue                                   |
| $\hat T_s$, $\hat J$, $\hat V_\text{ext}$ | KS kinetic, Hartree, external operators  |
