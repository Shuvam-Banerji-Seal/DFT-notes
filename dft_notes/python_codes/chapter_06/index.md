---
layout: page
title: "Chapter 06 — Python codes"
permalink: /dft-notes/python_codes/chapter-06/
description: >-
  Python samples for chapter 06 (Basis sets) — STO-3G H2 from
  scratch, no PySCF.
---

# Chapter 06 — Python codes

| #  | Script | Plot | What it does |
|:---|:-------|:-----|:-------------|
| 01 | [01-sto-3g-h2.py]({{ '/dft-notes/python_codes/chapter_06/01-sto-3g-h2.py' | relative_url }}) | [01-sto-3g-h2.png]({{ '/dft-notes/python_codes/chapter_06/plots/01-sto-3g-h2.png' | relative_url }}) | Constructs a STO-3G basis for H₂ at 1.4 a₀, builds S, h, F by hand, runs Hartree–Fock SCF, and plots the two lowest molecular orbitals. Reproduces Szabo & Ostlund Table 3.5 (`E_HF = -1.1167 E_h`). |

Run from the repo root:

```bash
python dft_notes/python_codes/chapter_06/01-sto-3g-h2.py
```

See [python_codes/]({{ '/dft-notes/python_codes/' | relative_url }}) for the conventions and dependencies.
