import json
import re
from pathlib import Path
from typing import Dict, Any

import pandas as pd
from openai import OpenAI
from ollama import Client as OllamaClient

# ==============================
# Configuration
# ==============================

PROMPT_FILE = "proxy_representation_prompt.txt"

# Model labels (for output)
MODEL_A = "gpt-4o"
MODEL_B = "ollama_mistral"         # label shown in tables
OLLAMA_MODEL_NAME = "mistral"      # actual Ollama model name

# Output files (per-model + combined)
GPT4O_EVIDENCE_TXT = "gpt4o_proxy_representation_evidence.txt"
OLLAMA_EVIDENCE_TXT = "ollama_proxy_representation_evidence.txt"

GPT4O_JSON_OUT = "gpt4o_proxy_scoring_weighted.json"
OLLAMA_JSON_OUT = "ollama_proxy_scoring_weighted.json"

GPT4O_XLSX_OUT = "gpt4o_proxy_scoring_weighted.xlsx"
OLLAMA_XLSX_OUT = "ollama_proxy_scoring_weighted.xlsx"
COMBINED_XLSX_OUT = "proxy_representation_scoring_weighted.xlsx"

# Scoring weights (same as dataset coverage branch)
SCORING_WEIGHTS = {
    "evidence_extraction_quality": 0.25,
    "coverage_of_proxy_representation_dimensions": 0.25,
    "structure_and_formatting": 0.15,
    "relevance_and_faithfulness": 0.15,
    "identification_of_missing_disclosures": 0.10,
    "audit_usefulness": 0.10,
}

# ==============================
# Clients
# ==============================

openai_client = OpenAI()
ollama_client = OllamaClient()


# ==============================
# Helper functions
# ==============================

def read_prompt_file(path: str) -> str:
    """Read the ADA evidence-collection prompt file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Prompt file not found: {p}")
    return p.read_text(encoding="utf-8")


def build_generation_prompt(base_prompt: str) -> str:
    """
    Wrap the original proxy_representation_prompt.txt with additional
    instructions to enforce a detailed, structured evidence report.
    """
    return f"""
You are an AI ethics evaluation assistant generating an ADA-style evidence report
for the L4-2 Fairness indicator:
"Proxy or representation analysis performed where direct attributes unavailable."

You must follow the user's core instruction below, and in addition:

- Produce a detailed report (~1500–2500 words).
- Use Markdown with clear headings and tables.
- At minimum, include the following sections:
  1. Overview of Sources
  2. Evidence Table for Proxy Attributes and Representation Bias
  3. Analysis of Proxy / Representation Dimensions:
     - What counts as a proxy attribute
     - Representation bias and proxy discrimination
     - Methods for detecting proxy effects (causal graphs, correlation, latent variables, etc.)
     - Risks of indirect inference of protected attributes
     - Documented harms of proxy-based or representational bias
  4. Identified Gaps / Missing Disclosures (e.g., lack of OpenAI-specific proxy analysis).

- In the evidence table, include columns:
  - source_name
  - source_type (e.g., textbook, paper, NIST guidance, policy doc)
  - url_or_reference
  - excerpt (long verbatim quote, not paraphrased)
  - proxy_or_representation_concept (e.g., proxy discrimination, representational harm)
  - methods_or_analysis_type (e.g., causal graph, counterfactual fairness, correlation tests)
  - harms_or_risks

- Include multiple long verbatim excerpts from the requested sources:
  - Fairness and Machine Learning (Barocas, Hardt, Narayanan)
  - Counterfactual Fairness (Kusner et al., 2017)
  - NIST SP 1270
  - Any additional credible sources
- Be explicit and concrete: avoid vague statements without direct evidence.
- Do NOT speculate beyond what is stated in the documents.

Here is the core instruction you must follow (user prompt):

\"\"\"{base_prompt}\"\"\"
"""


def generate_with_gpt4o(prompt_text: str) -> str:
    """
    Use GPT-4o to generate a detailed proxy/representation evidence report.
    This is the 'document response' that will be scored later.
    """
    wrapped_prompt = build_generation_prompt(prompt_text)
    chat = openai_client.chat.completions.create(
        model=MODEL_A,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI ethics evaluation assistant generating an "
                    "ADA-style evidence report about proxy attributes and "
                    "representation analysis in fairness-aware ML systems."
                ),
            },
            {"role": "user", "content": wrapped_prompt},
        ],
        temperature=0.0,
        max_tokens=4096,
    )
    return chat.choices[0].message.content.strip()


def generate_with_ollama(prompt_text: str) -> str:
    """
    Use the local Ollama model to generate a detailed proxy/representation evidence report.

    This assumes:
      - Ollama is running locally.
      - You have already pulled the model (e.g., `ollama pull mistral`).
    """
    wrapped_prompt = build_generation_prompt(prompt_text)
    response = ollama_client.chat(
        model=OLLAMA_MODEL_NAME,
        messages=[{"role": "user", "content": wrapped_prompt}],
    )
    # Ollama Python client returns a dict with a 'message' field.
    return response["message"]["content"].strip()


def build_scoring_prompt(evidence_text: str) -> str:
    """
    Build the scoring instruction given the evidence report text.

    GPT-4o will be used as a scoring judge and must output strict JSON.
    The rubric is strict: do NOT give 5/5 unless the dimension is nearly perfect.
    """
    return f"""
You are an evaluation assistant scoring an ADA-style evidence report for the L4-2 Fairness indicator:
"Proxy or representation analysis performed where direct attributes unavailable."

You MUST score the following evidence report based on these six criteria (0–5, integers only).
Use a STRICT grading standard:

- 5 = Exceptional / near-perfect. Very rare. Only if you see almost no flaws.
- 4 = Strong but with some clear, non-trivial weaknesses.
- 3 = Reasonable / acceptable with several limitations.
- 2 = Weak / incomplete, many issues.
- 1 = Very poor.
- 0 = No evidence of this dimension.

Most realistic reports should fall in the 2–4 range. Avoid giving 5 unless you can explicitly
justify why the dimension is almost flawless.

Scoring dimensions:

1. Evidence Extraction Quality
   - Accuracy and fidelity of verbatim quotations from the cited sources.
   - Correct citation of source names, URLs, and page numbers or sections.
   - No hallucinated documents or fabricated citations.
   - Extracted text should be full sentences, not fragmented snippets.

2. Coverage of Proxy/Representation Dimensions
   - Definition and examples of proxy attributes (e.g., ZIP code → race; browsing history → gender).
   - Description of proxy discrimination and representation bias.
   - Methods for detecting proxy relationships or representational harms:
     causal graphs, counterfactual reasoning, correlation tests, variable importance,
     latent variable inference, etc.
   - Risks of indirect inference of protected characteristics.
   - Documented harms when proxies encode societal or historical biases.
   - Each of these aspects should be explicitly addressed with supporting evidence.

3. Structure & Formatting
   - Evidence is organized into clear structures (tables or sections).
   - Includes fields such as source metadata, extracted evidence, relevance to L4-2,
     and gaps/limitations.
   - Headings and layout are consistent and readable.

4. Relevance & Faithfulness
   - All statements remain grounded in the source documents.
   - No speculation or unsupported assumptions about any specific system or dataset.
   - Evidence and commentary are directly related to proxy attributes or representational bias.

5. Identification of Missing Disclosures
   - Explicitly identifies which important details are NOT disclosed in the available documentation,
     especially around whether proxy analysis has been performed by developers.
   - Example: no disclosure of causal analysis, no mention of correlation/proxy tests,
     no explicit representational harm analysis.
   - Absence claims must not contradict existing text.

6. Audit Usefulness
   - Output is traceable, citable, and verifiable.
   - Clear enough to support cross-model comparison and AI Ethics Index auditing.
   - Avoids vague or purely subjective statements.
   - Provides a usable audit trail from source to evidence to conclusion.

You must return a JSON object with this exact structure:

{{
  "scores": {{
    "evidence_extraction_quality": X,
    "coverage_of_proxy_representation_dimensions": X,
    "structure_and_formatting": X,
    "relevance_and_faithfulness": X,
    "identification_of_missing_disclosures": X,
    "audit_usefulness": X
  }},
  "justification": "Overall justification within 150 words, referring to the six dimensions and mentioning at least one concrete weakness."
}}

Where:
- X are integers from 0 to 5.
- The justification is a single string and must mention both strengths AND weaknesses.

Now, here is the full evidence report you must score (between <EVIDENCE> tags):

<EVIDENCE>
{evidence_text}
</EVIDENCE>
"""


def robust_json_parse(raw_content: str) -> Dict[str, Any]:
    """
    Attempt to parse JSON from the model's response.
    If the response contains extra text, try to extract a JSON block using regex.
    """
    try:
        return json.loads(raw_content)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", raw_content)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    raise ValueError(f"Could not parse JSON from response:\n{raw_content}")


def score_with_gpt4o(evidence_text: str) -> Dict[str, Any]:
    """
    Use GPT-4o as a scoring judge on the given evidence report.

    Returns a dict containing:
      - scores (six raw dimensions)
      - justification
      - weighted_scores_detailed
      - weighted_final_score
    """
    scoring_prompt = build_scoring_prompt(evidence_text)

    chat = openai_client.chat.completions.create(
        model=MODEL_A,  # reuse GPT-4o as the scoring model
        messages=[
            {
                "role": "system",
                "content": "You are an expert evaluator for AI fairness, proxy discrimination, and documentation quality.",
            },
            {"role": "user", "content": scoring_prompt},
        ],
        temperature=0.0,
        max_tokens=1024,
    )

    raw_content = chat.choices[0].message.content.strip()
    result_json = robust_json_parse(raw_content)

    if "scores" not in result_json:
        raise KeyError(f"No 'scores' field found in JSON:\n{result_json}")

    scores = result_json["scores"]

    # Compute weighted scores for each dimension
    detailed_weighted = {}
    for key, weight in SCORING_WEIGHTS.items():
        if key not in scores:
            raise KeyError(f"Missing score for '{key}' in model response.")
        detailed_weighted[key] = round(scores[key] * weight, 3)

    # Compute final weighted score (sum of weighted dimensions)
    weighted_final_score = round(sum(detailed_weighted.values()), 3)

    result_json["weighted_scores_detailed"] = detailed_weighted
    result_json["weighted_final_score"] = weighted_final_score

    return result_json


def scoring_result_to_df(model_label: str, scoring_result: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert a single scoring result dict into a one-row pandas DataFrame.
    """
    scores = scoring_result["scores"]
    weighted = scoring_result["weighted_scores_detailed"]
    final_score = scoring_result["weighted_final_score"]
    justification = scoring_result.get("justification", "")

    data = {
        "model_name": model_label,
        "evidence_extraction_quality": scores["evidence_extraction_quality"],
        "coverage_of_proxy_representation_dimensions": scores["coverage_of_proxy_representation_dimensions"],
        "structure_and_formatting": scores["structure_and_formatting"],
        "relevance_and_faithfulness": scores["relevance_and_faithfulness"],
        "identification_of_missing_disclosures": scores["identification_of_missing_disclosures"],
        "audit_usefulness": scores["audit_usefulness"],
        "w_evidence_extraction_quality": weighted["evidence_extraction_quality"],
        "w_coverage_of_proxy_representation_dimensions": weighted["coverage_of_proxy_representation_dimensions"],
        "w_structure_and_formatting": weighted["structure_and_formatting"],
        "w_relevance_and_faithfulness": weighted["relevance_and_faithfulness"],
        "w_identification_of_missing_disclosures": weighted["identification_of_missing_disclosures"],
        "w_audit_usefulness": weighted["audit_usefulness"],
        "weighted_final_score": final_score,
        "justification": justification,
    }

    return pd.DataFrame([data])


# ==============================
# Main pipeline
# ==============================

def main() -> None:
    """Main entry point for the script."""
    # 1. Read proxy/representation evidence-collection prompt
    prompt_text = read_prompt_file(PROMPT_FILE)

    # 2. Generate evidence reports from two models
    print("🔹 Generating proxy/representation evidence report with GPT-4o...")
    gpt4o_evidence = generate_with_gpt4o(prompt_text)

    print("🔹 Generating proxy/representation evidence report with Ollama model...")
    ollama_evidence = generate_with_ollama(prompt_text)

    # Save raw evidence for inspection
    Path(GPT4O_EVIDENCE_TXT).write_text(gpt4o_evidence, encoding="utf-8")
    Path(OLLAMA_EVIDENCE_TXT).write_text(ollama_evidence, encoding="utf-8")

    # 3. Score each evidence report using GPT-4o as judge
    print("🔹 Scoring GPT-4o proxy/representation evidence report...")
    gpt4o_scoring = score_with_gpt4o(gpt4o_evidence)

    print("🔹 Scoring Ollama proxy/representation evidence report...")
    ollama_scoring = score_with_gpt4o(ollama_evidence)

    # 4. Save scoring results as JSON
    Path(GPT4O_JSON_OUT).write_text(
        json.dumps(gpt4o_scoring, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    Path(OLLAMA_JSON_OUT).write_text(
        json.dumps(ollama_scoring, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 5. Export to Excel (per-model)
    print("🔹 Exporting GPT-4o proxy scoring to Excel...")
    df_gpt4o = scoring_result_to_df(MODEL_A, gpt4o_scoring)
    df_gpt4o.to_excel(GPT4O_XLSX_OUT, index=False)

    print("🔹 Exporting Ollama proxy scoring to Excel...")
    df_ollama = scoring_result_to_df(MODEL_B, ollama_scoring)
    df_ollama.to_excel(OLLAMA_XLSX_OUT, index=False)

    # 6. Export combined Excel (two models in one file)
    print("🔹 Exporting combined proxy/representation scoring to Excel...")
    df_combined = pd.concat([df_gpt4o, df_ollama], ignore_index=True)
    df_combined.to_excel(COMBINED_XLSX_OUT, index=False)

    print("✅ Done. Generated files:")
    print(f"  - {GPT4O_EVIDENCE_TXT}")
    print(f"  - {OLLAMA_EVIDENCE_TXT}")
    print(f"  - {GPT4O_JSON_OUT}")
    print(f"  - {OLLAMA_JSON_OUT}")
    print(f"  - {GPT4O_XLSX_OUT}")
    print(f"  - {OLLAMA_XLSX_OUT}")
    print(f"  - {COMBINED_XLSX_OUT}")


if __name__ == "__main__":
    main()
