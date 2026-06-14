/* =============================================================
 * DFT Notes — nav.js
 * Mobile menu open/close.  Vanilla JS, no framework.
 *
 *   1. Hamburger toggles the .mobile-menu sheet.
 *   2. Close button inside the sheet closes it.
 *   3. Clicking any link inside the sheet closes it.
 *   4. Pressing Escape closes it.
 *   5. Body gets .nav-open while the menu is open (CSS prevents
 *      background scroll).
 *
 *   Selectors used (all set in _includes/nav.html):
 *     - [data-nav-toggle]      the hamburger button
 *     - [data-nav-close]       the X button inside the mobile sheet
 *     - [data-mobile-menu]     the sheet itself
 *     - [data-nav-link]        any link inside the sheet
 * =========================================================== */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var toggle = document.querySelector("[data-nav-toggle]");
    var close  = document.querySelector("[data-nav-close]");
    var menu   = document.querySelector("[data-mobile-menu]");
    if (!toggle || !menu) return;

    function open() {
      menu.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close menu");
      document.body.classList.add("nav-open");
      // Focus the close button so keyboard users can dismiss.
      if (close) window.requestAnimationFrame(function () { close.focus(); });
    }

    function closeMenu() {
      menu.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
      document.body.classList.remove("nav-open");
      // Return focus to the hamburger.
      toggle.focus();
    }

    function isOpen() {
      return !menu.hidden;
    }

    toggle.addEventListener("click", function () {
      if (isOpen()) closeMenu();
      else open();
    });

    if (close) {
      close.addEventListener("click", closeMenu);
    }

    // Clicking a link in the sheet navigates and closes.
    menu.querySelectorAll("[data-nav-link]").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });

    // Escape closes.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen()) {
        e.preventDefault();
        closeMenu();
      }
    });
  });
})();
