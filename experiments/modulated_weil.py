"""Certified Weil values for modulated interval indicators (note 005).

No RH assumption and no list of known zeros is used. Negative values are
candidates requiring independent replay; positive values certify only tests.
"""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import time

from flint import acb, arb, ctx
if __package__:
    from .weil_kernel import ArithmeticScrew, rational
else:
    from weil_kernel import ArithmeticScrew, rational


class ModulatedWeil:
    def __init__(self, length='8', dps=80):
        self.length = Fraction(length)
        if self.length <= 0 or dps < 30:
            raise ValueError('require length>0, dps>=30')
        self.dps = dps
        ctx.dps = dps
        arithmetic = ArithmeticScrew(self.length, dps)
        self.l = rational(self.length)
        self.weights = []
        for (n, p), logn in zip(arithmetic.powers, arithmetic.logs):
            if logn < self.l:
                self.weights.append((logn, (self.l-logn)*arb(p).log()/arb(n).sqrt()))
            elif not logn > self.l:
                raise ArithmeticError('prime cutoff unresolved')
        self.terms = max(1, math.ceil((dps+10)*math.log(10)/(2*float(self.l.mid()))))

    def value(self, frequency):
        ctx.dps = self.dps
        t = rational(Fraction(frequency))
        pole = arb(0)
        for real in (arb('1/2'), arb('-1/2')):
            z = acb(real, -t)
            pole += 2*(self.l/z-(1-(-z*self.l).exp())/z**2).real
        primes = sum((weight*(t*logn).cos() for logn, weight in self.weights), arb(0))
        q = acb(arb('1/4'), -t/2)
        arch = self.l*(q.digamma().real-arb.pi().log())+acb(2).zeta(q).real/2
        series = acb(0)
        for k in range(self.terms):
            z = acb(arb(2*k)+arb('1/2'), -t)
            series += (-z*self.l).exp()/z**2
        # |z_k| >= 2k+1/2; denominators increase. Geometric tail.
        first = arb(2*self.terms)+arb('1/2')
        tail = (-first*self.l).exp()/first**2/(1-(-2*self.l).exp())
        value = pole-2*primes+arch-2*series.real
        return value+arb(0, 2*tail.upper())


def run(length='8', start='3000000000001', step='1/4', samples=32, dps=80):
    begin = time.time()
    evaluator = ModulatedWeil(length, dps)
    frequencies = [Fraction(start)+j*Fraction(step) for j in range(samples)]
    values = [evaluator.value(t)/evaluator.l for t in frequencies]
    negative = [str(t) for t, value in zip(frequencies, values) if value < 0]
    uncertain = [str(t) for t, value in zip(frequencies, values) if not (value > 0 or value < 0)]
    return {
        'status': 'negative_candidates_require_replay' if negative else
                  'inconclusive_values' if uncertain else 'specified_tests_positive',
        'length': str(evaluator.length), 'precision_digits': dps,
        'prime_power_count': len(evaluator.weights), 'tail_terms': evaluator.terms,
        'frequencies': [str(t) for t in frequencies],
        'normalized_weil_enclosures': [str(v) for v in values],
        'negative_candidates': negative, 'uncertain': uncertain,
        'seconds': round(time.time()-begin, 3),
        'scope': 'finite test functions only; not a zero count or a zero-free region',
        'rh_status': 'unresolved',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', default='8')
    parser.add_argument('--start', default='3000000000001')
    parser.add_argument('--step', default='1/4')
    parser.add_argument('--samples', type=int, default=32)
    parser.add_argument('--dps', type=int, default=80)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error('samples must be positive')
    rendered = json.dumps(run(args.length, args.start, args.step, args.samples, args.dps), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
