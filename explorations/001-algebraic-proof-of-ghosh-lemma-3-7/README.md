<!-- meta:start -->
# An algebraic proof of Ghosh's Lemma 3.7

**Status:** 🔴 Refuted \
**Area:** Commutative Algebra / Algebraic Geometry \
**Date:** 2026-09-16 \
**AI system:** Claude Opus 5 (Anthropic), model claude-opus-5 — via Claude Code \
**Published by:** Santiago Laplagne
<!-- meta:end -->

📄 **[Read the note (PDF, 3 pages)](exploration.pdf)** · [LaTeX source](source.tex) ·
[original AI output](ai-output.md) · [computations](computations/)

> [!WARNING]
> **Refuted (2026-09-17).** The note's second claim — that the conditional lemma proved here
> can stand in for Lemma 3.7 in the preprint — does not hold: what the argument actually needs
> at the point of use does not follow from it. With that claim goes the point of the note,
> which was to remove the preprint's only topological ingredient. See *Verification status*.
> The page is kept as part of the record.

### Summary

Ghosh (arXiv:2501.09272, v2) proves his Lemma 3.7, an existence statement for "almost
counterexamples", using Abel–Gontcharoff polynomials and the topological Brouwer degree over
ℂ; this is the only analytic ingredient of his preprint and takes about three pages.

**The AI-generated note published here** claims that at the point where the lemma is actually
used — inside a downward induction, where the conjecture is already assumed in degree *n*+1 —
the statement follows from the projective dimension theorem in a few lines, with no topology
and no hypothesis on the characteristic.

### Research context

The exploration came out of a project on subresultant formulas without denominators, part of
ongoing work with colleagues, which led to the Casas–Alvero conjecture and, from there, to a
reading of Ghosh's preprint [*Proof of the Casas–Alvero conjecture*,
arXiv:2501.09272] (v2, March 2026). When I asked whether anything in that preprint could be
simplified, the AI pointed at its Lemma 3.7 — the single place where the argument leaves
algebra for topology — and then produced this note.

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
inside Section 4.2, where (H) is the inductive hypothesis 4.1.1. **This is the claim that
fails**, and it is what the note was for; see below.

### Verification status

> Refuted. The reduction the note depends on does not work: what Section 4.2 of the preprint
> actually needs does not follow from the conditional lemma proved here.

When this was published, the first thing a reader was asked to check was the second claim —
that the conditional version suffices to replace Lemma 3.7, since the lemma reaches Section 4.2
only through Corollary 3.9, and the note itself asked the author of the preprint to confirm it
(Remark, §3). That is the step that was checked, and it failed: the statement required at the
point of use is stronger than `F_l ∉ √(F_{l+1},…,F_n)` under (H), and does not follow from it.

What this leaves standing is the conditional lemma and its half-page proof, which is not where
the error is. But the lemma was only of interest as a replacement for the three pages of
Abel–Gontcharoff polynomials and Brouwer degree, and it does not replace them. Ghosh's Lemma
3.7, and the analytic ingredient with it, stand as written; the preprint is untouched by this.

The SageMath computations in [`computations/`](computations/) are unaffected and equally
inconsequential: they confirm (H) and the conclusion of the conditional lemma for *d* = 4 and
*d* = 5, and were never evidence for the claim that failed. Two questions raised at publication
— the behaviour in positive characteristic and the dimension count in the last step — were
never resolved, and no longer matter to anything.

### Verification record

| Date | Status | By | Reference |
| --- | --- | --- | --- |
| 2026-09-17 | 🟠 Unverified | — | published as generated |
| 2026-09-17 | 🔴 Refuted | S. Laplagne | the reduction to Corollary 3.9 fails; see above |

### Files

- [exploration.pdf](exploration.pdf) — the note, 3 pages
- [source.tex](source.tex) — LaTeX source, with the editorial changes listed in its header
- [ai-output.md](ai-output.md) — the original AI output and the prompts, unedited
- [computations/](computations/) — the SageMath scripts written by the AI, and their output

### Community

The page stays up refuted rather than deleted: a note that looked like it removed the only
analytic ingredient of a proof of the Casas–Alvero conjecture, and did not, is part of what
this archive is for. Open an [issue](../../../../issues/new/choose) if the refutation itself is
wrong, or if the conditional lemma — which is not what failed — is useful for something else.
See [CONTRIBUTING.md](../../CONTRIBUTING.md).
