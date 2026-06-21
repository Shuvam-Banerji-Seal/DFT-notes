---
layout: page
title: "Crystallography and space groups — DFT Notes"
permalink: /dft-notes/extras/crystallography/
description: >-
  A reader-facing reference for crystallography and space groups
  as used in density-functional theory: the 7 crystal systems, the
  14 Bravais lattices, the 32 point groups, the 230 space groups,
  Wyckoff positions, reciprocal lattices, Brillouin zones, and the
  high-symmetry k-paths. With practical examples for FCC, BCC,
  hexagonal, and perovskite structures.
keywords: "crystallography, space group, Bravais lattice, point group,
  Wyckoff position, reciprocal lattice, Brillouin zone, k-path,
  Hermann-Mauguin, Schoenflies, Pearson symbol, International
  Tables, Bilbao Crystallographic Server, symmetry"
---

# Crystallography and space groups

> The "I need to figure out which space group my crystal is, what
> the conventional cell looks like, and how to specify it in a DFT
> code" reference.  Open it, look up the symbol, close it, return
> to the calculation.

This page is the **crystallographic analogue** of the
[notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }})
and the
[math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}).
It collects, in one place, every crystallographic symbol, table,
and convention the chapters of DFT Notes refer to in passing.
Whenever a chapter writes "$Fm\bar 3 m$" or "$P 6_3 / m m c$" or
"the 8a Wyckoff position of $Fd\bar 3 m$", the meaning lives
here and is linked back to its source.

**Conventions used in this page.**

- MathJax 3 is used.  Numbered equations use
  `\begin{equation} ... \label{eq:cryst-foo} ... \end{equation}`;
  cross-references in this file are `\eqref{eq:cryst-foo}`.
- Crystallographic angles $\alpha$, $\beta$, $\gamma$ are the
  angles between pairs of conventional cell edges:
  $\alpha = \angle(\mathbf b, \mathbf c)$, $\beta = \angle(\mathbf a, \mathbf c)$,
  $\gamma = \angle(\mathbf a, \mathbf b)$.
- Lattice parameters $(a, b, c)$ and reciprocal parameters
  $(`a*, b*`, `c`)$ are in Å and Å⁻¹ respectively; we follow
  the crystallographic convention rather than the
  atomic-unit convention of
  [chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }}) when
  quoting experimental values.  Atomic-unit values are stated
  explicitly when needed.
- High-symmetry k-points use the **Setyawan–Curtarolo** convention
  adopted by the Materials Project, AFLOW, and most modern DFT
  codes.  This is the same convention as
  [chapter 07 §7.4.3]({{ "/dft-notes/chapter-07/" | relative_url }})
  and
  [chapter 11 §11.2]({{ "/dft-notes/chapter-11/" | relative_url }}).
- Hermann–Mauguin (HM) symbols are written in **bold itali`c*`*
  in the running text for legibility (e.g. *P 6₃/m m `c*`); Schoenflies
  symbols are written upright (e.g. $D_{6h}^4$).  The slash `/`
  in an HM symbol separates *equivalent* directions perpendicular
  and parallel to the principal axis.

**Cross-references.**  This page assumes the reader is familiar
with the reciprocal lattice (chapter 07 §7.4), the Bloch theorem
(chapter 07 §7.1), and the band-structure plotting workflow
(chapter 11 §11.2).  The 32 point groups and 230 space groups
are introduced in [chapter 07 §7.10]({{ "/dft-notes/chapter-07/" | relative_url }})
in their DFT context; this page is the *reference* companion.

The page is organised in ten sections.  Sections 1–5 are the
"what is it?" reference: lattices, point groups, space groups,
Wyckoff positions, Pearson symbols.  Sections 6–7 are the
"where is it in reciprocal space?" reference: Brillouin zones and
k-paths.  Section 8 is the "how do I use it?" practical guide
for VASP, Quantum ESPRESSO, CASTEP, SIESTA, and the Bilbao
Crystallographic Server.  Sections 9–10 are the side-by-side
translation tables (Pearson, HM/Schoenflies).

| § | Topic | Reader's question |
|:-:|:------|:-------------------|
| 1 | Direct and reciprocal lattices | "What are the 7 systems and 14 Bravais lattices?" |
| 2 | The 32 point groups | "Which point group is this crystal?" |
| 3 | The 230 space groups | "What's the space group number of *P 6₃/m m `c*`?" |
| 4 | Wyckoff positions | "Which sites in the unit cell are symmetry-equivalent?" |
| 5 | Bravais lattice parameter table | "What's the Pearson symbol of a base-centred monoclinic cell?" |
| 6 | Reciprocal lattice and Brillouin zones | "What is the first BZ of an FCC crystal?" |
| 7 | High-symmetry k-paths | "What k-path should I use for BCC iron?" |
| 8 | Working with space groups in DFT codes | "How do I tell VASP the space group?" |
| 9 | Pearson symbol cheat sheet | "What does the suffix of `tI` mean?" |
| 10 | Hermann–Mauguin and Schoenflies side-by-side | "What is $O_h$ in Hermann–Mauguin?" |

---

## 1. Direct and reciprocal lattices

A **Bravais lattice** is the infinite, discrete set of points
$\{\mathbf R = n_1 \mathbf a_1 + n_2 \mathbf a_2 + n_3 \mathbf a_3 :
n_i \in \mathbb Z\}$ in $\mathbb R^3$ that a real crystal's
translations form.  The **primitive vectors** $\mathbf a_1,
\mathbf a_2, \mathbf a_3$ are the three linearly-independent
shortest vectors that generate the lattice.  The **conventional
cell** is a (typically larger) cubic-, orthorhombic-, or
hexagonal-shaped cell that exposes the lattice's symmetry; it is
the cell of choice for reporting lattice parameters and atomic
positions, while the primitive cell is the cell of choice for
band-structure and density-of-states calculations.

### 1.1 The 7 crystal systems

The **7 crystal systems** classify lattices by the metric
properties of the conventional cell.  Each system has its own
set of constraints on the six cell parameters
$(a, b, c, \alpha, \beta, \gamma)$, where $a, b, c$ are the
edge lengths and $\alpha, \beta, \gamma$ are the angles between
pairs of edges (definitions in the conventions box above).

| Crystal system | Cell constraints | Holohedral point group (HM) | Order |
|:--|:--|:--|:-:|
| Triclinic | $a \ne b \ne c$; $\alpha \ne \beta \ne \gamma \ne 90°$ | $\bar 1$ | 2 |
| Monoclinic | $a \ne b \ne c$; $\alpha = \gamma = 90°$, $\beta \ne 90°$ | $2/m$ | 4 |
| Orthorhombic | $a \ne b \ne c$; $\alpha = \beta = \gamma = 90°$ | $mmm$ | 8 |
| Tetragonal | $a = b \ne c$; $\alpha = \beta = \gamma = 90°$ | $4/mmm$ | 16 |
| Trigonal (rhombohedral axes) | $a = b = c$; $\alpha = \beta = \gamma \ne 90°$ | $\bar 3 m$ | 12 |
| Hexagonal | $a = b \ne c$; $\alpha = \beta = 90°$, $\gamma = 120°$ | $6/mmm$ | 24 |
| Cubic | $a = b = c$; $\alpha = \beta = \gamma = 90°$ | $m\bar 3 m$ | 48 |

The **holohedral point grou`p** (or holohedry*) is the
full point group that maps the conventional cell onto itself.
It is the highest-symmetry point group of the crystal system;
every other point group in the same system is a subgroup of the
holohedry.  The order column is the number of operations in the
group.  See §2 below for the full 32-point-group classification.

> **Trigonal vs hexagonal.**  Some authors use the term
> "rhombohedral" for the trigonal system.  The lattice can be
> described with either rhombohedral axes ($a = b = c$,
> $\alpha = \beta = \gamma$) or hexagonal axes (three times
> larger conventional cell with $a = b \ne c$,
> $\gamma = 120°$).  Both descriptions are valid; the
> hexagonal setting is more common in modern DFT codes
> (VASP, Quantum ESPRESSO) because the BZ is a regular
> hexagonal prism, easier to navigate.

### 1.2 The 14 Bravais lattices

The 7 crystal systems admit 14 distinct Bravais lattices when
the **centring** of the conventional cell is taken into account.
Centring types are:

- $P$ — **primitive**: lattice points only at the corners.
- $I$ — **body-centre`d*`*: extra lattice point at the centre
  $(0, 0, 0) + (1/2, 1/2, 1/2)$ (in fractional cell coordinates).
- $F$ — **face-centre`d*`*: extra lattice points at
  $(0, 1/2, 1/2)$, $(1/2, 0, 1/2)$, $(1/2, 1/2, 0)$.
- $C$ (or $A$, $B$) — **base-centre`d*`*: extra lattice point on
  a single pair of opposite faces, e.g. $C$-centring on
  $(0, 1/2, 1/2)$.

| Crystal system | Bravais lattices | Centring variants | Lattice points per conventional cell |
|:--|:--|:--|:-:|
| Triclinic | $aP$ | $P$ | 1 |
| Monoclinic | $mP$, $mS$ | $P$, $C$ (called $S$ in Pearson) | 1, 2 |
| Orthorhombic | $oP$, $oS$, $oI$, $oF$ | $P$, $C$, $I$, $F$ | 1, 2, 2, 4 |
| Tetragonal | $tP$, $tI$ | $P$, $I$ | 1, 2 |
| Trigonal | $hP$ (hex. axes), $hR$ (rhomb. axes) | $P$ (hex), $R$ (rhomb) | 1, 3 (rhomb cell) |
| Hexagonal | $hP$ | $P$ | 1 |
| Cubic | $cP$, $cI$, $cF$ | $P$, $I$, $F$ | 1, 2, 4 |

The labels in the second column are the **Pearson symbols**.
The lowercase letter is the crystal system ($a$ = anorthic =
triclinic, $m$ = monoclinic, $o$ = orthorhombic, $t$ =
tetragonal, $h$ = hexagonal or trigonal, $c$ = cubic); the
uppercase letter is the centring.  See §9 for the full Pearson
cheat sheet.

The 14 Bravais lattices are sometimes called the 14 *Bravais
types*: a primitive cubic lattice and a primitive hexagonal
lattice are the only "primitive" Bravais lattices in their
systems, and adding centring to a primitive lattice either
generates a new lattice type (e.g. body-centred cubic $\ne$
primitive cubic) or, in some cases, is equivalent to a smaller
primitive cell of another centring.  E.g. base-centred
orthorhombic ($oS$ or $oC$) is *not* equivalent to primitive
orthorhombic; the extra centring point gives a different
topology.

### 1.3 Reciprocal lattice

For every Bravais lattice with primitive vectors
$\mathbf a_1, \mathbf a_2, \mathbf a_3$ there is a dual Bravais
lattice, the **reciprocal lattice**, with primitive vectors
$\mathbf b_1, \mathbf b_2, \mathbf b_3$ defined by

\begin{equation}
\label{eq:cryst-recip-def}
\mathbf a_i \cdot \mathbf b_j \;=\; 2\pi \delta_{ij}, \qquad i, j \in \{1, 2, 3\}.
\end{equation}

This is the definition adopted by the solid-state community
(Kittel, Ashcroft & Mermin, the DFT notes themselves).  The
crystallographic community sometimes uses
$\mathbf a_i \cdot \mathbf b_j = \delta_{ij}$ (no $2\pi$); when
in doubt, check the convention of the code or paper you are
reading.  In the DFT notes the $2\pi$ convention is universal
(see
[notation glossary §10]({{ "/dft-notes/extras/notation-glossary/" | relative_url }})
and [chapter 07 §7.4.1]({{ "/dft-notes/chapter-07/" | relative_url }})).
Every reciprocal-lattice vector is an integer combination

\begin{equation}
\label{eq:cryst-recip-vector}
\mathbf G \;=\; h \mathbf b_1 + k \mathbf b_2 + l \mathbf b_3, \qquad h, k, l \in \mathbb Z,
\end{equation}

and the **volume of the reciprocal primitive cell** is

\begin{equation}
\label{eq:cryst-recip-volume}
V_\text{BZ}^* \;=\; \mathbf b_1 \cdot (\mathbf b_2 \times \mathbf b_3) \;=\; \frac{(2\pi)^3}{V_\text{cell}},
\end{equation}

where $V_\text{cell} = \mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)$
is the direct-lattice primitive-cell volume.  Equation
\eqref{eq:cryst-recip-volume} is the reason the BZ volume scales
as $1/V_\text{cell}$: a larger direct-space cell gives a denser
reciprocal space with a smaller BZ.

An explicit construction of the reciprocal primitive vectors
that avoids solving a $3 \times 3$ linear system is

\begin{equation}
\label{eq:cryst-recip-explicit}
\mathbf b_1 \;=\; 2\pi\, \frac{\mathbf a_2 \times \mathbf a_3}{\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)},
\qquad
\mathbf b_2 \;=\; 2\pi\, \frac{\mathbf a_3 \times \mathbf a_1}{\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)},
\qquad
\mathbf b_3 \;=\; 2\pi\, \frac{\mathbf a_1 \times \mathbf a_2}{\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)} .
\end{equation}

The denominator $\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)$ is
six times the volume of the primitive cell (the scalar triple
product).  Equation \eqref{eq:cryst-recip-explicit} is the
formula used in `numpy` and `spglib` to compute the reciprocal
lattice from the direct lattice.

> **Verification of \eqref{eq:cryst-recip-explicit}.**  Take
> $\mathbf a_1 \cdot \mathbf b_1$ as the test:
> $\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3) / \mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3) = 1$,
> so $\mathbf a_1 \cdot \mathbf b_1 = 2\pi$.  The other two
> $\mathbf a_i \cdot \mathbf b_1$ are $\mathbf a_2 \cdot (\mathbf a_2 \times \mathbf a_3) = 0$ and
> $\mathbf a_3 \cdot (\mathbf a_2 \times \mathbf a_3) = 0$ (a vector dotted into a cross product
> that contains itself is zero).  Thus $\mathbf a_i \cdot \mathbf b_j = 2\pi \delta_{ij}$ as
> required.

### 1.4 Reciprocal lattice of each Bravais lattice

The reciprocal lattice of a centred direct lattice is *itsel`f*`
a Bravais lattice, and the pairing is its own kind of duality.
The complete table:

| Direct Bravais | Centring | Reciprocal Bravais | Centring | Verdict |
|:--|:--|:--|:--|:--|
| Triclinic $P$ ($aP$) | $P$ | Triclinic $P$ ($aP$) | $P$ | Self-dual |
| Monoclinic $P$ ($mP$) | $P$ | Monoclinic $P$ ($mP$, $`b*`$ unique) | $P$ | Self-dual |
| Monoclinic $C$ ($mS$, $C$-centred) | $C$ | Monoclinic $P$ ($mP$) | $P$ | $\to$ primitive |
| Orthorhombic $P$ ($oP$) | $P$ | Orthorhombic $P$ ($oP$) | $P$ | Self-dual |
| Orthorhombic $C$ ($oS$) | $C$ | Orthorhombic $P$ ($mP$ in monoclinic) | $P$ | $\to$ primitive |
| Orthorhombic $I$ ($oI$) | $I$ | Orthorhombic $F$ ($oF$) | $F$ | $\leftrightarrow$ |
| Orthorhombic $F$ ($oF$) | $F$ | Orthorhombic $I$ ($oI$) | $I$ | $\leftrightarrow$ |
| Tetragonal $P$ ($tP$) | $P$ | Tetragonal $P$ ($tP$) | $P$ | Self-dual |
| Tetragonal $I$ ($tI$) | $I$ | Tetragonal $I$ ($tI$) | $I$ | Self-dual |
| Hexagonal $P$ ($hP$) | $P$ | Hexagonal $P$ ($hP$) | $P$ | Self-dual |
| Rhombohedral $R$ ($hR$) | $R$ | Rhombohedral $R$ ($hR$) | $R$ | Self-dual |
| Cubic $P$ ($cP$) | $P$ | Cubic $P$ ($cP$) | $P$ | Self-dual |
| Cubic $I$ ($cI$) | $I$ | Cubic $F$ ($cF$) | $F$ | $\leftrightarrow$ |
| Cubic $F$ ($cF$) | $F$ | Cubic $I$ ($cI$) | $I$ | $\leftrightarrow$ |

The two most important dualities for solid-state DFT are
**FCC $\leftrightarrow$ BCC** and **body-centred orthorhombic
$\leftrightarrow$ face-centred orthorhombi`c*`*.

### 1.5 Worked example: FCC direct $\to$ BCC reciprocal

> The reciprocal lattice of a face-centred cubic direct lattice
> is a body-centred cubic reciprocal lattice (and vice versa).
> This is a famous result that the DFT notes use in
> [chapter 07 §7.4.3]({{ "/dft-notes/chapter-07/" | relative_url }}).

The conventional FCC lattice with cubic parameter $a$ has
primitive vectors

\begin{equation}
\label{eq:cryst-fcc-prim}
\mathbf a_1 = \frac{a}{2}(0, 1, 1), \quad
\mathbf a_2 = \frac{a}{2}(1, 0, 1), \quad
\mathbf a_3 = \frac{a}{2}(1, 1, 0).
\end{equation}

The scalar triple product is

\begin{align}
\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3)
   &\;=\; \frac{a^3}{8} \det \begin{pmatrix} 0 & 1 & 1 \\\\ 1 & 0 & 1 \\\\ 1 & 1 & 0 \end{pmatrix} \nonumber \\\
   &\;=\; \frac{a^3}{8} (0 + 1 + 1) \;=\; \frac{a^3}{4} ,
\end{align}

so the primitive cell volume is $V_\text{cell} = a^3/4 = a^3/4$
— exactly $1/4$ of the conventional cubic cell volume, as
expected for an FCC lattice (4 lattice points per conventional
cell).

Apply \eqref{eq:cryst-recip-explicit}.  The cross product
$\mathbf a_2 \times \mathbf a_3 = (a^2/4)(-1, 1, 0)$ (expand
by hand or use `numpy.cross`), and dividing by
$\mathbf a_1 \cdot (\mathbf a_2 \times \mathbf a_3) = a^3/4$
gives

\begin{equation}
\label{eq:cryst-b1}
\mathbf b_1 \;=\; \frac{2\pi}{a}(-1, 1, 0) .
\end{equation}

Cyclic permutation gives the full set:

\begin{equation}
\label{eq:cryst-fcc-recip}
\mathbf b_1 = \frac{2\pi}{a}(-1, 1, 1), \quad
\mathbf b_2 = \frac{2\pi}{a}(1, -1, 1), \quad
\mathbf b_3 = \frac{2\pi}{a}(1, 1, -1) .
\end{equation}

The shortest reciprocal-lattice vectors are
$\pm (2\pi/a)(\pm 1, \pm 1, \pm 1)$ — 8 in total — and the
**conventional cubic cell** of the reciprocal lattice has
parameter

\begin{equation}
\label{eq:cryst-fcc-bcc-conv}
a^* \;=\; \frac{4\pi}{a} ,
\end{equation}

with body-centring translations $(2\pi/a)(1, 1, 1)$ etc.  The
reciprocal lattice is therefore **BCC** with conventional
parameter $4\pi/a$.

> **Sanity check.**  The reciprocal of the reciprocal is the
> original: applying \eqref{eq:cryst-recip-explicit} to the BCC
> lattice with parameter $4\pi/a$ recovers an FCC lattice with
> parameter $a$.

---

## 2. The 32 crystallographic point groups

A **point grou`p*`* of a crystal is the set of isometries of
$\mathbb R^3$ that leave at least one point fixed and map the
crystal onto itself.  These isometries are the rotations,
reflections, inversions, and improper rotations (rotoinversions)
of §2.2 below.  The point group is the **directional** part of
the full **space grou`p*`* (§3); the space group adds the
translations.

### 2.1 The crystallographic restriction theorem

The only rotation orders $n$ for which an $n$-fold rotation
axis can be a symmetry of a 3-D Bravais lattice are

\begin{equation}
\label{eq:cryst-restriction}
n \;\in\; \{1, 2, 3, 4, 6\} .
\end{equation}

A 5-fold axis, an 8-fold axis, or a 7-fold axis is *not* a
Bravais-lattice symmetry.  (5-fold symmetries do appear in
**quasicrystals** — the Shechtman 1982 discovery, Nobel 2011 —
but those are not periodic in 3-D and are not the topic of this
page.)

The proof is a quick number-theoretic argument.  Take a
primitive cell with primitive vectors $\mathbf a$ and $\mathbf b$
in the plane perpendicular to the $n$-fold axis.  Rotate
$\mathbf a$ by $2\pi/n$ to get $\mathbf a'$.  By symmetry,
$\mathbf a' - \mathbf a$ must be a lattice vector, hence an
integer combination of $\mathbf a$ and $\mathbf b$.  In matrix
form,

\begin{equation}
\begin{pmatrix} a'_x \\\\ a'_y \end{pmatrix}
\;=\;
\begin{pmatrix} \cos(2\pi/n) & -\sin(2\pi/n) \\\\ \sin(2\pi/n) & \cos(2\pi/n) \end{pmatrix}
\begin{pmatrix} a_x \\\\ a_y \end{pmatrix}
\;=\;
\begin{pmatrix} p & q \\\\ r & s \end{pmatrix}
\begin{pmatrix} a_x \\\\ a_y \end{pmatrix}
\end{equation}

with $p, q, r, s$ integers (this is a property of the rotation
matrix with determinant 1 and integer entries).  Taking the
trace of both sides, $2\cos(2\pi/n) = p + s$ must be an integer.
The values of $2\cos(2\pi/n)$ are tabulated below.

| $n$ | $2\cos(2\pi/n)$ | Integer? |
|:-:|:-:|:-:|
| 1 | 2 | Yes |
| 2 | −2 | Yes |
| 3 | 1 | Yes |
| 4 | 0 | Yes |
| 5 | $(\sqrt{5}-1)/2$ | **No** |
| 6 | 1 | Yes |

Only $n = 1, 2, 3, 4, 6$ pass.  This is the **crystallographic
restriction theorem**.

### 2.2 The symmetry elements

The five "generators" of the point groups are the operations
that, combined with the cyclic group of order $n$, give every
crystallographic point group:

| Symbol | Operation | Order | Description |
|:--|:--|:-:|:--|
| $E$ | Identity | 1 | Does nothing |
| $C_n$ | Proper rotation by $2\pi/n$ | $n$ | Rotation about an axis; $n \in \{1, 2, 3, 4, 6\}$ |
| $\sigma$ | Mirror reflection | 2 | Reflection in a plane; sometimes written $m$ |
| $i$ | Inversion | 2 | Maps $\mathbf r \to -\mathbf r$; written $\bar 1$ in HM |
| $S_n$ | Improper rotation (rotoinversion) | $n$ | Rotation followed by inversion; $S_2 = i$, $S_1 = \sigma$ |
| $S_4$, $S_6$ | Special improper rotations | 4, 6 | $S_4$ is a 4-fold rotoinversion; $S_6$ a 6-fold rotoinversion |

The combination of these generators, with the restriction
$n \in \{1, 2, 3, 4, 6\}$ of \eqref{eq:cryst-restriction}, gives
exactly 32 distinct point groups — a counting result first
established by Hessel (1830), Gadolin (1867), and Schoenflies
(1891).

### 2.3 Schoenflies vs Hermann–Mauguin notation

Two notations coexist in the literature.  **Schoenflies**
notation is the older one (1891), used by chemists,
spectroscopists, and molecular physicists.  **Hermann–Mauguin**
(HM) notation is the international crystallographic standard
and is what every space-group database, the *International
Tables for Crystallography*, the Bilbao Crystallographic
Server, and every modern DFT code use.

| Feature | Schoenflies | Hermann–Mauguin |
|:--|:--|:--|
| Rotation $C_n$ | $C_2, C_3, C_4, C_6$ | $2, 3, 4, 6$ |
| Mirror $\sigma$ | $\sigma_h, \sigma_v, \sigma_d$ | $m$ |
| Inversion $i$ | $i$ | $\bar 1$ |
| $n$-fold rotoinversion $S_n$ | $S_4, S_6$ | $\bar 4, \bar 6$ |
| $n$-fold rotation + perpendicular $C_2$ | $D_n$ | $n 2$ or $n m m$ depending on mirrors |
| Order count (cubic $O_h$) | 48 | 48 |
| Default use | Spectroscopy, point-group theory | Crystallography, DFT |

A side-by-side table of all 32 point groups is in §10. ### 2.4 The 32 point groups grouped by crystal system

| Crystal system | Point groups (HM) | Point groups (Schoenflies) | Count |
|:--|:--|:--|:-:|
| Triclinic | $\bar 1$, $1$ | $C_i$, $C_1$ | 2 |
| Monoclinic | $2$, $m$, $2/m$ | $C_2$, $C_s$, $C_{2h}$ | 3 |
| Orthorhombic | $222$, $mm2$, $mmm$ | $D_2$, $C_{2v}$, $D_{2h}$ | 3 |
| Tetragonal | $4$, $\bar 4$, $4/m$, $422$, $4mm$, $\bar 4 2m$, $4/mmm$ | $C_4, S_4, C_{4h}, D_4, C_{4v}, D_{2d}, D_{4h}$ | 7 |
| Trigonal | $3$, $\bar 3$, $32$, $3m$, $\bar 3 m$ | $C_3, C_{3i}, D_3, C_{3v}, D_{3d}$ | 5 |
| Hexagonal | $6$, $\bar 6$, $6/m$, $622$, $6mm$, $\bar 6 m2$, $6/mmm$ | $C_6, C_{3h}, C_{6h}, D_6, C_{6v}, D_{3h}, D_{6h}$ | 7 |
| Cubic | $23$, $m\bar 3$, $432$, $\bar 4 3m$, $m\bar 3 m$ | $T, T_h, O, T_d, O_h$ | 5 |
| **Total** | | | **32** |

Sum check: $2 + 3 + 3 + 7 + 5 + 7 + 5 = 32$. ✓

### 2.5 Reference table: the 32 point groups with examples

Each row gives the HM symbol, the Schoenflies symbol, the order
of the group, the generating symmetry elements, and a typical
example material.

| # | HM | Schoenflies | Order | Generators | Example material |
|:-:|:--|:--|:-:|:--|:--|
| 1 | $1$ | $C_1$ | 1 | $E$ | CaCO₃-Pm (hypothetical) |
| 2 | $\bar 1$ | $C_i$ | 2 | $E, i$ | CuSO₄·5H₂O (triclinic) |
| 3 | $2$ | $C_2$ | 2 | $E, C_2$ | Sucrose |
| 4 | $m$ | $C_s$ | 2 | $E, \sigma$ | HCl (incommensurate) |
| 5 | $2/m$ | $C_{2h}$ | 4 | $E, C_2, i, \sigma_h$ | Gypsum, CaSO₄·2H₂O |
| 6 | $222$ | $D_2$ | 4 | $E, 3 C_2$ | Cholesterol |
| 7 | $mm2$ | $C_{2v}$ | 4 | $E, C_2, 2 \sigma_v$ | H₂O (molecular) |
| 8 | $mmm$ | $D_{2h}$ | 8 | $E, 3 C_2, i, 3 \sigma$ | α-Sulfur |
| 9 | $4$ | $C_4$ | 4 | $E, 2 C_4, C_2$ | C₃H₇I (iodopropane) |
| 10 | $\bar 4$ | $S_4$ | 4 | $E, 2 S_4, C_2$ | CaWO₄-Pm (low-T) |
| 11 | $4/m$ | $C_{4h}$ | 4 | $E, 2 C_4, C_2, i, S_4, \sigma_h$ | Scheelite, CaWO₄ |
| 12 | $422$ | $D_4$ | 8 | $E, 2 C_4, C_2, 4 C_2'$ | NiSO₄·6H₂O |
| 13 | $4mm$ | $C_{4v}$ | 8 | $E, 2 C_4, C_2, 4 \sigma_v$ | BaTiO₃ (tetragonal, HT) |
| 14 | $\bar 4 2m$ | $D_{2d}$ | 8 | $E, 2 S_4, C_2, 2 C_2', 2 \sigma_d$ | Chalcopyrite, CuFeS₂ |
| 15 | $4/mmm$ | $D_{4h}$ | 16 | $E, 2 C_4, C_2, 4 C_2', i, 2 S_4, \sigma_h, 4 \sigma_v, 4 \sigma_d$ | TiO₂ (rutile) |
| 16 | $3$ | $C_3$ | 3 | $E, 2 C_3$ | Quartz-P3 (low-T) |
| 17 | $\bar 3$ | $C_{3i}$ | 6 | $E, 2 C_3, i, 2 S_6$ | Dolomite |
| 18 | $32$ | $D_3$ | 6 | $E, 2 C_3, 3 C_2$ | α-Quartz-P3₁21 |
| 19 | $3m$ | $C_{3v}$ | 6 | $E, 2 C_3, 3 \sigma_v$ | Tourmaline |
| 20 | $\bar 3 m$ | $D_{3d}$ | 12 | $E, 2 C_3, 3 C_2, i, 2 S_6, 3 \sigma_d$ | Calcite, CaCO₃ |
| 21 | $6$ | $C_6$ | 6 | $E, 2 C_6, 2 C_3, C_2$ | — |
| 22 | $\bar 6$ | $C_{3h}$ | 6 | $E, 2 C_3, \sigma_h, 2 S_3$ | — |
| 23 | $6/m$ | $C_{6h}$ | 6 | $E, 2 C_6, 2 C_3, C_2, i, 2 S_3, 2 S_6, \sigma_h$ | Apatite (low-T) |
| 24 | $622$ | $D_6$ | 12 | $E, 2 C_6, 2 C_3, C_2, 6 C_2'$ | — |
| 25 | $6mm$ | $C_{6v}$ | 12 | $E, 2 C_6, 2 C_3, C_2, 6 \sigma_v$ | ZnO (wurtzite) |
| 26 | $\bar 6 m2$ | $D_{3h}$ | 12 | $E, 2 C_3, 3 C_2, \sigma_h, 2 S_3, 3 \sigma_v$ | Graphite, BN |
| 27 | $6/mmm$ | $D_{6h}$ | 24 | $E, 2 C_6, 2 C_3, C_2, 6 C_2', i, 2 S_3, 2 S_6, \sigma_h, 6 \sigma_v, 6 \sigma_d$ | hcp Mg, h-BN, graphite |
| 28 | $23$ | $T$ | 12 | $E, 8 C_3, 3 C_2$ | — |
| 29 | $m\bar 3$ | $T_h$ | 24 | $E, 8 C_3, 3 C_2, i, 8 S_6, 3 \sigma_h$ | Pyrite, FeS₂ |
| 30 | $432$ | $O$ | 24 | $E, 8 C_3, 3 C_2, 6 C_4, 6 C_2'$ | β-Mn (A13) |
| 31 | $\bar 4 3m$ | $T_d$ | 24 | $E, 8 C_3, 3 C_2, 6 S_4, 6 \sigma_d$ | Sphalerite, ZnS |
| 32 | $m\bar 3 m$ | $O_h$ | 48 | $E, 8 C_3, 3 C_2, 6 C_4, 6 C_2', i, 8 S_6, 3 \sigma_h, 6 S_4, 6 \sigma_d$ | Rocksalt NaCl, Cu, Si |

> **Order counting.**  The order of a point group is the
> number of distinct symmetry operations it contains.  For $C_n$
> it is $n$; for $D_n$ it is $2n$; for $T$ (chiral tetrahedral)
> it is 12; for $O$ (chiral octahedral, sometimes called the
> *rotation grou`p*` of the cube) it is 24; for $O_h$ (full
> octahedral) it is 48. The five cubic point groups are 12,
> 24, 24, 24, 48 in size, which sums with the others to 32. ---

## 3. The 230 space groups

A **space grou`p*`* is the full symmetry group of a crystal,
including both the directional symmetries of the point group
(§2) and the translational symmetries of the Bravais lattice
(§1).  The full group is **infinite** because translations
$\mathbf R \in \{\text{Bravais lattice}\}$ are infinite in
number; but the *factor* by which the group is infinite — the
**point grou`p*`* — is finite.  Every space group can be written
as a *coset decomposition* of its point group over the
translation subgroup, so the space group is "point group + a
small set of generators".

The enumeration of 3-D space groups is one of the great
counting theorems of 19th-century mathematics: there are
**exactly 230 distinct space groups** in three dimensions, a
result proved independently by
Schoenflies (1891), Fedorov (1891), and Barlow (1894).  The
classification is tabulated in the
*International Tables for Crystallography*, vol. A (6th ed.,
2016), and the equivalent Schoenflies notation in vol. E
(2002).  Modern web resources are the
[Bilbao Crystallographic Server](<https://www.cryst.ehu.es/>)
(BCS) and the `spglib` library.

### 3.1 The Seitz notation

Every element $g$ of a space group can be written in **Seitz
notation**

\begin{equation}
\label{eq:cryst-seitz}
g \;=\; \{R \mid \mathbf v\}, \qquad g \mathbf r \;=\; R \mathbf r + \mathbf v,
\end{equation}

with $R \in O(3)$ a point-group operation (rotation,
reflection, inversion, rotoinversion, or a product thereof) and
$\mathbf v \in \mathbb R^3$ a translation.  The composition rule
is

\begin{equation}
\label{eq:cryst-seitz-mult}
\{R_1 \mid \mathbf v_1\} \{R_2 \mid \mathbf v_2\}
\;=\; \{R_1 R_2 \mid R_1 \mathbf v_2 + \mathbf v_1\} .
\end{equation}

The translation subgroup is $\{\mathbf E \mid \mathbf R\}$ for
$\mathbf R \in \text{Bravais lattice}$, and the point group is
the set of $\{R \mid \mathbf 0\}$ operations in the group.

In the DFT notes the Seitz notation is introduced in
[chapter 07 §7.10.1]({{ "/dft-notes/chapter-07/" | relative_url }}).
Equations \eqref{eq:cryst-seitz} and \eqref{eq:cryst-seitz-mult}
above are identical to equations (7.139) and (7.140) of that
chapter.

### 3.2 Symmorphic vs non-symmorphic space groups

A space group is **symmorphi`c*`* if its point group is a
*subgrou`p*` of the space group in the literal sense — that is,
if every element of the point group $\{R \mid \mathbf 0\}$ is in
the space group.  Equivalently, a symmorphic space group is a
*direct product* of the point group and the translation
subgroup.

In a non-symmorphic space group, on the other hand, some
"point-group" operations are accompanied by a *fractional*
translation $\mathbf v$ that is not a Bravais vector.  These
fractional translations can be of two kinds:

- **Screw axis:** $\mathbf v$ is parallel to the rotation
  axis; the operation is a rotation + translation.  The
  notation $n_p$ denotes an $n$-fold rotation accompanied by a
  $p/n$ translation along the axis (in units of the cell
  parameter along the axis).  E.g. $2_1$ is a 2-fold rotation
  with translation by $c/2$; $4_1$ is a 4-fold rotation with
  translation by $c/4$.

- **Glide plane:** $\mathbf v$ lies in the mirror plane; the
  operation is a reflection + translation.  Glides are denoted
  $a$ (translation by $a/2$), $b$ (by $b/2$), $c$ (by $c/2$),
  $n$ (translation by $(a+b)/2$ or any other diagonal), and
  $d$ (translation by $(a+b)/4$ — a "diamond" glide).

Of the 230 space groups, exactly **73 are symmorphi`c*`* and
**157 are non-symmorphi`c*`*.  The symmorphic space groups are
the ones in which every crystal axis is described by a single
HM symbol without subscripts (screws) or letter (glides).  The
most common symmorphic space groups in DFT are $Pm\bar 3 m$
(No. 221), $F m \bar 3 m$ (No. 225), $P 6/m m m$ (No. 191), and
$P 4/m m m$ (No. 123).

### 3.3 Looking up a space group from its number

The *International Tables for Crystallography*, vol. A,
tabulates the 230 space groups in order from No. 1 to No. 230.
The numbering is unique and universal; "space group No. 227" is
$Fd\bar 3 m$ (the diamond structure) in every reference.  The
first 73 are symmorphic; numbers 74–230 are non-symmorphic.

A short cut for the practitioner:

- The number, the HM symbol, and the Schoenflies symbol are
  three equivalent labels for the same space group.  All three
  are accepted by modern DFT codes.
- The HM symbol has the structure
  $\text{centring} \, \text{position 1} \, \text{position 2} \,
  \text{position 3}$ where each *position* is a generator
  (rotation, screw, mirror, glide, or rotoinversion) along a
  specific crystallographic direction.
- The full entry in the *International Tables* (or on the BCS)
  includes the Wyckoff positions (§4), the maximal subgroups,
  and the generators.

> **Tip.**  The Python library `spglib` (H. T. Stokes, D. M.
> Hatch, Brigham Young University; python wrapper
> `pyspglib`) is the standard tool for symmetry analysis.  It
> takes a crystal structure (cell + atomic positions) and
> returns the space group number, the HM symbol, the
> Schoenflies symbol, the equivalent Wyckoff positions, and a
> symmetrised cell.

### 3.4 The most common space groups for DFT calculations

The 230 space groups are not used equally.  DFT calculations
in 2025 overwhelmingly use the following dozen-or-so, with
silicon, copper, α-quartz, and graphite as the canonical
examples.

| # | HM (full) | Schoenflies | Point group | Bravais lattice | Example compound |
|:-:|:--|:--|:--|:--|:--|
| 1 | $P 1$ | $C_1^1$ | $C_1$ | $aP$ | Generic disordered structure |
| 2 | $P \bar 1$ | $C_i^1$ | $C_i$ | $aP$ | CuSO₄·5H₂O |
| 14 | $P 2_1/c$ | $C_{2h}^5$ | $C_{2h}$ | $mP$ | Most molecular crystals |
| 15 | $C 2/c$ | $C_{2h}^6$ | $C_{2h}$ | $mS$ | Graphite intercalation compounds |
| 62 | $P n m a$ | $D_{2h}^{16}$ | $D_{2h}$ | $oP$ | Olivine, LiFePO₄; perovskite orthorhombic |
| 63 | $C m c m$ | $D_{2h}^{17}$ | $D_{2h}$ | $oS$ | LiCoO₂ (delithiated); TiB₂ |
| 123 | $P 4/m m m$ | $D_{4h}^{1}$ | $D_{4h}$ | $tP$ | La₂₋ₓSrₓCuO₄ (tetragonal) |
| 139 | $I 4/m m m$ | $D_{4h}^{17}$ | $D_{4h}$ | $tI$ | BaFe₂As₂; cuprate parent La₂CuO₄ |
| 186 | $P 6_3 m c$ | $C_{6v}^4$ | $C_{6v}$ | $hP$ | w-ZnO, w-CdS, AlN (2H polytype) |
| 194 | $P 6_3/m m c$ | $D_{6h}^4$ | $D_{6h}$ | $hP$ | hcp Mg, h-BN, graphite, 2H-MoS₂ |
| 164 | $P \bar 3 m 1$ | $D_{3d}^{1}$ | $D_{3d}$ | $hP$ | CdI₂ (1T polytype) |
| 166 | $R \bar 3 m$ | $D_{3d}^{5}$ | $D_{3d}$ | $hR$ | Bi, Sb, α-NaFeO₂ |
| 221 | $P m \bar 3 m$ | $O_h^1$ | $O_h$ | $cP$ | CsCl, simple cubic perovskite |
| 225 | $F m \bar 3 m$ | $O_h^5$ | $O_h$ | $cF$ | Cu, Al, Ni, NaCl, γ-Fe |
| 229 | $I m \bar 3 m$ | $O_h^9$ | $O_h$ | $cI$ | α-Fe, W, Mo, Cr |
| 227 | $F d \bar 3 m$ | $O_h^7$ | $O_h$ | $cF$ | Si, Ge, diamond, GaAs (zincblende) |
| 216 | $F \bar 4 3 m$ | $T_d^2$ | $T_d$ | $cF$ | Sphalerite ZnS, GaAs (zincblende) |
| 224 | $P n \bar 3 m$ | $O_h^4$ | $O_h$ | $cP$ | Perovskite (cubic), SrTiO₃ |

> **Zincblende vs diamond.**  $F \bar 4 3 m$ (No. 216) and
> $F d \bar 3 m$ (No. 227) have the same FCC Bravais lattice
> and the same occupied Wyckoff positions, but different
> *glide* planes.  In $F d \bar 3 m$ the two atoms of the basis
> sit at $(0, 0, 0)$ and $(1/4, 1/4, 1/4)$, which is the
> **diamon`d*`* structure.  In $F \bar 4 3 m$ the second atom is
> at $(1/4, 1/4, 1/4)$ as well, but the *`d*` glide of the
> diamond is replaced by a pure mirror — the **zincblende**
> structure.  If the two basis atoms are different species
> (GaAs, ZnS, CdTe), the inversion symmetry is broken and the
> group is zincblende.  If they are the same (Si, Ge, C), the
> group is diamond.

> **HM and Schoenflies — the canonical mappings for DFT.**
> Five space groups do most of the work: $F m \bar 3 m$ = $O_h^5$
> for FCC metals and NaCl; $I m \bar 3 m$ = $O_h^9$ for BCC
> metals; $F d \bar 3 m$ = $O_h^7$ for diamond/zincblende;
> $P 6_3/m m c$ = $D_{6h}^4$ for hcp and graphite; $P 2_1/c$ =
> $C_{2h}^5$ for molecular crystals.  The five together cover
> 80 % of the materials in the ICSD.

---

## 4. Wyckoff positions

A **Wyckoff position** of a space group is the set of
symmetry-equivalent sites in the unit cell.  Each space group
has a finite number of Wyckoff positions; the position with the
**highest site symmetry** and **lowest multiplicity** is the
**most special** and is conventionally labelled with the
**lowest letter** ($a$).

### 4.1 Multiplicity, letter, and site symmetry

Three numbers describe a Wyckoff position:

- **Multiplicity** $m$ — the number of symmetry-equivalent
  sites per **conventional** unit cell.  For a primitive cell
  $m$ counts the sites in the primitive cell; for a centred
  cell it is multiplied by the centring factor (1 for $P$, 2
  for $C$, 4 for $F$).

- **Wyckoff letter** — a single Latin letter starting from
  $a$ for the most special position, then $b, c, d, \dots$.
  Positions with the same letter have the same site symmetry.
  Letters run out after $z$ (or before, depending on the
  group); the IUC uses subscripts after that point.

- **Site symmetry** — the subgroup of the point group that
  leaves the site invariant.  E.g. in $Pm\bar 3 m$ the 1a
  Wyckoff position has site symmetry $m\bar 3 m$ (the full
  cubic point group), the 3c position has site symmetry
  $4/mm.m$, the 6e position has site symmetry $4m.m$, and so
  on.

The general rule is **multiplicity $\times$ site-symmetry order
= space-group order**.  E.g. in $Pm\bar 3 m$ (order 48), the
1a site has full cubic symmetry (order 48) and multiplicity
$48 / 48 = 1$; the 3c site has site-symmetry order 16
($4/mm.m$) and multiplicity $48 / 16 = 3$.

### 4.2 Worked example: the diamond structure in $Fd\bar 3 m$

The diamond structure (Si, Ge, C) has space group $F d \bar 3 m$
(No. 227).  The conventional cell has 8 atoms; the Wyckoff
positions are:

| Letter | Multiplicity | Site symmetry | Coordinates |
|:--|:-:|:--|:--|
| 8a | 8 | $\bar 4 3 m$ ($T_d$, order 24) | $(0, 0, 0), (1/4, 1/4, 1/4) + \text{FCC}$ |
| 8b | 8 | $\bar 4 3 m$ ($T_d$, order 24) | $(1/2, 1/2, 1/2), (3/4, 3/4, 3/4) + \text{FCC}$ |
| 16c | 16 | $\bar 3 m$ ($D_{3d}$) | All $(x, x, x)$ with $x$ free, plus FCC |
| 16d | 16 | $\bar 3 m$ ($D_{3d}$) | All $(5/8, 1/8, 7/8)$-like, plus FCC |
| 32e | 32 | $3 m$ ($C_{3v}$) | $(x, x, x)$, $x \ne 0$ |
| 48f | 48 | $2/m$ ($C_{2h}$) | $(x, 1/8, 1/8)$ |

The 8a position places the two atoms of the basis at
$(0, 0, 0)$ and $(1/4, 1/4, 1/4)$ plus the FCC translations.
The 8b position is the **other** tetrahedral site of the FCC
lattice — the one that gives the *antifluorite* structure when
occupied by a different species.  Si and Ge sit on 8a; in
zincblende (GaAs) the Ga is on 8a and the As is on 8b.

The **site-symmetry consistency chec`k*`* for the 8a position:
multiplicity $\times$ site-symmetry order = $8 \times 24 = 192$,
which is the order of the space group $F d \bar 3 m$ (a
non-symmorphic group with coset representatives beyond the
point group).  The check passes. ✓

> **Reading the BCS / ITC entry.**  On the Bilbao
> Crystallographic Server, the Wyckoff positions of $F d \bar 3
> m$ are listed under "Wyckoff positions" with three columns
> (multiplicity, letter, site symmetry) and a fourth column of
> representative coordinates.  The 8a position has 2
> representative lines — $(0, 0, 0)$ and $(1/4, 1/4, 1/4)$ —
> the FCC translations being implicit.

---

## 5. Bravais lattice parameter tables

The full 14-Bravais-lattice table with conventional cell
parameters, number of lattice points per conventional cell, and
Pearson symbol.

| # | Bravais lattice | Pearson symbol | Crystal system | Conventional cell | Lattice points per conv. cell |
|:-:|:--|:--|:--|:--|:-:|
| 1 | Triclinic $P$ | $aP$ | Triclinic | $a \ne b \ne c$, $\alpha \ne \beta \ne \gamma \ne 90°$ | 1 |
| 2 | Monoclinic $P$ | $mP$ | Monoclinic | $a \ne b \ne c$, $\alpha = \gamma = 90°$, $\beta \ne 90°$ | 1 |
| 3 | Monoclinic $C$ (or $S$ in Pearson) | $mS$ | Monoclinic | $a \ne b \ne c$, $\alpha = \gamma = 90°$, $\beta \ne 90°$ | 2 |
| 4 | Orthorhombic $P$ | $oP$ | Orthorhombic | $a \ne b \ne c$, $\alpha = \beta = \gamma = 90°$ | 1 |
| 5 | Orthorhombic $C$ (base-centred) | $oS$ | Orthorhombic | $a \ne b \ne c$, $\alpha = \beta = \gamma = 90°$ | 2 |
| 6 | Orthorhombic $I$ (body-centred) | $oI$ | Orthorhombic | $a \ne b \ne c$, $\alpha = \beta = \gamma = 90°$ | 2 |
| 7 | Orthorhombic $F$ (face-centred) | $oF$ | Orthorhombic | $a \ne b \ne c$, $\alpha = \beta = \gamma = 90°$ | 4 |
| 8 | Tetragonal $P$ | $tP$ | Tetragonal | $a = b \ne c$, $\alpha = \beta = \gamma = 90°$ | 1 |
| 9 | Tetragonal $I$ | $tI$ | Tetragonal | $a = b \ne c$, $\alpha = \beta = \gamma = 90°$ | 2 |
| 10 | Hexagonal $P$ | $hP$ | Hexagonal | $a = b \ne c$, $\alpha = \beta = 90°$, $\gamma = 120°$ | 1 |
| 11 | Rhombohedral $R$ | $hR$ | Trigonal | $a = b = c$, $\alpha = \beta = \gamma \ne 90°$ (rhomb. axes) | 3 (per rhomb cell) |
| 12 | Cubic $P$ | $cP$ | Cubic | $a = b = c$, $\alpha = \beta = \gamma = 90°$ | 1 |
| 13 | Cubic $I$ (body-centred, BCC) | $cI$ | Cubic | $a = b = c$, $\alpha = \beta = \gamma = 90°$ | 2 |
| 14 | Cubic $F$ (face-centred, FCC) | $cF$ | Cubic | $a = b = c$, $\alpha = \beta = \gamma = 90°$ | 4 |

> **Trigonal vs hexagonal rhombohedral setting.**  The
> rhombohedral lattice can be described with *rhombohedral
> axes* (one rhombohedral cell, 3 lattice points) or with
> *hexagonal axes* (three times larger hexagonal cell, 1
> lattice point per hexagonal cell).  Both descriptions refer
> to the same lattice.  The hexagonal setting is what
> `spglib` and most DFT codes use; the rhombohedral setting is
> what older textbooks use.

---

## 6. Reciprocal lattice and Brillouin zones

The **first Brillouin zone** (1st BZ) is the **Wigner–Seitz
cell of the reciprocal lattice** — the set of points in
reciprocal space that are closer to the origin than to any
other reciprocal-lattice point.  Equation (7.16) of chapter 07
gives the formal definition:

\begin{equation}
\label{eq:cryst-bz}
\text{1st BZ} \;=\; \Bigl\lbrace \mathbf k \in \mathbb R^3 \;:\;
   |\mathbf k| \le |\mathbf k - \mathbf G| \text{ for every }
   \mathbf G \in \text{reciprocal lattice} \Bigr\rbrace .
\end{equation}

The boundary of the 1st BZ is built from the perpendicular
bisector planes of the **shortest** reciprocal-lattice vectors
$\mathbf G$.  The **higher-order** BZs are the 2nd, 3rd, …
shells: the 2nd BZ is the set of points closer to *one*
non-origin reciprocal lattice point than to any other, and so on.

### 6.1 Construction algorithm

The construction of the 1st BZ in 3-D is straightforward:

1. Generate the list of all $\mathbf G$ vectors with
   $|\mathbf G|$ less than some cutoff (typically
   $3 \times |\mathbf b_1|$ for the first few shells).
2. For each $\mathbf G$, compute the perpendicular bisector
   plane: $\{\mathbf k : \mathbf k \cdot \hat{\mathbf G} = |\mathbf G|/2\}$.
3. The 1st BZ is the intersection of all half-spaces
   $\{\mathbf k : \mathbf k \cdot \hat{\mathbf G} \le |\mathbf G|/2\}$.
4. Find the vertices of the polyhedron by intersecting
   triples of bisector planes; classify them by the number of
   bisecting planes they lie on (4 = vertex where 4 planes
   meet, etc.).
5. The high-symmetry points are those vertices that are
   invariant under the largest subgroup of the point group.

In practice, this algorithm is implemented in `spglib` and
`seekpath`.  For the 7 lattice types, the resulting polyhedra
are well-known and tabulated below.

### 6.2 BZ for the simple cubic (SC) lattice

The SC direct lattice has reciprocal lattice $\mathbf b_i = (2\pi/a) \hat{\mathbf e}_i$.
The shortest $\mathbf G$ are $\pm (2\pi/a)\hat{\mathbf e}_i$, so
the 1st BZ is a **cube** of side $2\pi/a$, centred at the origin.
The high-symmetry points are:

| Label | Cartesian (in $2\pi/a$) | Description |
|:--|:--|:--|
| $\Gamma$ | $(0, 0, 0)$ | Centre of the BZ |
| $X$ | $(1/2, 0, 0)$ | Centre of a square face |
| $M$ | $(1/2, 1/2, 0)$ | Centre of an edge |
| $R$ | $(1/2, 1/2, 1/2)$ | Corner of the cube |

The standard k-path is $\Gamma \to X \to M \to \Gamma \to R \to X | M \to R$
(see §7).

### 6.3 BZ for the BCC lattice

The BCC direct lattice has reciprocal FCC lattice (§1.5 above).
The shortest $\mathbf G$ vectors are
$\pm (2\pi/a)(1, 1, 1)$ — 8 in total.  The 1st BZ is a
**truncated octahedron** (a regular octahedron with the six
vertices cut off), with 14 faces:

- 6 square faces centred at $\pm (2\pi/a)(1, 0, 0)$ and
  permutations (perpendicular bisectors of
  $\pm (4\pi/a)(1, 0, 0)$, etc.)
- 8 hexagonal faces centred at $\pm (\pi/a)(1, 1, 1)$ and
  permutations.

The high-symmetry points are:

| Label | Cartesian (in $2\pi/a$) | Multiplicity | Description |
|:--|:--|:-:|:--|
| $\Gamma$ | $(0, 0, 0)$ | 1 | Centre of the BZ |
| $H$ | $(1, 0, 0)$ | 6 | Vertex: 2 hexagons + 1 square meet |
| $N$ | $(1/2, 1/2, 0)$ | 12 | Centre of a square face |
| $P$ | $(1/4, 1/4, 1/4)$ | 8 | Centre of a hexagonal face |

The standard k-path is $\Gamma \to H \to N \to \Gamma \to P \to H$
(see §7).

### 6.4 BZ for the FCC lattice

The FCC direct lattice has reciprocal BCC lattice (§1.5).
The shortest $\mathbf G$ are $\pm (2\pi/a)(1, 1, 1)$ etc., so
the 1st BZ is also a truncated octahedron — but the *labels* of
the high-symmetry points differ from the BCC case.  See
[chapter 07 §7.4.3]({{ "/dft-notes/chapter-07/" | relative_url }})
for the full table:

| Label | Cartesian (in $2\pi/a$) | Multiplicity | Description |
|:--|:--|:-:|:--|
| $\Gamma$ | $(0, 0, 0)$ | 1 | Centre of the BZ |
| $X$ | $(1, 0, 0)$ | 6 | Centre of a square face |
| $L$ | $(1/2, 1/2, 1/2)$ | 8 | Centre of a hexagonal face |
| $W$ | $(1, 1/2, 0)$ | 24 | Vertex: 2 hexagons + 1 square meet |
| $K$ | $(3/4, 3/4, 0)$ | 24 | Midpoint of a hex–hex edge |
| $U$ | $(5/8, 1/4, 5/8)$ | 24 | Midpoint of an $L$–$W$ edge |

The standard k-path is
$\Gamma \to X \to W \to K \to \Gamma \to L \to U \to W \to L \to K$
(see §7).

### 6.5 BZ for the hexagonal lattice

The hexagonal lattice with $a = b \ne c$, $\gamma = 120°$ has
the reciprocal hexagonal lattice in the basal plane.  The
primitive reciprocal vectors are

\begin{equation}
\label{eq:cryst-hex-recip}
\mathbf b_1 = \frac{2\pi}{a} \left(1, -\frac{1}{\sqrt 3}, 0\right), \quad
\mathbf b_2 = \frac{2\pi}{a} \left(0, \frac{2}{\sqrt 3}, 0\right), \quad
\mathbf b_3 = \frac{2\pi}{c} (0, 0, 1) .
\end{equation}

The 1st BZ is a **regular hexagonal prism** with hexagonal
faces at $k_z = \pm \pi/c$ and rectangular side faces.  The
high-symmetry points:

| Label | Cartesian | Description |
|:--|:--|:--|
| $\Gamma$ | $(0, 0, 0)$ | Centre of the BZ |
| $M$ | $(\pi/a, 0, 0) \cdot (1, 0, 0)$ in $(2\pi/a, 2\pi/a, 2\pi/c)$ | Centre of a hexagonal face |
| $K$ | $(2\pi/3a, 2\pi/3a, 0) = (1/3, 1/3, 0) \cdot (2\pi/a, 2\pi/a, 2\pi/c)$ | Hex–hex edge midpoint; the Dirac point of graphene |
| $A$ | $(0, 0, \pi/c) = (0, 0, 1/2)$ | Top of the BZ |
| $L$ | $(\pi/a, 0, \pi/c) = (1/2, 0, 1/2)$ | Centre of a side face |
| $H$ | $(2\pi/3a, 2\pi/3a, \pi/c) = (1/3, 1/3, 1/2)$ | Edge midpoint on the top face |

> **Why $K$ is special in graphene.**  The point $K$ is a
> *corner* of the hexagonal BZ (not a centre) and is the point
> where the two inequivalent Dirac cones of graphene sit.  See
> [chapter 11 §11.9]({{ "/dft-notes/chapter-11/" | relative_url }})
> for the tight-binding model that produces the linear
> dispersion at $K$.

---

## 7. High-symmetry k-paths for common lattices

The 1-D k-path used to plot a band structure is a *chain of
straight segments* joining the high-symmetry points.  The path
must visit every symmetry-inequivalent point in the IBZ at
least once; longer paths are more complete but harder to read.
The four "canonical" paths below are the ones used by the
Materials Project, AFLOW, the BoltzTraP code, and every modern
VASP/QE tutorial.

### 7.1 Simple cubic (SC)

The SC lattice has a **cubi`c*`* 1st BZ of side $2\pi/a$.  The
high-symmetry points are $\Gamma$ (centre, $0, 0, 0$), $X$
(face centre, $1/2, 0, 0$), $M$ (edge centre, $1/2, 1/2, 0$),
and $R$ (corner, $1/2, 1/2, 1/2$) — all coordinates in $2\pi/a$
units.  The standard k-path visits the four points in the order
$\Gamma \to X \to M \to \Gamma \to R \to X$ plus the closing
segment $M \to R$ on the back face.  The shorthand is

$$
\Gamma \;\to\; X \;\to\; M \;\to\; \Gamma \;\to\; R \;\to\; X \;\vert\; M \;\to\; R .
$$

The SC lattice is rarely encountered in real materials (CsCl is
the most common example, and it is *BCC* in the reciprocal
lattice); the SC path is shown in many textbooks as a pedagogic
introduction because the BZ is a cube and the path is
self-evident.

### 7.2 Body-centred cubic (BCC)

The standard BCC path covers the 4 high-symmetry points of the
BCC BZ.  The high-symmetry points and the segment sequence are
given in the table below.  Note the symmetry: $\Gamma \to H$
has the same length as $H \to N \to \Gamma$, and $\Gamma \to P$
is the shortest of the five segments.

| Segment | From $\to$ To | Cartesian (in $2\pi/a$) | Length (in $2\pi/a$) |
|:--|:--|:--|:-:|
| 1 | $\Gamma \to H$ | $(0,0,0) \to (1, 0, 0)$ | 1.000 |
| 2 | $H \to N$ | $(1, 0, 0) \to (1/2, 1/2, 0)$ | $\sqrt{2}/2 \approx 0.707$ |
| 3 | $N \to \Gamma$ | $(1/2, 1/2, 0) \to (0, 0, 0)$ | $\sqrt{2}/2 \approx 0.707$ |
| 4 | $\Gamma \to P$ | $(0, 0, 0) \to (1/4, 1/4, 1/4)$ | $\sqrt{3}/4 \approx 0.433$ |
| 5 | $P \to H$ | $(1/4, 1/4, 1/4) \to (1, 0, 0)$ | $\sqrt{21}/4 \approx 1.146$ |

The path in shorthand is
$\Gamma \to H \to N \to \Gamma \to P \to H | N \to P$.
Total length: $\approx 3.99$ in units of $2\pi/a$.  BCC metals
(alkali metals, α-Fe, W, Mo, Cr) are usually plotted along this
path.

### 7.3 Face-centred cubic (FCC)

The standard FCC path (Setyawan–Curtarolo) has 10 segments and
6 high-symmetry points.  The shorter, older convention is
$\Gamma \to X \to W \to K \to \Gamma \to L \to W \to X$
(7 segments); the modern, longer convention is
$\Gamma \to X \to W \to K \to \Gamma \to L \to U \to W \to L \to K$
(9 segments after the closing loop).  We follow the modern
convention here, as it is what VASP, Quantum ESPRESSO, and the
Materials Project use.

| Segment | From $\to$ To | Cartesian (in $2\pi/a$) | Length (in $2\pi/a$) |
|:--|:--|:--|:-:|
| 1 | $\Gamma \to X$ | $(0,0,0) \to (1, 0, 0)$ | 1.000 |
| 2 | $X \to W$ | $(1, 0, 0) \to (1, 1/2, 0)$ | 0.500 |
| 3 | $W \to K$ | $(1, 1/2, 0) \to (3/4, 3/4, 0)$ | $\sqrt{2}/4 \approx 0.354$ |
| 4 | $K \to \Gamma$ | $(3/4, 3/4, 0) \to (0, 0, 0)$ | $3\sqrt{2}/4 \approx 1.061$ |
| 5 | $\Gamma \to L$ | $(0, 0, 0) \to (1/2, 1/2, 1/2)$ | $\sqrt{3}/2 \approx 0.866$ |
| 6 | $L \to U$ | $(1/2, 1/2, 1/2) \to (5/8, 1/4, 5/8)$ | $\sqrt{(1/8)^2 + (1/4)^2 + (1/8)^2} \approx 0.306$ |
| 7 | $U \to W$ | $(5/8, 1/4, 5/8) \to (1, 1/2, 0)$ | $\sqrt{(3/8)^2 + (1/4)^2 + (5/8)^2} \approx 0.756$ |
| 8 | $W \to L$ | $(1, 1/2, 0) \to (1/2, 1/2, 1/2)$ | $\sqrt{1/2} \approx 0.707$ |
| 9 | $L \to K$ | $(1/2, 1/2, 1/2) \to (3/4, 3/4, 0)$ | $\sqrt{(1/4)^2 + (1/4)^2 + (1/2)^2} \approx 0.612$ |

Total path length: $\approx 5.16$ in units of $2\pi/a$.

> **Warning — the $U$ point.**  The Setyawan–Curtarolo
> convention places $U$ at $(5/8, 1/4, 5/8)$.  Older textbooks
> (Kittel, Ashcroft & Mermin) place $U$ at $(3/4, 1/2, 1/4)$,
> which is a *different* point — the midpoint of a hex–square
> edge.  When comparing band-structure plots from different
> references, always check which convention is used.  See
> [chapter 11 §11.2.2]({{ "/dft-notes/chapter-11/" | relative_url }})
> for the explicit warning.

### 7.4 Hexagonal (HEX)

The standard hexagonal path visits the 6 high-symmetry points
of §6.5 in two halves.  The first half
($\Gamma \to M \to K \to \Gamma$) lives in the basal plane
$k_z = 0$ and is the path used for 2-D materials such as
graphene.  The second half
($\Gamma \to A \to L \to H \to A$) samples the $k_z$
dispersion.  Three closing segments ($L \to M$, $K \to H$)
connect the top of the BZ back to the basal plane.  The
shorthand is

$$
\Gamma \;\to\; M \;\to\; K \;\to\; \Gamma \;\to\; A \;\to\; L \;\to\; H \;\to\; A \;\vert\; L \;\to\; M \;\vert\; K \;\to\; H .
$$

For 2-D materials, drop the second half: the path reduces to
$\Gamma \to M \to K \to \Gamma$, the canonical graphene path of
[chapter 11 §11.9]({{ "/dft-notes/chapter-11/" | relative_url }}).

> **The K point is doubly counted.**  In the path above, the
> segment $K \to \Gamma$ is on the basal plane and the segment
> $K \to H$ is between the basal plane and the top face.  The
> point $K$ therefore appears *twice* in the path.  This is
> correct — the basal-plane $K$ and the top-face $H$ are
> *different* points in the 3-D BZ, even though they share the
> $k_z$-component when projected to the basal plane.

### 7.5 Summary of the four canonical k-paths

| Lattice | Path (Setyawan–Curtarolo) | Points | Segments |
|:--|:--|:-:|:-:|
| SC | $\Gamma \to X \to M \to \Gamma \to R \to X \vert M \to R$ | 4 | 6 |
| BCC | $\Gamma \to H \to N \to \Gamma \to P \to H \vert N \to P$ | 4 | 6 |
| FCC | $\Gamma \to X \to W \to K \to \Gamma \to L \to U \to W \to L \to K$ | 6 | 9 |
| HEX | $\Gamma \to M \to K \to \Gamma \to A \to L \to H \to A \vert L \to M \vert K \to H$ | 6 | 9 |

For the hexagonal path the exact total length depends on the
$c/a$ ratio; the segments in the $k_z$ direction scale with
$a/c$.

### 7.6 Code output for the FCC k-path

`pymatgen` (the standard Python materials science library) will
print the Setyawan–Curtarolo k-path for an FCC material as:

```python
from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath

s = Structure.from_file("POSCAR")
kpath = HighSymmKpath(s)
path = kpath.kpath["kpoints"]  # dict: label -> coord (fractional)
print(path)
# {'Gamma': [0, 0, 0], 'X': [0.5, 0, 0.5], 'L': [0.5, 0.5, 0.5], ...}
print(kpath.kpath["path"])
# [['Gamma', 'X', 'W', 'K', 'Gamma', 'L', 'U', 'W', 'L', 'K']]
```

The `HighSymmKpath` class is the canonical way to get a
Setyawan–Curtarolo k-path for any crystal structure.  The path
returned is the modern (long) convention, and the k-point
coordinates are *fractional* in the reciprocal basis
$\mathbf b_1, \mathbf b_2, \mathbf b_3$.

---

## 8. Working with space groups in DFT codes

The four most common DFT codes — VASP, Quantum ESPRESSO,
CASTEP, and SIESTA — accept the space group in different ways.
VASP uses the symmetry operations in the `POSCAR`/`CONTCAR`
itself; QE uses `space_group` in the `&SYSTEM` namelist; CASTEP
uses `.cell` keyword; SIESTA uses a separate Z-matrix file.
The **CIF file** is the universal interchange format and the
recommended starting point for any new crystal.

### 8.1 The CIF (Crystallographic Information File) format

A **CIF** file is a plain-text file with a fixed structure:
data are organised in `data_block`s, with each datum a
`key value` pair (text or numeric).  The standard fields for a
crystal structure are:

```cif
data_Cu
_chemical_name_common              "Copper"
_chemical_formula_structural       "Cu"
_cell_length_a                     3.6149
_cell_length_b                     3.6149
_cell_length_c                     3.6149
_cell_angle_alpha                  90
_cell_angle_beta                   90
_cell_angle_gamma                  90
_cell_volume                       47.246
_space_group_name_H-M_alt          "F m -3 m"
_space_group_IT_number             225
loop_
_space_group_symop_operation_xyz
'x, y, z'
'-x, -y, z'
'-x, y, -z'
'x, -y, -z'
'z, x, y'
'-z, -x, y'
... (48 operations in total for Fm-3m)
loop_
_atom_site_label
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Cu1  0.0  0.0  0.0  1.0
```

The key fields:

- `_cell_length_*` and `_cell_angle_*` — the conventional
  cell parameters $(a, b, c)$ in Å and $(\alpha, \beta, \gamma)$
  in degrees.
- `_space_group_name_H-M_alt` — the Hermann–Mauguin symbol.
- `_space_group_IT_number` — the IUC space-group number
  (1–230).
- `_space_group_symop_operation_xyz` — the 48 (or however
  many) symmetry operations in `(x, y, z)` shorthand.  The
  first operation is always the identity; the others are the
  coset representatives.
- `_atom_site_*` — the atomic positions in fractional
  coordinates of the conventional cell.

The CIF standard is maintained by the IUCr (International
Union of Crystallography) and documented in
*International Tables for Crystallography* vol. G.

### 8.2 VASP

VASP reads the structure from `POSCAR`.  Symmetry is detected
from the atomic positions; the user does not need to specify
the space group explicitly.  The relevant `INCAR` tags are:

| Tag | Default | Meaning |
|:--|:-:|:--|
| `ISYM` | 2 | Symmetry: 0 = off, 1 = use operations, 2 = use operations + break when $E$ stops decreasing |
| `SYMPREC` | 1e-5 | Tolerance for symmetry detection (Å) |
| `LWAVE` | .FALSE. | Write `WAVECAR` |
| `LCHARG` | .FALSE. | Write `CHGCAR` |
| `IBRION` | — | Optimisation algorithm |

For a non-symmorphic space group with a glide plane, VASP
detects the glide automatically; the symmetry-derived k-point
reduction (`KPOINTS` with `Auto` mesh) respects the glide.

> **Tip.**  If you have a CIF file, use `pymatgen` or `ase` to
> convert it to a POSCAR:
> `Structure.from_file("Cu.cif").to("POSCAR", "POSCAR")`.

### 8.3 Quantum ESPRESSO

QE uses the `&SYSTEM` namelist in the input file:

```fortran
&SYSTEM
  ibrav = 2                  ! FCC
  celldm(1) = 7.65           ! a in Bohr (= 4.05 Å / 0.529)
  nat = 1
  ntyp = 1
  space_group = 225          ! Fm-3m
/
```

The `ibrav` codes are QE-internal shortcuts for the 14 Bravais
lattices.  When `space_group` is given, QE uses the symmetry
operations from the *International Tables* for k-point
reduction and Hamiltonian symmetrisation.  This is more
reliable than letting QE *guess* the symmetry from the atomic
positions.

### 8.4 CASTEP

CASTEP uses a `.cell` file:

```text
%BLOCK LATTICE_CART
   3.6149 0.0    0.0
   0.0    3.6149 0.0
   0.0    0.0    3.6149
%ENDBLOCK LATTICE_CART
%BLOCK POSITIONS_FRAC
   Cu  0.0 0.0 0.0
%ENDBLOCK POSITIONS_FRAC
SYMMETRY_GENERATE
SNAP_TO_SYMMETRY
```

The `SYMMETRY_GENERATE` keyword asks CASTEP to find the space
group from the structure; `SNAP_TO_SYMMETRY` rounds the atomic
positions to the nearest high-symmetry site.

### 8.5 SIESTA

SIESTA reads the structure from a `.fdf` file:

```text
LatticeConstant  1.0  Ang
%block LatticeVectors
   3.6149 0.0    0.0
   0.0    3.6149 0.0
   0.0    0.0    3.6149
%endblock LatticeVectors
%block AtomicCoordinatesAndAtomicSpecies
   0.0  0.0  0.0  1
%endblock AtomicCoordinatesAndAtomicSpecies
```

SIESTA does not have explicit space-group support; symmetry is
detected by the `SIESTA`-internal module or by an external tool
such as `spglib`.

### 8.6 The Bilbao Crystallographic Server (BCS)

The
[Bilbao Crystallographic Server](<https://www.cryst.ehu.es/>)
(BCS) is the de-facto web reference for space-group analysis.
It hosts a dozen tools; the most useful for DFT work are:

| Tool | URL | Use |
|:--|:--|:--|
| GENPOS | `genpos` | Generate the general-position list of a space group |
| WYCKPOS | `wpos` | List Wyckoff positions with coordinates |
| SUBGROUPGRAPH | `subgroupgraph` | Find maximal subgroups (Bärnighausen tree) |
| HKLCOND | `hklcond` | Check reflection conditions for a space group |
| IDENTIFY | `ident` | Identify a space group from a list of symmetry operations |
| PSEUDO | `pseudo` | Bilbao-adopted pseudopotential database |
| NCSYM | `ncsym` | Magnetic space groups (Shubnikov groups) |

The BCS also hosts the **Bilbao Crystallographic Dat`a*`* for
each space group: the full Wyckoff-position list with site
symmetries, the maximal and minimal non-isomorphic
subgroups, and the Brillouin-zone data.

### 8.7 Worked example: building $\alpha$-quartz (SiO₂) from scratch

$\alpha$-quartz is a low-temperature polymorph of SiO₂ with
space group $P 3_1 2 1$ (No. 152, Schoenflies $D_3^4$) and
three formula units per unit cell.  Here is how to build it
from a CIF file and a `pymatgen` script that emits a VASP
`POSCAR`.

**Step 1. The CIF file.**

```cif
data_alpha_quartz
_chemical_name_common             "alpha-quartz"
_chemical_formula_structural      "SiO2"
_cell_length_a                    4.9134
_cell_length_b                    4.9134
_cell_length_c                    5.4052
_cell_angle_alpha                 90
_cell_angle_beta                  90
_cell_angle_gamma                 120
_space_group_name_H-M_alt         "P 31 21"
_space_group_IT_number            152
loop_
_atom_site_label
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Si1  0.4697  0.0000  0.0000
Si2  0.0000  0.4697  0.6667
Si3  0.5303  0.5303  0.3333
O1   0.4133  0.2672  0.1187
O2   0.2672  0.4133  0.5479
O3   0.7328  0.1461  0.4521
O4   0.5867  0.8539  0.2146
O5   0.1461  0.7328  0.8813
O6   0.8539  0.5867  0.7854
```

**Step 2. The `pymatgen` script that converts to POSCAR.**

```python
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

s = Structure.from_file("alpha_quartz.cif")
spg = SpacegroupAnalyzer(s, symprec=1e-3)
print("Space group:", spg.get_space_group_symbol())   # -> "P 31 21"
print("Number:     ", spg.get_space_group_number())   # -> 152
s_sym = spg.get_symmetrized_structure()
s_sym.to(fmt="poscar", filename="POSCAR")
```

**Step 3. The VASP input files.**

```text
# INCAR (geometry optimisation)
SYSTEM = alpha-quartz
ENCUT  = 520
EDIFF  = 1e-5
IBRION = 2
ISIF   = 3
ISYM   = 2
NSW    = 30
EDIFFG = -0.02
```

```text
# KPOINTS (Auto mesh, 6x6x6 for a hexagonal cell)
Auto
0
Gamma
6 6 6
0 0 0
```

The key `ISYM = 2` lets VASP detect the $P 3_1 2 1$ symmetry
from the POSCAR and use it for k-point reduction and
Hamiltonian symmetrisation.  The point group of $P 3_1 2 1$ is
$D_3$ (order 6), so the speedup from symmetry is modest
($\sim 6 \times$) but the band-structure plot along the
hexagonal k-path (§7.4) is well-defined.

> **Reading note.**  The point group of $\alpha$-quartz is
> $D_3$, *not* the more symmetric $D_{3d}$ of $\beta$-quartz
> (the high-temperature polymorph, space group $P 3_2 21$, No.
> 154).  The two structures differ in their screw sense: $P
> 3_1 21$ has a right-handed screw, $P 3_2 21$ a left-handed
> screw.  Enantiomorphic pairs of this kind are common in
> chiral minerals.

---

## 9. The Pearson symbol cheat sheet

The **Pearson symbol** is a two-character code for a Bravais
lattice.  It is used in crystallographic databases (CRYSTMET,
ICSD, Pearson's Handbook) and in the materials science
literature to identify a structure type.

### 9.1 Structure

A Pearson symbol has the form `XY` where:

- `X` is a **lowercase** letter denoting the crystal system
  (see §1.1).
- `Y` is an **uppercase** letter denoting the centring
  (see §1.2).

The two letters together identify the Bravais lattice.
Combined with the number of atoms per cell, a Pearson symbol
becomes a structure-type identifier: e.g. `cF8` is the
diamond structure (FCC, 8 atoms per conventional cell).

### 9.2 The 23 Pearson symbols

There are **23** Pearson symbols in common use.  The reason
there are 23 and not 14 (the number of Bravais lattices) is
that some authors extend the convention to include the lattice
*centring* of the reciprocal lattice or the lattice system
in a non-standard way.  The 14 standard Pearson symbols are in
the table below; the 9 extras ($aS$, $mI$, $oA$, $oB$, $oC$,
$tS$, $hS$, $cS$, and one more historical variant) are
alternate names for one of the 14 and are encountered only in
older references.

### 9.3 The "atoms per cell" extension

The Pearson symbol is sometimes extended with a third
character, the number of atoms in the conventional cell:

| Structure | Atoms per cell | Extended Pearson |
|:--|:-:|:--|
| Diamond (Si, Ge, C) | 8 | $cF8$ |
| FCC Cu, Al | 4 | $cF4$ |
| BCC Fe, W, Na | 2 | $cI2$ |
| HCP Mg, Ti | 2 | $hP2$ |
| Rocksalt NaCl | 8 | $cF8$ |
| CsCl | 2 | $cP2$ |
| Zincblende ZnS | 8 | $cF8$ |
| Perovskite CaTiO₃ | 5 | $cP5$ |
| Graphite (hex.) | 4 | $hP4$ |

Note that diamond, rocksalt, and zincblende all have the
*same* extended Pearson symbol `cF8` (8 atoms per conventional
FCC cell) — what distinguishes them is the space group
($Fd\bar 3 m$, $Fm\bar 3 m$, $F\bar 4 3m$ respectively) and
the species on each Wyckoff position.

### 9.4 Worked example: identifying a material from its Pearson symbol

> A material in the ICSD has Pearson symbol `oF8` and is
> reported to be an intercalation compound.  What crystal
> system, Bravais lattice, and conventional cell does it have?

`oF8` is the structure of $\beta$-NaFeO₂ — a layered
intercalation compound used as a positive electrode in
Na-ion batteries.  The breakdown:

- `o` = orthorhombic ($a \ne b \ne c$, $\alpha = \beta =
  \gamma = 90°$).
- `F` = face-centred (4 lattice points per conventional cell).
- `8` = 8 atoms per conventional cell, so 8/4 = 2 atoms per
  primitive cell.

The full structural description is in space group
$P n a 2_1$ (No. 33) or $P n m a$ (No. 62) — depending on
the specific chemistry.  The ICSD entry will list the space
group explicitly; the Pearson symbol alone is a *family*
identifier, not a *structure* identifier.

> **Pearson symbol as a structure-type identifier.**  The
> 1-to-1 mapping is *not* a structure-type identifier.  Two
> materials can share a Pearson symbol but have different
> space groups (e.g. $cF8$ for diamond, rocksalt, and
> zincblende).  Use the Pearson symbol as a quick filter; use
> the full space group + Wyckoff positions for a complete
> structure description.

---

## 10. Hermann–Mauguin and Schoenflies side-by-side

The two notations are not in 1-to-1 correspondence.  The
Schoenflies symbols depend on the *rotational* subgroup (the
"axial" part) and use letter+number, while the HM symbols
depend on the full point group and use number+letter+number.
Some groups have the same Schoenflies symbol across crystal
systems (e.g. $C_{2h}$ is the point group of *bot`h*` the
monoclinic $P 2_1/c$ and the orthorhombic $P n m a$); the HM
symbol distinguishes them.

### 10.1 Why both exist

**Schoenflies** is preferred in:

- Spectroscopy (IR, Raman, polarisation selection rules).
- Molecular quantum chemistry (point group of a single
  molecule).
- Group theory of finite groups (the Schoenflies notation
  emphasises the abstract group structure: $C_n$ cyclic, $D_n$
  dihedral, $T$ tetrahedral, $O$ octahedral, $I$ icosahedral).

**Hermann–Mauguin** is preferred in:

- Crystallography (the *International Tables*, every
  database, the BCS).
- Solid-state physics and DFT (every modern code).
- Materials science (the Pearson Handbook uses HM).

When in doubt, use HM.  When reading a spectroscopy paper, you
will encounter Schoenflies.

### 10.2 Complete mapping table (32 point groups)

This is the side-by-side reference.  The 32 point groups are
listed in crystal-system order (Triclinic $\to$ Cubic) so that
related groups are adjacent.

| # | HM (full) | Schoenflies | Order | Crystal system | Common space group example |
|:-:|:--|:--|:-:|:--|:--|
| 1 | $1$ | $C_1$ | 1 | Triclinic | $P 1$ (No. 1) |
| 2 | $\bar 1$ | $C_i$ (= $S_2$) | 2 | Triclinic | $P \bar 1$ (No. 2) |
| 3 | $2$ | $C_2$ | 2 | Monoclinic | $P 2$ (No. 3) |
| 4 | $m$ | $C_s$ (= $C_{1h}$) | 2 | Monoclinic | $P m$ (No. 6) |
| 5 | $2/m$ | $C_{2h}$ | 4 | Monoclinic | $P 2/m$ (No. 10) |
| 6 | $222$ | $D_2$ (= $V$) | 4 | Orthorhombic | $P 222$ (No. 16) |
| 7 | $mm2$ | $C_{2v}$ | 4 | Orthorhombic | $P mm2$ (No. 25) |
| 8 | $mmm$ | $D_{2h}$ (= $V_h$) | 8 | Orthorhombic | $P m m m$ (No. 47) |
| 9 | $4$ | $C_4$ | 4 | Tetragonal | $P 4$ (No. 75) |
| 10 | $\bar 4$ | $S_4$ | 4 | Tetragonal | $P \bar 4$ (No. 81) |
| 11 | $4/m$ | $C_{4h}$ | 4 | Tetragonal | $P 4/m$ (No. 83) |
| 12 | $422$ | $D_4$ | 8 | Tetragonal | $P 422$ (No. 89) |
| 13 | $4mm$ | $C_{4v}$ | 8 | Tetragonal | $P 4mm$ (No. 99) |
| 14 | $\bar 4 2m$ | $D_{2d}$ (= $V_d$) | 8 | Tetragonal | $P \bar 4 2m$ (No. 111) |
| 15 | $4/mmm$ | $D_{4h}$ | 16 | Tetragonal | $P 4/m m m$ (No. 123) |
| 16 | $3$ | $C_3$ | 3 | Trigonal | $P 3$ (No. 143) |
| 17 | $\bar 3$ | $C_{3i}$ (= $S_6$) | 6 | Trigonal | $P \bar 3$ (No. 147) |
| 18 | $32$ | $D_3$ | 6 | Trigonal | $P 3 1 2$ (No. 149) |
| 19 | $3m$ | $C_{3v}$ | 6 | Trigonal | $P 3 m 1$ (No. 156) |
| 20 | $\bar 3 m$ | $D_{3d}$ | 12 | Trigonal | $P \bar 3 m 1$ (No. 164) |
| 21 | $6$ | $C_6$ | 6 | Hexagonal | $P 6$ (No. 168) |
| 22 | $\bar 6$ | $C_{3h}$ | 6 | Hexagonal | $P \bar 6$ (No. 174) |
| 23 | $6/m$ | $C_{6h}$ | 6 | Hexagonal | $P 6/m$ (No. 175) |
| 24 | $622$ | $D_6$ | 12 | Hexagonal | $P 6 2 2$ (No. 177) |
| 25 | $6mm$ | $C_{6v}$ | 12 | Hexagonal | $P 6 m m$ (No. 183) |
| 26 | $\bar 6 m2$ | $D_{3h}$ | 12 | Hexagonal | $P \bar 6 m 2$ (No. 187) |
| 27 | $6/mmm$ | $D_{6h}$ | 24 | Hexagonal | $P 6/m m m$ (No. 191) |
| 28 | $23$ | $T$ | 12 | Cubic | $P 23$ (No. 195) |
| 29 | $m\bar 3$ | $T_h$ | 24 | Cubic | $P m \bar 3$ (No. 200) |
| 30 | $432$ | $O$ | 24 | Cubic | $P 432$ (No. 207) |
| 31 | $\bar 4 3m$ | $T_d$ | 24 | Cubic | $P \bar 4 3m$ (No. 215) |
| 32 | $m\bar 3 m$ | $O_h$ | 48 | Cubic | $P m \bar 3 m$ (No. 221) |

> **Sum check.**  Adding up the orders in the third column
> counts the total number of operations: $1 + 2 + 2 + 2 + 4 +
> 4 + 4 + 8 + 4 + 4 + 4 + 8 + 8 + 8 + 16 + 3 + 6 + 6 + 6 +
> 12 + 6 + 6 + 6 + 12 + 12 + 12 + 24 + 12 + 24 + 24 + 24 +
> 48 = 298$.  This is the sum of *distinct* operations across
> the 32 point groups; the *average* is $298/32 \approx 9.3$.
> The 5 cubic point groups alone contribute $12 + 24 + 24 + 24
> + 48 = 132$ of those 298 operations.

### 10.3 The Schoenflies $D$, $C$, $S$, $T$, $O$ prefixes

A short glossary for the Schoenflies letters:

| Letter | Meaning | Examples |
|:--|:--|:--|
| $C_n$ | Cyclic group of order $n$ generated by a $C_n$ rotation | $C_2, C_3, C_4, C_6$ |
| $C_{nh}$ | $C_n$ + horizontal mirror $\sigma_h$ | $C_{2h}, C_{4h}, C_{6h}$ |
| $C_{nv}$ | $C_n$ + $n$ vertical mirrors | $C_{2v}, C_{3v}, C_{4v}, C_{6v}$ |
| $C_s$ | One mirror only ($C_{1h}$) | — |
| $C_i$ | Inversion only ($S_2$) | — |
| $D_n$ | $C_n$ + $n$ perpendicular $C_2$ rotations | $D_2, D_3, D_4, D_6$ |
| $D_{nh}$ | $D_n$ + horizontal mirror | $D_{2h}, D_{3h}, D_{4h}, D_{6h}$ |
| $D_{nd}$ | $D_n$ + diagonal mirrors | $D_{2d}, D_{3d}$ |
| $S_n$ | Improper rotation of order $n$ | $S_4, S_6$ (=$C_{3i}$), $S_2$ (=$C_i$) |
| $T$ | Chiral tetrahedral (12 operations: $E$, $8 C_3$, $3 C_2$) | $T$ |
| $T_h$ | $T$ + inversion (24 operations) | $T_h$ |
| $T_d$ | Full tetrahedral (24 operations: $T$ + $6 S_4$, $6 \sigma_d$) | $T_d$ |
| $O$ | Chiral octahedral (24 operations: $E$, $8 C_3$, $3 C_2$, $6 C_4$, $6 C_2'$) | $O$ |
| $O_h$ | Full octahedral (48 operations: $O$ + $i$, $8 S_6$, $3 \sigma_h$, $6 S_4$, $6 \sigma_d$) | $O_h$ |

The 7 infinite families $C_n, C_{nh}, C_{nv}, D_n, D_{nh}, D_{nd}$
and the 5 cubic groups $T, T_h, T_d, O, O_h$ together generate
the 32 crystallographic point groups when the cyclic orders are
restricted to $n \in \{1, 2, 3, 4, 6\}$ and the cubic groups are
restricted to $T$ and $O$ (the icosahedral group $I$ of order
120 is *not* a 3-D Bravais-lattice symmetry; it is the symmetry
of the icosahedron, the buckyball C₆₀, and quasicrystals).

> **Mapping rule of thumb.**  To convert Schoenflies $\to$ HM:
> - $C_n \to n$ (with horizontal bar if there is inversion,
>   letter `m` for horizontal mirror).
> - $D_n \to n 2 2$ (in cubic) or $n m m$ (with mirrors).
> - $T \to 23$ (cubic, chiral); $T_d \to \bar 4 3m$ (cubic, with mirrors);
>   $O \to 432$; $O_h \to m \bar 3 m$.
> When in doubt, look it up in §10.2 above.

---

## 11. What we left out

This page is a *reference*, not a derivation.  The topics
below are *not* covered here and would each deserve their own
section (or chapter):

- **Magnetic space groups** (Shubnikov groups, 1651 of them).
  The 230 "grey" space groups above are the paramagnetic
  groups; once time-reversal symmetry is broken, the magnetic
  point group can be any of 32 + 32 + 58 = 122 *magneti`c*` point
  groups, and the magnetic space groups number 1651. The BCS
  has a separate `NCSYM` tool for these.
- **Incommensurate structures.**  Modulated structures and
  quasicrystals have no 3-D Bravais lattice; the symmetry is
  described in $(3 + d)$-D superspace.
- **Quasicrystals.**  The 5-fold and icosahedral symmetries of
  quasicrystals are *local* (i.e. on the diffraction pattern)
  but the structure is aperiodic.
- **Subperiodic groups** (layer groups, rod groups, frieze
  groups).  These are the symmetry groups of 2-D and 1-D
  submanifolds of 3-D space; they are useful for surfaces and
  polymers.
- **Higher-dimensional crystallography.**  The 230 space
  groups are the 3-D case; $n$-D generalisations exist and are
  tabulated for $n = 4$ and $n = 5$ (relevant for
  quasicrystal structure solution).
- **Relativistic crystallography.**  Magnetic groups and
  spin-space groups are the relativistic generalisations; the
  spin-space groups number 11994 in 3-D (Litvin 2013).
- **Group theory of space groups.**  The 230 space groups are
  abstractly a small set of isomorphism classes (73 symmorphic
  + 157 non-symmorphic), and their irreps at the high-symmetry
  k-points are tabulated in *International Tables* vol. B.

For the DFT context, the **230 space groups** and their **k-
point conventions** (Setyawan–Curtarolo) are the only ones you
need.  Everything else is on the BCS.

---

## 12. References and further reading

- **International Tables for Crystallography**, vol. A
  (Space-group symmetry), 6th ed., ed. M. I. Aroyo
  (Wiley, 2016).  The canonical reference.  Every library
  with a crystallography section has it.
- M. I. Aroyo, ed., **International Tables for
  Crystallography** vol. E (Subperiodic groups), 2nd ed.
  (Wiley, 2020).  Layer, rod, and frieze groups.
- C. Kittel, **Introduction to Solid State Physics**, 9th ed.
  (Wiley, 2021), chapters 1–2. The classic textbook.  Uses
  the $2\pi$ convention for the reciprocal lattice (§1.3).
- N. W. Ashcroft and N. D. Mermin, **Solid State Physics**
  (Holt, Rinehart, Winston, 1976), chapters 4–7. More
  thorough than Kittel on reciprocal space.
- M. S. Dresselhaus, G. Dresselhaus, and A. Jorio, **Group
  Theory: Application to the Physics of Condensed Matter**
  (Springer, 2008).  The standard reference for space-group
  applications in solid-state physics.
- W. Setyawan and S. Curtarolo, "High-throughput electronic
  band structure calculations: Challenges and tools",
  *Computational Materials Science* **49**, 299 (2010).
  The paper that defined the canonical k-paths of §7. *Every*
  modern band-structure database uses these conventions.
- G. K. H. Madsen and D. J. Singh, "BoltzTraP. A code for
  calculating band-structure dependent quantities",
  *Computer Physics Communications* **175**, 67 (2006).
  The BoltzTraP code uses the Setyawan–Curtarolo conventions.
- The
  [Bilbao Crystallographic Server](<https://www.cryst.ehu.es/>),
  M. I. Aroyo et al.  The de-facto web reference.
- The `spglib` library, H. T. Stokes and D. M. Hatch
  (Brigham Young University).  Python wrapper `pyspglib`.
  The standard tool for symmetry analysis from a CIF or
  POSCAR.
- The `pymatgen` library, S. P. Ong et al. (Materials
  Project).  The standard Python materials-science library;
  uses Setyawan–Curtarolo k-paths as defaults.
- The `ase` library (Atomic Simulation Environment), A. H.
  Larsen et al.  An alternative to `pymatgen`; similar
  capabilities for reading CIF and computing k-paths.
- D. Shechtman, I. Blech, D. Gratias, and J. W. Cahn,
  "Metallic phase with long-range orientational order and no
  translational symmetry", *Physical Review Letters* **53**,
  1951 (1984).  The original quasicrystal paper (5-fold
  symmetry in a metallic solid).

> **Up next in DFT Notes.**  This page is the static
> crystallography reference.  For the *practical* workflow of
> building a structure from a CIF and computing a band
> structure, see
> [chapter 11]({{ "/dft-notes/chapter-11/" | relative_url }}) §11.5
> (the k-path algorithm) and the
> [software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }})
> entries for `pymatgen`, `spglib`, `ASE`, and `BoltzTraP`.
