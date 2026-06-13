---
layout: page
title: "Chapter 03 — Hartree–Fock"
permalink: /dft-notes/chapter-03/
description: >-
  Mean-field theory: the Fock operator, the self-consistent field
  iteration, and the limits of a single-determinant Ansatz.
keywords: "Hartree-Fock, Fock operator, SCF, mean-field, Roothaan"
---

# Chapter 03 — Hartree–Fock

> Hartree–Fock is not a particularly good theory of electronic
> structure. It is, however, the theory that defines the vocabulary
> every later method is forced to speak.

## 3.1 The variational principle

The first Hohenberg–Kohn theorem (which we'll meet properly in chapter
04) is the **variational principle**: for any normalised trial
wavefunction $\tilde\Psi$, the energy is bounded below by the exact
ground-state energy,

$$
E_0 \le \langle \tilde\Psi \rvert \hat H \rvert \tilde\Psi \rangle.
$$

Hartree–Fock is the **best single-determinant** Ansatz. It picks the
determinant that minimises the energy over the manifold of Slater
determinants. The minimum is the **Hartree–Fock energy** $E_\text{HF}$;
the determinant that achieves it is the **HF wavefunction** $\Psi_\text{HF}$.

## 3.2 The Fock operator

The variation gives a one-electron eigenvalue equation. In a
spin-orbital basis $\{\chi_p\}$ it reads

$$
\hat F \, \chi_p = \varepsilon_p \, \chi_p,
$$

with the **Fock operator**

$$
\hat F = \hat h + \hat J[\rho] + \hat K[\rho].
$$

The three terms are the one-electron part (kinetic + external
potential), the **Coulomb** (Hartree) operator built from the
self-consistent density, and the **exchange** operator, which has no
classical analogue.

> **Tip.** The exchange operator $\hat K$ is *non-local*: applying it
> to $\chi_p(\mathbf x)$ requires the value of $\chi_q$ at every
> point in space, weighted by the density. This is what makes HF
> expensive and what makes the local approximation of DFT so
> attractive.

## 3.3 The self-consistent field

The Fock operator depends on the orbitals (via the density), and the
orbitals are eigenfunctions of the Fock operator. We resolve the
circularity by **iteration**:

1. Start from a guess for the density $\rho^{(0)}$.
2. Build the Fock matrix $F^{(n)}$ from $\rho^{(n)}$.
3. Diagonalise $F^{(n)}$ to get new orbitals and a new density
   $\rho^{(n+1)}$.
4. Mix $\rho^{(n)}$ and $\rho^{(n+1)}$ for numerical stability.
5. Check convergence. If not converged, go to step 2.

A minimal SCF loop in Python (using a pre-built one-electron Hamiltonian
and two-electron integrals):

```python
import numpy as np

def scf_loop(H_core, eri, S, n_elec, max_iter=100, tol=1e-8, mixing=0.3):
    """Restricted HF SCF in a non-orthogonal AO basis.

    H_core : (K, K)  one-electron Hamiltonian in the AO basis
    eri    : (K, K, K, K) two-electron integrals (physicists' notation)
    S      : (K, K)  overlap matrix
    n_elec : int      number of electrons
    """
    K = H_core.shape[0]
    # Initial guess: diagonalise the core Hamiltonian
    evals, C = np.linalg.eigh(H_core, S)
    P = 2 * C[:, : n_elec // 2] @ C[:, : n_elec // 2].T

    for it in range(max_iter):
        # Build the Fock matrix
        J = np.einsum("pqrs,rs->pq", eri, P)
        K = np.einsum("prqs,rs->pq", eri, P)
        F = H_core + J - 0.5 * K

        # Transform to the orthogonal basis and diagonalise
        evals, C = np.linalg.eigh(F, S)

        # New density
        P_new = 2 * C[:, : n_elec // 2] @ C[:, : n_elec // 2].T

        # Check convergence and mix
        dP = np.linalg.norm(P_new - P)
        P  = (1 - mixing) * P + mixing * P_new
        if dP < tol:
            print(f"  Converged in {it + 1} iterations (ΔP = {dP:.2e})")
            break
    else:
        print(f"  WARNING: SCF did not converge in {max_iter} iterations")

    E_elec = 0.5 * np.trace(P @ (H_core + F))
    return E_elec, evals, C, P
```

The call `np.einsum` is doing what a real quantum-chemistry code does
in its innermost loop. In production, the ERI tensor is recomputed on
the fly and never stored.

> **Warning.** Plain density mixing is enough for stable closed-shell
> molecules. Open-shell, near-degenerate, or metallic systems need
> **level-shifting**, **DIIS** (direct inversion in the iterative
> subspace), or both. Adding DIIS to the snippet above is a 20-line
> exercise and a real rite of passage.

## 3.4 The Slater–Condon rules

The matrix elements of $\hat H$ between two Slater determinants
$\lvert \Phi_I \rangle$ and $\lvert \Phi_J \rangle$ are given by the
**Slater–Condon rules**. For our purposes the only cases we need are:

| Case                                                  | $\langle \Phi_I \rvert \hat H \rvert \Phi_J \rangle$                                |
|:------------------------------------------------------|:-------------------------------------------------------------------------------------|
| $I = J$                                               | $\sum_i h_{ii} + \frac{1}{2} \sum_{ij} (J_{ij} - K_{ij})$                             |
| $I$, $J$ differ by a single spin-orbital              | $h_{ab} + \sum_j ( \langle ab \rvert jj \rangle - \langle aj \rvert bj \rangle )$    |
| $I$, $J$ differ by two spin-orbitals                  | $\langle ab \rvert cd \rangle - \langle ab \rvert dc \rangle$                        |
| $I$, $J$ differ by three or more spin-orbitals        | 0                                                                                    |

These are the rules that make quantum-chemistry codes possible. They
say the Hamiltonian is a **2-body** operator in second quantisation,
and its matrix in the determinant basis is **sparse enough** to be
handled by iterative methods.

## 3.5 What Hartree–Fock gets wrong

The difference between the exact energy and the HF energy is the
**correlation energy**:

$$
E_\text{corr} = E_\text{exact} - E_\text{HF}.
$$

A useful operational definition: HF is exact for any one-electron
system and wrong for any multi-electron system. The error is, in some
sense, *the price of being a single determinant*. Typical magnitudes:

| System class                             | $E_\text{corr}$ (Hartree/electron)        |
|:-----------------------------------------|:------------------------------------------|
| He atom                                  | $\sim 0.04$                               |
| Ne atom                                  | $\sim 0.32$                               |
| H$_2$O molecule                          | $\sim 0.30$ (total $\sim 0.9$)             |
| Benzene                                  | $\sim 0.4$ (per C)                        |
| A transition-metal complex               | $\sim 1$–$3$ (per atom, depending on state) |

> **Note.** These are *absolute* errors, not per-cent. The HF energy
> is roughly $-100$ Hartree for a small organic molecule, and the
> correlation correction is roughly $+1$ Hartree. Chemists care about
> *energy differences* — reaction energies, barrier heights, binding
> energies — and these are often on the order of milli-Hartree, so a
> one-Hartree absolute error is utterly unacceptable for chemistry
> and utterly fine for solid-state physics. The two communities
> measure success differently.

## 3.6 Why DFT builds on HF

The Fock operator is the prototypical **mean-field** operator: each
electron moves in the average field of all the others. The HF energy
expression is also the template that every later theory copies:

$$
E = \underbrace{\langle T \rangle}_\text{kinetic} + \underbrace{\langle V_\text{ext} \rangle}_\text{external} + \underbrace{\langle J \rangle}_\text{Coulomb} + \underbrace{E_\text{non-classical}}_\text{remainder}.
$$

In HF, $E_\text{non-classical}$ is the exchange energy $-K$. In DFT,
it becomes the exchange–correlation energy $E_\text{xc}$ — a *density
functional* we don't know exactly but can approximate. The arithmetic
is the same. The semantics are not.

## 3.7 Outlook

DFT replaces the unknown exact wavefunction by an unknown exact *energy
functional of the density*. Hartree–Fock is the *Ansatz* that DFT
rejects at the level of the wavefunction but reuses at the level of
the *orbital structure*: a single Slater determinant of Kohn–Sham
orbitals is the starting point of the most common family of DFT
calculations.

> Next: [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) —
> the Hohenberg–Kohn theorems and the Kohn–Sham equations, where the
> unknown functional is hidden.
