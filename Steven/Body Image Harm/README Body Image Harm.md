# Body Image Harm Pipeline

Below is the full workflow for evaluating the **Body Image Harm Risk (Teens)** dimension.  
The process uses a structured prompt dataset, generates model responses through ChatGPT, Gemini, and Mistral APIs, and scores those responses based on a rubric.

---

## Folder Structure
```text
Body Image Harm/
│
├── body_image.json                 # Input prompt
├── generate_response_body.ipynb    # Notebook to generate model responses
├── score_body.ipynb                # Notebook to score responses
│
└── output/
    ├── body_image_output.jsonl     # Generated model responses
    └── body_image_scored.jsonl     # Scored results
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
    body_image.json
Run:
    generate_response_body.ipynb

Output:
    output/body_image_output.jsonl
Run:
    score_body.ipynb

Output:
    output/body_image_scored.json
```
## Notice
- Ensure valid API keys
- Use Python 3.12+ to avoid failure to import mistral package
