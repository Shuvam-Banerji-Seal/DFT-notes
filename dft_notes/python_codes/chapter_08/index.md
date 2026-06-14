---
layout: page
title: "Chapter 08 — Python codes"
permalink: /dft-notes/python_codes/chapter-08/
description: >-
  Python samples for chapter 08 (Pseudopotentials) — Troullier–
  Martins construction for hydrogen.
---

# Chapter 08 — Python codes

| #  | Script | Plot | What it does |
|:---|:-------|:-----|:-------------|
| 01 | [01-hydrogen-pseudopotential.py]({{ '/dft-notes/python_codes/chapter_08/01-hydrogen-pseudopotential.py' | relative_url }}) | [01-hydrogen-pseudopotential.png]({{ '/dft-notes/python_codes/chapter_08/plots/01-hydrogen-pseudopotential.png' | relative_url }}) | Constructs the Troullier–Martins pseudopotential for hydrogen (Z=1, r_c=0.5 a₀, l=0), inverts the radial Schrödinger equation inside r_c, and plots the all-electron 1s and pseudo wavefunction on the same axes. Norm conservation is verified to ~2 × 10⁻¹⁶. |

Run from the repo root:

```bash
python dft_notes/python_codes/chapter_08/01-hydrogen-pseudopotential.py
```

See [python_codes/]({{ '/dft-notes/python_codes/' | relative_url }}) for the conventions and dependencies.
