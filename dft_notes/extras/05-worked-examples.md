---
layout: page
title: "Worked examples anthology"
permalink: /dft-notes/extras/worked-examples/
description: >-
  A topic-by-topic collection of the most important worked examples
  in the DFT Notes: quantum mechanics basics, mean-field methods,
  pseudopotentials, solids, geometry optimisation, phonons, band
  structures, and excited states. Each entry links to the runnable
  Python, the generated plot, the expected numbers, and the chapter
  section that does the derivation.
keywords: "worked examples, Python, DFT, plot, anthology,
  particle in a box, harmonic oscillator, hydrogen atom,
  STO-3G H2, Hartree-Fock, direct SCF, DIIS, Kohn-Sham SCF,
  pseudopotential, free-electron band, diatomic chain,
  graphene, two-level absorption"
---

# Worked examples anthology

> One page that pulls together the **most important worked
> examples** from the DFT Notes, organised by topic rather than
> by chapter. Every entry links to (i) the runnable Python in
> [`dft_notes/python_codes/`]({{ site.baseurl }}/dft-notes/python_codes/),
> (ii) the committed plot in `plots/`, (iii) the chapter section
> that does the derivation, and (iv) the expected numerical
> output. The anthology is the natural starting point for a
> reader who already knows the theory and wants to see numbers.

This page is the **executables index** of the notes. The chapters
derive; this page *runs*. If you have a one-hour commute and want
to know which script does what, this is the place.

## How to read this page

Each section is a self-contained worked example. The shape of
each entry is the same:

1. **Problem statement** — what system and what calculation.
2. **Approach** — one paragraph on the method.
3. **Script** — link to the runnable Python.
4. **Plot** — link to the committed PNG.
5. **Expected output** — the key numbers you should see when
   you run the script.
6. **Chapter section** — the cross-reference into the prose.

> **Status of the chapter scripts.**  Chapters 00–08 are
> *shipped*; chapters 09–13 are *planned* (see
> [`chapters-map.md`]({{ site.baseurl }}/dft-notes/chapters-map/)).
> Where a script exists in `python_codes/`, the entry below
> links to it directly. Where the example exists only as inlined
> chapter code (or is from a planned chapter), the entry
> points to the chapter section that *contains* the worked
> example, and says so explicitly.

---

## 1. Quantum mechanics basics

The three textbook problems every DFT student must have seen at
least once: a particle in a 1-D box, the harmonic oscillator, and
the hydrogen atom. The first is the simplest discretised
differential equation; the second introduces ladder operators
and Hermite polynomials; the third is the only Coulomb problem
with a closed-form solution and the anchor of every atomic
orbital used in chemistry.

### 1.1 Particle in a box

**Problem.** A single electron in a 1-D box of length
$L = 1\,a_0$ with infinite walls at $x = 0$ and $x = L$.
Compute the first four eigenfunctions and eigenvalues
$\psi_n(x), E_n$.

**Approach.** Solve the time-independent Schrödinger equation
analytically:

$$
\psi_n(x) = \sqrt{\frac{2}{L}} \sin\!\left(\frac{n\pi x}{L}\right),
\qquad
E_n = \frac{\pi^2 n^2}{2 L^2} .
$$

The script samples the closed-form solution on a fine grid,
plots $\psi_n$ and $|\psi_n|^2$ for $n = 1, 2, 3, 4$, and
labels each curve with its eigenvalue.

- **Script** — [chapter_00/01-particle-in-box.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_00/01-particle-in-box.py)
- **Plot** — [chapter_00/plots/01-particle-in-box.png]({{ site.baseurl }}/dft-notes/python_codes/chapter_00/plots/01-particle-in-box.png)
- **Chapter section** — [Chapter 01, §1.3 (Particle in a box)]({{ site.baseurl }}/dft-notes/chapter-01/#13-a-minimal-example-the-particle-in-a-box); also discussed in [Chapter 00, *Hello world*]({{ site.baseurl }}/dft-notes/chapter-00/) (the 1s-density version of the same idea).
- **Expected output.** Eigenvalues in atomic units:
  $E_1 = 4.9348$, $E_2 = 19.7392$, $E_3 = 44.4132$, $E_4 = 78.9568$ (in $E_h$).
  The first plot panel shows the four sine-shaped wavefunctions
  with the expected node count (1s = no node, 2s = one node,
  etc.); the second panel shows the corresponding probability
  densities. The total runtime is under a second on a laptop.

> **Note on the chapter reference.** The chapter markdown
> cross-references the script as
> `dft_notes/python_codes/chapter_01/01-particle-in-box.py`,
> but the canonical, runnable file currently lives in
> `chapter_00/` (where it was written first, as the
> ["hello world"]({{ site.baseurl }}/dft-notes/chapter-00/#hello-world--a-chapters-smallest-program)
> for the entire site). The path above is the one that
> *runs*; the chapter path will be moved into `chapter_01/` in
> a follow-up commit by `agent:code-runner`.

### 1.2 Harmonic oscillator

**Problem.** The 1-D quantum harmonic oscillator with
unit mass and $\omega = 1$ (atomic units). Find the lowest
six eigenpairs of

$$
\hat H = -\tfrac{1}{2}\partial_x^2 + \tfrac{1}{2}\,x^2 .
$$

**Approach.** Discretise the Hamiltonian on the interval
$[-L, L]$ with $L = 8$ and $N = 800$ points and a 3-point
stencil for the second derivative. The result is a sparse
tridiagonal matrix. The lowest six eigenpairs are found with
`scipy.sparse.linalg.eigsh(H, k=6, which="SM")`. Eigenvectors
are normalised to unit $L^2$ norm on the grid. The expected
eigenvalues are $E_n = n + 1/2$ in units of $\omega$.

- **Script** — the code is inlined in
  [Chapter 01, §1.11.2]({{ site.baseurl }}/dft-notes/chapter-01/#1112-harmonic-oscillator-via-finite-differences)
  (`dft_notes/python_codes/chapter_01/02-harmonic-oscillator.py`,
  in chapter markdown only; the runnable file in
  `python_codes/chapter_01/` is forthcoming from `agent:code-runner`).
- **Plot** — referenced in
  [§1.11.2 of chapter 01]({{ site.baseurl }}/dft-notes/chapter-01/#1112-harmonic-oscillator-via-finite-differences)
  as `plots/02-harmonic-oscillator.png`.
- **Chapter section** — [Chapter 01, §1.9 (Ladder operators and the QHO spectrum)]({{ site.baseurl }}/dft-notes/chapter-01/#19-the-harmonic-oscillator); §1.11.2 (numerical solution).
- **Expected output.** Eigenvalues (in units of $\omega$):
  $E_0 = 0.500000$, $E_1 = 1.500000$, $E_2 = 2.500000$,
  $E_3 = 3.500000$, $E_4 = 4.500000$, $E_5 = 5.500000$,
  each accurate to better than $10^{-6}\,\omega$ for the
  default $L = 8$, $N = 800$. The figure shows the four
  lowest eigenfunctions superposed on the potential
  $V(x) = x^2/2$, each centred on the corresponding
  classical turning point $x = \pm\sqrt{2 E_n}$.

### 1.3 Hydrogen radial wavefunctions

**Problem.** Plot the first six radial hydrogen
eigenfunctions $R_{n\ell}(r)$ for $n = 1, 2, 3$ and
$\ell = 0, 1, 2$, on a linear radial grid.

**Approach.** Use the closed-form hydrogen radial
wavefunctions

$$
R_{n\ell}(r) = -\sqrt{\left(\frac{2Z}{n}\right)^{\!3}\!
                 \frac{(n - \ell - 1)!}{2n\,[(n + \ell)!]^3}}\;
                 e^{-Zr/n}\,(2Zr/n)^\ell\,
                 L_{n-\ell-1}^{2\ell+1}(2Zr/n) ,
$$

with $Z = 1$. The associated Laguerre polynomials
$L_{n-\ell-1}^{2\ell+1}$ are evaluated with
`scipy.special.genlaguerre`. The plot shows six curves on a
linear $r$ grid from $0.05$ to $30\,a_0$.

- **Script** — the code is inlined in
  [Chapter 01, §1.11.3]({{ site.baseurl }}/dft-notes/chapter-01/#1113-hydrogen-radial-eigenfunctions)
  (referenced path:
  `dft_notes/python_codes/chapter_01/03-hydrogen-radial.py`;
  runnable file in `python_codes/chapter_01/` is forthcoming).
- **Plot** — referenced in
  [§1.11.3 of chapter 01]({{ site.baseurl }}/dft-notes/chapter-01/#1113-hydrogen-radial-eigenfunctions)
  as `plots/03-hydrogen-radial.png`.
- **Chapter section** — [Chapter 01, §1.10 (Hydrogen atom; the Bohr formula and the explicit eigenfunctions)]({{ site.baseurl }}/dft-notes/chapter-01/#110-the-hydrogen-atom).
- **Expected output.** Six curves with the expected node
  counts: 1s (nodeless, peaked at the origin), 2s (one
  radial node at $r = 2\,a_0$), 2p (one peak, no radial
  node, $\propto r$ at the origin), 3s (two radial nodes),
  3p (one radial node), 3d (no radial nodes, $\propto r^2$
  at the origin). The energies shown in the legend are the
  Bohr levels $E_n = -1/(2n^2)\,E_h$:
  $E_1 = -0.5000$, $E_2 = -0.1250$, $E_3 = -0.0556\,E_h$.

---

## 2. Mean-field methods

Three "first-principles" calculations on a system with two
electrons and two nuclei: a textbook HF in a Gaussian basis, a
direct-SCF HF with DIIS acceleration, and the equivalent
Kohn–Sham loop with a local exchange–correlation functional.
All three reduce to iterating a single matrix eigenproblem
until self-consistency.

### 2.1 H₂ in STO-3G, closed-shell Hartree–Fock

**Problem.** Hartree–Fock on H₂ at $R = 1.4\,a_0$ in the
minimal STO-3G basis (one contracted $s$-function per
hydrogen). Compute the converged total energy, the two MO
energies, the MO coefficients, and plot the two MOs along
the bond axis.

**Approach.** Build the overlap $\mathbf S$, the kinetic
matrix $\mathbf T$, the nuclear-attraction matrix $\mathbf
V$, the core Hamiltonian $\mathbf h = \mathbf T + \mathbf V$,
and the four-index ERI tensor $\langle \mu\nu \rvert
\lambda\sigma \rangle$ by contracting the
Hehre–Stewart–Pople STO-3G primitives for hydrogen
($\alpha = 0.168856, 0.623913, 3.425250$ with
$d = 0.444635, 0.535328, 0.154329$). Iterate
$\mathbf F = \mathbf h + \mathbf J[\mathbf P] - \tfrac{1}{2}
\mathbf K[\mathbf P]$ with $\mathbf P = 2 \mathbf c_1
\mathbf c_1^\dagger$ until the density and the energy both
stop moving. Diagonalise the Fock matrix at every iteration
with `scipy.linalg.eigh(F, S)`.

- **Script** — [chapter_06/01-sto-3g-h2.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_06/01-sto-3g-h2.py)
- **Plot** — [chapter_06/plots/01-sto-3g-h2.png]({{ site.baseurl }}/dft-notes/python_codes/chapter_06/plots/01-sto-3g-h2.png)
- **Chapter section** — [Chapter 06, §6.9 (STO-3G H₂ worked example)]({{ site.baseurl }}/dft-notes/chapter-06/#69-worked-example-sto-3g-h), the central numerical anchor of the notes.
- **Expected output.**
  - Overlap $\mathbf S$: `[[1.0000, 0.6593], [0.6593, 1.0000]]`.
  - Core Hamiltonian $\mathbf h$: `[[-1.1204, -0.9584], [-0.9584, -1.1204]]`.
  - Selected ERIs (chemists' notation): $(11|11) = 0.7746$, $(11|22) = 0.5697$, $(12|12) = 0.2970$, $(11|12) = 0.4441$.
  - Converged MO energies: $\varepsilon_1 = -0.5782$, $\varepsilon_2 = +0.6703\,E_h$.
  - Bonding MO coefficient: $C_{11} = C_{21} = 0.5489$; antibonding $C_{12} = -C_{22} = 1.2115$ (signs arbitrary up to a global phase).
  - **Converged HF energy: $E_\text{tot} = -1.1167\,E_h$** (Szabo & Ostlund, table 3.5).
  - SCF converges in 3 iterations from $\mathbf P = \mathbf 0$.

> **Tip.**  This calculation is the *single most quoted*
> number in introductory quantum chemistry. It is also the
> reference point for every KS calculation that follows
> in the notes: a HF/KS-DFT result on H₂ in a minimal basis
> is not "DFT vs. experiment" but "DFT vs. this number".

### 2.2 Direct SCF for H₂ with DIIS

**Problem.** Same as §2.1 (H₂ STO-3G, $R = 1.4\,a_0$),
but with two algorithmic upgrades: (i) the ERI tensor is
*recomputed* on the fly every iteration rather than stored
(*direct SCF*), and (ii) the Fock matrix is *extrapolated*
using Pulay's DIIS (direct inversion in the iterative
subspace) accelerator.

**Approach.** The ERI tensor $\langle \mu\nu \rvert
\lambda\sigma \rangle$ has $K^4 = 16$ entries for the
$2 \times 2$ problem and is rebuilt every iteration from the
primitive Gaussians using the Schwarz inequality as a screen
(though for $K = 2$ every integral is computed). DIIS keeps
a history of the last $m = 6$ Fock matrices and their
commutator error vectors $\mathbf e^{(i)} = \mathbf F^{(i)}
\mathbf P^{(i)} \mathbf S - \mathbf S \mathbf P^{(i)}
\mathbf F^{(i)}$, then extrapolates the next Fock matrix as
a linear combination $\mathbf F = \sum_i c_i \mathbf
F^{(i)}$ with the $c_i$ chosen to minimise the norm of the
extrapolated error.

- **Script** — the code is inlined in
  [Chapter 03, §3.8.5]({{ site.baseurl }}/dft-notes/chapter-03/#385-full-implementation-h₂-sto-3g-with-diis)
  (referenced path:
  `dft_notes/python_codes/chapter_03/01-direct-scf-h2-sto3g-diis.py`;
  runnable file in `python_codes/chapter_03/` is forthcoming).
- **Plot** — this example has no plot; it is a pure number
  (the SCF convergence trace is printed to stdout).
- **Chapter section** — [Chapter 03, §3.8 (Direct SCF, conventional SCF, and DIIS)]({{ site.baseurl }}/dft-notes/chapter-03/#38-direct-scf-conventional-scf-and-diis); §3.8.5 has the full source.
- **Expected output.** From the chapter's reference run:
  - `Converged in 11 iterations, dP = 9.7e-11`
  - MO energies: $\varepsilon_1 = -0.5782$, $\varepsilon_2 = +0.6703\,E_h$
  - $E_\text{HF} = -1.116714\,E_h$ (matches Szabo & Ostlund to all six digits).
  - With DIIS replaced by simple density mixing ($\alpha = 0.3$), the same calculation needs ~30 iterations and shows visible oscillations; DIIS converges monotonically and drops the error norm by ~3 decades per iteration once the DIIS regime is entered.

### 2.3 Kohn–Sham SCF loop

**Problem.** The Kohn–Sham analogue of §2.1: a
closed-shell KS calculation on H₂ in a Gaussian basis, with
a *local* (LDA-style) exchange–correlation functional
contributing a matrix $\mathbf F_\text{xc}$ to the Fock
matrix.

**Approach.** Replace the non-local exchange operator of
HF by a local potential $\hat v_\text{xc}(\mathbf r) =
\delta E_\text{xc}/\delta \rho(\mathbf r)$. The matrix
element $\langle \chi_\mu \rvert \hat v_\text{xc} \rvert
\chi_\nu \rangle$ is computed on a real-space grid (or, in
the simplest possible version, as a constant times $S_{\mu\nu}$).
The SCF loop is otherwise identical in shape to HF.

- **Script** — the canonical "shape of the loop" is given
  as the inlined `ks_scf` function in
  [Chapter 04, §4.4 (The KS self-consistent loop)]({{ site.baseurl }}/dft-notes/chapter-04/#44-the-ks-self-consistent-loop).
  (Referenced path:
  `dft_notes/python_codes/chapter_04/01-ks-scf.py`; the
  runnable file in `python_codes/chapter_04/` is forthcoming
  from `agent:code-runner`.)
- **Plot** — none (the canonical example prints the
  converged KS energy, MO energies, and total energy).
- **Chapter section** — [Chapter 04, §4.4 (KS SCF loop)]({{ site.baseurl }}/dft-notes/chapter-04/#44-the-ks-self-consistent-loop); §4.6 (mixing and DIIS for KS); §4.10 (the full implementation).
- **Expected output.**  With the LDA functional and the
  STO-3G basis, the KS calculation on H₂ at
  $R = 1.4\,a_0$ reproduces the HF energy
  $-1.1167\,E_h$ to within the basis-set error (because LDA
  exchange is a poorer approximation than HF exchange on
  one electron, where they coincide exactly). With a
  hybrid functional (B3LYP), the result shifts to roughly
  $-1.18\,E_h$, in agreement with high-level calculations
  and experiment. SCF convergence in 5–10 iterations with
  DIIS.

> **Tip.**  The shape of the loop in §4.4 is the
> *proto-loop* of every production DFT code.  The
> differences between codes (Gaussian vs. plane-wave, all-
> electron vs. pseudopotential, serial vs. parallel) are
> all hiding inside the two lines that build $\mathbf J$
> and $\mathbf F_\text{xc}$.

---

## 3. Pseudopotentials

The pseudopotential approximation replaces the strongly
oscillating all-electron wavefunction of an atom near the
nucleus by a smooth nodeless pseudo-wavefunction that
matches the all-electron one outside a chosen cutoff radius
$r_c$. This is the worked construction of a Troullier–
Martins (TM) norm-conserving pseudopotential for the
hydrogen 1s state.

### 3.1 Hydrogen Troullier–Martins pseudopotential

**Problem.** Construct a norm-conserving pseudopotential
for hydrogen ($Z = 1$, $l = 0$) with cutoff
$r_c = 0.5\,a_0$, in the Troullier–Martins parameterisation.
Verify the four matching conditions at $r_c$ (value, first
derivative, second derivative, and integrated norm) and
plot the pseudo-wavefunction and pseudo-potential on top of
the all-electron reference.

**Approach.** Invert the radial Schrödinger equation with
the ansatz

$$
\phi(r) = r \exp\bigl(c_0 + c_1 r^2 + c_2 r^4 + c_3 r^6\bigr)
$$

inside $r_c$. Enforce (1) value, (2) first derivative, (3)
second derivative, and (4) integrated norm at $r_c$. (1)
fixes $c_0$; (2)–(4) form a 3×3 nonlinear system in
$(c_1, c_2, c_3)$, solved with `scipy.optimize.fsolve` from
an initial guess derived from the linear ansatz. The
pseudo-potential inside $r_c$ is then obtained by inversion
of the radial equation; outside $r_c$ it equals the
all-electron $-1/r$ tail.

- **Script** — [chapter_08/01-hydrogen-pseudopotential.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_08/01-hydrogen-pseudopotential.py)
- **Plot** — [chapter_08/plots/01-hydrogen-pseudopotential.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_08/plots/01-hydrogen-pseudopotential.png)
- **Chapter section** — [Chapter 08, §8.8 (Worked example: hydrogen 1s, $l = 0$, $r_c = 0.5\,a_0$)]({{ site.baseurl }}/dft-notes/chapter-08/#88-worked-example--hydrogen-1s-l--0-r_c--05a_0).
- **Expected output.** Coefficients (atomic units, with
  $r_c = 0.5$):
  $c_0 = -0.765\,548$, $c_1 = -0.286\,743$, $c_2 = +0.602\,752$, $c_3 = -0.378\,179$
  (the exact values depend on the residual tolerance of
  `fsolve`; the script reports them to 6 d.p.). Matching
  at $r_c$: all-electron $u_{1s}(r_c) = 0.6065$, pseudo
  $\phi(r_c) = 0.6065$ (matches to 6 d.p.),
  $Q_0^\text{ae} = 0.9206$ (closed form), pseudo
  $Q_0^\text{ps} = 0.9206$ (quadrature). Pseudo-potential
  is finite at the origin ($V_\text{ps}(0) = -0.5 + 3 c_1
  \approx -1.36\,E_h$) and continuous at $r_c$ (matches
  $-1/r_c = -2.0\,E_h$ to machine precision). The script
  prints a residual $\max\lvert f_i\rvert < 10^{-9}$ on the
  three matching conditions.

> **Tip.**  The pseudo-potential is *finite* at the origin
> ($V_\text{ps}(0) \approx -1.36\,E_h$), in contrast to the
> all-electron $-1/r$ that diverges.  This is the whole
> point: the pseudo-potential is smooth enough to expand in
> a small plane-wave basis, while the all-electron one
> would need 30 oscillations for a heavy atom's $1s$.

---

## 4. Solids

The simplest band-structure calculation: a one-dimensional
periodic lattice with a weak periodic potential, treated in a
plane-wave basis at the $\Gamma$-point and along the
Brillouin zone. This is the nearly-free-electron model that
is the conceptual ancestor of every modern solid-state code.

### 4.1 1-D nearly-free-electron band structure

**Problem.** Band structure of a 1-D periodic lattice with
lattice constant $a = 5\,a_0$ and cosine potential
$V(x) = -\tfrac{1}{2} \cos(2\pi x / a)$. Compute and plot
the lowest four bands as a function of $k$ across the first
Brillouin zone $[-\pi/a, +\pi/a]$, using 21 plane waves
($m = -10, \dots, +10$) and 100 k-points.

**Approach.** The plane-wave basis is
$|k + m \cdot 2\pi/a\rangle$ for $m = -10, \dots, +10$. The
$21 \times 21$ Hamiltonian at each $k$ is

$$
H_{mm'}(k) = \tfrac{1}{2}\bigl(k + m \cdot 2\pi/a\bigr)^2 \delta_{mm'}
           + V_\text{per}\bigl((m' - m) \cdot 2\pi/a\bigr) ,
$$

with $V_\text{per}$ nonzero only for
$\lvert m' - m\rvert = 1$, where it equals
$V_0/2 = -1/4$ Hartree. Diagonalise at each of the 100
$k$-points with `numpy.linalg.eigvalsh` and plot the lowest
four eigenvalues as a function of $k$.

- **Script** — [chapter_07/01-free-electron-bands.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_07/01-free-electron-bands.py)
- **Plot** — [chapter_07/plots/01-free-electron-bands.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_07/plots/01-free-electron-bands.png)
- **Chapter section** — [Chapter 07, §7.7 (Worked example: 1-D periodic lattice)]({{ site.baseurl }}/dft-notes/chapter-07/#77-worked-example--band-structure-of-a-1-d-periodic-lattice).
- **Expected output.** At $k = \pm \pi/a$, the lowest two
  bands are split by the matrix element
  $2 |V(2\pi/a)| = 0.5\,E_h$. The script prints a sanity
  check: `eps_1 = +0.08xxx E_h`, `eps_2 = +0.58xxx E_h`,
  `gap ≈ +0.50 E_h` (the predicted $0.5\,E_h$ is recovered
  to better than $10^{-4}$). The first band is well
  described by the free-electron parabola
  $\tfrac{1}{2}(k - 2\pi/a)^2$ (band-folded into the first
  BZ); the second band is well described by
  $\tfrac{1}{2} k^2$ at small $k$ and crosses into
  $\tfrac{1}{2}(k + 2\pi/a)^2$ near the BZ boundary.

> **Tip.**  The 0.5-Hartree gap at the BZ boundary is
> *exactly* what the textbook nearly-free-electron formula
> $E_\text{gap} = 2 |V(G)|$ predicts for a cosine
> potential of amplitude $V_0 = -1/2$ Hartree.  The script
> prints the comparison; if the printed gap differs from
> 0.5 by more than $10^{-3}$, the plane-wave basis is too
> small to converge the splitting.

---

## 5. Geometry optimisation

**Status.** *Chapter 09 (Forces & geometry optimisation) is a
planned chapter.* No chapter markdown and no runnable script
exist in the repository at this point. The worked example
will appear here once the chapter lands. The example
*concept* (from the [chapters map]({{ site.baseurl }}/dft-notes/chapters-map/))
is:

### 5.1 H₂ bond relaxation (planned)

**Problem.** Starting from a stretched H₂ geometry
($R = 1.8\,a_0$, well above equilibrium), use the
Hellmann–Feynman force to relax the bond length to
equilibrium, then report the converged geometry and the
total-energy curve as a function of $R$.

**Approach.** At each geometry, run a closed-shell KS or HF
calculation in a Gaussian basis, compute the analytic
gradient

$$
\frac{d E_\text{tot}}{d \mathbf R_A} = -Z_A \int \rho(\mathbf r) \frac{\mathbf r - \mathbf R_A}{\lvert \mathbf r - \mathbf R_A\rvert^3}\, d\mathbf r
   + \text{(basis-set correction)},
$$

and take a step along the direction of decreasing energy
using BFGS or L-BFGS. Repeat until the maximum force
component is below $10^{-4}\,E_h/a_0$.

- **Script (planned)** — `dft_notes/python_codes/chapter_09/01-h2-bond-relaxation.py`
- **Plot (planned)** — `dft_notes/python_codes/chapter_09/plots/01-h2-bond-relaxation.png`
- **Chapter section (planned)** — Chapter 09, §9.5 (work to land with the chapter).
- **Expected output (planned).**  Converged bond length
  $R_\text{eq} = 1.40\,a_0$ (HF/STO-3G, matching Szabo &
  Ostlund table 3.5), equilibrium energy
  $E_\text{eq} = -1.1167\,E_h$, force at the converged
  geometry below $10^{-6}\,E_h/a_0$. The energy-vs-$R$ plot
  should show the textbook Morse-like shape with a minimum
  at $R_\text{eq}$, dissociation limit
  $2 \times E_\text{H} = -1.0\,E_h$ at large $R$, and a
  force-constant second derivative
  $k = 0.37\,E_h/a_0^2$ (vibrational frequency
  $\omega \approx 4400\,\text{cm}^{-1}$, the well-known
  H₂ stretch).

> **Tracking.**  The full source is to be inlined in
> chapter 09, §9.5 once the chapter lands.  This entry
> will be filled in by `agent:code-runner` as part of the
> monthly parallel research deploy.

---

## 6. Phonons

**Status.** *Chapter 10 (Phonons & vibrations) is a planned
chapter.* No chapter markdown and no runnable script exist
yet. The worked example concept is:

### 6.1 1-D diatomic-chain dispersion (planned)

**Problem.** A 1-D infinite chain of alternating masses
$m_1$ and $m_2$ ($m_1 = 1$, $m_2 = 3$ in arbitrary units)
with lattice constant $a$ and spring constant $K$ between
nearest neighbours. Compute the phonon dispersion relation
$\omega(q)$ in the first Brillouin zone
$-\pi/a \le q \le \pi/a$.

**Approach.** The classical equations of motion yield a
$2 \times 2$ dynamical matrix

$$
\mathbf D(q) = \frac{K}{m_1 m_2}
\begin{pmatrix}
m_1 + m_2 & -\sqrt{m_1 m_2}\,(1 + e^{-i q a}) \\
-\sqrt{m_1 m_2}\,(1 + e^{i q a}) & m_1 + m_2
\end{pmatrix} .
$$

The two eigenvalues give the **acoustic** branch
($\omega \to 0$ as $q \to 0$) and the **optical** branch
($\omega \to \sqrt{2K(1/m_1 + 1/m_2)}$ as $q \to 0$). The
bandwidth of the acoustic branch is set by
$\sqrt{2K/m_1}$ at $q = \pi/a$ and the gap at $q = 0$ is
$\sqrt{2K(1/m_1 + 1/m_2)}$.

- **Script (planned)** — `dft_notes/python_codes/chapter_10/01-diatomic-chain.py`
- **Plot (planned)** — `dft_notes/python_codes/chapter_10/plots/01-diatomic-chain.png`
- **Chapter section (planned)** — Chapter 10, §10.3 (1-D model, the simplest phonon dispersion).
- **Expected output (planned).** Two branches; with
  $m_1 = 1$, $m_2 = 3$, $K = 1$: acoustic branch
  $\omega_\text{ac}(0) = 0$, $\omega_\text{ac}(\pi/a) = \sqrt{2} \approx 1.414$;
  optical branch $\omega_\text{op}(0) = \sqrt{8/3} \approx 1.633$,
  $\omega_\text{op}(\pi/a) = \sqrt{2}$ (the two branches
  cross at the BZ boundary in the equal-mass limit; with
  $m_1 \neq m_2$ they touch but do not cross). The group
  velocities at $q = 0$ are $0$ (acoustic) and $0$
  (optical), and the maximum acoustic group velocity is
  $\sqrt{K/m_1}$ (large-mass endpoint) and the maximum
  optical group velocity is $\sqrt{K/m_2}$ (small-mass
  endpoint).

---

## 7. Band structures

**Status.** *Chapter 11 (Band structures & Fermi surfaces) is
a planned chapter.* No chapter markdown and no runnable
script exist yet. The worked example concept is:

### 7.1 Graphene tight-binding bands (planned)

**Problem.** Graphene's tight-binding band structure in the
honeycomb lattice, with one $p_z$ orbital per carbon and
nearest-neighbour hopping $t \approx -2.7\,$eV. Plot the
$\pi$ and $\pi^*$ bands along the high-symmetry path
$\Gamma \to M \to K \to \Gamma$.

**Approach.** The honeycomb lattice is a **bipartite**
lattice (A and B sublattices); the Bloch Hamiltonian at
wavevector $\mathbf k$ is

$$
H(\mathbf k) =
\begin{pmatrix}
0 & t\, f(\mathbf k) \\
t\, f^*(\mathbf k) & 0
\end{pmatrix} ,
$$

with
$f(\mathbf k) = e^{i k_x a/\sqrt{3}} + 2 e^{-i k_x a/(2\sqrt{3})} \cos(k_y a / 2)$,
where $a$ is the lattice constant. The eigenvalues are
$\varepsilon_\pm(\mathbf k) = \pm |t|\,|f(\mathbf k)|$.
The two bands touch at the **K and K'** points of the
Brillouin zone — the *Dirac points* that give graphene its
linear dispersion and its anomalous transport.

- **Script (planned)** — `dft_notes/python_codes/chapter_11/01-graphene-bands.py`
- **Plot (planned)** — `dft_notes/python_codes/chapter_11/plots/01-graphene-bands.png`
- **Chapter section (planned)** — Chapter 11, §11.4 (graphene's tight-binding bands as the canonical 2-D example).
- **Expected output (planned).** Two bands that are
  symmetric about zero. At the K point
  $\mathbf k = (4\pi/(3a), 0)$ the gap is exactly zero
  (numerical zero to machine precision); the dispersion
  around K is linear with Fermi velocity
  $v_F = \sqrt{3} |t| a / (2 \hbar) \approx 10^6\,\text{m/s}$.
  The bandwidth is $3 |t| \approx 8.1\,$eV. The K and K'
  points are *inequivalent* under time-reversal; the two
  valleys give graphene a *pseudo-spin* degree of freedom
  that is the basis of much of its physics.

> **Tip.**  Graphene's tight-binding Hamiltonian is
> identical in shape to the **2-D massive Dirac
> Hamiltonian** (a $2 \times 2$ Pauli-matrix structure
> with a single off-diagonal coupling).  Adding a
> sublattice-staggered potential $\pm \Delta$ to the
> diagonal opens a gap of $2\Delta$ — the BHZ model that
> is the basis of the quantum spin Hall effect.

---

## 8. Excited states

**Status.** *Chapter 12 (TDDFT) is a planned chapter.* No
chapter markdown and no runnable script exist yet. The
worked example concept is:

### 8.1 Two-level absorption spectrum (planned)

**Problem.** A two-level system with ground state $|g\rangle$
and excited state $|e\rangle$, separated by transition
energy $\hbar\omega_0$, and a time-dependent electric field
$E(t) = E_0 \cos(\omega t)$ in the dipole approximation.
Compute the absorption spectrum $\sigma(\omega)$ (the
Fermi-golden-rule cross section) near resonance.

**Approach.** Time-dependent perturbation theory (see
[Chapter 01, §1.8, Fermi's golden rule]({{ site.baseurl }}/dft-notes/chapter-01/#18-time-dependent-perturbation-theory))
gives the transition rate

$$
\Gamma_{g \to e}(\omega) = \frac{\pi}{3} \frac{E_0^2}{\hbar^2} |\langle e \rvert \hat{\boldsymbol\mu} \rvert g\rangle|^2
                              \,\delta(\omega - \omega_0) .
$$

For a Lorentzian lineshape of width $\gamma$ (the spontaneous
emission rate of the upper state), the cross section is

$$
\sigma(\omega) = \frac{\pi |\mu_{eg}|^2}{3 \epsilon_0 \hbar c} \,
                  \frac{\gamma / 2\pi}{(\omega - \omega_0)^2 + (\gamma/2)^2} .
$$

The script evaluates $\sigma(\omega)$ on a fine grid of
$\omega$ for $\omega_0 = 1.0$ and $\gamma = 0.05$ (atomic
units) and plots the resulting Lorentzian.

- **Script (planned)** — `dft_notes/python_codes/chapter_12/01-two-level-absorption.py`
- **Plot (planned)** — `dft_notes/python_codes/chapter_12/plots/01-two-level-absorption.png`
- **Chapter section (planned)** — Chapter 12, §12.3 (Fermi's golden rule and the two-level model as the warm-up to TDDFT).
- **Expected output (planned).** A single Lorentzian peak
  centred at $\omega = 1.0$ with full-width at half maximum
  $\gamma = 0.05$. The integrated strength
  $\int \sigma(\omega)\, d\omega = \pi |\mu_{eg}|^2 / (3 \epsilon_0 \hbar c)$
  is the **oscillator strength** of the transition in SI
  units (or
  $\int \sigma(\omega)\, d\omega = 2 \pi^2 |\mu_{eg}|^2 / c$
  in Gaussian units). The peak value is
  $\sigma(\omega_0) = 2/(3 \gamma) \cdot |\mu_{eg}|^2/(\epsilon_0 \hbar c)$.
  For an electric-dipole-allowed transition in a small
  molecule, $|\mu_{eg}| \sim 1\,ea_0 \approx 2.5\,$D, and
  the peak cross section is of order $10^{-16}\,\text{cm}^2$
  in laboratory units.

> **Note on framing.**  The two-level system is the
> conceptual ancestor of the **Casida linear-response TDDFT**
> equations: in TDDFT the *ground state* is a Slater
> determinant, the *excited states* are the
> resonant solutions of the density-density response
> function, and the *oscillator strengths* are the residues
> of the polarisation propagator at its poles.  The
> two-level example above is the $K = 1$ case of a
> general $K$-orbital Casida calculation.

---

## What's next

- The [Python codes]({{ site.baseurl }}/dft-notes/python_codes/)
  index has a chapter-by-chapter list of every script in
  the repository, with the plots in `plots/`.
- The [chapters map]({{ site.baseurl }}/dft-notes/chapters-map/)
  is the live dependency graph of every chapter, shipped
  or planned.
- [Chapter 00]({{ site.baseurl }}/dft-notes/chapter-00/) has
  the *Notation* table that this anthology assumes
  throughout.

> **Disclaimer.**  These notes are a personal study aid.
> They are correct to the best of the author's knowledge,
> but they are *not* a substitute for a textbook.  Cite
> primary sources, not these notes.
