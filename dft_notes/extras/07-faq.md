---
layout: page
title: "FAQ — DFT Notes"
permalink: /dft-notes/extras/faq/
description: >-
  Frequently asked questions about Density Functional Theory, with
  short, opinionated answers and cross-references to the relevant
  chapters in the DFT Notes.  Topics: foundations, mathematics,
  practical calculations, common pitfalls, and software.  Every answer
  links into the chapter or python_codes file that develops the
  underlying idea in full.
keywords: "DFT, FAQ, frequently asked, exchange correlation, basis set,
  SCF, band gap, convergence, VASP, Quantum ESPRESSO, GPAW, SIESTA,
  pseudopotential, PAW, k-points, geometry optimisation, smearing,
  self-consistent"
---

# FAQ — DFT Notes

> A working FAQ for readers who have just opened these notes and
> want a *short* answer before they commit to a chapter.  Every
> entry is self-contained: one question, one answer, and a list of
> cross-references.  Click a question to reveal the answer; click
> again to hide it.

This page is *not* a substitute for the chapters.  It is a
**look-up table** for the questions a new reader actually asks —
in lectures, in group meetings, in the first week of a project.
The answers are deliberately concise (50–200 words) and
opinionated; for the derivations, the proofs, and the working
code, follow the cross-references.

> **Conventions.**  Atomic units
> ($\hbar = m_e = e = 4\pi\varepsilon_0 = 1$) are used throughout,
> matching the
> [notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }})
> and the
> [math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}).
> Lengths are in Bohr ($a_0 \approx 0.529177\,\text{Å}$); energies
> in Hartree ($E_h \approx 27.2114\,\text{eV}$).

## How to read this page

Every question is wrapped in a `<details>` block.  Click the
question to reveal the answer; click again to hide it.  Use the
table of contents below to jump to a section.  If your question
is **not** here, try the
[notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}),
the [math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}),
the [software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}),
the [worked examples]({{ "/dft-notes/extras/worked-examples/" | relative_url }}),
or the [problems anthology]({{ "/dft-notes/extras/problems/" | relative_url }}).
File an issue against `agent:docs-keeper` (see
[`agents.md`]({{ "/agents.html" | relative_url }}) for the
contract) if it is still not there.

## Table of contents

- **A. Foundations** — what DFT is, what a wavefunction is, why the
  Schrödinger equation is hard, the Born–Oppenheimer approximation,
  and the "ab initio" / "first-principles" distinction.
- **B. Mathematics** — Dirac notation, Slater determinants, the
  density, basis sets, "self-consistent", functionals, and the
  Hohenberg–Kohn theorem.
- **C. Practical** — how to choose an XC functional and a basis
  set, how to converge a calculation, k-points, pseudopotentials,
  band structures, DOS, geometry optimisation vs. MD, and smearing.
- **D. Common pitfalls** — band-gap underestimation, k-point
  non-convergence, oscillating optimisations, noisy forces, and
  inter-code disagreement.
- **E. Software** — which code, the VASP licence, free compute
  resources, and PAW vs. pseudopotential.

---

## A. Foundations

The "what is this all about" questions.  Read these first if you
have never taken a quantum-mechanics course.

### A.1 — What is DFT, in one paragraph?

<details>
<summary><strong>A.1 — What is DFT, in one paragraph?</strong></summary>

Density Functional Theory is a *reformulation* of quantum
mechanics that uses the one-electron density
\(\rho(\mathbf r)\) — a real, positive, three-dimensional scalar
field — as the fundamental variable, instead of the many-body
wavefunction \(\Psi(\mathbf r_1, \dots, \mathbf r_N)\).  The
Hohenberg–Kohn theorem (1964) proves that the ground-state
energy of a many-electron system is a *unique functional* of
\(\rho(\mathbf r)\); the Kohn–Sham construction (1965) turns
that existence proof into a *practical algorithm* by introducing
an auxiliary non-interacting system whose density equals the
true interacting density.  In Kohn–Sham DFT, the central
equation is

\begin{equation}
\label{eq:faq-ks}
\left[-\tfrac{1}{2}\nabla^2 + v_\text{ext}(\mathbf r) + v_\text{H}[\rho](\mathbf r) + v_\text{xc}[\rho](\mathbf r)\right] \phi_i(\mathbf r) = \varepsilon_i\, \phi_i(\mathbf r) ,
\end{equation}

a set of one-electron Schrödinger-like equations solved
self-consistently.  DFT in the Kohn–Sham form is the workhorse
of modern computational chemistry and materials science because
it offers a favourable cost–accuracy trade-off for systems with
tens to thousands of electrons.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1–4.2; [Chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }}) — "What is DFT in 200 words"
</details>

### A.2 — What is a "wavefunction" and why do we need it?

<details>
<summary><strong>A.2 — What is a "wavefunction" and why do we need it?</strong></summary>

The wavefunction \(\Psi(\mathbf r_1, \dots, \mathbf r_N)\) is the
object in quantum mechanics that *encodes everything knowable
about a many-electron system*.  By the Born rule, \(|\Psi|^2\)
gives the joint probability density for finding electron 1 at
\(\mathbf r_1\), electron 2 at \(\mathbf r_2\), and so on.  The
wavefunction lives in a \(3N\)-dimensional configuration space
(one \(\mathbb R^3\) per electron); for \(N = 100\) that is 300
real numbers per grid point — vastly more than any computer
can store.  All measurable quantities are expectation values
\(\langle \hat A \rangle = \langle \Psi \rvert \hat A \rvert \Psi \rangle\);
the wavefunction evolves under the time-dependent Schrödinger
equation.  DFT's big theoretical move is to *avoid* the
wavefunction and work with the one-electron density
\(\rho(\mathbf r)\) instead, which lives in ordinary 3-D space
and is enormously cheaper to store and manipulate.

**See:** [Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) §1.1–1.2; [Notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}) §3
</details>

### A.3 — Why is the Schrödinger equation so hard to solve for atoms and molecules?

<details>
<summary><strong>A.3 — Why is the Schrödinger equation so hard to solve for atoms and molecules?</strong></summary>

The time-independent Schrödinger equation
\(\hat H \Psi = E \Psi\) for \(N\) electrons and \(M\) nuclei
is a *linear eigenvalue problem* in a \(3N\)-dimensional space.
Three things make it hard:

1. **Dimensionality.**  The wavefunction is a function of
   \(3N\) coordinates; storing it on a grid is infeasible past
   \(N \approx 10\) electrons.
2. **The electron–electron repulsion**
   \(\hat V_{ee} = \sum_{i<j} 1/r_{ij}\) is *non-separable*: you
   cannot write the wavefunction as a product of one-electron
   factors without losing essential correlation physics.  This
   is the "many-body problem" of
   [Chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}).
3. **The exchange–correlation physics is non-local** in subtle
   ways.  The exact functional of DFT is unknown; the
   approximate functionals (LDA, GGA, hybrid, …) of
   [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }})
   are the workarounds, and they are not always accurate.

For one electron and one proton (the hydrogen atom) the
equation *is* separable and has a closed-form solution; for
anything bigger, approximation is unavoidable.

**See:** [Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) §1.1, §1.10; [Chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.1
</details>

### A.4 — What is the Born–Oppenheimer approximation?

<details>
<summary><strong>A.4 — What is the Born–Oppenheimer approximation?</strong></summary>

The Born–Oppenheimer (BO) approximation **decouples the
electrons from the nuclei** by exploiting the fact that a
proton is ~1836 times heavier than an electron, so the
electrons move *much* faster.  The approximation treats the
nuclei as classical, point-like, *fixed* sources of an external
potential \(v_\text{ext}(\mathbf r) = -\sum_A Z_A / |\mathbf r -
\mathbf R_A|\); the electronic Schrödinger equation is then
solved for each nuclear geometry \(\{\mathbf R_A\}\) separately.
The electronic energy \(E_\text{el}(\{\mathbf R_A\})\) becomes
the *potential energy surface* on which the nuclei move; the
nuclear Schrödinger equation (or, classically, Newton's second
law) is solved on that surface.  The approximation is *very*
good for ground-state properties: the residual
electron–nuclear coupling is small, and corrections can be
added perturbatively if needed.  It is *less* good when two
potential-energy surfaces come close together (conical
intersections, Jahn–Teller systems, some excited states), where
the non-adiabatic coupling becomes large.

**See:** [Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) §1.1 (footnote on BO); [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7
</details>

### A.5 — What's the difference between "ab initio" and "first-principles"?

<details>
<summary><strong>A.5 — What's the difference between "ab initio" and "first-principles"?</strong></summary>

In practice, **the two terms mean the same thing** in the
context of electronic-structure theory: a calculation that
takes only the atomic numbers and positions as input — no
empirical parameters, no fitted data, no adjustable parameters.
"Ab initio" is the older term, popular in quantum chemistry;
"first-principles" is the term preferred in condensed-matter
physics and materials science.  DFT, Hartree–Fock, coupled
cluster, quantum Monte Carlo, and $GW$ are all "ab initio" /
"first-principles" methods; tight-binding and force-field
methods are *not*.  DFT in particular is sometimes called
"first-principles DFT" to emphasise that the *only* empirical
input is the choice of XC functional — and even that is a
controlled, systematically improvable approximation, not a
fitted parameter.  When you see the phrase "from first
principles" in a paper, the author is telling you that no
experimental data was used beyond the atomic numbers.

**See:** [Chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }}) — "What is in scope"; [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.0
</details>

### A.6 — Why is DFT called a "theory" if we still need to pick a functional?

<details>
<summary><strong>A.6 — Why is DFT called a "theory" if we still need to pick a functional?</strong></summary>

Strictly speaking, the *theory* is exact: the Hohenberg–Kohn
theorem and the Kohn–Sham construction together prove that,
for any external potential, there exists a universal
functional \(F[\rho]\) whose minimum gives the exact
ground-state energy and density.  The *approximation* is
entirely in the choice of \(E_\text{xc}[\rho]\), the
exchange–correlation part of that functional.  DFT in this
sense is "exact in principle but approximate in practice" —
the same status as the Schrödinger equation, which is also
exact in principle but never solved exactly for more than two
particles.  The systematic improvement of
\(E_\text{xc}[\rho]\) is the subject of "Jacob's ladder" of
[Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}):
each rung (LDA → GGA → meta-GGA → hybrid → double hybrid)
adds more ingredients and brings you systematically closer to
the exact functional, at a systematically higher cost.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1, §4.2; [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.0
</details>

### A.7 — What kinds of problems can DFT solve (and which can't it)?

<details>
<summary><strong>A.7 — What kinds of problems can DFT solve (and which can't it)?</strong></summary>

DFT (Kohn–Sham) is good for: **ground-state geometries** of
molecules, solids, surfaces; **vibrational frequencies** (from
finite differences or DFPT); **elastic constants and moduli**;
**relative energies** of similar configurations (adsorption
sites, polymorphs, reaction paths); **band structures and DOS**
of semiconductors and metals (with caveats on the gap);
**charge densities, dipoles, ESPs** for qualitative chemistry.
DFT is *less good* for: **band gaps** of semiconductors and
insulators (typically 30–50 % too small with semilocal
functionals, fixable with hybrids or $GW$); **weak
interactions** (van der Waals / dispersion — needs a
correction); **strongly correlated electrons** (Mott
insulators, multi-centre transition-metal complexes — often
needs DFT+U or embedding); **excited states** (needs TDDFT or
beyond); **reaction barriers** (often ±3–5 kcal/mol; CCSD(T)
is the gold standard); **thermochemistry of large molecules**
(needs a hybrid or double-hybrid for chemical accuracy).

**See:** [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.7; [Chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}); [Chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }})
</details>

---

## B. Mathematics

The "what does this symbol mean" questions.  Open
[Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) in
parallel if you are reading for the first time; these answers
are the short form of the chapter's notation.

### B.1 — What does \(\langle \phi \rvert \hat A \rvert \psi \rangle\) mean?

<details>
<summary><strong>B.1 — What does \(\langle \phi \rvert \hat A \rvert \psi \rangle\) mean?</strong></summary>

It is the **matrix element of the operator \(\hat A\) between
two states \(\phi\) and \(\psi\)** in Dirac's bra–ket notation.
The ket \(\rvert \psi \rangle\) is a vector in the Hilbert
space; the bra \(\langle \phi \rvert\) is the dual vector
(linear functional) of \(\rvert \phi \rangle\); the operator
\(\hat A\) sits in between and acts on \(\rvert \psi \rangle\).
The full expression is read right-to-left:
\(\hat A \rvert \psi \rangle\) produces a new state, which is
then inner-producted with \(\langle \phi \rvert\).  In
position-space representation it is the integral

\begin{equation}
\label{eq:faq-brak}
\langle \phi \rvert \hat A \rvert \psi \rangle \;\equiv\; \int \phi^*(\mathbf r)\, \bigl(\hat A \psi(\mathbf r)\bigr)\, d\mathbf r .
\end{equation}

When \(\phi = \psi\) this is the **expectation value** of
\(\hat A\) in the state \(\rvert \psi \rangle\); when
\(\hat A = \hat{\mathbf 1}\) it is the **inner product**
\(\langle \phi \rvert \psi \rangle\).  Every Fock-matrix
element \(F_{\mu\nu} = \langle \chi_\mu \rvert \hat F \rvert
\chi_\nu \rangle\) in
[Chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) is
an instance of this notation.

**See:** [Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) §1.2; [Math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}) §1
</details>

### B.2 — What is a Slater determinant, and why do we use it?

<details>
<summary><strong>B.2 — What is a Slater determinant, and why do we use it?</strong></summary>

A **Slater determinant** is an antisymmetrised product of
\(N\) orthonormal single-particle spin-orbitals
\(\chi_i(\mathbf x)\):

\begin{equation}
\label{eq:faq-slater}
\Psi(\mathbf x_1, \dots, \mathbf x_N) \;=\; \frac{1}{\sqrt{N!}} \begin{vmatrix}
\chi_1(\mathbf x_1) & \chi_2(\mathbf x_1) & \cdots & \chi_N(\mathbf x_1) \\
\chi_1(\mathbf x_2) & \chi_2(\mathbf x_2) & \cdots & \chi_N(\mathbf x_2) \\
\vdots & \vdots & \ddots & \vdots \\
\chi_1(\mathbf x_N) & \chi_2(\mathbf x_N) & \cdots & \chi_N(\mathbf x_N)
\end{vmatrix} .
\end{equation}

The determinant form **enforces the Pauli exclusion principle
automatically**: swapping two rows flips the sign, so \(\Psi\)
changes sign under particle exchange, which is what "fermions
are antisymmetric" means.  It also gives a clean route to the
*exact* exchange that the Hartree–Fock method builds on.  In
Kohn–Sham DFT we use a Slater determinant **even though the
true wavefunction is not a single determinant**, because the
determinant is just the Ansatz for the auxiliary non-interacting
system that reproduces the interacting density.  The
determinant form makes the kinetic energy \(T_s\) and the
Hartree energy \(J[\rho]\) tractable.

**See:** [Chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) §2.2; [Chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.1; [Math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}) §4
</details>

### B.3 — What's the difference between \(\Psi\) and \(\psi\)?

<details>
<summary><strong>B.3 — What's the difference between \(\Psi\) and \(\psi\)?</strong></summary>

Capital \(\Psi(\mathbf r_1, \dots, \mathbf r_N)\) is the
**many-body wavefunction**: a function of \(N\) electronic
coordinates (and \(N\) spin labels).  Lower-case \(\psi_i(\mathbf
r)\) is a **single-particle orbital**: a function of *one*
electronic coordinate (and one spin).  In Kohn–Sham DFT the
many-body wavefunction is approximated by a Slater determinant
of single-particle orbitals:

\begin{equation}
\label{eq:faq-Psipsi}
\Psi(\mathbf x_1, \dots, \mathbf x_N) \;\approx\; \Phi[\{\psi_i\}] \;=\; \frac{1}{\sqrt{N!}} \det\bigl[\psi_i(\mathbf x_j)\bigr] .
\end{equation}

The mapping \(\Psi \to \{\psi_i\}\) is the Kohn–Sham Ansatz.
In the Kohn–Sham equations the \(\{\psi_i(\mathbf r)\}\) are
the eigenvectors (orbitals) and the \(\{\varepsilon_i\}\) are
the eigenvalues (orbital energies).  When a chapter uses the
bare symbol \(\psi\) with no index, it usually means "some
specific orbital in some specific context" — read the
surrounding paragraph to find out which one.

**See:** [Notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}) §3; [Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) §1.1
</details>

### B.4 — What is the density \(\rho(\mathbf r)\) and how is it related to the wavefunction?

<details>
<summary><strong>B.4 — What is the density \(\rho(\mathbf r)\) and how is it related to the wavefunction?</strong></summary>

The **one-electron density** is the integral of \(|\Psi|^2\)
over all electron coordinates but one, summed over spins:

\begin{equation}
\label{eq:faq-rho}
\rho(\mathbf r) \;=\; N \sum_{\sigma_1, \dots, \sigma_N} \int \lvert \Psi(\mathbf r, \sigma_1, \mathbf r_2, \sigma_2, \dots, \mathbf r_N, \sigma_N) \rvert^2 d\mathbf r_2 \cdots d\mathbf r_N .
\end{equation}

It is a non-negative, real, three-dimensional scalar field
that integrates to the number of electrons:
\(\int \rho(\mathbf r)\, d\mathbf r = N\).  Its physical
content is the *marginal* probability density for finding
*any* electron at \(\mathbf r\); the prefactor \(N\) comes
from summing over the \(N\) equivalent choices of "which
electron is at \(\mathbf r\)".  In a Slater-determinant
Ansatz the density simplifies to
\(\rho(\mathbf r) = \sum_{i=1}^N |\phi_i(\mathbf r)|^2\)
(closed shell: double that with a factor of 2).  The
Hohenberg–Kohn theorem guarantees that \(\rho(\mathbf r)\)
contains *exactly* the same information as \(\Psi\) for the
ground state — they are in one-to-one correspondence.

**See:** [Chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) §1.6; [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1
</details>

### B.5 — What's a basis set?

<details>
<summary><strong>B.5 — What's a basis set?</strong></summary>

A **basis set** is a finite set of known functions
\(\{\chi_\mu(\mathbf r)\}\) used to expand the unknown
molecular orbitals:

\begin{equation}
\label{eq:faq-basis}
\phi_i(\mathbf r) \;\approx\; \sum_{\mu=1}^{K} C_{\mu i}\, \chi_\mu(\mathbf r) .
\end{equation}

The choice of basis set controls both the **accuracy** and
the **cost** of the calculation.  Two main families: (i)
**localised atomic-orbital bases** (Gaussians, Slater-type
orbitals, numerical atomic orbitals) — used for molecules;
(ii) **delocalised plane-wave bases** — used for periodic
solids.  A *complete* basis is infinite; in practice the
expansion is truncated at some \(K\), and the basis-set
incompleteness error is the dominant source of error in many
production calculations.  The plane-wave basis is
*systematically improvable* (one knob: the cutoff energy
\(E_\text{cut}\)); the Gaussian basis is *not* (one has to
climb the Pople or Dunning ladder).

**See:** [Chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.1–6.8; [Notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}) §6
</details>

### B.6 — What does "self-consistent" mean?

<details>
<summary><strong>B.6 — What does "self-consistent" mean?</strong></summary>

The Kohn–Sham potential depends on the density, and the
density is built from the Kohn–Sham orbitals, which are the
eigenvectors of the Kohn–Sham Hamiltonian.  So the problem
has a **circular dependency**: density \(\to\) potential
\(\to\) Hamiltonian \(\to\) orbitals \(\to\) density.  A
calculation is **self-consistent** when the density that
comes *out* of one diagonalisation equals (within tolerance)
the density that was used to build the Hamiltonian.  In
practice, the SCF loop is iterated until convergence:

\begin{equation}
\label{eq:faq-scf}
\rho^{(n+1)}(\mathbf r) \;=\; \mathcal F[\rho^{(n)}](\mathbf r) ,
\qquad \rho^{(n+1)} \approx \rho^{(n)} .
\end{equation}

The map \(\mathcal F\) is the **SCF map**; its fixed point is
the self-consistent solution.  Convergence can be
*accelerated* by density mixing (Pulay, Broyden, DIIS); see
[Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
§4.6.  "SCF" stands for "self-consistent field" — a
historical name from the Hartree–Fock days.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6; [Chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.6
</details>

### B.7 — What is a "functional"?

<details>
<summary><strong>B.7 — What is a "functional"?</strong></summary>

A **functional** is a map from a *function* to a *number* (or
to another function).  For example, the Kohn–Sham total
energy is a functional of the density:

\begin{equation}
\label{eq:faq-func}
E[\rho] \;=\; T_s[\rho] + \int \rho(\mathbf r)\, v_\text{ext}(\mathbf r)\, d\mathbf r + J[\rho] + E_\text{xc}[\rho] .
\end{equation}

Each term is itself a functional: \(T_s[\rho]\) returns a
number given a function \(\rho\); \(J[\rho]\) returns a
number; \(E_\text{xc}[\rho]\) returns a number.  The
fundamental derivative of a functional is the **functional
derivative** \(\delta F / \delta \rho(\mathbf r)\), defined
implicitly by \(\delta F = \int (\delta F / \delta \rho(\mathbf
r))\, \delta\rho(\mathbf r)\, d\mathbf r\); the Kohn–Sham
effective potential is exactly
\(v_\text{xc}(\mathbf r) = \delta E_\text{xc} / \delta \rho(\mathbf r)\).
A "functional" is *not* the same as a "function": a function
takes numbers, a functional takes functions.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.2; [Math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}) §11
</details>

### B.8 — What is the Hohenberg–Kohn theorem actually saying?

<details>
<summary><strong>B.8 — What is the Hohenberg–Kohn theorem actually saying?</strong></summary>

The Hohenberg–Kohn (HK) theorem, in two parts:

**(1) Existence.**  The ground-state density
\(\rho(\mathbf r)\) of a many-electron system in an external
potential \(v_\text{ext}(\mathbf r)\) *uniquely determines*
that potential (up to an additive constant).  Consequently,
\(\rho\) determines the full Hamiltonian, the full
wavefunction, and the ground-state energy.  The map
\(v_\text{ext} \to \rho\) is invertible.

**(2) Variational principle.**  The ground-state energy is
obtained by minimising the energy functional
\(E_v[\rho] = F_\text{HK}[\rho] + \int \rho v_\text{ext}\,
d\mathbf r\) over all \(v\)-representable densities; the
minimiser is the exact ground-state density.

The HK theorem is an *existence proof*; it does not give a
recipe for the functional \(F_\text{HK}[\rho]\).  The Kohn–
Sham construction is the practical realisation: it replaces
the *unknown* functional \(F_\text{HK}\) by an *exactly known*
non-interacting kinetic energy \(T_s\) plus a small
correction \(E_\text{xc}[\rho]\) that absorbs everything
unknown.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1; [Chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }}) — "What is DFT in 200 words"
</details>

---

## C. Practical

The "how do I actually run a calculation" questions.  This is
the section to read before you start a project.

### C.1 — How do I choose an XC functional?

<details>
<summary><strong>C.1 — How do I choose an XC functional?</strong></summary>

A short, opinionated guide:

| Functional | Use it for | Don't use it for |
|:-----------|:-----------|:-----------------|
| **LDA** | Quick sanity check; metals; pedagogical baselines | Quantitative chemistry (gaps, thermochemistry) |
| **PBE** (GGA) | Mainstream solids, geometries, phonons | Band gaps; thermochemistry of molecules |
| **PBEsol** | Lattice parameters of solids | Molecules |
| **SCAN** (meta-GGA) | Improved geometries, formation energies | Needs dispersion (use SCAN+rVV10) |
| **PBE0 / HSE06** (hybrid) | Band gaps, defect levels, semiconductors | Very large supercells; Mott insulators |
| **B3LYP** (hybrid) | Mainstream molecular thermochemistry | Solids (use a periodic code) |
| **M06-2X** | Main-group thermochemistry, non-covalent interactions | Transition metals |

The default for a *new project* is PBE for solids, PBE0 or
B3LYP for molecules.  Always **report the functional you used**
— and report the convergence parameters (cutoff, mesh,
tolerance) in the same sentence.

**See:** [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.0–5.6; [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
</details>

### C.2 — How do I choose a basis set?

<details>
<summary><strong>C.2 — How do I choose a basis set?</strong></summary>

For **molecules** (Gaussian codes — PySCF, Psi4, ORCA, Q-Chem,
Gaussian): start with **def2-SVP** for screening; for
publication, climb to **def2-TZVP** or **def2-QZVP**; for
non-covalent interactions, add a **-D3** dispersion correction
to a triple-zeta; for very high accuracy, use **aug-cc-pVTZ**
(Dunning) with CBS extrapolation.

For **solids** (plane-wave codes — VASP, Quantum ESPRESSO,
CASTEP, ABINIT): the only knob is the **kinetic-energy
cutoff \(E_\text{cut}\)**.  Converge the total energy to
your target tolerance (typically 1 meV/atom) and the stress
to ~0.1 kbar.  **Pseudopotential** files have a *recommended
minimum cutoff*; use that as a starting point and converge
*upwards*.  For structures that need empty / high-energy
states (DOS, band structure), also converge the **augmentation
cutoff** (PAW) and the **number of bands**.

Always **check for basis-set superposition error (BSSE)** in
weakly-bound complexes — counterpoise correction.

**See:** [Chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.9 (GTOs), §6.10–6.11 (plane waves); [Notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}) §6
</details>

### C.3 — How do I converge a calculation?

<details>
<summary><strong>C.3 — How do I converge a calculation?</strong></summary>

Convergence means the *quantity you care about* stops changing
as you tighten the numerical parameters.  Recipe:

1. **Pick a target tolerance.**  E.g. total energy to
   0.1 meV/atom, forces to 10 meV/Å, stress to 0.1 kbar.
2. **Vary one parameter at a time**, in this order:
   molecules: basis set, then integration grid, then SCF
   tolerance; solids: k-point mesh, then plane-wave cutoff,
   then smearing width, then SCF tolerance.
3. **Plot the quantity vs. parameter** on a log scale; pick
   the value at which the curve plateaus *and* is still
   affordable.  A monotonic improvement without a plateau
   means you are not yet converged.
4. **Add a safety margin**: take the smallest converged
   value, multiply the cutoff by 1.2–1.5×, verify the
   quantity doesn't move.

The most common mistake is to converge the *total energy* and
not the *property of interest*.  A calculation can be
converged to 1 μHartree in energy and still be 50 meV/Å off
on the forces (because the *gradient* of the unconverged
quantity is not converged at the same point).

**See:** [Chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6; [Chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.11; [Worked examples]({{ "/dft-notes/extras/worked-examples/" | relative_url }})
</details>

### C.4 — What does "k-point sampling" mean, and when do I need it?

<details>
<summary><strong>C.4 — What does "k-point sampling" mean, and when do I need it?</strong></summary>

For a **periodic** system (crystal, surface, polymer), Bloch's
theorem forces the orbitals to be labelled by a crystal
momentum \(\mathbf k\) in the first Brillouin zone.  The
Kohn–Sham equations need to be solved at *every* \(\mathbf k\)
— but there are infinitely many, so we sample the BZ on a
discrete mesh (Monkhorst–Pack, \(\Gamma\)-centred).  A finer
mesh \(\to\) better-sampled BZ integrals (Fermi surface, DOS)
and a more converged total energy.  **Rules of thumb:**

- **Metals** need *many* k-points (the integrand is
  discontinuous at the Fermi surface); start with
  \(20 \times 20 \times 20\) or denser.
- **Semiconductors / insulators** need *fewer* k-points (the
  integrand is smooth in the gap); \(6 \times 6 \times 6\) is
  often enough.
- **Molecules / clusters** in a box need *only* the
  \(\Gamma\) point; the box is a finite system.
- **Band structures** are *not* a uniform BZ integration;
  they are a path through high-symmetry points.

Always converge the **k-point density** (k-points per
reciprocal Ångström) rather than the *number* of k-points,
since the latter depends on the cell size.

**See:** [Chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6, §7.7; [Chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }})
</details>

### C.5 — What's a pseudopotential and why do I need one?

<details>
<summary><strong>C.5 — What's a pseudopotential and why do I need one?</strong></summary>

A **pseudopotential** replaces the strong nuclear Coulomb
potential and the tightly-bound core electrons by a weaker,
effective potential that reproduces the *valence*
wavefunction outside a cutoff radius \(r_c\).  The reasons
to use one are practical: the valence wavefunction is smooth
(no radial nodes from the core), so it can be expanded in a
*small* plane-wave basis; relativistic effects
(mass–velocity, Darwin, spin–orbit) can be folded into the
pseudopotential; the frozen-core approximation is excellent
for most ground-state properties (the core does not change
much between atoms, molecules, and solids).  The three main
flavours: **norm-conserving** (Hamann, Troullier–Martins),
**ultrasoft** (Vanderbilt), and **PAW** (Blöchl).  PAW is
technically not a pseudopotential — it is a *transformation*
that recovers the all-electron wavefunction inside \(r_c\) —
but it is used the same way.  Pseudopotentials are *not*
transferable by magic; always test convergence and check for
ghost states.

**See:** [Chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.1–8.7; [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
</details>

### C.6 — How do I compute a band structure?

<details>
<summary><strong>C.6 — How do I compute a band structure?</strong></summary>

A **band structure** is the orbital energy
\(\varepsilon_{n\mathbf k}\) plotted along a high-symmetry
path in the Brillouin zone (e.g. \(\Gamma \to X \to W \to K
\to \Gamma \to L \to U \to W\) for FCC).  Recipe:

1. **Converge the ground state** at a uniform k-mesh with a
   finite smearing (Gaussian, Methfessel–Paxton, Fermi–Dirac).
2. **Restart from the converged charge density**; switch off
   the smearing (or use a tiny cold-smearing width).
3. **Sample the BZ along the high-symmetry path**, not on a
   uniform mesh.  Use ~50–200 k-points along the path.
4. **Plot \(\varepsilon_{n\mathbf k}\) vs. the path
   coordinate**; align the Fermi energy to zero (set
   \(E_F = \varepsilon_F\) from the uniform-mesh run).

Caveats: Kohn–Sham band structures are *not* the quasiparticle
band structure; the gap is wrong, and the band widths and
dispersions can be off.  For a quantitatively correct band
structure you need $GW$ or similar.

**See:** [Chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.7–7.8; [Chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) §11.2; [Worked examples]({{ "/dft-notes/extras/worked-examples/" | relative_url }})
</details>

### C.7 — How do I compute a density of states?

<details>
<summary><strong>C.7 — How do I compute a density of states?</strong></summary>

The **density of states (DOS)** is the number of orbitals
per unit energy:

\begin{equation}
\label{eq:faq-dos}
g(\varepsilon) \;=\; \sum_{n\mathbf k}\, \delta(\varepsilon - \varepsilon_{n\mathbf k}) .
\end{equation}

In a plane-wave code you compute it by: (i) running a
**uniform k-mesh** (denser than for the ground state —
\(20 \times 20 \times 20\) or more for metals); (ii)
collecting all the eigenvalues \(\{\varepsilon_{n\mathbf
k}\}\); (iii) **smearing the delta peaks** (Gaussian,
Lorentzian) so the histogram is smooth, with a smearing
width comparable to the *energy resolution* you want
(typically 0.1–0.3 eV); (iv) **plotting** \(g(\varepsilon)\)
vs. \(\varepsilon\), aligning \(E_F\) to zero.  The
"projected DOS" or "PDOS" weights each band by the
contribution of a chosen atom or orbital (handy for assigning
spectral features to specific chemical species).  The DOS is
the right convolution partner for comparing to photoemission
or STM spectroscopy; the band structure is the right partner
for direct / indirect gap assignments.

**See:** [Chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) §11.3; [Chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.8
</details>

### C.8 — What's the difference between geometry optimisation and molecular dynamics?

<details>
<summary><strong>C.8 — What's the difference between geometry optimisation and molecular dynamics?</strong></summary>

Both move the nuclei on the *Born–Oppenheimer* potential
energy surface; they differ in what they do once they get
there.  **Geometry optimisation** finds a *stationary point*
— usually the *minimum* (an equilibrium geometry) — by
iteratively following the forces until they fall below some
tolerance (typically 10 meV/Å).  The output is a single
geometry and its energy.  Algorithms: steepest descent,
conjugate gradient, BFGS, L-BFGS.  *Transition-state search*
is the same idea but targets a saddle point.  **Molecular
dynamics (MD)** propagates the nuclei *classically*
(Newton's second law) or *quantum-mechanically*
(path-integral, ring-polymer) under the same BO surface, with
a finite temperature.  The output is a *trajectory* — a
sequence of geometries over time, from which you can compute
thermodynamic averages, diffusion constants, vibrational
spectra, free energies.  Algorithms: Verlet, Nose–Hoover,
Langevin.  Use the first for *geometries and energies*; use
the second for *finite-temperature properties and dynamics*.

**See:** [Chapter 09]({{ "/dft-notes/chapter-09/" | relative_url }}) §9.2 (geometry optimisation), §9.4 (MD)
</details>

### C.9 — What does "SCF" mean and why does it sometimes not converge?

<details>
<summary><strong>C.9 — What does "SCF" mean and why does it sometimes not converge?</strong></summary>

"SCF" stands for **self-consistent field** — the iterative
loop that solves the Kohn–Sham (or Hartree–Fock) equations
self-consistently (see B.6).  A non-converging SCF is one of
the most common practical headaches.  Possible causes and
fixes:

| Symptom | Likely cause | Fix |
|:--------|:-------------|:----|
| Energy oscillates | Charge sloshing | Add more density mixing; switch to DIIS or Broyden |
| Energy diverges | Too-aggressive mixing | Reduce mixing parameter (0.1–0.3) |
| Stuck above the converged energy | Bad initial guess | Smaller basis first, then restart; try `lumos` initial guess |
| Converges to different energies for different starts | Multiple SCF solutions (rare) | Different starting density; increase mixing |
| Converges, but forces are huge | Spin / occupation problem | Try spin-polarised; check occupations; try SMEARING |

Most codes have a built-in "SCF" panel that lets you change
the mixing parameter, the mixing history length, the
diagonalisation algorithm, and the convergence tolerance.
A non-converging SCF is *usually* a sign that the system is
in a physically unusual state — open-shell, metallic,
near-degenerate, broken-symmetry.  Diagnose, don't just turn
knobs.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6; [Chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.11
</details>

### C.10 — What is smearing and when do I need it?

<details>
<summary><strong>C.10 — What is smearing and when do I need it?</strong></summary>

**Smearing** is a numerical trick that replaces the
zero-temperature step function in the Fermi–Dirac occupation
with a smooth function (Gaussian, Methfessel–Paxton,
Fermi–Dirac with a finite \(T\), cold smearing).  It is
*necessary* for **metals**: the zero-temperature occupation
discontinuity at \(E_F\) makes the energy a non-smooth
function of the Kohn–Sham potential, and the SCF loop
struggles.  Smearing also helps with **fractional
occupations** in near-degenerate cases (HOMO–LUMO near
zero, transition states).  The price is that the energy you
get is the *free energy*, not the ground-state energy, and
the occupations are no longer 0 or 1.  A pragmatic recipe:
run with smearing (e.g. \(\sigma = 0.05\)–0.1 eV) and **tight
SCF**; **re-converge the final result without smearing** (or
with a very small width), starting from the smeared density.
For a *production* calculation of a metal, the converged
zero-smearing energy is the right number to report.  For an
insulator or a molecule, you usually do not need any smearing
at all.

**See:** [Chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6.3; [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6.5
</details>

---

## D. Common pitfalls

The "I ran the calculation and got a weird result" questions.
Read this section when (not if) something goes wrong.

### D.1 — My band gap is too small — what's wrong?

<details>
<summary><strong>D.1 — My band gap is too small — what's wrong?</strong></summary>

LDA and GGA functionals **systematically underestimate band
gaps** of semiconductors and insulators by 30–50 % — this is
not a bug, it is a *known feature* of semilocal
approximations.  The Kohn–Sham gap
\(\varepsilon_\text{LUMO} - \varepsilon_\text{HOMO}\) is *not*
the fundamental gap (which is \(I - A\), the ionisation
potential minus the electron affinity); the difference is the
**derivative discontinuity** of \(E_\text{xc}\), which is
missing from semilocal functionals.  Options to fix: **hybrid
functionals** (PBE0, HSE06) add 25 % (or screened) exact
exchange; HSE06 gaps are typically within 5–10 % of
experiment for sp semiconductors.  **Range-separated
hybrids** (HSE06, $\omega$B97X) for solids and molecules
respectively.  **DFT+U** for transition-metal oxides (adds
an on-site Coulomb penalty to localised $d$ states).  **$GW$**
(many-body perturbation theory) for quantitative gaps and
band structures; expensive.  The first thing to try is HSE06
(solids) or PBE0 (molecules).  If your gap is *zero* (metallic)
when the material is known to be an insulator, check that you
have a spin-polarised calculation *if* the gap is
correlation-driven (NiO, MnO).

**See:** [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) §5.4 (hybrids), §5.5 (range-separated); [Chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) §11.4
</details>

### D.2 — My energy is not converged as I add more k-points — why?

<details>
<summary><strong>D.2 — My energy is not converged as I add more k-points — why?</strong></summary>

Two common reasons.

**1. You are computing a metal.**  The integrand (density of
states times occupation) is *discontinuous* at \(E_F\); a
finite k-mesh undersamples the Fermi surface, and the
integrated quantities oscillate with mesh density.  Two
fixes: (a) **denser k-mesh** — a \(20 \times 20 \times 20\)
mesh is a starting point for unit-cell metals; (b)
**smearing** with a finite electronic temperature, which
smooths the integrand.

**2. Your smearing width is too small** (or zero).  A small
smearing means the discontinuity is barely smoothed and you
need a *very* fine k-mesh to converge.  Use a larger
smearing for the *convergence* run, then a tight-smearing
final run.

A diagnostic: plot total energy vs. k-mesh density on a log
scale.  For a metal, the curve should oscillate with
*decreasing* amplitude as you refine the mesh; the envelope
should follow a \(\sim 1/N_\mathbf k\) decay.  For an
insulator, the curve should be smooth and converge
*exponentially* fast in \(N_\mathbf k\).

**See:** [Chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6; [Chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) §11.3
</details>

### D.3 — My geometry optimisation oscillates — what to do?

<details>
<summary><strong>D.3 — My geometry optimisation oscillates — what to do?</strong></summary>

An oscillating optimisation is a *sign* that the algorithm
is fighting the curvature of the potential energy surface.
The most common causes: **The step size is too large** — try
reducing the maximum step (in ASE: `fmax=0.05` eV/Å instead
of `fmax=0.5`).  **You are using steepest descent** —
notoriously bad at handling anisotropic curvature; switch to
**LBFGS** (default in ASE, VASP, Quantum ESPRESSO, CP2K).
**The forces are not converged** — a force of 0.1 eV/Å is not
accurate enough for tight geometry optimisation; converge
the SCF to \(10^{-6}\) eV (not \(10^{-4}\)).  **You are
near a saddle point** — the algorithm wants a minimum, but
the geometry is closer to a transition state; try a different
starting point, or use a transition-state search.  **The
unit cell is also relaxing** (cell optimisation) with the
wrong optimiser; use the variable-cell LBFGS / BFGS, not
steepest descent.  If the oscillation is *periodic* with two
geometries alternating, you are probably bouncing back and
forth across a saddle.  Damp the step, or change the
algorithm.

**See:** [Chapter 09]({{ "/dft-notes/chapter-09/" | relative_url }}) §9.3, §9.5; [Worked examples]({{ "/dft-notes/extras/worked-examples/" | relative_url }})
</details>

### D.4 — My forces are noisy — what gives?

<details>
<summary><strong>D.4 — My forces are noisy — what gives?</strong></summary>

"Noisy" forces — values that fluctuate by ~50 meV/Å or
more between iterations, or that don't monotonically
decrease in magnitude — have a few common culprits: **The SCF
is not converged** — forces are *gradients of the energy*;
if the energy has \(10^{-4}\) eV noise, the forces have
\(10^{-2}\) eV/Å noise.  Tighten the SCF convergence.
**The k-mesh is too coarse** — especially in metals, an
insufficiently-converged BZ integral makes the energy a noisy
function of the nuclear positions.  **The smearing is too
small** — forces with cold smearing are notoriously noisier
than with Fermi–Dirac; switch smearing scheme if you are
chasing micro-eV/Å accuracy.  **The basis set is too small**
— plane-wave: increase \(E_\text{cut}\); Gaussian: climb the
basis-set ladder.  **Symmetry breaking** — the structure is
close to a high-symmetry point; tiny numerical errors pick a
random lower-symmetry direction and the forces wiggle around
it.  A practical rule: if your forces are noisy at the
0.1 eV/Å level, do not trust the geometry.  Re-converge
*everything* and try again.

**See:** [Chapter 09]({{ "/dft-notes/chapter-09/" | relative_url }}) §9.1; [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7
</details>

### D.5 — I get different results from different codes — why?

<details>
<summary><strong>D.5 — I get different results from different codes — why?</strong></summary>

A "different result" can mean:

- **Different total energy** (most common).  This is *usually*
  a basis-set / cutoff / convergence issue, not a code bug.
  Make sure the inputs are *truly* the same: same functional,
  same basis (or converged basis), same k-mesh (or converged
  mesh), same smearing scheme, same SCF tolerance, same
  number of bands, same integration grid.  Differences below
  the convergence threshold are normal; differences above it
  mean at least one code is wrong.
- **Different geometry** (after "optimisation").  Most codes
  will find the same minimum *if* the convergence parameters
  match; small (\(<0.001\) Å) differences are normal; larger
  ones usually mean one of the calculations did not actually
  converge.
- **Different gap / different orbital ordering**.  Often a
  real physical difference — symmetry breaking, spin
  polarisation, metallic vs. insulating.  *Check the
  occupations* and the *spin state* in both codes.

A pragmatic check: run the same system in two codes with
*identical* inputs and confirm that the energies agree to
better than 1 meV/atom.  If they don't, one is wrong; *do
not* average them.  Cross-validation between codes is a
*powerful* convergence test, because bugs that survive in
one code rarely survive in two.

**See:** [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}); [Chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.11
</details>

### D.6 — My calculation crashed with a cryptic error — what does it mean?

<details>
<summary><strong>D.6 — My calculation crashed with a cryptic error — what does it mean?</strong></summary>

Cryptic error messages are a *symptom*, not a diagnosis.
A few common ones and what they usually mean:

| Message (loosely) | Likely meaning |
|:------------------|:---------------|
| `zpotbr > 1000` (VASP), `rho is negative` | Charge sloshing; SCF diverging.  Tighten mixing, reduce \(\alpha\), try a different starting density. |
| `BRMIX: linear search failed` (VASP) | Same as above; the Kerker-style mixer cannot find a step that lowers the energy. |
| `subspacematrix not positive definite` (VASP) | Almost-empty bands / numerical instability in subspace diagonalisation.  Try a different `ALGO`, or add more bands. |
| `cannot orthogonalise` (CP2K) | Linear-dependency collapse in a Gaussian basis (very diffuse functions).  Tighten the basis, or use `EPS_DEFAULT`. |
| `SCF run did not converge` (ORCA) | As in C.9.  Try `SlowConv`, `DIIS`, or change `MAXITER`. |
| `k-point fold > max` (Quantum ESPRESSO) | Lattice vectors are too small; the BZ is over-folded.  Check the structure. |
| `poisson solver failed` (SIESTA, GPAW) | Bad initial guess; try `DM.Init.State random` or `density_init` from a previous run. |

The pattern: read the *last* error, not the first;
identify the *subsystem* (SCF, optimiser, diagonaliser);
fix the *root cause*; do not just increase `MAXITER`.

**See:** [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6; [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
</details>

---

## E. Software

The "which code, and on which machine" questions.  See the
[Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
for the full per-code profiles.

### E.1 — Which DFT code should I use?

<details>
<summary><strong>E.1 — Which DFT code should I use?</strong></summary>

Match the code to the **boundary condition** and the
**physics**:

- **Molecules / clusters, ground-state DFT** — PySCF (open
  source, friendly), Psi4 (open source, production), ORCA
  (free for academics, strong on TM chemistry), Q-Chem
  (commercial, high-throughput), Gaussian (commercial, broad
  coverage).
- **Periodic solids, plane-wave PAW** — VASP (commercial —
  see E.2), Quantum ESPRESSO (open source), CASTEP
  (commercial academic), ABINIT (open source).
- **All-electron, full potential** — WIEN2k, Elk, FLEUR,
  FHI-aims, exciting.  Needed for properties that depend on
  the core electrons (hyperfine, Mössbauer, $f$-electron
  systems).
- **Large systems (thousands of atoms)** — CP2K (Gaussian +
  plane wave), SIESTA (linear-scaling, real-space), GPAW
  (real-space grid, Python), BigDFT (wavelets).
- **High-accuracy wavefunction (CCSD(T), FCI)** — MRCC,
  CFOUR, Psi4, PySCF.
- **Workflow / automation** — ASE (Python front end), AiiDA
  (provenance + HPC), atomate, Fireworks.

The [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
has full per-code profiles (licence, language, methods, when
to use, when not to).

**See:** [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}) — all sections
</details>

### E.2 — Is VASP free?

<details>
<summary><strong>E.2 — Is VASP free?</strong></summary>

**No.**  VASP (Vienna Ab-initio Simulation Package) is
**commercial software**, distributed under a paid licence
by the VASP Software GmbH (University of Vienna).  It is
*not* open source; the source code is not available to
non-licence-holders.  Typical licence categories:
**Academic licence** — paid annually, available to
universities and non-profit research institutes.
**Commercial licence** — paid, for industry.  **Some
national consortia** have site licences that cover every
researcher at a participating institution — check with your
local HPC centre.

Open-source alternatives that cover the same physics:
**Quantum ESPRESSO** (plane-wave PAW, very mature),
**CASTEP** (commercial-academic), **ABINIT** (open source),
**CP2K** (open source, GPW), **SIESTA** (open source,
linear-scaling).  Most of the methods VASP implements
(PAW, hybrid functionals, DFPT, $GW$ via WEST) are also
implemented in Quantum ESPRESSO and ABINIT.

**See:** [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}) — "Plane-wave / PAW codes"; [Chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7
</details>

### E.3 — Where can I run DFT calculations for free?

<details>
<summary><strong>E.3 — Where can I run DFT calculations for free?</strong></summary>

Three kinds of free resource: **Free, open-source codes**
that you install and run on your own machine or your
institution's cluster: PySCF, Psi4, Quantum ESPRESSO, SIESTA,
CP2K, GPAW, ABINIT, BigDFT, FHI-aims (academic).  The code
itself is free; the *compute* is whatever you can afford.
**Free web interfaces** to commercial codes: some companies
(Schrödinger, Q-Chem) offer a small number of free
web-submitted jobs per month; useful for *exploration* but
not for production.  **Free national HPC allocations**: in
many countries the national supercomputing centre has an
open allocation track (e.g. XSEDE/ACCESS in the US, ARCHER
in the UK, Jean-Zay in France, MareNostrum in Spain, JURECA
in Germany).  The compute is free; the *proposal* and the
*queue* are the cost.  **Free test allocations on cloud
platforms** (AWS, GCP, Azure, Oracle Cloud) — typically
$300–$500 of free credit when you first sign up, enough for
a few mid-sized DFT calculations.

The catch: the "free" usually applies to the *code* or to
the *allocation*, not to both.  A VASP run on a free
allocation is still not free; an open-source code on a paid
cloud is also not free.

**See:** [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}) — "Licence" column
</details>

### E.4 — What's a "PAW potential" vs a "pseudopotential"?

<details>
<summary><strong>E.4 — What's a "PAW potential" vs a "pseudopotential"?</strong></summary>

A **pseudopotential** (norm-conserving or ultrasoft)
replaces the strong nuclear Coulomb potential and the
frozen core by a *smooth effective potential* that
reproduces the valence wavefunction outside a cutoff radius
\(r_c\).  Inside \(r_c\) the pseudo-wavefunction is
*nodeless* (no core radial nodes) and is *not* the
all-electron wavefunction; information about the core
electrons is lost.  A **PAW (projector augmented wave)
potential** is a *transformation* (Blöchl, 1994) that maps
the smooth pseudo-wavefunction back to the *true*
all-electron wavefunction inside \(r_c\) via a linear
augmentation.  In practice the user provides a *PAW dataset*
(atom-centred partial waves, projectors, augmentation
charges); the code applies the transformation.  PAW retains
the efficiency of ultrasoft pseudopotentials (small basis)
while recovering the all-electron accuracy inside the
augmentation sphere.  In modern plane-wave codes (VASP,
Quantum ESPRESSO, ABINIT, CASTEP) "PAW" is the default;
"pseudopotential" in the old norm-conserving sense is the
legacy option.  The terms are often used interchangeably in
casual conversation, but they are not the same thing.

**See:** [Chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) §8.7 (PAW), §8.5 (ultrasoft), §8.3 (norm-conserving)
</details>

### E.5 — How do I cite a DFT code in a paper?

<details>
<summary><strong>E.5 — How do I cite a DFT code in a paper?</strong></summary>

Every code has a *canonical citation* — usually a **methods
paper** that you cite in addition to the code website.
**VASP** — Kresse & Furthmüller (1996) *Comput. Mater. Sci.*
**6**, 15; Kresse & Joubert (1999) *Phys. Rev. B* **59**, 1758
(for PAW).  **Quantum ESPRESSO** — Giannozzi et al. (2009)
*J. Phys. Condens. Matter* **21**, 395502; Giannozzi et al.
(2017) *J. Phys. Condens. Matter* **29**, 465901.  **CP2K** —
Hutter et al. (2014) *WIREs Comput. Mol. Sci.* **4**, 15.
**SIESTA** — Soler et al. (2002) *J. Phys. Condens. Matter*
**14**, 2745.  **ORCA** — Neese (2012) *WIREs Comput. Mol.
Sci.* **2**, 73; Neese (2018) *WIREs Comput. Mol. Sci.* **8**,
e1327.  **Gaussian** — Frisch et al., *Gaussian 16 Revision
C.01*, Gaussian Inc., 2016.  **CASTEP** — Clark et al. (2005)
*Z. Kristallogr.* **220**, 567.  **PySCF** — Sun et al.
(2018) *J. Chem. Phys.* **153**, 024109.

Always cite the *version* (e.g. "VASP 6.3.0"), the
*functional* (e.g. "PBE-D3"), the *pseudopotential library*
(e.g. "PAW_PBE from the VASP library"), and the *convergence
parameters* in the methods section.  This is the most common
source of irreproducibility in published DFT.

**See:** [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}) — "References" in each code profile; [Bibliography]({{ "/dft-notes/extras/bibliography/" | relative_url }})
</details>

---

## What this FAQ is not

This page deliberately does not cover:

- **Derivation of the Hohenberg–Kohn theorem** — see
  [Chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1.
- **Detailed XC functional derivations** — see
  [Chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) for
  LDA, GGA, meta-GGA, hybrid, range-separated, double-hybrid.
- **Implementation details of any specific code** — see the
  [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
  and the code's manual.
- **The full list of DFT codes** — the Software cheatsheet has
  nine categories; we mention six of them here.
- **Beyond-DFT methods in depth** ($GW$, BSE, DMFT, …) — see
  [Chapter 12]({{ "/dft-notes/chapter-12/" | relative_url }}) (TDDFT)
  and [Chapter 13]({{ "/dft-notes/chapter-13/" | relative_url }})
  (planned; beyond-DFT).

If your question is not answered here, try the
[Notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}),
the [Math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}),
the [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}),
the [Worked examples]({{ "/dft-notes/extras/worked-examples/" | relative_url }}),
or the [Problems anthology]({{ "/dft-notes/extras/problems/" | relative_url }}).
This page is maintained by `agent:docs-keeper` and is open to
additions.

---

> Back to the
> [chapter index]({{ "/dft-notes/" | relative_url }}) or jump to
> the [chapters map]({{ "/dft-notes/chapters-map/" | relative_url }}).
> Related reference pages: the
> [Notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}),
> [Math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}),
> [Bibliography]({{ "/dft-notes/extras/bibliography/" | relative_url }}),
> [Software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}),
> [Worked examples]({{ "/dft-notes/extras/worked-examples/" | relative_url }}),
> and [Problems anthology]({{ "/dft-notes/extras/problems/" | relative_url }}).
