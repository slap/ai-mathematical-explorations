# -*- coding: utf-8 -*-
"""
Verificacion de la demostracion algebraica del Lema 3.7 de Ghosh.

Argumento (teoria de interseccion / teorema de la dimension proyectiva):
  F_i := F(i, j_i) = Phi_{j_i}(e_{n+1-i}), forma de grado n+1-i en K[x_1..x_n].
  (H) Casas-Alvero en grado n+1  <=>  V(F_1,...,F_n) = {0} en A^n
                                 <=>  V_+(F_1,...,F_n) = vacio en P^{n-1}.
  Si F_l estuviera en sqrt(F_{l+1},...,F_n):
    Z := V_+(F_{l+1},...,F_n) tiene dim >= (n-1)-(n-l) = l-1  (y es no vacio);
    Z ⊆ V_+(F_l), luego V_+(F_l,...,F_n) = Z tiene dim >= l-1;
    cortando con las l-1 formas restantes, dim V_+(F_1..F_n) >= 0, no vacio.
  Contradice (H).

Este script comprueba los ingredientes cuantitativos:
  (1) dim V(F_{l+1},...,F_n) en A^n  >= l        (o sea dim proyectiva >= l-1)
  (2) dim V(F_1,...,F_n) = 0 en A^n              (o sea V_+ vacio: hipotesis (H))
  (3) por lo tanto F_l no esta en el radical     (ya verificado aparte)

Correr:  sage -python -u interseccion_lema37.py n
"""

import sys
from itertools import product
from sage.all import QQ, PolynomialRing


def main(n):
    R = PolynomialRing(QQ, ['x%d' % k for k in range(1, n + 1)], order='degrevlex')
    x = R.gens()
    E = [R.one()]
    for v in x:
        prev = E + [R.zero()]
        E = [prev[k] + (v * prev[k - 1] if k > 0 else 0) for k in range(len(prev))]

    def F(i, j):
        p = E[n + 1 - i]
        if j == n + 1:
            return p
        return p.subs({x[l]: (x[l] - x[j - 1]) if l != j - 1 else -x[j - 1]
                       for l in range(n)})

    print("n = %d (grado d = %d)" % (n, n + 1))

    # (2) hipotesis (H): V(F_1..F_n) = {0} para toda rama
    malas = []
    for j in product(range(1, n + 2), repeat=n):
        I = R.ideal([F(i, j[i - 1]) for i in range(1, n + 1)])
        if I.dimension() != 0:
            malas.append(j)
    print("  (H) dim V(F_1..F_n) = 0 en las %d ramas: %s"
          % ((n + 1)**n, "si" if not malas else "NO en %s" % malas[:5]))

    # (1) cota de dimension para las colas
    print("  (1) dim V(F_{l+1}..F_n) >= l  (teorema de la dimension):")
    for l in range(1, n + 1):
        dims = set()
        for cola in product(range(1, n + 2), repeat=n - l):
            gens = [F(i, cola[i - l - 1]) for i in range(l + 1, n + 1)]
            I = R.ideal(gens) if gens else R.ideal([R.zero()])
            dims.add(I.dimension())
        ok = all(dd >= l for dd in dims)
        print("      l=%d : dimensiones observadas %s   cota >= %d : %s"
              % (l, sorted(dims), l, "OK" if ok else "FALLA"))


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
