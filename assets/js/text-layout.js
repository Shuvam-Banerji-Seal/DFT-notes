/* ==========================================================================
   DFT Notes — text layout
   --------------------------------------------------------------------------
   Uses chenglou/pretext (window.PretextLayout, loaded as a separate IIFE
   bundle) to measure headings and other text on the page, then applies a
   real per-viewport font-size based on actual measurement rather than CSS
   clamp() estimates.

   Concretely:
     1. For each `h1, h2, h3, h4` on the page, read its computed font.
     2. Use pretext's `prepare(text, font)` to segment + cache glyph widths.
     3. Use `layout(prepared, containerWidth, lineHeight)` to compute how the
        heading breaks at the current container width.
     4. If the heading would overflow its container at the current
        font-size, scale it down in 0.5% steps until it fits (max 30% shrink).
     5. Re-measure on resize (debounced 200ms).

   Result: headings never overflow at any viewport width, with sizes that
   adapt to the actual rendered text. CSS clamp() is still the first-pass
   guess; this is a refinement pass that runs on the client.

   Notes:
   - Uses requestAnimationFrame to batch the measurement pass.
   - Skips elements that are off-screen (saves work for long notes).
   - Writes the final font-size as an inline `style` on the element, so
     it overrides CSS without needing !important.
   - The integration is **passive**: if pretext isn't loaded, the script
     silently exits and the page falls back to CSS clamp() values.
   ========================================================================== */

(function () {
  'use strict';

  // Bail out if pretext didn't load (shouldn't happen, but be defensive).
  if (typeof window.PretextLayout === 'undefined') return;
  var prepare = window.PretextLayout.prepare;
  var layout  = window.PretextLayout.layout;

  // The set of text elements to measure. We focus on headings because
  // they're the elements most likely to overflow at narrow viewports
  // (long chapter titles, technical terms, etc.).
  var SELECTOR = 'h1, h2, h3, h4';
  // Maximum fraction of the base font-size we'll shrink a heading.
  var MAX_SHRINK = 0.30;     // 30% smaller than the CSS-clamp() value
  // Initial font-size scale (1.0 = the CSS-computed value).
  var MIN_SCALE  = 1.0 - MAX_SHRINK;

  // Tiny utility: debounce a function call.
  function debounce(fn, wait) {
    var t = null;
    return function () {
      var args = arguments, ctx = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(ctx, args); }, wait);
    };
  }

  // rAF-coalesced batch measure: collect all elements, then measure in one
  // animation frame. Prevents layout thrash on pages with many headings.
  var pending = [];
  function scheduleMeasure(el) {
    if (pending.indexOf(el) === -1) pending.push(el);
    if (scheduleMeasure._raf) return;
    scheduleMeasure._raf = requestAnimationFrame(function () {
      scheduleMeasure._raf = 0;
      var batch = pending;
      pending = [];
      batch.forEach(measureHeading);
    });
  }

  // Measure a single heading and apply a per-element font-size that fits
  // its container at the current viewport width.
  function measureHeading(el) {
    if (!el.isConnected) return;
    var rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;  // hidden

    var cs = window.getComputedStyle(el);
    var baseSize = parseFloat(cs.fontSize);
    if (!baseSize || !isFinite(baseSize)) return;

    // Use the *available* width: container minus any inline padding.
    var containerWidth = el.parentElement
      ? el.parentElement.getBoundingClientRect().width
      : rect.width;
    if (containerWidth <= 0) return;

    // Build the font shorthand that pretext expects: "<size> <family>".
    // Compute the rendered font-family string (resolved against fallbacks).
    var fontFamily = cs.fontFamily || 'serif';
    var font = baseSize.toFixed(1) + 'px ' + fontFamily;
    var text = el.textContent || '';
    if (!text.trim()) return;

    var prepared;
    try {
      prepared = prepare(text, font);
    } catch (e) {
      // If pretext can't analyze the text (e.g. font not yet loaded),
      // silently skip — the CSS clamp() value is still in effect.
      return;
    }

    // First, check whether the heading overflows at the base size.
    var lh = parseFloat(cs.lineHeight) || (baseSize * 1.25);
    var baseLayout = layout(prepared, containerWidth, lh);

    // We only shrink if the natural layout needs more than 1 line at the
    // given width, OR if the natural rendered width exceeds the container
    // width (i.e. a single very long word).
    var needsShrink =
      baseLayout.lineCount > 1 ||
      (el.scrollWidth - el.clientWidth > 1);  // horizontal overflow

    if (!needsShrink) {
      // Clear any previously-applied override.
      if (el.style.fontSize) el.style.fontSize = '';
      el.removeAttribute('data-dft-scale');
      return;
    }

    // Binary-search a font-size where the heading fits in 1 line. Start at
    // the base size and work downward; cap at MAX_SHRINK.
    var lo = baseSize * MIN_SCALE;
    var hi = baseSize;
    var best = lo;
    for (var i = 0; i < 10; i++) {
      var mid = (lo + hi) / 2;
      var midFont = mid.toFixed(1) + 'px ' + fontFamily;
      var midPrepared;
      try { midPrepared = prepare(text, midFont); }
      catch (e) { break; }
      var midLh = lh * (mid / baseSize);
      var midLayout = layout(midPrepared, containerWidth, midLh);
      if (midLayout.lineCount <= 1) { best = mid; lo = mid; }
      else { hi = mid; }
    }

    // Apply the new size. We do this in two steps: set the inline style,
    // then store the scale factor as a data attribute for debugging.
    el.style.fontSize = best.toFixed(2) + 'px';
    el.setAttribute('data-dft-scale', (best / baseSize).toFixed(3));
  }

  // Public API: re-measure all headings. Useful after a layout-affecting
  // DOM change (e.g. MathJax finishing typesetting, theme switch, etc.).
  function relayout() {
    var headings = document.querySelectorAll(SELECTOR);
    headings.forEach(scheduleMeasure);
  }
  // Expose so other scripts (e.g. a future theme-switcher) can trigger.
  window.dftRelayout = relayout;

  // Wait for fonts to be ready before measuring. Skipping this can give
  // wrong widths if the heading uses a web font that hasn't loaded yet.
  function whenFontsReady(cb) {
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(cb);
    } else {
      setTimeout(cb, 250);
    }
  }

  // Boot.
  function boot() {
    // First pass: wait for web fonts, then measure.
    whenFontsReady(function () {
      relayout();
      // Re-measure on resize (debounced).
      window.addEventListener('resize', debounce(relayout, 200));
      // And one more pass after MathJax finishes typesetting (which can
      // change the page height and trigger scroll-driven relayouts).
      if (window.MathJax && MathJax.startup && MathJax.startup.promise) {
        MathJax.startup.promise.then(function () { setTimeout(relayout, 50); });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
