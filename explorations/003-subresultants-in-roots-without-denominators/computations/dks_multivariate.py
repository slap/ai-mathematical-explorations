# -*- coding: utf-8 -*-
"""
Multivariate test: Example 3.4 of D'Andrea-Krick-Szanto (n=2, d1=d2=d3=2, t=2).

There the paper obtains

    |O_S| = -c0 |V_{2,5}| + c2 |V_{0,5}| + c5 |V_{0,2}|,     V_T = |V_{4,5}|,

with V the 6 x 4 matrix of evaluations of the monomials (1, u, v, uv, u^2, v^2)
at the 4 common roots xi_j = (u_j, v_j) of f_1, f_2, and V_{i,j} the 4 x 4
submatrix obtained by deleting rows i and j.

QUESTION: does the multivariate version of divisibility hold, i.e. does
          V_T = |V_{4,5}|  divide  |O_S|  in Q[u_1..u_4, v_1..v_4] ?

The key observation that makes the test conclusive: the coefficients c0, c2, c5
of f_3 are free independent variables, so |O_S| is divisible by V_T if and only
if EACH of |V_{2,5}|, |V_{0,5}|, |V_{0,2}| is.

And the roots really are free parameters in this case: 4 general points of the
plane are the base locus of a pencil of conics, so the map
(coefficients) -> (roots) is dominant and the u_j, v_j are algebraically
independent. Hence the divisibility test in Q[u,v] is exactly the test of
"universal polynomiality in the roots".

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import sympy as sp
from itertools import combinations

u = sp.symbols('u1:5')
v = sp.symbols('v1:5')

# monomios en el orden del paper: indices 0..5
MON = [lambda U, V: sp.Integer(1),
       lambda U, V: U,
       lambda U, V: V,
       lambda U, V: U * V,
       lambda U, V: U**2,
       lambda U, V: V**2]
NOMBRE = ['1', 'u', 'v', 'uv', 'u^2', 'v^2']


def V_del(i, j):
    """Submatriz 4x4 de la matriz 6x4 de evaluaciones, borrando filas i, j."""
    filas = [r for r in range(6) if r not in (i, j)]
    return sp.Matrix(4, 4, lambda a, b: MON[filas[a]](u[b], v[b]))


def divide_exacto(num, den, gens):
    q, r = sp.div(sp.Poly(sp.expand(num), *gens), sp.Poly(sp.expand(den), *gens))
    return (r == 0), q.as_expr()


def main():
    gens = list(u) + list(v)
    VT = sp.expand(V_del(4, 5).det())      # Vandermonde generalizado asociado a T
    print("V_T = |V_{4,5}|  (monomios T = 1, u, v, uv)")
    print("  grado total:", sp.Poly(VT, *gens).total_degree())
    print("  factorizacion:", sp.factor(VT))
    print()

    for (i, j) in [(2, 5), (0, 5), (0, 2)]:
        filas = [NOMBRE[r] for r in range(6) if r not in (i, j)]
        D = sp.expand(V_del(i, j).det())
        ok, q = divide_exacto(D, VT, gens)
        print("|V_{%d,%d}|  (filas %s), grado %d :  divisible por V_T ? %s"
              % (i, j, filas, sp.Poly(D, *gens).total_degree(), ok))
        if ok:
            print("     cociente =", sp.factor(q))
    print()

    # panorama completo: que pares (i,j) dan alternantes divisibles por V_T
    print("Barrido sobre TODOS los pares (i,j):")
    for (i, j) in combinations(range(6), 2):
        if (i, j) == (4, 5):
            continue
        D = sp.expand(V_del(i, j).det())
        if D == 0:
            print("  (%d,%d): determinante nulo" % (i, j)); continue
        ok, q = divide_exacto(D, VT, gens)
        print("  (%d,%d) filas %-28s divisible: %s%s"
              % (i, j, str([NOMBRE[r] for r in range(6) if r not in (i, j)]), ok,
                 ("   cociente = " + str(sp.factor(q))) if ok else ""))


if __name__ == '__main__':
    main()
