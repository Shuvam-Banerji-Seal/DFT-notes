/* =============================================================
 * DFT Notes — nav.js
 * Mobile drawer open/close + theme label sync.  Vanilla JS,
 * no framework.
 *
 *   Drawer architecture (rewritten 2026-06):
 *     - [data-nav-toggle]      the hamburger button (top nav)
 *     - [data-nav-close]       the X button inside the drawer header
 *     - [data-mobile-menu]     the right-side <aside> drawer
 *     - [data-mobile-backdrop] the full-viewport overlay behind
 *                              the drawer; click-to-dismiss
 *     - [data-nav-link]        any link inside the drawer
 *                              (auto-closes on tap)
 *     - [data-theme-toggle]    the theme switcher (top nav + drawer)
 *     - [data-theme-label]     the drawer's text label that mirrors
 *                              the active theme ("Light" / "Dark")
 *
 *   Animations:
 *     - Drawer slides in from the right (~280ms ease-out)
 *     - Backdrop fades in (~200ms ease-out)
 *     - Both reverse on close
 *
 *   Body scroll lock:
 *     - Body gets `data-mobile-open="true"` while open
 *     - CSS uses [data-mobile-open] to lock scroll and shift
 *       the page (when room) so the user can still see context
 *
 *   Focus management:
 *     - On open, focus the close button (keyboard users can dismiss)
 *     - On close, return focus to the hamburger
 *     - Escape closes
 *     - Click on backdrop closes
 * =========================================================== */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var toggle   = document.querySelector("[data-nav-toggle]");
    var closeBtn = document.querySelector("[data-nav-close]");
    var menu     = document.querySelector("[data-mobile-menu]");
    var backdrop = document.querySelector("[data-mobile-backdrop]");
    if (!toggle || !menu) return;

    // ------- open / close -------

    function open() {
      // Unhide both first so CSS transitions can run.
      menu.hidden = false;
      if (backdrop) backdrop.hidden = false;
      // Force a reflow before adding the open class so the
      // slide-in animation actually plays (otherwise the browser
      // may coalesce the two style changes).
      // eslint-disable-next-line no-unused-expressions
      menu.offsetWidth;
      menu.classList.add("mobile-drawer--open");
      if (backdrop) backdrop.classList.add("mobile-backdrop--visible");
      document.documentElement.setAttribute("data-mobile-open", "true");
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close menu");
      // Focus the close button so keyboard users can dismiss.
      if (closeBtn) {
        window.requestAnimationFrame(function () { closeBtn.focus(); });
      }
    }

    function closeMenu() {
      menu.classList.remove("mobile-drawer--open");
      if (backdrop) backdrop.classList.remove("mobile-backdrop--visible");
      document.documentElement.removeAttribute("data-mobile-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
      // Hide after the animation completes (matches CSS duration).
      var onEnd = function () {
        // Only hide if still in the closing state (not reopened).
        if (!menu.classList.contains("mobile-drawer--open")) {
          menu.hidden = true;
          if (backdrop) backdrop.hidden = true;
        }
        menu.removeEventListener("transitionend", onEnd);
      };
      menu.addEventListener("transitionend", onEnd);
      // Return focus to the hamburger.
      toggle.focus();
    }

    function isOpen() {
      return menu.classList.contains("mobile-drawer--open");
    }

    toggle.addEventListener("click", function () {
      if (isOpen()) closeMenu();
      else open();
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", closeMenu);
    }

    // Backdrop click-to-dismiss.
    if (backdrop) {
      backdrop.addEventListener("click", closeMenu);
    }

    // Clicking a link in the drawer navigates and closes.
    menu.querySelectorAll("[data-nav-link]").forEach(function (a) {
      a.addEventListener("click", function () {
        // Defer the close slightly so navigation starts cleanly
        // — if the link is to the current page, the close still
        // runs and there's no flash.
        window.setTimeout(closeMenu, 0);
      });
    });

    // Escape closes.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen()) {
        e.preventDefault();
        closeMenu();
      }
    });

    // ------- theme label sync (drawer only — top nav has no label) -------

    function syncThemeLabels() {
      var t = document.documentElement.getAttribute("data-theme") || "light";
      document.querySelectorAll("[data-theme-label]").forEach(function (el) {
        el.textContent = t === "dark" ? "Dark" : "Light";
      });
    }
    syncThemeLabels();

    // Watch the data-theme attribute for changes (set by theme.js).
    var observer = new MutationObserver(syncThemeLabels);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"]
    });
  });
})();
