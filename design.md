---
layout: default
title: "Design Specification — DFT Notes"
permalink: /dft-notes/design/
description: >-
  The complete design specification for the DFT Notes site:
  typography, layout, colour palette, Mermaid, MathJax,
  Jekyll configuration, and the implementation status of every
  component.
keywords: "design, typography, layout, color palette, mermaid, mathjax, jekyll, implementation"
---

# Design Specification

> **Stack:** Jekyll + MathJax 3 · Mermaid diagrams · Theme switcher
> (light + dark) · Pastel poppy-green / warm dark · Mobile-first ·
> EB Garamond + Inter + JetBrains Mono

---

> **Iteration history** — this document is the single source of
> truth and is updated as the site evolves.  Older iterations
> stay below for reference.
>
> - **v1 (2026-06-14)** — Claude/Anthropic design (cream + coral +
>   dark navy, slab-serif display, humanist sans body).  Single
>   light theme, minima theme overridden.  See git history.
> - **v2 (this version)** — reading-friendly rebuild:
>   - Palette shifted to **pastel poppy green** (light) and
>     **warm dark** (dark) for long-session comfort.  Coral
>     retained as the brand accent.
>   - **Theme switcher** with persistent preference
>     (localStorage), no flash of wrong theme.
>   - **Wider reading column** on large screens (max-width
>     grows from 760px on mobile to 1100px on wide screens).
>   - **Marginalia rail** for figure captions, side notes,
>     and figure-with-caption blocks.
>   - **Mermaid diagrams** supported via ```` ```mermaid ````
>     code fences, theme-aware.
>   - **Chapters map** (`dft_notes/chapters-map.md`) — a live
>     Mermaid graph of the whole knowledge base with hover
>     details.
>   - **Python codes folder** (`dft_notes/python_codes/`) —
>     per-chapter subfolders with the same code that runs
>     inside the chapters, plus generated plots.
>   - **Hidden answers** via `<details><summary>` for
>     thought-provoking problems.
>   - **agents.md** — the agent handbook documenting how
>     everything is built and the parallel-research pattern.
>   - **Footer** shrunk to four short link columns
>     (Project / Built with / Legal / Contribute) — the
>     chapter list lives in the **chapters map** and the
>     nav, not the footer.

---

```yaml
version: alpha
name: Claude-design-analysis
description: A warm-canvas editorial interface for Anthropic's Claude product. The system anchors on a tinted cream canvas with serif display headlines, warm coral CTAs, and dark navy product surfaces (code editor mockups, model showcase cards). Brand voltage comes from the cream/coral pairing — deliberately warm and humanist where most AI brands use cool blue + slate. Type voice runs a slab-serif display ("Copernicus" / Tiempos Headline) for h1/h2 and a humanist sans for body. The signature Anthropic black-radial-spike mark anchors the wordmark.

colors:
  primary: "#cc785c"
  primary-active: "#a9583e"
  primary-disabled: "#e6dfd8"
  ink: "#141413"
  body: "#3d3d3a"
  body-strong: "#252523"
  muted: "#6c6a64"
  muted-soft: "#8e8b82"
  hairline: "#e6dfd8"
  hairline-soft: "#ebe6df"
  canvas: "#faf9f5"
  surface-soft: "#f5f0e8"
  surface-card: "#efe9de"
  surface-cream-strong: "#e8e0d2"
  surface-dark: "#181715"
  surface-dark-elevated: "#252320"
  surface-dark-soft: "#1f1e1b"
  on-primary: "#ffffff"
  on-dark: "#faf9f5"
  on-dark-soft: "#a09d96"
  accent-teal: "#5db8a6"
  accent-amber: "#e8a55a"
  success: "#5db872"
  warning: "#d4a017"
  error: "#c64545"

typography:
  display-xl:
    fontFamily: "Copernicus, Tiempos Headline, serif"
    fontSize: 64px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: -1.5px
  display-lg:
    fontFamily: "Copernicus, Tiempos Headline, serif"
    fontSize: 48px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: -1px
  display-md:
    fontFamily: "Copernicus, Tiempos Headline, serif"
    fontSize: 36px
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: -0.5px
  display-sm:
    fontFamily: "Copernicus, Tiempos Headline, serif"
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: -0.3px
  title-lg:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 22px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: 0
  title-md:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 18px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  title-sm:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  body-md:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0
  body-sm:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0
  caption:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0
  caption-uppercase:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 1.5px
  code:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  button:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0
  nav-link:
    fontFamily: "StyreneB, Inter, sans-serif"
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0

rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  xl: 16px
  pill: 9999px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 96px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 20px
    height: 40px
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
  button-primary-disabled:
    backgroundColor: "{colors.primary-disabled}"
    textColor: "{colors.muted}"
    rounded: "{rounded.md}"
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 20px
    height: 40px
  button-secondary-on-dark:
    backgroundColor: "{colors.surface-dark-elevated}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  button-text-link:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.button}"
  button-icon-circular:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.full}"
    size: 36px
  text-link:
    backgroundColor: transparent
    textColor: "{colors.primary}"
    typography: "{typography.body-md}"
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.nav-link}"
    height: 64px
  hero-band:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-xl}"
    padding: 96px
  hero-illustration-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
  feature-card:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  product-mockup-card-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.title-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  code-window-card:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.code}"
    rounded: "{rounded.lg}"
    padding: 24px
  model-comparison-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.title-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  pricing-tier-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.title-lg}"
    rounded: "{rounded.lg}"
    padding: 32px
  pricing-tier-card-featured:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.title-lg}"
    rounded: "{rounded.lg}"
    padding: 32px
  callout-card-coral:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.title-md}"
    rounded: "{rounded.lg}"
    padding: 32px
  connector-tile:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.title-sm}"
    rounded: "{rounded.lg}"
    padding: 20px
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 10px 14px
    height: 40px
  text-input-focused:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
  cookie-consent-card:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.lg}"
    padding: 24px
  category-tab:
    backgroundColor: transparent
    textColor: "{colors.muted}"
    typography: "{typography.nav-link}"
    padding: 8px 14px
    rounded: "{rounded.md}"
  category-tab-active:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.nav-link}"
    rounded: "{rounded.md}"
  badge-pill:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.pill}"
    padding: 4px 12px
  badge-coral:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.caption-uppercase}"
    rounded: "{rounded.pill}"
    padding: 4px 12px
  cta-band-coral:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.display-sm}"
    rounded: "{rounded.lg}"
    padding: 64px
  cta-band-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark}"
    typography: "{typography.display-sm}"
    rounded: "{rounded.lg}"
    padding: 64px
  footer:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-dark-soft}"
    typography: "{typography.body-sm}"
    padding: 64px
```

---

## Overview

Claude.com is the warmest, most editorial interface in the AI-product
category. The base atmosphere is a **tinted cream canvas**
(`{colors.canvas}` — #faf9f5) — distinctly warm, deliberately not the
cool gray-white that every other AI brand uses. Headlines run a
**slab-serif display** ("Copernicus" / Tiempos Headline) at weight 400
with negative letter-spacing, paired with **StyreneB / Inter** body
sans. The combination feels like a literary publication, not a SaaS
marketing page.

Brand voltage comes from the **cream + coral pairing** — coral
(`{colors.primary}` — #cc785c) is the signature Anthropic accent,
used on every primary CTA, on the brand wordmark, and on full-bleed
callout cards. The coral is warm, slightly muted, never cyan/blue —
a deliberate counter-positioning against OpenAI's cool slate,
Google's saturated blue, and Microsoft's corporate cyan.

The system has three surface modes that alternate page-by-page:

1. **Cream canvas** (`{colors.canvas}`) — default body floor
2. **Light cream cards** (`{colors.surface-card}`) — feature card
   backgrounds
3. **Dark navy product surfaces** (`{colors.surface-dark}`) — code
   editor mockups, model showcase cards, pre-footer CTAs, footer
   itself

The dark surfaces are where Claude shows its product chrome — code
blocks, terminal output, model comparison tables, agentic-flow
diagrams. The cream-to-dark contrast is the page's pacing rhythm.

**Key Characteristics:**

- Warm cream canvas (`{colors.canvas}` — #faf9f5) with dark warm-ink
  text (`{colors.ink}` — #141413). The brand's defining color choice.
- Coral primary CTA (`{colors.primary}` — #cc785c). Used scarcely on
  individual buttons, generously on full-bleed coral callout cards.
- Slab-serif display headlines via Copernicus / Tiempos Headline at
  weight 400 with negative letter-spacing. Pairs with humanist sans
  body for a literary editorial voice.
- Dark navy product mockup cards (`{colors.surface-dark}` — #181715)
  carrying code blocks, terminal panels, model comparison data — the
  brand shows the product chrome at scale rather than abstract
  marketing illustrations.
- Light cream feature cards (`{colors.surface-card}` — #efe9de) —
  slightly darker than canvas, used for content-driven feature
  explanations.
- Anthropic radial-spike mark — a small black asterisk-like glyph
  (4-spoke radial) — appears as the brand wordmark prefix and as a
  content marker.
- Border radius is hierarchical: `{rounded.md}` (8px) for buttons +
  inputs, `{rounded.lg}` (12px) for content + product cards,
  `{rounded.xl}` (16px) for the hero illustration container,
  `{rounded.pill}` for badges.
- Section rhythm `{spacing.section}` (96px) — modern-SaaS standard.
  Internal card padding stays generous at `{spacing.xl}` (32px).

### Note on Font Substitutes (we use on this site)

Copernicus and StyreneB are licensed Anthropic typefaces and not
available as public web fonts. On this site we substitute with the
closest open-source matches that preserve the editorial voice:

| Role            | Spec (licensed)            | We use                              | Why |
|:----------------|:---------------------------|:------------------------------------|:----|
| Display         | Copernicus / Tiempos Headline | **EB Garamond** (400, 500)         | The closest open-source editorial serif; refined, period-correct feel; loads from Google Fonts |
| Body            | StyreneB                   | **Inter** (400, 500, 600)           | Humanist sans designed for screen reading; identical proportions to StyreneB at body sizes |
| Code            | JetBrains Mono             | **JetBrains Mono** (400)            | Already the spec's monospace; available on Google Fonts |

For the display font, the spec recommends **Cormorant Garamond** at
weight 500 with `-0.02em` letter-spacing as the primary substitute;
we use EB Garamond because it has a slightly wider x-height that
reads better at small sizes, but the visual character is the same
family. If you'd prefer Cormorant, swap the `--font-display` CSS
variable in `assets/css/site.css` to `"Cormorant Garamond", ...` and
update the Google Fonts link in `_includes/head.html`.

## Colors

### Brand & Accent

- **Coral / Primary** (`{colors.primary}` — #cc785c): The signature
  Anthropic warm coral. Used on every primary CTA background, on
  full-bleed coral callout cards, on the brand wordmark accent. The
  most-recognized Anthropic color outside of the spike-mark logo.
- **Coral Active** (`{colors.primary-active}` — #a9583e): The press
  / hover-darker variant.
- **Coral Disabled** (`{colors.primary-disabled}` — #e6dfd8): A
  desaturated cream-tinted disabled state.
- **Accent Teal** (`{colors.accent-teal}` — #5db8a6): Used sparingly
  on secondary product surfaces (terminal status indicators, "active
  connection" dots in connectors page).
- **Accent Amber** (`{colors.accent-amber}` — #e8a55a): A small
  companion warm-tone used on category badges and inline highlights.

### Surface

- **Canvas** (`{colors.canvas}` — #faf9f5): The default page floor.
  Tinted cream — warm, deliberately not pure white.
- **Surface Soft** (`{colors.surface-soft}` — #f5f0e8): Section
  dividers, very-soft band backgrounds.
- **Surface Card** (`{colors.surface-card}` — #efe9de): Feature
  cards, content cards. One step darker than canvas.
- **Surface Cream Strong** (`{colors.surface-cream-strong}` — #e8e0d2):
  A strongest-cream variant used on selected category tabs and
  emphasized section bands.
- **Surface Dark** (`{colors.surface-dark}` — #181715): Code editor
  mockups, model showcase cards, footer. The dominant dark surface.
- **Surface Dark Elevated** (`{colors.surface-dark-elevated}` —
  #252320): Elevated cards inside dark bands (settings panels in
  mockups).
- **Surface Dark Soft** (`{colors.surface-dark-soft}` — #1f1e1b):
  Slightly lighter dark, used for code block backgrounds inside
  larger dark cards.
- **Hairline** (`{colors.hairline}` — #e6dfd8): The 1px border tone
  on cream surfaces. Same hex as `{colors.primary-disabled}` —
  borders feel like one elevation step rather than ink lines.
- **Hairline Soft** (`{colors.hairline-soft}` — #ebe6df):
  Barely-visible divider used inside the same band.

### Text

- **Ink** (`{colors.ink}` — #141413): All headlines and primary
  text. Warm dark, slightly off-pure-black.
- **Body Strong** (`{colors.body-strong}` — #252523): Emphasized
  paragraphs, lead text.
- **Body** (`{colors.body}` — #3d3d3a): Default running-text color.
- **Muted** (`{colors.muted}` — #6c6a64): Sub-headings, breadcrumbs,
  footer-adjacent secondary text.
- **Muted Soft** (`{colors.muted-soft}` — #8e8b82): Captions,
  fine-print, copyright lines.
- **On Primary** (`{colors.on-primary}` — #ffffff): Text on coral
  buttons.
- **On Dark** (`{colors.on-dark}` — #faf9f5): Cream-tinted white used
  on dark surfaces (echoes the canvas tone).
- **On Dark Soft** (`{colors.on-dark-soft}` — #a09d96): Footer body
  text, secondary labels in dark mockups.

### Semantic

- **Success** (`{colors.success}` — #5db872): Green status dots,
  "available" indicators.
- **Warning** (`{colors.warning}` — #d4a017): Warning callouts (rare
  on marketing surfaces).
- **Error** (`{colors.error}` — #c64545): Validation errors.

## Typography

### Font Family

The system runs **Copernicus** (or **Tiempos Headline** as
substitute) as the slab-serif display face for headlines, and
**StyreneB** (or **Inter** as substitute) as the humanist sans for
body, navigation, and UI labels. **JetBrains Mono** handles code
blocks. The fallback stack walks `Tiempos Headline, Garamond, "Times
New Roman", serif` for display and `Inter, -apple-system,
BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` for body.

The display/body split is editorial:

- Copernicus serif (weight 400, negative tracking) → h1, h2, h3, hero
  display
- StyreneB sans (weight 400-500) → body, navigation, buttons,
  captions, labels
- JetBrains Mono → all code blocks and terminal text

### Hierarchy

| Token                       | Size  | Weight | Line Height | Letter Spacing | Use |
|:----------------------------|:-----:|:------:|:-----------:|:--------------:|:---|
| `{typography.display-xl}`  | 64px  | 400    | 1.05        | -1.5px         | Homepage h1 ("Meet your thinking partner") — Copernicus serif |
| `{typography.display-lg}`  | 48px  | 400    | 1.1         | -1px           | Section heads — Copernicus |
| `{typography.display-md}`  | 36px  | 400    | 1.15        | -0.5px         | Sub-section heads, model names — Copernicus |
| `{typography.display-sm}`  | 28px  | 400    | 1.2         | -0.3px         | Pricing tier names, callout headlines — Copernicus |
| `{typography.title-lg}`    | 22px  | 500    | 1.3         | 0              | Pricing plan size labels — StyreneB |
| `{typography.title-md}`    | 18px  | 500    | 1.4         | 0              | Feature card titles, intro paragraphs |
| `{typography.title-sm}`    | 16px  | 500    | 1.4         | 0              | Connector tile titles, list labels |
| `{typography.body-md}`     | 16px  | 400    | 1.55        | 0              | Default running-text — StyreneB |
| `{typography.body-sm}`     | 14px  | 400    | 1.55        | 0              | Footer body, fine-print |
| `{typography.caption}`     | 13px  | 500    | 1.4         | 0              | Badge labels, captions |
| `{typography.caption-uppercase}` | 12px | 500 | 1.4      | 1.5px          | Category tags, "NEW" badges |
| `{typography.code}`        | 14px  | 400    | 1.6         | 0              | Code blocks — JetBrains Mono |
| `{typography.button}`      | 14px  | 500    | 1.0         | 0              | Standard button labels |
| `{typography.nav-link}`    | 14px  | 500    | 1.4         | 0              | Top-nav menu items |

### Principles

Display sizes use weight 400 (regular), never bold. Negative
letter-spacing (-0.3 to -1.5px) is essential — Copernicus without it
reads as off-brand. The serif character is what gives Anthropic its
literary, considered voice; switching to a sans-serif display would
make Claude feel like every other AI tool.

Body type stays at weight 400 for paragraphs, weight 500 for labels
and emphasized phrases. The sans body is humanist (StyreneB) — never
geometric. Inter is an acceptable substitute because of its similar
humanist proportions; Helvetica or Arial would be too neutral and
break the warm-editorial feel.

## Layout

### Spacing System

- **Base unit:** 4px.
- **Tokens:** `{spacing.xxs}` 4px · `{spacing.xs}` 8px ·
  `{spacing.sm}` 12px · `{spacing.md}` 16px · `{spacing.lg}` 24px ·
  `{spacing.xl}` 32px · `{spacing.xl}` 32px · `{spacing.xxl}` 48px ·
  `{spacing.section}` 96px.
- **Section padding:** `{spacing.section}` (96px) — modern-SaaS rhythm.
- **Card internal padding:** `{spacing.xl}` (32px) for feature cards,
  pricing tier cards, model comparison cards; `{spacing.lg}` (24px)
  for code-window cards and connector tiles.
- **Callout / CTA bands:** `{spacing.xxl}` (48px) inside coral callout
  cards; 64px inside the larger dark CTA band.

### Grid & Container

- **Max content width:** ~1200px centered.
- **Editorial body:** Single 12-column grid; hero often uses 6/6
  split (h1 left, illustration right).
- **Feature card grids:** 3-up at desktop, 2-up at tablet, 1-up at
  mobile.
- **Connector tile grids:** 4-up or 6-up at desktop, 2-up at tablet,
  1-up at mobile.
- **Pricing grid:** 3-up at desktop (Free / Pro / Team / Enterprise
  often), 1-up at mobile.

### Whitespace Philosophy

The cream canvas + serif display + generous internal padding create
an editorial pacing — Claude reads like a long-form magazine column
rather than a marketing template. Whitespace between bands stays
uniform at 96px; whitespace inside cards is generous (32px), letting
type breathe.

## Elevation & Depth

| Level                  | Treatment                                              | Use |
|:-----------------------|:-------------------------------------------------------|:----|
| Flat                   | No shadow, no border                                   | Body sections, top nav, hero bands |
| Soft hairline          | 1px `{colors.hairline}` border                         | Inputs, sub-nav, occasionally on cards |
| Cream card             | `{colors.surface-card}` background — no shadow         | Feature cards, content cards |
| Dark surface card      | `{colors.surface-dark}` background — no shadow         | Code editor mockups, model showcase cards |
| Subtle drop shadow     | Faint shadow at low alpha                              | Hover-elevated states (the system uses `0 1px 3px rgba(20,20,19,0.08)` rarely) |

The elevation philosophy is **color-block first, shadow rare**. Most
depth comes from the cream-vs-dark surface contrast. Shadows are
minimal. The dark surface mockups have their own internal product
chrome (code editor scrollbars, line numbers, syntax highlighting)
which adds detail without needing external shadows.

### Decorative Depth

- The Anthropic spike-mark glyph (4-spoke radial asterisk) appears
  as a small black mark in the brand wordmark and inline as a
  content marker.
- Code editor mockups carry their own internal depth: syntax-
  highlighted text in muted blues / oranges / grays, line numbers
  in `{colors.muted-soft}`, status bars at the bottom in
  `{colors.surface-dark-elevated}`.
- Some hero illustrations use simple line-art with coral and dark-
  navy strokes on cream — minimal, hand-drawn-feeling, never
  photorealistic.

## Shapes

### Border Radius Scale

| Token            | Value          | Use |
|:-----------------|:--------------:|:----|
| `{rounded.xs}`   | 4px            | Reserved for badge accents and tiny dropdowns |
| `{rounded.sm}`   | 6px            | Small inline buttons, dropdown items |
| `{rounded.md}`   | 8px            | Standard CTA buttons, text inputs, category tabs |
| `{rounded.lg}`   | 12px           | Content cards (feature, pricing, code-window, model-comparison) |
| `{rounded.xl}`   | 16px           | Hero illustration container, the larger marquee components |
| `{rounded.pill}` | 9999px         | Badge pills, "NEW" tags |
| `{rounded.full}` | 9999px / 50%   | Avatar substitutes, icon buttons |

### Photography & Illustrations

Claude's hero rarely uses photography. Instead it uses:

- Simple line-art illustrations with coral + dark-navy strokes on
  the cream canvas
- Code editor mockups (the dominant "hero" treatment on
  developer-focused pages)
- Terminal output mockups with monospace text on dark
- Model comparison cards (Opus / Sonnet / Haiku) with abstract
  geometric thumbnails

When photography is used (rare — mostly testimonials), avatars crop
to perfect circles at 40px diameter.

## Components

### Top Navigation

**`top-nav`** — Cream nav bar pinned to the top of every page. 64px
tall, `{colors.canvas}` background. Carries the Anthropic spike-mark +
"Claude" wordmark at left, primary horizontal menu (Product,
Solutions, Use Cases, Pricing, Research, Company) center-left,
right-side cluster with "Sign in" text-link, "Try Claude"
`{component.button-primary}` (coral). Menu items in
`{typography.nav-link}` (StyreneB 14px / 500).

### Buttons

**`button-primary`** — The signature coral CTA. Background
`{colors.primary}` (#cc785c), text `{colors.on-primary}` (white),
type `{typography.button}` (StyreneB 14px / 500), padding 12px ×
20px, height 40px, rounded `{rounded.md}` (8px). Active state
`button-primary-active` darkens to `{colors.primary-active}`
(#a9583e).

**`button-secondary`** — Cream button with hairline outline.
Background `{colors.canvas}`, text `{colors.ink}`, 1px hairline
border, same padding + height + radius as primary.

**`button-secondary-on-dark`** — Used over `{colors.surface-dark}`
cards. Background `{colors.surface-dark-elevated}` (#252320), text
`{colors.on-dark}`. Stays dark — the system never inverts to a light
secondary on dark surfaces.

**`button-text-link`** — Inline text button, no background. Used for
"Sign in" in the top nav and inline CTA links.

**`button-icon-circular`** — 36px circular icon button. Background
`{colors.canvas}`, hairline border, ink-color icon. Used for
carousel arrows, share, "view more".

**`text-link`** — Inline body links in `{colors.primary}` (the
coral). Underlined on press; the coral inline link is one of the
system's most distinctive small details.

### Cards & Containers

**`hero-band`** — Cream-canvas hero with a 6-6 grid: h1 + sub-
headline + button row on the left, hero illustration card or product
mockup card on the right. Vertical padding `{spacing.section}`
(96px).

**`hero-illustration-card`** — A larger card holding the hero's
right-side artifact — sometimes a coral-stroke line illustration on
cream background, sometimes a dark code editor mockup. Background
`{colors.canvas}` or `{colors.surface-dark}` depending on context,
rounded `{rounded.xl}` (16px).

**`feature-card`** — Used in 3-up feature grids. Background
`{colors.surface-card}` (#efe9de — slightly darker cream), rounded
`{rounded.lg}` (12px), internal padding `{spacing.xl}` (32px).
Carries a small icon at top, an `{typography.title-md}` headline,
and a body description in `{typography.body-md}`.

**`product-mockup-card-dark`** — Dark navy card showing actual
Claude product chrome (chat interface, code editor, agent
controls). Background `{colors.surface-dark}`, rounded
`{rounded.lg}`, internal padding `{spacing.xl}` (32px). Carries text
labels in `{colors.on-dark}` and product UI fragments below.

**`code-window-card`** — A specialized dark card showing a code
editor with line numbers, syntax-highlighted code in
`{typography.code}` (JetBrains Mono), and sometimes a "Run" button
or terminal output panel below. Background `{colors.surface-dark}`
with `{colors.surface-dark-soft}` for the inner code block, rounded
`{rounded.lg}`, padding `{spacing.lg}` (24px). The signature visual
element of Claude Code product pages.

**`model-comparison-card`** — Used on the homepage's "Which problem
are you up against?" section comparing Opus / Sonnet / Haiku.
Background `{colors.canvas}` with hairline border, rounded
`{rounded.lg}`, internal padding `{spacing.xl}` (32px). Carries the
model name, a short capability blurb, and a
`{component.text-link}` to learn more.

**`pricing-tier-card`** — Standard tier card. Background
`{colors.canvas}` with hairline border, rounded `{rounded.lg}`,
padding `{spacing.xl}` (32px). Carries the plan name in
`{typography.title-lg}` (StyreneB), price in `{typography.display-sm}`
(Copernicus serif!), feature checklist in `{typography.body-md}`,
and a `{component.button-primary}` at the bottom.

**`pricing-tier-card-featured`** — The featured tier (typically
"Pro" or "Team"). Background flips to `{colors.surface-dark}`, text
inverts to `{colors.on-dark}`. The dark surface IS the featured-tier
signal.

**`callout-card-coral`** — A full-bleed coral card carrying a major
call-to-action. Background `{colors.primary}` (#cc785c), text
`{colors.on-primary}` (white), rounded `{rounded.lg}`, padding
`{spacing.xxl}` (48px). The coral surface IS the voltage; the CTA
inside uses an inverted button style (cream/canvas button on
coral).

**`connector-tile`** — Used on the connectors page's integration
grid. Background `{colors.canvas}` with hairline border, rounded
`{rounded.lg}`, padding 20px. Each tile carries a logo at top, a
`{typography.title-sm}` connector name, and a short description.

### Inputs & Forms

**`text-input`** — Standard text input. Background
`{colors.canvas}`, text `{colors.ink}`, type `{typography.body-md}`,
rounded `{rounded.md}` (8px), padding 10px × 14px, height 40px.
1px hairline border in `{colors.hairline}`.

**`text-input-focused`** — Focus state. Border thickens or shifts to
`{colors.primary}` (coral) for emphasis. Carries a 3px
coral-at-15%-alpha outer ring.

**`cookie-consent-card`** — Bottom-right floating dark cookie
banner. Background `{colors.surface-dark}`, text
`{colors.on-dark}`, rounded `{rounded.lg}`, padding
`{spacing.lg}` (24px). One of the few places dark surface appears
at small scale on cream pages.

### Tags / Badges

**`badge-pill`** — Small pill label used for category tags.
Background `{colors.surface-card}`, text `{colors.ink}`, type
`{typography.caption}` (13px / 500), rounded `{rounded.pill}`,
padding 4px × 12px.

**`badge-coral`** — Coral-fill badge for "NEW", "BETA", featured
highlights. Background `{colors.primary}`, text
`{colors.on-primary}`, type `{typography.caption-uppercase}` (12px
/ 500 / 1.5px tracking), rounded `{rounded.pill}`, padding 4px ×
12px.

### Tab / Filter

**`category-tab`** + **`category-tab-active`** — Used in sub-nav
rows on solutions / connectors pages. Inactive: transparent
background, `{colors.muted}` text. Active: `{colors.surface-card}`
background, `{colors.ink}` text. Padding 8px × 14px, rounded
`{rounded.md}`.

### CTA / Footer

**`cta-band-coral`** — A pre-footer "Try Claude" CTA card. Full-
width coral fill, white type, rounded `{rounded.lg}`, padding 64px.
Carries an h2 in `{typography.display-sm}` (still serif!), a sub-
line, and a cream-button CTA.

**`cta-band-dark`** — Alternative pre-footer band on developer-
focused pages. Background `{colors.surface-dark}`, text
`{colors.on-dark}`, rounded `{rounded.lg}`, padding 64px. Often pairs
with a code-window card.

**`footer`** — Dark navy footer that closes every page. Background
`{colors.surface-dark}` (#181715), text `{colors.on-dark-soft}`.
4-column link list at desktop covering Product / Company / Resources
/ Legal. Vertical padding 64px. The Anthropic spike-mark +
"Anthropic" wordmark sits at the top in `{colors.on-dark}`. The
footer never inverts.

## Do's and Don'ts

### Do

- Anchor every page on the cream canvas. Pure white reads as "any
  other AI tool"; the warm tint is the brand differentiator.
- Use Copernicus serif for every display headline. Pair with
  StyreneB sans body. Negative letter-spacing on display sizes is
  non-negotiable.
- Reserve `{colors.primary}` (coral) for primary CTAs and full-bleed
  `{component.callout-card-coral}` moments. Don't paint accent
  moments coral elsewhere.
- Use `{component.product-mockup-card-dark}` and
  `{component.code-window-card}` to show actual Claude product
  chrome. Don't paint marketing illustrations of code when you can
  show real code.
- Pair `{component.feature-card}` (cream) with
  `{component.product-mockup-card-dark}` (navy) in alternating
  bands. The cream-to-dark rhythm is the brand's pacing mechanism.
- Use the Anthropic spike-mark glyph as the brand wordmark prefix.
  Never invert the mark to white-on-dark within the wordmark itself.
- Apply `{spacing.section}` (96px) between major bands.

### Don't

- Don't use cool grays or pure white for canvas. Cream is the brand.
- Don't bold serif display weight. Copernicus at 700 reads as
  bombastic; the system stays at 400.
- Don't use cool blue or saturated cyan as a brand accent. The coral
  is the brand voltage.
- Don't put coral everywhere. The coral is scarce on individual
  elements and generous only on full-bleed coral callout cards.
- Don't use Inter for display headlines. The serif character is the
  brand voice.
- Don't repeat the same surface mode in two consecutive bands. The
  pacing alternates: cream → cream-card → dark-mockup → cream →
  coral-callout → dark-footer.
- Don't add hover state styling beyond what the system already
  encodes — primary darkens on press; nothing else changes.

## Responsive Behavior

### Breakpoints

| Name    | Width       | Key Changes |
|:--------|:------------|:------------|
| Mobile  | < 768px     | Hamburger nav; hero h1 64→32px; hero-illustration-card stacks below content; feature grids 1-up; connector tiles 2-up; pricing 1-up; footer 4 cols → 1 |
| Tablet  | 768–1024px  | Top nav stays horizontal but tightens; feature cards 2-up; connector tiles 3-up; pricing 2-up |
| Desktop | 1024–1440px | Full top-nav with all menu items; 3-up feature cards; 4-up or 6-up connector tiles; 3-up pricing tiers |
| Wide    | > 1440px    | Same as desktop with more outer breathing room; max content width caps at 1200px |

### Touch Targets

- `{component.button-primary}` at minimum 40 × 40px.
- `{component.button-icon-circular}` at exactly 36 × 36 — slightly
  under WCAG 44 but visually centered.
- `{component.text-input}` height is 40px.
- Connector tile entire card area is tappable; effective tap area
  >> 44px.

### Collapsing Strategy

- Top nav collapses to hamburger at < 768px; menu opens as a
  full-screen cream sheet.
- Hero band's 6-6 grid collapses to single-column on mobile — h1 +
  sub-head + buttons first, then the illustration / mockup card
  below.
- Feature grids reduce columns rather than scaling cards down.
- Pricing tier cards collapse 4 → 2 → 1; featured-tier dark surface
  stays visually distinct at every breakpoint.
- Code-window cards retain code legibility at every breakpoint by
  allowing horizontal scroll within the card rather than wrapping
  code lines.

### Image Behavior

- Code blocks inside dark mockups stay at fixed font-size;
  horizontal scroll on mobile rather than wrapping.
- Hero illustrations scale proportionally; line-art strokes thin
  slightly on mobile.
- Avatar photos in testimonials crop to circles at every breakpoint.

## Iteration Guide

1. Focus on ONE component at a time. Reference its YAML key
   (`{component.feature-card}`, `{component.code-window-card}`).
2. Variants of an existing component (`-active`, `-disabled`,
   `-focused`) live as separate entries in `components:`.
3. Use `{token.refs}` everywhere — never inline hex.
4. Never document hover. Default and Active/Pressed states only.
5. Display headlines stay Copernicus serif 400 with negative
   tracking. Body stays StyreneB / Inter 400. The split is
   unbreakable.
6. Cream + coral + dark navy is the trinity. Don't introduce a
   fourth surface tone (no purple cards, no green sections).
7. When in doubt about emphasis: bigger Copernicus serif before
   bolder weight.

## Known Gaps

- Copernicus and StyreneB are licensed Anthropic typefaces and not
  available as public web fonts. Substitutes (Tiempos Headline /
  Cormorant Garamond / EB Garamond for serif; Inter / Söhne for sans)
  are documented in the typography section.
- The Anthropic radial-spike-mark is a brand glyph rendered as
  inline SVG; it's not formalized as a system token here. Treat it
  as a logo asset.
- Animation and transition timings (chat message reveal, code
  block typewriter effect on the homepage, agentic-flow diagram
  animations) are not in scope.
- Form validation states beyond `{component.text-input-focused}`
  are not extracted — error / success states would need a sign-up or
  feedback flow to confirm.
- The actual Claude product surface (claude.ai chat interface)
  shares some tokens with the marketing site but adds many product-
  specific components (chat bubbles, message tools, file upload
  chips, conversation history sidebar) that are out of scope for
  this marketing-surface document.
- The "agent" / "computer use" demo cards on certain pages display
  animated Claude controlling a browser — the static screenshot
  doesn't fully capture the animation chrome.

## Implementation Status (DFT Notes site)

What this site has built from this spec:

- [x] Color tokens → `--color-*` CSS variables in
      `assets/css/site.css`
- [x] Typography scale → `--font-display`, `--font-body`,
      `--font-mono`, type-scale CSS variables
- [x] `top-nav` component with mobile hamburger
- [x] `button-primary` (coral), `button-secondary` (cream +
      hairline), `button-text-link`
- [x] `hero-band` with 6-6 grid that collapses on mobile
- [x] `code-window-card` for code samples
- [x] `feature-card` for content cards
- [x] `callout-card-coral` (used for pre-footer CTA)
- [x] `badge-pill`, `badge-coral`
- [x] `footer` (dark navy, 4-col → 1-col on mobile)
- [x] Mobile hamburger menu (vanilla JS, no framework)
- [x] Skip-to-content link for a11y
- [x] **v2** — Theme switcher (light + dark) with persistent
      localStorage
- [x] **v2** — Pastel poppy-green light palette, warm-dark
      dark palette
- [x] **v2** — Wider reading column on large screens
      (760px → 960px → 1100px)
- [x] **v2** — Marginalia rail for figures and side notes
- [x] **v2** — Mermaid diagrams (` ```mermaid ` fences) with
      theme-aware palette
- [x] **v2** — `dft_notes/chapters-map.md` — a live Mermaid
      graph of every chapter
- [x] **v2** — `dft_notes/python_codes/` — per-chapter
      subfolders with runnable Python + generated plots
- [x] **v2** — Hidden answers via `<details><summary>` for
      problem sets
- [x] **v2** — `agents.md` — the agent handbook
- [x] **v2** — Footer cleaned up: no chapter list, just four
      short link columns

What this site has not yet built (out of scope right now):

- [ ] Pricing tier cards (we don't have a pricing surface)
- [ ] Cookie consent banner (no third-party tracking)
- [ ] `cta-band-coral` (we use `callout-card-coral` instead —
      equivalent component, different name)
- [ ] Connector tile grid (no integrations page yet)
- [ ] `@chenglou/pretext` e-reader (see `design.md` v3 in
      git history — future work, not the current Jekyll site)
- [ ] Animated transitions (motion-reduced by default per
      `prefers-reduced-motion`)

## Palette (v2)

The v1 cream + coral palette worked for a marketing surface,
but the user pointed out that for *reading* long sessions the
cream was too close to white.  v2 picks a softer pastel:

| Token                  | Light (v2) | Dark (v2)  | Notes |
|:-----------------------|:-----------|:-----------|:------|
| `--color-canvas`       | `#eef0e6`  | `#1a1814`  | Pastel poppy-green vs warm dark |
| `--color-surface-soft` | `#e3e6d8`  | `#252220`  | One step darker than canvas |
| `--color-surface-card` | `#d6dcc8`  | `#2e2a24`  | Feature cards, callouts in light |
| `--color-hairline`     | `#cdd3bd`  | `#3a342a`  | 1px borders on the canvas |
| `--color-ink`          | `#1c1f17`  | `#f0ebde`  | Headlines, body emphasis |
| `--color-body`         | `#3a4031`  | `#c4bca8`  | Default running text |
| `--color-muted`        | `#6b7060`  | `#8a8270`  | Secondary text |
| `--color-primary`      | `#cc785c`  | `#cc785c`  | **Coral — unchanged in v2** |
| `--color-primary-active` | `#a9583e` | `#a9583e` | Hover/active coral |
| `--color-on-primary`   | `#ffffff`  | `#ffffff`  | Text on coral |
| `--color-on-dark`      | —          | `#f0ebde`  | Cream-tinted text on dark surfaces |
| `--color-on-dark-soft` | —          | `#a09d96`  | Secondary text on dark |

The cream + dark-navy product surfaces (`--color-surface-dark`
etc.) are **kept unchanged** for code-window cards, model
comparisons, and the footer — they work on both themes.

## Reading column (v2)

The v1 chapter column was `max-width: 760px` everywhere.  On
a 1920px screen that left ~580px of dead space on each side.
v2 grows progressively:

| Breakpoint     | `.page-content` max-width |
|:---------------|:--------------------------|
| `< 768px`      | `100%` (with 24px padding) |
| `768 – 1024px` | `760px` (mobile-friendly) |
| `1024 – 1440px` | `960px` (slightly wider) |
| `≥ 1440px`     | `1100px` (wide-screen reading) |

Inside the wider column, authors can use:

- `<aside class="marginalia">` for right-rail figure captions
  or side notes
- `<figure class="figure-wide">` for full-width images
- `<table class="table-scroll">` for wide tables with
  horizontal scroll

## Theme switcher (v2)

The user wants to read for long sessions.  v2 adds a
**light / dark** toggle:

- The toggle is a small icon button in the top nav, between
  the GitHub text-link and the "Read the notes" CTA.
- Preference is persisted in `localStorage` under the key
  `dft-notes:theme` with values `light` | `dark`.
- A tiny inline script in `<head>` reads the stored value
  (or the OS `prefers-color-scheme`) and sets
  `data-theme="dark"` on `<html>` **before** the CSS loads —
  this prevents a flash of the wrong theme on first paint.
- CSS variables are organized so `:root` holds the light
  palette and `[data-theme="dark"]` overrides the same names
  with the dark palette.  All component styles are written
  against the variable names, so the switch is automatic.

## Mermaid (v2)

Authors can drop a Mermaid diagram into any chapter with a
fenced code block whose language is `mermaid`:

````markdown
```mermaid
graph TD
  A[Schrödinger] --> B[Hartree-Fock]
  B --> C[Kohn-Sham]
```
````

The Mermaid library is loaded from
`https://cdn.jsdelivr.net/npm/mermaid@10` and initialized with
`startOnLoad: true`.  The init script picks the theme palette
from `[data-theme]` so diagrams match the page.

`dft_notes/chapters-map.md` is the canonical example — a live
Mermaid graph of every chapter, with the planned future
chapters dimmed and labelled `(planned)`.

## Python codes (v2)

Code that runs in a chapter lives **twice**:

1. **Inline in the chapter** (as a fenced code block) for
   reading.
2. **In `dft_notes/python_codes/chapter_NN/NN-slug.py`** as a
   runnable file.

The folder structure is:

```
dft_notes/python_codes/
├── README.md                 ← how to run, how to add a new script
├── chapter_00/
│   ├── 01-particle-in-box.py
│   ├── plots/
│   │   └── particle-in-box.png  ← generated, committed
│   └── ...
├── chapter_01/
│   └── ...
```

Scripts that produce plots commit the PNG alongside the
script.  The README documents the `python` version, the
required packages (numpy, matplotlib, scipy), and the
convention for naming.

## Hidden answers (v2)

Problem sets use HTML `<details>` for the answer:

```html
<details class="problem">
  <summary>Show hint</summary>
  Start from $E = mc^2$ and the definition of momentum.
</details>

<details class="answer">
  <summary>Show answer</summary>
  Derivation: ...step by step...
</details>
```

CSS styles `<details>` with the design system: a soft-card
background, coral summary text, a thin left border, smooth
open/close animation.

## Repository structure (v2)

The full tree, with purpose of each path:

```
DFT-notes/
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/bug_report.md
│   ├── pull_request_template.md
│   └── workflows/
│       ├── jekyll.yml           ← build + deploy to Pages
│       └── markdown-lint.yml   ← markdownlint-cli2 (v0.40)
│
├── _includes/                  ← Liquid partials
│   ├── head.html               ← meta + fonts + CSS + SEO + MathJax + Mermaid
│   ├── nav.html                ← top nav, mobile menu, theme switcher
│   ├── footer.html             ← dark navy footer (no chapter list)
│   ├── spike-mark.html         ← reusable 4-spoke radial SVG
│   └── mathjax.html            ← MathJax 3 config
│
├── _layouts/                   ← Jekyll layouts
│   ├── default.html            ← wrapper: skip + nav + main + footer + nav.js + theme init
│   └── page.html               ← .page-content div for reading column
│
├── assets/
│   ├── css/site.css            ← The design system (variables + components)
│   └── js/
│       ├── nav.js              ← mobile menu toggle
│       ├── theme.js            ← theme switcher (persist + toggle)
│       └── mermaid-init.js     ← mermaid.initialize() with theme-aware palette
│
├── design.md                   ← THIS FILE (excluded from served site)
├── agents.md                   ← The agent handbook (excluded from served site)
│
├── dft_notes/                  ← The actual content
│   ├── index.md                ← chapter index
│   ├── chapters-map.md         ← Mermaid graph of all chapters
│   ├── chapter_00/00-welcome.md
│   ├── chapter_NN/00-topic.md
│   ├── python_codes/
│   │   ├── README.md
│   │   ├── chapter_00/
│   │   │   ├── 01-particle-in-box.py
│   │   │   ├── plots/particle-in-box.png
│   │   │   └── ...
│   │   └── chapter_NN/
│   └── ...
│
├── _config.yml                 ← Jekyll config
├── Gemfile                     ← jekyll 3.10 + minima + kramdown-parser-gfm
├── 404.md
├── index.md                    ← hero-band home page
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── README.md                   ← repo overview + this structure
└── .markdownlint-cli2.jsonc    ← linter config (MD013, MD033, MD025,
                                  MD040, MD024, MD026, MD049, MD060
                                  disabled by design)
```

This is the structure that **must not drift**.  Adding a
new chapter goes in `dft_notes/chapter_NN/`.  Adding a new
Python script goes in `dft_notes/python_codes/chapter_NN/`.
Adding a new component class goes in `assets/css/site.css`.
Adding a new page-level layout goes in `_layouts/`.  No new
top-level directories without updating this file.



