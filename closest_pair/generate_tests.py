# makes tests/case01.txt .. case10.txt
# case i = 2^(i+9) random integer points in [0, 2^24)^2
# expected answer comes from scipy's kd-tree (needs numpy + scipy)

import os
import random
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tests")
COORD_RANGE = 1 << 24

def closest_sq_kdtree(points):
    arr = np.array(points, dtype=np.int64)
    dist, idx = cKDTree(arr).query(arr, k=2)
    nn = dist[:, 1]
    # kd-tree distances are floats, recheck the near-minimum ones with ints
    cand = np.nonzero(nn <= nn.min() * (1 + 1e-9) + 1e-9)[0]
    best = None
    for i in cand:
        j = idx[i, 1]
        d2 = int(((arr[i] - arr[j]) ** 2).sum())
        if best is None or d2 < best:
            best = d2
    return best

def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(1, 11):
        n = 2 ** (i + 9)
        rng = random.Random(3000 + i)
        pts = [(rng.randrange(COORD_RANGE), rng.randrange(COORD_RANGE))
               for _ in range(n)]
        expected = closest_sq_kdtree(pts)
        path = os.path.join(OUT, f"case{i:02d}.txt")
        with open(path, "w") as f:
            f.write(f"# closest pair case {i}: {n} uniform random points in "
                    f"[0, 2^24)^2, seed {3000 + i}\n")
            f.write(f"n {n}\n")
            f.write(f"expected_dist_sq {expected}\n")
            f.writelines(f"{x} {y}\n" for x, y in pts)
        print(f"wrote {os.path.relpath(path, HERE)}  ({n} points, "
              f"closest squared distance {expected})")

if __name__ == "__main__":
    main()