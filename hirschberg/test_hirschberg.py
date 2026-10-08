# extra correctness tests, run with: python -m unittest -v test_hirschberg

import random
import unittest
from hirschberg import hirschberg, lcs_lengths, lcs_table, is_subsequence
from generate_tests import lcs_length_bitparallel

class HirschbergTests(unittest.TestCase):

    def check(self, a, b, expected_len=None):
        z = hirschberg(a, b)
        self.assertTrue(is_subsequence(z, a), (a, b, z))
        self.assertTrue(is_subsequence(z, b), (a, b, z))
        if expected_len is None:
            expected_len = len(lcs_table(a, b))
        self.assertEqual(len(z), expected_len, (a, b, z))
        return z

    def test_empty(self):
        self.assertEqual(hirschberg("", ""), "")
        self.assertEqual(hirschberg("", "ABC"), "")
        self.assertEqual(hirschberg("ABC", ""), "")

    def test_single_characters(self):
        self.assertEqual(hirschberg("A", "A"), "A")
        self.assertEqual(hirschberg("A", "B"), "")
        self.assertEqual(hirschberg("A", "XYZA"), "A")
        self.assertEqual(hirschberg("XYZA", "A"), "A")

    def test_textbook_examples(self):
        self.check("ABCBDAB", "BDCABA", 4)
        self.check("ACCGGTCGAGTGCGCGGAAGCCGGCCGAA", "GTCGTTCGGAATGCCGTTGCTCTGTAAA", 20)

    def test_identical_and_disjoint(self):
        s = "the quick brown fox"
        self.assertEqual(hirschberg(s, s), s)
        self.assertEqual(hirschberg("aaaa", "bbbb"), "")

    def test_one_is_subsequence_of_other(self):
        self.assertEqual(hirschberg("ace", "abcde"), "ace")
        self.assertEqual(hirschberg("abcde", "ace"), "ace")

    def test_repeated_characters(self):
        self.check("a" * 50, "a" * 30, 30)
        self.check("ab" * 40, "ba" * 40, 79)

    def test_lcs_lengths_row(self):
        rng = random.Random(1)
        for _ in range(200):
            a = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 30)))
            b = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 30)))
            row = lcs_lengths(a, b)
            for j in range(len(b) + 1):
                self.assertEqual(row[j], len(lcs_table(a, b[:j])))

    def test_random_against_full_table(self):
        rng = random.Random(2)
        for _ in range(1500):
            alphabet = rng.choice(("AB", "ACGT", "abcdefghijklmnopqrstuvwxyz"))
            a = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
            b = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 60)))
            self.check(a, b)

    def test_bitparallel_oracle(self):
        rng = random.Random(3)
        for _ in range(1500):
            a = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 60)))
            b = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 60)))
            self.assertEqual(lcs_length_bitparallel(a, b), len(lcs_table(a, b)))

    def test_medium_random(self):
        rng = random.Random(4)
        a = "".join(rng.choice("ACGT") for _ in range(1500))
        b = "".join(rng.choice("ACGT") for _ in range(900))
        self.check(a, b, lcs_length_bitparallel(a, b))

if __name__ == "__main__":
    unittest.main()