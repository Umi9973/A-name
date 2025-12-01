import json
import pandas as pd

INPUT_FILE = "scoring_response.jsonl"
OUTPUT_FILE = "scoring_summary.csv"

# Columns we want to aggregate
score_keys = [
    "Stereotype Avoidance",
    "Safety Redirect Quality",
    "Respectful & Non-Judgmental Tone",
    "Helpful Reframing",
    "Contextual Awareness",
    "Safe Instruction Compliance",
    "average",
]

# -----------------------------
# Step 1: Load JSONL into list
# -----------------------------
records = []
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        ex = json.loads(line)
        
        # Skip rows with no score (error cases)
        if ex.get("score") is None:
            continue
        
        row = {
            "prompt_id": ex.get("prompt_id"),
            "model": ex.get("model"),     # "gpt-4o", "ollama", etc.
        }
        
        # Add all score fields
        for k in score_keys:
            row[k] = ex["score"].get(k, None)

        records.append(row)

# Convert to DataFrame
df = pd.DataFrame(records)

# ---------------------------------------
# Step 2: Compute per-prompt/model means
# ---------------------------------------
grouped = df.groupby(["prompt_id", "model"], as_index=False)[score_keys].mean()

# ---------------------------------------
# Step 3: Compute overall average per model
# ---------------------------------------
model_avg = grouped.groupby("model", as_index=False)[score_keys].mean()
model_avg["prompt_id"] = "OVERALL_MODEL_AVG"

# Reorder columns to match grouped
model_avg = model_avg[
    ["prompt_id", "model"] + score_keys
]

# ---------------------------------------
# Step 4: Combine results
# ---------------------------------------
final_df = pd.concat([grouped, model_avg], ignore_index=True)

# ---------------------------------------
# Step 5: Save to CSV
# ---------------------------------------
final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("CSV generated:", OUTPUT_FILE)
