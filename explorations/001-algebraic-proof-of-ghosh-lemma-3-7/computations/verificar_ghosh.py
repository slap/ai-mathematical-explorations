# -*- coding: utf-8 -*-
"""
Verificacion computacional del Lema 3.7 de Ghosh (arXiv:2501.09272), que es el
unico punto donde su demostracion usa caracteristica 0 (grado de Brouwer).

Enunciado. Para cualquier eleccion de indices j_1,...,j_n en {1,...,n+1} y
cualquier l, existe f = X·prod(X - alpha_i) de grado n+1 sobre C con
    f^{(i)}(alpha_{j_i}) = 0  para todo i = l+1,...,n,   pero  f^{(l)}(alpha_{j_l}) != 0.

Por el Nullstellensatz eso equivale, en el espacio de raices, a
    F(l, j_l)  no pertenece a  sqrt( F(i, j_i) : i > l ),
con F(i,j) = Phi_j(e_{n+1-i}) como en el paper. Se testea con el truco de
Rabinowitsch: F(l,j_l) esta en el radical  <=>  1 pertenece a
(F(i,j_i) : i>l) + (1 - t·F(l,j_l)).

Ademas (Observacion 3.8(1) del paper) hay testigos explicitos cuando
|{j_{l+1},...,j_n}| <= l  (son nuestros binomiales X^{n+1} - X^l): se reporta
que fraccion de los casos queda cubierta por esa via elemental, es decir cuanto
del argumento topologico seria evitable.

Correr:  sage -python -u verificar_ghosh.py n
"""

import sys
from itertools import product
from sage.all import QQ, PolynomialRing


def main(n):
    R = PolynomialRing(QQ, ['x%d' % k for k in range(1, n + 1)] + ['t'],
                       order='degrevlex')
    x = R.gens()[:n]
    t = R.gens()[n]
    E = [R.one()]
    for v in x:
        prev = E + [R.zero()]
        E = [prev[k] + (v * prev[k - 1] if k > 0 else 0) for k in range(len(prev))]

    def Phi(j, p):
        if j == n + 1:
            return p
        return p.subs({x[l]: (x[l] - x[j - 1]) if l != j - 1 else -x[j - 1]
                       for l in range(n)})

    def F(i, j):
        return Phi(j, E[n + 1 - i])

    print("n = %d (grado d = %d): test del Lema 3.7 de Ghosh" % (n, n + 1))
    total = ok = cubierto_elemental = 0
    fallas = []
    for l in range(1, n + 1):
        for cola in product(range(1, n + 2), repeat=n - l):
            for jl in range(1, n + 2):
                total += 1
                gens = [F(i, cola[i - l - 1]) for i in range(l + 1, n + 1)]
                J = R.ideal(gens + [1 - t * F(l, jl)])
                en_radical = (J.groebner_basis() == [1])
                ok += (not en_radical)
                if en_radical:
                    fallas.append((l, jl, cola))
                if len(set(cola)) <= l:
                    cubierto_elemental += 1
    print("  casos (l, j_l, j_{l+1..n}): %d" % total)
    print("  F(l,j_l) NO esta en el radical de los posteriores: %d/%d" % (ok, total))
    print("  cubiertos por testigos explicitos (Obs. 3.8(1), |{j_{l+1..n}}| <= l): %d/%d (%.0f%%)"
          % (cubierto_elemental, total, 100.0 * cubierto_elemental / total))
    if fallas:
        print("  CASOS QUE FALLAN (contradirian el Lema 3.7):")
        for l, jl, cola in fallas[:20]:
            print("     l=%d  j_l=%d  cola=%s" % (l, jl, cola))
    else:
        print("  -> el Lema 3.7 se verifica en todos los casos de este grado")


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
