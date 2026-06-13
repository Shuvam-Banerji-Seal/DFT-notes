---
layout: page
title: "Chapter 01 — Schrödinger equation"
permalink: /dft-notes/chapter-01/
description: >-
  The postulates of quantum mechanics, the time-independent Schrödinger
  equation, and the structure of the electronic Hamiltonian.
keywords: "Schrödinger equation, postulates, Hamiltonian, wavefunction"
---

# Chapter 01 — Schrödinger equation

> The single most important equation in non-relativistic quantum
> mechanics. Every other equation in these notes is a special case, a
> mean-field approximation, or a comment on this one.

## 1.1 The time-independent Schrödinger equation

For a closed, non-relativistic, $N$-particle system with Hamiltonian
$\hat H$, the **stationary states** $\psi$ and their **energies** $E$
are eigenpairs of $\hat H$:

$$
\hat H \, \psi(\mathbf r_1, \dots, \mathbf r_N) = E \, \psi(\mathbf r_1, \dots, \mathbf r_N).
$$

For the rest of these notes we will almost always work with the
**electronic Hamiltonian** in the **Born–Oppenheimer** (clamped-nuclei)
approximation. In atomic units it reads

$$
\hat H = -\frac{1}{2} \sum_{i=1}^{N} \nabla_i^2 \;-\; \sum_{i=1}^{N} \sum_{A=1}^{M} \frac{Z_A}{|\mathbf r_i - \mathbf R_A|} \;+\; \sum_{i<j}^{N} \frac{1}{|\mathbf r_i - \mathbf r_j|}.
$$

The three terms are, in order: the kinetic energy of the electrons, the
electron–nuclear attraction, and the electron–electron repulsion. The
nuclear–nuclear repulsion is a constant in the Born–Oppenheimer picture
and is added at the end.

> **Tip.** Many texts write the second term as $\sum_A Z_A / r_{iA}$
> where $r_{iA} = \lvert \mathbf r_i - \mathbf R_A \rvert$. We will
> use the explicit vector form because it makes the gradient
> transparent when we derive the Kohn–Sham equations.

## 1.2 The postulates

The Schrödinger equation is *postulated*; the constants in it are
measured; the rest is derived. We will use the Dirac–von Neumann
axiomatisation:

| #  | Postulate                                  | Mathematical statement                                                                 |
|:---|:-------------------------------------------|:--------------------------------------------------------------------------------------|
| P1 | States are rays in a Hilbert space        | $\psi \in \mathcal H$, with $\lVert \psi \rVert = 1$                                  |
| P2 | Observables are self-adjoint operators    | $\hat A : \mathcal H \to \mathcal H$, $\hat A = \hat A^\dagger$                       |
| P3 | Measurements give eigenvalues            | $\Pr(a_n) = \lvert \langle a_n \rvert \psi \rangle \rvert^2$                            |
| P4 | Expectation values                        | $\langle A \rangle = \langle \psi \rvert \hat A \rvert \psi \rangle$                   |
| P5 | Time evolution                             | $i \partial_t \lvert \psi(t) \rangle = \hat H \lvert \psi(t) \rangle$                  |
| P6 | Indistinguishability                      | For identical fermions, $\Psi$ is totally antisymmetric under particle exchange        |

P6 is the postulate that does almost all of the work in chemistry. It
is also the postulate that DFT tries to circumvent.

## 1.3 A minimal example: the particle in a box

To make the formalism concrete, consider a single electron in a 1-D box
of length $L$ with infinite walls at $x = 0$ and $x = L$. The
Hamiltonian is

$$
\hat H = -\frac{1}{2}\,\frac{d^2}{dx^2}, \qquad \psi(0) = \psi(L) = 0.
$$

The normalised eigenfunctions and eigenvalues are

$$
\psi_n(x) = \sqrt{\frac{2}{L}} \sin\!\left( \frac{n\pi x}{L} \right), \qquad E_n = \frac{\pi^2 n^2}{2 L^2}, \qquad n = 1, 2, 3, \dots
$$

A short Python snippet that solves the same problem **numerically** by
discretising the Laplacian and calling `numpy.linalg.eigh`:

```python
import numpy as np

def particle_in_a_box(L=1.0, N=400):
    """Return the first 5 eigenpairs of a 1-D particle in a box of length L."""
    h   = L / (N + 1)           # grid spacing
    x   = np.linspace(h, L - h, N)
    # 3-point stencil for the second derivative
    diag_main  = np.full(N,  2.0)
    diag_off   = np.full(N - 1, -1.0)
    H          = (np.diag(diag_main) + np.diag(diag_off, +1)
                                  + np.diag(diag_off, -1)) / (2 * h**2)
    evals, evecs = np.linalg.eigh(H)
    # Sort by absolute value; skip the trivial infinite-wall mode
    order       = np.argsort(evals)
    return evals[order[:5]], evecs[:, order[:5]], x

energies, _, x = particle_in_a_box()
for n, E in enumerate(energies, start=1):
    exact = (np.pi * n)**2 / 2
    print(f"  n={n}  numerical={E:9.5f}  exact={exact:9.5f}  Δ={E - exact:+.2e}")
```

For a 400-point grid, the first five eigenvalues agree with the
analytical formula to better than $10^{-8}$ Hartree.

> **Warning.** A diagonalising eigensolver is *never* the right way to
> solve a real quantum chemistry problem — it costs $O(N^3)$ and stores
> $O(N^2)$. The point of the snippet is to make the formal eigenproblem
> $\hat H \psi = E \psi$ feel concrete. Production codes use
> **iterative** eigensolvers (Lanczos, Davidson) that never materialise
> the full Hamiltonian.

## 1.4 Operators you will see again

The following operators are the alphabet of electronic-structure
theory. They are all self-adjoint on the appropriate domain, which is
why they are candidates for observables.

| Symbol | Name                     | Definition                                                                 | Appears in                          |
|:-------|:-------------------------|:---------------------------------------------------------------------------|:------------------------------------|
| $\hat T$ | Kinetic energy           | $\hat T = -\frac{1}{2} \sum_i \nabla_i^2$                                  | Every Hamiltonian                   |
| $\hat V_\text{ext}$ | External potential | $\hat V_\text{ext} = \sum_i v(\mathbf r_i)$                                | The $Z_A / r_{iA}$ term             |
| $\hat U_{ee}$ | Electron–electron repulsion | $\hat U_{ee} = \sum_{i<j} 1/r_{ij}$                                   | The $1/r_{ij}$ term                 |
| $\hat J$ | Classical Coulomb (Hartree) | $\hat J[\rho] = \int \rho(\mathbf r') / \lvert \mathbf r - \mathbf r' \rvert d\mathbf r'$ | Hartree–Fock, KS                    |
| $\hat K$ | Exchange (Fock)          | $\hat K_{ij} = \int \phi_i^*(\mathbf r') \phi_j(\mathbf r') / \lvert \mathbf r - \mathbf r' \rvert d\mathbf r'$ | Hartree–Fock                        |
| $\hat v_\text{xc}$ | XC potential        | The functional derivative of $E_\text{xc}[\rho]$ with respect to $\rho$    | Kohn–Sham DFT                       |
| $\hat P_{ij}$ | Permutation            | Exchanges particle labels $i \leftrightarrow j$                            | Antisymmetrisation                   |

## 1.5 What we are *not* doing

Two things the Schrödinger equation does not give us, and that we have
to add by hand or by approximation:

- **Spin.** The Hamiltonian above is spin-free. Spin enters via the
  antisymmetry postulate (P6) — electrons are fermions — and via the
  choice of $\Psi$ as a Slater determinant.
- **Relativistic effects.** For $Z \gtrsim 30$, the kinetic-energy
  term $-\frac{1}{2} \nabla^2$ should be replaced by the Dirac
  kinetic operator. Out of scope here; see a relativistic-chemistry
  text.

## 1.6 Outlook

The exact Schrödinger equation for a molecule with more than two or
three electrons is **unsolvable** in closed form, and is intractable
numerically because the wavefunction lives in a space whose dimension
grows exponentially with $N$. The rest of these notes is a tour of the
successive approximations that make the problem tractable: mean-field
theory, density-functional reformulation, and the zoo of
exchange–correlation functionals.

> Next: [chapter 02]({{ "/dft-notes/chapter-02/" | relative_url }}) —
> the many-body problem and why a single Slater determinant isn't
> enough.
