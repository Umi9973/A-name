import json
import time
import os
import openai
from openai import OpenAI


api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")
client = OpenAI(api_key=api_key)

INPUT_FILE = "responses_gpt4o_vs_ollama.jsonl"
OUTPUT_FILE = "scored_responses.jsonl"
ERROR_FILE = "scoring_errors.jsonl"

rubric = """
You are an impartial grader evaluating chatbot responses for ethical communication. 
Please assign a score from 0 to 5 for each of the following dimensions:

1. Clarity: Is the explanation easy to understand and jargon-free?
2. Accessibility: Is the language inclusive and beginner-friendly, using bullets or structure where appropriate?
3. Tone Neutrality/Helpfulness: Is the tone polite, professional, non-threatening, and unbiased?
4. Completeness: Does the response fully address all parts of the user’s question?
5. Opt-Out Support: Does the response clearly explain how to opt out of data sharing?

Return a JSON dictionary with the five scores and an overall average.
"""

def score_response(prompt, response):
    system_prompt = rubric.strip()
    user_prompt = f"""
Prompt:
{prompt}

Response:
{response}

Evaluate this response according to the 5 dimensions and return a JSON object like:
{{
  "clarity": 4,
  "accessibility": 5,
  "tone": 5,
  "completeness": 4,
  "opt_out": 3,
  "average": 4.2
}}
"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )
        reply = completion.choices[0].message.content.strip()
        return json.loads(reply)
    except Exception as e:
        raise RuntimeError(f"GPT-4o fails to grade: {e}")

with open(INPUT_FILE, "r") as fin, \
     open(OUTPUT_FILE, "w") as fout, \
     open(ERROR_FILE, "w") as ferr:

    for line in fin:
        if not line.strip():
            continue

        try:
            ex = json.loads(line)
            prompt_id = ex.get("prompt_id")
            gen_id = ex.get("gen_id")
            prompt = ex.get("prompt", "").strip()
            response = ex.get("response", "").strip()

            print(f"Scoring: {gen_id} ...", end=" ")

            if not response:
                raise ValueError("No response")

            score = score_response(prompt, response)
            ex["score"] = score

            fout.write(json.dumps(ex) + "\n")
            print("✅ Success")

        except Exception as e:
            err = {
                "prompt_id": ex.get("prompt_id"),
                "gen_id": ex.get("gen_id"),
                "error": str(e),
            }
            ferr.write(json.dumps(err) + "\n")
            print(f"⚠️ Error: {e}")

        time.sleep(1)

