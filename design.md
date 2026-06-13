---
version: 1.0
name: ebook-design-system
description: >
  A reader-first design system for ebook and long-form academic reading interfaces,
  built on PreTeXt's fluid-layout philosophy. The system is palette-agnostic at its
  core — a token architecture that swaps through six curated reading themes (each
  with light and dark variants) without touching structure or typography. Type is
  anchored in Literata (ebook-optimised serif) for prose, STIX Two Math / Latin
  Modern Math for mathematical notation (rendered via KaTeX), and JetBrains Mono
  for code. The layout engine follows PreTeXt's "know-nothing" column model — fluid
  widths, no fixed breakpoints, everything scales to any viewport.

framework:
  renderer: PreTeXt   # pretext-book.com — XML → HTML pipeline
  math: KaTeX         # katex.min.js + katex.min.css (fallback: MathJax 3)
  math-fallback: MathJax
  fluid-type: true    # clamp()-based type scale; no fixed px sizes in body text
  rtl-ready: true

themes:
  - id: coffee-green
    label: "Coffee Green"
    description: >
      Soft sage green canvas. Restful on the eyes. Preferred by long-session
      readers. Light variant uses near-black forest ink; dark variant inverts
      to very dark moss with pale celadon text.
  - id: parchment
    label: "Warm Parchment"
    description: >
      Traditional sepia/cream book page. Closest to physical paper reading.
      Dark variant uses deep espresso canvas with aged-ivory text.
  - id: obsidian
    label: "Obsidian High-Contrast"
    description: >
      True black canvas with stark white text (light = white page / black ink).
      For readers who want the sharpest possible contrast. Dark variant:
      pure black + neon chartreuse headings.
  - id: midnight
    label: "Midnight Blue"
    description: >
      Cool navy-wash canvas. Cinematic and focused. Light variant is a soft
      blue-grey page; dark is deep navy with glacier-blue text.
  - id: rose-dusk
    label: "Rose Dusk"
    description: >
      Warm blush canvas — gentle contrast, calm atmosphere. Light: faint rose
      page with plum ink. Dark: near-black with dusty rose accents.
  - id: terminal-amber
    label: "Terminal Amber"
    description: >
      Retro phosphor-screen aesthetic. Dark only (light forced to a bone-white
      paper variant). Dark: near-black with amber/gold text and coral accents.
      High-focus, zero eye-strain at night.

default-theme: parchment
default-mode: light
---

## Overview

This is a **reader-first** design system for any ebook, academic text, or long-form
reading interface built on PreTeXt. The design is deliberately minimal at the
structural level — no hero bands, no marketing chrome, no unrelated surface variety.
Every decision serves one goal: putting words in front of the reader without friction.

### Why PreTeXt

PreTeXt (formerly MathBook XML) is the rendering substrate. Key properties:

- **Fluid column model**: content width scales continuously between 320 px and 
  unlimited without a fixed breakpoint list. The reading column self-constrains
  at its optimal character width (~70 ch) and re-centres at every viewport width.
- **Native math pipeline**: PreTeXt emits KaTeX-ready HTML for all 
  `<m>`, `<me>`, `<md>` elements. No post-processing step needed.
- **Accessible by default**: proper ARIA landmarks, skip-nav, logical heading
  order, and keyboard-navigable sidebars come from the framework.
- **Print-ready**: the same source produces screen HTML and a high-fidelity PDF
  (via LaTeX) from one build. Font and spacing tokens carry through both.

### Theme Architecture

The system uses a single CSS custom-property layer (`--er-*` prefix). All six
themes override the same 20 root variables; structural CSS never touches color
or scale directly. Users toggle themes via a `data-theme` + `data-mode` attribute
pair on `<html>`. No JavaScript framework required — pure CSS cascade.

```html
<!-- Default -->
<html data-theme="parchment" data-mode="light">

<!-- User-switched -->
<html data-theme="coffee-green" data-mode="dark">
```

---

## Color Palettes

Each theme exposes **two mode variants** (light / dark). Variables below follow
the pattern `--er-canvas`, `--er-ink`, etc.  The table shows hex values for
each theme × mode combination.

### Token Definitions

| Token | Role |
|---|---|
| `--er-canvas` | Page background — the "paper" |
| `--er-canvas-raised` | Slightly lifted surface (sidebars, callout insets) |
| `--er-canvas-sunken` | Code-block and pull-quote recesses |
| `--er-ink` | Primary body text |
| `--er-ink-soft` | Secondary / muted text (captions, footnotes) |
| `--er-ink-faint` | Decorative rules, very soft dividers |
| `--er-accent` | Heading emphasis, active link, math label accent |
| `--er-accent-soft` | Hover states, subtle highlight strips |
| `--er-link` | Inline hyperlink color |
| `--er-link-visited` | Visited link |
| `--er-selection` | Text selection highlight |
| `--er-math-accent` | KaTeX number / variable tint (overrides default blue) |
| `--er-code-canvas` | Code block background |
| `--er-code-ink` | Code block foreground |
| `--er-code-comment` | Comment token color |
| `--er-code-string` | String token color |
| `--er-code-keyword` | Keyword token color |
| `--er-code-number` | Number token color |
| `--er-focus-ring` | Keyboard-focus outline color |
| `--er-scrollbar-thumb` | Custom scrollbar thumb |

---

### Theme 1 — Coffee Green

> Restful sage. Long-session reading. Zero harsh contrast edges.

#### Light Mode (`data-theme="coffee-green" data-mode="light"`)

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#eef4ec` | Pale sage — very soft, nearly white with a green tint |
| `--er-canvas-raised` | `#e2ede0` | One step greener; sidebar, callout |
| `--er-canvas-sunken` | `#d5e6d2` | Code block recess |
| `--er-ink` | `#1a2e1a` | Dark forest green — primary prose |
| `--er-ink-soft` | `#3d5c3a` | Muted moss — captions, footnotes |
| `--er-ink-faint` | `#8ab08a` | Hairline rules, decorative dividers |
| `--er-accent` | `#2e6b2e` | Forest green — headings and active elements |
| `--er-accent-soft` | `#4a8c4a` | Hover / secondary emphasis |
| `--er-link` | `#2e6b2e` | Consistent with accent |
| `--er-link-visited` | `#6b8c5c` | Desaturated olive for visited |
| `--er-selection` | `#b4d9b4` | Soft sage selection |
| `--er-math-accent` | `#2e6b2e` | Math variables in forest green |
| `--er-code-canvas` | `#ddecd9` | Sunken code block |
| `--er-code-ink` | `#1a2e1a` | Forest ink in code |
| `--er-code-comment` | `#6b8c5c` | Olive muted comments |
| `--er-code-string` | `#5a8a3a` | Medium leaf-green strings |
| `--er-code-keyword` | `#2e5c1a` | Dark keyword tones |
| `--er-code-number` | `#8a5c2e` | Warm amber numbers |
| `--er-focus-ring` | `#2e6b2e` | Clear forest focus ring |
| `--er-scrollbar-thumb` | `#8ab08a` | Soft moss scrollbar |

#### Dark Mode (`data-theme="coffee-green" data-mode="dark"`)

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#0d1a0d` | Very dark moss — true dark reading surface |
| `--er-canvas-raised` | `#162616` | Slightly lifted panels |
| `--er-canvas-sunken` | `#0a130a` | Code recess — slightly deeper |
| `--er-ink` | `#c8e6c0` | Pale celadon — primary text, soft on dark moss |
| `--er-ink-soft` | `#8ab08a` | Muted sage — captions, footnotes |
| `--er-ink-faint` | `#3d5c3a` | Dark hairlines — barely-visible dividers |
| `--er-accent` | `#7dc87d` | Medium-bright sage — headings |
| `--er-accent-soft` | `#5aaa5a` | Hover / secondary |
| `--er-link` | `#7dc87d` | Sage link |
| `--er-link-visited` | `#5c8a5c` | Dimmer visited |
| `--er-selection` | `#2e5c2e` | Subdued dark selection |
| `--er-math-accent` | `#7dc87d` | Celadon math variables |
| `--er-code-canvas` | `#0a1a0a` | Deepest moss for code |
| `--er-code-ink` | `#c8e6c0` | Celadon code foreground |
| `--er-code-comment` | `#5c7d5c` | Subdued olive |
| `--er-code-string` | `#8aba6a` | Leaf green strings |
| `--er-code-keyword` | `#aad47a` | Bright leaf keyword |
| `--er-code-number` | `#d4a85a` | Amber numbers |
| `--er-focus-ring` | `#7dc87d` | Sage focus ring |
| `--er-scrollbar-thumb` | `#3d5c3a` | Muted dark scrollbar |

---

### Theme 2 — Warm Parchment (Default)

> Closest analogue to a physical book. The design system's default.

#### Light Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#f5edd8` | Aged ivory / warm parchment |
| `--er-canvas-raised` | `#ede4cc` | Darker cream for raised panels |
| `--er-canvas-sunken` | `#e4d9bc` | Deep cream code recess |
| `--er-ink` | `#2c1a0e` | Espresso — very dark warm brown |
| `--er-ink-soft` | `#5c3c22` | Medium sienna for secondary |
| `--er-ink-faint` | `#b09070` | Warm tan hairlines |
| `--er-accent` | `#8b4513` | Saddle brown — chapter headings |
| `--er-accent-soft` | `#a0522d` | Sienna hover state |
| `--er-link` | `#8b4513` | Consistent with accent |
| `--er-link-visited` | `#a07050` | Warm tan for visited |
| `--er-selection` | `#e8c88a` | Gold-amber selection |
| `--er-math-accent` | `#8b4513` | Brown math variables |
| `--er-code-canvas` | `#dfd3b5` | Parchment code block |
| `--er-code-ink` | `#2c1a0e` | Espresso code text |
| `--er-code-comment` | `#7a5c3a` | Sienna comments |
| `--er-code-string` | `#5a7a2a` | Olive-green strings |
| `--er-code-keyword` | `#7a2a0a` | Deep rust keyword |
| `--er-code-number` | `#3a5a8a` | Muted blue numbers |
| `--er-focus-ring` | `#8b4513` | Brown focus ring |
| `--er-scrollbar-thumb` | `#b09070` | Tan scrollbar |

#### Dark Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#18100a` | Deep espresso — near-black warm |
| `--er-canvas-raised` | `#241808` | Slightly lighter raised espresso |
| `--er-canvas-sunken` | `#100a04` | Darkest espresso for code |
| `--er-ink` | `#e8d5b0` | Aged ivory — primary text |
| `--er-ink-soft` | `#b09070` | Warm tan for secondary |
| `--er-ink-faint` | `#5c3c22` | Dark sienna hairlines |
| `--er-accent` | `#d4843a` | Warm amber — headings |
| `--er-accent-soft` | `#c46a1a` | Darker amber hover |
| `--er-link` | `#d4843a` | Amber link |
| `--er-link-visited` | `#a0622a` | Dimmer sienna visited |
| `--er-selection` | `#5c3c10` | Deep warm selection |
| `--er-math-accent` | `#d4843a` | Amber math variables |
| `--er-code-canvas` | `#100c06` | Deepest espresso |
| `--er-code-ink` | `#e8d5b0` | Ivory code text |
| `--er-code-comment` | `#7a6040` | Muted sienna |
| `--er-code-string` | `#7ab04a` | Leaf strings |
| `--er-code-keyword` | `#d48050` | Amber keyword |
| `--er-code-number` | `#6a9ad4` | Muted sky numbers |
| `--er-focus-ring` | `#d4843a` | Amber focus ring |
| `--er-scrollbar-thumb` | `#5c3c22` | Dark sienna scrollbar |

---

### Theme 3 — Obsidian High-Contrast

> Maximum legibility. For readers with low vision or strong preference for stark
> contrast. The dark variant adds neon chartreuse headings.

#### Light Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#ffffff` | True white — uncompromising light mode |
| `--er-canvas-raised` | `#f0f0f0` | Very light grey raised panel |
| `--er-canvas-sunken` | `#e0e0e0` | Code block recess |
| `--er-ink` | `#000000` | True black prose |
| `--er-ink-soft` | `#333333` | Dark grey secondary |
| `--er-ink-faint` | `#888888` | Medium grey hairlines |
| `--er-accent` | `#000000` | Black headings — maximum contrast |
| `--er-accent-soft` | `#222222` | Near-black hover |
| `--er-link` | `#0000cc` | Traditional saturated blue link |
| `--er-link-visited` | `#551a8b` | Traditional purple visited |
| `--er-selection` | `#aad4ff` | Classic blue selection |
| `--er-math-accent` | `#0000cc` | Blue math variables (standard KaTeX) |
| `--er-code-canvas` | `#f4f4f4` | Near-white code block |
| `--er-code-ink` | `#000000` | Black code text |
| `--er-code-comment` | `#555555` | Grey comments |
| `--er-code-string` | `#006600` | Pure green strings |
| `--er-code-keyword` | `#000066` | Deep navy keyword |
| `--er-code-number` | `#660000` | Deep red numbers |
| `--er-focus-ring` | `#0000cc` | Blue focus ring |
| `--er-scrollbar-thumb` | `#888888` | Mid-grey scrollbar |

#### Dark Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#000000` | True black canvas |
| `--er-canvas-raised` | `#111111` | One-step grey raised panel |
| `--er-canvas-sunken` | `#080808` | Code recess — near-void |
| `--er-ink` | `#ffffff` | True white prose |
| `--er-ink-soft` | `#cccccc` | Light grey secondary |
| `--er-ink-faint` | `#555555` | Mid hairlines |
| `--er-accent` | `#ccff00` | Neon chartreuse headings — high-voltage |
| `--er-accent-soft` | `#aadd00` | Dimmer neon hover |
| `--er-link` | `#66ffaa` | Neon mint link |
| `--er-link-visited` | `#44aa77` | Dimmer visited |
| `--er-selection` | `#334400` | Dark neon selection background |
| `--er-math-accent` | `#ccff00` | Chartreuse math variables |
| `--er-code-canvas` | `#0a0a0a` | Near-void code block |
| `--er-code-ink` | `#ffffff` | White code foreground |
| `--er-code-comment` | `#888888` | Grey comments |
| `--er-code-string` | `#88ff44` | Bright neon-green strings |
| `--er-code-keyword` | `#ccff00` | Chartreuse keywords |
| `--er-code-number` | `#ff8844` | Neon amber numbers |
| `--er-focus-ring` | `#ccff00` | Chartreuse focus ring |
| `--er-scrollbar-thumb` | `#333333` | Dark scrollbar |

---

### Theme 4 — Midnight Blue

> Focused, cinematic. Works well under dim ambient light. Light mode has an
> airier feel than parchment — slightly cool and airy like foggy morning.

#### Light Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#edf1f7` | Blue-grey fog — cool light page |
| `--er-canvas-raised` | `#dfe6f0` | Slightly deeper fog for panels |
| `--er-canvas-sunken` | `#d0dcea` | Code block cool recess |
| `--er-ink` | `#0e1a30` | Deep navy ink |
| `--er-ink-soft` | `#2e4060` | Medium slate secondary |
| `--er-ink-faint` | `#8090b0` | Blue-grey hairlines |
| `--er-accent` | `#1a3a8b` | Strong navy headings |
| `--er-accent-soft` | `#2a50b0` | Lighter navy hover |
| `--er-link` | `#1a3a8b` | Navy link |
| `--er-link-visited` | `#6a60a0` | Muted slate visited |
| `--er-selection` | `#b8d0f0` | Glacier blue selection |
| `--er-math-accent` | `#1a3a8b` | Navy math variables |
| `--er-code-canvas` | `#d4deed` | Cool code block |
| `--er-code-ink` | `#0e1a30` | Deep navy code text |
| `--er-code-comment` | `#607090` | Slate comments |
| `--er-code-string` | `#2e7050` | Teal strings |
| `--er-code-keyword` | `#1a3a8b` | Navy keyword |
| `--er-code-number` | `#8b3a1a` | Rust numbers |
| `--er-focus-ring` | `#1a3a8b` | Navy focus ring |
| `--er-scrollbar-thumb` | `#8090b0` | Blue-grey scrollbar |

#### Dark Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#07101e` | Deep navy — near-black with a blue cast |
| `--er-canvas-raised` | `#0f1e30` | Elevated navy panel |
| `--er-canvas-sunken` | `#050c15` | Deepest navy code recess |
| `--er-ink` | `#c8ddf5` | Glacier blue-white text |
| `--er-ink-soft` | `#7a9fc8` | Muted sky secondary |
| `--er-ink-faint` | `#1e3a5a` | Dark navy hairlines |
| `--er-accent` | `#7ab8f5` | Light glacier — headings |
| `--er-accent-soft` | `#5a98d8` | Mid blue hover |
| `--er-link` | `#7ab8f5` | Glacier link |
| `--er-link-visited` | `#5a7aa0` | Dimmer visited |
| `--er-selection` | `#1a3a5a` | Dark navy selection |
| `--er-math-accent` | `#7ab8f5` | Glacier math variables |
| `--er-code-canvas` | `#050c18` | Near-void navy |
| `--er-code-ink` | `#c8ddf5` | Glacier code text |
| `--er-code-comment` | `#4a6a8a` | Muted steel comments |
| `--er-code-string` | `#5ab8a0` | Teal strings |
| `--er-code-keyword` | `#7ab8f5` | Glacier keywords |
| `--er-code-number` | `#f5a87a` | Peach-amber numbers |
| `--er-focus-ring` | `#7ab8f5` | Glacier focus ring |
| `--er-scrollbar-thumb` | `#1e3a5a` | Dark navy scrollbar |

---

### Theme 5 — Rose Dusk

> Warm blush canvas. Low aggression. Often preferred by readers who find
> pure warm-white fatiguing.

#### Light Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#fdf0f0` | Faint blush — barely-pink white |
| `--er-canvas-raised` | `#f5e4e4` | Rose panel |
| `--er-canvas-sunken` | `#ead8d8` | Code block warm recess |
| `--er-ink` | `#2d1515` | Deep plum-black prose |
| `--er-ink-soft` | `#5c2e2e` | Dark rose secondary |
| `--er-ink-faint` | `#c09090` | Rose hairlines |
| `--er-accent` | `#8b2252` | Deep rose headings |
| `--er-accent-soft` | `#aa3066` | Brighter rose hover |
| `--er-link` | `#8b2252` | Rose link |
| `--er-link-visited` | `#7a5060` | Muted mauve visited |
| `--er-selection` | `#f0b8c8` | Pastel pink selection |
| `--er-math-accent` | `#8b2252` | Rose math variables |
| `--er-code-canvas` | `#eadada` | Warm rose code block |
| `--er-code-ink` | `#2d1515` | Plum code text |
| `--er-code-comment` | `#8a6060` | Muted rose comments |
| `--er-code-string` | `#5a7040` | Sage strings |
| `--er-code-keyword` | `#8b2252` | Rose keywords |
| `--er-code-number` | `#5a3a8a` | Muted purple numbers |
| `--er-focus-ring` | `#8b2252` | Rose focus ring |
| `--er-scrollbar-thumb` | `#c09090` | Blush scrollbar |

#### Dark Mode

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#170808` | Deep dark rose-black |
| `--er-canvas-raised` | `#240e0e` | Dark rose panel |
| `--er-canvas-sunken` | `#100404` | Near-black code recess |
| `--er-ink` | `#f5d0d8` | Dusty rose text — warm and soft |
| `--er-ink-soft` | `#c09090` | Muted blush secondary |
| `--er-ink-faint` | `#5c2e2e` | Dark rose hairlines |
| `--er-accent` | `#f07090` | Warm rose heading accent |
| `--er-accent-soft` | `#d05070` | Deeper hover |
| `--er-link` | `#f07090` | Rose link |
| `--er-link-visited` | `#a05068` | Dimmer visited |
| `--er-selection` | `#5c1a2a` | Dark rose selection |
| `--er-math-accent` | `#f07090` | Rose math variables |
| `--er-code-canvas` | `#100606` | Deepest rose-black |
| `--er-code-ink` | `#f5d0d8` | Dusty rose code text |
| `--er-code-comment` | `#7a4a4a` | Muted rose comments |
| `--er-code-string` | `#90d080` | Sage green strings |
| `--er-code-keyword` | `#f07090` | Rose keywords |
| `--er-code-number` | `#d0a870` | Amber numbers |
| `--er-focus-ring` | `#f07090` | Rose focus ring |
| `--er-scrollbar-thumb` | `#5c2e2e` | Dark rose scrollbar |

---

### Theme 6 — Terminal Amber

> Phosphor-screen retro. Night-mode only. Evokes classic CRT displays.
> Light variant uses bone-white with ink-black as a fallback only.

#### Light Mode (fallback only — bone-white variant)

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#f8f4e8` | Warm bone — not cream, not white |
| `--er-canvas-raised` | `#f0e8d8` | Raised bone panel |
| `--er-canvas-sunken` | `#e8dcc8` | Sunken code recess |
| `--er-ink` | `#1a1408` | Near-black warm ink |
| `--er-ink-soft` | `#5a4a2e` | Dark amber secondary |
| `--er-ink-faint` | `#b09050` | Amber hairlines |
| `--er-accent` | `#8a5a00` | Dark amber headings |
| `--er-accent-soft` | `#aa7010` | Lighter amber hover |
| `--er-link` | `#8a5a00` | Amber link |
| `--er-link-visited` | `#7a6040` | Muted brown visited |
| `--er-selection` | `#f0d890` | Gold selection |
| `--er-math-accent` | `#8a5a00` | Amber math variables |
| `--er-code-canvas` | `#ede0c0` | Warm bone code block |
| `--er-code-ink` | `#1a1408` | Black code text |
| `--er-code-comment` | `#7a6040` | Brown comments |
| `--er-code-string` | `#5a7a2a` | Olive strings |
| `--er-code-keyword` | `#8a3a00` | Deep rust keyword |
| `--er-code-number` | `#3a5a8a` | Navy numbers |
| `--er-focus-ring` | `#8a5a00` | Amber focus ring |
| `--er-scrollbar-thumb` | `#b09050` | Gold scrollbar |

#### Dark Mode (primary — phosphor amber)

| Token | Hex | Perceptual note |
|---|---|---|
| `--er-canvas` | `#0a0800` | Near-void warm black — deeper than standard black |
| `--er-canvas-raised` | `#14100a` | One step raised dark panel |
| `--er-canvas-sunken` | `#060400` | Darkest code recess |
| `--er-ink` | `#e8a81a` | Phosphor amber — primary text |
| `--er-ink-soft` | `#b07a0a` | Dimmer amber secondary |
| `--er-ink-faint` | `#503a00` | Very dark amber hairlines |
| `--er-accent` | `#ffcc00` | Bright gold headings — maximum pop |
| `--er-accent-soft` | `#e8aa00` | Warm gold hover |
| `--er-link` | `#ffcc00` | Gold link |
| `--er-link-visited` | `#aa8800` | Dim gold visited |
| `--er-selection` | `#3a2800` | Dark amber selection background |
| `--er-math-accent` | `#ffcc00` | Gold math variables |
| `--er-code-canvas` | `#080600` | Near-void code block |
| `--er-code-ink` | `#e8a81a` | Phosphor amber code text |
| `--er-code-comment` | `#7a5a08` | Muted amber comments |
| `--er-code-string` | `#88cc44` | Phosphor green strings |
| `--er-code-keyword` | `#ffcc00` | Gold keywords |
| `--er-code-number` | `#ff8844` | Phosphor orange numbers |
| `--er-focus-ring` | `#ffcc00` | Gold focus ring |
| `--er-scrollbar-thumb` | `#503a00` | Dark amber scrollbar |

---

## Typography

The ebook typography system has **four roles**, each with its own face and
scale. All body sizes use `clamp()` for fluid scaling — no hard pixel sizes
for reading text.

### Font Families

| Role | Primary | Fallback | Purpose |
|---|---|---|---|
| **Prose** | Literata | Lora, Source Serif 4, Georgia, serif | All body paragraphs, chapter intros |
| **Display** | Literata | Lora, Georgia, serif | Chapter titles, section headings |
| **Math** | STIX Two Math | Latin Modern Math, "Times New Roman", serif | KaTeX inline and display math |
| **Code** | JetBrains Mono | "Fira Code", "Source Code Pro", ui-monospace, monospace | Code blocks and inline code |
| **UI** | Inter | -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif | Navigation, theme picker, footnote labels |

#### Font Loading

```html
<!-- Literata — ebook-optimized variable font (Google Fonts) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?
  family=Literata:ital,opsz,wght@
  0,7..72,300..700;
  1,7..72,300..500&
  display=swap">

<!-- STIX Two Math — open-source math font (CDN or self-host) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/
  stix-two-math-webfont@1.0.0/stix-two-math.min.css">

<!-- KaTeX for math rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/
  katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/
  katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/
  katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body)"></script>
```

### Type Scale (Fluid Clamp Values)

All sizes are `clamp(min, preferred, max)`. The preferred value is a viewport-
width expression so type scales continuously. These tokens map onto CSS custom
properties (`--er-text-*`).

| Token | Clamp value | Approx desktop | Use |
|---|---|---|---|
| `--er-text-display` | `clamp(2rem, 4vw + 1rem, 3.5rem)` | ~56px | Book title, cover page |
| `--er-text-chapter` | `clamp(1.75rem, 3vw + 0.75rem, 2.75rem)` | ~44px | Chapter number + title |
| `--er-text-section` | `clamp(1.375rem, 2vw + 0.5rem, 2rem)` | ~32px | Section (h2) heading |
| `--er-text-subsection` | `clamp(1.125rem, 1.5vw + 0.35rem, 1.5rem)` | ~24px | Subsection (h3) |
| `--er-text-prose` | `clamp(1rem, 0.5vw + 0.875rem, 1.2rem)` | ~19px | Body prose |
| `--er-text-caption` | `clamp(0.8rem, 0.3vw + 0.7rem, 0.95rem)` | ~15px | Figure captions, footnotes |
| `--er-text-code` | `clamp(0.8rem, 0.4vw + 0.7rem, 0.95rem)` | ~15px | Code blocks (mono) |
| `--er-text-ui` | `clamp(0.75rem, 0.3vw + 0.65rem, 0.875rem)` | ~14px | Nav, theme picker, labels |
| `--er-text-math-inline` | inherits `--er-text-prose` | — | KaTeX inline math |
| `--er-text-math-display` | `clamp(1rem, 0.5vw + 0.875rem, 1.2rem)` | ~19px | KaTeX display-mode equations |

### Line Length and Rhythm

Reading research consistently points to 60–75 characters as the optimal prose
line length. The system enforces this via:

```css
.er-prose {
  max-width: 72ch;
  line-height: var(--er-lh-prose);   /* 1.65 */
  letter-spacing: var(--er-ls-prose); /* 0.01em — Literata needs a tiny push */
}
```

| Token | Value | Use |
|---|---|---|
| `--er-lh-display` | `1.1` | Large chapter / display headings |
| `--er-lh-heading` | `1.25` | Section and subsection headings |
| `--er-lh-prose` | `1.65` | Body paragraphs — generous for reading comfort |
| `--er-lh-code` | `1.6` | Code blocks |
| `--er-lh-caption` | `1.5` | Captions and footnotes |
| `--er-ls-display` | `-0.02em` | Negative tracking on large display |
| `--er-ls-heading` | `-0.01em` | Slight tracking pull on section heads |
| `--er-ls-prose` | `0.01em` | Tiny tracking push on Literata body |
| `--er-ls-code` | `0` | Zero tracking on monospace |
| `--er-ls-ui` | `0.02em` | Slight opening on UI labels |
| `--er-ls-caption-uppercase` | `0.08em` | Wide tracking on ALL-CAPS labels |

### Font Weight Mapping

Literata ships as a variable font with optical-size (`opsz`) and `wght` axes.
Use the optical-size axis to improve rendering at small sizes.

| Context | `font-weight` | `font-style` | `font-variation-settings` |
|---|---|---|---|
| Display title | 400 | normal | `"opsz" 60` |
| Chapter title | 400 | normal | `"opsz" 40` |
| Section head (h2) | 500 | normal | `"opsz" 20` |
| Subsection (h3) | 400 | italic | `"opsz" 14` |
| Body prose | 400 | normal | `"opsz" 12` |
| Body emphasis | 600 | normal | `"opsz" 12` |
| Body italic (literary / math prose) | 400 | italic | `"opsz" 12` |
| Caption | 400 | normal | `"opsz" 9` |
| Code (JetBrains Mono) | 400 | normal | — |
| Code keyword | 600 | normal | — |
| UI (Inter) | 400 | normal | — |
| UI label / nav | 500 | normal | — |

---

## Mathematical Typography

Math is a first-class citizen. All inline and display math is rendered by
**KaTeX** (faster than MathJax, offline-capable). The system overrides KaTeX's
default blue-ink variables to match the active theme's `--er-math-accent`.

### KaTeX Integration with Theming

```css
/* Override KaTeX's default color to follow theme */
.katex { color: var(--er-ink); }
.katex .mord { color: var(--er-ink); }
.katex .mbin,
.katex .mrel { color: var(--er-math-accent); }
.katex .mop  { color: var(--er-accent); }

/* Display-mode equation block */
.katex-display {
  background: var(--er-canvas-raised);
  border-left: 3px solid var(--er-accent);
  padding: var(--er-space-md) var(--er-space-lg);
  border-radius: var(--er-radius-sm);
  overflow-x: auto;          /* scroll on narrow viewports */
  margin: var(--er-space-xl) 0;
}
```

### Equation Numbering

Equations in theorem/proof environments get auto-numbered via PreTeXt's
`<mrow xml:id="...">` → `<span class="er-eq-number">(n.m)</span>` system.
The number sits flush right in the same row as the equation, using a soft
muted color so it doesn't compete with the math itself.

```css
.er-eq-number {
  color: var(--er-ink-soft);
  font-family: var(--er-font-ui);
  font-size: var(--er-text-caption);
  float: right;
  margin-left: var(--er-space-lg);
}
```

### Symbol and Special Character Rendering

For non-KaTeX mathematical symbols in prose:

- **Greek letters**: Use KaTeX inline `\(\alpha\)` syntax, never Unicode Greek
  glyphs in source, as Unicode rendering varies across OS/font stacks.
- **Set notation** (`∈`, `⊂`, `∅`): KaTeX inline. Fallback: Unicode in a
  `<span class="er-sym">` wrapper that switches to STIX Two Math.
- **Arrows** (`→`, `⇒`, `↔`): KaTeX inline for math contexts; HTML entities
  (`&rarr;`, `&rArr;`) for prose arrows.
- **Superscript / subscript in prose**: Always `<sup>` / `<sub>` tags. Never
  Unicode superscript digits (`²`, `³`) — they use the wrong font metrics.

```css
/* STIX Two Math for stand-alone symbol spans in prose */
.er-sym {
  font-family: "STIX Two Math", "Latin Modern Math", serif;
  font-size: 1.05em;  /* STIX runs slightly smaller than Literata */
}
```

### Theorem / Definition / Proof Environments

PreTeXt emits semantic blocks for mathematical environments. The design maps
these to visually distinct but non-garish inset boxes.

| Environment | Left border color | Canvas | Label style |
|---|---|---|---|
| `theorem` | `--er-accent` | `--er-canvas-raised` | "Theorem N.M" in `--er-accent`, small caps |
| `definition` | `--er-ink-faint` | `--er-canvas-raised` | "Definition N.M" in `--er-ink-soft` |
| `proof` | `--er-ink-faint` | transparent | "Proof." in italic prose; QED glyph right-aligned |
| `example` | `--er-accent-soft` | `--er-canvas-raised` | "Example N.M" in `--er-accent-soft` |
| `remark` | `--er-ink-faint` | `--er-canvas-sunken` | "Remark." in italic |
| `corollary` | `--er-accent` | `--er-canvas-raised` | "Corollary N.M" in `--er-accent` |
| `algorithm` | `--er-accent` | `--er-canvas-sunken` | Monospace header in `--er-code-keyword` |

```css
.er-env {
  border-left: 3px solid var(--er-accent);
  background: var(--er-canvas-raised);
  padding: var(--er-space-md) var(--er-space-lg);
  border-radius: 0 var(--er-radius-sm) var(--er-radius-sm) 0;
  margin: var(--er-space-xl) 0;
}

.er-env-label {
  font-family: var(--er-font-ui);
  font-size: var(--er-text-caption);
  font-variant: small-caps;
  letter-spacing: var(--er-ls-caption-uppercase);
  color: var(--er-accent);
  display: block;
  margin-bottom: var(--er-space-sm);
}

.er-proof-qed::after {
  content: "□";
  display: block;
  text-align: right;
  color: var(--er-ink-soft);
  font-size: var(--er-text-prose);
}
```

---

## Layout — PreTeXt Fluid Model

PreTeXt's layout philosophy: **no fixed breakpoints**. Instead, every structural
element uses intrinsic sizing and `clamp()` values so the reading column finds
its optimal width at any viewport.

### Column Structure

```css
/* Root reading column — self-constrains at 72ch, re-centres everywhere else */
.er-content {
  width: min(72ch, 100% - 2 * var(--er-margin-inline));
  margin-inline: auto;
}

/* Wide figures, equations, tables that may need more space */
.er-wide {
  width: min(90ch, 100% - 2 * var(--er-margin-inline));
  margin-inline: auto;
}

/* Full-bleed elements (hero banner, chapter dividers) */
.er-full-bleed {
  width: 100%;
  margin-inline: 0;
}
```

### Spacing Tokens

| Token | Value | Use |
|---|---|---|
| `--er-space-xxs` | `clamp(0.25rem, 0.5vw, 0.375rem)` | Tight glyph gaps |
| `--er-space-xs` | `clamp(0.375rem, 0.75vw, 0.5rem)` | Inline padding |
| `--er-space-sm` | `clamp(0.5rem, 1vw, 0.75rem)` | Caption-to-figure gap |
| `--er-space-md` | `clamp(0.75rem, 1.5vw, 1rem)` | Standard paragraph spacing |
| `--er-space-lg` | `clamp(1rem, 2vw, 1.5rem)` | Between prose blocks |
| `--er-space-xl` | `clamp(1.5rem, 3vw, 2.5rem)` | Before/after headings |
| `--er-space-xxl` | `clamp(2.5rem, 5vw, 4rem)` | Chapter section breaks |
| `--er-space-chapter` | `clamp(4rem, 8vw, 7rem)` | Between chapters |
| `--er-margin-inline` | `clamp(1rem, 5vw, 3rem)` | Side breathing room |

### Sidebar Navigation

PreTeXt renders a collapsible `<nav>` TOC sidebar. It overlays on narrow
viewports (< ~600px) and pins beside the content column on wider viewports.
The sidebar uses the same `--er-canvas-raised` background and `--er-font-ui`
typeface.

```css
.er-sidebar {
  width: clamp(200px, 22vw, 280px);
  background: var(--er-canvas-raised);
  border-right: 1px solid var(--er-ink-faint);
  position: sticky;
  top: 0;
  height: 100dvh;
  overflow-y: auto;
  font-family: var(--er-font-ui);
  font-size: var(--er-text-ui);
}

/* On narrow viewports: off-canvas */
@media (max-width: 640px) {
  .er-sidebar {
    position: fixed;
    transform: translateX(-100%);
    transition: transform 0.2s ease;
    z-index: 100;
  }
  .er-sidebar[data-open="true"] {
    transform: translateX(0);
  }
}
```

---

## Components

### Theme Picker

A compact control exposed to readers. Typically lives in the top-right corner
of the reading UI or in a settings panel. Allows switching theme and mode
independently.

**Behavior:** Writes `data-theme` and `data-mode` to `<html>`. Persists
selection to `localStorage`. Does not require a page reload.

```html
<!-- Minimal markup -->
<div class="er-theme-picker" role="group" aria-label="Reading theme">
  <label class="er-theme-picker-label">Theme</label>
  <div class="er-theme-swatches">
    <button data-pick-theme="parchment"    title="Warm Parchment"   />
    <button data-pick-theme="coffee-green" title="Coffee Green"     />
    <button data-pick-theme="obsidian"     title="Obsidian Contrast"/>
    <button data-pick-theme="midnight"     title="Midnight Blue"    />
    <button data-pick-theme="rose-dusk"    title="Rose Dusk"        />
    <button data-pick-theme="terminal-amber" title="Terminal Amber" />
  </div>
  <div class="er-mode-toggle">
    <button data-pick-mode="light">☀ Light</button>
    <button data-pick-mode="dark"> ◑ Dark</button>
    <button data-pick-mode="auto"> ⊙ Auto</button>  <!-- follows prefers-color-scheme -->
  </div>
</div>
```

Theme swatch buttons use a 24×24px circle, colored with each theme's `canvas`
(outer ring) and `accent` (inner fill), so readers can preview before
selecting.

### Font Size Control

Three-step font scale (S / M / L) that adjusts the root `font-size` by ±10%.

```css
:root { --er-scale: 1; }
html[data-font-size="s"] { --er-scale: 0.9; }
html[data-font-size="l"] { --er-scale: 1.1; }

/* All clamp() values multiply by --er-scale */
:root {
  --er-text-prose: calc(clamp(1rem, 0.5vw + 0.875rem, 1.2rem) * var(--er-scale));
}
```

### Chapter Header

Full-width chapter opener. Uses a large chapter number in display serif
(`--er-text-display`), a decorative rule using `--er-accent`, and the chapter
title in `--er-text-chapter`.

```css
.er-chapter-header {
  padding-block: var(--er-space-chapter);
  border-bottom: 1px solid var(--er-ink-faint);
}

.er-chapter-number {
  font-family: var(--er-font-display);
  font-size: var(--er-text-display);
  font-weight: 400;
  font-variation-settings: "opsz" 60;
  color: var(--er-accent);
  letter-spacing: var(--er-ls-display);
  line-height: var(--er-lh-display);
}

.er-chapter-title {
  font-family: var(--er-font-display);
  font-size: var(--er-text-chapter);
  font-weight: 400;
  font-variation-settings: "opsz" 40;
  color: var(--er-ink);
  letter-spacing: var(--er-ls-display);
  line-height: var(--er-lh-display);
}
```

### Figure and Caption

Figures (images, diagrams, tables) sit in `.er-wide` when possible and include
a caption below in `--er-text-caption` with a left-aligned label in
`--er-accent`.

```css
.er-figure {
  margin: var(--er-space-xxl) 0;
}

.er-figure img,
.er-figure svg {
  width: 100%;
  height: auto;
  border-radius: var(--er-radius-sm);
}

.er-figure-caption {
  font-family: var(--er-font-ui);
  font-size: var(--er-text-caption);
  line-height: var(--er-lh-caption);
  color: var(--er-ink-soft);
  margin-top: var(--er-space-sm);
}

.er-figure-label {
  font-weight: 600;
  color: var(--er-accent);
}
```

### Footnote / Marginal Note

Footnotes render in a small column in the margin (when viewport ≥ 900px),
pinned beside the originating paragraph. On narrow viewports they collapse
to numbered inline endnotes.

```css
/* Margin note (wide viewport only) */
@media (min-width: 900px) {
  .er-marginnote {
    position: absolute;
    right: calc(-1 * (100vw - 72ch) / 2 + var(--er-margin-inline));
    width: clamp(160px, 18vw, 220px);
    font-family: var(--er-font-ui);
    font-size: var(--er-text-caption);
    color: var(--er-ink-soft);
    line-height: var(--er-lh-caption);
  }
}
```

### Blockquote / Epigraph

```css
.er-blockquote {
  border-left: 3px solid var(--er-accent-soft);
  padding-left: var(--er-space-lg);
  margin-left: 0;
  color: var(--er-ink-soft);
  font-style: italic;
  font-variation-settings: "opsz" 12;
}

.er-epigraph {
  font-style: italic;
  font-size: var(--er-text-caption);
  color: var(--er-ink-soft);
  text-align: right;
  margin-top: var(--er-space-xl);
  padding-right: var(--er-space-lg);
}
```

### Code Block

```css
.er-code-block {
  font-family: var(--er-font-code);
  font-size: var(--er-text-code);
  line-height: var(--er-lh-code);
  background: var(--er-code-canvas);
  color: var(--er-code-ink);
  border-radius: var(--er-radius-md);
  padding: var(--er-space-lg);
  overflow-x: auto;
  tab-size: 4;
  /* Label for language tag */
  position: relative;
}

.er-code-block::before {
  content: attr(data-language);
  position: absolute;
  top: var(--er-space-sm);
  right: var(--er-space-sm);
  font-family: var(--er-font-ui);
  font-size: var(--er-text-ui);
  color: var(--er-ink-faint);
  text-transform: uppercase;
  letter-spacing: var(--er-ls-caption-uppercase);
}

.er-code-block .comment { color: var(--er-code-comment); }
.er-code-block .string  { color: var(--er-code-string);  }
.er-code-block .keyword { color: var(--er-code-keyword); font-weight: 600; }
.er-code-block .number  { color: var(--er-code-number);  }
```

### Inline Code

```css
code:not([class]) {
  font-family: var(--er-font-code);
  font-size: 0.9em;
  background: var(--er-canvas-sunken);
  color: var(--er-accent);
  border-radius: var(--er-radius-xs);
  padding: 0.1em 0.35em;
}
```

### Reading Progress Bar

A thin 2px bar at the very top of the viewport, colored `--er-accent`, that
fills left-to-right as the reader scrolls. Driven by a tiny script that
computes `scrollY / (scrollHeight - innerHeight)`.

```css
.er-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 2px;
  background: var(--er-accent);
  transition: width 0.1s linear;
  z-index: 200;
}
```

---

## Border Radius Tokens

| Token | Value | Use |
|---|---|---|
| `--er-radius-xs` | `3px` | Inline code pills |
| `--er-radius-sm` | `6px` | Theorem/definition boxes, figures |
| `--er-radius-md` | `10px` | Code blocks, callout cards |
| `--er-radius-lg` | `16px` | Theme picker panel |
| `--er-radius-full` | `9999px` | Theme swatch circles, footnote numbers |

---

## Accessibility & Motion

```css
/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  .er-progress     { transition: none; }
  .er-sidebar      { transition: none; }
}

/* Keyboard focus */
:focus-visible {
  outline: 2px solid var(--er-focus-ring);
  outline-offset: 3px;
  border-radius: var(--er-radius-xs);
}

/* Forced colors (Windows High Contrast) */
@media (forced-colors: active) {
  .er-env          { border-left-color: Highlight; }
  .er-blockquote   { border-left-color: GrayText; }
  .er-progress     { background: Highlight; }
}
```

---

## CSS Custom Property Implementation

Paste this block in your PreTeXt HTML output's `<head>` (after the
PreTeXt base stylesheet) to wire up the full token system.

```css
/* ============================================
   EBOOK DESIGN SYSTEM — CUSTOM PROPERTIES
   Paste after pretext-default.css
   ============================================ */

/* --- Font stacks --- */
:root {
  --er-font-display: "Literata", "Lora", "Source Serif 4", Georgia, serif;
  --er-font-prose:   "Literata", "Lora", "Source Serif 4", Georgia, serif;
  --er-font-math:    "STIX Two Math", "Latin Modern Math", "Times New Roman", serif;
  --er-font-code:    "JetBrains Mono", "Fira Code", "Source Code Pro",
                      ui-monospace, monospace;
  --er-font-ui:      Inter, -apple-system, BlinkMacSystemFont,
                      "Segoe UI", Roboto, sans-serif;
  --er-scale: 1;
}

/* --- Parchment Light (default) --- */
[data-theme="parchment"][data-mode="light"], :root {
  --er-canvas:          #f5edd8;
  --er-canvas-raised:   #ede4cc;
  --er-canvas-sunken:   #e4d9bc;
  --er-ink:             #2c1a0e;
  --er-ink-soft:        #5c3c22;
  --er-ink-faint:       #b09070;
  --er-accent:          #8b4513;
  --er-accent-soft:     #a0522d;
  --er-link:            #8b4513;
  --er-link-visited:    #a07050;
  --er-selection:       #e8c88a;
  --er-math-accent:     #8b4513;
  --er-code-canvas:     #dfd3b5;
  --er-code-ink:        #2c1a0e;
  --er-code-comment:    #7a5c3a;
  --er-code-string:     #5a7a2a;
  --er-code-keyword:    #7a2a0a;
  --er-code-number:     #3a5a8a;
  --er-focus-ring:      #8b4513;
  --er-scrollbar-thumb: #b09070;
}

/* --- Parchment Dark --- */
[data-theme="parchment"][data-mode="dark"] {
  --er-canvas:          #18100a;
  --er-canvas-raised:   #241808;
  --er-canvas-sunken:   #100a04;
  --er-ink:             #e8d5b0;
  --er-ink-soft:        #b09070;
  --er-ink-faint:       #5c3c22;
  --er-accent:          #d4843a;
  --er-accent-soft:     #c46a1a;
  --er-link:            #d4843a;
  --er-link-visited:    #a0622a;
  --er-selection:       #5c3c10;
  --er-math-accent:     #d4843a;
  --er-code-canvas:     #100c06;
  --er-code-ink:        #e8d5b0;
  --er-code-comment:    #7a6040;
  --er-code-string:     #7ab04a;
  --er-code-keyword:    #d48050;
  --er-code-number:     #6a9ad4;
  --er-focus-ring:      #d4843a;
  --er-scrollbar-thumb: #5c3c22;
}

/* --- Coffee Green Light --- */
[data-theme="coffee-green"][data-mode="light"] {
  --er-canvas:          #eef4ec;
  --er-canvas-raised:   #e2ede0;
  --er-canvas-sunken:   #d5e6d2;
  --er-ink:             #1a2e1a;
  --er-ink-soft:        #3d5c3a;
  --er-ink-faint:       #8ab08a;
  --er-accent:          #2e6b2e;
  --er-accent-soft:     #4a8c4a;
  --er-link:            #2e6b2e;
  --er-link-visited:    #6b8c5c;
  --er-selection:       #b4d9b4;
  --er-math-accent:     #2e6b2e;
  --er-code-canvas:     #ddecd9;
  --er-code-ink:        #1a2e1a;
  --er-code-comment:    #6b8c5c;
  --er-code-string:     #5a8a3a;
  --er-code-keyword:    #2e5c1a;
  --er-code-number:     #8a5c2e;
  --er-focus-ring:      #2e6b2e;
  --er-scrollbar-thumb: #8ab08a;
}

/* --- Coffee Green Dark --- */
[data-theme="coffee-green"][data-mode="dark"] {
  --er-canvas:          #0d1a0d;
  --er-canvas-raised:   #162616;
  --er-canvas-sunken:   #0a130a;
  --er-ink:             #c8e6c0;
  --er-ink-soft:        #8ab08a;
  --er-ink-faint:       #3d5c3a;
  --er-accent:          #7dc87d;
  --er-accent-soft:     #5aaa5a;
  --er-link:            #7dc87d;
  --er-link-visited:    #5c8a5c;
  --er-selection:       #2e5c2e;
  --er-math-accent:     #7dc87d;
  --er-code-canvas:     #0a1a0a;
  --er-code-ink:        #c8e6c0;
  --er-code-comment:    #5c7d5c;
  --er-code-string:     #8aba6a;
  --er-code-keyword:    #aad47a;
  --er-code-number:     #d4a85a;
  --er-focus-ring:      #7dc87d;
  --er-scrollbar-thumb: #3d5c3a;
}

/* --- Obsidian Light --- */
[data-theme="obsidian"][data-mode="light"] {
  --er-canvas:          #ffffff;
  --er-canvas-raised:   #f0f0f0;
  --er-canvas-sunken:   #e0e0e0;
  --er-ink:             #000000;
  --er-ink-soft:        #333333;
  --er-ink-faint:       #888888;
  --er-accent:          #000000;
  --er-accent-soft:     #222222;
  --er-link:            #0000cc;
  --er-link-visited:    #551a8b;
  --er-selection:       #aad4ff;
  --er-math-accent:     #0000cc;
  --er-code-canvas:     #f4f4f4;
  --er-code-ink:        #000000;
  --er-code-comment:    #555555;
  --er-code-string:     #006600;
  --er-code-keyword:    #000066;
  --er-code-number:     #660000;
  --er-focus-ring:      #0000cc;
  --er-scrollbar-thumb: #888888;
}

/* --- Obsidian Dark --- */
[data-theme="obsidian"][data-mode="dark"] {
  --er-canvas:          #000000;
  --er-canvas-raised:   #111111;
  --er-canvas-sunken:   #080808;
  --er-ink:             #ffffff;
  --er-ink-soft:        #cccccc;
  --er-ink-faint:       #555555;
  --er-accent:          #ccff00;
  --er-accent-soft:     #aadd00;
  --er-link:            #66ffaa;
  --er-link-visited:    #44aa77;
  --er-selection:       #334400;
  --er-math-accent:     #ccff00;
  --er-code-canvas:     #0a0a0a;
  --er-code-ink:        #ffffff;
  --er-code-comment:    #888888;
  --er-code-string:     #88ff44;
  --er-code-keyword:    #ccff00;
  --er-code-number:     #ff8844;
  --er-focus-ring:      #ccff00;
  --er-scrollbar-thumb: #333333;
}

/* --- Midnight Light --- */
[data-theme="midnight"][data-mode="light"] {
  --er-canvas:          #edf1f7;
  --er-canvas-raised:   #dfe6f0;
  --er-canvas-sunken:   #d0dcea;
  --er-ink:             #0e1a30;
  --er-ink-soft:        #2e4060;
  --er-ink-faint:       #8090b0;
  --er-accent:          #1a3a8b;
  --er-accent-soft:     #2a50b0;
  --er-link:            #1a3a8b;
  --er-link-visited:    #6a60a0;
  --er-selection:       #b8d0f0;
  --er-math-accent:     #1a3a8b;
  --er-code-canvas:     #d4deed;
  --er-code-ink:        #0e1a30;
  --er-code-comment:    #607090;
  --er-code-string:     #2e7050;
  --er-code-keyword:    #1a3a8b;
  --er-code-number:     #8b3a1a;
  --er-focus-ring:      #1a3a8b;
  --er-scrollbar-thumb: #8090b0;
}

/* --- Midnight Dark --- */
[data-theme="midnight"][data-mode="dark"] {
  --er-canvas:          #07101e;
  --er-canvas-raised:   #0f1e30;
  --er-canvas-sunken:   #050c15;
  --er-ink:             #c8ddf5;
  --er-ink-soft:        #7a9fc8;
  --er-ink-faint:       #1e3a5a;
  --er-accent:          #7ab8f5;
  --er-accent-soft:     #5a98d8;
  --er-link:            #7ab8f5;
  --er-link-visited:    #5a7aa0;
  --er-selection:       #1a3a5a;
  --er-math-accent:     #7ab8f5;
  --er-code-canvas:     #050c18;
  --er-code-ink:        #c8ddf5;
  --er-code-comment:    #4a6a8a;
  --er-code-string:     #5ab8a0;
  --er-code-keyword:    #7ab8f5;
  --er-code-number:     #f5a87a;
  --er-focus-ring:      #7ab8f5;
  --er-scrollbar-thumb: #1e3a5a;
}

/* --- Rose Dusk Light --- */
[data-theme="rose-dusk"][data-mode="light"] {
  --er-canvas:          #fdf0f0;
  --er-canvas-raised:   #f5e4e4;
  --er-canvas-sunken:   #ead8d8;
  --er-ink:             #2d1515;
  --er-ink-soft:        #5c2e2e;
  --er-ink-faint:       #c09090;
  --er-accent:          #8b2252;
  --er-accent-soft:     #aa3066;
  --er-link:            #8b2252;
  --er-link-visited:    #7a5060;
  --er-selection:       #f0b8c8;
  --er-math-accent:     #8b2252;
  --er-code-canvas:     #eadada;
  --er-code-ink:        #2d1515;
  --er-code-comment:    #8a6060;
  --er-code-string:     #5a7040;
  --er-code-keyword:    #8b2252;
  --er-code-number:     #5a3a8a;
  --er-focus-ring:      #8b2252;
  --er-scrollbar-thumb: #c09090;
}

/* --- Rose Dusk Dark --- */
[data-theme="rose-dusk"][data-mode="dark"] {
  --er-canvas:          #170808;
  --er-canvas-raised:   #240e0e;
  --er-canvas-sunken:   #100404;
  --er-ink:             #f5d0d8;
  --er-ink-soft:        #c09090;
  --er-ink-faint:       #5c2e2e;
  --er-accent:          #f07090;
  --er-accent-soft:     #d05070;
  --er-link:            #f07090;
  --er-link-visited:    #a05068;
  --er-selection:       #5c1a2a;
  --er-math-accent:     #f07090;
  --er-code-canvas:     #100606;
  --er-code-ink:        #f5d0d8;
  --er-code-comment:    #7a4a4a;
  --er-code-string:     #90d080;
  --er-code-keyword:    #f07090;
  --er-code-number:     #d0a870;
  --er-focus-ring:      #f07090;
  --er-scrollbar-thumb: #5c2e2e;
}

/* --- Terminal Amber Light (bone fallback) --- */
[data-theme="terminal-amber"][data-mode="light"] {
  --er-canvas:          #f8f4e8;
  --er-canvas-raised:   #f0e8d8;
  --er-canvas-sunken:   #e8dcc8;
  --er-ink:             #1a1408;
  --er-ink-soft:        #5a4a2e;
  --er-ink-faint:       #b09050;
  --er-accent:          #8a5a00;
  --er-accent-soft:     #aa7010;
  --er-link:            #8a5a00;
  --er-link-visited:    #7a6040;
  --er-selection:       #f0d890;
  --er-math-accent:     #8a5a00;
  --er-code-canvas:     #ede0c0;
  --er-code-ink:        #1a1408;
  --er-code-comment:    #7a6040;
  --er-code-string:     #5a7a2a;
  --er-code-keyword:    #8a3a00;
  --er-code-number:     #3a5a8a;
  --er-focus-ring:      #8a5a00;
  --er-scrollbar-thumb: #b09050;
}

/* --- Terminal Amber Dark (primary phosphor) --- */
[data-theme="terminal-amber"][data-mode="dark"] {
  --er-canvas:          #0a0800;
  --er-canvas-raised:   #14100a;
  --er-canvas-sunken:   #060400;
  --er-ink:             #e8a81a;
  --er-ink-soft:        #b07a0a;
  --er-ink-faint:       #503a00;
  --er-accent:          #ffcc00;
  --er-accent-soft:     #e8aa00;
  --er-link:            #ffcc00;
  --er-link-visited:    #aa8800;
  --er-selection:       #3a2800;
  --er-math-accent:     #ffcc00;
  --er-code-canvas:     #080600;
  --er-code-ink:        #e8a81a;
  --er-code-comment:    #7a5a08;
  --er-code-string:     #88cc44;
  --er-code-keyword:    #ffcc00;
  --er-code-number:     #ff8844;
  --er-focus-ring:      #ffcc00;
  --er-scrollbar-thumb: #503a00;
}

/* --- Auto mode: follow OS preference --- */
@media (prefers-color-scheme: dark) {
  [data-mode="auto"] {
    /* Inherit the dark variant of the current theme automatically.
       The JavaScript theme-switcher sets data-mode="light" or "dark"
       based on this media query when data-mode="auto" is set. */
  }
}
```

---

## JavaScript — Theme Persistence

```javascript
// ebook-theme.js — ~40 lines, no dependencies
(function () {
  const ROOT    = document.documentElement;
  const STORAGE = localStorage;
  const KEY_T   = "er-theme";
  const KEY_M   = "er-mode";
  const THEMES  = ["parchment","coffee-green","obsidian",
                   "midnight","rose-dusk","terminal-amber"];
  const MODES   = ["light","dark","auto"];

  function applyTheme(theme, mode) {
    ROOT.setAttribute("data-theme", THEMES.includes(theme) ? theme : "parchment");
    const resolved = mode === "auto"
      ? (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
      : mode;
    ROOT.setAttribute("data-mode", MODES.includes(resolved) ? resolved : "light");
  }

  // Boot: restore from localStorage or apply defaults
  applyTheme(
    STORAGE.getItem(KEY_T) ?? "parchment",
    STORAGE.getItem(KEY_M) ?? "auto"
  );

  // Theme picker buttons
  document.addEventListener("click", function (e) {
    const t = e.target.closest("[data-pick-theme]");
    const m = e.target.closest("[data-pick-mode]");
    if (t) {
      const theme = t.dataset.pickTheme;
      STORAGE.setItem(KEY_T, theme);
      applyTheme(theme, ROOT.getAttribute("data-mode"));
    }
    if (m) {
      const mode = m.dataset.pickMode;
      STORAGE.setItem(KEY_M, mode);
      applyTheme(ROOT.getAttribute("data-theme"), mode);
    }
  });

  // React to OS preference changes when in auto mode
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if ((STORAGE.getItem(KEY_M) ?? "auto") === "auto") {
      applyTheme(STORAGE.getItem(KEY_T) ?? "parchment", "auto");
    }
  });
})();
```

---

## Do's and Don'ts

### Do
- Use `clamp()` for every sizing value. Fixed `px` values are only permitted
  for `--er-radius-*` tokens and thin lines (1–2px).
- Let the content column self-constrain at 72ch. Do not override `max-width`
  for body prose.
- Use STIX Two Math / KaTeX for all math notation. Never rely on Unicode
  mathematical characters in plain prose.
- Use Literata's variable axes: set `font-variation-settings: "opsz" N` at each
  size breakpoint. Optical sizing substantially improves legibility.
- Offer all six themes via the theme picker. Do not hide themes because they
  seem niche — readers with print disabilities or strong preferences are
  disproportionate beneficiaries.
- Test every theme combination for WCAG AA contrast on prose text
  (≥ 4.5:1) and for AA on large headings (≥ 3:1).

### Don't
- Don't animate the canvas background on theme switch — a hard cut is
  less jarring than a 300ms color transition when the entire page flips.
- Don't set `font-weight: 700` on Literata display text. Weight 400 with
  optical sizing is the designed reading weight; bold display text reads
  as typographic pressure, not authority.
- Don't wrap math in `<i>` or `<em>` — always use KaTeX `\textit{}` or
  the standard italic math convention.
- Don't use the Terminal Amber light variant as a design showcase — it is a
  fallback for operating-system incompatibility only. The primary Terminal
  Amber experience is the dark phosphor variant.
- Don't add a fourth font family. The four-family stack (Literata / STIX Two /
  JetBrains Mono / Inter) is the ceiling. Adding more creates loading overhead
  and typographic inconsistency.
- Don't apply `--er-accent` to prose body text — it's for headings, active
  navigation links, and environment labels only. Body links use `--er-link`.
- Don't use border-box shadows for elevation on dark themes — use
  `--er-canvas-raised` background shifts instead. Shadows read as light-mode
  artifacts on very dark surfaces.

---

## Known Gaps & Extension Points

- **Lean 4 / proof assistant syntax highlighting**: The default code-token
  set (keyword / string / number / comment) does not include Lean 4's tactic
  tokens (`rw`, `simp`, `exact`, `apply`, `linarith`). A Lean-specific token
  extension should add `--er-code-tactic` and `--er-code-type` variables.
- **Chemistry / structural formulae**: KaTeX does not render structural
  chemistry (mhchem is a KaTeX extension — add via
  `katex.renderMathInElement(el, { macros: {...}, ...mhchem })`).
- **Right-to-left support**: The `rtl-ready: true` flag notes intent;
  actual RTL mirroring (sidebar direction, text-align, margin/padding flips)
  requires a `[dir="rtl"]` override block not included here.
- **Annotation / highlighting**: Reader annotations (highlights, sticky notes)
  are not in scope — they require a back-end persistence layer outside this
  CSS system.
- **Print stylesheet**: PreTeXt's LaTeX path handles print output; the
  CSS tokens here are screen-only. A `@media print` block should reference
  Parchment Light values unconditionally for consistent print output.
- **E-ink display mode**: High-contrast black-on-white with zero colour for
  e-ink (Kindle, Kobo) screens. A `data-theme="e-ink"` stub can be added
  using Obsidian Light values with all colour tokens clamped to greyscale.
