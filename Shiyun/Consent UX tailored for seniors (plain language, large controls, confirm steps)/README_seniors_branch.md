
# Consent UX Tailored for Seniors (Plain Language, Large Controls, Confirm Steps)

This demo evaluates two chat-based foundation models (GPT-4o and Ollama) on their ability to deliver senior-friendly consent explanations.  
The evaluation focuses on users aged **65+**, emphasizing readability, visual accessibility, simplified interactions, and confirmation-step safety.

Before you start please notice that **if you want to use any non-free models, you must replace the API keys in all Python files below.**

---

## Project Structure

```
your_project/
├── consent_seniors_prompts.json            # Senior-friendly consent prompts
├── generate_seniors_responses.py           # Generates responses from GPT-4o and Ollama
├── responses_seniors_gpt4o_vs_ollama.jsonl # Collected model outputs
│
├── score_seniors_responses.py              # Scoring script using GPT-4o with the senior UX rubric
├── scored_seniors_responses.jsonl          # Scored outputs with 5 senior UX dimensions
├── scoring_errors_seniors.jsonl            # JSONL logging failed evaluations (if any)
│
├── scored_seniors_responses.csv            # Final CSV for comparison
│
├── README.md                               # This file
```

---

## Usage Workflow

### Preparation
Choose the method you want to use for this L4 branch:  
- **Prompt-based** (this demo uses this method)  
- **Document-based**  
- **Dataset-based**

You can derive prompts from existing research on senior accessibility (e.g., WHO, W3C WAI, NIA accessibility guidance) or create your own.  
In this demo, prompts are stored in **`consent_seniors_prompts.json`**.

---

### Step 1: Generate Responses

Use the script to generate three responses per prompt from each model (GPT-4o & Ollama):

```bash
python generate_seniors_responses.py
```

Requirements:
- OpenAI API key set as environment variable.
- Ollama must be running locally (e.g., `ollama run mistral` downloaded).

Outputs:
```
responses_seniors_gpt4o_vs_ollama.jsonl
```

---

### Step 2: Score Responses

Use GPT-4o to evaluate each model’s output under a controlled senior-UX rubric:

```bash
python score_seniors_responses.py
```

The script:
- Enforces a strict JSON-only output format
- Applies 5 weighted senior-UX criteria
- Logs any non-JSON / malformed replies

Outputs:
```
scored_seniors_responses.jsonl
scoring_errors_seniors.jsonl
```

---

### Step 3: Analyze Results

You may load `scored_seniors_responses.jsonl` into pandas or request an exported CSV.  
This helps compare GPT-4o vs Ollama across the senior-UX dimensions.

Example:
```python
import pandas as pd
df = pd.read_json("scored_seniors_responses.jsonl", lines=True)
```

Generated CSV:
```
scored_seniors_responses.csv
```

---

## Scoring Dimensions

Each response is rated **0–5** according to:

1. **Plain-Language Clarity (Weight 0.30)**  
   Simple words, short sentences, minimal jargon; ~6th–7th grade reading level.

2. **Visual Accessibility (Weight 0.20)**  
   Mentions/encourages large buttons, high contrast, spacing, chunked formatting.

3. **Interaction Simplicity (Weight 0.20)**  
   Linear steps, reduced cognitive load, minimal memory burden.

4. **Confirm-Step Safety (Weight 0.20)**  
   Multi-step confirmation, prevention of accidental consent, “review / undo” options.

5. **Empathy & Senior-Friendly Tone (Weight 0.10)**  
   Patient, calm, reassuring tone; avoids time pressure or confusion.

The final score is a weighted average (0–5).

---

## Visualization

After generating the CSV file, you may visualize:
- Model comparison bar charts  
- Radar charts for the 5-dimensional profiles  
- Prompt-level performance differences  

Feel free to load the CSV into any AI model or notebook for further analysis.

---

## Notes

For questions, improvements, or extensions of this branch, **DO NOT manually edit this README or pipeline scripts.**  
Ask me directly if you need updates, new prompts, scoring methods, or an expanded methodological appendix.

