---
layout: page
title: "Physical constants and unit conversions"
permalink: /dft-notes/extras/physical-constants/
description: >-
  A single, comprehensive reference for the physical constants and unit
  conversions used throughout the DFT notes. 2019 CODATA values,
  atomic-unit definitions, and the conversion factors that come up
  over and over in computational chemistry and materials science.
keywords: "CODATA, physical constants, atomic units, hartree, bohr,
  eV, kcal/mol, cm^-1, conversion factors, 2019 SI redefinition,
  Bohr magneton, fine-structure constant, Rydberg"
---

# Physical constants and unit conversions

> The single, comprehensive reference for every physical constant
> and every unit conversion that recurs in the DFT Notes.  Open it,
> look up the value, close it, return to the chapter.  Every
> numerical value is a 2019 CODATA recommended value; the values
> fixed by the 2019 SI redefinition are exact by definition and
> are flagged with *(exact)*.

This page is the **physical-constants analogue** of the
[notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }})
and the [math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}).
It collects, in one place, the numbers the chapters refer to
without proof.  Whenever a chapter uses a constant
($c$, $h$, $k_B$, $e$, $m_e$, …) or a non-atomic unit
(eV, kcal/mol, cm⁻¹, Debye, …), the value lives here and is
linked back to its source.

**Conventions used in this page.**

- The 2019 SI redefinition is adopted throughout.  The defining
  constants $c$, $h$, $k_B$, $N_A$, and $e$ are therefore
  **exact** (no uncertainty), and every other constant in the
  table is a 2019 CODATA recommended value.
- All atomic-unit values follow the conventions of
  [Chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }})
  and the
  [notation glossary §13.1]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}):
  $\hbar = m_e = e = 4\pi\varepsilon_0 = 1$.
  The non-relativistic Hartree atomic units (not the Gaussian
  "au") are used; the speed of light in these units is
  $c = 1/\alpha \approx 137.036$.
- Numbers are quoted to the precision the chapters need.  The
  2019 CODATA values are quoted to 6–11 significant figures
  depending on the constant; the conversion factors are quoted
  to 6 significant figures, which is the precision at which
  rounding errors in DFT calculations are negligible.
- MathJax 3 is used.  Numbered equations use
  `\begin{equation} ... \label{eq:pc-foo} ... \end{equation}`;
  cross-references in this file are `\eqref{eq:pc-foo}`.

---

## 1. The seven 2019 SI base units

The **International System of Units (SI)** is the system in which
all of the 2019 CODATA values are reported.  Since 20 May 2019
the seven base units have been defined by fixing seven constants
of nature; the base units are no longer defined by *artefacts*
(kilogram) or *reference implementations* (metre, candela).
The seven defining constants are summarised at the bottom of
this section.

### 1.1 Metre (length)

The **metre**, symbol $\text{m}$, is the SI unit of length,
defined by fixing the speed of light in vacuum,

\begin{equation}
\label{eq:pc-metre}
c \;\equiv\; 299\,792\,458 \;\text{m} \,\text{s}^{-1} \quad \text{(exact)} .
\end{equation}

Historically the metre was the length of a prototype bar kept
at Sèvres (1889), then a multiple of the wavelength of the
krypton-86 2p₁₀ → 5d₅ transition (1960).  Since 1983 it has
been defined by $c$.  In atomic units (this page, §3) the metre
is $1\;\text{m} = 1.88973 \times 10^{10}\, a_0$ (§5).

### 1.2 Kilogram (mass)

The **kilogram**, symbol $\text{kg}$, is the SI unit of mass,
defined by fixing the Planck constant,

\begin{equation}
\label{eq:pc-kilogram}
h \;\equiv\; 6.626\,070\,15 \times 10^{-34} \;\text{J} \,\text{s} \quad \text{(exact)} .
\end{equation}

Combined with the definitions of the metre and the second, this
fixes $h$ and hence (via the de Broglie relation
$p = h/\lambda$) the kilogram.  The old "Le Grand K" prototype
cylinder, kept at the BIPM in Sèvres, was retired on 20 May
2019. ### 1.3 Second (time)

The **second**, symbol $\text{s}$, is the SI unit of time,
defined by fixing the cesium-133 ground-state hyperfine
transition frequency,

\begin{equation}
\label{eq:pc-second}
\nu_\text{Cs} \;\equiv\; 9\,192\,631\,770 \;\text{Hz} \quad \text{(exact)} .
\end{equation}

The second is the duration of $9\,192\,631\,770$ periods of
the corresponding Cs-133 radiation.

### 1.4 Ampere (electric current)

The **ampere**, symbol $\text{A}$, is the SI unit of electric
current, defined by fixing the elementary charge,

\begin{equation}
\label{eq:pc-ampere}
e \;\equiv\; 1.602\,176\,634 \times 10^{-19} \;\text{C} \quad \text{(exact)} .
\end{equation}

Historically the ampere was the current which, if maintained
in two straight parallel conductors of infinite length and
negligible cross-section placed one metre apart in vacuum,
would produce a force of $2 \times 10^{-7}$ newtons per metre
of length.  The 2019 redefinition replaces that mechanical
artefact with the fixed $e$, after which the magnetic
constant $\mu_0$ is measured and the electric constant
$\varepsilon_0 = 1/(\mu_0 c^2)$ is determined.

### 1.5 Kelvin (temperature)

The **kelvin**, symbol $\text{K}$, is the SI unit of
thermodynamic temperature, defined by fixing the Boltzmann
constant,

\begin{equation}
\label{eq:pc-kelvin}
k_B \;\equiv\; 1.380\,649 \times 10^{-23} \;\text{J} \,\text{K}^{-1} \quad \text{(exact)} .
\end{equation}

Combined with the definitions of the kilogram, metre, and
second this fixes $k_B$ and hence the kelvin.  The old
triple-point-of-water definition (273.16 K) is no longer
primary; water's triple-point temperature is now a measured
quantity.  In atomic units the kelvin is
$1\;\text{K} \times k_B = 3.16681 \times 10^{-6}\, E_h$ (§4).

### 1.6 Mole (amount of substance)

The **mole**, symbol $\text{mol}$, is the SI unit of amount of
substance, defined by fixing the Avogadro constant,

\begin{equation}
\label{eq:pc-mole}
N_A \;\equiv\; 6.022\,140\,76 \times 10^{23} \;\text{mol}^{-1} \quad \text{(exact)} .
\end{equation}

The mole is the amount of substance of a system that contains
exactly $6.022\,140\,76 \times 10^{23}$ elementary entities
(atoms, molecules, ions, electrons, …).  Before 2019 the mole
was defined by the 0.012 kg of carbon-12 convention; that
definition is no longer primary.

### 1.7 Candela (luminous intensity)

The **candela**, symbol $\text{cd}$, is the SI unit of luminous
intensity, defined by fixing the luminous efficacy of
monochromatic radiation of frequency $540 \times 10^{12}$ Hz:

\begin{equation}
\label{eq:pc-candela}
K_\text{cd} \;\equiv\; 683 \;\text{lm} \,\text{W}^{-1} \quad \text{(exact)} .
\end{equation}

The candela does not enter the DFT chapters.

### 1.8 The seven defining constants at a glance

The seven constants of nature that **define** the seven base
units of the SI are summarised in the table below.  The 2019
redefinition is sometimes called the **"new SI"**; it entered
into force on 20 May 2019 (the 144th anniversary of the Metre
Convention).  Because the seven defining constants are exact,
the *only* source of numerical uncertainty in any 2019 CODATA
value is the *measurement* of the constant itself.  For
example, the value of the fine-structure constant
$\alpha \approx 1/137.036$ is *measure`d*' (it is not fixed by
the SI); its relative uncertainty is $2.3 \times 10^{-10}$.  The
2019 CODATA value is $\alpha^{-1} = 137.035\,999\,084(21)$.

---

## 2. The 2019 CODATA constants

The 2019 CODATA recommended values of the fundamental physical
constants, in the SI units of §1. The values flagged *(exact)*
are fixed by the 2019 SI redefinition; the rest are the
2019 CODATA recommended values.  References: Tiesinga, Mohr,
Newell, Taylor (2021), *Rev. Mod. Phys.* **93**, 025010. ### 2.1 The five defining constants (also in §1)

| Symbol | Name | Value (SI) | Comment |
|:-------|:-----|:-----------|:--------|
| $c$ | speed of light in vacuum | $299\,792\,458\;\text{m}\,\text{s}^{-1}$ *(exact)* | eq. \eqref{eq:pc-metre} |
| $h$ | Planck constant | $6.626\,070\,15 \times 10^{-34}\;\text{J}\,\text{s}$ *(exact)* | eq. \eqref{eq:pc-kilogram} |
| $k_B$ | Boltzmann constant | $1.380\,649 \times 10^{-23}\;\text{J}\,\text{K}^{-1}$ *(exact)* | eq. \eqref{eq:pc-kelvin} |
| $N_A$ | Avogadro constant | $6.022\,140\,76 \times 10^{23}\;\text{mol}^{-1}$ *(exact)* | eq. \eqref{eq:pc-mole} |
| $e$ | elementary charge | $1.602\,176\,634 \times 10^{-19}\;\text{C}$ *(exact)* | eq. \eqref{eq:pc-ampere} |

### 2.2 The reduced Planck constant

\begin{equation}
\label{eq:pc-hbar}
\hbar \;\equiv\; \frac{h}{2\pi} \;\approx\; 1.054\,571\,817 \times 10^{-34}\;\text{J}\,\text{s} .
\end{equation}

Exact in the new SI: $\hbar = h/(2\pi)$ with $h$ exact.  In
atomic units $\hbar = 1$ (by definition).

### 2.3 The electron rest mass

\begin{equation}
\label{eq:pc-me}
m_e \;\approx\; 9.109\,383\,7015 \times 10^{-31}\;\text{kg} .
\end{equation}

The 2019 CODATA value; the relative uncertainty is
$3.0 \times 10^{-10}$.  In atomic units $m_e = 1$ (by
definition).

### 2.4 The fine-structure constant

\begin{equation}
\label{eq:pc-alpha}
\alpha \;\equiv\; \frac{e^2}{4\pi \varepsilon_0 \hbar c}
\;\approx\; \frac{1}{137.035\,999\,084} \;\approx\; 7.297\,352\,5693 \times 10^{-3} .
\end{equation}

Dimensionless.  Equal to $e^2/(\hbar c)$ in Gaussian units
(setting $4\pi\varepsilon_0 = 1$).  Drives *all* of atomic
physics: the speed of light in atomic units is $c = 1/\alpha$
(§7), the Bohr magneton contains $e$ explicitly, and the
relativistic correction to the kinetic energy of a 1s electron
is $\approx \alpha^2/2$ a.u.  See Chapter 01 §1.10.7 for the
$2p \to 1s$ spontaneous emission rate of hydrogen, which is
proportional to $\alpha^3$.

### 2.5 The vacuum permittivity

\begin{equation}
\label{eq:pc-eps0}
\varepsilon_0 \;\equiv\; \frac{1}{\mu_0 c^2}
\;\approx\; 8.854\,187\,8128 \times 10^{-12}\;\text{F}\,\text{m}^{-1} .
\end{equation}

In atomic units $4\pi\varepsilon_0 = 1$ (so
$\varepsilon_0 = 1/(4\pi)$).  The Coulomb interaction between
two point charges is $V_\text{Coulomb}(r) = e^2/(4\pi\varepsilon_0 r)$,
which reduces to $1/r$ in atomic units.

### 2.6 The Rydberg constant

\begin{equation}
\label{eq:pc-rydberg}
R_\infty \;\equiv\; \frac{m_e e^4}{8 \varepsilon_0^2 h^3 c}
\;\approx\; 1.097\,373\,156\,8160 \times 10^{7}\;\text{m}^{-1} .
\end{equation}

The wavenumber of the lowest-energy (Lyman-$\alpha$) hydrogen
1s → 2p transition is $R_\infty (1 - 1/4) = (3/4) R_\infty$.
Multiplied by $hc$, the ionisation energy of hydrogen is
$E_\text{ion} = h c R_\infty \approx 13.6057\;\text{eV} = (1/2) E_h$
(since the Bohr-model 1s energy is $-R_\infty hc = -E_h/2$;
see [Chapter 01 §1.10]({{ "/dft-notes/chapter-01/" | relative_url }})).
The Rydberg *frequency* is $R_\infty c$; the Rydberg energy
is $R_\infty hc$.

### 2.7 The Bohr radius

\begin{equation}
\label{eq:pc-bohr}
a_0 \;\equiv\; \frac{4\pi \varepsilon_0 \hbar^2}{m_e e^2}
\;\approx\; 5.291\,772\,109\,03 \times 10^{-11}\;\text{m} .
\end{equation}

The most probable radius of the hydrogen 1s orbital.  Equal to
$1/(\alpha m_e c)$ in Gaussian units.  In atomic units
$a_0 = 1$ (by definition); in SI,
$1\;\text{Å} = 10^{-10}\;\text{m} = 1.88973\,a_0$.

### 2.8 The Hartree energy

\begin{equation}
\label{eq:pc-hartree}
E_h \;\equiv\; \frac{e^2}{4\pi \varepsilon_0 a_0}
\;\equiv\; m_e c^2 \alpha^2
\;\approx\; 4.359\,744\,722\,2071 \times 10^{-18}\;\text{J} .
\end{equation}

The energy unit of atomic units.  Twice the magnitude of the
hydrogen 1s energy: $|E_\text{1s}| = E_h/2 \approx 13.6057\;\text{eV}$.

### 2.9 The Bohr magneton

\begin{equation}
\label{eq:pc-bohr-magneton}
\mu_B \;\equiv\; \frac{e \hbar}{2 m_e}
\;\approx\; 9.274\,010\,0783 \times 10^{-24}\;\text{J}\,\text{T}^{-1} .
\end{equation}

The natural unit of electron magnetic moment; the spin
magnetic moment is $-\mu_B$ (with $g_e \approx 2.002\,319\,304\,36$).
The nuclear magneton is $\mu_N = \mu_B \times m_e/m_p$.

### 2.10 The classical electron radius

\begin{equation}
\label{eq:pc-re}
r_e \;\equiv\; \frac{e^2}{4\pi \varepsilon_0 m_e c^2}
\;\approx\; 2.817\,940\,3262 \times 10^{-15}\;\text{m} .
\end{equation}

The radius at which the electrostatic self-energy of a
uniformly charged sphere equals $m_e c^2$.  The
Thomson-scattering cross-section is $\sigma_T = (8\pi/3) r_e^2$.

### 2.11 The reduced Compton wavelength

\begin{equation}
\label{eq:pc-compton}
\bar\lambda_C \;\equiv\; \frac{\hbar}{m_e c}
\;=\; a_0 \, \alpha
\;\approx\; 3.861\,592\,6796 \times 10^{-13}\;\text{m} .
\end{equation}

The wavelength of a photon whose energy equals $m_e c^2$ (up
to a factor of $2\pi$; the *unreduce`d*' Compton wavelength is
$\lambda_C = 2\pi \bar\lambda_C \approx 2.426 \times 10^{-12}\;\text{m}$).

### 2.12 Where to find more

> **Cross-references.**  $c$, $\alpha$: Chapter 01 §1.10.7
> (hydrogen 2p→1s); $a_0$, $E_h$, $\hbar$: throughout
> ([notation glossary §13.1]({{ "/dft-notes/extras/notation-glossary/" | relative_url }})
> for the formal conventions); $k_B$: Chapter 07 §7.6.3
> (smearing); $N_A$: Chapter 09 (molar energies);
> $\mu_B$: Chapter 04 §4.8.4 (non-collinear spin DFT) and
> planned Chapter 11 (magnetic response).

---

## 3. Atomic units (au)

The DFT notes use **atomic units** (also called Hartree atomic
units) throughout.  In atomic units the four fundamental
constants

\begin{equation}
\label{eq:pc-au-def}
\hbar \;=\; m_e \;=\; e \;=\; 4\pi \varepsilon_0 \;\equiv\; 1 \quad \text{(in atomic units)} .
\end{equation}

This choice of units turns the Schrödinger equation for a
one-electron atom into the dimensionless equation

$$
\Bigl( -\tfrac{1}{2} \nabla^2 - \frac{Z}{r} \Bigr) \psi \;=\; \varepsilon \, \psi ,
$$

with the Bohr-model 1s energy $\varepsilon_{1s} = -Z^2/2$ a.u.
and the Bohr radius $a_0 = 1$ a.u.  In Gaussian units, the
equivalent choice is $\hbar = m_e = e = 1$ (i.e. $4\pi\varepsilon_0$
is *not* set to 1, but the Coulomb interaction is
$1/r$ directly because $k_e = 1$ in Gaussian units); the
two conventions differ by factors of $4\pi$ in the
electromagnetic potentials only.

The combination $E_h/a_0$ is sometimes called a "natural
unit" of force.  The atomic units below are the units in
which the defining constants of \eqref{eq:pc-au-def} are 1. ### 3.1 The atomic unit of length — the Bohr radius

\begin{equation}
\label{eq:pc-au-length}
1\;\text{a.u. of length} \;\equiv\; a_0
\;\approx\; 5.291\,772\,109\,03 \times 10^{-11}\;\text{m}
\;\approx\; 0.529\,177\,\text{Å}
\;\approx\; 0.529\,177 \times 10^{-8}\;\text{cm} .
\end{equation}

The Bohr radius of \eqref{eq:pc-bohr}.  See §5 for the
conversion table.

### 3.2 The atomic unit of energy — the Hartree

\begin{equation}
\label{eq:pc-au-energy}
1\;\text{a.u. of energy} \;\equiv\; E_h
\;\approx\; 4.359\,744\,722\,2071 \times 10^{-18}\;\text{J}
\;\approx\; 27.211\,386\,245\,988\;\text{eV}
\;\approx\; 627.509\;\text{kcal}\,\text{mol}^{-1}
\;\approx\; 219\,474.631\,370\,8\;\text{cm}^{-1} .
\end{equation}

The Hartree energy of \eqref{eq:pc-hartree}.  Twice the binding
energy of the hydrogen 1s electron.  See §4 for the full
conversion table; the values quoted here are the exact
CODATA-based ones to the precision of the constants.

### 3.3 The atomic unit of time

\begin{equation}
\label{eq:pc-au-time}
1\;\text{a.u. of time} \;\equiv\; \frac{\hbar}{E_h}
\;\approx\; 2.418\,884\,326\,5857 \times 10^{-17}\;\text{s}
\;\approx\; 2.418\,884 \times 10^{-2}\;\text{fs}
\;\approx\; 24.188\,84\;\text{as} .
\end{equation}

The time for an electron in the hydrogen 1s orbital to
complete one classical orbit.  1 fs = 41.34 a.u. of time.

### 3.4 The atomic unit of force

\begin{equation}
\label{eq:pc-au-force}
1\;\text{a.u. of force} \;\equiv\; \frac{E_h}{a_0}
\;\approx\; 8.238\,723\,498\,36 \times 10^{-8}\;\text{N}
\;\approx\; 82.387\;\text{nN} .
\end{equation}

The natural unit of force in chemistry.  A typical converged
SCF force on a light atom is $\sim 10^{-3}$ a.u. of force =
$\sim 10^{-10}$ N.

### 3.5 The atomic unit of momentum

\begin{equation}
\label{eq:pc-au-momentum}
1\;\text{a.u. of momentum} \;\equiv\; \frac{\hbar}{a_0}
\;\approx\; 1.992\,851\,914\,10 \times 10^{-24}\;\text{kg}\,\text{m}\,\text{s}^{-1} .
\end{equation}

Appears in the **Hellmann–Feynman** force on a nucleus
(Chapter 04 §4.7.1).

### 3.6 The atomic unit of charge

\begin{equation}
\label{eq:pc-au-charge}
1\;\text{a.u. of charge} \;\equiv\; e
\;\approx\; 1.602\,176\,634 \times 10^{-19}\;\text{C} .
\end{equation}

The elementary charge, exact in the new SI.  In the
electron-repulsion integral the factor $1/r$ in atomic
units absorbs the $e^2/(4\pi\varepsilon_0) = 1$.

### 3.7 The atomic unit of mass

\begin{equation}
\label{eq:pc-au-mass}
1\;\text{a.u. of mass} \;\equiv\; m_e
\;\approx\; 9.109\,383\,7015 \times 10^{-31}\;\text{kg} .
\end{equation}

Nuclear masses in atomic units are $M_I / m_e$: hydrogen
$\approx 1836.15\,m_e$, carbon-12 $\approx 21\,979.4\,m_e$.

### 3.8 The atomic unit of electric field

\begin{equation}
\label{eq:pc-au-efield}
1\;\text{a.u. of electric field} \;\equiv\; \frac{E_h}{e\,a_0}
\;\approx\; 5.142\,206\,747\,63 \times 10^{11}\;\text{V}\,\text{m}^{-1} .
\end{equation}

The electric field that, applied across a Bohr radius, does
one Hartree of work on a unit charge.  The field of a proton
at the Bohr radius is exactly 1 a.u. of electric field.

### 3.9 The atomic unit of electric potential

\begin{equation}
\label{eq:pc-au-potential}
1\;\text{a.u. of electric potential} \;\equiv\; \frac{E_h}{e}
\;\approx\; 27.211\,386\,245\,988\;\text{V} .
\end{equation>

Numerically equal to the conversion factor of §4.2. The
first ionisation potential of hydrogen is
$\approx 0.5\;\text{a.u.} = 13.6057\;\text{V}$.

### 3.10 The atomic unit of dipole moment

\begin{equation}
\label{eq:pc-au-dipole}
1\;\text{a.u. of dipole moment} \;\equiv\; e\,a_0
\;\approx\; 8.478\,353\,6255 \times 10^{-30}\;\text{C}\,\text{m}
\;\approx\; 2.5417\;\text{D} .
\end{equation}

A molecule with one electron separated from a unit positive
charge by $a_0$ has a dipole moment of 1 a.u.  See §6 for the
Debye conversion.

### 3.11 The atomic unit of magnetic flux density

\begin{equation}
\label{eq:pc-au-bfield}
1\;\text{a.u. of magnetic flux density} \;\equiv\; \frac{\hbar}{e\,a_0^2}
\;\approx\; 2.350\,517\,567\,58 \times 10^{5}\;\text{T} .
\end{equation}

The magnetic field that, acting on a Bohr magneton, gives
$\mu_B B = E_h$ (one Hartree of Zeeman energy).  Typical
laboratory fields of 1–10 T are $4.3 \times 10^{-6}$ –
$4.3 \times 10^{-5}$ a.u.  See §6 for the conversion.

### 3.12 The atomic unit of frequency and angular frequency

\begin{equation}
\label{eq:pc-au-frequency}
1\;\text{a.u. of frequency} \;\equiv\; \frac{E_h}{\hbar}
\;\approx\; 6.579\,683\,920\,502 \times 10^{15}\;\text{Hz} .
\end{equation}

The inverse of the atomic unit of time.  Visible-light
frequencies ($\sim 5 \times 10^{14}\;\text{Hz}$) are
$\sim 0.08$ a.u.; soft X-rays ($\sim 1\;\text{keV}$) are
$\sim 0.04$ a.u. (since $1\;\text{eV} = 0.0367$ a.u.).

### 3.13 Summary of the most-used atomic units

| Quantity | Atomic unit | Value in SI | Ref. eq. |
|:---------|:------------|:------------|:---------|
| length | $a_0$ | $5.29177 \times 10^{-11}\;\text{m}$ | \eqref{eq:pc-au-length} |
| energy | $E_h$ | $4.35974 \times 10^{-18}\;\text{J}$ | \eqref{eq:pc-au-energy} |
| time | $\hbar/E_h$ | $2.41888 \times 10^{-17}\;\text{s}$ | \eqref{eq:pc-au-time} |
| force | $E_h/a_0$ | $8.23872 \times 10^{-8}\;\text{N}$ | \eqref{eq:pc-au-force} |
| momentum | $\hbar/a_0$ | $1.99285 \times 10^{-24}\;\text{kg}\,\text{m}\,\text{s}^{-1}$ | \eqref{eq:pc-au-momentum} |
| charge | $e$ | $1.60218 \times 10^{-19}\;\text{C}$ | \eqref{eq:pc-au-charge} |
| mass | $m_e$ | $9.10938 \times 10^{-31}\;\text{kg}$ | \eqref{eq:pc-au-mass} |
| electric field | $E_h/(e a_0)$ | $5.14221 \times 10^{11}\;\text{V}\,\text{m}^{-1}$ | \eqref{eq:pc-au-efield} |
| potential | $E_h/e$ | $27.2114\;\text{V}$ | \eqref{eq:pc-au-potential} |
| dipole moment | $e a_0$ | $8.47835 \times 10^{-30}\;\text{C}\,\text{m}$ | \eqref{eq:pc-au-dipole} |
| magnetic flux density | $\hbar/(e a_0^2)$ | $2.35052 \times 10^{5}\;\text{T}$ | \eqref{eq:pc-au-bfield} |
| frequency | $E_h/\hbar$ | $6.57969 \times 10^{15}\;\text{Hz}$ | \eqref{eq:pc-au-frequency} |

> **Cross-references.**  Atomic units are used in **every**
> chapter of the DFT notes; see
> [Chapter 00 §"Notation"]({{ "/dft-notes/chapter-00/" | relative_url }})
> for the conventions and
> [notation glossary §13.1]({{ "/dft-notes/extras/notation-glossary/" | relative_url }})
> for the formal statement.  When a chapter *deviates* from
> atomic units (e.g. SI units for a spectroscopic rate, or
> natural units $\hbar = c = 1$ for a relativistic
> digression), the deviation is announced at the top of the
> chapter.

---

## 4. Energy conversions

The energy unit of atomic units ($E_h \approx 27.2\;\text{eV}$)
is convenient for the *electroni`c*' degrees of freedom but is
cumbersome for chemists (kcal/mol), spectroscopists (cm⁻¹),
and thermal measurements (K).  All values below are derived
from the 2019 CODATA values of $E_h$, $e$, $k_B$, $N_A$, $h$
and the definition $1\;\text{cm}^{-1} \equiv h c \times 100\;\text{J}$.

### 4.1 The Hartree as the master unit

The conversion factors are tabulated as **row unit → column
unit**, with the *Hartree* as the common reference.  To use
the table, multiply the entry by the source quantity.

| Unit | In Hartree | In eV | In kJ/mol | In kcal/mol | In cm⁻¹ | In K ($k_B T$) |
|:-----|:-----------|:------|:----------|:------------|:--------|:---------------|
| **1 Hartree** | 1 | 27.2114 | 2625.50 | 627.509 | 219474.6 | 315775.1 |
| 1 eV | 0.0367493 | 1 | 96.4853 | 23.0605 | 8065.54 | 11604.5 |
| 1 kJ/mol | $3.80871 \times 10^{-4}$ | 0.010364 | 1 | 0.239006 | 83.5935 | 120.272 |
| 1 kcal/mol | $1.59360 \times 10^{-3}$ | 0.043364 | 4.18400 | 1 | 349.755 | 503.217 |
| 1 cm⁻¹ | $4.55633 \times 10^{-6}$ | $1.23984 \times 10^{-4}$ | 0.0119627 | $2.85911 \times 10^{-3}$ | 1 | 1.43878 |
| 1 K ($k_B T$) | $3.16681 \times 10^{-6}$ | $8.61733 \times 10^{-5}$ | $8.31446 \times 10^{-3}$ | $1.98720 \times 10^{-3}$ | 0.695039 | 1 |
| 1 J | $2.29371 \times 10^{17}$ | $6.24151 \times 10^{18}$ | $6.02214 \times 10^{20}$ | $1.43934 \times 10^{20}$ | $5.03412 \times 10^{22}$ | $7.24297 \times 10^{22}$ |
| 1 J/mol | $3.80871 \times 10^{-7}$ | $1.03643 \times 10^{-5}$ | $1.00000 \times 10^{-3}$ | $2.39006 \times 10^{-4}$ | 0.0835935 | 0.120272 |

### 4.2 The Hartree in the other units (explicitly)

For convenience — these are the row of §4.1 for the Hartree:

\begin{equation}
1\;E_h \;=\; 27.211\,386\,245\,988\;\text{eV} , \label{eq:pc-Eh-eV}
\end{equation}
\begin{equation}
1\;E_h \;=\; 627.509\,474\,063\,1\;\text{kcal}\,\text{mol}^{-1} , \label{eq:pc-Eh-kcal}
\end{equation}
\begin{equation}
1\;E_h \;=\; 219\,474.631\,363\,2\;\text{cm}^{-1} , \label{eq:pc-Eh-cm}
\end{equation}
\begin{equation}
1\;E_h \;=\; 4.359\,744\,722\,2071 \times 10^{-18}\;\text{J} , \label{eq:pc-Eh-J}
\end{equation}
\begin{equation}
1\;E_h \;=\; 2625.499\,639\,479\,9\;\text{kJ}\,\text{mol}^{-1} , \label{eq:pc-Eh-kJ}
\end{equation}
\begin{equation}
1\;E_h \;=\; 315\,775.13\;\text{K} \times k_B . \label{eq:pc-Eh-K}
\end{equation}

The **hydrogen 1s binding energy** $E_h/2 = 13.6057\;\text{eV}
= 313.755\;\text{kcal/mol} = 109\,737.3\;\text{cm}^{-1}$ is
the calibration point for every UV/vis spectrum of an atom.

### 4.3 The electronvolt as the practical unit

The electronvolt is the most common *practical* energy unit
in atomic, molecular, and solid-state physics — the energy
gained by an electron traversing a potential difference of
one volt:

\begin{equation}
\label{eq:pc-eV-def}
1\;\text{eV} \;\equiv\; e \times 1\;\text{V} \;=\; 1.602\,176\,634 \times 10^{-19}\;\text{J} \quad \text{(exact)} .
\end{equation}

The conversion to atomic units:

\begin{equation}
1\;\text{eV} \;=\; 0.036\,749\,322\,175\,654\,43\;E_h , \label{eq:pc-eV-Eh}
\end{equation}
\begin{equation}
1\;\text{eV} \;=\; 23.060\,547\,830\,619\,929\;\text{kcal}\,\text{mol}^{-1} , \label{eq:pc-eV-kcal}
\end{equation}
\begin{equation}
1\;\text{eV} \;=\; 8065.543\,937\,321\,525\;\text{cm}^{-1} . \label{eq:pc-eV-cm}
\end{equation}

A 1 eV excitation corresponds to a thermal energy of
$\sim 23\;\text{kcal/mol}$, well above $k_B T$ at room
temperature ($\sim 0.6\;\text{kcal/mol}$) — the basis of
photochemistry.

### 4.4 The cm⁻¹ as the spectroscopic unit

The wavenumber $\tilde\nu$ in cm⁻¹ is the *practical* unit
for vibrational and rotational spectroscopy; the
corresponding energy is $E = h c \tilde\nu$:

\begin{equation}
1\;\text{cm}^{-1} \;=\; 1.986\,445\,857\,1489 \times 10^{-23}\;\text{J} , \label{eq:pc-cm-J}
\end{equation}
\begin{equation}
1\;\text{cm}^{-1} \;=\; 4.556\,335\,834\,8019 \times 10^{-6}\;E_h , \label{eq:pc-cm-Eh}
\end{equation}
\begin{equation}
1\;\text{cm}^{-1} \;=\; 1.239\,841\,984\,3322 \times 10^{-4}\;\text{eV} , \label{eq:pc-cm-eV}
\end{equation}
\begin{equation}
1\;\text{cm}^{-1} \;=\; 1.438\,776\,877\,0001\;\text{K} \times k_B . \label{eq:pc-cm-K}
\end{equation}

The CO stretch at $\sim 2170\;\text{cm}^{-1}$ corresponds to
$0.254\;\text{eV} = 5.85\;\text{kcal/mol}$.

### 4.5 The kelvin (as a thermal energy $k_B T$)

The **thermal energy** at temperature $T$ is
$E_\text{th} = k_B T$.  At room temperature
$T = 298.15\;\text{K}$,

$$
k_B T \;\approx\; 0.025\,692\;\text{eV}
\;\approx\; 0.000\,944\,E_h
\;\approx\; 0.592\;\text{kcal}\,\text{mol}^{-1}
\;\approx\; 207\;\text{cm}^{-1} .
$$

This is the "thermal scale" that sets the magnitude of
finite-temperature smearing in Chapter 07
(§7.6.3) and the temperature dependence of the Fermi–Dirac
distribution in [math cheatsheet §14.3]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}).

### 4.6 The joule and the molar energy

The **joule** is the SI unit of energy, with conversion

\begin{equation}
\label{eq:pc-J-Eh}
1\;\text{J} \;=\; 2.293\,712\,278\,3963 \times 10^{17}\;E_h .
\end{equation}

The two relations that come up in thermochemistry are

\begin{equation}
1\;\text{kJ}\,\text{mol}^{-1} \;=\; 3.80871 \times 10^{-4}\;E_h \,\text{(molecule)}^{-1}
\;=\; 1.03643 \times 10^{-2}\;\text{eV}\,\text{(molecule)}^{-1} , \label{eq:pc-kJmol}
\end{equation}
\begin{equation}
1\;\text{kcal}\,\text{mol}^{-1} \;=\; 1.59360 \times 10^{-3}\;E_h \,\text{(molecule)}^{-1}
\;=\; 4.33640 \times 10^{-2}\;\text{eV}\,\text{(molecule)}^{-1} . \label{eq:pc-kcalmol}
\end{equation}

The factor $1\;\text{kcal/mol} = 4.184\;\text{kJ/mol}$ is
exact in the post-2019 SI.  The most common energy-unit
confusion in chemistry is between *per molecule* and
*per mole*; the "hartree" is per particle, the "kcal/mol"
is per mole.

---

## 5. Length conversions

Lengths in atomic units (the Bohr radius) are the natural
unit for the DFT chapters.  The most-used practical units
are **Ångström** (1 Å $= 10^{-10}$ m) for chemical bonds
and **nanometre** (1 nm $= 10^{-9}$ m) for mesoscopic
structures.

### 5.1 Bohr as the master unit

The atomic unit of length is $a_0 \approx 0.529\,177$ Å.

| Unit | In Bohr ($a_0$) | In metres | In Ångström |
|:-----|:----------------|:----------|:------------|
| **1 Bohr ($a_0$)** | 1 | $5.29177 \times 10^{-11}$ | 0.529177 |
| 1 metre (m) | $1.88973 \times 10^{10}$ | 1 | $10^{10}$ |
| 1 Ångström (Å) | 1.88973 | $10^{-10}$ | 1 |
| 1 nanometre (nm) | 18.8973 | $10^{-9}$ | 10 |
| 1 picometre (pm) | 0.0188973 | $10^{-12}$ | 0.01 |

The *exact* (to 6 sig fig) conversion factor between metres
and Bohr is

\begin{equation}
\label{eq:pc-m-bohr}
1\;\text{m} \;=\; 1.889\,725\,988\,6 \times 10^{10}\,a_0 ,
\end{equation}

the inverse of eq. \eqref{eq:pc-bohr}.  The corresponding
Ångström conversion is

\begin{equation}
\label{eq:pc-A-bohr}
1\;\text{Å} \;=\; 1.889\,725\,988\,6\,a_0 ,
\end{equation}

and the nanometre conversion is

\begin{equation}
\label{eq:pc-nm-bohr}
1\;\text{nm} \;=\; 18.897\,259\,886\,a_0 .
\end{equation}

### 5.2 Typical length scales (sanity check)

To check the magnitudes: a C–C single bond in ethane is
$\sim 1.54\;\text{Å} \approx 2.91\,a_0$; a water molecule is
$\sim 3\;\text{Å}$ end-to-end $\approx 5.7\,a_0$; a typical
unit cell of a metal is $\sim 4\;\text{Å} \approx 7.6\,a_0$;
a graphene lattice constant is $\sim 2.46\;\text{Å} \approx
4.65\,a_0$.  The Bohr radius is small compared to chemistry
but large compared to nuclear physics (a proton charge radius
is $\sim 0.88\;\text{fm} \approx 1.7 \times 10^{-5}\,a_0$).

For photons, the wavelength–energy correspondence
$E = hc/\lambda$ becomes $E = 1240 / \lambda\;(\text{nm})$ in
eV·nm — the rule-of-thumb every photochemist memorises
(200 nm = 6.20 eV, 500 nm = 2.48 eV, 1 µm = 1.24 eV).

---

## 6. Other common conversions

A handful of additional unit conversions come up repeatedly in
DFT: forces on atoms (in eV/Å or Hartree/Bohr), magnetic
fields (in T or a.u. of B), and dipole moments (in Debye or
a.u. of dipole).  The conversion factors are tabulated below.

### 6.1 Force

The atomic unit of force is $E_h/a_0$ (§3.4).  The most
common practical unit is eV/Å, used by every solid-state code
(VASP, Quantum ESPRESSO, CASTEP, …):

\begin{equation}
1\;\text{eV}\,\text{Å}^{-1} \;=\; 1.944\,691\,754 \times 10^{-2}\;E_h\,a_0^{-1} , \label{eq:pc-eVperA}
\end{equation}
\begin{equation}
1\;E_h\,a_0^{-1} \;=\; 5.142\,206\,748 \times 10^{11}\;\text{eV}\,\text{m}^{-1} . \label{eq:pc-EhperB-eVperm}
\end{equation}

A converged SCF force on a light atom in a molecule is
$\sim 10^{-3}\;E_h/a_0 = 5.1 \times 10^{8}\;\text{eV/m} =
0.051\;\text{eV/Å} = 7.9 \times 10^{-11}\;\text{N}$.

### 6.2 Magnetic flux density

The atomic unit of magnetic flux density is $\hbar/(ea_0^2)$
(§3.11).  The most common practical unit is the **tesla**
(1 T = 1 V·s/m² = 1 kg·s⁻²·A⁻¹):

\begin{equation}
\label{eq:pc-T-au}
1\;\text{T} \;=\; 4.254\,382\,446 \times 10^{-6}\;\text{a.u. of } B .
\end{equation}

The inverse is $1\;B_\text{au} = 2.350\,517\,567 \times 10^{5}\;\text{T}$.
A field of 1 T gives an electron-spin Zeeman splitting of
$2 \mu_B \approx 1.16 \times 10^{-4}\;\text{eV} \approx
0.94\;\text{cm}^{-1}$ — in the microwave / ESR range, as
expected.

### 6.3 Dipole moment

The atomic unit of dipole moment is $e a_0$ (§3.10).  The
**Debye** is the most common practical unit
(1 D $\equiv 3.335\,64 \times 10^{-30}\;\text{C}\,\text{m}$):

\begin{equation}
1\;\text{D} \;=\; 0.393\,430\,227\;\text{a.u. of dipole} , \label{eq:pc-D-au}
\end{equation}
\begin{equation}
1\;\text{a.u. of dipole} \;=\; 2.5417\,\text{D} . \label{eq:pc-au-D}
\end{equation}

Typical molecular dipoles: HCl $\sim 1.08$ D, water
$\sim 1.85$ D, NaCl $\sim 9$ D, CO $\sim 0.12$ D.

### 6.4 Pressure and stress (for chapter 09 on geometry optimisation)

The DFT chapters (Chapter 04 §4.7.4 on the stress tensor) use
**GPa** as the unit of pressure; the atomic-unit conversion is
$1\;\text{GPa} = 3.39894 \times 10^{-5}\,E_h\,a_0^{-3}$.  Atmospheric
pressure is $\sim 10^{-4}$ GPa; a typical diamond-indenter
pressure is $\sim 10$ GPa; pressures at the centre of the
Earth are $\sim 350$ GPa.  The conversion
$1\;\text{GPa} = 10\;\text{kbar}$ is used in older
solid-state papers.

### 6.5 Energy per unit area (surface energy)

The atomic unit of surface energy is $E_h / a_0^2$, with
$1\;\text{J}\,\text{m}^{-2} = 1.60453 \times 10^{-4}\,E_h\,a_0^{-2}$ and
$1\;\text{eV}\,\text{Å}^{-2} = 6.34146 \times 10^{-3}\,E_h\,a_0^{-2}$.
Typical surface energies: Cu(111) $\sim 1.8\;\text{J/m}^2$,
Al(111) $\sim 1.1\;\text{J/m}^2$, water/vapour
$\sim 0.072\;\text{J/m}^2$.

### 6.6 Power and intensity (for laser–matter interaction)

For laser–matter interaction (planned Chapter 11), a
"strong-field" laser pulse is $\sim 10^{14}\;\text{W/cm}^2$;
the Keldysh-parameter boundary between multiphoton and
tunnelling ionisation is at $\sim 10^{13}\;\text{W/cm}^2$ for
typical atoms.

---

## 7. Useful formulae

A small set of derived relations come up over and over across
the chapters.  They are not the **fundamental** constants of
§2 — they are combinations of those constants that have
their own names and that the chapters quote directly.

### 7.1 The speed of light in atomic units

In atomic units $c$ has the numerical value $1/\alpha$:

\begin{equation}
\label{eq:pc-c-au}
c \;\xrightarrow[\text{atomic units}]{}\; \frac{1}{\alpha}
\;\approx\; 137.035\,999\,084\;\text{a.u.}
\;\approx\; 137\;\text{a.u.}
\end{equation}

i.e. 137 atomic units of velocity.  The "137" is the famous
fine-structure-constant number that appears in every
introductory physics course ("the 137 problem").  In
Gaussian units (where $4\pi\varepsilon_0 = 1$ is *not* imposed
but the Coulomb interaction is $1/r$) the speed of light in
atomic units is $c = 1/\alpha$ as well, but the *unit of
charge* differs from the SI definition by a factor of
$\sqrt{4\pi\varepsilon_0}$.

### 7.2 The fine-structure constant

\begin{equation}
\label{eq:pc-alpha-def}
\alpha \;\equiv\; \frac{e^2}{4\pi \varepsilon_0 \hbar c}
\;\approx\; \frac{1}{137.035\,999\,084} \;\approx\; 7.297\,352\,5693 \times 10^{-3} .
\end{equation}

Dimensionless; equal to $e^2/(\hbar c)$ in Gaussian units.
The Hartree energy is $m_e c^2 \alpha^2$ (§2.8), so *every*
atomic energy scale is "$\alpha^2 m_e c^2$" in character.

### 7.3 The electron Compton wavelength

\begin{equation}
\label{eq:pc-compton-formula}
\bar\lambda_C \;\equiv\; \frac{\hbar}{m_e c}
\;=\; a_0 \, \alpha
\;\approx\; 3.861\,592\,6796 \times 10^{-13}\;\text{m} .
\end{equation}

The wavelength of a photon whose energy equals $m_e c^2$ (up
to a factor of $2\pi$; the *unreduce`d*' Compton wavelength is
$\lambda_C = 2\pi \bar\lambda_C \approx 2.426 \times 10^{-12}\;\text{m}$).
The identity $\bar\lambda_C = a_0 \alpha$ is the simple
algebraic relation between the Compton wavelength and the
Bohr radius.

### 7.4 The classical electron radius

\begin{equation}
\label{eq:pc-re-formula}
r_e \;\equiv\; \frac{e^2}{4\pi \varepsilon_0 m_e c^2}
\;\approx\; 2.817\,940\,3262 \times 10^{-15}\;\text{m} .
\end{equation}

The radius at which the electrostatic self-energy of a
uniformly charged sphere equals $m_e c^2$.  The
Thomson-scattering cross-section is $\sigma_T = (8\pi/3) r_e^2$
— the low-energy limit of Compton scattering.  In atomic units
$r_e = \alpha^2 \approx 5.32 \times 10^{-5}\, a_0$.

### 7.5 The Bohr magneton

\begin{equation}
\label{eq:pc-muB-formula}
\mu_B \;\equiv\; \frac{e \hbar}{2 m_e}
\;\approx\; 9.274\,010\,0783 \times 10^{-24}\;\text{J}\,\text{T}^{-1} .
\end{equation}

The natural unit of electron magnetic moment.  The electron
spin moment is $-\mu_B$ (with $g_e \approx 2.002\,319\,304\,36$).
The nuclear magneton is $\mu_N = \mu_B \times m_e/m_p$, about
1/1836 of $\mu_B$; used in NMR.

---

## 8. Source attribution

The values in this page are taken from:

- **Tiesinga, E., Mohr, P. J., Newell, D. B. & Taylor, B. N.**
  (2021).  "CODATA recommended values of the fundamental
  physical constants: 2019."  *Reviews of Modern Physics*
  **93**, 025010. The five defining constants of the 2019
  SI redefinition ($c$, $h$, $k_B$, $N_A$, $e$) are
  **exact by definition**; the rest are the 2019 CODATA
  recommended values.
- **Szabo, A. & Ostlund, N. S.** (1982/1996).  *Modern
  Quantum Chemistry: Introduction to Advanced Electronic
  Structure Theory.*  Dover/McGraw-Hill.  The atomic-unit
  conventions follow this reference.
- **NIST Reference on Constants, Units, and Uncertainty**
  ([physics.nist.gov/cuu](<https://physics.nist.gov/cuu/Constants/>)).

### 8.1 Discrepancies with earlier tables

The 2019 CODATA recommended values of the *non-fixe`d*'
constants differ from the 2014 CODATA values at the level of
the 9th–11th significant figure; for the conversions in §4
the change is at the level of 1 part in $10^{9}$ and is
invisible at the 6-significant-figure precision used here.
For example, the 2014 CODATA value of the Hartree energy is
$E_h = 4.359\,744\,6499 \times 10^{-18}\;\text{J}$, whereas
the 2019 CODATA value is
$E_h = 4.359\,744\,7222 \times 10^{-18}\;\text{J}$; the
relative change is $1.7 \times 10^{-8}$.

### 8.2 What is *not* in this page

This page is **not** the source of the *physical* constants
used in a DFT calculation — those are the *input* to the
code, not the *output*.  Specifically:

- The **atomic-orbital basis** coefficients (Chapter 06 §6.3)
  are basis-set parameters, not physical constants; see the
  [EMSL basis-set exchange](<https://www.basissetexchange.org/>).
- The **nuclear charges** $Z_I$ of the chemical elements are
  integers, defined by the atomic number.
- The **Standard Model** constants (Fermi constant, CKM
  angles, …) do not enter DFT and are not listed here.
- The **isotopic masses** are tabulated by the
  [NIST Atomic Spectra Database](<https://www.nist.gov/pml/atomic-spectra-database>).

### 8.3 Recommended reading

- For a 20-page introduction to the 2019 SI redefinition:
  Newell, D. B. & Tiesinga, E. (2019), *Metrologi`a*'
  **56**, 022001.
- For the full 2019 CODATA adjustment: Tiesinga et al.
  (2021), *Rev. Mod. Phys.* **93**, 025010 — the primary
  source of every non-exact value in §2.
- For the historical development of atomic units:
  Petley, B. W. (1988), *The Fundamental Physical Constants
  and the Frontier of Measurement*, Adam Hilger.

> **Disclaimer.**  This page is a *reference*, not a primary
> source.  Cite the original CODATA adjustment, not this
> page, for any value used in a publication.  If you need
> more digits, go to the 2019 CODATA adjustment directly.

---

## Where to look for what you need

This page is the entry point.  The things that come up
*alongside* the constants live in:

- **Atomic-unit conventions** — [notation glossary §13.1]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}) and [Chapter 00 §"Notation"]({{ "/dft-notes/chapter-00/" | relative_url }}).
- **Mathematical identities** (commutators, Fourier transforms, special functions) — [math cheatsheet]({{ "/dft-notes/extras/math-cheatsheet/" | relative_url }}).
- **Notation of every symbol used in the chapters** — [notation glossary]({{ "/dft-notes/extras/notation-glossary/" | relative_url }}).
- **Software (basis sets, codes, plotting libraries)** — [software cheatsheet]({{ "/dft-notes/extras/software-cheatsheet/" | relative_url }}).
- **Bibliography (the references for the chapters)** — [bibliography]({{ "/dft-notes/extras/bibliography/" | relative_url }}).
