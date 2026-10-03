# Source ledger

Checked 2026-10-04. This is a focused survey of the pair-correlation / spectral-defect route, not an exhaustive claim about all RH research. Numerical proportions refer to asymptotic counts, not every zero.

| Primary source | Relevant input | Verification in this repository |
| --- | --- | --- |
| [Baluyot, Goldston, Suriajaya, Turnage-Butterbaugh, arXiv:2306.04799](https://arxiv.org/abs/2306.04799) | Unconditional pair-correlation input used downstream | Bibliographic reference; analytic proof not replayed |
| [Alpöge–Furman, arXiv:2608.13637v2](https://arxiv.org/html/2608.13637v2) | Critical simple-zero proportion about 0.6725; different-zero proportion about 0.8362 | Abstract and selected sections, including Section 1.4 limitations, consulted; full formalization not replayed |
| [Lamzouri, arXiv:2609.02882v1](https://arxiv.org/html/2609.02882v1) | Proposition 2.1, finite conjugation-invariant multisets; second-moment counting | Relevant finite inequality and proof consulted |
| [Lamzouri, arXiv:2609.02882v2](https://arxiv.org/abs/2609.02882v2) | Additional lower bound 88.76% for the union of simple zeros and critical-line zeros, and average-proportion bound 83.62% | Updated abstract checked; these are different counting statistics from simple critical-line zeros |
| [Wang, arXiv:2609.24167v1](https://arxiv.org/html/2609.24167v1) | Spectral defect in Proposition 2.1 and triple pinching in Lemma 3.1; small claimed global gain | Relevant matrix lemmas read; global transfer not independently certified |
| [Santibañez-Leal, Zenodo version 0.01](https://zenodo.org/records/22940291) | September 24 sharp auxiliary three-point ratio claim | Landing-page claim only; proof/certificates not audited |
| [Knausgård, arXiv:2609.33043v1](https://arxiv.org/html/2609.33043v1) | September 27 distinct-zero proportion claim about 0.836993; variable clipping and mixed multiplicities | Relevant statement and verification section read; imported interval certificate not replayed |
| [Zhu, arXiv:2608.24827v2](https://arxiv.org/html/2608.24827v2) | Claimed all-function positivity on [-0.8,0.8], very small variational upper bounds, and a barrier for its particular finite-reduction method | Abstract and introductory statements consulted; complete reduction and certificates not independently audited |
| [Seven-point optimized-window submission, fixed commit](https://github.com/josusanmartin/riemann/blob/dc788ef833400b4f24901ae0c6d654082e066c5c/submissions/seven-point-optimised-window/submission.json) | Submitted exact lower-bound score 67342981/100000000, with Lean solution named in metadata | GitHub API content and immutable commit checked; full Lean project and analytic imports not independently replayed |
| [Yang–Yang, Zenodo 21975237](https://zenodo.org/records/21975237) | Claimed 79.62% simple critical-line proportion | Authors explicitly label it a certified candidate rather than an established theorem; analytic formalization and external review pending; no promotion to an accepted baseline here |

Knausgård's paper explicitly lists analytic and computational inputs that are hypotheses in its formal statements. Its stated formal checks should not be read as a complete formal proof of all analytic inputs.

Knausgård's references also point to [ainta/zeta-simple-zeros](https://github.com/ainta/zeta-simple-zeros), [yuhangshi888/zeta-simple-zeros-673316977](https://github.com/yuhangshi888/zeta-simple-zeros-673316977), [tawanerguo-cn/zeta-simple-zeros](https://github.com/tawanerguo-cn/zeta-simple-zeros), and [trmdy/zeta-simple-zeros-673137](https://github.com/trmdy/zeta-simple-zeros-673137). These are discovery leads, not independently verified baselines here. Therefore 0.6725 is not described as the latest record. Nor is the seven-point submission asserted here to be the uniquely largest independently accepted bound.

## Attribution and novelty

Zhu's claimed full-window certificate is different in scope from this
repository's finite-cell certificates. The latter do not bound the infinite
complement. Extremely small or floating-point negative values are particularly
unsafe here. The preprint's method-specific complexity barrier should not be
interpreted as a theorem excluding every possible RH proof or disproof route.

The clipped defect and pinching framework come from the cited work. Note 001 gives an independent elementary optimization of a local 3-by-3 problem. No priority claim is made; a broader literature and repository check is still needed. Note 002 is an elementary diagnostic construction, not a new zeta-zero theorem.

## Evidence levels

- Local notes: written proofs, exact rational regression checks, and floating-point stress tests.
- External preprints: attributed statements, with selected sections read.
- Global improvement or RH proof: not established by this repository.
