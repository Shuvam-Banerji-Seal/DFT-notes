# Contributing to DFT Notes

Thanks for your interest in improving this knowledge base. Notes,
corrections, references, examples, and infrastructure improvements are all
welcome.

## How to file an issue

Use the [Bug report](../../issues/new?template=bug_report.md) template
for anything broken — wrong formulas, dead links, build failures,
rendering issues, accessibility problems. Include the page URL and
what you expected vs. what you saw.

For new content suggestions (a new note, a new section in an existing
note, a new reference), open a regular issue and describe what you'd
like to add and why.

## How to make a pull request

1. **Open an issue first** for non-trivial changes. This avoids
   duplicate work and gives the maintainer a chance to weigh in on
   scope and direction.
2. **Fork** the repository and create a branch: `git checkout -b my-change`.
3. **Make your change.** Follow the conventions below.
4. **Verify locally**: `bundle exec jekyll serve`. Open the affected
   page in a browser and check that math renders, links resolve, and
   nothing is visually broken.
5. **Open a pull request** using the PR template. Reference the
   related issue with `Fixes #<n>`.

## Conventions

### Markdown

- Notes are `.md` files in the `notes/` directory. Use lowercase,
  dash-separated filenames: `NN-kebab-name.md`, where `NN` is a
  zero-padded sequence number.
- Every note has YAML front matter with at least `title`, `permalink`,
  and `description`. Use `keywords` for SEO when relevant.
- All notes must be valid CommonMark with kramdown's GFM extensions
  (tables, fenced code blocks, task lists, autolinks).
- The linter (`markdownlint-cli2-action` in CI) enforces style. The
  config is in `.markdownlint-cli2.jsonc` — read it before wondering
  why a rule is disabled.

### Math

- Inline math: `$ ... $`
- Display math: `$$ ... $$`
- Numbered equations: `\begin{equation} ... \label{eq:key} ... \end{equation}`,
  referenced as `\eqref{eq:key}`. Convention: label prefix is `eq:`.
- Math is rendered by **MathJax 3** with AMS extensions loaded. Don't
  write math that depends on features MathJax 3 can't handle (e.g.
  some very recent LaTeX3 packages, exotic Unicode math).
- See any existing note for the working math style.

### Code

- Indent with 2 spaces in `.md`, 2 or 4 in `.html`/`.css`/`.js`.
- No tabs in source files.
- If you're adding a Ruby dep to the Gemfile, pin it with `~>`.
- If you're adding a JS dep, prefer a CDN link over a node_modules
  install. The site is built to be Node-free at runtime.

### Commits

- Imperative mood, present tense: "Fix table contrast in dark mode",
  not "Fixed" or "Fixes".
- One logical change per commit. Don't mix typo fixes with feature
  work.
- Reference the issue number when relevant: "Closes #42".

### Branches and PRs

- One logical change per PR.
- PR title mirrors the commit message: short, imperative, descriptive.
- Use the PR template. Fill in the checklist.
- Expect review iterations. Don't take feedback personally — the
  maintainer is trying to keep the knowledge base accurate and
  consistent.

## Style

- **Prose** — Literata (serif), with `--er-text-prose` clamp() values
  defined in `assets/css/site.css`. Don't override font sizes in
  individual notes.
- **Code** — JetBrains Mono, in `pre` blocks or inline backticks.
- **Math** — see the Math section above. The visual styling of
  equations is owned by `site.css` and `MathJax` — don't reach into
  mjx-container classes from individual notes.
- **Colour** — site-wide themes are defined in `site.css` (six
  themes × light/dark). Don't hardcode colours in a note.

## Local development

```bash
# Install deps
bundle install

# Serve with live reload
bundle exec jekyll serve
```

The site is served at `http://localhost:4000/`. The GitHub Pages baseurl
is `/DFT-notes`, so all internal links should use the `| relative_url`
Jekyll filter, e.g. `[link]({{ '/path/' | relative_url }})`.

## Adding a new note

1. Create `notes/NN-slug.md` with front matter:

   ```yaml
   ---
   layout: page
   title: "NN — Title"
   permalink: /notes/NN-slug.html
   description: "One-sentence description for SEO + meta tags."
   keywords: "comma, separated, keywords"
   ---
   ```
2. Update `notes/README.md` to include the new note in the table of
   contents.
3. If the new note cites papers or books, add them to `notes/99-references.md`.
4. Verify locally and open a PR.

## Code of conduct

Be kind, assume good faith, and help us keep this a welcoming place
for students and researchers of all backgrounds.
