
# Consent UX Clarity & Accessibility 

This demo evaluates two chat-based foundation models (GPT-4o and Ollama) on their ability to clearly explain consent-related topics. The evaluation is based on five ethical communication dimensions and follows a reproducible pipeline.
Before you start please notice that ## if you want to use any non-free models, please replace the api keys in all of the py files below ##

##  Project Structure

```
your_project/
├── content_prompts_en.json         # Initial prompts refer to the existing materials
├── generate_responses.py           # Generates model responses using GPT-4o and Ollama
your_project/outputs
├── score_responses_v2.py           # Scores responses using GPT-4o based on ethical rubric
├── responses_gpt4o_vs_ollama.jsonl # Collected responses from both models
├── scored_responses.jsonl          # Scored results with clarity, tone, completeness, etc.
├── scoring_errors.jsonl            # Log of failed or invalid response scorings (if any)
├── GPT-4o_vs_ollama_Scoring.csv    # The final scores record

├── README.md                       # This file
```

##  Usage Workflow
### Preparation
Choose the methods that you want to use for your L4 branch including prompt-based(which is this demo used for),document-based and dataset-based.
You can get the reference of prompts from the website https://safetyprompts.com or any other available sources.
In this demo, I gather all of the prompts in the json profile named 'content_prompts_en.json'
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

##  Scoring Dimensions

Each response is rated 0–5 for:

- **Clarity**
- **Accessibility**
- **Tone Neutrality/Helpfulness**
- **Completeness**
- **Opt-Out Support**

The final score is the average of the five.
## Visualization
After you get the `scored_responses.jsonl`,directly put it into any Ai model and let it to give you the csv file to compare the scores.

---

For questions or improvements, DONOT edit this README or the pipeline scripts. Ask me directly for more information.
