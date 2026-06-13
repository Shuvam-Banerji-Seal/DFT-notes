# Changelog

All notable changes to the **DFT Notes** knowledge base are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **Full design system (design.md v2.0) applied to the live site.**
  The site now implements the design spec in CSS, HTML, and JS:
  - **Design tokens** — typography (clamp() type scale), spacing, radius
    (defined as `--er-*` CSS custom properties)
  - **12 theme variants** — 6 themes × 2 modes (light/dark). Parchment
    (default), Coffee Green, Obsidian, Midnight, Rose Dusk, Terminal
    Amber. Each theme overrides the same 20 colour tokens; structural
    CSS never references colours directly.
  - **Typography** — Literata (variable serif, ebook-optimised) for
    prose, Inter for UI, JetBrains Mono for code, STIX Two Math for
    math. Optical-size axis (`font-variation-settings: "opsz" N`) set
    per heading level.
  - **Reading column** — `main.page-content .wrapper` self-constrains
    at `min(72ch, 100% - 2 * var(--er-margin-inline))`.
  - **Theme picker UI** — fixed top-right, 6 swatches (one per theme,
    showing each theme's canvas+accent as the preview) + 3 mode
    buttons (light/dark/auto). `assets/js/theme-picker.js` handles
    click events, persists choice to `localStorage` (keys `er-theme`,
    `er-mode`), tracks OS `prefers-color-scheme` for `auto` mode, and
    dispatches a `dft-theme-changed` CustomEvent so other scripts can
    react.
  - **Reading progress bar** — 2px fixed bar at top of viewport,
    rAF-throttled scroll listener, auto-hides on non-scrollable
    pages, re-checks after MathJax + pretext relayout.
  - **Components** — blockquote, code block (with `rouge`-highlighted
    token colours from the theme), figure, footnote/marginal note,
    theorem-like environment boxes (`.er-env` with `theorem`,
    `definition`, `proof`, `example`, `remark`, `algorithm` variants).
  - **Accessibility** — `:focus-visible` outline, `prefers-reduced-
    motion` short-circuits, `forced-colors` (Windows High Contrast)
    overrides, print stylesheet.
- **Updated `design.md` to v2.0** — retargeted from the (misnamed)
  PreTeXt substrate to the actual Jekyll + MathJax 3 + chenglou/pretext
  stack. Front matter now declares the renderer, math engine, and
  text-measurement library, with a `pretext-role` block explaining
  the IIFE bundle + integration. A v2.0 changelog at the top of the
  body documents the retargeting.
- **Custom font links** in `_includes/head.html` — preconnect +
  Google Fonts (Literata + JetBrains Mono + Inter) + jsDelivr
  (STIX Two Math webfont).

### Changed

- **Math engine: KaTeX → MathJax 3.** Replaced KaTeX with MathJax 3
  (tex-chtml.js, AMS extensions loaded) in `_includes/head.html`.
  Adds real support for `\begin{equation}`, `\label`, `\ref`,
  `\eqref`, `\begin{align}`, and the full AMS math environment.
  Kramdown now uses `input: GFM` + `math_engine: mathjax` so raw
  LaTeX passes through to the client. Note 03's § 3.7 demonstrates
  numbered equations with `eq:ks` and `eq:density` labels and
  `\eqref` cross-references.
- **CSS pipeline: Sass → plain CSS.** The Jekyll Sass converter
  was silently not running in the GitHub Pages build environment
  for this repo. Moved the source to `assets/css/site.css` (plain
  CSS) and load it after minima's `assets/main.css` in
  `head.html` so cascade gives our rules priority.
- **`_config.yml` site metadata** updated to describe the new stack
  (Jekyll + MathJax 3 + chenglou/pretext + design.md v2.0 design
  system).
- **`assets/css/site.css`** is now a comprehensive 999-line
  stylesheet (vs the previous 84-line override) implementing the
  full design spec.

## [0.0.0] — 2026-06-13

### Added

- Initial public release of the repository.
- Jekyll static site on GitHub Pages.
- GitHub Actions workflows: build + deploy to Pages, Markdown lint, dependabot.
- Issue templates (bug, content, feature) and pull request template.
- Five substantial notes (01-many-body-qm through 04-exchange-correlation
  plus 99-references).
- `vendor/pretext` submodule (chenglou/pretext v0.0.8) for text
  measurement and layout.
- `design.md` v1.0 — original design system spec (later updated to v2.0
  to reflect actual implementation stack).
- MIT license, contributing guide, security policy.
