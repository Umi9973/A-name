# Counterfectual Fairness Pipeline

Below is the full workflow for evaluating the **Counterfactual fairness spot-checks conducted** dimension.  
The process uses a structured prompt dataset, generates model responses through ChatGPT, Gemini, and Mistral APIs, and scores those responses based on a rubric.

---

## Folder Structure
```text
Counterfectual Fairness/
│
├── counterfectual.json                 # Input prompt
├── generate_response_counter.ipynb    # Notebook to generate model responses
├── score_counter.ipynb                # Notebook to score responses
│
└── output/
    ├── counterfectual_output.jsonl     # Generated model responses
    └── counterfectual.jsonl     # Scored results
```
## Environment Setup
Python Version:
    Python 3.12+ is required.

Install Dependencies:
    pip install google-generativeai groq python-dotenv pandas tqdm
    pip install --upgrade pydantic mistralai

Environment Variables (.env):
    OPENAI_API_KEY=your_chatgpt_api_key
    GOOGLE_API_KEY=your_gemini_api_key
    GROQ_API_KEY=your_mistral_api_key

## Work Flow
```text
Input File:
    counterfectual.json
Run:
    generate_response_counter.ipynb

Output:
    output/counterfectual_output.jsonl
Run:
    score_counter.ipynb

Output:
    output/counterfectual_scored.json
```
## Notice
- Ensure valid API keys
- Use Python 3.12+ to avoid failure to import mistral package
