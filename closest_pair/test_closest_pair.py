# extra correctness tests, run with: python -m unittest -v test_closest_pair

import math
import random
import unittest
from closest_pair import closest_pair, closest_pair_sq

def brute_sq(pts):
    return min((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
               for i, p in enumerate(pts) for q in pts[i + 1:])

class ClosestPairTests(unittest.TestCase):

    def check(self, pts):
        d2, p, q = closest_pair_sq(pts)
        self.assertEqual(d2, brute_sq(pts))
        self.assertEqual((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2, d2)
        self.assertIn(p, pts)
        self.assertIn(q, pts)
        return d2

    def test_too_few_points(self):
        with self.assertRaises(ValueError):
            closest_pair([])
        with self.assertRaises(ValueError):
            closest_pair([(1, 2)])

    def test_two_and_three_points(self):
        self.assertEqual(closest_pair_sq([(0, 0), (3, 4)])[0], 25)
        self.assertEqual(closest_pair([(0, 0), (3, 4)])[0], 5.0)
        self.check([(0, 0), (10, 0), (4, 3)])

    def test_duplicates(self):
        self.assertEqual(self.check([(5, 5), (1, 1), (5, 5), (9, 0)]), 0)
        self.assertEqual(self.check([(2, 2)] * 10), 0)

    def test_all_on_vertical_line(self):
        rng = random.Random(1)
        for _ in range(50):
            pts = [(7, rng.randint(-10_000, 10_000)) for _ in range(rng.randint(2, 300))]
            self.check(pts)

    def test_all_on_horizontal_line(self):
        rng = random.Random(2)
        for _ in range(50):
            pts = [(rng.randint(-10_000, 10_000), -3) for _ in range(rng.randint(2, 300))]
            self.check(pts)

    def test_pair_straddles_the_split(self):
        pts = [(x * 10, 0) for x in range(10)] + [(45, 1), (46, 1)]
        pts += [(x * 10, 100) for x in range(10)]
        self.assertEqual(self.check(pts), 1)
        pts = [(0, 0), (100, 0), (49, 50), (51, 50), (0, 100), (100, 100)]
        self.assertEqual(self.check(pts), 4)

    def test_square_grid(self):
        pts = [(x, y) for x in range(30) for y in range(30)]
        random.Random(3).shuffle(pts)
        self.assertEqual(self.check(pts), 1)

    def test_floats(self):
        rng = random.Random(4)
        for _ in range(100):
            pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(rng.randint(2, 200))]
            d2, _, _ = closest_pair_sq(pts)
            self.assertTrue(math.isclose(d2, brute_sq(pts), rel_tol=1e-12, abs_tol=0))

    def test_random_small(self):
        rng = random.Random(5)
        for _ in range(1000):
            n = rng.randint(2, 80)
            r = rng.choice((3, 50, 10**6))
            pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
            self.check(pts)

    def test_clustered(self):
        rng = random.Random(6)
        centers = [(rng.uniform(0, 1e6), rng.uniform(0, 1e6)) for _ in range(5)]
        pts = []
        for _ in range(1500):
            cx, cy = rng.choice(centers)
            pts.append((round(rng.gauss(cx, 1000)), round(rng.gauss(cy, 1000))))
        self.check(pts)

    def test_input_not_modified(self):
        pts = [(3, 1), (0, 0), (2, 2), (1, 5)]
        before = list(pts)
        closest_pair(pts)
        self.assertEqual(pts, before)

if __name__ == "__main__":
    unittest.main()