---
layout: page
title: "Chapter 05 — XC functionals"
permalink: /dft-notes/chapter-05/
description: >-
  A tour of the most-used exchange–correlation functionals: LDA, GGA,
  meta-GGA, hybrid, range-separated, and double-hybrid. With guidance
  on which to pick and which to avoid.
keywords: "LDA, GGA, PBE, B3LYP, SCAN, hybrid, range-separated, dispersion"
---

# Chapter 05 — XC functionals

> Every approximation in this chapter has the form "guess the shape of
> $E_\text{xc}[\rho]$". They differ in what they guess from — uniform
> electron gas, gradient expansions, exact exchange on a model system,
> empirical fits to a training set — and in how well they generalise.

## 5.1 The uniform electron gas

Every modern XC functional traces an ancestor to the **uniform
electron gas** (UEG): a hypothetical system of $N$ electrons in a box
of volume $V$ with a constant positive background charge. The UEG
is parameterised by the **Wigner–Seitz radius**

$$
r_s = \left( \frac{3}{4\pi n} \right)^{1/3},
$$

where $n = N / V$ is the density. The exchange–correlation energy
*per electron* of the UEG, $\varepsilon_\text{xc}(r_s)$, has been
computed by quantum Monte Carlo to high accuracy (Ceperley & Alder,
1980; refined by many authors since).

The **local density approximation** is, almost by definition, the
first rung of Jacob's ladder:

$$
E_\text{xc}^\text{LDA}[\rho] = \int \rho(\mathbf r)\, \varepsilon_\text{xc}^\text{UEG}(\rho(\mathbf r))\, d\mathbf r.
$$

The L (local) in LDA does all the work: it pretends the *real* density
$\rho(\mathbf r)$ is locally uniform, and uses the UEG result point
by point.

> **Tip.** LDA is unexpectedly good for systems that *are* close to the
> uniform electron gas: simple $sp$ metals, jellium surfaces, the
> interiors of nearly-free-electron solids. It is *bad* for systems
> with strong density gradients: atoms, molecules, surfaces, $d$- and
> $f$-electron materials.

## 5.2 GGA — adding the gradient

The next rung adds the **gradient** $\nabla \rho$ as a local variable.
The general form is

$$
E_\text{xc}^\text{GGA}[\rho] = \int f(\rho(\mathbf r), \nabla\rho(\mathbf r))\, d\mathbf r.
$$

The function $f$ is not derivable from first principles. It is
constructed by:

- **Constraint satisfaction** (PBE, 1996): write down the analytical
  conditions that the exact $f$ must satisfy — the gradient expansion
  at small $s = \lvert \nabla\rho \rvert / (2 k_F \rho)$, the LDA
  limit at small $s$, the Lieb–Oxford bound — and find the simplest
  $f$ that satisfies all of them.
- **Empirical fitting** (B88, LYP): parametrise $f$ and fit a handful
  of parameters to a set of atomic and molecular benchmarks.

| Functional | Year | Strategy        | Best for                                | Watch out for                              |
|:-----------|:-----|:----------------|:----------------------------------------|:-------------------------------------------|
| LDA        | 1980 | Uniform gas     | Simple metals, jellium                  | Atoms, molecules, surfaces                 |
| PW91       | 1991 | Constraint      | Solid-state physics                     | Molecules                                  |
| PBE        | 1996 | Constraint      | General-purpose solid state             | Strongly-correlated systems                |
| BLYP       | 1988 | Empirical       | Main-group chemistry                    | Metals, semiconductors                    |
| BP86       | 1988 | Empirical       | Main-group chemistry                    | Metals                                     |

> **Note.** PBE is the *de facto* default functional for solid-state
> physics. B3LYP is the *de facto* default for main-group quantum
> chemistry. They were not designed for the other's regime, and using
> them outside their sweet spots is asking for trouble.

## 5.3 Meta-GGA — adding the kinetic-energy density

The third rung adds the **orbital kinetic-energy density**
$\tau = \frac{1}{2} \sum_i \lvert \nabla \phi_i \rvert^2$. Two
consequences:

1. The functional can distinguish **single-orbital** regions (bonds,
   lone pairs) from **multi-orbital** regions (atom cores), which a
   GGA cannot do.
2. The functional can detect **bonding character**: $\tau$ behaves
   differently in covalent, metallic, and weak-interaction regions.

The most successful meta-GGA of the last decade is **SCAN** (Sun,
Ruzsinszky, Perdew, 2015). It satisfies 17 known exact constraints of
the XC functional and is parameter-free.

| Functional | Year | Strategy                  | Best for                                |
|:-----------|:-----|:--------------------------|:----------------------------------------|
| TPSS       | 2003 | Constraint                | Solid state, lattice constants          |
| SCAN       | 2015 | Constraint (17)           | General purpose, surfaces, 2-D materials |
| r²SCAN     | 2021 | Regularised SCAN          | Same as SCAN, more numerically stable   |

## 5.4 Hybrids — adding a fraction of exact exchange

The fourth rung **mixes in a fraction** of non-local HF exchange:

$$
E_\text{xc}^\text{hybrid} = a \, E_\text{x}^\text{exact} + (1 - a)\, E_\text{x}^\text{GGA} + E_\text{c}^\text{GGA}.
$$

The factor $a$ is in the range $0.2$–$0.3$ for "global" hybrids.
B3LYP (Becke, 3-parameter, Lee–Yang–Parr) is the workhorse:

$$
E_\text{xc}^\text{B3LYP} = 0.20\, E_\text{x}^\text{exact} + 0.08\, E_\text{x}^\text{LDA} + 0.72\, E_\text{x}^\text{B88} + 0.81\, E_\text{c}^\text{LYP} + 0.19\, E_\text{c}^\text{VWN}.
$$

The coefficients are fit to a training set of atomisation energies.
B3LYP works well for main-group thermochemistry; it works less well
for barrier heights, non-covalent interactions, transition-metal
chemistry, and band gaps.

> **Warning.** B3LYP is *not* a universal default. It is the
> *historical* default of organic chemistry, and there are many
> systems where it is now known to be misleading. Always check what
> the field has converged on for *your* system class.

## 5.5 Range-separated hybrids

The fifth rung is the realisation that exact exchange is
**range-dependent**. The long-range part of the Coulomb interaction
*is* screened in real materials and is poorly described by the GGA;
the short-range part is well described by the GGA. A
**range-separated hybrid** writes

$$
\frac{1}{r_{12}} = \underbrace{\frac{\text{erfc}(\omega r_{12})}{r_{12}}}_\text{short range, DFT} + \underbrace{\frac{\text{erf}(\omega r_{12})}{r_{12}}}_\text{long range, exact exchange},
$$

and treats the two pieces with different functionals. The
**range-separation parameter** $\omega$ controls the split: small
$\omega$ means more exact exchange in the bulk, large $\omega$ means
less.

| Functional | $\omega$ (bohr⁻¹) | Use case                                        |
|:-----------|:------------------|:------------------------------------------------|
| CAM-B3LYP  | 0.33               | Excited states, Rydberg, charge transfer        |
| LC-ωPBE    | 0.40               | Long-range CT excitations, organic electronics  |
| ωB97X-D    | 0.25               | Main-group thermochemistry + dispersion         |
| HSE06      | 0.11 (screened)   | Solid-state physics, screened-exchange limit    |

## 5.6 The full zoo

For reference, the functionals most commonly seen in production
DFT codes (as of writing):

| Functional        | Class             | Chemistry strength        | Solid-state strength     | Cost        |
|:------------------|:------------------|:--------------------------|:-------------------------|:------------|
| LDA               | Local             | Poor                      | Good (free-electron)     | $O(K)$      |
| PBE               | GGA               | Mediocre                  | Good                     | $O(K)$      |
| BLYP              | GGA               | Good                      | Mediocre                 | $O(K)$      |
| SCAN              | Meta-GGA          | Good                      | Good                     | $O(K)$      |
| B3LYP             | Global hybrid     | Good                      | Bad (band gap)           | $O(K^4)$    |
| PBE0              | Global hybrid     | Good                      | OK                       | $O(K^4)$    |
| HSE06             | Screened hybrid   | OK                        | Excellent                | $O(K^4)$    |
| ωB97X-D           | RS hybrid + D     | Excellent                 | OK                       | $O(K^4)$    |
| B2PLYP            | Double hybrid     | Excellent                 | Poor                     | $O(K^5)$    |
| RPA@PBE           | Post-KS           | Excellent                 | Excellent                | $O(K^4)$    |

## 5.7 A short decision tree

> **Tip.** If you don't know what functional to use, here is a rough
> decision tree. It is *not* a substitute for reading the recent
> literature on your system class.
>
> 1. **Solid state, band structure, semiconductors** → HSE06 or SCAN.
> 2. **Main-group organic chemistry** → ωB97X-D or B3LYP-D3.
> 3. **Transition-metal complex, single-reference** → TPSSh or
>    ωB97X-D.
> 4. **Strong correlation** → DFT is the wrong tool. Use a
>    multireference method, DFT+U, or DMFT.
> 5. **Van der Waals / dispersion-dominated** → Use a functional with
>    a D3 or D4 correction, or use a non-local correlation functional
>    (vdW-DF).
> 6. **High-throughput screening** → PBE or PBE+U, accept the noise,
>    filter outliers.
>
> **Disclaimer.** Functional recommendations in DFT are a moving
> target. A functional that was state-of-the-art in 2015 (e.g. M06-2X)
> is often superseded by a better one in 2025. Always check the
> literature for your *specific* system class.

## 5.8 What's next

We have completed the *theoretical* part of these notes. A natural
follow-on — out of scope here — is the **practical** side: basis sets,
pseudopotentials, periodic-boundary conditions, convergence
acceleration, and code-specific tricks. A good DFT course covers at
least the first three of these; the last is learned in the trenches.

> Back to the [index]({{ "/dft-notes/" | relative_url }}) — or revisit
> [chapter 04]({{ "/dft-notes/chapter-04/" | relative_url }}) for the
> Kohn–Sham equations these functionals plug into.
