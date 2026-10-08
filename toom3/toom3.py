# Toom-3 multiplication
# Interpolation sequence from Bodrato (2007), see the Wikipedia page for Toom-Cook

CUTOFF_BITS = 64  # stay under CPython's karatsuba cutoff (2100 bits)
MIN_CUTOFF = 8    # smaller than ~6 bits and the pieces don't shrink

def toom3(x, y, cutoff=CUTOFF_BITS):
    if cutoff < MIN_CUTOFF:
        raise ValueError(f"cutoff must be at least {MIN_CUTOFF} bits")
    
    if x < 0 or y < 0:
        neg = (x < 0) != (y < 0)
        r = toom3(abs(x), abs(y), cutoff)
        return -r if neg else r

    n = max(x.bit_length(), y.bit_length())
    if n <= cutoff:
        return x * y

    k = (n + 2) // 3
    mask = (1 << k) - 1

    x0, x1, x2 = x & mask, (x >> k) & mask, x >> (2 * k)
    y0, y1, y2 = y & mask, (y >> k) & mask, y >> (2 * k)

    # evaluate at 0, 1, -1, -2, inf
    t = x0 + x2
    p1 = t + x1
    pm1 = t - x1
    pm2 = ((pm1 + x2) << 1) - x0

    t = y0 + y2
    q1 = t + y1
    qm1 = t - y1
    qm2 = ((qm1 + y2) << 1) - y0

    r0 = toom3(x0, y0, cutoff)
    r1 = toom3(p1, q1, cutoff)
    rm1 = toom3(pm1, qm1, cutoff)
    rm2 = toom3(pm2, qm2, cutoff)
    rinf = toom3(x2, y2, cutoff)

    # interpolate (divisions are exact)
    c0 = r0
    c4 = rinf
    c3 = (rm2 - r1) // 3
    c1 = (r1 - rm1) >> 1
    c2 = rm1 - r0
    c3 = ((c2 - c3) >> 1) + (rinf << 1)
    c2 = c2 + c1 - c4
    c1 = c1 - c3

    return c0 + (c1 << k) + (c2 << (2 * k)) + (c3 << (3 * k)) + (c4 << (4 * k))

if __name__ == "__main__":
    import random
    import sys

    nbits = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    a = random.getrandbits(nbits)
    b = random.getrandbits(nbits)
    assert toom3(a, b) == a * b
    print(f"ok: {nbits}-bit operands, product has {(a * b).bit_length()} bits")