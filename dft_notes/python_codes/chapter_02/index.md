---
layout: page
title: "Chapter 02 — Python codes"
permalink: /dft-notes/python_codes/chapter-02/
description: >-
  Python samples for chapter 02 (The many-body problem):
  H₂⁺ in the Hückel approximation, helium in the minimal
  STO basis, and a full-CI toy for two electrons in two
  orbitals.
---

# Chapter 02 — Python codes

This folder holds the runnable Python that accompanies
chapter 02 (The many-body problem).  The three scripts cover
the three "model systems" that the chapter uses to introduce
the electronic Hamiltonian: a one-electron two-centre problem
(H₂⁺ in Hückel), a two-electron one-centre problem (He in
a single STO), and the simplest possible 2-electron 2-orbital
full CI (H₂ minimal basis).

| #  | Script | Plot | What it does |
|:---|:-------|:-----|:-------------|
| 01 | [01-h2-plus-huckel.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_02/01-h2-plus-huckel.py) | [01-h2-plus-huckel.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_02/plots/01-h2-plus-huckel.png) | H₂⁺ in the Hückel approximation: 2×2 generalised eigenproblem $HC=SC E$ with $S(R)=e^{-R}$ gives $E_\pm(R) = \pm1/(1\pm S)$ and $c_\pm(R)=1/\sqrt{2(1\pm S)}$.  Plots the energies, coefficients, and a snapshot of the two MOs at $R=2\,a_0$. |
| 02 | [02-helium-sto.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_02/02-helium-sto.py) | [02-helium-sto.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_02/plots/02-helium-sto.png) | Helium atom in a single 1s STO: closed-shell singlet energy $E(\zeta)=\zeta^2-4\zeta+\frac{5}{8}\zeta$ minimised at $\zet`a*`=27/16=1.6875$ with $E_{\min}=-729/256=-2.8477\,E_h$.  The plot shows the variational curve, the optimum, and the missing correlation relative to the Hylleraas reference $E=-2.8617\,E_h$. |
| 03 | [03-h2-full-ci-toy.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_02/03-h2-full-ci-toy.py) | [03-h2-full-ci-toy.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_02/plots/03-h2-full-ci-toy.png) | Full CI on the 2-electron, 2-orbital H₂ minimal basis.  Builds the AO integrals (STO-3G), runs RHF, transforms to the MO basis, and diagonalises the 3×3 singlet CI matrix in the $\{|\!gg\rangle,|\!uu\rangle,|(gu)S=0\rangle\}$ basis.  Plots $E_{\rm FCI}(R)$, $E_{\rm RHF}(R)$, and $E_T(R)$. |

## How to run

From the repo root:

```bash
# Run them one at a time
python dft_notes/python_codes/chapter_02/01-h2-plus-huckel.py
python dft_notes/python_codes/chapter_02/02-helium-sto.py
python dft_notes/python_codes/chapter_02/03-h2-full-ci-toy.py

# Or run them all in order
for f in dft_notes/python_codes/chapter_02/0?-*.py; do
    python "$f"
done
```

Each script writes its PNG to `dft_notes/python_codes/chapter_02/plots/`
and prints the key numerical results (energies, coefficients, MO
integrals) to stdout.

## Dependencies

`numpy`, `scipy` (eigh, erf), `matplotlib` with the headless
`Agg` backend.  Same pinned versions as the rest of the
`python_codes/` tree (see [python_codes/]({{ site.baseurl }}/dft-notes/python_codes/)).
