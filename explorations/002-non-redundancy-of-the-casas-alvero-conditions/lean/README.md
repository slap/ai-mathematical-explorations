# Lean 4 development

Written by the same AI system, in the same project, on 2026-09-17. It formalises the
existence of the witnesses, which is the load-bearing part of the note.

| Theorem | Statement |
| --- | --- |
| `CasasAlvero.exists_witness` | For `1 ≤ i < d`, over a field of characteristic zero, there is a monic `f` of degree `d` with `f(0) = 0`, coprime to `H_i f`, sharing a non-constant factor with `H_j f` for every `j ≠ i` in range. |
| `CasasAlvero.exists_witness_resultant` | The same in terms of resultants: `Res(f, H_i f) ≠ 0` and `Res(f, H_j f) = 0` for `j ≠ i`. |

[`CasasAlvero/Degree4.lean`](CasasAlvero/Degree4.lean) spells the three instances out for
`d = 4`.

What is **not** formalised: the closed-form value of `R_i` on the witness lines, the step from
the witnesses to `R_i ∉ √(R_j : j ≠ i)`, and the consequences in §4 of the note.

## Reproducing the check

The files are copied from the project where they were written; they form a Lake package that
builds against Mathlib at the revision pinned in `lake-manifest.json` (Lean 4.34.0):

```
lake exe cache get
lake build
```

and, for the axiom check,

```lean
import CasasAlvero.Witnesses
#print axioms CasasAlvero.exists_witness
#print axioms CasasAlvero.exists_witness_resultant
```

Run on 2026-09-17, the build succeeded and both theorems reported `[propext,
Classical.choice, Quot.sound]` — the standard axioms of Mathlib, with no `sorry`.
