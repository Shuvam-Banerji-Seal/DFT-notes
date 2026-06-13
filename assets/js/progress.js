/* ==========================================================================
   DFT Notes — reading progress bar (design.md v2.0)
   --------------------------------------------------------------------------
   2px fixed bar at the top of the viewport, filled with --er-accent,
   that tracks scroll position. Driven by a tiny scroll/resize listener
   (rAF-throttled) and an IntersectionObserver-based early bail-out for
   very short pages (where the bar is always 100% and pointless).
   ========================================================================== */

(function () {
  'use strict';

  function init() {
    var bar = document.getElementById('er-progress');
    if (!bar) return;

    var ticking = false;
    function update() {
      ticking = false;
      var doc = document.documentElement;
      var scrollable = doc.scrollHeight - doc.clientHeight;
      var pct = scrollable > 0
        ? Math.min(100, Math.max(0, (doc.scrollTop / scrollable) * 100))
        : 0;
      bar.style.width = pct + '%';
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }

    // Hide the bar entirely on pages that don't scroll.
    function checkVisibility() {
      var doc = document.documentElement;
      if (doc.scrollHeight <= doc.clientHeight + 4) {
        bar.style.display = 'none';
      } else {
        bar.style.display = '';
      }
    }

    window.addEventListener('scroll',  onScroll, { passive: true });
    window.addEventListener('resize',  onScroll, { passive: true });
    // Re-check after MathJax finishes typesetting (page height changes).
    if (window.MathJax && MathJax.startup && MathJax.startup.promise) {
      MathJax.startup.promise.then(function () {
        checkVisibility();
        update();
      });
    }
    // And re-check after pretext relayout (font-size changes can shift
    // heading heights and thus page height).
    document.addEventListener('dft-relayout', function () {
      setTimeout(function () { checkVisibility(); update(); }, 50);
    });

    checkVisibility();
    update();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
