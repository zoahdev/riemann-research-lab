# Exact saturation of the second-moment counting bounds

Date: 2026-10-04. Elementary diagnostic result; novelty unconfirmed.

Take eta equal to 1 on [-1/2,1/2] and zero elsewhere. It is real and even, its squared integral is one, and its support lies strictly inside (-lambda,lambda) if lambda>1/2. The Fourier kernel is

\[
 K(z)=\frac{\sin(\pi z)}{\pi z},\qquad K(0)=1.
\]

Choose distinct integer points, a of multiplicity one and b of multiplicity two. The resulting finite multiset is conjugation invariant. For unequal integer points K(x-y)=0, exactly. With multiplicities included,

\[
 N=a+2b,\quad E=\sum_{z,s}K(z-s)^2=a+4b,\quad S=a,\quad D=a+b.
\]

Consequently

\[
 S=2N-E,\qquad D=\frac{3N-E}{2}.
\]

These are equality configurations for the bounds in [Lamzouri, Proposition 2.1](https://arxiv.org/html/2609.02882v1). The simple-point Gram matrix is the identity, so the clipped spectral defect is also exactly zero.

Any rational q in [1,2] can occur as E/N: choose integers a,b with q=(a+4b)/(a+2b). For example, if q=u/v in lowest terms, a=2(2v-u), b=u-v works (including endpoints); then N=2v, E=2u. Taking disjoint new integer sites replicates this at arbitrarily large N.

Therefore no strictly positive correction depending only on q can hold uniformly over all these kernels and multisets at rational q in [1,2]. This does not exclude a kernel-specific or density-dependent improvement, does not construct zeta zeros, and does not obstruct RH itself.

The useful research implication is precise: do not spend effort strengthening the universal second-moment inequality alone at these ratios. Investigate extra information that rules out the equality configurations, such as a fixed optimized window plus a bound on total spread and local overlaps.
