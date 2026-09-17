<!-- meta:start -->
# An algebraic proof of Ghosh's Lemma 3.7

**Status:** 🟠 Unverified \
**Area:** Commutative Algebra / Algebraic Geometry \
**Date:** 2026-09-16 \
**AI system:** Claude Opus 5 (Anthropic), model claude-opus-5 — via Claude Code \
**Curator:** Santiago Laplagne
<!-- meta:end -->

**Research context.** The exploration came out of a project on subresultant formulas without
denominators, which led to the Casas–Alvero conjecture and, from there, to a reading of
Ghosh's preprint [*Proof of the Casas–Alvero conjecture*, arXiv:2501.09272] (v2, March 2026).
Asked whether anything in that preprint could be simplified, the AI pointed at its Lemma 3.7 —
the single place where the argument leaves algebra for topology — and then produced this note.

### Summary

Ghosh proves his Lemma 3.7, an existence statement for "almost counterexamples", using
Abel–Gontcharoff polynomials and the topological Brouwer degree over ℂ; this is the only
analytic ingredient of the preprint and takes about three pages. The note claims that at the
point where the lemma is actually used — inside a downward induction, where the conjecture is
already assumed in degree *n*+1 — the statement follows from the projective dimension theorem
in a few lines, with no topology and no hypothesis on the characteristic.

### The mathematical claim

In the root-space formulation, let `F_i = Φ_{j_i}(e_{n+1-i})` be the forms of degree
*n*+1−*i* in `K[x_1,…,x_n]` attached to a choice of indices **j**, and let (H) be the
condition `V₊(F_1,…,F_n) = ∅` in `P^{n-1}`, which by Proposition 1.4 of the preprint is the
Casas–Alvero conjecture in degree *n*+1.

> **Lemma.** Let `K` be algebraically closed and assume (H) for the choice **j**. Then, for
> every `1 ≤ l ≤ n`, `F_l ∉ √(F_{l+1},…,F_n)` in `K[x_1,…,x_n]`.

The proof is half a page: if `F_l` were in that radical, the variety cut out by the last
*n*−*l* forms would have dimension at least *l*−1 and would be contained in `V₊(F_l)`, so
cutting with the remaining *l*−1 forms would leave `V₊(F_1,…,F_n)` non-empty, contradicting (H).

A second claim accompanies it: that this **conditional** version suffices to replace Lemma 3.7
in the preprint, because the lemma is used only through Corollary 3.9, itself invoked only
inside Section 4.2, where (H) is the inductive hypothesis 4.1.1.

### Verification status

> The result has not been independently verified. The arguments should be regarded as
> conjectural until checked.

What exists so far is evidence produced by the same AI system, which does not count as
verification: symbolic computations in SageMath confirming (H) and the conclusion of the lemma
for *d* = 4 and *d* = 5, and showing the dimension bound is sharp. The scripts are in
[`computations/`](computations/) and the printed output is in the record.

Points a reader might go to first:

- the second claim — that the conditional lemma suffices — rests on tracing cross-references
  in the preprint, and the note itself asks for the author to confirm it (Remark, §3);
- the note asserts the argument holds in any characteristic, while the reformulation it relies
  on is quoted from the preprint; the scope of that proposition is worth checking;
- the dimension count in the last step of the proof, where the *l*−1 remaining cuts are made.

### Verification record

| Date | Status | By | Reference |
| --- | --- | --- | --- |
| 2026-09-17 | 🟠 Unverified | — | published as generated |

### Documents

- [exploration.pdf](exploration.pdf) — the note, 3 pages
- [source.tex](source.tex) — LaTeX source, with the editorial changes listed in its header
- [ai-output.md](ai-output.md) — the original AI output and the prompts, unedited
- [computations/](computations/) — the SageMath scripts written by the AI, and their output

### Community

Open an [issue](../../../../issues/new/choose) if you can check the argument or any step of
it, find an error or a counterexample, know of prior work where this or a stronger statement
appears, or can improve or generalise the proof. Partial checks are useful; see
[CONTRIBUTING.md](../../CONTRIBUTING.md).

The natural addressee of the second claim is the author of the preprint, and the note says so.
