---
layout: page
title: "Python codes — Chapter 04"
permalink: /dft-notes/python_codes/chapter-04/
description: >-
  Runnable Python that accompanies Chapter 04 (Kohn–Sham DFT):
  from-scratch KS-LDA SCF for H₂ in STO-3G, a KS-vs-HF comparison,
  and a 1-D jellium slab solved on a real-space grid.
---

# Chapter 04 — Python codes (Kohn–Sham DFT)

Three scripts cover the chapter's three "from-scratch" KS-DFT
worked examples.  The first two are matrix-mechanics companions
to chapter 06's HF machinery — every Gaussian integral
(overlap, kinetic, nuclear attraction, two-electron repulsion)
is built by hand from the Szabo & Ostlund primitive-Gaussian
formulas, exactly as in `chapter_06/01-sto-3g-h2.py`.  The
third script drops the basis set entirely and solves the
1-D Kohn–Sham equations on a real-space grid for a slab of
jellium.

| #  | Script | Plot | What it does |
|:---|:-------|:-----|:-------------|
| 01 | [01-h2-lda-scf.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/01-h2-lda-scf.py) | [01-h2-lda-scf.png]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/plots/01-h2-lda-scf.png) | From-scratch KS-LDA SCF for H₂ in STO-3G.  Builds S, T, V_nuc, and the 2e-tensor (μν\|λσ) by hand; the F_xc matrix is evaluated numerically on a 6 a₀ box, 21 points/side, with `v_xc = (4/3)ε_x` (Dirac) + Wigner correlation.  Linear mixing (α = 0.3) until `|ΔE| < 1e-8`.  Plots the SCF convergence of E_elec. |
| 02 | [02-h2-ks-vs-hf.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/02-h2-ks-vs-hf.py) | [02-h2-ks-vs-hf.png]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/plots/02-h2-ks-vs-hf.png) | Four-method bar-chart comparison at R = 1.4 a₀: RHF/STO-3G, KS-LDA/STO-3G (re-runs script 01), Full CI/STO-3G, Full CI/CBS (non-relativistic exact).  Labels each bar with its value and the gap ΔE relative to RHF. |
| 03 | [03-jellium-slab.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/03-jellium-slab.py) | [03-jellium-slab.png]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/plots/03-jellium-slab.png) | 1-D jellium slab on a 20 a₀ box with N = 10 electrons in a central 10 a₀ slab (r_s = 1 a₀).  Real-space grid (200 points, h ≈ 0.10 a₀), finite-difference Laplacian, Dirichlet BCs, Poisson-solve Hartree & jellium potentials, 1-D Dirac + Wigner XC.  Linear mixing (α = 0.2).  2×2 subplot grid: density, Hartree potential, full KS potential, eigenvalues with `\|ψ₁\|²` overlaid. |

## How to run

From the repo root:

```bash
python dft_notes/python_codes/chapter_04/01-h2-lda-scf.py
python dft_notes/python_codes/chapter_04/02-h2-ks-vs-hf.py
python dft_notes/python_codes/chapter_04/03-jellium-slab.py
```

Each script writes its plot to `dft_notes/python_codes/chapter_04/plots/`
using an absolute path derived from `__file__` (no `os.chdir`).

## Dependencies

`numpy`, `scipy` (`eigh`, `erf`), and `matplotlib` (headless
via `matplotlib.use("Agg")`).  No other packages.  See
[python_codes/]({{ site.baseurl }}/dft-notes/python_codes/) for
the full repository-wide conventions.

## Honest note on the KS-LDA numbers

The simplest defensible Dirac + Wigner LDA used here gives
`E_total ≈ -1.03 E_h` for H₂/STO-3G at R = 1.4 a₀, which sits
*above* the RHF value of -1.117 E_h.  Production-quality LDA
calculations that *do* sit below HF use the Vosko–Wilk–Nusair
(VWN) or Perdew–Wang (PW92) correlation form, both of which
give a much larger `|E_c|` in the r_s ~ 1.5 regime typical of
the H₂ bond.  See the long docstring of
[01-h2-lda-scf.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_04/01-h2-lda-scf.py)
for a longer discussion.  The point of these scripts is to
demonstrate the Kohn–Sham SCF *structure*, not to reproduce a
production total energy.
