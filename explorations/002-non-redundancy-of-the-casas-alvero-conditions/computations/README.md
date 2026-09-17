# Computations

The SageMath script written by the AI system alongside the note, kept unedited; its comments
are in Spanish, as generated. Evidence produced with the argument, not a check of it.

| File | What it does |
| --- | --- |
| [`radical_non_membership.py`](radical_non_membership.py) | Evaluates every `R_j` at the witnesses for `d = 3…10`, and runs an independent radical test by Gröbner bases (Rabinowitsch) for small `d`. |
| [`radical_non_membership.out`](radical_non_membership.out) | Output as produced, from a short run: the evaluation check for `d = 3` and the Gröbner test up to `d = 5`. |

```
sage -python -u radical_non_membership.py
```

The note's verification table also reports the evaluation check up to `d = 9` and the
284 symbolic resultants of the proposition, from longer runs of the same script whose output
was not kept as a file. The script was later renamed by the same model (it was
`no_pertenencia_radical.py` when written); nothing else in it changed.
