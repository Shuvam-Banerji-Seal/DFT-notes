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
  C14["14 · Quantum chemistry beyond DFT<br/><small>MP2, CI, CC, CASSCF,<br/>semiempirical, CBS</small>"]
  C15["15 · Relativistic effects<br/><small>Dirac equation, DKH, ZORA,<br/>spin-orbit coupling</small>"]
  C16["16 · Topological materials<br/><small>Chern numbers, Z₂ invariants,<br/>Weyl/Dirac semimetals</small>"]
  C17["17 · Machine learning for DFT<br/><small>Equivariant NNs, MACE,<br/>delta-learning, foundation models</small>"]

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
  C03 --> C14
  C08 --> C15
  C15 --> C16
  C04 --> C17
  C16 --> C17

  classDef shipped fill:#d6dcc8,stroke:#3a4031,color:#1c1f17,stroke-width:1.5px;
  classDef planned stroke-dasharray: 6 4,stroke:#a09d96,fill:#eef0e6,color:#6b7060,stroke-width:1.5px;
  class C00 shipped;
  class C01 shipped;
  class C02 shipped;
  class C03 shipped;
  class C04 shipped;
  class C05 shipped;
  class C06 shipped;
  class C07 shipped;
  class C08 shipped;
  class C09 shipped;
  class C10 shipped;
  class C11 shipped;
  class C12 shipped;
  class C13 shipped;
  class C14 shipped;
  class C15 shipped;
  class C16 shipped;
  class C17 shipped;
  classDef planned stroke-dasharray: 6 4,stroke:#a09d96,fill:#eef0e6,color:#6b7060,stroke-width:1.5px;

  click C00 "javascript:void(0)" "How to read these notes, the notation table, and the prerequisites for the DFT Notes series."
  click C01 "javascript:void(0)" "The postulates of quantum mechanics, the electronic Hamiltonian, and a worked particle-in-a-box derivation."
  click C02 "javascript:void(0)" "Why a single Slater determinant is not enough, the exponential wall, and the full-CI limit."
  click C03 "javascript:void(0)" "Mean-field theory, the Fock operator, the SCF loop, and the Slater–Condon rules for matrix elements."
  click C04 "javascript:void(0)" "Hohenberg–Kohn existence theorem, the Kohn–Sham ansatz, and the practical KS SCF loop."
  click C05 "javascript:void(0)" "Jacob's ladder: LDA, GGA, meta-GGA, hybrid, and range-separated functionals."
  click C06 "javascript:void(0)" "Gaussian-type orbitals, plane waves, real-space grids, and the Roothaan–Hall equations."
  click C07 "javascript:void(0)" "Bloch's theorem, the Brillouin zone, plane-wave cutoffs, and Monkhorst–Pack k-point sampling."
  click C08 "javascript:void(0)" "Norm-conserving, ultrasoft, and PAW pseudopotentials — construction, transferability, and validation."
  click C09 "javascript:void(0)" "Hellmann–Feynman theorem, BFGS and LBFGS optimisers, and convergence criteria for forces and displacements."
  click C10 "javascript:void(0)" "Frozen-phonon supercells, density-functional perturbation theory, and electron–phonon coupling."
  click C11 "javascript:void(0)" "Density of states, projected DOS, band-structure plots, and Fermi-surface visualisation."
  click C12 "javascript:void(0)" "Runge–Gross theorem, linear-response TDDFT, the Casida equations, and excitons."
  click C13 "javascript:void(0)" "DFT+U for strong correlation, hybrid functionals revisited, and a DMFT outlook."
  click C14 "javascript:void(0)" "Quantum chemistry methods beyond DFT: MP2, CI, CCSD(T), CASSCF, NEVPT2, and the basis-set extrapolation ladder."
  click C15 "javascript:void(0)" "The Dirac equation, scalar-relativistic corrections, and spin-orbit coupling in modern DFT."
  click C16 "javascript:void(0)" "Topology in band theory: Chern numbers, Z₂ invariants, topological insulators, and Weyl semimetals."
  click C17 "javascript:void(0)" "Machine learning for DFT: interatomic potentials, equivariant networks, delta-learning, and foundation models."
``'

## Edges

The arrows in the diagram above encode the **prerequisite**
relation.  Reading a chapter assumes the reader is comfortable
with the material in every chapter that points *into* it.  The
table below lists every edge and the reason it exists.

| From | To | Why the dependency |
|:-----|:---|:-------------------|
| C00 | C01 | The how-to-read preamble must come first. |
| C01 | C02 | The Schrödinger picture and the Hamiltonian are needed to set up the many-body problem. |
| C02 | C03 | The Slater-determinant language is the input to Hartree–Fock. |
| C03 | C04 | Hartree–Fock is the reference point against which KS-DFT is derived. |
| C04 | C05 | The XC functional is the only piece KS-DFT leaves undetermined. |
| C05 | C06 | The choice of basis set is entangled with the choice of functional. |
| C06 | C07 | Bloch sums are built from a basis; plane waves are a basis. |
| C06 | C08 | Pseudopotentials are defined by projector-augmented basis operators. |
| C04 | C09 | Forces come from differentiating the KS total energy. |
| C07 | C10 | Phonons need a periodic supercell and k-point sampling. |
| C07 | C11 | Band structures are defined on the Brillouin zone of a periodic system. |
| C04 | C12 | TDDFT is a time-dependent extension of ground-state KS-DFT. |
| C04 | C13 | DFT+U is a correction to the KS exchange–correlation. |
| C03 | C14 | Post-HF methods (MP2, CI, CC, CASSCF) are alternatives to KS-DFT; HF from chapter 3 is the starting point. |
| C08 | C15 | Relativistic effects enter DFT through the pseudopotential (scalar-relativistic and fully-relativistic PPs). |
| C15 | C16 | Topological materials need spin-orbit coupling from chapter 15 (SOC opens band gaps, gives Z₂ invariants). |
| C04 | C17 | ML for DFT uses KS-DFT energies, forces, and densities as the ground truth for training. |
| C16 | C17 | ML methods are increasingly used to predict topological invariants (Chern numbers, Z₂) from band structures. |

## Tracks

After chapter 05 the chapters split into three conceptual
tracks.  Pick the track that matches your problem domain — you
do not have to read all of them.

- **Methods track** (always relevant) — 06 basis sets, 08
  pseudopotentials, 13 DFT+U & beyond, 14 quantum chemistry
  beyond DFT (alternative to DFT), 17 machine learning for DFT
  (fast surrogate).
- **Solids track** (for periodic systems) — 07 PBC, 10 phonons,
  11 band structures, 15 relativistic effects (heavy elements),
  16 topological materials.
- **Dynamics track** (for time-dependent and static-response
  phenomena) — 09 forces & geometry optimisation, 12 TDDFT.
  phenomena) — 09 forces & geometry optimisation, 12 TDDFT.

## Conventions

- Each chapter follows the [template]({{ "/dft-notes/agents/#the-chapter-rigor-checklist" | relative_url }})
  in `agents.md`.  All derivations are step-by-step; no
  calculation is omitted; problem sets have hidden answers.
- The Python code that runs in a chapter also lives in
  [`dft_notes/python_codes/`]({{ site.baseurl }}/dft-notes/python_codes/).
  Each chapter has its own subfolder there; scripts are
  numbered in the order they appear in the chapter; plots are
  committed alongside the script.
- This map is a **living document**.  Every time
  `agent:content-writer' lands a new chapter,
  `agent:diagram-artist' updates this Mermaid graph in the
  same commit — moving the new node from `planned' to
  `shipped`, adding the prerequisite edge, and refreshing the
  `Edges' table.  The `shipped' / `planned' split in
  `classDef' above is the single source of truth.
