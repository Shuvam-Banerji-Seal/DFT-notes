---
layout: page
title: "Software cheatsheet"
permalink: /dft-notes/extras/software-cheatsheet/
description: >-
  The practical "which code should I use" reference. Every
  electronic-structure code the working calculator actually
  reaches for, organised by use case — molecular Gaussian,
  plane-wave / PAW, all-electron, real-space grid, wavelet,
  high-accuracy wavefunction, special-system, visualisation,
  and workflow.
keywords: "software, codes, PySCF, Psi4, ORCA, Q-Chem, Gaussian,
  VASP, Quantum ESPRESSO, CASTEP, ABINIT, CP2K, WIEN2k, Elk,
  FLEUR, Octopus, GPAW, SIESTA, BigDFT, MRCC, CFOUR, CRYSTAL,
  FHI-aims, exciting, WEST, Yambo, VESTA, OVITO, ParaView,
  XCrySDen, ASE, AiiDA, Fireworks, atomate"
---

# Software cheatsheet

> The DFT chapters tell you *what* the equations are. This
> page tells you *which program to run* when you actually
> want a number.

The cheatsheet is organised by **use case**, not by history.
Each section opens with a summary table and follows with a
short profile of every code in the category: name, license,
language, repository, the DFT methods it implements, the
basis sets / boundary conditions it supports, the DFT Notes
chapters it is most relevant to, and a "when to use"
recommendation.

> **How to read this page.** Jump to the section that matches
> the *boundary condition* of your system (molecule vs. solid
> vs. surface) and its *physics* (ground-state DFT vs. TDDFT
> vs. high-accuracy wavefunction vs. excited-state $GW$/BSE).
> The chapter cross-references in each profile are the most
> useful pointers: chapter numbers tell you *which*
> theoretical machinery the code is exposing to you.

---

## Table of contents

1. [Molecular / cluster codes (Gaussian basis)](#1-molecular--cluster-codes-gaussian-basis)
2. [Plane-wave / PAW codes](#2-plane-wave--paw-codes)
3. [All-electron codes (full potential)](#3-all-electron-codes-full-potential)
4. [Real-space grid codes](#4-real-space-grid-codes)
5. [Wavelet codes](#5-wavelet-codes)
6. [Coupled-cluster / high-accuracy wavefunction](#6-coupled-cluster--high-accuracy-wavefunction)
7. [Codes for special systems](#7-codes-for-special-systems)
8. [Visualisation](#8-visualisation)
9. [Workflow managers](#9-workflow-managers)

---

## 1. Molecular / cluster codes (Gaussian basis)

For finite systems (molecules, clusters, bio-organic
fragments, transition-metal complexes). Common thread: a
**Gaussian-type orbital (GTO)** basis
([chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.3–6.6)
centred on the atoms, with the Fock or Kohn–Sham matrix
built from analytical electron-repulsion integrals
([chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.6.3).

| Code     | License              | Language      | Best at                                          |
|:---------|:---------------------|:--------------|:-------------------------------------------------|
| PySCF    | Apache-2.0           | Python (C ext)| Open-source QC, embedding, method development    |
| Psi4     | LGPL-3.0             | Python / C++  | Open-source thermochemistry, DFT, CC             |
| ORCA     | Free for academics   | C++           | Main-group, TM spectroscopy, multi-reference     |
| Q-Chem   | Commercial           | C++ / Fortran | High-throughput, large molecules, excited states |
| Gaussian | Commercial           | Fortran       | General-purpose, broad method coverage           |

### 1.1 PySCF

- **License:** Apache-2.0. **Language:** Python (C kernels).
  **Repo:** <https://github.com/pyscf/pyscf>
- **DFT methods:** RKS / UKS / GKS DFT, hybrid and
  range-separated functionals ([chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4–5.5),
  collinear and non-collinear spin-DFT, density-fitting DFT,
  explicit-response TDDFT, real-time TDDFT, DFT+DMFT.
- **Basis sets:** GTOs. Pople, Dunning, Karlsruhe (def2),
  ANO, even-tempered; user-defined sets.
- **DFT Notes chapters:** 03, 04, 05, 06.
- **When to use.** The de facto open-source QC code. The
  right default for *method development*: the entire SCF,
  ERI contraction, and DIIS loop is in plain `numpy`-readable
  Python, and the source compiles in minutes. It is *not*
  the right default for *production* CCSD(T) on a 50-atom
  organic molecule with a triple-zeta basis — Psi4 or
  Q-Chem will be 3–10× faster because they ship hand-tuned
  integral engines (Libint) and more aggressive
  parallelisation. For TM multi-reference work, use ORCA
  or PySCF's CASSCF.

### 1.2 Psi4

- **License:** LGPL-3.0. **Language:** Python front end,
  C++ back end. **Repo:** <https://github.com/psi4/psi4>
- **DFT methods:** SCF, DFT (LDA, GGA, hybrid,
  range-separated), explicit-response TDDFT, ADC(2),
  EOM-CCSD, MP2, MP3, CC2, CCSD, CCSD(T), SAPT, DFT-SAPT,
  FCIQMC plugin. Geometry optimisation, harmonic
  frequencies, IRC, transition states.
- **Basis sets:** GTOs. Pople, Dunning, Karlsruhe, JKFIT
  / RIFIT auxiliary bases, ccECP effective core
  potentials.
- **DFT Notes chapters:** 02, 03, 04, 05, 06.
- **When to use.** The right pick for open-source
  *production* quantum chemistry at small-to-medium scale.
  The C++ side uses Libint and is fast; the Python front
  end is pleasant to script. The community is friendly
  and the documentation is excellent. For TM
  multi-reference work, reach for ORCA or PySCF.

### 1.3 ORCA

- **License:** Free for academic use; commercial for
  industry (source-available, not OSI open source).
  **Language:** C++. **Repo:** <https://orcaforum.kofo.mpg.de/>
- **DFT methods:** SCF, KS-DFT (LDA, GGA, meta-GGA, hybrid,
  range-separated, double-hybrid), TDDFT, RIJCOSX,
  broken-symmetry DFT for antiferromagnets, CASSCF,
  NEVPT2, MRCI, DLPNO-CCSD(T), CEPA. Strong on
  spectroscopy: UV/Vis, XAS, EPR, NMR, Mössbauer.
- **Basis sets:** GTOs. def2 family, SARC auxiliary bases
  for transition metals, Karlsruhe segmented-contracted
  sets.
- **DFT Notes chapters:** 03, 04, 05, 06.
- **When to use.** The de facto standard in *inorganic and
  organometallic* quantum chemistry. **DLPNO-CCSD(T)**
  makes canonical-accuracy coupled cluster tractable on
  100–200-atom systems; the broken-symmetry DFT framework
  is the workhorse for antiferromagnetic TM clusters
  ([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.8.5);
  the spectroscopy modules are unmatched. The main
  weakness is the closed-source distribution and the
  steep licence procedure.

### 1.4 Q-Chem

- **License:** Commercial. **Language:** C++ / Fortran.
  **Repo:** <https://www.q-chem.com/>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  range-separated, double-hybrid), explicit-response
  TDDFT, ADC(2), EOM-CCSD, CCSD(T), EOM-CC methods,
  spin-flip TDDFT, ab-initio MD, fragment-based methods
  (ALMO, FMO, XPol), constrained DFT, non-equilibrium PCM.
- **Basis sets:** GTOs. Pople, Dunning, Karlsruhe, midbond
  functions, user-definable.
- **DFT Notes chapters:** 03, 04, 05, 06.
- **When to use.** The right pick for *high-throughput
  quantum chemistry* in a commercial setting: pharmaceutical
  screening, large-molecule excited states (EOM-CCSD is
  well-developed), spin-flip TDDFT for diradicals. The
  fragment-based methods (ALMO) are unmatched for large
  covalently-bonded systems.

### 1.5 Gaussian

- **License:** Commercial. **Language:** Fortran.
  **Repo:** <https://gaussian.com/>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  range-separated, double-hybrid), TDDFT, MP2, MP4, CCSD,
  CCSD(T), CASSCF, CASPT2, ECP, ONIOM, PCM, SMD. The
  broadest method coverage in the commercial QC
  ecosystem, with a 50-year track record.
- **Basis sets:** GTOs. STO-nG, 3-21G, 6-31G family,
  6-311G family, cc-pV*X*Z, aug-cc-pV*X*Z, LanL2DZ, SDD,
  ANO.
- **DFT Notes chapters:** 03, 04, 05, 06.
- **When to use.** The right pick for *publication-
  benchmark* organic-chemistry calculations where maximum
  compatibility with the historical record is wanted
  (chapter 05 §5.4 explains why B3LYP is the lingua
  franca). GaussView is unmatched for setting up geometry
  optimisations, IRCs, and NMR calculations. The Fortran
  internals are old, parallel scaling is poor past ~32
  cores, and the licence model is restrictive. For new
  *method-development* work the open-source codes win; for
  new *production* work in TM chemistry, ORCA wins.

---

## 2. Plane-wave / PAW codes

For **periodic solids**: crystals, surfaces, defects,
interfaces, liquids (with PBC). The common thread is a
**plane-wave basis**
([chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7,
[chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}))
with **Bloch's theorem** for periodicity
([chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.3)
and **pseudopotentials or PAW** to handle the core
electrons ([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }})).
The plane-wave basis is *position-independent*, which
eliminates the Pulay force
([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7.3).

| Code                | License           | Language   | Best at                                       |
|:--------------------|:------------------|:-----------|:----------------------------------------------|
| Quantum ESPRESSO    | GPL               | Fortran    | Open-source periodic DFT, phonons, TDDFT      |
| VASP                | Commercial        | Fortran    | Industry / academic standard for solids       |
| CASTEP              | Commercial (UK)   | Fortran    | UK academic, phonons, NMR, TDDFT              |
| ABINIT              | GPL               | Fortran    | Open-source, response properties, GW          |
| CP2K                | GPL               | Fortran    | Mixed Gaussian / plane wave, AIMD, large cells |
| WIEN2k              | Commercial (ac.)  | Fortran    | Full-potential LAPW (see §3)                  |

### 2.1 Quantum ESPRESSO

- **License:** GPL. **Language:** Fortran 2003.
  **Repo:** <https://gitlab.com/QEF/q-e>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid
  HSE06, PBE0, exact exchange), spin-polarised and
  non-collinear DFT, DFT+U(+V), Wannier-function methods
  (Wannier90), TDDFT in the real-time (`turboTDDFT`) and
  linear-response (`turboEELS`) flavours, $G_0W_0$ and $GW$
  via `Yambo` and `West`, phonon dispersion and
  electron-phonon coupling (`EPW`), NMR chemical shifts
  (`QE-Knopp`), Hubbard parameters (`HP`),
  Born–Oppenheimer and Car–Parrinello MD.
- **Basis sets:** Plane waves (kinetic cutoff
  $E_\text{cut}$), with norm-conserving (Troullier–Martins,
  ONCV), ultrasoft, or PAW datasets from the `pseudodojo`
  library.
- **DFT Notes chapters:** 04, 05, 06 §6.7, 07, 08.
- **When to use.** The de facto open-source plane-wave DFT
  code. The right pick for any *academic* solid-state DFT
  project that wants to read, modify, and publish the
  source. The phonons module is the most-used open-source
  phonon code. The hybrid / GW / TDDFT stack is
  well-maintained but a step behind VASP in
  user-friendliness. If you want a method VASP does not
  have (Wannier interpolation, second-variational
  spin–orbit, $G_0W_0$ at scale), Quantum ESPRESSO is
  usually the right pick.

### 2.2 VASP

- **License:** Commercial. **Language:** Fortran.
  **Repo:** <https://www.vasp.at/>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  PBE0, HSE06, SCAN, r²SCAN, exact exchange),
  spin-polarised and non-collinear DFT, DFT+U, DFT+DMFT
  via external interface, electric-field response, dipole
  corrections, GW and BSE via the `vasp_gw` module, MD,
  NEB, dimer method, finite-difference phonons, ML
  force-field interface.
- **Basis sets:** Plane waves with **PAW** augmentation
  ([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7, §8.12).
  The PAW library is the most extensive in the field: a
  wide range of valence configurations (small-core,
  large-core, $d$- and $f$-electron "sv" / "pv" / "d" /
  "s" variants).
- **DFT Notes chapters:** 04, 05, 06, 07, 08.
- **When to use.** The workhorse of *industrial and
  academic solid-state DFT*. The materials community has
  converged on it, and the convergence of opinion is
  itself a reason to use it: every reviewer of a
  solid-state paper expects to see "VASP" in the methods
  section. The PAW library is the deepest, the parallel
  efficiency is the highest, and the documentation is
  comprehensive. The main weaknesses are the closed-source
  licence and the cost. For light elements in simple
  structures, Quantum ESPRESSO produces equivalent
  results. For strongly-correlated oxides
  ([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.5),
  VASP + DFT+U is the workhorse; for $GW$ spectroscopy,
  VASP GW or Yambo on top of VASP is standard.

### 2.3 CASTEP

- **License:** Commercial, but the **UK academic site
  licence** gives every UK university unlimited use.
  **Language:** Fortran. **Repo:** <https://www.castep.org/>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  exact exchange), spin-polarised DFT, DFT+U, NMR
  chemical shifts, EELS, phonon dispersion,
  electron-phonon coupling, TDDFT in the linear-response
  Casida formulation, ab-initio MD (NVT, NPT, metadynamics
  via PLUMED), NEB, transition-state search,
  linear-scaling DFT for large cells (DFPT + TS).
- **Basis sets:** Plane waves with norm-conserving or
  ultrasoft pseudopotentials. PAW is not native; the
  on-the-fly-generated "C9" library is well-tested.
- **DFT Notes chapters:** 04, 05, 06, 07, 08.
- **When to use.** A strong pick for *UK academic*
  solid-state work where the licence is free; outside the
  UK, Quantum ESPRESSO is the standard open-source
  alternative. The NMR chemical-shift and EELS modules
  are particularly well-developed. The phonon and
  electron-phonon coupling suite is mature. The user
  community is smaller than VASP / Quantum ESPRESSO's.

### 2.4 ABINIT

- **License:** GPL. **Language:** Fortran 2003.
  **Repo:** <https://github.com/abinit/abinit>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  exact exchange), spin-polarised DFT, DFT+U,
  linear-response DFPT for phonons, dielectric response,
  Born effective charges, IR / Raman, $G_0W_0$ (the
  `Optics` and `SIGMA` modules are the workhorse $GW$
  code for the open-source community), BSE, TDDFT in the
  Casida and Sternheimer flavours, electron stopping
  power, electron–phonon coupling, finite electric
  fields, orbital-free DFT, PAW (Blöchl's original 1994
  algorithm); one of the most mature *response-property*
  suites in the field.
- **Basis sets:** Plane waves. Norm-conserving
  pseudopotentials (Troullier–Martins, ONCV), PAW
  datasets from the ABINIT `JTH` table.
- **DFT Notes chapters:** 04, 05, 06, 07, 08; also the
  response-property chapters 10/11 (in preparation).
- **When to use.** The right pick for *response-property*
  and *many-body perturbation theory* work where the
  open-source path is mandatory. The DFPT implementation
  is one of two production implementations in the world
  (the other being Quantum ESPRESSO's `PHonon`);
  ABINIT's response suite is broader. The $G_0W_0$
  implementation is the most-used open-source $GW$ code.
  ABINIT is *not* the right pick for high-throughput
  materials screening (no comprehensive potential
  library, no batch interface).

### 2.5 CP2K

- **License:** GPL. **Language:** Fortran 2003
  (MPI / OpenMP hybrid, GPU via CUDA / HIP).
  **Repo:** <https://github.com/cp2k/cp2k>
- **DFT methods:** KS-DFT in the **mixed Gaussian /
  plane-wave (GPW)** and Gaussian / augmented-plane-wave
  (GAPW) flavours. LDA, GGA, meta-GGA, hybrid (HFX, PBE0,
  HSE06 via truncated Coulomb), DFT+U, range-separated
  hybrids, MP2, RPA, GW, TDDFT, Ehrenfest MD,
  Born–Oppenheimer MD, metadynamics (PLUMED), NEB,
  finite-temperature DFT, ML potentials (MTP); one of
  the *fastest* ab-initio MD codes for systems in the
  100–10,000-atom range.
- **Basis sets:** Gaussian for the wavefunctions (DZVP,
  TZV2P, QZV2P, MOLOPT, ccGRB); plane waves for the
  auxiliary density. GTH pseudopotentials, ONCV, and PAW
  via the GAPW back end.
- **DFT Notes chapters:** 03, 04, 05, 06 §6.7, 07, 08.
- **When to use.** The right pick for *ab-initio molecular
  dynamics of large systems*: water simulations (1,000+
  water molecules in a box), solid–liquid interfaces,
  organic–inorganic interfaces, battery electrolytes,
  MOFs with diffusing ions. The GPW/GAPW mixed basis is
  what makes this scale: the plane-wave auxiliary grid
  is much cheaper than a pure plane-wave code at the same
  accuracy for inhomogeneous systems. CP2K also ships
  *linear-scaling* DFT for systems beyond 10,000 atoms
  where diagonalisation becomes the bottleneck. If you
  are running solid-state DFT and do not need MD, Quantum
  ESPRESSO or VASP are better defaults.

### 2.6 WIEN2k

See section 3 (all-electron codes). WIEN2k is the most
widely-used **full-potential LAPW** code and is listed in
this table because of its prominence in solid-state DFT;
it is the entry that breaks the "plane-wave +
pseudopotential" mould.

---

## 3. All-electron codes (full potential)

Codes that make **no pseudopotential approximation** — the
core electrons are computed explicitly, on the same footing
as the valence. The price is computational cost: the core
wavefunctions are sharp and require a very high plane-wave
cutoff or an alternative basis (Muffin-tin orbitals in
LAPW). The reward is the correct treatment of magnetic
core states, hyperfine parameters, NMR contact shifts,
Mössbauer isomer shifts, spin–orbit coupling, and
$f$-electron localisation
([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.13–8.14).

| Code   | License           | Language  | Basis            | Best at                                   |
|:-------|:------------------|:----------|:-----------------|:------------------------------------------|
| WIEN2k | Commercial (ac.)  | Fortran   | APW + LAPW + lo  | Solids, $f$-electron systems, hyperfine   |
| Elk    | GPL               | Fortran   | FP-LAPW          | Open-source all-electron DFT, response    |
| FLEUR  | GPL (BSD-style)   | Fortran   | FP-LAPW + lo     | Open-source, magnetism, MAE, NRIXS        |

### 3.1 WIEN2k

- **License:** Commercial, free for academic use.
  **Language:** Fortran. **Repo:** <https://susi.theochem.tuwien.ac.at/>
- **DFT methods:** Full-potential LAPW + local orbitals
  (lo) in the WIEN2k / Madsen–Kunesch formulation. LDA,
  GGA, meta-GGA (SCAN, TB-mBJ), hybrid (PBE0, HSE06 via
  Yukawa screening), exact exchange, DFT+U,
  spin-polarised and non-collinear DFT, spin–orbit
  coupling as a *first-class* option, electric-field
  gradient, NMR chemical shifts and Knight shifts,
  Mössbauer isomer shifts, EELS, XANES, optical
  conductivity, $G_0W_0$ and BSE via the `wien2wannier`
  and `exciting` interfaces.
- **Basis sets:** APW + LAPW + lo in a **Muffin-tin +
  interstitial** decomposition. The MT spheres handle
  the strongly-bound core and valence states; the
  plane-wave expansion handles the smooth interstitial
  region. No pseudopotential.
- **DFT Notes chapters:** 04 §4.9 (relativistic KS,
  spin–orbit), 08 §8.13 (the all-electron analog).
- **When to use.** The right pick when the physics *forces*
  full-potential treatment: hyperfine parameters that
  depend on the core electron density at the nucleus,
  magnetic anisotropy energies of $f$-electron compounds,
  NMR shifts in heavy-element materials, Mössbauer isomer
  shifts. The user community is concentrated in the
  magnetism and actinide communities. The trade-off is
  pragmatics: the code is harder to use than VASP or
  Quantum ESPRESSO, the run-time is typically 10–100×
  longer than PAW for the same system, and the inputs
  (MT radii, basis-set choice, RKmax) require more care.
  If you can use PAW and get away with it, use PAW.

### 3.2 Elk

- **License:** GPL. **Language:** Fortran 2003.
  **Repo:** <https://elk.sourceforge.io/>
- **DFT methods:** Full-potential LAPW. LDA, GGA,
  meta-GGA (SCAN), hybrid (HSE06, PBE0, exact exchange),
  DFT+U, spin-polarised and non-collinear DFT, spin–orbit
  coupling as a first-class option, ground state and
  linear-response DFPT: phonons, dielectric response,
  Born effective charges, IR / Raman, electron-phonon
  coupling, $G_0W_0$, BSE.
- **Basis sets:** APW + LAPW + lo; same formal structure
  as WIEN2k.
- **DFT Notes chapters:** 04, 05, 08.
- **When to use.** The open-source alternative to WIEN2k.
  The implementation is faithful to the LAPW formalism
  and the documentation is thorough. Elk is *slower* than
  WIEN2k for serial runs but supports MPI parallelism and
  is on par in production. The right pick for
  open-source, all-electron, full-potential DFT, in
  particular for response properties at the DFT level.

### 3.3 FLEUR

- **License:** BSD-style (open source). **Language:**
  Fortran 2003. **Repo:** <https://www.flapw.de/maX-4/>
- **DFT methods:** Full-potential LAPW. LDA, GGA,
  meta-GGA, hybrid (PBE0, HSE06), exact exchange, DFT+U,
  spin-polarised and non-collinear DFT, spin–orbit
  coupling, magnetic anisotropy energy (MAE), NMR
  contact and dipolar hyperfine fields, resonant
  inelastic X-ray scattering (NRIXS) via the *Rixs*
  module, $G_0W_0$ via interface with `Spex` and `Yambo`.
- **Basis sets:** APW + LAPW + lo.
- **DFT Notes chapters:** 04, 05, 08.
- **When to use.** The right pick for *magnetism* and
  *spectroscopy* on open-source infrastructure. The MAE
  workflow is the most-used benchmark for the open-source
  LAPW community. The RIXS / NRIXS implementation is
  unique. The user interface is more challenging than
  VASP's, and the parallel scaling on large systems is
  good but not class-leading.

---

## 4. Real-space grid codes

Codes that discretise **all of real space** (not just the
atoms) on a finite-difference, finite-element, or
multigrid grid. The basis is *position-independent* (no
atom-centred functions), so the Pulay force vanishes
([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7.3)
and the representation is exact in the limit of an
infinitely-fine grid. Real-space grids are the natural
setting for **time-dependent** problems: the wavefunction
can be propagated in time with a leap-frog, Crank–
Nicolson, or exponential-midpoint scheme, and there is
no wrap-around artefact from periodic images of a
localised excitation.

| Code    | License | Language         | Best at                                                |
|:--------|:--------|:-----------------|:-------------------------------------------------------|
| Octopus | GPL     | Fortran + C      | TDDFT, atoms in strong fields, large clusters          |
| GPAW    | GPL     | Python + C       | PAW on a grid, ASE integration, ML hooks               |
| SIESTA  | GPL     | Fortran          | NAO basis, linear-scaling DFT, large systems           |

### 4.1 Octopus

- **License:** GPL. **Language:** Fortran 2003, C for I/O.
  **Repo:** <https://gitlab.com/octopus-code/octopus>
- **DFT methods:** Real-space grid KS-DFT (LDA, GGA,
  meta-GGA, hybrid, exact exchange), real-time TDDFT,
  Ehrenfest MD, Maxwell + TDDFT coupling for plasmonics
  and light-matter interaction, magnetic response,
  multiplet ligand-field theory, density-functional
  tight-binding. Finite systems in real space with
  absorbing boundaries; periodic systems via a multi-cell
  or supercell formulation.
- **Basis sets:** Real-space grid (uniform or adaptive
  mesh refinement), finite-element basis; optional
  plane-wave basis for compatibility.
- **DFT Notes chapters:** 04, 05, 06 §6.8, 07 (real-space
  PBC); the TDDFT chapter 10/11.
- **When to use.** The right pick for *time-dependent* DFT
  in real time: laser excitation of molecules, plasmonics,
  attosecond spectroscopy, atoms in strong laser fields,
  light–matter coupling beyond the dipole approximation.
  The user community is concentrated in the *atomic,
  molecular, and optical physics* (AMO) community. For
  ground-state solid-state DFT the plane-wave codes
  (VASP, Quantum ESPRESSO) are faster and more
  established. Octopus is the right default for "I need
  to propagate a wavefunction in time on a grid" — there
  is essentially no other production open-source code
  for this.

### 4.2 GPAW

- **License:** GPL. **Language:** Python (front end) +
  C / Cython (kernels); ASE ([section 9](#9-workflow-managers))
  is the standard geometry / calculator interface.
  **Repo:** <https://gitlab.com/gpaw/gpaw>
- **DFT methods:** PAW
  ([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7) on a
  real-space grid (default), a plane-wave mode (LAPW-
  equivalent accuracy with plane-wave diagonalisation),
  and an LCAO mode (atomic-orbital projection of the PAW
  solution, useful for linear-scaling DFT). LDA, GGA,
  meta-GGA, hybrid (HSE06, PBE0, exact exchange,
  range-separated), DFT+U, spin-polarised and
  non-collinear DFT, real-time TDDFT, linear-response
  TDDFT (Casida), GW and BSE via external interface,
  RPA, Delta-SCF, constrained DFT, transition-state
  search, NEB.
- **Basis sets:** PAW datasets (the GPAW / ASE PAW dataset
  library, with the `0.9.x` series being the production
  default). Real-space grid (multi-grid for the Poisson
  solver) or plane waves. LCAO projections in dzp / szp
  configurations for the LCAO mode.
- **DFT Notes chapters:** 04, 05, 06, 07, 08.
- **When to use.** The right pick for *PAW-quality*
  calculations with a *Python* interface and ASE
  integration. It is the most user-friendly of the PAW
  codes for new methods development: most algorithm
  changes require no Fortran. The LCAO mode makes GPAW
  usable for systems with thousands of atoms. The main
  weakness is raw speed: the same calculation in VASP
  or Quantum ESPRESSO typically runs 2–5× faster.

### 4.3 SIESTA

- **License:** GPL. **Language:** Fortran 2003.
  **Repo:** <https://gitlab.com/siesta-project/siesta>
- **DFT methods:** KS-DFT with **numerical atomic
  orbitals (NAOs)** as the basis
  ([chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.13).
  LDA, GGA, meta-GGA, hybrid (HSE06, PBE0),
  spin-polarised DFT, DFT+U, fully-relativistic
  spin–orbit, real-space grid for the Poisson solver,
  real-time TDDFT (newer developments), linear-scaling
  DFT (the "Order-N" mode) for systems with $O(10^4)$
  atoms and a finite band gap. Troullier–Martins
  pseudopotentials in the Kleinman–Bylander form.
- **Basis sets:** NAOs: radial numerical pseudo-atomic
  orbitals on a logarithmic radial grid, with
  multiple-ζ and polarisation variants. The user
  specifies a *single* energy shift that controls the
  cutoff radius $R_c$; the basis is automatically
  generated. The result is a *compact* basis: typical
  production calculations are tractable with $K \sim
  100$ functions per atom (vs. $K \sim 10{,}000$ for
  plane waves).
- **DFT Notes chapters:** 06 §6.13, 07, 08; the
  linear-scaling chapter 10/11.
- **When to use.** The right pick for *very large
  systems* (thousands of atoms) where the atom-centred
  basis is an advantage and a tightly converged energy
  is not the goal. Widely used for biomolecular systems,
  polymers, disordered solids, and battery electrode /
  electrolyte interfaces. The linear-scaling mode is one
  of the few production linear-scaling DFT codes; it
  pays off for insulators with a clean band gap. The
  trade-off is that the *energy* convergence is harder
  to control than in VASP.

---

## 5. Wavelet codes

Wavelet bases — **Daubechies wavelets**, in particular —
are the next step up from finite-difference real-space
grids: they combine the locality of the real-space grid
(so the Pulay force is zero) with the systematic
improvability of a basis-set expansion
([chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.14).
The convergence of the total energy with the wavelet
resolution is *exponential*, rather than the polynomial
convergence of finite-difference / finite-element methods.

### 5.1 BigDFT

- **License:** GPL. **Language:** Fortran 2003 (C kernels).
  **Repo:** <https://gitlab.com/l_sim/bigdft-suite>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  exact exchange) on a Daubechies-wavelet basis, in both
  finite systems and PBC. Wavelet-based multigrid
  Poisson solver, real-time TDDFT (`BigDFT-Turbo`),
  linear-response TDDFT, constrained DFT, high-lying /
  Rydberg states via a "C-IC" (continuum in crystal)
  embedding, fragmentation approach.
- **Basis sets:** Daubechies wavelets (the original
  BigDFT-1n) and the newer 2G (second-generation)
  formulation. Both are systematically improvable: the
  energy converges exponentially with the wavelet
  resolution parameter `hgrids`.
- **DFT Notes chapters:** 06 §6.14.
- **When to use.** The right pick when you want the
  *guarantees* of a systematically-improvable basis:
  clean convergence behaviour, no basis-set
  superposition error in the localised-basis sense, and
  a Poisson solver that is exact (within the basis) for
  the whole simulation cell. The community is centred in
  the French electronic-structure community (the GenCI
  consortium). For a production run on a moderate-size
  solid, VASP or Quantum ESPRESSO will be faster and
  have more turnkey workflows. For *systematic basis-set
  convergence studies* or *systematically-improvable
  reference calculations*, BigDFT is the unique
  open-source choice.

---

## 6. Coupled-cluster / high-accuracy wavefunction

Codes that implement wavefunction-based *post-HF* methods
to high accuracy: MP2, MP3, CCSD, CCSD(T), FCI, EOM-CC,
explicitly correlated (F12) methods, multireference
methods. The hierarchy is described in
[chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.3;
DFT is the *cheap* alternative, but for small molecules
where accuracy is paramount, CCSD(T) in a quadruple-zeta
basis is the gold standard
([chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.4).
The "all in Hartree" cost of CCSD(T) is $K^7$, so these
codes are aimed at small-to-medium molecules.

| Code  | License         | Language   | Best at                                         |
|:------|:----------------|:-----------|:------------------------------------------------|
| MRCC  | Free            | Fortran / C| High-accuracy CC, F12, arbitrary-order CC       |
| CFOUR | GPL             | Fortran / C| Open-source CC, EOM-CC, MR-CC                   |

### 6.1 MRCC

- **License:** Free (closed-source but redistributable;
  no cost for any user). **Language:** Fortran / C.
  **Repo:** <https://www.mrcc.hu/>
- **Methods:** MP2, MP3, MP4, CCSD, CCSDT, CCSDTQ,
  CCSD(T), CCSDT(Q), CC(n) (closed-shell CCSD up to
  CCSDTQPHH), perturbative triples (T) and beyond,
  explicitly-correlated CC (F12), density-fitted
  integrals, arbitrary-order CC up to CCSDTQPHH, MR-CC
  methods (Mk-MRCCSD, BW-MRCCSD). The author is Mihály
  Kállay.
- **Basis sets:** GTOs. Pople, Dunning, Karlsruhe, custom.
  Density-fitting auxiliary bases.
- **DFT Notes chapters:** 02, 03.
- **When to use.** The right pick for *single-point
  coupled-cluster reference* calculations on small
  molecules. Its principal strength is the *arbitrary-
  order* CC capability: there is no other production
  code that routinely reaches CCSDTQPHH, and the F12
  implementation is one of the most accurate in the
  field. The trade-off is that MRCC is a single-point-
  energy code: geometry optimisations, finite
  differences, and properties are typically computed by
  calling MRCC from an external driver (CFOUR, Psi4, or
  a user script).

### 6.2 CFOUR

- **License:** GPL. **Language:** Fortran / C.
  **Repo:** <https://github.com/CFOUR/cfour>
- **Methods:** HF, MP2, MP3, MP4, CCSD, CCSD(T), CCSDT,
  CC(n), EOM-CCSD (ionised, attached, excited), MR-CC
  (Mk-MRCCSD, BW-MRCCSD), explicit correlation (F12),
  analytic first- and second-derivatives (gradients,
  Hessians) for HF, MP2, CCSD, CCSD(T), EOM-CCSD;
  geometry optimisation, harmonic frequencies, anharmonic
  vibrational spectroscopy, vibrational configuration
  interaction (VCI), equation-of-motion coupled cluster
  for excited states.
- **Basis sets:** GTOs. Pople, Dunning, Karlsruhe, ANO.
  Spherical-harmonic and Cartesian conventions.
- **DFT Notes chapters:** 02, 03.
- **When to use.** The right pick for *high-accuracy
  wavefunction* methods where the open-source path is
  mandatory. The analytic second-derivatives for CCSD(T)
  are state-of-the-art and enable *anharmonic*
  vibrational spectroscopy at the CCSD(T) level. The
  EOM-CCSD suite is mature. CFOUR is slower than MRCC
  for single-point energies above CCSD(T), but is the
  better pick for geometry optimisation, vibrational
  spectroscopy, and any workflow that needs gradients.
  The PySCF and Psi4 interfaces to CFOUR give a modern
  Python front end.

---

## 7. Codes for special systems

Codes that occupy a niche. Either they implement a basis
that is unique (CRYSTAL with Gaussians for solids, FHI-aims
with NAOs of tier-4 quality, exciting with FP-LAPW for
excited states), or they are layered on top of a more
general code as a *post-processor* (WEST, Yambo for
$G_0W_0$ and BSE).

| Code       | License          | Language   | Best at                                          |
|:-----------|:-----------------|:-----------|:-------------------------------------------------|
| CRYSTAL    | Free (ac.)       | Fortran    | Gaussian basis for crystals, phonons             |
| FHI-aims   | Academic (ac.)   | Fortran    | All-electron NAO, numerical basis, hybrid DFT    |
| exciting   | GPL              | Fortran    | FP-LAPW excited states, BSE, $GW$                |
| WEST       | GPL              | Fortran    | $G_0W_0$ + BSE on top of PW / PAW codes          |
| Yambo      | GPL              | Fortran    | $G_0W_0$ + BSE on top of PW / PAW codes          |

### 7.1 CRYSTAL

- **License:** Free for academic use; commercial for
  industry. **Language:** Fortran.
  **Repo:** <https://www.crystal.unito.it/>
- **DFT methods:** KS-DFT (LDA, GGA, hybrid B3LYP, PBE0,
  range-separated), spin-polarised DFT, HF, MP2, CC, CI.
  Periodic systems in 1-D, 2-D, 3-D, with full space
  group symmetry. Phonon dispersion, elastic constants,
  piezo-electric tensors, NMR chemical shifts, EELS, XAS.
- **Basis sets:** Gaussian basis for solids (the unique
  selling point). Pople, Dunning, Karlsruhe families;
  also CRYSTAL's own polarised-valence sets. "Ghost-atom"
  approach supports basis-set superposition error (BSSE)
  studies.
- **DFT Notes chapters:** 04, 05, 06, 07.
- **When to use.** The right pick when you need a
  **Gaussian basis for a crystalline solid**: reduced
  BSSE, well-defined extrapolation to the complete basis
  set, easier comparison to molecular calculations using
  the same basis family. The MP2 and CC implementations
  for periodic systems are unique. The trade-off is that
  the plane-wave + PAW codes are faster, more
  user-friendly, and have larger community for "standard"
  solid-state DFT; CRYSTAL is the specialist choice.

### 7.2 FHI-aims

- **License:** Free for academic use; per-group licence
  for industry (source-available; not OSI open source).
  **Language:** Fortran. **Repo:** <https://fhi-aims.org/>
- **DFT methods:** KS-DFT with **all-electron numerical
  atom-centred orbital (NAO)** basis at "tier" levels
  (tier 1, 2, 3, 4 — the higher the tier, the more
  functions). LDA, GGA, meta-GGA, hybrid, range-separated,
  exact exchange, DFT+U, spin-polarised and non-collinear
  DFT, real-time TDDFT, linear-response TDDFT, RPA, GW
  and BSE via interface, RPA correlation, $G_0W_0$,
  dispersion-corrected DFT, ZORA scalar-relativistic and
  full-relativistic, geometry optimisation, MD, NEB,
  phonons. Tier-4 bases are essentially all-electron
  reference-quality.
- **Basis sets:** NAO on a logarithmic radial grid; the
  user selects a "tier" (a basis-set level); the basis
  is pre-tabulated for the entire periodic table.
- **DFT Notes chapters:** 04, 05, 06 §6.13, 08.
- **When to use.** The right pick when you need
  *all-electron* accuracy on a *molecular* (or cluster)
  system without the cost of a full LAPW treatment. The
  tier-4 basis is the most accurate practical all-electron
  basis in the molecular regime; the GW and RPA
  implementations are the gold standard for molecular
  $G_0W_0$ benchmarks. The community is centred in the
  FHI Berlin and surrounding groups. The trade-off is
  the licence and the smaller user community relative
  to ORCA / Psi4.

### 7.3 exciting

- **License:** GPL. **Language:** Fortran.
  **Repo:** <https://exciting-code.org/>
- **DFT methods:** Full-potential LAPW (LDA, GGA,
  meta-GGA, hybrid, DFT+U, spin–orbit), *linear-response
  TDDFT* in the Bethe–Salpeter equation (BSE) formulation,
  $G_0W_0$, phonon dispersion, electron-phonon coupling,
  optical absorption, XAS, EELS, magneto-optical Kerr
  effect.
- **Basis sets:** APW + LAPW + lo; same as Elk / WIEN2k.
- **DFT Notes chapters:** 04, 05, 07, 08; the
  excited-state chapter 10/11.
- **When to use.** The right pick for *excited-state
  solids* with full-potential LAPW accuracy. The BSE
  implementation is among the best in the open-source
  LAPW community. The user community is smaller than
  Elk's or WIEN2k's, but the spectroscopic workflows
  (optical, XAS, EELS) are well-developed.

### 7.4 WEST

- **License:** GPL. **Language:** Fortran.
  **Repo:** <https://west-code.org/>
- **DFT methods:** Many-body perturbation theory on top
  of KS-DFT ground state: $G_0W_0$, $GW$ (partially
  self-consistent $evGW$, $qsGW$), BSE. Reads the
  converged ground state from Quantum ESPRESSO, CP2K,
  or SIESTA. Large-scale parallelism (MPI + OpenMP +
  GPU). Stochastic approaches for ultra-large systems.
- **Basis sets:** Inherits from the host code. Plane
  waves (Quantum ESPRESSO, CP2K GPW), NAOs (SIESTA).
- **DFT Notes chapters:** 04 (response formalism), 05,
  07, 10/11 (response properties).
- **When to use.** The right pick for $G_0W_0$ and BSE
  on systems too large for VASP GW to handle. The
  stochastic $GW$ implementation makes the method scale
  to thousands of atoms; the deterministic $G_0W_0$ is
  the most-used open-source production $GW$ in the
  plane-wave community after Yambo. The downside is
  WEST's tighter coupling to Quantum ESPRESSO and a
  smaller user community than Yambo.

### 7.5 Yambo

- **License:** GPL. **Language:** Fortran 2003.
  **Repo:** <https://www.yambo-code.org/>
- **DFT methods:** Many-body perturbation theory:
  $G_0W_0$, $GW_0$, $evGW$, BSE, time-dependent BSE,
  dielectric response, EELS, $GW$ in the "full-frequency"
  and plasmon-pole approximations, parallel over bands,
  k-points, and frequency.
- **Basis sets:** Reads ground-state data from Quantum
  ESPRESSO, VASP, ABINIT, SIESTA, and others. Uses the
  host code's basis (plane waves, PAW, etc.) for the KS
  orbitals, then constructs the $GW$ self-energy and
  BSE kernel in the host basis.
- **DFT Notes chapters:** 04 (response), 05, 07, 10/11
  (response and excited states).
- **When to use.** The right pick for $G_0W_0$ and BSE
  on top of an existing KS-DFT calculation. It is *the*
  de facto open-source code for these methods, with a
  large user community and well-developed documentation.
  The Yambo + Quantum ESPRESSO pipeline is the standard
  open-source route to a many-body corrected band gap,
  dielectric function, optical spectrum, or XAS. For
  very large systems, WEST is the better pick; for
  molecular $G_0W_0$ benchmarks, FHI-aims is the
  better pick.

---

## 8. Visualisation

Codes for rendering the **outputs** of electronic-
structure calculations. None of these are themselves
electronic-structure codes; they read the outputs of the
production codes and turn them into pictures. The DFT
chapters that *produce* the data are 04 (charge densities,
Kohn–Sham orbitals), 05 (spin densities), 06 (basis-set
isosurfaces), 07 (band structures, Fermi surfaces), 08
(PAW augmentation densities), and 10/11 (response
properties, optical absorption).

| Code      | License    | Language     | Best at                                    |
|:----------|:-----------|:-------------|:-------------------------------------------|
| VESTA     | Freeware   | C            | Crystal structures, isosurfaces, charge     |
| OVITO     | Commercial | C++ / Python | Molecular-dynamics visualisation            |
| ParaView  | BSD        | C++ / Python | General 3-D scientific visualisation        |
| XCrySDen  | GPL        | C / Tcl/Tk   | Band structures, Fermi surfaces             |

### 8.1 VESTA

- **License:** Freeware (no cost, source-closed).
  **Language:** C. **Repo:** <https://jp-minerals.org/vesta/en/>
- **Reads:** CIF, VASP POSCAR / CHGCAR / WAVECAR / LOCPOT,
  Gaussian cube, XCrySDen structure (XSF), PDB, Quantum
  ESPRESSO input / output, ABINIT input / output, SIESTA.
- **When to use.** The right default for *crystal-structure
  and isosurface* visualisation: lattice, atoms, bonds,
  charge density isosurfaces, spin-density isosurfaces,
  ELF, structure comparison, polyhedral rendering. The
  bond-rendering and polyhedral drawing are the most
  developed in any open-source or freeware tool.
  Limitations: no animation, no MD visualisation, no
  large-scale 3-D scene handling.

### 8.2 OVITO

- **License:** Commercial; academic licence free of
  charge; open-source Python API. **Language:** C++ /
  Python. **Repo:** <https://www.ovito.org/>
- **Reads:** LAMMPS dump, XDATCAR (VASP), GROMACS, CIF,
  POSCAR, custom formats.
- **When to use.** The right default for *molecular-
  dynamics visualisation*: trajectories, defects,
  dislocation analysis, CNA / DXA / Wigner–Seitz analysis,
  bond-orientational order parameters. The Python
  scripting layer is the most powerful of any
  visualisation tool.

### 8.3 ParaView

- **License:** BSD. **Language:** C++ / Python.
  **Repo:** <https://www.paraview.org/>
- **Reads:** VTK, NetCDF, Exodus II, raw arrays, custom
  readers; VASP data via *ParaView Catalyst* and *PVGeo*
  plug-ins.
- **When to use.** The right pick for *general 3-D
  scientific visualisation at scale*: finite-element
  meshes, fluid flow, large spatiotemporal fields. The
  "client–server" model distributes rendering to a remote
  cluster. For DFT-specific visualisation (crystal
  structures, isosurfaces, band structures), VESTA and
  XCrySDen are more direct.

### 8.4 XCrySDen

- **License:** GPL. **Language:** C / Tcl/Tk.
  **Repo:** <http://www.xcrysden.org/>
- **Reads:** XSF, SIESTA output, Quantum ESPRESSO
  output, VASP, FHI-aims.
- **When to use.** The right pick for *band-structure
  and Fermi-surface* visualisation in the solid-state
  community. The Brillouin-zone rendering and the k-path
  generator are the most-used in the plane-wave DFT
  community. The "Fermi surface" mode (with a 3-D
  Brillouin-zone integration) is the unique feature.

---

## 9. Workflow managers

Codes for *organising* electronic-structure calculations.
A workflow manager accepts a high-level specification
("compute the band structure of MoS₂, then the phonons,
then the GW correction") and turns it into a sequence of
job submissions, with dependency tracking, error
recovery, and provenance. Workflow managers are not
electronic-structure codes; they sit *on top of* the
production codes from sections 1–7.

| Code      | License  | Language   | Best at                                          |
|:----------|:---------|:-----------|:-------------------------------------------------|
| ASE       | LGPL     | Python     | Lightweight scripting, structure handling, IO    |
| AiiDA     | MIT      | Python     | Workflow + provenance, sharing, materials cloud  |
| Fireworks | BSD      | Python     | Lightweight workflow + database                  |
| atomate   | MIT      | Python     | Pre-built workflows (MP-style) for VASP, Q-Chem  |

### 9.1 ASE (Atomic Simulation Environment)

- **License:** LGPL. **Language:** Python.
  **Repo:** <https://gitlab.com/ase/ase>
- **Capabilities:** Atom / geometry handling, file I/O
  for the major codes (VASP, Quantum ESPRESSO, CASTEP,
  ABINIT, GPAW, SIESTA, ORCA, FHI-aims, ...), high-level
  "calculator" interface that lets the user swap codes by
  changing one line, structure optimisation, NEB,
  molecular dynamics, phonons, equation of state,
  defects and surfaces module, band structure helper,
  materials project compatibility.
- **DFT Notes chapters:** all of them — ASE is the
  recommended Python interface for nearly every
  production code mentioned above.
- **When to use.** The right default for *Python-driven*
  electronic-structure scripting. The calculator
  interface is the most useful pattern: a `Vasp`,
  `GPAW`, `Espresso`, or `ORCA` calculator exposes the
  same `.get_potential_energy()` API. ASE does *not*
  manage job submission to a cluster (use Fireworks or
  AiiDA for that) and does *not* track provenance (use
  AiiDA for that). For a *campaign* (a thousand
  calculations) the workflow managers below are better.

### 9.2 AiiDA

- **License:** MIT. **Language:** Python.
  **Repo:** <https://github.com/aiidateam/aiida-core>
- **Capabilities:** Workflow management with **provenance
  tracking**: every calculation is stored in a database
  with its full input, output, and dependencies.
  Workflows are written in Python, with built-in
  primitives for common patterns (relax, band structure,
  phonons). The Materials Cloud
  (<https://www.materialscloud.org/>) is built on AiiDA.
  Pluggable schedulers (SLURM, PBS, SGE, LSF, etc.) and
  pluggable codes (Quantum ESPRESSO, VASP, CP2K, CASTEP,
  SIESTA, Fleur, NWChem).
- **DFT Notes chapters:** all of them, but especially
  the chapter 12 (high-throughput / database — planned)
  workflow.
- **When to use.** The right default for a *research
  group that runs thousands of DFT calculations* and
  needs to *reproduce* them. The provenance graph is
  the unique feature: every result is automatically
  linked to the input geometry, code version,
  pseudopotential library, and workflow definition. The
  trade-off is the on-ramp: AiiDA has its own daemon,
  its own database (PostgreSQL), and its own workflow
  language. For a single calculation the overhead is
  too much. For a campaign, the reproducibility gain
  is worth it.

### 9.3 Fireworks

- **License:** BSD. **Language:** Python.
  **Repo:** <https://github.com/materialsproject/fireworks>
- **Capabilities:** Lightweight workflow management with
  MongoDB-backed job tracking. Each calculation is a
  *firework*, workflows are *fireworks + links*. The
  central `lpad` command-line interface manages the
  queue. Pluggable queue interfaces (SLURM, PBS, SGE,
  LSF). Provenance tracking through the *launchpad* —
  not as deep as AiiDA's, but lighter.
- **DFT Notes chapters:** all of them.
- **When to use.** The right default for *a research
  group that needs a queue manager and workflow*
  without the full AiiDA overhead. The *atomate* package
  (below) is built on top of Fireworks. Use Fireworks if
  you want the queue management and dependency tracking
  but do not need the formal provenance graph; use
  AiiDA if you do.

### 9.4 atomate

- **License:** MIT. **Language:** Python (built on top
  of Fireworks, pymatgen, and custodian).
  **Repo:** <https://github.com/materialsproject/atomate>
- **Capabilities:** Pre-built workflows for the
  Materials Project style: structural optimisation,
  static calculation, band structure, density of states,
  elastic tensor, dielectric constant, piezoelectric
  tensor, phonon dispersion, NEB, GW / BSE, defect
  formation energies. Plug-in calculators for VASP
  (the main target) and Q-Chem. Automatic error
  handling via `custodian` (the calculation re-runs
  with adjusted parameters if a job fails).
- **DFT Notes chapters:** all of them.
- **When to use.** The right default for *"I want a
  standard Materials-Project-style workflow, and I do
  not want to write it myself"*. The pre-built
  workflows cover the 80% case; the remaining 20% is
  built by chaining them or by writing a new `Firework`.
  The error-correction infrastructure (`custodian`) is
  the unique feature: a calculation that converges to
  the wrong magnetic state, or fails the convergence
  test, is automatically restarted with adjusted
  parameters. The cost is the deep coupling to VASP;
  for non-VASP workflows, AiiDA's pluggability is
  more flexible.

---

> Back to the [chapter index]({{ "/dft-notes/" | relative_url }}) or
> jump to [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }})
> for the theory of basis sets that makes the
> "Gaussian vs. plane wave vs. real space" split sensible.
