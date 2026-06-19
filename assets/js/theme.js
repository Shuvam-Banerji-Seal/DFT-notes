/* =============================================================
 * DFT Notes — theme.js
 * Toggles the `data-theme` attribute on <html> between
 * `light` and `dark`, and persists the choice in localStorage.
 *
 * The initial value is set by an inline script in
 * _includes/head.html BEFORE the CSS loads, so there is no flash
 * of the wrong theme on first paint.  This file handles the
 * interactive part (the toggle button in the top nav).
 *
 * The button shows a sun when the active theme is dark (so the
 * user knows clicking it will go to light) and a moon when the
 * active theme is light (clicking it will go to dark).  The
 * swap is done purely via CSS, not by re-rendering the SVG.
 * =========================================================== */
(function () {
  "use strict";

  var STORAGE_KEY = "dft-notes:theme";

  function readStored() {
    try { return localStorage.getItem(STORAGE_KEY); }
    catch (e) { return null; }
  }

  function writeStored(theme) {
    try { localStorage.setItem(STORAGE_KEY, theme); }
    catch (e) { /* localStorage unavailable — the preference
                   will revert on next page load */ }
  }

  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") || "light";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    writeStored(theme);
    // Re-initialise Mermaid so its theme tracks the new palette.
    if (window.__dftReinitMermaid) {
      try { window.__dftReinitMermaid(); } catch (e) {}
    }
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var btns = document.querySelectorAll("[data-theme-toggle]");
    if (!btns.length) return;

    // Update the aria-label on every theme toggle so the buttons
    // announce which way they will switch.  "Switch to dark" if
    // the current is light, etc.
    function syncLabels() {
      var t = currentTheme();
      btns.forEach(function (btn) {
        btn.setAttribute(
          "aria-label",
          t === "dark" ? "Switch to light theme" : "Switch to dark theme"
        );
      });
    }
    syncLabels();

    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var next = currentTheme() === "dark" ? "light" : "dark";
        applyTheme(next);
        syncLabels();
      });
    });

    // If the OS preference changes (e.g. user toggled the system
    // dark mode) AND the user has not explicitly chosen, follow
    // the OS.  We detect an explicit choice by the presence of
    // the storage key.
    if (!window.matchMedia) return;
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function (e) {
      if (readStored()) return; // explicit user choice wins
      applyTheme(e.matches ? "dark" : "light");
      syncLabels();
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange); // older Safari
  });
})();
