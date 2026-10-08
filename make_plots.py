# makes the runtime plots in writeup/figures from each results.csv
# usage: python make_plots.py [toom3|hirschberg|closest_pair]

import csv
import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "writeup", "figures")

MEASURED = "#2a78d6"
THEORY = "#eb6834"
OTHER = "#8a8984"
INK = "#1f1f1e"
INK2 = "#52514e"
GRID = "#e4e3df"

N_FIT = 5  # fit c on the largest 5 cases

LOG3_5 = math.log(5, 3)
LOG2_3 = math.log2(3)

ALGOS = {
    "toom3": {
        "title": "Toom-3 multiplication",
        "xcol": "n",
        "xlabel": "operand size n (bits)",
        "f": lambda n: n ** LOG3_5,
        "f_label": r"$c\cdot n^{\log_3 5}$  ($n^{1.465}$)",
        "f_short": r"$n^{\log_3 5}$",
        "others": [(lambda n: n ** LOG2_3, r"$n^{\log_2 3}$ (Karatsuba)"),
                   (lambda n: n ** 2, r"$n^2$ (schoolbook)")],
    },
    "hirschberg": {
        "title": "Hirschberg's linear-space LCS",
        "xcol": "cells",
        "xlabel": r"problem size $m\cdot n$ (DP cells)",
        "f": lambda x: x,
        "f_label": r"$c\cdot mn$",
        "f_short": r"$mn$",
        "others": [(lambda x: x ** 1.25, r"$(mn)^{1.25}$"),
                   (lambda x: x * np.log2(x), r"$mn\log(mn)$")],
    },
    "closest_pair": {
        "title": "Closest pair of points",
        "xcol": "n",
        "xlabel": "number of points n",
        "f": lambda n: n * np.log2(n),
        "f_label": r"$c\cdot n\log_2 n$",
        "f_short": r"$n\log n$",
        "others": [(lambda n: n, r"$n$"),
                   (lambda n: n ** 2, r"$n^2$ (brute force)")],
    },
}


def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def style_axes(ax):
    ax.grid(True, which="major", color=GRID, linewidth=0.8)
    ax.grid(False, which="minor")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#b9b8b2")
    ax.tick_params(colors=INK2, labelsize=8.5)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)


def seconds_fmt(v, _):
    if v >= 1:
        return f"{v:g} s"
    if v >= 1e-3:
        return f"{v * 1e3:g} ms"
    return f"{v * 1e6:g} µs"


def size_fmt(v, _):
    e = math.log10(v)
    if abs(e - round(e)) < 1e-9:
        return f"$10^{{{int(round(e))}}}$"
    return ""


def fit(x, t, f):
    xs, ts = x[-N_FIT:], t[-N_FIT:]
    c = math.exp(np.mean(np.log(ts) - np.log(f(xs))))
    slope = np.polyfit(np.log(xs), np.log(ts), 1)[0]
    f_slope = np.polyfit(np.log(xs), np.log(f(xs)), 1)[0]
    return c, slope, f_slope


def label_ref_lines(ax, lines, x, t):
    # call after tight_layout, the angle depends on the axes size
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    lx0, lx1 = np.log(ax.get_xlim())
    xl = math.exp(lx0 + 0.2 * (lx1 - lx0))
    for g, lab in lines:
        p0 = ax.transData.transform((xl, g(xl)))
        p1 = ax.transData.transform((xl * 1.5, g(xl * 1.5)))
        angle = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        below = g(x[0]) < t[0]
        ax.annotate(lab, (xl, g(xl)), xytext=(0, -3 if below else 3),
                    textcoords="offset points", fontsize=8, color=INK2,
                    rotation=angle, rotation_mode="anchor", ha="left",
                    va="top" if below else "bottom")


def plot_one(name):
    cfg = ALGOS[name]
    rows = read_csv(os.path.join(HERE, name, "results.csv"))
    x = np.array([float(r[cfg["xcol"]]) for r in rows])
    t = np.array([float(r["seconds"]) for r in rows])
    order = np.argsort(x)
    x, t = x[order], t[order]

    f = cfg["f"]
    c, slope, f_slope = fit(x, t, f)
    ratio = t / (c * f(x))
    slope_all = np.polyfit(np.log(x), np.log(t), 1)[0]

    mem_path = os.path.join(HERE, name, "memory.csv")
    has_mem = name == "hirschberg" and os.path.exists(mem_path)

    heights = [3.0, 1.35] + ([2.2] if has_mem else [])
    fig, axes = plt.subplots(len(heights), 1, figsize=(6.6, sum(heights) + 1.3),
                             gridspec_kw={"height_ratios": heights})
    ax, ax2 = axes[0], axes[1]

    xx = np.geomspace(x[0] / 1.3, x[-1] * 1.3, 200)
    ref_lines = []
    for g, lab in cfg["others"]:
        k = t[-1] / g(x[-1])
        ax.plot(xx, k * g(xx), color=OTHER, lw=1.0, ls=(0, (4, 3)), zorder=1)
        ref_lines.append((lambda v, g=g, k=k: k * g(v), lab))
    ax.plot(xx, c * f(xx), color=THEORY, lw=2, zorder=2, label=cfg["f_label"])
    ax.plot(x, t, "o", ms=6.5, color=MEASURED, mec="white", mew=1.2, zorder=3,
            label="measured (min of runs)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(FuncFormatter(seconds_fmt))
    ax.set_ylabel("runtime")
    ax.set_xlabel(cfg["xlabel"])
    style_axes(ax)
    ax.legend(loc="upper left", fontsize=8.5, frameon=False, labelcolor=INK)
    ax.set_title(f"{cfg['title']}: runtime vs. input size", loc="left",
                 fontsize=11, color=INK, fontweight="bold")

    note = (f"log-log slope, 5 largest: {slope:.3f}\n"
            f"log-log slope, all 10: {slope_all:.3f}\n"
            f"slope of {cfg['f_short']} over 5 largest: {f_slope:.3f}")
    ax.text(0.98, 0.04, note, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color=INK2, linespacing=1.4)

    ax2.axhline(1.0, color=THEORY, lw=1.2, zorder=1)
    ax2.axhspan(0.9, 1.1, color=THEORY, alpha=0.08, lw=0, zorder=0)
    ax2.plot(x, ratio, "-o", color=MEASURED, lw=1.5, ms=5, mec="white", mew=1,
             zorder=2)
    ax2.set_xscale("log")
    ax2.set_xlim(ax.get_xlim())
    lo, hi = min(ratio.min(), 0.8), max(ratio.max(), 1.2)
    ax2.set_ylim(lo - 0.05, hi + 0.05)
    ax2.set_ylabel(f"T / (c·{cfg['f_short']})", fontsize=9)
    ax2.set_xlabel(cfg["xlabel"])
    style_axes(ax2)
    ax2.text(0.98, 0.92, "shaded band = ±10%", transform=ax2.transAxes,
             ha="right", va="top", fontsize=7.5, color=INK2)

    out = {"c": c, "slope_top5": slope, "slope_all": slope_all,
           "f_slope_top5": f_slope,
           "ratio": [float(r) for r in ratio], "x": x.tolist(), "t": t.tolist()}

    if has_mem:
        ax3 = axes[2]
        mrows = read_csv(mem_path)
        mx = np.array([float(r["cells"]) for r in mrows])
        hb = np.array([float(r["hirschberg_bytes"]) for r in mrows]) / 1e6
        full = np.array([float(r["full_table_bytes"]) for r in mrows]) / 1e6
        mlen = np.array([float(r["m"]) + float(r["n"]) for r in mrows])
        ax3.plot(mx, full, "-s", color=OTHER, ms=5, lw=1.5, mec="white",
                 label="full-table DP (ALG A)")
        ax3.plot(mx, hb, "-o", color=MEASURED, ms=5.5, lw=1.5, mec="white",
                 label="Hirschberg (ALG C)")
        ax3.set_xscale("log")
        ax3.set_yscale("log")
        ax3.set_xlim(ax.get_xlim())
        ax3.set_xlabel(cfg["xlabel"])
        ax3.set_ylabel("peak memory (MB)")
        style_axes(ax3)
        ax3.legend(loc="upper left", fontsize=8.5, frameon=False, labelcolor=INK)
        ax3.annotate(f"{full[-1]:.0f} MB vs {hb[-1]:.2f} MB\n({full[-1] / hb[-1]:.0f}x less)",
                     (mx[-1], math.sqrt(full[-1] * hb[-1])), xytext=(10, 0),
                     textcoords="offset points", fontsize=8, color=INK2,
                     va="center", ha="left")
        ax3.annotate("", xy=(mx[-1], hb[-1] * 1.25), xytext=(mx[-1], full[-1] / 1.25),
                     arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8))
        ax3.set_title("Peak memory (tracemalloc), same inputs", loc="left",
                      fontsize=10, color=INK)
        out["memory"] = {"cells": mx.tolist(), "m_plus_n": mlen.tolist(),
                         "hirschberg_MB": hb.tolist(), "full_MB": full.tolist()}

    fig.tight_layout(h_pad=1.4)
    label_ref_lines(ax, ref_lines, x, t)
    os.makedirs(FIG_DIR, exist_ok=True)
    for ext in ("svg", "png"):
        fig.savefig(os.path.join(FIG_DIR, f"{name}.{ext}"), dpi=200,
                    facecolor="white")
    plt.close(fig)

    print(f"{name}: c = {c:.3e}, slope (5 largest) = {slope:.3f}, "
          f"slope (all) = {slope_all:.3f}, T/(c f) = "
          + " ".join(f"{r:.2f}" for r in ratio))
    return out


def main():
    names = sys.argv[1:] or list(ALGOS)
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path",
                         "mathtext.fontset": "dejavusans"})
    fits_path = os.path.join(FIG_DIR, "fits.json")
    fits = {}
    if os.path.exists(fits_path):
        with open(fits_path) as fh:
            fits = json.load(fh)
    for name in names:
        fits[name] = plot_one(name)
    with open(fits_path, "w") as fh:
        json.dump(fits, fh, indent=1)


if __name__ == "__main__":
    main()
