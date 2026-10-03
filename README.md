# Riemann research lab / 黎曼猜想研究记录

Public research notebook started on 2026-10-04 (Asia/Shanghai), with AI assistance from OpenAI Codex.

**Status: RH is neither proved nor disproved here. No new global zero-proportion record is claimed.**

当前方向：寻找严格的证伪证书。已核对 Claude 的约 67.25% 下界成果；它没有确定剩余零点在临界线外。新增基于素数端显式公式和 Arb 区间运算的有限核矩阵搜索，首轮没有找到反例。见 [证伪路线审计](notes/003-disproof-audit.md)。

首批结果是一个有完整初等证明的三点谱缺陷精确界，以及一个说明仅靠二阶矩无法统一改进计数不等式的等号构造。它们是可审查的局部数学结果；文献新颖性尚未确认，也没有完成到黎曼零点全局界限的转移。

## Results

1. [Sharp three-point spectral defect profile](notes/001-sharp-triple-profile.md): for a PSD Hermitian 3-by-3 matrix with unit diagonal and off-diagonal energy `e`, the minimum clipped spectral defect is exactly
   - `2e`, for `0 <= e <= 3/4`;
   - `2e - (sqrt(4e/3)-1)^2`, for `3/4 <= e <= 3`.
   Equicorrelation matrices attain equality at every energy. The sharp uniform coefficient is `Delta >= (5/3)e`.
2. [Second-moment saturation obstruction](notes/002-saturation.md): explicit sinc-kernel multisets saturate both finite-multiset counting inequalities. A universally positive correction needs additional kernel or configuration information.
3. [Source ledger and verification boundaries](notes/000-sources.md): recent primary sources, with proof status and imported hypotheses kept separate.
4. [Disproof audit and arithmetic search](notes/003-disproof-audit.md): Claude's result, selected equivalent criteria, rigorous finite positivity checks and explicit search limitations.
5. [Pointwise-positive semigroup obstruction](notes/004-semigroup-obstruction.md): an explicit positive cross term rules out a direct positivity-preserving semigroup argument for the localized Weil operator at all scales; this is compatible with RH.
6. [High-frequency modulated Weil probe](notes/005-modulated-weil.md): exact prime-side formula, geometric remainder enclosure, and 32 positive test values above height 3 trillion. These values are not a zero-free-region certificate.
7. [Hermitian forms on modulated cells](notes/006-weil-cell-forms.md): certified cross terms and full finite-subspace positivity at 48 and 96 dimensions, plus exact dyadic candidate replay for negative directions.
8. [Stage evidence and remaining objective](notes/007-stage-audit.md): requirement-by-requirement evidence, current-status distinctions, and the unfulfilled larger disproof objective.

## Reproduce

Python 3.10+:

```sh
python -m pip install -r requirements.txt
python -m pip install -r requirements-rh.txt
python -m unittest discover -s tests -v
python experiments/check_triple_profile.py --samples 10000 --output results/triple-profile.json
python experiments/weil_kernel.py --max-node 6 --intervals 64 --dps 100
```

Exact rational tests cover the equality family and elementary proof identities. Seeded floating-point tests check complex Gram matrices and pinching; they are regression evidence, not a proof or an interval certificate. The proof is in the notes. No Lean verification is claimed.

## Next research steps

The current priority is a rigorous negative Weil/screw witness or a certified
off-line zero beyond the verified height. No quick resolution is promised.
The proportion-improvement directions below remain secondary background work.

- Audit kernel-specific attainability of the extremal matrices; arbitrary correlation matrices need not come from distinct zeta-zero ordinates.
- Seek a certified lower bound on three-point overlap energy that exceeds the low-energy regime, or use larger blocks and a different window.
- Independently replay the local interval certificates behind recent global claims before importing their constants.
- Derive and verify all smoothing, counting and asymptotic transfer steps before claiming an improvement in a zero proportion.

Progress is published as reviewable commits. External results retain their original attribution; this repository does not certify the complete proofs of its cited preprints.
