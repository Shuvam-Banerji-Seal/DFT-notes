# DFT Notes

> A curated, SEO-friendly knowledge base on **Density Functional Theory (DFT)** — the workhorse of modern quantum chemistry, computational materials science, and electronic-structure theory.

[![GitHub Pages](https://img.shields.io/badge/site-live-brightgreen?style=flat-square&logo=github)](https://shuvam-banerji-seal.github.io/DFT-notes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Repo: Shuvam-Banerji-Seal/DFT-notes](https://img.shields.io/badge/repo-DFT--notes-181717?style=flat-square&logo=github)](https://github.com/Shuvam-Banerji-Seal/DFT-notes)
[![Markdown](https://img.shields.io/badge/notes-Markdown-000000?style=flat-square&logo=markdown)](https://commonmark.org/)
[![Math: KaTeX](https://img.shields.io/badge/math-KaTeX-0077b6?style=flat-square)](https://katex.org/)

---

## What is this?

This repository is a **growing, well-organized set of notes on Density Functional Theory (DFT)**, written in plain Markdown with LaTeX-style math, automatically rendered as a fast static website via [Jekyll](https://jekyllrb.com/) and [KaTeX](https://katex.org/) on [GitHub Pages](https://pages.github.com/).

The goal is to give a clear, self-contained path from the **mathematical foundations** of DFT to **practical, hands-on computation** of electronic structure — for students, researchers, and practitioners.

> Density Functional Theory is a quantum-mechanical modelling method used in **physics, chemistry, and materials science** to investigate the electronic structure (principally the ground state) of many-body systems — atoms, molecules, and condensed phases.

---

## Table of Contents

- [Quick start](#quick-start)
- [What you'll find here](#what-youll-find-here)
- [Site & math rendering](#site--math-rendering)
- [Mathematical conventions](#mathematical-conventions)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [References & further reading](#references--further-reading)
- [License](#license)

---

## Quick start

**Read the site online (recommended):**
👉 **[shuvam-banerji-seal.github.io/DFT-notes](https://shuvam-banerji-seal.github.io/DFT-notes/)**

**Browse the notes on GitHub:**
👉 **[github.com/Shuvam-Banerji-Seal/DFT-notes/notes](https://github.com/Shuvam-Banerji-Seal/DFT-notes/tree/main/notes)**

**Clone the repo locally:**

```bash
git clone https://github.com/Shuvam-Banerji-Seal/DFT-notes.git
cd DFT-notes
```

**Run the site locally** (requires Ruby + Bundler):

```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000/DFT-notes/
```

---

## What you'll find here

The notes are organized into thematic modules. Each module is a self-contained Markdown file that you can read in any order, but together they form a coherent curriculum.

| Module | Topic | Status |
| --- | --- | --- |
| 01 | Many-body quantum mechanics primer | planned |
| 02 | Hohenberg–Kohn theorems | planned |
| 03 | Kohn–Sham equations | planned |
| 04 | Exchange–correlation functionals (LDA, GGA, meta-GGA, hybrid) | planned |
| 05 | Basis sets & pseudopotentials | planned |
| 06 | Practical workflows (VASP, Quantum ESPRESSO, Gaussian, ORCA) | planned |
| 07 | Common pitfalls & error estimation | planned |
| 99 | References & further reading | planned |

> The site is intentionally a **living document** — content will be added and refined over time.

---

## Site & math rendering

The static site is built with:

- **[Jekyll](https://jekyllrb.com/)** — static site generator, native to GitHub Pages.
- **[KaTeX](https://katex.org/)** — fast, high-quality math typesetting for the web.
- **[minima](https://github.com/jekyll/minima)** — the default Jekyll theme.
- **Plugins:** `jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-feed`.

Deployment is fully automated via **GitHub Actions** (`.github/workflows/jekyll.yml`) on every push to `main`.

Math is written in standard LaTeX-style delimiters, which GitHub itself also renders:

```latex
$$
E_\text{XC}[\rho] = \int f(\rho(\mathbf{r}), \nabla\rho(\mathbf{r}), \tau(\mathbf{r})) \, d^3r
$$
```

---

## Mathematical conventions

Unless stated otherwise, every note uses:

- **Atomic units** ($\hbar = m_e = e = 4\pi\varepsilon_0 = 1$) unless otherwise noted.
- **Bold** symbols for vectors, **blackboard** for operators, **calligraphic** for spaces.
- Real-space coordinates written as $\mathbf{r}$, $\mathbf{r}'$; spin index $\sigma \in \{\uparrow,\downarrow\}$.
- Electronic density $\rho(\mathbf{r})$ is the central variable in Kohn–Sham DFT.
- Spin-polarized vs. spin-paired systems are flagged explicitly per note.

---

## Repository layout

```
DFT-notes/
├── .github/
│   ├── workflows/      # GitHub Actions: build + deploy to Pages
│   └── ISSUE_TEMPLATE/ # Bug report, content suggestion templates
├── _includes/          # KaTeX injection in <head>
├── assets/             # CSS, images, static site assets
├── notes/              # The actual notes (Markdown + LaTeX)
│   ├── README.md       # Index of all notes
│   └── NN-*.md         # Numbered, ordered notes
├── _config.yml         # Jekyll site configuration
├── index.md            # Homepage (renders the site landing page)
├── Gemfile             # Ruby gem pins (for local dev)
├── LICENSE             # MIT
└── README.md           # You are here
```

---

## Contributing

Spotted a typo, a missing citation, or a wrong formula? Contributions are welcome.

- **Open an issue** using the relevant template (bug report / content suggestion).
- **Open a pull request** with your change.

Please preserve the existing math style and conventions. The math in each note is built to be readable both on GitHub (which renders `$...$` and `$$...$$`) and on the rendered site (KaTeX).

---

## Roadmap

- [x] Public repository + GitHub Pages site
- [x] Jekyll + KaTeX math rendering pipeline
- [x] GitHub Actions deploy workflow
- [x] SEO meta tags + sitemap
- [ ] Foundations: many-body QM primer
- [ ] Hohenberg–Kohn theorems
- [ ] Kohn–Sham equations
- [ ] Exchange–correlation functionals deep dive
- [ ] Practical code examples (input files for VASP/QE/ORCA)
- [ ] Search functionality on the site

---

## References & further reading

- Parr, R. G. & Yang, W. — *Density-Functional Theory of Atoms and Molecules* (Oxford, 1989)
- Dreizler, R. M. & Gross, E. K. U. — *Density Functional Theory* (Springer, 1990)
- Kohn, W. (1999). *Nobel Lecture: Electronic structure of matter — wave functions and density functionals.* Rev. Mod. Phys. **71**, 1253.
- Burke, K. — *The ABC of DFT* (free online primer)
- Koch, W. & Holthausen, M. C. — *A Chemist's Guide to Density Functional Theory* (Wiley-VCH)

A longer curated list lives in [`notes/99-references.md`](notes/99-references.md).

---

## License

Released under the [MIT License](LICENSE). Feel free to use, copy, modify, and redistribute — with attribution.
