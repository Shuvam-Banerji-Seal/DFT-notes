---
layout: page
title: "Mathematical identities cheatsheet"
permalink: /dft-notes/extras/math-cheatsheet/
description: >-
  A reference card of the mathematical identities used throughout the
  DFT Notes chapters — Dirac notation, operator algebra, second
  quantisation, Fourier transforms, Green's functions, special
  functions, differential operators in curvilinear coordinates,
  functional and variational calculus, the Coulomb kernel and its
  Ewald decomposition, and the standard integrals of statistical
  mechanics. Each entry is cross-referenced to the chapter that uses
  it.
keywords: "math cheatsheet, identities, Dirac notation, commutator, BCH,
  second quantisation, Wick's theorem, Fourier transform, Green's
  function, spectral function, Hermite, Laguerre, Legendre, Bessel,
  spherical harmonics, gamma function, Levi-Civita, Kronecker delta,
  SVD, matrix exponential, trace, functional derivative, Euler-Lagrange,
  Ewald sum, Fermi-Dirac, Bose-Einstein, polylog"
---

# Mathematical identities cheatsheet

> A single-page reference for the math that recurs across the DFT
> Notes. Every identity is stated in the **conventions used in the
> chapters** (atomic units, Dirac bra-ket, real spherical harmonics,
> the Pople `N-M₁M₂G` basis-set notation, etc.). Each entry is
> cross-referenced to the chapter that uses it, so the reader can
> jump straight to the worked derivation.

The cheatsheet is **not** a substitute for the chapters themselves.
It is a lookup table: when a derivation uses an identity you have
forgotten, the cheatsheet tells you what the identity *is* and where
to find the step-by-step use of it. For proofs, see the linked
chapter.

> **Notation.** All formulas are in **atomic units**
> ($\hbar = m_e = e^2 / (4\pi\varepsilon_0) = 1$) unless otherwise
> stated. Lengths are in Bohr ($a_0$), energies in Hartree
> ($E_h$), and the charge of the electron is $-1$. The notation
> table in [chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }})
> is the source of truth; this page only collects the math.

---

## 1. Dirac notation

The chapters use the Dirac bra-ket notation of
[chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}) for
every inner product and every matrix element. The same notation
works in $\mathbb C^n$ (for finite-basis calculations) and in
$L^2(\mathbb R^3)$ (for the continuous Hilbert space).

### 1.1 Inner product

\begin{equation}
\label{eq:ch-extra-inner}
\langle u \rvert v \rangle \;\equiv\;
\begin{cases}
\displaystyle \sum_{i=1}^{n} u_i^* v_i & \text{in } \mathbb C^n, \\[6pt]
\displaystyle \int u^*(\mathbf r)\, v(\mathbf r)\, d\mathbf r & \text{in } L^2(\mathbb R^3).
\end{cases}
\end{equation}

Used to define the **Born rule**, the **Fock and overlap matrix
elements** in the AO basis
$F_{\mu\nu} = \langle \chi_\mu \rvert \hat F \rvert \chi_\nu \rangle$,
and the **MO normalisation** $\langle \phi_i \rvert \phi_j \rangle =
\delta_{ij}$. Cross-reference: chapters 01 (§1.2), 03 (§3.2, §3.6).

### 1.2 Outer product

\begin{equation}
\label{eq:ch-extra-outer}
\rvert u \rangle \langle v \rvert \;:\; \text{the rank-one operator that maps } \rvert w \rangle \mapsto \rvert u \rangle \langle v \rvert w \rangle .
\end{equation}

Used to build the **closed-shell AO density matrix** as
$\mathbf P = 2 \sum_i \rvert \phi_i \rangle \langle \phi_i \rvert$
and the **projector onto the occupied subspace** in a finite
basis. Cross-reference: chapter 03 (§3.6.4, the idempotency
$\mathbf P \mathbf S \mathbf P = \mathbf P$).

### 1.3 Completeness (resolution of the identity)

\begin{equation}
\label{eq:ch-extra-completeness}
\hat{\mathbf 1} \;=\; \sum_{i=1}^{K} \rvert \chi_i \rangle \langle \chi_i \rvert
\;\;(\text{discrete basis}), \qquad
\hat{\mathbf 1} \;=\; \int \rvert \mathbf r \rangle \langle \mathbf r \rvert\, d\mathbf r
\;\;(\text{position basis}).
\end{equation}

Inserted between operators in derivations to convert
operator equations to matrix form. The two forms above are
**equivalent** when $\{\chi_i\}$ is a complete orthonormal set;
for a *non-orthogonal* basis the form $\mathbf S^{-1} = \sum_i
\rvert \chi^i \rangle \langle \chi_i \rvert$ requires the **dual
vectors** $\rvert \chi^i \rangle$. Cross-reference: chapters 01
(§1.8.3, transition amplitudes), 06 (§6.1, Roothaan–Hall).

### 1.4 Projection operators

A **projector** $\hat P$ satisfies $\hat P^2 = \hat P$ and
$\hat P^\dagger = \hat P$. The projector onto the subspace
spanned by the $K$ vectors $\{\rvert \chi_i \rangle\}$ (in
general non-orthogonal) is

\begin{equation}
\label{eq:ch-extra-projector}
\hat P \;=\; \sum_{i,j=1}^{K} \rvert \chi_i \rangle\, (\mathbf S^{-1})_{ij}\, \langle \chi_j \rvert ,
\qquad \hat P^2 = \hat P, \quad \hat P^\dagger = \hat P .
\end{equation}

For an orthonormal set the matrix $\mathbf S^{-1}$ reduces to
$\mathbf 1$, giving $\hat P = \sum_i \rvert \chi_i \rangle \langle \chi_i \rvert$.
The idempotency of $\mathbf P$ in the AO basis
($\mathbf P \mathbf S \mathbf P = \mathbf P$) is exactly the
statement that the density matrix is a projector onto the
occupied subspace. Cross-reference: chapter 03 (§3.6.4).

> **Tip.** The Hermitian conjugate of $\rvert u \rangle \langle v \rvert$
> is $\rvert v \rangle \langle u \rvert$. The trace of an outer
> product is $\operatorname{Tr}\bigl(\rvert u \rangle \langle v \rvert\bigr) = \langle v \rvert u \rangle$.
> Both facts are used in the half-trace form of the HF energy,
> $E_\text{HF} = \tfrac{1}{2} \operatorname{Tr}\bigl[ \mathbf P (\mathbf h + \mathbf F) \bigr]$.

---

## 2. Operator identities

### 2.1 The commutator and its algebra

\begin{equation}
\label{eq:ch-extra-commutator}
[\hat A, \hat B] \;\equiv\; \hat A \hat B - \hat B \hat A .
\end{equation}

The commutator is **bilinear**, **antisymmetric**
$([\hat A, \hat B] = -[\hat B, \hat A]$), and satisfies the
**Jacobi identity**

\begin{equation}
\label{eq:ch-extra-jacobi}
[\hat A, [\hat B, \hat C]] + [\hat B, [\hat C, \hat A]] + [\hat C, [\hat A, \hat B]] \;=\; 0 .
\end{equation}

The **canonical commutation relation** (CCR) of quantum mechanics,

\begin{equation}
\label{eq:ch-extra-ccr}
[\hat r_a, \hat p_b] \;=\; i\, \delta_{ab} \qquad (a, b \in \{x, y, z\}) ,
\end{equation}

defines the algebra on which the Heisenberg uncertainty
principle $\Delta A \Delta B \ge \tfrac{1}{2} \lvert \langle [\hat A, \hat B] \rangle \rvert$
rests. Cross-reference: chapter 01 (§1.4, §1.7.5, problem 1 of §1.13).

### 2.2 The anticommutator

\begin{equation}
\label{eq:ch-extra-anticommutator}
\{\hat A, \hat B\} \;\equiv\; \hat A \hat B + \hat B \hat A .
\end{equation}

For **fermionic** creation and annihilation operators,
$\{\hat a, \hat a^\dagger\} = 1$, $\{\hat a, \hat a\} = 0$ —
the algebra of the **canonical anticommutation relation**
(CAR). The fermionic CAR is what makes a Slater determinant
antisymmetric. Cross-reference: chapter 01 (§1.2, postulate P6).

### 2.3 Baker–Campbell–Hausdorff (BCH)

The product of two exponentials of non-commuting operators
re-exponentiates as

\begin{equation}
\label{eq:ch-extra-bch}
e^{\hat A} e^{\hat B}
\;=\; e^{\hat A + \hat B + \tfrac{1}{2}[\hat A, \hat B] + \tfrac{1}{12}[\hat A, [\hat A, \hat B]] - \tfrac{1}{12}[\hat B, [\hat A, \hat B]] + \cdots} .
\end{equation}

The series terminates at finite order only when the nested
commutators eventually vanish (e.g. $[\hat A, \hat B]$ is a
$c$-number, as for the position-momentum pair). For
$\hat A = \lambda \hat X$, $\hat B = \lambda \hat Y$ with
$[\hat X, \hat Y] = \hat Z$ independent of $\hat X, \hat Y$, the
BCH formula gives the **Zassenhaus formula**

\begin{equation}
\label{eq:ch-extra-zassenhaus}
e^{\hat A + \hat B}
\;=\; e^{\hat A}\, e^{\hat B}\, e^{-\tfrac{1}{2}[\hat A, \hat B]}\, e^{\tfrac{1}{6}(2[\hat B, [\hat A, \hat B]] + [\hat A, [\hat A, \hat B]])} \cdots ,
\end{equation}

i.e. the product of two exponentials is the exponential of the
sum *plus* correction factors. Used in the derivation of the
**time-evolution operator in the interaction picture**
(chapter 01, §1.8) and in the **factorisation of the Fock
matrix** (chapter 03).

### 2.4 Useful specific identities

\begin{align}
e^{\hat A} \hat B e^{-\hat A} &\;=\; \hat B + [\hat A, \hat B] + \tfrac{1}{2!}[\hat A, [\hat A, \hat B]] + \tfrac{1}{3!}[\hat A, [\hat A, [\hat A, \hat B]]] + \cdots \quad &\text{(similarity transform)} , \label{eq:ch-extra-sim} \\
[\hat A \hat B, \hat C] &\;=\; \hat A [\hat B, \hat C] + [\hat A, \hat C] \hat B \quad &\text{(product rule)} , \label{eq:ch-extra-prodcom} \\
\operatorname{Tr}[\hat A, \hat B] &\;=\; 0 \quad &\text{(trace of a commutator)} . \label{eq:ch-extra-tracecom}
\end{align}

The first is the **Hadamard lemma** (or **Campbell identity**)
in series form. The second lets you reduce a commutator with a
product to a sum of simpler commutators. The third is the
**cyclicity of the trace** applied to a commutator; it is the
reason the Fock-operator trace formulas of chapter 03 (§3.2)
collapse so cleanly. Cross-reference: chapters 01, 03.

---

## 3. Hilbert-space identities

### 3.1 Trace identities

\begin{align}
\operatorname{Tr}(\mathbf A \mathbf B) &\;=\; \operatorname{Tr}(\mathbf B \mathbf A) , \label{eq:ch-extra-tracecyc} \\
\operatorname{Tr}(\mathbf A + \mathbf B) &\;=\; \operatorname{Tr}\mathbf A + \operatorname{Tr}\mathbf B , \label{eq:ch-extra-tracelin} \\
\operatorname{Tr}(\mathbf A \mathbf B \mathbf C) &\;=\; \operatorname{Tr}(\mathbf C \mathbf A \mathbf B) = \operatorname{Tr}(\mathbf B \mathbf C \mathbf A) \quad \text{(cyclic)} . \label{eq:ch-extra-tracecyc3}
\end{align}

The cyclic property is the engine behind every trace formula
in DFT: $E = \operatorname{Tr}[\mathbf P \mathbf h]$ follows
because $\mathbf P$ and $\mathbf h$ can be cyclically permuted
inside the trace. Cross-reference: chapters 03 (§3.2, §3.6.5),
04 (§4.4).

### 3.2 Trace of a function of a matrix

If $\mathbf A$ has eigenvalues $\{a_i\}$ and eigenvectors
$\{\rvert v_i \rangle\}$, then for any function $f$ that admits
a Taylor series,

\begin{equation}
\label{eq:ch-extra-tracef}
\operatorname{Tr} f(\mathbf A) \;=\; \sum_{i=1}^{K} f(a_i) .
\end{equation}

The same is true for $f(\hat A)$ in any finite-dimensional
representation: $\operatorname{Tr} f(\hat A) = \sum_i f(a_i)$
where the sum is over the spectrum of $\hat A$. Used in the
proof that the sum of orbital energies equals the trace of the
Fock matrix, and in deriving the **Janak theorem** from the
Kohn–Sham energy expression.

### 3.3 Hilbert–Schmidt inner product

\begin{equation}
\label{eq:ch-extra-hs}
\langle \mathbf A, \mathbf B \rangle_\text{HS} \;\equiv\; \operatorname{Tr}(\mathbf A^\dagger \mathbf B) .
\end{equation}

The Frobenius / Hilbert–Schmidt norm is
$\lVert \mathbf A \rVert_\text{HS}^2 = \operatorname{Tr}(\mathbf A^\dagger \mathbf A)$.
This is the inner product used in the **DIIS metric**
$\mathbf B_{ij} = \langle R_i, R_j \rangle$ in
chapter 04 (§4.6.2). Cross-reference: chapter 04.

### 3.4 Trace of a projector

\begin{equation}
\label{eq:ch-extra-traceproj}
\operatorname{Tr} \hat P \;=\; \dim(\text{range of } \hat P) .
\end{equation}

In a finite basis, $\operatorname{Tr} \mathbf P = N_\text{occ}$
(counting spins separately). Used in the constraint that the
density matrix integrates to the number of electrons.

---

## 4. Second quantisation

Second quantisation replaces the antisymmetrised Slater
determinants of chapter 02 (§2.2) by **creation and
annihilation operators** acting on a Fock space. This section
collects the identities the chapters use.

### 4.1 Bosonic creation and annihilation operators

\begin{align}
[\hat a, \hat a^\dagger] &\;=\; \hat 1 , \label{eq:ch-extra-bosonic} \\
[\hat a, \hat a] &\;=\; [\hat a^\dagger, \hat a^\dagger] \;=\; 0 . \label{eq:ch-extra-bosonic2}
\end{align}

The **number operator** $\hat n = \hat a^\dagger \hat a$ has
eigenvalues $n = 0, 1, 2, \dots$ (any non-negative integer) and
spectrum $E_n = \omega(n + 1/2)$ for the harmonic oscillator.
Cross-reference: chapter 01 (§1.9, ladder operators).

### 4.2 Fermionic creation and annihilation operators

\begin{align}
\{\hat c_p, \hat c_q^\dagger\} &\;=\; \delta_{pq} , \label{eq:ch-extra-fermionic} \\
\{\hat c_p, \hat c_q\} &\;=\; \{\hat c_p^\dagger, \hat c_q^\dagger\} \;=\; 0 . \label{eq:ch-extra-fermionic2}
\end{align}

The $\delta_{pq}$ is **Kronecker**, not Dirac — the
anticommutation is only between operators in the *same* single-
particle basis. The CAR is what enforces the **Pauli exclusion
principle**: $\hat c_p^\dagger \hat c_p^\dagger = 0$ means no
state can be doubly created. Cross-reference: chapter 02 (§2.2).

### 4.3 Field operators

A general **field operator** is the superposition over a
single-particle basis

\begin{equation}
\label{eq:ch-extra-field}
\hat \psi(\mathbf r) \;=\; \sum_{p} \hat c_p\, \chi_p(\mathbf r) , \qquad
\hat \psi^\dagger(\mathbf r) \;=\; \sum_{p} \hat c_p^\dagger\, \chi_p^*(\mathbf r) .
\end{equation}

For fermions, $\hat \psi$ and $\hat \psi^\dagger$ satisfy the
**continuum CAR**

\begin{equation}
\label{eq:ch-extra-fieldcar}
\{ \hat\psi(\mathbf r), \hat\psi^\dagger(\mathbf r') \} \;=\; \delta(\mathbf r - \mathbf r') , \qquad
\{ \hat\psi(\mathbf r), \hat\psi(\mathbf r') \} \;=\; 0 .
\end{equation}

The one-body density is $\hat\rho(\mathbf r) = \hat\psi^\dagger(\mathbf r) \hat\psi(\mathbf r)$;
its expectation value is the **one-particle density matrix**
of chapter 03 (§3.6.4). Cross-reference: chapters 02, 03.

### 4.4 Wick's theorem (statement)

For a product of $2n$ creation/annihilation operators,
Wick's theorem says

\begin{equation}
\label{eq:ch-extra-wick}
\hat c_1 \hat c_2 \cdots \hat c_{2n}
\;=\; \sum_{\text{all full pairings}} (\pm) \;
    \widehat{\hat c_{i_1} \hat c_{i_2}}\, \widehat{\hat c_{i_3} \hat c_{i_4}} \cdots \widehat{\hat c_{i_{2n-1}} \hat c_{i_{2n}}} ,
\end{equation}

where the hat denotes a **contraction** (the vacuum
expectation value $\langle 0 \rvert \hat c_i \hat c_j \rvert 0 \rangle$,
or its generalisation to a non-vacuum reference) and the
$(\pm)$ sign is the parity of the permutation needed to bring
the paired operators next to each other. The generalisation to
**normal ordering with respect to a non-vacuum reference** is
the workhorse of every many-body perturbation theory
(MP2, CCSD, …). Cross-reference: chapter 02 (§2.3, the
hierarchy of post-HF methods).

> **Tip.** The simplest non-trivial case is the product of
> two operators, $\hat c_1 \hat c_2 = :\!\hat c_1 \hat c_2\!:
> + \widehat{\hat c_1 \hat c_2}$, where $:\cdots:$ is the
> normal-ordered product (annihilators to the right) and the
> contraction is a $c$-number. Wick's theorem for the
> 4-operator case $\hat c_1^\dagger \hat c_2 \hat c_3^\dagger \hat c_4$
> is the **Slater–Condon rules** of chapter 03 (§3.4).

---

## 5. Fourier transforms in 1, 2, 3 dimensions

The chapters use the **physics convention** for the Fourier
transform (no $1/(2\pi)^{n/2}$ prefactor in the forward
transform, the inverse carries the prefactor). This is the
convention of chapter 07 (§7.5) and the convention implicitly
assumed in chapter 04 (§4.6.4, the Kerker preconditioner).

### 5.1 One dimension

\begin{align}
\tilde f(k) &\;=\; \int_{-\infty}^{\infty} f(x)\, e^{-i k x}\, dx , \label{eq:ch-extra-ft1d-fwd} \\
f(x) &\;=\; \frac{1}{2\pi} \int_{-\infty}^{\infty} \tilde f(k)\, e^{+i k x}\, dk . \label{eq:ch-extra-ft1d-inv}
\end{align}

The **Parseval / Plancherel identity** is
$\int |f(x)|^2\, dx = (1/2\pi) \int |\tilde f(k)|^2\, dk$.
Cross-reference: chapter 01 (§1.11.3, the free-particle
propagator by path integration).

### 5.2 Three dimensions

\begin{align}
\tilde f(\mathbf k) &\;=\; \int_{\mathbb R^3} f(\mathbf r)\, e^{-i \mathbf k \cdot \mathbf r}}\, d\mathbf r , \label{eq:ch-extra-ft3d-fwd} \\
f(\mathbf r) &\;=\; \frac{1}{(2\pi)^3} \int_{\mathbb R^3} \tilde f(\mathbf k)\, e^{+i \mathbf k \cdot \mathbf r}}\, d\mathbf k . \label{eq:ch-extra-ft3d-inv}
\end{align}

For a **cell-periodic** function $u(\mathbf r)$ on a lattice
with primitive cell volume $\Omega$, the natural transform is
the **discrete Fourier series** on the reciprocal lattice
$\{\mathbf G\}$:

\begin{align}
u(\mathbf r) &\;=\; \frac{1}{\sqrt{\Omega}} \sum_{\mathbf G} \tilde u(\mathbf G)\, e^{i \mathbf G \cdot \mathbf r} , \label{eq:ch-extra-fs-fwd} \\
\tilde u(\mathbf G) &\;=\; \frac{1}{\sqrt{\Omega}} \int_\Omega u(\mathbf r)\, e^{-i \mathbf G \cdot \mathbf r}}\, d\mathbf r . \label{eq:ch-extra-fs-inv}
\end{align}

The reciprocal-lattice vectors are defined by
$\mathbf a_i \cdot \mathbf b_j = 2\pi \delta_{ij}$
(chapter 07, §7.4.1). The plane-wave basis function
$\Omega^{-1/2} e^{i(\mathbf k + \mathbf G) \cdot \mathbf r}$
of chapter 07 (§7.5) and chapter 06 (§6.7) uses this convention.

### 5.3 The Fourier transform of $1/r$ and $1/r^2$

The two transforms every DFT code needs:

\begin{align}
\int_{\mathbb R^3} \frac{e^{-i \mathbf k \cdot \mathbf r}}{r}\, d\mathbf r &\;=\; \frac{4\pi}{k^2} , \label{eq:ch-extra-fourier-1r} \\
\int_{\mathbb R^3} \frac{e^{-i \mathbf k \cdot \mathbf r}}{r^2}\, d\mathbf r &\;=\; \frac{\pi^2}{k} \quad \text{(distributional sense)} . \label{eq:ch-extra-fourier-1r2}
\end{align}

The first is the **Coulomb kernel in reciprocal space** — the
Fourier transform of $1/r$ — and is the foundation of the
Ewald-summed Coulomb interaction in periodic codes
(chapter 07). Cross-reference: chapter 04 (§4.4, the
Hartree operator in reciprocal space), §13 below.

### 5.4 Useful transforms on a finite interval

The **sinc kernel**

\begin{equation}
\label{eq:ch-extra-sinc}
\int_{-L/2}^{L/2} e^{-i k x}\, dx \;=\; L\, \frac{\sin(kL/2)}{kL/2} \;=\; L\, \operatorname{sinc}(kL/2)
\end{equation}

arises whenever a function is truncated to a box of length $L$.
In 3-D it generalises to a product of three 1-D sincs. Used in
the **planar-averaging** and **slab-coupling** corrections of
chapter 07.

---

## 6. Green's functions

Green's functions are the second-quantised, frequency-dependent
generalisation of the resolvent $(\omega - \hat H)^{-1}$. Every
**spectral property** of a Hamiltonian — density of states,
spectral function, optical conductivity — is a Green's function
in disguise. The chapters use the imaginary-frequency / real-
time conventions of chapter 04 (the Lindhard function in
§4.6.4) and chapter 07 (the smearing Fermi function in §7.6.3).

### 6.1 The resolvent and the free-particle Green's function

The **resolvent** of a Hamiltonian $\hat H$ at complex
frequency $z$ is

\begin{equation}
\label{eq:ch-extra-resolvent}
\hat G(z) \;\equiv\; (z - \hat H)^{-1} .
\end{equation}

For the **free-particle** Hamiltonian
$\hat H_0 = -\tfrac{1}{2} \nabla^2$, the resolvent in
position space is

\begin{equation}
\label{eq:ch-extra-g0}
G_0(\mathbf r, \mathbf r'; E) \;=\; -\frac{e^{i k \lvert \mathbf r - \mathbf r' \rvert}}{2\pi \lvert \mathbf r - \mathbf r' \rvert} ,
\qquad k = \sqrt{2E} ,
\end{equation}

with the $i\eta$ prescription $E \to E + i\eta$ fixing the
boundary condition (outgoing waves for $E > 0$, decaying
exponential for $E < 0$). Used in the **Born series** for
scattering, the **Lippmann–Schwinger equation**, and the
**GW self-energy** of many-body perturbation theory. Cross-
reference: chapters 01 (§1.8, the time-domain Dyson series),
03 (the Fock-operator resolvent).

### 6.2 The Matsubara / imaginary-frequency form

For a finite-temperature **Matsubara Green function** at the
fermionic frequencies $i\omega_n = i(2n+1)\pi / \beta$ (with
$\beta = 1/k_B T$),

\begin{equation}
\label{eq:ch-extra-matsubara}
\mathcal G(\mathbf r, \mathbf r'; i\omega_n)
\;=\; \int_0^\beta d\tau\, e^{i\omega_n \tau}\, \bigl\langle \hat\psi(\mathbf r, \tau)\, \hat\psi^\dagger(\mathbf r', 0) \bigr\rangle ,
\end{equation}

where $\hat\psi(\tau) = e^{\tau \hat H}\, \hat\psi\, e^{-\tau \hat H}$
is the Heisenberg-picture field. The Matsubara sum is the
**finite-temperature** version of the contour-ordered Green
function.

### 6.3 The Dyson equation

If the full Hamiltonian is $\hat H = \hat H_0 + \hat V$, the
**Dyson equation** relates the full Green function $\hat G$ to
the free one $\hat G_0$ and the **self-energy** $\hat\Sigma$:

\begin{equation}
\label{eq:ch-extra-dyson}
\hat G(z) \;=\; \hat G_0(z) \;+\; \hat G_0(z)\, \hat\Sigma(z)\, \hat G(z) .
\end{equation}

Iterating gives the **Born series**
$\hat G = \hat G_0 + \hat G_0 \hat V \hat G_0 + \hat G_0 \hat V \hat G_0 \hat V \hat G_0 + \cdots$.
In the time domain, the Dyson equation is the **Dyson series**
of chapter 01 (§1.8.2). Cross-reference: chapter 01 (§1.8),
chapter 04 (§4.6.4, the Lindhard response function as a
Green-function product).

### 6.4 The spectral function

The **spectral function** is the discontinuity of $\hat G$
across the real axis,

\begin{equation}
\label{eq:ch-extra-spectral}
\mathbf A(\omega) \;\equiv\; \frac{i}{2\pi} \bigl[ \hat G(\omega + i\eta) - \hat G(\omega - i\eta) \bigr] ,
\end{equation}

and is **positive semi-definite** with unit weight
$\int \mathbf A(\omega)\, d\omega = \hat 1$. In the
**Lehmann representation** of a many-body Hamiltonian,

\begin{equation}
\label{eq:ch-extra-lehmann}
A_{ij}(\omega) \;=\; \sum_{n} \bigl[ \langle i \rvert n \rangle \langle n \rvert j \rangle \bigr]\, \delta(\omega - (E_n - E_0)) ,
\end{equation}

where the sum runs over the many-body eigenstates $|n\rangle$.
The spectral function is the bridge from the **Green-function
language** of many-body theory to the **band-structure
language** of chapter 07: at the Hartree–Fock level
($\hat\Sigma = \hat V_\text{HF}$), $A(\omega)$ is a sum of
delta peaks at the HF orbital energies, weighted by the
**spectral weights** of the one-particle states. Cross-
reference: chapters 01, 03, 04, 07.

> **Tip.** The **density of states** is
> $g(\omega) = \operatorname{Tr} \mathbf A(\omega) = \sum_i A_{ii}(\omega)$.
> In Kohn–Sham DFT the spectral function is *approximated* by
> the KS density of states, which is a sum of delta peaks at the
> KS eigenvalues — this is the *physical content* of the
> "Kohn–Sham band structure" of chapter 07.

---

## 7. Special functions

### 7.1 Hermite polynomials

The **physicists' Hermite polynomials** are defined by

\begin{equation}
\label{eq:ch-extra-hermite}
H_n(x) \;=\; (-1)^n e^{x^2}\, \frac{d^n}{dx^n}\, e^{-x^2} .
\end{equation}

The first few are $H_0 = 1$, $H_1 = 2x$,
$H_2 = 4x^2 - 2$, $H_3 = 8x^3 - 12x$, $H_4 = 16x^4 -
48x^2 + 12$. They satisfy the orthogonality relation

\begin{equation}
\label{eq:ch-extra-hermite-orth}
\int_{-\infty}^{\infty} H_m(x)\, H_n(x)\, e^{-x^2}\, dx \;=\; 2^n n!\,\sqrt{\pi}\, \delta_{mn} .
\end{equation}

The **generating function**
$\exp(2xt - t^2) = \sum_n H_n(x) t^n / n!$ is the link to
the **Glauber coherent states** of chapter 01 (§1.9.5). Cross-
reference: chapter 01 (§1.9.4), chapter 06 (§6.13.5, the NAO
polarisation-orbital recipe uses energy derivatives of bound-
state radial functions, which in the harmonic-oscillator basis
are Hermite polynomials).

### 7.2 Laguerre polynomials

The **associated Laguerre polynomials** $L_n^\alpha(x)$ are
defined by the generating function

\begin{equation}
\label{eq:ch-extra-laguerre-gen}
\frac{e^{-x t/(1-t)}}{(1-t)^{\alpha+1}} \;=\; \sum_{n=0}^{\infty} L_n^\alpha(x)\, t^n ,
\end{equation}

or, equivalently, by the differential equation

\begin{equation}
\label{eq:ch-extra-laguerre-eq}
x\, \frac{d^2 L_n^\alpha}{dx^2} + (\alpha + 1 - x)\, \frac{dL_n^\alpha}{dx} + n\, L_n^\alpha(x) \;=\; 0 .
\end{equation}

The orthogonality relation is

\begin{equation}
\label{eq:ch-extra-laguerre-orth}
\int_0^\infty L_m^\alpha(x)\, L_n^\alpha(x)\, x^\alpha e^{-x}\, dx \;=\; \frac{\Gamma(n+\alpha+1)}{n!}\, \delta_{mn} .
\end{equation}

The hydrogen radial wavefunctions of chapter 01 (§1.10) are
$L_{n-\ell-1}^{2\ell+1}$ evaluated at $2Zr/n$. Cross-reference:
chapter 01 (§1.10.5), chapter 06 (the radial STO primitives).

### 7.3 Legendre polynomials

The **Legendre polynomials** $P_\ell(\cos\theta)$ are
restrictions of the spherical harmonics to $m = 0$. They
satisfy the **addition theorem**

\begin{equation}
\label{eq:ch-extra-legen-add}
P_\ell(\cos\gamma) \;=\; \frac{4\pi}{2\ell+1} \sum_{m=-\ell}^{\ell} Y_\ell^{m*}(\hat{\mathbf n}_1)\, Y_\ell^m(\hat{\mathbf n}_2) ,
\end{equation}

where $\gamma$ is the angle between the two unit vectors
$\hat{\mathbf n}_1$ and $\hat{\mathbf n}_2$. This identity is
the workhorse of the **molecular multipole expansion** and of
the **angular-momentum coupling** that underlies the Gaunt
integral of chapter 01 (§1.10.7). Cross-reference: chapter 01
(§1.10.7).

### 7.4 Spherical harmonics

The **spherical harmonics** are the simultaneous eigenfunctions
of $\hat L^2$ and $\hat L_z$ in $L^2(S^2)$:

\begin{equation}
\label{eq:ch-extra-sph}
\hat L^2 Y_\ell^m(\theta, \phi) \;=\; \ell(\ell+1)\, Y_\ell^m , \qquad
\hat L_z Y_\ell^m \;=\; m\, Y_\ell^m ,
\end{equation}

with $\ell = 0, 1, 2, \dots$ and $-\ell \le m \le \ell$. The
**orthonormality** is

\begin{equation}
\label{eq:ch-extra-sph-orth}
\int_0^{2\pi} d\phi \int_0^{\pi} \sin\theta\, d\theta\, Y_\ell^{m*}(\theta, \phi)\, Y_{\ell'}^{m'}(\theta, \phi)
\;=\; \delta_{\ell\ell'}\, \delta_{mm'} .
\end{equation}

The chapters use the **Condon–Shortley phase convention**
(an explicit $(-1)^m$ for $m > 0$), and the real
spherical harmonics for cubic harmonics. The parity
$Y_\ell^m(-\hat{\mathbf r}) = (-1)^\ell Y_\ell^m(\hat{\mathbf r})$
is what gives the **selection rule** $\Delta \ell = \pm 1$
for electric-dipole transitions (chapter 01, §1.10.8).
Cross-reference: chapters 01 (§1.10.2, §1.10.7), 03 (the
Gaunt integral), 06 (real spherical harmonics in NAO basis
sets).

### 7.5 Bessel functions

The **Bessel functions of the first kind** $J_\nu(x)$ satisfy
Bessel's equation

\begin{equation}
\label{eq:ch-extra-bessel}
x^2 \frac{d^2 J_\nu}{dx^2} + x \frac{dJ_\nu}{dx} + (x^2 - \nu^2)\, J_\nu \;=\; 0 ,
\end{equation}

with the small- and large-$x$ asymptotics
$J_\nu(x) \sim (x/2)^\nu / \Gamma(\nu+1)$ for $x \to 0$
and $J_\nu(x) \sim \sqrt{2/(\pi x)} \cos(x - \nu\pi/2 - \pi/4)$
for $x \to \infty$. The **spherical Bessel functions**
$j_\ell(x) = \sqrt{\pi/(2x)}\, J_{\ell+1/2}(x)$ are the radial
parts of the free-particle spherical waves. The free-particle
Green function of equation \eqref{eq:ch-extra-g0} admits the
partial-wave expansion

\begin{equation}
\label{eq:ch-extra-g0-pw}
G_0(\mathbf r, \mathbf r'; E) \;=\; -i k \sum_{\ell, m} j_\ell(k r_<)\, h^{(1)}_\ell(k r_>)\, Y_\ell^m(\hat{\mathbf r})\, Y_\ell^{m*}(\hat{\mathbf r}') ,
\end{equation}

where $h^{(1)}_\ell$ is the spherical Hankel function of the
first kind and $r_< = \min(r, r')$, $r_> = \max(r, r')$.
Cross-reference: chapter 01 (§1.11.3, free-particle path
integral), chapter 07 (Bessel-function solution of the
nearly-free-electron band structure).

### 7.6 The gamma function

The **Euler gamma function**

\begin{equation}
\label{eq:ch-extra-gamma}
\Gamma(z) \;=\; \int_0^\infty t^{z-1} e^{-t}\, dt , \qquad
\operatorname{Re} z > 0 ,
\end{equation}

extends the factorial to non-integer arguments: $\Gamma(n) =
(n-1)!$ for positive integer $n$. The **reflection formula**

\begin{equation}
\label{eq:ch-extra-gamma-reflect}
\Gamma(z)\, \Gamma(1-z) \;=\; \frac{\pi}{\sin(\pi z)} ,
\end{equation}

and the **Legendre duplication formula**

\begin{equation}
\label{eq:ch-extra-gamma-dup}
\Gamma(z)\, \Gamma\!\left(z + \tfrac{1}{2}\right) \;=\; \frac{\sqrt{\pi}}{2^{2z-1}}\, \Gamma(2z) ,
\end{equation}

are the identities used in evaluating the **Gaussian
overlaps** and **Boys-function integrals** of chapter 06. The
**Bohr radius** and **Hartree energy** of atomic units are
$\Gamma$-function normalisations in disguise. Cross-reference:
chapters 01, 03, 06.

### 7.7 The Boys function

The **Boys function**

\begin{equation}
\label{eq:ch-extra-boys}
F_0(t) \;=\; \int_0^1 e^{-t u^2}\, du
\;=\; \frac{1}{2}\sqrt{\frac{\pi}{t}}\, \operatorname{erf}(\sqrt{t}) ,
\qquad F_0(0) = 1 ,
\end{equation}

handles the Coulomb singularity $1/r_{12}$ inside the
primitive four-centre electron-repulsion integral of
chapter 06 (§6.3). The general
$F_n(t) = \int_0^1 u^{2n} e^{-t u^2}\, du$ appears in the
higher-angular-momentum recursion. Cross-reference: chapter 06
(§6.3), chapter 03 (§3.6.3).

### 7.8 The error function

The **error function** $\operatorname{erf}(x)$ and its
complement $\operatorname{erfc}(x) = 1 - \operatorname{erf}(x)$:

\begin{equation}
\label{eq:ch-extra-erf}
\operatorname{erf}(x) \;=\; \frac{2}{\sqrt\pi} \int_0^x e^{-t^2}\, dt ,
\qquad \operatorname{erfc}(x) \;=\; \frac{2}{\sqrt\pi} \int_x^\infty e^{-t^2}\, dt .
\end{equation}

Asymptotics: $\operatorname{erf}(x) \to 1$ as $x \to \infty$ and
$\operatorname{erfc}(x) \sim e^{-x^2}/(x\sqrt\pi)$ as
$x \to \infty$. Used in the **Boys function** above, in the
**range-separation of the Coulomb kernel** (chapter 05, §5.5),
and in the **Gaussian smearing** occupation function
(chapter 07, §7.6.3). Cross-reference: chapters 03, 05, 06, 07.

---

## 8. Tensor identities

### 8.1 The Kronecker delta

\begin{equation}
\label{eq:ch-extra-kron}
\delta_{ij} \;=\; \begin{cases} 1, & i = j, \\ 0, & i \ne j. \end{cases}
\end{equation}

The **completeness** of an orthonormal basis is
$\sum_i \lvert i \rangle \langle i \rvert = \hat 1$, which in
index notation is $\sum_i v_i w_i = \mathbf v \cdot \mathbf w$
and in tensor notation is
$\sum_i e_i \otimes e_i = \mathbf 1$. The Kronecker $\delta$
is the **identity tensor on $\mathbb R^n$**.

### 8.2 The Levi–Civita symbol

The three-dimensional **Levi–Civita symbol** is totally
antisymmetric in its three indices:

\begin{equation}
\label{eq:ch-extra-levicivita}
\epsilon_{ijk} \;=\;
\begin{cases}
+1 & \text{even permutation of } (1, 2, 3), \\
-1 & \text{odd permutation of } (1, 2, 3), \\
0 & \text{otherwise}.
\end{cases}
\end{equation}

The two **Levi–Civita contraction identities** every DFT code
uses are

\begin{align}
\sum_k \epsilon_{ijk}\, \epsilon_{\ell m k} &\;=\; \delta_{i\ell}\, \delta_{jm} - \delta_{im}\, \delta_{j\ell} , \label{eq:ch-extra-eps2} \\
\sum_j \epsilon_{ijk}\, \epsilon_{\ell j m} &\;=\; \delta_{i\ell}\, \delta_{km} - \delta_{im}\, \delta_{k\ell} . \label{eq:ch-extra-eps1}
\end{align}

The **cross product** is
$(\mathbf a \times \mathbf b)_i = \sum_{jk} \epsilon_{ijk}\, a_j b_k$;
the **scalar triple product** is
$\mathbf a \cdot (\mathbf b \times \mathbf c) = \sum_{ijk} \epsilon_{ijk}\, a_i b_j c_k$.
The **angular momentum** $\hat{\mathbf L} = \hat{\mathbf r} \times \hat{\mathbf p}$
is the prototype.

### 8.3 Einstein summation convention

Repeated upper and lower indices are summed over their range.
For an orthogonal basis, upper and lower indices are equivalent
and the convention reduces to summing over any repeated index.
Examples used in the chapters:

\begin{align}
\mathbf F \mathbf c_i &\;=\; \sum_{\mu\nu} F_{\mu\nu}\, c_{\nu i} \quad &\text{(matrix–vector)} , \label{eq:ch-extra-eins-mat} \\
E_\text{el} &\;=\; \frac{1}{2} \sum_{\mu\nu} P_{\nu\mu}\, (h_{\mu\nu} + F_{\mu\nu}) \quad &\text{(half-trace)} . \label{eq:ch-extra-eins-half}
\end{align}

The `numpy.einsum` call in chapter 03 (§3.3) implements these
contractions verbatim. Cross-reference: chapters 03, 04, 06.

### 8.4 Rotation of tensors

Under an orthogonal transformation $R$ with $R^T R = \mathbf 1$
and $\det R = +1$ (proper rotation), a rank-2 tensor
transforms as $A'_{ij} = \sum_{k\ell} R_{ik}\, R_{j\ell}\, A_{k\ell}$.
For a **vector** ($\mathbf v' = R \mathbf v$) and a **scalar**
($\mathbf v^T A \mathbf w$ invariant), the pattern is the same.
The **Wigner D-matrix** $D^\ell_{m,m'}(R)$ is the
$\ell$-dimensional representation of $R$ on the
$Y_\ell^m$ basis. Cross-reference: chapter 07 (the action of
the point group on Bloch states at $\mathbf k$).

---

## 9. Linear algebra

### 9.1 Eigenvalues, eigenvectors, spectral theorem

A square matrix $\mathbf A$ has the **eigendecomposition**

\begin{equation}
\label{eq:ch-extra-eig}
\mathbf A \mathbf v_i \;=\; a_i \mathbf v_i ,
\end{equation}

where $a_i$ are the **eigenvalues** and $\mathbf v_i$ the
**eigenvectors**. The **spectral theorem** says that a
**Hermitian** matrix ($\mathbf A^\dagger = \mathbf A$) has
**real eigenvalues** and a **complete orthonormal** set of
eigenvectors. In matrix form,

\begin{equation}
\label{eq:ch-extra-spec}
\mathbf A \;=\; \mathbf U\, \boldsymbol\Lambda\, \mathbf U^\dagger ,
\end{equation}

with $\mathbf U$ unitary and $\boldsymbol\Lambda$ real
diagonal. This is the **diagonalisation** that
`numpy.linalg.eigh` performs. The Hermitian eigenvalue problem
is the workhorse of DFT — every Fock-matrix diagonalisation
(HF, KS) is a Hermitian eigenproblem. Cross-reference:
chapters 03 (§3.6.2), 04, 06 (§6.1).

### 9.2 Generalised eigenvalue problem

A **generalised eigenproblem** is
$\mathbf A \mathbf v = \lambda \mathbf B \mathbf v$ with
$\mathbf B$ positive-definite Hermitian. It reduces to the
standard eigenproblem by **Löwdin orthogonalisation**
$\mathbf X = \mathbf B^{-1/2}$:

\begin{equation}
\label{eq:ch-extra-gep}
\mathbf X^\dagger \mathbf A \mathbf X\, \mathbf c' \;=\; \lambda\, \mathbf c', \qquad
\mathbf v \;=\; \mathbf X \mathbf c' .
\end{equation}

This is the **Roothaan–Hall** equation
$\mathbf F \mathbf C = \mathbf S \mathbf C \boldsymbol\varepsilon$
of chapters 03 (§3.6) and 06 (§6.1). The standard numerical
recipe is `scipy.linalg.eigh(F, S)`, which forms
$\mathbf X$ by Cholesky factorisation of $\mathbf S$. Cross-
reference: chapters 03, 06.

### 9.3 Singular value decomposition (SVD)

Every $m \times n$ matrix $\mathbf A$ admits the decomposition

\begin{equation}
\label{eq:ch-extra-svd}
\mathbf A \;=\; \mathbf U\, \boldsymbol\Sigma\, \mathbf V^\dagger ,
\end{equation}

with $\mathbf U$ $(m \times m)$ unitary, $\mathbf V$ $(n \times n)$
unitary, and $\boldsymbol\Sigma = \operatorname{diag}(\sigma_1, \dots, \sigma_r, 0, \dots)$
with $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$ the
**singular values**. The SVD is the basis of the **density-
fitting / resolution-of-the-identity** approximation to the
ERI tensor of chapter 06 (§6.12). Cross-reference: chapter 06
(§6.12, the resolution-of-the-identity approximation).

### 9.4 Trace of a matrix

\begin{equation}
\label{eq:ch-extra-tr}
\operatorname{Tr}\mathbf A \;=\; \sum_i A_{ii} \;=\; \sum_i a_i ,
\end{equation}

where $a_i$ are the eigenvalues of $\mathbf A$. The second
equality is the **trace-invariance under similarity**: the
trace of $\mathbf A$ equals the trace of $\mathbf U^\dagger
\mathbf A \mathbf U$, and the diagonal form has the eigenvalues
on the diagonal. Cross-reference: chapters 03, 04.

### 9.5 Determinant of a matrix

\begin{equation}
\label{eq:ch-extra-det}
\det \mathbf A \;=\; \prod_i a_i \;=\; e^{\operatorname{Tr}\ln \mathbf A} .
\end{equation}

The last form is the **Jacobi formula** for the derivative of
a determinant: $d(\ln \det \mathbf A) = \operatorname{Tr}(\mathbf A^{-1}\, d\mathbf A)$.
The determinant of an antisymmetric matrix
is the **square of the Pfaffian**; the determinant of a
Slater matrix is the **Slater determinant** of chapter 02
(§2.2). Cross-reference: chapter 02.

### 9.6 Matrix exponential

The **matrix exponential** is defined by the Taylor series

\begin{equation}
\label{eq:ch-extra-matexp}
e^{\mathbf A} \;=\; \sum_{n=0}^{\infty} \frac{\mathbf A^n}{n!} ,
\end{equation}

which converges for every square matrix. For Hermitian
$\mathbf A = \mathbf U \boldsymbol\Lambda \mathbf U^\dagger$,

\begin{equation}
\label{eq:ch-extra-matexp-diag}
e^{\mathbf A} \;=\; \mathbf U\, e^{\boldsymbol\Lambda}\, \mathbf U^\dagger ,
\qquad e^{\boldsymbol\Lambda} = \operatorname{diag}(e^{\lambda_1}, e^{\lambda_2}, \dots) .
\end{equation}

Used in the **time-evolution operator**
$\hat U(t) = e^{-i \hat H t}$ of chapter 01 (§1.7.1) and in
the **Löwdin orthogonaliser**
$\mathbf X = \mathbf S^{-1/2}$ of chapter 03 (§3.6.6). Cross-
reference: chapters 01, 03.

### 9.7 Sherman–Morrison–Woodbury identities

\begin{align}
(\mathbf A + \mathbf u \mathbf v^T)^{-1} &\;=\; \mathbf A^{-1} - \frac{\mathbf A^{-1} \mathbf u \mathbf v^T \mathbf A^{-1}}{1 + \mathbf v^T \mathbf A^{-1} \mathbf u} \quad &\text{(rank-1)} , \label{eq:ch-extra-sm1} \\
(\mathbf A + \mathbf U \mathbf C \mathbf V^T)^{-1} &\;=\; \mathbf A^{-1} - \mathbf A^{-1} \mathbf U (\mathbf C^{-1} + \mathbf V^T \mathbf A^{-1} \mathbf U)^{-1} \mathbf V^T \mathbf A^{-1} \quad &\text{(rank-}k\text{)} . \label{eq:ch-extra-smk}
\end{align}

The first is the **Sherman–Morrison formula**, the second the
**Woodbury identity**. The latter is the workhorse of the
**Broyden update** in chapter 04 (§4.6.3). Cross-reference:
chapter 04.

---

## 10. Differential operators

The chapters use the standard $\nabla$ operators of vector
calculus in three coordinate systems: **Cartesian**, **spherical
polar**, and **cylindrical**.

### 10.1 Cartesian

\begin{align}
\nabla f &\;=\; \left( \frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y},\, \frac{\partial f}{\partial z} \right) , \label{eq:ch-extra-grad} \\
\nabla \cdot \mathbf F &\;=\; \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z} , \label{eq:ch-extra-div} \\
\nabla \times \mathbf F &\;=\; \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z},\;
                                 \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x},\;
                                 \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) , \label{eq:ch-extra-curl} \\
\nabla^2 f &\;=\; \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2} . \label{eq:ch-extra-lap-cart}
\end{align}

The **vector Laplacian** acts component-wise on a vector field:
$\nabla^2 \mathbf F = (\nabla^2 F_x, \nabla^2 F_y, \nabla^2 F_z)$.
The **Laplacian on a tensor** is the same: one component at a
time. The **gradient of a dot product** is

\begin{equation}
\label{eq:ch-extra-grad-dot}
\nabla (\mathbf A \cdot \mathbf B) \;=\; (\mathbf A \cdot \nabla) \mathbf B + (\mathbf B \cdot \nabla) \mathbf A + \mathbf A \times (\nabla \times \mathbf B) + \mathbf B \times (\nabla \times \mathbf A) .
\end{equation}

### 10.2 Spherical polar coordinates

With $r = |\mathbf r|$, $\theta$ the polar angle from $\hat z$
and $\phi$ the azimuth,

\begin{align}
\nabla f &\;=\; \hat{\mathbf r}\, \frac{\partial f}{\partial r} + \hat{\boldsymbol\theta}\, \frac{1}{r}\, \frac{\partial f}{\partial \theta} + \hat{\boldsymbol\phi}\, \frac{1}{r \sin\theta}\, \frac{\partial f}{\partial \phi} , \label{eq:ch-extra-grad-sph} \\
\nabla \cdot \mathbf F &\;=\; \frac{1}{r^2} \frac{\partial (r^2 F_r)}{\partial r}
                       + \frac{1}{r \sin\theta} \frac{\partial (\sin\theta\, F_\theta)}{\partial \theta}
                       + \frac{1}{r \sin\theta} \frac{\partial F_\phi}{\partial \phi} , \label{eq:ch-extra-div-sph} \\
\nabla^2 f &\;=\; \frac{1}{r^2} \frac{\partial}{\partial r} \!\left( r^2 \frac{\partial f}{\partial r} \right)
                + \frac{1}{r^2 \sin\theta} \frac{\partial}{\partial \theta} \!\left( \sin\theta\, \frac{\partial f}{\partial \theta} \right)
                + \frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2} . \label{eq:ch-extra-lap-sph}
\end{align}

The angular part of $\nabla^2$ is $-\hat L^2 / r^2$, so
$\nabla^2 (R Y_\ell^m) = [r^{-2} \partial_r(r^2 \partial_r R) -
\ell(\ell+1)/r^2 R]\, Y_\ell^m$ — the **radial equation** of
chapter 01 (§1.10.3). Cross-reference: chapter 01 (§1.10).

### 10.3 Cylindrical coordinates

With $\rho = \sqrt{x^2 + y^2}$, $\phi$ the azimuth, and $z$ the
axial coordinate,

\begin{align}
\nabla f &\;=\; \hat{\boldsymbol\rho}\, \frac{\partial f}{\partial \rho} + \hat{\boldsymbol\phi}\, \frac{1}{\rho}\, \frac{\partial f}{\partial \phi} + \hat{\mathbf z}\, \frac{\partial f}{\partial z} , \label{eq:ch-extra-grad-cyl} \\
\nabla^2 f &\;=\; \frac{1}{\rho} \frac{\partial}{\partial \rho} \!\left( \rho \frac{\partial f}{\partial \rho} \right)
                + \frac{1}{\rho^2} \frac{\partial^2 f}{\partial \phi^2}
                + \frac{\partial^2 f}{\partial z^2} . \label{eq:ch-extra-lap-cyl}
\end{align}

The cylindrical Laplacian is the natural operator for systems
with axial symmetry: nanotubes, wires, the
**near-degeneracy** of the $p_x, p_y$ orbitals in
transition-metal complexes. Used in chapter 07 when working
out the band structure of a **single-wall nanotube** or a
**2-D electron gas** confined to a wire.

### 10.4 Vector identities

\begin{align}
\nabla \cdot (\nabla \times \mathbf F) &\;=\; 0 , \label{eq:ch-extra-vec-id1} \\
\nabla \times (\nabla f) &\;=\; \mathbf 0 , \label{eq:ch-extra-vec-id2} \\
\nabla \times (\nabla \times \mathbf F) &\;=\; \nabla(\nabla \cdot \mathbf F) - \nabla^2 \mathbf F , \label{eq:ch-extra-vec-id3} \\
\nabla \cdot (f \mathbf F) &\;=\; f\, \nabla \cdot \mathbf F + \mathbf F \cdot \nabla f , \label{eq:ch-extra-vec-id4} \\
\nabla \times (f \mathbf F) &\;=\; f\, \nabla \times \mathbf F + \nabla f \times \mathbf F . \label{eq:ch-extra-vec-id5}
\end{align}

Identity \eqref{eq:ch-extra-vec-id3} is the reason the
**Coulomb gauge** $\nabla \cdot \mathbf A = 0$ and the
**continuity equation** of chapter 01 (§1.7.4) have the
structure they do. Cross-reference: chapter 01.

---

## 11. Functional derivatives

The chapters use the functional derivative to derive the
**Kohn–Sham potential**
$\hat v_\text{xc} = \delta E_\text{xc}/\delta \rho$
(chapter 04, §4.2) and the **forces on the nuclei** via the
Hellmann–Feynman theorem (chapter 04, §4.7.1). This section
collects the working rules.

### 11.1 Definition

The **functional derivative** $\delta F / \delta f(x)$ of a
functional $F[f]$ is the function (or distribution) such that
for every variation $\delta f(x)$,

\begin{equation}
\label{eq:ch-extra-fdef}
\delta F \;=\; \int \frac{\delta F}{\delta f(x)}\, \delta f(x)\, dx .
\end{equation}

The simplest case: for $F[f] = \int g(x)\, f(x)\, dx$, the
functional derivative is $\delta F / \delta f(x) = g(x)$.
For $F[f] = f(x_0)^2$, the derivative is
$\delta F / \delta f(x) = 2 f(x_0) \delta(x - x_0)$.

### 11.2 Chain rule

If $F = G[f, h]$ depends on $f$ and $h$ (which themselves
depend on the same underlying variables), then

\begin{equation}
\label{eq:ch-extra-fchain}
\frac{\delta F}{\delta g(y)} \;=\; \int dx\, \frac{\delta F}{\delta f(x)} \frac{\delta f(x)}{\delta g(y)} + \int dx\, \frac{\delta F}{\delta h(x)} \frac{\delta h(x)}{\delta g(y)} .
\end{equation}

Used in deriving the **chain rule for the KS potential**: the
density depends on the orbitals, the orbitals depend on the
potential, and the potential depends on the density.

### 11.3 Integration by parts

Under a functional integral, integration by parts swaps a
derivative at no cost (boundary terms vanish under the standard
assumptions of the variational principle):

\begin{equation}
\label{eq:ch-extra-fibp}
\int \frac{\delta F}{\delta f(x)} \frac{\partial f}{\partial x}\, dx \;=\; -\int f(x)\, \frac{\partial}{\partial x} \frac{\delta F}{\delta f(x)}\, dx .
\end{equation}

The boundary term is $\left[ f\, \delta F/\delta f \right]_{-\infty}^{+\infty}$
and vanishes if $f \to 0$ at infinity (or if the boundary
variations are restricted to vanish). Used in the derivation
of the **Euler–Lagrange equation** in §12 below and in the
**Pulay-force** integration by parts of chapter 04 (§4.7.3).

### 11.4 Functional derivative of a density-functional

For the Kohn–Sham energy
$E[\rho] = T_s[\rho] + \int \rho v_\text{ext}\, d\mathbf r + J[\rho] + E_\text{xc}[\rho]$,
the functional derivative with respect to $\rho(\mathbf r)$ is

\begin{equation}
\label{eq:ch-extra-vxc}
\frac{\delta E}{\delta \rho(\mathbf r)} \;=\; v_\text{ext}(\mathbf r) + v_\text{H}[\rho](\mathbf r) + \frac{\delta E_\text{xc}}{\delta \rho(\mathbf r)} \;=\; v_\text{eff}(\mathbf r) .
\end{equation}

The right-hand side is the **Kohn–Sham effective potential**.
The functional derivative $\delta E_\text{xc}/\delta\rho$ is
the **XC potential** of chapter 04 (§4.2, §4.5). Cross-
reference: chapter 04.

---

## 12. Variational calculus

### 12.1 The action

The **action** is the time-integral of a Lagrangian:

\begin{equation}
\label{eq:ch-extra-action}
\mathcal S[q] \;=\; \int_{t_1}^{t_2} \mathcal L(q(t), \dot q(t), t)\, dt .
\end{equation}

The **principle of stationary action** says the physical
trajectory $q(t)$ is an extremum of $\mathcal S[q]$ against
variations $\delta q(t)$ that vanish at the endpoints. The
Lagrangian of the **TDSE derivation** of chapter 01 (§1.7.2)
is the **Dirac–Frenkel (McLachlan) Lagrangian**
$\mathcal L = \langle \psi \rvert i \partial_t - \hat H \rvert \psi \rangle$,
which is a *functional* of the time-dependent state.

### 12.2 The Euler–Lagrange equation

For a Lagrangian $\mathcal L(q, \dot q, t)$, the stationary-
action condition $\delta \mathcal S = 0$ gives the **Euler–
Lagrange equation**

\begin{equation}
\label{eq:ch-extra-el}
\frac{d}{dt} \frac{\partial \mathcal L}{\partial \dot q} - \frac{\partial \mathcal L}{\partial q} \;=\; 0 .
\end{equation}

The generalisation to several coordinates is
$\partial_t (\partial \mathcal L / \partial \dot q_i) -
\partial \mathcal L / \partial q_i = 0$. The Euler–Lagrange
equation of the Dirac–Frenkel Lagrangian of chapter 01
(§1.7.2) is the **time-dependent Schrödinger equation** —
the TDSE is the *unique* dynamics consistent with
stationary action *and* unitarity.

### 12.3 The Euler–Lagrange equation in field theory

For a Lagrangian density $\mathcal L = \mathcal L(\phi, \partial_\mu \phi)$,

\begin{equation}
\label{eq:ch-extra-el-field}
\partial_\mu \frac{\partial \mathcal L}{\partial (\partial_\mu \phi)} - \frac{\partial \mathcal L}{\partial \phi} \;=\; 0 .
\end{equation}

This is the **Dirac–Frenkel variational principle** of chapter
01 (§1.7.2) written for the wavefunction field. The
**time-dependent KS equations** of chapter 04 are recovered by
restricting $|\psi(t)\rangle$ to a single Slater determinant
and varying over the orbital rotations.

### 12.4 Constrained variation

A constrained minimisation (e.g. orthonormality of the
orbitals in HF/KS) introduces a **Lagrange multiplier**
matrix $\boldsymbol\Lambda$ in the variational principle:

\begin{equation}
\label{eq:ch-extra-constraint}
\delta \bigl[ E - \operatorname{Tr}(\boldsymbol\Lambda^\dagger (\mathbf C^\dagger \mathbf S \mathbf C - \mathbf 1)) \bigr] \;=\; 0 .
\end{equation}

Differentiating with respect to the MO coefficients $\mathbf C$
gives the **Roothaan–Hall equation** (chapters 03 and 06),
with $\boldsymbol\Lambda$ identified as the diagonal orbital
energy matrix $\boldsymbol\varepsilon$. Cross-reference:
chapters 03, 06.

---

## 13. The Coulomb kernel $1 / |\mathbf r - \mathbf r'|$ and the Ewald sum

The Coulomb kernel is the single most important special
function in DFT. Its Fourier transform, its decomposition
into short- and long-range parts, and the Ewald sum that
renders the lattice sum of $1/R$ convergent are the three
identities every solid-state code needs.

### 13.1 Fourier transform

The Fourier transform of the Coulomb kernel is

\begin{equation}
\label{eq:ch-extra-fourier-coulomb}
\int_{\mathbb R^3} \frac{e^{-i \mathbf k \cdot \mathbf r}}{r}\, d\mathbf r \;=\; \frac{4\pi}{k^2} ,
\end{equation}

with the convention of §5.2 above (no $1/(2\pi)^{3/2}$
prefactor). Equivalently,

\begin{equation}
\label{eq:ch-extra-poisson}
-\nabla^2 \left( \frac{1}{\lvert \mathbf r - \mathbf r' \rvert} \right) \;=\; 4\pi\, \delta(\mathbf r - \mathbf r') ,
\end{equation}

i.e. $1/r$ is the Green's function of the **Poisson equation**
in three dimensions. The Fourier-space form
$v_\text{Coulomb}(k) = 4\pi / k^2$ is what makes the Hartree
operator **diagonal in reciprocal space** — a $k$-space
Hartree potential is just
$v_H(\mathbf G) = (4\pi / G^2) \rho(\mathbf G)$, and the
**plane-wave Hartree-energy evaluation** of chapter 07
(§7.5) is therefore an $\mathcal O(N_\text{PW} \log N_\text{PW})$
FFT per SCF iteration. Cross-reference: chapters 04 (§4.4),
07 (§7.5).

### 13.2 Range separation

The Coulomb kernel can be split into a **short-range** and a
**long-range** part by an error-function partition

\begin{equation}
\label{eq:ch-extra-range-sep}
\frac{1}{r_{12}} \;=\; \underbrace{\frac{\operatorname{erfc}(\omega r_{12})}{r_{12}}}_\text{short range}
                     + \underbrace{\frac{\operatorname{erf}(\omega r_{12})}{r_{12}}}_\text{long range} .
\end{equation}

The range-separation parameter $\omega$ controls the split:
$\omega \to 0$ recovers the full $1/r$ on the long-range
side; $\omega \to \infty$ puts everything on the short-range
side. The two pieces are treated with different functionals
in **range-separated hybrid** XC functionals (chapter 05,
§5.5). Cross-reference: chapter 05.

### 13.3 The Ewald sum

The **lattice sum**

\begin{equation}
\label{eq:ch-extra-lattice}
V_\text{Mad} \;=\; \frac{1}{2} \sum_{\mathbf R \ne 0} \frac{1}{\lvert \mathbf R \rvert}
\end{equation}

is **conditionally convergent** (depends on the order of
summation). The **Ewald decomposition** renders it absolutely
convergent by writing

\begin{equation}
\label{eq:ch-extra-ewald}
\frac{1}{r} \;=\; \underbrace{\frac{\operatorname{erfc}(\alpha r)}{r}}_\text{short range, real space}
                + \underbrace{\frac{\operatorname{erf}(\alpha r)}{r}}_\text{long range, reciprocal space} .
\end{equation}

The sum then splits into three pieces:

\begin{align}
V_\text{Mad} &\;=\; \underbrace{\frac{1}{2} \sum_{\mathbf R \ne 0} \frac{\operatorname{erfc}(\alpha \lvert \mathbf R \rvert)}{\lvert \mathbf R \rvert}}_{V_\text{real}} \label{eq:ch-extra-ewald-real} \\
&\quad + \underbrace{\frac{1}{2\Omega} \sum_{\mathbf G \ne 0} \frac{4\pi e^{-\lvert \mathbf G \rvert^2 / 4\alpha^2}}{G^2}}_{V_\text{recip}} \label{eq:ch-extra-ewald-recip} \\
&\quad - \underbrace{\frac{\alpha}{\sqrt\pi}}_{V_\text{self}} . \label{eq:ch-extra-ewald-self}
\end{align}

The real-space sum $V_\text{real}$ converges rapidly because
$\operatorname{erfc}(\alpha r) \sim e^{-\alpha^2 r^2}$ at large
$r$. The reciprocal-space sum $V_\text{recip}$ converges
rapidly because $e^{-G^2/4\alpha^2}$ kills large $G$. The
self-term $V_\text{self}$ subtracts the spurious interaction
of each ion with its own image, introduced when the long-range
part is summed in reciprocal space. The parameter $\alpha$
trades real-space and reciprocal-space convergence; the
optimal choice is $\alpha \sim \sqrt{\pi}/\text{cell size}$.

The Ewald sum is the **Madelung constant** of the lattice
(for point ions in a compensating background), generalised to
finite-size ions and to the **electron–ion** interaction in
periodic DFT. It is the heart of every plane-wave and
real-space-grid periodic code. Cross-reference: chapters 04
(the Hartree potential in a periodic cell), 07.

### 13.4 The Madelung constant

The **Madelung constant** $\mathcal M$ of a Bravais lattice is
defined by

\begin{equation}
\label{eq:ch-extra-madelung}
V_\text{Mad} \;=\; -\frac{\mathcal M}{2 r_0} ,
\end{equation}

where $r_0$ is the nearest-neighbour distance. Examples:

| Lattice | $\mathcal M$ |
|:--------|:-------------|
| NaCl (rocksalt) | 1.74756… |
| CsCl (bcc) | 1.76267… |
| ZnS (zincblende) | 1.63806… |

The Ewald sum with the appropriate geometry gives these
numbers. Cross-reference: chapter 07 (§7.7, the
nearly-free-electron band structure).

---

## 14. Common integrals

The chapters need a small set of standard integrals over and
over: the **Gaussian** (basis-set normalisation, the Ewald
sum, the path-integral propagator), the **Fermi–Dirac** and
**Bose–Einstein** distributions (finite-temperature DFT, the
electronic entropy of chapter 07), and the **polylogarithm**
that ties them together.

### 14.1 The Gaussian integral

\begin{equation}
\label{eq:ch-extra-gauss}
\int_{-\infty}^{\infty} e^{-a x^2}\, dx \;=\; \sqrt{\frac{\pi}{a}} , \qquad
\int_{-\infty}^{\infty} x^{2n}\, e^{-a x^2}\, dx \;=\; \frac{(2n-1)!!}{(2a)^n} \sqrt{\frac{\pi}{a}} .
\end{equation}

In $d$ dimensions, with $a > 0$,

\begin{equation}
\label{eq:ch-extra-gauss-d}
\int_{\mathbb R^d} e^{-a \mathbf x \cdot \mathbf x}\, d^d x \;=\; \left( \frac{\pi}{a} \right)^{d/2} .
\end{equation}

The Gaussian is the **only** integral that converges in the
*free-particle path integral* of chapter 01 (§1.11.3, problem
3 of §1.13). It is also the workhorse of the **overlap and
kinetic-energy integrals of chapter 06** (§6.3, the Gaussian
product theorem).

### 14.2 The error-function integral

\begin{equation}
\label{eq:ch-extra-erfint}
\int_0^\infty e^{-a x^2}\, \operatorname{erf}(b x)\, dx \;=\; \frac{1}{2\sqrt{a}}\left[ \frac{\pi}{2} - \arctan\!\left( \frac{\sqrt{a}}{b} \right) \right] \quad (a, b > 0) .
\end{equation}

This identity is needed when the Coulomb kernel is split by
the range-separation of §13.2 above: the short-range
contribution to the Hartree energy is a *quadrature* over
Gaussian primitives weighted by an error function. Cross-
reference: chapter 05 (§5.5, range-separated hybrids).

### 14.3 The Fermi–Dirac integral

The **Fermi–Dirac occupation** of chapter 07 (§7.6.3) is

\begin{equation}
\label{eq:ch-extra-fd}
f(\varepsilon) \;=\; \frac{1}{e^{(\varepsilon - \mu)/k_B T} + 1} .
\end{equation}

The corresponding **Fermi–Dirac integral of order $j$** is

\begin{equation}
\label{eq:ch-extra-fdj}
\mathcal F_j(\eta) \;=\; \frac{1}{\Gamma(j+1)} \int_0^\infty \frac{x^j}{e^{x - \eta} + 1}\, dx ,
\end{equation}

with $\eta = \mu / k_B T$ the **reduced chemical potential**.
The Sommerfeld expansion at low temperature gives

\begin{equation}
\label{eq:ch-extra-sommerfeld}
\mathcal F_j(\eta) \;=\; \frac{\eta^{j+1}}{(j+1) \Gamma(j+1)} \left[ 1 + \frac{\pi^2}{6}\, j(j+1)\, \eta^{-2} + \mathcal O(\eta^{-4}) \right] .
\end{equation}

For the density of states $g(\varepsilon)$ of a metal, the
electron number is $N = \int_0^\infty g(\varepsilon) f(\varepsilon) d\varepsilon$.
The Sommerfeld expansion is the bridge from the low-$T$
behaviour to the $T = 0$ band structure of chapter 07. Cross-
reference: chapter 07 (§7.6.3).

### 14.4 The Bose–Einstein integral

The **Bose–Einstein occupation** is

\begin{equation}
\label{eq:ch-extra-be}
n(\varepsilon) \;=\; \frac{1}{e^{(\varepsilon - \mu)/k_B T} - 1} ,
\end{equation}

with $\varepsilon > \mu$ (chemical potential below the band
edge for a stable Bose gas). The corresponding **Bose–Einstein
integral of order $j$** is

\begin{equation}
\label{eq:ch-extra-be-j}
\mathcal B_j(\eta) \;=\; \frac{1}{\Gamma(j+1)} \int_0^\infty \frac{x^j}{e^{x - \eta} - 1}\, dx \;=\; \operatorname{Li}_{j+1}(e^\eta) \zeta(j+1) / \zeta(j+1) \cdots
\end{equation}

The Bose–Einstein distribution describes **phonons** (chapter
10, vibrations in molecules and solids) and the photon gas.
The phonon contribution to the **free energy** of a harmonic
crystal is

\begin{equation}
\label{eq:ch-extra-phonon-f}
F_\text{ph} \;=\; k_B T \sum_{\mathbf q, s} \ln\!\bigl(1 - e^{-\hbar\omega_{\mathbf q s}/k_B T}\bigr) ,
\end{equation}

where the sum is over phonon branches $s$ and wavevectors
$\mathbf q$. Cross-reference: chapter 10 (phonons), chapter 01
(§1.2, P6 for bosons).

### 14.5 The polylogarithm

The **polylogarithm** $\operatorname{Li}_s(z)$ is defined by
the series

\begin{equation}
\label{eq:ch-extra-polylog}
\operatorname{Li}_s(z) \;=\; \sum_{k=1}^{\infty} \frac{z^k}{k^s} \;=\; \frac{z}{\Gamma(s)} \int_0^\infty \frac{t^{s-1}}{e^t / z - 1}\, dt ,
\end{equation}

convergent for $|z| \le 1$ (real $s > 0$; analytic
continuation elsewhere). The integral form is the
**Bose–Einstein integral** of the previous section. Special
values: $\operatorname{Li}_1(z) = -\ln(1 - z)$,
$\operatorname{Li}_2(1) = \pi^2/6$,
$\operatorname{Li}_3(1) = \zeta(3) \approx 1.20206$,
$\operatorname{Li}_s(1) = \zeta(s)$ (the **Riemann zeta
function**). The **Fermi–Dirac integral** is
$\mathcal F_j(\eta) = -\operatorname{Li}_{j+1}(-e^\eta)$. Cross-
reference: chapter 07 (finite-temperature occupation numbers).

### 14.6 The Bose–Einstein condensation temperature

For a three-dimensional non-interacting Bose gas of $N$
particles in a volume $V$ with mass $m$,

\begin{equation}
\label{eq:ch-extra-bec-tc}
k_B T_c \;=\; \frac{2\pi \hbar^2}{m} \left( \frac{N}{V\, \zeta(3/2)} \right)^{2/3} ,
\end{equation}

where $\zeta(3/2) \approx 2.612$ is the Riemann zeta function.
This is the textbook result that anchors every discussion of
**macroscopic quantum phenomena** in the notes. The DFT
chapters do not derive it, but it appears in the
"what we left out" sections as the canonical example of a
**broken-symmetry ground state** beyond the reach of
single-Slater-determinant theory. Cross-reference: chapter 01
(§1.14, identical-particle statistics for bosons).

### 14.7 The Planck (black-body) integral

\begin{equation}
\label{eq:ch-extra-planck}
\int_0^\infty \frac{x^3}{e^x - 1}\, dx \;=\; \frac{\pi^4}{15} .
\end{equation}

This is the **Stefan–Boltzmann constant** in disguise:
$\sigma = (2\pi^5 k_B^4)/(15 h^3 c^2)$. It is the integral that
sets the scale of the **zero-point radiation** that gives the
**Lamb shift** of chapter 01 (§1.14, "what we left out"). Cross-
reference: chapter 01.

### 14.8 The complete elliptic integrals

The two **complete elliptic integrals** of the first and second
kind,

\begin{align}
K(k) &\;=\; \int_0^{\pi/2} \frac{d\theta}{\sqrt{1 - k^2 \sin^2 \theta}} , \label{eq:ch-extra-ellip-k} \\
E(k) &\;=\; \int_0^{\pi/2} \sqrt{1 - k^2 \sin^2 \theta}\, d\theta , \label{eq:ch-extra-ellip-e}
\end{align}

appear in the **2-D Coulomb problem** and in the **image-charge
sums of surface science**. They are not in the main text of
the DFT Notes but are the right tool when the geometry of a
problem is planar (a graphene sheet, a 2-D electron gas, a
slab in a surface calculation). The values at $k = 1$ are
$K(1) = \infty$ (logarithmic divergence) and $E(1) = 1$.

---

## Where to look for what you forgot

- **NIST Digital Library of Mathematical Functions**
  ([dlmf.nist.gov](https://dlmf.nist.gov)) — the standard
  reference for everything in §7 and §14.
- **Abramowitz & Stegun** (the older print companion to the
  DLMF) — same content, harder to search.
- **Arfken, Weber, Harris** — *Mathematical Methods for
  Physicists*, the standard graduate-level textbook. Covers §5,
  §7, §8, §9, §10.
- **Sakurai** — *Modern Quantum Mechanics*, for everything in
  §1, §2, §4, and the angular-momentum material in §7.4.
- **Helgaker, Jorgensen, Olsen** — *Molecular Electronic-
  Structure Theory*, for the matrix-algebra identities of §9
  in the context of quantum chemistry.
- **Martin** — *Electronic Structure: Basic Theory and
  Practical Methods*, for the DFT-specific identities in §3,
  §6, §11, §12, §13.

> **Disclaimer.** This cheatsheet is a *reference*, not a
> textbook. Every identity is stated without proof; the proof
> is in the linked chapter (and ultimately in the references
> above). Cite the chapter, not the cheatsheet, in any
> publication that uses one of these results.
>
> **Cross-reference index.** Dirac notation: ch. 01. Operator
> algebra: ch. 01. Hilbert-space traces: ch. 03, 04. Second
> quantisation: ch. 01, 02. Fourier transforms: ch. 01, 07.
> Green's functions: ch. 01, 04. Special functions: ch. 01
> (Hermite, Laguerre, spherical harmonics), ch. 06 (Boys,
> erfc), ch. 07 (Bessel). Tensors: ch. 01 (Levi-Civita in
> the angular momentum). Linear algebra: ch. 03, 06.
> Differential operators: ch. 01 (spherical Laplacian, the
> gradient in $\hat v_\text{ext}$), ch. 04 (the gradient
> correction of GGA functionals), ch. 07 (the strain
> derivative of the stress tensor). Functional derivatives:
> ch. 04 (the KS potential), ch. 09 (forces). Variational
> calculus: ch. 01 (the TDSE), ch. 03, 04 (the HF/KS
> eigenvalue equations). Coulomb kernel: ch. 04, 07. Common
> integrals: ch. 07 (Fermi–Dirac and Bose–Einstein).
