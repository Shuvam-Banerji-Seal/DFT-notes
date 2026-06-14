---
layout: default
title: Home
permalink: /
description: >-
  Reader-first notes on Density Functional Theory (DFT) — a
  progressive walk through the foundations, methods, and practice
  of the standard workhorse of modern quantum chemistry and
  computational materials science.
---

<header class="hero-band">
  <div class="hero-band__inner">
    <div class="hero-band__content">
      <p class="hero-band__eyebrow">Reader-first knowledge base</p>
      <h1 class="hero-band__title">Density&nbsp;Functional Theory, <em>reader-first</em>.</h1>
      <p class="hero-band__subtitle">
        A progressive walk through the foundations, methods, and
        practice of DFT — from the postulates of quantum mechanics
        to the Kohn–Sham equations, exchange–correlation
        functionals, and the modern zoo of practical
        approximations.
      </p>
      <div class="hero-band__actions">
        <a href="{{ '/dft-notes/chapter-00/' | relative_url }}" class="btn btn--primary">Read the notes</a>
        <a href="{{ '/dft-notes/' | relative_url }}" class="btn btn--secondary">Browse the chapters</a>
        <a href="{{ '/design.md' | relative_url }}" class="btn btn--text-link">Design spec</a>
      </div>
    </div>
    <div class="hero-band__visual">
      <div class="code-window-card">
        <div class="code-window-card__titlebar">
          <span class="code-window-card__dot code-window-card__dot--red"></span>
          <span class="code-window-card__dot code-window-card__dot--yellow"></span>
          <span class="code-window-card__dot code-window-card__dot--green"></span>
          <span class="code-window-card__filename">ks_scf.py</span>
        </div>
<pre class="code-window-card__body"><code><span style="color:#a09d96"># Restricted Kohn–Sham SCF loop.</span>
<span style="color:#e8a55a">def</span> ks_scf(n_elec, v_xc, max_iter=<span style="color:#f0b070">100</span>):
    <span style="color:#a09d96">"""Return the converged density + KS eigenvalues."""</span>
    P = initial_guess(n_elec)
    <span style="color:#e8a55a">for</span> it <span style="color:#e8a55a">in</span> <span style="color:#b6c4ff">range</span>(max_iter):
        J   = hartree_from(P)
        F   = H_core + J + v_xc(P)
        ev, C = diagonalise(F, S)
        P_new = density_from(C, n_elec)
        <span style="color:#e8a55a">if</span> converged(P, P_new):
            <span style="color:#e8a55a">return</span> energy(P), ev, C
        P = mix(P, P_new, α=<span style="color:#f0b070">0.3</span>)
    <span style="color:#e8a55a">raise</span> <span style="color:#ff8b7a">RuntimeError</span>(<span style="color:#8fc89a">"SCF did not converge"</span>)</code></pre>
      </div>
    </div>
  </div>
</header>

<section class="section section--soft">
  <div class="container">
    <p class="section__eyebrow">What you'll find</p>
    <h2 class="section__heading">Six chapters, one continuous argument.</h2>
    <p class="section__lede">
      Every chapter follows the same template: the claim, the
      derivation, a minimal code sample, and an honest list of
      what the formula doesn't tell you. Math is rendered
      client-side; code is Python unless otherwise noted.
    </p>
    <div class="feature-grid">
      <article class="feature-card">
        <div class="feature-card__icon" aria-hidden="true">ℏ</div>
        <h3 class="feature-card__title">Schrödinger, slowly.</h3>
        <p class="feature-card__body">
          The postulates, the electronic Hamiltonian, the Born
          interpretation. One minimal example (the particle in a
          box) solved both analytically and numerically.
        </p>
        <a href="{{ '/dft-notes/chapter-01/' | relative_url }}" class="feature-card__link">Read chapter 01 →</a>
      </article>
      <article class="feature-card">
        <div class="feature-card__icon" aria-hidden="true">Ψ</div>
        <h3 class="feature-card__title">The exponential wall.</h3>
        <p class="feature-card__body">
          Why the exact electronic wavefunction is unsolvable for
          any non-trivial molecule, and a tour of the hierarchy
          that tries to fix it: CI, MP2, CCSD(T), full CI.
        </p>
        <a href="{{ '/dft-notes/chapter-02/' | relative_url }}" class="feature-card__link">Read chapter 02 →</a>
      </article>
      <article class="feature-card">
        <div class="feature-card__icon" aria-hidden="true">F̂</div>
        <h3 class="feature-card__title">Hartree–Fock, then Kohn–Sham.</h3>
        <p class="feature-card__body">
          Mean-field theory and the self-consistent field — the
          vocabulary every later method is forced to speak. Then
          the Kohn–Sham reformulation that hides the unknown
          inside a single functional.
        </p>
        <a href="{{ '/dft-notes/chapter-03/' | relative_url }}" class="feature-card__link">Read chapter 03 →</a>
      </article>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    <p class="section__eyebrow">The future plan</p>
    <h2 class="section__heading">A canvas e-reader for the chapters.</h2>
    <p class="section__lede">
      The current site is plain Jekyll. The future plan is a
      custom e-reader surface — <a href="https://github.com/chenglou/pretext" rel="noopener"><code>@chenglou/pretext</code></a>
      for the layout (faster than DOM measurement), KaTeX for
      math, light/dark themes, and a font-size slider. The full
      system is documented in the
      <a href="{{ '/design.md' | relative_url }}">design spec</a>
      at the root of the repo.
    </p>
  </div>
</section>

<section class="container" style="padding: var(--space-section) 0;">
  <div class="callout-card-coral">
    <p class="callout-card-coral__eyebrow">Start reading</p>
    <h2 class="callout-card-coral__title">Chapter 00 — Welcome.</h2>
    <p class="callout-card-coral__body">
      How to read these notes, the notation we use, the
      prerequisites, and a short reading list. No equations —
      that's the only one.
    </p>
    <div class="callout-card-coral__actions">
      <a href="{{ '/dft-notes/chapter-00/' | relative_url }}" class="btn btn--on-coral">Read chapter 00</a>
      <a href="{{ '/dft-notes/' | relative_url }}" class="btn btn--text-link" style="color: var(--color-on-primary);">Browse all chapters</a>
    </div>
  </div>
</section>
