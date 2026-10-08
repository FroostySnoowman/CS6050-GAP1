# makes tests/case01.txt .. case10.txt
# case i = two random 3^(i+3)-bit numbers, expected product from python's *
# numbers are stored in hex since python won't print ints over 4300 digits

import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tests")


def random_nbit(rng, n):
    return rng.getrandbits(n) | (1 << (n - 1))


def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(1, 11):
        bits = 3 ** (i + 3)
        rng = random.Random(1000 + i)
        a = random_nbit(rng, bits)
        b = random_nbit(rng, bits)
        path = os.path.join(OUT, f"case{i:02d}.txt")
        with open(path, "w") as f:
            f.write(f"# toom3 case {i}: two random {bits}-bit operands, seed {1000 + i}\n")
            f.write(f"bits {bits}\n")
            f.write(f"a {a:x}\n")
            f.write(f"b {b:x}\n")
            f.write(f"product {a * b:x}\n")
        print(f"wrote {os.path.relpath(path, HERE)}  ({bits} bits)")


if __name__ == "__main__":
    main()
