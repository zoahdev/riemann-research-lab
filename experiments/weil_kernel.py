"""Arithmetic screw kernel with explicit tail enclosures; no RH assumed.

Reference: Suzuki, arXiv:2606.09096v1, equation (1.3).
Arb encloses rounding and the omitted geometric-series tail. A positive
finite matrix certifies only that matrix, never the full Weil criterion.
"""
from bisect import bisect_right
from fractions import Fraction
import argparse
import json
import math
from pathlib import Path
import time

from flint import arb, ctx


def rational(x):
    x = Fraction(x)
    return arb(x.numerator) / x.denominator


def prime_powers(limit):
    """Return (p**k,p) with integer sieve and all k>=1, no duplicates."""
    sieve = bytearray(b'\x01') * (limit + 1)
    sieve[0:2] = b'\x00\x00'
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p*p:limit+1:p] = b'\x00' * ((limit-p*p)//p+1)
    out = []
    for p in range(2, limit + 1):
        if sieve[p]:
            power = p
            while power <= limit:
                out.append((power, p))
                power *= p
    return sorted(out)


class ArithmeticScrew:
    def __init__(self, max_t, dps=80):
        ctx.dps = dps
        self.dps = dps
        self.max_t = Fraction(max_t)
        self.max_ball = rational(self.max_t)
        # This integer bound must be verified, not trusted from a float.
        limit = int(float(self.max_ball.exp().mid())) + 2
        while not arb(limit) > self.max_ball.exp():
            limit += 1
        self.powers = prime_powers(limit)
        self.logs = [arb(n).log() for n, _ in self.powers]
        self.log_midpoints = [float(x.mid()) for x in self.logs]
        self.mass = [arb(0)]
        self.logmass = [arb(0)]
        for (n, p), logn in zip(self.powers, self.logs):
            weight = arb(p).log() / arb(n).sqrt()
            self.mass.append(self.mass[-1] + weight)
            self.logmass.append(self.logmass[-1] + weight * logn)
        self.psi_quarter = arb('1/4').digamma()
        self.zeta_quarter = arb(2).zeta(arb('1/4'))
        self.cache = {Fraction(0): arb(0)}

    def g(self, t):
        key = abs(Fraction(t))
        if key > self.max_t:
            raise ValueError('argument exceeds precomputed prime range')
        if key in self.cache:
            return self.cache[key]
        x = rational(key)
        index = bisect_right(self.log_midpoints, float(x.mid()))
        # Float arithmetic proposes an index; Arb validates the exact cut.
        while index and self.logs[index-1] > x:
            index -= 1
        while index < len(self.logs) and self.logs[index] < x:
            index += 1
        if index and not self.logs[index-1] < x:
            raise ArithmeticError('prime boundary unresolved; increase precision')
        if index < len(self.logs) and not self.logs[index] > x:
            raise ArithmeticError('prime boundary unresolved; increase precision')
        prime_part = x*self.mass[index] - self.logmass[index]
        q = (-2*x).exp()
        # Any positive M is valid. This choice makes the rigorous tail small.
        terms = max(1, math.ceil((self.dps+10)*math.log(10)/(2*float(x.mid()))))
        term = (-x/2).exp()
        arch_series = arb(0)
        for n in range(terms):
            arch_series += 16*term / (4*n+1)**2
            term *= q
        # Remaining sum <= exp(-(2M+1/2)x)/(M+1/4)^2/(1-q).
        tail = term / rational(Fraction(terms) + Fraction(1, 4))**2 / (1-q)
        if not tail >= 0:
            raise ArithmeticError('tail sign unresolved')
        arch_series += arb(0, tail.upper())
        value = (-4*((x/2).exp()+(-x/2).exp()-2) + prime_part
                 - x/2*(self.psi_quarter-arb.pi().log())
                 - (self.zeta_quarter-arch_series)/4)
        self.cache[key] = value
        return value

    def matrix(self, points):
        points = [Fraction(t) for t in points]
        values = [self.g(t) for t in points]
        return [[self.g(x-y)-values[i]-values[j]
                 for j, y in enumerate(points)] for i, x in enumerate(points)]


def certify_ldl(matrix):
    """Enclose an LDL* factorization of the real symmetric exact matrix.

    Positive interval pivots prove positive definiteness at these nodes.
    A nonpositive/uncertain pivot is INCONCLUSIVE, not a counterexample.
    """
    n = len(matrix)
    lower = [[arb(0) for _ in range(n)] for _ in range(n)]
    diagonal = []
    for j in range(n):
        pivot = matrix[j][j] - sum((lower[j][k]**2*diagonal[k] for k in range(j)), arb(0))
        if not pivot > 0:
            return {'status': 'inconclusive', 'pivot_index': j, 'pivot': str(pivot)}
        diagonal.append(pivot)
        lower[j][j] = arb(1)
        for i in range(j+1, n):
            cross = matrix[i][j] - sum((lower[i][k]*lower[j][k]*diagonal[k] for k in range(j)), arb(0))
            lower[i][j] = cross / pivot
    smallest = min(diagonal, key=lambda x: float(x.lower()))
    return {'status': 'finite_matrix_positive_definite', 'size': n,
            'minimum_pivot_enclosure': str(smallest),
            'scope': 'specified nodes only; no continuum or all-scale conclusion'}


def rayleigh(matrix, vector):
    vector = [rational(v) for v in vector]
    return sum((vector[i]*matrix[i][j]*vector[j]
                for i in range(len(vector)) for j in range(len(vector))), arb(0))


def toy_offline_g(t, gamma=1, sigma=Fraction(1, 4)):
    """Synthetic conjugate non-real frequency pair, not zeta data."""
    gamma, sigma = rational(gamma), rational(sigma)
    real_numerator = 1-(gamma*t).cos()*(sigma*t).cosh()
    imaginary_numerator = (gamma*t).sin()*(sigma*t).sinh()
    c, d = gamma**2-sigma**2, 2*gamma*sigma
    return -2*(real_numerator*c+imaginary_numerator*d)/(c**2+d**2)


def off_diagonal_density(d):
    """Weil form density away from zero and all prime-power shifts."""
    return 2*(d/2).cosh()-(-d/2).exp()/(1-(-2*d).exp())


def run(max_node=3, intervals=24, dps=80):
    start = time.time()
    maximum = Fraction(max_node)
    evaluator = ArithmeticScrew(2*maximum, dps)
    # Positive and negative nodes; zero omitted since its row is identically zero.
    points = [maximum*Fraction(j, intervals) for j in range(-intervals, intervals+1) if j]
    matrix = evaluator.matrix(points)
    result = certify_ldl(matrix)
    # Deterministic rational directions are separately enclosed.
    directions = ([Fraction((-1)**j) for j in range(len(points))],
                  [Fraction(1) for _ in points])
    enclosed = [rayleigh(matrix, v) for v in directions]
    control_t = 2*arb.pi()
    control_diagonal = -2*toy_offline_g(control_t)
    if not control_diagonal < 0:
        raise AssertionError('negative control failed')
    density = off_diagonal_density(arb(2).log()/2)
    if not density > 0:
        raise AssertionError('semigroup obstruction sign failed')
    result.update({
        'max_node': str(maximum), 'intervals_per_side': intervals,
        'precision_digits': dps, 'prime_power_count': len(evaluator.powers),
        'g_zero': '0 (exact)',
        'rational_direction_enclosures': [str(v) for v in enclosed],
        'synthetic_offline_diagonal': str(control_diagonal),
        'synthetic_control_is_zeta_counterexample': False,
        'off_diagonal_density_at_log_sqrt2': str(density),
        'seconds': round(time.time()-start, 3),
        'rh_status': 'unresolved',
    })
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-node', default='3')
    parser.add_argument('--intervals', type=int, default=24)
    parser.add_argument('--dps', type=int, default=80)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.intervals < 1 or Fraction(args.max_node) <= 0 or args.dps < 30:
        parser.error('require intervals>=1, max-node>0, dps>=30')
    rendered = json.dumps(run(args.max_node, args.intervals, args.dps), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
