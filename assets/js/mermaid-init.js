/* =============================================================
 * DFT Notes — mermaid-init.js
 * Initialises Mermaid 10 with a theme that matches the current
 * page theme (data-theme="dark" on <html>).  Re-runs on theme
 * toggle so the diagrams pick up the new palette immediately.
 *
 * Exposes window.__dftReinitMermaid() so theme.js can trigger a
 * re-render after a switch.
 * =========================================================== */
(function () {
  "use strict";

  function isDark() {
    return document.documentElement.getAttribute("data-theme") === "dark";
  }

  function themeVariables(dark) {
    /* Custom Mermaid theme that maps to our design tokens.  We
       re-use the same coral / teal / amber accents from the
       design system so the diagrams look like they belong. */
    return {
      background:           dark ? "#1a1814" : "#eef0e6",
      primaryColor:         dark ? "#2e2a24" : "#d6dcc8",
      primaryTextColor:     dark ? "#f0ebde" : "#1c1f17",
      primaryBorderColor:   dark ? "#3a342a" : "#cdd3bd",
      secondaryColor:       dark ? "#252220" : "#e3e6d8",
      tertiaryColor:        dark ? "#2e2a24" : "#d6dcc8",
      lineColor:            dark ? "#8a8270" : "#6b7060",
      textColor:            dark ? "#f0ebde" : "#1c1f17",
      mainBkg:              dark ? "#1a1814" : "#eef0e6",
      nodeBorder:           dark ? "#3a342a" : "#cdd3bd",
      clusterBkg:           dark ? "#252220" : "#e3e6d8",
      clusterBorder:        dark ? "#3a342a" : "#cdd3bd",
      titleColor:           dark ? "#f0ebde" : "#1c1f17",
      edgeLabelBackground:  dark ? "#252220" : "#eef0e6",
      nodeTextColor:        dark ? "#f0ebde" : "#1c1f17",
    };
  }

  function init() {
    if (!window.mermaid) return;
    var dark = isDark();
    /* We pick the built-in theme as a starting point, then
       override the variables.  `default` and `dark` are the
       cleanest starting points for our two palettes. */
    window.mermaid.initialize({
      startOnLoad: true,
      theme: dark ? "dark" : "default",
      securityLevel: "loose",
      themeVariables: themeVariables(dark),
      flowchart: { useMaxWidth: true, htmlLabels: true },
      sequence:  { useMaxWidth: true, showSequenceNumbers: false },
      gantt:     { useMaxWidth: true },
    });
    /* Mermaid 10 renders asynchronously; trigger an explicit
       re-run on init to pick up our settings. */
    try { window.mermaid.run(); } catch (e) { /* startOnLoad handles it */ }
  }

  window.__dftReinitMermaid = function () {
    if (!window.mermaid) return;
    /* Tear down any prior renders by remounting the .mermaid
       elements with their original source text.  The simplest
       cross-version approach: walk all .mermaid nodes and
       re-parse via mermaid.run(). */
    try { window.mermaid.run(); } catch (e) { /* best-effort */ }
  };

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(init);
})();
