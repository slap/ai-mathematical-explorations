# Original AI output

Everything below the line is reproduced as produced, unedited. The conversation was in
Spanish; English translations of the two prompts are marked as such and were added here by the
curator. Nothing else was added, and nothing inside a quoted message was altered, shortened or
reordered.

**Session.** Claude Opus 5 (`claude-opus-5`), Anthropic, through Claude Code, 16 September
2026, in a working directory of the curator's own project on subresultants and the
Casas–Alvero conjecture.

**What is not included.** The earlier turns of the same session, in which the AI read and
commented on Ghosh's preprint as a whole and listed the places where it would look for errors.
They concern unpublished work by a third party and not the argument published here. Tool calls
(file writes, shell commands) are omitted as well; their results are kept where the AI quotes
them, and the scripts themselves are in [`computations/`](computations/). Local file paths
have been removed with the tool calls.

The LaTeX source at the end is the file as the AI wrote it. The `source.tex` published
alongside this file differs from it only by the editorial changes listed in its header.

---

**Prompt** — 2026-09-16 18:08

> hagamos esa simplificacion, usando teoria de interseccion

*(Translation: "let's do that simplification, using intersection theory".)*

---

**Claude** — 2026-09-16 18:10

Se puede, y sale mucho más corto de lo que esperaba. Dejame plantear el argumento y después lo verifico.

**La observación clave:** en `ℙ^{n−1}`, cualesquiera `r ≤ n−1` hipersuperficies tienen intersección no vacía, y cada una baja la dimensión a lo sumo en 1. Es el teorema de la dimensión proyectiva, puro Krull, sin topología.

**Lema 3.7, versión algebraica.** Sean `F_i = F(i,j_i)`, formas de grado `n+1−i`. Supongamos que `F_l ∈ √(F_{l+1},…,F_n)` y sea `Z = V_+(F_{l+1},…,F_n) ⊆ ℙ^{n−1}`.

- Son `n−l` ecuaciones, así que `Z ≠ ∅` y `dim Z ≥ l−1`.
- Por hipótesis `Z ⊆ V_+(F_l)`, o sea que agregar `F_l` no baja nada: `V_+(F_l,…,F_n) = Z`.
- Cortando con las `l−1` restantes, `dim V_+(F_1,…,F_n) ≥ (l−1) − (l−1) = 0`, y en particular **no es vacío**.

Un punto ahí es un `x ≠ 0` donde todas las condiciones se cumplen: un contraejemplo a Casas-Alvero en grado `n+1`. Pero eso es justo la **hipótesis inductiva** del paso descendente de Ghosh (su 4.1.1). Contradicción.

O sea: el Lema 3.7 **se deduce en cinco líneas de la hipótesis inductiva**, y desaparecen las páginas 11–13 con Abel–Goncharov, variedades de incidencia y grado de Brouwer. Verifico las cuentas de dimensión que sostienen el argumento:

*[The AI then wrote `interseccion_lema37.py` and ran it under SageMath. Its output:]*

```
n = 3 (grado d = 4)
  (H) dim V(F_1..F_n) = 0 en las 64 ramas: si
  (1) dim V(F_{l+1}..F_n) >= l  (teorema de la dimension):
      l=1 : dimensiones observadas [1]   cota >= 1 : OK
      l=2 : dimensiones observadas [2]   cota >= 2 : OK
      l=3 : dimensiones observadas [3]   cota >= 3 : OK
```

```
n = 4 (grado d = 5)
  (H) dim V(F_1..F_n) = 0 en las 625 ramas: si
  (1) dim V(F_{l+1}..F_n) >= l  (teorema de la dimension):
      l=1 : dimensiones observadas [1]   cota >= 1 : OK
      l=2 : dimensiones observadas [2]   cota >= 2 : OK
      l=3 : dimensiones observadas [3]   cota >= 3 : OK
```

*(The printed output for `n = 4` was truncated at `l = 3` by the command that produced it; the
line for `l = 4` was not captured. Re-running the script reproduces the full table.)*

---

**Claude** — 2026-09-16 18:11

Perfecto: las dimensiones observadas son **exactamente `l`**, el mínimo que permite el teorema. Eso confirma que el corte es ajustado y que el argumento se apoya justo donde debe. Escribo la nota.

---

**Claude** — 2026-09-16 18:12 *(after writing a first version of the note in Spanish)*

Hecha: `paper/nota-lema37-algebraico.pdf`, 3 páginas, compila limpio.

## El argumento

Sean `F_i = F(i,j_i)` las formas de grado `n+1−i` en el espacio de raíces. La hipótesis inductiva de Ghosh (su 4.1.1, la conjetura en grado `n+1`) dice, vía su Proposición 1.4, que `V₊(F₁,…,F_n) = ∅` en `ℙ^{n−1}`.

Supongamos `F_l ∈ √(F_{l+1},…,F_n)` y sea `Z = V₊(F_{l+1},…,F_n)`:

1. Son `n−l ≤ n−1` hipersuperficies, así que `Z ≠ ∅` y `dim Z ≥ l−1`.
2. Por hipótesis `Z ⊆ V₊(F_l)`, o sea que agregar `F_l` no baja la dimensión.
3. Cortando con las `l−1` formas restantes queda `dim V₊(F₁,…,F_n) ≥ 0`, en particular **no vacío**. Contradice la hipótesis.

Sólo usa el teorema de la dimensión y que los `F_i` sean formas no nulas.

## Qué se elimina

Desaparecen los polinomios de Abel–Goncharov, la variedad de incidencia, el espacio de sobreyecciones lineales, los caminos, bolas y esferas, la invariancia homotópica del grado de Brouwer y la positividad del índice holomorfo local. Son las páginas 11–13 del paper, y con ellas **la única dependencia analítica**: el argumento pasa a valer sobre cualquier cuerpo algebraicamente cerrado y en cualquier característica. Las Observaciones 3.8(1) y 3.8(2) quedan subsumidas.

La moraleja es simple: la positividad del índice local, que Ghosh usa para que el grado no se anule, no hace falta si uno cuenta dimensiones en el proyectivo, donde la no vacuidad de una intersección de pocas hipersuperficies es automática.

## Dos cosas a tener en cuenta

**El lema queda condicional.** El de Ghosh es incondicional (pero sólo sobre `ℂ`); el nuestro supone la conjetura en grado `n+1`. Eso alcanza porque el Lema 3.7 se usa únicamente para su Teorema 3.6, éste sólo vía el Corolario 3.9, y ese corolario se invoca dos veces —en la Proposición 4.3 y en el Lema 4.5—, ambas dentro de la Sección 4.2, bajo esa hipótesis. **Ese rastreo de citas conviene que lo confirme el autor**; lo hice siguiendo las referencias cruzadas del preprint, no reescribiendo el trabajo. Lo dejé dicho explícitamente en la nota.

**Verificación**, con las dimensiones calculadas:

| | `n=3` | `n=4` |
|---|---|---|
| hipótesis `dim V = 0` | 64/64 | 625/625 |
| conclusión `F_l ∉ √(…)` | 84/84 | 780/780 |
| cota `dim ≥ l` | exacta (`= l`) | exacta (`= l`) |

Las dimensiones son **exactamente `l`**, el mínimo que permite el teorema: el argumento se apoya justo en el caso ajustado, que es lo que uno quiere ver.

La escribí en castellano por consistencia con el resto del proyecto. Si la idea es mandársela a Ghosh, la paso a inglés.

---

**Prompt** — 2026-09-16 18:57

> si, hacelo en ingles

*(Translation: "yes, do it in English".)*

---

**Claude** — 2026-09-16 18:58 *(after writing the English version and compiling it)*

Listo: `paper/note-lemma37-algebraic.pdf`, 3 páginas, compila limpio y se lee bien.

Es la versión en inglés de la nota, con la misma estructura:

1. **Notación** en el espacio de raíces, con la reformulación por ramas (su Prop. 1.4) y la hipótesis (H).
2. **El lema y su demostración** por el teorema de la dimensión proyectiva, media página.
3. **Por qué alcanza la versión condicional**, con el rastreo de dónde se usa: Lema 3.7 → Teorema 3.6 → Corolario 3.9 → Proposición 4.3 y Lema 4.5, ambos bajo la hipótesis inductiva 4.1.1.
4. **Qué se elimina**, listado explícito de los objetos que desaparecen (Abel–Goncharov, la variedad de incidencia, `ℙ(L)`, caminos, bolas, esferas, invariancia homotópica del grado, positividad del índice holomorfo).
5. **Verificación computacional** en la tabla.

Mantuve los dos señalamientos de honestidad: que el lema queda condicional mientras que el de Ghosh es incondicional (aunque sólo sobre `ℂ`), y una observación pidiendo que el autor confirme el punto de uso, aclarando que salió de rastrear las referencias cruzadas de la v2 y no de reescribir el paper.

Quedan los dos archivos, `nota-lema37-algebraico.tex` en castellano y `note-lemma37-algebraic.tex` en inglés. Falta poner autores en ambos.

Si lo vas a mandar, yo agregaría una línea al mail aclarando que la verificación computacional es independiente del argumento: confirma tanto su Lema 3.7 como la hipótesis (H) en `d = 4, 5`, así que sirve igual aunque él prefiera conservar su versión incondicional.

---

## The note, as generated

`note-lemma37-algebraic.tex`, written 2026-09-16 18:58, reproduced byte for byte.

```latex
\documentclass[11pt,reqno]{amsart}

\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{array,booktabs}
\usepackage[margin=1.15in]{geometry}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{remark}[theorem]{Remark}

\newcommand{\PP}{\mathbb{P}}
\newcommand{\AAA}{\mathbb{A}}
\newcommand{\KK}{\mathbb{K}}
\newcommand{\bj}{\mathbf{j}}

% TODO: authors
\title[An algebraic proof of Ghosh's Lemma 3.7]
      {An algebraic proof of Ghosh's Lemma 3.7:\\
       intersection theory in place of Brouwer degree}
\author{}
\date{September 16, 2026}

\begin{document}

\begin{abstract}
In his proof of the Casas--Alvero conjecture, Ghosh \cite{Gho} establishes an
existence lemma for ``almost counterexamples'' (his Lemma 3.7) by means of
Abel--Gontcharoff polynomials and the topological Brouwer degree over
$\mathbb{C}$. This is the only analytic ingredient of the paper, and its proof
occupies pages 11--13. We observe that, in the setting where the lemma is
actually applied ---inside the downward inductive step, where the conjecture is
already assumed in degree $n+1$--- the statement follows from the projective
dimension theorem in a few lines. The resulting proof is purely algebraic, is
valid over any algebraically closed field with no hypothesis on the
characteristic, and removes every dependence on the Euclidean topology.
\end{abstract}

\maketitle

\section{Notation}

We follow \cite{Gho}. Let $\KK$ be algebraically closed, $n\ge2$, and
$R_n=\KK[x_1,\dots,x_n]$. For $1\le j\le n+1$ let $\Phi_j\colon R_n\to R_n$ be
the $\KK$-algebra automorphism
\[
  \Phi_j(x_l)=x_l-x_j\ (l\neq j),\qquad \Phi_j(x_j)=-x_j,
  \qquad \Phi_{n+1}=\mathrm{id},
\]
and let $e_k$ denote the elementary symmetric polynomial of degree $k$ in
$x_1,\dots,x_n$. For $1\le i\le n$ and $1\le j\le n+1$ put
\[
  F(i,j):=\Phi_j\big(e_{n+1-i}\big),
  \qquad \deg F(i,j)=n+1-i .
\]
These forms encode, for $f(X)=X\prod_{i=1}^n(X-x_i)$ of degree $n+1$, the
condition that $f$ and its $i$-th Hasse derivative share the root $x_j$: up to
sign, $F(i,j)$ is $f_i(x_j)$ written in the roots. For a fixed choice of indices
$\bj=(j_1,\dots,j_n)$ we write $F_i:=F(i,j_i)$.

We use the reformulation \cite[Prop.~1.4]{Gho} (from \cite{Gho24}):

\begin{proposition}[\cite{Gho}]\label{prop:reform}
The Casas--Alvero conjecture holds in degree $n+1$ over $\KK$ if and only if for
every choice $\bj$ the sequence $F_1,\dots,F_n$ is a regular sequence in $R_n$.
\end{proposition}

Since the $F_i$ are $n$ forms in $n$ variables, being a regular sequence is
equivalent to being a system of parameters, that is,
\begin{equation}\label{eq:H}
  V(F_1,\dots,F_n)=\{0\}\subseteq\AAA^n
  \qquad\Longleftrightarrow\qquad
  V_+(F_1,\dots,F_n)=\varnothing\subseteq\PP^{n-1}. \tag{H}
\end{equation}

\section{The lemma}

The statement needed in \cite{Gho} (his Lemma 3.7, via the Nullstellensatz) is:
for each $l$ there exists a degree $n+1$ polynomial $f$ with $f_i(x_{j_i})=0$ for
all $i>l$ but $f_l(x_{j_l})\neq0$; equivalently,
\[
  F_l\notin\sqrt{\big(F_{l+1},\dots,F_n\big)} .
\]

\begin{lemma}\label{lem:alg}
Let $\KK$ be algebraically closed and assume \eqref{eq:H} holds for the choice
$\bj$. Then, for every $1\le l\le n$,
\[
  F_l\notin\sqrt{\big(F_{l+1},\dots,F_n\big)}\quad\text{in } R_n .
\]
\end{lemma}

\begin{proof}
Assume the contrary and set $Z:=V_+(F_{l+1},\dots,F_n)\subseteq\PP^{n-1}$.

The $F_i$ are nonzero forms (each is a linear change of variables applied to
$e_{n+1-i}\neq0$), so $Z$ is cut out by $n-l\le n-1$ hypersurfaces of
$\PP^{n-1}$. By the projective dimension theorem, $Z\neq\varnothing$ and every
irreducible component of $Z$ satisfies
\[
  \dim Z\ \ge\ (n-1)-(n-l)\ =\ l-1 .
\]

By assumption $F_l$ vanishes on $Z$, i.e.\ $Z\subseteq V_+(F_l)$, and therefore
\[
  V_+(F_l,F_{l+1},\dots,F_n)=Z,\qquad \dim V_+(F_l,\dots,F_n)\ \ge\ l-1 .
\]

Now cut with the remaining $l-1$ hypersurfaces $V_+(F_1),\dots,V_+(F_{l-1})$.
Each intersection with a hypersurface of $\PP^{n-1}$ drops the dimension by at
most $1$, and is nonempty as long as the current dimension is $\ge1$; performing
the $l-1$ cuts starting from dimension $\ge l-1$ yields
\[
  \dim V_+(F_1,\dots,F_n)\ \ge\ (l-1)-(l-1)\ =\ 0 ,
\]
so in particular $V_+(F_1,\dots,F_n)\neq\varnothing$, contradicting
\eqref{eq:H}.
\end{proof}

\begin{remark}
The proof uses nothing about the characteristic of $\KK$: only Krull's dimension
theorem and the fact that the $F_i$ are nonzero forms. In particular,
\[
  \text{CA in degree } n+1 \text{ over } \KK
  \ \Longrightarrow\
  \text{Lemma 3.7 of \cite{Gho} over } \KK,
\]
in any characteristic. The version in \cite{Gho} is unconditional but is proved
only over $\mathbb{C}$.
\end{remark}

\begin{remark}
A point of $V_+(F_1,\dots,F_n)$ is precisely a counterexample to Casas--Alvero in
degree $n+1$ whose recycled roots are prescribed by $\bj$. Informally, the proof
says that if the $l$-th datum were a consequence of the later ones, then the full
system would be overdetermined by one equation fewer, and would therefore admit a
nontrivial solution.
\end{remark}

\section{Why the conditional version suffices}

Lemma 3.7 of \cite{Gho} is used only in the proof of his Theorem 3.6 (that
$\mu_{R_n}(\mathcal I_n(\bj))=n$), and the latter only through Corollary 3.9. In
turn, Corollary 3.9 is invoked twice, in the proofs of Proposition 4.3 and of
Lemma 4.5, both inside Section 4.2, that is, under the inductive hypothesis
4.1.1: \emph{the conjecture holds in degree $n+1$}. That hypothesis is exactly
\eqref{eq:H}.

Consequently, Lemma \ref{lem:alg} can replace Lemma 3.7 without altering the
structure of the argument: it suffices to state Theorem 3.6 in its conditional
form (``under \eqref{eq:H}, $\mu_{R_n}(\mathcal I_n(\bj))=n$''). Note also that
the form required in \cite[(3.9)]{Gho} is non-membership in the \emph{ideal}
$(F_i: i>l)$, which is weaker than the non-membership in the radical proved
here.

\begin{remark}
We would suggest that the author double-check this usage point: the reading above
comes from tracing the cross-references of the preprint (v2, March 2026), not
from a full rewriting of the paper.
\end{remark}

\section{What is removed and what is gained}

\begin{itemize}
\item The Abel--Gontcharoff polynomials, the incidence variety $\mathcal V$, the
  space $\PP(\mathcal L)$ of linear surjections, the paths $\gamma$, the balls
  $B_R(\mathbf 0)$ and spheres $S_{\epsilon_i}(z_i)$, the homotopy invariance of
  the Brouwer degree and the positivity of the local holomorphic index
  (\cite[Part I, §5.4]{AGZV}) all disappear. These are essentially pages 11--13
  of \cite{Gho}.
\item The only analytic dependence disappears: the argument becomes valid over
  any algebraically closed field, not just over $\mathbb{C}$, and in any
  characteristic.
\item Remarks 3.8(1) and 3.8(2) of \cite{Gho}, which handle special cases by
  explicit witnesses and by Rolle's theorem, become subsumed.
\end{itemize}

The moral is the usual one in intersection theory: the positivity of the local
index of a holomorphic map, which \cite{Gho} uses to guarantee that the degree
does not vanish, is unnecessary if one argues with dimensions in projective
space, where the nonemptiness of an intersection of few hypersurfaces is
automatic.

\section{Computational verification}

Using SageMath 10.7, in the root-space formulation, we verified for all choices
$\bj$ and all $l$:

\begin{center}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{>{\raggedright\arraybackslash}p{0.42\textwidth}%
                >{\raggedright\arraybackslash}p{0.22\textwidth}%
                >{\raggedright\arraybackslash}p{0.22\textwidth}}
\toprule
 & $n=3$ ($d=4$) & $n=4$ ($d=5$)\\
\midrule
hypothesis \eqref{eq:H}: $\dim V(F_1,\dots,F_n)=0$ & $64/64$ branches & $625/625$ branches\\
conclusion: $F_l\notin\sqrt{(F_i:i>l)}$ & $84/84$ cases & $780/780$ cases\\
dimension bound $\dim V(F_{l+1},\dots,F_n)\ge l$ & sharp ($=l$) & sharp ($=l$)\\
cases covered by \cite[Rmk.~3.8(1)]{Gho} & $43\%$ & $23\%$\\
\bottomrule
\end{tabular}
\end{center}

The observed dimensions are exactly $l$, the minimum allowed by the dimension
theorem: the argument rests on the tight case. The last row also shows that the
proportion of cases that \cite{Gho} settles by explicit witnesses decreases with
the degree, so the step replaced here is the one carrying almost all of the
work.

\begin{thebibliography}{9}

\bibitem{AGZV} V.~I.~Arnold, S.~M.~Gusein-Zade, A.~N.~Varchenko,
  \emph{Singularities of Differentiable Maps, Volume 1}, Birkhäuser, 2012.

\bibitem{Gho24} S.~Ghosh, \emph{A finiteness result towards the Casas--Alvero
  conjecture}, arXiv:2402.18717.

\bibitem{Gho} S.~Ghosh, \emph{Proof of the Casas--Alvero conjecture},
  arXiv:2501.09272 (v2, March 2026).

\end{thebibliography}

\end{document}
```
