# A directly evaluable high-frequency Weil probe

This note derives an exact arithmetic formula with an explicit tail bound.
It supplies a disproof-search instrument, not a new RH theorem or a priority
claim. The starting normalization is the introductory Weil functional in
[Suzuki](https://arxiv.org/html/2606.09096v1). No zero list or RH assumption is
used in the implementation.

## Test family and the smooth approximation

For L>0 and real T take

    v(x) = exp(iTx) 1_{[-L/2,L/2]}(x),
    f(x) = (v*tilde(v))(x) = (L-|x|)_+ exp(iTx).

Its squared L² norm is L. Although v has jumps, its autocorrelation f is
compactly supported and Lipschitz, and the regularized Weil integral converges
absolutely. This family is valid for a disproof test by mollification:
v_epsilon=v*eta_epsilon for a smooth nonnegative approximate identity. Then
f_epsilon=f*(eta_epsilon*tilde(eta_epsilon)) converges uniformly to f, with
uniformly bounded support and Lipschitz constants at each fixed L,T.
The regularized numerator near zero is bounded by C|x| uniformly in epsilon.
The archimedean density is O(1/|x|) there, giving an integrable bound; outside
zero it is dominated by an integrable exponential tail. Only finitely many
prime-power evaluations occur in the common support. Dominated convergence
therefore gives W(f_epsilon)->W(f).

Under RH every smooth autocorrelation has nonnegative Weil value. Thus an
independently verified strictly negative W(f) would contradict RH. No such
value has been found here. Positivity of this restricted family is not itself
claimed to be equivalent to RH.

## Exact formula

Set q=1/4-iT/2, z_k=2k+1/2-iT, and

    J(z) = L/z - (1-exp(-zL))/z².

Write psi for digamma and zeta(2,q) for Hurwitz zeta, not Riemann zeta at
complex height. Direct evaluation of the Weil functional gives

    Q_L(T) = 2 Re[J(1/2-iT)+J(-1/2-iT)]
           - 2 sum_{n<=exp(L)} Lambda(n)/sqrt(n) (L-log(n)) cos(T log(n))
           + L (Re psi(q)-log(pi))
           + (1/2) Re zeta(2,q)
           - 2 Re sum_{k>=0} exp(-z_k L)/z_k².

The prime term is finite and includes all prime powers, not just primes.
An endpoint with log(n)=L contributes zero.

To verify the archimedean algebra, its original regularized contribution is

    2 sum_{k>=0} [L/(2k+1) - Re J(z_k)].

The bracketed series converges absolutely. In the grouped difference,

    sum [L/(2k+1)-Re L/z_k]
       = (L/2) Re[psi(q)-psi(1/2)],
    sum Re(1/z_k²) = (1/4) Re zeta(2,q).

Finally psi(1/2)=-EulerGamma-2log(2). Combining this with the diagonal term
-L(log(4pi)+EulerGamma) yields -L log(pi), as displayed above. These operations
keep the two divergent harmonic sums grouped; they are not summed separately.

The identity J(z)=integral_0^L (L-x)exp(-zx) dx also verifies the pole term.
All relevant z have nonzero real part, so these expressions have no removable
singularity needing a special case.

## Tail certificate and complexity

After k=0,...,M-1, use |z_k|>=2k+1/2 and monotonically increasing denominators:

    |sum_{k>=M} exp(-z_k L)/z_k²|
      <= exp(-(2M+1/2)L)/((2M+1/2)² (1-exp(-2L))).

The real value Q_L(T) is enclosed by adding twice this bound as a symmetric
Arb radius. The tail bound and number of geometric terms do not grow with T.
The number of prime powers grows with exp(L); large support remains expensive.
Phase evaluation and special-function precision still depend on the size of T,
so this is not a claim of constant total complexity at arbitrarily large T.

The implementation enumerates prime powers with integer arithmetic, checks the
cutoff with Arb, and evaluates exact rational T and L with interval arithmetic.
Ambiguous cutoffs fail explicitly. No floating-point sign is accepted as proof.

## Validation and first high-height run

At T=0 the independent screw-function identity is Q_L(0)=-2g(L). Tests verify
overlapping enclosures at several lengths. A separately coded direct numerical
integral verifies the normalization for nonzero low frequencies; this mpmath
check is regression evidence, not an interval proof. A 60/100-digit replay
checks the high-frequency evaluation. The enclosure proof is the formula and
tail bound above, implemented with Arb.

`results/modulated-high-12.json` records L=12 and 32 rational frequencies
T=3000000000001+j/4, j=0,...,31, at 80 digits. All normalized Q_L(T)/L values
were strictly positive. This is a finite set of test-function certificates.
It is not a certified zero count, a zero-free interval, or evidence sufficient
to prove RH. Its purpose is to establish that a prime-side high-frequency
search can run without enumerating trillions of zeros or using a prohibitively
fine spatial grid.

Reproduce:

```sh
python -m pip install -r requirements-rh.txt
python experiments/modulated_weil.py --length 12 --samples 32 --output results/modulated-high-12.json
python -m unittest discover -s tests -v
```

The next step is to enlarge the function space with interference between
multiple probes. Checking positive diagonal values alone cannot rule out a
negative direction of a Hermitian form.
