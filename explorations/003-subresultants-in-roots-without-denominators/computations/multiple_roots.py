# -*- coding: utf-8 -*-
"""
Extension to multiple roots (univariate case).

If g has distinct roots y_1,...,y_s with multiplicities m_1,...,m_s
(sum m_i = d2), both |O_S| and V_{d2} vanish: the formula of Theorem 2.2 is
0/0. The confluent version replaces, for each root y_i, the m_i repeated
columns by the divided derivatives

        column (i, r)  =  (1/r!) d^r/dy_i^r  [ row evaluated at y_i ],   0 <= r < m_i.

With that normalisation the confluent Vandermonde determinant is exactly

        V^conf  =  prod_{i<j} (y_j - y_i)^{m_i m_j}.

CONJECTURE (C4) tested here:

        |O_S^conf| / V^conf   =   P_S(y_1,...,y_1, y_2,...,y_2, ...)

that is: the universal polynomial P_S of the simple-root case, evaluated at the
multiset of roots, computes the confluent case. Equivalently: the diagram "take
the quotient" / "specialise the roots" commutes, and no new formula is needed
for multiple roots, only the correct reading of numerator and denominator.

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import sympy as sp

from dks_univariate import O_matrix, check_divisibility, k_of


def confluente(exprs_por_fila, xsym, patron):
    """
    exprs_por_fila: lista de expresiones en la variable xsym (una por fila).
    patron: lista de pares (y_i, m_i).
    Devuelve la matriz confluente: columnas (i, r) con r = 0..m_i-1.
    """
    cols = []
    for (y, m) in patron:
        for r in range(m):
            cols.append([sp.diff(e, xsym, r).subs(xsym, y) / sp.factorial(r)
                         for e in exprs_por_fila])
    n = len(exprs_por_fila)
    return sp.Matrix(n, len(cols), lambda i, j: sp.expand(cols[j][i]))


def vandermonde_confluente(patron):
    ys = [y for (y, m) in patron]
    ms = [m for (y, m) in patron]
    return sp.prod([(ys[j] - ys[i])**(ms[i] * ms[j])
                    for i in range(len(ys)) for j in range(i + 1, len(ys))])


def filas_simbolicas(d1, d2, t, gammas, xsym):
    """Las filas de O_S como funciones de una sola variable x."""
    a = sp.symbols('a0:%d' % (d1 + 1))
    tstar = max(d2 - 1, t)
    f = sum(a[l] * xsym**l for l in range(d1 + 1))
    filas = []
    for g in sorted(gammas):
        filas.append(xsym**g)
    for e in range(t + 1, tstar + 1):
        filas.append(xsym**e)
    for i in range(0, t - d1 + 1):
        filas.append(xsym**i * f)
    return filas, a


def test(d1, d2, t, gammas, patron_mult):
    """patron_mult: lista de multiplicidades, p.ej. [2,1] para d2=3."""
    assert sum(patron_mult) == d2
    print("\n=== d1=%d d2=%d t=%d S=%s   multiplicidades=%s ===" %
          (d1, d2, t, str(gammas), str(patron_mult)))

    # 1) polinomio universal P_S del caso generico
    ok, P = check_divisibility(d1, d2, t, gammas, verbose=False)
    assert ok
    xi = sp.symbols('x1:%d' % (d2 + 1))

    # 2) version confluente
    x = sp.Symbol('X')
    filas, a = filas_simbolicas(d1, d2, t, gammas, x)
    ys = sp.symbols('y1:%d' % (len(patron_mult) + 1))
    patron = list(zip(ys, patron_mult))
    Oc = confluente(filas, x, patron)
    Vc = sp.expand(vandermonde_confluente(patron))
    detOc = sp.expand(Oc.det())
    q, r = sp.div(sp.Poly(detOc, *ys), sp.Poly(Vc, *ys))
    print("  division exacta en el caso confluente : %s" % (r == 0))

    # 3) P_S especializado al multiconjunto de raices
    sust = {}
    idx = 0
    for (y, m) in patron:
        for _ in range(m):
            sust[xi[idx]] = y
            idx += 1
    P_esp = sp.expand(P.subs(sust, simultaneous=True))
    coinciden = sp.expand(q.as_expr() - P_esp) == 0
    print("  |O^conf|/V^conf  ==  P_S(raices con multiplicidad) : %s" % coinciden)
    if not coinciden:
        print("    cociente confluente :", sp.factor(q.as_expr()))
        print("    P_S especializado   :", sp.factor(P_esp))
    return (r == 0) and coinciden


CASOS = [
    (2, 2, 2, (0,),    [2]),
    (3, 3, 4, (1,),    [2, 1]),
    (3, 3, 4, (1,),    [3]),
    (2, 3, 3, (0,),    [2, 1]),
    (2, 3, 3, (2,),    [3]),
    (4, 4, 5, (0, 2),  [2, 2]),
    (4, 4, 5, (0, 2),  [3, 1]),
    (3, 4, 5, (2,),    [2, 1, 1]),
]

if __name__ == '__main__':
    todo = True
    for c in CASOS:
        todo &= test(*c)
    print("\n================ TODO OK ================" if todo
          else "\n============== HAY FALLAS ==============")
