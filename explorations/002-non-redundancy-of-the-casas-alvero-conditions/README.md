<!-- meta:start -->
# Non-redundancy of the Casas–Alvero conditions

**Status:** 🟡 Partially verified \
**Area:** Commutative Algebra \
**Date:** 2026-09-16 \
**AI system:** Claude Opus 5 (Anthropic), model claude-opus-5 — via Claude Code \
**Published by:** Santiago Laplagne
<!-- meta:end -->

📄 **[Read the note (PDF, 5 pages)](exploration.pdf)** · [LaTeX source](source.tex) ·
[original AI output](ai-output.md) · [Lean development](lean/) · [computations](computations/)

### Summary

For the generic polynomial `f = x^d + a_1 x^{d-1} + … + a_{d-1} x`, let `R_i` be the resultant
of `f` with its *i*-th Hasse derivative. Schaub and Spivakovsky (arXiv:2312.08742, Theorem 5)
proved that `R_i ∉ √(R_j : j ≠ i)` for the three highest indices, `i ∈ {d-3, d-2, d-1}`, by an
indirect argument about real roots.

**The AI-generated note published here** claims the same for **every** index
`i ∈ {1,…,d-1}`, by exhibiting explicit degenerate witnesses, and draws three consequences:
none of the `d-1` Casas–Alvero conditions is redundant; the conjecture reduces to a statement
about every irreducible component of `V(R_j : j ≠ i)`; and every membership certificate over ℚ
is constrained along `d-1` explicit lines.

### Research context

The exploration came out of a project on subresultant formulas without denominators, part of
ongoing work with colleagues, which led to the Casas–Alvero conjecture. I asked for a closed
formula for membership of a resultant in an ideal, or an example of non-membership, over ℚ;
the model went to the partial result of Schaub–Spivakovsky (arXiv:2312.08742) and produced
this note.

### The mathematical claim

Let `K` have characteristic 0, `d ≥ 3`, `H_i` the *i*-th Hasse derivative and
`R_i = Res(f, H_i(f)) ∈ K[a_1,…,a_{d-1}]`.

> **Proposition (witness lines).** For `f_{i,t} = x^d + t·x^i` (`1 ≤ i ≤ d-2`) and
> `f_{d-1,t} = x^d − t·x^{d-1}`: `R_j(f_{i,t}) = 0` for every `j ≠ i`, and
> `R_i(f_{i,t}) = ±(C(d,i) − 1)^{d-i} · t^d`.
>
> **Theorem.** For every `d ≥ 3` and every `i ∈ {1,…,d-1}`,
> `R_i ∉ √(R_1,…,Ř_i,…,R_{d-1})` in `K[a_1,…,a_{d-1}]`.

The theorem extends Theorem 5 of Schaub–Spivakovsky, which covers `i ∈ {d-3, d-2, d-1}`, and
its proof evaluates at a single point: no Nullstellensatz, no real roots, no use of the
conjecture. The consequences drawn in §4 of the note — the component reformulation and the
constraints on certificates — are separate claims resting on it.

### Verification status

Part of this is machine-checked, and it is worth being precise about which part.

**Checked.** The note ships a Lean 4 development ([`lean/`](lean/)), written by the same AI
system, that proves `exists_witness` and `exists_witness_resultant`: for every `d` and every
`1 ≤ i ≤ d-1`, over any field of characteristic zero, there is a monic `f` of degree `d` with
`f(0) = 0` that is coprime to `H_i f` and shares a non-constant factor with every `H_j f`,
`j ≠ i` — equivalently `R_i ≠ 0` and `R_j = 0` for `j ≠ i`. On 2026-09-17 I built it against
Mathlib (Lean 4.34.0): `lake build` succeeds, and `#print axioms` reports only `propext`,
`Classical.choice` and `Quot.sound` for both theorems — no `sorry`, no extra axiom.

**Not checked.** Everything else:

- the closed-form value `±(C(d,i) − 1)^{d-i} t^d` — Lean gives non-vanishing only;
- the step from the witnesses to non-membership in the radical, i.e. the theorem as stated
  over `K[a_1,…,a_{d-1}]`;
- the consequences in §4 — the component lemma and the two certificate corollaries;
- whether the Lean statements faithfully express the note's proposition. A proof assistant
  checks a proof against a statement, not a statement against a paper, and here both were
  written by the same system.

Points a reader might go to first, beyond those:

- the note and the Lean docstring disagree on whether the deduction needs the
  Nullstellensatz; the note says only its trivial direction is used;
- the note's own caveat: the general case is not in version 7 of Schaub–Spivakovsky, and it
  does not rule out that it appears elsewhere in the literature.

### Verification record

| Date | Status | By | Reference |
| --- | --- | --- | --- |
| 2026-09-16 | 🟠 Unverified | — | published as generated |
| 2026-09-17 | 🟡 Partially verified | Lean 4.34.0 / Mathlib | the witness statements, built with no `sorry`; see above |

### Files

- [exploration.pdf](exploration.pdf) — the note, 5 pages
- [source.tex](source.tex) — LaTeX source, with the editorial changes listed in its header
- [ai-output.md](ai-output.md) — the original AI output, Spanish and English, and the prompts
- [lean/](lean/) — the Lean 4 formalisation of the witnesses
- [computations/](computations/) — the SageMath script behind the note's verification table

### Community

Open an [issue](../../../../issues/new/choose) if you can check the unformalised part of the
argument, find an error or a counterexample, know of prior work where the general case
appears — the note explicitly asks this question — or can improve or generalise the result.
Partial checks are useful; see [CONTRIBUTING.md](../../CONTRIBUTING.md).
