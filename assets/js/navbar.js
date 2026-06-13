/* ==========================================================================
   DFT Notes — navbar behaviour
   --------------------------------------------------------------------------
   Toggles the .er-navbar's data-open attribute when the hamburger is
   pressed, and auto-closes the panel on:
     - clicking a nav link
     - Escape
     - an outside click
     - resize back to desktop (so the panel doesn't get stuck open)
   Keeps aria-expanded in sync.
   No dependencies.
   ========================================================================== */

(function () {
  'use strict';

  function init() {
    var nav = document.querySelector('.er-navbar');
    var toggle = document.querySelector('.er-navbar-toggle');
    if (!nav || !toggle) return;

    function setOpen(open) {
      nav.dataset.open = String(open);
      toggle.setAttribute('aria-expanded', String(open));
    }

    function isOpen() {
      return nav.dataset.open === 'true';
    }

    // Toggle on click. stopPropagation so the document-level
    // outside-click handler doesn't immediately close it.
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(!isOpen());
    });

    // Close when a nav link is clicked (mobile UX).
    var links = nav.querySelectorAll('.er-navbar-link');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function () {
        if (isOpen()) setOpen(false);
      });
    }

    // Escape closes and returns focus to the toggle.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Outside click closes.
    document.addEventListener('click', function (e) {
      if (isOpen() && !nav.contains(e.target)) {
        setOpen(false);
      }
    });

    // Resize back to desktop auto-closes the panel.
    var mq = window.matchMedia('(min-width: 720px)');
    var onMqChange = function (e) {
      if (e.matches && isOpen()) setOpen(false);
    };
    if (mq.addEventListener) mq.addEventListener('change', onMqChange);
    else if (mq.addListener)   mq.addListener(onMqChange);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
