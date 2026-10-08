# runs closest_pair_sq on every case in tests/, checks the answer and times it
# usage: python run_tests.py [--quick] [--repeat N]

import argparse
import csv
import gc
import glob
import os
import sys
import time
from closest_pair import closest_pair_sq

HERE = os.path.dirname(os.path.abspath(__file__))

def load_case(path):
    header = {}
    pts = []
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            a, b = line.split()
            if a[0].isalpha():
                header[a] = int(b)
            else:
                pts.append((int(a), int(b)))
    assert len(pts) == header["n"], f"{path}: expected {header['n']} points"
    return pts, header["expected_dist_sq"]

def best_time(fn, repeat, min_total=1.0):
    times = []
    result = None
    gc.collect()
    gc.disable()
    try:
        while len(times) < repeat or (sum(times) < min_total and len(times) < 1000):
            t0 = time.perf_counter()
            result = fn()
            times.append(time.perf_counter() - t0)
    finally:
        gc.enable()
    return min(times), len(times), result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--quick", action="store_true", help="skip cases 9 and 10")
    args = ap.parse_args()

    cases = sorted(glob.glob(os.path.join(HERE, "tests", "case*.txt")))
    if not cases:
        sys.exit("no test cases found, run generate_tests.py first")
    if args.quick:
        cases = cases[:8]

    rows = []
    failed = 0
    print(f"{'case':<8}{'n':>9}{'time (s)':>12}{'runs':>6}   result")
    for path in cases:
        name = os.path.basename(path)[:-4]
        pts, expected = load_case(path)
        t, runs, (d2, p, q) = best_time(lambda: closest_pair_sq(pts), args.repeat)

        # ties are possible so only check the distance and that p, q are real
        point_set = set(pts)
        real = (p in point_set and q in point_set
                and (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 == d2)
        if p == q:
            real = real and pts.count(p) >= 2
        ok = d2 == expected and real
        failed += not ok
        print(f"{name:<8}{len(pts):>9}{t:>12.4f}{runs:>6}   "
              f"{'PASS' if ok else 'FAIL'} (dist^2 {d2}, expected {expected})")
        rows.append({"case": name, "n": len(pts), "seconds": t, "runs": runs,
                     "passed": ok})

    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(rows) - failed}/{len(rows)} passed, timings in results.csv")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()