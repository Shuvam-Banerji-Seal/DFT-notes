---
layout: page
title: "Index of Notes"
permalink: /notes/
description: >-
  Complete index of all notes in the DFT knowledge base, ordered by topic and
  difficulty. Foundations, theorems, practical methods, and references.
keywords: "DFT index, table of contents, notes, density functional theory curriculum"
---

# Index of Notes

A complete, ordered list of every note in this knowledge base. Notes are
numbered in the recommended reading order, but every note is self-contained and
can be read in any order once the prerequisites are met.

## Foundations

| # | Title | Topics | Prerequisites |
| - | --- | --- | --- |
| 01 | [Many-body quantum mechanics primer](01-many-body-qm.html) | Born–Oppenheimer, second quantization, Fock space, the electronic Hamiltonian | Linear algebra, basic QM |
| 02 | [Hohenberg–Kohn theorems](02-hohenberg-kohn.html) | HK I & II, the universal functional, the mapping $v_\text{ext} \leftrightarrow \rho$ | Note 01 |
| 03 | [Kohn–Sham equations](03-kohn-sham.html) | Auxiliary non-interacting system, self-consistent field, $E_\text{XC}[\rho]$ | Note 02 |

## Functionals & approximations

| # | Title | Topics | Prerequisites |
| - | --- | --- | --- |
| 04 | [Exchange–correlation functionals](04-exchange-correlation.html) | LDA, GGA, meta-GGA, hybrids, Jacob's ladder | Notes 02, 03 |
| 05 | *Basis sets & numerical details* (planned) | Plane waves, PAW, Gaussian-type orbitals | Note 03 |

## Practice & applications

| # | Title | Topics | Prerequisites |
| - | --- | --- | --- |
| 06 | *Workflows in VASP / QE / ORCA* (planned) | Input files, convergence, common settings | Note 05 |
| 07 | *Common pitfalls & error estimation* (planned) | SCF convergence, basis-set superposition, basis incompleteness | Note 06 |

## Reference

| # | Title | Topics | Prerequisites |
| - | --- | --- | --- |
| 99 | [References & further reading](99-references.html) | Textbooks, review articles, online resources | — |

---

## How to use these notes

- Each note is a single Markdown file under [`notes/`](https://github.com/Shuvam-Banerji-Seal/DFT-notes/tree/main/notes).
- Math in `$...$` (inline) and `$$...$$` (display) is rendered by **GitHub
  itself** when you read the file on github.com, and by **KaTeX** when you read
  it on the rendered site.
- Each note ends with a **"See also"** section linking to the next notes in
  the curriculum.

## Conventions

We use atomic units throughout ($\hbar = m_e = e = 4\pi\varepsilon_0 = 1$)
unless otherwise stated. The electron density is written $\rho(\mathbf{r})$.
Vectors are bold, operators carry a hat, sets/spaces are calligraphic.
