# Toom-3 multiplication

`toom3.py` multiplies two integers by splitting each one into 3 pieces. It
evaluates the two resulting degree-2 polynomials at 0, 1, -1, -2 and
infinity, does 5 recursive multiplications and interpolates the product
back. The interpolation sequence is Bodrato's (WAIFI 2007, also on the
Wikipedia page). Below 64 bits it falls back to a builtin multiply of a few
machine words.

Recurrence: T(n) = 5T(n/3) + O(n), so T(n) = O(n^log₃5) ≈ O(n^1.465).

## Run the 10 test cases

```
python run_tests.py            # all 10, about 25 s
python run_tests.py --quick    # skip the 2 largest
```

Each case is checked against the product stored in its file and timed. The
fastest of at least 3 runs is kept. Small cases are repeated until about 1 s
of total time has gone by. Timings are written to `results.csv`.

## Test cases

`tests/caseNN.txt` holds two random operands of exactly 3^(NN+3) bits each,
so 81 bits for case 1 up to 1,594,323 bits for case 10. Each file has these
lines:

```
bits <n>
a <hex>
b <hex>
product <hex>
```

Numbers are stored in hex because Python limits int↔decimal-string
conversion to 4300 digits. To regenerate the files (same seeds, same
output):

```
python generate_tests.py
```

## Unit tests

```
python -m unittest -v test_toom3
```

These cover signs, zero, all-ones operands, very unbalanced operand sizes,
many different cutoffs, and 2000 random pairs compared against the builtin
`*`.

You can also try the module directly: `python toom3.py 100000` multiplies two
random 100000-bit numbers and checks the result.
