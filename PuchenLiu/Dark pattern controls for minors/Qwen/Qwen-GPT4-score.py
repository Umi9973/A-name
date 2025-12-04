import requests
import csv
import json
from statistics import mean
from openai import OpenAI

client = OpenAI()


DOCS = [
    {
        "id": "qwen_privacy_cn",
        "title": "Qwen Product Privacy Policy (Chinese Version)",
        "url": "https://terms.alicdn.com/legal-agreement/terms/privacy_policy_full/20231011201849846/20231011201849846.html"
    },
    {
        "id": "qwen_user_service_agreement",
        "title": "Qwen User Service Agreement (Chinese Version)",
        "url": "https://terms.alicdn.com/legal-agreement/terms/c_end_product_protocol/20231011201348415/20231011201348415.html"
    },
    {
        "id": "aliyun_bailian_privacy_notice",
        "title": "Alibaba Cloud Model Studio Privacy Notice",
        "url": "https://help.aliyun.com/zh/model-studio/privacy-notice"
    }
]


SYSTEM_PROMPT = """
You evaluate policy documents for “Dark Pattern Controls for Minors.”

Your task is to assess how well Qwen's official documents protect minors from
manipulative design, unsafe UI patterns, inappropriate data practices, and 
lack of transparency or parental oversight.

Base your evaluation strictly on the provided text. Do NOT assume any features 
not explicitly mentioned.

Your evaluation MUST follow the **five most authoritative global standards**:

1. OECD AI Principles (2019): transparency, safety, accountability, protection of vulnerable users.
2. UNGPs (UN Guiding Principles on Business & Human Rights): children's rights, fairness, due diligence.
3. GDPR (EU Data Protection): consent, age verification, parental control, children's data safeguards.
4. NIST AI Risk Management Framework: safe design, harmful interaction prevention, user protection.
5. Santa Clara Principles (2nd ed.): transparency, notice, appeals, prevention of manipulative design.

Score the document on 5 dimensions (0–4 scale):

0 = No evidence  
1 = Very weak / vague  
2 = Partial / unclear  
3 = Strong / clear but incomplete  
4 = Best-practice level, highly protective

The five dimensions:

1. Protection Against Manipulative UI / Dark Patterns  
2. Age Verification and Parental Consent Controls  
3. Data Practices and Safeguards for Minors  
4. Transparency and Notice for Minor Users / Guardians  
5. Remedy, Appeal, and Safety Escalation Options for Minors

Your output MUST be a **single JSON object** with this schema:

{
  "document_id": "...",
  "document_title": "...",
  "scores": {
    "manipulative_ui_protection": { "score": X, "justification": "..." },
    "age_verification_controls": { "score": X, "justification": "..." },
    "child_data_protection": { "score": X, "justification": "..." },
    "transparency_for_minors": { "score": X, "justification": "..." },
    "remedy_and_escalation": { "score": X, "justification": "..." }
  },
  "overall_score": X,
  "summary": "A concise professional evaluation."
}

Return ONLY valid JSON.
"""


def fetch(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text



def evaluate(doc_id, title, text):
    MAX_CHARS = 25000
    safe_text = text[:MAX_CHARS]

    user_prompt = f"""
Evaluate the following official Qwen document for Dark Pattern Controls for Minors:

Document ID: {doc_id}
Title: {title}

The document text below may be truncated due to token limits.

Full text:
\"\"\"{safe_text}\"\"\"
"""

    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    content = completion.choices[0].message.content
    data = json.loads(content)  

    dims = [
        "manipulative_ui_protection",
        "age_verification_controls",
        "child_data_protection",
        "transparency_for_minors",
        "remedy_and_escalation",
    ]

    scores = [float(data["scores"][k]["score"]) for k in dims]
    data["overall_score"] = round(mean(scores), 2)

    return data



def main():
    results = []

    for doc in DOCS:
        print(f"\n=== Evaluating {doc['title']} ===")
        html_text = fetch(doc["url"])
        result = evaluate(doc["id"], doc["title"], html_text)
        results.append(result)
        print("→ Score:", result["overall_score"])

    with open("qwen_darkpattern_eval.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\nSaved JSON → qwen_darkpattern_eval.json")

    with open("qwen_darkpattern_eval.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "document_id",
            "document_title",
            "manipulative_ui_protection",
            "age_verification_controls",
            "child_data_protection",
            "transparency_for_minors",
            "remedy_and_escalation",
            "overall_score",
            "summary",
        ])
        for r in results:
            s = r["scores"]
            writer.writerow([
                r["document_id"],
                r["document_title"],
                s["manipulative_ui_protection"]["score"],
                s["age_verification_controls"]["score"],
                s["child_data_protection"]["score"],
                s["transparency_for_minors"]["score"],
                s["remedy_and_escalation"]["score"],
                r["overall_score"],
                r["summary"].replace("\n", " "),
            ])

    print("Saved CSV → qwen_darkpattern_eval.csv")


if __name__ == "__main__":
    main()