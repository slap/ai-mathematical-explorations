# -*- coding: utf-8 -*-
"""
Closing line 3. Three independent sections:

(a) END-TO-END VALIDATION. Up to here everything was verified *relative* to the
    expression |O_S|/V of DKS. Here we compare against the CLASSICAL definition
    of the scalar subresultant S_k^{(j)} (formula (3) of the paper), closing the
    chain

        S_k^{(j)} = (-1)^{(d1-k)(d2-k)} · sg(S_j) · b_{d2}^{d1-k} · P_{S_j}

    where P_{S_j} = |O_S|/V and the b_l are written in the roots of g:
    b_l = b_{d2}·(-1)^{d2-l}·e_{d2-l}(Xi). This validates Theorem 2.2 as well.

(b) HANKEL / PADE FORM. With a and b INDEPENDENT, let
        c_r := [z^r] f_rev(z)/g_rev(z),   f_rev(z) = sum_j a_{d1-j} z^j,
                                          g_rev(z) = sum_j b_{d2-j} z^j
    (the series of f/g "at infinity"). Conjecture:

        S_k^{(k)} = +- b_{d2}^{d1+d2-2k} · det( c_{(d1-k)-p+q} )_{p,q=1..d2-k}

    that is, Theorem B read as a Toeplitz determinant of the series, which is
    the formulation of the Pade approximation problem.

(c) COEFFICIENTS = SKEW SCHUR. In Theorem C the coefficients are maximal minors
    of the band of the h_s(A). With rows (exponents of Gamma) and columns (F) in
    DECREASING order, the minor is det( h_{gamma_p - f_q}(A) ), which is the
    skew Jacobi-Trudi determinant of the shape

        lambda_p = gamma_p + p,     mu_q = f_q + q.

    We test that the minor is nonzero exactly when mu subset lambda and the skew
    shape has no column of length > d1.

Note: identifiers, comments inside functions and printed messages are still in
Spanish; the scripts are kept exactly as they were run.
"""

from sage.all import (PolynomialRing, QQ, matrix, prod, Permutation,
                      SymmetricFunctions, Partition, PowerSeriesRing, FractionField)
from itertools import combinations


# ------------------------------------------------------------------ comunes

def k_of(d1, d2, t):
    return t + 1 - max(0, t - d1 + 1) - max(0, t - d2 + 1)


def sg_S(gammas, t, tstar):
    """sg(S) tal como se define en las notaciones de [DKS05, sec. 2]."""
    objetivo = (list(sorted(gammas)) + list(range(t + 1, tstar + 1))
                + [c for c in range(t + 1) if c not in gammas])
    return Permutation([v + 1 for v in objetivo]).signature()


def elementales(x):
    """e_0, ..., e_d en las variables x."""
    E = [1]
    for xi in x:
        prev = E + [0]
        E = [prev[j] + (xi * prev[j - 1] if j > 0 else 0) for j in range(len(prev))]
    return E


# ------------------------------------------------------------------------ (a)

def anillo_ab_raices(d1, d2):
    A = PolynomialRing(QQ, ['a%d' % i for i in range(d1 + 1)] + ['bd'])
    R = PolynomialRing(A, ['x%d' % (j + 1) for j in range(d2)])
    return A, R


def P_S(d1, d2, t, gammas, A, R):
    """|O_S| / V, con los a en A y las raices en R."""
    tstar = max(d2 - 1, t)
    x = R.gens()
    a = [R(A.gen(i)) for i in range(d1 + 1)]
    f = lambda z: sum(a[l] * z**l for l in range(d1 + 1))
    filas = []
    for g in sorted(gammas):
        filas.append([xj**g for xj in x])
    for e in range(t + 1, tstar + 1):
        filas.append([xj**e for xj in x])
    for i in range(0, t - d1 + 1):
        filas.append([xj**i * f(xj) for xj in x])
    assert len(filas) == d2
    V = prod([x[j] - x[i] for i in range(d2) for j in range(i + 1, d2)])
    q, r = matrix(R, filas).determinant().quo_rem(V)
    assert r == 0
    return q


def subresultante_clasico(d1, d2, k, j, a, b, anillo):
    """S_k^{(j)} por la formula (3) de [DKS05]."""
    cols = list(range(d1 + d2 - k - 1, k, -1)) + [j]
    filas = []
    for i in range(d2 - k):
        sh = d2 - k - 1 - i
        filas.append([a[c - sh] if 0 <= c - sh <= d1 else anillo.zero() for c in cols])
    for i in range(d1 - k):
        sh = d1 - k - 1 - i
        filas.append([b[c - sh] if 0 <= c - sh <= d2 else anillo.zero() for c in cols])
    return matrix(anillo, filas).determinant()


def test_punta_a_punta(d1, d2, k, j):
    t = d1 + d2 - k - 1
    tstar = max(d2 - 1, t)
    S = tuple(i for i in range(k + 1) if i != j)
    assert len(S) == k_of(d1, d2, t)

    A, R = anillo_ab_raices(d1, d2)
    x = R.gens()
    bd = R(A.gen(d1 + 1))
    e = elementales(x)
    b = [bd * (-1)**(d2 - l) * e[d2 - l] for l in range(d2 + 1)]
    a = [R(A.gen(i)) for i in range(d1 + 1)]

    izq = subresultante_clasico(d1, d2, k, j, a, b, R)
    der = (-1)**((d1 - k) * (d2 - k)) * sg_S(S, t, tstar) * bd**(d1 - k) * P_S(d1, d2, t, S, A, R)
    ok = (izq == der)
    print("  (a) d1=%d d2=%d k=%d j=%d : S_k^(j) clasico == DKS/P_S  ->  %s"
          % (d1, d2, k, j, ok))
    return ok


# ------------------------------------------------------------------------ (b)

def test_hankel(d1, d2, k):
    """
    Con a, b independientes: S_k^{(k)} = +- b_{d2}^{d1+d2-2k} det(c_{(d1-k)-p+q}).

    Para no trabajar en el cuerpo de fracciones (que explota con d1=d2=4), se usa
    chi_r := b_{d2}^{r+1} c_r, que es POLINOMIAL. Como el indice de la entrada
    (p,q) es r_{pq} = (d1-k)-p+q, el exponente (r_{pq}+1) se parte en un termino
    de fila mas uno de columna, asi que la potencia sale afuera del determinante:

        det(c) = b_{d2}^{-m(d1-k+1)} · det(chi),     m = d2-k.
    """
    B = PolynomialRing(QQ, ['a%d' % i for i in range(d1 + 1)] + ['b%d' % i for i in range(d2 + 1)])
    a = [B.gen(i) for i in range(d1 + 1)]
    b = [B.gen(d1 + 1 + i) for i in range(d2 + 1)]
    bd = b[d2]

    m = d2 - k
    N = (d1 - k) + m + 2
    # chi_r = b^r a_{d1-r} - sum_{s>=1} b_{d2-s} b^{s-1} chi_{r-s}
    chi = []
    for r in range(N + 1):
        val = (bd**r * a[d1 - r] if 0 <= d1 - r <= d1 else B.zero())
        val -= sum(b[d2 - s] * bd**(s - 1) * chi[r - s] for s in range(1, min(r, d2) + 1))
        chi.append(val)

    def ent(p, q):
        idx = (d1 - k) - (p + 1) + (q + 1)
        return chi[idx] if 0 <= idx <= N else B.zero()

    D = matrix(B, m, m, ent).determinant() if m > 0 else B.one()
    # S_k^{(k)} · b^{m(d1-k+1)} = +- b^{d1+d2-2k} · det(chi)
    izq = subresultante_clasico(d1, d2, k, k, a, b, B) * bd**(m * (d1 - k + 1))
    der = bd**(d1 + d2 - 2 * k) * D
    signo = 0
    if izq == der:
        signo = +1
    elif izq == -der:
        signo = -1
    print("  (b) d1=%d d2=%d k=%d : S_k^(k) == %s b_{d2}^{%d} det(Toeplitz c)  ->  %s"
          % (d1, d2, k, {1: '+', -1: '-', 0: '?'}[signo], d1 + d2 - 2 * k,
             "OK" if signo else "FALLA"))
    return signo != 0, signo


# ------------------------------------------------------------------------ (c)

def test_skew(d1, d2, t, gammas):
    """
    Menores de la banda de h_s(A) vs forma sesgada lambda/mu.
    f monico (a_{d1} = 1) para que los h_s(A) sean polinomiales.
    """
    Ar = PolynomialRing(QQ, ['a%d' % i for i in range(d1)])   # a_{d1} = 1
    a = list(Ar.gens()) + [Ar.one()]
    tstar = max(d2 - 1, t)
    Gamma = sorted(list(gammas) + list(range(t + 1, tstar + 1)), reverse=True)
    kp = len(Gamma)
    Nmax = max(Gamma) + 1 if Gamma else 1

    # h_s(A) = [z^s] 1/f_rev(z),  f_rev(z) = sum_j a_{d1-j} z^j  (f monico: f_rev(0)=1)
    frev = [a[d1 - j] for j in range(d1 + 1)]
    hA = [Ar.one()]
    for s in range(1, Nmax + 1):
        hA.append(-sum(frev[jj] * hA[s - jj] for jj in range(1, min(s, d1) + 1)))

    lam = [Gamma[p] + (p + 1) for p in range(kp)]
    coincidencias, total = 0, 0
    for Fset in combinations(range(0, Nmax + 1), kp):
        Fdec = sorted(Fset, reverse=True)
        menor = matrix(Ar, kp, kp,
                       lambda p, q: hA[Gamma[p] - Fdec[q]]
                       if 0 <= Gamma[p] - Fdec[q] <= Nmax else Ar.zero()).determinant()
        mu = [Fdec[q] + (q + 1) for q in range(kp)]
        contenido = all(mu[i] <= lam[i] for i in range(kp))
        # columnas de lambda/mu de largo > d1 anulan s_{lambda/mu}(A)
        col_ok = True
        if contenido:
            for col in range(1, (lam[0] if lam else 0) + 1):
                largo = sum(1 for i in range(kp) if mu[i] < col <= lam[i])
                if largo > d1:
                    col_ok = False
                    break
        predice_no_nulo = contenido and col_ok
        total += 1
        if (menor != 0) == predice_no_nulo:
            coincidencias += 1
        else:
            print("      discrepancia F=%s: menor%s, prediccion=%s"
                  % (Fdec, "!=0" if menor != 0 else "==0", predice_no_nulo))
    ok = (coincidencias == total)
    print("  (c) d1=%d d2=%d t=%d S=%-10s Gamma=%s : %d/%d subconjuntos F "
          "predichos por 'mu ⊆ lambda + columnas <= d1' -> %s"
          % (d1, d2, t, str(tuple(gammas)), str(Gamma), coincidencias, total,
             "OK" if ok else "FALLA"))
    return ok


# --------------------------------------------------------------------- driver

if __name__ == '__main__':
    import sys
    sec = sys.argv[1] if len(sys.argv) > 1 else 'todo'
    ok = True

    if sec in ('todo', 'a'):
        print("=== (a) validacion punta a punta contra el subresultante clasico ===")
        for (d1, d2, k) in [(2, 2, 1), (3, 2, 1), (3, 3, 1), (3, 3, 2),
                            (4, 3, 2), (2, 4, 1), (3, 4, 2), (4, 4, 2)]:
            for j in range(k + 1):
                ok &= test_punta_a_punta(d1, d2, k, j)

    if sec in ('todo', 'b'):
        print("\n=== (b) forma Hankel/Toeplitz (Pade) del coeficiente principal ===")
        signos = {}
        for d1 in range(1, 5):
            for d2 in range(1, 5):
                for k in range(0, min(d1, d2) + 1):
                    if d1 + d2 - k - 1 >= 0:
                        o, s = test_hankel(d1, d2, k)
                        ok &= o
                        signos[(d1, d2, k)] = s
        print("  signos observados:", sorted(set(signos.values())))

    if sec in ('todo', 'c'):
        print("\n=== (c) coeficientes del Teorema C como Schur sesgadas ===")
        for c in [(3, 3, 4, (1,)), (2, 3, 3, (2,)), (3, 3, 3, (0, 1)),
                  (4, 4, 5, (0, 2)), (2, 5, 3, (0, 1))]:
            ok &= test_skew(*c)

    print("\n%s" % ("======== TODO OK ========" if ok else "======== HAY FALLAS ========"))
