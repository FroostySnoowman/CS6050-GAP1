# extra correctness tests, run with: python -m unittest -v test_toom3

import random
import unittest
from toom3 import toom3, MIN_CUTOFF

class Toom3Tests(unittest.TestCase):

    def test_small_values(self):
        for x in range(-40, 41):
            for y in range(-40, 41):
                self.assertEqual(toom3(x, y, cutoff=MIN_CUTOFF), x * y)

    def test_zero_and_one(self):
        big = random.Random(1).getrandbits(5000)
        self.assertEqual(toom3(0, big), 0)
        self.assertEqual(toom3(big, 0), 0)
        self.assertEqual(toom3(1, big), big)
        self.assertEqual(toom3(-1, big), -big)

    def test_signs(self):
        rng = random.Random(2)
        a, b = rng.getrandbits(3000), rng.getrandbits(2000)
        for sa in (1, -1):
            for sb in (1, -1):
                self.assertEqual(toom3(sa * a, sb * b), sa * a * sb * b)

    def test_powers_of_two_and_all_ones(self):
        for n in (65, 100, 192, 193, 1000, 3**7):
            ones = (1 << n) - 1
            self.assertEqual(toom3(ones, ones), ones * ones)
            self.assertEqual(toom3(1 << n, ones), (1 << n) * ones)

    def test_unbalanced_operands(self):
        rng = random.Random(3)
        for _ in range(50):
            a = rng.getrandbits(rng.randint(1, 50))
            b = rng.getrandbits(rng.randint(2000, 6000))
            self.assertEqual(toom3(a, b), a * b)
            self.assertEqual(toom3(b, a), a * b)

    def test_random_many_cutoffs(self):
        rng = random.Random(4)
        for _ in range(2000):
            a = rng.getrandbits(rng.randint(0, 4000)) * rng.choice((1, -1))
            b = rng.getrandbits(rng.randint(0, 4000)) * rng.choice((1, -1))
            c = rng.choice((MIN_CUTOFF, 9, 16, 31, 64, 200))
            self.assertEqual(toom3(a, b, cutoff=c), a * b)

    def test_large(self):
        rng = random.Random(5)
        a, b = rng.getrandbits(200_000), rng.getrandbits(200_000)
        self.assertEqual(toom3(a, b), a * b)

    def test_cutoff_too_small(self):
        with self.assertRaises(ValueError):
            toom3(12345, 6789, cutoff=MIN_CUTOFF - 1)

if __name__ == "__main__":
    unittest.main()