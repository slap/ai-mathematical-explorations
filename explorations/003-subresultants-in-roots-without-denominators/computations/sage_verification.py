# -*- coding: utf-8 -*-
"""
Verification in SageMath (much faster than sympy, and with native symmetric
functions to cross-check against).

Run from Windows:
    wsl -d Ubuntu-24.04 -- bash -lc '~/miniforge3/envs/sage/bin/sage -python \
        /mnt/c/.../research-subresultantes/experiments/sage_verification.py'

Checks:
  (T1) V | |O_S| and the quotient P_S is symmetric.
  (T3) P_S = (-1)^{d2(d2-1)/2} sgn(sigma) det( X_{eps_i-d2+j}(A_i) ).
  (REC) Rectangle theorem: for S = {1,...,x^{k-1}} (leading coefficient),
        P_S = det( H_{(d1-k)-p+q} )_{p,q=1..d2-k} = a_{d1}^{d2-k} s_{((d1-k)^{d2-k})}(Xi-A).
  (SF) Independent cross-check with Sage's native symmetric functions: P_S is
       expanded in the Schur basis and compared with the maximal minors of the
       band matrix of f (Theorem T2).

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

from sage.all import (PolynomialRing, QQ, matrix, prod, Permutation,
                      SymmetricFunctions, Partition)


# --------------------------------------------------------------------- setup

def k_of(d1, d2, t):
    return t + 1 - max(0, t - d1 + 1) - max(0, t - d2 + 1)


def anillo(d1, d2):
    A = PolynomialRing(QQ, ['a%d' % i for i in range(d1 + 1)])
    R = PolynomialRing(A, ['x%d' % (j + 1) for j in range(d2)])
    return A, R


def filas(d1, d2, t, gammas, R, A):
    """Filas de O_S: devuelve (lista de filas, eps, kind)."""
    tstar = max(d2 - 1, t)
    x = R.gens()
    a = [R(A.gen(i)) for i in range(d1 + 1)]
    f = lambda z: sum(a[l] * z**l for l in range(d1 + 1))
    F, eps, kind = [], [], []
    for g in sorted(gammas):
        F.append([xj**g for xj in x]);          eps.append(g);      kind.append('mon')
    for e in range(t + 1, tstar + 1):
        F.append([xj**e for xj in x]);          eps.append(e);      kind.append('mon')
    for i in range(0, t - d1 + 1):
        F.append([xj**i * f(xj) for xj in x]);  eps.append(i + d1); kind.append('f')
    assert len(F) == d2
    return F, eps, kind


def vandermonde(R):
    x = R.gens()
    d = len(x)
    return prod([x[j] - x[i] for i in range(d) for j in range(i + 1, d)])


def series_h_H(d1, d2, R, A, N):
    """h_r = [z^r] 1/prod(1-x z);  H_r = [z^r] f_rev(z)/prod(1-x z)."""
    x = R.gens()
    E = [R.one()]
    for xi in x:
        prev = E + [R.zero()]
        E = [prev[j] - (xi * prev[j - 1] if j > 0 else R.zero()) for j in range(len(prev))]
    h = [R.one()]
    for r in range(1, N + 1):
        h.append(-sum(E[j] * h[r - j] for j in range(1, min(r, len(E) - 1) + 1)))
    frev = [R(A.gen(d1 - j)) for j in range(d1 + 1)]
    H = [sum(frev[j] * h[r - j] for j in range(0, min(r, d1) + 1)) for r in range(N + 1)]
    return h, H


def P_de(d1, d2, t, gammas):
    A, R = anillo(d1, d2)
    F, eps, kind = filas(d1, d2, t, gammas, R, A)
    detO = matrix(R, F).determinant()
    V = vandermonde(R)
    q, r = detO.quo_rem(V)
    return A, R, q, (r == 0), eps, kind


# ----------------------------------------------------------------- chequeos

def test_T1_T3(d1, d2, t, gammas):
    A, R, P, exacto, eps, kind = P_de(d1, d2, t, gammas)
    x = R.gens()
    sim = all(P == P.subs({x[0]: x[j], x[j]: x[0]}) for j in range(1, d2))

    perm = sorted(range(d2), key=lambda i: (-eps[i], i))
    sgn = Permutation([p + 1 for p in perm]).signature()
    signo = sgn * (-1)**(d2 * (d2 - 1) // 2)
    h, H = series_h_H(d1, d2, R, A, max(eps) + d2 + 2)

    def ent(i, j):
        r = eps[i] - d2 + (j + 1)
        return R.zero() if r < 0 else (H if kind[i] == 'f' else h)[r]

    D = matrix(R, d2, d2, lambda ii, j: ent(perm[ii], j)).determinant()
    t3 = (signo * D == P)
    print("  T1/T3  d1=%d d2=%d t=%d S=%-12s : div=%s sim=%s multiSchur(signo %+d)=%s"
          % (d1, d2, t, str(tuple(gammas)), exacto, sim, signo, t3))
    return exacto and sim and t3


def test_rectangulo(d1, d2, k):
    t = d1 + d2 - k - 1
    S = tuple(range(k))
    assert len(S) == k_of(d1, d2, t)
    A, R, P, exacto, eps, kind = P_de(d1, d2, t, S)
    m = d2 - k
    h, H = series_h_H(d1, d2, R, A, (d1 - k) + m + 2)
    D = matrix(R, m, m,
               lambda p, q: H[(d1 - k) - (p + 1) + (q + 1)]
               if (d1 - k) - (p + 1) + (q + 1) >= 0 else R.zero()).determinant()
    ok = exacto and (D == P)
    print("  RECT   d1=%d d2=%d k=%d : nu=(%d)^%d -> %s" % (d1, d2, k, d1 - k, m, "OK" if ok else "FALLA"))
    return ok


def test_schur_nativo(d1, d2, t, gammas):
    """
    Contraste independiente: expandir P_S en la base de Schur con las funciones
    simetricas NATIVAS de Sage, y comparar con los menores maximales de la
    matriz banda de f (T2).
    """
    A, R, P, exacto, eps, kind = P_de(d1, d2, t, gammas)
    tstar = max(d2 - 1, t)
    B = matrix(A, d2, tstar + 1)
    fila = 0
    for g in sorted(gammas):
        B[fila, g] = 1; fila += 1
    for e in range(t + 1, tstar + 1):
        B[fila, e] = 1; fila += 1
    for i in range(0, t - d1 + 1):
        for l in range(d1 + 1):
            B[fila, i + l] = A.gen(l)
        fila += 1

    # OJO: NO usar Sym.from_polynomial(). Eso levanta P a Lambda (infinitas
    # variables), donde la expansion de Schur tiene terminos con ell(lambda) > d2
    # que solo se anulan al restringir a d2 variables. El enunciado T2 es la
    # expansion en FINITAS variables, asi que comparamos polinomios.
    from itertools import combinations
    s = SymmetricFunctions(QQ).schur()
    x = R.gens()
    total, nterm = R.zero(), 0
    for E in combinations(range(tstar + 1), d2):
        menor = B.matrix_from_columns(list(E)).determinant()
        if menor == 0:
            continue
        lam = [E[d2 - 1 - r] - (d2 - 1 - r) for r in range(d2)]
        lam = Partition([v for v in lam if v > 0])
        total += R(menor) * R(s[lam].expand(d2, alphabet=list(x)))
        nterm += 1
    coincide = (total == P)
    print("  SF     d1=%d d2=%d t=%d S=%-12s : %d terminos Schur (Sage nativo), T2: %s"
          % (d1, d2, t, str(tuple(gammas)), nterm, coincide))
    return coincide


# ------------------------------------------------------------------- driver

if __name__ == '__main__':
    import sys
    seccion = sys.argv[1] if len(sys.argv) > 1 else 'todo'

    if seccion == 'sf':
        ok = all(test_schur_nativo(*c) for c in
                 [(3, 3, 4, (1,)), (4, 4, 5, (0, 2)), (2, 3, 3, (0,)), (3, 4, 5, (2,))])
        print("\n%s" % ("======== SF OK ========" if ok else "======== SF FALLA ========"))
        sys.exit(0)

    print("=== T1 / T3 (divisibilidad, simetria, multi-Schur con signo) ===")
    casos = [(2, 2, 2, (0,)), (3, 3, 4, (1,)), (2, 3, 3, (0,)), (2, 3, 3, (2,)),
             (4, 4, 5, (0, 2)), (2, 5, 3, (0, 1)), (5, 2, 4, (1, 4)),
             (3, 4, 5, (2,)), (1, 3, 2, (0,)), (5, 5, 6, (0, 2, 4)),
             (4, 6, 7, (1, 3)), (6, 4, 6, (0, 3, 5))]
    ok1 = all(test_T1_T3(*c) for c in casos)

    print("\n=== Teorema del rectangulo (coeficiente principal, S={1,...,x^{k-1}}) ===")
    ok2 = True
    for d1 in range(1, 6):
        for d2 in range(1, 6):
            for k in range(0, min(d1, d2) + 1):
                if d1 + d2 - k - 1 >= 0 and k_of(d1, d2, d1 + d2 - k - 1) == k:
                    ok2 &= test_rectangulo(d1, d2, k)

    print("\n=== Contraste con funciones simetricas nativas de Sage (T2) ===")
    ok3 = all(test_schur_nativo(*c) for c in
              [(3, 3, 4, (1,)), (4, 4, 5, (0, 2)), (2, 3, 3, (0,)), (3, 4, 5, (2,))])

    print("\n%s" % ("======== TODO OK ========" if (ok1 and ok2 and ok3)
                    else "======== HAY FALLAS ========"))
