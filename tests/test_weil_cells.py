from fractions import Fraction as F
import unittest
import mpmath as mp
from flint import acb, arb, ctx

from experiments.weil_cells import WeilCells, certify_hermitian, rayleigh
from experiments.modulated_weil import ModulatedWeil
from experiments.weil_kernel import ArithmeticScrew, prime_powers


class CellForms(unittest.TestCase):
    def test_partition_reconstructs_full_interval(self):
        for t in (F(0), F(3, 4), F(3000000000001)):
            evaluator = WeilCells(2, 4, 80)
            matrix = evaluator.matrix(t)
            combined = rayleigh(matrix, [(F(1), F(0))]*4)
            expected = ModulatedWeil(2, 80).value(t)
            self.assertTrue(combined.overlaps(expected))

    def test_zero_frequency_second_difference(self):
        evaluator = WeilCells(2, 4, 80)
        matrix = evaluator.matrix(0)
        kernel = ArithmeticScrew(2, 80)
        for lag in range(1, 4):
            s, h = lag*F(1, 2), F(1, 2)
            expected = 2*kernel.g(s)-kernel.g(s-h)-kernel.g(s+h)
            self.assertTrue(matrix[0][lag].real.overlaps(expected))
            self.assertTrue(matrix[0][lag].imag.contains(0))

    def test_refined_partition_embeds_coarse_form(self):
        coarse = WeilCells(2, 4, 80).matrix(3000000000001)
        fine = WeilCells(2, 8, 80).matrix(3000000000001)
        for i in range(4):
            for j in range(4):
                combined = sum((fine[2*i+a][2*j+b] for a in (0, 1) for b in (0, 1)), acb(0))
                self.assertTrue(coarse[i][j].overlaps(combined))

    def test_complex_cross_integral(self):
        evaluator = WeilCells(2, 4, 80)
        matrix = evaluator.matrix(3)
        with mp.workdps(110):
            h, t = mp.mpf('0.5'), mp.mpf(3)
            for lag in (1, 2):
                s = lag*h
                def integrand(x):
                    if not x:
                        return -mp.mpf('0.5')
                    tent = h-abs(x-s)
                    density = 2*mp.cosh(x/2)-mp.exp(-x/2)/(-mp.expm1(-2*x))
                    return tent*density*mp.exp(1j*t*x)
                value = mp.quad(integrand, [s-h, s, s+h])
                for n, p in prime_powers(int(mp.exp(s+h))+1):
                    logn = mp.log(n)
                    if s-h < logn < s+h:
                        value -= mp.log(p)/mp.sqrt(n)*(h-abs(logn-s))*mp.exp(1j*t*logn)
                self.assertTrue(matrix[0][lag].real.overlaps(arb(mp.nstr(value.real, 105), '1e-90')))
                self.assertTrue(matrix[0][lag].imag.overlaps(arb(mp.nstr(value.imag, 105), '1e-90')))

    def test_planted_pair_negative_combination(self):
        ctx.dps = 80
        depth = arb('1/4')
        h = arb(1)
        # A conjugate off-line pair at the modulation frequency.
        mass = 2*(2*(depth*h/2).sinh()/depth)**2
        cross = mass*(depth*h).cosh()
        matrix = [[acb(mass), acb(cross)], [acb(cross), acb(mass)]]
        self.assertTrue(mass > 0)
        self.assertTrue(rayleigh(matrix, [(F(1), F(0)), (F(-1), F(0))]) < 0)
        self.assertEqual(certify_hermitian(matrix)['status'], 'inconclusive')

    def test_complex_precision_replay(self):
        first = WeilCells(2, 4, 60).matrix(3000000000001)
        second = WeilCells(2, 4, 100).matrix(3000000000001)
        for i in range(4):
            for j in range(4):
                self.assertTrue(first[i][j].overlaps(second[i][j]))


if __name__ == '__main__':
    unittest.main()
