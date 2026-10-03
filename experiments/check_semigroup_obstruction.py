"""Enclose constants in note 004; the complete proof is in the note."""
import argparse
import json
from pathlib import Path

from flint import arb, ctx
if __package__:
    from .weil_kernel import off_diagonal_density
else:
    from weil_kernel import off_diagonal_density


def run(dps=80):
    ctx.dps = dps
    r = (arb(3)/2).log()
    epsilon = (arb(9)/8).log()/4
    low, high = r-2*epsilon, r+2*epsilon
    support = r/2+epsilon
    h = off_diagonal_density(low)
    identity = (arb(2).sqrt()-1)/arb(2).root(4)
    assert support < arb(1)/4
    assert low > 0 and high < arb(2).log()
    assert h > arb('0.3483') and h.overlaps(identity)
    # Even-support distances avoid every prime-power shift.
    assert arb('0.41') < arb(2).log() < arb('0.79')
    assert arb('0.81') < arb(3).log()
    even_bound = off_diagonal_density(arb('0.39'))
    assert even_bound > 0
    # A positive-definite matrix can have a non-positive-preserving semigroup.
    matrix_semigroup_cross = ((-arb(3)).exp()-(-arb(1)).exp())/2
    assert matrix_semigroup_cross < 0
    return {
        'status': 'constant_enclosures_verified',
        'precision_digits': dps,
        'support_radius': str(support),
        'cross_distance_min': str(low),
        'cross_distance_max': str(high),
        'cross_form_lower_bound': str(h),
        'even_cross_form_lower_bound': str(even_bound),
        'positive_matrix_semigroup_cross_at_t1': str(matrix_semigroup_cross),
        'scope': 'obstruction to the usual pointwise cone, not RH',
        'rh_counterexample': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dps', type=int, default=80)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.dps < 30:
        parser.error('require dps>=30')
    rendered = json.dumps(run(args.dps), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
