# DFT Notes — Manim animation plan

> Scope: design the pipeline for high-quality mathematical animations
> that live alongside the static chapter content, and pick the first
> batch to produce.

**Status: draft, awaiting review.** Do not start rendering yet.

---

## 1. Why Manim

The chapters already use two visual aids:

| Aid | Tool | Use today |
|---|---|---|
| Inline Mermaid diagrams | Mermaid 10 (vendored) | Every chapter's structure, SCF loops, Jacob's ladder |
| Python plots | `matplotlib` (`Agg`) | All numerics, tables, convergence curves |

Both are **static** — they show the end-state of a calculation. For
concepts that are inherently dynamic ("watch the density oscillate and
converge", "watch ψ factorise into a plane wave and a cell-periodic
piece") the right tool is a short animated clip.

**Manim Community Edition** (the `manim` PyPI package) is the standard
for this in 2025. It produces MP4 / GIF / WebM from Python scripts
using a small, well-designed scene-graph API, and it is the same
engine behind 3Blue1Brown's videos. We will use the Community Edition,
not the original `manimgl`, because the latter is bound to a C
binary that is fragile to install.

### Why not alternatives

| Tool | Verdict |
|---|---|
| Lottie / Bodymovin (vector) | Lovely for icons and short loops, but DFT animations need axes, grids, and many simultaneous curves — vector would be ~10× the size. |
| D3 / p5.js (interactive JS) | Right tool for *interactive* visualisations (sliders, hover, drag) — deferred to a later tier. |
| Animated SVG / CSS | Right tool for very small icons (rotating arrow, pulsing dot). One or two of these in the plan. |
| Hand-drawn video (After Effects, Blender) | Highest visual quality, lowest reproducibility. Out of scope. |

Manim sits in the sweet spot: reproducible, scriptable, committed
alongside the rest of the source.

---

## 2. Tier strategy

Three tiers, with Tier 1 being this plan's deliverable.

| Tier | Tool | What goes here | When |
|---|---|---|---|
| **1. Manim MP4 clips** | `manim` Community Edition | The big concepts: particle in a box, H-atom orbitals, SCF iteration, Bloch factorisation, KS mapping, pseudopotential construction, DFT+U, … | **Now** |
| **2. Interactive JS** | p5.js or three.js | Concepts that benefit from a slider or a drag handle: "vary L and watch E₁ change", "rotate a 3-D orbital" | After Tier 1 ships |
| **3. Animated SVG** | inline `<animate>`, CSS keyframes | Tiny inline accents: a rotating 3-vector, a pulsating marker, an auto-drawing equation | Ad-hoc, opportunistic |

Tier 1 is this plan. Tier 2 and 3 are noted in `agents.md` as
`agent:visualizer` follow-up work.

---

## 3. The first batch (10 animations)

Curated for *clarity of concept*, not visual flair. Order = the order
they should be produced, fastest-to-easiest first.

| # | Slug | Chapter | Title | Concept |
|---|---|---|---|---|
| 1 | `01-particle-in-box` | ch01 | The first four particle-in-a-box eigenfunctions | ψ_n(x) and \|ψ_n\|² drawn live, with a moving "where is the particle" dot |
| 2 | `02-hydrogen-orbitals` | ch01 | The first nine hydrogen atomic orbitals | 1s, 2s, 2p, 3s, 3p, 3d shown as isosurfaces or radial plots |
| 3 | `03-many-body-slater` | ch02 | Building a Slater determinant | Two spin-orbitals → antisymmetrised 2×2 product, with the exchange hole drawn |
| 4 | `04-scf-convergence` | ch03 | An SCF cycle that almost diverges, then converges | Density matrix oscillates, then settles; the Fock eigenvalues are traced |
| 5 | `05-kohn-sham-mapping` | ch04 | The Hohenberg–Kohn bijection | V_ext(r) ⇄ ρ(r) shown as a forward / inverse arrow, with a one-to-one correspondence highlighted |
| 6 | `06-jacobs-ladder` | ch05 | Climbing Jacob's ladder | A small "character" climbs the rungs; cost and accuracy bars grow as it ascends |
| 7 | `07-bloch-factorisation` | ch07 | Plane wave × cell-periodic | A 1-D periodic potential and a Bloch state shown as e^{ikr} × u(r); k varies and the wavevector arrow slides |
| 8 | `08-pseudopotential-inversion` | ch08 | Troullier–Martins inversion | The all-electron 1s and the pseudo 1s drawn on top of each other, with V(r) shown inverted between them |
| 9 | `09-phonon-chain` | ch10 | Atoms in a 1-D chain | A row of masses on springs; the optical and acoustic modes animate as eigenmodes |
| 10 | `10-dft-u` | ch13 | LDA fails, LDA+U fixes it | A 3-orbital Hubbard model: with U=0 the gap is 0; with U>0 the gap opens; the projected DOS splits into lower/upper Hubbard bands |

Each one is a **20-40 second clip** at 720p, 30 fps.

---

## 4. File structure

Mirrors the existing `python_codes/` convention exactly.

```
dft_notes/
├── animations/                       ← new top-level folder
│   ├── README.md                     (how to render locally + in CI)
│   ├── index.md                      (a gallery page, optional, deferred)
│   ├── chapter_01/
│   │   ├── 01-particle-in-box.py
│   │   ├── 02-hydrogen-orbitals.py
│   │   ├── videos/
│   │   │   ├── 01-particle-in-box.mp4
│   │   │   ├── 01-particle-in-box.png   (poster frame)
│   │   │   └── 02-hydrogen-orbitals.mp4
│   │   │   └── 02-hydrogen-orbitals.png
│   │   └── index.md                  (per-chapter animation index)
│   ├── chapter_02/
│   │   ├── 03-many-body-slater.py
│   │   └── videos/…
│   └── …
└── (everything else unchanged)
```

Naming rules — same as the Python-codes convention:

- Two-digit numeric prefix, dash, kebab-case slug, `.py` for the
  source and `.mp4` for the rendered video.
- One script produces one video → the video is named
  `videos/<same prefix>-<same slug>.mp4`.
- The poster frame is `<same prefix>-<same slug>.png` (the last
  frame of the animation, captured by Manim).

### Why a new top-level folder

I considered `dft_notes/python_codes/chapter_NN/videos/` (mirroring
the existing `plots/` convention). The reason to make a separate
top-level `animations/` folder is that the **rendering pipeline is
distinct** (Manim is a heavy install, ffmpeg + cairo + pango
required, separate CI job). Keeping animations in their own tree
makes the dependency story cleaner and lets the GitHub Actions
workflow skip Manim on PRs that only touch chapter markdown.

---

## 5. Render pipeline

### Local

```sh
# install once
pip install manim

# render one
cd /path/to/DFT-notes
manim -qm dft_notes/animations/chapter_01/01-particle-in-box.py ParticleInBox
#   -q l = low  (480p15,  fast)
#   -q m = medium (720p30, default for the plan)
#   -q h = high  (1080p60, ~10× slower)
#   -q k = 4k    (not used)

# render the whole batch
for s in dft_notes/animations/chapter_*/0*.py; do
  manim -qm --disable_caching "$s" "${s%.py}"
done
```

The script writes the .mp4 to `videos/<class-name>/720p30/`. A small
post-processing step (`scripts/render_animations.py`) renames to
`videos/NN-slug.mp4` and captures a poster PNG with `ffmpeg -ss ...`.

### CI

A new GitHub Actions workflow, `.github/workflows/animations.yml`:

- Trigger: push to `main` that touches `dft_notes/animations/**/*.py`,
  OR manual `workflow_dispatch`.
- Matrix over the 10 chapters (10 parallel jobs, each rendering 1
  animation at `-qm`).
- Cache pip wheels and Manim's LaTeX template cache across runs.
- Upload rendered .mp4 and poster .png as artifacts.
- Commit them back with `git-auto-commit` (or open a PR if the
  user has a bot account) — *or* open a follow-up PR. The
  recommended default is **PR not push** so the human reviews the
  diff.

Total CI time budget: ~6 min per animation × 10 animations in
parallel = ~6 min wall time on GitHub-hosted runners (free tier).
Fits within the 6-hour job limit with massive headroom.

### Caching

Most of the render time is LaTeX / font / cairo cache. The
workflow will:

1. Cache `~/.cache/manim` between runs (key on Manim version +
   lockfile hash).
2. Use `--disable_caching` only for the *animation* cache, not the
   *system* cache. (Manim's `--disable_caching` flag is about the
   per-scene render cache, not the system font cache.)

---

## 6. Jekyll integration

Each chapter that has an animation gets a short section:

```markdown
## 1.10 Visualisation

<figure class="dft-animation">
  <video controls preload="metadata" width="100%"
         poster="{{ site.baseurl }}/dft_notes/animations/chapter_01/videos/01-particle-in-box.png">
    <source src="{{ site.baseurl }}/dft_notes/animations/chapter_01/videos/01-particle-in-box.mp4"
            type="video/mp4">
    Your browser does not support embedded video.
    <a href="{{ site.baseurl }}/dft_notes/animations/chapter_01/videos/01-particle-in-box.mp4">Download the MP4</a>.
  </video>
  <figcaption>Figure 1.4 — the first four particle-in-a-box eigenfunctions
    and their probability densities. Rendered with <a href="…">Manim</a>;
    source script in <a href="…">chapter 1's animation folder</a>.</figcaption>
</figure>
```

CSS (in `assets/css/site.css`, new section) handles the figure,
caption, and a poster-frame hover. `preload="metadata"` keeps the
page light — the browser fetches only the first frame and the
duration, not the whole video, until the user clicks play.

### Autoplay policy

**Do not autoplay with sound.** Sound is opt-in only.
**Do not autoplay at all on the page-load.** Autoplay with sound is
anti-pattern; autoplay muted is OK for decorative loops but **DFT
animations are explanatory, not decorative** — the reader needs
to see the whole thing at their own pace.

So: no `autoplay` attribute. The reader clicks play.

### Caching & bandwidth

- The site is on GitHub Pages → all videos served from the
  `Shuvam-Banerji-Seal.github.io/DFT-notes` origin.
- Cloudflare caches static assets on the edge. Videos will be
  cached aggressively (they have hashes in the URL).
- Each video is **5-10 MB** (720p30, H.264 CRF 22, 20-40 s).
  10 animations × 7.5 MB ≈ 75 MB total video budget.
- Well under the GitHub Pages 1 GB soft limit and the 100 MB-per-file
  recommended cap.

### The optional gallery page

Deferred. The `extras/10-visualizations.md` gallery is nice-to-have
but not required for the first batch — the per-chapter embeds give
each animation context (a particle-in-box animation in ch01, next
to the postulates discussion, is more useful than a gallery that
decouples the video from the equation). We can add the gallery
later if/when there are enough animations to warrant it.

---

## 7. The Manim script template

Every animation file follows the same shape, adapted from the
Python-codes convention.

```python
"""
01-particle-in-box.py
======================

The first four particle-in-a-box eigenfunctions, animated.

Scene graph
-----------
1.  Draw the potential well V(x) = 0 for 0 < x < L, +∞ outside.
2.  Draw the axis and the boundary labels.
3.  For n = 1, 2, 3, 4 (sequenced):
      - write the equation ψ_n(x) = sqrt(2/L) sin(nπx/L) on the left
      - plot ψ_n(x) on the right, with the same axes scale
      - animate a dot moving at the group velocity of |ψ_n|²
4.  Fade to a panel of all four |ψ_n|² on one set of axes for comparison.

Why this animation lives in chapter 01's animations folder:
- it is the simplest non-trivial quantum-mechanical system
- it is the first eigenstate problem a chemistry student meets
- it sets the visual idiom (axes, wavefunctions drawn as curves) used
  by every later animation

Run from the repo root:
    manim -qm dft_notes/animations/chapter_01/01-particle-in-box.py ParticleInBox
Writes to:
    dft_notes/animations/chapter_01/videos/videos/particle_in_box/720p30/ParticleInBox.mp4
"""

from manim import (Axes, Create, Dot, FadeIn, FadeOut, MathTex,
                   Scene, Text, VGroup, Write, config)

import numpy as np

class ParticleInBox(Scene):
    def construct(self):
        # ... 30-40 lines of Manim code
        pass
```

The docstring follows the existing `python_codes/` convention
(file header, scene graph, where-it-lives rationale, how-to-run
invocation). The `agent:code-runner` workflow for animations is
the same as for the Python codes:

1. Write the source.
2. Render to MP4 (`manim -qm`).
3. Capture the poster frame (`ffmpeg`).
4. Commit source, MP4, and PNG.
5. Embed in the chapter with the snippet from §6.

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Manim install is heavy (system ffmpeg + cairo + pango + dvisvgm) | Document the install in `animations/README.md`; provide a `Dockerfile` (Manim's official `manimcommunity/manim` image is already a great option) and run the local renders through that. |
| Render times blow up — one animation takes 30 min instead of 6 | Cap the medium-quality render at 30 s of *scene time* (not wall time). If a script needs more, the script is too dense — split into two. |
| 720p looks bad on a 1080p monitor | 720p is fine for ~30 s clips. Document the `-qh` option for the user who wants 1080p. |
| Videos don't play on iOS Safari | Use H.264 in MP4 (we are). Add a `playsinline` attribute and a poster frame. Verify in Safari before declaring done. |
| Mermaid and Manim both render large files, slowing page load | Mermaid runs client-side (fast, cached after first paint). Manim is a video tag with `preload="metadata"` (browser fetches ~1 KB until the reader clicks play). |
| Total size explodes past 1 GB | 75 MB video budget + 24 MB of source/scripts is comfortable. A safety net: a CI step that fails the build if `du -sh dft_notes/animations/` exceeds 200 MB. |
| Animation source is updated but the rendered MP4 is stale | CI re-renders on every push that touches the `.py` file, and the rendered MP4 is committed. The reviewer sees both the source diff and the (committed) MP4 diff. |
| A new chapter wants a Manim animation but no agent knows Manim | Document the template in `animations/README.md`; the existing `python_codes/` template is the model. |

---

## 9. The first deliverable

The minimum that proves the pipeline:

1. **`animations/README.md`** — how to install Manim, how to render a
   single file, how to render the whole batch, the file conventions,
   the embedding snippet.
2. **`animations/chapter_01/01-particle-in-box.py`** — the first
   script, 30-60 lines, modelled on the docstring template above.
3. **`animations/chapter_01/videos/01-particle-in-box.mp4`** — the
   rendered clip.
4. **`animations/chapter_01/videos/01-particle-in-box.png`** — the
   poster frame.
5. **An embed of the video in `dft_notes/chapter_01/00-schrodinger-equation.md`**
   in a new `## 1.10 Visualisation` section.
6. **A new CI workflow** at `.github/workflows/animations.yml` that
   renders on push.

The first deliverable is small enough to be reviewed in one PR
and proves the whole pipeline (script → render → poster → embed →
CI). Once that lands, the rest of the batch can be produced in
parallel and merged in larger PRs (2-3 animations per PR).

---

## 10. What this plan does **not** cover

- **Tier 2 (interactive JS visualisations).** The right tool for
  sliders, drag, and parameter sweeps. Not in this plan. Tracked
  separately as `agent:visualizer` follow-up work in `agents.md`.
- **Tier 3 (animated SVG / CSS).** Tiny inline accents. Will be
  added opportunistically when a chapter wants one.
- **The `extras/10-visualizations.md` gallery page.** Deferred
  until there are enough animations to make the page worth
  navigating to.
- **A new `agent:visualizer` role in `agents.md`.** After the
  first batch lands, we add the role to the roster, with the
  template from §7 as the contract.

---

## 11. Open questions

1. **Resolution**: 720p30 or 1080p30? Default `manim -qm` is 720p30.
   The plan says 720p30. Confirm?
2. **Format**: H.264 in MP4 (proposed) or VP9 in WebM (smaller but
   slower to encode, less browser support on older iOS)? The plan
   says H.264. Confirm?
3. **Autoplay**: never autoplay (proposed). Some educational sites
   do autoplay-muted-with-`<video autoplay muted loop>` for short
   loops. We are *not* doing that — the animations are explanatory,
   not decorative. Confirm?
4. **Gallery page**: defer (proposed). The per-chapter embed is
   enough for now. Confirm?

If you say "go" I'll produce the first deliverable (§9) in the next
turn: README, the first script, its MP4 + poster, the embed, and
the CI workflow.
