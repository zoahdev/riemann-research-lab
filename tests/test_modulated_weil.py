from fractions import Fraction as Q
import unittest
import mpmath as mp
from flint import arb
from experiments.modulated_weil import ModulatedWeil
from experiments.weil_kernel import ArithmeticScrew, prime_powers


def direct_integral(length, frequency):
    """Independent ordinary-integral regression, not an interval proof."""
    with mp.workdps(110):
        l = mp.mpf(length.numerator)/length.denominator
        t = mp.mpf(frequency.numerator)/frequency.denominator
        pole = 2*mp.quad(lambda x: (l-x)*mp.cos(t*x)*(mp.exp(x/2)+mp.exp(-x/2)), [0, l])
        def integrand(x):
            if not x:
                return l/4-mp.mpf('0.5')
            diff = -2*l*mp.sin(t*x/2)**2-x*mp.cos(t*x)-l*mp.expm1(-x/2)
            return diff*mp.exp(-x/2)/(-mp.expm1(-2*x))
        arch = -2*mp.quad(integrand, [0, l])+2*l*mp.atanh(mp.exp(-l))
        prime = sum((mp.log(p)/mp.sqrt(n)*(l-mp.log(n))*mp.cos(t*mp.log(n))
                     for n, p in prime_powers(int(mp.exp(l))+1) if mp.log(n)<l), mp.mpf(0))
        value = pole-2*prime-l*(mp.log(4*mp.pi)+mp.euler)+arch
        return mp.nstr(value, 105)


class ModulatedCertificates(unittest.TestCase):
    def test_zero_frequency_matches_screw_difference(self):
        for length in (Q(1, 2), Q(1), Q(4)):
            kernel = ArithmeticScrew(length, 80)
            expected = -2*kernel.g(length)
            actual = ModulatedWeil(length, 80).value(0)
            self.assertTrue(actual.overlaps(expected))

    def test_independent_regularized_integral(self):
        for length, frequency in ((Q(6, 5), Q(3, 4)), (Q(2), Q(5)), (Q(2), Q(20))):
            actual = ModulatedWeil(length, 80).value(frequency)
            numerical = arb(direct_integral(length, frequency), '1e-90')
            self.assertTrue(actual.overlaps(numerical))

    def test_high_frequency_precision_replay(self):
        t = Q(3000000000001)
        first = ModulatedWeil(8, 60).value(t)
        second = ModulatedWeil(8, 100).value(t)
        self.assertTrue(first.overlaps(second))
        self.assertTrue(second > 0)


if __name__ == '__main__':
    unittest.main()
