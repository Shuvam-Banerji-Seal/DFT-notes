---
layout: page
title: "Notation glossary"
permalink: /dft-notes/extras/notation-glossary/
description: >-
  A single, comprehensive reference for every symbol used across the
  DFT Notes chapters — scalars, vectors, operators, basis-set indices,
  special functions, crystallographic and relativistic notation, and
  the conventions (atomic units, Fourier transform, ERI definition)
  that hold throughout the notes.
keywords: "DFT, notation, glossary, atomic units, basis set, operators,
  crystallographic, relativistic, conventions, bra-ket, ERI,
  Fourier transform, Pauli, Dirac, Bloch, Brillouin"
---

# Notation glossary

> The single source of truth for *what every symbol means* in
> these notes.  If a chapter uses a symbol that is not listed
> here, it is a chapter-specific quantity; the chapter defines
> it at first use and the editor (you) should add it to this
> file in the same pull request.

This file is intentionally long (≈ 900 lines).  It is a
*reference*, not a chapter — open it, look up the symbol,
close it, return to the chapter.  The 13 sections correspond
to the 13 categories of symbols the DFT notes use, and the
conventions summary at the end pins down the cross-chapter
defaults.

The notation in this file is consistent with the rest of the
notes — in particular, with the *Notation* section of
[Chapter 00]({{ "/dft-notes/chapter-00/" | relative_url }})
and with the *Notation* callouts at the top of every later
chapter.  When a chapter deviates (e.g. SI units for a
spectroscopic result, natural units $\hbar = c = 1$ for a
relativistic digression), the deviation is announced at the
top of the chapter and is *not* repeated in this glossary.

For each symbol we give:

- the **LaTeX comman`d*`* (copy-pasteable),
- the **plain text** form (for editing or for notes in
  environments that don't render LaTeX),
- a one-line **description**,
- the **first appearance** in the notes (chapter and section),
  so a reader can trace the symbol back to its definition.

The chapters are numbered `00`–`13`.  Chapters `00`–`08` are
shipped; chapters `09`–`13` are listed in
[chapters-map.md]({{ "/dft-notes/chapters-map/" | relative_url }})
as planned.  Symbols that are introduced in a planned chapter
are flagged *(planned: ch-NN)*.

---

## 1. Scalars and constants

The fundamental constants of nature, the derived atomic units
of length and energy, and the dimensionless numbers used
throughout.

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\hbar$ | `\hbar` | h-bar | Reduced Planck constant ($h / 2\pi$); set to 1 in atomic units | Ch 00 §"Notation"; Ch 01 §1.1 |
| $m_e$ | `m_e` | m_e | Electron mass; set to 1 in atomic units | Ch 00 §"Notation" |
| $e$ | `e` | e | Elementary charge (magnitude); set to 1 in atomic units | Ch 00 §"Notation" |
| $4\pi\varepsilon_0$ | `4\pi\varepsilon_0` | 4 pi epsilon_0 | Vacuum permittivity; set to 1 in atomic units | Ch 01 §1.1 (implicit) |
| $c$ | `c` | c | Speed of light in vacuum; ≈ 137.036 a.u. | Ch 01 §1.10.7 |
| $a_0$ | `a_0` | a_0 | Bohr radius (≈ 0.529177 Å); unit of length in atomic units | Ch 00 §"Notation" |
| $E_h$ | `E_h` | E_h | Hartree energy (≈ 27.2114 eV); unit of energy in atomic units | Ch 00 §"Notation" |
| $k_B$ | `k_B` | k_B | Boltzmann constant; set to 1 in atomic units | Ch 07 §7.6.3 (smearing) |
| $\alpha$ | `\alpha` | alpha | Fine-structure constant $e^2/(\hbar c) \approx 1/137$ | Ch 01 §1.10.7 |
| $Z$ | `Z` | Z | Generic nuclear charge; $Z_I$ is the charge of nucleus $I$ | Ch 01 §1.1 |
| $Z_A$, $Z_I$ | `Z_A`, `Z_I` | Z_A, Z_I | Nuclear charge of atom/nucleus $A$ or $I$ | Ch 00 §"Notation"; Ch 01 §1.1 |
| $N$ | `N` | N | Number of electrons (always positive) | Ch 00 §"Notation"; Ch 01 §1.1 |
| $M$ | `M` | M | Number of nuclei (in a molecule) | Ch 01 §1.1 |
| $n$ | `n` | n | Principal quantum number (hydrogen, §1.10), or a generic band/state index (solids, ch 07) | Ch 01 §1.10 |
| $\ell$ | `\ell` | ell | Azimuthal (orbital angular momentum) quantum number; $\ell \ge 0$ | Ch 01 §1.10.2 |
| $m$ | `m` | m | Magnetic quantum number; $-\ell \le m \le \ell$ | Ch 01 §1.10.2 |
| $\omega$ | `\omega` | omega | Angular frequency (QHO, phonons, time-dependent perturbation) | Ch 01 §1.9; Ch 01 §1.8 |
| $T$ | `T` | T | Absolute temperature (smearing) or kinetic energy | Ch 07 §7.6.3 |
| $g_n$ | `g_n` | g_n | Degeneracy of the hydrogen shell $n$ ($= n^2$ in the non-relativistic case) | Ch 01 §1.10.5 |
| $\delta_n$ | `\delta_n` | delta_n | Quantum defect (Dirac hydrogenic spectrum) | Ch 04 §4.9.1 |
| $\eta$ | `\eta` | eta | Infinitesimal switching rate (adiabatic switching, $0^+$) | Ch 01 §1.8.1 |
| $\mu$ | `\mu` | mu | Reduced mass; in atomic units the electron mass | Ch 01 §1.10.1 |

**Conventions at a glance.**  Atomic units
($\hbar = m_e = e = 4\pi\varepsilon_0 = 1$) are used in every
chapter; see §13 below.  Lengths in Bohr, energies in Hartree.
Conversion factors ($1\,E_h \approx 27.2114$ eV,
$1\,a_0 \approx 0.529177$ Å) are stated once in
[Chapter 01 §1.1]({{ "/dft-notes/chapter-01/" | relative_url }})
and used without comment thereafter.

---

## 2. Vectors and tensors

Position vectors, momenta, lattice vectors, and the angular
momenta.  All vectors in this section are 3-D Euclidean
vectors; in this section and throughout, *bol`d*` indicates a
vector.  Operators on them are in §3. | Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\mathbf r$ | `\mathbf r` | **r** | Position of an electron in $\mathbb R^3$ | Ch 00 §"Notation" |
| $\mathbf r_i$ | `\mathbf r_i` | **r_i** | Position of the $i$-th electron | Ch 01 §1.1 |
| $\mathbf R$, $\mathbf R_A$, $\mathbf R_I$ | `\mathbf R`, `\mathbf R_A`, `\mathbf R_I` | **R**, **R_A**, **R_I** | Position(s) of nucleus/nuclei; $A$ and $I$ index nuclei | Ch 00 §"Notation"; Ch 01 §1.1 |
| $\mathbf A$, $\mathbf B$, $\mathbf C$, $\mathbf D$ | `\mathbf A` ... | **A** ... | Centres of basis functions (Gaussian primitives, GTOs) | Ch 06 §6.3 |
| $\mathbf p$ | `\mathbf p` | **`p*`* | Momentum vector; in atomic units $\hat{\mathbf p} = -i\nabla$ | Ch 01 §1.4 |
| $\mathbf k$ | `\mathbf k` | **`k*`* | Bloch wavevector / crystal momentum; lives in the first Brillouin zone | Ch 07 §7.1 |
| $\mathbf q$ | `\mathbf q` | **q** | Phonon wavevector; or a generic reciprocal-space vector in a response function | Ch 10 (planned); Ch 11 (planned) |
| $\mathbf G$ | `\mathbf G` | **G** | Reciprocal-lattice vector | Ch 07 §7.4.1 |
| $\mathbf a_1, \mathbf a_2, \mathbf a a_3$ | `\mathbf a_1, \mathbf a_2, \mathbf a_3` | **a_1, a_2, a_3** | Direct (Bravais) lattice primitive vectors | Ch 07 §7.2.1 |
| $\mathbf b_1, \mathbf b_2, \mathbf b_3$ | `\mathbf b_1, \mathbf b_2, \mathbf b_3` | **b_1, b_2, b_3** | Reciprocal-lattice primitive vectors, $\mathbf a_i \cdot \mathbf b_j = 2\pi\delta_{ij}$ | Ch 07 §7.4.1 |
| $\mathbf R$ | `\mathbf R` | **R** | Bravais-lattice vector; integer combination of the $\mathbf a_i$ | Ch 07 §7.1 |
| $\mathbf L$ | `\mathbf L` | **L** | Orbital angular momentum vector, $\mathbf L = \mathbf r \times \mathbf p$ | Ch 01 §1.10.2 |
| $\mathbf S$ | `\mathbf S` | **S** | Spin angular momentum vector, $\mathbf S = (\hbar/2)\boldsymbol\sigma$ | Ch 01 §1.4 (in $\hat L \cdot \hat S$); Ch 04 §4.9.2 |
| $\boldsymbol\sigma$ | `\boldsymbol\sigma` | **sigm`a*`* | Vector of Pauli matrices $(\sigma_x, \sigma_y, \sigma_z)$ | Ch 04 §4.8.4 |
| $\boldsymbol\alpha$, $\boldsymbol\beta$ | `\boldsymbol\alpha`, `\boldsymbol\beta` | **alph`a*`*, **bet`a*`* | Dirac matrices (4×4) in the standard representation | Ch 04 §4.9.1 |
| $\boldsymbol\rho$ | `\boldsymbol\rho` | **rho** | Relative electron–nuclear coordinate in the hydrogen atom ($\mathbf r - \mathbf R$) | Ch 01 §1.10.1 |
| $\hat{\mathbf r}$ | `\hat{\mathbf r}` | **r̂** | Unit vector $\mathbf r / r$ | Ch 01 §1.10 |
| $\hat{\mathbf n}$ | `\hat{\mathbf n}` | **n̂** | Generic unit vector (e.g. surface normal, polarisation) | Ch 04 §4.8 (implicit) |
| $\mathbf m$ | `\mathbf m` | **m** | Magnetisation density vector $(m_x, m_y, m_z)$ in non-collinear spin DFT | Ch 04 §4.8.4 |
| $\mathbf B$ | `\mathbf B` | **B** | External magnetic field (sometimes $\mathbf B_\text{xc}$, the XC magnetic field) | Ch 04 §4.8.4 |
| $\mathbf F_I$ | `\mathbf F_I` | **F_I** | Force on nucleus $I$ | Ch 04 §4.7.2 |
| $\boldsymbol\sigma$ (Pauli), $\boldsymbol\varepsilon$ | (see above) | — | Tensor / matrix symbols — see §4 (operators), §5 (DFT objects), and §9 (linear algebra) | Ch 04 §4.8.4 |

> **Tip.**  When a vector symbol also has an operator counterpart
> (e.g. $\mathbf r$ and $\hat{\mathbf r}$ are the same in
> position representation), the hat distinguishes the operator;
> the bare symbol is the eigenvalue, the corresponding
> classical variable, or the $c$-number coordinate.

---

## 3. Operators and quantum-mechanical objects

Hamiltonians, one-body operators, many-body operators, and the
states they act on.  Operators are written with hats; bras
and kets use Dirac's notation.

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\hat H$ | `\hat H` | H-hat | Hamiltonian (total); in chapters 01–05 typically the electronic Hamiltonian in the Born–Oppenheimer approximation | Ch 00 §"Notation"; Ch 01 §1.1 |
| $\hat T$ | `\hat T` | T-hat | Kinetic energy; in atomic units $\hat T = -\frac{1}{2}\sum_i \nabla_i^2$ | Ch 00 §"Notation"; Ch 01 §1.4 |
| $\hat V$ | `\hat V` | V-hat | Generic potential-energy operator | Ch 01 §1.4 |
| $\hat V_{en}$ | `\hat V_{en}` | V_en-hat | Electron–nuclear attraction, $-\sum_{i,A} Z_A / \lvert\mathbf r_i - \mathbf R_A\rvert$ | Ch 00 §"Notation"; Ch 01 §1.1 |
| $\hat V_{ee}$ / $\hat U_{ee}$ | `\hat V_{ee}`, `\hat U_{ee}` | V_ee-hat, U_ee-hat | Electron–electron repulsion, $\sum_{i<j} 1/r_{ij}$ | Ch 01 §1.1; Ch 01 §1.4 |
| $\hat V_{nn}$ | `\hat V_{nn}` | V_nn-hat | Nuclear–nuclear repulsion (a $c$-number in BO) | Ch 03 §3.5 |
| $\hat h$ | `\hat h` | h-hat | One-electron (core) Hamiltonian, $-\frac{1}{2}\nabla^2 + \hat v_\text{ext}$ | Ch 03 §3.2 |
| $\hat F$ | `\hat F` | F-hat | Fock operator, $\hat F = \hat h + \hat J[\rho] - \hat K[\rho]$ | Ch 00 §"Notation"; Ch 03 §3.2 |
| $\hat J[\rho]$ | `\hat J[\rho]` | J-hat | Coulomb (Hartree) operator; non-local; classical electrostatic potential of $\rho$ | Ch 00 §"Notation"; Ch 03 §3.2 |
| $\hat K[\rho]$ | `\hat K[\rho]` | K-hat | Exchange operator; non-local, non-Hermitian; $\hat F$ subtracts it | Ch 00 §"Notation"; Ch 03 §3.2 |
| $\hat H_\text{KS}$ | `\hat H_\text{KS}` | H_KS-hat | Kohn–Sham Hamiltonian, $-\frac{1}{2}\nabla^2 + v_\text{eff}$ | Ch 00 §"Notation"; Ch 04 §4.2 |
| $\hat v_\text{xc}$ | `\hat v_\text{xc}` | v_xc-hat | Exchange–correlation potential; functional derivative of $E_\text{xc}$ | Ch 00 §"Notation"; Ch 01 §1.4 |
| $\hat v_\text{ext}$ | `\hat v_\text{ext}` | v_ext-hat | External one-electron potential (electron–nuclear attraction in a molecule) | Ch 01 §1.4 |
| $\hat v_\text{eff}$ | `\hat v_\text{eff}` | v_eff-hat | Kohn–Sham effective potential, $v_\text{ext} + v_\text{H} + v_\text{xc}$ | Ch 04 §4.2 |
| $\hat v_\text{H}$ | `\hat v_\text{H}` | v_H-hat | Hartree (classical Coulomb) potential of the density | Ch 04 §4.2 |
| $\hat{\mathbf r}$ | `\hat{\mathbf r}` | r̂ | Position operator (multiplication by $\mathbf r$ in the position representation) | Ch 01 §1.4 |
| $\hat{\mathbf p}$ | `\hat{\mathbf p}` | p̂ | Momentum operator, $-i\nabla$ (atomic units) | Ch 01 §1.4 |
| $\hat L^2$, $\hat L_z$ | `\hat L^2`, `\hat L_z` | L²-hat, L_z-hat | Squared and z-component of the orbital angular momentum | Ch 01 §1.10.2 |
| $\hat S^2$, $\hat S_z$ | `\hat S^2`, `\hat S_z` | S²-hat, S_z-hat | Squared and z-component of the total spin | Ch 01 §1.2 (P3/P4); Ch 03 §3.7.5 |
| $\hat a$, $\hat a^\dagger$ | `\hat a`, `\hat a^\dagger` | a-hat, a†-hat | Annihilation / creation operators (harmonic oscillator, second quantisation) | Ch 01 §1.9.2 |
| $\hat n$ | `\hat n` | n-hat | Number operator, $\hat a^\dagger \hat a$ (QHO) | Ch 01 §1.9.2 |
| $\hat T_{\mathbf R}$ | `\hat T_{\mathbf R}` | T_R-hat | Bravais-lattice translation operator, $(\hat T_{\mathbf R} f)(\mathbf r) = f(\mathbf r + \mathbf R)$ | Ch 07 §7.3, step 1 |
| $\hat P_{ij}$ | `\hat P_{ij}` | P_ij-hat | Permutation operator; exchanges particles $i \leftrightarrow j$ | Ch 01 §1.4 |
| $\hat A_1$ | `\hat A_1` | A_1-hat | Quartet annihilator, $\hat S^2 - 15/4$ | Ch 03 §3.7.6 |
| $\hat U(t)$ | `\hat U(t)` | U(t)-hat | Time-evolution operator, $\exp(-i\hat H t)$ | Ch 01 §1.7.1 |
| $\hat U_I(t, t_0)$ | `\hat U_I(t, t_0)` | U_I(t,t0)-hat | Interaction-picture evolution operator (Dyson series) | Ch 01 §1.8.1 |
| $\hat V_I(t)$ | `\hat V_I(t)` | V_I(t)-hat | Interaction-picture perturbation operator | Ch 01 §1.8.1 |
| $\hat S$ | `\hat S` | S-hat | Generic action functional, or scattering matrix (context-dependent) | Ch 01 §1.7.2 |
| $\mathcal L$ | `\mathcal L` | L (script) | Lagrangian (TDVP, Ch 01 §1.7.2) or Liouvillian (open systems, planned) | Ch 01 §1.7.2 |
| $\hat{\mathcal F}$ | `\hat{\mathcal F}` | F (script) | SCF map from input density to output density (Ch 04 §4.6) | Ch 04 §4.6 |

### States (kets, bras, wavefunctions)

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\psi(\mathbf r)$ | `\psi(\mathbf r)` | ψ(**r**) | Generic one-electron wavefunction (molecular or atomic) | Ch 01 §1.1 |
| $\phi_i(\mathbf r)$ | `\phi_i(\mathbf r)` | φ_i(**r**) | $i$-th molecular orbital (Hartree–Fock or Kohn–Sham spatial orbital) | Ch 00 §"Notation"; Ch 03 §3.2 |
| $\phi_{n\mathbf k}(\mathbf r)$ | `\phi_{n\mathbf k}(\mathbf r)` | φ_{n**`k*`*}(**r**) | Bloch orbital; band index $n$, wavevector $\mathbf k$ | Ch 06 §6.7; Ch 07 §7.1 |
| $u_{n\mathbf k}(\mathbf r)$ | `u_{n\mathbf k}(\mathbf r)` | u_{n**`k*`*}(**r**) | Cell-periodic part of the Bloch orbital | Ch 06 §6.7; Ch 07 §7.1 |
| $\chi_p(\mathbf x)$ | `\chi_p(\mathbf x)` | χ_p(**x**) | Generic spin-orbital; $\mathbf x = (\mathbf r, \sigma)$ | Ch 02 §2.2 |
| $\chi_\mu(\mathbf r)$ | `\chi_\mu(\mathbf r)` | χ_μ(**r**) | A single AO (atomic-orbital) basis function | Ch 00 §"Notation"; Ch 03 §3.6 |
| $\Psi$ | `\Psi` | Ψ (capital) | Many-body wavefunction; $\Psi(\mathbf x_1, \dots, \mathbf x_N)$ | Ch 01 §1.1 |
| $\Phi$ | `\Phi` | Φ (capital) | Slater determinant; sometimes $\Phi_0$ for the HF / KS reference | Ch 02 §2.2; Ch 03 §3.1 |
| $\Phi_I$, $\Phi_J$ | `\Phi_I`, `\Phi_J` | Φ_I, Φ_J | Generic Slater determinants in a CI expansion | Ch 02 §2.2; Ch 03 §3.4 |
| $\rho(\mathbf r)$ | `\rho(\mathbf r)` | ρ(**r**) | One-electron ground-state density (3-D scalar field) | Ch 00 §"Notation"; Ch 01 §1.6 |
| $\rho(\mathbf x)$ | `\rho(\mathbf x)` | ρ(**x**) | One-electron density in spin-position space | Ch 02 §2.2 |
| $\rho^\alpha$, $\rho^\beta$ | `\rho^\alpha`, `\rho^\beta` | ρ^α, ρ^β | Spin-up / spin-down densities (collinear spin DFT) | Ch 04 §4.8.1 |
| $\rho(\mathbf r, \mathbf r')$ | `\rho(\mathbf r, \mathbf r')` | ρ(**r**, **r**') | One-particle density matrix (1-RDM) | Ch 03 §3.5 (refs); Ch 05 (refs) |
| $\lvert \phi \rangle$ | `\lvert \phi \rangle` | \|φ⟩ | Ket; element of the Hilbert space $\mathcal H$ | Ch 00 §"Notation" |
| $\langle \phi \rvert$ | `\langle \phi \rvert` | ⟨φ\| | Bra; dual vector | Ch 00 §"Notation" |
| $\langle \phi \rvert \psi \rangle$ | `\langle \phi \rvert \psi \rangle` | ⟨φ\|ψ⟩ | Inner product | Ch 00 §"Notation" |

---

## 4. Density-functional objects

The energy functionals, potentials, kernels, and other
quantities that are specific to Kohn–Sham DFT and appear in
chapters 04 and 05 (and downstream).

### Energy functionals

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $E[\rho]$ | `E[\rho]` | E[ρ] | Kohn–Sham total-energy functional of the density | Ch 00 §"Notation"; Ch 04 §4.1 |
| $F_\text{HK}[\rho]$ | `F_\text{HK}[\rho]` | F_HK[ρ] | Hohenberg–Kohn universal functional, $T + U_{ee}$ | Ch 04 §4.1 |
| $T_s[\rho]$ | `T_s[\rho]` | T_s[ρ] | Non-interacting (Kohn–Sham) kinetic-energy functional | Ch 04 §4.2 |
| $E_\text{xc}[\rho]$ | `E_\text{xc}[\rho]` | E_xc[ρ] | Exchange–correlation energy functional | Ch 00 §"Notation"; Ch 04 §4.2 |
| $E_x[\rho]$ | `E_x[\rho]` | E_x[ρ] | Exchange-only energy functional (HF exchange when $\rho$ is the HF density) | Ch 03 §3.5; Ch 05 §5.4 |
| $E_c[\rho]$ | `E_c[\rho]` | E_c[ρ] | Correlation energy functional, $E_\text{xc} - E_x$ | Ch 05 §5.4 |
| $J[\rho]$ | `J[\rho]` | J[ρ] | Hartree (classical Coulomb) energy, $\tfrac{1}{2}\int\!\int \rho\rho/r$ | Ch 04 §4.2 |
| $E_\text{HK}$ | `E_\text{HK}` | E_HK | Hohenberg–Kohn total energy (alternative notation for $E[\rho]$) | Ch 04 §4.1 |
| $E_\text{HF}$ | `E_\text{HF}` | E_HF | Hartree–Fock total energy (variational minimum) | Ch 03 §3.1 |
| $E_\text{corr}$ | `E_\text{corr}` | E_corr | Correlation energy, $E_\text{exact} - E_\text{HF}$ | Ch 03 §3.5 |

### Energies per particle / per unit volume

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\varepsilon_\text{xc}(\rho)$ | `\varepsilon_\text{xc}(\rho)` | ε_xc(ρ) | XC energy per particle of the uniform electron gas at density $\rho$ | Ch 05 §5.1 |
| $\varepsilon_\text{xc}(r_s)$ | `\varepsilon_\text{xc}(r_s)` | ε_xc(r_s) | Same, expressed in terms of the Wigner–Seitz radius $r_s$ | Ch 05 §5.1 |
| $r_s$ | `r_s` | r_s | Wigner–Seitz radius, $r_s = (3/4\pi n)^{1/3}$ | Ch 05 §5.1 |
| $k_\text{TF}$ | `k_\text{TF}` | k_TF | Thomas–Fermi screening wavevector | Ch 04 §4.6.4 |
| $\zeta(\mathbf r)$ | `\zeta(\mathbf r)` | ζ(**r**) | Relative spin polarisation, $(\rho_\uparrow - \rho_\downarrow)/\rho$ | Ch 04 §4.8.2 |

### Potentials and kernels

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $v_\text{xc}(\mathbf r)$ | `v_\text{xc}(\mathbf r)` | v_xc(**r**) | XC potential; $v_\text{xc} = \delta E_\text{xc}/\delta \rho$ | Ch 00 §"Notation"; Ch 04 §4.2 |
| $v_{\text{xc},\sigma}(\mathbf r)$ | `v_{\text{xc},\sigma}(\mathbf r)` | v_xc,σ(**r**) | Spin-dependent XC potential (collinear spin DFT) | Ch 04 §4.8.2 |
| $v_\text{H}[\rho](\mathbf r)$ | `v_\text{H}[\rho](\mathbf r)` | v_H[ρ](**r**) | Hartree potential of the density | Ch 04 §4.2 |
| $f_\text{xc}(\mathbf r, \mathbf r')$ | `f_\text{xc}(\mathbf r, \mathbf r')` | f_xc(**r**, **r**') | XC kernel, $\delta^2 E_\text{xc}/\delta\rho(\mathbf r)\delta\rho(\mathbf r')$ | Ch 12 (planned) |
| $\chi(\mathbf r, \mathbf r'; \omega)$ | `\chi(\mathbf r, \mathbf r'; \omega)` | χ(**r**, **r**'; ω) | Density–density response function (TDDFT) | Ch 11 (planned); Ch 12 (planned) |
| $\chi_0$ | `\chi_0` | χ_0 | Bare (non-interacting) response function, or a scalar density of states | Ch 04 §4.6.4 |
| $\epsilon(\mathbf q)$ | `\epsilon(\mathbf q)` | ε(**q**) | Dielectric function (response theory) | Ch 04 §4.6.4 |

### Ladder and Jacob's-ladder abbreviations

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| LDA | `\text{LDA}` | LDA | Local Density Approximation (uniform-gas XC) | Ch 04 §4.5; Ch 05 §5.1 |
| LSDA | `\text{LSDA}` | LSDA | Local Spin-Density Approximation (spin-polarised LDA) | Ch 04 §4.8.1 |
| GGA | `\text{GGA}` | GGA | Generalised Gradient Approximation (ρ and ∇ρ) | Ch 04 §4.5; Ch 05 §5.2 |
| meta-GGA | `\text{meta-GGA}` | meta-GGA | Adds the orbital kinetic-energy density τ | Ch 04 §4.5; Ch 05 §5.3 |
| SCAN | `\text{SCAN}` | SCAN | Strongly Constrained and Appropriately Normed (Sun, Ruzsinszky, Perdew 2015) | Ch 05 §5.3 |
| PBE | `\text{PBE}` | PBE | Perdew–Burke–Ernzerhof GGA (1996) | Ch 05 §5.2 |
| B3LYP | `\text{B3LYP}` | B3LYP | Becke-3-parameter hybrid with LYP correlation | Ch 05 §5.4 |
| B88 | `\text{B88}` | B88 | Becke 1988 exchange GGA | Ch 05 §5.2 |
| LYP | `\text{LYP}` | LYP | Lee–Yang–Parr correlation GGA | Ch 05 §5.2 |
| PBE0 | `\text{PBE0}` | PBE0 | "PBE with no parameters" — 25 % HF exchange + 75 % PBE exchange | Ch 05 §5.6 |
| HSE06 | `\text{HSE06}` | HSE06 | Heyd–Scuseria–Ernzerhof screened hybrid (ω = 0.11 bohr⁻¹) | Ch 05 §5.5 |
| RS | `\text{RS}` | RS | Range-separated (hybrid) | Ch 05 §5.5 |
| $\omega$ | `\omega` | omega | Range-separation parameter (bohr⁻¹) | Ch 05 §5.5 |

---

## 5. Many-body objects

The second-quantised machinery, Slater determinants, and the
many-body operators that act on Fock space.  Some of this
appears only in passing (chapters 02, 03, 04); the deeper
treatment is left to a future chapter on post-HF methods.

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\lvert \Phi \rangle$ | `\lvert \Phi \rangle` | \|Φ⟩ | Slater determinant (the canonical many-body state) | Ch 02 §2.2 |
| $\lvert \Phi_0 \rangle$ | `\lvert \Phi_0 \rangle` | \|Φ_0⟩ | Reference (HF or KS) Slater determinant | Ch 02 §2.2; Ch 03 |
| $\lvert i \rangle$, $\lvert f \rangle$ | `\lvert i \rangle`, `\lvert f \rangle` | \|i⟩, \|f⟩ | Initial / final state (Fermi's golden rule, time-dependent perturbation theory) | Ch 01 §1.8.3 |
| $\lvert n \rangle$ | `\lvert n \rangle` | \|n⟩ | $n$-th Fock state of the QHO (also: $n$-th stationary state of any Hamiltonian) | Ch 01 §1.9.2 |
| $\lvert 0 \rangle$ | `\lvert 0 \rangle` | \|0⟩ | Vacuum; lowest-weight state of the QHO | Ch 01 §1.9.2 |
| $\lvert \alpha \rangle$ | `\lvert \alpha \rangle` | \|α⟩ | Coherent state of the QHO, $\hat a \lvert \alpha \rangle = \alpha \lvert \alpha \rangle$ | Ch 01 §1.9.5 |
| $\hat T_1$ | `\hat T_1` | T_1-hat | Singles excitation operator (cluster / CI) | (planned: post-HF) |
| $\hat T_2$ | `\hat T_2` | T_2-hat | Doubles excitation operator | (planned: post-HF) |
| $\hat T = \hat T_1 + \hat T_2 + \cdots$ | `\hat T` | T-hat | Cluster operator (CC); exponential Ansatz $\lvert \Psi \rangle = e^{\hat T} \lvert \Phi_0 \rangle$ | (planned: post-HF) |
| $E_0$ | `E_0` | E_0 | Exact non-relativistic ground-state energy (in the given basis / Hamiltonian) | Ch 01 §1.1 |
| $E_\text{exact}$ | `E_\text{exact}` | E_exact | Same as $E_0$; used when emphasising the *exact* value | Ch 03 §3.5 |
| $E_\text{CBS}$ | `E_\text{CBS}` | E_CBS | Complete-basis-set limit energy | Ch 06 §6.2 |
| $E_n$ | `E_n` | E_n | Energy of the $n$-th stationary state; principal-quantum-number label in hydrogen | Ch 01 §1.1; Ch 01 §1.10 |
| $\varepsilon_i$ | `\varepsilon_i` | ε_i | Single-particle (orbital) energy; eigenvalue of $\hat F$ or $\hat H_\text{KS}$ | Ch 00 §"Notation"; Ch 03 §3.2 |
| $\varepsilon_{n\mathbf k}$ | `\varepsilon_{n\mathbf k}` | ε_{n**`k*`*} | Band energy: orbital energy indexed by band $n$ and wavevector $\mathbf k$ | Ch 07 §7.5.2 |
| $\varepsilon_F$ | `\varepsilon_F` | ε_F | Fermi energy | Ch 07 §7.6.2 |
| $\omega_{fi}$ | `\omega_{fi}` | ω_fi | Transition frequency $E_f - E_i$ | Ch 01 §1.8.3 |

---

## 6. Basis set notation

The index conventions used in chapters 03 (Hartree–Fock), 04
(Kohn–Sham), 06 (basis sets), and 07 (plane waves in
reciprocal space).

### Atomic-orbital (AO) basis

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\chi_\mu(\mathbf r)$ | `\chi_\mu(\mathbf r)` | χ_μ(**r**) | The $\mu$-th AO basis function, $\mu = 1, \dots, K$ | Ch 00 §"Notation"; Ch 03 §3.6 |
| $K$ | `K` | K | Number of contracted basis functions in the AO basis | Ch 03 §3.6 |
| $n_\mu$ | `n_\mu` | n_μ | Number of primitive Gaussians in contraction $\mu$ | Ch 06 §6.3 |
| $d_{\mu p}$ | `d_{\mu p}` | d_μp | Contraction coefficient; $p$ indexes the primitives within $\mu$ | Ch 06 §6.3 |
| $g(\mathbf r; \alpha, \mathbf A, \boldsymbol\ell)$ | `g(\mathbf r; \alpha, \mathbf A, \boldsymbol\ell)` | g(**r**; α, **A**, ℓ) | Primitive Cartesian Gaussian with exponent $\alpha$, centre $\mathbf A$, angular index $\boldsymbol\ell$ | Ch 06 §6.3 |
| $\alpha$ | `\alpha` | alpha | Gaussian exponent (a.u.⁻²); primitive-shell parameter | Ch 06 §6.3 |
| $\zeta$ | `\zeta` | zeta | Slater exponent (in STO-nG); $\alpha_p = \zeta^2 \alpha_p^{(0)}$ | Ch 06 §6.4 |
| $\mathbf A_\mu$ | `\mathbf A_\mu` | **A**_μ | Centre of basis function $\chi_\mu$ (atom coordinate) | Ch 04 §4.7.3; Ch 06 §6.3 |
| $\boldsymbol\ell = (\ell_x, \ell_y, \ell_z)$ | `\boldsymbol\ell` | ℓ | Angular-momentum vector for a Cartesian Gaussian | Ch 06 §6.3 |

### Molecular-orbital (MO) basis

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\phi_i(\mathbf r)$ | `\phi_i(\mathbf r)` | φ_i(**r**) | The $i$-th MO | Ch 00 §"Notation"; Ch 03 §3.6 |
| $C_{\mu i}$ | `C_{\mu i}` | C_μi | MO coefficient: the $\mu$-th basis-function contribution to the $i$-th MO | Ch 00 §"Notation"; Ch 03 §3.6 |
| $i, j, k, l$ | `i, j, k, l` | i, j, k, l | Occupied-orbital indices | Ch 00 §"Notation"; Ch 03 §3.6 |
| $a, b$ | `a, b` | a, b | Virtual (unoccupied) orbital indices | Ch 03 §3.4 (in $(\langle ab\rvert cd\rangle)$) |
| $p, q, r, s$ | `p, q, r, s` | p, q, r, s | General MO indices (occupied or virtual) | Ch 00 §"Notation"; Ch 02 §2.2 |
| $\alpha, \beta$ | `\alpha`, `\beta` | alpha, beta | Spin labels ($\alpha = \uparrow$, $\beta = \downarrow$); also used for Cartesian-Gaussian angular indices — context disambiguates | Ch 01 §1.2 (P6); Ch 02 §2.2; Ch 06 §6.3 |
| $\sigma$ | `\sigma` | sigma | Spin label in collinear spin DFT; also index in $(\mu\nu \rvert \rho\sigma)$ | Ch 03 §3.4; Ch 04 §4.8 |
| $\sigma$ (Pauli) | `\boldsymbol\sigma` | **sigm`a*`* | Vector of Pauli matrices; the bold distinguishes it from the spin label | Ch 04 §4.8.4 |
| $n$ | `n` | n | Number of doubly-occupied spatial orbitals in a closed-shell calculation, $N/2$ | Ch 03 §3.3 |
| $N_\alpha$, $N_\beta$ | `N_\alpha`, `N_\beta` | N_α, N_β | Number of $\alpha$-spin / $\beta$-spin electrons (UHF) | Ch 03 §3.7.1 |
| $S_z$ | `S_z` | S_z | $z$-component of the total spin, $(N_\alpha - N_\beta)/2$ | Ch 03 §3.7.1 |
| $\mathbf C$ | `\mathbf C` | **C** | Matrix of MO coefficients, $C_{\mu i}$ | Ch 00 §"Notation"; Ch 03 §3.6 |
| $\boldsymbol\varepsilon$ | `\boldsymbol\varepsilon` | **ε** | Diagonal matrix of orbital energies | Ch 00 §"Notation"; Ch 03 §3.6 |
| $\mathbf n$ | `\mathbf n` | **n** | Diagonal matrix of MO occupation numbers (general spin, fractional occupations) | Ch 03 §3.6 (problem 2) |

### Plane-wave basis

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\chi_{\mathbf G}^{\mathbf k}(\mathbf r) = \Omega^{-1/2} e^{i(\mathbf k + \mathbf G)\cdot\mathbf r}$ | `\chi_{\mathbf G}^{\mathbf k}(\mathbf r)` | χ_**G**^**`k*`*(**r**) | Plane-wave basis function | Ch 06 §6.7 |
| $E_\text{cut}$ | `E_\text{cut}` | E_cut | Kinetic-energy cutoff for the plane-wave basis | Ch 00 §"Notation"; Ch 06 §6.7 |
| $G_\text{max}$ | `G_\text{max}` | G_max | Largest retained $\lvert \mathbf k + \mathbf G \rvert$ | Ch 00 §"Notation"; Ch 06 §6.7 |
| $N_\text{PW}$ | `N_\text{PW}` | N_PW | Number of plane waves retained | Ch 00 §"Notation"; Ch 06 §6.7 |
| $c_{n\mathbf k}(\mathbf G)$ | `c_{n\mathbf k}(\mathbf G)` | c_{n**`k*`*}(**G**) | Plane-wave coefficient of the Bloch orbital | Ch 06 §6.7 |
| $E_\text{cut}^\text{grid}$ | `E_\text{cut}^\text{grid}` | E_cut^grid | Implicit kinetic cutoff of a real-space grid | Ch 06 §6.8 |
| $h$ | `h` | h | Real-space grid spacing (or: Planck's constant, in non-atomic-unit contexts) | Ch 06 §6.8 |
| $G_\text{Nyq}$ | `G_\text{Nyq}` | G_Nyq | Nyquist frequency of a real-space grid, $\pi/h$ | Ch 06 §6.8 |

### AO-basis matrices

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $S_{\mu\nu}$ | `S_{\mu\nu}` | S_μν | Overlap matrix element, $\langle \chi_\mu \rvert \chi_\nu \rangle$ | Ch 00 §"Notation"; Ch 03 §3.6 |
| $h_{\mu\nu}$ | `h_{\mu\nu}` | h_μν | Core-Hamiltonian matrix element, $\langle \chi_\mu \rvert \hat h \rvert \chi_\nu \rangle$ | Ch 03 §3.6.3 |
| $F_{\mu\nu}$ | `F_{\mu\nu}` | F_μν | Fock matrix element, $\langle \chi_\mu \rvert \hat F \rvert \chi_\nu \rangle$ | Ch 00 §"Notation"; Ch 03 §3.6 |
| $J_{\mu\nu}$ | `J_{\mu\nu}` | J_μν | Coulomb matrix element, $\langle \chi_\mu \rvert \hat J \rvert \chi_\nu \rangle$ | Ch 03 §3.6.3 |
| $K_{\mu\nu}$ | `K_{\mu\nu}` | K_μν | Exchange matrix element, $\langle \chi_\mu \rvert \hat K \rvert \chi_\nu \rangle$ | Ch 03 §3.6.3 |
| $P_{\mu\nu}$ | `P_{\mu\nu}` | P_μν | Density-matrix element, $2\sum_i C_{\mu i} C_{\nu i}^*$ (closed shell) | Ch 00 §"Notation"; Ch 03 §3.6.4 |
| $P^\alpha$, $P^\beta$ | `P^\alpha`, `P^\beta` | P^α, P^β | Spin-up / spin-down density matrices (UHF) | Ch 03 §3.7.2 |
| $P^s$ | `P^s` | P^s | Spin density matrix, $P^\alpha - P^\beta$ | Ch 03 §3.7.2 |
| $(\mu\nu \rvert \rho\sigma)$ | `(\mu\nu \rvert \rho\sigma)` | (μν\|ρσ) | Electron-repulsion integral (ERI) in **chemists'** notation | Ch 00 §"Notation"; Ch 03 §3.6.3 |
| $\langle \mu\nu \rvert \rvert \rho\sigma \rangle$ | `\langle \mu\nu \rvert \rvert \rho\sigma \rangle` | ⟨μν‖ρσ⟩ | ERI in **physicists'** notation, $\int\!\!\int \chi_\mu^*(\mathbf r_1) \chi_\nu(\mathbf r_1) (1/r_{12}) \chi_\rho^*(\mathbf r_2) \chi_\sigma(\mathbf r_2)\, d\mathbf r_1 d\mathbf r_2$ | Ch 03 §3.3 (comment) |
| $\mathbf S$, $\mathbf h$, $\mathbf F$, $\mathbf P$, $\mathbf C$ | `\mathbf S`, etc. | **S**, **`h*`*, **F**, **P**, **C** | The corresponding $K \times K$ matrices in the AO basis | Ch 03 §3.6 |
| $\mathbf G$ | `\mathbf G` | **G** | Two-electron part of the Fock matrix, $G_{\mu\nu} = J_{\mu\nu} - \tfrac{1}{2}K_{\mu\nu}$ (closed shell) | Ch 03 §3.6.5 |
| $\mathbf X$ | `\mathbf X` | **X** | Löwdin orthogonaliser, $\mathbf S^{-1/2}$ | Ch 03 §3.6.6 |

---

## 7. Special functions

The named functions and symbols that recur in derivations.

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $Y_\ell^m(\theta, \phi)$ | `Y_\ell^m(\theta, \phi)` | Y_ℓ^m(θ, φ) | Spherical harmonic; simultaneous eigenfunction of $\hat L^2$ and $\hat L_z$ | Ch 00 §"Notation"; Ch 01 §1.10.2 |
| $H_n(x)$ | `H_n(x)` | H_n(x) | Physicists' Hermite polynomial | Ch 00 §"Notation"; Ch 01 §1.9.4 |
| $L_n(x)$ | `L_n(x)` | L_n(x) | Laguerre polynomial | Ch 00 §"Notation"; Ch 06 (in STO radial functions) |
| $L_n^k(x)$ | `L_n^k(x)` | L_n^k(x) | Associated (generalised) Laguerre polynomial | Ch 01 §1.10.5 |
| $P_\ell^m(\cos\theta)$ | `P_\ell^m(\cos\theta)` | P_ℓ^m(cos θ) | Associated Legendre function | Ch 01 §1.10 (implicit) |
| $\delta_{ij}$ | `\delta_{ij}` | δ_ij | Kronecker delta: 1 if $i = j$, 0 otherwise | Ch 00 §"Notation"; Ch 01 §1.2 |
| $\delta(\mathbf r)$ | `\delta(\mathbf r)` | δ(**r**) | Dirac delta in 3-D | Ch 01 §1.8.4 (implicit) |
| $\delta(x)$ | `\delta(x)` | δ(x) | Dirac delta in 1-D | Ch 01 §1.8.4 |
| $\delta_t(\omega)$ | `\delta_t(\omega)` | δ_t(ω) | "Nascent" delta, $\sin(\omega t)/(\pi\omega)$ | Ch 01 §1.8.4 |
| $\varepsilon_{ijk}$ | `\varepsilon_{ijk}` | ε_ijk | Levi-Civita symbol (3-D totally antisymmetric tensor) | Ch 01 §1.4 (cross product) |
| $\operatorname{erf}(x)$ | `\operatorname{erf}(x)` | erf(x) | Error function, $\frac{2}{\sqrt\pi}\int_0^x e^{-u^2}\, du$ | Ch 00 §"Notation"; Ch 05 §5.5 |
| $\operatorname{erfc}(x)$ | `\operatorname{erfc}(x)` | erfc(x) | Complementary error function, $1 - \operatorname{erf}(x)$ | Ch 05 §5.5 |
| $F_0(t)$ | `F_0(t)` | F_0(t) | Boys function, $\int_0^1 e^{-t u^2}\, du = \tfrac{1}{2}\sqrt{\pi/t}\,\operatorname{erf}(\sqrt t)$ | Ch 00 §"Notation"; Ch 06 §6.3 |
| $F_n(t)$ | `F_n(t)` | F_n(t) | Higher-order Boys function (Ch 06 footnote) | Ch 06 §6.3 |
| $\Gamma(z)$ | `\Gamma(z)` | Γ(z) | Gamma function (factorial: $\Gamma(n+1) = n!$) | Ch 01 §1.9 (implicit) |
| $\Theta(x)$ | `\Theta(x)` | Θ(x) | Heaviside step function (Fermi–Dirac smearing, $T=0$) | Ch 07 §7.6.3 (implicit) |
| $\mathcal F[\,f\,]$ | `\mathcal F[f]` | F[f] | Functional (variational) derivative; also the Fourier transform (context-dependent) | Ch 04 §4.6 |
| $\delta f / \delta \rho$ | `\delta f / \delta \rho` | δf/δρ | Functional derivative of $f$ with respect to $\rho$ | Ch 04 §4.2 |

---

## 8. Common operator shorthands

The differential operators, inner products, commutators, and
shorthand notation that every chapter uses.

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\nabla$ | `\nabla` | ∇ (nabla) | Gradient; in Cartesian components $(\partial_x, \partial_y, \partial_z)$ | Ch 00 §"Notation"; Ch 01 §1.1 |
| $\nabla^2$ | `\nabla^2` | ∇² | Laplacian; $\sum_i \partial_{x_i}^2$ | Ch 00 §"Notation"; Ch 01 §1.1 |
| $\nabla_i$ | `\nabla_i` | ∇_i | Gradient with respect to the $i$-th electron's coordinates | Ch 01 §1.1 |
| $\int d\mathbf r$ | `\int d\mathbf r` | ∫ `d*`*r** | Volume integral over all of $\mathbb R^3$ | Ch 00 §"Notation"; Ch 03 §3.2 |
| $\int d\mathbf x$ | `\int d\mathbf x` | ∫ `d*`*x** | Volume + spin integral (sum over $\sigma$ implicit) | Ch 02 §2.2 |
| $\int d\Omega$ | `\int d\Omega` | ∫ dΩ | Angular integral over the unit sphere | Ch 01 §1.10 |
| $\partial / \partial x$ | `\partial / \partial x` | ∂/∂x | Partial derivative | Ch 00 §"Notation"; Ch 01 §1.3 |
| $\partial_t$ | `\partial_t` | ∂_t | Partial derivative with respect to time | Ch 00 §"Notation"; Ch 01 §1.2 (P5) |
| $\partial_\lambda$ | `\partial_\lambda` | ∂_λ | Partial derivative with respect to a parameter $\lambda$ (Hellmann–Feynman) | Ch 04 §4.7.1 |
| $\nabla \cdot \mathbf j$ | `\nabla \cdot \mathbf j` | ∇ · **j** | Divergence of the probability current | Ch 01 §1.7.4 |
| $\langle \psi \rvert \phi \rangle$ | `\langle \psi \rvert \phi \rangle` | ⟨ψ\|φ⟩ | Bra–ket inner product | Ch 00 §"Notation"; Ch 01 §1.2 |
| $\langle \hat A \rangle$ | `\langle \hat A \rangle` | ⟨A-hat⟩ | Expectation value $\langle \psi \rvert \hat A \rvert \psi \rangle$ | Ch 00 §"Notation"; Ch 01 §1.2 (P4) |
| $[\hat A, \hat B]$ | `[\hat A, \hat B]` | [A, B] | Commutator, $\hat A \hat B - \hat B \hat A$ | Ch 01 §1.4; Ch 01 §1.7.5 |
| $\{\hat A, \hat B\}$ | `\{\hat A, \hat B\}` | {A, B} | Anticommutator, $\hat A \hat B + \hat B \hat A$ | Ch 01 (rare) |
| $[\hat A, \hat B]_\pm$ | `[\hat A, \hat B]_\pm` | [A, B]_± | Commutator (upper) or anticommutator (lower sign) | Ch 01 (rare) |
| $\hat A^\dagger$ | `\hat A^\dagger` | A† | Hermitian conjugate (adjoint) | Ch 00 §"Notation"; Ch 01 §1.2 (P2) |
| $\text{c.c.}$ | `\text{c.c.}` | c.c. | Complex conjugate | Ch 03 §3.6 (implicit) |
| $\text{H.c.}$ | `\text{H.c.}` | H.c. | Hermitian conjugate (in informal contexts) | Ch 03 (rare) |
| $\text{Tr}$ | `\text{Tr}` | Tr | Trace (of a matrix) | Ch 03 §3.6.4 |
| $\det$ | `\det` | det | Determinant (of a matrix) | Ch 02 §2.2 |
| $\text{diag}(\dots)$ | `\text{diag}(\dots)` | diag(…) | Diagonal matrix with the given diagonal entries | Ch 03 §3.6.5 |
| $\lVert \mathbf v \rVert$ | `\lVert \mathbf v \rVert` | \|**v**\| | Vector 2-norm | Ch 03 §3.3 |
| $\lVert f \rVert$ | `\lVert f \rVert` | \|f\| | Function $L^2$ norm, $\sqrt{\langle f \rvert f \rangle}$ | Ch 01 §1.2 |

---

## 9. Linear-algebra notation

The conventions used in every chapter that touches a matrix
or a vector.  Vectors are lowercase bold ($\mathbf v$);
matrices are uppercase bold ($\mathbf A$).  The exception is
the bra–ket, which uses upright letters in Dirac notation
(see §3).

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\mathbf A$, $\mathbf B$ | `\mathbf A`, `\mathbf B` | **A**, **B** | Generic matrices | Ch 00 §"Notation" |
| $\mathbf v$, $\mathbf w$ | `\mathbf v`, `\mathbf w` | **v**, **w** | Generic column vectors | Ch 00 §"Notation" |
| $A_{ij}$ | `A_{ij}` | A_ij | The $(i, j)$ matrix element | Ch 00 §"Notation" |
| $v_i$ | `v_i` | v_i | The $i$-th component of $\mathbf v$ | Ch 00 §"Notation" |
| $\mathbf A^T$ | `\mathbf A^T` | **A**^T | Transpose | Ch 00 §"Notation" |
| $\mathbf A^\dagger$ | `\mathbf A^\dagger` | **A**† | Conjugate transpose (Hermitian adjoint) | Ch 00 §"Notation"; Ch 03 §3.6.6 |
| $\mathbf A^*$ | `\mathbf A^*` | **A*** | Element-wise complex conjugate (rarely used alone) | Ch 03 (rare) |
| $\mathbf A^{-1}$ | `\mathbf A^{-1}` | **A**⁻¹ | Matrix inverse | Ch 03 §3.6.6 (Löwdin) |
| $\mathbf A^{-1/2}$ | `\mathbf A^{-1/2}` | **A**^{-1/2} | Inverse square root (defined for positive-definite $\mathbf A$) | Ch 03 §3.6.6 |
| $\mathbf I$ / $\mathbf 1$ | `\mathbf I`, `\mathbf 1` | **I**, **1** | Identity matrix (of the appropriate size) | Ch 00 §"Notation"; Ch 01 §1.2 (P1) |
| $\mathbf 0$ | `\mathbf 0` | **0** | Zero matrix or zero vector | Ch 03 (implicit) |
| $\text{Tr}(\mathbf A)$ | `\text{Tr}(\mathbf A)` | Tr(**A**) | Trace | Ch 03 §3.6.4 |
| $\det(\mathbf A)$ | `\det(\mathbf A)` | det(**A**) | Determinant | Ch 00 §"Notation"; Ch 02 §2.1 |
| $\mathbf A \otimes \mathbf B$ | `\mathbf A \otimes \mathbf B` | **A** ⊗ **B** | Tensor (Kronecker) product | Ch 02 §2.1 (implicit) |
| $\langle \mathbf u, \mathbf v \rangle$ | `\langle \mathbf u, \mathbf v \rangle` | ⟨**u**, **v**⟩ | Euclidean inner product, $\sum_i u_i^* v_i$ | Ch 00 §"Notation" |
| $\mathbf u \cdot \mathbf v$ | `\mathbf u \cdot \mathbf v` | **u** · **v** | Euclidean inner product (real vectors) | Ch 00 §"Notation" |
| $\text{einsum}$ | `\text{einsum}` | einsum | NumPy's Einstein summation convention (programming shorthand) | Ch 03 §3.3 |
| $\boldsymbol\Lambda$ | `\boldsymbol\Lambda` | **Λ** | Diagonal matrix of eigenvalues | Ch 00 §"Notation" (linear-algebra bullet) |
| $\mathbf U$ | `\mathbf U` | **U** | Unitary matrix (e.g. $\mathbf A = \mathbf U \boldsymbol\Lambda \mathbf U^\dagger$) | Ch 00 §"Notation" (linear-algebra bullet) |
| $\sigma(\hat H)$ | `\sigma(\hat H)` | σ(H-hat) | Spectrum of $\hat H$ | Ch 01 §1.1 |
| $\rho(\mathbf A)$ | `\rho(\mathbf A)` | ρ(**A**) | Spectral radius of $\mathbf A$ | Ch 04 §4.6.2 |
| $\lVert \mathbf A \rVert$ | `\lVert \mathbf A \rVert` | \|**A**\| | Matrix norm (operator, Frobenius, etc.; usually clear from context) | Ch 03 §3.3 |
| $O(\cdot)$ | `O(\cdot)` | O(·) | Big-O notation (asymptotic scaling) | Ch 03 §3.8 |
| $o(\cdot)$ | `o(\cdot)` | o(·) | Little-o notation | Ch 01 §1.8 |

---

## 10. Crystallographic notation

The notation that enters with chapter 07 (solids & PBC) and
is reused in chapters 08 (pseudopotentials), 10 (phonons),
and 11 (band structures).

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\mathbf a_1, \mathbf a_2, \mathbf a_3$ | `\mathbf a_1`, `\mathbf a_2`, `\mathbf a_3` | **a_1, a_2, a_3** | Direct-lattice primitive vectors | Ch 07 §7.2.1 |
| $\mathbf b_1, \mathbf b_2, \mathbf b_3$ | `\mathbf b_1`, `\mathbf b_2`, `\mathbf b_3` | **b_1, b_2, b_3** | Reciprocal-lattice primitive vectors, $\mathbf a_i \cdot \mathbf b_j = 2\pi\delta_{ij}$ | Ch 07 §7.4.1 |
| $\mathbf R = n_1 \mathbf a_1 + n_2 \mathbf a_2 + n_3 \mathbf a_3$ | `\mathbf R` | **R** | Generic Bravais-lattice vector ($n_i \in \mathbb Z$) | Ch 07 §7.1 |
| $\mathbf G = h \mathbf b_1 + k \mathbf b_2 + l \mathbf b_3$ | `\mathbf G` | **G** | Reciprocal-lattice vector ($h, k, l \in \mathbb Z$) | Ch 07 §7.4.1 |
| $\mathbf k$ | `\mathbf k` | **`k*`* | Crystal momentum / Bloch wavevector; lives in the 1st BZ | Ch 07 §7.1 |
| $\mathbf q$ | `\mathbf q` | **q** | Phonon wavevector; or a generic reciprocal-space wavevector in a response function | Ch 10 (planned); Ch 11 (planned) |
| $\Omega$ | `\Omega` | Ω | Volume of the primitive cell; also: supercell volume in BvK | Ch 00 §"Notation"; Ch 07 §7.5.1 |
| $V_\text{cell}$ | `V_\text{cell}` | V_cell | Same as $\Omega$ (alternative notation) | Ch 07 §7.4.1 |
| $V_\text{BZ}^*$ | V_\text{BZ}^*` | V_BZ | Volume of the reciprocal primitive cell, $(2\pi)^3 / V_\text{cell}$ | Ch 07 §7.4.1 |
| $\Gamma$ | `\Gamma` | Γ | Centre of the Brillouin zone, $\mathbf k = \mathbf 0$ | Ch 07 §7.4.3 |
| $X$, $L$, $W$, $K$, $U$ | `X`, `L`, `W`, `K`, `U` | X, L, W, K, U | High-symmetry points of the FCC Brillouin zone (Setyawan–Curtarolo) | Ch 07 §7.4.3 |
| $N_\mathbf k$ | `N_\mathbf k` | N_**`k*`* | Number of $\mathbf k$-points in the BZ sampling mesh | Ch 07 §7.2.2 |
| $w_\mathbf k$ | `w_\mathbf k` | w_**`k*`* | Weight of $\mathbf k$-point in the BZ sum | Ch 07 §7.2.2 |
| $N_1, N_2, N_3$ | `N_1`, `N_2`, `N_3` | N_1, N_2, N_3 | BvK supercell dimensions; also Monkhorst–Pack mesh sizes | Ch 07 §7.2.1 |
| $m_i$ | `m_i` | m_i | Monkhorst–Pack mesh index along direction $i$ | Ch 07 §7.6.1 |
| $a$ | `a` | a | Cubic lattice parameter (when applicable) | Ch 07 §7.4.3 |
| $V_{ps,l}(r)$ | `V_{ps,l}(r)` | V_ps,l(r) | Channel-dependent pseudopotential | Ch 08 §8.1 |
| $r_c$ | `r_c` | r_c | Pseudopotential cutoff radius | Ch 08 §8.1 |
| $\phi_l(r)$ | `\phi_l(r)` | φ_l(r) | Pseudo-wavefunction in channel $l$ | Ch 08 §8.1 |
| $u_l(r)$ | `u_l(r)` | u_l(r) | All-electron radial wavefunction in channel $l$ | Ch 08 §8.1 |
| $E_l$ | `E_l` | E_l | Valence eigenvalue used to construct the pseudo | Ch 08 §8.1 |
| $D_l(E)$ | `D_l(E)` | D_l(E) | Logarithmic derivative of the radial wavefunction at $r_c$ | Ch 08 §8.3 |
| $Z_\text{core}$ | `Z_\text{core}` | Z_core | Number of core electrons removed by the pseudopotential | Ch 08 §8.2 |

> **Warning.**  The labels $K$ and $L$ are reused across
> chapters: $K$ is the *basis size* in chapters 03 and 06, the
> *Bloch wavevector* $\mathbf k$ in chapter 07, and a
> *high-symmetry point* in chapter 07 (the FCC band-structure
> path).  $L$ is the *angular-momentum quantum number* in
> chapter 01 and a *high-symmetry point* in chapter 07. The
> context always disambiguates.

---

## 11. Phonon notation

The symbols that appear in chapter 10 (phonons & vibrations,
planned) and the sections of chapters 04 and 09 that
prefigure it.

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\omega$ | `\omega` | omega | Phonon angular frequency | (planned: ch 10) |
| $\omega_\nu(\mathbf q)$ | `\omega_\nu(\mathbf q)` | ω_ν(**q**) | Frequency of branch $\nu$ at wavevector $\mathbf q$ | (planned: ch 10) |
| $\mathbf q$ | `\mathbf q` | **q** | Phonon wavevector (lives in the 1st BZ) | (planned: ch 10) |
| $D_{ij}(\mathbf R)$ | `D_{ij}(\mathbf R)` | D_ij(**R**) | Force-constant matrix between atoms in cell $\mathbf 0$ and cell $\mathbf R$ | (planned: ch 10) |
| $D_{ij}(\mathbf q)$ | `D_{ij}(\mathbf q)` | D_ij(**q**) | Dynamical matrix: Fourier transform of $D_{ij}(\mathbf R)$ | (planned: ch 10) |
| $M_I$ | `M_I` | M_I | Mass of nucleus $I$ (in units of $m_e$) | (planned: ch 10) |
| $F_{\mu\nu}^\text{ph}$ | `F_{\mu\nu}^\text{ph}` | F_μν^ph | Phonon force-constant supermatrix (mass-weighted) | (planned: ch 10) |
| $e_{I\alpha,\nu}(\mathbf q)$ | `e_{I\alpha,\nu}(\mathbf q)` | e_{Iα,ν}(**q**) | Phonon polarisation vector: displacement of atom $I$ in direction $\alpha$ for branch $\nu$ | (planned: ch 10) |
| $\epsilon_{\alpha\beta}$ | `\epsilon_{\alpha\beta}` | ε_αβ | Strain tensor; or symmetrised strain in elasticity | Ch 04 §4.7.4 |
| $\sigma_{\alpha\beta}$ | `\sigma_{\alpha\beta}` | σ_αβ | Stress tensor | Ch 04 §4.7.4 |

---

## 12. Relativistic notation

The symbols that enter with chapter 04 §4.9 (relativistic KS
DFT) and that are flagged for the planned chapters 12 (TDDFT,
where spin–orbit is sometimes needed) and 13 (DFT+U &
beyond).

| Symbol | LaTeX | Plain text | Description | First appearance |
|:------|:------|:-----------|:------------|:-----------------|
| $\boldsymbol\alpha$ | `\boldsymbol\alpha` | **alph`a*`* | Dirac matrix (vector of three 4×4 matrices) | Ch 04 §4.9.1 |
| $\boldsymbol\beta$ | `\boldsymbol\beta` | **bet`a*`* | Dirac matrix (single 4×4 matrix) | Ch 04 §4.9.1 |
| $\gamma^5 = \gamma_5$ | `\gamma^5`, `\gamma_5` | γ⁵, γ_5 | Chirality matrix, $i \gamma^0 \gamma^1 \gamma^2 \gamma^3$ in the Dirac representation | Ch 04 §4.9 (referenced) |
| $\sigma^{\mu\nu} = \tfrac{i}{2}[\gamma^\mu, \gamma^\nu]$ | `\sigma^{\mu\nu}` | σ^{μν} | Generator of Lorentz transformations on Dirac spinors; appears in the spin–orbit coupling | Ch 04 §4.9.2 (implicit) |
| $\hat H_\text{Dirac}$ | `\hat H_\text{Dirac}` | H_Dirac-hat | Dirac Hamiltonian, $c\,\boldsymbol\alpha \cdot \hat{\mathbf p} + \boldsymbol\beta mc^2 + v(\mathbf r)$ | Ch 04 §4.9.1 |
| $\Phi^L$, $\Phi^S$ | `\Phi^L`, `\Phi^S` | Φ^L, Φ^S | "Large" and "small" 2-component spinors of the Dirac 4-spinor | Ch 04 §4.9.2 |
| $\xi(r)$ | `\xi(r)` | ξ(r) | Spin–orbit coupling strength; $\xi(r) = (1/2m^2 c^2 r)(dv/dr)$ | Ch 04 §4.9.2 |
| $\hat H_\text{SO}$ | `\hat H_\text{SO}` | H_SO-hat | Spin–orbit coupling operator, $\xi(r) \hat{\mathbf L} \cdot \hat{\mathbf S}$ | Ch 04 §4.9.2 |
| $\hat H_\text{Pauli}$ | `\hat H_\text{Pauli}` | H_Pauli-hat | Pauli (non-relativistic limit) Hamiltonian, $\hat H_\text{Pauli} = \hat p^2/2m + v + \cdots$ | Ch 04 §4.9.2 |
| $\Delta_\text{x}$ | `\Delta_\text{x}` | Δ_x | Exchange splitting (spin-up vs spin-down band shift) | Ch 04 §4.8.3 |
| $\Delta E_\text{BSIE}$ | `\Delta E_\text{BSIE}` | ΔE_BSIE | Basis-set incompleteness error (alias $\Delta E_\text{BSIE}(K)$) | Ch 06 §6.2 |
| $\mathbf B_\text{xc}(\mathbf r)$ | `\mathbf B_\text{xc}(\mathbf r)` | **B**_xc(**r**) | XC magnetic field in non-collinear spin DFT, $\delta E_\text{xc}/\delta \mathbf m$ | Ch 04 §4.8.4 |
| $\zeta$ (relativistic) | `\zeta` | zeta | Speed ratio $v/c$ (in the Pauli expansion); often written $v/c$ | Ch 04 §4.9.2 |

> **Note.**  The spin label $\sigma$ used in collinear spin
> DFT (chapter 04 §4.8) and the Pauli-matrix vector
> $\boldsymbol\sigma$ (chapter 04 §4.8.4 onward) are
> deliberately the same Greek letter; the boldface
> $\boldsymbol\sigma$ identifies the *matrix* unambiguously.
> In inline text the bare $\sigma$ is the spin label.

---

## 13. Conventions summary

The cross-chapter defaults that hold unless a chapter
explicitly overrides them.  When a chapter *does* override
(e.g. SI units for a spectroscopy result, atomic units for
the hydrogen 1s example), the override is announced at the
top of the chapter.

### 13.1 Atomic units

**Default throughout the notes: atomic units.**
$\hbar = m_e = e = 4\pi\varepsilon_0 = 1$.  Lengths in Bohr
($a_0 \approx 0.529177$ Å); energies in Hartree
($E_h \approx 27.2114$ eV); charges in units of $e$; masses
in units of $m_e$.  Times are in $\hbar/E_h \approx 2.4189
\times 10^{-17}$ s.  The kinetic-energy operator for a
single electron is $-\tfrac{1}{2}\nabla^2$ (not
$-\hbar^2/2m \nabla^2$); the Coulomb interaction between two
charges is $1/r$ (not $e^2/4\pi\varepsilon_0 r$).

### 13.2 Sign convention for the Fourier transform

**Default convention:**

$$
\tilde f(\mathbf k) = \int_{\mathbb R^3} f(\mathbf r)\,
e^{-i \mathbf k \cdot \mathbf r}\, d\mathbf r ,
\qquad
f(\mathbf r) = \int_{\mathbb R^3} \tilde f(\mathbf k)\,
e^{+i \mathbf k \cdot \mathbf r}\, \frac{d\mathbf k}{(2\pi)^3} .
$$

The plane wave basis in chapter 06 / 07 follows the same
convention: $\chi_{\mathbf G}^\mathbf k(\mathbf r) =
\Omega^{-1/2} e^{+i(\mathbf k + \mathbf G) \cdot \mathbf r}$.
The opposite sign convention is used in some engineering
texts; check when reading a citation.

### 13.3 Definition of the ERI

The notes use the **chemists' notation** for the
electron-repulsion integral (ERI):

$$
(\mu\nu \rvert \rho\sigma)
\;\equiv\;
\int\!\!\int
\chi_\mu^*(\mathbf r_1)\, \chi_\nu(\mathbf r_1)\,
\frac{1}{\lvert \mathbf r_1 - \mathbf r_2\rvert}\,
\chi_\rho^*(\mathbf r_2)\, \chi_\sigma(\mathbf r_2)\,
d\mathbf r_1\, d\mathbf r_2 .
$$

The bar separates the bra pair $(\mu\nu\rvert$ from the
ket pair $\rvert \rho\sigma)$.  The **physicists'
notation** $\langle \mu\nu \rvert \rvert \rho\sigma\rangle$
differs only by $1/r_{12} \to 1/r_{12}$ ordering (the
physicists' integral is $(\mu\rho \rvert \nu\sigma)$ in
chemists' notation).  The 8-fold permutational symmetry
(Ch 03 §3.6.3) holds for both notations with real basis
functions:

$$
(\mu\nu \rvert \rho\sigma) = (\nu\mu \rvert \rho\sigma) = (\mu\nu \rvert \sigma\rho) = (\rho\sigma \rvert \mu\nu) = \cdots
$$

### 13.4 Matrix sign and order

- $\mathbf F \mathbf C = \mathbf S \mathbf C \boldsymbol\varepsilon$
  is the Roothaan–Hall GEP, with the Fock matrix on the
  *left*.  The MO coefficients are the columns of
  $\mathbf C$.
- The density matrix in a closed-shell calculation is
  $\mathbf P = 2 \mathbf C_\text{occ} \mathbf C_\text{occ}^\dagger$.
- The HF energy in the AO basis is
  $E_\text{el} = \tfrac{1}{2} \text{Tr}[\mathbf P(\mathbf h + \mathbf F)]$;
  the *hal`f*` accounts for the double-counting correction in
  $\text{Tr}[\mathbf P \mathbf F]$.

### 13.5 Occupation and spin

- **Restricted (closed-shell):** all spatial orbitals doubly
  occupied, $N$ even, $N/2$ spatial orbitals.
  $\rho(\mathbf r) = 2\sum_{i=1}^{N/2} |\phi_i(\mathbf r)|^2$.
- **Unrestricted (UHF):** $\alpha$ and $\beta$ spatial
  orbitals are *different*; occupations $N_\alpha \ge N_\beta$.
  $S_z = (N_\alpha - N_\beta)/2$.
- **Restricted open-shell (ROHF):** open-shell electrons are
  unpaired, but the wavefunction is a spin eigenfunction.  See
  Ch 03 §3.7.7 for the trade-off vs UHF.

### 13.6 Phonon and band index conventions

- **Bands:** $n$ is the band index, $\mathbf k$ the
  wavevector.  In equation labels, $\varepsilon_{n\mathbf k}$.
- **Phonons:** $\nu$ is the branch index, $\mathbf q$ the
  wavevector.  In equation labels, $\omega_\nu(\mathbf q)$.
- **Conventions differ by community** (e.g. solid-state
  physics uses $\mathbf k$ for electrons, $\mathbf q$ for
  phonons; some optics texts swap them).  The DFT Notes
  follow the solid-state convention.

### 13.7 Where to look for deviations

| Chapter | Override |
|:--------|:---------|
| Ch 01 §1.10.7 | SI factors pulled in for the hydrogen 2p→1s spontaneous emission rate ($\alpha$, $c$). |
| Ch 01 §1.8.3 | Conventional TDPT prefactor $1/\hbar$ in SI; set to 1 in atomic units. |
| Ch 04 §4.9.1 | Dirac equation written with $\hbar$ and $c$ explicit, then Pauli limit recovers atomic units. |
| Ch 05 §5.4 | B3LYP coefficients drawn from the original 1994 paper; the *form* is a linear combination of five components, not an atomic-units statement. |
| Ch 07 §7.6.3 | Fermi–Dirac smearing introduced with $k_B$ explicit; in atomic units $k_B = 1$. |

If a chapter introduces a symbol *not* in this glossary, the
chapter's *first use* is the canonical definition, and a
one-line PR that adds the symbol to this file is the right
follow-up.

---

> **Cross-references.**
> [Chapter 00 §"Notation"]({{ "/dft-notes/chapter-00/" | relative_url }})
> is the in-chapter version of this glossary.  This file is
> the cross-chapter, cross-volume single source of truth.
> When in doubt, the more recent of the two definitions
> wins; the QA reviewer is responsible for catching any
> drift.
