# Computations

SymPy and SageMath scripts written by the AI system in the same session, kept under their
original names and unedited except for one local path (see below). They are the evidence
behind §11 of the note: they test the statements in the cases listed there, which is not a
verification of the proofs. See the exploration page.

| File | What it does |
| --- | --- |
| [`dks_univariate.py`](dks_univariate.py) | The univariate core: exact division of `\|O_S\|` by the Vandermonde and symmetry of the quotient (Thm. 3.2), and the Cauchy–Binet expansion in the Schur basis of the roots of `g` (Thm. 4.1). 9 configurations, including the two examples of [DKS05]. |
| [`natural_basis.py`](natural_basis.py) | The exact sign of the multi-Schur determinant (Thm. 5.1) and the collapse of the classical case to the rectangle (Thm. 6.1), plus the exhaustive search over partitions showing that no single supersymmetric Schur function works when `S` has gaps. |
| [`difference_basis.py`](difference_basis.py) | The dual expansion in the basis `{s_ν(Ξ − A)}` for arbitrary `S` (Thm. 8.1), and the sparsity of its support. |
| [`line3_closure.py`](line3_closure.py) | Three things at once: the end-to-end validation against the classical definition of the scalar subresultant with exact signs, the Hankel/Padé form (Thm. 7.1), and the skew-Schur coefficients with their vanishing criterion (Cor. 8.2). |
| [`newton_divided_differences.py`](newton_divided_differences.py) | The Newton form `P_S = det(R_i[ξ₁,…,ξ_j])` (Thm. 9.1). |
| [`multiple_roots.py`](multiple_roots.py) | The confluent case (Cor. 9.2): 8 multiplicity patterns over several `(d₁,d₂,t,S)`. |
| [`dks_multivariate.py`](dks_multivariate.py) | The negative result (Prop. 10.1): a sweep over the 15 alternants of [DKS05, Ex. 3.4]. |
| [`sage_verification.py`](sage_verification.py) | The SageMath rerun of the univariate statements, cross-checked against Sage's native symmetric function routines rather than the script's own bialternant. |

Raw output, as produced: [`output-univariate.txt`](output-univariate.txt),
[`output-line3-closure.txt`](output-line3-closure.txt),
[`output-multiple-roots.txt`](output-multiple-roots.txt),
[`output-multivariate.txt`](output-multivariate.txt), [`output-sage.txt`](output-sage.txt).

The SymPy scripts (1.14) run directly:

```
python dks_univariate.py        # ~45 s
python multiple_roots.py        # ~20 s
python dks_multivariate.py      # ~10 s
```

The SageMath ones were run under SageMath 10.7, installed with Miniforge inside WSL
Ubuntu-24.04, with `sage -python -u` (without `-u` the output is buffered). They are one to
two orders of magnitude faster, which is what made `d₁ = d₂ = 5` reachable.

The comments in the scripts are in English, as generated; the identifiers are still in
Spanish (`filas`, `signo_predicho`, `confluente`, ...), since renaming them would mean
re-running every computation. The only edit is in the header of
[`sage_verification.py`](sage_verification.py), where the example invocation contained the
absolute path of the machine it was run on; it now reads
`/mnt/c/.../research-subresultantes/...`.
