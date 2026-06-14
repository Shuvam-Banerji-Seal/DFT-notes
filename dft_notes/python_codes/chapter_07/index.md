---
layout: page
title: "Chapter 07 — Python codes"
permalink: /dft-notes/python_codes/chapter-07/
description: >-
  Python samples for chapter 07 (Solids & PBC) — free-electron
  band structure of a 1-D cosine potential.
---

# Chapter 07 — Python codes

| #  | Script | Plot | What it does |
|:---|:-------|:-----|:-------------|
| 01 | [01-free-electron-bands.py]({{ '/dft-notes/python_codes/chapter_07/01-free-electron-bands.py' | relative_url }}) | [01-free-electron-bands.png]({{ '/dft-notes/python_codes/chapter_07/plots/01-free-electron-bands.png' | relative_url }}) | Builds the 21×21 plane-wave Hamiltonian in reciprocal space for $V(x) = -0.5\cos(2\pi x/a)$ at $a = 5$ bohr, diagonalises at 100 k-points, plots the first 4 bands. The BZ-boundary gap of 0.488 E_h matches the 2×2 analytic leading-order result. |

Run from the repo root:

```bash
python dft_notes/python_codes/chapter_07/01-free-electron-bands.py
```

See [python_codes/]({{ '/dft-notes/python_codes/' | relative_url }}) for the conventions and dependencies.
