import CasasAlvero.Witnesses

-- TODO: add a copyright header with authors and re-enable this linter.
set_option linter.style.header false

/-!
# The Casas-Alvero witnesses in degree 4

Instances of the general results of `CasasAlvero.Witnesses` for `d = 4`,
spelled out for the three indices `i = 1, 2, 3`. The witnesses are

| `i` | witness     | Hasse derivatives                        |
|-----|-------------|------------------------------------------|
| 1   | `X^4 + X`   | `4X^3+1`, `6X^2`, `4X`                   |
| 2   | `X^4 + X^2` | `4X^3+2X`, `6X^2+1`, `4X`                |
| 3   | `X^4 - X^3` | `4X^3-3X^2`, `6X^2-3X`, `4X-1`           |

In each row the polynomial is coprime to the `i`-th derivative and shares the
factor `X` with the other two.
-/

open Polynomial

namespace CasasAlvero.Degree4

variable {K : Type*} [Field K] [CharZero K]

/-! ## Coprimality pattern -/

theorem witness_one :
    IsCoprime ((X : K[X]) ^ 4 + X ^ 1) (hasseDeriv 1 ((X : K[X]) ^ 4 + X ^ 1)) ∧
    ¬ IsCoprime ((X : K[X]) ^ 4 + X ^ 1) (hasseDeriv 2 ((X : K[X]) ^ 4 + X ^ 1)) ∧
    ¬ IsCoprime ((X : K[X]) ^ 4 + X ^ 1) (hasseDeriv 3 ((X : K[X]) ^ 4 + X ^ 1)) :=
  ⟨isCoprime_binomial (by norm_num) (by norm_num),
   not_isCoprime_binomial (by norm_num) (by norm_num) (by norm_num),
   not_isCoprime_binomial (by norm_num) (by norm_num) (by norm_num)⟩

theorem witness_two :
    ¬ IsCoprime ((X : K[X]) ^ 4 + X ^ 2) (hasseDeriv 1 ((X : K[X]) ^ 4 + X ^ 2)) ∧
    IsCoprime ((X : K[X]) ^ 4 + X ^ 2) (hasseDeriv 2 ((X : K[X]) ^ 4 + X ^ 2)) ∧
    ¬ IsCoprime ((X : K[X]) ^ 4 + X ^ 2) (hasseDeriv 3 ((X : K[X]) ^ 4 + X ^ 2)) :=
  ⟨not_isCoprime_binomial (by norm_num) (by norm_num) (by norm_num),
   isCoprime_binomial (by norm_num) (by norm_num),
   not_isCoprime_binomial (by norm_num) (by norm_num) (by norm_num)⟩

theorem witness_three :
    ¬ IsCoprime ((X : K[X]) ^ 4 - X ^ 3) (hasseDeriv 1 ((X : K[X]) ^ 4 - X ^ 3)) ∧
    ¬ IsCoprime ((X : K[X]) ^ 4 - X ^ 3) (hasseDeriv 2 ((X : K[X]) ^ 4 - X ^ 3)) ∧
    IsCoprime ((X : K[X]) ^ 4 - X ^ 3) (hasseDeriv 3 ((X : K[X]) ^ 4 - X ^ 3)) :=
  ⟨not_isCoprime_top (d' := 3) (by norm_num) (by norm_num),
   not_isCoprime_top (d' := 3) (by norm_num) (by norm_num),
   isCoprime_top (d' := 3) (by norm_num)⟩

/-! ## The same statement for the resultants `R_j = Res(f, H_j f)` -/

theorem resultants_degree_four :
    -- witness `i = 1`
    resultant ((X : K[X]) ^ 4 + X ^ 1) (hasseDeriv 1 ((X : K[X]) ^ 4 + X ^ 1)) ≠ 0 ∧
    resultant ((X : K[X]) ^ 4 + X ^ 1) (hasseDeriv 2 ((X : K[X]) ^ 4 + X ^ 1)) = 0 ∧
    resultant ((X : K[X]) ^ 4 + X ^ 1) (hasseDeriv 3 ((X : K[X]) ^ 4 + X ^ 1)) = 0 ∧
    -- witness `i = 2`
    resultant ((X : K[X]) ^ 4 + X ^ 2) (hasseDeriv 1 ((X : K[X]) ^ 4 + X ^ 2)) = 0 ∧
    resultant ((X : K[X]) ^ 4 + X ^ 2) (hasseDeriv 2 ((X : K[X]) ^ 4 + X ^ 2)) ≠ 0 ∧
    resultant ((X : K[X]) ^ 4 + X ^ 2) (hasseDeriv 3 ((X : K[X]) ^ 4 + X ^ 2)) = 0 ∧
    -- witness `i = 3`
    resultant ((X : K[X]) ^ 4 - X ^ 3) (hasseDeriv 1 ((X : K[X]) ^ 4 - X ^ 3)) = 0 ∧
    resultant ((X : K[X]) ^ 4 - X ^ 3) (hasseDeriv 2 ((X : K[X]) ^ 4 - X ^ 3)) = 0 ∧
    resultant ((X : K[X]) ^ 4 - X ^ 3) (hasseDeriv 3 ((X : K[X]) ^ 4 - X ^ 3)) ≠ 0 := by
  obtain ⟨a1, a2, a3⟩ := witness_one (K := K)
  obtain ⟨b1, b2, b3⟩ := witness_two (K := K)
  obtain ⟨c1, c2, c3⟩ := witness_three (K := K)
  have hf1 : ((X : K[X]) ^ 4 + X ^ 1) ≠ 0 := fun h => by
    have := congrArg natDegree h
    rw [natDegree_add_eq_left_of_natDegree_lt (by simp)] at this
    simp at this
  have hf2 : ((X : K[X]) ^ 4 + X ^ 2) ≠ 0 := fun h => by
    have := congrArg natDegree h
    rw [natDegree_add_eq_left_of_natDegree_lt (by simp)] at this
    simp at this
  have hf3 : ((X : K[X]) ^ 4 - X ^ 3) ≠ 0 := fun h => by
    have := congrArg natDegree h
    rw [sub_eq_add_neg, natDegree_add_eq_left_of_natDegree_lt (by simp)] at this
    simp at this
  exact ⟨resultant_ne_zero_of_isCoprime a1,
    resultant_eq_zero_of_not_isCoprime hf1 a2,
    resultant_eq_zero_of_not_isCoprime hf1 a3,
    resultant_eq_zero_of_not_isCoprime hf2 b1,
    resultant_ne_zero_of_isCoprime b2,
    resultant_eq_zero_of_not_isCoprime hf2 b3,
    resultant_eq_zero_of_not_isCoprime hf3 c1,
    resultant_eq_zero_of_not_isCoprime hf3 c2,
    resultant_ne_zero_of_isCoprime c3⟩

end CasasAlvero.Degree4
