import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

deepseek_path = "/Users/liupuchen/Desktop/A-name/PuchenLiu/Dark pattern controls for minors/DeepSeek/deepseek_darkpattern_eval.csv"
qwen_path = "/Users/liupuchen/Desktop/A-name/PuchenLiu/Dark pattern controls for minors/Qwen/qwen_darkpattern_eval.csv"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR

deepseek_df = pd.read_csv(deepseek_path)
qwen_df = pd.read_csv(qwen_path)

DIM_COLS = [
    "manipulative_ui_protection",
    "age_verification_controls",
    "child_data_protection",
    "transparency_for_minors",
    "remedy_and_escalation",
]
OVERALL_COL = "overall_score"

deepseek_means = deepseek_df[DIM_COLS + [OVERALL_COL]].mean()
qwen_means = qwen_df[DIM_COLS + [OVERALL_COL]].mean()

summary_df = pd.DataFrame({
    "dimension": DIM_COLS + [OVERALL_COL],
    "DeepSeek-V3": [deepseek_means[c] for c in DIM_COLS + [OVERALL_COL]],
    "Qwen3": [qwen_means[c] for c in DIM_COLS + [OVERALL_COL]],
})

def make_label(name: str) -> str:
    mapping = {
        "manipulative_ui_protection": "Manipulative\nUI protection",
        "age_verification_controls": "Age\nverification",
        "child_data_protection": "Child data\nprotection",
        "transparency_for_minors": "Transparency\nfor minors",
        "remedy_and_escalation": "Remedy &\nescalation",
        "overall_score": "Overall\nscore",
    }
    return mapping.get(name, name)

radar_labels = [make_label(c) for c in DIM_COLS]
num_dims = len(DIM_COLS)
angles = np.linspace(0, 2 * np.pi, num_dims, endpoint=False)
angles = np.concatenate([angles, [angles[0]]])

deepseek_vals = [deepseek_means[c] for c in DIM_COLS]
qwen_vals = [qwen_means[c] for c in DIM_COLS]
deepseek_vals = np.concatenate([deepseek_vals, [deepseek_vals[0]]])
qwen_vals = np.concatenate([qwen_vals, [qwen_vals[0]]])

plt.figure(figsize=(7.5, 7.5))
ax = plt.subplot(111, polar=True)
ax.plot(angles, deepseek_vals, linewidth=2, label="DeepSeek-V3")
ax.fill(angles, deepseek_vals, alpha=0.15)
ax.plot(angles, qwen_vals, linewidth=2, linestyle="--", label="Qwen3")
ax.fill(angles, qwen_vals, alpha=0.15)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(radar_labels, fontsize=11)
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.set_ylim(0, 5)
ax.tick_params(axis="x", pad=12)

plt.title("Dark pattern controls for minors – Dimension means", fontsize=14, pad=20)
plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.05))
plt.tight_layout()

radar_path = os.path.join(OUTPUT_DIR, "darkpattern_radar_deepseek_vs_qwen3.png")
plt.savefig(radar_path, dpi=300)
plt.close()

x_labels = [make_label(c) for c in DIM_COLS + [OVERALL_COL]]
x = np.arange(len(x_labels))
width = 0.35

deepseek_bar_vals = [deepseek_means[c] for c in DIM_COLS + [OVERALL_COL]]
qwen_bar_vals = [qwen_means[c] for c in DIM_COLS + [OVERALL_COL]]

plt.figure(figsize=(9, 5))
ax = plt.gca()
ax.bar(x - width/2, deepseek_bar_vals, width, label="DeepSeek-V3")
ax.bar(x + width/2, qwen_bar_vals, width, label="Qwen3")

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_ylim(0, 5)
ax.set_ylabel("Mean score (0–5)")
ax.set_title("Dark pattern controls for minors – Dimension & overall means")
ax.legend()

plt.tight_layout()
bar_path = os.path.join(OUTPUT_DIR, "darkpattern_total_mean_bar.png")
plt.savefig(bar_path, dpi=300)
plt.close()
