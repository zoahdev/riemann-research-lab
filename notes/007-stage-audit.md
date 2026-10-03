# Research-stage evidence and limits

Audit date: 2026-10-04. This audits the bounded stage of checking recent status,
examining the spectral/local-certificate route, completing a strictly checkable
local target, and publishing proofs, code, validation and limitations. It does
not declare the user's larger RH-disproof objective achieved.

## Current mathematical status

[Clay](https://www.claymath.org/millennium/riemann-hypothesis/) still lists RH
as unsolved. [Anthropic's original announcement](https://www.anthropic.com/research/riemann-zeta)
and the [Alpöge–Furman paper](https://arxiv.org/abs/2608.13637v2) concern an
unconditional proportion bound, not a solution. Later attributed claims and
their verification boundaries are documented in note 000. A largest number
on a search page is not by itself an accepted mathematical record. No attempt
is made to certify every published or unpublished RH argument.

The four statistics below must remain distinct:

- zeros both simple and on the critical line;
- distinct zeros;
- zeros simple or on the critical line (a union);
- the average of two separate proportions.

None determines where the complement of a lower bound lies. None excludes
a sparse off-line set.

## Requirement-by-requirement evidence

| Stage requirement | Evidence | Scope of completion |
| --- | --- | --- |
| Check current RH and recent zero-proportion status | Primary-source ledger 000 and route audit 003; official status checked on the audit date | Selected current sources and reported verification levels; no exhaustive-literature or latest-world-record claim |
| Audit spectral-defect and local-certificate route | Notes 001, 002 and 004 separate unrestricted matrix sharpness, attainable saturation, and a pointwise-semigroup obstruction | Local written derivations; no automatic global transfer |
| Complete a strictly checkable local mathematical target | Note 001 proves the exact minimum defect at every energy, gives attaining matrices, and proves sharpness of the uniform coefficient | The stated 3-by-3 PSD unit-diagonal matrix problem is solved completely |
| Implement arithmetic disproof instruments with explicit errors | Notes 003, 005 and 006 derive prime-side values, geometric tail bounds and Hermitian forms; corresponding scripts use Arb | Negative candidates can be proposed and enclosed; no negative zeta witness found |
| Validate formulas rather than rely on floating-point signs | Exact rational identities, independent ordinary-integral checks, precision replay, partition/refinement identities, synthetic negative controls and interval LDL* | 20 automated tests; tests complement the written proofs and do not certify RH |
| Publish proofs, code, results and limitations | Public repository contains notes, tracked experiments, JSON results and CI workflow | Public files and the CI run at the final publication commit must be checked after publishing this audit |

## Verification distinctions

The note-001 proof is elementary and complete within its stated assumptions;
it is neither peer reviewed nor Lean formalized, and its novelty is unconfirmed.
Floating-point stress tests are regression checks only. Arb certificates enclose
rounding and the explicit omitted tails; their mathematical force depends on
the written formula and the interval library's implementation. The independent
mpmath integrals are normalization checks, not additional rigorous certificates.

The semigroup obstacle is compatible with a positive Weil form. A failed LDL*
pivot is inconclusive. A positive minimum pivot is not a minimum-eigenvalue
lower bound. Floating-point eigenvectors only propose exact dyadic vectors;
the Rayleigh sign is recomputed with intervals.

The 48- and 96-cell certificates cover all complex combinations in specified
finite spaces. They neither bound the discarded infinite-dimensional complement
nor establish a zero-free region. Synthetic off-line pairs validate negative
detection but are not zeta zeros.

## Outcome and remaining larger objective

This stage produced a complete local optimization theorem, explicit proof-route
diagnostics and reproducible rigorous arithmetic search tools. It did not
improve a global zeta-zero proportion, establish novelty, prove RH, or disprove
RH. The original larger request to find a counterexample remains unfulfilled.

A genuine disproof would require an independently verified off-line zero or
a strictly negative admissible Weil/screw witness. Increasing positive finite
tests alone does not achieve that objective. The code is available to support
further searches, but there is no mathematical guarantee of a fast disproof.
