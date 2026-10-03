"""Hermitian Weil forms on modulated disjoint cells; see note 006."""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import time

import numpy as np
from flint import acb, arb, ctx
if __package__:
    from .modulated_weil import ModulatedWeil
    from .weil_kernel import ArithmeticScrew, rational
else:
    from modulated_weil import ModulatedWeil
    from weil_kernel import ArithmeticScrew, rational


def exponential_tail(delta, frequency, dps):
    """E(delta)=sum exp(-(2k+1/2-iT)delta)/(2k+1/2-iT)^2."""
    delta = Fraction(delta)
    t = rational(frequency)
    if delta == 0:
        return acb(2).zeta(acb(arb('1/4'), -t/2))/4
    if delta < 0:
        raise ValueError('delta must be nonnegative')
    x = rational(delta)
    terms = max(1, math.ceil((dps+10)*math.log(10)/(2*float(x.mid()))))
    total = acb(0)
    for k in range(terms):
        z = acb(arb(2*k)+arb('1/2'), -t)
        total += (-z*x).exp()/z**2
    first = arb(2*terms)+arb('1/2')
    bound = (-first*x).exp()/first**2/(1-(-2*x).exp())
    return total+acb(arb(0, bound.upper()), arb(0, bound.upper()))


def abs_square(z):
    return z.real**2+z.imag**2


def certify_hermitian(matrix):
    """Interval LDL*: positive pivots certify the exact constructed form.

    Precondition: the exact matrix is Hermitian by its analytic construction.
    Overlapping entry intervals alone cannot establish that identity.
    """
    n = len(matrix)
    lower = [[acb(0) for _ in range(n)] for _ in range(n)]
    diagonal = []
    for j in range(n):
        pivot = matrix[j][j].real-sum((abs_square(lower[j][k])*diagonal[k]
                                      for k in range(j)), arb(0))
        if not pivot > 0:
            return {'status': 'inconclusive', 'pivot_index': j, 'pivot': str(pivot)}
        diagonal.append(pivot)
        lower[j][j] = acb(1)
        for i in range(j+1, n):
            cross = matrix[i][j]-sum((lower[i][k]*lower[j][k].conjugate()*diagonal[k]
                                     for k in range(j)), acb(0))
            lower[i][j] = cross/pivot
    return {'status': 'specified_subspace_positive_definite', 'size': n,
            'minimum_pivot_enclosure': str(min(diagonal, key=lambda v: float(v.lower())))}


def rayleigh(matrix, coefficients):
    c = [acb(rational(re), rational(im)) for re, im in coefficients]
    return sum((c[i].conjugate()*matrix[i][j]*c[j]
                for i in range(len(c)) for j in range(len(c))), acb(0)).real


class WeilCells:
    def __init__(self, length='12', cells=48, dps=80):
        if cells < 1 or Fraction(length) <= 0 or dps < 30:
            raise ValueError('require positive length/cells and dps>=30')
        self.length, self.cells, self.dps = Fraction(length), cells, dps
        self.width = self.length/cells
        ctx.dps = dps
        self.h = rational(self.width)
        self.diagonal = ModulatedWeil(self.width, dps)
        arithmetic = ArithmeticScrew(self.length, dps)
        self.weights = [[] for _ in range(cells)]
        for (n, p), logn in zip(arithmetic.powers, arithmetic.logs):
            if logn > rational(self.length):
                continue
            # Floating-point bin proposal must pass exact interval comparisons.
            k = math.floor(float(logn.mid())/float(self.width))
            if not rational(k*self.width) < logn < rational((k+1)*self.width):
                raise ArithmeticError('prime bin unresolved; increase precision')
            for lag in (k, k+1):
                if 1 <= lag < cells:
                    tent = self.h-abs(logn-rational(lag*self.width))
                    if not tent > 0:
                        raise ArithmeticError('tent sign unresolved')
                    self.weights[lag].append((logn, arb(p).log()/arb(n).sqrt()*tent))

    def matrix(self, frequency):
        ctx.dps = self.dps
        frequency = Fraction(frequency)
        t = rational(frequency)
        tails = [exponential_tail(k*self.width, frequency, self.dps)
                 for k in range(self.cells+1)]
        cross = [acb(self.diagonal.value(frequency))]
        for lag in range(1, self.cells):
            s = lag*self.width
            pole = acb(0)
            for real in (arb('1/2'), arb('-1/2')):
                z = acb(real, -t)
                pole += ((-z*rational(s-self.width)).exp()
                         +(-z*rational(s+self.width)).exp()
                         -2*(-z*rational(s)).exp())/z**2
            prime = sum((weight*acb(0, t*logn).exp()
                         for logn, weight in self.weights[lag]), acb(0))
            arch = tails[lag-1]+tails[lag+1]-2*tails[lag]
            cross.append(pole-prime-arch)
        # M_ij=Q(v_j,v_i), so c* M c = Q(sum c_j v_j).
        return [[cross[j-i] if j >= i else cross[i-j].conjugate()
                 for j in range(self.cells)] for i in range(self.cells)]


def run(length='12', cells=48, start='3000000000001', step='1/4', samples=8, dps=80):
    begin = time.time()
    evaluator = WeilCells(length, cells, dps)
    results = []
    for j in range(samples):
        frequency = Fraction(start)+j*Fraction(step)
        matrix = evaluator.matrix(frequency)
        certificate = certify_hermitian(matrix)
        # A floating-point vector proposes an exact dyadic candidate; Arb verifies it.
        midpoints = np.array([[complex(float(z.real.mid()), float(z.imag.mid()))
                               for z in row] for row in matrix])
        eigenvalues, vectors = np.linalg.eigh(midpoints)
        vector = vectors[:, 0]
        c = [(Fraction(round(float(z.real)*2**24), 2**24),
              Fraction(round(float(z.imag)*2**24), 2**24)) for z in vector]
        value = rayleigh(matrix, c)
        norm = evaluator.h*sum((rational(re)**2+rational(im)**2 for re, im in c), arb(0))
        candidate = value/norm
        certificate.update({'frequency': str(frequency),
                            'normalized_dyadic_rayleigh_enclosure': str(candidate),
                            'approximate_minimum_eigenvalue_over_width': float(eigenvalues[0])/float(evaluator.width),
                            'negative_candidate': bool(candidate < 0)})
        if candidate < 0:
            certificate['dyadic_coefficients'] = [[str(re), str(im)] for re, im in c]
        results.append(certificate)
    return {'length': str(evaluator.length), 'cells': cells,
            'precision_digits': dps, 'runs': results,
            'seconds': round(time.time()-begin, 3),
            'scope': 'specified finite subspaces; not all functions or a zero-free region',
            'rh_status': 'unresolved'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', default='12')
    parser.add_argument('--cells', type=int, default=48)
    parser.add_argument('--start', default='3000000000001')
    parser.add_argument('--step', default='1/4')
    parser.add_argument('--samples', type=int, default=8)
    parser.add_argument('--dps', type=int, default=80)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error('samples must be positive')
    rendered = json.dumps(run(args.length, args.cells, args.start, args.step,
                              args.samples, args.dps), indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
