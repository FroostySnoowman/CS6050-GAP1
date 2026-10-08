# Hirschberg's linear space LCS
# Hirschberg, "A linear space algorithm for computing maximal common
# subsequences", CACM 1975. lcs_lengths = ALG B, hirschberg = ALG C,
# lcs_table = ALG A (only used for testing)

def lcs_lengths(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0]
        left = 0
        for bj, diag, up in zip(b, prev, prev[1:]):
            if ch == bj:
                left = diag + 1
            elif up > left:
                left = up
            cur.append(left)
        prev = cur
    return prev

def hirschberg(a, b):
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return ""
    if m == 1:
        return a if a in b else ""

    i = m // 2
    l1 = lcs_lengths(a[:i], b)
    l2 = lcs_lengths(a[i:][::-1], b[::-1])

    best, k = -1, 0
    for j in range(n + 1):
        s = l1[j] + l2[n - j]
        if s > best:
            best, k = s, j

    return hirschberg(a[:i], b[:k]) + hirschberg(a[i:], b[k:])

def lcs_table(a, b):
    m, n = len(a), len(b)
    t = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        ai = a[i - 1]
        row, above = t[i], t[i - 1]
        for j in range(1, n + 1):
            if ai == b[j - 1]:
                row[j] = above[j - 1] + 1
            else:
                row[j] = max(above[j], row[j - 1])
    out = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))

def is_subsequence(s, t):
    it = iter(t)
    return all(ch in it for ch in s)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        x, y = sys.argv[1], sys.argv[2]
    else:
        x, y = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA", "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    z = hirschberg(x, y)
    print(f"LCS length {len(z)}: {z}")