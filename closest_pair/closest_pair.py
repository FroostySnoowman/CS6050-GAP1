# Closest pair of points, divide and conquer (CLRS 33.4)
# uses squared distances so integer inputs stay exact

from math import sqrt

def _brute(pts):
    best = (float("inf"), None, None)
    for i in range(len(pts)):
        px, py = pts[i]
        for j in range(i + 1, len(pts)):
            qx, qy = pts[j]
            d = (px - qx) ** 2 + (py - qy) ** 2
            if d < best[0]:
                best = (d, pts[i], pts[j])
    return best

def _merge_by_y(left, right):
    out = []
    i = j = 0
    nl, nr = len(left), len(right)
    while i < nl and j < nr:
        if left[i][1] <= right[j][1]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    if i < nl:
        out.extend(left[i:])
    else:
        out.extend(right[j:])
    return out

# returns (best, points sorted by y) so the parent can merge instead of sorting
def _closest(px, lo, hi):
    n = hi - lo
    if n <= 3:
        pts = px[lo:hi]
        return _brute(pts), sorted(pts, key=lambda p: p[1])

    mid = (lo + hi) // 2
    mid_x = px[mid][0]
    best_l, ys_l = _closest(px, lo, mid)
    best_r, ys_r = _closest(px, mid, hi)
    best = best_l if best_l[0] <= best_r[0] else best_r
    ys = _merge_by_y(ys_l, ys_r)

    d2 = best[0]
    strip = [p for p in ys if (p[0] - mid_x) ** 2 < d2]

    for i in range(len(strip)):
        px_, py_ = strip[i]
        for j in range(i + 1, len(strip)):
            qx, qy = strip[j]
            dy = qy - py_
            if dy * dy >= d2:
                break
            d = (px_ - qx) ** 2 + dy * dy
            if d < d2:
                d2 = d
                best = (d, strip[i], strip[j])

    return best, ys

def closest_pair_sq(points):
    pts = [tuple(p) for p in points]
    if len(pts) < 2:
        raise ValueError("need at least two points")
    pts.sort()
    (d2, p, q), _ = _closest(pts, 0, len(pts))
    return d2, p, q

def closest_pair(points):
    d2, p, q = closest_pair_sq(points)
    return sqrt(d2), p, q

if __name__ == "__main__":
    import random
    rng = random.Random(0)
    pts = [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(1000)]
    d, p, q = closest_pair(pts)
    print(f"closest pair {p} {q}  distance {d:.4f}")