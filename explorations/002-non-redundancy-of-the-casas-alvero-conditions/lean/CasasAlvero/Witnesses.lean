import Mathlib.Algebra.Polynomial.HasseDeriv
import Mathlib.Algebra.Polynomial.Degree.Operations
import Mathlib.RingTheory.Polynomial.Resultant.Basic
import Mathlib.RingTheory.Coprime.Lemmas
import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

-- TODO: add a copyright header with authors and re-enable this linter.
set_option linter.style.header false

/-!
# Explicit witnesses for the Casas-Alvero conditions

Let `K` be a field of characteristic zero and, for a monic `f ∈ K[X]` of degree
`d` with `f(0) = 0`, let `H_j f` denote the `j`-th Hasse derivative and
`R_j := Res(f, H_j f)`.

For every `d ≥ 3` and every index `1 ≤ i ≤ d - 1` we exhibit a witness `f` that
satisfies *all* the Casas-Alvero conditions except the `i`-th:

| index         | witness             |
|---------------|---------------------|
| `1 ≤ i ≤ d-2` | `f = X^d + X^i`     |
| `i = d-1`     | `f = X^d - X^(d-1)` |

The main results are `CasasAlvero.exists_witness` (in terms of coprimality) and
`CasasAlvero.exists_witness_resultant` (in terms of resultants: `R_j = 0` for
`j ≠ i` and `R_i ≠ 0`).

Together with the Nullstellensatz this gives `R_i ∉ √(R_j : j ≠ i)` for *every*
index `i`, extending Theorem 5 of Schaub-Spivakovsky (arXiv:2312.08742), which
covers `i ∈ {d-3, d-2, d-1}`.

## Proof idea

Write `m = d - i`, so that `f = X^i (X^m + 1)` and `H_i f = C(d,i) X^m + 1`.

* For `j ≠ i` the variable `X` divides both `f` and `H_j f`: if `j < i` both
  monomials of `H_j f` have positive exponent, and if `j > i` then
  `C(i,j) = 0`, so only the first monomial survives.
* For `j = i` we check coprimality against each factor of `f`. Against `X`
  because the constant term of `H_i f` is `1`; against `X^m + 1` because
  `C(d,i) (X^m + 1) - H_i f = C(d,i) - 1`, which is nonzero in characteristic
  zero precisely because `C(d,i) ≠ 1`.
-/

open Polynomial

namespace CasasAlvero

variable {K : Type*} [Field K]

/-! ## Auxiliary lemmas -/

/-- If `X` divides two polynomials, they are not coprime. -/
lemma not_isCoprime_of_X_dvd {p q : K[X]} (hp : X ∣ p) (hq : X ∣ q) :
    ¬ IsCoprime p q :=
  fun h => not_isUnit_X (h.isUnit_of_dvd' hp hq)

/-- A nonzero constant in the ideal `(p, q)` makes `p` and `q` coprime. -/
lemma isCoprime_of_const {p q u v : K[X]} {c : K} (hc : c ≠ 0)
    (h : u * p + v * q = C c) : IsCoprime p q :=
  ⟨C c⁻¹ * u, C c⁻¹ * v, by
    calc C c⁻¹ * u * p + C c⁻¹ * v * q = C c⁻¹ * (u * p + v * q) := by ring
      _ = C c⁻¹ * C c := by rw [h]
      _ = 1 := by rw [← C_mul, inv_mul_cancel₀ hc, C_1]⟩

/-- The Hasse derivative of a power of `X`. -/
lemma hasseDeriv_X_pow (k n : ℕ) :
    hasseDeriv k ((X : K[X]) ^ n) = (n.choose k : K[X]) * X ^ (n - k) := by
  rw [X_pow_eq_monomial, hasseDeriv_monomial, ← C_mul_X_pow_eq_monomial, mul_one,
    map_natCast]

/-- `X` divides `X ^ a + X ^ b` when both exponents are positive. -/
lemma X_dvd_X_pow_add_X_pow {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (X : K[X]) ∣ X ^ a + X ^ b := by
  obtain ⟨a', rfl⟩ : ∃ a', a = a' + 1 := ⟨a - 1, by omega⟩
  obtain ⟨b', rfl⟩ : ∃ b', b = b' + 1 := ⟨b - 1, by omega⟩
  exact ⟨X ^ a' + X ^ b', by ring⟩

/-- `X` divides `X ^ a - X ^ b` when both exponents are positive. -/
lemma X_dvd_X_pow_sub_X_pow {a b : ℕ} (ha : 1 ≤ a) (hb : 1 ≤ b) :
    (X : K[X]) ∣ X ^ a - X ^ b := by
  obtain ⟨a', rfl⟩ : ∃ a', a = a' + 1 := ⟨a - 1, by omega⟩
  obtain ⟨b', rfl⟩ : ∃ b', b = b' + 1 := ⟨b - 1, by omega⟩
  exact ⟨X ^ a' - X ^ b', by ring⟩

/-! ## Hasse derivatives of the two witnesses -/

/-- The `i`-th Hasse derivative of the binomial witness. -/
lemma hasseDeriv_binomial (d i : ℕ) :
    hasseDeriv i ((X : K[X]) ^ d + X ^ i) = (d.choose i : K[X]) * X ^ (d - i) + 1 := by
  rw [map_add, hasseDeriv_X_pow, hasseDeriv_X_pow, Nat.choose_self]
  simp

/-- The `(d-1)`-st Hasse derivative of the top witness. -/
lemma hasseDeriv_top (d' : ℕ) :
    hasseDeriv d' ((X : K[X]) ^ (d' + 1) - X ^ d') = ((d' : K[X]) + 1) * X - 1 := by
  have h1 : (d' + 1).choose d' = d' + 1 := Nat.choose_succ_self_right d'
  have h2 : d' + 1 - d' = 1 := by omega
  have h3 : d' - d' = 0 := by omega
  rw [map_sub, hasseDeriv_X_pow, hasseDeriv_X_pow, Nat.choose_self, h1, h2, h3]
  push_cast
  ring

/-! ## The witnesses share a factor with the other Hasse derivatives -/

/-- The binomial witness shares a non-constant factor with every other Hasse
derivative in range. -/
theorem not_isCoprime_binomial {d i j : ℕ} (hi : 1 ≤ i) (hjd : j + 1 ≤ d)
    (hji : j ≠ i) :
    ¬ IsCoprime ((X : K[X]) ^ d + X ^ i) (hasseDeriv j ((X : K[X]) ^ d + X ^ i)) := by
  refine not_isCoprime_of_X_dvd (X_dvd_X_pow_add_X_pow (by omega) hi) ?_
  rw [map_add, hasseDeriv_X_pow, hasseDeriv_X_pow]
  rcases lt_or_gt_of_ne hji with h | h
  · exact dvd_add ((dvd_pow_self (X : K[X]) (n := d - j) (by omega)).mul_left _)
      ((dvd_pow_self (X : K[X]) (n := i - j) (by omega)).mul_left _)
  · rw [Nat.choose_eq_zero_of_lt h]
    simpa using (dvd_pow_self (X : K[X]) (n := d - j) (by omega)).mul_left _

/-- The top witness shares a non-constant factor with every earlier Hasse
derivative. -/
theorem not_isCoprime_top {d' j : ℕ} (hj : 1 ≤ j) (hjd : j + 1 ≤ d') :
    ¬ IsCoprime ((X : K[X]) ^ (d' + 1) - X ^ d')
      (hasseDeriv j ((X : K[X]) ^ (d' + 1) - X ^ d')) := by
  refine not_isCoprime_of_X_dvd (X_dvd_X_pow_sub_X_pow (by omega) (by omega)) ?_
  rw [map_sub, hasseDeriv_X_pow, hasseDeriv_X_pow]
  exact dvd_sub ((dvd_pow_self (X : K[X]) (n := d' + 1 - j) (by omega)).mul_left _)
    ((dvd_pow_self (X : K[X]) (n := d' - j) (by omega)).mul_left _)

/-! ## Reformulation in terms of resultants -/

lemma resultant_ne_zero_of_isCoprime {f g : K[X]} (h : IsCoprime f g) :
    resultant f g ≠ 0 :=
  fun h0 => (resultant_eq_zero_iff.mp h0).2 h

lemma resultant_eq_zero_of_not_isCoprime {f g : K[X]} (hf : f ≠ 0)
    (h : ¬ IsCoprime f g) : resultant f g = 0 :=
  resultant_eq_zero_iff.mpr ⟨Or.inl hf, h⟩

/-! ## Coprimality with the `i`-th derivative (characteristic zero) -/

variable [CharZero K]

/-- In characteristic zero, `C(d,i) - 1 ≠ 0` whenever `1 ≤ i < d`. -/
lemma choose_sub_one_ne_zero {d i : ℕ} (hi : 1 ≤ i) (hid : i + 1 ≤ d) :
    ((d.choose i : K) - 1) ≠ 0 := by
  have h1 : d.choose i ≠ 1 := by
    rw [Ne, Nat.choose_eq_one_iff]; omega
  have : ((d.choose i : K)) ≠ 1 := by simpa [Nat.cast_eq_one] using h1
  exact sub_ne_zero.mpr this

/-- The binomial witness is coprime to its `i`-th Hasse derivative. -/
theorem isCoprime_binomial {d i : ℕ} (hi : 1 ≤ i) (hid : i + 1 ≤ d) :
    IsCoprime ((X : K[X]) ^ d + X ^ i) (hasseDeriv i ((X : K[X]) ^ d + X ^ i)) := by
  obtain ⟨m, hm⟩ : ∃ m, d = i + m := ⟨d - i, by omega⟩
  have hm1 : 1 ≤ m := by omega
  obtain ⟨m', hm'⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
  have hdi : d - i = m := by omega
  rw [hasseDeriv_binomial, hdi, show ((X : K[X]) ^ d + X ^ i) = X ^ i * (X ^ m + 1) by
    rw [hm]; ring]
  -- coprime to `X`, hence to `X ^ i`
  have hX : IsCoprime (X : K[X]) ((d.choose i : K[X]) * X ^ m + 1) :=
    ⟨-((d.choose i : K[X]) * X ^ m'), 1, by rw [hm']; ring⟩
  -- coprime to `X ^ m + 1`
  have hfac : IsCoprime ((X : K[X]) ^ m + 1) ((d.choose i : K[X]) * X ^ m + 1) := by
    refine isCoprime_of_const (c := (d.choose i : K) - 1) (choose_sub_one_ne_zero hi hid)
      (u := (d.choose i : K[X])) (v := -1) ?_
    rw [map_sub, map_natCast, C_1]; ring
  exact hX.pow_left.mul_left hfac

/-- The top witness is coprime to its `(d-1)`-st Hasse derivative. -/
theorem isCoprime_top {d' : ℕ} (hd' : 1 ≤ d') :
    IsCoprime ((X : K[X]) ^ (d' + 1) - X ^ d')
      (hasseDeriv d' ((X : K[X]) ^ (d' + 1) - X ^ d')) := by
  rw [hasseDeriv_top, show ((X : K[X]) ^ (d' + 1) - X ^ d') = X ^ d' * (X - 1) by ring]
  have hX : IsCoprime (X : K[X]) (((d' : K[X]) + 1) * X - 1) :=
    ⟨(d' : K[X]) + 1, -1, by ring⟩
  have hfac : IsCoprime ((X : K[X]) - 1) (((d' : K[X]) + 1) * X - 1) := by
    refine isCoprime_of_const (c := -(d' : K))
      (neg_ne_zero.mpr (Nat.cast_ne_zero.mpr (by omega : d' ≠ 0)))
      (u := (d' : K[X]) + 1) (v := -1) ?_
    rw [map_neg, map_natCast]; ring
  exact hX.pow_left.mul_left hfac

/-! ## The main statement -/

/-- **Explicit witnesses for all indices.** For every `d ≥ 3` and every
`1 ≤ i ≤ d - 1` there is a monic `f ∈ K[X]` of degree `d` with `f(0) = 0` which
shares a non-constant factor with `H_j f` for every `1 ≤ j ≤ d - 1`, `j ≠ i`,
but is coprime to `H_i f`. -/
theorem exists_witness (d i : ℕ) (hi : 1 ≤ i) (hid : i + 1 ≤ d) :
    ∃ f : K[X], f.natDegree = d ∧ f.eval 0 = 0 ∧
      IsCoprime f (hasseDeriv i f) ∧
      ∀ j, 1 ≤ j → j + 1 ≤ d → j ≠ i →
        ¬ IsCoprime f (hasseDeriv j f) := by
  rcases eq_or_lt_of_le hid with h | h
  · -- `i = d - 1`: the top witness
    subst h
    refine ⟨(X : K[X]) ^ (i + 1) - X ^ i, ?_, ?_, isCoprime_top hi, ?_⟩
    · rw [sub_eq_add_neg,
        natDegree_add_eq_left_of_natDegree_lt (by simp),
        natDegree_X_pow]
    · simp [zero_pow (by omega : i ≠ 0)]
    · intro j hj hjd hji
      exact not_isCoprime_top hj (by omega)
  · -- `1 ≤ i ≤ d - 2`: the binomial witness
    refine ⟨(X : K[X]) ^ d + X ^ i, ?_, ?_, isCoprime_binomial hi hid, ?_⟩
    · rw [natDegree_add_eq_left_of_natDegree_lt
        (by simp only [natDegree_X_pow]; omega), natDegree_X_pow]
    · simp [zero_pow (by omega : d ≠ 0), zero_pow (by omega : i ≠ 0)]
    · intro j hj hjd hji
      exact not_isCoprime_binomial hi hjd hji

/-- **Explicit witnesses, in terms of resultants.** With `R_j = Res(f, H_j f)`:
for every `d ≥ 3` and every `1 ≤ i ≤ d - 1` there is a monic `f` of degree `d`
with `R_j = 0` for all `j ≠ i` in range and `R_i ≠ 0`. -/
theorem exists_witness_resultant (d i : ℕ) (hi : 1 ≤ i) (hid : i + 1 ≤ d) :
    ∃ f : K[X], f.natDegree = d ∧ f.eval 0 = 0 ∧
      resultant f (hasseDeriv i f) ≠ 0 ∧
      ∀ j, 1 ≤ j → j + 1 ≤ d → j ≠ i → resultant f (hasseDeriv j f) = 0 := by
  obtain ⟨f, hdeg, heval, hcop, hncop⟩ := exists_witness (K := K) d i hi hid
  have hf : f ≠ 0 := fun h => by simp [h] at hdeg; omega
  exact ⟨f, hdeg, heval, resultant_ne_zero_of_isCoprime hcop,
    fun j hj hjd hji => resultant_eq_zero_of_not_isCoprime hf (hncop j hj hjd hji)⟩

end CasasAlvero
