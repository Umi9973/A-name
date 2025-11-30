import os
import json
import time
from datetime import datetime
from openai import OpenAI


MODEL_NAME = "gpt-4o"  
NUM_RUNS_PER_PROMPT = 3  
INPUT_FILE = "prompts.json" 
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_JSON = f"handoff_eval_{MODEL_NAME}_{TIMESTAMP}.json"
OUTPUT_TXT = f"handoff_eval_{MODEL_NAME}_{TIMESTAMP}.txt"

client = OpenAI()

def load_prompts(filename): 
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filename}。请确保它与脚本在同一目录下。")
        return []

def query_model(prompt_text, model=MODEL_NAME):
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant tasked with drafting safety policies and response templates."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7, 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def save_json_results(results, filename):
   
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

def save_txt_summary(results, filename):
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"=== Handoff Evaluation Report ===\n")
        f.write(f"Model: {MODEL_NAME}\n")
        f.write(f"Time: {datetime.now()}\n")
        f.write("="*40 + "\n\n")

        for entry in results:
            f.write(f"ID: {entry['id']}\n")
            f.write(f"Category: {entry['category']}\n")
            f.write(f"Prompt Source: {entry['source_url']}\n")
            f.write("-" * 20 + " Prompt " + "-" * 20 + "\n")
            f.write(f"{entry['prompt_text']}\n\n")
            
            for i, run in enumerate(entry['runs']):
                f.write(f"--- Run {i+1} ---\n")
                f.write(f"{run['response']}\n\n")
            f.write("="*40 + "\n\n")

def main():
    prompts = load_prompts(INPUT_FILE)
    if not prompts:
        return

    all_results = []
    print(f"开始测试 {len(prompts)} 个 Prompt，模型: {MODEL_NAME}...")

    for i, item in enumerate(prompts):
        p_id = item.get("id", "Unknown")
        p_text = item.get("prompt_text", "")
        print(f"[{i+1}/{len(prompts)}] 正在处理 {p_id} ...")

        prompt_results = {
            "id": p_id,
            "category": item.get("category"),
            "prompt_text": p_text,
            "source_url": item.get("source_url"),
            "runs": []
        }

        for run_idx in range(NUM_RUNS_PER_PROMPT):
            print(f"   -> Run {run_idx + 1}...")
            response_text = query_model(p_text)
            prompt_results["runs"].append({
                "run_id": run_idx + 1,
                "response": response_text
            })
           
            time.sleep(1)

        all_results.append(prompt_results)

    
    save_json_results(all_results, OUTPUT_JSON)
    save_txt_summary(all_results, OUTPUT_TXT)
    print(f"\n测试完成！\nJSON 结果已保存至: {OUTPUT_JSON}\n文本报告已保存至: {OUTPUT_TXT}")

if __name__ == "__main__":
    main()
