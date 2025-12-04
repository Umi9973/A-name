from openai import OpenAI
import json
import csv
from pathlib import Path
from statistics import mean
import requests

client = OpenAI()


DOCS = [
    {
        "id": "qwen_privacy_cn",
        "title": "Qwen Product Privacy Policy (Chinese Official Version)",
        "url": "https://terms.alicdn.com/legal-agreement/terms/privacy_policy_full/20231011201849846/20231011201849846.html",
    },
    {
        "id": "qwen_user_service_agreement",
        "title": "Qwen User Service Agreement (Chinese Official Version)",
        "url": "https://terms.alicdn.com/legal-agreement/terms/c_end_product_protocol/20231011201348415/20231011201348415.html",
    },
    {
        "id": "aliyun_bailian_privacy_notice",
        "title": "Alibaba Cloud Model Studio Privacy Notice (Data Processing & Retention Mechanisms)",
        "url": "https://help.aliyun.com/zh/model-studio/privacy-notice",
    },
]


SYSTEM_PROMPT = """
You evaluate policy documents for “Appeals and Remediation Process for Affected Users.”

Your goal is to assess how well a provider (e.g., DeepSeek, Qwen, etc.) documents the existence,
clarity, and effectiveness of mechanisms that allow users to appeal decisions, raise complaints,
or seek remediation when they are harmed or negatively affected.

You must evaluate based strictly on the text of the document provided. Do NOT assume anything
that is not explicitly stated or clearly implied.

Your evaluation must follow the five most authoritative global standards in this area:
1. OECD AI Principles (2019) — contestability and redress mechanisms.
2. UN Guiding Principles on Business and Human Rights (UNGPs) — effectiveness criteria
   for grievance mechanisms (legitimate, accessible, predictable, equitable, transparent,
   rights-compatible, source of learning, based on engagement).
3. EU GDPR — data-subject rights and the right to lodge complaints and seek judicial remedies.
4. NIST AI Risk Management Framework (AI RMF) — governance, user feedback channels,
   incident reporting, and remediation pathways.
5. Santa Clara Principles (2nd edition) — notice, appeal rights, transparency, and review processes.

Using these standards, score the document on 5 dimensions (each scored 0–4):
0 = No evidence
1 = Very weak / vague mention only
2 = Partial evidence; incomplete or unclear
3 = Strong; clear statement with minor gaps
4 = Very strong; complete and aligned with best practices

The 5 dimensions:

1. Channels and Clarity
   - Are there clearly identified channels for appeals, complaints, or redress?
   - Are contact methods visible and unambiguous (email, portal, form, hotline)?
   - Does the document explicitly allow users to raise concerns about harms or rights violations?

2. Accessibility and Usability
   - Are mechanisms easy to find, understand, and use?
   - Are requirements reasonable (no excessive identity verification or burdens)?
   - Is the language user-friendly?
   - Are multiple languages or accessible formats mentioned?

3. Scope of Issues and User Rights
   - What types of issues can users appeal or complain about?
   - Are substantive rights described (access, correction, deletion, objection, portability,
     consent withdrawal)?
   - Does the provider specify categories of harms covered?

4. Procedure, Timelines, and Escalation
   - Does the document describe how complaints are handled (steps, workflow)?
   - Are there response deadlines (e.g., 15 days)?
   - Are there escalation paths (regulators, ombudspersons, arbitration, external authorities)?

5. Remedy Effectiveness and Accountability
   - What remedies are offered? Examples: correcting data, reversing decisions, restoring access,
     updating models, internal reviews.
   - Are responsibilities clearly assigned (DPO, grievance officer, compliance team)?
   - Are there commitments to continuous improvement based on complaints?
"""


def read_text(url: str) -> str:
    """Fetch raw HTML content from an official policy URL."""
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text



def evaluate_document(doc_id: str, title: str, text: str) -> dict:
    """Call GPT-5.1 to evaluate a single policy document for appeals & remediation criteria. Returns a Python dict."""

    user_prompt = f"""
You are evaluating the following official document from a provider (e.g., Qwen / Tongyi Qianwen).

Document ID: {doc_id}
Document title: {title}

Full text of the document (verbatim):
\"\"\"{text}\"\"\"

Read the document carefully and then output ONLY a single JSON object.
The JSON must match this structure (but you do NOT need to restate the schema):

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
        print(" → Overall score:", result["overall_score"])

    json_path = "qwen_appeals_eval.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✔ Saved JSON: {json_path}")

    csv_path = "qwen_appeals_eval.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "document_id",
            "document_title",
            "channels_and_clarity",
            "accessibility_and_usability",
            "scope_of_issues_and_rights",
            "procedure_timelines_and_escalation",
            "remedy_effectiveness_and_accountability",
            "overall_score",
            "overall_summary",
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

    print(f"✔ Saved CSV: {csv_path}")


if __name__ == "__main__":
    main()