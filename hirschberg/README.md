# Hirschberg's linear-space LCS

`hirschberg.py` is a Python translation of the procedures in
D. S. Hirschberg, "A linear space algorithm for computing maximal common
subsequences", CACM 18(6), 1975:

* `lcs_lengths(a, b)` is ALG B. It returns the last row of the LCS-length
  table while keeping only two rows in memory.
* `hirschberg(a, b)` is ALG C. It splits `a` in half, runs ALG B forward on
  the first half and backward on the second, picks the column `k` where the
  two halves meet on an optimal path, and recurses on both pieces.
* `lcs_table(a, b)` is ALG A, the ordinary full-table DP. It is only used by
  the tests and the memory comparison.

The algorithm takes O(mn) time and O(m+n) space.

## Run the 10 test cases

```
python run_tests.py              # all 10, about 75 s
python run_tests.py --quick      # skip the 2 largest
python run_tests.py --memory     # also record peak memory vs. the full
                                 # table (cases up to ~17M cells)
```

An answer passes if it is a subsequence of both strings and its length
equals the expected LCS length in the file. The LCS itself usually isn't
unique, so the strings aren't compared directly. Timings go to
`results.csv`, and memory figures to `memory.csv` when `--memory` is used.

## Test cases

`tests/caseNN.txt` contains DNA strings A and B. The product m·n doubles from
case to case, from 512×512 up to 16384×8192, and the shapes vary (A longer,
B longer, square). Cases 3, 5, 7 and 9 use B = A with ~10% random mutations,
to mimic aligning two similar sequences. The other cases are two independent
random strings. Each file has these lines:

```
A <string>
B <string>
lcs_length <expected length>
```

The expected length comes from a bit-parallel LCS algorithm (Allison & Dix
1986 / Hyyrö 2004), which is independent of the code being tested. For
cases up to 2.5M cells, `generate_tests.py` also checks it against the plain
DP. To regenerate the files:

```
python generate_tests.py
```

## Unit tests

```
python -m unittest -v test_hirschberg
```

These cover empty strings, single characters, the CLRS examples, identical
and disjoint strings, repeated characters, ALG B's row against the full
table, 1500 random pairs against ALG A, and a check of the bit-parallel
oracle itself.