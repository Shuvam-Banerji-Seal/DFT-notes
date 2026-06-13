---
layout: page
title: "Chapter 04 — Kohn–Sham DFT"
permalink: /dft-notes/chapter-04/
description: >-
  The Hohenberg–Kohn existence theorem, the Kohn–Sham practical
  reformulation, and the self-consistent loop that powers every
  production DFT code.
keywords: "Hohenberg-Kohn, Kohn-Sham, density functional, SCF, XC"
---

# Chapter 04 — Kohn–Sham DFT

> Kohn–Sham DFT replaces an unknown *wavefunction* with an unknown
> *density functional*. The reformulation is exact; the approximation
> is the functional. The whole of modern DFT is the search for better
> functionals.

## 4.1 The Hohenberg–Kohn theorems

The 1964 paper by Hohenberg and Kohn contains two theorems.

**Theorem 1 (existence).** For any non-degenerate ground state of a
system of $N$ electrons in an external potential $v_\text{ext}(\mathbf r)$,
the external potential is a unique functional of the ground-state
electron density $\rho(\mathbf r)$, up to an additive constant.

**Corollary.** Every observable of the ground state is a functional of
$\rho$ alone. In particular, the ground-state energy is

$$
E[\rho] = \underbrace{F_\text{HK}[\rho]}_\text{universal} + \int \rho(\mathbf r) v_\text{ext}(\mathbf r) d\mathbf r,
$$

where $F_\text{HK}[\rho] = \langle \hat T \rangle + \langle \hat U_{ee} \rangle$
is a *universal* functional — the same for every system — and only
$v_\text{ext}$ carries the system-specific information.

**Theorem 2 (variational principle).** For any trial density
$\tilde\rho$ that integrates to $N$ and is $v$-representable,

$$
E_0 \le E[\tilde\rho].
$$

> **Tip.** The "v-representability" assumption in Theorem 2 is a
> technical restriction. It is rarely the binding constraint in
> practice, but it matters for some formal proofs of the
> Kohn–Sham equations.

The two theorems together reduce the problem of finding the ground-
state energy of an interacting $N$-electron system to the problem of
*minimising a functional over all admissible densities*. The catch:
$F_\text{HK}[\rho]$ is unknown.

## 4.2 The Kohn–Sham ansatz

Kohn and Sham's 1965 observation is that the *minimisation problem* is
much easier if we *introduce* a fictitious non-interacting reference
system whose density equals the interacting density. The reference
system lives in an **effective potential** $v_\text{eff}(\mathbf r)$
defined by

$$
v_\text{eff}(\mathbf r) = v_\text{ext}(\mathbf r) + v_\text{H}[\rho](\mathbf r) + v_\text{xc}[\rho](\mathbf r).
$$

The Kohn–Sham orbitals $\{\phi_i\}$ are the eigenfunctions of the
Kohn–Sham Hamiltonian

$$
\hat H_\text{KS} = -\frac{1}{2} \nabla^2 + v_\text{eff}(\mathbf r),
$$

and the density is reconstructed from the occupied orbitals as

$$
\rho(\mathbf r) = 2 \sum_{i=1}^{N/2} \lvert \phi_i(\mathbf r) \rvert^2.
$$

The factor of 2 is for spin-paired (restricted) systems.

The Kohn–Sham energy functional reads

$$
E_\text{KS}[\rho] = T_s[\rho] + \int \rho v_\text{ext} \, d\mathbf r + J[\rho] + E_\text{xc}[\rho],
$$

where $T_s$ is the **non-interacting** kinetic energy (which we *can*
compute from the orbitals) and $E_\text{xc}$ absorbs everything we
don't know how to compute:

$$
E_\text{xc}[\rho] = (T - T_s) + (U_{ee} - J) = \text{exchange} + \text{correlation} + \text{kinetic correction}.
$$

## 4.3 Why the reformulation is exact

It is worth pausing to emphasise: the Kohn–Sham equations are *exact*
given the exact $E_\text{xc}$. The error budget of a DFT calculation
is *entirely* in the approximation to $E_\text{xc}[\rho]$.

| Quantity                   | How we get it                                                         | Error source |
|:---------------------------|:----------------------------------------------------------------------|:-------------|
| $T_s[\rho]$               | Sum of occupied orbital kinetic energies — exact by construction       | None         |
| $\int \rho v_\text{ext}$   | One-electron integral over the basis                                   | Basis only   |
| $J[\rho]$                  | Coulomb integral of the density — exact                               | None         |
| $E_\text{xc}[\rho]$        | **Approximated.** This is the only place the error lives.             | Functional   |

> **Warning.** It is tempting to read "DFT" as a mean-field theory like
> Hartree–Fock. It is not. The KS equations are *exact* in the sense
> that the *form* of the energy expression is exact; the *value* of
> $E_\text{xc}$ is approximate. Calling DFT a "mean-field theory" is
> the most common conceptual error in introductory DFT.

## 4.4 The KS self-consistent loop

The KS equations have the same self-referential structure as HF: the
potential depends on the orbitals, and the orbitals are eigenfunctions
of the potential. The SCF procedure is identical in shape:

```python
import numpy as np

def ks_scf(H_core, eri, S, n_elec, v_xc, max_iter=100, tol=1e-7, mixing=0.3):
    """Restricted KS-SCF in a non-orthogonal AO basis.

    H_core : (K, K)  one-electron Hamiltonian
    eri    : (K, K, K, K) electron-repulsion integrals
    S      : (K, K)  overlap matrix
    n_elec : int      number of electrons
    v_xc   : callable  v_xc(rho_grid, density_matrix) -> F_xc on the grid
    """
    K = H_core.shape[0]
    evals, C = np.linalg.eigh(H_core, S)
    P = 2 * C[:, : n_elec // 2] @ C[:, : n_elec // 2].T

    for it in range(max_iter):
        # Hartree potential
        J = np.einsum("pqrs,rs->pq", eri, P)
        # Exchange–correlation potential, evaluated on the grid
        F_xc = v_xc(rho_grid=None, P=P)   # signature depends on the XC code
        # Fock-like matrix
        F = H_core + J + F_xc

        evals, C = np.linalg.eigh(F, S)
        P_new = 2 * C[:, : n_elec // 2] @ C[:, : n_elec // 2].T
        dP = np.linalg.norm(P_new - P)
        P  = (1 - mixing) * P + mixing * P_new
        if dP < tol:
            print(f"  Converged in {it + 1} iterations (ΔP = {dP:.2e})")
            break

    E = 0.5 * np.trace(P @ (H_core + F))
    return E, evals, C, P
```

The structure is the same as HF; the only thing that changes is the
$\hat K$ term being replaced by a local (in the DFT case) or
semi-local (in the hybrid case) $\hat v_\text{xc}$ contribution.

## 4.5 The Jacobian of approximations to $E_\text{xc}$

Approximations to $E_\text{xc}[\rho]$ are conventionally organised
into a "Jacob's ladder" of increasing complexity and (usually)
increasing accuracy:

| Rung | Approximation                  | Form of $E_\text{xc}$                                                | Cost        |
|:-----|:-------------------------------|:----------------------------------------------------------------------|:------------|
| 1    | LDA (local)                    | $\int \rho(\mathbf r) \, \varepsilon_\text{xc}(\rho(\mathbf r))\, d\mathbf r$ | $O(K)$      |
| 2    | GGA (semi-local)              | + $\int f(\rho, \nabla\rho)\, d\mathbf r$                              | $O(K)$      |
| 3    | Meta-GGA                       | + $\int g(\rho, \nabla\rho, \tau)\, d\mathbf r$                        | $O(K)$      |
| 4    | Hybrid                         | + fraction of exact HF exchange                                       | $O(K^4)$    |
| 5    | Range-separated hybrid        | + range-separation of exchange                                        | $O(K^4)$    |
| 6    | Double-hybrid                 | + MP2-like correlation from KS orbitals                               | $O(K^5)$    |
| 7    | Random-phase approximation     | + exact (adiabatic) exchange + ring-Coulomb correlation              | $O(K^4)$    |

> **Tip.** "Higher rung" does not mean "always better". The LDA is
> surprisingly good for simple metals and is often the cheapest,
> most robust choice for screening crystal structures. A bad hybrid
> can be much worse than a good GGA on the same system.

## 4.6 What we have bought

The Kohn–Sham reformulation has reduced an exponentially hard problem
to a *cubic*-in-basis-size problem (HF-like) with a *local* or
*semi-local* potential that is much cheaper to apply than the
non-local HF exchange. The price is that we don't know the
exchange–correlation functional exactly, and we have to settle for an
approximation.

The next chapter is a tour of the approximations.

> Next: [chapter 05]({{ "/dft-notes/chapter-05/" | relative_url }}) —
> the practical zoo of XC functionals, and how to pick one.
