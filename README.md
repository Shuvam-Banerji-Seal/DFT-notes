# DFT Notes

> A reader-first knowledge base on Density Functional Theory
> (DFT) — the standard workhorse of modern quantum chemistry
> and computational materials science.

This site is built with Jekyll + MathJax 3 + Mermaid, served
from GitHub Pages.  The full design system is documented in
[`design.md`](./design.md); the build process and contributor
workflow are documented in [`agents.md`](./agents.md).

## What you'll find

- **Six shipped chapters** (00 Welcome → 05 XC functionals) that
  walk progressively through DFT: Schrödinger, many-body,
  Hartree–Fock, Kohn–Sham, exchange–correlation functionals.
- **A live chapters map** at `/dft-notes/chapters-map/` — a
  Mermaid graph of every chapter past, present, and planned.
- **Runnable Python** for every chapter, in
  `/dft-notes/python_codes/`.  Generated plots are committed
  alongside the scripts.
- **A light + dark theme** — pastel poppy green by default,
  warm dark for long-session reading.  The switcher is in
  the top nav.
- **A Mermaid-driven knowledge graph** that updates as new
  chapters land.

## Repository structure

```
DFT-notes/
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/bug_report.md
│   ├── pull_request_template.md
│   └── workflows/
│       ├── jekyll.yml           ← build + deploy to Pages
│       └── markdown-lint.yml   ← markdownlint-cli2 (v0.40)
│
├── _includes/                  ← Liquid partials
│   ├── head.html               ← meta + fonts + CSS + SEO + MathJax + Mermaid
│   ├── nav.html                ← top nav, mobile menu, theme switcher
│   ├── footer.html             ← dark navy footer (no chapter list)
│   ├── spike-mark.html         ← reusable 4-spoke radial SVG
│   └── mathjax.html            ← MathJax 3 config
│
├── _layouts/                   ← Jekyll layouts
│   ├── default.html            ← skip + nav + main + footer + JS
│   └── page.html               ← .page-content div for reading column
│
├── assets/
│   ├── css/site.css            ← The design system (CSS variables + components)
│   └── js/
│       ├── nav.js              ← mobile menu toggle
│       ├── theme.js            ← light/dark switcher (persists in localStorage)
│       └── mermaid-init.js     ← Mermaid init, theme-aware
│
├── design.md                   ← The Claude/Anthropic design spec (repo-only)
├── agents.md                   ← The agent handbook (repo-only)
├── README.md                   ← This file
│
├── dft_notes/                  ← The actual content
│   ├── index.md                ← chapter index
│   ├── chapters-map.md         ← Mermaid graph of all chapters
│   ├── chapter_00/00-welcome.md
│   ├── chapter_NN/00-topic.md
│   ├── python_codes/
│   │   ├── README.md           ← how to run, how to add a new script
│   │   ├── chapter_00/
│   │   │   ├── 01-particle-in-box.py
│   │   │   └── plots/01-particle-in-box.png
│   │   └── chapter_NN/
│   └── ...
│
├── _config.yml                 ← Jekyll config
├── Gemfile                     ← jekyll 3.10 + minima + kramdown-parser-gfm
├── 404.md
├── index.md                    ← hero-band home page
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── .markdownlint-cli2.jsonc
└── .gitignore
```

**Do not** add new top-level directories without updating this
file.  New chapters go in `dft_notes/chapter_NN/`.  New Python
scripts go in `dft_notes/python_codes/chapter_NN/`.  New
components go in `assets/css/site.css`.  New layouts go in
`_layouts/`.

## Running locally

Requires Ruby 3.2+ and the `bundler` gem.

```bash
bundle install
bundle exec jekyll serve
```

The site is served at `http://localhost:4000/`.  The GitHub
Pages baseurl is `/DFT-notes`, so all internal links use
`{{ '/path/' | relative_url }}`.

## Running the Python codes

The chapter scripts are tested against **Python 3.11+** with
`numpy<2`, `matplotlib>=3.7`, and `scipy>=1.10`.  Run from the
repo root:

```bash
python dft_notes/python_codes/chapter_00/01-particle-in-box.py
```

Generated plots land in the chapter's `plots/` subfolder and
are committed alongside the script.

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md).  Major changes —
new chapters, new components, design changes — should follow
the agent pattern in [`agents.md`](./agents.md) and the design
spec in [`design.md`](./design.md).

## License

[MIT](./LICENSE) © 2026 Shuvam Banerji Seal.
