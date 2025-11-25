# DocuBase Safety Evaluation – Evidence Collection and Automated Scoring

This repository contains all files required to reproduce the evidence collection and automated scoring workflow for evaluating *“Presence and prominence of safety-related interface entries (menu placement, iconography, label clarity)”* in ChatGPT as part of Assignment 3 for the DocuBase measurement process.

The analysis is based on official and non-official but credible sources and follows an **ADA (Automated Document Analysis)** methodology. The evaluation includes evidence extraction, weighted scoring using GPT-4o, and reproducible prompt design.

---

## Repository Structure

| File | Description |
|------|-------------|
| `docu_base_safety_entries_eng.xlsx` | Source evidence table (English) used for scoring. Contains full excerpts and URLs. |
| `docu_base_scoring_weighted.json` | JSON output from automated scoring, including raw scores, weighted breakdown, final score, and justification for each evidence item. |
| `docu_base_scoring_weighted.xlsx` | Scoring results exported to Excel format for easier review and integration into DocuBase tables. |
| `docubase_safety_prompt.txt` | Reproducible prompt used for evidence collection (search and extraction phase). Designed to ensure consistency and traceability in DocuBase evaluations. |
| `score_docubasev1.ipynb` | Jupyter Notebook containing the full code implementation for automated scoring using GPT-4o (with weighted evaluation and error handling). |

---

## Workflow Overview

### 1. Evidence Collection
- Based on instruction: *“Search and compile information related to prominence of safety entries in ChatGPT (menu placement, iconography, label clarity)”*.
- All sources are evaluated for UI accessibility, visibility, and clarity of safety-related controls (e.g., Data Controls, Chat History & Training toggle).
- Deliverable: `docu_base_safety_entries_eng.xlsx`

### 2. Scoring Design
- Scored using five criteria:  
  - Menu Placement Visibility  
  - Iconography Prominence  
  - Label Clarity  
  - User Effort (steps required)  
  - Trust & UX Confidence  
- Scoring weight distribution:
  - Menu Placement Visibility: **0.25**  
  - Iconography Prominence: **0.20**  
  - Label Clarity: **0.25**  
  - User Effort: **0.15**  
  - Trust & UX Confidence: **0.15**

### 3. Automated Scoring Execution
- Implemented in `score_docubasev1.ipynb` using GPT-4o.
- Includes:
  - Weighted score calculation  
  - JSON-safe parsing  
  - Extraction of full raw and weighted score breakdown

- Output:
  - JSON: `docu_base_scoring_weighted.json`
  - Excel: `docu_base_scoring_weighted.xlsx`

### 4. Prompt Reproducibility
- The file `docubase_safety_prompt.txt` stores the exact collection prompt used.
- Used to ensure the evidence extraction process is repeatable in future DocuBase evaluations or audits.

---

## Instructions for Reproduction

### Prerequisites
- Python 3.10 or higher  
- OpenAI Python SDK **version ≥ 1.0.0**  
- Environment variable `OPENAI_API_KEY` configured

### Setup Commands

```bash
pip install openai pandas
export OPENAI_API_KEY="your_key_here"
Then open and run:

score_docubasev1.ipynb

---

## Notes on Usage

The generated outputs include:

- **`scores`**: raw criterion scores (1–5)
- **`weighted_scores_detailed`**: per-dimension score multiplied by its assigned weight
- **`weighted_final_score`**: total weighted score calculated as the sum of weighted dimensions
- **`justification`**: concise rationale (≤70 words) for the assigned score

The file **`docu_base_scoring_weighted.xlsx`** can be directly incorporated into DocuBase evidence and scoring tables for evaluation reporting.

---

## Recommended Next Steps

- Integrate `docu_base_scoring_weighted.xlsx` into the scoring matrix of the Assignment 3 DocuBase evaluation.
- Use `docubase_safety_prompt.txt` to document the reproducibility of the evidence acquisition phase.
- Include a short methodology summary referencing this repository to demonstrate evaluation traceability, stability, and adherence to DocuBase measurement standards.

---

## Contact or Support

For methodology or reproducibility inquiries, refer to the DocuBase evaluation framework documentation or contact the designated evaluation designer responsible for this branch.

---

This repository serves as the complete record of:

- Prompt design for evidence collection  
- Evidence extraction process (ADA methodology)  
- Automated scoring logic implementation (GPT-4o)  
- Final scoring outputs and data transformation artifacts
