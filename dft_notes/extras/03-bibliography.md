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

### 1.1 Hohenberg & Kohn (1964) — Inhomogeneous electron gas {#hk-1964}

**Hohenberg, P.; Kohn, W.** "Inhomogeneous Electron Gas." *Physical
Review* **1964**, *136* (3B), B864–B871. DOI:
[10.1103/PhysRev.136.B864](<https://doi.org/10.1103/PhysRev.136.B864>).
URL: <https://journals.aps.org/pr/abstract/10.1103/PhysRev.136.B864>.

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

### 1.2 Kohn & Sham (1965) — Self-consistent equations {#ks-1965}

**Kohn, W.; Sham, L. J.** "Self-Consistent Equations Including
Exchange and Correlation Effects." *Physical Review* **1965**, *140*
(4A), A1133–A1138. DOI:
[10.1103/PhysRev.140.A1133](<https://doi.org/10.1103/PhysRev.140.A1133>).
URL: <https://journals.aps.org/pr/abstract/10.1103/PhysRev.140.A1133>.

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

### 1.3 Sham & Kohn (1966) — Uniform electron gas {#sk-1966}

**Sham, L. J.; Kohn, W.** "One-Particle Properties of an
Inhomogeneous Interacting Electron Gas." *Physical Review* **1966**,
*145* (2), 561–567. DOI:
[10.1103/PhysRev.145.561](<https://doi.org/10.1103/PhysRev.145.561>).
URL: <https://journals.aps.org/pr/abstract/10.1103/PhysRev.145.561>.

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

### 1.4 Perdew & Zunger (1981) — Self-interaction correction {#pz-1981}

**Perdew, J. P.; Zunger, A.** "Self-interaction correction to
density-functional approximations for many-electron systems."
*Physical Review B* **1981**, *23* (10), 5048–5079. DOI:
[10.1103/PhysRevB.23.5048](<https://doi.org/10.1103/PhysRevB.23.5048>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.23.5048>.

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

### 1.5 Perdew & Wang (1992) — LDA parameterisation {#pw-1992}

**Perdew, J. P.; Wang, Y.** "Accurate and simple analytic
representation of the electron-gas correlation energy." *Physical
Review B* **1992**, *45* (23), 13244–13249. DOI:
[10.1103/PhysRevB.45.13244](<https://doi.org/10.1103/PhysRevB.45.13244>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.45.13244>.

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

### 1.6 Perdew, Burke & Ernzerhof (1996) — PBE {#pbe-1996}

**Perdew, J. P.; Burke, K.; Ernzerhof, M.** "Generalized Gradient
Approximation Made Simple." *Physical Review Letters* **1996**, *77*
(18), 3865–3868. DOI:
[10.1103/PhysRevLett.77.3865](<https://doi.org/10.1103/PhysRevLett.77.3865>).
URL: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.77.3865>.

Erratum: *Physical Review Letters* **1997**, *78* (7), 1396. DOI:
[10.1103/PhysRevLett.78.1396](<https://doi.org/10.1103/PhysRevLett.78.1396>).
URL: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.78.1396>.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.2
("GGA — adding the gradient"), as the canonical non-empirical
GGA; also [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.9.1
("The PBE paper: a literature deep-dive").

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

### 1.7 Sun, Ruzsinszky & Perdew (2015) — SCAN {#scan-2015}

**Sun, J.; Ruzsinszky, A.; Perdew, J. P.** "Strongly Constrained and
Appropriately Normed Semilocal Density Functional." *Physical Review
Letters* **2015**, *115* (3), 036402. DOI:
[10.1103/PhysRevLett.115.036402](<https://doi.org/10.1103/PhysRevLett.115.036402>).
URL: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.115.036402>.

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

### 2.1 Vosko, Wilk & Nusair (1980) — VWN {#vwn-1980}

**Vosko, S. H.; Wilk, L.; Nusair, M.** "Accurate spin-dependent
electron liquid correlation energies for local spin density
calculations: a critical analysis." *Canadian Journal of Physics*
**1980**, *58* (8), 1200–1211. DOI:
[10.1139/p80-159](<https://doi.org/10.1139/p80-159>).
URL: <https://doi.org/10.1139/p80-159>.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.8.2
and [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4 (as a
component of B3LYP); also [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.9.2
("The VWN paper: a literature deep-dive").

The standard closed-form parameterisation of the LSDA
correlation energy, derived from the Ceperley–Alder (1980)
quantum Monte Carlo data. The "VWN" functional (re-parameterised
"VWN5" in the 1980 erratum, and a simplified "VWN3" form) is
the most-cited LSDA correlation parameterisation in
chemistry-focused DFT codes. It enters many composite
functionals (notably B3LYP) as a component.

### 2.2 Becke (1988) — B88 exchange {#b88-1988}

**Becke, A. D.** "Density-functional exchange-energy approximation
with correct asymptotic behavior." *Physical Review A* **1988**, *38*
(6), 3098–3100. DOI:
[10.1103/PhysRevA.38.3098](<https://doi.org/10.1103/PhysRevA.38.3098>).
URL: <https://journals.aps.org/pra/abstract/10.1103/PhysRevA.38.3098>.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.2
and §5.4 (as the exchange component of BLYP and B3LYP); also
[chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.9.3
("The B88 paper: a literature deep-dive").

The B88 exchange functional was the first GGA exchange to fix
the LDA's spurious self-interaction by adding a gradient
correction that recovers the correct $-1/r$ asymptotic
behaviour of the exchange energy density. Fitted to the
exchange energies of six noble-gas atoms, B88 is the empirical
counterpart to the constraint-based PBE. It is the most widely
used GGA exchange in chemistry-focused DFT (B88-PW91, B88-LYP,
B88-P86, B3LYP).

### 2.3 Lee, Yang & Parr (1988) — LYP correlation {#lyp-1988}

**Lee, C.; Yang, W.; Parr, R. G.** "Development of the
Colle–Salvetti correlation-energy formula into a functional of the
electron density." *Physical Review B* **1988**, *37* (2), 785–789.
DOI:
[10.1103/PhysRevB.37.785](<https://doi.org/10.1103/PhysRevB.37.785>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.37.785>.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4
(as the correlation component of BLYP and B3LYP); also
[chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.9.4
("The LYP paper: a literature deep-dive").

The LYP correlation functional is derived from the
Colle–Salvetti (1975) expression for the correlation energy of
a two-electron Hartree–Fock pair density, reformulated as a
functional of the density and its Laplacian. It is purely
empirical (four parameters fit to the helium atom) and has no
LDA component — it is used as a *replacement* for the LSDA
correlation, not a correction. Combined with B88 exchange it
gives the famous "BLYP" functional, the default GGA in
pre-B3LYP computational chemistry.

### 2.4 Becke (1993) — B3LYP hybrid {#b3lyp-1993}

**Becke, A. D.** "Density-functional thermochemistry. III. The role
of exact exchange." *The Journal of Chemical Physics* **1993**, *98*
(7), 5648–5652. DOI:
[10.1063/1.464913](<https://doi.org/10.1063/1.464913>).
URL: <https://doi.org/10.1063/1.464913>.

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

### 2.5 Heyd, Scuseria & Ernzerhof (2003) — HSE {#hse-2003}

**Heyd, J.; Scuseria, G. E.; Ernzerhof, M.** "Hybrid functionals
based on a screened Coulomb potential." *The Journal of Chemical
Physics* **2003**, *118* (18), 8207–8215. DOI:
[10.1063/1.1564060](<https://doi.org/10.1063/1.1564060>).
URL: <https://doi.org/10.1063/1.1564060>.

Erratum: *The Journal of Chemical Physics* **2006**, *124* (21),
219906. DOI:
[10.1063/1.219906](<https://doi.org/10.1063/1.219906>).
URL: <https://doi.org/10.1063/1.219906>.

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

### 2.6 Tao, Perdew, Staroverov & Scuseria (2003) — TPSS meta-GGA {#tpss-2003}

**Tao, J.; Perdew, J. P.; Staroverov, V. N.; Scuseria, G. E.**
"Climbing the Density-Functional Ladder: Nonempirical
Meta–Generalized Gradient Approximation Designed for Molecules
and Solids." *Physical Review Letters* **2003**, *91* (14),
146401. DOI: [10.1103/PhysRevLett.91.146401](https://doi.org/10.1103/PhysRevLett.91.146401).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.91.146401>.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4
("Meta-GGAs") and §5.5 ("The Jacob's ladder metaphor").

The first *meta-GGA*: a functional that depends not only on
$
ho(\mathbf r)$ and $
abla
ho(\mathbf r)$ but also on the
kinetic-energy density
$    au(\mathbf r) =     frac{1}{2} \sum_i^    ext{occ} |
abla\phi_i(\mathbf r)|^2$.
TPSS satisfies 12 of the 17 known exact constraints on the
XC functional; SCAN (§1.7 above) satisfies all 17. The TPSS
exchange enhancement factor is a rational function of $p = |
abla
ho|/(2(3\pi^2)^{1/3}
ho^{4/3})$
designed to recover the fourth-order gradient expansion at
small $p$ and the uniform scaling at large $p$.

### 2.7 Perdew & Schmidt (2001) — Jacob's ladder of XC functionals {#jacobsladder-2001}

**Perdew, J. P.; Schmidt, K.** "Jacob's ladder of density
functional approximations for the exchange-correlation
energy." In *Density Functional Theory and Its Applications
to Materials*, edited by V. E. Van Doren, C. P. Alsenoy,
P. Geerlings (American Institute of Physics, Melville NY,
2001). DOI: [10.1063/1.1396675]<https://doi.org/10.1063/1.1396675>).
URL: <https://pubs.aip.org/aip/acp/article-abstract/577/1/1/822036>.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.1
("The rungs of Jacob's ladder").

The paper that introduced the "Jacob's ladder" metaphor: each
successive rung of the DFT ladder (LDA, GGA, meta-GGA, hybrid,
double-hybrid, ...) adds a new ingredient to the exchange–
correlation functional and improves the accuracy on standard
benchmarks. The hierarchy has *no top rung*; the exact XC
functional is the "last rung" but is unknown in closed form.
The metaphor is useful pedagogically because each rung can be
motivated as a *correction* to the rung below.

### 2.8 Herman, Van Dyke & Ortenburger (1969) — Gradient expansion of exchange {#hvo-1969}

**Herman, F.; Van Dyke, J. P.; Ortenburger, I. B.** "Improved
Statistical Exchange Approximation for Inhomogeneous Many-Electron
Systems." *Physical Review Letters* **1969**, *22* (16),
807–811. DOI: [10.1103/PhysRevLett.22.807](https://doi.org/10.1103/PhysRevLett.22.807).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.22.807>.

Cited in: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.2
("The gradient expansion of the GEA") and §5.3 ("Becke's
correction to LDA").

The original derivation of the *gradient expansion of exchange*
(GEA) for the slowly-varying electron gas. The GEA is the
first non-trivial correction to LDA, including the leading
$|
abla
ho|^2$ term. The GEA is *not* a usable functional
(it is negative for many atoms and has no lower bound) but it
is the mathematical starting point for the GGA family. The
Becke 1988 paper (B88, §2.2) was the first to *tame* the
gradient expansion by adding an empirical correction designed
to give the correct $-1/r$ asymptotic behaviour of exchange.

---

## 3. Many-body methods

The hierarchy of wavefunction-based methods that DFT replaces
for problems where it is too expensive. The benchmarks and
calibration points for every DFT functional are computed with
these methods.

### 3.1 Møller & Plesset (1934) — MP perturbation theory {#mp-1934}

**Møller, C.; Plesset, M. S.** "Note on an Approximation Treatment
for Many-Electron Systems." *Physical Review* **1934**, *46* (7),
618–622. DOI:
[10.1103/PhysRev.46.618](<https://doi.org/10.1103/PhysRev.46.618>).
URL: <https://journals.aps.org/pr/abstract/10.1103/PhysRev.46.618>.

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

### 3.2 Čížek (1966) — Coupled cluster {#cc-1966}

**Čížek, J.** "On the Correlation Problem in Atomic and Molecular
Systems. Calculation of Wavefunction Components in Ursell-Type
Expansion Using Quantum-Field Theoretical Methods." *The Journal of
Chemical Physics* **1966**, *45* (11), 4256–4266. DOI:
[10.1063/1.1727484](<https://doi.org/10.1063/1.1727484>).
URL: <https://doi.org/10.1063/1.1727484>.

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

### 3.3 Purvis & Bartlett (1982) — CCSD {#ccsd-1982}

**Purvis, G. D., III; Bartlett, R. J.** "A full coupled-cluster
singles and doubles model: the inclusion of disconnected triples."
*The Journal of Chemical Physics* **1982**, *76* (4), 1910–1918.
DOI:
[10.1063/1.443164](<https://doi.org/10.1063/1.443164>).
URL: <https://doi.org/10.1063/1.443164>.

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

### 3.4 Raghavachari, Trucks, Pople & Head-Gordon (1989) — CCSD(T) {#ccsdt-1989}

**Raghavachari, K.; Trucks, G. W.; Pople, J. A.; Head-Gordon, M.**
"A fifth-order perturbation comparison of electron correlation
theories." *Chemical Physics Letters* **1989**, *157* (6), 479–483.
DOI:
[10.1016/0009-2614(89)87395-6](<https://doi.org/10.1016/0009-2614(89>)87395-6).
URL: <https://doi.org/10.1016/0009-2614(89)87395-6>.

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

### 4.1 Hamann, Schlüter & Chiang (1979) — Norm-conserving pseudopotentials {#hsc-1979}

**Hamann, D. R.; Schlüter, M.; Chiang, C.** "Norm-Conserving
Pseudopotentials." *Physical Review Letters* **1979**, *43* (20),
1494–1497. DOI:
[10.1103/PhysRevLett.43.1494](<https://doi.org/10.1103/PhysRevLett.43.1494>).
URL: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.43.1494>.

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

### 4.2 Troullier & Martins (1991) — Efficient construction {#tm-1991}

**Troullier, N.; Martins, J. L.** "Efficient pseudopotentials for
plane-wave calculations." *Physical Review B* **1991**, *43* (3),
1993–2006. DOI:
[10.1103/PhysRevB.43.1993](<https://doi.org/10.1103/PhysRevB.43.1993>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.1993>.

Cited in: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.4
("Construction — Troullier-Martins and BHS") as the
preferred modern construction recipe.

The Troullier–Martins (TM) construction is the standard
high-accuracy, smooth-pseudo recipe. It parameterises the
pseudo-wavefunction inside $r_c$ as
$\phi_l(r) = r^{l+1} \exp\Bigl(\sum_{n=0}^N c_n r^{2n}\Bigr)$
with $N = 5$ or 6 polynomial coefficients, and uses six
matching conditions (value, first and second derivative at
$r_c$, plus a "kinetic-energy-conservation" condition matching
the second moment of the charge density in the core) to
determine them. The resulting pseudo is *smoother* than the
Hamann–Schlüter–Chiang (1979) form at the same accuracy, and
therefore requires a smaller plane-wave cutoff — typically
$E_\text{cut} \sim 30$–$50$ Ry for first-row atoms.

### 4.3 Vanderbilt (1990) — Ultrasoft pseudopotentials {#v-1990}

**Vanderbilt, D.** "Soft self-consistent pseudopotentials in a
generalized eigenvalue formalism." *Physical Review B* **1990**, *41*
(11), 7892–7895. DOI:
[10.1103/PhysRevB.41.7892](<https://doi.org/10.1103/PhysRevB.41.7892>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.41.7892>.

Cited in: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.6
("Ultrasoft pseudopotentials (Vanderbilt)") as the
generalisaton of the NC-PP framework to smoother
pseudopotentials.

Vanderbilt's insight is that the norm-conservation condition
can be *relaxe`d*` and replaced by a generalised overlap
operator, at the cost of a more complex formalism. The
"ultrasoft" pseudo-wavefunction is allowed to have a norm
*deficit* $\Delta Q_l = Q_l^\text{ae} - Q_l^\text{ps}$ inside
$r_c$, and the missing charge is recovered by an **augmentation
charge** that adds an atom-centred correction to the density.
The KS equations become a *generalise`d*` eigenvalue problem
$\hat H |\phi\rangle = \varepsilon \hat S |\phi\rangle$, with
$\hat S \neq \mathbf 1$. The payoff is a factor of 2–3
reduction in the required plane-wave cutoff for hard elements
(3$d$ transition metals, 4$f$ rare earths, O, N) at the same
accuracy. USPPs are the default in VASP, Quantum ESPRESSO,
and CASTEP.

### 4.4 Blöchl (1994) — PAW {#paw-1994}

**Blöchl, P. E.** "Projector augmented-wave method." *Physical Review
B* **1994**, *50* (24), 17953–17979. DOI:
[10.1103/PhysRevB.50.17953](<https://doi.org/10.1103/PhysRevB.50.17953>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.50.17953>.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
§4.10.3 and [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }})
§8.7 ("The PAW method (Blöchl)"); also the source of the
Blöchl tetrahedron integration in
[chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.11. The PAW method is the most accurate of the plane-wave
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

### 5.1 Boys (1950) — Gaussian basis functions {#boys-1950}

**Boys, S. F.** "Electronic wave functions. I. A general method of
calculation for the stationary states of any molecular system."
*Proceedings of the Royal Society of London. Series A, Mathematical
and Physical Sciences* **1950**, *200* (1063), 542–554. DOI:
[10.1098/rspa.1950.0036](<https://doi.org/10.1098/rspa.1950.0036>).
URL: <https://royalsocietypublishing.org/doi/10.1098/rspa.1950.0036>.

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

### 5.2 Hehre, Stewart & Pople (1969) — STO-nG minimal basis {#sto-ng-1969}

**Hehre, W. J.; Stewart, R. F.; Pople, J. A.** "Self-Consistent
Molecular-Orbital Methods. I. Use of Gaussian Expansions of
Slater-Type Atomic Orbitals." *The Journal of Chemical Physics*
**1969**, *51* (6), 2657–2664. DOI:
[10.1063/1.1672397](<https://doi.org/10.1063/1.1672397>).
URL: <https://doi.org/10.1063/1.1672397>.

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

### 5.3 Krishnan, Binkley, Seeger & Pople (1980) — 6-31G split-valence {#kbs-1980}

**Krishnan, R.; Binkley, J. S.; Seeger, R.; Pople, J. A.**
"Self-consistent molecular orbital methods. XX. A basis set for
correlated wave functions." *The Journal of Chemical Physics*
**1980**, *72* (1), 650–654. DOI:
[10.1063/1.438980](<https://doi.org/10.1063/1.438980>).
URL: <https://doi.org/10.1063/1.438980>.

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
with polarisation and diffuse functions (`6-31G*`, `6-31+G*`),
the Pople split-valence family dominated computational
chemistry from 1980 until the Dunning correlation-consistent
bases displaced it in the 1990s.

### 5.4 Dunning (1989) — cc-pVXZ correlation-consistent bases {#dunning-1989}

**Dunning, T. H., Jr.** "Gaussian basis sets for use in correlated
molecular calculations. I. The atoms boron through neon and
hydrogen." *The Journal of Chemical Physics* **1989**, *90* (2),
1007–1023. DOI:
[10.1063/1.456153](<https://doi.org/10.1063/1.456153>).
URL: <https://doi.org/10.1063/1.456153>.

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

### 6.1 Bloch (1929) — Bloch's theorem {#bloch-1929}

**Bloch, F.** "Über die Quantenmechanik der Elektronen in
Kristallgittern." *Zeitschrift für Physi`k*` **1929**, *52*, 555–600.
DOI:
[10.1007/BF01339455](<https://doi.org/10.1007/BF01339455>).
URL: <https://link.springer.com/article/10.1007/BF01339455>.

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

### 6.2 Kohn & Rostoker (1954) — KKR method {#kr-1954}

**Kohn, W.; Rostoker, N.** "Solution of the Schrödinger Equation in
Periodic Lattices with an Application to Metallic Lithium." *Physical
Review* **1954**, *94* (5), 1111–1120. DOI:
[10.1103/PhysRev.94.1111](<https://doi.org/10.1103/PhysRev.94.1111>).
URL: <https://journals.aps.org/pr/abstract/10.1103/PhysRev.94.1111>.

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

### 6.3 Andersen (1975) — LMTO method {#lmto-1975}

**Andersen, O. K.** "Linear methods in band theory." *Physical Review
B* **1975**, *12* (8), 3060–3083. DOI:
[10.1103/PhysRevB.12.3060](<https://doi.org/10.1103/PhysRevB.12.3060>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.12.3060>.

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

### 6.4 Monkhorst & Pack (1976) — k-point sampling {#mp-1976}

**Monkhorst, H. J.; Pack, J. D.** "Special points for Brillouin-zone
integrations." *Physical Review B* **1976**, *13* (12), 5188–5192.
DOI:
[10.1103/PhysRevB.13.5188](<https://doi.org/10.1103/PhysRevB.13.5188>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.13.5188>.

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

### 6.5 Blöchl, Jepsen & Andersen (1994) — Improved tetrahedron integration {#bja-1994}

**Blöchl, P. E.; Jepsen, O.; Andersen, O. K.** "Improved tetrahedron
method for Brillouin-zone integration." *Physical Review B* **1994**,
*49* (23), 16223–16233. DOI:
[10.1103/PhysRevB.49.16223](<https://doi.org/10.1103/PhysRevB.49.16223>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.49.16223>.

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

### 7.1 Runge & Gross (1984) — The RG theorem {#rg-1984}

**Runge, E.; Gross, E. K. U.** "Density-Functional Theory for
Time-Dependent Systems." *Physical Review Letters* **1984**, *52*
(12), 997–1000. DOI:
[10.1103/PhysRevLett.52.997](<https://doi.org/10.1103/PhysRevLett.52.997>).
URL: <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.52.997>.

Cited in: [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (planned)
and [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.3
as the source of the time-dependent Hohenberg–Kohn analogue.

The Runge–Gross theorem is the time-dependent analogue of the
Hohenberg–Kohn theorem: for a many-electron system evolving
under a time-dependent external potential $v_\text{ext}(\mathbf r,
t)$ that is *analyti`c*` in time (admits a Taylor expansion at
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

### 7.2 Casida (1995) — Linear response formulation {#casida-1995}

**Casida, M. E.** "Time-dependent density functional response theory
for molecules." In *Recent Advances in Density Functional Methods*,
Part I; **Chong, D. P., Ed.**; World Scientific: Singapore, **1995**;
pp 155–192. ISBN: 978-981-02-2442-1.
URL: <https://www.worldscientific.com/worldscibooks/10.1142/2945>.

Cited in: [chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (planned)
and indirectly through the Casida equations in
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.3. Casida's formulation is the standard linear-response TDDFT used
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

### 8.1 Hellmann (1937) — The Hellmann–Feynman theorem {#hellmann-1937}

**Hellmann, H.** *Einführung in die Quantenchemie*; **Franz Deuticke**:
Leipzig, **1937**; p 285. (No ISBN — pre-ISBN era.)

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

### 8.2 Feynman (1939) — The Feynman theorem {#feynman-1939}

**Feynman, R. P.** "Forces in Molecules." *Physical Review* **1939**,
*56* (4), 340–343. DOI:
[10.1103/PhysRev.56.340](<https://doi.org/10.1103/PhysRev.56.340>).
URL: <https://journals.aps.org/pr/abstract/10.1103/PhysRev.56.340>.

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

### 8.3 Pulay (1969) — Forces in a Gaussian basis {#pulay-1969}

**Pulay, P.** "Ab initio calculation of the force constant in
molecules." *Molecular Physics* **1969**, *17* (2), 197–204. DOI:
[10.1080/00268976900101341](<https://doi.org/10.1080/00268976900101341>).
URL: <https://doi.org/10.1080/00268976900101341>.

Cited in: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7.3
("The Pulay correction") as the source of the basis-set
correction to the Hellmann–Feynman force.

The Pulay force is the correction to the Hellmann–Feynman
formula that arises in a *finite, atom-centre`d*` basis. The
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

### 8.4 Pulay (1980) — Improved force formula and DIIS {#pulay-1980}

**Pulay, P.** "Convergence acceleration of iterative sequences. The
case of SCF iteration." *Chemical Physics Letters* **1980**, *73* (2),
393–398. DOI:
[10.1016/0009-2614(80)80396-4](<https://doi.org/10.1016/0009-2614(80>)80396-4).
URL: <https://doi.org/10.1016/0009-2614(80)80396-4>.

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

### 9.1 Born & Huang (1954) — Dynamical theory of crystal lattices {#bh-1954}

**Born, M.; Huang, K.** *Dynamical Theory of Crystal Lattices*;
**Oxford University Press (Clarendon Press)**: Oxford, **1954**;
xvi + 420 pp. (No ISBN — pre-ISBN era. Reprinted 1988.)
URL: <https://global.oup.com/academic/product/dynamical-theory-of-crystal-lattices-9780198512420>.

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
chapter 01. ### 9.2 Giannozzi, de Gironcoli, Pavone & Baroni (1991) — DFPT, Quantum ESPRESSO

**Giannozzi, P.; de Gironcoli, S.; Pavone, P.; Baroni, S.**
"Ab initio calculation of phonon dispersions in semiconductors."
*Physical Review B* **1991**, *43* (9), 7231–7242. DOI:
[10.1103/PhysRevB.43.7231](<https://doi.org/10.1103/PhysRevB.43.7231>).
URL: <https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.7231>.

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
open-source **Quantum ESPRESSO** distribution (also by
Giannozzi, de Gironcoli, Pavone, and Baroni) and of every
modern plane-wave phonon calculation.
DFPT also gives the dielectric constant, Born effective
charges, the non-linear optical susceptibility, and the
electron–phonon coupling matrix elements — all from the same
linear-response machinery.

---

## 11. Modern DFT+DMFT (the LDA+DMFT formalism and solvers)

The papers that built the *machinery* used in production
LDA+DMFT codes. Cited in [chapter 13]({{ "/dft-notes/chapter-13/" | relative_url }}) §13.10.

### 11.1 Kotliar, Savrasov, Haule, Oudovenko, Parcollet & Marianetti (2006) — the standard review {#kotliar-2006}

**Kotliar, G.; Savrasov, S. Y.; Haule, K.; Oudovenko, V. S.; Parcollet, O.; Marianetti, C.** *Electronic structure calculations with dynamical mean-field theory: A review of the LDA+DMFT approac`h*`. **Reviews of Modern Physics** **2006**, *78* (3), 865–951.
DOI: [10.1103/RevModPhys.78.865](https://doi.org/10.1103/RevModPhys.78.865).
URL: <https://link.aps.org/doi/10.1103/RevModPhys.78.865>.

The 87-page review that defined the modern LDA+DMFT formalism.
Covers the Wannier projection, the Hubbard Hamiltonian, the
double-counting correction, the Hirsch–Fye solver, and the
applications to $\alpha$-Mn, $\gamma$-Mn, $\delta$-Pu, and
the 3$d$ ferromagnets. Equation numbers in chapter 13 §13.10.1
refer to this review.

### 11.2 Haule (2007) — the CT-HYB solver {#haule-2007}

**Haule, K.** *Quantum Monte Carlo Impurity Solver for Cluster DMFT and Electronic Structure Calculations in Adjustable Base*. **Physical Review B** **2007**, *75* (15), 155113.
DOI: [10.1103/PhysRevB.75.155113](https://doi.org/10.1103/PhysRevB.75.155113).
URL: <https://link.aps.org/doi/10.1103/PhysRevB.75.155113>.

The continuous-time quantum Monte Carlo impurity solver that
is the workhorse of modern LDA+DMFT. Replaces the older
Hirsch–Fye auxiliary-field QMC and gives a continuous-time,
no-$\Delta\tau$ algorithm. The partition function is
expanded in powers of the bath hybridisation $V$.

### 11.3 Werner, Comanac, de' Medici, Troyer & Millis (2006) — the original CT-HYB {#werner-2006}

**Werner, P.; Comanac, A.; de' Medici, L.; Troyer, M.; Millis, A. J.** *Continuous-Time Solver for Quantum Impurity Models*. **Physical Review Letters** **2006**, *97* (7), 076405.
DOI: [10.1103/PhysRevLett.97.076405](https://doi.org/10.1103/PhysRevLett.97.076405).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.97.076405>.

The first CT-HYB paper, published simultaneously with Haule
2007. Slightly less general than the Haule framework but
introduces the key idea of the stochastic series expansion
in the bath hybridisation.

### 11.4 Haule, Yee & Kim (2010) — the full-potential LDA+DMFT and the force formula {#haule-2010}

**Haule, K.; Yee, C.-H.; Kim, K.** *Dynamical mean-field theory within the full-potential methods: Electronic structure of CeIrIn$_5$, CeCoIn$_5$, and CeRhIn$_5$*. **Physical Review B** **2010**, *81* (19), 195107.
DOI: [10.1103/PhysRevB.81.195107](https://doi.org/10.1103/PhysRevB.81.195107).
URL: <https://link.aps.org/doi/10.1103/PhysRevB.81.195107>.

The first full-potential LDA+DMFT implementation (no
approximations to the potential shape). Derives the
DFT+DMFT force formula (Eq. 12 of this paper, cited in
chapter 13 §13.10.1) which is required for
geometry optimisation and molecular dynamics.

### 11.5 Haule & Birol (2015) — the stationary free-energy functional {#haule-2015}

**Haule, K.; Birol, T.** *Free Energy from Stationary Implementation of the DFT+DMFT*. **Physical Review Letters** **2015**, *115* (25), 256402.
DOI: [10.1103/PhysRevLett.115.256402](https://doi.org/10.1103/PhysRevLett.115.256402).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.115.256402>.

The stationary free-energy functional (Eq. 1 of this paper)
that makes the DFT+DMFT forces well-defined. Solves a
long-standing problem in the formalism: the "naïve" energy
$E[\rho, G]$ is not stationary with respect to the
self-energy, so the Hellmann–Feynman theorem does not apply.

### 11.6 Rubtsov, Savkin & Lichtenstein (2005) — the weak-coupling CT-INT solver {#rubtsov-2005}

**Rubtsov, A. N.; Savkin, V. V.; Lichtenstein, A. I.** *Continuous-time quantum Monte Carlo method for fermions*. **Physical Review B** **2005**, *72* (3), 035122.
DOI: [10.1103/PhysRevB.72.035122](https://doi.org/10.1103/PhysRevB.72.035122).
URL: <https://link.aps.org/doi/10.1103/PhysRevB.72.035122>.

The weak-coupling CT-INT solver. Complementary to CT-HYB:
works well at small $U$ and poorly at large $U$.

### 11.7 Lichtenstein & Katsnelson (1998) — the original LDA+DMFT {#lk-1998}

**Lichtenstein, A. I.; Katsnelson, M. I.** *Ab initio calculations of the electronic structure of strongly correlated systems: LDA+U+DMFT*. **Physical Review B** **1998**, *57* (12), 6884–6895.
DOI: [10.1103/PhysRevB.57.6884](https://doi.org/10.1103/PhysRevB.57.6884).
URL: <https://link.aps.org/doi/10.1103/PhysRevB.57.6884>.

The original "LDA+U+DMFT" paper that combined the
Liechtenstein 1995 DFT+U with the Metzner–Vollhardt DMFT
self-consistency. Introduces the Wannier projection and the
double-counting correction.

### 11.8 Czyzyk & Sawatzky (1994) — the around-mean-field double counting {#cs-1994}

**Czyzyk, M. T.; Sawatzky, G. A.** *Local-density functional and on-site correlations: The electronic structure of La$_2$CuO$_4$ and LaCuO$_3$*. **Physical Review B** **1994**, *49* (20), 14211–14228.
DOI: [10.1103/PhysRevB.49.14211](https://doi.org/10.1103/PhysRevB.49.14211).
URL: <https://link.aps.org/doi/10.1103/PhysRevB.49.14211>.

The around-mean-field (AMF) double-counting formula (Eq. 17
of this paper, cited in chapter 13 §13.10.1). The alternative
to the FLL double-counting, preferred for metallic systems.

### 11.9 Yin, Haule & Kotliar (2011) — Hund's metals {#yin-2011}

**Yin, Z. P.; Haule, K.; Kotliar, G.** *Kinetic frustration and the nature of the magnetic and paramagnetic states in iron pnictides and iron chalcogenides*. **Nature Materials** **2011**, *10*, 932–935.
DOI: [10.1038/nmat3120](https://doi.org/10.1038/nmat3120).
URL: <https://www.nature.com/articles/nmat3120>.

The "Hund's metal" classification of the iron pnictides from
DFT+DMFT. The correlations in these materials are driven by
the Hund's-rule coupling $J_H$, not by the Hubbard $U$.

### 11.10 Hirsch & Fye (1986) — the older auxiliary-field solver {#hf-1986}

**Hirsch, J. E.; Fye, R. M.** *Monte Carlo Method for Magnetic Impurities in Metals*. **Physical Review Letters** **1986**, *56* (23), 2521–2524.
DOI: [10.1103/PhysRevLett.56.2521](https://doi.org/10.1103/PhysRevLett.56.2521).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.56.2521>.

The Hirsch–Fye auxiliary-field QMC impurity solver. The old
workhorse, now superseded by CT-HYB.

### 11.11 Marzari & Vanderbilt (1997) — maximally-localised Wannier functions {#mv-1997}

**Marzari, N.; Vanderbilt, D.** *Maximally localized generalized Wannier functions for composite energy bands*. **Physical Review B** **1997**, *56* (20), 12847–12865.
DOI: [10.1103/PhysRevB.56.12847](https://doi.org/10.1103/PhysRevB.56.12847).
URL: <https://link.aps.org/doi/10.1103/PhysRevB.56.12847>.

The maximally-localised Wannier function construction used
in Step 2 of the LDA+DMFT loop.

### 11.12 Biermann, Aryasetiawan & Georges (2003) — the first GW+DMFT {#bag-2003}

**Biermann, S.; Aryasetiawan, F.; Georges, A.** *First-principles calculation of the electronic structure of the strongly correlated system $\alpha$-MnS*. **Physical Review Letters** **2003**, *90* (8), 086402.
DOI: [10.1103/PhysRevLett.90.086402](https://doi.org/10.1103/PhysRevLett.90.086402).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.90.086402>.

The first GW+DMFT calculation. Captures both the non-local
screening (from GW) and the local strong correlations (from DMFT).

### 11.13 Rohringer et al. (2018) — diagrammatic extensions of DMFT {#rohringer-2018}

**Rohringer, G.; Hafermann, H.; Toschi, A.; Katanin, A. A.; Antipov, A. E.; Buser, M. I.; Tomczak, J. M.; Thunström, P.; Held, K.; Lombardo, L.; Valli, R.; Toschi, A.; Held, K.** *Diagrammatic routes to non-local correlations beyond dynamical mean field theory*. **Reviews of Modern Physics** **2018**, *90* (2), 025003.
DOI: [10.1103/RevModPhys.90.025003](https://doi.org/10.1103/RevModPhys.90.025003).
URL: <https://link.aps.org/doi/10.1103/RevModPhys.90.025003>.

The modern review of diagrammatic extensions of DMFT (DCA,
CDMFT, dual fermion, etc.). Cited in chapter 13 §13.10.5.

### 11.14 Freericks, Turkowski & Zlatić (2006) — non-equilibrium DMFT {#ftz-2006}

**Freericks, J. K.; Turkowski, V. M.; Zlatić, V.** *Nonequilibrium dynamical mean-field theory*. **Physical Review Letters** **2006**, *97* (26), 266408.
DOI: [10.1103/PhysRevLett.97.266408](https://doi.org/10.1103/PhysRevLett.97.266408).
URL: <https://link.aps.org/doi/10.1103/PhysRevLett.97.266408>.

The Keldysh-DMFT formalism for non-equilibrium. Cited in
chapter 13 §13.10.5.

### 11.15 Held (2000) — the LDA+DMFT energy formula {#held-2000}

**Held, K.; Nekrasov, I. A.; Keller, G.; Eyert, V.; Oudovenko, V. S.; Kunes, J.; McMahan, A. K.; Scalettar, R. T.; Albers, R. C.; Anisimov, V. I.; Lichtenstein, A. I.** *Mott transition in paramagnetic V$_2$O$_3$ within LDA+DMFT*. **2000**, lecture notes and the standard reference for the LDA+DMFT total energy formula.
URL: <https://arxiv.org/abs/cond-mat/0112078>.

The Mott transition in V$_2$O$_3$ as the textbook example
of the LDA+DMFT methodology. The 2006 RMP review by Kotliar
et al. above superseded this for the formalism.

---
## 10. Standard textbooks

The five monographs that should sit on the shelf of anyone
working in electronic-structure theory. They are not cited in
the chapters directly — the chapters are self-contained — but
they are the *next ste`p*` after these notes for a reader who
wants the full mathematical apparatus, the historical context,
or the production-code perspective.

### 10.1 Parr & Yang (1989) — Density-Functional Theory of Atoms and Molecules {#parryang-1989}

**Parr, R. G.; Yang, W.** *Density-Functional Theory of Atoms and
Molecules*; **Oxford University Press**: New York, **1989**; ix +
333 pp. ISBN: 978-0-19-509276-9 (paperback) / 0-19-504279-4
(hardcover).
URL: <https://global.oup.com/academic/product/density-functional-theory-of-atoms-and-molecules-9780195092769>.

A monograph written from the chemistry perspective. Covers the
Hohenberg–Kohn theorem, the Kohn–Sham equations, the L(S)DA,
the connection to chemical concepts (chemical potential,
hardness, Fukui functions, electronegativity equalisation), and
the early GGAs. The book is the *bridge* between the physics
of the KS equations and the language of conceptual DFT that
chemists use. It assumes only an undergraduate background in
quantum mechanics and is the most accessible entry in this
section.

### 10.2 Martin (2004) — Electronic Structure {#martin-2004}

**Martin, R. M.** *Electronic Structure: Basic Theory and Practical
Methods*; **Cambridge University Press**: Cambridge, UK, **2004**;
xxi + 640 pp. ISBN: 978-0-521-78285-6 (paperback) /
0-521-78285-6 (hardcover).
URL: <https://www.cambridge.org/9780521782856>.

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

### 10.3 Dreizler & Gross (1990) — Density Functional Theory {#dg-1990}

**Dreizler, R. M.; Gross, E. K. U.** *Density Functional Theory: An
Approach to the Quantum Many-Body Problem*; **Springer-Verlag**:
Berlin, **1990**; xii + 302 pp. ISBN: 978-3-540-51991-7 /
3-540-51991-1.
URL: <https://link.springer.com/book/10.1007/978-3-642-86105-5>.

The first comprehensive DFT textbook, written from the
many-body physics perspective. Covers the Hohenberg–Kohn
theorem and its extensions (spin DFT, current DFT, time
dependent), the Kohn–Sham equations, the L(S)DA and its
limitations, the early GGAs, and the time-dependent formalism
(Runge–Gross, linear response, the Casida equations). More
mathematical than Parr–Yang, more physics-oriented than
Martin; the standard reference on the formal side of DFT.

### 10.4 Szabo & Ostlund (1989) — Modern Quantum Chemistry {#szabo-1989}

**Szabo, A.; Ostlund, N. S.** *Modern Quantum Chemistry: Introduction
to Advanced Electronic Structure Theory*; **McGraw-Hill**: New York,
**1989**; xv + 466 pp. ISBN: 0-07-062739-8 (1st ed.). Revised Dover
edition: *Dover Publications*: Mineola, NY, **1996**; 480 pp.
ISBN: 978-0-486-69186-2.
URL: <https://store.doverpublications.com/9780486691862.html>.

The standard introduction to *wavefunction-base`d*` quantum
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

### 10.5 Helgaker, Jorgensen & Olsen (2000) — Molecular Electronic-Structure Theory {#hjo-2000}

**Helgaker, T.; Jørgensen, P.; Olsen, J.** *Molecular
Electronic-Structure Theory*; **John Wiley & Sons**: Chichester, UK,
**2000**; xiv + 908 pp. ISBN: 978-0-471-96755-3 / 0-471-96755-6.
URL: <https://www.wiley.com/en-us/Molecular+Electronic+Structure+Theory-p-9780471967553>.

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
