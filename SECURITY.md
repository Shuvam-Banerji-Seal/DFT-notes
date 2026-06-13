# Security

## Supported versions

This repository hosts a Jekyll static site deployed to GitHub Pages.
There is no long-lived server-side state, no user accounts, and no
runtime database. The threat surface is small and primarily concerns
content-injection in Markdown and dependency vulnerabilities in the
build chain.

The `main` branch receives security fixes. Older revisions are not
actively maintained.

## Reporting a vulnerability

If you spot a security issue (e.g. a way to inject arbitrary content
via a Markdown feature, a vulnerable dependency in the Gemfile, a
workflow permission that exceeds what's needed), please **do not open
a public issue**.

Instead, open a **private security advisory**:

<https://github.com/Shuvam-Banerji-Seal/DFT-notes/security/advisories/new>

Or contact the maintainer directly through GitHub.

You should get a response within a few days. We'll triage, fix, and
coordinate disclosure timing if needed.

## Disclosure policy

- Issues are fixed as quickly as practical. Critical issues get
  priority.
- After a fix is merged, a security advisory may be published
  describing the issue and the fix.
- No bug-bounty program at this time.

## Scope

In scope:

- Build-chain vulnerabilities (Ruby gems in the Gemfile, GitHub
  Actions from third parties).
- Content-injection vectors in the Markdown → HTML pipeline.
- Workflow permission escalations (e.g. an action that requests
  more permissions than necessary).

Out of scope:

- Issues in third-party repositories (file them upstream — e.g.
  github-pages, jekyll, jekyll-seo-tag, etc.).
- Denial of service against GitHub Pages itself.
- Theoretical vulnerabilities with no demonstrated impact.
