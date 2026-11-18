# Authors: Zakaria and Moses
# Game Loot Drop: Chest A vs Chest B
#   Chest A: 45-55 gold, every amount equally likely
#   Chest B: 10 gold (80%) or 210 gold (20%)
# Simulates each chest 10 ... 1,000,000 times and makes every chart for the slides.

import numpy as np
import matplotlib.pyplot as plt

SEED = 6
SIZES = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
SIZE_LABELS = ["10", "100", "1K", "10K", "100K", "1M"]

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#52514e"
LINE_STYLES = {"Mean": "-", "Median": "--", "Mode": ":"}


# ---------- simulation ----------
def open_chests(rng, n):
    a = rng.integers(45, 56, size=n)                     # 56 is exclusive, so 45..55
    b = rng.choice([10, 210], size=n, p=[0.8, 0.2])
    return a, b


def modes(loot):
    """All values tied for the highest count (there can be more than one)."""
    values, counts = np.unique(loot, return_counts=True)
    return values[counts == counts.max()].tolist()


def stats(loot):
    return {
        "Mean": np.mean(loot),
        "Median": np.median(loot),
        "Mode": modes(loot),
        "Std": np.std(loot),
    }


def clean_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)


def mode_text(m):
    return ", ".join(str(v) for v in m)


# ---------- run every sample size once, reuse results everywhere ----------
rng = np.random.default_rng(SEED)
results = {}  # n -> {"A": loot, "B": loot}
for n in SIZES:
    a, b = open_chests(rng, n)
    results[n] = {"A": a, "B": b}

all_stats = {n: {c: stats(results[n][c]) for c in ("A", "B")} for n in SIZES}


# ---------- Slide 4: results table ----------
print(f"{'Openings':>10} | {'A Mean':>7} {'A Med':>6} {'A Mode':>8} {'A Std':>6} | "
      f"{'B Mean':>7} {'B Med':>6} {'B Mode':>7} {'B Std':>6}")
print("-" * 82)
for n in SIZES:
    sa, sb = all_stats[n]["A"], all_stats[n]["B"]
    print(f"{n:>10,} | {sa['Mean']:7.2f} {sa['Median']:6.1f} {mode_text(sa['Mode']):>8} {sa['Std']:6.2f} | "
          f"{sb['Mean']:7.2f} {sb['Median']:6.1f} {mode_text(sb['Mode']):>7} {sb['Std']:6.2f}")


# ---------- Slide 5: law of large numbers ----------
means_a = [all_stats[n]["A"]["Mean"] for n in SIZES]
means_b = [all_stats[n]["B"]["Mean"] for n in SIZES]

fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(SIZES, means_a, "o-", color=BLUE, linewidth=2, markersize=8, label="Chest A")
ax.plot(SIZES, means_b, "o-", color=ORANGE, linewidth=2, markersize=8, label="Chest B")
ax.axhline(50, color=GRAY, linestyle="--", linewidth=1, label="Expected value = 50")
for n, m in zip(SIZES, means_b):
    ax.annotate(f"{m:.1f}", (n, m), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=9)
ax.set_xscale("log")
ax.set_xticks(SIZES)
ax.set_xticklabels(SIZE_LABELS)
ax.set_ylim(40, max(means_b) + 8)
ax.set_xlabel("Number of openings (log scale)")
ax.set_ylabel("Mean gold per opening")
ax.set_title("Law of Large Numbers: Chest B needs far more samples", loc="left")
ax.legend(frameon=False)
clean_axes(ax)
fig.tight_layout()
fig.savefig("slide5_convergence.png", dpi=200)


# ---------- Slide 6: histograms at the largest sample size ----------
def histogram(ax, loot, st, color, title, bar_width, legend_loc):
    values, counts = np.unique(loot, return_counts=True)
    pct = counts / len(loot) * 100
    ax.bar(values, pct, width=bar_width, color=color)

    lines = [("Mean", st["Mean"]), ("Median", st["Median"])]
    lines += [("Mode", m) for m in st["Mode"]]
    for label, value in lines:
        ax.axvline(value, color="black", linestyle=LINE_STYLES[label], linewidth=1.8,
                   label=f"{label} = {value:.2f}" if label == "Mean" else f"{label} = {value:g}")
    ax.plot([], [], " ", label=f"Std dev = {st['Std']:.2f}")  # legend-only entry

    ax.set_title(title, loc="left")
    ax.set_xlabel("Gold per opening")
    ax.set_ylabel("% of openings")
    ax.set_ylim(0, pct.max() * 1.45)
    ax.legend(frameon=False, fontsize=9, loc=legend_loc)
    clean_axes(ax)


n_big = SIZES[-1]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
histogram(ax1, results[n_big]["A"], all_stats[n_big]["A"], BLUE,
          "Chest A: every amount equally likely", 0.8, "upper left")
ax1.set_xticks(range(45, 56))
histogram(ax2, results[n_big]["B"], all_stats[n_big]["B"], ORANGE,
          "Chest B: usually 10, sometimes 210", 12, "upper right")
ax2.set_xticks([10, 50, 100, 150, 210])
fig.suptitle(f"Same mean, different story ({n_big:,} openings)",
             fontsize=13, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("slide6_histograms.png", dpi=200)

plt.show()
