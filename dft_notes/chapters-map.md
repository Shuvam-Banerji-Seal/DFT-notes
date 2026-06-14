---
layout: page
title: "Chapters map"
permalink: /dft-notes/chapters-map/
description: >-
  The full DFT Notes knowledge graph — every chapter past, present,
  and planned, with the reading order.
keywords: "DFT, chapters, map, knowledge graph, learning path"
---

# Chapters map

> The full DFT Notes knowledge graph.  Boxes are chapters; arrows
> are "depends on" (read this after the arrow's source).  Boxes
> with a dashed border are planned but not yet written.

This is the **canonical index** of every chapter that exists or
will exist in this knowledge base.  For a human-readable list,
see the [chapter index]({{ site.baseurl }}/dft-notes/).

```mermaid
%%{init: {'flowchart': {'htmlLabels': true, 'curve': 'basis'}}}%%
graph TD
  C00["00 · Welcome<br/><small>How to read these notes,<br/>notation, prerequisites</small>"]
  C01["01 · Schrödinger equation<br/><small>Postulates, Hamiltonian,<br/>particle-in-a-box</small>"]
  C02["02 · The many-body problem<br/><small>Slater determinants,<br/>exponential wall, full CI</small>"]
  C03["03 · Hartree–Fock<br/><small>Fock operator, SCF,<br/>Slater–Condon rules</small>"]
  C04["04 · Kohn–Sham DFT<br/><small>Hohenberg–Kohn, KS ansatz,<br/>SCF loop</small>"]
  C05["05 · XC functionals<br/><small>LDA → GGA → hybrid → RS,<br/>Jacob's ladder</small>"]
  C06["06 · Basis sets<br/><small>Gaussians, plane waves,<br/>numerical orbitals</small>"]
  C07["07 · Solids & PBC<br/><small>Brillouin zone, Bloch's theorem,<br/>k-point sampling</small>"]
  C08["08 · Pseudopotentials<br/><small>Norm-conserving, ultrasoft,<br/>PAW</small>"]
  C09["09 · Forces & geometry opt<br/><small>Hellmann–Feynman,<br/>BFGS, LBFGS</small>"]
  C10["10 · Phonons & vibrations<br/><small>Frozen phonon, DFPT,<br/>electron–phonon coupling</small>"]
  C11["11 · Band structures<br/><small>DOS, projected DOS,<br/>Fermi surfaces</small>"]
  C12["12 · TDDFT<br/><small>Runge–Gross theorem,<br/>linear response, excitons</small>"]
  C13["13 · DFT+U & beyond<br/><small>Strong correlation,<br/>hybrid functionals, DMFT</small>"]

  C00 --> C01
  C01 --> C02
  C02 --> C03
  C03 --> C04
  C04 --> C05
  C05 --> C06
  C06 --> C07
  C06 --> C08
  C04 --> C09
  C07 --> C10
  C07 --> C11
  C04 --> C12
  C04 --> C13

  classDef planned stroke-dasharray: 6 4,stroke:#a09d96,fill:#eef0e6,color:#6b7060;
  classDef shipped fill:#d6dcc8,stroke:#3a4031,color:#1c1f17;
  class C00,C01,C02,C03,C04,C05,C06,C07,C08 shipped;
  class C09,C10,C11,C12,C13 planned;
```

## Tracks

The chapters above split into three conceptual tracks after
chapter 05:

- **Methods track** (always relevant) — 06 basis sets, 08
  pseudopotentials, 13 DFT+U.
- **Solids track** (for periodic systems) — 07 PBC, 10 phonons,
  11 band structures.
- **Dynamics track** (for time-dependent phenomena) — 09 forces
  (technically static, but it's the first step), 12 TDDFT.

You don't have to read all of them.  Pick the track that matches
your problem domain.

## Conventions

- Each chapter follows the [template]({{ site.baseurl }}/agents.md#the-chapter-rigor-checklist)
  in `agents.md`.  All derivations are step-by-step; no
  calculation is omitted; problem sets have hidden answers.
- The Python code that runs in a chapter also lives in
  [`dft_notes/python_codes/`]({{ site.baseurl }}/dft-notes/python_codes/).
  Each chapter has its own subfolder there; scripts are
  numbered in the order they appear in the chapter; plots are
  committed alongside the script.

> This map is a **living document**.  Every time
> `agent:content-writer` lands a new chapter,
> `agent:diagram-artist` updates this Mermaid graph.
