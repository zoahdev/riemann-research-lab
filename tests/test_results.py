from fractions import Fraction as Q
import unittest

from experiments.check_triple_profile import run


class ExactResults(unittest.TestCase):
    def test_equicorrelation_family_exact(self):
        for denominator in range(1, 101):
            for numerator in range(denominator + 1):
                r = Q(numerator, denominator)
                eigenvalues = (1+2*r, 1-r, 1-r)
                self.assertEqual(sum(eigenvalues), 3)
                self.assertTrue(all(x >= 0 for x in eigenvalues))
                defect = sum((x-1)**2 if x <= 2 else 2*x-3 for x in eigenvalues)
                e = 3*r*r
                exact_profile = 2*e - max(Q(0), 2*r-1)**2
                self.assertEqual(defect, exact_profile)
                self.assertGreaterEqual(defect, Q(5, 3)*e)

    def test_uniform_coefficient_sharp(self):
        self.assertEqual(Q(5)/3, Q(5, 3))  # B=all-ones: defect=5, energy=3
        self.assertLess(Q(5), Q(167, 100)*3)  # a larger candidate fails

    def test_variance_decomposition(self):
        for i in range(31):
            for j in range(31-i):
                eig = sorted((Q(i, 10), Q(j, 10), Q(30-i-j, 10)), reverse=True)
                t, a, b = eig
                v = sum((x-1)**2 for x in eig)
                self.assertEqual(v-Q(3, 2)*(t-1)**2, (a-b)**2/2)
                defect = sum((x-1)**2 if x <= 2 else 2*x-3 for x in eig)
                self.assertEqual(defect, v-max(Q(0), t-2)**2)
                self.assertGreaterEqual(defect, Q(5, 6)*v)

    def test_saturation_all_rational_ratios(self):
        for v in range(1, 101):
            for u in range(v, 2*v+1):
                a, b = 2*(2*v-u), u-v
                n, energy, distinct = a+2*b, a+4*b, a+b
                self.assertEqual(Q(energy, n), Q(u, v))
                self.assertEqual(a, 2*n-energy)
                self.assertEqual(2*distinct, 3*n-energy)

    def test_seeded_complex_and_block_regression(self):
        self.assertEqual(run(1000, 20261004)["status"], "passed")


if __name__ == "__main__":
    unittest.main()
