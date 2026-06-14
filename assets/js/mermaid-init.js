/* =============================================================
 * DFT Notes — mermaid-init.js
 * Renders the ```` ```mermaid ```` fences inside chapters and
 * the chapters map, then attaches a "Download PNG" button to
 * every rendered diagram.
 *
 * Kramdown-GFM emits each mermaid fence as
 *   <pre><code class="language-mermaid">…</code></pre>
 * Mermaid 10 wants `class="mermaid"` on an element whose text
 * content is the diagram source.  We copy the `mermaid` class
 * onto the inner <code> (the source-bearing element), then call
 * `mermaid.run({ querySelector: "code.mermaid" })` to render
 * the SVGs in place.  We also tag the parent <pre> defensively
 * so the diagrams look like code blocks while they are still
 * unrendered.
 *
 * Theme switching (`data-theme` on <html>):
 *   `theme.js` re-runs this script on every toggle, so each
 *   diagram is re-rendered with the new palette and the
 *   download button re-injected.
 *
 * PNG download:
 *   Serialise the rendered <svg> with XMLSerializer, wrap it in
 *   a Blob, load it through an <img>, rasterise onto a <canvas>
 *   (with the page background painted behind for legibility),
 *   then save the canvas as a PNG.  Everything happens client
 *   side; the SVG never leaves the browser.
 * =========================================================== */
(function () {
  "use strict";

  /* --- helpers ------------------------------------------------ */

  function isDark() {
    return (
      document.documentElement.getAttribute("data-theme") === "dark"
    );
  }

  function readVar(name) {
    return getComputedStyle(document.documentElement)
      .getPropertyValue(name)
      .trim();
  }

  function themeVariables(dark) {
    /* Map our design tokens to Mermaid theme variables so the
       diagrams pick up the same palette as the rest of the page.
       We read the live CSS custom properties at render-time so
       a future palette swap is a single-line change in site.css. */
    return {
      background:           readVar("--color-canvas")     || (dark ? "#1a1814" : "#eef0e6"),
      primaryColor:         readVar("--color-card")       || (dark ? "#2e2a24" : "#d6dcc8"),
      primaryTextColor:     readVar("--color-ink")        || (dark ? "#f0ebde" : "#1c1f17"),
      primaryBorderColor:   readVar("--color-border")     || (dark ? "#3a342a" : "#cdd3bd"),
      secondaryColor:       readVar("--color-muted-bg")   || (dark ? "#252220" : "#e3e6d8"),
      tertiaryColor:        readVar("--color-card")       || (dark ? "#2e2a24" : "#d6dcc8"),
      lineColor:            readVar("--color-muted-ink")  || (dark ? "#8a8270" : "#6b7060"),
      textColor:            readVar("--color-ink")        || (dark ? "#f0ebde" : "#1c1f17"),
      mainBkg:              readVar("--color-canvas")     || (dark ? "#1a1814" : "#eef0e6"),
      nodeBorder:           readVar("--color-border")     || (dark ? "#3a342a" : "#cdd3bd"),
      clusterBkg:           readVar("--color-muted-bg")   || (dark ? "#252220" : "#e3e6d8"),
      clusterBorder:        readVar("--color-border")     || (dark ? "#3a342a" : "#cdd3bd"),
      titleColor:           readVar("--color-ink")        || (dark ? "#f0ebde" : "#1c1f17"),
      edgeLabelBackground:  readVar("--color-card")       || (dark ? "#252220" : "#eef0e6"),
      nodeTextColor:        readVar("--color-ink")        || (dark ? "#f0ebde" : "#1c1f17"),
    };
  }

  function tagDiagrams() {
    /* Kramdown-GFM:
         <pre><code class="language-mermaid">…source…</code></pre>
       We want Mermaid to find an element with `class="mermaid"`
       whose text content is the source.  The inner <code> is the
       natural target.  We also tag the parent <pre> so the un-
       rendered block has a tell-tale CSS hook. */
    var tagged = 0;
    document
      .querySelectorAll("pre > code.language-mermaid")
      .forEach(function (code) {
        code.classList.add("mermaid");
        tagged++;
        var pre = code.parentNode;
        if (pre && pre.tagName === "PRE") pre.classList.add("dft-mermaid-pre");
      });
    /* Some pages may already have `class="mermaid"` (e.g. a hand-
       written chapter).  Catch them too. */
    document
      .querySelectorAll("pre.mermaid:not(.dft-mermaid-pre)")
      .forEach(function (pre) {
        pre.classList.add("dft-mermaid-pre");
        tagged++;
      });
    return tagged;
  }

  function sourceText(el) {
    /* The original Mermaid source.  Once Mermaid renders, the
       element's textContent is gone (replaced by the <svg>), so
       we capture it on a `data-source` attribute *before* we
       render.  This is what we feed to the PNG download. */
    if (el.dataset && typeof el.dataset.dftSource === "string") {
      return el.dataset.dftSource;
    }
    return el.textContent || "";
  }

  function captureSources() {
    document
      .querySelectorAll("code.mermaid, pre.mermaid")
      .forEach(function (el) {
        if (el.dataset && typeof el.dataset.dftSource !== "string") {
          el.dataset.dftSource = el.textContent || "";
        }
      });
  }

  /* --- render ------------------------------------------------- */

  async function render() {
    if (!window.mermaid) {
      console.warn("[dft-notes] mermaid.min.js did not load; diagrams will not render.");
      return;
    }
    tagDiagrams();
    captureSources();
    var dark = isDark();
    /* `startOnLoad: false` because we render explicitly below.
       Mermaid 10's `run({ querySelector })` returns a promise
       that resolves once every selected element is rendered. */
    try {
      window.mermaid.initialize({
        startOnLoad: false,
        theme: dark ? "dark" : "default",
        securityLevel: "loose",
        themeVariables: themeVariables(dark),
        flowchart: { useMaxWidth: true, htmlLabels: true, curve: "basis" },
        sequence:  { useMaxWidth: true, showSequenceNumbers: false },
        gantt:     { useMaxWidth: true },
        fontFamily: 'Inter, "Helvetica Neue", system-ui, sans-serif',
      });
    } catch (e) {
      console.error("[dft-notes] mermaid.initialize failed:", e);
      return;
    }
    try {
      await window.mermaid.run({ querySelector: "code.mermaid, pre.mermaid" });
    } catch (e) {
      console.error("[dft-notes] mermaid.run failed:", e);
      return;
    }
    injectDownloadButtons();
  }

  /* --- PNG download ------------------------------------------- */

  function injectDownloadButtons() {
    document
      .querySelectorAll("code.mermaid svg, pre.mermaid svg")
      .forEach(function (svg) {
        /* Mermaid renders the <svg> inside the .mermaid element.
           The parent may be either <code> or <pre> depending on
           what the page had.  We attach the button to a wrapper
           so it lives next to the diagram, not inside it. */
        var host = svg.parentNode;
        if (!host || host.dataset.dftPngReady === "1") return;
        host.dataset.dftPngReady = "1";
        var wrap = document.createElement("figure");
        wrap.className = "dft-mermaid-figure";
        host.parentNode.insertBefore(wrap, host);
        wrap.appendChild(host);
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "dft-mermaid-download";
        btn.setAttribute("aria-label", "Download this diagram as a PNG");
        btn.innerHTML =
          '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">' +
          '<path fill="currentColor" d="M8 1.5a.75.75 0 0 1 .75.75v6.69l1.97-1.97a.75.75 0 1 1 1.06 1.06l-3.25 3.25a.75.75 0 0 1-1.06 0L4.22 8.03a.75.75 0 0 1 1.06-1.06l1.97 1.97V2.25A.75.75 0 0 1 8 1.5Z" />' +
          '<path fill="currentColor" d="M2.75 12a.75.75 0 0 0-1.5 0v1.5A1.5 1.5 0 0 0 2.75 15h10.5a1.5 1.5 0 0 0 1.5-1.5V12a.75.75 0 0 0-1.5 0v1.5H2.75V12Z" />' +
          "</svg>" +
          '<span>Download PNG</span>';
        btn.addEventListener("click", function (event) {
          event.preventDefault();
          downloadPng(svg, wrap);
        });
        wrap.appendChild(btn);
      });
  }

  function downloadPng(svg, wrap) {
    /* Inline the source we captured *before* Mermaid replaced
       textContent.  Build a clean, self-contained <svg> with
       explicit width/height, an XML declaration, and the
       xmlns attribute, so the browser can rasterise it through
       an <img>. */
    var clone = svg.cloneNode(true);
    var bbox = svg.getBoundingClientRect();
    var widthAttr = svg.getAttribute("width");
    var heightAttr = svg.getAttribute("height");
    var width = parseFloat(widthAttr) || bbox.width || 800;
    var height = parseFloat(heightAttr) || bbox.height || 600;
    if (!clone.getAttribute("xmlns")) {
      clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    }
    if (!clone.getAttribute("xmlns:xlink")) {
      clone.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
    }
    clone.setAttribute("width", width);
    clone.setAttribute("height", height);
    /* Strip taint sources before rasterising.  Mermaid's rendered
       SVG includes three things that taint a canvas:
         (1) <a xlink:href="javascript:void(0)"> wrappers around
             clickable nodes — these are Mermaid's click-to-navigate
             feature.  The PNG doesn't need them, so we unwrap the
             children and discard the anchor.
         (2) <foreignObject>…</foreignObject> blocks used for HTML
             labels — these taint because they may contain scripts
             or other restricted content.  We replace them with a
             simple <text> placeholder.
         (3) Inline event handlers (onclick, etc.) — none in the
             current Mermaid output, but we strip them defensively.
       Internal `url(#marker-id)` references (Mermaid's own marker
       arrows) are safe and kept. */
    var anchors = clone.querySelectorAll("a");
    anchors.forEach(function (a) {
      while (a.firstChild) a.parentNode.insertBefore(a.firstChild, a);
      a.parentNode.removeChild(a);
    });
    /* `xlink:href` and `href` cannot be used as CSS attribute
       selectors because of the colon; iterate attributes
       directly. */
    function stripHrefs(root) {
      var elements = root.querySelectorAll("*");
      elements.forEach(function (el) {
        if (el.getAttribute("xlink:href")) el.removeAttribute("xlink:href");
        if (el.getAttribute("href")) el.removeAttribute("href");
      });
    }
    stripHrefs(clone);
    var fo = clone.querySelectorAll("foreignObject");
    fo.forEach(function (f) {
      var t = document.createElementNS("http://www.w3.org/2000/svg", "text");
      t.setAttribute("x", "0");
      t.setAttribute("y", "0");
      t.textContent = "";
      f.parentNode.replaceChild(t, f);
    });
    /* Walk all elements and strip inline event handlers (Mermaid
       does not currently emit any, but be defensive). */
    var allEls = clone.querySelectorAll("*");
    allEls.forEach(function (el) {
      for (var aIdx = 0; aIdx < el.attributes.length; aIdx++) {
        var attr = el.attributes[aIdx];
        if (/^on/i.test(attr.name)) {
          el.removeAttribute(attr.name);
        }
      }
    });
    /* Inline the Mermaid-specific styles so the rasterised PNG
       keeps the rendered colors.  We deliberately do NOT pull
       in external @import, @font-face, or url() data sources
       because those taint the canvas and break `canvas.toBlob`.
       Mermaid injects the relevant rules into the document
       <style> blocks at render-time; we discover them by
       querying the live stylesheets.  The fallback Inter /
       Helvetica / sans-serif font stack on the canvas means
       the PNG renders with a reasonable system font even when
       the user's web font has not loaded. */
    var styles = "";
    for (var ssi = 0; ssi < document.styleSheets.length; ssi++) {
      try {
        var rules = document.styleSheets[ssi].cssRules;
        for (var sri = 0; sri < rules.length; sri++) {
          var rule = rules[sri];
          if (rule.type === CSSRule.STYLE_RULE) {
            var text = rule.cssText || "";
            if (
              /mermaid|\.node|\.edge|\.cluster|\.label|\.actor|\.messageText|\.task|\.section/i.test(
                text
              ) &&
              !/url\s*\(/i.test(text) &&
              !/@import|@font-face/i.test(text)
            ) {
              styles += text + "\n";
            }
          }
        }
      } catch (e) {
        /* CORS-blocked stylesheet; skip. */
      }
    }
    if (styles) {
      var styleEl = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "style"
      );
      styleEl.appendChild(document.createTextNode(styles));
      clone.insertBefore(styleEl, clone.firstChild);
    }
    var serializer = new XMLSerializer();
    var svgText = serializer.serializeToString(clone);
    /* Use a base64 data URI rather than a Blob URL: data URIs
       are same-origin, so the <img> does not taint the canvas
       and `canvas.toBlob` is allowed to fire.  Blob URLs are
       cross-origin from the canvas' point of view even when the
       Blob is constructed in the same document. */
    var b64;
    if (typeof TextEncoder !== "undefined" && typeof btoa === "function") {
      /* btoa() needs Latin-1; TextEncoder gives us a clean path
         for any unicode the Mermaid labels might contain. */
      var bytes = new TextEncoder().encode(svgText);
      var bin = "";
      for (var k = 0; k < bytes.length; k++) bin += String.fromCharCode(bytes[k]);
      b64 = btoa(bin);
    } else {
      b64 = btoa(unescape(encodeURIComponent(svgText)));
    }
    var dataUri = "data:image/svg+xml;base64," + b64;
    var img = new Image();
    img.onload = function () {
      /* 2x scale for a sharper PNG on high-DPI displays. */
      var scale = Math.max(2, window.devicePixelRatio || 1);
      var canvas = document.createElement("canvas");
      canvas.width = Math.round(width * scale);
      canvas.height = Math.round(height * scale);
      var ctx = canvas.getContext("2d");
      /* Paint the page background first so transparent regions
         in the SVG pick up the same cream / dark as the rest of
         the page. */
      var bg =
        readVar("--color-canvas") ||
        (isDark() ? "#1a1814" : "#eef0e6");
      ctx.fillStyle = bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(function (blob) {
        if (!blob) {
          console.error("[dft-notes] canvas.toBlob returned null");
          flashError(wrap);
          return;
        }
        var pngUrl = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = pngUrl;
        a.download = filenameFromSource(wrap) + ".png";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(pngUrl); }, 1000);
        flashSuccess(wrap);
      }, "image/png");
    };
    img.onerror = function (e) {
      console.error("[dft-notes] could not rasterise mermaid SVG:", e);
      flashError(wrap);
    };
    img.src = dataUri;
  }

  function filenameFromSource(wrap) {
    /* Derive a friendly filename from the surrounding heading,
       falling back to a timestamp. */
    var heading = wrap.closest("section, article, .page-content");
    if (heading) {
      var h = heading.querySelector("h1, h2, h3, h4");
      if (h) {
        var slug = h.textContent
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-+|-+$/g, "")
          .slice(0, 60);
        if (slug) return "mermaid-" + slug;
      }
    }
    return "mermaid-" + new Date().toISOString().replace(/[:.]/g, "-");
  }

  function flashSuccess(wrap) {
    var btn = wrap.querySelector(".dft-mermaid-download");
    if (!btn) return;
    var original = btn.innerHTML;
    btn.classList.add("is-success");
    btn.innerHTML = '<span>Saved</span>';
    setTimeout(function () {
      btn.classList.remove("is-success");
      btn.innerHTML = original;
    }, 1400);
  }

  function flashError(wrap) {
    var btn = wrap.querySelector(".dft-mermaid-download");
    if (!btn) return;
    var original = btn.innerHTML;
    btn.classList.add("is-error");
    btn.innerHTML = '<span>Failed</span>';
    setTimeout(function () {
      btn.classList.remove("is-error");
      btn.innerHTML = original;
    }, 1800);
  }

  /* --- re-init on theme toggle -------------------------------- */

  function teardown() {
    /* Mermaid 10 does not expose a clean "unmount" API.  We
       wipe the rendered SVGs and restore the original source
       text so a re-render produces a clean slate.

       The non-obvious step is removing `data-processed="true"`:
       Mermaid 10 stamps this attribute on every element it
       renders and uses it as a guard to skip already-rendered
       nodes on subsequent `run()` calls.  Without stripping it,
       the second call to `mermaid.run()` is a no-op. */
    document
      .querySelectorAll("code.mermaid, pre.mermaid")
      .forEach(function (el) {
        var src = el.dataset && el.dataset.dftSource;
        if (typeof src === "string") {
          el.textContent = src;
        }
        el.removeAttribute("data-processed");
        el.removeAttribute("data-mermaid-id");
        el.removeAttribute("data-dft-png-ready");
      });
    document
      .querySelectorAll(".dft-mermaid-figure")
      .forEach(function (fig) {
        var inner = fig.querySelector("code.mermaid, pre.mermaid");
        if (inner) {
          fig.parentNode.insertBefore(inner, fig);
        }
        if (fig.parentNode) {
          fig.parentNode.removeChild(fig);
        }
      });
  }

  window.__dftReinitMermaid = function () {
    teardown();
    return render();
  };

  /* --- bootstrap ---------------------------------------------- */

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    render().catch(function (e) {
      console.error("[dft-notes] mermaid init crashed:", e);
    });
  });
})();
