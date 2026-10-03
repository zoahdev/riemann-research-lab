# Exact minimum spectral defect for a triple

Date: 2026-10-04. Written elementary proof; not peer reviewed or formalized. Literature novelty unconfirmed.

## Problem

Let B be a positive semidefinite Hermitian 3-by-3 matrix with B_ii = 1. Set

\[
 e=\sum_{i<j}|B_{ij}|^2,\qquad
 V=\operatorname{tr}(B-I)^2=2e.
\]

For nonnegative t define

\[
 \Psi(t)=\begin{cases}(t-1)^2&0\le t\le2,\\2t-3&t\ge2,\end{cases}
 \qquad \Delta(B)=\sum_{j=1}^3\Psi(\lambda_j(B)).
\]

This is the defect used in [Wang, Proposition 2.1 and Lemma 3.1](https://arxiv.org/html/2609.24167v1). We optimize the local matrix problem without assuming B arises from a particular Fourier kernel.

## Theorem

For every such B, 0 <= e <= 3 and

\[
 \Delta(B)\ge F(e):=
 \begin{cases}
 2e,&0\le e\le3/4,\\
 2e-\big(\sqrt{4e/3}-1\big)^2,&3/4\le e\le3.
 \end{cases}
\]

For every e in [0,3] equality is attainable. Thus F is the exact minimum, not merely a lower estimate. In particular

\[
 \Delta(B)\ge \frac53 e,
\]

and the coefficient 5/3 cannot be increased for this class of matrices.

## Proof

Write the eigenvalues as t >= a >= b >= 0. Their sum is 3, so t <= 3. The sum of their squares is at most 9, hence V <= 6 and e <= 3. Alternatively each off-diagonal entry has absolute value at most 1 by positivity of 2-by-2 minors.

At most one eigenvalue can exceed 2. Since

\[
 \Psi(x)=(x-1)^2-(x-2)_+^2,
\]

we have the exact identity

\[
 \Delta(B)=V-(t-2)_+^2.
\]

The relation (a-1)+(b-1)=1-t and the inequality x^2+y^2 >= (x+y)^2/2 imply

\[
 V\ge (t-1)^2+\frac12(t-1)^2=\frac32(t-1)^2.
\]

Since t >= 1, it follows that t <= 1+sqrt(2V/3). Thus

\[
 \Delta(B)\ge V-\big(\sqrt{2V/3}-1\big)_+^2=F(e).
\]

For attainability choose r=sqrt(e/3) in [0,1] and

\[
 B_r=(1-r)I+r\mathbf1\mathbf1^*.
\]

It has unit diagonal, is positive semidefinite, and has eigenvalues 1+2r, 1-r, 1-r. Its energy is e=3r^2 and its defect equals F(e). This proves exactness for every e.

For the uniform coefficient, if t <= 2 then Delta=V. If t>2, the same variance inequality gives

\[
 \frac{(t-2)^2}{V}\le\frac23\left(\frac{t-2}{t-1}\right)^2\le\frac16,
\]

because 2<t<=3. Consequently Delta >= (5/6)V=(5/3)e. At B_1=11* the eigenvalues are 3,0,0, giving Delta=5 and e=3, so the coefficient is sharp. QED.

## Block consequence

Let G be any PSD Hermitian matrix with unit diagonal. Choose disjoint principal triples B_j, with energies e_j. Then

\[
 \operatorname{tr}\Psi(G)\ge\sum_j\operatorname{tr}\Psi(B_j)\ge\sum_j F(e_j).
\]

To justify the first inequality without operator-convexity assumptions, take an orthonormal eigenbasis of each principal block and the remaining principal block. Together these form a basis of the whole space. Each diagonal expectation of G is a convex combination of its eigenvalues. Scalar Jensen applies because Psi is convex; summing over this basis proves the trace inequality. The unused block contributes nonnegatively.

F is increasing: its derivative is 2 below 3/4 and 2/3+2/sqrt(3e)>0 above 3/4. Thus e_j >= e_* implies Delta(G) >= J F(e_*), for any 0<=e_*<=3. This extends the threshold range of the cited triple lemma.

## What this changes and what it does not

The result provides the complete local energy-to-defect profile and equality matrices. It does not automatically sharpen Wang's global constant: that argument's guaranteed overlap energy is small, and in the small-energy regime this result gives the same 2e_* factor. A new global gain needs stronger kernel-specific local information or a different assembly.

The equality matrices describe all PSD correlation matrices at fixed energy, not necessarily Fourier-kernel matrices for three distinct ordinates. In particular B_1 uses identical vectors. Sharpness for the unrestricted matrix class does not establish sharpness for the zeta-kernel subclass.
