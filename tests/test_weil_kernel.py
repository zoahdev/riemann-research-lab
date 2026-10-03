from fractions import Fraction as Q
import unittest

from flint import arb, ctx
from experiments.weil_kernel import (
    ArithmeticScrew, certify_ldl, prime_powers, rayleigh, toy_offline_g,
)
from experiments.check_semigroup_obstruction import run as obstruction


class KernelCertificates(unittest.TestCase):
    def test_prime_powers_include_higher_powers_once(self):
        self.assertEqual(prime_powers(16), [(2, 2), (3, 3), (4, 2),
                         (5, 5), (7, 7), (8, 2), (9, 3), (11, 11),
                         (13, 13), (16, 2)])

    def test_special_constants_independent_identities(self):
        ctx.dps = 80
        evaluator = ArithmeticScrew(1)
        self.assertTrue(evaluator.psi_quarter.overlaps(
            -arb.const_euler()-arb.pi()/2-3*arb(2).log()))
        self.assertTrue(evaluator.zeta_quarter.overlaps(
            arb.pi()**2+8*arb.const_catalan()))

    def test_evenness_zero_and_precision_replay(self):
        low = ArithmeticScrew(2, 60)
        values = [low.g(t) for t in (Q(1, 100), Q(1, 2), Q(1), Q(2))]
        high = ArithmeticScrew(2, 100)
        self.assertEqual(high.g(0), 0)
        for t, value in zip((Q(1, 100), Q(1, 2), Q(1), Q(2)), values):
            self.assertTrue(value.overlaps(high.g(t)))
            self.assertIs(high.g(t), high.g(-t))  # same even cache key
        with self.assertRaises(ValueError):
            high.g(3)

    def test_factorization_and_negative_witness_are_distinct(self):
        ctx.dps = 80
        matrix = [[arb(2), arb(1)], [arb(1), arb(2)]]
        self.assertEqual(certify_ldl(matrix)['status'],
                         'finite_matrix_positive_definite')
        uncertain = [[arb(0, 1)]]
        self.assertEqual(certify_ldl(uncertain)['status'], 'inconclusive')
        # Indefinite matrix with positive diagonal: eigenvector witness is needed.
        negative = [[arb(1), arb(2)], [arb(2), arb(1)]]
        self.assertTrue(rayleigh(negative, [Q(1), Q(-1)]) < 0)
        self.assertEqual(certify_ldl(negative)['status'], 'inconclusive')

    def test_synthetic_offline_pair_is_detected(self):
        ctx.dps = 80
        self.assertTrue(-2*toy_offline_g(2*arb.pi()) < 0)

    def test_obstruction_supports_and_signs(self):
        result = obstruction(80)
        self.assertEqual(result['status'], 'constant_enclosures_verified')
        self.assertFalse(result['rh_counterexample'])


if __name__ == '__main__':
    unittest.main()
