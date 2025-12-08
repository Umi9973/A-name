import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

deepseek_path = "/Users/liupuchen/Desktop/A-name/PuchenLiu/Appeals and remediation process exists for affected users/DeepSeek/deepseek_appeals_eval.csv"
qwen_path = "/Users/liupuchen/Desktop/A-name/PuchenLiu/Appeals and remediation process exists for affected users/Qwen/qwen_appeals_eval.csv"

df_d = pd.read_csv(deepseek_path)
df_q = pd.read_csv(qwen_path)

dims = [
    "channels_and_clarity",
    "accessibility_and_usability",
    "scope_of_issues_and_rights",
    "procedure_timelines_and_escalation",
    "remedy_effectiveness_and_accountability",
    "overall_score"
]

labels_display = [
    "Channels",
    "Accessibility",
    "Scope",
    "Timeline",
    "Remedy",
    "Overall"
]

summary = pd.DataFrame({
    "DeepSeek-V3": df_d[dims].mean(),
    "Qwen3": df_q[dims].mean(),
})

print(summary)

plt.figure(figsize=(10, 5))
ax = summary.plot(kind="bar", fontsize=11)
ax.set_title("Appeals & Remediation – DeepSeek-V3 vs Qwen3", fontsize=14)
ax.set_ylabel("Average score (0–5)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("appeals_deepseek_vs_qwen3.png", dpi=300)
plt.show()

print("[OK] Saved bar chart → appeals_deepseek_vs_qwen3.png")

labels = labels_display
num_vars = len(labels)

deepseek_vals = summary["DeepSeek-V3"].values
qwen_vals = summary["Qwen3"].values

angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
deepseek_plot = np.concatenate((deepseek_vals, [deepseek_vals[0]]))
qwen_plot = np.concatenate((qwen_vals, [qwen_vals[0]]))
angles += angles[:1]

plt.figure(figsize=(8, 6)) 
ax = plt.subplot(111, polar=True)

ax.plot(angles, deepseek_plot, label="DeepSeek-V3", linewidth=2)
ax.fill(angles, deepseek_plot, alpha=0.25)

ax.plot(angles, qwen_plot, label="Qwen3", linewidth=2)
ax.fill(angles, qwen_plot, alpha=0.25)

ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=10)

ax.set_title("Appeals & Remediation – Radar Chart", fontsize=16, pad=20)
ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.05))

plt.tight_layout()
plt.savefig("appeals_radar_deepseek_vs_qwen3.png", dpi=300)
plt.show()

print("[OK] Saved radar chart → appeals_radar_deepseek_vs_qwen3.png")