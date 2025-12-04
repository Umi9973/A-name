from openai import OpenAI
import json
import csv
from pathlib import Path
from statistics import mean
import requests

client = OpenAI()

DOCS = [
    {
        "id": "deepseek_privacy_zh",
        "title": "DeepSeek Privacy Policy (Chinese Version)",
        "url": "https://cdn.deepseek.com/policies/zh-CN/deepseek-privacy-policy.html",
    },
    {
        "id": "deepseek_privacy_en",
        "title": "DeepSeek Privacy Policy (EN)",
        "url": "https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html",
    },
    {
        "id": "deepseek_terms_en",
        "title": "DeepSeek Terms of Use (EN)",
        "url": "https://cdn.deepseek.com/policies/en-US/deepseek-terms-of-use.html",
    },
]

EVAL_SCHEMA = {
    "name": "appeals_and_remediation_evaluation",
    "schema": {
        "type": "object",
        "properties": {
            "document_id": {"type": "string"},
            "document_title": {"type": "string"},
            "scores": {
                "type": "object",
                "properties": {
                    "channels_and_clarity": {
                        "type": "object",
                        "properties": {"score": {"type": "number"},
                                       "justification": {"type": "string"}},
                        "required": ["score", "justification"],
                    },
                    "accessibility_and_usability": {
                        "type": "object",
                        "properties": {"score": {"type": "number"},
                                       "justification": {"type": "string"}},
                        "required": ["score", "justification"],
                    },
                    "scope_of_issues_and_rights": {
                        "type": "object",
                        "properties": {"score": {"type": "number"},
                                       "justification": {"type": "string"}},
                        "required": ["score", "justification"],
                    },
                    "procedure_timelines_and_escalation": {
                        "type": "object",
                        "properties": {"score": {"type": "number"},
                                       "justification": {"type": "string"}},
                        "required": ["score", "justification"],
                    },
                    "remedy_effectiveness_and_accountability": {
                        "type": "object",
                        "properties": {"score": {"type": "number"},
                                       "justification": {"type": "string"}},
                        "required": ["score", "justification"],
                    },
                },
                "required": [
                    "channels_and_clarity",
                    "accessibility_and_usability",
                    "scope_of_issues_and_rights",
                    "procedure_timelines_and_escalation",
                    "remedy_effectiveness_and_accountability",
                ],
            },
            "overall_score": {"type": "number"},
            "overall_summary": {"type": "string"},
        },
        "required": ["document_id", "document_title", "scores",
                     "overall_score", "overall_summary"],
    },
    "strict": True,
}

SYSTEM_PROMPT = """
You evaluate policy documents for appeals & remediation mechanisms.
Use OECD AI Principles, UNGPs, GDPR, NIST AI RMF, and Santa Clara Principles.
Score 5 dimensions: 0–4 (0=no evidence, 4=best practice).
Return structured JSON only.
"""

def read_text(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def evaluate_document(doc_id: str, title: str, text: str):
    """Call GPT‑5 API to evaluate one policy document for appeals & remediation criteria.
    Returns a Python dict."""

    user_prompt = f"""
You are evaluating the following official document from a provider (e.g., DeepSeek).

Document ID: {doc_id}
Document title: {title}

Full text of the document (verbatim):
\"\"\"{text}\"\"\"

Read the document carefully and then output **only** a single JSON object.
The JSON must match this schema (but you do NOT need to restate the schema):
- document_id: string
- document_title: string
- scores: object with keys
    - channels_and_clarity: {{ score: number, justification: string }}
    - accessibility_and_usability: {{ score: number, justification: string }}
    - scope_of_issues_and_rights: {{ score: number, justification: string }}
    - procedure_timelines_and_escalation: {{ score: number, justification: string }}
    - remedy_effectiveness_and_accountability: {{ score: number, justification: string }}
- overall_score: number
- overall_summary: string

All scores must be between 0 and 4 (inclusive). Do not include any extra keys.
Return ONLY valid JSON, no explanations or markdown.
"""

    completion = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    content = completion.choices[0].message.content

    data = json.loads(content)

    data["document_id"] = doc_id
    data["document_title"] = title

    scores_obj = data["scores"]
    dims = [
        "channels_and_clarity",
        "accessibility_and_usability",
        "scope_of_issues_and_rights",
        "procedure_timelines_and_escalation",
        "remedy_effectiveness_and_accountability",
    ]
    dim_scores = [float(scores_obj[d]["score"]) for d in dims]
    data["overall_score"] = round(mean(dim_scores), 2)

    return data


def main():
    results = []

    for doc in DOCS:
        print(f"\n=== Evaluating {doc['title']} ===")
        text = read_text(doc["url"])
        result = evaluate_document(doc["id"], doc["title"], text)
        results.append(result)
        print(" → Score:", result["overall_score"])

    with open("deepseek_appeals_eval.json", "w",
              encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\n✔ Saved JSON: deepseek_appeals_eval.json")

    with open("deepseek_appeals_eval.csv", "w",
              encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "document_id", "document_title",
            "channels_and_clarity",
            "accessibility_and_usability",
            "scope_of_issues_and_rights",
            "procedure_timelines_and_escalation",
            "remedy_effectiveness_and_accountability",
            "overall_score", "overall_summary",
        ])
        for r in results:
            s = r["scores"]
            writer.writerow([
                r["document_id"],
                r["document_title"],
                s["channels_and_clarity"]["score"],
                s["accessibility_and_usability"]["score"],
                s["scope_of_issues_and_rights"]["score"],
                s["procedure_timelines_and_escalation"]["score"],
                s["remedy_effectiveness_and_accountability"]["score"],
                r["overall_score"],
                r["overall_summary"].replace("\n", " "),
            ])
    print("✔ Saved CSV: deepseek_appeals_eval.csv")


if __name__ == "__main__":
    main()