---
layout: page
title: "Python codes — Chapter 03"
permalink: /dft-notes/python_codes/chapter-03/
description: >-
  Runnable Python that accompanies Chapter 03 (Hartree–Fock): from-scratch
  Roothaan–Hall SCF for H₂ in STO-3G, the H₂ dissociation curve,
  and a comparison of SCF convergence methods (plain, linear mixing, DIIS).
---

# Chapter 03 — Python codes

Three scripts that together implement Hartree–Fock from scratch, in only
`numpy` + `scipy.special.erf` + `scipy.linalg.eigh`.  No quantum-chemistry
package is imported — every integral is built from the Boys $F_0$ function
and the Gaussian product formulas of Szabo & Ostlund Appendix A.  The
first script is the source of truth for the $E_\mathrm{HF} = -1.1167\,E_h$
number quoted in §3.6.7; the second sweeps the bond length to draw the
dissociation curve discussed in §3.5; the third illustrates the
convergence aids of §3.8 on a 4-atom problem that's actually hard enough
to need them.

| #  | Script | Plot | Chapter section | What it does |
|:---|:-------|:-----|:----------------|:-------------|
| 01 | [01-h2-sto3g-scf.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_03/01-h2-sto3g-scf.py) | [01-h2-sto3g-scf.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_03/plots/01-h2-sto3g-scf.png) | §3.6 Roothaan–Hall in a Gaussian basis | Builds $S$, $T$, $V$, $(\mu\nu\lvert\lambda\sigma)$ analytically for two STO-3G H 1s functions at $R = 1.4\,a_0$, runs the from-scratch Roothaan–Hall SCF from $P=0$, and plots $E_\mathrm{elec}$ versus iteration.  Converges in 3 iterations to $E_\mathrm{HF} = -1.116714\,E_h$. |
| 02 | [02-h2-dissociation.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_03/02-h2-dissociation.py) | [02-h2-dissociation.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_03/plots/02-h2-dissociation.png) | §3.5 What Hartree–Fock gets wrong | Scans $R \in [0.4, 6.0]\,a_0$ in 55 points and plots the RHF dissociation curve.  Locates $R_e = 1.355\,a_0$ and $D_e = 0.118\,E_h$ (vs the exact $2 E_H = -1.0$ limit).  Shows the textbook RHF dissociation failure: at $R = 6\,a_0$ the curve sits at $-0.645\,E_h$, well *above* the correct $2E_H = -1.0\,E_h$ limit. |
| 03 | [03-scf-mixing-demo.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_03/03-scf-mixing-demo.py) | [03-scf-mixing-demo.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_03/plots/03-scf-mixing-demo.png) | §3.8 Direct SCF, conventional SCF, and DIIS | Compares plain Roothaan–Hall, linear density mixing ($\alpha = 0.5$), and Pulay DIIS on an H$_4$ linear chain (4 atoms, 4 basis functions, 4 electrons) starting from a deliberately bad initial guess.  Plots $\lvert E^{(k)} - E_\mathrm{ref}\rvert$ on a log scale.  DIIS hits $10^{-6}\,E_h$ in 6 iterations; plain takes 9; linear mixing takes 25. |

## How to run

From the repo root:

```bash
# all three scripts at once
for f in dft_notes/python_codes/chapter_03/0?-*.py; do
    python "$f"
done

# or individually
python dft_notes/python_codes/chapter_03/01-h2-sto3g-scf.py
python dft_notes/python_codes/chapter_03/02-h2-dissociation.py
python dft_notes/python_codes/chapter_03/03-scf-mixing-demo.py
```

Each script writes its PNG to `dft_notes/python_codes/chapter_03/plots/`.

## Dependencies

`numpy`, `scipy` (`linalg.eigh`, `special.erf`), `matplotlib` (with
`matplotlib.use("Agg")` for headless runs).  Nothing else.  See
[python_codes/]({{ site.baseurl }}/dft-notes/python_codes/) for the
repo-wide pinned versions.
