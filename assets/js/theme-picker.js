/* ==========================================================================
   DFT Notes — theme picker (design.md v2.0)
   --------------------------------------------------------------------------
   Reads the saved theme/mode from localStorage (or falls back to the
   defaults from design.md), writes data-theme + data-mode onto <html>,
   and persists future choices.

   Dispatches a 'dft-theme-changed' CustomEvent on document so other
   scripts (notably assets/js/text-layout.js, the pretext integration)
   can re-measure text after a theme switch.

   No dependencies, ~80 lines, no-build, no-framework.
   ========================================================================== */

(function () {
  'use strict';

  var ROOT     = document.documentElement;
  var STORAGE  = window.localStorage;
  var KEY_T    = 'er-theme';
  var KEY_M    = 'er-mode';
  var DEFAULT  = { theme: 'parchment', mode: 'auto' };

  var THEMES = [
    'parchment',
    'coffee-green',
    'obsidian',
    'midnight',
    'rose-dusk',
    'terminal-amber'
  ];
  var MODES = ['light', 'dark', 'auto'];

  function applyTheme(theme, mode) {
    var safeTheme = THEMES.indexOf(theme) === -1 ? DEFAULT.theme : theme;
    var safeMode  = MODES.indexOf(mode)    === -1 ? DEFAULT.mode  : mode;

    var resolvedMode = safeMode === 'auto'
      ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : safeMode;

    ROOT.setAttribute('data-theme', safeTheme);
    ROOT.setAttribute('data-mode',  resolvedMode);
    // Stash the *user* choice (not the resolved one) so re-runs of
    // applyTheme with the same args are idempotent.
    ROOT.dataset.userTheme = safeTheme;
    ROOT.dataset.userMode  = safeMode;

    // Reflect active state in the picker buttons.
    syncActiveStates(safeTheme, safeMode);
  }

  function syncActiveStates(theme, mode) {
    var i, btn;
    var swatches = document.querySelectorAll('[data-pick-theme]');
    for (i = 0; i < swatches.length; i++) {
      btn = swatches[i];
      btn.classList.toggle('is-active', btn.dataset.pickTheme === theme);
    }
    var modes = document.querySelectorAll('[data-pick-mode]');
    for (i = 0; i < modes.length; i++) {
      btn = modes[i];
      btn.classList.toggle('is-active', btn.dataset.pickMode === mode);
    }
  }

  // Boot: restore from localStorage, or apply defaults.
  function boot() {
    var savedTheme = STORAGE.getItem(KEY_T) || DEFAULT.theme;
    var savedMode  = STORAGE.getItem(KEY_M) || DEFAULT.mode;
    applyTheme(savedTheme, savedMode);
  }

  // Click delegation for picker buttons.
  function onClick(e) {
    var t = e.target.closest('[data-pick-theme]');
    var m = e.target.closest('[data-pick-mode]');
    if (!t && !m) return;

    var currentTheme = ROOT.dataset.userTheme || DEFAULT.theme;
    var currentMode  = ROOT.dataset.userMode  || DEFAULT.mode;

    if (t) {
      var newTheme = t.dataset.pickTheme;
      if (newTheme !== currentTheme) {
        STORAGE.setItem(KEY_T, newTheme);
        applyTheme(newTheme, currentMode);
        document.dispatchEvent(new CustomEvent('dft-theme-changed', {
          detail: { theme: newTheme, mode: currentMode, source: 'user' }
        }));
      }
    }
    if (m) {
      var newMode = m.dataset.pickMode;
      if (newMode !== currentMode) {
        STORAGE.setItem(KEY_M, newMode);
        applyTheme(currentTheme, newMode);
        document.dispatchEvent(new CustomEvent('dft-theme-changed', {
          detail: { theme: currentTheme, mode: newMode, source: 'user' }
        }));
      }
    }
  }

  // OS preference change while in 'auto' mode.
  function onOsPrefChange() {
    var mode = STORAGE.getItem(KEY_M) || DEFAULT.mode;
    if (mode === 'auto') {
      var theme = STORAGE.getItem(KEY_T) || DEFAULT.theme;
      applyTheme(theme, 'auto');
      document.dispatchEvent(new CustomEvent('dft-theme-changed', {
        detail: { theme: theme, mode: 'auto', source: 'os' }
      }));
    }
  }

  // Set up listeners.
  function init() {
    boot();
    document.addEventListener('click', onClick);
    var mq = window.matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) {
      mq.addEventListener('change', onOsPrefChange);
    } else if (mq.addListener) {
      // Safari < 14
      mq.addListener(onOsPrefChange);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
