import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_path = (
    "/Users/liupuchen/Desktop/A-name/PuchenLiu/"
    "Automated agent disclosure in user-facing interactions/GPT5-score/"
    "Automated agent disclosure in user-facing interactions/Automated-model_dimension_means.csv"
)

df = pd.read_csv(csv_path)
print("Loaded data:")
print(df)

models_to_keep = ["DeepSeek-V3_automated", "Qwen3_automated"]
df = df[df["model"].isin(models_to_keep)].reset_index(drop=True)

dimension_cols = [
    "agent_identity",
    "automation_scope",
    "user_intent_alignment",
    "autonomy_level",
    "risk_disclosure",
    "control_reversibility",
]
labels_display = ["Identity", "Scope", "Intent", "Autonomy", "Risk", "Control"]

def plot_radar(df, dimensions, labels_display, out_path):

    df_sorted = df.set_index("model").loc[
        ["DeepSeek-V3_automated", "Qwen3_automated"]
    ]

    values_deepseek = df_sorted.loc["DeepSeek-V3_automated", dimensions].values.astype(float)
    values_qwen = df_sorted.loc["Qwen3_automated", dimensions].values.astype(float)

    values_deepseek = np.concatenate([values_deepseek, values_deepseek[:1]])
    values_qwen = np.concatenate([values_qwen, values_qwen[:1]])

    num_vars = len(dimensions)
    angles = np.linspace(0, 2 * np.pi, num_vars + 1)

    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111, polar=True)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels_display, fontsize=10)

    ax.plot(angles, values_deepseek, linewidth=2, linestyle="solid", label="DeepSeek-V3")
    ax.fill(angles, values_deepseek, alpha=0.15)

    ax.plot(angles, values_qwen, linewidth=2, linestyle="solid", label="Qwen3")
    ax.fill(angles, values_qwen, alpha=0.15)

    ax.set_title("Automated Agent Disclosure – Dimension Means", fontsize=16, pad=20)

    ax.set_ylim(0, 5)

    ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.05), fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved radar chart to: {out_path}")

def plot_total_mean_bar(df, out_path):
    df_sorted = df.set_index("model").loc[
        ["DeepSeek-V3_automated", "Qwen3_automated"]
    ]
    models = ["DeepSeek-V3_automated", "Qwen3_automated"]
    means = df_sorted["total_mean"].values.astype(float)

    plt.figure(figsize=(6, 4))
    x = np.arange(len(models))
    plt.bar(x, means, width=0.5)

    plt.xticks(x, ["DeepSeek-V3", "Qwen3"], fontsize=10)
    plt.ylabel("Total Mean Score", fontsize=12)
    plt.ylim(0, 5)
    plt.title("Automated Agent Disclosure – Overall Mean Score", fontsize=14)

    for i, v in enumerate(means):
        plt.text(i, v + 0.05, f"{v:.2f}", ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved bar chart to: {out_path}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.dirname(csv_path))

    radar_path = os.path.join(out_dir, "automated_radar_deepseek_vs_qwen3.png")
    bar_path = os.path.join(out_dir, "automated_total_mean_bar.png")

    plot_radar(df, dimension_cols, labels_display, radar_path)
    plot_total_mean_bar(df, bar_path)

    print("All plots generated.")