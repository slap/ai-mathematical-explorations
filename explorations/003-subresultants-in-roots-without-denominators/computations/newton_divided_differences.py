# -*- coding: utf-8 -*-
"""
Newton form of P_S.

If row i of O_S is (R_i(xi_j))_j, let R[xi_1,...,xi_j] be the divided
difference of order j-1. The change-of-basis matrix from (R(xi_1),...,R(xi_d))
to (R[xi_1], R[xi_1,xi_2], ..., R[xi_1..xi_d]) is lower triangular with
diagonal 1/prod_{l<j}(xi_j - xi_l), so its determinant is 1/V_{d2}. Therefore

    LEMMA:  P_S = |O_S| / V_{d2} = det( R_i[xi_1, ..., xi_j] )_{i,j=1..d2}

which is manifestly polynomial and, upon specialising repeated roots, yields
the divided derivatives: R[y,...,y] (j times) = R^{(j-1)}(y)/(j-1)!.

That settles the multiple-root case at once.

This script verifies the LEMMA symbolically.

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import os
import sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dks_univariate import vandermonde, k_of


def filas_R(d1, d2, t, gammas, x):
    """Las filas de O_S como polinomios en una variable x."""
    tstar = max(d2 - 1, t)
    a = sp.symbols('a0:%d' % (d1 + 1))
    f = sum(a[l] * x**l for l in range(d1 + 1))
    R = []
    for g in sorted(gammas):
        R.append(x**g)
    for e in range(t + 1, tstar + 1):
        R.append(x**e)
    for i in range(0, t - d1 + 1):
        R.append(x**i * f)
    assert len(R) == d2
    return R, a


def dif_dividida(R, x, nodos):
    """R[nodos[0], ..., nodos[-1]] por la formula de Lagrange."""
    n = len(nodos)
    tot = 0
    for i in range(n):
        den = sp.prod([nodos[i] - nodos[l] for l in range(n) if l != i])
        tot += R.subs(x, nodos[i]) / den
    return sp.cancel(sp.together(tot))


def test(d1, d2, t, gammas):
    x = sp.Symbol('X')
    xi = sp.symbols('x1:%d' % (d2 + 1))
    R, a = filas_R(d1, d2, t, gammas, x)

    O = sp.Matrix(d2, d2, lambda i, j: sp.expand(R[i].subs(x, xi[j])))
    V = vandermonde(xi)
    q, r = sp.div(sp.Poly(sp.expand(O.det()), *xi), sp.Poly(sp.expand(V), *xi))
    assert r == 0
    P = sp.expand(q.as_expr())

    N = sp.Matrix(d2, d2, lambda i, j: dif_dividida(R[i], x, list(xi[:j + 1])))
    D = sp.expand(sp.cancel(N.det()))
    ok = sp.expand(D - P) == 0
    print("  d1=%d d2=%d t=%d S=%-10s : P_S == det(diferencias divididas) -> %s"
          % (d1, d2, t, str(tuple(gammas)), ok))
    return ok


CASOS = [
    (2, 2, 2, (0,)),
    (3, 3, 4, (1,)),
    (2, 3, 3, (0,)),
    (2, 3, 3, (2,)),
    (3, 4, 5, (2,)),
    (2, 5, 3, (0, 1)),
]

if __name__ == '__main__':
    print("LEMA de Newton:  P_S = det( R_i[xi_1,...,xi_j] )")
    todo = all(test(*c) for c in CASOS)
    print("\n%s" % ("=== TODO OK ===" if todo else "=== HAY FALLAS ==="))
