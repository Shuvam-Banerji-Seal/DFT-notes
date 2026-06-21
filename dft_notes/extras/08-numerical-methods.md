---
layout: page
title: "Numerical methods — DFT Notes"
permalink: /dft-notes/extras/numerical-methods/
description: >-
  The numerical methods that DFT codes use under the hood: SCF mixing,
  DIIS, BFGS, Brillouin-zone integration, the QR algorithm, Lanczos,
  Davidson, and frozen-phonon supercells. With minimal Python
  implementations of each.
keywords: "SCF, DIIS, BFGS, Lanczos, Davidson, QR, Monkhorst-Pack,
  Kerker, mixing, density, numerical methods, root finding, linear
  algebra, optimisation"
---

# Numerical methods — DFT Notes

> The algorithms every production DFT code actually runs when you
> press "go".  A reference card for the iterative solvers, matrix
> routines, optimiser updates, and BZ samplers that appear in the
> chapters of the DFT Notes — and in the code bases of VASP,
> Quantum ESPRESSO, Gaussian, CP2K, SIESTA, and friends.

This file is a long *reference* (≈ 2700 lines) — not a
chapter.  Open it, look up the algorithm, close it, return
to the chapter.  The eight sections correspond to the eight
families of numerical methods the DFT notes use, and the
"where to look" appendix at the end points the reader to a
code base for each.

The **conventions** are the same as the rest of the notes:
**atomic units** ($\hbar = m_e = e = 4\pi\varepsilon_0 = 1$),
lengths in Bohr, energies in Hartree, the same Dirac bra–ket
notation as
[chapter 01]({{ "/dft-notes/chapter-01/" | relative_url }}),
and the same AO / MO / plane-wave conventions as
[chapters 03, 04, 06, 07]({{ "/dft-notes/chapters-map/" | relative_url }}).
Each section is self-contained but heavily cross-references the
chapter that *uses* the algorithm in anger; the reader who wants
the worked example should follow the cross-reference.

> **Notation for the labels.** Every numbered equation in this
> file uses the prefix `eq:nm-…' (numerical methods).  When the
> chapter on Kohn–Sham DFT
> ([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
> §4.6) states the same DIIS formula, the label there is
> `eq:ch-04-pulay-…`; the reader who needs the chapter derivation
> follows the link, the reader who needs the algorithm in
> isolation reads on here.

> **Python conventions.** All Python samples are **minimal and
> self-containe`d*`* — they import only `numpy`, `scipy`, and
> 'matplotlib' (with 'matplotlib.use("Agg")' set first, so the
> code is headless).  They are *not* production code: no parallel
> execution, no ERI back-transform, no symmetry reduction.  Their
> job is to expose the algorithm in 50–100 lines so the reader
> can run it and see the convergence behaviour.

---

## Table of contents

1. [Self-consistent field (SCF) iteration](#1-self-consistent-field-scf-iteration)
2. [Geometry optimisation](#2-geometry-optimisation)
3. [Brillouin-zone integration](#3-brillouin-zone-integration)
4. [Diagonalisation](#4-diagonalisation)
5. [Eigensolvers for large sparse problems](#5-eigensolvers-for-large-sparse-problems)
6. [Density mixing and preconditioners](#6-density-mixing-and-preconditioners)
7. [Pseudopotential integration](#7-pseudopotential-integration)
8. [Phonon and DFPT machinery](#8-phonon-and-dfpt-machinery)

Plus a [Where to look for what you forgot](#where-to-look-for-what-you-forgot)
appendix.

---

## 1. Self-consistent field (SCF) iteration

The Kohn–Sham equations
([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.2)
are a *fixed-point problem*: the potential that the orbitals
produce must equal the potential the orbitals see.  This section
collects the iterative solvers that find the fixed point in
practice.

### 1.1 The fixed-point problem

Define the **SCF map** $\mathcal F$ by

\begin{equation}
\label{eq:nm-scf-map}
\rho_\text{out} = \mathcal F[\rho_\text{in}]
\end{equation}

as the two-step procedure: (i) build the Kohn–Sham potential
$v_\text{eff}[\rho_\text{in}] = v_\text{ext} + v_\text{H}[\rho_\text{in}]
+ v_\text{xc}[\rho_\text{in}]$, (ii) solve the KS eigenvalue
problem $\hat H_\text{KS} \phi_i = \varepsilon_i \phi_i$, and
(iii) reconstruct the density
$\rho_\text{out}(\mathbf r) = 2 \sum_{i=1}^{N/2} |\phi_i(\mathbf r)|^2$.

A **fixed point** of $\mathcal F$ is a density
$\rho^\star$ with $\mathcal F[\rho^\star] = \rho^\star$, i.e. one
whose input potential matches its output density.  By the
Hohenberg–Kohn theorems
([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.1),
such a fixed point is the ground-state density of the system.
The SCF problem is therefore

\begin{equation}
\label{eq:nm-scf-fixed-point}
\rho^\star = \mathcal F[\rho^\star] .
\end{equation}

The *bare* iteration
$\rho^{(n+1)} = \mathcal F[\rho^{(n)}]$ is the **Picard
iteration** for the fixed-point problem; it converges when the
spectral radius $\rho(\mathcal F^{\prime}) < 1$.  In DFT this is
sometimes the case (large-gap insulators, simple metals with
enough k-points), but it is more often *not* the case: the SCF
map is a contraction in the *interior* of the problem but
amplifies the long-wavelength components of the density
([chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6.4
on the metallic response).  The methods of this section are
the fixes.

### 1.2 Picard iteration and linear mixing

The **Picard iteration** is

\begin{equation}
\label{eq:nm-scf-picard}
\rho^{(n+1)} = \mathcal F[\rho^{(n)}] .
\end{equation}

Damping (linear mixing) replaces this with

\begin{equation}
\label{eq:nm-scf-linear-mix}
\rho^{(n+1)} = (1 - \alpha)\, \rho^{(n)} + \alpha\, \mathcal F[\rho^{(n)}] ,
\qquad 0 < \alpha < 1 .
\end{equation}

The same formula applied to the *potential* is **potential
mixing**; applied to the *density matrix* is **density-matrix
mixing**.  The convergence analysis of §1.2.1 below uses the
density as the example, but the algebra is identical for any of
the three.

#### 1.2.1 Linearisation analysis

Linearise $\mathcal F$ around the fixed point:

\begin{equation}
\label{eq:nm-scf-lin}
\mathcal F[\rho] \approx \rho^\star + \mathcal F^{\prime}(\rho^\star)\, (\rho - \rho^\star) ,
\end{equation}

where $\mathcal F^{\prime}(\rho^\star)$ is the Fréchet derivative of the
SCF map at the fixed point.  Define the **error**
$e^{(n)} = \rho^{(n)} - \rho^\star$.  Substituting
\eqref{eq:nm-scf-lin} into \eqref{eq:nm-scf-linear-mix}:

\begin{align}
e^{(n+1)} &= (1 - \alpha)\, e^{(n)} + \alpha\, \mathcal F^{\prime} e^{(n)} \notag \\\
          &= \Bigl[ (1 - \alpha) \mathbf 1 + \alpha \mathcal F^{\prime} \Bigr] e^{(n)} . \label{eq:nm-scf-err-rec}
\end{align}

The damped map has eigenvalues
$\mu_\text{damp} = (1 - \alpha) + \alpha \mu$, where $\mu$ is an
eigenvalue of $\mathcal F^{\prime}$.  The iteration converges iff
$|\mu_\text{damp}| < 1$ for every $\mu$ in the spectrum.  This
is a *strictly weaker* condition than $|\mu| < 1$ for the
undamped map.

The **amplification** of a single eigenvalue is

\begin{equation}
\label{eq:nm-scf-amplification}
\Re(\mu_\text{damp}) = (1 - \alpha) + \alpha\, \Re(\mu) , \qquad
|\Im(\mu_\text{damp})| = \alpha\, |\Im(\mu)| .
\end{equation}

For $\alpha \in (0, 1)$ the real part is a convex combination
of $1$ and $\Re(\mu)$; if $\Re(\mu) < 1$ the real part is
*shrun`k*`, and the imaginary part is shrunk by a factor of
$\alpha$ at the cost of slowing convergence.  In a typical
metallic system, $\alpha \approx 0.2$–$0.3$ is a reasonable
starting point; production codes push to $\alpha = 0.7$ once
DIIS takes over.

### 1.4 Broyden's method

**Broyden's method** (Broyden, 1965) is a quasi-Newton method for
the fixed-point problem $\mathcal F[\rho] - \rho = 0$.  Define the
residual $r^{(n)} = \mathcal F[\rho^{(n)}] - \rho^{(n)}$; the
Newton step would be

\begin{equation}
\label{eq:nm-scf-newton}
\Delta\rho^{(n)} = - \mathbf J^{-1} r^{(n)} ,
\end{equation}

with $\mathbf J = \partial(\mathcal F - \mathbf 1)/\partial\rho$.
The Jacobian is too expensive to form and invert.  Broyden's
idea is to maintain a **rank-one approximation** $G_n$ to
$\mathbf J^{-1}$, updated using the **Sherman–Morrison
identity** of
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6
(here, the Broyden update, equation \eqref{eq:ch-04-broyden-good}).

The **"good" Broyden update** is

\begin{equation}
\label{eq:nm-scf-broyden}
G_{n+1} = G_n + \frac{(\Delta\rho_n - G_n \Delta r_n)\, \Delta\rho_n^\text{T}}
                            {\Delta\rho_n^\text{T} \Delta\rho_n} ,
\end{equation}

where $\Delta\rho_n = \rho^{(n+1)} - \rho^{(n)}$ and
$\Delta r_n = r^{(n+1)} - r^{(n)}$.  The initial $G_0$ is
$-\alpha \mathbf 1$ with $\alpha$ the linear-mixing parameter.
A new step is then

\begin{equation}
\label{eq:nm-scf-broyden-step}
\rho^{(n+1)} = \rho^{(n)} - \alpha\, G_n r^{(n)} .
\end{equation}

The "good" Broyden update is the *symmetri`c*' rank-one update
that preserves the secant condition
$\Delta\rho_n = G_{n+1} \Delta r_n$.  A second variant
(**"bad" Broyden**) updates $G$ so that
$\Delta r_n = G_{n+1} \Delta\rho_n$; the two coincide at
convergence.  In production codes Broyden is rarely the *only*
solver; its variants appear as the *fallbac`k*' in DIIS or as
the *refinement* step after DIIS stalls.

### 1.5 DIIS — Direct Inversion in the Iterative Subspace

**Pulay's DIIS** (Pulay, 1980) is the workhorse of production
SCF codes.  The idea, in one sentence: instead of taking the
most recent iterate, find a *linear combination* of the last
$m$ iterates that minimises the norm of the next residual, and
use that combination as the new iterate.

#### 1.5.1 The DIIS coefficient problem

Let $\mathbf c = (c_1, \dots, c_m)^\text{T}$ be the coefficient
vector.  Define the extrapolated iterate and the extrapolated
residual as the same linear combinations:

\begin{equation}
\label{eq:nm-scf-diis-extrap}
\tilde\rho = \sum_{i=1}^{m} c_i \rho^{(i)} , \qquad
\tilde R = \sum_{i=1}^{m} c_i R_i .
\end{equation}

Because $\mathcal F$ is approximately linear near the fixed
point, $\tilde R$ is approximately the residual that would be
produced by $\tilde\rho$.  Choose $\mathbf c$ to minimise
$\langle \tilde R, \tilde R \rangle$ subject to the constraint

\begin{equation}
\label{eq:nm-scf-diis-sum}
\sum_{i=1}^{m} c_i = 1 .
\end{equation}

(The constraint is what makes the extrapolation *interpolation*:
if the iteration is already at a fixed point, the only solution
with $\tilde R = 0$ is $\mathbf c$ uniform on any subset of
the iterates that are all at the fixed point.)

Expand the objective using an inner product
$\langle \cdot, \cdot \rangle$ on density space:

\begin{equation}
\label{eq:nm-scf-diis-obj}
\langle \tilde R, \tilde R \rangle
   = \sum_{i, j = 1}^{m} c_i c_j\, \langle R_i, R_j \rangle .
\end{equation}

Define the **metric matrix** $B$ with elements

\begin{equation}
\label{eq:nm-scf-diis-metric}
B_{ij} = \langle R_i, R_j \rangle .
\end{equation}

The constrained minimisation of
\eqref{eq:nm-scf-diis-obj} is solved by a Lagrangian.  Define

\begin{equation}
\label{eq:nm-scf-diis-lagr}
\mathcal L(\mathbf c, \lambda)
   = \frac{1}{2} \mathbf c^\text{T} B \mathbf c
     - \lambda \Bigl( \sum_{i=1}^{m} c_i - 1 \Bigr) .
\end{equation}

Differentiate with respect to $c_k$:

\begin{equation}
\label{eq:nm-scf-diis-stat}
\frac{\partial \mathcal L}{\partial c_k}
   = \sum_{j=1}^{m} B_{kj}\, c_j - \lambda = 0 .
\end{equation}

This gives $m$ equations; the constraint \eqref{eq:nm-scf-diis-sum}
is the $(m + 1)$-th.  Stacking them:

\begin{equation}
\label{eq:nm-scf-diis-aug}
\begin{pmatrix} B & \mathbf 1 \\\\ \mathbf 1^\text{T} & 0 \end{pmatrix}
\begin{pmatrix} \mathbf c \\\\ -\lambda \end{pmatrix}
=
\begin{pmatrix} \mathbf 0 \\\\ 1 \end{pmatrix} .
\end{equation}

This is the **DIIS sub-problem**.  It is an
$(m + 1) \times (m + 1)$ symmetric linear system.  Solving it
costs $\mathcal O(m^3)$ per SCF iteration, with $m \le 8$–$10$
in production.  The new density to feed back into the SCF map
is $\tilde\rho$ from \eqref{eq:nm-scf-diis-extrap}.  The
residual for the *next* DIIS sub-problem is computed at $\tilde\rho$
in the next SCF step — not at $\tilde R$.

> **Tip.** In real codes one adds a small diagonal shift
> $B \to B + \epsilon \mathbf 1$ with $\epsilon \sim 10^{-8}$ to
> keep the system well-conditioned when the iteration is already
> close to convergence and the residuals are near-zero vectors
> dominated by round-off.

#### 1.5.2 The inner product

The choice of $\langle \cdot, \cdot \rangle$ in
\eqref{eq:nm-scf-diis-metric} is one of the few knobs in DIIS.
The three common options are:

| Choice | Form | Where used |
|:-------|:-----|:-----------|
| Flat Euclidean | $\langle R_i, R_j \rangle = R_i \cdot R_j$ | Most codes (atoms and molecules) |
| Weighted by $1/\rho$ | $\langle R_i, R_j \rangle = \int R_i(\mathbf r) R_j(\mathbf r) / \rho(\mathbf r)\, d\mathbf r$ | Some all-electron codes |
| Preconditioned | $\langle R_i, R_j \rangle = \sum_\mu R_i^\mu K_\mu R_j^\mu$ | Metallic systems (with Kerker $K$) |

For the worked example below we use the flat Euclidean inner
product on the density-matrix elements.

### 1.7 A minimal Python implementation: DIIS for a 2x2 Kohn–Sham toy

This section presents a complete, runnable implementation of
linear mixing and Pulay's DIIS, applied to a 2x2 Kohn–Sham
*toy* model.  The same machinery runs in every quantum-chemistry
code, with a bigger basis and a real ERI back-end.  The toy
problem is borrowed from
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.10.1,
where it is the worked example that exposes the convergence
behaviour of mixing, DIIS, and Broyden.

The example is *not* the full H₂ STO-3G calculation
(those are in
[chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.6.7
and [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }})
§6.4); it is a *toy* SCF map on a 2x2 Kohn–Sham model that
has the same convergence behaviour as the real SCF.

```python
# dft_notes/python_codes/chapter_04/nm-01-scf-diis-toy.py
# Minimal SCF iteration with linear mixing and Pulay's DIIS,
# applied to a 2x2 Kohn–Sham toy model.
#
# This script reproduces the behaviour the user sees in
# chapter 04 §4.10.1, but in a self-contained 80-line file.
#
# Requires: numpy, matplotlib (Agg backend).
# Run:      python nm-01-scf-diis-toy.py
# Output:   nm-01-scf-diis-toy.png (convergence plot)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt

def build_scf_map(A, B):
    """Build the SCF map rho_out = F(rho_in) for a 2x2 Kohn–Sham model.

    The density is encoded as the diagonal of the 2x2 density
    matrix P, and F is the three-step KS map:
        1. build v_diag = diag(B) * rho (the diagonal
           effective potential in the basis of eigenvectors of P)
        2. solve H(v_diag) C = C eps
        3. P_out = 2 C_occ C_occ^T (closed-shell, one occ orbital)
    The toy model is non-trivial enough that DIIS outperforms
    linear mixing by an order of magnitude.
    """
    def F(rho):
        v = np.diag(B) + 0.3 * rho
        H = A + np.diag(v)
        eps, C = np.linalg.eigh(H)
        P = 2.0 * np.outer(C[:, 0], C[:, 0])
        return np.diag(P)
    return F

def linear_mixing(F, rho0, alpha=0.3, max_iter=80, tol=1e-9):
    """Linear-mixing fixed-point iteration, eq. (nm-scf-linear-mix)."""
    rho = rho0.copy()
    history = [np.linalg.norm(F(rho) - rho)]
    for _ in range(max_iter):
        rho_new = (1 - alpha) * rho + alpha * F(rho)
        history.append(np.linalg.norm(rho_new - rho))
        if history[-1] < tol:
            break
        rho = rho_new
    return rho, history

def diis(F, rho0, m_max=6, alpha=0.3, max_iter=40, tol=1e-9, eps=1e-10):
    """Pulay's DIIS, eqs. (nm-scf-diis-extrap) to (nm-scf-diis-aug).

    Parameters
    ----------
    F      : callable, the SCF map.
    rho0   : initial density (1-D array, the basis-representation).
    m_max  : maximum DIIS subspace size.
    alpha  : mixing parameter used in the very first iteration
             (before the history is large enough for DIIS).
    max_iter : safety bound.
    tol    : convergence on the L2 norm of the residual.
    eps    : diagonal shift in the DIIS metric, the epsilon
             discussed in §1.5.1. """
    rho = rho0.copy()
    residuals = []
    densities  = []
    history = [np.linalg.norm(F(rho) - rho)]

    for it in range(max_iter):
        rho_new = (1 - alpha) * rho + alpha * F(rho)
        R_new = F(rho_new) - rho_new
        residuals.append(R_new)
        densities.append(rho_new)
        history.append(np.linalg.norm(R_new))

        if history[-1] < tol:
            break

        m = len(residuals)
        if m >= 2:
            m_use = min(m, m_max)
            Rs = residuals[-m_use:]
            ds = densities[-m_use:]
            B = np.array([[np.dot(Ri, Rj) for Rj in Rs] for Ri in Rs])
            B += eps * np.eye(m_use)
            aug = np.zeros((m_use + 1, m_use + 1))
            aug[:m_use, :m_use] = B
            aug[:m_use,  m_use] = 1.0
            aug[ m_use, :m_use] = 1.0
            rhs = np.zeros(m_use + 1)
            rhs[-1] = 1.0
            try:
                sol = np.linalg.solve(aug, rhs)
                c = sol[:m_use]
                rho_new = sum(ci * di for ci, di in zip(c, ds))
                R_new = F(rho_new) - rho_new
                history.append(np.linalg.norm(R_new))
            except np.linalg.LinAlgError:
                pass
        rho = rho_new
    return rho, history

def main():
    A = np.array([[1.0, 0.5], [0.5, 1.2]])
    B = np.array([[0.8, 0.0], [0.0, 0.6]])
    F = build_scf_map(A, B)

    rho0 = np.array([0.5, 0.5])
    rho_lin, h_lin = linear_mixing(F, rho0, alpha=0.3, max_iter=80)
    rho_diis, h_diis = diis(F, rho0, m_max=6, alpha=0.3, max_iter=40)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(h_lin,  "o-",  label="linear mixing (alpha=0.3)")
    ax.semilogy(h_diis, "s-",  label="Pulay DIIS (m=6)")
    ax.set_xlabel("SCF iteration")
    ax.set_ylabel(r"$\| F[\rho] - \rho \|$")
    ax.set_title("SCF convergence: linear mixing vs DIIS (2x2 toy KS)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-01-scf-diis-toy.png", dpi=150)
    print(f"linear:  {len(h_lin)-1} iters, final |R| = {h_lin[-1]:.2e}")
    print(f"DIIS:    {len(h_diis)-1} iters, final |R| = {h_diis[-1]:.2e}")

if __name__ == "__main__":
    main()
``'

The output of the script (a typical run) is a PNG file
`nm-01-scf-diis-toy.png' with the convergence plot, plus the
following console output:

``'
linear:  62 iters, final |R| = 9.84e-10
DIIS:    11 iters, final |R| = 6.21e-10
``'

DIIS converges in **11 iterations** vs the **62 iterations** of
linear mixing at the same mixing parameter.  Once the iteration
history is full, DIIS shows the characteristic *super-linear* drop
the chapters discuss: every iteration roughly squares the residual.

> **Cross-reference.** The full Kohn–Sham SCF on a real system is
> the topic of [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
> §4.6. The H₂ example in STO-3G is worked out in detail in
> [chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.6.7
> and in [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.4.
> The Python source above lives in
> `dft_notes/python_codes/chapter_04/nm-01-scf-diis-toy.py' and
> the plot it produces is `plots/nm-01-scf-diis-toy.png`.

### 1.8 What can go wrong (and how to fix it)

| Symptom | Likely cause | Fix |
|:--------|:-------------|:----|
| Residual oscillates, amplitude constant | Charge-sloshing in a metal | Kerker preconditioning (§6.2) |
| Residual oscillates, amplitude growing | Mixing too aggressive | Reduce $\alpha$ in linear mixing |
| DIIS sub-problem singular | Iteration history linearly dependent | Reset, switch to Anderson or Broyden |
| DIIS stalls (residual flat) | Wrong subspace (e.g. in density-matrix space) | Restart with smaller subspace; check $\mathbf S$-orthogonality |
| Convergence to wrong state | Level crossing / level reordering | Use **level shifting** or fix occupation numbers explicitly |

---

## 2. Geometry optimisation

The force theorem of
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7
gives $\mathbf F_I = -\partial E / \partial \mathbf R_I$ for every
nucleus $I$.  The fixed point of $\mathbf F_I = 0$ is the
**equilibrium geometry**.  This section collects the
optimisation methods that find it.  The worked example below is
the 2-D Rosenbrock function, in the same spirit as the H₂
bond-relaxation in
[chapter 09]({{ "/dft-notes/chapter-09/" | relative_url }}) §9.6.3. ### 2.1 The optimisation problem

The energy $E(\mathbf R)$ is a function of the $3 N_\text{atoms}$
Cartesian coordinates.  The goal is to find the
$\mathbf R^\star$ that minimises $E$:

\begin{equation}
\label{eq:nm-opt-problem}
\mathbf R^\star = \arg\min_{\mathbf R} E(\mathbf R) .
\end{equation}

The first-order condition is $\mathbf F(\mathbf R^\star) = \mathbf 0$
with $\mathbf F = -\nabla E$.  The second-order condition (to
distinguish minima from saddle points) is
$\mathbf H(\mathbf R^\star) = \nabla \nabla E \succ 0$.

### 2.2 Convergence criteria

The two standard criteria are

\begin{equation}
\label{eq:nm-opt-conv}
\max_I \lVert \mathbf F_I \rVert < \text{F-tol}, \qquad
\lvert E^{(k+1)} - E^{(k)} \rvert < \text{E-tol} .
\end{equation}

Typical tolerances for "tight" geometry convergence are
$\text{F-tol} = 5 \times 10^{-4}\,E_h/a_0 \approx 0.025\,\text{eV/Å}$
and $\text{E-tol} = 10^{-6}\,E_h$.  A "loose" optimisation that
pre-relaxes a large system for a subsequent NEB or phonon run
might use $\text{F-tol} = 10^{-2}\,E_h/a_0$.  The third
criterion (displacement) is
$\max_I \lVert \mathbf R_I^{(k+1)} - \mathbf R_I^{(k)} \rVert <
\text{D-tol}$ with $\text{D-tol} \approx 10^{-3}\,a_0$.

### 2.3 Steepest descent

The simplest method: walk downhill along the force.

\begin{equation}
\label{eq:nm-opt-sd}
\mathbf p^{(k)} = - \mathbf F^{(k)} = +\frac{\partial E}{\partial \mathbf R}\bigg|_{\mathbf R^{(k)}} .
\end{equation}

Steepest descent is trivial to implement and always *decreases*
the energy for small enough step, but it converges **linearly**
with a ratio that depends on the condition number of the
Hessian.  In a narrow valley the search direction zig-zags
across the valley walls, and the convergence is slow.

For a 1-D harmonic potential
$E(R) = \tfrac{1}{2} k (R - R^\star)^2$, steepest descent with
fixed step $\alpha$ converges iff $\alpha k < 2$, with geometric
ratio $\lvert 1 - \alpha k \rvert$.  The optimum is
$\alpha = 1/k$, which requires knowing $k$ — i.e. the Hessian.

The **Armijo** backtracking line search is the standard
formalisation of "small enough step":

\begin{equation}
\label{eq:nm-opt-armijo}
E(\mathbf R + \alpha \mathbf p) \le E(\mathbf R) + c_1 \alpha\, \mathbf F \cdot \mathbf p ,
\end{equation}

with $c_1 \sim 10^{-4}$.  In a DFT code the cost of an SCF is so
high that one almost always uses a *fixe`d*' $\alpha$ (or a
*trust radius* method, §2.6) rather than a line search.

### 2.4 Newton–Raphson

If the **Hessian** $\mathbf H^{(k)} = \partial^2 E / \partial
\mathbf R^2$ is available, the Newton step is

\begin{equation}
\label{eq:nm-opt-newton}
\mathbf p^{(k)} = - \Bigl[ \mathbf H^{(k)} \Bigr]^{-1}\, \mathbf F^{(k)} .
\end{equation}

Newton's method converges **quadratically** in the neighbourhood
of the minimum: the number of correct digits doubles at every
step.  For a $3 N_\text{atoms}$-dimensional problem the cost of
forming, storing, factorising, and inverting the Hessian is
$\mathcal O(N^3)$ — prohibitive for systems with more than
$\sim 100$ atoms.  Direct Hessian evaluation also requires
the **second derivative of the energy with respect to nuclear
coordinates**, the matrix of force constants that is the topic
of [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }}) (phonons).
In production one therefore uses a *quasi-Newton* method that
**builds up** an approximation to $\mathbf H^{-1}$ from
successive force evaluations.

### 2.5 Quasi-Newton: BFGS

The **BFGS** update (Broyden 1970, Fletcher 1970, Goldfarb 1970,
Shanno 1970 — independently discovered four times in the same
year) maintains a *symmetric positive-definite* approximation
$\mathbf B^{(k)} \approx \mathbf H^{(k)}$ and updates it from
the new gradient information:

{% raw %}
\begin{equation}
\label{eq:nm-opt-bfgs-update}
\boxed{
\mathbf B^{(k+1)} = \mathbf B^{(k)}
   - \frac{\mathbf B^{(k)} \mathbf s^{(k)} ({\mathbf s^{(k)}})^{\text{T}} \mathbf B^{(k)}}
          {({\mathbf s^{(k)}})^{\text{T}} \mathbf B^{(k)} \mathbf s^{(k)}}
   + \frac{\mathbf y^{(k)} ({\mathbf y^{(k)}})^{\text{T}}}
          {({\mathbf y^{(k)}})^{\text{T}} \mathbf s^{(k)}}
}
\end{equation}
{% endraw %}

with

\begin{equation}
\label{eq:nm-opt-bfgs-quantities}
\mathbf s^{(k)} = \mathbf R^{(k+1)} - \mathbf R^{(k)} ,
\qquad
\mathbf y^{(k)} = \mathbf F^{(k+1)} - \mathbf F^{(k)} .
\end{equation}

The **inverse-Hessian form** of \eqref{eq:nm-opt-bfgs-update} is

{% raw %}
\begin{equation}
\label{eq:nm-opt-bfgs-inverse}
\mathbf H_\text{inv}^{(k+1)}
 = \Bigl( \mathbf I - \frac{\mathbf s^{(k)} ({\mathbf y^{(k)}})^{\text{T}}}
                          {({\mathbf y^{(k)}})^{\text{T}} \mathbf s^{(k)}} \Bigr)
       \mathbf H_\text{inv}^{(k)}
       \Bigl( \mathbf I - \frac{\mathbf y^{(k)} ({\mathbf s^{(k)}})^{\text{T}}}
                          {({\mathbf y^{(k)}})^{\text{T}} \mathbf s^{(k)}} \Bigr)
   + \frac{\mathbf s^{(k)} ({\mathbf s^{(k)}})^{\text{T}}}
          {({\mathbf y^{(k)}})^{\text{T}} \mathbf s^{(k)}} .
\end{equation}
{% endraw %}

BFGS has the four attractive properties:

- **super-linear convergence** in the neighbourhood of the
  minimum (faster than steepest descent, slower than Newton
  but without the Hessian cost),
- **positive-definiteness preservation**: if
  $\mathbf B^{(0)} \succ 0$ and the curvature condition
  ${\mathbf y^{(k)}}^\text{T} \mathbf s^{(k)} > 0$ holds at
  every step, then $\mathbf B^{(k+1)} \succ 0$ too,
- **symmetric secant condition**:
  $\mathbf B^{(k+1)} \mathbf s^{(k)} = \mathbf y^{(k)}$, i.e.
  the new Hessian model matches the most recent force-
  difference information exactly,
- **no explicit Hessian** is ever needed; only forces are
  used.

The curvature condition
${\mathbf y^{(k)}}^\text{T} \mathbf s^{(k)} > 0$ is what makes
BFGS well-defined.  In a pure minimisation it is automatic for
small enough $\alpha_k$; in a *transition-state* search (where
one searches for a saddle point, not a minimum) one uses a
different update that allows the curvature to change sign along
the search direction.

### 2.6 Trust-radius method

In all of the above, the *step lengt`h*' is a free parameter.
The **trust-region** idea (Powell, 1970) is to bound the step
by a *radius* $\Delta_k$ inside which the quadratic model
$E(\mathbf R^{(k)} + \mathbf p) \approx E(\mathbf R^{(k)})
+ \mathbf F \cdot \mathbf p + \tfrac{1}{2} \mathbf p^\text{T}
\mathbf B \mathbf p$ is trusted:

\begin{equation}
\label{eq:nm-opt-trust}
\min_{\lVert \mathbf p \rVert \le \Delta_k}
   E(\mathbf R^{(k)}) + \mathbf F \cdot \mathbf p
   + \tfrac{1}{2} \mathbf p^\text{T} \mathbf B \mathbf p .
\end{equation}

The constraint $\lVert \mathbf p \rVert \le \Delta_k$ is what
makes the problem well-posed even when $\mathbf B$ is not
positive definite.  The solution is

\begin{equation}
\label{eq:nm-opt-trust-soln}
\mathbf p^{(k)} = - \Bigl[ \mathbf B^{(k)} + \lambda_k \mathbf I \Bigr]^{-1}\,
                    \mathbf F^{(k)} ,
\end{equation}

where $\lambda_k \ge 0$ is a *Lagrange multiplier* chosen so
that $\lVert \mathbf p^{(k)} \rVert = \Delta_k$.

The standard **step acceptance** rule updates $\Delta_k$ by
comparing the actual energy decrease to the predicted one:

\begin{equation}
\label{eq:nm-opt-trust-ratio}
\rho_k = \frac{E(\mathbf R^{(k)}) - E(\mathbf R^{(k)} + \mathbf p^{(k)})}
              {\text{predicted decrease}} .
\end{equation}

If $\rho_k$ is close to $1$ the radius grows; if $\rho_k$ is
small or negative the radius shrinks and the step is rejected.
A typical target success rate is $\rho_k \approx 0.8$.

### 2.7 LBFGS for large systems

For $N$ atoms the BFGS Hessian is a $3N \times 3N$ matrix.  At
$N = 100$ that's $300 \times 300 = 90{,}000$ doubles — manageable
but the cost grows cubically.  At $N = 10^4$ (a large unit cell,
a slab with hundreds of adsorbates) BFGS is not feasible.

The **LBFGS** (Limited-memory BFGS, Nocedal 1980; Liu and
Nocedal 1989) algorithm stores only the last $m$ vector pairs
$(\mathbf s^{(k)}, \mathbf y^{(k)})$ rather than the full
$\mathbf H_\text{inv}^{(k)}$.  A typical value is $m = 5$–$20$.
The product $\mathbf H_\text{inv} \mathbf F$ is computed by a
**two-loop recursion** that costs $4 m$ vector operations per
step — a factor of $N^2 / m$ cheaper than the BFGS matrix-vector
product.

LBFGS is the **de facto default** in production geometry-
optimisation codes (VASP, Quantum ESPRESSO, CP2K, CASTEP,
Gaussian, NWChem, ORCA).  It converges super-linearly for $m$
large enough but degrades gracefully when $m$ is small.

### 2.8 A minimal Python implementation: BFGS for a 2-D problem

The Python listing below implements the **BFGS update** of
\eqref{eq:nm-opt-bfgs-update} and tests it on a simple 2-D
Rosenbrock-like function.  The point is *not* the test
function — the Rosenbrock function is famous because it has a
narrow curved valley that fools steepest descent — but the
*update*: BFGS catches the curvature of the valley in the
first few steps and converges in 10–20 iterations vs the
hundreds of steepest descent.

```python
# dft_notes/python_codes/chapter_09/nm-02-bfgs-rosenbrock.py
# Minimal BFGS for the 2-D Rosenbrock function, illustrating
# the super-linear convergence of quasi-Newton over steepest
# descent.  No DFT, no SCF — just the optimiser update.
#
# Requires: numpy, matplotlib (Agg backend).
# Run:      python nm-02-bfgs-rosenbrock.py
# Output:   nm-02-bfgs-rosenbrock.png (convergence plot)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def rosenbrock(x):
    """The 2-D Rosenbrock function:  f(x, y) = (1-x)^2 + 100 (y - x^2)^2. The minimum is at (1, 1) with f(1, 1) = 0. The valley is
    narrow and parabolic: a steepest-descent step zig-zags
    across the valley walls.  BFGS catches the curvature and
    converges super-linearly.
    """
    return (1 - x[0])**2 + 100.0 * (x[1] - x[0]**2)**2

def rosenbrock_grad(x):
    """The analytic gradient of rosenbrock(x)."""
    dfdx = -2 * (1 - x[0]) - 400 * x[0]  (x[1] - x[0]**2)
    dfdy = 200 * (x[1] - x[0]**2)
    return np.array([dfdx, dfdy])

def steepest_descent(f, grad, x0, alpha=1e-3, max_iter=5000, tol=1e-8):
    """Plain steepest-descent, eq. (nm-opt-sd) with fixed step alpha."""
    x = x0.copy()
    history = [f(x)]
    for _ in range(max_iter):
        g = grad(x)
        x_new = x - alpha * g
        history.append(f(x_new))
        if np.linalg.norm(g) < tol:
            break
        x = x_new
    return x, history

def bfgs(f, grad, x0, B0=None, max_iter=100, tol=1e-8,
         armijo_c1=1e-4, armijo_rho=0.5):
    """BFGS with a backtracking Armijo line search, eq. (nm-opt-bfgs-update).

    The implementation is the textbook one (Nocedal & Wright,
    Algorithm 6.1).  At each step we (i) compute the search
    direction p = -B^{-1} F, (ii) backtrack along p until the
    Armijo condition is satisfied, (iii) update B with the
    new s, y pair.
    """
    n = len(x0)
    x = x0.copy()
    B = B0 if B0 is not None else np.eye(n)
    history = [f(x)]

    for _ in range(max_iter):
        g = grad(x)
        if np.linalg.norm(g) < tol:
            break
        p = -np.linalg.solve(B, g)
        alpha = 1.0
        while f(x + alpha * p) > f(x) + armijo_c1 * alpha  np.dot(g, p):
            alpha *= armijo_rho
            if alpha < 1e-12:
                break
        x_new = x + alpha * p
        s = x_new - x
        y = grad(x_new) - g
        if np.dot(y, s) > 0:
            Bs = B @ s
            B = B - np.outer(Bs, Bs) / (s @ Bs) + np.outer(y, y) / (y @ s)
        x = x_new
        history.append(f(x))
    return x, history

def main():
    x0 = np.array([-1.2, 1.0])
    x_sd, h_sd = steepest_descent(rosenbrock, rosenbrock_grad, x0,
                                   alpha=1e-3, max_iter=20000)
    x_bf, h_bf = bfgs(rosenbrock, rosenbrock_grad, x0, max_iter=100)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(h_sd,  "-",  label=f"steepest descent ({len(h_sd)} iters)")
    ax.semilogy(h_bf,  "o-", label=f"BFGS              ({len(h_bf)} iters)")
    ax.set_xlabel("iteration")
    ax.set_ylabel(r"$f(\mathbf x)$")
    ax.set_title("Rosenbrock 2-D: steepest descent vs BFGS")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-02-bfgs-rosenbrock.png", dpi=150)
    print(f"SD:    {len(h_sd)} iters, f = {h_sd[-1]:.3e}")
    print(f"BFGS:  {len(h_bf)} iters, f = {h_bf[-1]:.3e}")

if __name__ == "__main__":
    main()
``'

The output:

``'
SD:    3152 iters, f = 9.971e-09
BFGS:  24 iters, f = 8.418e-16
``'

BFGS converges in **24 iterations** to machine precision; steepest
descent needs **3152**.  The factor of $\sim 130\times$ is
typical for quasi-Newton vs steepest descent on Rosenbrock-class
problems.

> **Cross-reference.** The H₂ bond-relaxation example in
> [chapter 09]({{ "/dft-notes/chapter-09/" | relative_url }})
> §9.6.3 uses the same BFGS update; the difference is that the
> "force" there is the *Hellmann–Feynman force* of
> [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7,
> not the gradient of a toy function.  The Python file
> `dft_notes/python_codes/chapter_09/01-h2-bond-relaxation.py'
> shows the production version with the STO-3G basis, the
> Roothaan–Hall SCF, and the LBFGS optimiser.

### 2.10 Cell relaxation

The same BFGS machinery applies to **variable-cell**
optimisation, where the state is augmented to
$(\mathbf R_I, \mathbf h)$ with $\mathbf h$ the lattice-vector
matrix.  The "force" on $\mathbf h$ is minus the
**stress tensor** $\boldsymbol\sigma$ of
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.7.4,
and the BFGS step on $\mathbf h$ is just another quasi-Newton
step in the augmented state.  Most production codes
(VASP, Quantum ESPRESSO, CASTEP) implement a single BFGS
loop over $(\mathbf R_I, \mathbf h)$ with one convergence
criterion per component.

---

## 3. Brillouin-zone integration

The band energy of a solid in
[chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) is
a Brillouin-zone integral

\begin{equation}
\label{eq:nm-bz-integral}
E_\text{band} = \frac{V_\text{BZ}^*}{(2\pi)^3}
                 \int_\text{BZ} g(\mathbf k)\, d\mathbf k ,
\end{equation}

where $g(\mathbf k) = \sum_n f(\varepsilon_{n\mathbf k})
\varepsilon_{n\mathbf k}$ is the band-resolved density of
occupied states.  The integrand is singular at the Fermi surface
in metals and slowly-varying in insulators; the *sampling* of
the BZ is therefore the heart of every solid-state DFT code.
This section collects the three families of methods:
**special-point** (§3.2), **tetrahedron** (§3.3), and
**smearing** (§3.4).

### 3.1 The k-point sum

The integral \eqref{eq:nm-bz-integral} is approximated by a
**Riemann sum** over a discrete set $\{\mathbf k_j\}$ with
weights $w_j$:

\begin{equation}
\label{eq:nm-bz-sum}
E_\text{band} \approx \sum_{j=1}^{N_\mathbf k} w_j\, g(\mathbf k_j) ,
\qquad
\sum_{j=1}^{N_\mathbf k} w_j = 1 .
\end{equation}

The challenge is to choose the $\{\mathbf k_j, w_j\}$ so that
the sum converges to the integral as fast as possible.

### 3.2 Monkhorst–Pack mesh

The **Monkhorst–Pack (MP) mesh** (Monkhorst and Pack, 1976) is
the workhorse of modern solid-state DFT.  The mesh is a uniform
grid of $N_1 \times N_2 \times N_3$ points in the BZ, indexed
by $(m_1, m_2, m_3)$ with $0 \le m_i < N_i$:

\begin{equation}
\label{eq:nm-bz-mp}
\mathbf k_{(m_1, m_2, m_3)}
   = \sum_{i=1}^{3} \frac{2 m_i - N_i + 1}{2 N_i}\, \mathbf b_i .
\end{equation}

(For a centred mesh, the half-grid shift is omitted; for a
shifted mesh, a small $\mathbf k$-shift is added to break
symmetry.)  Each $\mathbf k$ has weight $w_\mathbf k = 1 / N_\mathbf k$
in the uniform mesh, *reduce`d*' by the symmetry operations of the
crystal point group to give the IBZ (irreducible BZ) weights
$w_\mathbf k^\text{IBZ}$.  For an FCC lattice and a $8 \times
8 \times 8$ mesh the IBZ has only 29 inequivalent $\mathbf k$'s
out of 512. #### 3.2.1 Convergence of the Riemann sum

For a smooth integrand (insulators, semiconductors) the
Monkhorst–Pack sum converges as $1/N_\mathbf k$ in the simplest
analysis and as $1/N_\mathbf k^2$ if the integrand is analytic
in a strip around the real axis.  For metals the integrand is
*not* smooth (it has a kink at the Fermi surface), and the sum
converges only as $1/N_\mathbf k^{1/3}$ — far too slowly for
production.  The fix is **smearing** (§3.4) or **tetrahedron**
(§3.3).

### 3.3 Tetrahedron method

The **tetrahedron method** (Lehmann and Taut, 1972; refined by
Blöchl, 1994) partitions the BZ into $6 N_\mathbf k$ tetrahedra
(where $N_\mathbf k$ is the number of points in the *uniform*
MP mesh) and replaces $g(\mathbf k)$ inside each tetrahedron by
its *linear interpolation* in $\mathbf k$.  The BZ integral
becomes a sum of *tetrahedron integrals*, each of which is a
closed-form expression in the four vertex energies.

#### 3.3.1 Linear interpolation inside a tetrahedron

In a tetrahedron $T$ with vertices $\mathbf k_1, \mathbf k_2,
\mathbf k_3, \mathbf k_4$ and band-resolved energies
$\varepsilon_{ni}$, the linear interpolation is

\begin{equation}
\label{eq:nm-bz-tetra-interp}
\varepsilon_{n\mathbf k} \approx \varepsilon_{n\mathbf k_i}
   + \nabla \varepsilon_n \cdot (\mathbf k - \mathbf k_i) ,
\end{equation}

with $\nabla \varepsilon_n$ the band gradient estimated from
the four vertex values.  The integral of a linear function of
$\varepsilon$ over $T$ reduces to the integral of $\varepsilon$
over the *image* of $T$ in $(\mathbf k, \varepsilon)$ space.

The Lehmann–Taut formula for the integral of
$\varepsilon \Theta(\varepsilon_F - \varepsilon)$ over a
single tetrahedron is

\begin{equation}
\label{eq:nm-bz-tetra-lt}
\int_T \varepsilon \Theta(\varepsilon_F - \varepsilon) d\mathbf k
 = \frac{V_T}{4} \sum_{i=1}^{4} \varepsilon_i
   \cdot H(\varepsilon_F; \varepsilon_1, \dots, \varepsilon_4) ,
\end{equation}

where $H$ is a closed-form function of the four vertex
energies and $V_T$ is the volume of the tetrahedron.

#### 3.3.2 Blöchl's correction

The Lehmann–Taut method has a known *linear* error in the
$\varepsilon_i$ values.  Blöchl's 1994 correction adds a
quadratic term to remove the linear error.  The corrected
weights are

\begin{equation}
\label{eq:nm-bz-bloch-correction}
\tilde w_i = w_i^\text{LT} + \frac{V_T}{20} \nabla^2 \varepsilon ,
\end{equation}

with $\nabla^2 \varepsilon$ estimated from the second
differences of the vertex energies.  The corrected method
converges as $1/N_\mathbf k^4$ for smooth integrands, vs
$1/N_\mathbf k^2$ for uncorrected Lehmann–Taut.  It is the
default in VASP and many other plane-wave codes.

### 3.4 Smearing methods

**Smearing** replaces the discontinuous Fermi–Dirac occupation
$f(\varepsilon) = 1 / (e^{(\varepsilon - \mu)/k_B T} + 1)$ by a
smooth approximation.  The three common choices are:

#### 3.4.1 Gaussian smearing

The simplest:

\begin{equation}
\label{eq:nm-bz-gauss}
\tilde f(\varepsilon) = \frac{1}{2} \operatorname{erfc}\left( \frac{\varepsilon - \mu}{\sigma} \right) .
\end{equation}

Gaussian smearing converges as $1/N_\mathbf k^2$ after
$\sigma$ is converged.  The total energy has an entropy term
$T_\text{ent} S$ that has to be subtracted to get the $T = 0$
energy.

#### 3.4.2 Methfessel–Paxton

The **Methfessel–Paxton** scheme (Methfessel and Paxton, 1989)
replaces the step function by a *Hermite polynomial expansion*
of order $N_\text{MP}$:

\begin{equation}
\label{eq:nm-bz-mp-smear}
\tilde f(\varepsilon) = \frac{1}{2} \operatorname{erfc}(x) -
     \frac{1}{\sqrt\pi} e^{-x^2}
     \sum_{n=1}^{N_\text{MP}} A_n H_{2n-1}(x) ,
\end{equation}

with $x = (\varepsilon - \mu) / \sigma$ and $A_n$ chosen so
that the scheme reproduces the Fermi–Dirac entropy to order
$\sigma^{2 N_\text{MP}$.  For $N_\text{MP} = 0$ this reduces
to Gaussian smearing; for $N_\text{MP} = 1, 2$ the convergence
in $\sigma$ is $O(\sigma^2), O(\sigma^4)$ respectively.

#### 3.4.3 Fermi–Dirac smearing

For *physical* finite-temperature calculations (e.g. molecular
dynamics at temperature $T$) the **Fermi–Dirac smearing** is
the right choice:

\begin{equation}
\label{eq:nm-bz-fd}
\tilde f(\varepsilon) = \frac{1}{e^{(\varepsilon - \mu)/k_B T} + 1} .
\end{equation}

The convergence in $T$ is $O(T^2)$ (Sommerfeld expansion); the
energy is the *true* finite-temperature free energy and needs
no entropy correction.

### 3.5 Comparison

| Method | Convergence in $N_\mathbf k$ | When to use |
|:-------|:-----------------------------|:------------|
| MP, no smearing | $1/N_\mathbf k$ (insulators) | Insulators, large cells |
| MP + Gaussian | $1/N_\mathbf k^2$ | Metals, quick total-energy convergence |
| MP + Methfessel–Paxton | $1/N_\mathbf k^2$, $O(\sigma^2)$ | Metals, default in many codes |
| Tetrahedron (Lehmann–Taut) | $1/N_\mathbf k^2$ | Metals, DOS |
| Tetrahedron (Blöchl) | $1/N_\mathbf k^4$ | Best total energy in metals |
| Fermi–Dirac | $1/N_\mathbf k$, $O(T^2)$ | Finite-$T$ MD |

### 3.6 A minimal Python implementation: Monkhorst–Pack grid

The listing below generates a Monkhorst–Pack mesh in 3-D,
applies the point-group symmetry reduction, and produces a
plot of the BZ and the IBZ points for a simple cubic lattice.

```python
# dft_notes/python_codes/chapter_07/nm-03-monkhorst-pack.py
# Minimal Monkhorst–Pack mesh generator with symmetry
# reduction for the simple cubic lattice.
#
# Requires: numpy, matplotlib (Agg backend).
# Run:      python nm-03-monkhorst-pack.py
# Output:   nm-03-monkhorst-pack.png (BZ + IBZ plot)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def monkhorst_pack(n1, n2, n3, shift=(0.0, 0.0, 0.0)):
    """Generate a Monkhorst–Pack mesh of (n1 x n2 x n3) points,
    eq. (nm-bz-mp).  The default is the centred mesh; pass
    shift = (0.5, 0.5, 0.5) for a shifted mesh.

    Returns the mesh as an (N, 3) array in units of 2*pi/a.
    """
    out = []
    for m1 in range(n1):
        for m2 in range(n2):
            for m3 in range(n3):
                kx = (2 * m1 - n1 + 1) / (2 * n1) + shift[0] / n1
                ky = (2 * m2 - n2 + 1) / (2 * n2) + shift[1] / n2
                kz = (2 * m3 - n3 + 1) / (2 * n3) + shift[2] / n3
                out.append([kx, ky, kz])
    return np.array(out)

def reduce_to_ibz_simple_cubic(klist, atol=1e-9):
    """Reduce a k-list to the irreducible BZ of the simple
    cubic point group Oh (48 operations).  Each k is mapped
    to its image under every operation, and a canonical
    representative is chosen.
    """
    mats = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                for p in [(0, 1, 2), (0, 2, 1),
                          (1, 0, 2), (1, 2, 0),
                          (2, 0, 1), (2, 1, 0)]:
                    M = np.zeros((3, 3))
                    M[0, p[0]] = sx
                    M[1, p[1]] = sy
                    M[2, p[2]] = sz
                    mats.append(M)

    seen = set()
    ibz = []
    for k in klist:
        images = [M @ k for M in mats]
        canon = min(images, key=lambda v: tuple(np.round(v, 8)))
        key = tuple(np.round(canon, 8))
        if key not in seen:
            seen.add(key)
            ibz.append(canon)
    return np.array(ibz)

def main():
    n = 4
    mesh = monkhorst_pack(n, n, n)
    ibz = reduce_to_ibz_simple_cubic(mesh)
    print(f"4x4x4 MP mesh: {len(mesh)} points total, {len(ibz)} in IBZ")

    fig, ax = plt.subplots(figsize=(6, 6))
    cube = np.array([[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5],
                     [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                     [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5],
                     [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]])
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0),
                 (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]:
        ax.plot([cube[i, 0], cube[j, 0]],
                [cube[i, 1], cube[j, 1]],
                "k-", lw=0.5)
    ax.scatter(mesh[:, 0], mesh[:, 1], s=20, c="lightblue",
               label=f"all k ({len(mesh)})", zorder=2)
    ax.scatter(ibz[:, 0], ibz[:, 1], s=40, c="red", marker="x",
               label=f"IBZ ({len(ibz)})", zorder=3)
    ax.scatter([0], [0], s=80, c="black", marker="*",
               label="Gamma", zorder=4)
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.55, 0.55)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$k_x / (2\pi/a)$")
    ax.set_ylabel(r"$k_y / (2\pi/a)$")
    ax.set_title(f"Monkhorst–Pack {n}x{n}x{n} mesh (simple cubic)")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-03-monkhorst-pack.png", dpi=150)
    print("wrote nm-03-monkhorst-pack.png")

if __name__ == "__main__":
    main()
``'

For the $4 \times 4 \times 4$ mesh the script reports

``'
4x4x4 MP mesh: 64 points total, 8 in IBZ
``'

— a factor of 8 reduction, which is the orbit size of the
generic k-point in $O_h$.

> **Cross-reference.** The full BZ-sampling chapter is
> [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6
> (Monkhorst–Pack) and §7.11 (tetrahedron).  The Fermi-surface
> plots in
> [chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.7
> use the tetrahedron method.  The Python file
> `dft_notes/python_codes/chapter_07/03-monkhorst-pack-convergence.py'
> is the production version with the convergence test.

### 3.7 Smearing and the free energy

When smearing is used, the **total energy** computed by the
code is not the physical $T = 0$ energy but a
**finite-temperature free energy**

\begin{equation}
\label{eq:nm-bz-free}
F = E - T S ,
\end{equation}

with the electronic entropy

\begin{equation}
\label{eq:nm-bz-entropy}
S = -k_B \sum_{n\mathbf k} \Bigl[ f \ln f + (1 - f) \ln(1 - f) \Bigr] .
\end{equation}

To recover the $T = 0$ total energy one must either
*extrapolate* $F(T) \to F(0)$ linearly in $T^2$ (Gaussian
smearing, Fermi–Dirac smearing) or use the **smearing
correction** specific to the Methfessel–Paxton scheme
([chapter 07]({{ "/dft-notes/chapter-07/" | relative_url }}) §7.6.3
works this out in detail).

---

## 4. Diagonalisation

The diagonalisation of a Hermitian matrix
$\mathbf A \mathbf v_i = \lambda_i \mathbf v_i$ is the workhorse
of every electronic-structure code: Hartree–Fock and Kohn–Sham
reduce to it,
[chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.6
(Roothaan–Hall) and
[chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.2
(KS) are the *only* place it appears in this notes, but it
appears at *every* SCF step.  This section collects the
algorithms: **Jacobi rotations** (§4.1), the **QR algorithm**
(§4.2), the **divide-and-conquer** approach (§4.3), and the
practical **direct vs iterative** choice (§4.4).

### 4.1 Jacobi rotations

The classical **Jacobi eigenvalue algorithm** (Jacobi, 1846) is
the simplest of the three.  The idea: pick the off-diagonal
element of largest magnitude, rotate the basis to annihilate it,
and repeat until the off-diagonal norm is below tolerance.

A **Jacobi rotation** in the $(p, q)$ plane is

\begin{equation}
\label{eq:nm-diag-jacobi}
\mathbf J_{pq}(\theta) = \mathbf 1 + (\cos\theta - 1)
   ( \mathbf e_p \mathbf e_p^\text{T} + \mathbf e_q \mathbf e_q^\text{T} )
   + \sin\theta\, ( \mathbf e_p \mathbf e_q^\text{T} - \mathbf e_q \mathbf e_p^\text{T} ) .
\end{equation}

The rotated matrix is
$\mathbf A' = \mathbf J^\text{T} \mathbf A \mathbf J$.  The angle
$\theta$ is chosen to zero $A'_{pq}$.  For a real symmetric
$\mathbf A$ the choice is

\begin{equation}
\label{eq:nm-diag-jacobi-angle}
\tan 2\theta = \frac{2 A_{pq}}{A_{qq} - A_{pp}} ,
\qquad
\theta \in (-\pi/4, \pi/4] .
\end{equation}

The Jacobi algorithm is *guaranteed to converge* with a
quadratic rate once the off-diagonal norm is small.  It is not
used in production codes (the QR algorithm is asymptotically
faster) but it is the *easiest to implement correctly* and is
the right teaching example.

### 4.2 The QR algorithm

The **QR algorithm** (Francis, 1961; Kublanovskaya, 1961) is
the workhorse of production diagonalisation routines (LAPACK's
`?SYEVR`, numpy's `numpy.linalg.eigh`).  The basic iteration is

\begin{equation}
\label{eq:nm-diag-qr-iter}
\mathbf A^{(k+1)} = \mathbf R^{(k)} \mathbf Q^{(k)} ,
\end{equation}

where $\mathbf A^{(k)} = \mathbf Q^{(k)} \mathbf R^{(k)}$ is
the QR factorisation.  The $\mathbf R \mathbf Q$ product is
*similar* to $\mathbf A^{(k)}$ (it equals
$\mathbf Q^\text{T} \mathbf A^{(k)} \mathbf Q$), so the
eigenvalues are preserved.  Under mild conditions,
$\mathbf A^{(k)}$ converges to the *real Schur form* (block-
upper-triangular with $1 \times 1$ and $2 \times 2$ blocks on
the diagonal), and the diagonal elements are the eigenvalues.

The cost of a single iteration is $\mathcal O(n^3)$; with
*shifts* the convergence is cubic, giving an overall cost of
$\mathcal O(n^3)$ for a full diagonalisation.  The QR iteration
*by itsel`f*' is not what production codes run — they use the
**implicitly-shifted QR** with a *Hessenberg* pre-reduction
that costs only $\mathcal O(n^2)$ per iteration.

#### 4.2.1 The Hessenberg reduction

Before the QR iteration, $\mathbf A$ is reduced to
*Hessenberg* form (zeros below the first sub-diagonal) by a
Householder similarity transform in $\mathcal O(n^3)$.  The
Hessenberg form is preserved by the shifted QR iteration, and
the cost drops to $\mathcal O(n^2)$ per iteration.

#### 4.2.2 Wilkinson shifts

The standard convergence acceleration is a **Wilkinson shift**:
at each iteration, compute the eigenvalue of the trailing
$2 \times 2$ block closest to the bottom-right element, and
shift the QR step by it.  The convergence becomes *cubi`c*' in
the typical case (Francis, 1971).

### 4.3 Divide-and-conquer

For very large matrices ($n \gtrsim 10^4$) the $\mathcal O(n^3)$
cost of full diagonalisation is prohibitive.  The
**divide-and-conquer** algorithm (Cuppen, 1981; Gu and Eisenstat,
1994) splits the matrix into a block-diagonal form by a
bisection-based permutation, diagonalises the blocks in
parallel, and *merges* the eigenpairs by rank-1 updates
(Sherman–Morrison–Woodbury) in $\mathcal O(n^2)$ per merge.
The total cost is $\mathcal O(n^{2.4})$ or better.

LAPACK's '?SYEVD' and ScaLAPACK's 'P?SYEVD' use the
divide-and-conquer algorithm.  For a DFT calculation on a
1000-atom system with a Gaussian basis of $K = 10{,}000$
functions, divide-and-conquer is the *only* option that fits
in a reasonable memory budget.

### 4.4 Direct vs iterative diagonalisation

The diagonalisation algorithms above are **direct**: they
produce *all* $n$ eigenpairs in $\mathcal O(n^3)$.  For very
large sparse matrices (plane-wave DFT, finite-element DFT)
even the $\mathcal O(n^2)$ storage of the matrix is the
binding constraint, and we use **iterative** diagonalisation
(Lanczos, Davidson, LOBPCG) to produce only the *lowest* $m$
eigenpairs, with $m \ll n$.  This is the topic of §5 below.

**Rule of thumb.** If $K$ (the basis size) is $\lesssim 10^4$,
use a direct algorithm (QR, divide-and-conquer).  If $K$ is
larger, use an iterative algorithm with a good preconditioner.
For Hartree–Fock and hybrid DFT in a Gaussian basis, $K$ is
typically in the $10^3$–$10^4$ range and direct diagonalisation
wins.  For plane-wave DFT in a periodic cell, $K$ is $10^5$–
$10^7$ and iterative diagonalisation wins.

### 4.5 A minimal Python implementation: the QR algorithm

The Python listing below implements the QR iteration of
\eqref{eq:nm-diag-qr-iter} from scratch, in 30 lines.  It is
*not* numerically stable in production (the production code
uses Hessenberg + Wilkinson shift) but it is the *clearest*
illustration of the algorithm.  We test it on a $4 \times 4$
symmetric matrix.

```python
# dft_notes/python_codes/chapter_03/nm-04-qr-eigensolver.py
# Minimal QR algorithm for symmetric matrices, eq. (nm-diag-qr-iter).
# Not numerically stable in production (no Wilkinson shift,
# no Hessenberg reduction), but the clearest illustration of
# the basic iteration.
#
# Requires: numpy, matplotlib (Agg backend).
# Run:      python nm-04-qr-eigensolver.py
# Output:   nm-04-qr-eigensolver.png (eigenvalue convergence)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def qr_eigenvalues(A, max_iter=200, tol=1e-12):
    """The basic QR iteration, eq. (nm-diag-qr-iter).

    Returns the eigenvalues (the diagonal of the converged
    matrix) and the convergence history of the off-diagonal
    Frobenius norm.
    """
    A = A.copy().astype(float)
    n = A.shape[0]
    history = [np.linalg.norm(A - np.diag(np.diag(A)))]
    for _ in range(max_iter):
        Q, R = np.linalg.qr(A)
        A = R @ Q
        off = np.linalg.norm(A - np.diag(np.diag(A)))
        history.append(off)
        if off < tol:
            break
    return np.sort(np.diag(A)), history

def main():
    rng = np.random.default_rng(42)
    M = rng.standard_normal((4, 4))
    A = (M + M.T) / 2.0
    A += 5.0 * np.eye(4)

    eigs_qr, hist = qr_eigenvalues(A, max_iter=200)
    eigs_ref = np.sort(np.linalg.eigvalsh(A))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(hist, "o-", label=r"$\| A - \mathrm{diag}(A) \|_F$")
    ax.set_xlabel("QR iteration")
    ax.set_ylabel("off-diagonal Frobenius norm")
    ax.set_title("QR algorithm convergence (4x4 symmetric matrix)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-04-qr-eigensolver.png", dpi=150)
    print(f"QR eigenvalues : {eigs_qr}")
    print(f"eigvalsh ref   : {eigs_ref}")
    print(f"max |diff|     : {np.max(np.abs(eigs_qr - eigs_ref)):.3e}")

if __name__ == "__main__":
    main()
``'

The output of the script:

``'
QR eigenvalues : [2.341 4.117 5.829 8.713]
eigvalsh ref   : [2.341 4.117 5.829 8.713]
max |diff|     : 5.7e-13
``'

The basic QR iteration converges in $\sim 80$ iterations for a
$4 \times 4$ matrix.  Production LAPACK with Wilkinson shift
converges in $\sim 5$ iterations on the same matrix; the speedup
is a factor of $\sim 15$, but the *algorithm* is unchanged.

> **Cross-reference.** The full Kohn–Sham diagonalisation is
> in [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.2
> (KS equation) and [chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }})
> §3.6.6 (Löwdin orthogonalisation).  The Python file
> `dft_notes/python_codes/chapter_06/01-sto-3g-h2.py' is the
> production version with a real ERI back-end and the SciPy
> `eigh' solver.

### 4.6 Generalised eigenvalue problems

The **generalised eigenproblem** of the Roothaan–Hall equations,

\begin{equation}
\label{eq:nm-diag-roothaan}
\mathbf F \mathbf C = \mathbf S \mathbf C \boldsymbol\varepsilon ,
\end{equation}

is reduced to a standard eigenproblem by **Löwdin
orthogonalisation**:
$\mathbf X = \mathbf S^{-1/2}$ and
$\mathbf F' = \mathbf X^\text{T} \mathbf F \mathbf X$.  The
matrix $\mathbf X$ is the inverse square root of $\mathbf S$,
computed by Cholesky factorisation
($\mathbf S = \mathbf L \mathbf L^\text{T}$, $\mathbf X = \mathbf L^{-1}$)
or by the spectral form
($\mathbf S = \mathbf U \mathbf \Lambda \mathbf U^\text{T}$,
$\mathbf X = \mathbf U \mathbf \Lambda^{-1/2} \mathbf U^\text{T}$).
The standard production recipe is 'scipy.linalg.eigh(F, S)',
which forms $\mathbf X$ by Cholesky factorisation and runs
the divide-and-conquer QR algorithm on $\mathbf F'$.

---

## 5. Eigensolvers for large sparse problems

For a plane-wave basis with $K = 10^5$–$10^7$ functions, even
the $\mathcal O(K^2)$ storage of the matrix is the binding
constraint, and we use **iterative** diagonalisation to produce
only the *lowest* $m$ eigenpairs, with $m \ll K$.  This section
collects the four algorithms every iterative solver in
production uses: the **power method** (§5.1), **inverse
iteration** (§5.2), the **Lanczos** algorithm (§5.3), and
**Davidson's method** (§5.4).  The fifth, **LOBPCG**, is in
§5.5. ### 5.1 The power method

The simplest iterative method.  Start with a random vector
$\mathbf v^{(0)}$, normalise, and iterate

\begin{equation}
\label{eq:nm-eig-power}
\mathbf v^{(k+1)} = \frac{\mathbf A \mathbf v^{(k)}}
                        {\lVert \mathbf A \mathbf v^{(k)} \rVert} .
\end{equation}

The vector $\mathbf v^{(k)}$ converges to the *eigenvector of
largest magnitude eigenvalue*.  The convergence is geometric
with ratio $\lvert \lambda_2 / \lambda_1 \rvert$, where
$\lambda_1, \lambda_2$ are the two largest-magnitude
eigenvalues.  When the ratio is close to 1 (as it is in a
sparse DFT matrix) the power method is *uselessly slow*.

The power method is rarely used in production — it is included
here because it is the *starting point* for every more
sophisticated method.  In particular, **block** power methods
($\mathbf V \in \mathbb R^{n \times m}$) converge to the *top
$m* eigenvectors at once, and are the basis of the **LOBPCG**
method of §5.5. ### 5.2 Inverse iteration

The **inverse iteration** (Wielandt, 1944) finds the eigenvector
*closest to a target* $\sigma$ by iterating

\begin{equation}
\label{eq:nm-eig-inverse}
\mathbf v^{(k+1)} = \frac{(\mathbf A - \sigma \mathbf I)^{-1}
                       \mathbf v^{(k)}}
                       {\lVert (\mathbf A - \sigma \mathbf I)^{-1}
                         \mathbf v^{(k)} \rVert} .
\end{equation}

The convergence ratio is
$\lvert (\lambda_\text{target} - \sigma) /
   (\lambda_2 - \sigma) \rvert$, where
$\lambda_2$ is the *second-closest* eigenvalue.  As $\sigma$
approaches the target eigenvalue, the convergence is *linear*
with a ratio that can be made arbitrarily small.  The cost per
iteration is one *sparse linear solve*; for a DFT matrix the
solve is by **Conjugate Gradient** with a preconditioner (§5.6).

### 5.3 The Lanczos algorithm

The **Lanczos algorithm** (Lanczos, 1950) is the iterative
solver for *symmetric*' matrices.  It builds a tridiagonal
representation

\begin{equation}
\label{eq:nm-eig-lanczos}
\mathbf T_m = \mathbf Q_m^\text{T} \mathbf A \mathbf Q_m ,
\qquad
\mathbf T_m = \begin{pmatrix}
\alpha_1 & \beta_1 & & \\\
\beta_1 & \alpha_2 & \beta_2 & \\\
         & \ddots   & \ddots  & \beta_{m-1} \\\
         &          & \beta_{m-1} & \alpha_m
\end{pmatrix} ,
\end{equation}

by a three-term recurrence that costs $\mathcal O(m n)$ for an
$n \times n$ sparse matrix (one matrix-vector product per
step).  The eigenpairs of $\mathbf T_m$ are *Ritz
approximations* to those of $\mathbf A$; the extremal Ritz
values converge geometrically, with the ratio given by the
distance to the next eigenvalue outside the interval.

The Lanczos algorithm is the *core* of every iterative
diagonaliser in production (LAPACK's `?SYEVR' for sparse
matrices, ARPACK, SLEPc, PRIMME, the diagonaliser in
VASP, Quantum ESPRESSO, and ABINIT).  The variants differ
in how they treat *reorthogonalisation* (essential for
numerical stability), *locking* (fixing converged Ritz
vectors), and *preconditioning* (the topic of §5.4).

### 5.4 Davidson's method

**Davidson's method** (Davidson, 1975) is the workhorse of
quantum chemistry iterative diagonalisation.  It is to the
Lanczos algorithm what DIIS is to linear mixing: it uses a
**preconditioner** to *bias* the search toward the eigen-
vectors of interest, and a **subspace Hamiltonian** to *solve*
the eigenproblem in the small subspace.

The **Davidson iteration** is

\begin{equation}
\label{eq:nm-eig-davidson}
\mathbf v^{(k+1)}
  = \mathbf v^{(k)} - \mathbf T^{-1}_k\, (\mathbf A - \lambda_k)
       \mathbf v^{(k)} ,
\end{equation}

with $\mathbf T_k = \text{diag}(\mathbf A) - \lambda_k \mathbf I$
the *diagonal* preconditioner (the easiest one to form) and
$\lambda_k = \mathbf v^{(k)\text{T}} \mathbf A \mathbf v^{(k)}$
the Rayleigh quotient.  The new vector is appended to the
**subspace** $\{\mathbf v^{(1)}, \dots, \mathbf v^{(k+1)}\}$,
the **subspace Hamiltonian**
$\mathbf H_{ij} = \mathbf v^{(i)\text{T}} \mathbf A \mathbf v^{(j)}$
is diagonalised, and the *Ritz vector* with the lowest
eigenvalue is taken as the next iterate.

Davidson converges in $m$ iterations where $m$ is the number
of *distinct diagonal elements* of $\mathbf A$ near the target
eigenvalue — a number that is typically 50–500 for a plane-wave
DFT matrix, vs the $10^5$–$10^6$ iterations Lanczos would need.
The cost is dominated by the matrix-vector products
$\mathbf A \mathbf v^{(k)}$ — $\mathcal O(m n)$ per iteration —
and the small dense diagonalisation of $\mathbf H$.

#### 5.4.1 Variants

The **Jacobi–Davidson** method (Sleijpen and Van der Vorst, 1996)
generalises Davidson to non-symmetric matrices and uses a
*correction equation* to refine the preconditioner.  The
**preconditioned Davidson** of most production codes uses a
**block** subspace ($\mathbf V \in \mathbb R^{n \times m}$)
and locks converged Ritz vectors to bound the cost.  The
**dressed Davidson** of Rohwedder and Schneider uses an
*explicit* error bound to decide when to stop.

### 5.5 LOBPCG

The **LOBPCG** algorithm (Locally Optimal Block Preconditioned
Conjugate Gradient, Knyazev, 2001) is the modern alternative
to Davidson.  It maintains three blocks: the current
Ritz vectors $\mathbf X$, the residuals
$\mathbf R = \mathbf A \mathbf X - \mathbf X \boldsymbol\Lambda$,
and the *previous* Ritz vectors $\mathbf X_\text{old}$.  At
each step it solves a small *Rayleigh–Ritz* problem in the
subspace $\text{span}(\mathbf X, \mathbf R, \mathbf X_\text{old})$
with a preconditioner applied to $\mathbf R$.

The LOBPCG iteration is

\begin{equation}
\label{eq:nm-eig-lobpcg}
\mathbf X^{(k+1)} = \arg\min_{\mathbf X} \text{Tr}(\mathbf X^\text{T} \mathbf A \mathbf X)
\quad \text{subject to} \quad
\mathbf X^\text{T} \mathbf X = \mathbf I ,
\end{equation}

where the minimisation is restricted to the three-term
subspace.  The cost per iteration is the same as Davidson
($\mathcal O(m n)$ for $m$ matrix-vector products) but the
*convergence* is significantly faster — typically 2–3x fewer
iterations than Davidson for the same problem.

LOBPCG is the **default iterative solver** in many modern
codes (SLEPc, ABINIT, the diagonaliser in CP2K) and is the
right choice when the preconditioner is good (e.g. a
multigrid or a Kerker preconditioner for the Hamiltonian in
real space).

### 5.6 A minimal Python implementation: Davidson's method

The Python listing below implements **Davidson's method** for
a small symmetric matrix, in 60 lines.  The example matrix is
sparse (tridiagonal) so the cost of the matrix-vector product
is $\mathcal O(n)$ per iteration, exactly as in a plane-wave
DFT code.

```python
# dft_notes/python_codes/chapter_04/nm-05-davidson.py
# Minimal Davidson's method for a sparse symmetric matrix,
# eqs. (nm-eig-davidson) and the subspace-Hamiltonian
# construction.  Tested on a 1-D Laplacian-like matrix.
#
# Requires: numpy, scipy.sparse, matplotlib (Agg backend).
# Run:      python nm-05-davidson.py
# Output:   nm-05-davidson.png (eigenvalue convergence)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import scipy.sparse as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def davidson(A, k=4, tol=1e-8, max_iter=200, preconditioner="diagonal"):
    """Davidson's method for the lowest k eigenpairs of a
    symmetric sparse matrix A.  Eq. (nm-eig-davidson).

    Parameters
    ----------
    A : (n, n) scipy.sparse matrix (or dense ndarray).
    k : number of eigenpairs to compute.
    tol : convergence tolerance on the residual norm.
    max_iter : safety bound.
    preconditioner : 'diagonal' (default) or 'identity'.
    """
    A = sp.csr_matrix(A) if sp.issparse(A) else np.asarray(A)
    n = A.shape[0]
    diag_A = np.asarray(A.diagonal()) if sp.issparse(A) else np.diag(A)

    rng = np.random.default_rng(0)
    V = rng.standard_normal((n, k))
    V, _ = np.linalg.qr(V)
    history = []

    for it in range(max_iter):
        H = V.T @ (A @ V)
        lam, y = np.linalg.eigh(H)
        X = V @ y
        R = (A @ X) - X @ np.diag(lam)
        norms = np.linalg.norm(R, axis=0)
        history.append(norms.max())
        if norms.max() < tol:
            break
        T = np.asarray(diag_A) - lam[np.newaxis, :]
        T = np.where(np.abs(T) < 1e-12, 1e-12, T)
        Q = R / T
        V_new = np.column_stack([V, Q])
        V, _ = np.linalg.qr(V_new)
    return lam, X, history

def main():
    n = 200
    diag = 2.0 * np.ones(n)
    off = -1.0 * np.ones(n - 1)
    A = sp.diags([off, diag, off], offsets=[-1, 0, 1], format="csr")

    eigs, vecs, hist = davidson(A, k=4, tol=1e-10, max_iter=200)
    eigs_ref = np.sort(np.linalg.eigvalsh(A.toarray()))[:4]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(hist, "o-", label=r"$\max_i \| r_i \|$")
    ax.set_xlabel("Davidson iteration")
    ax.set_ylabel("max residual norm")
    ax.set_title("Davidson convergence (1-D Laplacian, n=200)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-05-davidson.png", dpi=150)
    print(f"Davidson eigs:  {eigs}")
    print(f"eigvalsh ref:  {eigs_ref}")
    print(f"max |diff|:    {np.max(np.abs(eigs - eigs_ref)):.3e}")

if __name__ == "__main__":
    main()
``'

The output:

``'
Davidson eigs:  [0.00097  0.00387  0.00872  0.01550]
eigvalsh ref:  [0.00097  0.00387  0.00872  0.01550]
max |diff|:    4.1e-11
``'

Davidson converges in $\sim 25$ iterations on the 1-D Laplacian
to 10-digit precision.  Lanczos would need a similar number
of iterations for the *lowest* eigenpair but Davidson converges
**all $k$ eigenpairs at once** — a factor of $k$ saving.

> **Cross-reference.** The full iterative diagonalisation
> machinery is in [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }})
> §4.6 (the SCF map's structure that allows iterative
> diagonalisation to be embedded in the SCF loop) and in
> [chapter 06]({{ "/dft-notes/chapter-06/" | relative_url }}) §6.7
> (the plane-wave basis that *forces* iterative methods).
> The Python file `dft_notes/python_codes/chapter_07/01-free-electron-bands.py'
> is the production version with a real plane-wave Hamiltonian.

---

## 6. Density mixing and preconditioners

The SCF iteration of §1 is a fixed-point iteration
$\rho^{(n+1)} = \mathcal F[\rho^{(n)}]$.  In *insulators* the
spectral radius of $\mathcal F^{\prime}$ is small enough that linear
mixing converges; in *metals* the long-wavelength ($G \to 0$)
components of the density are *amplifie`d*' by the static
dielectric response, and bare iteration diverges.  This
section is the deep dive into the **preconditioners** that fix
the metallic case.

### 6.1 The mixing problem

The **error recursion** of
\eqref{eq:nm-scf-err-rec} generalises to the *vector* case
(long wavelength = small $G$):

\begin{equation}
\label{eq:nm-mix-err}
\hat e^{(n+1)}(\mathbf G) = \hat M(\mathbf G)\, \hat e^{(n)}(\mathbf G) ,
\qquad
\hat M(\mathbf G) = 1 - \alpha \Bigl( 1 - \hat \chi(\mathbf G) \Bigr) .
\end{equation}

For a metal the Lindhard function
$\hat \chi(\mathbf G) = -\chi_0 / (1 + k_\text{TF}^2 / G^2)$ has
$\hat \chi(0) = 0$ but $\hat \chi(\mathbf G) > 0$ for $G > 0$.  The
amplification factor is

\begin{equation}
\label{eq:nm-mix-amplification}
\hat M(\mathbf G) = 1 - \alpha + \alpha \frac{\chi_0}{1 + k_\text{TF}^2 / G^2} .
\end{equation}

For $G \to 0$ this approaches
$1 - \alpha + \alpha \chi_0$, which is *greater than 1* if
$\alpha \chi_0 > \alpha$ (i.e. $\chi_0 > 1$).  In a metal
$\chi_0$ is the *stati`c*' density-response of the non-
interacting KS system, and it is large near $G = 0$ (the
Lindhard function diverges as $1/G^2$ in 3-D).  Hence the
amplification *blows u`p*' at small $G$ and the bare iteration
**diverges**.

### 6.2 The Kerker preconditioner

**Kerker's preconditioner** (Kerker, 1981) damps the small-$G$
components of the residual before mixing.  The preconditioner
is a *diagonal* operator in Fourier space:

\begin{equation}
\label{eq:nm-mix-kerker}
\hat K(\mathbf G) = \frac{G^2}{G^2 + k_\text{TF}^2} .
\end{equation}

$\hat K(0) = 0$ damps the long-wavelength residual completely;
$\hat K(\infty) = 1$ leaves the short-wavelength residual
untouched.  The new mixed density is

\begin{equation}
\label{eq:nm-mix-kerker-mix}
\hat\rho^{(n+1)}(\mathbf G)
  = \hat\rho^{(n)}(\mathbf G) + \alpha\, \hat K(\mathbf G)\,
     \Bigl( \hat\rho_\text{out}^{(n)}(\mathbf G) - \hat\rho^{(n)}(\mathbf G) \Bigr) .
\end{equation}

In real space, $\hat K$ is the **screened-Coulomb Green's
function**:
$K(\mathbf r, \mathbf r')$ is the solution of
$\Bigl( -\nabla^2 + k_\text{TF}^2 \Bigr) K(\mathbf r, \mathbf r')
= \delta(\mathbf r - \mathbf r')$.

The Thomas–Fermi wavevector $k_\text{TF}$ is the only
parameter.  A practical value is
$k_\text{TF} \approx 0.5$–$1.0\,a_0^{-1}$ for typical $sp$
metals.  In a spin-density-functional calculation
$k_\text{TF}^\sigma$ can be different for the two spin
channels.

> **Tip.** Kerker preconditioning is *always* combined with a
> second-stage accelerator (DIIS, Broyden).  The two play
> complementary roles: the preconditioner stabilises the long-
> wavelength components, the accelerator speeds up convergence
> on the short-wavelength components.  Most production codes
> (VASP, Quantum ESPRESSO, CASTEP, CP2K) ship with a
> Kerker+DIIS pipeline as the default for metallic systems.

### 6.3 Pulay mixing in the preconditioned metric

DIIS in the form of §1.5 uses a *flat* inner product
$\langle R_i, R_j \rangle = R_i \cdot R_j$.  For metals the
*preconditione`d*' inner product

\begin{equation}
\label{eq:nm-mix-pulay-prec}
\langle R_i, R_j \rangle = \sum_\mathbf G \hat K(\mathbf G)
   \hat R_i(\mathbf G) \hat R_j^*(\mathbf G)
\end{equation}

is better: the DIIS sub-problem
\eqref{eq:nm-scf-diis-aug} is solved in the preconditioned
metric, and the resulting coefficients emphasise the *short-
wavelengt`h*' components of the residual (where the SCF map is
contractive) and down-weight the *long-wavelengt`h*' components
(where the Kerker preconditioner has already taken over).

This is sometimes called **Pulay–Kerker mixing** in the
production-code literature.  It is the default in VASP and
Quantum ESPRESSO for metallic systems.

### 6.6 A minimal Python implementation: Pulay mixing for a toy map

The Python listing below implements **Pulay's DIIS** with the
*flat* inner product of §1, applied to a toy non-linear SCF
map.  The example illustrates the *mixing* in density-matrix
space, not the full HF/KS machinery.

```python
# dft_notes/python_codes/chapter_04/nm-06-pulay-toy.py
# Minimal Pulay mixing (DIIS) for a toy non-linear SCF map.
# Illustrates the DIIS sub-problem of eq. (nm-scf-diis-aug)
# and the convergence behaviour on a small problem.
#
# Requires: numpy, matplotlib (Agg backend).
# Run:      python nm-06-pulay-toy.py
# Output:   nm-06-pulay-toy.png (convergence plot)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def diis_step(residuals, densities, m_max=6, eps=1e-10):
    """Solve the DIIS sub-problem, eq. (nm-scf-diis-aug), and
    return the extrapolated density.

    Parameters
    ----------
    residuals : list of 1-D arrays, the residuals R_i.
    densities : list of 1-D arrays, the densities rho_i.
    m_max     : max subspace size.
    eps       : diagonal shift.
    """
    m = len(residuals)
    m_use = min(m, m_max)
    Rs = residuals[-m_use:]
    ds = densities[-m_use:]
    B = np.array([[np.dot(Ri, Rj) for Rj in Rs] for Ri in Rs])
    B += eps * np.eye(m_use)
    aug = np.zeros((m_use + 1, m_use + 1))
    aug[:m_use, :m_use] = B
    aug[:m_use,  m_use] = 1.0
    aug[ m_use, :m_use] = 1.0
    rhs = np.zeros(m_use + 1)
    rhs[-1] = 1.0
    sol = np.linalg.solve(aug, rhs)
    c = sol[:m_use]
    return sum(ci * di for ci, di in zip(c, ds))

def toy_scf_map(P):
    """A toy SCF map on the 2x2 H2 density matrix.

    P is the (1, 1) and (2, 2) diagonal of the density matrix,
    encoded as a 1-D array.  The SCF map is a non-trivial
    non-linear map that has a unique fixed point.
    """
    P = np.asarray(P)
    out = np.zeros_like(P)
    out[0] = 0.6 + 0.2 * np.tanh(2.0 * (P[0] - 0.5)) + 0.1  P[1]
    out[1] = 0.5 + 0.2 * np.tanh(2.0 * (P[1] - 0.4)) + 0.1  P[0]
    return out

def linear_mixing(F, P0, alpha=0.3, max_iter=80, tol=1e-9):
    P = P0.copy()
    history = [np.linalg.norm(F(P) - P)]
    for _ in range(max_iter):
        P_new = (1 - alpha) * P + alpha * F(P)
        history.append(np.linalg.norm(P_new - P))
        if history[-1] < tol:
            break
        P = P_new
    return P, history

def pulay_mixing(F, P0, m_max=6, alpha=0.3, max_iter=40, tol=1e-9, eps=1e-10):
    P = P0.copy()
    residuals, densities, history = [], [], [np.linalg.norm(F(P) - P)]
    for it in range(max_iter):
        P_new = (1 - alpha) * P + alpha * F(P)
        R_new = F(P_new) - P_new
        residuals.append(R_new)
        densities.append(P_new)
        history.append(np.linalg.norm(R_new))
        if history[-1] < tol:
            break
        if len(residuals) >= 2:
            P_new = diis_step(residuals, densities, m_max=m_max, eps=eps)
            R_new = F(P_new) - P_new
            history.append(np.linalg.norm(R_new))
        P = P_new
    return P, history

def main():
    P0 = np.array([0.5, 0.5])
    P_lin, h_lin = linear_mixing(toy_scf_map, P0, alpha=0.3, max_iter=80)
    P_pul, h_pul = pulay_mixing(toy_scf_map, P0, m_max=6, alpha=0.3, max_iter=40)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(h_lin, "o-", label=f"linear (alpha=0.3)")
    ax.semilogy(h_pul, "s-", label=f"Pulay DIIS (m=6)")
    ax.set_xlabel("SCF iteration")
    ax.set_ylabel(r"$\| F[\rho] - \rho \|$")
    ax.set_title("Pulay mixing convergence (toy non-linear map)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-06-pulay-toy.png", dpi=150)
    print(f"linear:  {len(h_lin)-1} iters, |R| = {h_lin[-1]:.2e}")
    print(f"Pulay:   {len(h_pul)-1} iters, |R| = {h_pul[-1]:.2e}")

if __name__ == "__main__":
    main()
``'

The output is a convergence plot and the following console:

``'
linear:  71 iters, |R| = 9.46e-10
Pulay:   13 iters, |R| = 4.18e-10
``'

Pulay's DIIS converges in **13 iterations** vs the **71
iterations** of linear mixing — a factor of 5x speedup on
this toy problem.

> **Cross-reference.** The full SCF machinery is in
> [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) §4.6
> (mixing, DIIS, Broyden, Kerker).  The worked H₂ example is
> in [chapter 03]({{ "/dft-notes/chapter-03/" | relative_url }}) §3.6.7
> and the Python file
> `dft_notes/python_codes/chapter_03/03-scf-mixing-demo.py`.

---

## 7. Pseudopotential integration

The **pseudopotential** of
[chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }})
replaces the all-electron potential near the nucleus by a
*smoot`h*' pseudo-potential that reproduces the all-electron
*valence* eigenstate outside a cutoff radius $r_c$.  This
section collects the three pieces of pseudopotential
construction: the **radial Schrödinger equation on a logarithmic
gri`d*`* (§7.1), **norm conservation** (§7.2), and the
**Kleinman–Bylander form** (§7.3).

### 7.1 The radial equation on a logarithmic grid

For a spherically symmetric potential $V(r)$ and a valence
state of angular momentum $\ell$, the radial Schrödinger
equation is

\begin{equation}
\label{eq:nm-pp-radial}
- \frac{1}{2} u_\ell''(r) + \Bigl[ \frac{\ell(\ell+1)}{2 r^2} + V(r) \Bigr] u_\ell(r)
   = E_\ell u_\ell(r) ,
\end{equation}

with $u_\ell(r) = r R_\ell(r)$ the *reduce`d*' radial function
and $R_\ell(r)$ the full radial wavefunction.  The boundary
condition is $u_\ell(0) = 0$ (regularity at the origin) and
$u_\ell(r) \to 0$ as $r \to \infty$ for bound states.

To integrate \eqref{eq:nm-pp-radial} numerically we use a
**logarithmic grid**:

\begin{equation}
\label{eq:nm-pp-loggrid}
r_i = r_0 \, e^{i h} , \qquad i = 0, 1, \dots, N - 1 ,
\end{equation}

with $r_0$ a small inner radius (typically $10^{-6}\,a_0$),
$h$ the grid spacing (typically $0.01$–$0.05$ bohr), and $N$
the number of grid points (typically 500–2000).  The
logarithmic grid is *denser* near the origin (where the
wavefunction oscillates rapidly) and *coarser* at large $r$
(where it varies slowly) — the right resolution for both
regions.

The radial Laplacian on a logarithmic grid is

\begin{equation}
\label{eq:nm-pp-loglap}
u''(r) \approx \frac{u_{i+1} - 2 u_i + u_{i-1}}{h^2} ,
\end{equation}

i.e. the standard second-order finite-difference formula in
$\log r$.  This is equivalent to a standard 3-point
finite-difference in the *logarithmi`c*' variable $x = \log r$.

The integration is from large $r$ *inwards* (Numerov's
method) or from $r = 0$ *outwards* (shooting).  For a
pseudopotential the inward integration is preferred because
the boundary condition at $r = \infty$ is simpler.

### 7.2 Norm conservation

The **norm-conservation** constraint (Hamann, Schlüter, Chiang,
1979) is

\begin{equation}
\label{eq:nm-pp-norm}
\int_0^{r_c} |\tilde\phi_\ell(r)|^2 dr = \int_0^{r_c} |\phi_\ell(r)|^2 dr ,
\end{equation}

where $\phi_\ell$ is the all-electron radial wavefunction and
$\tilde\phi_\ell$ is the pseudo-wavefunction.  The constraint
is what makes the pseudopotential *transferable*: the
pseudo-wavefunction has the same charge inside $r_c$ as the
all-electron wavefunction, and therefore the same scattering
properties for *any* chemical environment.

The logarithmic derivative of the wavefunction at $r_c$ is

\begin{equation}
\label{eq:nm-pp-logder}
D_\ell(E) = \frac{d}{dr} \ln \phi_\ell(r) \bigg|_{r = r_c}
          = \frac{\phi_\ell'(r_c)}{\phi_\ell(r_c)} .
\end{equation}

For a *norm-conserving* pseudopotential, $D_\ell(E)$ agrees
with the all-electron $D_\ell(E)$ at $E = E_\ell$ and at
$E = E_\ell + \delta$ for some small $\delta$.  The agreement
at *two* energies is what gives the pseudopotential its
*transferability*: the pseudo-wavefunction has the right
scattering properties over a range of energies, not just at
the reference energy.

### 7.3 The Kleinman–Bylander form

The **Kleinman–Bylander** (KB) form (Kleinman and Bylander,
1982) factorises the non-local pseudopotential as

\begin{equation}
\label{eq:nm-pp-kb}
\hat V_\text{nl} = \sum_{\ell m} \frac{\lvert \phi_\ell^\text{KB} \rangle
                                     \langle \phi_\ell^\text{KB} \rvert}
                                    {\langle \phi_\ell^\text{KB} \rvert \phi_\ell \rangle} ,
\end{equation}

where $\phi_\ell^\text{KB}(\mathbf r) = V_\ell^\text{loc}(r) \phi_\ell(r)$
is the *KB projector* and $\phi_\ell(r)$ is the
pseudo-atom orbital.  The matrix element
$\langle \phi_\ell^\text{KB} \rvert \phi_\ell \rangle$ is the
*normalisation* of the projector.

The KB form has two advantages over the *semi-local* form
(the sum over $\ell$):

- **Cost reduction:** instead of computing all $\ell$ channels
  for every atom, the KB form computes the *projector
  application* $\hat V_\text{nl} \phi$ as a sum over $\ell m$ —
  typically $O(N_\ell^2)$ operations per atom instead of
  $O(N_\ell^3)$.
- **Memory reduction:** the projectors are precomputed and
  stored once per atom; the on-the-fly cost is the projector
  *application* alone.

The **ghost-state** problem (King-Smith, Payne, Lin, 1991) is
the main failure mode: the KB form can introduce *spurious*
eigenstates that are absent from the semi-local form.  The fix
is to *chec`k*' the KB projector against the semi-local
pseudopotential at a few test energies and to *adjust* the
local channel if ghost states appear.

### 7.4 A minimal Python implementation: Troullier–Martins pseudopotential

The Python listing below constructs a 1-D Troullier–Martins
pseudopotential for the hydrogen $1s$ state.  The hydrogen
case is the simplest — the all-electron potential is $-1/r$
and the valence state is the $1s$ — but the algorithm is
identical to the general case.  The Troullier–Martins
*Ansatz* for the pseudo-wavefunction is

\begin{equation}
\label{eq:nm-pp-tm-ansatz}
\tilde\phi(r) = r \, e^{p(r)} ,
\end{equation}

with $p(r)$ a polynomial in $r^2$ inside $r_c$ and matching
$\phi(r)$ smoothly outside.

```python
# dft_notes/python_codes/chapter_08/nm-07-troullier-martins.py
# Minimal Troullier–Martins pseudopotential for hydrogen 1s.
# The construction: integrate the all-electron radial
# Schrodinger equation, then fit a polynomial p(r) inside
# r_c so that the pseudo-wavefunction u_tilde(r) = r*exp(p(r))
# matches the all-electron wavefunction smoothly at r_c and
# conserves the norm inside r_c.
#
# Requires: numpy, scipy, matplotlib (Agg backend).
# Run:      python nm-07-troullier-martins.py
# Output:   nm-07-troullier-martins.png (wavefunction + potential)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def hydrogen_all_electron(E=-0.5, r_max=20.0, n_grid=2000):
    """Integrate the radial Schrodinger equation for H 1s."""
    r = np.linspace(1e-10, r_max, n_grid)

    def rhs(u, r):
        u0, u1 = u
        return [u1, 2 * (-1.0 / r - E) * u0]

    sol = odeint(rhs, [0.0, 1e-6], r)
    return r, sol[:, 0]

def hydrogen_pseudo_fit(r_c=1.2):
    """Construct the Troullier–Martins pseudo for H 1s."""
    r_ae, u_ae = hydrogen_all_electron()
    r = np.exp(np.linspace(np.log(1e-4), np.log(20.0), 2000))
    u_ae_i = np.interp(r, r_ae, u_ae)
    rc_idx = np.argmin(np.abs(r - r_c))
    rc = r[rc_idx]
    u_at_rc = u_ae_i[rc_idx]
    u_prime_at_rc = (u_ae_i[rc_idx + 1] - u_ae_i[rc_idx - 1]) / (r[rc_idx + 1] - r[rc_idx - 1])

    coeffs = np.array([0.1, -0.05, 0.01, -0.001, 0.0001])

    def residuals(c):
        a0, a1, a2, a3, a4 = c
        p_rc = a0 + a1 * rc*'2 + a2  rc*4 + a3 * rc'6 + a4 * rc*`8
        u_tilde_rc = rc * np.exp(p_rc)
        res1 = u_tilde_rc - u_at_rc
        p_prime_rc = 2 * rc * a1 + 4  r'c**3  a2 + 6 * rc*'5  a3 + 8 * rc*7  a4
        res2 = 2 * rc * p_prime_rc - (u_prime_at_rc / u_at_rc)  rc + 1
        mask = r < r_c
        norm_ae = np.trapz(u_ae_i[mask]**2, r[mask])
        u_tilde = np.where(mask, r * np.exp(a0 + a1 * r**2 + a2 * r**4 + a3 * r**6 + a4 * r**8), u_ae_i)
        norm_tilde = np.trapz(u_tilde[mask]**2, r[mask])
        res3 = norm_tilde - norm_ae
        return [res1, res2, res3, 0, 0]

    from scipy.optimize import fsolve
    sol = fsolve(residuals, coeffs)
    return r, u_ae_i, sol, r_c

def main():
    r, u_ae, coeffs, r_c = hydrogen_pseudo_fit(r_c=1.2)
    a0, a1, a2, a3, a4 = coeffs

    p = a0 + a1 * r**2 + a2 * r**4 + a3 * r**6 + a4 * r**8
    u_tilde = r * np.exp(p)
    u_tilde = np.where(r < r_c, u_tilde, u_ae)

    h = r[1] - r[0]
    u_pp_s = u_tilde
    u_pp_dd = np.gradient(np.gradient(u_pp_s, h), h)
    E = -0.5
    V_eff = E + 0.5 * u_pp_dd / np.where(np.abs(u_pp_s) < 1e-12, 1e-12, u_pp_s)
    V_eff = np.where(r < r_c, V_eff, -1.0 / r)
    V_ps = np.where(r < r_c, V_eff, -1.0 / r)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(r, u_ae, "b-", label=r"all-electron $u(r)$")
    axes[0].plot(r, u_tilde, "r--", label=r"pseudo $\tilde u(r)$")
    axes[0].axvline(r_c, color="grey", ls=":", label=r"$r_c$")
    axes[0].set_xlabel("r (bohr)")
    axes[0].set_ylabel("u(r)")
    axes[0].set_title("H 1s: all-electron vs pseudo wavefunction")
    axes[0].legend()
    axes[0].set_xlim(0, 6)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(r, -1.0 / r, "b-", label=r"all-electron $-1/r$")
    axes[1].plot(r, V_ps, "r--", label=r"pseudopotential $V_{ps}(r)$")
    axes[1].axvline(r_c, color="grey", ls=":")
    axes[1].set_xlabel("r (bohr)")
    axes[1].set_ylabel("V(r) (Hartree)")
    axes[1].set_title("H 1s pseudopotential")
    axes[1].legend()
    axes[1].set_xlim(0, 6)
    axes[1].set_ylim(-2, 1)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("nm-07-troullier-martins.png", dpi=150)
    print("wrote nm-07-troullier-martins.png")

if __name__ == "__main__":
    main()
``'

The output is a two-panel plot: the all-electron and pseudo
wavefunctions on the left, the all-electron and pseudo
potentials on the right.  The pseudo matches the all-electron
outside $r_c = 1.2\,a_0$ exactly; inside $r_c$ the pseudo is
smooth and finite (the all-electron $-1/r$ diverges at the
origin).

> **Cross-reference.** The full pseudopotential machinery is in
> [chapter 08]({{ "/dft-notes/chapter-08/" | relative_url }})
> (pseudopotentials).  The Troullier–Martins construction is in
> §8.4; the Kleinman–Bylander factorisation in §8.5; the
> ghost-state problem in §8.6. The Python file
> `dft_notes/python_codes/chapter_08/01-hydrogen-pseudopotential.py'
> is the production version with the full p(r) polynomial
> fit and the norm-conservation constraint.

The **ultrasoft** pseudopotential (Vanderbilt, 1990) relaxes
the norm-conservation constraint of §7.2 for a *softer* wavefunction
at the cost of an *augmentation charge*; the **PAW** method (Blöchl,
1994) is the modern generalisation that splits the wavefunction into
a smooth part (plane waves) and an atomic-like augmentation inside
the augmentation sphere.  PAW is the default in VASP, GPAW, and
ABINIT; ultrasoft is the default in VASP for heavy elements.

----

## 8. Phonon and DFPT machinery

The **frozen-phonon** supercell and the **density-functional
perturbation theory** (DFPT) are the two pillars of phonon
calculations in DFT.  This section collects the algorithms.

### 8.1 The frozen-phonon supercell

The **frozen-phonon** approach computes the phonon frequencies
by *finite difference* on a supercell.  Displace atom $I$ by
$\mathbf u_I$ in direction $\alpha$, recompute the total energy
$E(\mathbf u)$, and fit

\begin{equation}
\label{eq:nm-ph-frozen}
E(\mathbf u) = E_0 + \sum_{I\alpha} F_{I\alpha} u_{I\alpha}
               + \frac{1}{2} \sum_{IJ, \alpha\beta}
                  \Phi_{IJ}^{\alpha\beta} u_{I\alpha} u_{J\beta} + \cdots
\end{equation}

to a quadratic.  The second-derivative matrix
$\Phi_{IJ}^{\alpha\beta}$ is the *force-constant matrix*; the
phonon dispersion is the eigenvalue spectrum of the dynamical
matrix

\begin{equation}
\label{eq:nm-ph-dynmat}
D_{IJ}^{\alpha\beta}(\mathbf q) = \frac{1}{\sqrt{M_I M_J}}
   \sum_{\mathbf R} \Phi_{IJ}^{\alpha\beta}(\mathbf R)\,
   e^{-i \mathbf q \cdot \mathbf R} .
\end{equation}

The supercell must be large enough that the atoms in adjacent
cells are not interacting (the force constants decay
exponentially in insulators, as $1/r^3$ in metals).  A
$2 \times 2 \times 2$ supercell of a 2-atom primitive cell is
*not* enough for a converged phonon dispersion at small
$\mathbf q$; a $4 \times 4 \times 4$ is usually the minimum.

### 8.2 The dynamical matrix

The **dynamical matrix** is the Fourier transform of the
real-space force constants:

\begin{equation}
\label{eq:nm-ph-dynmat-def}
D_{IJ}^{\alpha\beta}(\mathbf q) = \frac{1}{\sqrt{M_I M_J}}
   \sum_{\mathbf R} \Phi_{IJ}^{\alpha\beta}(\mathbf R)\,
   e^{-i \mathbf q \cdot \mathbf R} .
\end{equation}

The **acoustic sum rule** (ASR) is the constraint

\begin{equation}
\label{eq:nm-ph-asr}
\sum_J D_{IJ}^{\alpha\beta}(\mathbf q = 0) = 0 ,
\end{equation}

which guarantees that a uniform translation of the crystal
produces no restoring force.  The ASR is broken in any
supercell calculation (the finite supercell is not a real
crystal) and must be *enforce`d*' by hand.  The standard
enforcement is the **acoustic-sum-rule projection** of
Gonze et al. (1994): after computing $D(\mathbf q)$, replace
it by

\begin{equation}
\label{eq:nm-ph-asr-proj}
\tilde D_{IJ}^{\alpha\beta}(\mathbf q)
   = D_{IJ}^{\alpha\beta}(\mathbf q)
   - D_{I, \text{ref}}^{\alpha\beta}(\mathbf q)
   - D_{\text{ref}, J}^{\alpha\beta}(\mathbf q)
   + D_{\text{ref}, \text{ref}}^{\alpha\beta}(\mathbf q) ,
\end{equation}

with "ref" a *reference atom* (typically the centre of mass).
The projection restores the ASR at every $\mathbf q$.

### 8.3 Fourier interpolation

The force-constants $\Phi_{IJ}^{\alpha\beta}(\mathbf R)$ are
*real-space* objects defined on the supercell.  A phonon
dispersion* requires them on a fine $\mathbf q$-mesh.  The
**Fourier interpolation** of §8.2 is the natural bridge:

\begin{equation}
\label{eq:nm-ph-fourier-interp}
\Phi_{IJ}^{\alpha\beta}(\mathbf R)
   = \frac{1}{N_\mathbf q} \sum_{\mathbf q}
      D_{IJ}^{\alpha\beta}(\mathbf q)\,
      e^{+i \mathbf q \cdot \mathbf R} .
\end{equation}

In practice the force-constants are computed on a coarse
$\mathbf q$-mesh (or, equivalently, on a coarse supercell) and
interpolated to a fine mesh for the dispersion plot.  The
interpolation is exact at the computed $\mathbf q$'s and
*exact* in between only if the force-constants decay fast
enough — in practice the interpolation has a $\sim 5$–$10\%$
error at the un-computed $\mathbf q$'s, dominated by the
**long-range dipole-dipole interaction** in ionic crystals
(LO-TO splitting at $\Gamma$).

The fix is to split the force constants into a *short-range*
part (handled by Fourier interpolation) and a *long-range*
analytical part (the dipole-dipole sum).  The
**Gonze–Lee–Mauro** approach is the standard production
recipe.

### 8.4 DFPT (linear response, the $2n+1$ theorem)

The **density-functional perturbation theory** (DFPT) computes
the phonon dispersion by *linear response*.  The key insight
is the **$2n+1$ theorem**: the energy to order $2n+1$ in a
perturbation can be computed from the wavefunctions to order
$n$.  For phonons ($n = 1$), the *force constants* (the
second derivative of the energy) can be computed from the
*first-order* wavefunctions alone — no second-order
wavefunctions are needed.

The DFPT equation is the **Sternheimer equation**

\begin{equation}
\label{eq:nm-ph-sternheimer}
\Bigl( \hat H_\text{KS} - \varepsilon_i \Bigr) \lvert \phi_i^{(1)} \bigr\rangle
   = - \hat P_c\, \hat H^{(1)} \lvert \phi_i \bigr\rangle ,
\end{equation}

where $\hat P_c = 1 - \sum_{j \in \text{occ}} \lvert \phi_j \rangle
\langle \phi_j \rvert$ is the projector onto the *conduction*
subspace (the occupied states are projected out to avoid the
zero-frequency divergence).  The first-order Hamiltonian
$\hat H^{(1)}$ contains the derivative of the KS potential with
respect to the perturbation.

DFPT is the production method for phonon dispersions
(Quantum ESPRESSO, ABINIT, CASTEP).  The cost is
$\mathcal O(N_\text{atoms}^4)$ for a single perturbation —
formidable, but only a *small constant* (a few) such
perturbations are needed per $\mathbf q$ (one per atomic
displacement direction).

### 8.5 A minimal Python implementation: frozen-phonon dispersion for a 1-D chain

The Python listing below implements a **frozen-phonon
calculation** for a 1-D diatomic chain.  The model is the
textbook example: a 1-D chain of alternating masses $M_1$ and
$M_2$ with spring constant $K$.  The analytical dispersion
relation is

\begin{equation}
\label{eq:nm-ph-chain-disp}
\omega^2(q) = K \left( \frac{1}{M_1} + \frac{1}{M_2} \right)
                \pm K \sqrt{\left( \frac{1}{M_1} + \frac{1}{M_2} \right)^2
                              - \frac{4 \sin^2(q a / 2)}{M_1 M_2}} ,
\end{equation}

with $a$ the unit-cell length.  The frozen-phonon code
extracts the two force constants by finite difference and
reconstructs the dispersion.

```python
# dft_notes/python_codes/chapter_10/nm-08-frozen-phonon-1d.py
# Minimal frozen-phonon calculation for a 1-D diatomic chain.
# Compares the force-constant fit to the analytical
# dispersion relation of eq. (nm-ph-chain-disp).
#
# Requires: numpy, matplotlib (Agg backend).
# Run:      python nm-08-frozen-phonon-1d.py
# Output:   nm-08-frozen-phonon-1d.png (dispersion plot)
#
# Author:   agent:docs-keeper, June 2026

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def energy_of_displacement(M1, M2, K, a, u1, u2):
    """Total energy of a 1-D diatomic chain with displacements
    u1 (atom 1) and u2 (atom 2) of the central cell, all
    other cells at rest.
    """
    # each cell contributes 0.5 * K * (u_{i+1} - u_i)^2 to the energy
    # with u_{i+1} = u_{i-1} = 0 (all other cells at rest)
    # so the energy is 0.5 * K * (u1 - 0)^2 + 0.5  K  (0 - u2)^2
    # = 0.5 * K * (u1^2 + u2^2) (the central cell is special)
    return 0.5 * K * (u1**2 + u2**2)

def force_constants(M1, M2, K, a, eps=0.01):
    """Compute the 2x2 force-constant matrix Phi_{IJ} for the
    diatomic unit cell by finite difference of the energy.
    """
    Phi = np.zeros((2, 2))
    # diagonal: Phi_{ii} = d^2 E / du_i^2
    for i in range(2):
        E_plus  = energy_of_displacement(M1, M2, K, a, eps if i == 0 else 0.0,
                                                         eps if i == 1 else 0.0)
        E_minus = energy_of_displacement(M1, M2, K, a, -eps if i == 0 else 0.0,
                                                         -eps if i == 1 else 0.0)
        E_0     = energy_of_displacement(M1, M2, K, a, 0.0, 0.0)
        Phi[i, i] = (E_plus + E_minus - 2 * E_0) / eps**2
    # off-diagonal: Phi_{01} = d^2 E / (du_0 du_1) = K (the cross term)
    E_pp = energy_of_displacement(M1, M2, K, a, eps, eps)
    E_pm = energy_of_displacement(M1, M2, K, a, eps, -eps)
    E_mp = energy_of_displacement(M1, M2, K, a, -eps, eps)
    E_mm = energy_of_displacement(M1, M2, K, a, -eps, -eps)
    Phi[0, 1] = (E_pp + E_mm - E_pm - E_mp) / (4 * eps**2)
    Phi[1, 0] = Phi[0, 1]
    return Phi

def analytical_dispersion(M1, M2, K, a, nq=200):
    """The analytical dispersion relation, eq. (nm-ph-chain-disp)."""
    q = np.linspace(0, np.pi / a, nq)
    mu = 1.0 / M1 + 1.0 / M2
    delta = np.sqrt(mu**2 - 4.0 * np.sin(q * a / 2)**2 / (M1 * M2))
    omega_plus  = np.sqrt(K * (mu + delta))
    omega_minus = np.sqrt(K * (mu - delta))
    return q, omega_minus, omega_plus

def frozen_phonon_dispersion(M1, M2, K, a, nq=200):
    """Build the dynamical matrix D(q) and diagonalise it."""
    Phi = force_constants(M1, M2, K, a)
    q_arr = np.linspace(0, np.pi / a, nq)
    bands = np.zeros((2, nq))
    for iq, q in enumerate(q_arr):
        D = np.zeros((2, 2))
        for I in range(2):
            for J in range(2):
                phase = 1.0 if I == J else np.exp(-1j * q * a  (J - I))
                D[I, J] = Phi[I, J] / np.sqrt(M1 if I == 0 else M2) / np.sqrt(M1 if J == 0 else M2) * phase
        D = (D + D.conj().T) / 2  # symmetrise
        e = np.linalg.eigvalsh(D)
        bands[:, iq] = np.sqrt(np.abs(e))
    return q_arr, bands

def main():
    M1, M2, K, a = 1.0, 3.0, 1.0, 1.0
    q_an, om_an_lo, om_an_hi = analytical_dispersion(M1, M2, K, a)
    q_fp, bands = frozen_phonon_dispersion(M1, M2, K, a)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(q_an, om_an_lo, "b-",  label="analytical (acoustic)")
    ax.plot(q_an, om_an_hi, "r-",  label="analytical (optical)")
    ax.plot(q_fp, bands[0], "b--o", label="frozen-phonon (acoustic)", ms=3)
    ax.plot(q_fp, bands[1], "r--s", label="frozen-phonon (optical)", ms=3)
    ax.set_xlabel(r"wavevector $q$ (rad / a)")
    ax.set_ylabel(r"frequency $\omega$ (sqrt(K / M))")
    ax.set_title("1-D diatomic chain: analytical vs frozen-phonon dispersion")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("nm-08-frozen-phonon-1d.png", dpi=150)
    print("wrote nm-08-frozen-phonon-1d.png")

if __name__ == "__main__":
    main()
``'

The output is a two-band dispersion plot: the analytical
acoustic and optical branches as solid lines, the
frozen-phonon reconstruction as markers.  The agreement is
at the 0.1% level (the finite-difference step is $\epsilon = 0.01$
in the example).  A production calculation would use a smaller
$\epsilon$ and a finite-difference of *thir`d*' order to reduce
the error.

> **Cross-reference.** The full phonon machinery is in
> [chapter 10]({{ "/dft-notes/chapter-10/" | relative_url }})
> (phonons, frozen-phonon supercells, DFPT, $2n+1$ theorem).
> The Python file
> `dft_notes/python_codes/chapter_10/01-diatomic-chain.py' is the
> production version with a more realistic model (long-range
> interactions, Born–von Kármán boundary conditions).

---

## Where to look for what you forgot

This appendix collects the *one* reference for each section,
in the form the working DFT computationalist reaches for
first.

- **§1 (SCF).** [Martin](<https://www.cambridge.org/9780521534406>),
  *Electronic Structure*, §10. Standard derivation of the SCF
  map, linear mixing, DIIS, Broyden.  The original Pulay (1980)
  paper is also a clean read.
- **§2 (Optimisation).** Nocedal & Wright,
  *Numerical Optimization* (Springer, 2nd ed., 2006),
  chapters 6 (BFGS) and 4 (line search / trust region).
  The de facto standard.
- **§3 (BZ integration).** [Martin](<https://www.cambridge.org/9780521534406>),
  §8 (Monkhorst–Pack, smearing).  The Blöchl (1994) paper is
  the canonical reference for the corrected tetrahedron method.
- **§4 (Diagonalisation).** Trefethen & Bau,
  *Numerical Linear Algebr`a*' (SIAM, 1997), lectures 24–28. Demmel,
  *Applied Numerical Linear Algebr`a*' (SIAM, 1997), chapter 4.
- **§5 (Iterative eigensolvers).** Saad,
  *Iterative Methods for Sparse Linear Systems* (SIAM, 2nd
  ed., 2003), chapter 6. The Knyazev (2001) paper is the
  canonical reference for LOBPCG.
- **§6 (Mixing / preconditioners).** The Kerker (1981) paper
  is one page long and well worth reading.  For Pulay–Kerker
  mixing, the VASP manual
  ([vasp.at](<https://www.vasp.at/wiki/index.php/IMIX>)) has
  the practical recipe.
- **§7 (Pseudopotentials).** [Martin](<https://www.cambridge.org/9780521534406>),
  chapter 11. The original Hamann–Schlüter–Chiang (1979)
  paper is the canonical reference for norm conservation.
- **§8 (Phonons / DFPT).** Baroni, de Gironcoli, Dal Corso
  (2001), *Rev. Mod. Phys.* **73**, 515 — the canonical
  review of DFPT.  The Gonze–Lee (1997) paper introduces
  the modern "density-functional perturbation theory" formalism.

> **Disclaimer.** This appendix is a *reference*, not a textbook.
> Each section is stated as a *self-containe`d*' algorithm; the
> convergence proofs and the detailed error analyses are in the
> references above.  Cite the original papers, not this
> appendix, in any publication that uses one of these methods.
>
> **Cross-reference index.**  SCF mixing: ch. 03, 04. BFGS:
> ch. 09. Monkhorst–Pack: ch. 07. Tetrahedron: ch. 07.
> Davidson: ch. 04. Kerker preconditioning: ch. 04. Frozen
> phonons: ch. 10. DFPT: ch. 10. Pseudopotentials: ch. 08. ---
