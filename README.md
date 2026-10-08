# CS 6050 Graduate Algorithm Project

Three divide-and-conquer algorithms, each implemented in Python, tested on 10
inputs of increasing size, and timed to check the runtime against the
theoretical bound.

| folder | algorithm | source | expected runtime |
|---|---|---|---|
| [`toom3/`](toom3/) | Toom-3 (Toom-Cook 3-way) integer multiplication | Toom 1963, Cook 1966; interpolation from Bodrato 2007 | O(n^log₃5) ≈ O(n^1.465) |
| [`hirschberg/`](hirschberg/) | Hirschberg's linear-space LCS | Hirschberg, CACM 18(6), 1975 | O(mn) time, O(m+n) space |
| [`closest_pair/`](closest_pair/) | Closest pair of points in the plane | Shamos & Hoey 1975; CLRS 33.4 | O(n log n) |

The write-up is [`writeup/writeup.pdf`](writeup/writeup.pdf).

## Requirements

* Python 3.8 or newer. The algorithms, test cases and test runners use only
  the standard library.
* `numpy`, `matplotlib` and `scipy` are needed only to remake the plots
  (`make_plots.py`) and to regenerate the closest-pair test files.

```
pip install -r requirements.txt
```

## Running the test cases

Each folder works on its own. From the folder, run the 10 test cases:

```
cd toom3          && python run_tests.py && cd ..
cd hirschberg     && python run_tests.py && cd ..
cd closest_pair   && python run_tests.py && cd ..
```

Each runner prints PASS/FAIL and the runtime for every case and saves the
timings to `results.csv` in that folder. Every case runs at least 3 times and
the fastest time is kept. On an M1 Max the slowest single runs take about
5 s (Toom-3), 13 s (Hirschberg) and 3 s (closest pair). With repeats a full
run takes about 25 s, 75 s and 20 s. Pass `--quick` to skip the two largest
cases.

The extra edge-case tests are separate from the timed cases:

```
cd toom3 && python -m unittest -v test_toom3
cd hirschberg && python -m unittest -v test_hirschberg
cd closest_pair && python -m unittest -v test_closest_pair
```

## Remaking the plots

After the three `run_tests.py` runs (plus `python run_tests.py --memory` in
`hirschberg/` for the memory panel), run:

```
python make_plots.py
```

This writes `writeup/figures/{toom3,hirschberg,closest_pair}.{svg,png}`.

## Regenerating the test cases

The test files in each `tests/` folder were made by that folder's
`generate_tests.py` with fixed seeds, so re-running it produces identical
files. The expected answers come from code that shares nothing with the
implementation being tested:

* Toom-3: Python's built-in `*`.
* Hirschberg: a bit-parallel LCS length algorithm, cross-checked against
  the plain DP.
* Closest pair: scipy's k-d tree.

## Layout

```
toom3/  hirschberg/  closest_pair/
    <algorithm>.py       implementation
    generate_tests.py    makes tests/case01..case10.txt
    run_tests.py         checks + times the 10 cases -> results.csv
    test_<algorithm>.py  unit tests (edge cases, randomized checks)
    tests/               the 10 test case files
    README.md
make_plots.py            figures for the write-up
writeup/                 writeup.pdf and the figures
```