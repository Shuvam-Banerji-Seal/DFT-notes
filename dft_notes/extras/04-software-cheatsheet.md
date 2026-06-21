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
> useful pointers: chapter numbers tell you *whic`h*'
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
  organometalli`c*' quantum chemistry. **DLPNO-CCSD(T)**
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
  6-311G family, cc-pV*X*Z, aug-cc-pVXZ, LanL2DZ, SDD,
  ANO.
- **DFT Notes chapters:** 03, 04, 05, 06.
- **When to use.** The right pick for *publication-
  benchmar`k*' organic-chemistry calculations where maximum
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

- **License:** GPL. **Language:** Fortran 2003. **Repo:** <https://gitlab.com/QEF/q-e>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid
  HSE06, PBE0, exact exchange), spin-polarised and
  non-collinear DFT, DFT+U(+V), Wannier-function methods
  (Wannier90), TDDFT in the real-time (`turboTDDFT`) and
  linear-response (`turboEELS`) flavours, $G_0W_0$ and $GW$
  via 'Yambo' and 'West`, phonon dispersion and
  electron-phonon coupling (`EPW`), NMR chemical shifts
  (`QE-Knopp`), Hubbard parameters (`HP`),
  Born–Oppenheimer and Car–Parrinello MD.
- **Basis sets:** Plane waves (kinetic cutoff
  $E_\text{cut}$), with norm-conserving (Troullier–Martins,
  ONCV), ultrasoft, or PAW datasets from the `pseudodojo`'
  library.
- **DFT Notes chapters:** 04, 05, 06 §6.7, 07, 08.
- **When to use.** The de facto open-source plane-wave DFT
  code. The right pick for any *academi`c*' solid-state DFT
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
  corrections, GW and BSE via the `vasp_gw`' module, MD,
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
- **When to use.** A strong pick for *UK academi`c*'
  solid-state work where the licence is free; outside the
  UK, Quantum ESPRESSO is the standard open-source
  alternative. The NMR chemical-shift and EELS modules
  are particularly well-developed. The phonon and
  electron-phonon coupling suite is mature. The user
  community is smaller than VASP / Quantum ESPRESSO's.

### 2.4 ABINIT

- **License:** GPL. **Language:** Fortran 2003. **Repo:** <https://github.com/abinit/abinit>
- **DFT methods:** KS-DFT (LDA, GGA, meta-GGA, hybrid,
  exact exchange), spin-polarised DFT, DFT+U,
  linear-response DFPT for phonons, dielectric response,
  Born effective charges, IR / Raman, $G_0W_0$ (the
  'Optics' and 'SIGMA' modules are the workhorse $GW$
  code for the open-source community), BSE, TDDFT in the
  Casida and Sternheimer flavours, electron stopping
  power, electron–phonon coupling, finite electric
  fields, orbital-free DFT, PAW (Blöchl's original 1994
  algorithm); one of the most mature *response-property*
  suites in the field.
- **Basis sets:** Plane waves. Norm-conserving
  pseudopotentials (Troullier–Martins, ONCV), PAW
  datasets from the ABINIT `JTH`' table.
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
  conductivity, $G_0W_0$ and BSE via the `wien2wannier`'
  and `exciting`' interfaces.
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

- **License:** GPL. **Language:** Fortran 2003. **Repo:** <https://elk.sourceforge.io/>
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
  module, $G_0W_0$ via interface with 'Spex' and 'Yambo`.
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
  library, with the `0.9.x' series being the production
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

- **License:** GPL. **Language:** Fortran 2003. **Repo:** <https://gitlab.com/siesta-project/siesta>
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
DFT is the *chea`p*' alternative, but for small molecules
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
  are state-of-the-art and enable *anharmoni`c*'
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
  *all-electron* accuracy on a molecular (or cluster)
  system without the cost of a full LAPW treatment. The
  tier-4 basis is the most accurate practical all-electron
  basis in the molecular regime; the GW and RPA
  implementations are the gold standard for molecular
  $G_0W_0$ benchmarks. The community is centred in the
  FHI Berlin and surrounding groups. The trade-off is
  the licence and the smaller user community relative
  to ORCA / Psi4. ### 7.3 exciting

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

- **License:** GPL. **Language:** Fortran 2003. **Repo:** <https://www.yambo-code.org/>
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
  readers; VASP data via *ParaView Catalyst* and PVGeo
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
electronic-structure codes; they sit *on top o`f*' the
production codes from sections 1–7. | Code      | License  | Language   | Best at                                          |
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
  `GPAW`, `Espresso`, or `ORCA`' calculator exposes the
  same `.get_potential_energy()' API. ASE does *not*
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
  *firework*', workflows are fireworks + links. The
  central `lpad`' command-line interface manages the
  queue. Pluggable queue interfaces (SLURM, PBS, SGE,
  LSF). Provenance tracking through the *launchpa`d*' —
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
  handling via `custodian`' (the calculation re-runs
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

---

## 10. Code cheatsheets (input files)

> Companion to the use-case profiles in §§1–9. The
> profiles tell you *which code to reach for*; the
> cheatsheets below tell you *what to type into it*.
> Every entry shows a **minimal** input that produces a
> sensible result on a trivial system (a hydrogen
> molecule or a primitive cell), an **annotated** version
> of the same input for a slightly harder calculation (a
> band structure, a spin-polarised system, an MD step), a
> short list of *what to tweak for X*, a list of common
> pitfalls*, and a cross-reference to the chapter where
> the underlying theory is derived.

The cheatsheet is *not* a replacement for the manual of
any of these codes. It is the *first thing to look at*
when starting a new project, before reading the manual.
The "what to tweak" lists are the answers to the
questions you will ask on the third day of the project;
the "common pitfalls" lists are the answers to the
questions you will ask on the third week.

### Table of contents

1. [Quantum ESPRESSO](#101-quantum-espresso) — Si band structure
2. [VASP](#102-vasp) — Si band structure with HSE06
3. [GPAW](#103-gpaw) — Si band structure in Python
4. [SIESTA](#104-siesta) — Si band structure
5. [CP2K](#105-cp2k) — water in a box and NVT MD
6. [FLEUR](#106-fleur) — Fe bcc, spin-polarised, with SOC

### 10.1 Quantum ESPRESSO

Quantum ESPRESSO is a Fortran 2003 plane-wave DFT code
([§2.1](#21-quantum-espresso)). The cheatsheet below
covers the standard 'pw.x' (ground-state) and 'bands.x'
(post-processing) executables. The input format is
**name-list Fortran** — every section starts with
'&NAME' and ends with '/`.

#### 10.1.1 Minimal input — H₂ SCF

The smallest input that produces a sensible
single-point energy on a hydrogen molecule:

```fortran
&CONTROL
    calculation = 'scf'         ! 'scf' | 'relax' | 'vc-relax' | 'bands' | 'nscf'
    prefix      = 'h2'          ! base name for output files
    outdir      = './tmp/'      ! scratch directory (must exist)
    pseudo_dir  = './pseudo/'   ! directory containing *.UPF pseudopotentials
    verbosity   = 'low'         ! 'low' | 'high'
/
&SYSTEM
    ibrav = 0                    ! 0 = free-format lattice (ATOMIC_POSITIONS below)
    nat   = 2
    ntyp  = 1
    ecutwfc = 30.0               ! plane-wave cutoff for wavefunctions, Ry
    ecutrho = 240.0              ! charge-density cutoff, Ry
                                 !   >= 4*ecutwfc for NC-PP
                                 !   >= 8-12 * ecutwfc for USPP / PAW
/
&ELECTRONS
    conv_thr = 1.0d-8            ! SCF convergence threshold, Ry
/
ATOMIC_SPECIES
  H  1.008  H.upf                ! element, atomic mass, pseudopotential file
ATOMIC_POSITIONS angstrom
  H  0.0  0.0  0.0
  H  0.0  0.0  0.74              ! bond length 0.74 Å
K_POINTS gamma                    ! Gamma-only: 1 k-point
```

To run: 'pw.x < h2.scf.in > h2.scf.out'. The total
energy (in Rydberg) is in `h2.scf.out' after
'!    total energy'.

#### 10.1.2 Annotated example — Si band structure

A band structure of bulk silicon along the standard
Γ–X–W–K–Γ–L path. Three calculations: (i) self-consistent
ground state on a uniform Monkhorst–Pack mesh; (ii)
non-self-consistent calculation along the k-path using
the converged charge density; (iii) post-processing
with `bands.x' to extract the band energies.

**Step 1 — SCF** (`si.scf.in`):

```fortran
&CONTROL
    calculation = 'scf'
    prefix      = 'si'
    outdir      = './tmp/'
    pseudo_dir  = './pseudo/'
/
&SYSTEM
    ibrav     = 0
    nat       = 2
    ntyp      = 1
    ecutwfc   = 40.0            ! converged at 40 Ry for Si.pbe-n-rrkjus_psl.0.1.UPF
    ecutrho   = 320.0           ! 8x ecutwfc for ultrasoft / PAW
    occupations = 'fixed'       ! semiconductor: fixed occupations
/
&ELECTRONS
    conv_thr = 1.0d-10          ! tighter than the H2 default
/
ATOMIC_SPECIES
  Si  28.086  Si.pbe-n-rrkjus_psl.0.1.UPF
ATOMIC_POSITIONS crystal
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25         ! diamond structure, fractional
CELL_PARAMETERS angstrom
    0.00   2.715  2.715
    2.715  0.00   2.715
    2.715  2.715  0.00
K_POINTS automatic              ! Monkhorst-Pack mesh
  8 8 8  0 0 0
```

**Step 2 — bands** (`si.bands.in`): same as
'si.scf.in' but with 'calculation = 'bands'`, an
added `nbnd`, and the k-path:

```fortran
&CONTROL
    calculation = 'bands'          ! only this line differs from scf
    ...
/
&SYSTEM
    ...
    nbnd      = 12              ! >= number of electrons / 2
    occupations = 'fixed'
/
&ELECTRONS
    conv_thr = 1.0d-10
/
ATOMIC_SPECIES
  Si  28.086  Si.pbe-n-rrkjus_psl.0.1.UPF
ATOMIC_POSITIONS crystal
  Si  0.00  0.00  0.00
  Si  0.25  0.25  0.25
CELL_PARAMETERS angstrom
    0.00   2.715  2.715
    2.715  0.00   2.715
    2.715  2.715  0.00
K_POINTS tpiba_b               ! high-symmetry path; cartesian, 2*pi/bohr
  6
  0.0   0.0   0.0    30         ! Gamma
  0.5   0.0   0.5    30         ! X
  0.5   0.25  0.75   30         ! W
  0.375 0.375 0.375  30         ! K
  0.0   0.0   0.0    30         ! Gamma
  0.5   0.5   0.5    30         ! L
```

The '6' is the number of segments, the '30' is the
number of k-points per segment. Run:
'pw.x < si.scf.in > si.scf.out && pw.x < si.bands.in > si.bands.out'.

**Step 3 — post-processing** (`si.bands.post.in`):
extract band energies:

```fortran
&BANDS
    prefix   = 'si'
    outdir   = './tmp/'
    filband  = 'si.bands.dat'   ! output: k-index, E_1, E_2, ..., E_nbands
    lsym     = .true.           ! enforce the symmetries of the path
/
```

Run: 'bands.x < si.bands.post.in > si.bands.post.out'.
The file `si.bands.dat' has one row per k-point and one
column per band.

#### 10.1.3 What to tweak for X

- **To converge the total energy to 1 meV/atom**:
  sweep `ecutwfc`' from 20 to 80 Ry, recompute, and
  pick the smallest value at which the energy
  changes by less than 1 meV/atom. With PAW
  pseudopotentials from the `pslibrary`, typical
  converged values are 40–80 Ry.
- **To converge the band gap to 0.1 eV**: increase
  `ecutwfc`' (conduction bands converge more
  slowly), tighten 'conv_thr' to '1.0d-10`, and
  verify the k-point sampling. For an accurate gap
  with semilocal functionals, switch to a hybrid
  ('input_dft = 'HSE'',
  [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.5) or
  to $G_0W_0$ via 'Yambo' / 'West`.
- **To converge k-point sampling**: sweep the MP
  mesh from $4 \times 4 \times 4$ to
  $16 \times 16 \times 16$ on a primitive cell, and
  pick the smallest at which the energy changes by
  less than 1 meV/atom.
- **To converge k-point sampling**: sweep the MP mesh
  from $4 \times 4 \times 4$ to
  $16 \times 16 \times 16$ on a primitive cell, and
  pick the smallest mesh at which the total energy
  changes by less than 1 meV/atom.
- **For metals**: set 'occupations = 'smearing'',
  use `smearing = 'mp'' (Methfessel–Paxton, 2nd
  order) with `degauss = 0.02' Ry, and increase the
  k-mesh substantially. Never use `'gaussian'' for
  production — it converges too slowly with mesh
  density. For very high accuracy, use `'fd''
  (Fermi–Dirac) and extrapolate.
- **For spin-polarised systems**: add `nspin = 2'
  to '&SYSTEM' and set 'starting_magnetization(i)'
  for each species. For non-collinear, use
  'noncolin = .true.'.
- **For geometry optimisation**: use
  `calculation = 'relax'' (ions only) or
  `'vc-relax'' (ions and cell). Set
  'ion_dynamics = 'bfgs'' or ''damp'' (Wentzcovich
- **For geometry optimisation**: use
  `calculation = 'relax'' (ions only) or
  `'vc-relax'' (ions and cell). Set
  'ion_dynamics = 'bfgs'' or ''damp'' (Wentzcovich
  damping) for stability on tricky systems.

#### 10.1.4 Common pitfalls

- **Mismatched ecutrho**: must be $\geq 4 \times$
  `ecutwfc`' for norm-conserving and $\geq 8 \times$
  (often $12 \times$) for US/PAW. The error is
  silent — the SCF converges to a "wrong" total
  energy that is *not* variational.
- **Wrong pseudopotential file**: `pseudo_dir`' is
  relative to the working directory. Mismatched
  valence configurations (e.g. $3s^23p^2$ for Si
  when $3s^23p^63d^0$ is needed for excited
  states) silently produce wrong energies.
- **occupations = 'tetrahedron' on a coarse mesh**:
  the tetrahedron integrator needs at least
  $4 \times 4 \times 4$ on a primitive cell. With a
  coarser mesh, use `'fixed'' (semiconductor) or
  `'smearing'' (metal).
- **Forgetting prefix consistency between SCF and
  bands**: the bands run reads the charge from
  `outdir/prefix.save/`. If `prefix`' differs, the
  run fails with "file not found" or, worse, reads
  a different prefix's charge and gives a wrong
  answer without erroring.
- **PAW / USPP family mixing**: the
  pseudopotentials must be from the *same* family
  across elements (e.g. PBE ultrasoft with PBE
  ultrasoft, not with LDA norm-conserving).
  Mixing families gives a non-variational answer.

#### 10.1.5 Cross-references

- Theory: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7
  (plane waves), [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }})
  §7.3 (Bloch), §7.6 (k-points), §7.11 (tetrahedron).
- Pseudopotentials: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }})
  §8.3 (norm-conserving), §8.6 (ultrasoft), §8.7 (PAW).
- Hybrid functionals: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.5.
- Phonons (`ph.x' DFPT): [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}).
- Yambo + QE pipeline for $G_0W_0$ / BSE: [§7.5](#75-yambo).

---

### 10.2 VASP

VASP is the Fortran PAW plane-wave code
([§2.2](#22-vasp)). The cheatsheet below covers the
four input files — `INCAR`, `KPOINTS`, `POSCAR`,
`POTCAR`. The "POSCAR" is the structure, the
"INCAR" the run-time parameters, the "KPOINTS" the
k-point sampling, and the "POTCAR" the PAW
pseudopotential concatenation (one entry per
species, in POSCAR order).

#### 10.2.1 Minimal input — Si SCF

The smallest input that produces a sensible
single-point energy on bulk silicon:

```bash
# INCAR
ENCUT  = 250       # plane-wave cutoff, eV (typically 1.3 x max ENMAX in POTCAR)
EDIFF  = 1.0e-5    # SCF convergence, eV
ISMEAR = 0         # 0 = Gaussian (semiconductors and insulators)
SIGMA  = 0.05      # smearing width, eV
IBRION = -1        # -1 = no ionic update (static calculation)
```

```bash
# KPOINTS
Automatic mesh
0              # 0 = auto: Monkhorst-Pack with explicit offsets
Gamma          # Gamma-centred (use Monkhorst for non-Gamma-centred)
8  8  8        # mesh
0. 0. 0. # shift
```

```
# POSCAR
Si
 5.43           # cubic lattice constant, A
  1.0  0.0  0.0
  0.0  1.0  0.0
  0.0  0.0  1.0
Si
 2              # number of atoms
Cartesian
 0.00  0.00  0.00
 1.3575 1.3575 1.3575   # 1/4 of the cube diagonal
```

```bash
# POTCAR -- built by concatenating per-element POTCAR files from
# the VASP PAW library, in the order the species appear in POSCAR:
$ cat $VASP_PP_PATH/potcar/Si/PBE/Si/POTCAR > POTCAR
```

To run: 'mpirun -n 8 vasp_std'. The total energy (in eV)
is on the last "free  energy" line of `OUTCAR`.

#### 10.2.2 Annotated example — Si band structure with HSE06

A band structure of bulk silicon using the HSE06
range-separated hybrid
([chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.5).
Three steps: (i) standard SCF at PBE; (ii) HSE06 SCF on
the same mesh (re-using the PBE charge density as the
initial guess); (iii) HSE06 non-self-consistent
calculation along the k-path. The HSE06 step is
$\sim 100\times$ slower than PBE; SCF convergence is
harder.

**Step 1 — PBE SCF** (`INCAR.PBE`): add `LWAVE`' and
`LCHARG`' to the minimal input above (to write the
wavefunction and charge for the next step):

```bash
LWAVE  = .TRUE.
LCHARG = .TRUE.
```

**Step 2 — HSE06 SCF** (`INCAR.HSE`): same POTCAR,
KPOINTS, POSCAR. INCAR changes:

```bash
LHFCALC = .TRUE.        # turn on hybrid functional
HFSCREEN = 0.2          # HSE06 screening, 1/Angstrom
ALGO = Damped           # robust for HSE; 'All' is faster when stable
TIME = 0.4              # damped/All mixing parameter
PRECFOCK = Normal       # 'Fast' (FFT2) or 'Accurate' for the final run
EDIFF  = 1.0e-5         # tighter (1.0e-6) for production band gaps
```

The HSE06 SCF starts from the PBE charge density in
`CHGCAR`' if it is present. Run:
'mpirun -n 8 vasp_std'.

**Step 3 — HSE06 bands** (`INCAR.bands`): the k-path is
specified in `KPOINTS`' as a "line-mode" path:

```bash
# KPOINTS (line mode)
K-Path                  # header
6                       # number of high-symmetry segments
0.0  0.0  0.0   ! Gamma
0.5  0.0  0.5   ! X
0.5  0.25 0.75  ! W
0.375 0.375 0.375 ! K
0.0  0.0  0.0   ! Gamma
0.5  0.5  0.5   ! L
```

The bands INCAR has `ICHARG = 11' (read the converged
charge from `CHGCAR`, do not update) and `LWAVE = .FALSE.'
(we only need the eigenvalues):

```bash
LHFCALC = .TRUE.
HFSCREEN = 0.2
ALGO = Normal           # or 'Eigenvalue'
ICHARG = 11              # read CHGCAR, do not update
LWAVE  = .FALSE.
LCHARG = .FALSE.
EDIFF  = 1.0e-6
NBANDS = 16              # >= number of electrons / 2
```

To run:
'mpirun -n 8 vasp_std'. The band energies are in
`EIGENVAL`. Plot them with `p4vasp`, `sumo`, or a
custom script.

#### 10.2.3 What to tweak for X

- **To converge the total energy to 1 meV/atom**:
  sweep 'ENCUT' from the POTCAR 'ENMAX' (or
  `ENMIN`) to $1.5 \times$ `ENMAX`, recompute, and
  pick the smallest value at which the energy
  changes by less than 1 meV/atom. The VASP default
  `ENCUT = 1.3 x max(ENMAX)' is usually safe.
- **To converge the band gap to 0.05 eV**: increase
  `ENCUT`, tighten 'EDIFF' to '1.0e-6`, increase
  the k-point mesh, and add `LREAL = .FALSE.' (the
  projector operators are evaluated in reciprocal
  space) for the final run. For an accurate gap
  with semilocal functionals, switch to a hybrid
  ('LHFCALC = .TRUE.', `HFSCREEN = 0.2' for HSE06)
  or to a $G_0W_0$ correction via `vasp_gw`.
- **For metals**: use `ISMEAR = 1' (Methfessel–
  Paxton, 1st order) or `ISMEAR = 2' (Fermi–Dirac)
  with `SIGMA = 0.05-0.2' eV. Never use
  `ISMEAR = 0' (Gaussian) for metals. For very high
  accuracy, use `ISMEAR = -5' (tetrahedron with
  Blöchl corrections) on a dense enough mesh.
- **For spin-polarised systems**: set `ISPIN = 2'
  and specify `MAGMOM`' for every species (e.g.
  'MAGMOM = 2*0.5' for two Fe atoms, or '2*2.0'
  for a strong initial moment). For non-collinear,
  use `LNONCOLLINEAR = .TRUE.' and the 3-component
  `MAGMOM`' array.
- **For geometry optimisation**: use `IBRION = 2'
  (conjugate gradient) and `ISIF = 3' for full
  variable-cell, or `ISIF = 2' for ions-only.
  `IBRION = 1' (RMM-DIIS) is the workhorse.
  `EDIFFG = -0.02' eV/Å is the default.

#### 10.2.4 Common pitfalls

- **POTCAR ordering must match the POSCAR species
  order**: VASP silently uses the wrong
  pseudopotential if the order is wrong. The error
  is on the order of the difference between
  valence configurations. Always check with
  'grep TITEL POTCAR' and 'head POSCAR`.
- **POTCAR family mismatch**: the `POTCAR`' must be
  all `PBE`, all `LDA`, all `PBE_52`, etc. Mixing
  families gives a non-variational total energy.
- **LMAXMIX too small for d/f electrons**: VASP
  re-mixes the charge density in real space during
  SCF with an `LMAXMIX`-dependent augmentation. For
  transition metals and rare earths, set
  'LMAXMIX = 4' (or '6' for f-block) to avoid SCF
  convergence problems.
- **ISMEAR = 0 for metals**: Gaussian smearing
  with the default `SIGMA = 0.05' eV gives an
  entropy contribution to the free energy that is
  *larger* than the convergence error in the band
  energy. Always use 'ISMEAR = 1' or '-5' for
  metals, and check `smearing T*S -> 0' in
  `OUTCAR`.
- **Missing `MAGMOM`' for magnetic systems**: VASP
  defaults to non-spin-polarised ('ISPIN = 1'). For
  a magnetic ground state set `ISPIN = 2' and an
  initial `MAGMOM`. Without it, the SCF converges to
  a non-magnetic state and gives a wrong energy.

#### 10.2.5 Cross-references

- Theory: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7
  (plane waves), [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }})
  §7.3 (Bloch), §7.6 (k-points), §7.11 (tetrahedron).
- PAW: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7 (Blöchl),
  §8.12 (the VASP PAW library).
- Hybrid functionals: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.5.
- Forces and relaxation: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
  §4.7 (Hellmann–Feynman), §4.7.3 (Pulay).

---

### 10.3 GPAW

GPAW is a Python / C PAW code with a real-space grid
([§4.2](#42-gpaw)). The cheatsheet below uses the ASE
interface ([§9.1](#91-ase-atomic-simulation-environment))
— the same script works in serial, in parallel (with
'mpiexec gpaw python script.py'), and on a GPU (with
the `gpaw.cuda' build).

#### 10.3.1 Minimal script — H₂ SCF

The smallest script that produces a sensible
single-point energy on a hydrogen molecule:

```python
# h2.py
from ase import Atoms
from gpaw import GPAW, PW

h2 = Atoms('H2', positions=[(0, 0, 0), (0, 0, 0.74)])
h2.center(vacuum=4.0)             # pad the cell to avoid image interactions

calc = GPAW(
    mode=PW(300),                 # plane-wave cutoff, eV
    xc='PBE',
    kpts=(1, 1, 1),               # Gamma-only for a molecule
    txt='h2.txt',                 # log file
)
h2.calc = calc
energy = h2.get_potential_energy()
print(f'H2 energy: {energy:.4f} eV')
```

Run: 'gpaw python h2.py'. The total energy is in eV
(the GPAW output is in eV by default, unlike Quantum
ESPRESSO which uses Rydberg).

#### 10.3.2 Annotated example — Si band structure in 20 lines

A band structure of bulk silicon with a plane-wave
PAW calculation:

```python
# si_bands.py
import numpy as np
from ase.build import bulk
from ase.dft.kpoints import bandpath
from gpaw import GPAW, PW

# 1. Build the structure
si = bulk('Si', 'diamond', a=5.43)

# 2. Standard SCF on a uniform mesh
si.calc = GPAW(
    mode=PW(300),
    xc='PBE',
    kpts=(8, 8, 8),
    convergence={'energy': 1.0e-6},
    txt='si.scf.txt',
)
si.get_potential_energy()                   # runs the SCF
si.calc.write('si.gpw', mode='all')         # save everything for re-use

# 3. Non-self-consistent band structure along a path
calc = GPAW('si.gpw').fixed_density()       # reload, hold density fixed
kpts, x, X = bandpath('GXWKL', si.cell, npoints=60)
calc.set(kpts=kpts)                        # re-attach the calculator
si.calc = calc
si.get_potential_energy()                   # NSCF run

# 4. Extract the band structure
bs = calc.band_structure()
bs.plot(filename='si.bands.png', emax=15)  # one line for the plot
```

The 'mode='all'' write in step 2 saves *bot'h*' the
wavefunctions and the density. The `fixed_density()'
load in step 3 re-uses the SCF density for a
non-self-consistent NSCF run along the k-path —
exactly the same two-step workflow as QE / VASP, but
expressed in Python and re-runnable from a Jupyter
notebook. The `bs.plot()' call in step 4 produces a
publication-quality band-structure plot with one line
of code.

#### 10.3.3 What to tweak for X

- **To switch to a real-space grid**: replace
  'mode=PW(300)' with 'mode='fd'' (default
  $h = 0.2$ Å). The FD mode is faster for small
  systems and has no wrap-around from periodic
  images of a localised excitation.
- **To switch to LCAO** (linear-scaling DFT for
  large systems): use `mode='lcao'' and
  `basis='dzp'`. LCAO is mandatory for systems
  beyond a few hundred atoms; diagonalisation is
  the bottleneck otherwise.
- **To add spin–orbit coupling**: use `soc=True'
  in the calculator (GPAW switches to non-collinear
  automatically) or run a non-collinear NSCF after a
  collinear SCF. Spin–orbit in GPAW is non-collinear
  by construction.
- **To compute a DOS**: after the SCF, use
  `e, dos = si.calc.get_dos(spin=0)' and plot.
  Tetrahedron integration on the MP mesh by
  default; increase the mesh density to converge.
- **For TDDFT**: use the `GPAW(...).tddft()' API
  with `propagate(...)' (real-time TDDFT) or
  `Casida`' post-processing (linear-response TDDFT).
  Both are well-integrated with ASE.

#### 10.3.4 Common pitfalls

- **kpts=(1, 1, 1) for a periodic solid**: this is
  right for a *molecule* in a large cell, but wrong
  for a periodic solid. The default `kpts=(1, 1, 1)'
  (Gamma only) gives a wrong band structure for a
  metal and an under-converged one for a
  semiconductor. Always set `kpts`' for a solid.
- **PAW dataset version**: GPAW ships its own PAW
  library (`gpaw-setups' on PyPI). Default is the
  '0.9.x' series; older '0.8.x' data should not be
  used for new work.
- **LCAO basis convergence**: the `dzp`' basis is
  the default; for production band gaps, check
  convergence with `basis='tzp'' or a manually
  constructed set.
- **Real-space grid spacing**: the default
  $h = 0.2$ Å is usually fine, but for accurate
  forces use $h = 0.15$ Å or smaller. Convergence
  is exponential in $h$ (multi-grid).
- **fixed_density() requires mode='all'**: needs
  both density *an`d*' wavefunctions from the SCF.
  If you write `mode='wavefunctions'' instead, the
  band-structure run fails.

#### 10.3.5 Cross-references

- ASE interface: [§9.1](#91-ase-atomic-simulation-environment).
- PAW method: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7.
- TDDFT: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.3
  (Runge–Gross, Casida).
- Real-space grids: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.8. ---

### 10.4 SIESTA

SIESTA is a Fortran NAO basis code
([§4.3](#43-siesta)). The cheatsheet below uses the
**fdf** (flexible data format) input — a
Fortran-NAMELIST-inspired free format. The
pseudopotential is a separate file (`.psf' or
`.vps`).

#### 10.4.1 Minimal input — H₂ SCF

The smallest input that produces a sensible
single-point energy on a hydrogen molecule:

```fortran
# h2.fdf
SystemName          h2
SystemLabel         h2
LatticeConstant     1.0 Ang
%block LatticeVectors
    10.0  0.0   0.0
     0.0 10.0   0.0
     0.0  0.0  10.0
%endblock LatticeVectors
NumberOfAtoms        2
NumberOfSpecies      1
%block ChemicalSpeciesLabel
   1  1  H
%endblock ChemicalSpeciesLabel
%block AtomicCoordinatesAndAtomicNumbers
    0.0  0.0  0.0   1
    0.0  0.0  0.74  1
%endblock AtomicCoordinatesAndAtomicNumbers
PAO.BasisSize        DZP            # SZ | DZ | DZP | TZP
PAO.EnergyShift      0.05 eV        # energy shift of the radial functions
SplitNorm            0.15
MeshCutoff           100 Ry
XC.functional        GGA            # PBE
XC.authors           PBE
SolutionMethod       diagon
MaxSCFIterations     100
DM.MixingWeight      0.1
DM.NumberPulaySteps  5
DM.Tolerance         1.0d-4
```

The H₂ SCF total energy is in `h2.out' after
'siesta: Total energy ='.

#### 10.4.2 Annotated example — Si band structure

A band structure of bulk silicon. The key
SIESTA-specific parameters are the **PAO basis**
(`PAO.BasisSize`, `PAO.EnergyShift`, `SplitNorm`)
and the **MeshCutoff** (the real-space grid for the
Poisson solver and the local part of the
Hamiltonian).

```fortran
# si.fdf
SystemName          si
SystemLabel         si
LatticeConstant     1.0 Ang
%block LatticeVectors
     0.0   2.715  2.715
     2.715  0.0   2.715
     2.715  2.715  0.0
%endblock LatticeVectors
NumberOfAtoms        2
NumberOfSpecies      1
%block ChemicalSpeciesLabel
   1  14  Si
%endblock ChemicalSpeciesLabel
%block AtomicCoordinatesAndAtomicNumbers
    0.00  0.00  0.00  14
    0.25  0.25  0.25  14
%endblock AtomicCoordinatesAndAtomicNumbers
%block kgrid_Monkhorst_Pack
    8   0   0   0.0
    0   8   0   0.0
    0   0   8   0.0
%endblock kgrid_Monkhorst_Pack
PAO.BasisSize        DZP
PAO.EnergyShift      0.05 eV
SplitNorm            0.15
MeshCutoff           200 Ry
XC.functional        GGA
XC.authors           PBE
SolutionMethod       diagon
MaxSCFIterations     200
DM.MixingWeight      0.1
DM.NumberPulaySteps  5
DM.Tolerance         1.0d-5
```

For a band structure, set '%block BandLines' *instea'd*'
of the Monkhorst–Pack `kgrid_Monkhorst_Pack`:

```fortran
BandPointsScale      pi/a
WriteBands           .true.
%block BandLines
   1   0.000  0.000  0.000  Gamma
  30   0.500  0.000  0.500  X
  30   0.500  0.250  0.750  W
  30   0.375  0.375  0.375  K
  30   0.000  0.000  0.000  Gamma
  30   0.500  0.500  0.500  L
%endblock BandLines
```

The first column of `BandLines`' is the number of
k-points per segment; the last column is a label.
SIESTA writes the bands to `SystemLabel.bands`.

#### 10.4.3 What to tweak for X

- **To converge the basis set**: sweep
  `PAO.BasisSize' from SZ to DZP to TZP. For
  production band gaps, use DZP or TZP; for
  high-throughput screening, SZ is often
  acceptable.
- **To tighten the radial functions**: reduce
  `PAO.EnergyShift' from 0.05 eV to 0.01 eV —
  increases the cutoff radius and improves basis
  completeness at the cost of more overlap.
- **To converge the real-space mesh**: increase
  `MeshCutoff`' in Ry. The default 100–200 Ry is
  usually fine; for accurate forces, use 400 Ry or
  higher.
- **For metals**: set `SolutionMethod = diagon'
  with `MeshCutoff = 300' and a denser k-mesh
  ($12 \times 12 \times 12$ or more). Add
  `OccupationFunction FD' and a small electronic
  temperature.
- **For spin-polarised systems**: set
  `SpinPolarized .true.' and provide initial
  magnetic moments ('%block DM.InitSpin'). For
  non-collinear, use 'NonCollinearSpin .true.'.
- **For spin–orbit coupling**: set
  `SpinOrbitBit .true.' and use the fully-
  relativistic pseudopotential (`.vps' for some
  elements).

#### 10.4.4 Common pitfalls

- **PAO.EnergyShift units**: `meV`, `eV`, or `Ry`;
  SIESTA converts to the internal unit. The
  default (no unit) is `Ry`; 0.05 eV is good. The
  legacy default of 0.02 Ry (272 meV) is *too
  large* and gives a *too compact basis.
- **Basis convergence is *basis* convergence, not
  *mes'h*' convergence**: a too-small 'PAO.BasisSize'
  or a too-large `PAO.EnergyShift' is *not* fixed
  by `MeshCutoff`.
- **`MeshCutoff`' in Ry, not eV**: SIESTA uses Ry
  internally; the input is in Ry (or eV with the
  `eV`' unit). A common mistake is to use 100 *eV*
  (about 7.35 Ry) thinking it is Ry — 100 Ry is
  1360 eV.
- **'.vps' vs '.psf'**: '.vps' files (Siesta-specific
  generator) are usually better than the older
  `.psf' files.
- **Forgetting XC.authors**: `XC.functional = GGA'
  without `XC.authors = PBE' falls back to PW91,
  not PBE. Always set the XC authors explicitly.

#### 10.4.5 Cross-references

- NAO basis: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.13.
- Pseudopotentials: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.3
  (norm-conserving), §8.5 (Kleinman–Bylander form).
- Real-space Poisson: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.8.
- Linear-scaling DFT: SIESTA's "Order-N" mode is one of the
  few production linear-scaling codes ([§4.3](#43-siesta)).

---

### 10.5 CP2K

CP2K is a Fortran mixed Gaussian / plane-wave (GPW)
code ([§2.5](#25-cp2k)). The cheatsheet below covers
the standard 'cp2k.psmp' (or 'cp2k.popt`) executable.
The input format is a *structure`d*' Fortran-NAMELIST
with explicit section keywords (`&GLOBAL`, `&SUBSYS`,
`&DFT`, …) and matching `&END' lines. Indentation is
optional but is the standard convention.

#### 10.5.1 Minimal input — water in a box

The smallest input that produces a sensible geometry
optimisation of a water molecule in a cubic box:

```fortran
! h2o.inp
&GLOBAL PROJECT h2o RUN_TYPE GEO_OPT PRINT_LEVEL MEDIUM &END GLOBAL

&MOTION
  &GEO_OPT TYPE MINIMIZATION OPTIMIZER BFGS MAX_ITER 100 &END GEO_OPT
&END MOTION

&FORCE_EVAL
  METHOD QUICKSTEP
  &DFT
    BASIS_SET_FILE_NAME  BASIS_MOLOPT
    POTENTIAL_FILE_NAME  GTH_POTENTIALS
    CHARGE 0  MULTIPLICITY 1
    &QS EPS_DEFAULT 1.0E-12 &END QS
    &POISSON PERIODIC NONE PSOLVER MT &END POISSON
    &MGRID CUTOFF 300 REL_CUTOFF 50 &END MGRID
    &SCF MAX_SCF 50 EPS_SCF 1.0E-6 SCF_GUESS ATOMIC &END SCF
    &XC
      &XC_FUNCTIONAL PBE &END XC_FUNCTIONAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL ABC 6.0 6.0 6.0 PERIODIC NONE &END CELL
    &COORD
      O   0.000  0.000  0.000
      H   0.957  0.000  0.000
      H  -0.240  0.927  0.000
    &END COORD
    &KIND O BASIS_SET DZVP-MOLOPT-GTH POTENTIAL GTH-PBE-q6 &END KIND
    &KIND H BASIS_SET DZVP-MOLOPT-GTH POTENTIAL GTH-PBE-q1 &END KIND
  &END SUBSYS
&END FORCE_EVAL
```

To run:
'mpiexec -n 4 cp2k.psmp -i h2o.inp -o h2o.out'. The
geometry optimisation converges in ~5 steps; the total
energy is in `h2o.out' after
'ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.)'.

#### 10.5.2 Annotated example — NVT molecular dynamics of water

A short Born–Oppenheimer MD of a 32-water box at
300 K, the canonical "CP2K can do this" test case.
The `&FORCE_EVAL' block from the previous example is
re-used almost unchanged; only the `&MOTION' block
changes to MD.

```fortran
! md32h2o.inp
&GLOBAL
  PROJECT  md32h2o
  RUN_TYPE MD
  PRINT_LEVEL LOW
&END GLOBAL

&MOTION
  &MD
    ENSEMBLE NVT
    STEPS 1000
    TIMESTEP 0.5
    TEMPERATURE 300
    &THERMOSTAT REGION MASSIVE
      &NOSE LENGTH 3 YOSHIDA 3 TIMECON 1000 &END NOSE
    &END THERMOSTAT
  &END MD
  &PRINT
    &TRAJECTORY &EACH MD 1 &END EACH &END TRAJECTORY
    &RESTART   &EACH MD 50 &END EACH &END RESTART
  &END PRINT
&END MOTION

! &FORCE_EVAL re-uses the water molecule block from h2o.inp
! above, with the following changes:
&FORCE_EVAL
  METHOD QUICKSTEP
  &DFT
    BASIS_SET_FILE_NAME  BASIS_MOLOPT
    POTENTIAL_FILE_NAME  GTH_POTENTIALS
    &POISSON PERIODIC XYZ PSOLVER PERIODIC &END POISSON
    &MGRID CUTOFF 400 REL_CUTOFF 60 &END MGRID
    &SCF MAX_SCF 20 EPS_SCF 1.0E-6 SCF_GUESS RESTART
      &OT MINIMIZER DIIS PRECONDITIONER FULL_SINGLE_INVERSE &END OT
    &END SCF
    &XC
      &XC_FUNCTIONAL PBE &END XC_FUNCTIONAL
      &VDW_POTENTIAL POTENTIAL_TYPE PAIR_POTENTIAL
        &PAIR_POTENTIAL PARAMETER_FILE_NAME dftd3.dat
          TYPE DFTD3 REFERENCE_FUNCTIONAL PBE
        &END PAIR_POTENTIAL
      &END VDW_POTENTIAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL ABC 9.852 9.852 9.852 PERIODIC XYZ &END CELL
    &TOPOLOGY COORD_FILE_NAME water32.xyz COORD_FILE_FORMAT XYZ
      &CENTER_COORDINATES &END CENTER_COORDINATES
    &END TOPOLOGY
    &KIND O BASIS_SET DZVP-MOLOPT-GTH POTENTIAL GTH-PBE-q6 &END KIND
    &KIND H BASIS_SET DZVP-MOLOPT-GTH POTENTIAL GTH-PBE-q1 &END KIND
  &END SUBSYS
&END FORCE_EVAL
```

The `water32.xyz' is a standard XYZ with 32 waters
(96 atoms). D3 dispersion
([chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.7)
is enabled with '&VDW_POTENTIAL ... TYPE DFTD3'. The OT
solver (`&OT`) is the recommended SCF solver for large
systems: it is much more parallel-scalable than the
default diagonalisation, at the cost of requiring a
localised initial guess.

#### 10.5.3 What to tweak for X

- **To converge the total energy to 1 meV/atom**:
  sweep `CUTOFF`' from 300 to 1000 Ry, recompute,
  and pick the smallest value at which the energy
  changes by less than 1 meV/atom.
- **To converge the SCF**: tighten `EPS_SCF`'
  from '1.0E-6' to '1.0E-7`. For a difficult
  system, switch from `SCF_GUESS ATOMIC' to
  `RESTART`' from a previous run.
- **For large systems** (thousands of atoms): switch
  the SCF solver from 'DIAGONALIZATION' to 'OT'
  (orbital transformation). OT scales linearly
  with system size and is the default for
  production MD on large boxes.
- **For periodic systems**: set
  `&POISSON PERIODIC XYZ ... PSOLVER PERIODIC' and
  add a `&KPOINTS' section.
- **For geometry optimisation**: set
  'RUN_TYPE GEO_OPT' and choose an '&OPTIMIZER'
  (BFGS is the default; CG, LBFGS also available).
  For variable-cell, add
  '&CELL_OPT EXTERNAL_PRESSURE ...'.
- **For AIMD**: set `RUN_TYPE MD' and add an
  `&MD' block. The default is NVE; for NVT, add a
  thermostat ('&NOSE' / '&CSVR' / `&GLE`).

#### 10.5.4 Common pitfalls

- **CUTOFF too small for the chosen basis**: the
  Gaussian basis introduces spurious high-frequency
  components that the plane-wave auxiliary grid
  must represent. The `CUTOFF`' is for the
  *auxiliary* grid. 300 Ry is fine for DZVP, TZV2P
  needs 600–1000 Ry. Always check convergence.
- **SCF_GUESS ATOMIC for a difficult system**: the
  atomic guess is a superposition of atomic
  densities and is the most *robust* starting
  point, but it can be far from the converged
  density for covalent systems. Use `RESTART`' from
  a previous run, or 'SCF_GUESS HISTORY', for
  difficult cases.
- **Basis set / pseudopotential mismatch**: the
  GTH pseudopotential was generated with a
  *specifi`c*' basis set. Mixing GTH with a non-
  MOLOPT basis gives poor results. Always use the
  matched pair (e.g. `DZVP-MOLOPT-GTH' with
  `GTH-PBE-q6`).
- **POISSON PSOLVER MT for a periodic system**:
  the Martyna–Tuckerman solver is for *isolate`d*'
  systems. For a periodic system, use
  'PSOLVER PERIODIC' and 'PERIODIC XYZ`.
- **MD timestep too large**: the default 0.5 fs is
  safe for water with PBE. For H–H bonds or fast
  stretches, use 0.25 fs or smaller.

#### 10.5.5 Cross-references

- Theory: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7
  (plane waves), §6.3 (Gaussians).
- Pseudopotentials: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.8 (GTH).
- Dispersion corrections: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.7 (D3, D4).
- Forces and MD: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7
  (Hellmann–Feynman), §4.10.3 (Ehrenfest / BO-MD).

---

### 10.6 FLEUR

FLEUR is a Fortran FP-LAPW code
([§3.3](#33-fleur)). The cheatsheet below covers the
'inp' file (the main input) and the 'inpgen'
generator. FLEUR uses a two-step workflow: `inpgen`'
reads a structure (CIF or template) and produces the
'inp' file, then 'fleur' reads the `inp`' and runs.

#### 10.6.1 Minimal input — Fe bcc, spin-polarised

The smallest input that produces a sensible
spin-polarised ground state for bcc iron. The
structure is taken from `Fe.cif`; the generator
produces the `inp`' file.

**Step 1 — generate the input**:

```bash
# in the directory containing Fe.cif:
cat > inp.txt <<EOF
&input
  cartesian=F
  symrel=T
  film=T              ! 3D periodic (set film=F for 2D)
  rmt= 2.0            ! muffin-tin radius, bohr
  lmax= 8
  lnonsph= 4
  kcrel= 0            ! 0 = scalar-relativistic,
                      ! 1 = full-relativistic (with SOC)
/
&lattice
  ext=T               ! read lattice from external file (CIF)
/
&atom
  id= 26.1
  bmu= 2.2            ! initial magnetic moment, mu_B
  lo= 3s 3p           ! local orbitals for semicore states
  econfig= 3d6 4s2
/
EOF
inpgen < inp.txt
```

The 'inpgen' input is read from 'inp.txt`; the
output 'inp' is written. 'bmu=2.2' sets the initial
magnetic moment; `lo=3s 3p' adds local orbitals for
the 3s and 3p semicore states (necessary for an
accurate all-electron treatment of 3$d$ transition
metals).

**Step 2 — run FLEUR**:

```bash
fleur_MPI
```

The total energy is in 'out' (or 'out.xml`) after
'Total energy              :'.

#### 10.6.2 Annotated example — Fe bcc with spin–orbit coupling

The same system as above, but with spin–orbit
coupling (necessary for a correct magnetic
anisotropy energy;
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.9).
Re-run 'inpgen' with 'kcrel=1' (full-relativistic)
and add the magnetisation direction 'cth=30, 30, 30':

```bash
sed -i 's/kcrel=  0/kcrel=  1/' inp.txt   # or edit by hand
cat >> inp.txt <<EOF
&input
  cth= 30.0, 30.0, 30.0   ! magnetisation direction (theta, phi, alpha)
  swsp= 0                 ! 0 = ferromagnet, 1 = spin-spiral
/
EOF
inpgen < inp.txt
fleur_MPI
```

The MAE is the *difference* in total energy between
two magnetisation directions (e.g. `cth=0, 0, 0' —
z axis — versus `cth=90, 0, 0' — x axis). With SOC,
the k-mesh must be denser (an MAE of 0.1 meV/atom
is the typical target), and `lmax=8' should be
increased to `lmax=10' for production.

#### 10.6.3 What to tweak for X

- **To converge the basis set**: increase `lmax`'
  (max angular momentum of LAPW) and `lnonsph`'
  (max $L$ in non-spherical potential). Default:
  'lmax=8, lnonsph=4'; production: `lmax=10,
  lnonsph=6`.
- **To converge k-point sampling**: increase the
  k-point mesh. FLEUR uses a uniform Monkhorst–Pack
  mesh; default $8 \times 8 \times 8$ for a
  primitive cubic cell. For accurate Fermi
  surfaces: $20 \times 20 \times 20$ or denser.
- **To converge the magnetic anisotropy energy**:
  the MAE is a difference of total energies and
  converges very slowly with k-point mesh. For an
  MAE of 0.1 $\mu$eV/atom, a
  $40 \times 40 \times 40$ mesh is often required.
- **For $f$-electron systems** (rare earths,
  actinides): add local orbitals for $5s$, $5p$,
  $4f$ (or $6s$, $6p$, $5f$) semicore states, and
  set 'lmax=12, lnonsph=8'. Without them, the
  all-electron treatment is wrong by tens of mRy.
- **For spin–orbit coupling**: use `kcrel=1' and
  check convergence of `lmax`' and the k-mesh. The
  non-collinear version of the code is mandatory.

#### 10.6.4 Common pitfalls

- **Muffin-tin radii too small**: the MT radii
  must not overlap; `inpgen`' checks and aborts if
  they do. Default `rmt=2.0' is usually fine for
  bcc Fe. For low-symmetry structures, tune by
  hand.
- **Muffin-tin radii too large**: a too-large
  `rmt`' leaves little room for the plane-wave
  expansion in the interstitial, and
  `kmax = RKmax / RMT' becomes too small.
  Default `RKmax=7.0' is usually fine; production:
  'RKmax=8.5' or '9.0`.
- **Missing local orbitals for semicore states**:
  the $3s$ and $3p$ of Fe overlap with the 3$d$
  valence in energy. Without local orbitals, the
  all-electron treatment of 3$d$ is wrong. Always
  add `lo=3s 3p' for 3$d$ metals and the analogous
  local orbitals for heavier elements.
- **`kcrel=0' (scalar-relativistic) for SOC**:
  scalar-relativistic FLEUR misses spin–orbit
  coupling. For a correct MAE or any property
  that depends on the spin texture, use `kcrel=1`.
- **Inconsistent kcrel between inpgen and fleur**:
  the flag must be set in `inpgen`' and the input
  re-generated if changed. Running `fleur`' on an
  old 'inp' with the wrong 'kcrel' silently gives
  a scalar-relativistic answer.

#### 10.6.5 Cross-references

- LAPW basis: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.9–6.12
  and [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.13–8.14
  (all-electron methods).
- Relativistic KS and MAE: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.9
  and §4.9.3 (magnetic anisotropy energy).
- All-electron comparisons: [§3.1](#31-wien2k) (WIEN2k), [§3.2](#32-elk) (Elk).

---

> Back to the [chapter index]({{ "/dft-notes/" | relative_url }}) or
> jump to [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }})
> for the theory of basis sets that makes the
> "Gaussian vs. plane wave vs. real space" split sensible.
