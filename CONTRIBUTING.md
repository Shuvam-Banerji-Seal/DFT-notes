# Contributing to DFT Notes

Thanks for your interest in improving this knowledge base. The notes are a
**living document** and contributions of all sizes are welcome — typo fixes,
new references, better explanations, new notes, and infrastructure improvements.

## Quick links

- [Bug report issue template](.github/ISSUE_TEMPLATE/bug_report.md)
- [Content suggestion issue template](.github/ISSUE_TEMPLATE/content_suggestion.md)
- [Feature request issue template](.github/ISSUE_TEMPLATE/feature_request.md)
- [Pull request template](.github/pull_request_template.md)

## How to contribute

### 1. For small changes (typos, broken links, formula fixes)

- Click the **Edit this page** pencil icon on the rendered site (if present) or
  open the file directly on GitHub.
- Make the change and open a pull request.

### 2. For new content or larger changes

1. **Open an issue first** describing what you'd like to add or change. This
   avoids duplicate work and lets us discuss the right place and scope.
2. **Fork** the repository.
3. **Create a branch** for your change: `git checkout -b my-new-note`.
4. **Make your changes.** Follow the conventions below.
5. **Verify locally**: `bundle install && bundle exec jekyll serve`. Open
   `http://localhost:4000/DFT-notes/` and check that your changes look right
   and that math renders correctly.
6. **Open a pull request** using the provided template.

## Conventions

- **Markdown only.** Notes live under `notes/` and are `.md` files. Use
  lowercase-with-dashes filenames (e.g. `05-basis-sets.md`).
- **Math** is written in LaTeX-style delimiters — `$...$` for inline and
  `$$...$$` for display — which GitHub itself renders. KaTeX on the
  site handles the same syntax. The site also recognises `\(...\)` and
  `\[...\]`.
- **Atomic units** unless explicitly noted otherwise.
- **Front matter**: every note should include at least
  `title`, `permalink`, and `description`. Use `keywords` for SEO where useful.
- **Cross-references**: link between notes with `(/notes/NN-slug.html)`.
- **References**: every new note should cite at least one source. Use the
  format used in `notes/99-references.md`.
- **Style**: be precise, equation-first, but accessible. Include physical
  intuition and at least one worked example or problem where useful.

## Front-matter template

```yaml
---
layout: page
title: "NN — Title of the note"
permalink: /notes/NN-slug.html
description: >-
  One- or two-sentence description for SEO and the page <meta> tag.
keywords: "comma, separated, keywords, dft, keyword"
---
```

## Local development

You need **Ruby ≥ 3.1** and **Bundler**.

```bash
bundle install
bundle exec jekyll serve
```

The site is then available at `http://localhost:4000/DFT-notes/`.

## Reporting security issues

Please do **not** open a public issue for security problems. Instead, follow
the process in [SECURITY.md](SECURITY.md) if present, or contact the
maintainer directly through GitHub.

## Code of conduct

Be kind, assume good faith, and help us keep this a welcoming place for
students and researchers of all backgrounds.
