# E-Reader Design Specification (v3)

> **About `@chenglou/pretext`:** It is a pure JavaScript/TypeScript library
> for multiline text measurement & layout — fast, accurate, and supporting
> all languages. It allows rendering to DOM, Canvas, SVG and soon,
> server-side. Pretext side-steps the need for DOM measurements like
> `getBoundingClientRect` / `offsetHeight`, which trigger layout reflow —
> one of the most expensive operations in the browser.
>
> **Status of this document:** Reference spec for the future e-reader
> surface that will render the notes in `dft_notes/`. The current site
> (`_config.yml` + minima + MathJax 3) is the **Jekyll host**; the
> e-reader is a layer on top. See the README in `dft_notes/` for the
> short-term content plan.

---

> **Stack:** [`@chenglou/pretext`](https://github.com/chenglou/pretext) ·
> Math via KaTeX · Canvas/DOM/SVG render targets · Light & Dark themes

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Pretext Integration](#pretext-integration)
4. [Theme System](#theme-system)
5. [Typography Scale](#typography-scale)
6. [Math Rendering](#math-rendering)
7. [Tables](#tables)
8. [Figures & Media](#figures--media)
9. [Layout Engine](#layout-engine)
10. [Component Tree](#component-tree)
11. [Token Reference](#token-reference)
12. [Accessibility](#accessibility)
13. [Performance Budget](#performance-budget)
14. [File Structure](#file-structure)

---

## Overview

The e-reader is a **DOM-free, canvas-first** reading surface. Text layout
is delegated entirely to `@chenglou/pretext` — no `offsetHeight`, no
reflow, no layout thrash. Math blocks are rendered via **KaTeX**
(server-side pre-baked or client hydration). Figures, tables, and code
blocks are composited as discrete **layout boxes** sitting between
pretext text columns.

```
┌─────────────────────────────────────────────────┐
│  Toolbar  [☀︎/🌙]  [Aa]  [‹ Prev]  [Next ›]     │
├─────────────────────────────────────────────────┤
│                                                 │
│   ░░░░ Reading Column (pretext canvas) ░░░░     │
│                                                 │
│   ┌─────────────────────────────────────────┐  │
│   │  Inline Math / Block Math / Table / Fig │  │
│   └─────────────────────────────────────────┘  │
│                                                 │
│   ░░░░ Reading Column (cont.) ░░░░░░░░░░░░░░   │
│                                                 │
├─────────────────────────────────────────────────┤
│  Footer  [Page 12 / 340]  [████░░░░░░]  35 %   │
└─────────────────────────────────────────────────┘
```

## Architecture

```
src/
├── engine/
│   ├── pretextPipeline.ts   ← prepare() / layout() orchestration
│   ├── mathRenderer.ts      ← KaTeX → SVG → canvas compositing
│   ├── tableRenderer.ts     ← grid measure + pretext cell layout
│   └── figureRenderer.ts    ← image / diagram / caption pipeline
├── themes/
│   ├── tokens.ts            ← design tokens (light + dark)
│   └── themeProvider.ts     ← OS preference + manual toggle
├── components/
│   ├── ReaderCanvas.tsx     ← main <canvas> surface
│   ├── Toolbar.tsx
│   ├── ProgressBar.tsx
│   └── FontPicker.tsx
└── pages/
    └── index.tsx
```

### Data Flow

```
Raw document (Markdown / EPUB / HTML)
        │
        ▼
   ┌──────────┐      KaTeX
   │  Parser  │ ──────────────► MathBlock[]
   └──────────┘
        │ AST
        ▼
  ┌────────────────────────────────────────────┐
  │           Layout Orchestrator              │
  │  ┌──────────────┐   ┌──────────────────┐  │
  │  │ pretextPipeline│  │ figureRenderer   │  │
  │  │ prepare()     │  │ tableRenderer    │  │
  │  │ layout()      │  │ mathRenderer     │  │
  │  └──────────────┘   └──────────────────┘  │
  └─────────────────────────────┬──────────────┘
                                │ LineRange[]
                                ▼
                     ┌─────────────────┐
                     │  ReaderCanvas   │
                     │  ctx.fillText() │
                     │  ctx.drawImage()│
                     └─────────────────┘
```

## Pretext Integration

### Core API usage

```typescript
import {
  prepare,
  layout,
  layoutWithLines,
  measureNaturalWidth,
  materializeLineRange,
  setLocale,
  type PreparedText,
  type LayoutLine,
} from '@chenglou/pretext';

// ── 1. Prepare (horizontal-only, sync, cheap) ───────────────────
const prepared: PreparedText = prepare(paragraph.text, {
  font:        `${tokens.fontSize.body}px/${tokens.lineHeight.body} ${tokens.font.serif}`,
  width:       columnWidthPx,
  wordBreak:   'normal',
  whiteSpace:  'normal',
  letterSpacing: 0,
});

// ── 2. Layout (adds vertical geometry) ─────────────────────────
const lines: LayoutLine[] = layoutWithLines(prepared, {
  lineHeight: tokens.lineHeight.bodyPx,
});

// ── 3. Measure for truncation / column balancing ────────────────
const naturalW = measureNaturalWidth(prepared);

// ── 4. Materialize a page slice ────────────────────────────────
const pageSlice = materializeLineRange(lines, startLine, endLine);
```

### Rich inline (bold / italic / links / math inline)

```typescript
import {
  prepareWithSegments,
  type RichSpan,
} from '@chenglou/pretext';
import type { RichInlineItem } from '@chenglou/pretext/rich-inline';

const spans: RichSpan[] = parseInlineMarkdown(rawLine); // your parser
const prepared = prepareWithSegments(spans, {
  defaultFont: `${tokens.fontSize.body}px ${tokens.font.serif}`,
  width: columnWidthPx,
});
```

### Locale / CJK / RTL

```typescript
// Call once at boot, or on language change
setLocale(navigator.language);
```

## Theme System

### Light Theme tokens

```typescript
// tokens.ts
export const lightTheme = {
  // ── Surfaces ──────────────────────────────────────────────
  surface: {
    page:       '#FAF8F1',   // warm off-white — paper feel
    overlay:    '#FFFFFF',
    toolbar:    '#F2EFE7',
    footer:     '#F2EFE7',
    codeBlock:  '#F0EDE4',
    tableHead:  '#E8E4D9',
    tableRow:   '#FAF8F1',
    tableAlt:   '#F4F1E8',
    blockquote: '#EDE9DF',
    mathBlock:  '#FBF9F4',
  },

  // ── Text ──────────────────────────────────────────────────
  text: {
    primary:    '#1A1510',   // rich dark-brown
    secondary:  '#4A4035',
    muted:      '#7A7060',
    link:       '#2E5FA3',
    linkHover:  '#1A3D7A',
    code:       '#5A3E1B',
    math:       '#1A1510',
    caption:    '#6A6050',
    tableHead:  '#2A2015',
  },

  // ── Borders ───────────────────────────────────────────────
  border: {
    subtle:     '#DDD8CC',
    moderate:   '#C8C2B2',
    strong:     '#A09880',
    focus:      '#2E5FA3',
    table:      '#C8C2B2',
    mathBox:    '#D8D2C2',
  },

  // ── Syntax highlight (code blocks) ───────────────────────
  syntax: {
    keyword:    '#8B2252',
    string:     '#226622',
    number:     '#7A4000',
    comment:    '#808060',
    function:   '#2E5FA3',
    type:       '#5A3E8B',
    operator:   '#505050',
  },

  // ── Shadow ────────────────────────────────────────────────
  shadow: {
    card:       '0 2px 8px rgba(80,64,32,0.10)',
    toolbar:    '0 1px 4px rgba(80,64,32,0.08)',
    figure:     '0 3px 12px rgba(80,64,32,0.14)',
  },
};
```

### Dark Theme tokens

```typescript
export const darkTheme = {
  // ── Surfaces ──────────────────────────────────────────────
  surface: {
    page:       '#12100E',   // near-black warm
    overlay:    '#1C1916',
    toolbar:    '#1C1916',
    footer:     '#1C1916',
    codeBlock:  '#1E1C18',
    tableHead:  '#252220',
    tableRow:   '#12100E',
    tableAlt:   '#181512',
    blockquote: '#1A1714',
    mathBlock:  '#161310',
  },

  // ── Text ──────────────────────────────────────────────────
  text: {
    primary:    '#E8E0D0',   // warm parchment-white
    secondary:  '#B0A890',
    muted:      '#786E60',
    link:       '#7EB3F7',
    linkHover:  '#AAD0FF',
    code:       '#E0C090',
    math:       '#E8E0D0',
    caption:    '#8A8070',
    tableHead:  '#D0C8B0',
  },

  // ── Borders ───────────────────────────────────────────────
  border: {
    subtle:     '#2C2820',
    moderate:   '#3A342C',
    strong:     '#5A5040',
    focus:      '#7EB3F7',
    table:      '#38322A',
    mathBox:    '#30281E',
  },

  // ── Syntax highlight ─────────────────────────────────────
  syntax: {
    keyword:    '#F08090',
    string:     '#90C890',
    number:     '#E0A060',
    comment:    '#706860',
    function:   '#80B8F0',
    type:       '#C090E0',
    operator:   '#A09880',
  },

  // ── Shadow ────────────────────────────────────────────────
  shadow: {
    card:       '0 2px 8px rgba(0,0,0,0.40)',
    toolbar:    '0 1px 4px rgba(0,0,0,0.30)',
    figure:     '0 3px 12px rgba(0,0,0,0.50)',
  },
};

export type Theme = typeof lightTheme;
```

### Theme Provider

```typescript
// themeProvider.ts
import { lightTheme, darkTheme, type Theme } from './tokens';

type Mode = 'light' | 'dark' | 'system';

export function resolveTheme(mode: Mode): Theme {
  if (mode === 'light') return lightTheme;
  if (mode === 'dark')  return darkTheme;
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  return prefersDark ? darkTheme : lightTheme;
}

// Persist preference
export function saveTheme(mode: Mode) {
  localStorage.setItem('ereader-theme', mode);
}
export function loadTheme(): Mode {
  return (localStorage.getItem('ereader-theme') as Mode) ?? 'system';
}
```

## Typography Scale

| Role         | Size (rem) | Line-height | Weight | Font                  |
|:-------------|:----------:|:-----------:|:------:|:----------------------|
| `display`    | 2.25       | 1.25        | 700    | Merriweather Serif    |
| `h1`         | 1.875      | 1.30        | 700    | Merriweather Serif    |
| `h2`         | 1.50       | 1.35        | 600    | Merriweather Serif    |
| `h3`         | 1.25       | 1.40        | 600    | Merriweather Serif    |
| `h4`         | 1.125      | 1.45        | 600    | Merriweather Serif    |
| `body`       | 1.0625     | 1.75        | 400    | Merriweather Serif    |
| `bodySmall`  | 0.9375     | 1.65        | 400    | Merriweather Serif    |
| `caption`    | 0.8125     | 1.55        | 400    | Inter / System UI     |
| `code`       | 0.875      | 1.60        | 400    | JetBrains Mono        |
| `codeSmall`  | 0.8125     | 1.55        | 400    | JetBrains Mono        |
| `mathInline` | 1.0        | 1.75        | 400    | KaTeX Math (rendered) |
| `mathBlock`  | 1.1        | 1.80        | 400    | KaTeX Math (rendered) |
| `tableCell`  | 0.9375     | 1.55        | 400    | Inter / System UI     |
| `tableHead`  | 0.875      | 1.45        | 600    | Inter / System UI     |
| `ui`         | 0.875      | 1.40        | 500    | Inter / System UI     |
| `uiSmall`    | 0.75       | 1.35        | 500    | Inter / System UI     |

> User-adjustable range: **80 % → 150 %** of base via toolbar font-size
> slider. Pretext `prepare()` is re-invoked on every font-size change
> with the new `font` string; layout cache is invalidated automatically.

## Math Rendering

### Inline Math  `$...$`

Inline math is treated as a **single rich-inline item** inside a pretext
`prepareWithSegments()` call:

```typescript
import katex from 'katex';

// 1. Pre-render to SVG string
const svgString = katex.renderToString(expr, {
  output:       'svg',
  throwOnError: false,
  displayMode:  false,
});

// 2. Load as ImageBitmap for canvas compositing
const blob    = new Blob([svgString], { type: 'image/svg+xml' });
const url     = URL.createObjectURL(blob);
const bitmap  = await createImageBitmap(image);

// 3. Pass as a fixed-width RichInlineItem to pretext
const mathItem: RichInlineItem = {
  type:   'image',
  bitmap,
  width:  measuredWidth,
  height: lineHeightPx,
};
```

### Display Math  `$$...$$`

Display math breaks out of the pretext text stream as a **block box**:

```typescript
// mathRenderer.ts
export async function renderMathBlock(
  expr:     string,
  theme:    Theme,
  maxWidth: number,
): Promise<HTMLCanvasElement> {
  const svgString = katex.renderToString(expr, {
    output:      'svg',
    displayMode: true,
    throwOnError: false,
    macros: {
      '\\R': '\\mathbb{R}',
      '\\N': '\\mathbb{N}',
      '\\Z': '\\mathbb{Z}',
    },
  });

  // Tint SVG to theme text color
  const tinted  = svgString.replace(/currentColor/g, theme.text.math);
  const canvas  = document.createElement('canvas');
  // ... draw to canvas with correct DPR scaling
  return canvas;
}
```

### Math Examples (rendered at runtime)

**Inline:** The energy-mass equivalence $E = mc^2$ is foundational.

**Display — Maxwell's equations:**

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
$$

$$
\nabla \times \mathbf{B} - \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t} = \mu_0 \mathbf{J}
$$

**Display — Euler's identity:**

$$
e^{i\pi} + 1 = 0
$$

**Display — Gaussian integral:**

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

**Display — Matrix:**

$$
\mathbf{A} = \begin{pmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{pmatrix}
$$

**Display — Summation:**

$$
\sum_{k=1}^{n} k = \frac{n(n+1)}{2}
$$

## Tables

### Rendering Pipeline

```typescript
// tableRenderer.ts
import { prepare, layout } from '@chenglou/pretext';

export function measureTable(
  rows:     string[][],
  headers:  string[],
  maxWidth: number,
  tokens:   Theme,
): TableLayout {

  const colCount = headers.length;
  const colW     = Math.floor((maxWidth - (colCount + 1) * 1) / colCount);

  return {
    headers: headers.map(h => ({
      prepared: prepare(h, {
        font:  `600 ${tokens.fontSize.tableHead} ${tokens.font.ui}`,
        width: colW,
      }),
      lines: layout(/* ... */),
    })),
    rows: rows.map(row =>
      row.map(cell => ({
        prepared: prepare(cell, {
          font:  `${tokens.fontSize.tableCell} ${tokens.font.ui}`,
          width: colW,
        }),
        lines: layout(/* ... */),
      }))
    ),
    colWidths:  Array(colCount).fill(colW),
    rowHeights: /* computed from max cell line count */,
  };
}
```

### Example Table — Pretext API Surface

| Function                | Returns          | DOM-free | Notes                                    |
|:------------------------|:-----------------|:--------:|:-----------------------------------------|
| `prepare()`             | `PreparedText`   | ✅        | Horizontal measurement only              |
| `prepareWithSegments()` | `PreparedText`   | ✅        | Rich inline spans (bold, italic, images) |
| `layout()`              | `number`         | ✅        | Returns total height                     |
| `layoutWithLines()`     | `LayoutLine[]`   | ✅        | Per-line geometry                        |
| `layoutNextLineRange()` | `LineRange`      | ✅        | Geometry-first, manual pagination        |
| `materializeLineRange()`| `string[]`       | ✅        | Slice lines for a page                   |
| `measureNaturalWidth()` | `number`         | ✅        | Widest forced line                       |
| `measureLineStats()`    | `LineStats`      | ✅        | Detailed per-line metrics                |
| `setLocale()`           | `void`           | ✅        | Resets segmenter + caches                |

### Example Table — Theme Comparison

| Property       | Light Theme Value  | Dark Theme Value   | Token Name               |
|:---------------|:-------------------|:-------------------|:-------------------------|
| Page BG        | `#FAF8F1`          | `#12100E`          | `surface.page`           |
| Primary text   | `#1A1510`          | `#E8E0D0`          | `text.primary`           |
| Link color     | `#2E5FA3`          | `#7EB3F7`          | `text.link`              |
| Table head BG  | `#E8E4D9`          | `#252220`          | `surface.tableHead`      |
| Border subtle  | `#DDD8CC`          | `#2C2820`          | `border.subtle`          |
| Code BG        | `#F0EDE4`          | `#1E1C18`          | `surface.codeBlock`      |
| Math text      | `#1A1510`          | `#E8E0D0`          | `text.math`              |
| Focus ring     | `#2E5FA3`          | `#7EB3F7`          | `border.focus`           |

## Figures & Media

### Figure Types

```typescript
type FigureKind =
  | 'image'       // raster: JPEG, PNG, WebP, AVIF
  | 'svg'         // vector diagram
  | 'canvas'      // programmatic: charts, plots
  | 'math'        // display-mode KaTeX block
  | 'code'        // syntax-highlighted code block
  | 'table'       // pretext-laid-out data table
  | 'blockquote'  // pull quote
  | 'callout';    // info / warning / tip / danger
```

### Layout box insertion

```
Text line N
──────────────────────────────────────────── ← text ends
┌──────────────────────────────────────────┐
│             Figure / Table / Math        │ ← block box
│  ┌──────────────────────────────────┐   │
│  │        Image / Canvas / SVG      │   │
│  └──────────────────────────────────┘   │
│  Figure 1: Caption text laid out with    │
│  pretext at caption font size            │
└──────────────────────────────────────────┘
Text line N+1 continues here...
────────────────────────────────────────────
```

### Callout / Admonition styles

```
┌─ ℹ️  NOTE ───────────────────────────────┐   ← border-left: 4px; surface.overlay
│  Pretext's prepare() is synchronous and   │
│  allocates no heap after warm-up.         │
└───────────────────────────────────────────┘

┌─ ⚠️  WARNING ────────────────────────────┐
│  system-ui is unsafe for layout accuracy  │
│  on macOS. Use a named font instead.      │
└───────────────────────────────────────────┘

┌─ 💡  TIP ────────────────────────────────┐
│  Call setLocale() before preparing text   │
│  when switching document languages.      │
└───────────────────────────────────────────┘

┌─ 🚨  DANGER ─────────────────────────────┐
│  Never call getBoundingClientRect() in    │
│  the layout hot-path. Use pretext.        │
└───────────────────────────────────────────┘
```

### Callout token colors

| Type      | Light BG    | Dark BG     | Light Border | Dark Border |
|:----------|:------------|:------------|:-------------|:------------|
| `info`    | `#EAF2FF`   | `#0D1E2E`   | `#2E5FA3`    | `#7EB3F7`   |
| `warning` | `#FFF8E6`   | `#211A00`   | `#C07800`    | `#E0B040`   |
| `tip`     | `#EDFAEE`   | `#0B1E0D`   | `#2A8A30`    | `#60C868`   |
| `danger`  | `#FFECEC`   | `#200808`   | `#C02020`    | `#E06060`   |

## Layout Engine

### Page geometry

```
┌────────────────────── viewport ──────────────────────┐
│  marginTop: 56px (toolbar)                           │
│  ┌──────────────────────────────────────────────┐   │
│  │ paddingX: 5vw (min 24px, max 96px)           │   │
│  │ ┌──────────────────────────────────────────┐ │   │
│  │ │  Reading column                          │ │   │
│  │ │  maxWidth: 720px  (optimal ~66 chars)    │ │   │
│  │ │  centered in viewport                   │ │   │
│  │ └──────────────────────────────────────────┘ │   │
│  │ paddingBottom: 80px (progress bar)           │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### Pagination algorithm

```typescript
function paginate(
  blocks:     Block[],
  pageHeight: number,
  colWidth:   number,
  tokens:     Theme,
): Page[] {
  const pages: Page[]  = [];
  let   cursor         = 0;
  let   currentPage: Block[] = [];

  for (const block of blocks) {
    const h = measureBlockHeight(block, colWidth, tokens);

    if (cursor + h > pageHeight && currentPage.length > 0) {
      pages.push({ blocks: currentPage });
      currentPage = [];
      cursor      = 0;
    }

    // Hard page-break: split text blocks across pages
    if (block.type === 'text' && cursor + h > pageHeight) {
      const { top, bottom } = splitTextBlock(
        block, pageHeight - cursor, colWidth, tokens
      );
      currentPage.push(top);
      pages.push({ blocks: currentPage });
      currentPage = bottom ? [bottom] : [];
      cursor      = bottom ? measureBlockHeight(bottom, colWidth, tokens) : 0;
    } else {
      currentPage.push(block);
      cursor += h;
    }
  }

  if (currentPage.length) pages.push({ blocks: currentPage });
  return pages;
}
```

## Component Tree

```
<EReaderApp>
 ├── <ThemeProvider>          ← light / dark / system
 ├── <FontProvider>           ← user font-size preference
 ├── <Toolbar>
 │    ├── <ThemeToggle />      ← ☀︎ / 🌙 / auto
 │    ├── <FontSizePicker />   ← Aa slider
 │    ├── <TableOfContents />  ← chapter drawer
 │    └── <SearchBar />
 ├── <ReaderCanvas>           ← main <canvas> element
 │    ├── renderTextBlock()    ← pretext layout + ctx.fillText
 │    ├── renderMathBlock()    ← KaTeX SVG → ImageBitmap
 │    ├── renderTable()        ← pretext cell layout + grid lines
 │    ├── renderFigure()       ← image + caption
 │    ├── renderCodeBlock()    ← syntax-highlighted, monospace
 │    └── renderCallout()      ← admonition boxes
 └── <ProgressBar>            ← page / scroll position
```

## Token Reference

```typescript
// Full token shape (both themes conform to this interface)
export interface DesignTokens {
  surface: {
    page: string;       overlay: string;    toolbar: string;
    footer: string;     codeBlock: string;  tableHead: string;
    tableRow: string;   tableAlt: string;   blockquote: string;
    mathBlock: string;
  };
  text: {
    primary: string;    secondary: string;  muted: string;
    link: string;       linkHover: string;  code: string;
    math: string;       caption: string;    tableHead: string;
  };
  border: {
    subtle: string;     moderate: string;   strong: string;
    focus: string;      table: string;      mathBox: string;
  };
  syntax: {
    keyword: string;    string: string;     number: string;
    comment: string;    function: string;   type: string;
    operator: string;
  };
  shadow: {
    card: string;       toolbar: string;    figure: string;
  };
  font: {
    serif:  string;   // 'Merriweather, Georgia, serif'
    ui:     string;   // 'Inter, system-ui, sans-serif'
    mono:   string;   // 'JetBrains Mono, Fira Code, monospace'
    math:   string;   // 'KaTeX_Math, serif'
  };
  fontSize: Record<TypographyRole, string>;   // e.g. '1.0625rem'
  lineHeight: Record<TypographyRole, number>; // e.g. 1.75
  space: {
    xs: 4;  sm: 8;  md: 16;  lg: 24;  xl: 40;  '2xl': 64;
  };
  radius: {
    sm: 4;  md: 8;  lg: 12;  pill: 9999;
  };
  transition: {
    fast:   '120ms ease';
    normal: '220ms ease';
    slow:   '380ms ease';
  };
}
```

## Accessibility

| Requirement                    | Implementation                                              |
|:-------------------------------|:------------------------------------------------------------|
| WCAG AA contrast (body text)   | Light `#1A1510` on `#FAF8F1` → **14.4 : 1** ✅             |
| WCAG AA contrast (dark body)   | Dark `#E8E0D0` on `#12100E` → **13.8 : 1** ✅              |
| Focus ring                     | `border.focus` color, `2px` solid, `radius.md` offset       |
| Keyboard navigation            | Arrow keys page-turn; `T` TOC; `F` search; `Esc` close      |
| Screen reader                  | Canvas has ARIA live region; text extracted to hidden DOM    |
| Font size floor                | Never below `13px` regardless of user scale                 |
| Reduced motion                 | `prefers-reduced-motion` disables page-turn animation        |
| High contrast mode             | Detects `forced-colors: active`, switches to system palette  |

## Performance Budget

| Metric                              | Target      | Measured via               |
|:------------------------------------|:------------|:---------------------------|
| First page render (cold)            | < 120 ms    | `performance.now()`        |
| Page turn (pre-paginated)           | < 8 ms      | `requestAnimationFrame`    |
| `prepare()` per paragraph           | < 0.3 ms    | micro-benchmark            |
| `layout()` per paragraph            | < 0.1 ms    | micro-benchmark            |
| Math block render (KaTeX → bitmap)  | < 40 ms     | async, cached              |
| Table layout (50 rows × 8 cols)     | < 12 ms     | micro-benchmark            |
| Heap allocation per page turn       | 0 bytes     | Chrome Memory profiler     |
| Bundle size (`@chenglou/pretext`)   | < 30 kB gz  | `bundlephobia`             |

> Pretext's `prepare()` + `layout()` are the **hot-path zero-allocation
> pair** — no DOM, no reflow, no garbage pressure per frame.

## File Structure

```
ereader/
├── design.md                     ← this document
├── package.json
├── tsconfig.json
├── bun.lockb
├── src/
│   ├── main.ts
│   ├── engine/
│   │   ├── pretextPipeline.ts
│   │   ├── paginator.ts
│   │   ├── mathRenderer.ts
│   │   ├── tableRenderer.ts
│   │   ├── figureRenderer.ts
│   │   └── codeRenderer.ts
│   ├── parser/
│   │   ├── markdownParser.ts
│   │   ├── epubParser.ts
│   │   └── astTypes.ts
│   ├── themes/
│   │   ├── tokens.ts
│   │   ├── lightTheme.ts
│   │   ├── darkTheme.ts
│   │   └── themeProvider.ts
│   ├── components/
│   │   ├── ReaderCanvas.tsx
│   │   ├── Toolbar.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── FontPicker.tsx
│   │   ├── TableOfContents.tsx
│   │   └── SearchBar.tsx
│   └── utils/
│       ├── dpr.ts               ← device pixel ratio helpers
│       ├── color.ts             ← hex ↔ rgba, tinting
│       └── cache.ts             ← LRU for prepared text
├── public/
│   └── fonts/
│       ├── Merriweather-*.woff2
│       ├── Inter-*.woff2
│       └── JetBrainsMono-*.woff2
└── tests/
    ├── layout.test.ts
    ├── paginator.test.ts
    └── math.test.ts
```

---

*E-Reader Design Specification v3 · Stack:
[`@chenglou/pretext`](https://github.com/chenglou/pretext) · MIT License*
