# Disproof programme and Claude audit

Checked 2026-10-04. RH has neither been proved nor disproved in this repository.
This is a map of selected major routes, not a claim to have read every RH paper.

## What Claude accomplished

[Anthropic's announcement](https://www.anthropic.com/research/riemann-zeta)
attributes an improved unconditional zero-proportion bound to a research version
of Claude, subsequently checked by mathematicians.
[Alpöge and Furman's paper, v2](https://arxiv.org/html/2608.13637v2)
gives approximately 0.6725 for simple zeros on the critical line and 0.8362
for distinct zeros. Section 1.4 explicitly explains that the remaining zeros
are not shown to lie off the line. Its inputs tolerate a sparse set of off-line
zeros. Thus this proportion method alone cannot decide RH. Later refinements
listed in note 000 are separate claims, not a complete proof audit here.

The useful connection for a disproof search is the indefinite Weil form: a
strictly negative, correctly computed witness would refute RH. An improved
positive-index lower bound is not such a witness.

## Major constraints and potential disproof certificates

| Route and primary source | What is established | What would refute RH |
| --- | --- | --- |
| [Clay status](https://www.claymath.org/millennium/riemann-hypothesis/) | RH remains listed as unsolved | A verified nontrivial zero off the critical line |
| [Platt–Trudgian](https://arxiv.org/abs/2004.09765) | Rigorous verification for ordinates up to 3 trillion | A direct search must go beyond this verified region |
| [Suzuki's screw-function framework](https://arxiv.org/html/2606.09096v1) | Equivalent positivity criteria; small-scale positivity; proposed spectral limit | One strictly negative finite screw-kernel quadratic form |
| [Rodgers–Tao](https://arxiv.org/abs/1801.05914) | The de Bruijn–Newman constant is nonnegative | A strictly positive lower bound for that constant |
| [Griffin–Ono–Rolen–Zagier](https://arxiv.org/abs/1902.07321) | Eventual Jensen-polynomial hyperbolicity at each fixed degree | A rigorously non-hyperbolic member of the RH-equivalent family |
| [Guth–Maynard](https://arxiv.org/abs/2405.20552) | Stronger zero-density estimates | Density estimates alone do not provide a counterexample |
| [Connes survey](https://arxiv.org/html/2602.04022v1) | Spectral programmes and approximation results | Missing all-scale spectral properties cannot be assumed |

No route is known to guarantee a fast disproof. RH might be true. The operational
priority here is to produce checkable witnesses rather than infer failure from
an incomplete positive result.

## First arithmetic search: finite screw matrices

The evaluator in `experiments/weil_kernel.py` uses the prime-side expression
for g, not a truncated list containing only known critical-line zeros. Write
S(t,u)=g(t-u)-g(t)-g(u), with g even and g(0)=0. The existing equivalence in the
cited screw-function literature says that RH implies every finite S matrix
is positive semidefinite. Consequently, a negative finite quadratic form
is enough for disproof, after independent verification of the implementation
and the imported equivalence.

For exact rational nodes and coefficients, rounding is enclosed with Arb.
Prime powers are enumerated by an integer sieve; interval comparisons verify
the proposed summation cutoff. For t>0 the omitted archimedean series after M
terms is bounded above by

    exp(-(2M+1/2)t) / ((M+1/4)^2 (1-exp(-2t))).

This bound follows by replacing every remaining denominator by its first
denominator and summing a geometric series. A symmetric interval containing
this entire tail is added before forming the matrix. Interval LDL pivots
strictly above zero certify the specified matrix. A failed pivot is only
inconclusive; it is never automatically reported as a counterexample.

Published runs use 48 nodes in [-3,3] and 128 nodes in [-6,6]. Both matrices
were certified positive definite; no negative zeta witness was found.
A synthetic conjugate off-line frequency pair produces a negative diagonal
and checks that the detector can reject positivity. It is explicitly not
Riemann-zeta data. Precision replay and independent identities for the special
constants are covered by tests.

These coarse grids do not resolve oscillations at height 3 trillion. Increasing
the endpoint naively also costs roughly exp(2a) in prime enumeration. Neither
these tests nor scanning finitely many positive matrices proves RH. The next
technical bottleneck is an efficient high-frequency witness representation
or a certified direct contour search beyond the verified height.

## Rejected shortcuts

- Do not treat the complement of a lower bound as an off-line proportion.
- Do not build the Weil form from only already-known on-line zeros.
- Do not treat a floating-point negative eigenvalue as a certificate.
- Do not transfer a counterexample for a different zeta-like function to zeta.
- Do not assume all-scale positivity to construct a supposedly unconditional
  positive Hilbert-space metric.

Novelty is not claimed for this implementation or these finite checks.
