# Original AI output

Everything below the line is reproduced as produced, unedited. The conversation was in
Spanish; the English translations of the prompts are marked as such and were added by me.
Nothing else was added, and nothing inside a quoted message was altered, shortened or
reordered.

**Session.** Claude Opus 5 (`claude-opus-5`), Anthropic, through Claude Code, 16 September
2026, in the working directory of my project on subresultants and the Casas–Alvero
conjecture. The English version of the note was produced by the same model in the same
session on 17 September 2026.

**What is not included.** The intervening turns in which the model ran SageMath checks and
looked up the references, the earlier part of the session on subresultant formulas, and the
later work on membership certificates. Tool calls (file writes, shell commands) are omitted;
the scripts they produced are in [`computations/`](computations/) and the Lean development in
[`lean/`](lean/). Local file paths have been removed with the tool calls.

The two LaTeX sources at the end are the files as the AI wrote them. The `source.tex`
published alongside this file differs from the English one only by the editorial changes
listed in its header.

---

**Prompt** — 2026-09-16 13:42

> pero me perdi de nuevo, hace falta este analisis de primos malos? yo lo quiero es una formula cerrada para probar que una resultante pertenece a un ideal, o encontrar un ejemplo de no pertenencia. pero todo sobre Q, no creo que haga falta ir a Zp

*(Translation: "but I got lost again, is this analysis of bad primes needed? what I want is a
closed formula to prove that a resultant belongs to an ideal, or to find an example of
non-membership. but all over Q, I don't think we need to go to Zp".)*

---

**Claude** — 2026-09-16 13:55

Tenés razón: los primos no hacen falta para lo que buscás. Me quedé en `ℚ`, en el planteo exacto de Schaub–Spivakovsky ([arXiv:2312.08742](https://arxiv.org/abs/2312.08742)): `f = x^d + a₁x^{d−1} + … + a_{d−1}x` y `R_i = Res(f, H_i(f))`, con `H_i` la derivada de Hasse. Ahí hay dos enunciados distintos:

- **La conjetura** es la pertenencia `a_k^N ∈ (R₁,…,R_{d−1})`.
- **Su resultado parcial** es una no pertenencia: `R_i ∉ √(R₁,…,Ř_i,…,R_{d−1})`, sólo para `i ∈ {d−3, d−2, d−1}`, con una prueba indirecta (casi contraejemplos de Draisma–de Jong más argumentos de raíces reales).

## Resultado: la no pertenencia vale para todo `i`

Para ver que `R_i` no está en el radical de los otros alcanza un solo polinomio donde se anulen todos los `R_j` con `j ≠ i` y no se anule `R_i`. Hay testigos explícitos para cada índice:

| índice | testigo |
|---|---|
| `1 ≤ i ≤ d−2` | `f = x^d + xⁱ = xⁱ(x^{d−i} + 1)` |
| `i = d−1` | `f = x^d − x^{d−1} = x^{d−1}(x − 1)` |

La prueba es de cinco líneas: se calcula `H_j(f)` en el testigo y se ve que comparte la raíz 0 con `f` salvo cuando `j = i`. En ese caso las raíces de `H_i` no son raíces de `f`, porque `C(d,i) > 1`. Hay incluso un valor cerrado en el testigo: `R_i(x^d + t·xⁱ) = ±(C(d,i) − 1)^{d−i}·t^d`.

Lo verifiqué por dos caminos independientes:
- **Evaluando en los testigos:** todos los `i`, para `d = 3…9`.
- **Con un test de radical por Gröbner:** para `d = 3, 4, 5`, que no usa los testigos.

Me sorprende que ellos lo tengan sólo para tres índices. Convendría releer su enunciado con cuidado, pero con su definición de `f` y de `R_i` no veo qué se me escapa.

## Lo que esto no da

No da Casas-Alvero. Estar fuera del radical de los otros sólo significa que `R_i` no se anula en *algún* punto de `V(los otros)`. La pertenencia `a_k^N ∈ (R₁,…,R_{d−1})` pide que no se anule en *ninguna* componente de dimensión positiva. Esa distancia entre "algún punto" y "toda componente" es la dificultad.

Para el lado de la pertenencia todavía no tengo una fórmula cerrada. Lo que falta es un certificado `a_k^N = Σ c_j R_j` con los `c_j` explícitos. El paso concreto que propongo, siempre sobre `ℚ`: calcular esos `c_j` en `d = 4` y `d = 5` en este mismo planteo, y ver si se expresan con los menores de Toeplitz de `F/F_i`.

Quedó todo en `notas/04-no-pertenencia-radical.md`.

---

**Prompt** — 2026-09-16 13:59

> ok, antes de empezar sobre Q, explicame que es lo que mejoraste sobre Schaub–Spivakovsky y que implicancias tiene

*(Translation: "ok, before starting over Q, explain to me what you improved on
Schaub–Spivakovsky and what its implications are".)*

---

**Claude** — 2026-09-16 14:00

Lo explico con cuidado, porque la mejora es real pero modesta, y conviene no inflarla.

## Qué prueban Schaub–Spivakovsky

Su Teorema 5 dice, textualmente: si `i ∈ {d−3, d−2, d−1}`, entonces `R_i ∉ √(R₁, …, Ř_i, …, R_{d−1})`.

**Por qué les interesa.** Casas-Alvero implica este enunciado para todo `i`. Si algún `R_i` estuviera en el radical de los otros, la condición `i` no agregaría nada: `V(todos) = V(los otros)`, la altura sería a lo sumo `d−2` y la conjetura fallaría. Así que es una consecuencia necesaria, y probarla sin suponer la conjetura es un resultado parcial "en su dirección".

**Por qué se quedan en tres índices.** Negar la pertenencia equivale a exhibir un `f` donde valen todas las condiciones `j ≠ i` y la `i` falla, es decir `R_i(f) ≠ 0`.
- Draisma–de Jong ya dan, para cada `i`, polinomios reales que cumplen todas las condiciones `j ≠ i` y no son potencia de un lineal.
- Pero "no es potencia de un lineal" no implica `R_i(f) ≠ 0` a menos que ya sepas la conjetura.
- Para descartar que ese `f` sea un contraejemplo real usan argumentos de ubicación de raíces (Rolle) más que un contraejemplo tiene al menos cinco raíces distintas. Esos argumentos sólo cierran para los tres índices de arriba.

## Qué mejoré

Encontré testigos donde `R_i(f) ≠ 0` se **calcula directamente**, así que no hace falta saber nada de la conjetura:

| índice | testigo |
|---|---|
| `1 ≤ i ≤ d−2` | `f = xⁱ(x^{d−i} + 1)` |
| `i = d−1` | `f = x^{d−1}(x − 1)` |

La idea que evita su dificultad es usar testigos **degenerados**. La raíz `0`, con multiplicidad `i`, es compartida por todas las derivadas salvo la `i`-ésima. Ellos trabajan con polinomios de raíces reales bien distribuidas, donde verificar `R_i ≠ 0` es difícil. Acá es inmediato:

- en `x^d + t·xⁱ`, todo `R_j` con `j ≠ i` es `0`;
- y `R_i = ±(C(d,i) − 1)^{d−i}·t^d`.

Así que la mejora es:
1. **Todos los índices** `i ∈ {1,…,d−1}`, no sólo tres.
2. **Prueba elemental** de cinco líneas, sin Draisma–de Jong, Rolle ni la cota de cinco raíces.
3. **Testigos explícitos** con el valor de `R_i` en forma cerrada.

## Implicancias, de mayor a menor peso

**1. Ninguna de las `d−1` condiciones es redundante.** Para cada `i`, las otras `d−2` no implican la `i`-ésima, ni siquiera a nivel de radicales. Es un enunciado limpio e incondicional.

**2. La brecha con Casas-Alvero queda bien localizada.** `V(J_i)`, con `J_i = (R_j : j ≠ i)`, son `d−2` ecuaciones en `d−1` variables, así que todas sus componentes tienen dimensión al menos 1.
- La recta `t ↦ x^d + t·xⁱ` está dentro de `V(J_i)`, y sobre ella `R_i` sólo se anula en el origen.
- Casas-Alvero equivale a que eso pase en **toda** componente de `V(J_i)`: si la conjetura vale, `V(J_i)` es unión de curvas por el origen y `R_i` no se anula idénticamente en ninguna.
- Lo que probamos es que pasa en **una** componente. La diferencia entre "una" y "todas" es toda la dificultad.

**3. Consecuencia concreta para el programa sobre `ℚ`.** Supongamos un certificado `a_k^N = Σ_j c_j·R_j` y restringámoslo a la recta binomial del índice `i`. Ahí todos los `R_j` con `j ≠ i` se anulan, así que sobrevive un solo término:
- Si `k = d−i`, queda `c_i|recta · (±(C(d,i)−1)^{d−i} t^d) = t^N`. El certificado de `a_{d−i}^N` **tiene que usar** `R_i`, y su coeficiente sobre esa recta queda determinado: `c_i = ±t^{N−d}/(C(d,i)−1)^{d−i}`.
- Si `k ≠ d−i`, entonces `c_i` tiene que anularse sobre la recta.

Son restricciones explícitas sobre cualquier certificado, y sirven de punto de partida para buscarlos en `d = 4, 5`.

**4. Relación con Ghosh.** Si su demostración ([arXiv:2501.09272](https://arxiv.org/abs/2501.09272)) es correcta, implica este resultado. Nuestro aporte sería entonces una prueba elemental, independiente de la suya. Si tuviera un error, esto queda como un resultado parcial incondicional, un poco más fuerte que el de Schaub–Spivakovsky.

## Cautelas

- Verifiqué su enunciado en el PDF (versión 7, febrero 2025) y mi argumento en su planteo exacto: evaluando en los testigos hasta `d=9`, y con un test de radical por Gröbner hasta `d=5`, que no usa los testigos. Todo coincide.
- Me extraña que no lo hayan notado, así que no descartaría que esté observado en otro lado, o que su énfasis estuviera en el método (raíces reales) más que en el enunciado.
- No es un resultado profundo. Es un buen lema, y la implicancia 3 es la que realmente sirve para seguir.

---

**Prompt** — 2026-09-16 15:07

> oka, escribime todo esto en un pdf y despues seguimos con el problema sobre Q

*(Translation: "ok, write all this up in a pdf and then we continue with the problem over Q".)*

---

**Claude** — 2026-09-16 15:11

Listo: `paper/nota-casas-alvero.pdf`, 4 páginas en castellano, que compila limpio.

**Qué contiene:**
1. **Planteo** en la notación exacta de Schaub–Spivakovsky, con la conjetura escrita como pertenencia `a_k^N ∈ (R₁,…,R_{d−1})` sobre `ℚ`.
2. **Su Teorema 5**, por qué es un resultado parcial y por qué su prueba sólo cierra para `i ∈ {d−3, d−2, d−1}`.
3. **Proposición:** sobre las rectas `x^d + t·xⁱ` y `x^d − t·x^{d−1}` se anulan todos los `R_j` con `j ≠ i`, y `R_i = ±(C(d,i) − 1)^{d−i}·t^d`. De ahí sale el **teorema para todo `i`**, con una prueba que sólo evalúa en un punto: no usa el Nullstellensatz, raíces reales ni la conjetura.
4. **Consecuencias:**
   - ninguna de las `d−1` condiciones es redundante;
   - un lema que localiza la dificultad: la conjetura equivale a que `R_i` no se anule idénticamente en *ninguna* componente de `V(R_j : j≠i)`, y el lema da *una*;
   - un corolario que restringe cualquier certificado `a_k^N = Σ c_j R_j`: tiene que ser `N ≥ d`, el coeficiente `c_{d−k}` sobre su recta vale exactamente `±t^{N−d}/(C(d,k)−1)^k`, y los demás `c_i` se anulan sobre la suya;
   - la relación con la prueba de Ghosh.
5. **Verificación:** 284 resultantes sobre las rectas, evaluación en los testigos hasta `d=9`, y el test de radical por Gröbner para `d = 3, 4, 5`.
6. **Cautelas:** es un lema, no un resultado profundo, y puede que el caso general ya esté observado en otro lado.

La fórmula unificada, que incluye el caso `i = d−1`, la verifiqué recién para `d ≤ 10` antes de ponerla en el PDF. El lema de componentes está demostrado en el texto, pero no tiene verificación computacional aparte. Faltan los autores (`\author{}` vacío).

Para seguir sobre `ℚ`, el corolario de certificados da el punto de partida: fija cómo tiene que ser cada `c_j` sobre `d−1` rectas explícitas. Propongo calcular los certificados de `d=4` y `d=5` en este planteo sin normalizar y buscar una forma cerrada para los `c_j` que respete esas condiciones.

---

**Prompt** — 2026-09-17 17:56

> bien, sigamos, primero pasa todo a ingles, que voy a querer publicarlo en un repo publico. y hagamos ahora el caso general

*(Translation: "good, let's go on, first put everything into English, since I want to publish
it in a public repository. and now let's do the general case".)*

*[The model translated the project, this note among the rest, and wrote
`note-casas-alvero.tex` at 18:18 on 2026-09-17. Earlier the same day, before this prompt, it
had formalised the witnesses in Lean 4 — the development in [`lean/`](lean/) — and added the
remark and the table row about it to the note.]*

---

## The note, as first generated (Spanish, 2026-09-16)

`nota-casas-alvero.tex`, written 2026-09-16 15:10 and left in this state by the model after
two corrections of its own, minutes later, in the same session.

```latex
\documentclass[11pt,reqno]{amsart}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{array,booktabs}
\usepackage[margin=1.1in]{geometry}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}

\theoremstyle{plain}
\newtheorem{teorema}{Teorema}[section]
\newtheorem{proposicion}[teorema]{Proposición}
\newtheorem{lema}[teorema]{Lema}
\newtheorem{corolario}[teorema]{Corolario}
\newtheorem{conjetura}[teorema]{Conjetura}
\theoremstyle{definition}
\newtheorem{definicion}[teorema]{Definición}
\newtheorem{observacion}[teorema]{Observación}

\renewcommand{\proofname}{Demostración}
\renewcommand{\refname}{Referencias}
\renewcommand{\abstractname}{Resumen}
\renewcommand{\datename}{\textit{Fecha}:}

\DeclareMathOperator{\Res}{Res}
\newcommand{\KK}{\overline{K}}
\newcommand{\ba}{\mathbf a}

% TODO: autores
\title[No redundancia de las condiciones de Casas--Alvero]
      {No redundancia de las condiciones de Casas--Alvero:\\ un lema elemental y sus consecuencias}
\author{}
\date{16 de septiembre de 2026}

\begin{document}

\begin{abstract}
Sea $f=x^d+a_1x^{d-1}+\dots+a_{d-1}x$ genérico y $R_i=\Res(f,H_i(f))$ la
resultante de $f$ con su $i$-ésima derivada de Hasse. Schaub y Spivakovsky
probaron que $R_i\notin\sqrt{(R_j:j\neq i)}$ para $i\in\{d-3,d-2,d-1\}$. Mostramos
que esto vale para \emph{todo} $i\in\{1,\dots,d-1\}$, con una demostración
elemental basada en testigos explícitos: sobre las rectas
$t\mapsto x^d+t\,x^i$ (y $t\mapsto x^d-t\,x^{d-1}$) todas las resultantes
$R_j$ con $j\neq i$ se anulan y
$R_i=\pm\big(\binom{d}{i}-1\big)^{d-i}t^d$. Discutimos además las consecuencias:
ninguna de las $d-1$ condiciones de Casas--Alvero es redundante; la conjetura
equivale a que $R_i$ no se anule idénticamente sobre \emph{ninguna} componente
de $V(R_j:j\neq i)$, y nuestro lema lo establece para \emph{una}; y todo
certificado de pertenencia $a_k^N\in(R_1,\dots,R_{d-1})$ queda fuertemente
restringido sobre esas rectas.
\end{abstract}

\maketitle

\section{Planteo}

Seguimos la notación de Schaub--Spivakovsky \cite{SS}. Sea $K$ un cuerpo de
característica $0$, $d\ge3$, y
\[
  f=x^d+a_1x^{d-1}+\dots+a_{d-1}x\ \in\ K[a_1,\dots,a_{d-1}][x],
\]
es decir, con $a_0=1$ y $a_d=0$ (siempre puede suponerse, trasladando, que $0$ es
raíz de $f$). Para $1\le i\le d-1$ sea
\[
  H_i(f)=\sum_{k=0}^{d-i}\binom{d-k}{i}a_k\,x^{d-k-i}
\]
la $i$-ésima derivada de Hasse, $H_i(f)=f^{(i)}/i!$, y
\[
  R_i:=\Res\big(f,H_i(f)\big)\in K[a_1,\dots,a_{d-1}],\qquad
  J:=(R_1,\dots,R_{d-1}),\qquad J_i:=(R_j:\ j\neq i).
\]
Un polinomio $f$ tiene un factor común no constante con $H_i(f)$ si y sólo si
$R_i(f)=0$.

\begin{conjetura}[Casas--Alvero]\label{conj:CA}
Si $f$ tiene un factor común no constante con cada $H_i(f)$, $1\le i\le d-1$,
entonces $f=x^d$. Equivalentemente, $V(J)=\{0\}$; equivalentemente,
$a_k^N\in J$ para todo $k$ y algún $N$.
\end{conjetura}

Como los $R_j$ tienen coeficientes enteros, la validez de la última
formulación no depende de $K$ (en característica $0$), y por eso todo lo que
sigue es sobre $\mathbb{Q}$. Schaub y Spivakovsky observan además
\cite[Obs.~4]{SS} que la conjetura equivale a que $R_1,\dots,R_{d-1}$ sea una
sucesión regular en $K[a_1,\dots,a_{d-1}]$, en cualquier orden.

\subsection*{Cuasi-homogeneidad}
Con los pesos $\deg a_k=k$, cada $R_j$ es cuasi-homogéneo: la sustitución
$a_k\mapsto\lambda^ka_k$ corresponde a $f(x)\mapsto\lambda^df(x/\lambda)$, que
reescala las raíces de $f$ y de $H_j(f)$ por $\lambda$. En consecuencia
$V(J)$ y $V(J_i)$ son conos estables bajo la acción de $\KK^{\,*}$.

\section{El resultado de Schaub--Spivakovsky}

\begin{teorema}[{\cite[Teorema~5]{SS}}]\label{thm:SS}
Si $i\in\{d-3,d-2,d-1\}$, entonces $R_i\notin\sqrt{(R_1,\dots,\check R_i,\dots,R_{d-1})}$.
\end{teorema}

Es un resultado parcial ``en la dirección'' de la conjetura: si ésta vale,
entonces $R_i\notin\sqrt{J_i}$ para \emph{todo} $i$, porque si $R_i$ estuviera en
el radical de los otros se tendría $V(J_i)=V(J)$, y la altura de $J$ sería a lo
sumo $d-2$.

La demostración de \cite{SS} es indirecta. Negar $R_i\in\sqrt{J_i}$ equivale a
exhibir $f$ con $R_j(f)=0$ para $j\neq i$ y $R_i(f)\neq0$. Draisma y de Jong
\cite{DdJ} construyen, para cada $i$, polinomios reales que cumplen todas las
condiciones $j\neq i$ y no son potencia de un lineal (\emph{casi contraejemplos
de nivel $i$}). Pero ``no ser potencia de un lineal'' no implica $R_i(f)\neq0$ sin
conocer ya la conjetura. Para descartar que esos polinomios sean contraejemplos
genuinos, \cite{SS} combina argumentos de localización de raíces reales (Rolle)
con el hecho de que un contraejemplo tiene al menos cinco raíces distintas
\cite{CLO}; esos argumentos sólo cierran para los tres índices más altos.

\section{El lema: todos los índices}

La idea es usar testigos \emph{degenerados}: una raíz $0$ de multiplicidad $i$
es compartida por todas las derivadas salvo la $i$-ésima, y verificar
$R_i\neq0$ se vuelve un cálculo directo.

\begin{proposicion}[valores sobre las rectas testigo]\label{prop:rectas}
Para $t\in K$ sean
\[
  f_{i,t}:=x^d+t\,x^i=x^i\big(x^{d-i}+t\big)\quad(1\le i\le d-2),\qquad
  f_{d-1,t}:=x^d-t\,x^{d-1}=x^{d-1}(x-t).
\]
Entonces, para todo $i\in\{1,\dots,d-1\}$,
\[
  R_j(f_{i,t})=0\ \ (j\neq i),\qquad
  R_i(f_{i,t})=\pm\Big(\binom{d}{i}-1\Big)^{d-i}t^{d}.
\]
\end{proposicion}

\begin{proof}
Usamos la fórmula de Poisson
$\Res(f,g)=\pm\,\mathrm{lc}(g)^{\deg f}\prod_{g(\eta)=0}f(\eta)$.

\emph{Caso $1\le i\le d-2$.} Aquí
$H_j(f_{i,t})=\binom dj x^{d-j}+t\binom ij x^{i-j}$.
\begin{itemize}
\item Si $j<i$, ambos sumandos se anulan en $0$, y $f_{i,t}(0)=0$; luego $R_j=0$.
\item Si $j>i$, $\binom ij=0$ y $H_j=\binom dj x^{d-j}$ con $d-j\ge1$; comparte la
  raíz $0$, luego $R_j=0$.
\item Si $j=i$, sea $C=\binom di$ y $m=d-i$. Entonces $H_i=Cx^m+t$, cuyas raíces
  $\eta_1,\dots,\eta_m$ cumplen $\eta^m=-t/C$ y $\prod\eta_\ell=\pm t/C$. En ellas
  \[
    f_{i,t}(\eta)=\eta^i(\eta^m+t)=\eta^i\,t\Big(1-\frac1C\Big),
  \]
  así que
  \[
    R_i=\pm\,C^{d}\Big(\prod_\ell\eta_\ell\Big)^{i}t^m\Big(\frac{C-1}{C}\Big)^m
       =\pm\,C^{i+m}\,\frac{t^i}{C^i}\,t^m\,\frac{(C-1)^m}{C^m}
       =\pm\,(C-1)^{d-i}\,t^d .
  \]
\end{itemize}

\emph{Caso $i=d-1$.} Aquí
$H_j(f_{d-1,t})=\binom dj x^{d-j}-t\binom{d-1}{j}x^{d-1-j}$. Si $j\le d-2$,
ambos exponentes son $\ge1$, así que $H_j$ comparte con $f$ la raíz $0$ y
$R_j=0$. Si $j=d-1$, $H_{d-1}=dx-t$ tiene raíz $t/d$ y
$f_{d-1,t}(t/d)=(t/d)^{d-1}(t/d-t)=-(d-1)t^d/d^d$, de donde
$R_{d-1}=\pm d^d\cdot(d-1)t^d/d^d=\pm(d-1)t^d$, que es la fórmula con
$\binom{d}{d-1}-1=d-1$.
\end{proof}

\begin{teorema}\label{thm:todos}
Para todo $d\ge3$ y todo $i\in\{1,\dots,d-1\}$,
\[
  R_i\notin\sqrt{(R_1,\dots,\check R_i,\dots,R_{d-1})}\quad\text{en }K[a_1,\dots,a_{d-1}].
\]
\end{teorema}

\begin{proof}
Supongamos $R_i^N=\sum_{j\neq i}c_jR_j$ con $c_j\in K[a]$. Evaluando en el punto
$K$-racional correspondiente a $f_{i,1}$, la Proposición~\ref{prop:rectas} da
$0\neq\big(\pm(\binom di-1)^{d-i}\big)^N=0$, pues
$\binom di\ge d\ge3$ para $1\le i\le d-1$. Contradicción.
\end{proof}

\begin{observacion}
La prueba no usa el Nullstellensatz: sólo la dirección trivial ``si $R_i$ está
en el radical, se anula en cada cero de $J_i$''. Tampoco usa raíces reales ni la
conjetura. En coordenadas, el testigo de índice $i\le d-2$ es el punto con
$a_{d-i}=1$ y las demás coordenadas nulas; el de índice $d-1$ es $a_1=-1$.
En ambos casos la coordenada que se mueve es $a_{d-i}$.
\end{observacion}

\section{Consecuencias}

\subsection{Ninguna condición es redundante}

\begin{corolario}\label{cor:noredundante}
Para cada $i$, las $d-2$ condiciones ``$f$ comparte raíz con $H_j(f)$, $j\neq i$''
no implican la $i$-ésima, ni siquiera a nivel de radicales. Más precisamente, la
recta $L_i:=\{f_{i,t}:t\in K\}$ está contenida en $V(J_i)$ y
$L_i\cap V(R_i)=\{0\}$.
\end{corolario}

Nótese la diferencia con los casi contraejemplos de \cite{DdJ}: los polinomios
$f_{i,1}$ no sólo satisfacen las condiciones $j\neq i$, sino que
\emph{violan verificablemente} la $i$-ésima.

\subsection{Dónde está la dificultad: una componente contra todas}

\begin{lema}\label{lem:componentes}
Fijemos $i$. La Conjetura~\ref{conj:CA} vale en grado $d$ si y sólo si toda
componente irreducible $C$ de $V_{\KK}(J_i)$ cumple $\dim C=1$ y
$R_i|_C\not\equiv0$.
\end{lema}

\begin{proof}
($\Leftarrow$) Cada componente $C$ es estable por la acción de $\KK^{\,*}$ (el
grupo es conexo) y contiene a $0$ (límite $\lambda\to0$). Si $\dim C=1$ y
$p\in C\smallsetminus\{0\}$, la órbita de $p$ es infinita (los pesos son
positivos), así que su clausura es un cerrado irreducible de dimensión $1$
contenido en $C$, es decir, es $C$. Como $R_i$ es cuasi-homogéneo,
$R_i(\lambda\cdot p)=\lambda^wR_i(p)$; si $R_i(p)=0$ para algún $p\neq0$ de $C$,
entonces $R_i$ se anula en toda la órbita, luego en $C$, contra la hipótesis. Por
lo tanto $C\cap V(R_i)=\{0\}$ para toda componente, y
$V(J)=V(J_i)\cap V(R_i)=\{0\}$.

($\Rightarrow$) Si $V(J)=\{0\}$: por el teorema del ideal principal de Krull,
toda componente de $V(J_i)$ (definido por $d-2$ ecuaciones en $d-1$ variables)
tiene dimensión $\ge1$. Si alguna $C$ tuviera dimensión $\ge2$, entonces
$C\cap V(R_i)$ sería no vacío (contiene a $0$) de dimensión $\ge1$, contenido en
$V(J)$, absurdo. Y si $R_i\equiv0$ sobre alguna $C$, entonces $C\subseteq V(J)$,
también absurdo.
\end{proof}

El Teorema~\ref{thm:todos} dice que la componente de $V(J_i)$ que contiene a
$L_i$ satisface $R_i|_C\not\equiv0$. La conjetura pide lo mismo para \emph{todas}
las componentes (y que todas sean curvas). En particular, si la conjetura vale,
$L_i$ es una componente irreducible de $V(J_i)$. La distancia entre ``una
componente'' y ``todas'' es exactamente la dificultad de Casas--Alvero.

\subsection{Restricciones sobre certificados de pertenencia}

La formulación de la conjetura como pertenencia pide, para cada $k$, un
certificado
\begin{equation}\label{eq:cert}
  a_k^N=\sum_{j=1}^{d-1}c_j\,R_j,\qquad c_j\in\mathbb{Q}[a_1,\dots,a_{d-1}].
\end{equation}
Sea $\varphi_i:\mathbb{Q}[a]\to\mathbb{Q}[t]$ la restricción a la recta $L_i$,
es decir, $a_{d-i}\mapsto t$ (o $a_1\mapsto-t$ si $i=d-1$) y las demás
coordenadas $\mapsto0$. Cada coordenada $a_k$ se mueve sobre exactamente una de
las rectas, la de índice $i=d-k$.

\begin{corolario}\label{cor:certificados}
Todo certificado \eqref{eq:cert} cumple:
\begin{enumerate}
\item $N\ge d$;
\item $\varphi_{d-k}(c_{d-k})=\pm\,t^{N-d}\big/\big(\binom dk-1\big)^{k}$; en
  particular, el certificado de $a_k^N$ \emph{tiene que usar} $R_{d-k}$;
\item $\varphi_i(c_i)=0$ para todo $i\neq d-k$.
\end{enumerate}
\end{corolario}

\begin{proof}
Aplicamos $\varphi_i$ a \eqref{eq:cert}. Por la Proposición~\ref{prop:rectas}
sobrevive sólo el término $j=i$:
$\varphi_i(a_k)^N=\varphi_i(c_i)\cdot\big(\pm(\binom di-1)^{d-i}t^d\big)$.
Si $i=d-k$, el lado izquierdo es $\pm t^N$, lo que fuerza $N\ge d$ y el valor
de $\varphi_{d-k}(c_{d-k})$, usando $\binom d{d-k}=\binom dk$. Si $i\neq d-k$, el
lado izquierdo es $0$ y, como $(\binom di-1)^{d-i}t^d\neq0$ en $\mathbb{Q}[t]$,
$\varphi_i(c_i)=0$.
\end{proof}

Estas condiciones son el punto de partida natural para buscar certificados
explícitos sobre $\mathbb{Q}$: fijan el comportamiento de cada coeficiente $c_j$
sobre $d-1$ rectas explícitas.

\subsection{Relación con la demostración de Ghosh}

Ghosh \cite{Gh25} anunció una demostración completa de la conjetura (homología
de Koszul más argumentos de grado de Brouwer), revisada en marzo de 2026 y, hasta
donde vimos, no publicada en revista; un preprint de agosto de 2026 todavía la
trata como abierta. Si la demostración de Ghosh es correcta, implica el
Teorema~\ref{thm:todos}, y lo que aporta esta nota es una prueba elemental e
independiente. Si tuviera un error, el Teorema~\ref{thm:todos} queda como un
resultado parcial incondicional que extiende el Teorema~\ref{thm:SS}.

\section{Verificación computacional}

Todo fue verificado con SageMath 10.7 en el planteo exacto de \cite{SS}
(derivadas de Hasse, $f$ sin normalizar salvo $a_d=0$).

\begin{center}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{>{\raggedright\arraybackslash}p{0.34\textwidth}%
                >{\raggedright\arraybackslash}p{0.56\textwidth}}
\toprule
Enunciado & Verificación\\
\midrule
Prop.~\ref{prop:rectas}
  & las $284$ resultantes $R_j(f_{i,t})$, $3\le d\le10$, todos los $i,j$,
    con $t$ simbólico: sin fallas.\\
Teorema~\ref{thm:todos}, por evaluación
  & $3\le d\le9$, todos los $i$.\\
Teorema~\ref{thm:todos}, por Gröbner
  & test de radical independiente de los testigos (truco de Rabinowitsch,
    $1\in J_i+(1-yR_i)$): $d=3,4,5$, todos los $i$, resultado
    ``no pertenece''.\\
\bottomrule
\end{tabular}
\end{center}

\section{Cautelas}

\begin{itemize}
\item Verificamos el enunciado del Teorema~\ref{thm:SS} en la versión~7 de
  \cite{SS} (febrero de 2025). Llama la atención que el caso general no esté
  observado ahí; no descartamos que figure en otro lado, o que el interés de
  \cite{SS} estuviera en el método de raíces reales más que en el enunciado.
\item No es un resultado profundo: es un lema. Su utilidad principal es el
  Corolario~\ref{cor:certificados}, que restringe los certificados de pertenencia
  sobre $\mathbb{Q}$, y el Lema~\ref{lem:componentes}, que localiza con precisión
  la dificultad.
\end{itemize}

\begin{thebibliography}{9}

\bibitem{CA} E.~Casas--Alvero, \emph{Higher order polar germs},
  J.~Algebra \textbf{240} (2001), 326--337.

\bibitem{CLO} W.~Castryck, R.~Laterveer, M.~Ounaïes,
  \emph{Constraints on counterexamples to the Casas--Alvero conjecture and a
  verification in degree 12}, arXiv:1208.5404.

\bibitem{DdJ} J.~Draisma, J.~P.~de Jong, \emph{On the Casas--Alvero conjecture},
  Newsletter of the EMS \textbf{80} (2011), 29--33.

\bibitem{Gh24} S.~Ghosh, \emph{A finiteness result towards the Casas--Alvero
  conjecture}, arXiv:2402.18717.

\bibitem{Gh25} S.~Ghosh, \emph{Proof of the Casas--Alvero conjecture},
  arXiv:2501.09272 (v2, marzo de 2026).

\bibitem{GLSV} H.-C.~Graf von Bothmer, O.~Labs, J.~Schicho,
  C.~van de Woestijne, \emph{The Casas--Alvero conjecture for infinitely many
  degrees}, J.~Algebra \textbf{316} (2007), 224--230.

\bibitem{SS} D.~Schaub, M.~Spivakovsky, \emph{A note on the Casas--Alvero
  conjecture}, arXiv:2312.08742 (v7, febrero de 2025).

\end{thebibliography}

\end{document}
```

## The note in English (2026-09-17)

`note-casas-alvero.tex`, written 2026-09-17 18:18, reproduced byte for byte. This is the
version published here as `exploration.pdf`.

```latex
\documentclass[11pt,reqno]{amsart}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{array,booktabs}
\usepackage[margin=1.1in]{geometry}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{conjecture}[theorem]{Conjecture}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{remark}[theorem]{Remark}

\DeclareMathOperator{\Res}{Res}
\newcommand{\KK}{\overline{K}}

% TODO: authors
\title[Non-redundancy of the Casas--Alvero conditions]
      {Non-redundancy of the Casas--Alvero conditions:\\
       an elementary lemma and its consequences}
\author{}
\date{September 17, 2026}

\begin{document}

\begin{abstract}
Let $f=x^d+a_1x^{d-1}+\dots+a_{d-1}x$ be generic and let
$R_i=\Res(f,H_i(f))$ be the resultant of $f$ with its $i$-th Hasse derivative.
Schaub and Spivakovsky proved that $R_i\notin\sqrt{(R_j:j\neq i)}$ for
$i\in\{d-3,d-2,d-1\}$. We show that this holds for \emph{every}
$i\in\{1,\dots,d-1\}$, with an elementary proof based on explicit witnesses: on
the lines $t\mapsto x^d+t\,x^i$ (and $t\mapsto x^d-t\,x^{d-1}$) all the
resultants $R_j$ with $j\neq i$ vanish and
$R_i=\pm\big(\binom{d}{i}-1\big)^{d-i}t^d$. We also discuss the consequences:
none of the $d-1$ Casas--Alvero conditions is redundant; the conjecture is
equivalent to $R_i$ not vanishing identically on \emph{any} component of
$V(R_j:j\neq i)$, and our lemma establishes this for \emph{one}; and every
membership certificate $a_k^N\in(R_1,\dots,R_{d-1})$ is strongly constrained
along those lines.
\end{abstract}

\maketitle

\section{Setting}

We follow the notation of Schaub--Spivakovsky \cite{SS}. Let $K$ be a field of
characteristic $0$, let $d\ge3$, and let
\[
  f=x^d+a_1x^{d-1}+\dots+a_{d-1}x\ \in\ K[a_1,\dots,a_{d-1}][x],
\]
that is, with $a_0=1$ and $a_d=0$ (after a translation one may always assume that
$0$ is a root of $f$). For $1\le i\le d-1$ let
\[
  H_i(f)=\sum_{k=0}^{d-i}\binom{d-k}{i}a_k\,x^{d-k-i}
\]
be the $i$-th Hasse derivative, $H_i(f)=f^{(i)}/i!$, and set
\[
  R_i:=\Res\big(f,H_i(f)\big)\in K[a_1,\dots,a_{d-1}],\qquad
  J:=(R_1,\dots,R_{d-1}),\qquad J_i:=(R_j:\ j\neq i).
\]
A polynomial $f$ has a non-constant common factor with $H_i(f)$ if and only if
$R_i(f)=0$.

\begin{conjecture}[Casas--Alvero]\label{conj:CA}
If $f$ has a non-constant common factor with every $H_i(f)$, $1\le i\le d-1$,
then $f=x^d$. Equivalently, $V(J)=\{0\}$; equivalently, $a_k^N\in J$ for every
$k$ and some $N$.
\end{conjecture}

Since the $R_j$ have integer coefficients, the validity of the last formulation
does not depend on $K$ (in characteristic $0$), and for that reason everything
below is over $\mathbb{Q}$. Schaub and Spivakovsky also observe
\cite[Rmk.~4]{SS} that the conjecture is equivalent to $R_1,\dots,R_{d-1}$ being
a regular sequence in $K[a_1,\dots,a_{d-1}]$, in any order.

\subsection*{Quasi-homogeneity}
With the weights $\deg a_k=k$, each $R_j$ is quasi-homogeneous: the substitution
$a_k\mapsto\lambda^ka_k$ corresponds to $f(x)\mapsto\lambda^df(x/\lambda)$, which
rescales the roots of $f$ and of $H_j(f)$ by $\lambda$. Consequently $V(J)$ and
$V(J_i)$ are cones, stable under the action of $\KK^{\,*}$.

\section{The result of Schaub--Spivakovsky}

\begin{theorem}[{\cite[Theorem~5]{SS}}]\label{thm:SS}
If $i\in\{d-3,d-2,d-1\}$ then
$R_i\notin\sqrt{(R_1,\dots,\check R_i,\dots,R_{d-1})}$.
\end{theorem}

This is a partial result ``in the direction'' of the conjecture: if the
conjecture holds then $R_i\notin\sqrt{J_i}$ for \emph{every} $i$, because if
$R_i$ were in the radical of the others we would have $V(J_i)=V(J)$, and the
height of $J$ would be at most $d-2$.

The proof in \cite{SS} is indirect. Denying $R_i\in\sqrt{J_i}$ amounts to
exhibiting $f$ with $R_j(f)=0$ for $j\neq i$ and $R_i(f)\neq0$. Draisma and de
Jong \cite{DdJ} construct, for each $i$, real polynomials satisfying all the
conditions $j\neq i$ which are not powers of a linear polynomial (\emph{almost
counterexamples of level $i$}). But ``not being a power of a linear polynomial''
does not imply $R_i(f)\neq0$ without already knowing the conjecture. To rule out
those polynomials being genuine counterexamples, \cite{SS} combines arguments on
the location of real roots (Rolle) with the fact that a counterexample has at
least five distinct roots \cite{CLO}; those arguments only close for the three
highest indices.

\section{The lemma: all indices}

The idea is to use \emph{degenerate} witnesses: a root $0$ of multiplicity $i$ is
shared by all the derivatives except the $i$-th, and checking $R_i\neq0$ becomes
a direct computation.

\begin{proposition}[values on the witness lines]\label{prop:lines}
For $t\in K$ let
\[
  f_{i,t}:=x^d+t\,x^i=x^i\big(x^{d-i}+t\big)\quad(1\le i\le d-2),\qquad
  f_{d-1,t}:=x^d-t\,x^{d-1}=x^{d-1}(x-t).
\]
Then, for every $i\in\{1,\dots,d-1\}$,
\[
  R_j(f_{i,t})=0\ \ (j\neq i),\qquad
  R_i(f_{i,t})=\pm\Big(\binom{d}{i}-1\Big)^{d-i}t^{d}.
\]
\end{proposition}

\begin{proof}
We use Poisson's formula
$\Res(f,g)=\pm\,\mathrm{lc}(g)^{\deg f}\prod_{g(\eta)=0}f(\eta)$.

\emph{Case $1\le i\le d-2$.} Here
$H_j(f_{i,t})=\binom dj x^{d-j}+t\binom ij x^{i-j}$.
\begin{itemize}
\item If $j<i$, both summands vanish at $0$, and $f_{i,t}(0)=0$; hence $R_j=0$.
\item If $j>i$, then $\binom ij=0$ and $H_j=\binom dj x^{d-j}$ with $d-j\ge1$; it
  shares the root $0$, hence $R_j=0$.
\item If $j=i$, set $C=\binom di$ and $m=d-i$. Then $H_i=Cx^m+t$, whose roots
  $\eta_1,\dots,\eta_m$ satisfy $\eta^m=-t/C$ and $\prod\eta_\ell=\pm t/C$. At
  those roots
  \[
    f_{i,t}(\eta)=\eta^i(\eta^m+t)=\eta^i\,t\Big(1-\frac1C\Big),
  \]
  so that
  \[
    R_i=\pm\,C^{d}\Big(\prod_\ell\eta_\ell\Big)^{i}t^m\Big(\frac{C-1}{C}\Big)^m
       =\pm\,C^{i+m}\,\frac{t^i}{C^i}\,t^m\,\frac{(C-1)^m}{C^m}
       =\pm\,(C-1)^{d-i}\,t^d .
  \]
\end{itemize}

\emph{Case $i=d-1$.} Here
$H_j(f_{d-1,t})=\binom dj x^{d-j}-t\binom{d-1}{j}x^{d-1-j}$. If $j\le d-2$ both
exponents are $\ge1$, so $H_j$ shares the root $0$ with $f$ and $R_j=0$. If
$j=d-1$, then $H_{d-1}=dx-t$ has root $t/d$ and
$f_{d-1,t}(t/d)=(t/d)^{d-1}(t/d-t)=-(d-1)t^d/d^d$, whence
$R_{d-1}=\pm d^d\cdot(d-1)t^d/d^d=\pm(d-1)t^d$, which is the formula with
$\binom{d}{d-1}-1=d-1$.
\end{proof}

\begin{theorem}\label{thm:all}
For every $d\ge3$ and every $i\in\{1,\dots,d-1\}$,
\[
  R_i\notin\sqrt{(R_1,\dots,\check R_i,\dots,R_{d-1})}\quad\text{in }K[a_1,\dots,a_{d-1}].
\]
\end{theorem}

\begin{proof}
Suppose $R_i^N=\sum_{j\neq i}c_jR_j$ with $c_j\in K[a]$. Evaluating at the
$K$-rational point corresponding to $f_{i,1}$, Proposition~\ref{prop:lines} gives
$0\neq\big(\pm(\binom di-1)^{d-i}\big)^N=0$, since $\binom di\ge d\ge3$ for
$1\le i\le d-1$. Contradiction.
\end{proof}

\begin{remark}
The proof does not use the Nullstellensatz: only the trivial direction ``if $R_i$
lies in the radical then it vanishes at every zero of $J_i$''. It uses neither
real roots nor the conjecture. In coordinates, the witness of index $i\le d-2$ is
the point with $a_{d-i}=1$ and all other coordinates zero; the one of index $d-1$
is $a_1=-1$. In both cases the coordinate that moves is $a_{d-i}$.
\end{remark}

\begin{remark}
Theorem~\ref{thm:all} has been formally verified in Lean~4 with Mathlib, for
every $d$ and every $i$, over an arbitrary field of characteristic zero: see the
theorems \texttt{exists\_witness} and \texttt{exists\_witness\_resultant} in the
accompanying development.
\end{remark}

\section{Consequences}

\subsection{No condition is redundant}

\begin{corollary}\label{cor:nonredundant}
For each $i$, the $d-2$ conditions ``$f$ shares a root with $H_j(f)$, $j\neq i$''
do not imply the $i$-th one, not even at the level of radicals. More precisely,
the line $L_i:=\{f_{i,t}:t\in K\}$ is contained in $V(J_i)$ and
$L_i\cap V(R_i)=\{0\}$.
\end{corollary}

Note the difference with the almost counterexamples of \cite{DdJ}: the
polynomials $f_{i,1}$ not only satisfy the conditions $j\neq i$, they
\emph{verifiably violate} the $i$-th one.

\subsection{Where the difficulty lies: one component against all}

\begin{lemma}\label{lem:components}
Fix $i$. Conjecture~\ref{conj:CA} holds in degree $d$ if and only if every
irreducible component $C$ of $V_{\KK}(J_i)$ satisfies $\dim C=1$ and
$R_i|_C\not\equiv0$.
\end{lemma}

\begin{proof}
($\Leftarrow$) Each component $C$ is stable under the action of $\KK^{\,*}$ (the
group is connected) and contains $0$ (the limit $\lambda\to0$). If $\dim C=1$ and
$p\in C\smallsetminus\{0\}$, the orbit of $p$ is infinite (the weights are
positive), so its closure is an irreducible closed set of dimension $1$ contained
in $C$, hence equal to $C$. Since $R_i$ is quasi-homogeneous,
$R_i(\lambda\cdot p)=\lambda^wR_i(p)$; if $R_i(p)=0$ for some $p\neq0$ in $C$
then $R_i$ vanishes on the whole orbit, hence on $C$, contrary to hypothesis.
Therefore $C\cap V(R_i)=\{0\}$ for every component, and
$V(J)=V(J_i)\cap V(R_i)=\{0\}$.

($\Rightarrow$) Suppose $V(J)=\{0\}$. By Krull's principal ideal theorem, every
component of $V(J_i)$ (defined by $d-2$ equations in $d-1$ variables) has
dimension $\ge1$. If some $C$ had dimension $\ge2$, then $C\cap V(R_i)$ would be
nonempty (it contains $0$) of dimension $\ge1$, contained in $V(J)$, absurd. And
if $R_i\equiv0$ on some $C$, then $C\subseteq V(J)$, also absurd.
\end{proof}

Theorem~\ref{thm:all} says that the component of $V(J_i)$ containing $L_i$
satisfies $R_i|_C\not\equiv0$. The conjecture asks for the same on \emph{every}
component (and for all of them to be curves). In particular, if the conjecture
holds then $L_i$ is an irreducible component of $V(J_i)$. The distance between
``one component'' and ``all of them'' is exactly the difficulty of
Casas--Alvero.

\subsection{Constraints on membership certificates}

The membership formulation of the conjecture asks, for each $k$, for a
certificate
\begin{equation}\label{eq:cert}
  a_k^N=\sum_{j=1}^{d-1}c_j\,R_j,\qquad c_j\in\mathbb{Q}[a_1,\dots,a_{d-1}].
\end{equation}
Let $\varphi_i:\mathbb{Q}[a]\to\mathbb{Q}[t]$ be the restriction to the line
$L_i$, that is, $a_{d-i}\mapsto t$ (or $a_1\mapsto-t$ if $i=d-1$) and all other
coordinates $\mapsto0$. Each coordinate $a_k$ moves on exactly one of the lines,
the one of index $i=d-k$.

\begin{corollary}\label{cor:certificates}
Every certificate \eqref{eq:cert} satisfies:
\begin{enumerate}
\item $N\ge d$;
\item $\varphi_{d-k}(c_{d-k})=\pm\,t^{N-d}\big/\big(\binom dk-1\big)^{k}$; in
  particular, the certificate for $a_k^N$ \emph{must use} $R_{d-k}$;
\item $\varphi_i(c_i)=0$ for every $i\neq d-k$.
\end{enumerate}
\end{corollary}

\begin{proof}
Apply $\varphi_i$ to \eqref{eq:cert}. By Proposition~\ref{prop:lines} only the
term $j=i$ survives:
$\varphi_i(a_k)^N=\varphi_i(c_i)\cdot\big(\pm(\binom di-1)^{d-i}t^d\big)$. If
$i=d-k$, the left-hand side is $\pm t^N$, which forces $N\ge d$ and the value of
$\varphi_{d-k}(c_{d-k})$, using $\binom d{d-k}=\binom dk$. If $i\neq d-k$, the
left-hand side is $0$ and, since $(\binom di-1)^{d-i}t^d\neq0$ in
$\mathbb{Q}[t]$, we get $\varphi_i(c_i)=0$.
\end{proof}

These conditions are the natural starting point for a search for explicit
certificates over $\mathbb{Q}$: they fix the behaviour of each coefficient $c_j$
on $d-1$ explicit lines.

\subsection{Relation to Ghosh's proof}

Ghosh \cite{Gh25} announced a complete proof of the conjecture (Koszul homology
plus Brouwer degree arguments), revised in March 2026 and, as far as we could
see, not published in a journal; an August 2026 preprint still treats it as open.
If Ghosh's proof is correct, it implies Theorem~\ref{thm:all}, and what this note
contributes is an elementary and independent proof. Should it contain an error,
Theorem~\ref{thm:all} stands as an unconditional partial result extending
Theorem~\ref{thm:SS}.

\section{Computational verification}

Everything was verified with SageMath 10.7 in the exact setting of \cite{SS}
(Hasse derivatives, $f$ unnormalised except for $a_d=0$).

\begin{center}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{>{\raggedright\arraybackslash}p{0.34\textwidth}%
                >{\raggedright\arraybackslash}p{0.56\textwidth}}
\toprule
Statement & Verification\\
\midrule
Prop.~\ref{prop:lines}
  & all $284$ resultants $R_j(f_{i,t})$, $3\le d\le10$, all $i,j$, with $t$
    symbolic: no failures.\\
Theorem~\ref{thm:all}, by evaluation
  & $3\le d\le9$, all $i$.\\
Theorem~\ref{thm:all}, by Gröbner bases
  & a radical test independent of the witnesses (Rabinowitsch's trick,
    $1\in J_i+(1-yR_i)$): $d=3,4,5$, all $i$, with outcome ``not a member''.\\
Theorem~\ref{thm:all}, in Lean~4
  & all $d$ and all $i$, over any field of characteristic zero, with no
    \texttt{sorry}.\\
\bottomrule
\end{tabular}
\end{center}

\section{Caveats}

\begin{itemize}
\item We checked the statement of Theorem~\ref{thm:SS} in version~7 of \cite{SS}
  (February 2025). It is striking that the general case is not observed there; we
  do not rule out that it appears elsewhere, or that the interest of \cite{SS}
  lay in the real-root method rather than in the statement.
\item This is not a deep result: it is a lemma. Its main use is
  Corollary~\ref{cor:certificates}, which constrains membership certificates over
  $\mathbb{Q}$, and Lemma~\ref{lem:components}, which locates the difficulty
  precisely.
\end{itemize}

\begin{thebibliography}{9}

\bibitem{CA} E.~Casas--Alvero, \emph{Higher order polar germs},
  J.~Algebra \textbf{240} (2001), 326--337.

\bibitem{CLO} W.~Castryck, R.~Laterveer, M.~Ounaïes,
  \emph{Constraints on counterexamples to the Casas--Alvero conjecture and a
  verification in degree 12}, arXiv:1208.5404.

\bibitem{DdJ} J.~Draisma, J.~P.~de Jong, \emph{On the Casas--Alvero conjecture},
  Newsletter of the EMS \textbf{80} (2011), 29--33.

\bibitem{Gh24} S.~Ghosh, \emph{A finiteness result towards the Casas--Alvero
  conjecture}, arXiv:2402.18717.

\bibitem{Gh25} S.~Ghosh, \emph{Proof of the Casas--Alvero conjecture},
  arXiv:2501.09272 (v2, March 2026).

\bibitem{GLSV} H.-C.~Graf von Bothmer, O.~Labs, J.~Schicho,
  C.~van de Woestijne, \emph{The Casas--Alvero conjecture for infinitely many
  degrees}, J.~Algebra \textbf{316} (2007), 224--230.

\bibitem{SS} D.~Schaub, M.~Spivakovsky, \emph{A note on the Casas--Alvero
  conjecture}, arXiv:2312.08742 (v7, February 2025).

\end{thebibliography}

\end{document}
```
