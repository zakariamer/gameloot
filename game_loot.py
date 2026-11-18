# Authors: Zakaria and Moses

import numpy as np
import matplotlib.pyplot as plt

# Simulate loot from two different chests
chests = {
    "A": np.random.randint(45, 56, size=100000),
    "B": np.random.choice([10, 210], size=100000, p=[0.8, 0.2]),
}
stat_colors = {"Mean": "#e76f51", "Median": "#2a9d8f", "Mode": "#6a4c93"}

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# Calculate and plot statistics for each chest
for ax, (chest, loot) in zip(axes, chests.items()):
    values, counts = np.unique(loot, return_counts=True)
    ax.bar(values, counts, width=0.8 if chest == "A" else 12, color="#4c78a8")

    mean = np.mean(loot)
    median = np.median(loot)
    mode = np.bincount(loot).argmax()

    print(f"Chest {chest}: mean = {mean:.2f}, median = {median:.2f}, mode = {mode}")
    for label, value in [("Mean", mean), ("Median", median), ("Mode", mode)]:
        ax.axvline(value, color=stat_colors[label], linestyle="--", linewidth=1.8, label=label)

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

# Add a main title and adjust layout
fig.suptitle("Loot from 100 Chest Openings", fontsize=14, fontweight="bold")
fig.tight_layout()
plt.show()
