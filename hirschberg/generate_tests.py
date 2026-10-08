# makes tests/case01.txt .. case10.txt
# m*n doubles each case. "related" cases are B = A with ~10% mutations.
# expected LCS length comes from the bit-parallel LCS algorithm (Hyyro 2004)

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tests")

CASES = [
    (512, 512, "random"),
    (1024, 512, "random"),
    (1024, 1024, "related"),
    (1024, 2048, "random"),
    (2048, 2048, "related"),
    (4096, 2048, "random"),
    (4096, 4096, "related"),
    (4096, 8192, "random"),
    (8192, 8192, "related"),
    (16384, 8192, "random"),
]

DNA = "ACGT"

def random_dna(rng, n):
    return "".join(rng.choice(DNA) for _ in range(n))

def mutate(rng, s, rate=0.10):
    out = []
    for ch in s:
        r = rng.random()
        if r < rate / 3:
            continue
        elif r < 2 * rate / 3:
            out.append(rng.choice(DNA))
        elif r < rate:
            out.append(ch)
            out.append(rng.choice(DNA))
        else:
            out.append(ch)
    return "".join(out)

def lcs_length_bitparallel(a, b):
    m = len(a)
    if m == 0:
        return 0
    match = {}
    for i, ch in enumerate(a):
        match[ch] = match.get(ch, 0) | (1 << i)
    full = (1 << m) - 1
    v = full
    for ch in b:
        u = v & match.get(ch, 0)
        v = ((v + u) | (v - u)) & full
    return m - bin(v).count("1")

def lcs_length_dp(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if x == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def main():
    os.makedirs(OUT, exist_ok=True)
    for i, (m, n, kind) in enumerate(CASES, start=1):
        rng = random.Random(2000 + i)
        a = random_dna(rng, m)
        b = random_dna(rng, n) if kind == "random" else mutate(rng, a)
        expected = lcs_length_bitparallel(a, b)
        if len(a) * len(b) <= 2_500_000:
            assert expected == lcs_length_dp(a, b), f"oracles disagree on case {i}"
        path = os.path.join(OUT, f"case{i:02d}.txt")
        with open(path, "w") as f:
            f.write(f"# hirschberg case {i}: {kind} DNA, seed {2000 + i}\n")
            f.write(f"A {a}\n")
            f.write(f"B {b}\n")
            f.write(f"lcs_length {expected}\n")
        print(f"wrote {os.path.relpath(path, HERE)}  ({len(a)} x {len(b)}, "
              f"{kind}, LCS = {expected})")

if __name__ == "__main__":
    main()