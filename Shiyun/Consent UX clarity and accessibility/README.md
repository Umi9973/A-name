
# Consent UX Clarity & Accessibility Demo

This demo evaluates two chat-based foundation models (GPT-4o and Ollama) on their ability to clearly explain consent-related topics. The evaluation is based on five ethical communication dimensions and follows a reproducible pipeline.

## 📁 Project Structure

```
your_project/
├── generate_responses.py           # Generates model responses using GPT-4o and Ollama
├── score_responses.py              # Scores responses using GPT-4o based on ethical rubric
├── responses_gpt4o_vs_ollama.jsonl # Collected responses from both models
├── scored_responses.jsonl          # Scored results with clarity, tone, completeness, etc.
├── scoring_errors.jsonl            # Log of failed or invalid response scorings (if any)
├── README.md                       # This file
```

## 🧪 Usage Workflow

### Step 1: Generate Responses
Run the script to generate responses for multiple prompts from GPT-4o and Ollama:
```bash
python generate_responses.py
```

- Requires OpenAI API Key in environment.
- Ollama must be running locally with a model like `mistral` pulled.

### Step 2: Score Responses
Score all generated responses with GPT-4o using the provided ethical rubric:
```bash
python score_responses.py
```

- Ensure OpenAI API key is valid and set in the script or environment.
- Results are saved to `scored_responses.jsonl`.

### Step 3: Analyze Results
You can inspect or load `scored_responses.jsonl` into a pandas DataFrame for further analysis, visualization, or exporting.

### Optional: Error Handling
If any response failed to be scored (e.g., empty or invalid JSON), they will be logged to:
```
scoring_errors.jsonl
```

## 📋 Scoring Dimensions

Each response is rated 0–5 for:

- **Clarity**
- **Accessibility**
- **Tone Neutrality/Helpfulness**
- **Completeness**
- **Opt-Out Support**

The final score is the average of the five.

---

For questions or improvements, feel free to edit this README or the pipeline scripts.
