# A concrete obstruction to pointwise-positive Weil semigroups

This note proves a limitation of one possible spectral shortcut. It does not
refute RH, refute the cited spectral programmes, or establish a novelty claim.
All inequalities in the proof are elementary; the accompanying Arb script
independently encloses the constants.

## Setup and statement

Use the Weil functional and real bilinear form Q(u,v)=W(u*tilde(v)) in
[Suzuki, introductory explicit formula](https://arxiv.org/html/2606.09096v1).
Let A_a be the lower-bounded self-adjoint operator associated with its closed
localized form on L²(-a,a), containing compactly supported smooth functions
in its form domain. These operator/form constructions are imported from the
cited literature, not proved here.

Let rho be the unique root larger than 1 of x³-x-1=0. Then:

**Proposition.** If a > (log rho)/2, the semigroup exp(-t A_a), t>=0,
cannot preserve the usual cone of pointwise nonnegative real functions.
Adding any scalar multiple of the identity to A_a cannot remove this
obstruction. In particular, a=1/4 already admits an explicit pair of witnesses.

A second explicit construction shows the same failure on the even-function
subspace when a>121/200. This concerns the usual pointwise cone; alternative
cones or transforms, inverse operators and other spectral arguments are not
excluded.

## Step 1: off-diagonal density

For nonnegative smooth u,v with disjoint supports, suppose every distance
between their supports avoids all log(p^k). The convolution vanishes at zero
and at prime-power shifts. Substitution into the explicit formula, followed
by changing variables in the two ordinary integrals, gives

    Q(u,v) = integral integral u(x)v(y) H(|x-y|) dx dy,
    H(d) = 2 cosh(d/2) - exp(-d/2)/(1-exp(-2d)),   d>0.

There is no diagonal regularization term or prime-shift term in this case.
For x=exp(d)>1, exact simplification gives

    H(d) = x^(-1/2) (x³-x-1)/(x²-1).

The polynomial is strictly increasing for x>=1, so H(d)>0 exactly when
d>log rho. H is also strictly increasing on d>0: the first term has positive
derivative, and the positive function exp(-d/2)/(1-exp(-2d)) is decreasing.

## Step 2: disjoint positive witnesses

For a>(log rho)/2, choose d strictly between log rho and min(2a,log 2).
This interval is nonempty since rho<2. Choose a sufficiently small epsilon>0
such that bumps centred at ±d/2 with support radii epsilon lie inside (-a,a)
and all cross-distances lie in (log rho,log 2). They are disjoint; there are
no prime-power shifts below log 2. Normalize each bump to have integral 1.
Then Q(u,v)>0.

An explicit instance uses

    R = log(3/2),   epsilon = (1/4)log(9/8),
    u(x)=epsilon^(-1) b((x-R/2)/epsilon),
    v(x)=epsilon^(-1) b((x+R/2)/epsilon),

where b is any nonnegative C-infinity bump supported in [-1,1] with integral
1; for example normalize exp(-1/(1-x²)) on |x|<1 and set it to zero elsewhere.
The support is contained in (-1/4,1/4), since

    R/2+epsilon = (1/4)log(81/32) < 1/4.

For the last inequality, e>8/3>81/32 suffices. The distance interval is

    [log sqrt(2), log(9/(4sqrt(2)))] subset (0,log 2).

At its left endpoint,

    H(log sqrt(2)) = (sqrt(2)-1)/2^(1/4) > 0.

Monotonicity therefore proves the quantitative bound

    Q(u,v) >= (sqrt(2)-1)/2^(1/4) > 0.3483.

This is a positive CROSS term, not a negative value Q(u,u).

## Step 3: semigroup contradiction using the form domain

If a lower-bounded self-adjoint A generated a positivity-preserving semigroup
T_t=exp(-tA), disjoint nonnegative u,v in its form domain would satisfy
<u,v>=0 and <T_t u,v>>=0. The spectral representation of the closed form gives

    Q(u,v) = limit as t decreases to 0 of <(I-T_t)u,v>/t <= 0.

For completeness, first shift A to B=A+cI>=0. On its form domain,
(1-exp(-t lambda))/(t lambda) lies in [0,1] and tends to 1 for lambda>0.
The spectral theorem and dominated convergence applied to B^(1/2)u and
B^(1/2)v prove this limit. The shift term c<u,v> is zero. Multiplication by
exp(-ct)>0 leaves positivity preservation unchanged.

The positive cross term from Step 2 contradicts this necessary condition.
Only form-domain membership is needed, not differentiability in the operator
domain. This proves the proposition.

## Even-subspace witness

Let epsilon=1/200. Take nonnegative even normalized bump sums with centres
±3/5 for u and ±1/5 for v, giving half the mass to each bump. Their supports
are disjoint and fit in (-a,a) for a>121/200. Their cross-distances belong to

    [39/100,41/100] union [79/100,81/100].

The first interval lies below log 2, the second above log 2 and below log 3,
so no prime-power shift occurs. H is positive throughout both: exp(39/100)
>139/100 and (139/100)^3-139/100-1>0 suffice. Hence Q(u,v)>0.
Reflection invariance of the form makes the even subspace invariant under
the associated operator and semigroup. Applying Step 3 inside that subspace
gives the claimed even-cone obstruction.

## Meaning for RH research

Suzuki's Section 5.2 proves positivity improvement for the separate limiting
small-scale form L and its operator T. The proposition here concerns the full
localized Weil operator A_a; it does not contradict that result. Likewise,
small-scale ground-state information cannot simply be promoted to an
all-scale positivity-preserving semigroup statement for A_a.

This excludes applying Perron–Frobenius arguments directly to exp(-tA_a)
with the pointwise cone at all scales. It does not exclude ground-state
simplicity or evenness by another argument. A positive operator need not
generate a positivity-preserving semigroup: the matrix [[2,1],[1,2]] is
positive definite, but exp(-tA) has negative off-diagonal entries for t>0.
Consequently this obstruction is fully compatible with RH being true.

A targeted prior-work search also located the primary repository
[Siman–Claude, rh-spectral](https://github.com/monksealseal/rh-spectral),
which already lists an indefinite kernel as an obstacle to Perron–Frobenius,
and a bibliographic lead entitled *The pole term is the only obstruction to
Perron structure in the localized Weil quadratic form*,
[Zenodo 20682834](https://zenodo.org/records/20682834). The latter full text
was not accessible during this audit. The obstruction idea therefore must
not be presented as new; this note supplies an explicit continuum witness
and elementary proof, without a priority claim.

Reproduce the numerical enclosures with
`python experiments/check_semigroup_obstruction.py`.
