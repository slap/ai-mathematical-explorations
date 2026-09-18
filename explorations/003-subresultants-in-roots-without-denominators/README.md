<!-- meta:start -->
# Subresultants in roots without denominators

**Status:** 🟠 Unverified \
**Area:** Computer Algebra / Symmetric Functions \
**Date:** 2026-09-15 \
**AI system:** Claude Opus 5 (Anthropic), model claude-opus-5 — via Claude Code \
**Published by:** Santiago Laplagne
<!-- meta:end -->

📄 **[Read the paper (PDF, 10 pages)](exploration.pdf)** · [LaTeX source](source.tex) ·
[original AI output](ai-output.md) · [computations](computations/)

### Summary

The formulas of D'Andrea, Krick and Szanto express the subresultants of two univariate
polynomials in terms of the roots of one of them, but as a *ratio*: a determinant `|O_S|`
divided by the Vandermonde determinant `V` of those roots. **The AI-generated paper published
here** claims that the division is always exact over ℤ, and identifies the quotient
`P_S = |O_S| / V` as a multi-Schur function of Lascoux in two alphabets — the roots of `g`
and the difference of the two root alphabets — in three equivalent explicit forms. In the
classical case the quotient collapses to a single supersymmetric Schur function indexed by a
rectangle, which recovers a theorem of Lascoux and Pragacz; a determinant of divided
differences settles multiple roots; and the naive multivariate analogue is shown to be false.

### Research context

The question I put to the model was whether the rational expressions of [DKS05] can be
replaced by formulas that are universally polynomial in the roots, with an explicit
description of those polynomials. I gave it that problem statement, split into four lines —
prove the divisibility, find the quotient, express it in a natural basis of symmetric
functions, extend to multiple roots and to the multivariate case — and then only asked it to
close the third line before moving on, and to collect what it had into a paper. Beyond that
initial prompt there was no intervention of mine: the approach, the proofs, the computations
and the write-up are entirely the model's. The same session produced
[exploration 002](../002-non-redundancy-of-the-casas-alvero-conditions/), on the
Casas–Alvero conjecture.

### The mathematical claim

Let `f, g` be generic of degrees `d₁, d₂`, let `Ξ = {ξ₁,…,ξ_{d₂}}` be the roots of `g` and
`A = {α₁,…,α_{d₁}}` those of `f`, let `V = ∏_{i<j}(ξ_j − ξ_i)`, and let `O_S` be the matrix of
[DKS05, Thm. 2.2], whose rows are the evaluations at the roots of `g` of the monomials of `S`
and of the shifts `xⁱf`. Write `P_S := |O_S| / V`.

> **Theorem 3.2 (divisibility).** `V` divides `|O_S|` in `ℤ[a₀,…,a_{d₁}][ξ₁,…,ξ_{d₂}]`, and
> the quotient `P_S` is symmetric in the roots.
>
> **Theorem 5.1 (multi-Schur form, with the exact sign).** For *any* ordering `τ` of the rows,
> `P_S = (−1)^{C(d₂,2)} · sgn(τ) · det( X_{ε_{τ(i)}−d₂+q}(A_{τ(i)}) )`, a Jacobi–Trudi
> determinant with one alphabet per row: `Ξ` on the monomial rows, `Ξ − A` on the `f`-rows.
>
> **Theorem 6.1 (the classical case is a rectangle).** For `S_k = {1,x,…,x^{k−1}}`,
> `P_{S_k} = a_{d₁}^{d₂−k} · s_{((d₁−k)^{d₂−k})}(Ξ − A)`, with sign `+1`.

Around these: a Schur expansion whose coefficients are the maximal minors of the band matrix
of `f` (Thm. 4.1, Cauchy–Binet); the dual expansion in the basis `{s_ν(Ξ − A)}`, whose
coefficients are *skew* Schur functions `s_{λ/μ}(A)` with an explicit vanishing criterion
(Thm. 8.1, Cor. 8.2); the Toeplitz/Padé reading of the principal coefficient as a determinant
in the Taylor coefficients of `f/g` at infinity (Thm. 7.1); the Newton form
`P_S = det(R_i[ξ₁,…,ξ_j])` as a determinant of divided differences, which gives the
multiple-root case at once (Thm. 9.1, Cor. 9.2); and a negative result, that the naive
multivariate analogue of the divisibility statement fails already for four points of the plane
(Prop. 10.1).

### Verification status

> The results have not been independently verified. The arguments should be regarded as
> conjectural until checked.

What is on record, none of which counts as verification:

- **The paper's own §11.** Every statement was tested by symbolic computation by the AI
  itself, in two independent implementations (SymPy 1.14 and SageMath 10.7), with the Schur
  expansions cross-checked against SageMath's native symmetric function routines. The section
  gives the exact range for each statement; the scripts and their raw output are in
  [`computations/`](computations/). This is evidence that the statements are true in the cases
  tested, not that the proofs are correct.
- **The end-to-end check** at the end of §11 is the one worth a reader's attention: for 20
  tuples it compares `P_S` against the *classical* determinantal definition of the scalar
  subresultant, with exact signs, without assuming the DKS formula.
- **What the AI flagged itself.** The bibliographic data of [Hong], [DKS13], [DHKS] and
  [DKS15] were written from memory and are not checked — a `% TODO` to that effect is still in
  the source. The paper does not claim novelty for Theorem 6.1, which it presents as
  recovering Lascoux–Pragacz.

Points a reader might go to first: the sign in Theorem 5.1, which was observed computationally
before it was proved, and which came out `−1` in a small case with ties among the `ε_i`; the
confluent Corollary 9.2, whose proof was rewritten during the write-up; and the normalisation
`H₀ = a_{d₁} ≠ 1`, which makes the *size* of every Jacobi–Trudi determinant in the paper
matter.

### Verification record

| Date | Status | By | Reference |
| --- | --- | --- | --- |
| 2026-09-15 | 🟠 Unverified | — | published as generated |

### Files

- [exploration.pdf](exploration.pdf) — the paper, 10 pages
- [source.tex](source.tex) — LaTeX source, with the editorial changes listed in its header
- [ai-output.md](ai-output.md) — the original AI output, the prompts, and the LaTeX as written
- [computations/](computations/) — the SymPy and SageMath scripts behind §11, and their output

### Community

Open an [issue](../../../../issues/new/choose) if you can check any of the proofs — the
divisibility lemma, the Cauchy–Binet argument, the sign of Theorem 5.1, the collapse in
Theorem 6.1, the confluent limit of Corollary 9.2 — find an error or a counterexample, know of
prior work where these formulas, or stronger ones, already appear (the paper itself asks this
about Theorems 6.1 and 7.1), or can settle what replaces Proposition 10.1 in the multivariate
case. Partial checks are useful; see [CONTRIBUTING.md](../../CONTRIBUTING.md).
