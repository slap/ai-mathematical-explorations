# Computations

SageMath scripts written by the AI system in the same session, kept under their original
names and unedited. They are evidence produced alongside the argument, not a verification of
it; see the exploration page.

| File | What it does |
| --- | --- |
| [`verificar_ghosh.py`](verificar_ghosh.py) | Tests the conclusion of the lemma directly — `F_l ∉ √(F_i : i > l)` via Rabinowitsch — over all branches, and reports how many cases are covered by the explicit witnesses of Remark 3.8(1) of the preprint. |
| [`interseccion_lema37.py`](interseccion_lema37.py) | Tests the two dimension facts the algebraic proof rests on: hypothesis (H) for every branch, and `dim V(F_{l+1},…,F_n) ≥ l`. |
| [`verificar_ghosh-n4.out`](verificar_ghosh-n4.out) | Output of the first script for `n = 4` (`d = 5`), as produced. |

Both take `n` as argument and were run under SageMath 10.7:

```
sage -python -u verificar_ghosh.py 4
sage -python -u interseccion_lema37.py 4
```

`n = 4` takes a few minutes; `n = 5` was not attempted. The comments in the scripts are in
Spanish, as generated. The output of `interseccion_lema37.py` was not saved to a file at the
time; what was printed is quoted in [`../ai-output.md`](../ai-output.md).
