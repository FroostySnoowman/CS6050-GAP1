# Closest pair of points

`closest_pair.py` is the O(n log n) divide-and-conquer algorithm (Shamos &
Hoey 1975; Preparata & Shamos 1985; CLRS 33.4). It works as follows:

1. Sort the points by x once.
2. Split at the median, recurse on each half, and let d be the smaller of
   the two answers.
3. Check only the pairs inside the vertical strip of width 2d around the
   split line.

Each recursive call returns its points merged by y, the same way merge sort
does. That way the strip never needs re-sorting and every level is O(n),
which gives T(n) = 2T(n/2) + O(n) = O(n log n) rather than O(n log² n).

* `closest_pair(points)` returns `(distance, p, q)`.
* `closest_pair_sq(points)` returns the exact squared distance instead.
  This is what the tests use, since inputs are integers.

## Run the 10 test cases

```
python run_tests.py            # all 10, about 20 s
python run_tests.py --quick    # skip the 2 largest
```

A case passes if the returned squared distance equals the expected one and
the two returned points are input points that really are that far apart.
Ties are possible, so the pair itself isn't compared. Reading the file is
not timed; the initial sort is, because it's part of the algorithm. Timings
go to `results.csv`.

## Test cases

`tests/caseNN.txt` holds n = 2^(NN+9) points, so 1,024 for case 1 up to
524,288 for case 10. Coordinates are uniform random integers in
[0, 2^24) × [0, 2^24). Each file has this format:

```
n <count>
expected_dist_sq <value>
x y
x y
...
```

The expected value comes from scipy's k-d tree (`cKDTree`), which is
independent of this implementation. Regenerating the files needs numpy and
scipy:

```
python generate_tests.py
```

## Unit tests

```
python -m unittest -v test_closest_pair
```

These cover 2 and 3 points, duplicate points, all points on one vertical
line (every point lands in the strip at every level), all points on one
horizontal line, a pair straddling the split, a square grid with many ties,
float coordinates, clustered points, and 1000 random small inputs compared
against brute force.
