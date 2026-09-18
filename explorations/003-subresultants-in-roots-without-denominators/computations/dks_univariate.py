# -*- coding: utf-8 -*-
"""
Symbolic verification of the project's conjectures, univariate case.

Framework (D'Andrea-Krick-Szanto 2005, Theorem 2.2):

    Delta_S = sg(S) * b_{d2}^{t*-d2+1} * |O_S| / V_{d2}

where O_S is the d2 x d2 matrix whose columns are indexed by the roots
xi_1,...,xi_{d2} of g, with rows:
    * xi_j^{gamma}        for each x^gamma in S             (k rows)
    * xi_j^{e}            for e = t+1,...,t*                (t*-t rows)
    * xi_j^{i} f(xi_j)    for i = 0,...,t-d1                (t-d1+1 rows)
and V_{d2} = det(xi_j^{i-1}) = prod_{i<j} (xi_j - xi_i).

The conjectures tested here:

 (C1) DIVISIBILITY: |O_S| is alternating in xi_1,...,xi_{d2}, hence
      V_{d2} | |O_S| in Z[a_0..a_d1][xi_1..xi_d2]. The quotient P_S is
      symmetric in the xi and polynomial (no denominators).

 (C2) EXPLICIT FORMULA (Cauchy-Binet):  O_S = B * W  with
      W = (xi_j^e)_{0<=e<=t*}  and  B the "exponent selection" matrix
      (unit rows for Gamma, band rows of the coefficients of f). Then
          P_S = sum_{E subset {0..t*}, |E|=d2}  det(B_{:,E}) * s_{lambda(E)}(xi)
      that is: the quotient expands in the SCHUR BASIS of the roots of g with
      coefficients = maximal minors of the band matrix of f.

 (C3) MULTI-SCHUR / JACOBI-TRUDI with a difference of alphabets:
          P_S = +- det( h_{eps_i - d2 + j}(alphabet_i) )_{i,j=1..d2}
      with alphabet_i = Xi on the monomial rows and Xi - A (roots of f) on the
      rows coming from f; eps_i = total degree of the row.
      Denominator-free normalisation:  H_r := [z^r] f_rev(z)/prod(1-xi z).

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import sympy as sp
from itertools import combinations


# ---------------------------------------------------------------- utilidades

def k_of(d1, d2, t):
    """Formula (5) del paper."""
    return t + 1 - max(0, t - d1 + 1) - max(0, t - d2 + 1)


def setup(d1, d2, t, gammas):
    tstar = max(d2 - 1, t)
    k = k_of(d1, d2, t)
    assert len(gammas) == k, "|S| debe ser k=%d, recibi %d" % (k, len(gammas))
    assert all(0 <= g <= t for g in gammas) and len(set(gammas)) == k
    a = sp.symbols('a0:%d' % (d1 + 1))
    xi = sp.symbols('x1:%d' % (d2 + 1))
    return a, xi, tstar, k


def O_matrix(d1, d2, t, gammas):
    """Matriz O_S del Teorema 2.2, y los 'exponentes'/tipo de cada fila."""
    a, xi, tstar, k = setup(d1, d2, t, gammas)
    f = lambda z: sum(a[l] * z**l for l in range(d1 + 1))
    rows, eps, kind = [], [], []
    for g in sorted(gammas):
        rows.append([x**g for x in xi]);           eps.append(g);      kind.append('mon')
    for e in range(t + 1, tstar + 1):
        rows.append([x**e for x in xi]);           eps.append(e);      kind.append('mon')
    for i in range(0, t - d1 + 1):
        rows.append([x**i * f(x) for x in xi]);    eps.append(i + d1); kind.append('f')
    assert len(rows) == d2, "filas=%d != d2=%d" % (len(rows), d2)
    return sp.Matrix(rows), a, xi, tstar, eps, kind


def vandermonde(xi):
    d = len(xi)
    return sp.prod([xi[j] - xi[i] for i in range(d) for j in range(i + 1, d)])


def schur_bialternant(lam, xi):
    """
    s_lambda(xi) via formula bialternante, en la convencion de exponentes
    CRECIENTES (la misma que usa V = det(xi_j^{i-1}) = prod_{i<j}(xi_j-xi_i)):
    la fila i (0-indexada) tiene exponente lam[d-1-i] + i.
    """
    d = len(xi)
    lam = list(lam) + [0] * (d - len(lam))
    num = sp.Matrix(d, d, lambda i, j: xi[j]**(lam[d - 1 - i] + i))
    q, r = sp.div(sp.Poly(sp.expand(num.det()), *xi), sp.Poly(vandermonde(xi), *xi))
    assert r == 0, "el alternante no es divisible por el Vandermonde"
    return q.as_expr()


def partition_of(E, d2):
    """E = {e_1<...<e_d2} -> particion lambda_r = e_{d2-r} - (d2-1-r)."""
    E = sorted(E)
    return tuple(E[d2 - 1 - r] - (d2 - 1 - r) for r in range(d2))


# ------------------------------------------------------------------- (C1)

def check_divisibility(d1, d2, t, gammas, verbose=True):
    O, a, xi, tstar, eps, kind = O_matrix(d1, d2, t, gammas)
    detO = sp.expand(O.det())
    V = sp.expand(vandermonde(xi))
    q, r = sp.div(sp.Poly(detO, *xi), sp.Poly(V, *xi))
    exact = (r == 0)
    P = sp.expand(q.as_expr())
    if verbose:
        print("  (C1) division exacta por Vandermonde  : %s" % exact)
    sym = all(sp.expand(P - P.subs({xi[0]: xi[j], xi[j]: xi[0]}, simultaneous=True)) == 0
              for j in range(1, d2))
    if verbose:
        print("  (C1) cociente simetrico en las raices : %s" % sym)
    return (exact and sym), P


# ------------------------------------------------------------------- (C2)

def B_matrix(d1, d2, t, gammas):
    """Matriz d2 x (t*+1) tal que O_S = B * W,  W = (xi_j^e)_{e=0..t*}."""
    a, xi, tstar, k = setup(d1, d2, t, gammas)
    B = sp.zeros(d2, tstar + 1)
    row = 0
    for g in sorted(gammas):
        B[row, g] = 1; row += 1
    for e in range(t + 1, tstar + 1):
        B[row, e] = 1; row += 1
    for i in range(0, t - d1 + 1):
        for l in range(d1 + 1):
            B[row, i + l] = a[l]
        row += 1
    return B, a, xi, tstar


def check_cauchy_binet(d1, d2, t, gammas, P, verbose=True):
    B, a, xi, tstar = B_matrix(d1, d2, t, gammas)
    total, terms = 0, []
    for E in combinations(range(tstar + 1), d2):
        m = sp.expand(B[:, list(E)].det())
        if m == 0:
            continue
        lam = partition_of(E, d2)
        terms.append((lam, sp.factor(m)))
        total += m * schur_bialternant(lam, xi)
    ok = sp.expand(total - P) == 0
    if verbose:
        print("  (C2) expansion de Schur (Cauchy-Binet): %s   [%d terminos]" % (ok, len(terms)))
        for lam, m in terms:
            print("        s_%s  *  (%s)" % (lam, m))
    return ok, terms


# ------------------------------------------------------------------- (C3)

def H_series(d1, d2, t, gammas, N):
    """
    h_r = [z^r]     1     / prod_j (1 - xi_j z)      (alfabeto Xi)
    H_r = [z^r] f_rev(z)  / prod_j (1 - xi_j z)      (alfabeto Xi - A)
    """
    a, xi, tstar, k = setup(d1, d2, t, gammas)
    # E[j] = coeficiente de z^j en prod_j (1 - xi_j z) = (-1)^j e_j(xi)
    E = [sp.Integer(1)]
    for x in xi:
        prev = E + [sp.Integer(0)]
        E = [sp.expand(prev[j] - (x * prev[j - 1] if j > 0 else 0)) for j in range(len(prev))]
    # h_r = [z^r] 1/prod(1-xi z)  por recursion  h_r = -sum_{j>=1} E[j] h_{r-j}
    h = [sp.Integer(1)]
    for r in range(1, N + 1):
        h.append(sp.expand(-sum(E[j] * h[r - j] for j in range(1, min(r, len(E) - 1) + 1))))
    # H_r = [z^r] f_rev(z)/prod(1-xi z),  f_rev(z) = sum_j a_{d1-j} z^j
    frev = [a[d1 - j] for j in range(d1 + 1)]
    H = [sp.expand(sum(frev[j] * h[r - j] for j in range(0, min(r, d1) + 1)))
         for r in range(N + 1)]
    return h, H


def check_multischur(d1, d2, t, gammas, P, verbose=True):
    O, a, xi, tstar, eps, kind = O_matrix(d1, d2, t, gammas)
    N = max(eps) + d2 + 2
    h, H = H_series(d1, d2, t, gammas, N)
    order = sorted(range(d2), key=lambda i: -eps[i])          # exponentes decrecientes

    def entry(i, j):
        r = eps[i] - d2 + (j + 1)
        if r < 0:
            return sp.Integer(0)
        return (H if kind[i] == 'f' else h)[r]

    M = sp.Matrix(d2, d2, lambda ii, j: entry(order[ii], j))
    D = sp.expand(M.det())
    ok_plus = sp.expand(D - P) == 0
    ok_minus = sp.expand(D + P) == 0
    if verbose:
        print("  (C3) determinante multi-Schur         : %s"
              % ('OK (+)' if ok_plus else ('OK (-)' if ok_minus else 'FALLA')))
    return ok_plus or ok_minus


# ------------------------------------------------------------------- driver

CASOS = [
    # (d1, d2, t, S)   con |S| = k(d1,d2,t)
    (2, 2, 2, (0,)),
    (3, 3, 4, (1,)),
    (2, 3, 3, (0,)),
    (2, 3, 3, (2,)),
    (4, 4, 5, (0, 2)),
    (2, 5, 3, (0, 1)),     # Ejemplo 2.4 del paper (t < d2-1, usa t* = d2-1)
    (5, 2, 4, (1, 4)),     # Ejemplo 2.3 del paper
    (3, 4, 5, (2,)),
    (1, 3, 2, (0,)),
]


def main():
    import time
    todo_ok = True
    for (d1, d2, t, S) in CASOS:
        t_ini = time.time()
        k = k_of(d1, d2, t)
        print("\n=== d1=%d d2=%d t=%d t*=%d k=%d S=%s ===" % (d1, d2, t, max(d2 - 1, t), k, str(S)))
        if len(S) != k:
            print("  (saltado: |S| != k)")
            continue
        ok1, P = check_divisibility(d1, d2, t, S)
        print("  cociente P_S = %s" % sp.factor(P))
        ok2, _ = check_cauchy_binet(d1, d2, t, S, P)
        ok3 = check_multischur(d1, d2, t, S, P)
        todo_ok &= (ok1 and ok2 and ok3)
        print("  [%.1f s]" % (time.time() - t_ini))
    print("\n================ TODO OK ================" if todo_ok
          else "\n============== HAY FALLAS ==============")


if __name__ == '__main__':
    main()
