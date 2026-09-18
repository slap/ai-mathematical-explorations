# -*- coding: utf-8 -*-
"""
Line 3 of the plan: the natural basis.

(A) EXACT SIGN of the multi-Schur formula.
    Conjecture: ordering the rows of O_S by DECREASING eps,

        P_S = (-1)^{d2(d2-1)/2} * det( X_{eps_i - d2 + j}(A_i) )_{i,j=1..d2}

    with X = h (alphabet Xi) on the monomial rows and X = H (alphabet Xi - A)
    on the rows coming from f. With the row order of the paper one must
    multiply in addition by the sign of the reordering permutation.

(B) CLASSICAL CASE -> A SINGLE SUPERSYMMETRIC SCHUR FUNCTION.
    For the classical scalar subresultant S_k^{(j)} one takes
        t = d1 + d2 - k - 1,   S_j = {x^i : 0 <= i <= k, i != j}
    (Remark 2.1(2) of the paper). Conjecture: in that case the quotient
    collapses to

        P_{S_j} = +- s_nu(Xi - A) := +- det( H_{nu_p - p + q} )_{p,q=1..m},
        m = d2 - k,

    that is, a SINGLE Jacobi-Trudi determinant in the difference alphabet.
    The script searches for the partition nu and reports the pattern.

Grading used: deg(xi) = 1, deg(a_{d1-j}) = j. With it H_r and h_r are
homogeneous of degree r, |O_S| has degree sum_i eps_i, V has degree C(d2,2),
and therefore |nu| = sum_i eps_i - C(d2,2).

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

import os
import sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dks_univariate import O_matrix, check_divisibility, H_series, k_of


# ------------------------------------------------------------------ utilidades

def signo_permutacion(perm):
    """Signo de la permutacion dada como lista de indices."""
    n, visto, s = len(perm), [False] * len(perm), 1
    for i in range(n):
        if visto[i]:
            continue
        j, ciclo = i, 0
        while not visto[j]:
            visto[j] = True
            j = perm[j]
            ciclo += 1
        if ciclo % 2 == 0:
            s = -s
    return s


def orden_decreciente(eps):
    """Permutacion (estable) que ordena las filas por eps decreciente."""
    return sorted(range(len(eps)), key=lambda i: (-eps[i], i))


def particiones(n, k, cota):
    """Particiones de n con a lo sumo k partes, cada parte <= cota."""
    if k == 0:
        if n == 0:
            yield ()
        return
    for primera in range(min(n, cota), -1, -1):
        for resto in particiones(n - primera, k - 1, primera):
            yield (primera,) + resto


# ------------------------------------------------------------------------ (A)

def signo_predicho(d1, d2, t, gammas):
    O, a, xi, tstar, eps, kind = O_matrix(d1, d2, t, gammas)
    perm = orden_decreciente(eps)
    return signo_permutacion(perm) * (-1)**(d2 * (d2 - 1) // 2), eps, kind, perm


def test_signo(d1, d2, t, gammas):
    ok, P = check_divisibility(d1, d2, t, gammas, verbose=False)
    assert ok
    eps_sign, eps, kind, perm = signo_predicho(d1, d2, t, gammas)
    N = max(eps) + d2 + 2
    h, H = H_series(d1, d2, t, gammas, N)

    def entry(i, j):
        r = eps[i] - d2 + (j + 1)
        return sp.Integer(0) if r < 0 else (H if kind[i] == 'f' else h)[r]

    M = sp.Matrix(d2, d2, lambda ii, j: entry(perm[ii], j))
    D = sp.expand(M.det())
    ok = sp.expand(eps_sign * D - P) == 0
    print("  d1=%d d2=%d t=%d S=%-10s  eps=%-16s signo predicho=%+d  ->  %s"
          % (d1, d2, t, str(gammas), str(eps), eps_sign, "OK" if ok else "FALLA"))
    return ok


# ------------------------------------------------------------------------ (B)

def jacobi_trudi_H(nu, H):
    """det( H_{nu_p - p + q} )_{p,q=1..m}, con H_r = 0 si r < 0."""
    m = len(nu)
    def e(p, q):
        r = nu[p] - (p + 1) + (q + 1)
        return sp.Integer(0) if r < 0 else H[r]
    return sp.expand(sp.Matrix(m, m, e).det())


def caso_clasico(d1, d2, k, j, verbose=True):
    """S_j = {0..k} \\ {j},  t = d1+d2-k-1.  Busca nu con P_{S_j} = +- s_nu(Xi-A)."""
    t = d1 + d2 - k - 1
    S = tuple(i for i in range(k + 1) if i != j)
    assert len(S) == k_of(d1, d2, t), "|S| != k"
    ok, P = check_divisibility(d1, d2, t, S, verbose=False)
    assert ok

    O, a, xi, tstar, eps, kind = O_matrix(d1, d2, t, S)
    grado = sum(eps) - d2 * (d2 - 1) // 2
    m = d2 - k
    N = grado + m + 2
    h, H = H_series(d1, d2, t, S, N)

    # OJO con la normalizacion: H_r = a_{d1} * h_r(Xi - A), o sea H_0 = a_{d1}
    # y NO 1. Por eso un determinante de tamanio L aporta a_{d1}^L, y el tamanio
    # importa: para nu con mas de m partes hay que comparar contra
    # a_{d1}^{L-m} * P. (Para el alfabeto diferencia no hay cota de longitud:
    # s_nu(X-Y) se anula solo fuera del gancho (|X|,|Y|).)
    hallado = []
    a = sp.symbols('a0:%d' % (d1 + 1))
    for L in range(m, m + 4):
        objetivo = sp.expand(a[d1]**(L - m) * P)
        for nu in particiones(grado, L, grado):
            if len(nu) > L:
                continue
            D = jacobi_trudi_H(tuple(nu) + (0,) * (L - len(nu)), H)
            if sp.expand(D - objetivo) == 0:
                hallado.append((tuple(x for x in nu if x > 0), +1, L))
            elif sp.expand(D + objetivo) == 0:
                hallado.append((tuple(x for x in nu if x > 0), -1, L))
        if hallado:
            break
    if verbose:
        print("  d1=%d d2=%d k=%d j=%d | m=%d |nu|=%d -> %s"
              % (d1, d2, k, j, m, grado,
                 ", ".join("%s signo %+d L=%d" % (nu, s, L) for nu, s, L in hallado) or "NO ENCONTRADO"))
    return hallado, grado, m


# --------------------------------------------------------------------- driver

CASOS_SIGNO = [
    (2, 2, 2, (0,)), (3, 3, 4, (1,)), (2, 3, 3, (0,)), (2, 3, 3, (2,)),
    (4, 4, 5, (0, 2)), (2, 5, 3, (0, 1)), (5, 2, 4, (1, 4)), (1, 3, 2, (0,)),
]

CASOS_CLASICO = [
    (2, 2, 1, 0), (2, 2, 1, 1),
    (3, 2, 1, 0), (3, 2, 1, 1),
    (3, 3, 1, 0), (3, 3, 1, 1),
    (3, 3, 2, 0), (3, 3, 2, 1), (3, 3, 2, 2),
    (4, 3, 2, 0), (4, 3, 2, 1), (4, 3, 2, 2),
    (2, 4, 1, 0), (2, 4, 1, 1),
    (3, 4, 2, 0), (3, 4, 2, 1), (3, 4, 2, 2),
]


def verifica_rectangulo(d1, d2, k):
    """
    THEOREM (proved by elimination, see notes/01-natural-basis.md):
    for S_k = {1, x, ..., x^{k-1}} (the leading coefficient, j=k),

        P_{S_k} = a_{d1}^{d2-k} * s_{((d1-k)^{d2-k})}(Xi - A)
                = det( H_{(d1-k) - p + q} )_{p,q=1..d2-k}

    with no sign (the ordering permutation cancels (-1)^{d2(d2-1)/2} exactly).
    """
    t = d1 + d2 - k - 1
    S = tuple(range(k))
    ok, P = check_divisibility(d1, d2, t, S, verbose=False)
    assert ok
    m = d2 - k
    N = (d1 - k) + m + 2
    h, H = H_series(d1, d2, t, S, N)
    rect = ((d1 - k),) * m
    D = jacobi_trudi_H(rect, H)
    igual = sp.expand(D - P) == 0
    print("  d1=%d d2=%d k=%d : nu = (%d)^%d  ->  %s"
          % (d1, d2, k, d1 - k, m, "OK" if igual else "FALLA"))
    return igual


CASOS_RECTANGULO = [(d1, d2, k)
                    for d1 in range(2, 6) for d2 in range(2, 6)
                    for k in range(0, min(d1, d2) + 1)
                    if d1 + d2 - k - 1 >= 0]


def main():
    print("(A) SIGNO EXACTO de la formula multi-Schur")
    todo = all(test_signo(*c) for c in CASOS_SIGNO)
    print("    -> %s\n" % ("todos OK" if todo else "HAY FALLAS"))

    print("(B) CASO CLASICO: P_{S_j} como unica Schur supersimetrica s_nu(Xi - A)")
    tabla = []
    for (d1, d2, k, j) in CASOS_CLASICO:
        hallado, grado, m = caso_clasico(d1, d2, k, j)
        tabla.append((d1, d2, k, j, m, grado, hallado))
    print("\n  resumen (d1, d2, k, j) -> nu:")
    for (d1, d2, k, j, m, grado, hallado) in tabla:
        print("    (%d,%d,%d,%d): %s" % (d1, d2, k, j,
              ", ".join(str(nu) for nu, s, L in hallado) or "-"))


if __name__ == '__main__':
    main()
