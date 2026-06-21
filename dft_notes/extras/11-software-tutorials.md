---
layout: page
title: "Software tutorials — DFT codes in depth"
permalink: /dft-notes/extras/software-tutorials/
description: >-
  Deep, hands-on tutorials for five production DFT codes: VASP,
  Quantum ESPRESSO, ORCA, GPAW, and CP2K. Each tutorial covers
  install, input-file templates, convergence testing, common
  errors, advanced features (SOC, DFT+U, hybrid functionals,
  phonons, NEB), and a complete worked example.
keywords: "VASP, Quantum ESPRESSO, ORCA, GPAW, CP2K, DFT tutorial,
  plane wave, PAW, AIMD, NEB, phonon, INCAR, KPOINTS, POTCAR,
  pw.x, ph.x, neb.x, TDDFT, hybrid functional, PBE0, HSE06,
  spin-orbit coupling"
---

# Software tutorials — DFT codes in depth

> The [software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
> tells you *whic`h*' code to reach for. This page tells
> you *how to actually use* the five most-cited
> production codes in electronic-structure theory: how
> to install them, what to put in the input file, how
> to converge the result, what the cryptic error
> messages mean, and how to run a complete worked
> calculation end-to-end.

The five codes covered here are:

1. **VASP** — the de facto workhorse of solid-state DFT
   ([§1](#1-vasp)).
2. **Quantum ESPRESSO** — the open-source counterpart, with
   the deepest phonons module
   ([§2](#2-quantum-espresso)).
3. **ORCA** — the workhorse of *molecular* quantum chemistry:
   hybrid DFT, TDDFT, multi-reference, DLPNO-CCSD(T)
   ([§3](#3-orca)).
4. **GPAW** — a Python/PAW code with ASE integration; the
   natural choice when the rest of your workflow is in Python
   ([§4](#4-gpaw)).
5. **CP2K** — the mixed Gaussian / plane-wave code, the
   standard for *ab initio* molecular dynamics on thousand-
   atom systems ([§5](#5-cp2k)).

Each section has the same structure, mirroring the
"what-to-tweak / common-pitfalls" style of the
cheatsheet but going substantially deeper:

- **Overview** — what the code is, what it is best at, its
  license, and its user community.
- **Install** — how to obtain and build it, the dependencies,
  and the licensing terms.
- **Input file template** — a minimal but *real* input for a
  simple H₂O / Si / H₂ calculation, with every key parameter
  explained.
- **Convergence tests** — the practical recipe for
  converging the total energy, the band gap, the
  geometry, and the forces.
- **Common errors** — a table mapping the error message to
  the most likely cause and the fix.
- **Advanced features** — the syntax for SOC, DFT+U, hybrid
  functionals, vdW corrections, NEB, phonons, TDDFT, etc.
- **Worked example** — a complete end-to-end calculation
  (input files + output analysis) for at least one of:
  geometry optimisation, band structure, phonon dispersion,
  NEB, DOS / projected DOS.

> **How to read this page.** The page is long. Treat each
> section as a *self-contained manual* for one code. Skim the
> Overview and the Worked Example first; come back to the
> convergence tests and common errors when you are
> stuck on day three of a project. The "what to tweak" lists
> are the answers to the questions you will ask on the third
> day; the "common errors" tables are the answers to the
> questions you will ask on the third week.
>
> **Cross-references.** This page assumes the theory in
> [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) (forces,
> geometry optimisation, response),
> [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) (XC functionals,
> hybrids, vdW),
> [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) (basis sets:
> plane waves, Gaussians, PAW, real-space grids),
> [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) (solids, Bloch,
> k-points, smearing),
> [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) (pseudopotentials,
> PAW), [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}) (phonons),
> [chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) (response and
> TDDFT), [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (DFT+U,
> DFT+DMFT, hybrid functionals in practice), and
> [chapter 13]({{ "/dft-notes/chapter-13/" | relative_url }}) (NEB, dimer
> method, rare events). Per-code cross-references are
> given at the end of each code section.

---

## Table of contents

1. [VASP](#1-vasp)
   1. [Overview](#11-overview)
   2. [Install](#12-install)
   3. [Input file template — H₂O in a box](#13-input-file-template--h2o-in-a-box)
   4. [Convergence tests](#14-convergence-tests)
   5. [Common errors](#15-common-errors)
   6. [Advanced features](#16-advanced-features)
   7. [Worked example — band structure of Si with HSE06](#17-worked-example--band-structure-of-si-with-hse06)
2. [Quantum ESPRESSO](#2-quantum-espresso)
3. [ORCA](#3-orca)
4. [GPAW](#4-gpaw)
5. [CP2K](#5-cp2k)

---

## 1. VASP

### 1.1 Overview

VASP (Vienna Ab initio Simulation Package) is a Fortran
plane-wave DFT code that uses the **projector augmented
wave (PAW)** method
([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7, §8.12).
It is the most-cited DFT code in materials science: a 2024
Web-of-Science search returns > 100,000 papers citing the
original Kresse–Hafner / Kresse–Furthmüller series. The
combination of a comprehensive PAW pseudopotential library
([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.12), an aggressive
MPI / OpenMP parallelisation, a mature and *standardise`d*'
input file layout, and a 30-year investment in user-facing
features (DFPT phonons, NEB, dimer method, ML force fields,
$GW$, BSE) has made VASP the workhorse of solid-state DFT in
both industrial R&D (battery materials, catalysis, alloys,
semiconductors) and academic condensed-matter physics. Its
main limitation is the licence: VASP is commercial
software, with a "VASP Software User Licence" that costs
~€5,000/year for a research group. For a 50-atom metallic
alloy in a 500-atom cell with a hybrid functional, VASP
remains the most user-friendly code; the alternatives
(Quantum ESPRESSO, CASTEP, ABINIT) are open-source but lag
VASP in *ease-of-use* and in the depth of the PAW library.

### 1.2 Install

VASP is distributed as pre-compiled binaries or as source
code to licence holders. The build process uses
`makefile.include' (the system-specific configuration file)
and a Fortran 2003 compiler (Intel `ifort`, AMD `flang`, or
NVIDIA `nvfortran`). VASP supports MPI, OpenMP hybrid
parallelism, and (for the `vasp_gpu`' build) CUDA / HIP
acceleration on NVIDIA and AMD GPUs. The dependencies are
modest: a Fortran compiler, MPI (`openmpi`, `mpich`, or
Intel MPI), an FFT library (Intel MKL, AMD `fftw3`, or
NVIDIA `cuFFT`), BLAS / LAPACK, and the `libxc`' library
for the newer exchange-correlation functionals.

```bash
# Typical build steps
# 1. Get the source from the VASP portal (login required):
#    <https://www.vasp.at/>
unzip vasp.6.4.0.tar.gz
cd vasp.6.4.0

# 2. Copy a template makefile.include and edit for your system
cp arch/makefile.include.linux_intel makefile.include
#    Edit the following lines in makefile.include:
#      FC      = mpiifort
#      FCL     = mpiifort -mkl
#      OFLAG   = -O3 -xHOST
#      MKLROOT = /opt/intel/oneapi/mkl/latest

# 3. Compile (this takes ~30 minutes on a modern machine)
make -j 8

# 4. Verify
mpirun -n 4 ./bin/vasp_std
```

Licensing is annual (calendar year), with a discounted
"renewal" fee. Academic groups at degree-granting
institutions pay the standard academic fee; commercial
users pay a different rate. The "VASP Support Forum"
(`<https://vasp.at/forum/`>) is the primary support channel.

### 1.3 Input file template — H₂O in a box

A single-point energy on a single water molecule in a cubic
box of side 10 Å. Four files: `INCAR`, `KPOINTS`, `POSCAR`,
`POTCAR`. The `POTCAR`' is built by concatenating the
per-element PAW potentials in the order the species appear
in `POSCAR`.

```bash
# INCAR
SYSTEM = H2O in a box
ENCUT  = 520        # plane-wave cutoff, eV
EDIFF  = 1.0e-6     # SCF convergence, eV
ISMEAR = 0          # Gaussian smearing (semiconductor / molecule)
SIGMA  = 0.05       # smearing width, eV
IBRION = -1         # no ionic update (static SCF)
ISIF   = 2          # no stress (no cell update)
PREC   = Accurate   # default: Normal; tighten for final production
EDIFFG = -0.02      # force convergence, eV/Angstrom (not used for ISIF=2)
LWAVE  = .FALSE.    # do not write WAVECAR
LCHARG = .FALSE.    # do not write CHGCAR
LREAL  = .FALSE.    # projector operators in reciprocal space (most accurate)
```

```bash
# KPOINTS
Automatic mesh
0              # 0 = Monkhorst-Pack with explicit offsets
Gamma          # Gamma-centred mesh
1  1  1        # 1x1x1 (Gamma only) — a molecule in a large cell
0. 0. 0. # shift
```

```
# POSCAR
H2O in a box
  10.0           # cubic lattice constant, Angstrom
    1.0  0.0  0.0
    0.0  1.0  0.0
    0.0  0.0  1.0
O H
  1  2           # 1 O, 2 H
Cartesian
  0.000  0.000  0.000      # O
  0.957  0.000  0.000      # H
 -0.240  0.927  0.000      # H
```

```bash
# POTCAR — built by concatenating per-element PAW potentials
# from the VASP library, in POSCAR order:
$ cat $VASP_PP_PATH/pot/O/PBE/O/POTCAR \
      $VASP_PP_PATH/pot/H/PBE/H/POTCAR > POTCAR
# (The "PBE" variant; "PBE_52" and "LDA" are alternatives.)
```

To run on 8 cores:

```bash
mpirun -n 8 vasp_std > vasp.out 2>&1
```

The total energy (in eV) is on the last `free  energy'
line of `OUTCAR`:

```bash
$ grep "free  energy" OUTCAR | tail -1
  free  energy   TOTEN  =      -14.2203 eV
```

(For PBE on H₂O, the experimental equilibrium geometry
gives a total energy around -14.22 eV per molecule; this
matches the VASP PBE value to within ~ 5 meV depending on
the PAW variant.)

The four files above are the **minimum** needed. VASP also
recognises a number of optional auxiliary files (`CHGCAR`,
`WAVECAR`, 'KPOINTS_OPT' for 'IBRION = 6' finite-difference
phonons, `ML_FF`' for the machine-learning force field
interface, etc.) — these are introduced in the relevant
context below.

### 1.4 Convergence tests

VASP calculations are converged in three independent
parameters: the **plane-wave cutoff** `ENCUT`, the **k-point
mes`h*`* (`KPOINTS`), and the **electronic smearing**
('ISMEAR' / 'SIGMA`). The first two must be converged
*simultaneously* because the converged cutoff depends weakly
on the k-mesh and vice versa. The recipe:

1. **ENCUT convergence.** Pick the maximum `ENMAX`' from
   the 'POTCAR' (e.g. 'grep ENMAX POTCAR' returns the
   per-element cutoff; the maximum is the safe default).
   VASP recommends 'ENCUT = 1.3 × max(ENMAX)'. To
   *converge*, sweep `ENCUT`' from the default to
   `1.5 × max(ENMAX)' in steps of 20 eV, compute the total
   energy at the experimental geometry, and pick the
   smallest `ENCUT`' at which the total energy changes by
   less than 1 meV/atom. This typically lands in the range
   1.0 – 1.3 × `ENMAX`. For high-pressure phases
   (equation-of-state), tighten the convergence to
   0.1 meV/atom and pick the smallest converged `ENCUT`.

2. **K-point mesh.** For a metallic system, the k-mesh
   must be dense enough that the Fermi surface is sampled
   with at least ~ 50 k-points * 0.05 eV of smearing
   width. For a semiconductor with a clean band gap, the
   tetrahedron method ('ISMEAR = -5') converges much
   faster than smearing-based methods. The
   Materials-Project-style rule of thumb is **≥ 1000
   k-points per atom** in the *primitive* cell (i.e. a 2-
   atom Si cell wants an 8×8×8 mesh, a 4-atom cell wants
   a 6×6×6, etc.). Always converge *explicitly*: sweep
   the mesh density and pick the smallest that changes
   the total energy by less than 1 meV/atom.

3. **Smearing.** For molecules and semiconductors with a
   band gap, use `ISMEAR = 0' (Gaussian) with
   'SIGMA = 0.05' eV. For metals, use 'ISMEAR = 1'
   (Methfessel–Paxton, 1st order) with `SIGMA = 0.1 - 0.2'
   eV, and **always** check that the entropy term
   'smearing T*S' in 'OUTCAR' is smaller than the
   convergence target. The most accurate k-point
   integration is `ISMEAR = -5' (tetrahedron with Blöchl
   corrections), which works for insulators *an`d*' metals
   on a sufficiently dense mesh.

4. **SCF convergence.** The default `EDIFF = 1.0e-4' eV
   is too loose for production. Use `EDIFF = 1.0e-5' for
   routine geometry optimisation, `EDIFF = 1.0e-6' for
   final energies and band structures, and
   `EDIFF = 1.0e-7' for phonons and high-accuracy
   response.

5. **Geometry convergence.** `EDIFFG = -0.02' eV/Å is
   the default; `EDIFFG = -0.005' eV/Å is the production
   target for vibrational frequencies (a 1 cm⁻¹ error in
   a phonon corresponds to ~ 0.1 meV in the force
   difference). `EDIFFG = 0.01' (positive number,
   interpreted as an absolute energy change) is *muc`h*'
   looser and should not be used for production
   geometries.

### 1.5 Common errors

| Error message (or symptom)                                  | Likely cause                                          | Fix                                                                          |
|:------------------------------------------------------------|:------------------------------------------------------|:-----------------------------------------------------------------------------|
| 'ERROR: POTCARS do not match'                              | The 'POTCAR' was concatenated in the wrong order, or contains potentials from different families (PBE vs. LDA) | Rebuild 'POTCAR' so the order matches 'POSCAR' species; check `grep TITEL POTCAR' |
| 'WARNING: dE < EDIFF' but no convergence                    | SCF is stuck oscillating                              | Reduce 'AMIX' (e.g. 0.02), increase 'BMIX' (e.g. 1.5), or switch to 'ALGO = All' |
| 'ZBRENT: fatal error' during geometry optimisation          | 'POTCAR' has a too-shallow potential (e.g. `O_h`)    | Use a "harder" variant (e.g. `O`, `O_s`, 'O_h' — 'O_h' is the hardest)       |
| 'ZHEEV: eigenvalue solver failed'                          | Cell too small / atoms too close                      | Increase 'vacuum' (for slabs/molecules) or relax the cell with `ISIF = 3'    |
| 'WARNING: PSMAXN for non-local part exceeded'               | Too-small 'ENCUT' for a particular angular momentum   | Increase 'ENCUT' to at least the 'ENMAX' of the affected element             |
| 'BRMIX: charge density could not be remixed'                 | 'LMAXMIX' too small for a $d$- or $f$-block element  | Set `LMAXMIX = 4' (or 6 for $f$-block)                                        |
| 'EDWAV: internal error'                                    | Parallelisation issue on highly anisotropic cells     | Reduce 'NCORE' or `NPAR`, or switch to `KPAR`' decomposition                   |
| 'EDDDAV: RHOSYG internal error'                            | Same — too many k-points per MPI rank                  | 'KPAR = N_k' (split k-points across MPI ranks)                                |
| 'The distance between some ions is very small'              | Atoms too close in the initial 'POSCAR'                | Pre-relax with a smaller cell, or randomise the initial positions            |
| 'WARNING: SUBSPACEMAX > NPROCS'                              | 'NBANDS' not divisible by 'NPROCS'                     | Set 'NBANDS' to a multiple of 'NPROCS' (or 'NPAR' if used)                    |
| 'fatal error in DIIS'                                       | Non-collinear calculation with 'EDIFF' too tight      | Loosen 'EDIFF' for the first few steps; or initialise 'MAGMOM' explicitly      |
| 'LREAL = Auto' produces non-'LREAL = FALSE' energies         | The default 'LREAL = Auto' switches to real-space projectors; for high-accuracy work the result is not exactly the same | Set 'LREAL = .FALSE.' for the final run (slower but reproducible)             |
| 'WARNING: vasp encountered an internal error'               | OOM; 'LREAL' real-space projectors overflow memory    | Switch to 'LREAL = .FALSE.' or 'LREAL = OAuto', increase 'NCORE'              |
| 'IBRION = 5' (DFPT phonons) crashes on a metal               | DFPT requires a non-metallic ground state              | Use 'IBRION = 6' (finite differences) or 'ISMEAR = 0' with 'SIGMA = 0'       |

### 1.6 Advanced features

- **Hybrid functionals (HSE06, PBE0, SCAN0).** Set
  'LHFCALC = .TRUE.', `HFSCREEN = 0.2' (HSE06, screening
  in Å⁻¹), and `AEXX = 0.25' (the exact-exchange
  mixing, default for HSE06). `ALGO = Damped' is the
  robust default; `ALGO = All' is faster when stable.
  The hybrid SCF is ~50–100× slower than PBE, so
  converge the geometry at PBE first and run a
  single-point HSE06 calculation. For a band
  structure, run a PBE SCF (`LCHARG = .TRUE.' to write
  `CHGCAR`), then a hybrid NSCF with `ICHARG = 11'
  (read `CHGCAR`, do not update). See the worked
  example below.
- **DFT+U.** Set 'LDAU = .TRUE.' and 'LDAUTYPE = 2'
  (Dudarev's rotationally-invariant formulation
  [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }})). For
  a transition-metal oxide with the $d$ states localised,
  set 'LDAUL = 2' (the $l$ channel), 'LDAUU' and
  'LDAUJ' per species (e.g. 'LDAUU = 4.0 0.0' for O-d = 4
  eV, H-d = 0). For the Liechtenstein formulation
  ('LDAUTYPE = 1'), set both 'LDAUU' and 'LDAUJ' per
  $(l, m)$.
- **Spin–orbit coupling (SOC).** Set
  'LSORBIT = .TRUE.' and 'LNONCOLLINEAR = .TRUE.`. The
  initial `MAGMOM`' must be a 3-component vector (not a
  scalar). For a non-magnetic calculation with SOC, set
  'ISPIN = 1', 'LNONCOLLINEAR = .TRUE.', and
  'MAGMOM = 0 0 0'. The output is non-collinear
  ($2 \times 2$ density matrix); `LORBIT = 11' or
  `LORBIT = 13' produces the per-orbital projection.
- **van der Waals corrections (D3, D4, TS, MBD).** VASP
  ships Grimme's D3 since v5.4 ('IVDW = 12'). Set
  'IVDW = 12' for D3(BJ), 'IVDW = 20' for D4, `IVDW = 2'
  for Tkatchenko–Scheffler (TS), and `IVDW = 4' for the
  many-body dispersion (MBD@rsSCS). The D3 zero-damping
  is `IVDW = 11' and the Becke–Johnson damping is
  'IVDW = 12'.
- **Phonons (finite differences).** `IBRION = 6' with
  `NFREE = 2' (central differences) computes a phonon
  dispersion by finite differences. Requires a converged
  equilibrium geometry (forces < 0.001 eV/Å) and a
  non-metallic ground state (or a very dense k-mesh for
  metals). The output is a `phonon`' directory with the
  force constants; use 'phonopy' ('<https://phonopy.github.io/`>)
  to post-process.
- **Phonons (DFPT).** 'IBRION = 5' and 'LEPSILON = .TRUE.'
  invokes density-functional perturbation theory
  (DFPT) for the dynamical matrix. Required for IR
  intensities (Born effective charges from `LEPSILON`),
  and much faster than finite differences on a
  non-metallic system. Output: `OUTCAR`' contains the
  dynamical matrix at Γ; the full dispersion requires a
  supercell with 'PHON_NSTRUCT' and the 'PHON_CALCPATH'
  block in the `INCAR`.
- **Nudged elastic band (NEB).** `IBRION = 3' (NEB) or
  'IBRION = 1' with 'ICHAIN = 0' and `IOPT = 1' runs a
  NEB transition-state search. The initial and final
  images are read from 'POSCAR' and 'CONTCAR`; the
  intermediate images are specified in `POSCAR`' with the
  `Selective dynamics' tag. The climbing-image variant
  ('LCLIMB = .TRUE.') gives a more accurate saddle point
  at the cost of a slower NEB convergence.
- **Dimer method.** 'IBRION = 3' with 'ICHAIN = 0' and
  `IOPT = 3' runs the dimer method for a saddle-point
  search from a single initial configuration. The output
  is a `CONTCAR`' corresponding to the saddle point;
  frequency analysis (`NWRITE = 2' and a finite-difference
  follow-up) confirms a single imaginary mode.
- **$G_0W_0$ and BSE.** Set 'ALGO = GW'; requires a
  converged PBE / HSE06 starting point. The standard
  workflow is (i) PBE SCF, (ii) HSE06 SCF (or PBE0),
  (iii) $G_0W_0$ on top, (iv) BSE for optical absorption.
  The number of bands (`NBANDS`) must be increased to
  include all unoccupied states that contribute to the
  self-energy (typically 5–10× the number of occupied
  bands). The `vasp_gw`' executable is required.

### 1.7 Worked example — band structure of Si with HSE06

A complete workflow: PBE SCF → HSE06 SCF → HSE06 band
structure along Γ–X–W–K–Γ–L. The PBE step is the
"warm-up"; the HSE06 step is where the band gap opens up
to the experimental 1.12 eV (PBE gives 0.6 eV; HSE06
gives 1.13 eV).

**Step 1 — PBE SCF** (`INCAR.PBE`):

```bash
# INCAR
SYSTEM = Si PBE SCF
ENCUT  = 500
EDIFF  = 1.0e-5
ISMEAR = 0
SIGMA  = 0.05
IBRION = -1
LCHARG = .TRUE.     # write CHGCAR for HSE
LWAVE  = .TRUE.     # write WAVECAR for HSE
LREAL  = .FALSE.
```

`KPOINTS`, `POSCAR`, `POTCAR`' are as in the Si band
structure example in the cheatsheet
([§10.2]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})).
Run on 8 cores:

```bash
mpirun -n 8 vasp_std
```

**Step 2 — HSE06 SCF** (`INCAR.HSE`): identical to the PBE
INCAR with the following changes:

```bash
LHFCALC  = .TRUE.
HFSCREEN = 0.2           # HSE06 screening, 1/Angstrom
AEXX     = 0.25          # exact-exchange mixing
ALGO     = Damped        # robust SCF algorithm for hybrids
TIME     = 0.4           # damping parameter
PRECFOCK = Normal        # FFT grid for the exact exchange
EDIFF    = 1.0e-5        # tighter than PBE
```

Run again on 8 cores (HSE06 is ~ 100× slower than PBE on
this system):

```bash
mpirun -n 8 vasp_std
```

The HSE06 SCF starts from the PBE `CHGCAR`' (if present,
which is why `LCHARG = .TRUE.' in step 1). Convergence
typically takes 15–25 iterations; check the
'free energy' column in 'OUTCAR' for the convergence.

**Step 3 — HSE06 bands** (`INCAR.bands`): same
`POTCAR`, but a new `KPOINTS`' in line mode (a k-point
path instead of a uniform mesh):

```bash
# KPOINTS (line-mode k-path)
K-Path
6
0.0   0.0    0.0    ! Gamma
0.5   0.0    0.5    ! X
0.5   0.25   0.75   ! W
0.375 0.375  0.375  ! K
0.0   0.0    0.0    ! Gamma
0.5   0.5    0.5    ! L
```

The bands `INCAR`:

```bash
LHFCALC  = .TRUE.
HFSCREEN = 0.2
AEXX     = 0.25
ALGO     = Normal        # or 'Eigenvalue' (faster for the NSCF step)
ICHARG   = 11            # read CHGCAR, do not update
LWAVE    = .FALSE.
LCHARG   = .FALSE.
EDIFF    = 1.0e-6
NBANDS   = 16            # >= 8 (Si has 8 valence electrons in 2-atom cell)
```

Run:

```bash
mpirun -n 8 vasp_std
```

The eigenvalues are in `EIGENVAL`. To plot:

```bash
# Use pymatgen, sumo, or a custom script
python -c "
from pymatgen.io.vasp import Vasprun
v = Vasprun('vasprun.xml')
bs = v.get_band_structure()
bs.plot_brillouin()
"
```

The expected HSE06 band gap of Si is 1.13 eV; the VBM is
at Γ, the CBM is at X (a quasi-direct gap with the
indirect 1.13 eV and a direct gap of ~ 3.4 eV at Γ).
The total energy of the HSE06 calculation should be
~ 0.5 eV/atom lower than the PBE total energy (the
typical HSE06 vs. PBE difference for Si).

---

## 2. Quantum ESPRESSO

### 2.1 Overview

Quantum ESPRESSO (QE) is the de facto **open-source**
plane-wave DFT code, distributed under the GPL and
maintained by an international consortium. It is the
open-source counterpart to VASP for solid-state DFT and is
the workhorse of *academi`c*' solid-state physics, with a
particularly deep **phonon** implementation (DFPT and
finite-difference) and a mature `G_0W_0`' / BSE ecosystem
through the 'Yambo' and 'West' post-processors. The name
is an acronym: "opEn Source Package for Research in
Electronic Structure, Simulation, and Optimisation".
Unlike VASP, QE ships as a collection of independent
executables (`pw.x`, `ph.x`, `neb.x`, `pp.x`, `bands.x`,
`dos.x`, `projwfc.x`, `ppacf.x`, `matdyn.x`, `q2r.x`,
`pw2gw.x`, `turboTDDFT.x`, ...) — each does one
job, and the user scripts the workflow by piping the
outputs of one executable into the inputs of the
next. The consequence is that the user has a much
more *transparent* view of what the code is doing:
every intermediate file is text and can be
inspected. The cost is a steeper learning curve than
VASP's, and the user-written scripts are not always
short.

### 2.2 Install

QE is built with the standard GNU autotools
('/configure && make'). The dependencies are: a Fortran
2003 compiler (gfortran ≥ 7, ifort, AMD flang, or
nvfortran), an MPI library (openmpi, mpich, Intel MPI),
BLAS / LAPACK / ScaLAPACK, an FFT library (FFTW3 or
Intel MKL), and (for many modern functionals) the
`libxc`' library. The total build takes 30–90 minutes on
a modern machine.

```bash
# Clone the latest stable release
git clone -b qe-7.4 <https://gitlab.com/QEF/q-e.git> qe
cd qe

# Configure for MPI + OpenMP + CUDA (NVIDIA GPUs)
./configure --enable-parallel --enable-openmp \
            --with-cuda=/usr/local/cuda \
            --with-scalapack=intel \
            BLAS_LIBS="-mkl" LAPACK_LIBS="-mkl" \
            FFT_LIBS="-mkl"

# Build all executables
make -j 16 pw pp ph neb cp ld1 upftools

# Verify
./bin/pw.x -h | head -10
```

The executables end up in `./bin/`. The `pseudo/' folder
contains the standard pseudopotential library (the
PSLibrary, the SG15 ONCV, the UPF format). The "Pseudo
Dojo" (`<https://www.pseudo-dojo.org/`>) is a recommended
alternative.

### 2.3 Input file template — H₂O in a box

The smallest QE input that produces a sensible H₂O
single-point energy. The input format is **Fortran
namelist**: each section starts with `&NAME' and ends with
`/`.

```fortran
! h2o.scf.in
&CONTROL
    calculation = 'scf'        ! 'scf' | 'relax' | 'vc-relax' | 'bands' | 'nscf' | 'md' | 'vc-md'
    prefix      = 'h2o'        ! base name for output files
    outdir      = './tmp/'     ! scratch directory (MUST exist)
    pseudo_dir  = './pseudo/'  ! directory containing *.UPF pseudopotentials
    verbosity   = 'low'        ! 'low' | 'high' | 'debug'
/
&SYSTEM
    ibrav   = 0                ! 0 = free-format (CELL_PARAMETERS / ATOMIC_POSITIONS below)
    nat     = 3
    ntyp    = 2
    ecutwfc = 30.0             ! plane-wave cutoff for wavefunctions, Ry
    ecutrho = 240.0            ! charge-density cutoff, Ry
                              !  >= 4*ecutwfc for norm-conserving
                              !  >= 8-12*ecutwfc for USPP / PAW
    nbnd    = 8                ! >= number of occupied bands (H2O: 8 valence e-)
/
&ELECTRONS
    conv_thr = 1.0d-8          ! SCF convergence threshold, Ry
    mixing_beta = 0.7          ! charge-density mixing (0.7 is robust default)
/
ATOMIC_SPECIES
  O  15.999  O.upf            ! element, atomic mass, pseudopotential file
  H  1.008   H.upf
ATOMIC_POSITIONS angstrom
  O  0.000  0.000  0.000
  H  0.957  0.000  0.000
  H -0.240  0.927  0.000
K_POINTS gamma                ! Gamma-only: 1 k-point (molecule in a box)
CELL_PARAMETERS angstrom
   10.0   0.0   0.0
    0.0  10.0   0.0
    0.0   0.0  10.0
```

To run on 4 cores:

```bash
mpirun -n 4 pw.x -in h2o.scf.in > h2o.scf.out
```

The total energy (in Rydberg!) is in `h2o.scf.out' after
the line '!    total energy':

```bash
$ grep "total energy" h2o.scf.out
!    total energy              =     -34.92658373 Ry
```

(Rydberg is QE's default energy unit. To convert to
eV, multiply by 13.6057. The PBE H₂O total energy is
~ -475.5 eV = -34.93 Ry.)

### 2.4 Convergence tests

QE convergence is structured around the same three
parameters as VASP (cutoff, k-mesh, smearing), but with
different defaults.

1. **Plane-wave cutoff (`ecutwfc`).** Sweep from 20 Ry
   to 80 Ry in steps of 5–10 Ry. Pick the smallest value
   at which the total energy changes by less than
   1 meV/atom. For norm-conserving pseudopotentials, the
   converged `ecutwfc`' is typically 30–60 Ry; for
   ultrasoft and PAW, 40–80 Ry. The `ecutrho`' should be
   `>= 4 * ecutwfc' for norm-conserving and
   `>= 8 * ecutwfc' (often 10–12) for USPP/PAW. The
   error from a too-small `ecutrho`' is *silent* — the
   SCF converges to a "wrong" total energy that is not
   variational.

2. **K-point sampling.** For a metal, use a Monkhorst–Pack
   mesh with `occupations = 'smearing'' and a Methfessel–
   Paxton smearing ('smearing = 'mp'', `degauss = 0.02'
   Ry). For an insulator, use `occupations = 'fixed''
   with a uniform mesh, or `occupations = 'tetrahedron''
   on a sufficiently dense mesh (≥ 4×4×4 on a primitive
   cell). For a molecule in a box, `K_POINTS gamma' is
   correct.

3. **Smearing.** For metals, never use
   `smearing = 'gaussian'' for production (it converges
   too slowly). Use `smearing = 'mp'' (Methfessel–Paxton,
   2nd order: `degauss = 0.02' Ry) for routine work, and
   `smearing = 'fd'' (Fermi–Dirac) for very high
   accuracy (extrapolate to 'T = 0'). The
   `smearing = 'tetrahedron'' integrator is the most
   accurate, but it requires a *uniform* mesh (no
   custom k-paths) and at least 4×4×4 points per
   primitive cell.

4. **SCF convergence (`conv_thr`).** The default
   `1.0d-6' Ry is too loose for production. Use
   '1.0d-8' for geometry optimisation, '1.0d-10' for
   final energies, and `1.0d-12' for phonons and
   response.

5. **Charge-density mixing.** The default
   `mixing_beta = 0.7' is robust. For difficult systems
   (transition-metal oxides with strong correlation),
   reduce to '0.2' and increase 'mixing_ndim = 12' (the
   Broyden history length). For metallic systems with
   charge sloshing, use `mixing_mode = 'local-TF''
   (Thomas–Fermi local mixer).

### 2.5 Common errors

| Error / symptom                                                                                | Likely cause                                                  | Fix                                                                                  |
|:-----------------------------------------------------------------------------------------------|:--------------------------------------------------------------|:-------------------------------------------------------------------------------------|
| 'cannot read namelist &CONTROL'                                                                | File not pure ASCII, missing slash, wrong case                | Check '&CONTROL' ... `/`; case-sensitive namelist names; no leading whitespace       |
| 'from pw_readfile : error opening pseudo file'                                                  | Wrong path in 'pseudo_dir', or filename mismatch              | Check 'pseudo_dir'; 'ls $pseudo_dir/H*.UPF'                                            |
| 'wrong number of electrons' / 'number of electrons is wrong'                                    | 'ecutwfc' too small for the chosen pseudopotential             | Increase 'ecutwfc'; check the UPF file's 'ecutwfc`/`ecutrho`' recommended cutoffs       |
| 'the system is metallic, you must use occupations = 'smearing''                                | 'occupations = 'fixed'' on a metal                            | Switch to 'smearing = 'mp'' or ''fd''                                                |
| 'cannot restart from previous run: charge not found'                                            | 'prefix' differs between 'pw.x' and 'bands.x', or 'outdir' was deleted | Keep the same 'prefix' and 'outdir' for the whole workflow; never delete `outdir`' mid-workflow |
| 'phonon died abnormally' in 'ph.x'                                                            | Too coarse k-mesh, or 'conv_thr' too loose                     | Increase 'K_POINTS' mesh; tighten 'conv_thr' to '1.0d-12'; check 'tr2_ph'             |
| 'neb.x: negative image distances, check initial configuration'                                 | Initial images too far from a smooth path; or one image has crossed another | Use 'path_thr = 0.1' (initial path smoother); use `IMAGE_DISTANCE`' to enforce a minimum spacing |
| 'error in routine write_rec'                                                                  | Disk full in 'outdir'                                          | Clean `outdir`; use a larger scratch partition                                        |
| 'k-point parallelism with k-point symmetry not yet supported'                                  | 'K_POINTS tpiba_b' (custom path) with 'KPAR > 1'              | Use 'KPAR = 1' for band structures, or use a uniform mesh                             |
| 'cutoff is not sufficient for the pseudopotential'                                              | 'ecutwfc' < the UPF file's recommended cutoff                 | Increase `ecutwfc`' to at least the recommended value; or use the SR.04 standard cutoffs |
| 'fatal error in cdiaghg: matrix not positive definite'                                         | Numerical issue with a 'mixing_mode = 'local-TF'' on an insulator | Switch to `mixing_mode = 'plain'' (default)                                            |
| 'neb.x: path is not continuous, image 5 has a large distance from neighbours'                   | Insufficient NEB images; or steep initial path                 | Add more images; use 'path_thr = 0.05' for a tighter initial path smoothing            |
| 'error in do_scf: too many iterations'                                                         | SCF not converging; or a bad initial guess                     | Add 'starting_magnetization(i)' for each species; use 'mixing_beta = 0.2'; `mixing_ndim = 12' |
| 'Hybrid: harris-functional weights too large'                                                  | Hybrid functional SCF oscillating; 'TIME' or 'mixing_beta' wrong | Use 'mixing_beta = 0.4' and `mixing_ndim = 16' for the first hybrid run; pre-converge at PBE first |

### 2.6 Advanced features

- **Hybrid functionals (HSE06, PBE0, SCAN0).** Add
  'input_dft = 'HSE'' to '&SYSTEM' for HSE06,
  'input_dft = 'PBE0'' for PBE0, and 'input_dft = 'SCAN0''
  for the SCAN0 hybrid. The exact-exchange mixing and
  screening length are controlled by `nqx1`, `nqx2`,
  `nqx3`' (the FFT grid for the exact exchange) and
  'exxdiv_treatment = 'gygi-baldereschi''. The hybrid
  SCF is ~50× slower than the PBE SCF; use
  'mixing_beta = 0.4' and 'mixing_ndim = 16' for the
  first SCF iterations and switch to `mixing_beta = 0.7'
  once the energy is on track.
- **DFT+U (Dudarev).** Add `lda_plus_u = .TRUE.' and
  'Hubbard_U(i)' for each species to '&SYSTEM`. For the
  Liechtenstein formulation, use
  'Hubbard_U(i)' and 'Hubbard_J(i)' per $(l, m)$.
  QE also supports DFT+U+V (inter-site $V$) for
  non-collinear magnetism with 'lda_plus_u_kind = 1'.
- **Spin–orbit coupling.** Add `noncolin = .TRUE.' and
  'lspinorb = .TRUE.' to '&SYSTEM`. The initial
  `starting_magnetization`' must be a 3-component vector
  per atom. For collinear SOC (spin quantisation along
  one axis), use 'lspinorb = .TRUE., noncolin = .FALSE.'.
  The second-variational SOC (more accurate, faster
  convergence) is on by default.
- **Van der Waals (D3, D4, TS, MBD).** QE does *not*
  ship D3 by default; use the `dftd3`' plugin via
  `&SYSTEM ... dftd3 = .TRUE.' (since QE 7.0). For
  older QE versions, use the `xtorch`' interface or
  post-process the energy with a standalone D3
  implementation. Tkatchenko–Scheffler (TS) is
  available as 'dft_ts = .TRUE.'; the
  many-body dispersion (MBD@rsSCS) is in the
  `MBD`' plugin.
- **Phonons (DFPT).** 'ph.x' with 'tr2_ph = 1.0d-12' on
  a non-metallic system. The standard workflow is
  (i) PBE SCF, (ii) `ph.x' at a 2×2×2 (or 4×4×4) q-mesh,
  (iii) `q2r.x' to Fourier-interpolate the force
  constants, (iv) `matdyn.x' to plot the dispersion.
  For metals, use 'ph.x' with 'ldisp = .TRUE.' and
  `nq1, nq2, nq3' to compute the full dispersion by
  finite differences (DFPT does not work for metals in
  QE).
- **Phonons (finite differences).** `ph.x' with
  'tr2_ph = 1.0d-12' and 'ldisp = .TRUE.' on a
  supercell. Slower than DFPT but works for metals.
- **Nudged elastic band (NEB).** `neb.x' with an
  input `neb.dat' listing the initial and final images
  and a list of intermediate atom positions. The
  `path_thr`' parameter controls the initial-path
  smoothing; the `CI_scheme`' parameter turns on the
  climbing-image NEB. The converged saddle point is in
  the output, and a frequency calculation
  (`ph.x' on the saddle-point configuration) confirms
  a single imaginary mode.
- **Dimer method.** `neb.x' with
  `CI_scheme = 'dimer'' for a saddle-point search from
  a single initial configuration.
- **$G_0W_0$ and BSE.** The QE ground state is
  post-processed by 'Yambo' (most common) or 'West'
  (largest systems, stochastic). The `pw2gw.x' utility
  converts the QE 'WAVECAR' ('save/' directory) into the
  format Yambo reads. The `pw4gw.x' utility does the
  same for West.
- **Ab-initio MD (BO and CP).** `pw.x' with
  `calculation = 'md'' is Born–Oppenheimer MD; the CP
  code (`cp.x`) is Car–Parrinello MD. The default is
  NVE; for NVT, add `&THERMOSTAT ... &END THERMOSTAT'
  with `THERMOSTAT = 'nose'' (Nose–Hoover) or
  `'langevin'`. For NPT, use the `CP`' code's variable-
  cell MD.

### 2.7 Worked example — Si phonon dispersion by DFPT

The QE phonon workflow is the most-used in the open-
source community. Steps: (i) PBE SCF, (ii) DFPT at
q = Γ on the conventional cell, (iii) DFPT on a 2×2×2
q-mesh on the primitive cell, (iv) `q2r.x' to Fourier-
interpolate, (v) `matdyn.x' to plot the dispersion.

**Step 1 — PBE SCF** (`si.scf.in`): see the cheatsheet
[§10.1]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}).
The "right" converged `ecutwfc`' for the SG15 ONCV
pseudopotential is 40 Ry; the converged k-mesh is
8×8×8. **Step 2 — DFPT at Γ** (`si.ph.Gamma.in`):

```fortran
&INPUTPH
    tr2_ph  = 1.0d-14         ! threshold on the dynamical matrix
    prefix  = 'si'
    outdir  = './tmp/'
    fildyn  = 'si.dyn.Gamma'  ! output: dynamical matrix at q = 0
    recover = .TRUE.          ! resume from a previous run
/
```

Run:

```bash
mpirun -n 4 ph.x -in si.ph.Gamma.in > si.ph.Gamma.out
```

**Step 3 — DFPT on a 2×2×2 q-mesh** (`si.ph.qmesh.in`):

```fortran
&INPUTPH
    tr2_ph  = 1.0d-14
    prefix  = 'si'
    outdir  = './tmp/'
    fildyn  = 'si.dyn'        ! output: dynamical matrices for all q-points
    recover = .TRUE.
    start_q = 1               ! first q-point
    last_q  = 8               ! last q-point (2x2x2 = 8 q-points)
/
```

Run:

```bash
mpirun -n 4 ph.x -in si.ph.qmesh.in > si.ph.qmesh.out
```

**Step 4 — Fourier-interpolation** (`si.q2r.in`):

```fortran
&INPUT
    fildyn  = 'si.dyn'
    flfrc   = 'si.fc'         ! output: real-space force constants
    zasr    = 'simple'        ! acoustic-sum rule
/
```

Run:

```bash
q2r.x -in si.q2r.in > si.q2r.out
```

**Step 5 — Plot the dispersion** (`si.matdyn.in`):

```fortran
&INPUT
    flfrc  = 'si.fc'
    flfrq  = 'si.freq'        ! output: phonon frequencies along the path
    q_in_cryst_coord = .TRUE.
/
8
0.0   0.0   0.0   30
0.5   0.0   0.5   30
0.5   0.25  0.75  30
0.375 0.375 0.375 30
0.0   0.0   0.0   30
0.5   0.5   0.5   30
```

Run:

```bash
matdyn.x -in si.matdyn.in > si.matdyn.out
```

The output `si.freq' has one row per q-point and one
column per mode. The expected phonon dispersion of Si
peaks at ~ 520 cm⁻¹ (the TO mode at Γ); the TA mode is
acoustic (linear in `q`) with the slope of sound.

For visualisation, convert `si.freq' to a plot with
`plotband.x' or a custom Python script.

---

## 3. ORCA

### 3.1 Overview

ORCA is a C++ quantum-chemistry program distributed
**free of charge for academic use** (commercial for
industry) by the group of Frank Neese at the Max Planck
Institute for Kohlenforschung. It is the workhorse of
*inorganic and organometalli`c*' quantum chemistry, with
particularly strong modules for:
- Broken-symmetry DFT for antiferromagnets
  ([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.8.5)
- Multi-reference methods: CASSCF, NEVPT2, MRCI
- High-accuracy coupled cluster: DLPNO-CCSD(T)
  (the canonical-accuracy "golden standard" on
  100-atom systems)
- Spectroscopy: UV/Vis, XAS, EPR, NMR, Mössbauer
- Geometry optimisation, NEB, transition-state search,
  IRC, ab-initio MD

ORCA is **not** a plane-wave code; it uses a Gaussian
basis ([chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.3) and
is a *molecular* code — no periodic boundary conditions
in the standard build (the standalone `ORCA - 3D'
extension adds PBC for solids, but the community
standard for periodic solids is VASP / QE / CP2K).
For a single transition-metal complex, a small molecule,
or a spectroscopic property, ORCA is the de facto
choice in the inorganic-chemistry community.

### 3.2 Install

ORCA is distributed as a single static binary
(`orca.x.x.x.tar.xz`) that contains the entire program.
There is no compilation step; just unpack the archive
and add the directory to the `PATH`. The license is the
"ORCA License Agreement" — a free annual registration for
academic groups. The build supports MPI parallelism
(OpenMPI / MPICH), OpenMP, and a separate GPU build
(NVIDIA CUDA).

```bash
# Download from the ORCA forum (login required)
wget <https://orcaforum.kofo.mpg.de/forum/.../orca_5_0_4_linux_x86-64.tar.xz>
tar -xf orca_5_0_4_linux_x86-64.tar.xz
 export PATH=/opt/orca_5_0_4_linux_x86-64:${PATH}
 export LD_LIBRARY_PATH=/opt/orca_5_0_4_linux_x86-64:${LD_LIBRARY_PATH}

# Verify
orca --version
```

Dependencies: an MPI library (optional, for
parallel runs), and (for some methods) the `libgfortran`'
and `libcblas`' shared libraries that ship with the
distribution.

### 3.3 Input file template — H₂O geometry optimisation

The ORCA input is a **free-format** keyword-value file.
The same input file drives all calculations: SCF,
geometry optimisation, frequency, NEB, MD. The keywords
are not case-sensitive; the input is interpreted as
"smart" — a geometry optimisation reads the `Opt`' flag
and dispatches accordingly.

```text
# h2o_opt.inp
! B3LYP def2-SVP Opt TightSCF TightOpt        # method, basis, job
# OR equivalently:
# ! B3LYP def2-SVP
# ! Opt
# ! TightSCF
# ! TightOpt

%maxcore 4096                                  # per-core memory, MB

* xyz 0 1                                       # charge, multiplicity
O   0.000  0.000  0.000
H   0.957  0.000  0.000
H  -0.240  0.927  0.000
*
```

To run on 4 cores:

```bash
$PATH/orca h2o_opt.inp > h2o_opt.out
```

ORCA produces a directory `h2o_opt/' with the input,
output, GBW (binary orbital file), and the converged
geometry (`h2o_opt.xyz`). The total energy (in Hartree!)
is in the output:

```bash
$ grep "FINAL SINGLE POINT ENERGY" h2o_opt.out
                 FINAL SINGLE POINT ENERGY     -76.43421088
```

### 3.4 Convergence tests

ORCA is a Gaussian-basis code, so the convergence tests
are different from the plane-wave codes above. The two
main convergence parameters are the **basis set size**
('def2-SVP' → 'def2-TZVP' → `def2-QZVP`) and the
**numerical integration grid** (`GridX`' where X is 1–9).
For most methods, the default grid is fine, but for
geometry optimisation and properties the convergence
should be checked.

1. **Basis-set convergence.** Sweep the basis from
   'def2-SVP' to 'def2-TZVP' to `def2-QZVP' and check
   the convergence of the property of interest. For a
   single-point energy, `def2-TZVP' is usually within
   0.1 mEh of `def2-QZVP`; for a geometry, `def2-TZVP'
   gives bond lengths within 0.001 Å of `def2-QZVP`.
   For high-accuracy reference calculations, the
   **complete basis set (CBS)** extrapolation uses
   'n^{-3}' for the HF energy and 'n^{-5}' for the
   correlation energy (Helgaker–Halkier), with `n = 3
   (TZ)' and 'n = 4 (QZ)'.

2. **Integration grid.** The default is `Grid4`' for
   geometry optimisation and `Grid5`' for final
   properties. For an inaccurate grid (e.g. `Grid1`),
   the SCF can show "numerical noise" in the energy
   that does not converge. For high-accuracy
   spectroscopy (NMR, EPR), use `Grid7`' and the
   "no-final-grid" trick (`UseFinalGridX`' in the SCF
   block).

3. **SCF convergence.** The default `TightSCF`' flag
   gives `1.0e-8' Eh. For difficult systems (open-shell
   TM, near-degeneracy), use 'VeryTightSCF' ('1.0e-10`).
   For SCF convergence problems:
   `SlowConv`, `SOSCF`, `DIIS`, and `KDIIS`' are
   available; for very difficult cases, the
   `TRAH`' (transformation-based accelerated Hartree–
   Fock) method is robust.

4. **RI / RIJCOSX approximation.** The "Resolution of
   the Identity" approximation (RI) and the
   "RI-J + chain-of-spheres exchange" (RIJCOSX)
   approximation are *muc`h*' faster than the full
   ERI evaluation, with an error of < 0.1 mEh for most
   properties. For hybrid DFT, use `RIJCOSX`; for pure
   GGA, use `RI`. The auxiliary basis is the
   'def2/J' basis; for 'def2-SVP' it is `def2/J`; for
   'def2-TZVP' it is 'def2/J'; for 'def2-QZVP' it is
   `def2/J`.

5. **Dispersion.** For non-covalent interactions, use
   the D3 or D4 corrections: `! D3BJ' for D3 with
   Becke–Johnson damping, `! D4' for the newer D4. These add an empirical pairwise (or many-body)
   term to the energy.

### 3.5 Common errors

| Error / symptom                                                                  | Likely cause                                                       | Fix                                                                                    |
|:---------------------------------------------------------------------------------|:-------------------------------------------------------------------|:---------------------------------------------------------------------------------------|
| 'ORCA finished with error: UNKNOWN_EXIT_SIGNAL'                                  | Out of memory                                                      | Increase '%maxcore`; or reduce the basis set; or split the calculation into segments    |
| 'SCF NOT CONVERGED after 125 iterations'                                         | Difficult SCF (TM, near-degeneracy, bad initial guess)            | Use 'SlowConv', 'SOSCF'; or 'KDIIS'; or specify initial 'MOs' via `%scf ... GuessMO'     |
| 'RI not set up, but RI required'                                                  | Forgot the auxiliary basis for a RI / RIJCOSX calculation          | Add '! def2/J' or use `%basis ... AuxJ "def2/J" ... end'                                |
| `BASIS SET NOT FOUND: def2-QZVPPD'                                                | The basis set file is missing; or the ORCA version is too old     | Upgrade ORCA (≥ 5.0 has the full def2 family); or check the basis set table             |
| 'Aborting: too many negative frequencies' (geometry optim)                      | Saddle point found instead of minimum; or the SCF did not converge | Use 'Opt' (not `OptTS`); add `AnFreq`' (numerical frequency at the converged geometry)  |
| 'TDDFT EXCITED STATE X: convergence failed'                                     | State too high in energy; or the SCF is not tight enough          | Use 'TightSCF'; or use 'DoLamp' for the TDDFT iterations; or reduce the number of roots |
| `NEVPT2: too many active electrons'                                              | CAS active space too large                                         | Reduce the active space; or use a smaller basis                                         |
| 'CPSCF: numerical instability'                                                   | SCF grid too coarse; or a very diffuse basis                       | Use a finer grid ('Grid6'); check the basis set; or use '! NoFrozencore' if ECP is set  |
| 'OUT OF MEMORY: cannot allocate ... MB'                                          | System too large for the available RAM                            | Use '%maxcore' with a larger value; or reduce the basis; or use the RI approximation    |
| `'The use of the 'Truhlar' grid is not implemented for this method''              | Mismatch between grid and method                                   | Use 'Grid4' (default) or `Grid5`; check the documentation for the specific method        |
| 'Aborting: level shift value too large for this method'                          | Default level shift too high for a hybrid functional               | Use '%scf ... LevelShift 0.0 end' and `SlowConv`; or use the `%method ... HFX_Storage ... end' block |
| 'NEVPT2 requires the IROOT flag'                                                 | NEVPT2 needs a state-specific calculation                          | Set '! NEVPT2' with 'IRoot' in the '%tddft' block; or use the `casscf`' module directly  |

### 3.6 Advanced features

- **Hybrid functionals.** All common hybrids are
  available: B3LYP ('! B3LYP'), PBE0 ('! PBE0'),
  TPSSh ('! TPSSh'), the range-separated hybrids
  `ωB97X-D3`, `ωB97X-V`, `ωB97M-V`, `CAM-B3LYP'
  ('! CAM-B3LYP'). For dispersion-corrected hybrid
  functionals, add `! D3BJ' (D3 with Becke–Johnson
  damping), '! D4' (D4), or '! NL' (the non-local
  Vydrov–Van Voorhis dispersion, used in
  `ωB97X-V`).
- **Double-hybrids.** The "double-hybrid" functionals
  (MP2 correlation on top of a hybrid exchange,
  [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.6) are
  available: B2PLYP ('! B2PLYP'), DSD-PBEP86
  ('! DSD-PBEP86'), ωB97X-2 ('! ωB97X-2'). These are
  slower than hybrids but more accurate for
  non-covalent interactions and thermochemistry.
- **CASSCF / NEVPT2.** The complete active space SCF
  (CASSCF) module is a full multi-reference method;
  NEVPT2 is the *n*-electron valence perturbation
  theory 2nd-order perturbation on top of CASSCF. The
  active space is specified in `%casscf ... nel = 6
  ... norb = 5 ... end' (6 electrons in 5 orbitals for
  the Cr(CO)₆ example below). The orbital optimisation
  is restarted if the CASSCF SCF does not converge.
- **DLPNO-CCSD(T).** The "domain-based local pair
  natural orbital" CCSD(T) method is ORCA's flagship
  high-accuracy method. It is the canonical-accuracy
  "golden standard" on 100-atom systems. The
  convergence is controlled by `TightPNO`' (default) and
  `NormalPNO`' (faster, less accurate). The
  `%mdci ... TCutPNO ... end' block controls the
  PNO cutoffs.
- **Spectroscopy: UV/Vis (TDDFT).** The TDDFT module
  is a standard "Casida" linear-response TDDFT
  ([chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }})). Specify
  '! TDDFT' with 'NRoots 50' (50 excited states) and
  `MaxDim 200' (the maximum subspace size). For
  spin-flip TDDFT (diradicals), use '! SF-TDDFT'.
- **Spectroscopy: EPR / NMR.** ORCA computes
  hyperfine coupling (EPR) and NMR chemical shifts via
  the `EPRNMR`' module. The input is
  '! EPRNMR' with 'NTrip' (triplet state for EPR) or
  `NAtoms`' (for NMR shielding). The output is the
  hyperfine tensor and the shielding tensor.
- **Spectroscopy: Mössbauer.** The Mössbauer isomer
  shift is computed via the `Mossbauer`' module. The
  reference isomer shift is fitted to experiment; the
  computed contact density is the "raw" output.
- **Mössbauer / EPR with SOC.** For 5$d$ and 4$f$
  systems, SOC is required for an accurate EPR / NMR /
  Mössbauer property. Use `! SOMF' (the
  spin-orbit mean-field integral approximation) or
  `! RI-SOMF' for the SOC treatment.
- **Geometry optimisation + NEB.** ORCA's NEB module
  ('! NEB-TS') is a full climbing-image NEB for
  transition-state search. The input is
  '! NEB-TS' with 'NImages 8' (8 images between the
  initial and final states). The converged saddle
  point is in the output.
- **Ab-initio MD.** ORCA's MD module supports
  Born–Oppenheimer MD with the same input format as
  the geometry optimisation. Use `! MD' with
  'TimeStep 0.5 fs' and 'NSteps 1000`. For a thermal
  initial condition, use '! MDINIT 300 K'.

### 3.7 Worked example — Cr(CO)₆ CASSCF + NEVPT2

The Cr(CO)₆ complex has a Cr⁰ in an octahedral field,
with 6 CO ligands. The relevant electronic structure is
the $d^6$ configuration of Cr⁰ in a $t_{2g}$ ground
state. A CASSCF(6,5) calculation (6 electrons in 5 $d$
orbitals) with NEVPT2 dynamic correlation gives a
spectrum that matches the experimental UV/Vis
absorption to within 0.1 eV.

**Step 1 — geometry optimisation at DFT:**

```text
! BP86 def2-TZVP Opt TightSCF TightOpt
! D3BJ                                     # Becke-Johnson-damped D3
%maxcore 4096
* xyz 0 1
Cr   0.000  0.000  0.000
C    1.918  0.000  0.000
C   -1.918  0.000  0.000
C    0.000  1.918  0.000
C    0.000 -1.918  0.000
C    0.000  0.000  1.918
C    0.000  0.000 -1.918
O    3.075  0.000  0.000
O   -3.075  0.000  0.000
O    0.000  3.075  0.000
O    0.000 -3.075  0.000
O    0.000  0.000  3.075
O    0.000  0.000 -3.075
*
```

Run on 8 cores:

```bash
$PATH/orca crco6_opt.inp > crco6_opt.out
```

**Step 2 — CASSCF(6,5) at the converged geometry:**

```text
! CASSCF(6,5) def2-TZVP TightSCF
! NEVPT2                                   # perturbative correction on top
%maxcore 4096

%casscf
  nel     6                                 # 6 electrons
  norb    5                                 # 5 orbitals
  mult    1                                 # singlet (low-spin Cr^0)
  nroots  5                                 # 5 singlet roots
  switchstep nr                             # orbital optimisation
end

* xyzfile 0 1 crco6_opt.xyz                 # read geometry from the DFT optimisation
```

Run on 8 cores:

```bash
$PATH/orca crco6_casscf.inp > crco6_casscf.out
```

The CASSCF SCF converges in 10–20 iterations; the output
gives the energies of the 5 singlet roots
(singlet-a, singlet-b, ...) and the orbital
composition.

**Step 3 — NEVPT2 correction:**

ORCA's `! NEVPT2' flag runs the NEVPT2 perturbation
automatically as a post-processing step. The output
gives the NEVPT2-corrected energies:

```bash
$ grep "NEVPT2" crco6_casscf.out
NEVPT2 energies:
   0    0.000 eV
   1    3.42 eV
   2    3.42 eV
   3    3.42 eV
   4    4.15 eV
```

The 3.42 eV transition matches the experimental
~ 3.4 eV (in toluene, with a polarisation-corrected
shift).

For an open-shell case (e.g. a TM complex with a
$S = 1$ ground state, like a Mn²⁺ octahedral complex),
change 'mult 1' to 'mult 3' (triplet) and the active
space to `(5, 5)' for the high-spin $d^5$ case.

---

## 4. GPAW

### 4.1 Overview

GPAW is a Python / C PAW code
([chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7) with three
modes of operation:

- **Real-space grid mode (default):** the wavefunctions
  are represented on a uniform or adaptive real-space
  grid (similar to Octopus). This is the default mode
  and is the most general.
- **Plane-wave mode:** the wavefunctions are represented
  on a plane-wave basis (similar to VASP / QE). This is
  the most accurate mode and is mandatory for $GW$ and
  BSE.
- **LCAO mode:** the wavefunctions are represented on a
  set of atom-centred numerical atomic orbitals, with
  the PAW solution projected onto the LCAO basis. This
  is the *fastest* mode and is the only mode that scales
  linearly in system size.

The defining feature of GPAW is the **Python front
en`d*`*: the entire calculator is accessible from a
Python script, and the standard interface is the
**ASE** ([Atomic Simulation Environment]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}) §9.1).
This makes GPAW the natural choice when the rest of
the workflow (structure generation, MD, machine
learning, plotting) is in Python. It is also the most
*user-friendly* of the PAW codes: a typical "geometry
optimisation + band structure + DOS" workflow fits in
20–30 lines of Python, with no input files to write
beyond the script itself.

### 4.2 Install

GPAW is distributed on **PyPI** and **conda-forge** as
a pre-built binary (for Linux, macOS, and Windows with
WSL). The dependencies are: Python ≥ 3.9, NumPy,
SciPy, ASE, BLAS, and a C / Cython compiler. The
optional dependencies are `libxc`' (for modern
functionals), `fftw3`' (for the plane-wave mode), and
the `spglib`' library (for space-group detection).

```bash
# Easiest: pip install (Linux + Python 3.9+)
pip install gpaw

# Verify
gpaw --version

# To get the PAW datasets (required!):
gpaw install-data ~/.gpaw_data

# Alternatively, conda-forge:
conda install -c conda-forge gpaw
```

For a *custom* build (e.g. to enable the CUDA GPU
support), clone the GitLab repository and compile
manually:

```bash
git clone <https://gitlab.com/gpaw/gpaw.git>
cd gpaw
python -m pip install -e .
```

### 4.3 Input file template — H₂O geometry optimisation in 15 lines

```python
# h2o_opt.py
from ase import Atoms
from gpaw import GPAW, PW

# 1. Build the structure
h2o = Atoms('OH2',
            positions=[(0, 0, 0), (0.957, 0, 0), (-0.240, 0.927, 0)])
h2o.center(vacuum=4.0)               # pad the cell

# 2. Set up the calculator (plane-wave mode for accuracy)
calc = GPAW(
    mode=PW(500),                     # plane-wave cutoff, eV
    xc='PBE',
    kpts=(1, 1, 1),                   # Gamma-only for a molecule
    convergence={'energy': 1.0e-6},   # eV per electron
    convergence={'forces': 0.02},    # eV / Angstrom
    txt='h2o.txt',
)

# 3. Run a geometry optimisation
from ase.optimize import BFGS
h2o.calc = calc
opt = BFGS(h2o, logfile='h2o.opt.log')
opt.run(fmax=0.02)                    # convergence criterion: max force

# 4. Print the result
print(f'Final energy: {h2o.get_potential_energy():.4f} eV')
print(f'Optimised geometry:')
print(h2o.get_positions())
```

Run on 4 cores:

```bash
mpiexec -n 4 gpaw python h2o_opt.py
```

The total energy is in eV (GPAW's default unit).
The output `h2o.txt' is the log file; the optimised
geometry is in the output of the script.

### 4.4 Convergence tests

GPAW's convergence is structured around three
parameters: the **plane-wave cutoff** (in PW mode), the
**real-space grid spacing** (in FD mode), and the
**k-point mesh** (for periodic systems). The
convergence recipes:

1. **Plane-wave cutoff (PW mode).** Sweep from 300 eV
   to 800 eV in steps of 50 eV, compute the total
   energy at the experimental geometry, and pick the
   smallest value at which the energy changes by less
   than 1 meV/atom. For a typical PBE calculation on a
   transition-metal oxide with the `0.9.x' PAW data, the
   converged cutoff is 400–600 eV.

2. **Real-space grid spacing (FD mode).** Sweep h*
   from 0.25 Å to 0.10 Å in steps of 0.025 Å. The
   energy converges *exponentially* in h* (the
   multi-grid solver is exact in the limit of 'h = 0'),
   so the convergence is much faster than for the
   plane-wave cutoff. The default `h = 0.2' Å is fine
   for routine work; for high-accuracy forces
   ('< 0.01' eV/Å), use 'h = 0.15' Å or smaller.

3. **LCAO basis (LCAO mode).** The default basis is
   `dzp`' (double-zeta with polarisation). For
   high-accuracy, use `tzp`' (triple-zeta). The
   convergence is checked by running a PW mode
   calculation as a reference and confirming that the
   LCAO energy matches to within the desired
   tolerance.

4. **K-point mesh.** Same as VASP / QE: sweep the
   mesh density, pick the smallest converged. For a
   typical Si 2-atom cell, an 8×8×8 mesh converges
   the total energy to 1 meV/atom.

5. **SCF convergence.** `convergence={'energy':
   1.0e-6}' (eV per electron) is the default. For
   high-accuracy, use `1.0e-8`. For response
   properties, use '1.0e-10' and a tighter 'density'
   convergence (the default `1.0e-12' is fine).

6. **PAW dataset version.** GPAW ships with the
   `gpaw-setups' package (PyPI). The default is the
   '0.9.x' series. Older '0.8.x' data should not be
   used for new work. For *all-electron* accuracy
   benchmarks, use the `0.10.x' data.

### 4.5 Common errors

| Error / symptom                                                          | Likely cause                                                       | Fix                                                                                  |
|:-------------------------------------------------------------------------|:-------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
| 'gpaw.setup.SetupError: No setup for element X'                          | PAW dataset for element X is missing                               | Run 'gpaw install-data ~/.gpaw_data'; or set the 'GPAW_SETUP_PATH' environment variable |
| 'RuntimeError: Eigensolver did not converge'                            | SCF not converging; or a difficult system                          | Use 'eigensolver='cg''; or increase 'maxiter'; or use 'mixer={'beta': 0.05}' for slow mixing |
| 'MemoryError: cannot allocate ... MB'                                    | System too large for the available RAM                              | Switch from 'PW' mode to 'LCAO' mode; or use 'nbands=...' to limit the number of bands |
| 'ValueError: kpts=(1, 1, 1) for a periodic system'                       | Used Gamma-only for a metallic or large-gap periodic system        | Increase 'kpts' to (8, 8, 8) or denser                                                |
| 'gpaw.utilities.gpaw_error: Boundary conditions not implemented for this lattice' | Triclinic cell with 'PW' mode and a non-zero `k`-point            | Use 'PW' mode with 'fft2d=False'; or use 'FD' mode (handles all cell shapes)            |
| 'gpaw.eigensolvers.RMM_DIISError: ...'                                  | SCF stuck; 'eigensolver='rmm-diis'' is unstable for the system     | Switch to 'eigensolver='cg'' or ''lcao'`; or use a different initial magnetic moment  |
| 'The fixed_density() call requires mode='all' in the .gpw file'          | The '.gpw' file from the SCF was written with 'mode='wavefunctions'' | Re-write the SCF with 'calc.write('si.gpw', mode='all')'                              |
| 'numpy.AxisError: axis 3 is out of bounds for array of dimension 3'     | Old GPAW and new ASE version mismatch                               | Pin ASE version: 'pip install ase==3.22.0'                                            |
| 'gpaw.occupations.OccupationError: ...'                                  | Fermi–Dirac smearing with 'occupations=FermiDirac' and metallic    | Use 'occupations={'name': 'fermi-dirac', 'width': 0.05}'; or `occupations={'name': 'methfessel-paxton', 'order': 1, 'width': 0.05}' |
| `'PW mode does not support the requested 'xc=' functional''                | Functional not available in the pre-compiled GPAW                  | Use the 'libxc' name: 'xc='PBE'' is 'xc='LDA_X+LDA_C_PW''; or install GPAW from source with 'libxc' enabled |
| 'gpaw.lcao.LCAO error: LCAO setup not found for element X'               | Missing PAW dataset for the LCAO mode                              | Run 'gpaw install-data`; or use a different PAW version                                |

### 4.6 Advanced features

- **Real-time TDDFT.** `propagate(...)' from the
  calculator's TDDFT module. The standard workflow is
  (i) ground-state SCF, (ii) kick the system with a
  small electric-field pulse, (iii) propagate the
  Kohn–Sham orbitals in time, (iv) compute the
  time-dependent dipole moment, (v) Fourier-transform
  to the optical absorption spectrum. The
  `GPAW(...).tddft().propagate(...)' API is integrated
  with the rest of the Python workflow.
- **Linear-response TDDFT (Casida).** The `Casida`'
  post-processing gives the full excited-state
  spectrum (eigenvalues + oscillator strengths) on top
  of a converged ground state. The setup is
  `GPAW(...).diagonalize_full_hamiltonian()' followed
  by `GPAW(...).calculate_kschem()`.
- **$G_0W_0$ and BSE.** The plane-wave mode supports
  $G_0W_0$ via the `G0W0`' calculator. The BSE
  (Bethe–Salpeter equation) is implemented in the
  `BSE`' module. Both are in active development; the
  user community is small but active.
- **DFT+U.** Set `setup={'X': 'PBE+s'}' for the
  Dudarev DFT+U
  ([chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }})). The
  'X' is the atomic number. The 'U' value is
  specified in the setup dictionary.
- **Spin–orbit coupling.** Set `soc=True' in the
  calculator (GPAW switches to non-collinear
  automatically). SOC is only supported in the PW mode
  and the FD mode. For a band structure with SOC, the
  `band_structure()' method returns the SOC-split
  bands.
- **Delta-SCF.** The `deltaSCF`' module computes
  excited-state energies by enforcing a non-Aufbau
  occupation in the SCF. Useful for Hubbard-corrected
  calculations of charge-transfer excitations.
- **NEB and dimer.** The NEB module is integrated with
  ASE: 'from ase.neb import NEB'. The climbing-image
  NEB is 'climb=True' in the 'NEB' constructor. The
  dimer method is `from ase.dimer import Dimer' and
  `DimerRun`.

### 4.7 Worked example — Si band structure in 20 lines

A complete Si band structure with the plane-wave mode
in 20 lines of Python.

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

# 4. Extract and plot the band structure
bs = calc.band_structure()
bs.plot(filename='si.bands.png', emax=15)  # one line for the plot
```

Run:

```bash
mpiexec -n 8 gpaw python si_bands.py
```

The output `si.bands.png' is a publication-quality
band-structure plot with the high-symmetry points
labelled.

For a band structure with HSE06, change `xc='PBE'' to
`xc='HSE06'`. The HSE06 SCF is ~ 100× slower than PBE,
so the wall-time increases correspondingly. The
`fixed_density()' call re-uses the HSE06 density for the
NSCF band structure.

For a TDDFT calculation, the standard workflow is:

```python
from gpaw.tddft import photoabsorption
spectrum = photoabsorption('si.gpw', 'si.td.log',
                          e_min=0.0, e_max=10.0,
                          delta_e=0.05,                        # eV
                          kick_strength=1.0e-3)                # a.u.
spectrum[:].plot('si.td.png')
```

The `photoabsorption`' function runs a real-time TDDFT
calculation with a delta-function electric-field kick
at 't = 0', propagates the Kohn–Sham orbitals, computes
the time-dependent dipole, and Fourier-transforms to
the optical absorption spectrum. The output
'spectrum' is a 'Spectrum' object with the absorption
cross-section as a function of energy.

---

## 5. CP2K

### 5.1 Overview

CP2K is a Fortran mixed Gaussian / plane-wave (GPW)
code
([chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.3, §6.7). The
Gaussian basis handles the wavefunctions; the plane-
wave auxiliary grid handles the density and the
electron-repulsion integrals. The advantage of this
mixed basis is that it is **systematically-improvable**
(the Gaussian basis and the plane-wave cutoff are
independent convergence parameters) and **fast for
inhomogeneous systems** (the plane-wave grid adapts
locally). The cost is the complexity of the
convergence — the user must converge *two* parameters
(the Gaussian basis and the plane-wave cutoff) and
*three* SCF parameters (`EPS_SCF`, the OT minimiser,
the preconditioner).

CP2K's flagship application is **ab-initio molecular
dynamics** of large systems (water, electrolytes,
solid–liquid interfaces, MOFs with diffusing ions). A
1000-atom water simulation on a desktop workstation is
a routine calculation; a 10,000-atom electrolyte is
tractable on a small cluster. CP2K also has a
growing set of static-DFT features: geometry
optimisation, NEB, phonons, hybrid functionals
(within the GPW formulation, with truncated Coulomb
for HSE06), DFT+U, MP2, RPA, and $G_0W_0$.

### 5.2 Install

CP2K is distributed as a single `cp2k.ssmp' (serial),
'cp2k.psmp' (MPI / OpenMP), or 'cp2k.popt' (OpenMP)
executable, with a toolchain script that downloads and
compiles all the dependencies (BLAS, LAPACK, ScaLAPACK,
FFTW3, libint, libxc, libxsmm, ...). The build takes
1–3 hours on a modern machine.

```bash
# Clone and build
git clone --recursive -b support/v2024.3 \
    <https://github.com/cp2k/cp2k.git> cp2k
cd cp2k/tools/toolchain
./install_toolchain.sh                       # ~ 30 minutes
cd ../..
make -j 16 ARCH=local VERSION=psmp            # MPI + OpenMP

# Verify
./bin/local/cp2k.psmp --version
```

The dependencies are: GCC ≥ 9, MPI, BLAS / LAPACK /
ScaLAPACK, FFTW3, libint (for ERIs), libxc (for
modern functionals), libxsmm (for the matrix
multiplications), and CUDA (for GPU support).

### 5.3 Input file template — H₂O geometry optimisation

```fortran
! h2o.inp
&GLOBAL
  PROJECT       h2o
  RUN_TYPE      GEO_OPT
  PRINT_LEVEL   MEDIUM
&END GLOBAL

&MOTION
  &GEO_OPT
    TYPE        MINIMIZATION
    OPTIMIZER   BFGS
    MAX_ITER    100
    MAX_FORCE   1.0E-03                    ! Hartree / Bohr
  &END GEO_OPT
&END MOTION

&FORCE_EVAL
  METHOD QUICKSTEP
  &DFT
    BASIS_SET_FILE_NAME  BASIS_MOLOPT
    POTENTIAL_FILE_NAME  GTH_POTENTIALS
    CHARGE 0
    MULTIPLICITY 1
    &QS
      EPS_DEFAULT 1.0E-12                  ! orbital basis
    &END QS
    &POISSON
      PERIODIC NONE
      PSOLVER  MT                          ! Martyna-Tuckerman (isolated)
    &END POISSON
    &MGRID
      CUTOFF 300                           ! plane-wave cutoff, Ry
      REL_CUTOFF 50                        ! 50-100 Ry for the Gaussian density
    &END MGRID
    &SCF
      MAX_SCF 50
      EPS_SCF 1.0E-6
      SCF_GUESS ATOMIC
    &END SCF
    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC
  &END DFT
  &SUBSYS
    &CELL
      ABC 6.0 6.0 6.0
      PERIODIC NONE
    &END CELL
    &COORD
      O   0.000  0.000  0.000
      H   0.957  0.000  0.000
      H  -0.240  0.927  0.000
    &END COORD
    &KIND O
      BASIS_SET DZVP-MOLOPT-GTH
      POTENTIAL GTH-PBE-q6
    &END KIND
    &KIND H
      BASIS_SET DZVP-MOLOPT-GTH
      POTENTIAL GTH-PBE-q1
    &END KIND
  &END SUBSYS
&END FORCE_EVAL
```

To run on 4 cores:

```bash
mpiexec -n 4 cp2k.psmp -i h2o.inp -o h2o.out
```

The total energy (in Hartree!) is in `h2o.out' after:

```bash
$ grep "Total FORCE_EVAL" h2o.out
 ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.):      -17.2153
```

(For PBE on H₂O, the experimental geometry gives
~ -17.21 Eh = -468.5 eV; this matches the CP2K PBE
value with the DZVP-MOLOPT-GTH basis and the GTH-PBE
pseudopotential.)

### 5.4 Convergence tests

CP2K's convergence is structured around three
parameters: the **Gaussian basis set**, the
**plane-wave cutoff** ('CUTOFF' in '&MGRID`), and the
**relative cutoff** ('REL_CUTOFF' in '&MGRID`). The
convergence recipes:

1. **Gaussian basis set.** The MOLOPT family is the
   recommended choice: `DZVP-MOLOPT-GTH' (double-zeta
   with polarisation), `TZV2P-MOLOPT-GTH' (triple-zeta
   with two polarisation functions), and
   `QZV2P-MOLOPT-GTH' (quadruple-zeta). For a quick
   check, `DZVP-MOLOPT-GTH' is fine; for production
   geometries and energies, `TZV2P-MOLOPT-GTH' is the
   default. For high-accuracy reference calculations,
   `QZV2P-MOLOPT-GTH`.

2. **Plane-wave cutoff (`CUTOFF`).** Sweep from 200 Ry
   to 1000 Ry in steps of 50 Ry. Pick the smallest
   value at which the total energy changes by less
   than 1 meV/atom. For `DZVP-MOLOPT-GTH`, the
   converged `CUTOFF`' is 300–400 Ry; for
   `TZV2P-MOLOPT-GTH`, 500–700 Ry; for
   `QZV2P-MOLOPT-GTH`, 800–1000 Ry.

3. **Relative cutoff (`REL_CUTOFF`).** The `REL_CUTOFF`'
   is the cutoff for the *auxiliary* density (the
   Gaussian density expanded in plane waves). The
   default is 50 Ry, but for high-accuracy work,
   increase to 60–100 Ry. The energy converges
   *muc'h*' faster in 'REL_CUTOFF' than in `CUTOFF`.

4. **SCF convergence.** The default `EPS_SCF = 1.0E-6'
   is too loose for production. Use `1.0E-7' for
   routine geometry optimisation and `1.0E-8' for
   final energies and properties. For difficult
   systems (transition-metal oxides, mid-gap states),
   use `OT`' (the orbital transformation solver) with
   `PRECONDITIONER FULL_SINGLE_INVERSE' and
   'MINIMIZER DIIS'.

5. **OT solver for large systems.** The diagonalisation
   solver scales as `O(N³)' in the system size; the
   OT (orbital transformation) solver scales as
   'O(N²)' to 'O(N)' (with the right preconditioner).
   For systems with more than ~ 500 atoms, the OT
   solver is the only option.

6. **MD timestep.** The default 0.5 fs is safe for
   water with PBE. For H–H bonds or fast stretches,
   use 0.25 fs or smaller. For constant-temperature
   NVT, the thermostat relaxation time (the
   'TIMECON' in the '&NOSE' block) should be ~ 10×
   the timestep (e.g. `TIMECON 1000 fs' for a
   'TIMESTEP 0.5 fs').

### 5.5 Common errors

| Error / symptom                                                                | Likely cause                                                          | Fix                                                                                  |
|:-------------------------------------------------------------------------------|:----------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
| 'CUTOFF is too small for the chosen basis'                                     | 'CUTOFF' < the basis's recommended cutoff                             | Increase `CUTOFF`; check the `data/BASIS_MOLOPT' file                                 |
| 'OT minimizer did not converge'                                                | Bad SCF initial guess; or system with a gap closing                    | Use 'SCF_GUESS ATOMIC' (or `RESTART`); add `&OT ... PRECONDITIONER FULL_SINGLE_INVERSE ... end' |
| 'MGRID CUTOFF must be a multiple of ...'                                      | 'CUTOFF' not a multiple of the FFT grid size                           | Set `CUTOFF`' to a multiple of the recommended cutoff; or use the standard MOLOPT cutoffs  |
| 'POISSON solver MT: box too small'                                              | '&CELL ABC ...' too small for the molecule with the MT solver         | Increase the cell size; or use 'PSOLVER PERIODIC' with 'PERIODIC XYZ'                |
| 'KIND section: BASIS_SET ... not found'                                        | Basis set file is not in the path                                     | Check 'BASIS_SET_FILE_NAME'; check that the file 'BASIS_MOLOPT' is in the directory   |
| 'KIND section: POTENTIAL ... not found'                                        | Pseudopotential file is not in the path                               | Check 'POTENTIAL_FILE_NAME'; check that the file 'GTH_POTENTIALS' is in the directory   |
| 'MGRID: cell too small for the chosen CUTOFF'                                  | Cell too small for the plane-wave grid to be defined                    | Increase the cell; or decrease 'CUTOFF'                                              |
| 'neighbour list overflow'                                                      | Cell too small for a periodic calculation                              | Increase the vacuum in the cell; or use 'PSOLVER PERIODIC'                            |
| 'SCF did not converge in MAX_SCF iterations'                                   | SCF oscillating; or bad initial guess                                  | Use 'OT' solver; or restart from a converged run; or use `SCF_GUESS HISTORY'          |
| 'MD: cannot read frame'                                                         | Restart file '*.restart' is corrupt or missing                         | Re-run from scratch; or use `EXT_RESTART`' with a valid restart file                   |
| 'NEB: number of images does not match'                                          | Inconsistent number of images between the input and the restart        | Use 'BAND_TYPE IT-NEB' with `NUMBER_OF_REPLICA N' matching the input                  |
| 'HSE06 requires CUTOFF > 500 Ry'                                                | HSE06 hybrid needs a higher plane-wave cutoff than semilocal DFT       | Increase 'CUTOFF' to 600–1000 Ry                                                       |
| 'GTH pseudopotential does not match the basis set'                              | Mismatched GTH pseudopotential and MOLOPT basis                        | Use the matched pair (e.g. 'DZVP-MOLOPT-GTH' with `GTH-PBE-q6`)                       |
| 'K-point sampling is not implemented for this lattice'                        | Non-orthogonal lattice with 'KPOINTS'                                  | Use `KPOINTS SCHEME MONKHORST-PACK N1 N2 N3 0 0 0' only for orthorhombic cells         |
| 'OPTIMIZER BFGS: line search failed'                                            | Force convergence criterion too tight; or a difficult geometry         | Loosen 'MAX_FORCE'; or switch to 'CG' optimiser                                       |

### 5.6 Advanced features

- **OT solver (Orbital Transformation).** Switch
  '&SCF ... &END SCF' to '&SCF ... &OT ... &END OT
  &END SCF`. The OT solver is the recommended
  choice for systems with more than ~ 500 atoms. The
  'MINIMIZER' can be 'DIIS' (default), `CG`' (conjugate
  gradient), or `SD`' (steepest descent). The
  `PRECONDITIONER`' is the most important parameter:
  `FULL_SINGLE_INVERSE`' is the most robust default;
  `FULL_KINETIC`' is faster but less robust.
- **Hybrid functionals (HSE06, PBE0).** Add
  `&XC ... &HF ... &END HF &END XC' with
  `&HF ... FRACTION 0.25 ... &END HF' for PBE0, or
  with `&SCREENING ... &END SCREENING' for HSE06. The HSE06 calculation in CP2K uses a *truncated
  Coulom'b*' kernel — the '&SCREENING ... &END SCREENING'
  block specifies the screening length (0.2 Å⁻¹ for
  HSE06). The cost is ~ 50× that of semilocal DFT; the
  `CUTOFF`' must be increased to 600–1000 Ry.
- **DFT+U.** Add
  `&DFT ... &PLUS_U ... &END PLUS_U ... &END DFT'
  with `&PLUS_U ... &END PLUS_U' per species. The
  `L`, `U`, and `J`' parameters are specified per
  species. The Dudarev formulation is the default
  (the `U_eff = U - J' is the effective parameter).
- **MP2 and RPA.** Add `METHOD QUICKSTEP' with
  `&DFT ... &WF_CORRELATION ... &END WF_CORRELATION
  &END DFT' and 'METHOD MP2' (or 'METHOD RPA`).
  The MP2 calculation scales as `O(N⁵)`; the RPA scales
  as `O(N⁶)`. The output is the MP2 / RPA correlation
  energy on top of a converged PBE / PBE0 ground
  state.
- **$G_0W_0$ and BSE.** Available via the
  'METHOD GW' and 'METHOD BSE' blocks. The GW
  calculation is similar in scope to the `West`' /
  `Yambo`' implementations on top of QE / VASP.
- **Dispersion (D3, D4, TS, MBD).** Add
  `&XC ... &VDW_POTENTIAL ... &END VDW_POTENTIAL
  &END XC' with `POTENTIAL_TYPE PAIR_POTENTIAL' and
  `PARAMETER_FILE_NAME dftd3.dat' for D3, or
  `POTENTIAL_TYPE NON_LOCAL' for the
  many-body dispersion (MBD@rsSCS).
- **NEB and dimer.** The NEB module is invoked with
  'RUN_TYPE BAND' and a '&MOTION ... &BAND ... &END
  BAND &END MOTION' block. The `BAND_TYPE`' can be
  'IT-NEB' (improved tangent NEB), 'CI-NEB'
  (climbing image NEB), or `DIMER`. The output is the
  converged NEB trajectory; a frequency calculation on
  the saddle-point image confirms a single imaginary
  mode.
- **Metadynamics (PLUMED).** The `RUN_TYPE MD' with
  `&MOTION ... &MD ... &END MD &END MOTION' and the
  PLUMED interface for enhanced-sampling. PLUMED
  is loaded as a runtime library.
- **Ab-initio MD (NVE, NVT, NPT).** `RUN_TYPE MD'
  with the '&MD' block. 'ENSEMBLE NVE' (default),
  `NVT`' (Nose–Hoover, CSVR, or GLE thermostat), or
  `NPT`' (variable-cell MD with the Andersen or
  Martyna–Tobias–Klein barostat). The timestep is
  `TIMESTEP 0.5 fs' (default); for H–H bonds, use
  '0.25 fs'.

### 5.7 Worked example — NEB of H diffusion on Pt(111)

The H diffusion on Pt(111) is a textbook surface
science problem: H adsorbs on the *fc`c*' hollow site,
diffuses to the neighbouring *hc`p*' hollow site via a
*bridge* transition state. The activation energy is
~ 0.1 eV (PBE) — small enough that the diffusion is
fast at room temperature. This example is the
canonical "I want to test my NEB setup" calculation.

**Step 1 — initial and final geometries** (single-point
energies on the two endpoints):

```fortran
! pt111_h_fcc.inp
&GLOBAL
  PROJECT pt111_h_fcc
  RUN_TYPE GEO_OPT
&END GLOBAL
&FORCE_EVAL
  METHOD QUICKSTEP
  &DFT
    BASIS_SET_FILE_NAME  BASIS_MOLOPT
    POTENTIAL_FILE_NAME  GTH_POTENTIALS
    &POISSON PERIODIC XYZ PSOLVER PERIODIC &END POISSON
    &MGRID CUTOFF 400 REL_CUTOFF 60 &END MGRID
    &SCF MAX_SCF 50 EPS_SCF 1.0E-6 SCF_GUESS ATOMIC
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
    &CELL ABC 11.11 11.11 22.22 PERIODIC XYZ &END CELL
    ! Pt(111) surface: 3 layers, 4x4 supercell
    &TOPOLOGY COORD_FILE_NAME pt111_fcc.xyz COORD_FILE_FORMAT XYZ
      &CENTER_COORDINATES &END CENTER_COORDINATES
    &END TOPOLOGY
    &KIND Pt BASIS_SET DZVP-MOLOPT-SR-GTH POTENTIAL GTH-PBE-q10 &END KIND
    &KIND H  BASIS_SET DZVP-MOLOPT-GTH  POTENTIAL GTH-PBE-q1   &END KIND
  &END SUBSYS
&END FORCE_EVAL
```

(The `pt111_fcc.xyz' file contains the Pt(111) surface
with 48 Pt atoms and 1 H atom on the fcc hollow site.
The same XYZ with the H atom on the hcp hollow site is
the final image.)

**Step 2 — NEB calculation:**

```fortran
! pt111_h_neb.inp
&GLOBAL
  PROJECT pt111_h_neb
  RUN_TYPE BAND
&END GLOBAL
&MOTION
  &BAND
    BAND_TYPE CI-NEB                       ! climbing-image NEB
    NUMBER_OF_REPLICA 8                    ! 8 images between fcc and hcp
    K_SPRING 0.1                           ! spring constant, Hartree/Bohr^2
    &OPTIMIZER BFGS &END OPTIMIZER
    &CONVERGENCE
      MAX_FORCE 1.0E-3                     ! Hartree/Bohr
    &END CONVERGENCE
  &END BAND
&END MOTION
&FORCE_EVAL
  ...                                     ! same as the single-point input
&END FORCE_EVAL
```

Run on 16 cores:

```bash
mpiexec -n 16 cp2k.psmp -i pt111_h_neb.inp -o pt111_h_neb.out
```

The NEB converges in ~ 30 iterations; the output gives
the barrier height (the climbing image is the saddle
point). The expected barrier height for H/Pt(111) at
PBE is ~ 0.1 eV; the converged NEB trajectory in
`pt111_h_neb-1.restart' and the band energies in
`pt111_h_neb.log' confirm the diffusion pathway.

For a frequency calculation on the saddle-point image,
extract the image, fix the Pt atoms, and run a
frequency calculation with `RUN_TYPE VIBRATIONAL
ANALYSIS`. The output gives the imaginary frequency
at the saddle point (~ 700 cm⁻¹ for H/Pt(111) at PBE,
corresponding to a ~ 1 eV barrier height in a
harmonic approximation; the NEB is more accurate).

---

## Cross-references across the five codes

The following chapter cross-references are the most
useful for each code, in the order a working
calculator will need them.

- **VASP:** [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7 (forces, Hellmann–Feynman, Pulay); [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4–5.5 (XC, hybrids); [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7 (plane waves); [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.3 (Bloch), §7.6 (k-points), §7.11 (tetrahedron); [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7 (PAW), §8.12 (VASP PAW library); [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}) (phonons); [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (DFT+U, hybrids in practice); [chapter 13]({{ "/dft-notes/chapter-13/" | relative_url }}) (NEB, dimer).
- **Quantum ESPRESSO:** same as VASP, with [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}) being the *primary* phonon reference (DFPT is a QE strength).
- **ORCA:** [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) (post-HF, CC hierarchy); [chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) (HF, ERI); [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.8 (spin polarisation, broken-symmetry DFT); [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4–5.6 (XC, hybrids, double-hybrids); [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.3–6.6 (Gaussian basis); [chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) (TDDFT, Casida).
- **GPAW:** [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.3 (Runge–Gross, real-time TDDFT); [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.8 (real-space grids); [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7 (PAW).
- **CP2K:** [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7 (Hellmann–Feynman), §4.10.3 (BO-MD, Ehrenfest); [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.7 (D3, D4); [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.3 (Gaussians), §6.7 (plane waves); [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.8 (GTH).

---

## What this page is *not*

This page is a *tutorial* and a how-to. It is **not**:

- A replacement for the official manual of any of these
  five codes. The VASP manual is at
  `<https://www.vasp.at/wiki/index.php/The_VASP_Manual`>,
  the QE manual is at
  `<https://www.quantum-espresso.org/Doc/INPUT_PW.html`>,
  the ORCA manual is at
  `<https://www.faccts.de/docs/orca/`>,
  the GPAW documentation is at
  `<https://wiki.fysik.dtu.dk/gpaw/`>,
  and the CP2K reference manual is at
  `<https://manual.cp2k.org/`.>
  Read the manual *in addition to* this page.
- A reference for the theory. The chapter cross-
  references above are the pointers to the theory. For
  the equations that underlie PAW, plane waves, and
  Gaussian basis sets, see chapters 06 and 08; for the
  equations that underlie hybrid functionals and DFT+U,
  see chapters 05 and 12.
- A benchmarking study. The "expected values" in the
  worked examples are PBE values on small systems; they
  are *indicative* and should be verified against
  the literature before publication. The recommended
  benchmark database is the `ioChem-BD' repository
  (`<https://www.iochem-bd.org/`>) and the Materials
  Project (`<https://materialsproject.org/`>).
- A list of *all* features. Each code has more
  features than this page can document. The most
  important omissions: VASP's ML force field
  interface, QE's `EPW`' electron-phonon coupling
  module, ORCA's relativistic modules (ZORA, DKH,
  X2C), GPAW's $G_0W_0$ and BSE modules, and CP2K's
  linear-scaling DFT mode. These are mentioned in
  passing but not detailed.

> **Back to the [software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})**
> for a one-page summary of *all* the codes mentioned
> in the DFT Notes, or jump to
> [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) for the
> theory of basis sets that makes the "Gaussian vs.
> plane wave vs. real space" split sensible.
