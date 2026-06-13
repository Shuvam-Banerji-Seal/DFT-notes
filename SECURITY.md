# Security Policy

## Supported versions

This repository is a **static documentation site** built with Jekyll and
rendered on GitHub Pages. There is no executable server-side code and no
runtime database. As such, "vulnerabilities" here are limited to:

| Aspect | Notes |
| --- | --- |
| Markdown content | The site is static. Nothing executes on the server. |
| GitHub Actions workflows | Pinned to major versions; dependabot keeps them fresh. |
| KaTeX / jQuery / minima | Loaded from jsDelivr CDN; integrity hashes pinned. |
| Jekyll | `github-pages` gem pins the version to a known-good Pages build. |

## Reporting a vulnerability

If you spot a security issue (e.g. a malicious content-injection vector via a
broken link, a compromised CDN, an Actions token leak), please **do not open
a public issue**. Instead:

1. Open a private security advisory at
   <https://github.com/Shuvam-Banerji-Seal/DFT-notes/security/advisories/new>.
2. Or contact the maintainer directly via GitHub.

You should receive a response within a few days.

## Disclosure policy

- Issues will be fixed as quickly as possible, with a coordinated disclosure
  timeline if needed.
- After a fix is merged, the advisory will be published and a note added to
  the release notes / commit history.
