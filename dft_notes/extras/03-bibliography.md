---
layout: page
title: "Bibliography"
permalink: /dft-notes/extras/bibliography/
description: >-
  Foundational papers and standard textbooks behind every chapter
  of DFT Notes. Organised by topic — foundations, XC functionals,
  many-body methods, pseudopotentials, basis sets, plane waves and
  solids, time-dependent DFT, forces, phonons — with a short
  summary of each entry and a pointer to the chapter and section
  where it is cited.
keywords: "DFT, density functional theory, bibliography, references,
  Hohenberg-Kohn, Kohn-Sham, PBE, B3LYP, SCAN, pseudopotential,
  PAW, plane wave, Bloch, Roothaan, Boys, Gaussian, CCSD, MP2,
  Runge-Gross, TDDFT, DFPT, phonons, force theorem, Hellmann-Feynman,
  Pulay"
---

# Bibliography

> Every paper and textbook that shaped the derivations in
> chapters 01–08. Each entry gives the full reference (authors,
> year, title, journal), the chapter and section that cites it,
> and a 1–2 sentence summary of the contribution. Use this as a
> *reading list* alongside the chapters: a foundational paper is
> usually more carefully argued than its textbook summary, and
> reading the original is the best way to understand *why* a
> particular approximation is built the way it is.

The bibliography is organised by topic:

1. [Foundational DFT papers](#1-foundational-dft-papers)
2. [XC functionals](#2-xc-functionals)
3. [Many-body methods](#3-many-body-methods)
4. [Pseudopotentials](#4-pseudopotentials)
5. [Basis sets](#5-basis-sets)
6. [Plane waves and solids](#6-plane-waves-and-solids)
7. [Time-dependent DFT](#7-time-dependent-dft)
8. [Forces and geometry](#8-forces-and-geometry)
9. [Phonons](#9-phonons)
10. [Standard textbooks](#10-standard-textbooks)

Where a paper is cited in more than one chapter, the *primary*
reference is the chapter where the result is first introduced.

---

## 1. Foundational DFT papers

The seven papers below are the theoretical foundation of
Kohn–Sham DFT. Every chapter of these notes (except chapter 01)
cites at least one of them.

### 1.1 Hohenberg & Kohn (1964) — Inhomogeneous electron gas

**P. Hohenberg and W. Kohn**, *Inhomogeneous electron gas*,
**Phys. Rev. 126, B864 (1964)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1;
also [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) and
[chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) in their
historical-context paragraphs.

Two theorems: (i) the ground-state density of a non-relativistic
system of interacting electrons in an external potential
determines that potential uniquely (up to a constant), so every
ground-state observable is a functional of the density alone; and
(ii) the density-functional energy is minimised by the
ground-state density. The 1964 paper proves *existence* of the
density functional, but does not give a practical algorithm —
that is what Kohn–Sham 1965 adds.

### 1.2 Kohn & Sham (1965) — Self-consistent equations

**W. Kohn and L. J. Sham**, *Self-consistent equations including
exchange and correlation effects*, **Phys. Rev. 140, A1133 (1965)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.2–4.4
("The Kohn–Sham ansatz", "Why the reformulation is exact",
"The KS self-consistent loop").

The paper that makes DFT computable. Introduces the fictitious
non-interacting reference system whose density equals the
interacting density, and writes down the one-electron eigenvalue
equation — the Kohn–Sham equations — that determines the
orbitals self-consistently with the effective potential. All of
the error in a KS calculation is now confined to a single
unknown functional, $E_\text{xc}[\rho]$. The 1965 paper also
introduces the L(S)DA, the local approximation to $E_\text{xc}$
using the homogeneous electron gas as the local reference.

### 1.3 Sham & Kohn (1966) — Uniform electron gas

**L. J. Sham and W. Kohn**, *One-particle properties of an
inhomogeneous interacting electron gas*, **Phys. Rev. 145,
561 (1966)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.3
as the source of the "uniform electron gas" reference for the
LDA.

The companion paper to Kohn–Sham 1965. Establishes the
connection between the KS one-particle eigenvalues and the
occupation-number derivative of the total energy — the
foundation of Koopmans-type analyses in DFT (later extended by
Janak 1978). The paper also works out the L(S)DA for the
spin-unpolarised case and demonstrates that the local
approximation is well defined for the XC energy, the XC
potential, and the quasiparticle spectrum alike.

### 1.4 Perdew & Zunger (1981) — Self-interaction correction

**J. P. Perdew and A. Zunger**, *Self-interaction correction to
density-functional approximations for many-electron systems*,
**Phys. Rev. B 23, 5048 (1981)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.1–5.2
as the modern parameterisation of the LDA in terms of the
Ceperley–Alder Monte Carlo data.

The first systematic treatment of the self-interaction error
(SIE) that is present in every LDA/GGA functional: the Coulomb
energy of the density with itself is not cancelled by the
corresponding exchange–correlation piece. The Perdew–Zunger SIC
subtracts the SIE on an orbital-by-orbital basis and produces
significantly improved atomisation energies and ionisation
potentials. The paper is also the standard source for the LDA
parameterisation in terms of $r_s$ using the Ceperley–Alder
(1980) quantum Monte Carlo data.

### 1.5 Perdew & Wang (1992) — LDA parameterisation

**J. P. Perdew and Y. Wang**, *Accurate and simple analytic
representation of the electron-gas correlation energy*,
**Phys. Rev. B 45, 13244 (1992)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.8.2
("The spin-DFT energy functional") and
[chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.1, as the
standard "PW92" parameterisation of the LSDA XC energy.

A high-accuracy closed-form fit to the Ceperley–Alder
quantum-Monte-Carlo data for the homogeneous electron gas
across the metallic density range ($2 \le r_s \le 10$).
Combined with the Perdew–Zunger (1981) exchange, this defines
the "LDA" used in essentially every production DFT code from
1992 onward. The PW92 fit reproduces the QMC data to better
than 1 mHartree/electron.

### 1.6 Perdew, Burke & Ernzerhof (1996) — PBE

**J. P. Perdew, K. Burke, and M. Ernzerhof**, *Generalized
gradient approximation made simple*, **Phys. Rev. Lett. 77,
3865 (1966)**; erratum **Phys. Rev. Lett. 78, 1396 (1997)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.2
("GGA — adding the gradient"), as the canonical non-empirical
GGA.

The PBE functional replaces the earlier ad-hoc PW91 form with a
*constraint-satisfying* GGA: the enhancement factor over LDA
exchange and correlation is constructed to obey all the known
exact conditions on $E_\text{xc}[\rho, \nabla\rho]$ that the
authors could enumerate — the LDA limit, the uniform scaling
to the high-density limit, the Lieb–Oxford bound, the gradient
expansion at small $|\nabla\rho|$, and several more. PBE has
*no fitted parameters* and is the most-cited functional in the
solid-state literature. The 1997 erratum fixes the sign of one
of the constraints.

### 1.7 Sun, Ruzsinszky & Perdew (2015) — SCAN

**J. Sun, A. Ruzsinszky, and J. P. Perdew**, *Strongly
constrained and appropriately normed semilocal density
functional*, **Phys. Rev. Lett. 115, 036402 (2015)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.3
("Meta-GGA — adding the kinetic-energy density"), as the
canonical non-empirical meta-GGA.

SCAN is the highest-rung *parameter-free* functional in common
use. It is built by satisfying 17 known exact constraints on
the XC functional of the meta-GGA form
$E_\text{xc}[\rho, \nabla\rho, \tau]$ (where $\tau$ is the
positive-definite orbital kinetic-energy density), and is
"appropriately normed" by reproducing the exact XC energy of
the hydrogen atom. Significantly better than PBE for
diversely-bonded systems — surfaces, 2-D materials, ions in
solution, transition-metal complexes — at the same meta-GGA
cost ($\mathcal O(K)$ per SCF iteration). The 2021 r²SCAN
regularisation restores numerical stability.

---

## 2. XC functionals

The XC zoo — from the local-density approximation through
hybrids and range-separated hybrids. Each functional below adds
one more ingredient to the local-density picture.

### 2.1 Vosko, Wilk & Nusair (1980) — VWN

**S. H. Vosko, L. Wilk, and M. Nusair**, *Accurate
spin-dependent electron liquid correlation energies for local
spin density calculations: a critical analysis*,
**Can. J. Phys. 58, 1200 (1980)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.8.2
and [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4 (as a
component of B3LYP).

The standard closed-form parameterisation of the LSDA
correlation energy, derived from the Ceperley–Alder (1980)
quantum Monte Carlo data. The "VWN" functional (re-parameterised
"VWN5" in the 1980 erratum, and a simplified "VWN3" form) is
the most-cited LSDA correlation parameterisation in
chemistry-focused DFT codes. It enters many composite
functionals (notably B3LYP) as a component.

### 2.2 Becke (1988) — B88 exchange

**A. D. Becke**, *Density-functional exchange-energy
approximation with correct asymptotic behavior*,
**Phys. Rev. A 38, 3098 (1988)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.2
and §5.4 (as the exchange component of BLYP and B3LYP).

The B88 exchange functional was the first GGA exchange to fix
the LDA's spurious self-interaction by adding a gradient
correction that recovers the correct $-1/r$ asymptotic
behaviour of the exchange energy density. Fitted to the
exchange energies of six noble-gas atoms, B88 is the empirical
counterpart to the constraint-based PBE. It is the most widely
used GGA exchange in chemistry-focused DFT (B88-PW91, B88-LYP,
B88-P86, B3LYP).

### 2.3 Lee, Yang & Parr (1988) — LYP correlation

**C. Lee, W. Yang, and R. G. Parr**, *Development of the
Colle–Salvetti correlation-energy formula into a functional of
the electron density*, **Phys. Rev. B 37, 785 (1988)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4
(as the correlation component of BLYP and B3LYP).

The LYP correlation functional is derived from the
Colle–Salvetti (1975) expression for the correlation energy of
a two-electron Hartree–Fock pair density, reformulated as a
functional of the density and its Laplacian. It is purely
empirical (four parameters fit to the helium atom) and has no
LDA component — it is used as a *replacement* for the LSDA
correlation, not a correction. Combined with B88 exchange it
gives the famous "BLYP" functional, the default GGA in
pre-B3LYP computational chemistry.

### 2.4 Becke (1993) — B3LYP hybrid

**A. D. Becke**, *Density-functional thermochemistry. III.
The role of exact exchange*, **J. Chem. Phys. 98, 5648 (1993)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4
("Hybrids — adding a fraction of exact exchange").

The B3LYP functional is the most-cited density functional in
all of computational chemistry. It mixes 20% of exact
(non-local) Hartree–Fock exchange with 80% B88 GGA exchange,
combined with 81% LYP correlation and 19% VWN (LSDA)
correlation, with three parameters fit to a training set of 56
atomisation energies, 42 ionisation potentials, 8 proton
affinities, and 10 total atomic energies. B3LYP is the default
of essentially every quantum-chemistry code from 1993 onward
and remains the workhorse of organic thermochemistry.

### 2.5 Heyd, Scuseria & Ernzerhof (2003) — HSE

**J. Heyd, G. E. Scuseria, and M. Ernzerhof**, *Hybrid
functionals based on a screened Coulomb potential*,
**J. Chem. Phys. 118, 8207 (2003)**; erratum **J. Chem. Phys.
124, 219906 (2006)**.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.5
("Range-separated hybrids").

The HSE06 functional is the standard range-separated hybrid for
solid-state DFT. It splits the Coulomb interaction into a
short-range part treated at the PBE level and a long-range part
treated with 25% exact exchange, using the complementary error
function `erfc(ω r)` as the partition (with
$\omega = 0.11$ bohr$^{-1}$ — the inverse screening length).
The screening makes the exact-exchange integral short-ranged (so
it can be evaluated in a plane-wave basis with a modest
real-space cutoff). HSE06 is the default functional in many
solid-state codes (VASP, FHI-aims, Quantum ESPRESSO) for
production runs.

---

## 3. Many-body methods

The hierarchy of wavefunction-based methods that DFT replaces
for problems where it is too expensive. The benchmarks and
calibration points for every DFT functional are computed with
these methods.

### 3.1 Møller & Plesset (1934) — MP perturbation theory

**C. Møller and M. S. Plesset**, *Note on an approximation
treatment for many-electron systems*, **Phys. Rev. 46, 618
(1934)**.

Cited in: [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.3
("The hierarchy of wavefunction methods").

The paper that introduced Rayleigh–Schrödinger perturbation
theory using the sum of Fock operators as the zero-order
Hamiltonian. The first non-vanishing correction — second order
in the fluctuation potential — is "MP2" and remains the cheapest
correlated method that improves systematically on Hartree–Fock.
Scales as $\mathcal O(K^4)$ (now $\mathcal O(K^3)$ with density
fitting) and recovers roughly 80% of the correlation energy of a
closed-shell organic molecule near equilibrium. The 1934 paper
contains the full perturbative formalism; the modern MP2
implementation is in every quantum-chemistry code.

### 3.2 Čížek (1966) — Coupled cluster

**J. Čížek**, *On the correlation problem in atomic and
molecular systems. Calculation of wavefunction components in
perturbation theory*, **J. Chem. Phys. 45, 4256 (1966)**.

Cited in: [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.3
and §2.4 as the origin of the coupled-cluster series.

Introduces the coupled-cluster (CC) Ansatz
$|\Psi\rangle = e^{\hat T} |\Phi_0\rangle$ with the cluster
operator $\hat T = \hat T_1 + \hat T_2 + \dots$ (single, double,
… excitations) into quantum chemistry. The CC wave Ansatz is
*not* variational (in its original form) but is size-extensive
by construction — a property that makes it dramatically more
accurate than CI for systems beyond a few electrons. Čížek's
paper is the foundation of the modern hierarchy CCSD, CCSD(T),
CCSDT, …  The connection to nuclear physics and to the
linked-cluster theorem of Brueckner is explained in the
original.

### 3.3 Purvis & Bartlett (1982) — CCSD

**G. D. Purvis and R. J. Bartlett**, *A full coupled-cluster
singles and doubles model: the inclusion of disconnected
triples*, **J. Chem. Phys. 76, 1910 (1982)**.

Cited in: [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.3
and §2.4 as the canonical CCSD implementation.

The first efficient implementation of the coupled-cluster
singles-and-doubles (CCSD) equations for a general molecular
system. CCSD truncates the cluster operator at $\hat T_2$ and
solves the corresponding amplitude equations iteratively; the
resulting energy is correct through fourth order in
Møller–Plesset perturbation theory by construction. The paper
introduces the diagrammatic and computational machinery that
every modern CCSD code uses. CCSD scales as $\mathcal O(K^6)$
and is the workhorse of small-molecule correlated quantum
chemistry.

### 3.4 Raghavachari et al. (1989) — CCSD(T)

**K. Raghavachari, G. W. Trucks, J. A. Pople, and
M. Head-Gordon**, *A fifth-order perturbation comparison of
electron correlation theories*, **Chem. Phys. Lett. 157, 479
(1989)**.

Cited in: [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.3
and §2.4 ("The 'gold standard' and its limits").

The paper that introduced the now-ubiquitous CCSD(T) "gold
standard" of quantum chemistry. CCSD(T) is CCSD plus a
perturbative estimate of the connected-triples contribution,
evaluated using the CCSD amplitudes. The non-iterative
$\mathcal O(K^7)$ triples step adds a small, mostly-cancelling
correction to the CCSD energy that restores chemical accuracy
(1 kcal/mol) for the vast majority of closed-shell main-group
systems near equilibrium. The paper is a *comparison* of five
correlation methods at fifth-order perturbation theory and
demonstrates that CCSD(T) systematically out-performs the
others at a manageable cost. The "(T)" notation (with
parentheses to distinguish from the full CCSDT-1 iterative
triples) has become universal.

---

## 4. Pseudopotentials

The construction, the norm-conservation condition, the
ultrasoft extension, and the PAW reformulation. Every
plane-wave DFT calculation uses one of the four flavours in
this section.

### 4.1 Hamann, Schlüter & Chiang (1979) — Norm-conserving pseudopotentials

**D. R. Hamann, M. Schlüter, and C. Chiang**, *Norm-conserving
pseudopotentials*, **Phys. Rev. Lett. 43, 1494 (1979)**.

Cited in: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.3
("The norm-conservation condition") as the foundational
paper of the field, and §8.4 as the formal source of the
"transferability" property.

The paper that defined the modern norm-conserving pseudopotential
(NC-PP). The construction enforces three properties: the
pseudo-wavefunction matches the all-electron one in value,
first derivative, and logarithmic derivative outside a cutoff
radius $r_c$; inside $r_c$ the pseudo is nodeless; and the
**norm-conservation** condition
$\int_0^{r_c} |\phi_l|^2\, dr = \int_0^{r_c} |u_l|^2\, dr$
holds. The proof that the third condition is what makes the
pseudo *transferable* — i.e. gives the same energy eigenvalue
in any chemical environment — is the heart of the paper. NC-PPs
are the workhorse of high-accuracy plane-wave DFT and the
starting point of every later pseudopotential family.

### 4.2 Troullier & Martins (1991) — Efficient construction

**N. Troullier and J. L. Martins**, *Efficient pseudopotentials
for plane-wave calculations*, **Phys. Rev. B 43, 1993 (1991)**.

Cited in: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.4
("Construction — Troullier-Martins and BHS") as the
preferred modern construction recipe.

The Troullier–Martins (TM) construction is the standard
high-accuracy, smooth-pseudo recipe. It parameterises the
pseudo-wavefunction inside $r_c$ as
$\phi_l(r) = r^{l+1} \exp\bigl(\sum_{n=0}^N c_n r^{2n}\bigr)$
with $N = 5$ or 6 polynomial coefficients, and uses six
matching conditions (value, first and second derivative at
$r_c$, plus a "kinetic-energy-conservation" condition matching
the second moment of the charge density in the core) to
determine them. The resulting pseudo is *smoother* than the
Hamann–Schlüter–Chiang (1979) form at the same accuracy, and
therefore requires a smaller plane-wave cutoff — typically
$E_\text{cut} \sim 30$–$50$ Ry for first-row atoms.

### 4.3 Vanderbilt (1990) — Ultrasoft pseudopotentials

**D. Vanderbilt**, *Soft self-consistent pseudopotentials in a
generalized eigenvalue formalism*, **Phys. Rev. B 41, 7892
(1990)**.

Cited in: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.6
("Ultrasoft pseudopotentials (Vanderbilt)") as the
generalisaton of the NC-PP framework to smoother
pseudopotentials.

Vanderbilt's insight is that the norm-conservation condition
can be *relaxed* and replaced by a generalised overlap
operator, at the cost of a more complex formalism. The
"ultrasoft" pseudo-wavefunction is allowed to have a norm
*deficit* $\Delta Q_l = Q_l^\text{ae} - Q_l^\text{ps}$ inside
$r_c$, and the missing charge is recovered by an **augmentation
charge** that adds an atom-centred correction to the density.
The KS equations become a *generalised* eigenvalue problem
$\hat H |\phi\rangle = \varepsilon \hat S |\phi\rangle$, with
$\hat S \neq \mathbf 1$. The payoff is a factor of 2–3
reduction in the required plane-wave cutoff for hard elements
(3$d$ transition metals, 4$f$ rare earths, O, N) at the same
accuracy. USPPs are the default in VASP, Quantum ESPRESSO,
and CASTEP.

### 4.4 Blöchl (1994) — PAW

**P. E. Blöchl**, *Projector augmented wave method*,
**Phys. Rev. B 50, 17953 (1994)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
§4.10.3 and [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }})
§8.7 ("The PAW method (Blöchl)"); also the source of the
Blöchl tetrahedron integration in
[chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.11.

The PAW method is the most accurate of the plane-wave
valence-only approaches. It writes the all-electron
wavefunction as a *linear transformation* of a smooth
pseudo-wavefunction, with the difference carried by
**augmentation functions** localised inside atom-centred
spheres. The total energy splits into a smooth part
(computed on the plane-wave grid) and an on-site correction
(computed in real space around each atom) that is exact
within the chosen partial-wave basis. PAW is exact in the
all-electron limit (no frozen-core approximation) and admits
the same smooth-wavefunction speed-ups as USPP. The 1994
paper also introduces the **Blöchl tetrahedron method** for
Brillouin-zone integration, an $\mathcal O((\Delta k)^2)$
improvement over the standard Monkhorst–Pack Riemann sum.
PAW is the default in VASP and GPAW for high-accuracy
calculations on transition-metal and rare-earth systems.

---

## 5. Basis sets

The technology that turns the KS eigenvalue equation into a
finite matrix. Three families of basis are used in practice:
atom-centred Gaussians (chemistry), plane waves (solid-state),
and numerical atomic orbitals (linear scaling).

### 5.1 Boys (1950) — Gaussian basis functions

**S. F. Boys**, *Electronic wave functions. I. A general method
of calculation for the stationary states of any molecular
system*, **Proc. R. Soc. Lond. A 200, 542 (1950)**.

Cited in: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.3
("Gaussian-type orbitals (GTOs)") as the origin of the
Gaussian basis in quantum chemistry.

The paper that introduced the use of Gaussian-type functions
$e^{-\alpha r^2}$ (rather than Slater-type $e^{-\zeta r}$) as
basis functions for molecular electronic-structure calculations.
The motivation is purely computational: the **Gaussian product
theorem** (the product of two Gaussians at different centres is
a single Gaussian at a third centre) reduces the four-centre
two-electron integrals of Hartree–Fock to closed-form
expressions involving the **Boys function** $F_0(t)$. The paper
is short by modern standards but is the founding document of
the entire Gaussian-based quantum-chemistry industry. Every
production quantum-chemistry code (Gaussian, PSI4, PySCF, ORCA,
NWChem, …) uses a Gaussian basis.

### 5.2 Hehre, Stewart & Pople (1969) — STO-nG minimal basis

**W. J. Hehre, R. F. Stewart, and J. A. Pople**,
*Self-consistent molecular-orbital methods. I. Use of Gaussian
expansions of Slater-type atomic orbitals*,
**J. Chem. Phys. 51, 2657 (1969)**.

Cited in: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.4
("STO-nG — the minimal basis") as the source of the STO-3G
basis.

The Hehre–Stewart–Pople (HSP) paper fits each Slater-type
orbital $e^{-\zeta r}$ of the minimal basis (1$s$, 2$s$, 2$p$,
…) as a least-squares contraction of $n$ primitive Gaussians.
The case $n = 3$ — STO-3G — became the canonical "minimal
basis" of computational chemistry: a single contracted $s$
function for H, a contracted $s$ and three contracted $p$
functions for first-row atoms, etc. The HSP tables are the
universal starting point of every quantum chemistry education.
(Modern use: STO-3G is too small for production work but is the
workhorse of pedagogical examples and large-scale screening.)

### 5.3 Krishnan, Binkley, Seeger & Pople (1980) — 6-31G split-valence

**R. Krishnan, J. S. Binkley, R. Seeger, and J. A. Pople**,
*Self-consistent molecular orbital methods. XX. A basis set for
correlated wave functions*, **J. Chem. Phys. 72, 650 (1980)**.

Cited in: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.5
("Split-valence: 3-21G, 6-31G, 6-311G") as the source of the
6-31G basis.

The 6-31G basis is the canonical "double-zeta valence" basis
of computational chemistry. The core orbital of each atom is
described by a single contracted function of 6 primitives; the
valence shell is *split* into an "inner" contracted function
of 3 primitives and an "outer" single-primitive function,
giving the basis set its name. The 6-31G split allows the
SCF to readjust the *size* of the valence orbitals molecule
by molecule — the inner function is roughly atomic, the
outer function is roughly the chemical-bond radius. Combined
with polarisation and diffuse functions (6-31G\*, 6-31+G\*),
the Pople split-valence family dominated computational
chemistry from 1980 until the Dunning correlation-consistent
bases displaced it in the 1990s.

### 5.4 Dunning (1989) — cc-pVXZ correlation-consistent bases

**T. H. Dunning Jr.**, *Gaussian basis sets for use in correlated
molecular calculations. I. The atoms boron through neon and
hydrogen*, **J. Chem. Phys. 90, 1007 (1989)**.

Cited in: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.6
("Polarisation, diffuse, and the cc-pVXZ family") as the
source of the cc-pVXZ family.

Dunning's correlation-consistent (cc-pVXZ) basis family is
the standard path to basis-set convergence in modern quantum
chemistry. Each "rung" — D (double), T (triple), Q (quadruple),
5, 6, … — adds the functions of higher angular momentum that
are needed to recover the next decade of electron-correlation
energy. The "correlation consistent" name refers to the
property that the missing correlation energy falls off as a
geometric series in the cardinal number $X$, which makes the
two- or three-point extrapolation
$E_\text{corr}(X) \to E_\text{corr}(\infty)$ well-conditioned.
Dunning's 1989 paper is the foundation of every modern
basis-set convergence study.

---

## 6. Plane waves and solids

The periodic-symmetry machinery — Bloch's theorem, k-point
sampling, and the methods that take advantage of translational
symmetry to make the infinite-lattice problem finite.

### 6.1 Bloch (1929) — Bloch's theorem

**F. Bloch**, *Über die Quantenmechanik der Elektronen in
Kristallgittern*, **Z. Phys. 52, 555 (1929)**.

Cited in: [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7
("Plane waves") and [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.1,
§7.3 ("Derivation of Bloch's theorem") as the central theorem
of solid-state physics.

Bloch's 1929 paper proves the theorem that bears his name:
every eigenstate of a Hamiltonian with discrete translational
symmetry can be written as a plane wave
$e^{i\mathbf k \cdot \mathbf r}$ multiplied by a
cell-periodic function $u_{n\mathbf k}(\mathbf r)$. This
single fact is the foundation of the entire band theory of
solids — the discrete translational symmetry of the lattice
reduces the differential eigenvalue problem on an infinite
lattice to a discrete set of differential eigenvalue problems
indexed by the crystal momentum $\mathbf k$ in the first
Brillouin zone. Bloch's original paper is in German; the
result appears in every solid-state textbook under "Bloch's
theorem" with the standard proof via commutativity of $\hat
H$ and the translation operator.

### 6.2 Kohn & Rostoker (1954) — KKR method

**W. Kohn and N. Rostoker**, *Solution of the Schrödinger
equation in periodic lattices with an application to metallic
lithium*, **Phys. Rev. 94, 1111 (1954)**.

Cited in: [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.13
as a historical predecessor of the modern multiple-scattering
approaches to the band-structure problem.

The KKR (Korringa–Kohn–Rostoker) method is one of the three
foundational band-structure techniques (along with the
augmented-plane-wave APW method of Slater and the
orthogonalised-plane-wave OPW method of Herring). KKR
expands the wavefunction in each muffin-tin sphere as a sum
of spherical harmonics times radial solutions, and matches to
free-space plane waves in the interstitial region. The
resulting secular equation is in terms of **structure
constants** that depend only on the lattice geometry, and is
the natural starting point for multiple-scattering theory and
for the Coherent Potential Approximation (CPA) of disordered
alloys. The 1954 paper is the source of the formal KKR
equations and of the muffin-tin approximation still used in
many all-electron codes (WIEN2k, Elk, SPR-KKR).

### 6.3 Andersen (1975) — LMTO method

**O. K. Andersen**, *Linear methods in band theory*,
**Phys. Rev. B 12, 3060 (1975)**.

Cited in: [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.13
as the source of the linear-muffin-tin-orbital (LMTO)
formalism.

Andersen's LMTO method is the third foundational band-structure
technique. The key insight is that the energy dependence of
the muffin-tin orbitals can be **linearised** about a fixed
reference energy, and the resulting linear combinations form
an efficient, near-orthogonal basis that is minimal in size
(typically 9 orbitals per atom: one $s$, three $p$, five $d$).
The LMTO-ASA (atomic-sphere approximation) method is the
workhorse of historical electronic-structure calculations on
transition metals and their compounds. Andersen's paper
introduces the linearisation, the "screening" of the structure
constants, and the connection to the KKR formalism. Modern
descendants — the full-potential LMTO (FP-LMTO) and the NMTO
(order-$N$ MTO) methods — remain in use.

### 6.4 Monkhorst & Pack (1976) — k-point sampling

**H. J. Monkhorst and J. D. Pack**, *Special points for
Brillouin-zone integrations*, **Phys. Rev. B 13, 5188 (1976)**.

Cited in: [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6
("k-point sampling") as the source of the standard
uniform-mesh sampling of the Brillouin zone.

The Monkhorst–Pack (MP) mesh is the workhorse of solid-state
DFT. The paper constructs a uniform $N_1 \times N_2 \times N_3$
mesh in the Brillouin zone by the simple rule
$\mathbf k = (m_1/N_1) \mathbf b_1 + (m_2/N_2) \mathbf b_2 +
(m_3/N_3) \mathbf b_3$ with $m_i = 0, 1, \dots, N_i - 1$, and
shows that this mesh samples the BZ uniformly with a
convergence rate of $\mathcal O(1/N^2)$ in 1-D and
$\mathcal O(1/N^{2/3})$ in 3-D for smooth integrands. The MP
mesh is the default of every production plane-wave code;
together with the $\Gamma$-centred variant and the tetrahedron
integration of [Blöchl (1994)](#44-blöchl-1994--paw) it provides
the practical infrastructure for converging the BZ integral
to arbitrary precision.

### 6.5 Blöchl, Jepsen & Andersen (1994) — Improved tetrahedron integration

**P. E. Blöchl, O. Jepsen, and O. K. Andersen**, *Improved
tetrahedron method for Brillouin-zone integration*,
**Phys. Rev. B 49, 16223 (1994)**.

Cited in: [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.11
("The tetrahedron method for Brillouin-zone integration") as
the source of the modern linearisation correction.

The "Blöchl correction" to the standard Lehmann–Taut (1972)
tetrahedron method uses the energies of the four neighbouring
tetrahedra to estimate the second derivative of the band
energy within each tetrahedron, and subtracts the leading
$\mathcal O((\Delta k)^2)$ linearisation error analytically.
The result is an $\mathcal O((\Delta k)^4)$ integration scheme
— a factor of $2^{3/2}$ coarser mesh in each direction for
the same accuracy, with no adjustable smearing parameter. The
corrected tetrahedron method is the recommended BZ integrator
for production-quality total energies, densities of states,
and Fermi-surface-resolved properties (transport, de
Haas–van Alphen).

---

## 7. Time-dependent DFT

The TDDFT machinery that extends ground-state KS DFT to
excited states and to the linear-response regime.

### 7.1 Runge & Gross (1984) — The RG theorem

**E. Runge and E. K. U. Gross**, *Density-functional theory for
time-dependent systems*, **Phys. Rev. Lett. 52, 997 (1984)**.

Cited in: [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (planned)
and [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.3
as the source of the time-dependent Hohenberg–Kohn analogue.

The Runge–Gross theorem is the time-dependent analogue of the
Hohenberg–Kohn theorem: for a many-electron system evolving
under a time-dependent external potential $v_\text{ext}(\mathbf r,
t)$ that is *analytic* in time (admits a Taylor expansion at
$t_0$), the time-dependent density $\rho(\mathbf r, t)$
determines the potential uniquely (up to a purely
time-dependent function), and therefore determines the
time-dependent wavefunction. The proof uses the fact that the
*current density* $j(\mathbf r, t)$ is uniquely determined by
$\rho(\mathbf r, t)$ via the continuity equation, and that the
*action* functional $A[\rho]$ of the system has a unique
stationary point. The RG theorem is the foundation of TDDFT:
every observable that depends on the time-evolving state is,
in principle, a functional of $\rho(\mathbf r, t)$.

### 7.2 Casida (1995) — Linear response formulation

**M. E. Casida**, *Time-dependent density functional response
theory for molecules*, in *Recent Advances in Density
Functional Methods*, Part I, edited by D. P. Chong (World
Scientific, 1995), p. 155.

Cited in: [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (planned)
and indirectly through the Casida equations in
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.3.

Casida's formulation is the standard linear-response TDDFT used
in every quantum-chemistry code. The frequency-dependent
polarisability $\alpha(\omega)$ is written as the solution of
a non-Hermitian eigenvalue problem in the space of particle-hole
excitations:
$\Omega \mathbf F_I = \omega_I^2 \mathbf F_I$,
where the matrix $\Omega$ depends on the KS orbitals, the KS
eigenvalues, and the XC kernel
$f_\text{xc}(\mathbf r, \mathbf r') = \delta^2 E_\text{xc}
/\delta\rho(\mathbf r) \delta\rho(\mathbf r')$. The eigenvalues
$\omega_I$ are the *excitation energies* of the system; the
eigenvectors $\mathbf F_I$ give the oscillator strengths.
Casida's formulation is the basis of every production TDDFT
absorption spectrum and is what code names like "TDA"
(Tamm–Dancoff approximation) refer to when approximating the
full Casida matrix by its positive-energy block.

---

## 8. Forces and geometry

The theorems and algorithms that turn a converged SCF into a
force on the nuclei, the input to every geometry optimisation
and molecular-dynamics run.

### 8.1 Hellmann (1937) — The Hellmann–Feynman theorem

**H. Hellmann**, *Einführung in die Quantenchemie*,
**Franz Deuticke, Leipzig (1937)**, p. 285.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7.1
as the source of the force-formula $dE/d\lambda = \langle \Psi |
d\hat H/d\lambda | \Psi \rangle$.

The Hellmann–Feynman theorem (also attributed to Feynman 1939,
who re-derived it independently) states that the derivative of
the energy of an eigenstate with respect to any parameter
$\lambda$ in the Hamiltonian is equal to the expectation value
of the derivative of the Hamiltonian, with the eigenstate held
fixed. The proof is the two-line argument that the
wavefunction-derivative terms cancel by normalisation. The
theorem is the foundation of every analytic force evaluation:
the force on a nucleus in a molecule is the expectation value
of the Coulomb force between the nucleus and the electron
density, evaluated at fixed geometry. In a *complete* basis,
this is the entire force; in a finite basis, the Pulay
correction (next entry) is required.

### 8.2 Feynman (1939) — The Feynman theorem

**R. P. Feynman**, *Forces in molecules*,
**Phys. Rev. 56, 340 (1939)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7
as the second independent derivation of the Hellmann–Feynman
theorem; also the source of the modern
"force-on-a-nucleus = electron-density attraction +
nuclear-nuclear repulsion" formula.

Feynman's 1939 paper re-derives the Hellmann–Feynman theorem
and applies it to the molecular problem: the force on a
nucleus in a clamped-nuclei calculation is *exactly* the
classical Coulomb force on a point charge embedded in the
electron density. The paper also introduces the concept of the
"force" as a derivative of the energy with respect to a
parameter, separate from the concept of momentum, and uses the
example of a diatomic molecule to demonstrate that the nuclear
motion is adiabatic to leading order. Every modern force
theorem in quantum chemistry traces back to this paper.

### 8.3 Pulay (1969) — Forces in a Gaussian basis

**P. Pulay**, *Ab initio calculation of the force constant in
molecules*, **Mol. Phys. 17, 197 (1969)**.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7.3
("The Pulay correction") as the source of the basis-set
correction to the Hellmann–Feynman force.

The Pulay force is the correction to the Hellmann–Feynman
formula that arises in a *finite, atom-centred* basis. The
basis functions $\chi_\mu(\mathbf r; \mathbf R)$ depend on
the nuclear coordinates through their centres
$\mathbf A_\mu = \mathbf R_{I(\mu)}$, so
$\partial \chi_\mu / \partial \mathbf R_I \neq 0$. Pulay
showed in 1969 that the resulting correction to the
Hellmann–Feynman force — the **Pulay force** — is
non-vanishing and is given by
$\mathbf F_I^\text{Pulay} = -2 \sum_i^\text{occ}
\sum_{\mu \in I} \sum_\nu C_{\mu i} C_{\nu i}
\langle \partial \chi_\mu / \partial \mathbf R_I |
\hat H_\text{KS} - \varepsilon_i | \chi_\nu \rangle$.
The term vanishes in a complete basis (and trivially in a
plane-wave basis, where the basis is independent of
$\mathbf R$), but is essential in every Gaussian,
numerical-atomic-orbital, and finite-element code. The 1969
paper is the foundation of analytic-gradient Hartree–Fock and
DFT.

### 8.4 Pulay (1980) — Improved force formula and DIIS

**P. Pulay**, *Convergence acceleration of iterative sequences.
The case of SCF iteration*, **Chem. Phys. Lett. 73, 393
(1980)**.

Cited in: [chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.8.4
("DIIS — Pulay's accelerator") as the source of the Direct
Inversion in the Iterative Subspace (DIIS) convergence
accelerator.

The DIIS paper is the most-cited quantum-chemistry paper of
the 1980s. Pulay showed that the SCF fixed-point iteration
could be accelerated by extrapolating from the history of
recent Fock (or density) matrices: the optimal linear
combination of the last $m$ iterates — chosen to minimise the
squared norm of the extrapolated residual, subject to the
sum-to-one constraint — produces a quasi-Newton step on the
space of Fock matrices. DIIS converges in a handful of
iterations where plain density mixing oscillates or diverges,
and is the default convergence accelerator of every production
quantum-chemistry code (Gaussian, PSI4, PySCF, ORCA, NWChem,
…) and most plane-wave codes (VASP, Quantum ESPRESSO). The
1980 paper is also the source of the "commutator error" metric
$\mathbf e = [\mathbf F, \mathbf P]$ used as the DIIS residual
in most implementations.

---

## 9. Phonons

The two references that bridge the static DFT energy to the
dynamical properties of crystals — phonons, dielectric
response, electron–phonon coupling.

### 9.1 Born & Huang (1954) — Dynamical theory of crystal lattices

**M. Born and K. Huang**, *Dynamical Theory of Crystal
Lattices*, **Oxford University Press (1954)**.

Cited in: [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }})
(planned) as the source of the harmonic approximation, the
dynamical matrix, and the formalism of lattice vibrations in
insulators.

Born and Huang's *Dynamical Theory of Crystal Lattices* is the
standard reference for the theory of phonons in insulating
crystals. The book covers the harmonic approximation, the
dynamical matrix, the relation between the long-wavelength
acoustic modes and the elastic constants, the macroscopic
electric field and the LO–TO splitting, the
Lyddane–Sachs–Teller relation, the theory of the dielectric
function in the infrared, and the extension to anharmonic
effects. Every later phonon reference (Maradudin, Ashcroft &
Mermin, Yu & Cardona) traces its formalism to Born & Huang.
The book also introduces the **adiabatic (Born–Oppenheimer)
approximation** in the modern form that the DFT notes use in
chapter 01.

### 9.2 Giannozzi et al. (1991) — DFPT, Quantum ESPRESSO

**P. Giannozzi, S. de Gironcoli, P. Pavone, and S. Baroni**,
*Ab initio calculation of phonon dispersions in
semiconductors*, **Phys. Rev. B 43, 7231 (1991)**.

Cited in: [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }})
(planned) as the source of density-functional perturbation
theory (DFPT) for lattice dynamics.

Giannozzi, de Gironcoli, Pavone, and Baroni introduced
density-functional perturbation theory (DFPT) as a
*linear-response* method for the lattice dynamics of periodic
solids. Rather than computing the phonon dispersion by finite
differences of the total energy (the "frozen-phonon" method,
which requires a supercell of size proportional to the phonon
wavelength), DFPT computes the *derivative* of the KS orbitals
with respect to a periodic perturbation
$\partial V_\text{ext} / \partial \mathbf R_{I\alpha}$
directly using **Sternheimer's equation**
$(\hat H_\text{KS} - \varepsilon_i)^2 \, \partial \phi_i
= -(\partial \hat V_\text{KS} - \partial \varepsilon_i)
\phi_i$.
The result is a phonon dispersion that is exact at linear
order and costs *only* a small multiple of a single
ground-state SCF. The 1991 paper is the foundation of the
open-source **Quantum ESPRESSO** distribution (also Giannozzi
et al.) and of every modern plane-wave phonon calculation.
DFPT also gives the dielectric constant, Born effective
charges, the non-linear optical susceptibility, and the
electron–phonon coupling matrix elements — all from the same
linear-response machinery.

---

## 10. Standard textbooks

The five monographs that should sit on the shelf of anyone
working in electronic-structure theory. They are not cited in
the chapters directly — the chapters are self-contained — but
they are the *next step* after these notes for a reader who
wants the full mathematical apparatus, the historical context,
or the production-code perspective.

### 10.1 Parr & Yang (1989) — Density-Functional Theory of Atoms and Molecules

**R. G. Parr and W. Yang**, *Density-Functional Theory of
Atoms and Molecular Orbitals*, **Oxford University Press
(1989)**.

A monograph written from the chemistry perspective. Covers the
Hohenberg–Kohn theorem, the Kohn–Sham equations, the L(S)DA,
the connection to chemical concepts (chemical potential,
hardness, Fukui functions, electronegativity equalisation), and
the early GGAs. The book is the *bridge* between the physics
of the KS equations and the language of conceptual DFT that
chemists use. It assumes only an undergraduate background in
quantum mechanics and is the most accessible entry in this
section.

### 10.2 Martin (2004) — Electronic Structure

**R. M. Martin**, *Electronic Structure: Basic Theory and
Practical Methods*, **Cambridge University Press (2004)**.

The single most comprehensive textbook on the
electronic-structure problem at the graduate level. Covers
tight binding, the nearly-free-electron model, density
functional theory (Hohenberg–Kohn, KS, LDA, GGA, hybrids,
TDDFT), pseudopotentials, the plane-wave method, the
full-potential LAPW method, forces and stress, phonons
(frozen phonon and DFPT), electron–phonon coupling, the GW
approximation, and the Bethe–Salpeter equation. The
mathematical apparatus is given in full, the connections to
production codes are made explicit, and the worked examples
and problem sets are uniformly excellent. **The book to own
if you can own only one.**

### 10.3 Dreizler & Gross (1990) — Density Functional Theory

**R. M. Dreizler and E. K. U. Gross**, *Density Functional
Theory: An Approach to the Quantum Many-Body Problem*,
**Springer-Verlag (1990)**.

The first comprehensive DFT textbook, written from the
many-body physics perspective. Covers the Hohenberg–Kohn
theorem and its extensions (spin DFT, current DFT, time
dependent), the Kohn–Sham equations, the L(S)DA and its
limitations, the early GGAs, and the time-dependent formalism
(Runge–Gross, linear response, the Casida equations). More
mathematical than Parr–Yang, more physics-oriented than
Martin; the standard reference on the formal side of DFT.

### 10.4 Szabo & Ostlund (1989) — Modern Quantum Chemistry

**A. Szabo and N. S. Ostlund**, *Modern Quantum Chemistry:
Introduction to Advanced Electronic Structure Theory*,
**McGraw-Hill (1989)**; revised Dover edition (1996).

The standard introduction to *wavefunction-based* quantum
chemistry. Covers the postulates, the hydrogen atom, the
Hartree–Fock method, the Roothaan–Hall equations, electron
correlation (CI, MP, CC), and the Gaussian basis, with worked
numerical examples (the H$_2$ STO-3G calculation that is the
anchor of [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.9 is
table 3.5 of Szabo & Ostlund). The book assumes an
undergraduate physical-chemistry background and is the *only*
quantum-chemistry text that consistently derives each equation
step-by-step before quoting it. Out of print from McGraw-Hill
but freely available from the Dover edition.

### 10.5 Helgaker, Jorgensen & Olsen (2000) — Molecular Electronic-Structure Theory

**T. Helgaker, P. Jørgensen, and J. Olsen**, *Molecular
Electronic-Structure Theory*, **Wiley (2000)**.

The encyclopedic reference for wavefunction-based quantum
chemistry. Covers the Hartree–Fock method, Møller–Plesset
perturbation theory, configuration interaction, coupled-cluster
theory (CCSD, CCSDT, CCSD(T)), multiconfigurational SCF
(CASSCF), and the geometry optimisation and response-theory
machinery, at a level of detail suitable for *implementing* the
methods from scratch. The book is the standard reference for
the mathematical structure of the methods, the algorithmic
details, and the benchmark calculations. Every quantum
chemist who writes production code keeps a copy of
Helgaker–Jørgensen–Olsen within arm's reach.

---

> Back to the [chapter index]({{ "/dft-notes/" | relative_url }}).
