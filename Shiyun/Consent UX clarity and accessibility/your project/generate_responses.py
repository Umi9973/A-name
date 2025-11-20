import os
os.environ["OPENAI_API_KEY"] = "your openai_api_key_here"

import os
import json
import time
from pathlib import Path
from openai import OpenAI
from ollama import Client as OllamaClient

# === CONFIGURATION ===
NUM_GENERATIONS = 3
PROMPT_FILE = "consent_prompts_en.json"
OUTPUT_DIR = Path("outputs")
MODEL_A = "gpt-4o"
MODEL_B = "ollama_mistral"
OLLAMA_MODEL_NAME = "mistral"

# === SETUP ===
openai_client = OpenAI()
ollama_client = OllamaClient()
OUTPUT_DIR.mkdir(exist_ok=True)

with open(PROMPT_FILE, "r") as f:
    prompts = json.load(f)

def generate_with_gpt4o(prompt_text):
    chat = openai_client.chat.completions.create(
        model=MODEL_A,
        messages=[
            {"role": "system", "content": "You are a helpful assistant chatbot."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
        max_tokens=512,
    )
    return chat.choices[0].message.content.strip()

def generate_with_ollama(prompt_text):
    response = ollama_client.chat(model=OLLAMA_MODEL_NAME, messages=[
        {"role": "user", "content": prompt_text}
    ])
    return response['message']['content'].strip()

results = []

for prompt in prompts:
    prompt_id = prompt["id"]
    prompt_text = prompt["prompt_text"]

    for i in range(NUM_GENERATIONS):
        print(f"Generating [GPT-4o] Prompt {prompt_id}, Iteration {i+1}")
        response_a = generate_with_gpt4o(prompt_text)
        results.append({
            "prompt_id": prompt_id,
            "model": MODEL_A,
            "gen_id": f"{prompt_id}_gpt4o_gen{i+1}",
            "response": response_a
        })

        print(f"Generating [Ollama] Prompt {prompt_id}, Iteration {i+1}")
        response_b = generate_with_ollama(prompt_text)
        results.append({
            "prompt_id": prompt_id,
            "model": MODEL_B,
            "gen_id": f"{prompt_id}_ollama_gen{i+1}",
            "response": response_b
        })

# save to jsonl
outfile = OUTPUT_DIR / "responses_gpt4o_vs_ollama.jsonl"
with open(outfile, "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")

print(f"✅ Done. Saved to {outfile}")
