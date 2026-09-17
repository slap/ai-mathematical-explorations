# -*- coding: utf-8 -*-
"""
Non-membership in the radical, EVERYTHING over Q, in the Schaub-Spivakovsky
setting (arXiv:2312.08742):

    f = x^d + a_1 x^{d-1} + ... + a_{d-1} x          in Q[a_1,...,a_{d-1}][x]
    H_i(f) = i-th Hasse derivative
    R_i = Res(f, H_i(f)),   i = 1, ..., d-1.

Their Theorem 5: R_i is not in sqrt(R_1,..,R_i omitted,..,R_{d-1}) for i in
{d-3,d-2,d-1}.

CLAIM: it holds for EVERY i in {1,...,d-1}, with explicit witnesses:
    i <= d-2 :  f = x^i (x^{d-i} + 1)     (a_{d-i} = 1, the rest 0)
    i  = d-1 :  f = x^{d-1} (x - 1)       (a_1 = -1, the rest 0)
At the witness all R_j with j != i vanish and R_i != 0. Since R_i vanishes on
V(R_j : j != i) if and only if R_i is in the radical (Nullstellensatz over C,
and the R_j have coefficients in Z), a single point suffices.

Checks:
  (1) evaluation of the R_j at the witnesses, d = 3..10;
  (2) independent radical test by Groebner bases (Rabinowitsch trick:
      R_i in sqrt(J)  <=>  1 in J + (1 - y·R_i)), for small d.

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import sys
from sage.all import QQ, PolynomialRing, binomial


def sistema(d):
    A = PolynomialRing(QQ, ['a%d' % k for k in range(1, d)] + ['y'], order='degrevlex')
    a = [A.one()] + [A.gen(k - 1) for k in range(1, d)]          # a[0] = 1
    Rx = PolynomialRing(A, 'x')
    x = Rx.gen()
    f = sum(a[k] * x**(d - k) for k in range(d))                 # a_d = 0
    Rs = []
    for i in range(1, d):
        Hi = sum(binomial(d - k, i) * a[k] * x**(d - k - i) for k in range(d - i + 1))
        Rs.append(A(f.resultant(Hi)))
    return A, Rs


def testigo(d, i, A):
    """Diccionario de sustitucion a_k -> valor para el testigo del indice i."""
    val = {A.gen(k - 1): 0 for k in range(1, d)}
    if i <= d - 2:
        val[A.gen(d - i - 1)] = 1            # a_{d-i} = 1  <->  f = x^d + x^i
    else:
        val[A.gen(0)] = -1                   # a_1 = -1     <->  f = x^d - x^{d-1}
    return val


def chequeo_testigos(dmax):
    print("(1) evaluacion en testigos explicitos")
    todo = True
    for d in range(3, dmax + 1):
        A, Rs = sistema(d)
        fila = []
        for i in range(1, d):
            v = testigo(d, i, A)
            valores = [R.subs(v) for R in Rs]
            ok = all(valores[j - 1] == 0 for j in range(1, d) if j != i) and valores[i - 1] != 0
            todo &= ok
            fila.append("i=%d:%s" % (i, "ok" if ok else "FALLA"))
        print("    d=%-2d  %s" % (d, "  ".join(fila)))
    return todo


def chequeo_groebner(dmax):
    print("(2) test de radical por Groebner:  1 en (R_j : j != i) + (1 - y R_i) ?")
    todo = True
    for d in range(3, dmax + 1):
        A, Rs = sistema(d)
        y = A.gens()[-1]
        fila = []
        for i in range(1, d):
            J = A.ideal([Rs[j - 1] for j in range(1, d) if j != i] + [1 - y * Rs[i - 1]])
            en_radical = (J.groebner_basis() == [1])
            todo &= not en_radical
            fila.append("i=%d:%s" % (i, "no pertenece" if not en_radical else "PERTENECE"))
        print("    d=%-2d  %s" % (d, "  ".join(fila)))
    return todo


if __name__ == '__main__':
    dmax_t = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    dmax_g = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    ok1 = chequeo_testigos(dmax_t)
    print()
    ok2 = chequeo_groebner(dmax_g)
    print()
    print("TODO OK" if (ok1 and ok2) else "HAY FALLAS")
