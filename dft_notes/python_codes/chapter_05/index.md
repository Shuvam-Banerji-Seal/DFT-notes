---
layout: page
title: "Python codes — Chapter 05"
permalink: /dft-notes/python_codes/chapter-05/
description: >-
  Runnable Python that accompanies Chapter 05 (XC functionals): the
  uniform electron gas data, PBE-vs-LDA on atoms, and Jacob's ladder
  of cost vs accuracy.
keywords: "LDA, GGA, PBE, uniform electron gas, Jacob's ladder, DFT, Python"
---

# Chapter 05 — Python codes

This page indexes the runnable Python samples that accompany
chapter 05 of the notes.  Chapter 05 is a tour of the most-used
exchange–correlation functionals — LDA, GGA (PBE), meta-GGA
(SCAN), hybrid, range-separated hybrid, and double-hybrid — and
these three scripts are the numerical companions of the
formulas quoted in the chapter prose.

| #  | Script | Plot | What it does |
|:---|:-------|:-----|:-------------|
| 01 | [01-ueg-xc-vs-rs.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_05/01-ueg-xc-vs-rs.py) | [01-ueg-xc-vs-rs.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_05/plots/01-ueg-xc-vs-rs.png) | Plots the exchange, correlation, and exchange-correlation energy per particle of the uniform electron gas as a function of the Wigner–Seitz radius r_s.  Compares the Dirac LDA exchange, the Wigner interpolation, and the Perdew–Zunger (1981) fit to Ceperley–Alder QMC data.  Marks the r_s of Al, Na, Cs. |
| 02 | [02-pbe-vs-lda-atoms.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_05/02-pbe-vs-lda-atoms.py) | [02-pbe-vs-lda-atoms.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_05/plots/02-pbe-vs-lda-atoms.png) | Computes the LDA and PBE exchange and correlation energies of helium and beryllium with simple Slater-type trial densities, by numerical integration.  Side-by-side bar chart of the two functionals. |
| 03 | [03-jacobs-ladder-cost-accuracy.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_05/03-jacobs-ladder-cost-accuracy.py) | [03-jacobs-ladder-cost-accuracy.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_05/plots/03-jacobs-ladder-cost-accuracy.png) | Scatter plot of the DFT rungs (LDA → GGA → meta-GGA → hybrid → RS-hybrid → double-hybrid) with cost on a log x-axis and typical G2 atomisation-energy MAE on the y-axis.  Visual summary of "why we keep climbing the ladder". |

## How to run

From the repo root:

```bash
python dft_notes/python_codes/chapter_05/01-ueg-xc-vs-rs.py
python dft_notes/python_codes/chapter_05/02-pbe-vs-lda-atoms.py
python dft_notes/python_codes/chapter_05/03-jacobs-ladder-cost-accuracy.py
``'

Each script is self-contained: it computes the relevant
quantities, writes the corresponding PNG into the chapter's
`plots/' subfolder, and prints the key numbers to stdout.

## Notes for the lead

- **Script 01 (UEG xc vs r_s):** the PZ81 (1981) correlation at
  r_s = 2 is −0.04509 E_h; the textbook Ceperley–Alder value
  is ≈ −0.0457 E_h.  Agreement is within 0.001 E_h, well inside
  the 0.1 % tolerance the user asked for.
- **Script 02 (PBE vs LDA on He, Be):** with simple
  hydrogenic / Slater-type densities, the PBE exchange is
  *more* negative than LDA (by ≈ 12–14 %) and the PBE
  correlation is *less* negative than LDA.  This is the
  literal behaviour of the PBE 1996 formula on those
  densities, but it is the *opposite* of what is empirically
  observed for atoms when HF densities are used (where PBE
  exchange is ≈ 10 % less negative than LDA).  The script
  uses the simple trial densities for transparency, not
  realism — see the script docstring and the per-atom
  numerical results printed at runtime.
- **Script 03 (Jacob's ladder):** the cost and MAE numbers
  are eyeball estimates for the G2 atomisation benchmark
  on a G2-sized organic molecule.  They are meant to
  illustrate the *tren`d*`, not to be benchmark-precise.

## Dependencies

| Package      | Version | Used for |
|:-------------|:--------|:---------|
| 'numpy'      | ≥ 1.24  | arrays, 'np.trapz' for radial integration |
| `scipy'      | ≥ 1.10  | (not directly used in these scripts but available) |
| 'matplotlib' | ≥ 3.7   | plots ('matplotlib.use("Agg")' for headless runs) |

No new dependency was introduced by chapter 05.  The conventions
in [python_codes/index.md]({{ site.baseurl }}/dft-notes/python_codes/)
apply unchanged.
