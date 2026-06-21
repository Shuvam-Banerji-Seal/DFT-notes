---
layout: page
title: "Python codes"
permalink: /dft-notes/python_codes/
description: >-
  Runnable Python samples for every chapter, organised by chapter
  folder, with generated plots committed alongside the scripts.
keywords: "Python, numpy, matplotlib, scripts, plots, DFT"
---

# Python codes

> Every Python sample that appears in a chapter also lives here
> as a runnable file, in the same order it appears in the
> chapter.  When a script produces a plot, the PNG is committed
> alongside the script.

This is the **executable** companion to the chapters.  The code
in the chapters is inlined for reading; the code here is
committed, tested, and reproducible.  If you find a discrepancy
between the chapter and the script, the script is the source of
truth — open an issue.

## How to run

From the repo root:

```bash
# Pick a chapter
ls dft_notes/python_codes/

# Run a single script (writes its plot to plots/)
python dft_notes/python_codes/chapter_00/01-particle-in-box.py

# Or run all scripts in a chapter
for f in dft_notes/python_codes/chapter_00/NN-*.py; do
    python "$f"
done
``'

The scripts are tested against **Python 3.11+** with the
following pinned dependencies:

| Package      | Version | Why |
|:-------------|:--------|:----|
| `numpy'      | ≥ 1.24  | arrays, linalg, FFT        |
| `scipy'      | ≥ 1.10  | sparse matrices, special functions, `integrate.solve_ivp' |
| `matplotlib' | ≥ 3.7   | plots (`matplotlib.use("Agg")' for headless) |

Nothing else.  If a chapter needs a new dependency (e.g.
`pyscf`, `ase`, `gpaw`), it is added to this list in the same
PR as the script.

## Conventions

- Scripts are numbered with a two-digit prefix in the order
  they appear in the chapter.  `01-foo.py' appears first in
  the chapter prose; `02-bar.py' appears second; and so on.
- Plots are named with the same prefix and slug, and live in
  the chapter's `plots/' subfolder.
- No script may `os.chdir`; everything is computed and
  written with absolute paths relative to the chapter folder.
- A script that doesn't produce a figure still has the
  prefix — order matters across the whole chapter.
- A `chapter_NN/00-README.md' (optional) is where
  `agent:content-writer' explains anything specific to the
  chapter's scripts (numerical tolerances, expected
  runtime, etc.).

## Index of scripts

| Chapter | Script | What it does |
|:--------|:-------|:-------------|
| 00 | [01-particle-in-box.py]({{ site.baseurl }}/dft-notes/python_codes/chapter_00/01-particle-in-box.py) | Plots the first four particle-in-a-box eigenfunctions and the corresponding probability densities.  Introduces `numpy' arrays, `linalg.eigh`, and `matplotlib`. |

## Where the code goes in the chapter

The chapter template (`agents.md' § "The chapter writing
template") has a **{NN}.3 The code** section.  The code in
that section **must** be a copy-paste of the runnable
script here — not a re-typed ad-hoc version.  If you change
the script, the chapter changes too.
