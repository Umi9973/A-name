import os
import json
from pathlib import Path
from ollama import Client as OllamaClient

# === CONFIGURATION ===
NUM_GENERATIONS = 3
PROMPT_FILE = "avoid_stereotyping_prompts_en.json"
OUTPUT_DIR = Path("outputs")

# Two different local models (both run through Ollama)
MODEL_A = "ollama_llama3"
MODEL_B = "ollama_mistral"

# The actual model names used by Ollama
OLLAMA_MODEL_A_NAME = "llama3"      # Make sure you ran: ollama pull llama3
OLLAMA_MODEL_B_NAME = "mistral"     # Make sure you ran: ollama pull mistral

# === SETUP ===
ollama_client = OllamaClient()
OUTPUT_DIR.mkdir(exist_ok=True)

with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)


def generate_with_model_a(prompt_text):
    """
    Generate a response using Ollama Model A (llama3).
    """
    response = ollama_client.chat(
        model=OLLAMA_MODEL_A_NAME,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response["message"]["content"].strip()


def generate_with_model_b(prompt_text):
    """
    Generate a response using Ollama Model B (mistral).
    """
    response = ollama_client.chat(
        model=OLLAMA_MODEL_B_NAME,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    return response["message"]["content"].strip()


results = []

for prompt in prompts:
    prompt_id = prompt["id"]
    prompt_text = prompt["prompt_text"]

    for i in range(NUM_GENERATIONS):
        # --- Model A ---
        print(f"Generating [Model A: {MODEL_A}] Prompt {prompt_id}, Iteration {i+1}")
        response_a = generate_with_model_a(prompt_text)
        results.append({
            "prompt_id": prompt_id,
            "model": MODEL_A,
            "gen_id": f"{prompt_id}_modelA_gen{i+1}",
            "response": response_a
        })

        # --- Model B ---
        print(f"Generating [Model B: {MODEL_B}] Prompt {prompt_id}, Iteration {i+1}")
        response_b = generate_with_model_b(prompt_text)
        results.append({
            "prompt_id": prompt_id,
            "model": MODEL_B,
            "gen_id": f"{prompt_id}_modelB_gen{i+1}",
            "response": response_b
        })

# Save all generations as JSONL
outfile = OUTPUT_DIR / "responses_ollama_llama3_vs_mistral.jsonl"
with open(outfile, "w", encoding="utf-8") as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"✅ Done. Saved to {outfile}")
