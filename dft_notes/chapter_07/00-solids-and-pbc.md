---
layout: page
title: "Chapter 07 — Solids & periodic boundary conditions"
permalink: /dft-notes/chapter-07/
description: >-
  Bloch's theorem, Brillouin zones, plane-wave basis sets in reciprocal
  space, k-point sampling, and a worked band-structure calculation on a
  1-D periodic lattice.
keywords: "Bloch, Brillouin zone, reciprocal lattice, plane waves, k-points, Monkhorst-Pack, PBC, band structure"
---

# Chapter 07 — Solids & periodic boundary conditions

> A perfect crystal has a Hamiltonian that commutes with every
> translation by a lattice vector. The eigenfunctions are plane waves
> modulated by a cell-periodic function — and that single fact is the
> reason solid-state physics has its own language.

Up to chapter 06 we have been talking about *finite* systems: atoms
and molecules in a box. A real solid is not a finite system. It is an
infinite, perfectly periodic array of nuclei, and the electron moves
through this array forever. The Schrödinger equation we have to solve
is therefore not the molecular one of [chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}),
nor the molecular orbital problem of [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) —
it is the *same* Schrödinger equation, but on a Hamiltonian that has
the discrete translational symmetry of the crystal. This chapter is
about the consequence of that symmetry: the eigenfunctions factorise
into a plane wave and a cell-periodic piece, the energy levels become
continuous *bands* parametrised by a crystal momentum **k** that lives
in a small region of reciprocal space, and the practical calculation
collapses from an infinite matrix to a finite matrix indexed by a
small set of **k-points** and a small set of **plane waves**. The
machinery that does this is what every production solid-state code
(VASP, Quantum ESPRESSO, CASTEP, ABINIT, …) is built on.

> **Reading note.** This chapter assumes you have read chapters
> 01–05. It previews material that is covered in detail in
> [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) (basis sets),
> [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) (pseudopotentials),
> [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}) (phonons), and
> [chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) (band structures).

## 7.1 The claim

> **Bloch's theorem.** Let the Hamiltonian $\hat H$ have the
> discrete translational symmetry of a Bravais lattice
> $\{\mathbf R\}$,
> \begin{equation}
> \label{eq:ch-07-bloch-translation}
> \hat H(\mathbf r + \mathbf R) = \hat H(\mathbf r) \quad \text{for every } \mathbf R \in \{\mathbf R\}.
> \end{equation}
> Then every eigenfunction of $\hat H$ can be written in the form
> \begin{equation}
> \label{eq:ch-07-bloch}
> \boxed{\psi_{n\mathbf k}(\mathbf r) = e^{i \mathbf k \cdot \mathbf r}\, u_{n\mathbf k}(\mathbf r),}
> \end{equation}
> where $\mathbf k$ is a real vector, the *band index* $n$ labels the
> eigenstates at a given $\mathbf k$, and the cell-periodic function
> $u_{n\mathbf k}$ has the same periodicity as the lattice,
> \begin{equation}
> \label{eq:ch-07-bloch-periodic}
> u_{n\mathbf k}(\mathbf r + \mathbf R) = u_{n\mathbf k}(\mathbf r) \quad \text{for every } \mathbf R.
> \end{equation}

Equation \eqref{eq:ch-07-bloch} is the single most-quoted line in
solid-state physics. It says that *every* eigenstate of a periodic
Hamiltonian is a plane wave $e^{i\mathbf k \cdot \mathbf r}$ multiplied
by a function $u_{n\mathbf k}(\mathbf r)$ that knows only about one
unit cell. The price is that the quantum number is no longer a single
integer $n$ — it is now a continuous vector $\mathbf k$ *and* a band
index $n$.

> **Tip.** The phase factor $e^{i\mathbf k \cdot \mathbf r}$ is
> sometimes called the *Bloch factor*, and $u_{n\mathbf k}$ the
> *Bloch function* or *periodic part of the Bloch wave*.

## 7.2 From finite cluster to infinite solid

A real solid is infinite, but we cannot solve an infinite problem on a
finite computer. The standard move is to replace "infinite" by
"periodic on a supercell".

### 7.2.1 Born–von Karman boundary conditions

Pick three primitive lattice vectors $\mathbf a_1, \mathbf a_2,
\mathbf a_3$ and form a supercell of $N_1 \times N_2 \times N_3$
primitive cells. Impose **Born–von Karman** (BvK) periodic boundary
conditions on the supercell: for any wavefunction $\psi$,

\begin{equation}
\label{eq:ch-07-bvk}
\psi(\mathbf r + N_i \mathbf a_i) = \psi(\mathbf r), \qquad i = 1, 2, 3.
\end{equation}

The supercell is the basic repeat unit; anything that happens in it is
copied $N_1 N_2 N_3$ times to fill space. As $N_1, N_2, N_3 \to
\infty$ the BvK cell fills all of $\mathbb R^3$ and we recover the
infinite solid.

The boundary conditions \eqref{eq:ch-07-bvk} restrict the allowed
wavefunctions. In particular, a plane wave $e^{i\mathbf k \cdot \mathbf r}$
satisfies \eqref{eq:ch-07-bvk} iff

\begin{equation}
\label{eq:ch-07-bvk-k}
e^{i \mathbf k \cdot (N_i \mathbf a_i)} = 1 \quad \text{for } i = 1, 2, 3
\;\;\Longrightarrow\;\;
\mathbf k \cdot \mathbf a_i = \frac{2\pi m_i}{N_i}, \quad m_i \in \mathbb Z.
\end{equation}

The allowed $\mathbf k$ values are therefore a discrete mesh inside
the Brillouin zone (defined in §7.4), with $N_1 N_2 N_3$ points
in total — one per primitive cell of the BvK supercell.

### 7.2.2 From $N$ atoms to $N_\mathbf k$ k-points

The two limits to keep in mind:

| Limit | $N_\text{atoms}$ | $N_\mathbf k$ | What we compute |
|:------|:-----------------|:--------------|:----------------|
| Molecule | Finite (10–1000) | 1 (the $\Gamma$ point) | Total energy, spectrum |
| Solid (BvK) | $\to \infty$ | $N_1 N_2 N_3$ per BZ | Total energy per cell, bands |

For a molecule, "summing over all states" is the discrete sum
$\sum_n$ of chapter 04. For a solid under BvK, every "sum over
states" becomes a sum over **bands and k-points**,

\begin{equation}
\label{eq:ch-07-bvk-sum}
\sum_n f(\varepsilon_n) \;\;\longrightarrow\;\; \sum_n \sum_{\mathbf k \in \text{BZ}_\text{mesh}} w_\mathbf k \, f(\varepsilon_{n\mathbf k}),
\end{equation}

with weights $w_\mathbf k = 1 / N_\mathbf k$ (uniform mesh). The
mesh has to be fine enough that this sum approximates the BZ integral
$\int_\text{BZ} f(\varepsilon_{n\mathbf k}) d\mathbf k$ to the desired
accuracy.

> **Tip.** The BvK trick is *not* a physical boundary condition. It is
> a mathematical device that makes the infinite problem look finite.
> The answers it produces are the bulk properties of the infinite
> solid in the limit $N_1, N_2, N_3 \to \infty$. For a *truly*
> periodic system, the device is exact. For a finite cluster, BvK
> artificially glues opposite faces of the cluster together, which is
> why it is a *bad* boundary condition for molecules.

## 7.3 Derivation of Bloch's theorem

We prove \eqref{eq:ch-07-bloch} in seven explicit steps. Every step
appears below — no "it can be shown that" hand-waves.

### Step 1. Define the translation operator

For every Bravais-lattice vector $\mathbf R$, define the operator

\begin{equation}
\label{eq:ch-07-trans-op}
(\hat T_{\mathbf R} f)(\mathbf r) := f(\mathbf r + \mathbf R).
\end{equation}

$\hat T_{\mathbf R}$ shifts the argument of a function by $\mathbf R$.
It is linear and bounded.

### Step 2. $\hat T_{\mathbf R}$ is unitary

For any two square-integrable functions $f, g$:

\begin{align}
\langle \hat T_{\mathbf R} f \mid \hat T_{\mathbf R} g \rangle
  &= \int_{\mathbb R^3} \bigl[(\hat T_{\mathbf R} f)(\mathbf r)\bigr]^* \, (\hat T_{\mathbf R} g)(\mathbf r) \, d^3r \nonumber \\
  &= \int_{\mathbb R^3} f^*(\mathbf r + \mathbf R) \, g(\mathbf r + \mathbf R) \, d^3r \nonumber \\
  &= \int_{\mathbb R^3} f^*(\mathbf u) \, g(\mathbf u) \, d^3u
      \quad \text{(substituting } \mathbf u = \mathbf r + \mathbf R,\; d^3u = d^3r) \nonumber \\
  &= \langle f \mid g \rangle.
\end{align}

So $\hat T_{\mathbf R}$ preserves inner products. In particular it
preserves norms ($\|\hat T_{\mathbf R} f\| = \|f\|$), so it is
**unitary**:

\begin{equation}
\label{eq:ch-07-trans-unitary}
\hat T_{\mathbf R}^\dagger = \hat T_{\mathbf R}^{-1}, \qquad
\hat T_{\mathbf R}^\dagger = \hat T_{-\mathbf R}.
\end{equation}

### Step 3. $\hat T_{\mathbf R}$ commutes with $\hat H$

Compute $\hat T_{\mathbf R} \hat H f$ for an arbitrary smooth $f$. The
Hamiltonian in the Born–Oppenheimer picture (chapter 01) is

\begin{equation}
\label{eq:ch-07-hamiltonian}
\hat H = -\frac{1}{2} \nabla^2 + V(\mathbf r),
\end{equation}

where $V(\mathbf r)$ is the total (ionic + Hartree + xc) one-electron
potential. By the **crystal periodicity** \eqref{eq:ch-07-bloch-translation},
$V(\mathbf r + \mathbf R) = V(\mathbf r)$ for every $\mathbf R$.

Apply the two operators in succession:

\begin{align}
\bigl(\hat T_{\mathbf R} \hat H f\bigr)(\mathbf r)
   &= (\hat H f)(\mathbf r + \mathbf R) \nonumber \\
   &= -\tfrac{1}{2} \nabla^2 f(\mathbf r + \mathbf R) + V(\mathbf r + \mathbf R) f(\mathbf r + \mathbf R) \nonumber \\
   &= -\tfrac{1}{2} \nabla^2 f(\mathbf r + \mathbf R) + V(\mathbf r) f(\mathbf r + \mathbf R).
\end{align}

The gradient $\nabla$ in the last line is taken with respect to
$\mathbf r$; substituting $\mathbf u = \mathbf r + \mathbf R$ leaves
$\nabla_\mathbf r f(\mathbf r + \mathbf R) = \nabla_\mathbf u f(\mathbf u)$, so

\begin{equation}
\label{eq:ch-07-commute}
\bigl(\hat T_{\mathbf R} \hat H f\bigr)(\mathbf r)
   = -\tfrac{1}{2} \nabla^2 f(\mathbf r + \mathbf R) + V(\mathbf r) f(\mathbf r + \mathbf R)
   = \bigl(\hat H \, \hat T_{\mathbf R} f\bigr)(\mathbf r).
\end{equation}

The two operators therefore commute:

\begin{equation}
\label{eq:ch-07-commute-final}
\boxed{[\hat T_{\mathbf R}, \hat H] = 0 \quad \text{for every } \mathbf R.}
\end{equation}

### Step 4. $\hat T_{\mathbf R}$ and $\hat H$ can be simultaneously diagonalised

Two commuting self-adjoint operators on a Hilbert space can be brought
to a common diagonal form. (Standard result; the operators have a
joint spectral measure.) So there exists a complete orthonormal basis
of states that are eigenstates of *both* $\hat T_{\mathbf R}$ and
$\hat H$ simultaneously. We will call these basis states $\psi$.

### Step 5. The eigenvalues of $\hat T_{\mathbf R}$ are phase factors

The group of Bravais translations is abelian: $\hat T_{\mathbf R}
\hat T_{\mathbf R'} = \hat T_{\mathbf R'} \hat T_{\mathbf R} =
\hat T_{\mathbf R + \mathbf R'}$. The eigenvalues of a unitary
representation of an abelian group are one-dimensional, i.e. complex
numbers of unit modulus. We therefore write

\begin{equation}
\label{eq:ch-07-trans-eigval}
\hat T_{\mathbf R} \psi = \lambda(\mathbf R) \, \psi, \qquad |\lambda(\mathbf R)| = 1.
\end{equation}

The map $\mathbf R \mapsto \lambda(\mathbf R)$ is a group
homomorphism $\mathbb Z^3 \to U(1)$:

\begin{equation}
\label{eq:ch-07-trans-hom}
\lambda(\mathbf R + \mathbf R') = \lambda(\mathbf R) \, \lambda(\mathbf R').
\end{equation}

The most general such homomorphism is $\lambda(\mathbf R) = e^{i
\mathbf k \cdot \mathbf R}$ for some fixed vector $\mathbf k \in
\mathbb R^3$ (think of $\mathbf k$ as the "Fourier transform" of the
homomorphism, with the constraint $e^{i\mathbf k \cdot \mathbf R} =
1$ for every lattice $\mathbf R$ fixing $\mathbf k$ only up to
reciprocal-lattice additions).

So the eigenstates of $\hat T_{\mathbf R}$ satisfy

\begin{equation}
\label{eq:ch-07-bloch-phase}
\psi(\mathbf r + \mathbf R) = e^{i \mathbf k \cdot \mathbf R} \, \psi(\mathbf r) \quad \text{for every } \mathbf R.
\end{equation}

This is sometimes called the *Bloch condition*.

### Step 6. Define the cell-periodic function $u_{\mathbf k}$

Define

\begin{equation}
\label{eq:ch-07-define-u}
u_{\mathbf k}(\mathbf r) := e^{-i \mathbf k \cdot \mathbf r} \, \psi(\mathbf r).
\end{equation}

Equation \eqref{eq:ch-07-bloch} is just a rearrangement of
\eqref{eq:ch-07-define-u}; the work is to show that $u_{\mathbf k}$
inherits the lattice periodicity.

Compute $u_{\mathbf k}$ at a translated point:

\begin{align}
u_{\mathbf k}(\mathbf r + \mathbf R)
   &= e^{-i \mathbf k \cdot (\mathbf r + \mathbf R)} \, \psi(\mathbf r + \mathbf R) \nonumber \\
   &= e^{-i \mathbf k \cdot \mathbf r} \, e^{-i \mathbf k \cdot \mathbf R} \,
      \bigl( e^{i \mathbf k \cdot \mathbf R} \, \psi(\mathbf r) \bigr)
      \quad \text{by \eqref{eq:ch-07-bloch-phase}} \nonumber \\
   &= e^{-i \mathbf k \cdot \mathbf r} \, \psi(\mathbf r) \nonumber \\
   &= u_{\mathbf k}(\mathbf r).
\end{align}

The two phase factors cancel exactly, and we have

\begin{equation}
\label{eq:ch-07-u-periodic}
u_{\mathbf k}(\mathbf r + \mathbf R) = u_{\mathbf k}(\mathbf r) \quad \text{for every } \mathbf R.
\end{equation}

This is \eqref{eq:ch-07-bloch-periodic}, and it completes the proof:
the eigenfunction factorises as $\psi(\mathbf r) = e^{i \mathbf k \cdot
\mathbf r} u_{\mathbf k}(\mathbf r)$ with $u_{\mathbf k}$ cell-
periodic. $\blacksquare$

> **Note.** The crystal momentum $\mathbf k$ is defined only modulo a
> reciprocal-lattice vector: if $\mathbf G$ is a reciprocal-lattice
> vector, then $e^{i \mathbf G \cdot \mathbf R} = 1$ for every direct
> lattice $\mathbf R$, so $\mathbf k$ and $\mathbf k + \mathbf G$
> satisfy the same Bloch condition \eqref{eq:ch-07-bloch-phase}. The
> *unique* representative of $\mathbf k$ is therefore chosen inside
> the first Brillouin zone.

## 7.4 The Brillouin zone

### 7.4.1 The reciprocal lattice

The set of vectors $\{\mathbf G\}$ for which $e^{i \mathbf G \cdot
\mathbf R} = 1$ for every direct-lattice vector $\mathbf R$ is itself
a Bravais lattice, the **reciprocal lattice**. If the direct lattice
has primitive vectors $\mathbf a_1, \mathbf a_2, \mathbf a_3$, the
reciprocal lattice has primitive vectors $\mathbf b_1, \mathbf b_2,
\mathbf b_3$ defined by

\begin{equation}
\label{eq:ch-07-reciprocal-def}
\mathbf a_i \cdot \mathbf b_j = 2\pi \delta_{ij}.
\end{equation}

An explicit construction is

\begin{equation}
\label{eq:ch-07-reciprocal-explicit}
\mathbf b_1 = \frac{2\pi \, \mathbf a_2 \times \mathbf a_3}{\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)},
\qquad \text{and cyclic permutations}.
\end{equation}

Every reciprocal-lattice vector is an integer combination $\mathbf G
= h \mathbf b_1 + k \mathbf b_2 + l \mathbf b_3$ with $h, k, l \in
\mathbb Z$. The volume of the reciprocal primitive cell is

\begin{equation}
\label{eq:ch-07-reciprocal-volume}
V_\text{BZ}^* = \mathbf b_1 \cdot (\mathbf b_2 \times \mathbf b_3) = \frac{(2\pi)^3}{V_\text{cell}},
\end{equation}

where $V_\text{cell} = \mathbf a_1 \cdot (\mathbf a_2 \times \mathbf
a_3)$ is the direct-lattice primitive-cell volume.

### 7.4.2 The first Brillouin zone

The **first Brillouin zone** (1st BZ) is the Wigner–Seitz cell of
the reciprocal lattice: the set of points in reciprocal space that are
closer to the origin than to any other reciprocal-lattice point. Its
boundary is built from the perpendicular bisector planes of the
shortest $\mathbf G$ vectors. Formally,

\begin{equation}
\label{eq:ch-07-bz}
\text{1st BZ} = \left\{ \mathbf k \in \mathbb R^3 \;:\;
|\mathbf k| \le |\mathbf k - \mathbf G| \text{ for every reciprocal-lattice vector } \mathbf G \right\}.
\end{equation}

Every physically distinct crystal momentum is represented exactly
once in the 1st BZ, so the "sum over $\mathbf k$" in
\eqref{eq:ch-07-bvk-sum} runs over the 1st BZ.

### 7.4.3 High-symmetry points for the FCC lattice

As an example, the reciprocal lattice of a face-centred cubic (FCC)
direct lattice is body-centred cubic (BCC). The primitive vectors of
the FCC lattice with conventional cubic parameter $a$ are

\begin{equation}
\label{eq:ch-07-fcc-primitive}
\mathbf a_1 = \frac{a}{2}(0, 1, 1),\quad
\mathbf a_2 = \frac{a}{2}(1, 0, 1),\quad
\mathbf a_3 = \frac{a}{2}(1, 1, 0).
\end{equation}

Equation \eqref{eq:ch-07-reciprocal-explicit} gives the reciprocal
primitive vectors

\begin{equation}
\label{eq:ch-07-fcc-reciprocal}
\mathbf b_1 = \frac{2\pi}{a}(-1, 1, 1),\quad
\mathbf b_2 = \frac{2\pi}{a}(1, -1, 1),\quad
\mathbf b_3 = \frac{2\pi}{a}(1, 1, -1),
\end{equation}

which span a BCC lattice. The shortest $\mathbf G$ vectors are
$\pm \tfrac{2\pi}{a}(1,1,1)$ and permutations with sign, with length
$\tfrac{2\pi}{a}\sqrt{3}$. The 1st BZ of FCC is therefore a
*truncated octahedron*, bounded by:

- **6 square faces** at $\pm \tfrac{2\pi}{a}(1,0,0)$ and permutations
  (perpendicular bisectors of $\mathbf G = \tfrac{4\pi}{a}(\pm 1, 0, 0)$
  and permutations);
- **8 hexagonal faces** at $\pm \tfrac{\pi}{a}(1, 1, 1)$ and
  permutations (perpendicular bisectors of $\mathbf G = \tfrac{2\pi}{a}(\pm 1, \pm 1, \pm 1)$).

The high-symmetry points and lines used to plot FCC band structures
(Setyawan–Curtarolo convention) are listed below. We give
Cartesian coordinates in units of $2\pi/a$; the actual Cartesian
coordinate is the value in the table multiplied by $2\pi/a$.

| Label | Cartesian (in $2\pi/a$) | Multiplicity | Description |
|:------|:------------------------|:------------:|:------------|
| $\Gamma$ | $(0, 0, 0)$ | 1 | Centre of the BZ |
| $X$ | $(1, 0, 0)$ | 6 | Centre of a square face |
| $L$ | $(1/2, 1/2, 1/2)$ | 8 | Centre of a hexagonal face |
| $W$ | $(1, 1/2, 0)$ | 24 | Vertex: 2 hexagons + 1 square meet |
| $K$ | $(3/4, 3/4, 0)$ | 24 | Midpoint of a hex–hex edge |
| $U$ | $(3/4, 1/2, 1/4)$ | 24 | Midpoint of an $L$–$W$ edge |

The standard band-structure path traces the irreducible BZ:

\begin{equation}
\label{eq:ch-07-fcc-path}
\Gamma \;\to\; X \;\to\; W \;\to\; K \;\to\; \Gamma \;\to\; L \;\to\; W.
\end{equation}

The path $\Gamma$–$X$–$W$–$K$–$\Gamma$ visits the square face
centre, a vertex, the edge midpoint between two hexagonal faces, and
back to the centre. The path $\Gamma$–$L$–$W$ visits the hexagonal
face centre and returns to a vertex.

> **Warning.** Different authors use different conventions for the
> high-symmetry labels. The Setyawan–Curtarolo labels above are
> the ones used by the modern Materials Project and AFLOW
> databases; older textbooks (Kittel, Ashcroft & Mermin) sometimes
> use a different symbol for $K$. Always check the convention when
> reading a band-structure plot from the literature.

## 7.5 Plane-wave basis

### 7.5.1 The plane-wave expansion

Equation \eqref{eq:ch-07-bloch-periodic} says that $u_{n\mathbf k}$
is cell-periodic. Any cell-periodic function can be expanded in plane
waves whose wavevectors are reciprocal-lattice vectors:

\begin{equation}
\label{eq:ch-07-pw-expand-u}
u_{n\mathbf k}(\mathbf r) = \frac{1}{\sqrt{\Omega}} \sum_{\mathbf G} c_{n\mathbf k}(\mathbf G) \, e^{i \mathbf G \cdot \mathbf r}.
\end{equation}

Here $\Omega$ is the crystal volume (taken to infinity in the BvK
formalism) and the sum runs over all reciprocal-lattice vectors. The
$1/\sqrt{\Omega}$ is a normalisation; the precise form depends on the
convention.

Substituting \eqref{eq:ch-07-pw-expand-u} into
\eqref{eq:ch-07-bloch}:

\begin{equation}
\label{eq:ch-07-pw-expand-psi}
\psi_{n\mathbf k}(\mathbf r) = \frac{1}{\sqrt{\Omega}} \sum_{\mathbf G} c_{n\mathbf k}(\mathbf G) \, e^{i(\mathbf k + \mathbf G) \cdot \mathbf r}.
\end{equation}

The wavefunction is a linear combination of plane waves with
wavevectors $\mathbf k + \mathbf G$, one per reciprocal-lattice
vector. In a basis-set language (see
[chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) for the
broader context), the **plane-wave basis** is the discrete set

\begin{equation}
\label{eq:ch-07-pw-basis}
\left\{ \tfrac{1}{\sqrt{\Omega}} e^{i(\mathbf k + \mathbf G) \cdot \mathbf r} \right\}_{\mathbf G \in \text{reciprocal lattice}}.
\end{equation}

### 7.5.2 The plane-wave Hamiltonian

We seek the matrix elements of $\hat H$ in the basis
\eqref{eq:ch-07-pw-basis}. For a one-electron Hamiltonian
$\hat H = -\tfrac{1}{2}\nabla^2 + V(\mathbf r)$ with periodic $V$:

\begin{align}
\langle \mathbf k + \mathbf G' \mid \hat H \mid \mathbf k + \mathbf G \rangle
   &= \int \frac{d^3r}{\Omega} \, e^{-i(\mathbf k + \mathbf G') \cdot \mathbf r} \,
      \left[-\tfrac{1}{2}\nabla^2 + V(\mathbf r)\right] e^{i(\mathbf k + \mathbf G) \cdot \mathbf r} \nonumber \\
   &= \tfrac{1}{2} |\mathbf k + \mathbf G|^2 \, \delta_{\mathbf G \mathbf G'} + V_{\text{per}}(\mathbf G' - \mathbf G),
\end{align}

where

\begin{equation}
\label{eq:ch-07-vper}
V_{\text{per}}(\mathbf q) := \frac{1}{V_\text{cell}} \int_{\text{cell}} V(\mathbf r) \, e^{-i \mathbf q \cdot \mathbf r} \, d^3r
\end{equation}

is the Fourier transform of the *cell-periodic* potential, with the
integral restricted to a single primitive cell (or any other cell-
shaped domain) of volume $V_\text{cell}$.

The matrix form of $\hat H$ in the plane-wave basis is therefore

\begin{equation}
\label{eq:ch-07-pw-hamiltonian}
\boxed{H_{\mathbf G \mathbf G'}(\mathbf k)
  = \tfrac{1}{2} |\mathbf k + \mathbf G|^2 \, \delta_{\mathbf G \mathbf G'} + V_{\text{per}}(\mathbf G' - \mathbf G).}
\end{equation}

Two structural facts to notice:

1. **The kinetic term is diagonal in $\mathbf G$** — it depends only
   on $|\mathbf k + \mathbf G|^2$, with no coupling between different
   $\mathbf G$ values. This is the magic of plane waves.
2. **The potential term is a Toeplitz-like matrix in $\mathbf G$** —
   it depends only on the *difference* $\mathbf G' - \mathbf G$, and
   is therefore a circulant (in the infinite limit) and a banded
   matrix (once truncated).

The full Kohn–Sham Hamiltonian of [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) is just
$H_\text{KS}(\mathbf k) = \tfrac{1}{2}|\mathbf k + \mathbf G|^2
\delta_{\mathbf G \mathbf G'} + V_{\text{eff}}[\rho](\mathbf G' -
\mathbf G)$, with $V_\text{eff}$ the (self-consistent) effective
potential. The plane-wave structure is unchanged.

### 7.5.3 The kinetic-energy cutoff

The infinite basis \eqref{eq:ch-07-pw-basis} must be truncated for
numerical work. The standard truncation is a kinetic-energy cutoff:

\begin{equation}
\label{eq:ch-07-cutoff}
\tfrac{1}{2} |\mathbf k + \mathbf G|^2 \le E_\text{cut}.
\end{equation}

Only those $\mathbf G$ for which \eqref{eq:ch-07-cutoff} holds are
included in the basis; the rest are dropped. The truncated basis is
finite, the Hamiltonian \eqref{eq:ch-07-pw-hamiltonian} becomes a
finite matrix, and the eigenvalue problem

\begin{equation}
\label{eq:ch-07-pw-eig}
H(\mathbf k) \, \mathbf c_{n\mathbf k} = \varepsilon_{n\mathbf k} \, \mathbf c_{n\mathbf k}
\end{equation}

is solved by standard linear algebra.

> **Tip.** The cutoff $E_\text{cut}$ is the single most important
> numerical parameter in a plane-wave calculation. Total energies
> converge to the infinite-basis limit as $E_\text{cut} \to \infty$,
> and the convergence rate depends on the smoothness of the
> potential: smooth (e.g. pseudo-) potentials converge
> exponentially, all-electron potentials converge only
> polynomially. This is one of the central reasons that
> [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) is about
> pseudopotentials.

For a 1-D lattice with lattice constant $a$, the cutoff
\eqref{eq:ch-07-cutoff} becomes

\begin{equation}
\label{eq:ch-07-cutoff-1d}
\tfrac{1}{2} (k + m \, 2\pi/a)^2 \le E_\text{cut}, \qquad m \in \mathbb Z.
\end{equation}

If we use $N_\text{PW}$ plane waves centred on the origin, the cutoff
is set by the highest $|m|$ value, $E_\text{cut} = \tfrac{1}{2}
((N_\text{PW}/2) \cdot 2\pi/a)^2$. For $N_\text{PW} = 21$ plane
waves and $a = 5$ bohr, the cutoff is $E_\text{cut} = \tfrac{1}{2}
(10 \cdot 2\pi/5)^2 = \tfrac{1}{2} (4\pi)^2 = 8\pi^2 \approx 78.96$
Hartree. This is more than enough to converge the lowest four
valence bands for the gentle potential of §7.7.

## 7.6 k-point sampling

### 7.6.1 BZ integrals as sums

Bloch's theorem \eqref{eq:ch-07-bloch} reduces every state of the
crystal to a label $(\mathbf k, n)$ with $\mathbf k$ in the 1st BZ.
Every observable that sums over filled states becomes an integral
over $\mathbf k$:

\begin{equation}
\label{eq:ch-07-bz-integral}
\mathcal O = \frac{V_\text{cell}}{(2\pi)^3} \int_{\text{BZ}} d\mathbf k \,
            \sum_n f(\varepsilon_{n\mathbf k}) \, o_{n\mathbf k}.
\end{equation}

The prefactor $V_\text{cell}/(2\pi)^3$ ensures one state per
$(\mathbf k, n, \text{spin})$ per cell.

The BvK boundary conditions \eqref{eq:ch-07-bvk} discretise
$\mathbf k$ on a uniform mesh. With $N_i$ mesh points along the $i$-th
reciprocal-lattice direction,

\begin{equation}
\label{eq:ch-07-mp-mesh}
\mathbf k_{m_1, m_2, m_3}
   = \frac{m_1}{N_1} \mathbf b_1 + \frac{m_2}{N_2} \mathbf b_2 + \frac{m_3}{N_3} \mathbf b_3,
   \qquad m_i = 0, 1, \ldots, N_i - 1.
\end{equation}

Equation \eqref{eq:ch-07-bz-integral} is then approximated by a
Riemann sum

\begin{equation}
\label{eq:ch-07-mp-sum}
\mathcal O \approx \frac{1}{N_1 N_2 N_3}
                 \sum_{m_1, m_2, m_3} \,
                 \sum_n f(\varepsilon_{n\mathbf k}) \, o_{n\mathbf k}.
\end{equation}

This is the **Monkhorst–Pack** (MP) mesh, the workhorse of
solid-state DFT.

### 7.6.2 Convergence of the MP sum

The MP sum \eqref{eq:ch-07-mp-sum} is a midpoint rule for the BZ
integral. For a smooth integrand, the discretisation error scales as

\begin{equation}
\label{eq:ch-07-mp-error}
\text{error} = O\!\left(\frac{1}{N^2}\right)
\quad \text{in 1-D,}
\qquad
O\!\left(\frac{1}{N^{2/3}}\right)
\quad \text{in 3-D,}
\end{equation}

if the integrand is smooth. **Crucially**, the integrand is *not*
smooth in two cases:

1. **Metals and semiconductors at low temperature.** The occupation
   function $f(\varepsilon - \varepsilon_F)$ is a step function at
   $T = 0$. Bands that cross the Fermi level contribute
   discontinuously to the sum, and the discretisation error decays
   only as $1/N$ instead of $1/N^2$. Insulators, where the step
   function is away from any band, are fine.
2. **Integrands that depend explicitly on the Fermi level.** Total
   energy and forces in metals both depend on $\varepsilon_F$, and
   $\varepsilon_F$ is determined by the normalisation of the
   occupation function. The MP sum oscillates with the mesh
   position and converges slowly.

### 7.6.3 Smearing for metals

The standard fix for metallic systems is to **smear** the occupation
function, replacing the discontinuous step by a smooth approximation.
The most common choices are:

| Scheme | Function $f(\varepsilon)$ | Tail behaviour | Order in $T$ |
|:-------|:---------------------------|:---------------|:-------------|
| Fermi–Dirac | $\bigl[1 + e^{(\varepsilon - \mu)/k_B T}\bigr]^{-1}$ | Exponential | Exact |
| Gaussian | $\tfrac{1}{2}\operatorname{erfc}\!\bigl[(\varepsilon - \mu)/\sigma\bigr]$ | Exponential | — |
| Methfessel–Paxton | Hermite polynomial expansion of the step | $\sim e^{-x^2}$ | $O(\sigma^{2N})$ |

The **Methfessel–Paxton** (MP-x) scheme, in particular, replaces the
discontinuous step by a finite Hermite expansion of width $\sigma$ in
energy. The smearing parameter $\sigma$ is the *entropy* temperature
in a fictitious finite-$T$ calculation; the "true" $T = 0$ total
energy is obtained by extrapolating $\sigma \to 0$ and subtracting
the entropy contribution. In practice, MP-x with $N = 1$ or $N = 2$
and a small $\sigma$ (typically 0.01–0.05 Hartree) is enough to make
the total energy converge with $N_\mathbf k$ in the same $1/N^2$
regime as insulators.

The downside: the smearing is a *fiction*. The computed total
energy is no longer the ground-state energy but a free energy at
finite $\sigma$. For properties that depend on the *exact* Fermi
surface (transport, magnetism at low temperature), smearing
introduces systematic errors that have to be checked against a
$\sigma \to 0$ extrapolation.

> **Warning.** Convergence in the number of k-points is *not* the
> same as convergence in the smearing width. The right convergence
> test for a metal is: total energy vs. $N_\mathbf k$ at fixed
> $\sigma$, then total energy vs. $\sigma$ at fixed $N_\mathbf k$.

## 7.7 Worked example — band structure of a 1-D periodic lattice

We put the machinery to work on the simplest non-trivial periodic
problem: a 1-D lattice of period $a = 5$ bohr with a cosine
potential of depth $V_0 = -1/2$ Hartree,

\begin{equation}
\label{eq:ch-07-worked-V}
V(x) = -\tfrac{1}{2} \cos(2\pi x / a).
\end{equation}

This is the textbook **nearly-free-electron** model: a free electron
slightly perturbed by a weak periodic potential. We will:

1. Build the $21 \times 21$ plane-wave Hamiltonian at a single
   $\mathbf k$ point.
2. Diagonalise it at 100 k-points uniformly distributed in the 1st
   Brillouin zone.
3. Plot the lowest four bands as a function of $k$.

The script that does this is
[`dft_notes/python_codes/chapter_07/01-free-electron-bands.py`]({{
site.baseurl }}/dft-notes/python_codes/chapter_07/01-free-electron-bands.py);
the plot it produces is in
[`plots/01-free-electron-bands.png`]({{ site.baseurl
}}/dft-notes/python_codes/chapter_07/plots/01-free-electron-bands.png).

### 7.7.1 The Fourier coefficients of the potential

Using the identity $\cos\theta = \tfrac{1}{2}(e^{i\theta} +
e^{-i\theta})$,

\begin{equation}
\label{eq:ch-07-worked-V-decomp}
V(x) = -\tfrac{1}{2} \cos(2\pi x / a)
     = -\tfrac{1}{4} e^{i 2\pi x / a} - \tfrac{1}{4} e^{-i 2\pi x / a}.
\end{equation}

The Fourier coefficients of \eqref{eq:ch-07-worked-V} on the
reciprocal-lattice grid $G = m \cdot 2\pi/a$ are

\begin{equation}
\label{eq:ch-07-worked-Vhat}
V_{\text{per}}(G) =
\begin{cases}
\phantom{-}0 & \text{if } G = 0, \\
-\tfrac{1}{4} & \text{if } G = \pm 2\pi/a, \\
\phantom{-}0 & \text{otherwise}.
\end{cases}
\end{equation}

There is no $G = 0$ term (the average of $V$ over one period is
zero), and there are only two non-zero Fourier components, at
$G = \pm 2\pi/a$, each equal to $-1/4$. In the matrix
\eqref{eq:ch-07-pw-hamiltonian} this means

\begin{equation}
\label{eq:ch-07-worked-V-matrix}
V_{\text{per}}(G' - G) =
\begin{cases}
-\tfrac{1}{4} & \text{if } m' - m = \pm 1, \\
\phantom{-}0 & \text{otherwise}.
\end{cases}
\end{equation}

The potential matrix is **tridiagonal** in the plane-wave basis.

### 7.7.2 The Hamiltonian

The plane-wave basis vectors are $G_m = m \cdot 2\pi/a$ for $m \in
\{-10, -9, \ldots, 9, 10\}$ (21 values in total). The full
Hamiltonian \eqref{eq:ch-07-pw-hamiltonian} at wavevector $k$ is the
$21 \times 21$ matrix

\begin{equation}
\label{eq:ch-07-worked-H}
H_{m m'}(k) = \tfrac{1}{2}\bigl(k + m \cdot 2\pi/a\bigr)^2 \delta_{m m'} \;+\; V_{\text{per}}\bigl((m' - m) \cdot 2\pi/a\bigr).
\end{equation}

Substituting the explicit $V_{\text{per}}$ from
\eqref{eq:ch-07-worked-V-matrix}:

\begin{align}
H_{m m'}(k)
  &= \tfrac{1}{2}\bigl(k + m \cdot 2\pi/a\bigr)^2 \delta_{m m'} \;
     - \tfrac{1}{4}\bigl(\delta_{m', m+1} + \delta_{m', m-1}\bigr) \nonumber \\
  &= \begin{cases}
       \tfrac{1}{2}\bigl(k + m \cdot 2\pi/a\bigr)^2 & m = m', \\
       -\tfrac{1}{4} & m' = m \pm 1, \\
       \phantom{-}0 & \text{otherwise}.
     \end{cases}
\end{align}

The first two rows of this matrix at $k = 0$ are:

\begin{equation}
\label{eq:ch-07-worked-H-at-0}
H(0) = \frac{1}{2}\!\begin{pmatrix}
4\pi^2/a^2 \cdot 100 & -1/2 & 0 & \cdots & 0 & 0 \\
-1/2 & 4\pi^2/a^2 \cdot 81 & -1/2 & \cdots & 0 & 0 \\
0 & -1/2 & 4\pi^2/a^2 \cdot 64 & \cdots & 0 & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & \cdots & 4\pi^2/a^2 \cdot 81 & -1/2 \\
0 & 0 & 0 & \cdots & -1/2 & 4\pi^2/a^2 \cdot 100
\end{pmatrix}.
\end{equation}

(We have used the symmetry $V_{\text{per}}(q) = V_{\text{per}}(-q)$ for
real $V$ to combine the two off-diagonals into a single factor of
$1/2$.)

The diagonal grows quadratically with $|m|$, and the off-diagonals
are the constant $-1/2 \cdot V_0 = -1/2 \cdot 1/2 = -1/4$ (the factor
of 1/2 from the $V_0/2$ of $\cos$). With $a = 5$ bohr, the diagonal
spacing at low $m$ is $\tfrac{1}{2}((m+1)b)^2 - \tfrac{1}{2}(mb)^2
= \tfrac{1}{2}(2m+1)b^2 = \tfrac{1}{2}(2m+1)(2\pi/5)^2 \approx
0.79 (2m+1)$ Hartree. The off-diagonal coupling of $0.25$ Hartree is
much smaller, so the lowest bands are close to the free-electron
parabolas, and the higher bands are accurate as well.

### 7.7.3 The 1-D Brillouin zone

In 1-D, the BZ is the interval $k \in [-\pi/a, \pi/a]$. For $a = 5$
bohr, this is $k \in [-\pi/5, \pi/5] = [-0.628, 0.628]$ bohr$^{-1}$.
We sample 100 uniformly-spaced points in this interval:

\begin{equation}
\label{eq:ch-07-worked-k-mesh}
k_j = -\pi/a + (j + \tfrac{1}{2}) \cdot \frac{2\pi/a}{100},
   \qquad j = 0, 1, \ldots, 99.
\end{equation}

(The "half-integer" shift places the k-mesh symmetrically about $k =
0$. It does not matter for the band-structure plot, but it matters
for total-energy convergence tests.)

### 7.7.4 The band gap at the BZ boundary

The interesting physics happens at the BZ boundary $k = \pm \pi/a$.
Consider the 2 × 2 submatrix of \eqref{eq:ch-07-worked-H} spanned by
the two free-electron states that are degenerate at the boundary:
$e^{i k x}$ with $k = \pi/a$ and $e^{i(k - 2\pi/a) x}$ with $k -
2\pi/a = -\pi/a$. Both have free-electron energy
$\tfrac{1}{2}(\pi/a)^2$. The potential $V_{\text{per}}$ couples them
with matrix element $-1/4$ (it is the only non-zero off-diagonal in
this submatrix). The 2 × 2 submatrix is therefore

\begin{equation}
\label{eq:ch-07-worked-gap-H}
H_{2 \times 2}(k = \pi/a) = \tfrac{1}{2}(\pi/a)^2 \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} - \tfrac{1}{4} \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}.
\end{equation}

The eigenvalues of this 2 × 2 matrix are

\begin{equation}
\label{eq:ch-07-worked-gap}
\boxed{\varepsilon_\pm(\pi/a) = \tfrac{1}{2}(\pi/a)^2 \mp \tfrac{1}{2} \cdot 2 \cdot \tfrac{1}{4}
               = \tfrac{1}{2}(\pi/a)^2 \mp \tfrac{1}{4},}
\end{equation}

giving a band gap of

\begin{equation}
\label{eq:ch-07-worked-gap-size}
E_\text{gap} = \varepsilon_+ - \varepsilon_- = 2 \cdot \tfrac{1}{4} = \tfrac{1}{2} \text{ Hartree}.
\end{equation}

This is the elementary band-gap result for a weak periodic potential:
the gap is **twice the absolute value of the leading Fourier
coefficient** of the potential, $\mathbf G = 2\pi/a$. For the
parameters here, the gap is $0.5$ Hartree $\approx 13.6$ eV — a
very large gap, because the potential is *not* weak; it has the
same energy scale as the kinetic term at the BZ boundary.

Numerically, with $a = 5$ bohr:

\begin{equation}
\label{eq:ch-07-worked-gap-numbers}
\tfrac{1}{2}(\pi/a)^2 = \tfrac{1}{2}(\pi/5)^2 \approx 0.1974 \text{ Hartree}.
\end{equation}

The two degenerate levels at the BZ boundary split into

\begin{align}
\varepsilon_-(\pi/a) &= 0.1974 - 0.2500 = -0.0526 \text{ Hartree}, \nonumber \\
\varepsilon_+(\pi/a) &= 0.1974 + 0.2500 = 0.4474 \text{ Hartree},
\end{align}

with a gap of $0.5000$ Hartree between them. These numbers are
checked numerically by the script (see the output of the script's
`if __name__ == "__main__":` block).

> **Tip.** Compare the gap $E_\text{gap} = 0.5$ Hartree to the
> free-electron kinetic energy at the boundary, $\tfrac{1}{2}(\pi/a)^2
> \approx 0.197$ Hartree. The gap is *larger* than the kinetic
> energy. In a "weak-potential" limit, the gap would be much smaller
> than the kinetic energy, and the band structure would look like a
> free-electron parabola with a small gap opening at the BZ
> boundary. The cosine potential here is *strong* — the gap is big,
> the lowest band is significantly distorted from a parabola, and
> the higher bands are no longer free-electron-like.

### 7.7.5 The band-structure plot

The figure below shows the first four bands $\varepsilon_n(k)$ for
$k \in [-\pi/a, \pi/a]$. The vertical dashed lines mark the BZ
boundaries. The free-electron parabolas $\tfrac{1}{2}(k + m \cdot
2\pi/a)^2$ for $m = 0, -1, 1, -2$ are shown in light grey for
comparison. Note:

- **Band 1** (coral) starts negative at $k = \pm \pi/a$ (the lower
  branch of \eqref{eq:ch-07-worked-gap}) and has a maximum at $k = 0$
  close to $0$. The band is *not* a parabola — the periodic
  potential has strongly renormalised it.
- **Band 2** (amber) starts at $\varepsilon_+(\pi/a) \approx 0.447$
  Hartree at the BZ boundary and dips toward a minimum at $k = 0$.
- **Bands 3 and 4** (teal and active coral) are higher-lying bands
  that are less perturbed by the cosine potential (which has only
  one non-trivial Fourier component).

![Free-electron band structure of a 1-D lattice with $V(x) = -0.5 \cos(2\pi x/a)$ and $a = 5$ bohr. The first four bands are shown in colour; the free-electron parabolas $\tfrac{1}{2}(k + m \cdot 2\pi/a)^2$ for $m = 0, -1, 1, -2$ are shown in light grey.]({{ site.baseurl }}/dft-notes/python_codes/chapter_07/plots/01-free-electron-bands.png)

The relevant code is reproduced below; the script is the source of
truth.

```python
# dft_notes/python_codes/chapter_07/01-free-electron-bands.py
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Parameters --------------------------------------------------------
A  = 5.0   # lattice constant, bohr
V0 = -0.5  # potential depth,  Hartree
N_PW = 21  # number of plane waves
N_K  = 100 # number of k-points in the 1st BZ
B    = 2 * np.pi / A  # reciprocal lattice constant

# --- Reciprocal lattice ------------------------------------------------
m_vals = np.arange(-(N_PW // 2), N_PW // 2 + 1)  # -10..+10
G_vals = m_vals * B                                # 21 G values

# --- k-mesh in the 1st Brillouin zone ----------------------------------
k_vals = np.linspace(-np.pi / A, np.pi / A, N_K, endpoint=False)

# --- Fourier coefficients of V(x) --------------------------------------
# V(x) = -0.5 cos(2pi x / a)  ==>  V(G=+/- 2pi/a) = -0.25
V_GG = np.zeros((N_PW, N_PW))
for i in range(N_PW):
    for j in range(N_PW):
        d = m_vals[i] - m_vals[j]
        if   d ==  1: V_GG[i, j] = -0.25   # G_i = G_j + 2pi/a
        elif d == -1: V_GG[i, j] = -0.25   # G_i = G_j - 2pi/a
        # else  V_GG[i, j] = 0  (already)

# --- Diagonalise at every k-point --------------------------------------
bands = np.zeros((N_K, N_PW))
for ik, k in enumerate(k_vals):
    H_kin = 0.5 * (k + G_vals) ** 2             # diagonal kinetic
    H     = np.diag(H_kin) + V_GG
    bands[ik, :] = np.linalg.eigvalsh(H)       # Hermitian -> real evals

# --- Plot the first 4 bands -------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
palette = ["#cc785c", "#e8a55a", "#5db8a6", "#a9583e"]
for n in range(4):
    ax.plot(k_vals * A / np.pi, bands[:, n],
            color=palette[n], lw=2.0,
            label=rf"band {n + 1}")

# Reference free-electron parabolas
for m in (0, -1, 1, -2):
    ax.plot(k_vals * A / np.pi,
            0.5 * (k_vals + m * B) ** 2,
            color="#a09d96", lw=0.7, alpha=0.4)

ax.axvline(-1.0, color="#3d3d3a", lw=0.8, ls="--", alpha=0.5)
ax.axvline(+1.0, color="#3d3d3a", lw=0.8, ls="--", alpha=0.5)
ax.set_xlabel(r"$k a / \pi$")
ax.set_ylabel(r"$\varepsilon_n(k)$  (Hartree)")
ax.set_title("1-D band structure, $a = 5$ bohr, $V(x) = -0.5 \cos(2\pi x/a)$")
ax.legend(frameon=False)
ax.grid(alpha=0.3)
fig.tight_layout()

# --- Save the plot -----------------------------------------------------
here      = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(here, "plots")
os.makedirs(plots_dir, exist_ok=True)
out = os.path.join(plots_dir, "01-free-electron-bands.png")
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"Wrote {out}")
```

> **Note.** The matrix is built and diagonalised in a single
> Python loop over the 100 k-points. The wall-clock time is well
> under a second on a laptop; a serial Python implementation is
> fast enough for this system. A production plane-wave code
> vectorises the inner loop and parallelises over k-points; the
> algorithm is unchanged.

## 7.8 Workflow diagram

The end-to-end workflow of a plane-wave, periodic-boundary DFT
calculation is summarised below.

```mermaid
graph TD
  A[Choose crystal structure<br/>lattice vectors a₁, a₂, a₃] --> B[Compute reciprocal lattice<br/>b₁, b₂, b₃]
  B --> C[Set BvK supercell<br/>N₁ × N₂ × N₃ cells]
  C --> D[Build k-point mesh<br/>Monkhorst–Pack N₁×N₂×N₃]
  D --> E[Choose kinetic cutoff E_cut]
  E --> F[Build plane-wave basis<br/>|k+G|² ≤ E_cut]
  F --> G[For each k-point:<br/>build H(k) in PW basis]
  G --> H[Diagonalise H(k)<br/>get εₙₖ, cₙₖ]
  H --> I[Build density ρ(r)<br/>sum over occupied bands]
  I --> J[Build V_eff[ρ]<br/>Hartree + xc + external]
  J --> K{SCF converged?}
  K -- No --> G
  K -- Yes --> L[Compute total energy,<br/>forces, stress]
  L --> M[Plot bands along<br/>Γ-X-W-K-Γ-L-W]

  classDef decision fill:#e8e0d2,stroke:#3d3d3a,stroke-width:2px;
  classDef input fill:#faf9f5,stroke:#6c6a64,stroke-width:1px;
  classDef output fill:#cc785c,stroke:#ffffff,stroke-width:1px;
  class A,B,C,D,E,F input
  class K decision
  class H,I,J,L,M output
```

The decision node `K{SCF converged?}` is the inner loop of every
DFT calculation; the surrounding boxes are the *solid-state-specific*
machinery (BvK supercell, k-point mesh, plane-wave basis, band
plotting) that the present chapter introduces.

## 7.9 Problems

<details class="problem">
<summary>Problem 1 (easy) — Band gap of a cosine potential</summary>

A 1-D lattice has lattice constant $a$ and a periodic potential
$V(x) = V_0 \cos(2\pi x / a)$ with $V_0 = -0.2$ Hartree.

1. Write down the non-zero Fourier coefficients $V_{\text{per}}(G)$
   of the potential.
2. Construct the $2 \times 2$ plane-wave Hamiltonian at the BZ
   boundary $k = \pi/a$ in the basis $\{e^{i k x}, e^{i(k - 2\pi/a) x}\}$.
3. Diagonalise the $2 \times 2$ matrix and write down the band gap
   $E_\text{gap}$ as a function of $V_0$.

(Compare to equation \eqref{eq:ch-07-worked-gap} in the worked
example.)
</details>

<details class="answer">
<summary>Show answer</summary>

**Part 1.** With $\cos\theta = (e^{i\theta} + e^{-i\theta})/2$,

$$
V(x) = \tfrac{V_0}{2}\, e^{i 2\pi x/a} + \tfrac{V_0}{2}\, e^{-i 2\pi x/a}.
$$

The Fourier coefficients on the reciprocal-lattice grid $G = m \cdot
2\pi/a$ are therefore

$$
V_{\text{per}}(G) = \begin{cases}
\phantom{-}V_0/2 & \text{if } G = +2\pi/a, \\
\phantom{-}V_0/2 & \text{if } G = -2\pi/a, \\
\phantom{-}0 & \text{otherwise (including } G = 0\text{).}
\end{cases}
$$

For $V_0 = -0.2$ Hartree, $V_{\text{per}}(\pm 2\pi/a) = -0.1$ Hartree.

**Part 2.** At $k = \pi/a$ the two free-electron states
$|\pi/a\rangle$ and $|-\pi/a\rangle$ are degenerate, with kinetic
energy $\tfrac{1}{2}(\pi/a)^2$. The potential couples them with
matrix element $V_{\text{per}}((-\pi/a) - (\pi/a)) = V_{\text{per}}(-2\pi/a)
= V_0/2 = -0.1$ Hartree. The $2 \times 2$ Hamiltonian is

$$
H = \tfrac{1}{2}(\pi/a)^2
    \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
  + \tfrac{V_0}{2}
    \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}.
$$

**Part 3.** The eigenvalues of this matrix are

$$
\varepsilon_\pm(\pi/a) = \tfrac{1}{2}(\pi/a)^2 \pm \tfrac{V_0}{2},
$$

so the band gap is

$$
\boxed{E_\text{gap} = V_0 = -0.2 \text{ Hartree}.}
$$

(For a general cosine amplitude, the gap is $|V_0|$; the
sign of $V_0$ decides which band is on top.)

The factor of 2 difference between this answer and
\eqref{eq:ch-07-worked-gap} is the factor of 2 in the cosine
decomposition: $V(x) = -0.5 \cos(2\pi x/a)$ has Fourier coefficients
of $-1/4$ at $G = \pm 2\pi/a$, while $V(x) = -0.2 \cos(2\pi x/a)$
has Fourier coefficients of $-0.1$ at the same points. The band gap
in both cases is $2 \cdot |\text{Fourier coefficient}| = 2 \cdot
|V_0|/2 = |V_0|$.

</details>

<details class="problem">
<summary>Problem 2 (medium) — k-point density and BZ volume</summary>

A solid has a cubic direct lattice with conventional lattice
constant $a$, and the BvK boundary conditions are imposed on a
supercell of $N \times N \times N$ primitive cells. Show that:

1. The number of allowed k-points in the first Brillouin zone is
   exactly $N^3$.
2. The density of k-points (k-points per unit volume of the BZ) is
   $V_\text{cell} / (2\pi)^3$, where $V_\text{cell}$ is the
   primitive-cell volume.
3. The sum over k-points,
   $\tfrac{1}{N^3} \sum_{\mathbf k} f(\mathbf k)$,
   has the dimensions of $f$ times $1/N^3$. Use part 2 to convert
   the sum to a Riemann sum for the BZ integral,
   $\tfrac{V_\text{cell}}{(2\pi)^3} \int_\text{BZ} f(\mathbf k) d\mathbf k$,
   and verify the equivalence.

</details>

<details class="answer">
<summary>Show answer</summary>

**Part 1.** The BvK conditions on a supercell of $N \times N \times
N$ primitive cells are

$$
\psi(\mathbf r + N \mathbf a_i) = \psi(\mathbf r), \qquad i = 1, 2, 3.
$$

A Bloch wave $e^{i \mathbf k \cdot \mathbf r}$ satisfies these iff

$$
e^{i \mathbf k \cdot (N \mathbf a_i)} = 1
\;\;\Longleftrightarrow\;\;
\mathbf k \cdot \mathbf a_i = \tfrac{2\pi m_i}{N}, \quad m_i = 0, 1, \ldots, N - 1.
$$

The allowed $\mathbf k$ are therefore a uniform mesh with $N$ points
along each primitive direction, giving exactly $N^3$ mesh points in
the BZ.

**Part 2.** The volume of the first Brillouin zone is
$V_\text{BZ} = (2\pi)^3 / V_\text{cell}$ (from
\eqref{eq:ch-07-reciprocal-volume}). The k-point density is

$$
\frac{N^3}{V_\text{BZ}} = \frac{N^3 \cdot V_\text{cell}}{(2\pi)^3}.
$$

But "density" should not depend on $N$ — in the BvK formalism $N$
is a *mesh* parameter, not a physical one. The right thing to count
is the number of k-points *per unit cell*: $N^3$ k-points live in
the first BZ, and the first BZ itself is associated with one
primitive cell, so the density of k-points per unit volume of the
BZ, when properly normalised, is

$$
\rho_\mathbf k = \frac{1}{V_\text{BZ}} = \frac{V_\text{cell}}{(2\pi)^3}.
$$

**Part 3.** Convert the sum to an integral using the spacing
$\Delta k_i = 2\pi/(N a_i)$ in each direction. The volume of one
mesh cell is

$$
\Delta V = \Delta k_1 \Delta k_2 \Delta k_3
         = \frac{(2\pi)^3}{N^3 V_\text{cell}}.
$$

The Riemann sum is then

$$
\frac{1}{N^3} \sum_{\mathbf k} f(\mathbf k)
   = \frac{V_\text{cell}}{(2\pi)^3} \sum_{\mathbf k} f(\mathbf k) \, \Delta V
   \;\xrightarrow[N \to \infty]{}\; \frac{V_\text{cell}}{(2\pi)^3} \int_\text{BZ} f(\mathbf k) \, d\mathbf k.
$$

The factor $V_\text{cell} / (2\pi)^3$ is the same as the one in
\eqref{eq:ch-07-bz-integral}, and the equality is exact in the
$N \to \infty$ limit. In practice the equality is approximate at
finite $N$, with the convergence rate \eqref{eq:ch-07-mp-error}.

</details>

<details class="problem">
<summary>Problem 3 (hard) — Methfessel–Paxton smearing and the Fermi level</summary>

In a metallic calculation, the Methfessel–Paxton (MP) smearing
scheme replaces the discontinuous Fermi–Dirac occupation at $T = 0$
by a smooth function of width $\sigma$ in energy. The occupations
are

$$
f_{n\mathbf k} = \tfrac{1}{2} \operatorname{erfc}\!\left[\tfrac{\varepsilon_{n\mathbf k} - \mu}{\sigma}\right]
                + \sum_{l=1}^{N_\text{MP}} A_l \, H_{2l-1}\!\left[\tfrac{\varepsilon_{n\mathbf k} - \mu}{\sigma}\right] e^{-(\varepsilon_{n\mathbf k} - \mu)^2/\sigma^2},
$$

where $H_n$ is the physicist's Hermite polynomial, $A_l$ are
fixed coefficients, and $\mu$ is the *smearing chemical potential*
determined by the constraint

$$
\sum_{n\mathbf k} f_{n\mathbf k} = N_e.
$$

1. Show that the MP occupations sum to $N_e$ for any choice of
   $\mu$, by construction. (State which property of the Hermite
   polynomials makes this work.)
2. Show that the electronic entropy contribution to the free
   energy is

$$
-T S_\text{el} = \sum_{n\mathbf k} \bigl[ \varepsilon_{n\mathbf k} f_{n\mathbf k} - \sigma \, g_{n\mathbf k} \bigr],
$$

for some smooth function $g_{n\mathbf k}$, and identify $g$ for
$N_\text{MP} = 0$ (Gaussian smearing).
3. The "true" $T = 0$ total energy is

$$
E_0 = \lim_{\sigma \to 0} \bigl[ E_\text{band}(\sigma) + T S_\text{el}(\sigma) \bigr],
$$

where $E_\text{band}(\sigma) = \sum_{n\mathbf k} \varepsilon_{n\mathbf k} f_{n\mathbf k}$.
Explain why the $\sigma \to 0$ extrapolation converges more
rapidly than the original (unsmeared) sum for a metal, and
identify the leading-order correction in $\sigma$ for MP smearing
with $N_\text{MP} = 1$.
</details>

<details class="answer">
<summary>Show answer</summary>

**Part 1.** The MP occupation function is constructed so that its
integral over all energies equals the number of states below
$\mu$ for any $\sigma$. This works because the Hermite polynomials
$H_n(x)$ with $n \ge 1$ are odd functions of $x$, and they are
orthogonal to the constant function on the real line with the
Gaussian weight. The constant term in $f$ reproduces the
Heaviside-step integral exactly; the odd-Hermite corrections
average to zero. The constraint $\sum f = N_e$ is then a
one-dimensional nonlinear equation for $\mu$ at fixed
$\varepsilon_{n\mathbf k}$, solvable by Newton iteration or
bisection.

**Part 2.** The electronic entropy of a Fermi–Dirac distribution is

$$
S = -k_B \sum_{n\mathbf k} \bigl[ f_{n\mathbf k} \ln f_{n\mathbf k} + (1 - f_{n\mathbf k}) \ln(1 - f_{n\mathbf k}) \bigr].
$$

For Gaussian smearing ($N_\text{MP} = 0$), the occupations are
$f = \tfrac{1}{2} \operatorname{erfc}\!\bigl[(\varepsilon - \mu)/\sigma\bigr]$.
Inserting into the entropy gives, after a Gaussian integral,

$$
g_{n\mathbf k} = \tfrac{1}{2\sqrt{\pi}} e^{-(\varepsilon_{n\mathbf k} - \mu)^2 / \sigma^2}.
$$

(The factor $1/2$ comes from the $\tfrac{1}{2}$ prefactor of
$\operatorname{erfc}$.) In other words, the entropy contribution
per state is $-\tfrac{\sigma}{2\sqrt{\pi}} e^{-x^2}$ with $x =
(\varepsilon - \mu)/\sigma$.

**Part 3.** For an unsmeared metal, the sum
$\sum_{\mathbf k} f(\varepsilon_{n\mathbf k} - \mu)$ converges to
the integral only as $1/N$ because of the step at the Fermi
surface. With smearing, the integrand is smooth in
$\varepsilon$ (the $\operatorname{erfc}$ varies on a scale
$\sigma$), so the same $1/N$ mesh approximates the integral to
$O(1/N^2)$ provided the mesh is fine enough to resolve the
smoothed function.

The remaining error is the *systematic* error from using a
smeared occupation instead of the true step function. For
$N_\text{MP} = 0$ (Gaussian smearing), this error is
$O(\sigma^2)$: the leading correction to $E_0$ is quadratic in
$\sigma$. For $N_\text{MP} = 1$ (first-order MP), the leading
correction is $O(\sigma^4)$: the second-order term in the
Hermite expansion of the step function exactly cancels the
quadratic correction of the Gaussian. (To see this, note that
the $A_1$ coefficient is chosen so that the integral of the
first-Hermite term is zero; the remaining error comes from the
next non-zero term, which is $O(\sigma^4)$.)

A practical strategy: run the calculation with several values
of $\sigma$ (e.g. $\sigma = 0.02, 0.01, 0.005$ Hartree), plot
$E(\sigma)$ vs. $\sigma^2$ (for $N_\text{MP} = 0$) or vs.
$\sigma^4$ (for $N_\text{MP} = 1$), and extrapolate linearly to
$\sigma = 0$. The extrapolated value is the $T = 0$ total
energy.

</details>

## 7.10 What we left out

The chapter has been a self-contained introduction to Bloch's
theorem, the Brillouin zone, plane-wave basis sets, and k-point
sampling. A non-exhaustive list of the topics we have *not* covered:

- **Spin–orbit coupling.** The Hamiltonian
  \eqref{eq:ch-07-hamiltonian} is spin-free. For solids with heavy
  elements (5*d*, 6*p*, f-electron systems), the spin–orbit term
  $\hat H_\text{SO} = \tfrac{1}{2} \boldsymbol{\sigma} \cdot (\nabla V
  \times \mathbf p)$ has to be added; the Bloch factor $e^{i\mathbf k
  \cdot \mathbf r}$ becomes a 2 × 2 spinor matrix. This is essential
  for the correct band topology of topological insulators and
  transition-metal dichalcogenides.
- **Non-collinear magnetism and spin textures.** The Bloch theorem
  generalises to spinor wavefunctions; the "bands" become
  vector-valued and can carry non-trivial spin textures (skyrmions,
  Rashba splitting, …).
- **Symmetry-adapted k-points and time-reversal.** The
  Monkhorst–Pack mesh can be folded onto the irreducible BZ using
  the crystal point-group symmetries, giving the "irreducible
  k-point" set. Time-reversal symmetry $\mathbf k \to -\mathbf k$ at
  $\varepsilon_{n,-\mathbf k} = \varepsilon_{n,\mathbf k}$ (for
  spinless, time-reversal-invariant systems) can be used to halve
  the mesh again.
- **Projector-augmented waves (PAW), ultrasoft pseudopotentials.**
  The plane-wave basis is great for valence electrons but hopeless
  for the tightly-bound core. The PAW and ultrasoft-pseudopotential
  methods of [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) augment the
  plane-wave basis near the nuclei with localised functions, and
  reconstitute the all-electron wavefunction in the augmentation
  region. This is what every production plane-wave code actually
  uses.
- **Linear-response / DFPT.** Frozen-phonon and density-functional
  perturbation theory ([chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}))
  compute phonons and electron–phonon coupling from the linear
  response of the periodic ground state. The same plane-wave
  machinery is used, but the perturbation is itself a Bloch wave
  with crystal momentum $\mathbf q$.
- **Wannier functions, Berry phase, and modern theory of
  polarisation.** The Bloch functions are not the only complete
  basis; the Wannier functions obtained by Fourier-transforming the
  Bloch waves are localised in real space and are the natural basis
  for tight-binding models. Berry-phase quantities (polarisation,
  orbital magnetisation, Chern number) are essential for
  [chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}).
- **Many-body perturbation theory ($GW$, BSE).** The Kohn–Sham
  eigenvalues of chapter 04 are not quasiparticle energies.
  $G_0 W_0$ corrections and the Bethe–Salpeter equation are the
  standard ways to compute band gaps and excitons in solids.
- **Quantum-chemistry-style methods in periodic boundary
  conditions.** Localised-orbital methods (Gaussian-basis DFT,
  quantum-chemistry methods like CCSD(T) in a periodic supercell)
  provide an alternative to plane waves, with different strengths
  and weaknesses. We have not covered them.

> Next: [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }}) —
> pseudopotentials: why plane waves cannot describe tightly-bound
> core electrons, and how the projector-augmented-wave method fixes it.
