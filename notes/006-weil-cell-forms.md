# Certified interference between high-frequency Weil probes

This extends [note 005](005-modulated-weil.md) from individual positive values
to the complete Hermitian form on a specified finite-dimensional space. No
novelty or RH resolution is claimed. The Weil normalization remains that of
[Suzuki's explicit formula](https://arxiv.org/html/2606.09096v1).

## Basis and conjugation convention

Partition [-L/2,L/2] into N disjoint cells of width h=L/N, with centres
c_j=(j-(N-1)/2)h. Use v_j(x)=exp(iTx) times the indicator of cell j.
They are orthogonal in L² and each has squared norm h. Define

    M_ij = Q(v_j,v_i),
    Q(sum_j a_j v_j) = sum_ij conjugate(a_i) M_ij a_j,
    ||sum_j a_j v_j||² = h sum_j |a_j|².

The ordering matters because Q(u,v)=W(u*tilde(v)) is linear in its first
argument. This convention makes M the usual Hermitian matrix acting on the
coefficient column a. The smoothing argument from note 005 applies to every
fixed finite combination of these indicators; its autocorrelation remains
compactly supported and Lipschitz. Under RH the exact M is positive semidefinite.

The diagonal is the note-005 value Q_h(T). For j-i=k>=1, the cross
autocorrelation is supported at positive distances and equals

    f_k(d) = (h-|d-kh|)_+ exp(iTd).

It vanishes at zero, including for adjacent cells. Thus there is no diagonal
regularization term, and only positive prime-power shifts contribute.

## Exact off-diagonal formula

For s=kh define

    z_m=2m+1/2-iT,
    E(delta)=sum_{m>=0} exp(-z_m delta)/z_m²,  delta>=0,
    D_b(s)=[exp(-b(s-h))+exp(-b(s+h))-2exp(-bs)]/b².

Substitution into the explicit formula gives

    M_ij = D_{1/2-iT}(s)+D_{-1/2-iT}(s)
           - sum_n Lambda(n)/sqrt(n) (h-|log(n)-s|)_+ exp(iT log(n))
           - E(s-h)-E(s+h)+2E(s).

For i>j take the complex conjugate. The two D terms are elementary integrals
of the shifted triangular function against the pole exponentials.
For the archimedean term, expand
exp(-d/2)/(1-exp(-2d)) as a geometric series. Each integral equals
D_{z_m}(s), and therefore sums to the indicated second difference of E.
This interchange is absolutely convergent: even for s=h the triangle is O(d)
near zero while the archimedean density is O(1/d).

When delta=0, the tail is not bounded with a geometric denominator:

    E(0) = (1/4) zeta(2,1/4-iT/2).

For delta>0 truncate after m=M-1 and use the rigorous disk bound

    |E(delta)-partial_sum|
      <= exp(-(2M+1/2)delta)/((2M+1/2)²(1-exp(-2delta))).

A complex disk is enclosed conservatively by adding this radius to both real
and imaginary coordinates. All subsequent arithmetic is performed with Arb.
Each prime power contributes to at most two neighbouring lags. Floating-point
bin proposals are checked against exact rational boundaries by interval
comparisons; a failed comparison aborts rather than producing a sign claim.

## Matrix certification and candidate replay

Interval Hermitian LDL* uses

    D_j = M_jj - sum_{k<j}|L_jk|² D_k,
    L_ij = [M_ij-sum_{k<j} L_ik conjugate(L_jk)D_k]/D_j.

Strictly positive pivot enclosures certify positive definiteness of this exact
constructed Hermitian matrix. Inconclusive pivots are not a disproof. The
reported minimum pivot is not an eigenvalue lower bound.

Separately, a floating-point eigenvector proposes dyadic rational coefficients.
The exact-coefficient Rayleigh value is then enclosed with Arb. Only a strictly
negative enclosure would be a candidate for independent high-precision replay
and verification of the formula. The approximate eigenvalue is explicitly
labelled approximate and is never used as the certificate. When a negative
candidate occurs, all dyadic coefficients are saved to permit replay.

## Validation and results

- The all-ones coefficient vector reconstructs the full interval test from
  note 005, including at height 3000000000001.
- At T=0 each cross entry agrees with
  2g(s)-g(s-h)-g(s+h), independently linking it to the screw implementation.
- Direct low-frequency complex quadrature checks the real and imaginary
  components, including prime shifts. It is regression evidence, not the
  rigorous remainder bound.
- A 60/100-digit replay checks complex enclosures at high frequency.
- A synthetic off-line frequency pair has positive diagonal values but a
  negative linear combination, checking that the candidate detector catches
  interference that diagonal tests miss. This is not Riemann-zeta data.

Published arithmetic runs use L=12, T=3000000000001+j/4 for j=0,...,7, and
both N=48 and N=96. Every matrix was interval-certified positive definite.
No negative candidate was found. The runs certify all complex coefficient
vectors in those specific finite spaces, but not arbitrary functions on the
window and not a zero-free region. Doubling the mesh adds directions; it does
not supply a bound for the discarded infinite-dimensional complement.

Reproduce:

```sh
python experiments/weil_cells.py --samples 8 --output results/weil-cells-high.json
python experiments/weil_cells.py --cells 96 --samples 8 --output results/weil-cells-high-96.json
python -m unittest discover -s tests -v
```

Larger support still requires exponentially more prime powers, and uniform
positivity over all functions or frequencies remains a separate problem.
This instrument enables a more substantial disproof search; it does not
guarantee that one exists or that increasing a mesh will find one quickly.
