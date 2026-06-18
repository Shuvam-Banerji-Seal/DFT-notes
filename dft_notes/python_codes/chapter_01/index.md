---
layout: page
title: "Python codes — Chapter 01"
permalink: /dft-notes/python_codes/chapter-01/
description: >-
  Runnable Python that accompanies Chapter 01 (Schrödinger equation):
  particle in a box, finite square well, hydrogen radial orbitals.
keywords: "Python, numpy, scipy, matplotlib, Schrödinger, particle in a box,
  finite square well, hydrogen orbitals, radial wavefunctions"
---

# Chapter 01 — Python codes

> Runnable companions to [Chapter 01 (Schrödinger equation)]({{ site.baseurl }}/dft-notes/chapter-01/) — the three prototype
> one-body problems whose analytic solutions are the building
> blocks of every later chapter.  Each script is the source of
> truth for the numbers quoted in the chapter prose; if a
> caption and a script disagree, the script wins.

The chapter introduces the postulates of quantum mechanics and
applies them to three exactly-soluble one-body problems.  The
scripts here implement those solutions in the cleanest possible
form (analytic eigenfunctions for the particle in a box and
hydrogen, and a numerical root-find for the finite square well)
and produce one plot per script.

| #  | Script | Plot | Chapter section it illustrates |
|:---|:-------|:-----|:-------------------------------|
| 01 | [01-particle-in-box.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_01/01-particle-in-box.py) | [01-particle-in-box.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_01/plots/01-particle-in-box.png) | §1.3 — "A minimal example: the particle in a box".  Closed-form $\psi_n(x) = \sqrt{2/L}\sin(n\pi x/L)$ and $E_n = n^2\pi^2 / 2$ for $L = 1\,a_0$.  Prints $E_1 = \pi^2/2 \approx 4.9348\,E_h$ exactly. |
| 02 | [02-finite-square-well.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_01/02-finite-square-well.py) | [02-finite-square-well.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_01/plots/02-finite-square-well.png) | §1.3 — matching-condition generalisation of the particle in a box.  Solves the transcendental equations for the bound states of a finite well of width $L = 2\,a_0$ and depth $V_0 = 10\,E_h$ and confirms that the well supports **3** bound states. |
| 03 | [03-hydrogen-orbitals.py]({{ site.baseurl }}/dft_notes/python_codes/chapter_01/03-hydrogen-orbitals.py) | [03-hydrogen-orbitals.png]({{ site.baseurl }}/dft_notes/python_codes/chapter_01/plots/03-hydrogen-orbitals.png) | §1.10 — "The hydrogen atom".  Radial eigenfunctions $R_{n\ell}(r)$ for the six lowest states and their radial probability densities $P_{n\ell}(r) = r^2 |R_{n\ell}|^2$, with the analytic mean radii $\langle r\rangle_{n\ell} = a_0(3n^2 - \ell(\ell+1))/2$ marked.  Verifies the 1s peak at $r = a_0$. |

## How to run

From the repo root:

```bash
# Run a single script
python dft_notes/python_codes/chapter_01/01-particle-in-box.py

# Or run all three
for f in dft_notes/python_codes/chapter_01/0?-*.py; do
    python "$f"
done
```

Each script writes its PNG into
`dft_notes/python_codes/chapter_01/plots/` and prints the key
numerical results to stdout.

## Dependencies

`numpy`, `scipy` (only `scipy.optimize.brentq` for the finite-well
root find), and `matplotlib` (headless via `matplotlib.use("Agg")`).
See the top-level [python_codes/]({{ site.baseurl }}/dft-notes/python_codes/)
page for the version pins.
