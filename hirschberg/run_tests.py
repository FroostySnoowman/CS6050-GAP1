# runs hirschberg on every case in tests/, checks the answer and times it
# usage: python run_tests.py [--quick] [--repeat N] [--memory]
# --memory also records peak memory vs the full table DP (memory.csv)

import argparse
import csv
import gc
import glob
import os
import sys
import time
import tracemalloc
from hirschberg import hirschberg, lcs_table, is_subsequence

HERE = os.path.dirname(os.path.abspath(__file__))

MEMORY_CELL_LIMIT = 17_000_000  # full table is ~250MB here

def load_case(path):
    fields = {}
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            key, _, val = line.rstrip("\n").partition(" ")
            fields[key] = val
    return fields["A"], fields["B"], int(fields["lcs_length"])

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

def peak_memory(fn):
    gc.collect()
    tracemalloc.start()
    fn()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--quick", action="store_true", help="skip cases 9 and 10")
    ap.add_argument("--memory", action="store_true")
    args = ap.parse_args()

    cases = sorted(glob.glob(os.path.join(HERE, "tests", "case*.txt")))
    if not cases:
        sys.exit("no test cases found, run generate_tests.py first")
    if args.quick:
        cases = cases[:8]

    rows = []
    mem_rows = []
    failed = 0
    print(f"{'case':<8}{'m':>7}{'n':>7}{'m*n':>12}{'time (s)':>12}{'runs':>6}   result")
    for path in cases:
        name = os.path.basename(path)[:-4]
        a, b, expected = load_case(path)
        t, runs, z = best_time(lambda: hirschberg(a, b), args.repeat)
        # LCS isn't unique, so check length + that it's a common subsequence
        ok = len(z) == expected and is_subsequence(z, a) and is_subsequence(z, b)
        failed += not ok
        m, n = len(a), len(b)
        print(f"{name:<8}{m:>7}{n:>7}{m * n:>12}{t:>12.4f}{runs:>6}   "
              f"{'PASS' if ok else 'FAIL'} (LCS {len(z)}, expected {expected})")
        rows.append({"case": name, "m": m, "n": n, "cells": m * n,
                     "seconds": t, "runs": runs, "passed": ok})

    # separate pass, doing it between timings slowed the later cases down
    if args.memory:
        print("\npeak memory (tracemalloc):")
        for path in cases:
            name = os.path.basename(path)[:-4]
            a, b, _ = load_case(path)
            m, n = len(a), len(b)
            if m * n > MEMORY_CELL_LIMIT:
                continue
            hb = peak_memory(lambda: hirschberg(a, b))
            full = peak_memory(lambda: lcs_table(a, b))
            print(f"{name:<8}hirschberg {hb / 1e6:7.2f} MB   "
                  f"full table {full / 1e6:7.1f} MB")
            mem_rows.append({"case": name, "m": m, "n": n, "cells": m * n,
                             "hirschberg_bytes": hb, "full_table_bytes": full})

    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    if mem_rows:
        with open(os.path.join(HERE, "memory.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=mem_rows[0].keys())
            w.writeheader()
            w.writerows(mem_rows)

    print(f"\n{len(rows) - failed}/{len(rows)} passed, timings in results.csv")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()