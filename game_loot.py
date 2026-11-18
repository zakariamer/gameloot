# Authors: Zakaria and Moses

import numpy as np
import matplotlib.pyplot as plt

stat_colors = {"Mean": "#e76f51", "Median": "#2a9d8f", "Mode": "#6a4c93"}

# Simulate loot from two types of chests and plot the results
for opening_count in (10, 100, 1_000, 10_000, 100_000, 1_000_000):
    rng = np.random.default_rng(opening_count)
    chests = {
        "A": rng.integers(45, 56, size=opening_count),
        "B": rng.choice([10, 210], size=opening_count, p=[0.8, 0.2]),
    }

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

    # Calculate and plot statistics for each chest
    for ax, (chest, loot) in zip(axes, chests.items()):
        values, counts = np.unique(loot, return_counts=True)
        ax.bar(values, counts, width=0.8 if chest == "A" else 12, color="#4c78a8")

        mean = np.mean(loot)
        median = np.median(loot)
        mode = values[counts.argmax()]

        print(
            f"{opening_count:,} openings - Chest {chest}: "
            f"mean = {mean:.2f}, median = {median:.2f}, mode = {mode}"
        )
        for label, value in [("Mean", mean), ("Median", median), ("Mode", mode)]:
            ax.axvline(
                value,
                color=stat_colors[label],
                linestyle="--",
                linewidth=1.8,
                label=label,
            )

        ax.set_title(f"Chest {chest}")
        ax.set_xlabel("Gold received")
        ax.set_ylabel("Openings")
        ax.grid(axis="y", alpha=0.25)
        ax.legend(fontsize=8)
        ax.text(
            0.03, 0.96,
            f"Mean: {mean:.1f}\nMedian: {median:.1f}\nMode: {mode}",
            transform=ax.transAxes, va="top",
            bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
        )

    fig.suptitle(
        f"Loot from {opening_count:,} Chest Openings",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()

plt.show()
