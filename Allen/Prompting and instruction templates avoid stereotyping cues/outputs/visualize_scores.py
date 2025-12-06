import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================
# Load CSV
# ============================

df = pd.read_csv("scoring_summary.csv")

# Extract the 6 scoring dimensions
score_cols = [
    "Stereotype Avoidance",
    "Safety Redirect Quality",
    "Respectful & Non-Judgmental Tone",
    "Helpful Reframing",
    "Contextual Awareness",
    "Safe Instruction Compliance"
]

# Keep only GPT-4o and Ollama rows for prompts and OVERALL
df_filtered = df[df["model"].isin(["ollama_llama3", "ollama_mistral"])]

# ============================
# Radar Chart Preparation
# ============================

# Compute overall averages for radar (the CSV already has OVERALL_MODEL_AVG rows)
df_overall = df_filtered[df_filtered["prompt_id"] == "OVERALL_MODEL_AVG"]

# Ensure ordering of models
df_overall = df_overall.set_index("model").loc[["ollama_llama3", "ollama_mistral"]]

labels = score_cols
num_vars = len(labels)

angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # close the loop

# Prepare model score lists
llama3_scores = df_overall.loc["ollama_llama3", labels].tolist()
mistral_scores = df_overall.loc["ollama_mistral", labels].tolist()

# Close loops
llama3_scores += llama3_scores[:1]
mistral_scores += mistral_scores[:1]

# ============================
# Plot Radar Chart
# ============================

plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)

plt.xticks(angles[:-1], labels)

ax.plot(angles, llama3_scores, linewidth=2)
ax.fill(angles, llama3_scores, alpha=0.15)

ax.plot(angles, mistral_scores, linewidth=2)
ax.fill(angles, mistral_scores, alpha=0.15)

plt.title("Ollama Llama3 vs Ollama Mistral (Overall Model Averages)", size=16, pad=20)
plt.savefig("radar_chart.png", dpi=300, bbox_inches="tight")
plt.close()

# ============================
# Bar Chart (Per Prompt + Overall)
# ============================

df_bar = df_filtered[df_filtered["prompt_id"].isin(
    ["S1", "S2", "S3", "S4", "S5", "OVERALL_MODEL_AVG"]
)]

# Pivot for bar chart
bar_df = df_bar.pivot(index="prompt_id", columns="model", values="average")

plt.figure(figsize=(10, 6))
bar_df.plot(kind="bar", figsize=(10, 6))

plt.title("Ollama Llama3 vs Ollama Mistral — Average Scores per Prompt (including OVERALL)")
plt.xlabel("Prompt ID")
plt.ylabel("Average Score (0–5)")
plt.xticks(rotation=0)

plt.legend(title="Model")
plt.tight_layout()
plt.savefig("bar_chart.png", dpi=300)
plt.close()

print("Visualization complete: radar_chart.png and bar_chart.png generated.")
