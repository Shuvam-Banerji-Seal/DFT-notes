---
layout: page
title: Home
permalink: /
description: >-
  A curated knowledge base on Density Functional Theory (DFT) — Hohenberg–Kohn
  theorems, Kohn–Sham equations, exchange–correlation functionals, and
  computational chemistry methods. Markdown notes with LaTeX math, served as a
  static site on GitHub Pages.
keywords:
  - Density Functional Theory
  - DFT
  - Hohenberg Kohn
  - Kohn Sham
  - exchange correlation functional
  - quantum chemistry
  - computational chemistry
  - electronic structure
  - first principles
  - ab initio
---

<div align="center">

# DFT Notes

### Density Functional Theory — a curated knowledge base

</div>

---

## What is this?

A growing, well-organized set of notes on **Density Functional Theory (DFT)** — the standard workhorse of modern quantum chemistry and computational materials science. Notes are written in **Markdown with LaTeX-style math** and rendered as a fast static site via **Jekyll + KaTeX on GitHub Pages**.

> Density Functional Theory is a quantum-mechanical modelling method used in
> **physics, chemistry, and materials science** to investigate the electronic
> structure (principally the ground state) of many-body systems — atoms,
> molecules, and the condensed phase.

---

## Start here

- **[Foundations of many-body QM](notes/01-many-body-qm.html)** — the prerequisite
  for everything that follows. Second quantization, the electron gas, the
  many-body Hamiltonian.
- **[Hohenberg–Kohn theorems](notes/02-hohenberg-kohn.html)** — the *existence*
  of an exact density functional.
- **[Kohn–Sham equations](notes/03-kohn-sham.html)** — the *practical* route to
  computing the density.
- **[Exchange–correlation functionals](notes/04-exchange-correlation.html)** —
  the LDA / GGA / meta-GGA / hybrid zoo and the Jacob's ladder picture.
- **[References & further reading](notes/99-references.html)** — textbooks,
  review articles, and online resources.

> Links above go to the **rendered HTML pages on this site**. The source
> Markdown files live under [`notes/`](https://github.com/Shuvam-Banerji-Seal/DFT-notes/tree/main/notes).

---

## Why this site?

- **Math-first** — every concept is shown in its actual mathematical form, not
  just handwaved.
- **Readable on both GitHub and the web** — math in `$...$` / `$$...$$` renders
  on GitHub.com *and* is re-typeset with KaTeX on this site.
- **Free, open, citable** — MIT-licensed, easy to fork, easy to contribute to.

---

## A taste of the math

The total energy of a Kohn–Sham system can be written as

$$
E_\text{tot}[\rho] = T_s[\rho] + \int v_\text{ext}(\mathbf{r})\,\rho(\mathbf{r})\,d^3r + E_H[\rho] + E_\text{XC}[\rho]
$$

where each term has a clear physical meaning:

- $T_s[\rho]$ — kinetic energy of a *fictitious* non-interacting system that
  reproduces the same density $\rho(\mathbf{r})$.
- $\int v_\text{ext}\,\rho$ — interaction of the density with an external
  potential (e.g. nuclei).
- $E_H[\rho]$ — classical Hartree (Coulomb) electron–electron repulsion.
- $E_\text{XC}[\rho]$ — everything else: exchange, correlation, and the
  self-interaction correction.

The exact $E_\text{XC}[\rho]$ is **unknown** — the entire zoo of approximate
functionals (LDA, PBE, SCAN, B3LYP, …) is an attempt to model it well enough
to be useful. See the [exchange–correlation note](notes/04-exchange-correlation.html)
for the full story.

---

## Built with

| Tool | Role |
| --- | --- |
| [Jekyll](https://jekyllrb.com/) | Static site generator |
| [KaTeX](https://katex.org/) | Math typesetting (auto-render) |
| [minima](https://github.com/jekyll/minima) | Theme |
| [jekyll-seo-tag](https://github.com/jekyll/jekyll-seo-tag) | SEO + Open Graph + JSON-LD |
| [jekyll-sitemap](https://github.com/jekyll/jekyll-sitemap) | `sitemap.xml` |
| [jekyll-feed](https://github.com/jekyll/jekyll-feed) | `feed.xml` |
| [GitHub Actions](https://github.com/features/actions) | Build + deploy |

---

<div align="center">

[Browse the notes on GitHub →](https://github.com/Shuvam-Banerji-Seal/DFT-notes/tree/main/notes)
&nbsp;·&nbsp;
[Suggest an improvement →](https://github.com/Shuvam-Banerji-Seal/DFT-notes/issues/new/choose)

</div>
