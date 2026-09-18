# -*- coding: utf-8 -*-
"""
Line 3, open item 2: expansion of P_S in the basis {s_nu(Xi - A)} for ARBITRARY S.

Idea: in the multi-Schur determinant of Theorem A every row is a combination of
the "basic rows" u_r := h_r(Xi - A):

    row of f     (eps):    H_{eps-d2+q}  = a_{d1} * u_{eps-d2+q}
    monomial row (gamma):  h_{gamma-d2+q}(Xi) = sum_s h_s(A) * u_{gamma-s-d2+q}

    (because Xi = (Xi - A) + A, hence h_r(Xi) = sum_s h_s(A) h_{r-s}(Xi-A))

That is, M = C * U with U_{r,q} = u_{r-d2+q}. Cauchy-Binet then gives

    P_S = sgn(sigma) * sum_E det(C_{:,E}) * s_{nu(E)}(Xi - A)

with coefficients det(C_{:,E}) that are symmetric functions of the roots of f
ONLY. (The two factors (-1)^{d2(d2-1)/2} -- the one from Theorem A and the one
from passing from the increasing row order to the Jacobi-Trudi order -- cancel.)

So that the h_s(A) are polynomial we take f MONIC (a_{d1} = 1); in general they
live in Z[a][1/a_{d1}].

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import os
import sys
import sympy as sp
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dks_univariate import O_matrix, vandermonde, k_of
from natural_basis import orden_decreciente, signo_permutacion


def monico(expr, a, d1):
    return sp.expand(expr.subs(a[d1], 1))


def test(d1, d2, t, gammas, Rmax_extra=2):
    O, a, xi, tstar, eps, kind = O_matrix(d1, d2, t, gammas)
    P = sp.expand(sp.div(sp.Poly(sp.expand(O.det()), *xi),
                         sp.Poly(vandermonde(xi), *xi))[0].as_expr())
    P = monico(P, a, d1)

    z = sp.Symbol('z')
    N = max(eps) + d2 + 3
    # u_r = h_r(Xi - A) = [z^r] f_rev(z)/(a_{d1} prod(1-xi z)), con a_{d1}=1
    denom = sp.prod([1 - x * z for x in xi])
    f_rev = sum(a[d1 - j] * z**j for j in range(d1 + 1)).subs(a[d1], 1)
    E_ = [sp.Integer(1)]
    for x in xi:
        prev = E_ + [sp.Integer(0)]
        E_ = [sp.expand(prev[j] - (x * prev[j - 1] if j > 0 else 0)) for j in range(len(prev))]
    hxi = [sp.Integer(1)]
    for r in range(1, N + 1):
        hxi.append(sp.expand(-sum(E_[j] * hxi[r - j] for j in range(1, min(r, len(E_) - 1) + 1))))
    frev = [sp.Integer(1) if j == 0 else a[d1 - j] for j in range(d1 + 1)]
    u = [sp.expand(sum(frev[j] * hxi[r - j] for j in range(0, min(r, d1) + 1)))
         for r in range(N + 1)]
    # h_s(A) = [z^s] 1/f_rev(z)  (serie, f monico => f_rev(0)=1)
    hA = [sp.Integer(1)]
    for s in range(1, N + 1):
        hA.append(sp.expand(-sum(frev[j] * hA[s - j] for j in range(1, min(s, d1) + 1))))

    # matriz C: d2 filas, columnas indexadas por r = 0..Rmax
    Rmax = max(eps) + Rmax_extra
    C = sp.zeros(d2, Rmax + 1)
    for i in range(d2):
        if kind[i] == 'f':
            C[i, eps[i]] = 1                       # a_{d1} = 1
        else:
            for s in range(0, eps[i] + 1):
                C[i, eps[i] - s] = hA[s]

    perm = orden_decreciente(eps)
    sgn = signo_permutacion(perm)

    total, terms = 0, []
    for Eset in combinations(range(Rmax + 1), d2):
        m = sp.expand(C[[perm[i] for i in range(d2)], list(Eset)].det())
        if m == 0:
            continue
        # JT: nu_p = r_{d2+1-p} - d2 + p  (filas en orden decreciente)
        rs = sorted(Eset)
        nu = tuple(rs[d2 - 1 - p] - (d2 - 1 - p) for p in range(d2))
        if any(n < 0 for n in nu):
            continue
        L = d2
        D = sp.Matrix(L, L, lambda p, q: u[nu[p] - (p + 1) + (q + 1)]
                      if 0 <= nu[p] - (p + 1) + (q + 1) <= N else sp.Integer(0)).det()
        terms.append((tuple(n for n in nu if n > 0), sp.factor(m)))
        total += m * D
    ok = sp.expand(sgn * total - P) == 0
    print("  d1=%d d2=%d t=%d S=%-10s : %s   [%d terminos, signo %+d]"
          % (d1, d2, t, str(tuple(gammas)), "OK" if ok else "FALLA", len(terms), sgn))
    for nu, c in terms:
        print("       s_%-12s(Xi-A)  *  (%s)" % (str(nu), c))
    return ok


CASOS = [
    (3, 3, 4, (1,)),      # S con hueco
    (2, 3, 3, (2,)),      # S con hueco
    (3, 3, 3, (0, 1)),    # intervalo inicial (deberia dar UN solo termino)
    (4, 4, 5, (0, 2)),    # S con hueco
]

if __name__ == '__main__':
    print("Expansion de P_S en la base {s_nu(Xi - A)}  (f monico)")
    todo = all(test(*c) for c in CASOS)
    print("\n%s" % ("=== TODO OK ===" if todo else "=== HAY FALLAS ==="))
