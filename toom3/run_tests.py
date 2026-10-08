# runs toom3 on every case in tests/, checks the product and times it
# usage: python run_tests.py [--quick] [--repeat N]

import argparse
import csv
import gc
import glob
import os
import sys
import time
from toom3 import toom3

HERE = os.path.dirname(os.path.abspath(__file__))

def load_case(path):
    fields = {}
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, val = line.split(maxsplit=1)
            fields[key] = val.strip()
    return (int(fields["bits"]), int(fields["a"], 16), int(fields["b"], 16),
            int(fields["product"], 16))

# min over runs like timeit, small cases repeat until ~1s total
def best_time(fn, repeat, min_total=1.0):
    times = []
    result = None
    gc.collect()
    gc.disable()
    try:
        while len(times) < repeat or (sum(times) < min_total and len(times) < 10_000):
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
    print(f"{'case':<8}{'bits':>10}{'time (s)':>14}{'runs':>7}   result")
    for path in cases:
        name = os.path.basename(path)[:-4]
        bits, a, b, expected = load_case(path)
        t, runs, got = best_time(lambda: toom3(a, b), args.repeat)
        ok = got == expected
        failed += not ok
        print(f"{name:<8}{bits:>10}{t:>14.6f}{runs:>7}   {'PASS' if ok else 'FAIL'}")
        rows.append({"case": name, "n": bits, "seconds": t, "runs": runs,
                     "passed": ok})

    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"\n{len(rows) - failed}/{len(rows)} passed, timings in results.csv")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()