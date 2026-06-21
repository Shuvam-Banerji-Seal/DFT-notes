# Manim animations for DFT Notes

This directory holds the Manim animation scripts and rendered videos
that complement the static chapter content. Mermaid diagrams and
`matplotlib' plots are still the workhorses; Manim is reserved for
concepts that are inherently dynamic ("watch the density oscillate
and converge", "watch ψ factorise into a plane wave and a
cell-periodic piece").

## Quick start

```sh
# Install (one-time, heavy: needs ffmpeg, cairo, pango, dvisvgm)
pip install manim

# Render one
cd /path/to/DFT-notes
manim -qm dft_notes/animations/chapter_01/01-particle-in-box.py ParticleInBox
#   -q l = low  (480p15,  fast)
#   -q m = medium (720p30, default for the plan)
#   -q h = high  (1080p60, ~10× slower)

# Render the whole batch
for s in dft_notes/animations/chapter_*/0*.py; do
  manim -qm --disable_caching "$s" "${s%.py}"
done
``'

## File conventions

``'
dft_notes/animations/
├── chapter_NN/
│   ├── NN-slug.py            (the Manim source)
│   ├── videos/
│   │   ├── NN-slug.mp4       (rendered video, 720p30, H.264)
│   │   └── NN-slug.png       (poster frame, last frame of the animation)
│   └── index.md              (per-chapter index, optional)
``'

The naming is the same as the existing `python_codes/' convention
(two-digit prefix, kebab-case slug). The MP4 and PNG live next to the
source so a chapter's animations stay together.

## The script template

Every animation file follows the shape used in the first deliverable,
`chapter_01/01-particle-in-box.py`:

```python
"""
NN-slug.py
==========

<one-line description of what the animation shows>

Scene graph
-----------
1. <step>
2. <step>
…

Why this animation lives in chapter NN's animations folder:
- <reason 1>
- <reason 2>

Run from the repo root:
    manim -qm dft_notes/animations/chapter_NN/NN-slug.py SceneName
Writes to:
    dft_notes/animations/chapter_NN/videos/...
"""

from manim import (Axes, Create, Dot, FadeIn, FadeOut, MathTex,
                   Scene, Text, VGroup, Write, config)
import numpy as np

class SceneName(Scene):
    def construct(self):
        # ... 30-100 lines of Manim code
        pass
``'

The docstring follows the existing `python_codes/' convention
(file header, scene graph, where-it-lives rationale, how-to-run
invocation).

## Embedding in a chapter

Each chapter that has an animation gets a short section like:

```markdown
## 1.X Visualisation

<figure class="dft-animation">
  <video controls preload="metadata" width="100%"
         poster="{{ site.baseurl }}/dft_notes/animations/chapter_01/videos/01-particle-in-box.png">
    <source src="{{ site.baseurl }}/dft_notes/animations/chapter_01/videos/01-particle-in-box.mp4"
            type="video/mp4">
    Your browser does not support embedded video.
    <a href="{{ site.baseurl }}/dft_notes/animations/chapter_01/videos/01-particle-in-box.mp4">Download the MP4</a>.
  </video>
  <figcaption>Figure 1.X — ...</figcaption>
</figure>
``'

CSS for the figure lives in `assets/css/site.css`, in the
`dft-animation' section.

## Status

- [x] `chapter_01/01-particle-in-box.py' — first deliverable
- [ ] `chapter_01/02-hydrogen-orbitals.py'
- [ ] `chapter_02/03-many-body-slater.py'
- [ ] `chapter_03/04-scf-convergence.py'
- [ ] `chapter_04/05-kohn-sham-mapping.py'
- [ ] `chapter_05/06-jacobs-ladder.py'
- [ ] `chapter_07/07-bloch-factorisation.py'
- [ ] `chapter_08/08-pseudopotential-inversion.py'
- [ ] `chapter_10/09-phonon-chain.py'
- [ ] `chapter_13/10-dft-u.py'

See `dft_notes/ANIMATIONS_PLAN.md' for the full plan, risks, and
CI workflow.
