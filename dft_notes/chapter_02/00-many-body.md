---
layout: page
title: "Chapter 02 — The many-body problem"
permalink: /dft-notes/chapter-02/
description: >-
  Why a single Slater determinant is wrong, how badly it scales, and
  the wavefunction Ansätze that try to fix it.
keywords: "many-body, Slater determinant, antisymmetry, full CI, MP2, CCSD(T)"
---

# Chapter 02 — The many-body problem

> The exact electronic Schrödinger equation is solvable in closed form
> for $H_2^+$ and approximately for $H_2$. For every other molecule in
> the periodic table, we are forced to *approximate*. This chapter is
> about what the approximations are approximating.

## 2.1 The wavefunction lives in a huge space

For a system of $N$ electrons with one spin-orbital per electron, the
Hilbert space is the $N$-fold tensor product of the one-electron
Hilbert space. Its dimension grows **exponentially** with $N$:

$$
\dim \mathcal H = K^N,
$$

where $K$ is the size of the one-electron basis (e.g. $K \sim 100$ for
a typical Gaussian basis on a small organic molecule, $K \sim 10^6$ for
a plane-wave basis on a periodic solid). The wavefunction itself is a
function of $3N$ continuous variables *and* lives in a $K^N$-dimensional
discrete space.

This is the **exponential wall**. There is no known algorithm that
defeats it in general.

## 2.2 The Slater determinant

Postulate P6 — fermions are antisymmetric — means that the simplest
non-trivial wavefunction Ansatz is a **Slater determinant** of
one-electron spin-orbitals $\chi_i$:

$$
\Psi(\mathbf x_1, \dots, \mathbf x_N) =
\frac{1}{\sqrt{N!}}
\begin{vmatrix}
\chi_1(\mathbf x_1) & \chi_2(\mathbf x_1) & \cdots & \chi_N(\mathbf x_1) \\
\chi_1(\mathbf x_2) & \chi_2(\mathbf x_2) & \cdots & \chi_N(\mathbf x_2) \\
\vdots             & \vdots             & \ddots & \vdots             \\
\chi_1(\mathbf x_N) & \chi_2(\mathbf x_N) & \cdots & \chi_N(\mathbf x_N)
\end{vmatrix}.
$$

The determinant enforces antisymmetry: swapping two rows multiplies the
wavefunction by $-1$. This is what Pauli exclusion *is*, mathematically.

The corresponding one-particle density is

$$
\rho(\mathbf r) = \sum_{i=1}^{N} \sum_{\sigma \in \{\uparrow, \downarrow\}} \lvert \chi_i(\mathbf r, \sigma) \rvert^2.
$$

> **Tip.** A single Slater determinant is the exact ground state of a
> **non-interacting** system of fermions. For an interacting system it
> is, in general, only a starting point. The Hartree–Fock method
> (chapter 03) finds the *best* single determinant in a least-squares
> sense; the rest of many-body theory is a hierarchy of corrections on
> top of that.

## 2.3 The hierarchy of wavefunction methods

Once we accept that a single determinant is approximate, the next
question is: how do we add correlation back in? The standard answer is
a systematic ladder of methods, each with a known accuracy and a known
cost:

| Method           | Ansatz                                       | Cost (typical)    | Typical error (kcal/mol) |
|:-----------------|:---------------------------------------------|:------------------|:-------------------------|
| HF               | Single Slater determinant                   | $O(K^2 N)$        | 1 – 10 (relative)        |
| MP2              | 2nd-order Møller–Plesset perturbation       | $O(K^4)$          | 0.5 – 2                  |
| CISD             | Singles + doubles excitation CI             | $O(K^6)$          | 0.5 – 2                  |
| CCSD             | Coupled-cluster singles + doubles           | $O(K^6)$          | 0.2 – 1                  |
| CCSD(T)          | CCSD + perturbative triples                 | $O(K^7)$          | 0.1 – 0.5                |
| Full CI          | Exact (in the basis)                        | $O(K^N)$          | 0 (in basis)             |

> **Note.** "Cost" here is the *leading-order* scaling. All of these
> methods have a steep prefactor, but the scaling is what makes them
> intractable. CCSD(T) on a 20-atom organic molecule with a triple-zeta
> basis is feasible; CCSD(T) on a 100-atom protein is not. Full CI on
> more than about 12 electrons in a double-zeta basis is not.

## 2.4 The "gold standard" and its limits

CCSD(T) is widely called the *gold standard* of quantum chemistry. The
nickname is deserved for small molecules near their equilibrium
geometry. Three regimes where it fails or breaks down:

1. **Strong (static) correlation.** Bond-breaking, transition-metal
   complexes with near-degenerate $d$-orbitals, biradicals. The single
   reference breaks down; the perturbative triples are no longer a
   small correction.
2. **Large systems.** CCSD(T) on a 50-atom molecule with a triple-zeta
   basis is on the edge of feasibility. On a 500-atom protein it is
   impossible.
3. **Excited states.** The single-reference, ground-state Ansatz is
   inappropriate for states with very different orbital character.

DFT was designed to side-step these problems, not by adding correlation
on top of HF, but by *reformulating* the problem in terms of the
density, which lives in a fixed 3-D space.

## 2.5 A small full-CI experiment

To see the exponential wall in action, here is a 4-electron, 4-orbital
problem — a minimal-basis $H_4$ chain — solved **exactly** by full CI.
The code is short because the matrix is small (the Hamiltonian is
$36 \times 36$, indexed by Slater determinants of 4 electrons in 4
spatial-orbitals with $\alpha$ and $\beta$ spins).

```python
import numpy as np
from itertools import combinations
from math import factorial

def determinants(n_elec, n_orb):
    """Yield all α- and β-string pairs (D_alpha, D_beta) with n_elec electrons."""
    orbs = list(range(n_orb))
    for da in combinations(orbs, n_elec // 2):
        for db in combinations(orbs, n_elec - n_elec // 2):
            yield da, db

def hamiltonian_matrix(int1e, int2e, n_elec, n_orb):
    """Build the second-quantised Hamiltonian in the determinant basis."""
    dets = list(determinants(n_elec, n_orb))
    dim  = len(dets)
    H    = np.zeros((dim, dim))
    # ... Slater–Condon rules applied to int1e (one-electron) and
    # int2e (two-electron) integrals. The implementation is a few dozen
    # lines and is the standard exercise in any quantum-chemistry
    # textbook. (Omitted here for brevity — see Helgaker, Jorgensen,
    # Olsen, *Molecular Electronic-Structure Theory*, §11.)
    return H, dets

# int1e, int2e = build_integrals(geometry="H-H-H-H", basis="STO-3G")
# H, dets     = hamiltonian_matrix(int1e, int2e, n_elec=4, n_orb=4)
# evals, _    = np.linalg.eigh(H)
# print("Lowest eigenvalue:", evals[0], "Hartree")
```

For $H_4$ in a minimal basis the full-CI ground state is exact (within
the basis), takes a fraction of a second on a laptop, and is the
calibration point we compare approximate methods against.

> **Warning.** Don't be misled by the small size of this example. A
> 20-electron, 20-orbital problem has $184{,}756$ determinants. A
> 30-electron, 30-orbital problem has $155{,}117{,}520$. A
> 50-electron, 50-orbital problem has $2.7 \times 10^{14}$ — the
> number of *seconds* in 9 million years.

## 2.6 Outlook

Two escape routes from the exponential wall:

- **Systematically improvable wavefunctions.** CI, CC, MBPT, FCIQMC,
  selected CI, DMRG, tensor networks. Each has a regime where it
  works and a regime where it doesn't. We won't pursue these further
  in these notes.
- **Density-functional reformulation.** Throw out the wavefunction,
  reformulate the problem in terms of $\rho(\mathbf r)$, and accept
  that the *functional* is unknown. This is the path DFT takes, and
  it's the subject of the rest of these notes.

> Next: [chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) —
> Hartree–Fock, the *mean-field* starting point that all of DFT lives
> on top of.
