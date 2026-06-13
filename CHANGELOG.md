# Changelog

All notable changes to the **DFT Notes** knowledge base are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- **Math engine: KaTeX → MathJax 3.** Replaced KaTeX with MathJax 3
  (tex-chtml.js, AMS extensions loaded) in `_includes/head.html`.
  Adds real support for `\begin{equation}`, `\label`, `\ref`, `\eqref`,
  `\begin{align}`, and the full AMS math environment. The new
  `\S 3.7` in `notes/03-kohn-sham.md` demonstrates numbered equations
  with `eq:ks` and `eq:density` labels and `\eqref` cross-references.
  Kramdown now uses `input: GFM` + `math_engine: mathjax` so raw
  LaTeX passes through to the client.
- **CSS pipeline: Sass → plain CSS.** The Jekyll Sass converter was
  silently not running in the GitHub Pages build environment for this
  repo, so all custom rules (body typography, tables, note-boxes,
  mjx-container, tags) were never being served. Moved the file to
  `assets/css/site.css` (plain CSS) and load it after minima's
  `assets/main.css` in `head.html`, so the cascade gives our rules
  priority on overlap.

### Added

- **Cross-device text measurement via chenglou/pretext.** Built the
  pretext submodule (`vendor/pretext/`) with `tsc` and bundled the
  result with esbuild for the browser (50 KB IIFE, attached as
  `window.PretextLayout`). Added `assets/js/text-layout.js` which uses
  pretext's `prepare()` and `layout()` to measure each `h1`–`h4` on
  the page and apply a per-viewport `font-size` that prevents overflow
  at any container width. Re-runs on resize (debounced 200 ms) and
  after MathJax finishes typesetting. CSS `clamp()` remains the
  first-pass guess; pretext is a refinement pass that uses real
  measurements instead of estimates.

### Removed

- `assets/main.scss` — the SCSS source that was never being compiled.
  Replaced by `assets/css/site.css` (plain CSS, identical ruleset).

## [0.0.0] — 2026-06-13

### Added

- Initial public release of the repository.
- Jekyll + MathJax 3 static site with full SEO meta tags, sitemap,
  and JSON-LD.
- GitHub Actions workflows: build + deploy to Pages, Markdown lint, dependabot.
- Issue templates (bug, content, feature) and pull request template.
- Five substantial notes (01-many-body-qm through 04-exchange-correlation
  plus 99-references).
- `vendor/pretext` submodule (chenglou/pretext v0.0.8) for text
  measurement and layout.
- `design.md` — reference design system spec (PreTeXt-flavored, used
  as inspiration rather than implementation).
- MIT license, contributing guide, security policy.
