# Vendored third-party libraries

This file tracks third-party JavaScript / Python / etc. that the
DFT Notes repo vendors locally (instead of pulling from a CDN at
runtime) so the site has no runtime network dependency.

## Mermaid 10.9.1 — `assets/js/mermaid.min.js`

- **Upstream:** https://github.com/mermaid-js/mermaid
- **Version:** 10.9.1
- **File size:** ~3.3 MB
- **Licence:** MIT
- **Vendored on:** 2026-06-14

### Why we vendor

The user explicitly requested no CDN runtime dependencies.  CDN
URLs (e.g. `https://cdn.jsdelivr.net/npm/mermaid@10/...`) can
fail behind firewalls, offline archives, or aggressive ad
blockers, and they make the site depend on a third party that
can change its URL scheme without warning.  Vendoring a single
3.3 MB file is a one-time cost that buys the site deterministic
rendering forever.

### How to update

```sh
# Download the latest 10.x
curl -sL -o assets/js/mermaid.min.js \
  "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"
# Bump the version number in this file
```

Pin to a specific patch version (not `@latest`) so a future
breaking change in the Mermaid API doesn't break the site
silently.

### Licences

Mermaid is distributed under the MIT licence.  The full licence
text is in the upstream repository:
https://github.com/mermaid-js/mermaid/blob/develop/LICENSE

The relevant permission notice:

> Copyright (c) 2014-2024 Knut Sveidqvist
>
> Permission is hereby granted, free of charge, to any person
> obtaining a copy of this software and associated documentation
> files (the "Software"), to deal in the Software without
> restriction, including without limitation the rights to use,
> copy, modify, merge, publish, distribute, sublicense, and/or
> sell copies of the Software, and to permit persons to whom the
> Software is furnished to do so, subject to the following
> conditions:
>
> The above copyright notice and this permission notice shall be
> included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
> OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
> NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
> HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
> FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
> OTHER DEALINGS IN THE SOFTWARE.
