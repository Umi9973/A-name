import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "System-model_dimension_means.csv")
df = pd.read_csv(csv_path)

print("Loaded data:")
print(df)

metrics = [
    "identity_clarity",
    "capabilities",
    "limitations",
    "uncertainty",
    "contextualization",
    "safety_boundaries",
]

labels = np.array(metrics)
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

plt.figure(figsize=(6, 6))
ax = plt.subplot(111, polar=True)

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
for idx, (_, row) in enumerate(df.iterrows()):
    values = row[metrics].values.astype(float)
    values = np.concatenate((values, [values[0]]))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.15)
    ax.scatter(angles, values, s=20)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=9)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8)
ax.set_ylim(0, 5)

legend_labels = df["model"].tolist()
ax.legend(legend_labels, loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=9)

plt.tight_layout()
radar_path = os.path.join(base_dir, "system_radar_deepseek_vs_qwen3.png")
plt.savefig(radar_path, dpi=300)
plt.close()
print(f"Saved radar chart to: {radar_path}")

plt.figure(figsize=(5, 4))
x = np.arange(len(df))
width = 0.6
plt.bar(x, df["overall_average"].astype(float), width)
plt.xticks(x, df["model"], rotation=20, ha="right", fontsize=9)
plt.ylabel("Overall average", fontsize=10)
plt.tight_layout()
bar_path = os.path.join(base_dir, "system_overall_average_bar.png")
plt.savefig(bar_path, dpi=300)
plt.close()
print(f"Saved bar chart to: {bar_path}")

print("All plots generated.")