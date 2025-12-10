# Presence and prominence of safety entries

This repository contains all files required to reproduce the evidence collection and automated scoring workflow for evaluating *“Presence and prominence of safety-related interface entries (menu placement, iconography, label clarity)”* in ChatGPT as part of Assignment 3 for the DocuBase measurement process.

The analysis is based on official and non-official but credible sources and follows an **ADA (Automated Document Analysis)** methodology. The evaluation includes evidence extraction, weighted scoring using GPT-4o, and reproducible prompt design.

---

## Repository Structure

| File | Description |
|------|-------------|
| `docubase_safety_prompt.txt` | The reproducible prompt used to perform evidence collection. This is the starting point of the workflow. |
| `docu_base_safety_entries_eng.xlsx` | Evidence table compiled based on the prompt, containing long-form excerpts and URLs. Used as the input for scoring. |
| `score_docubasev1.ipynb` | Jupyter Notebook running automated scoring using GPT-4o, including weighting logic and error handling. |
| `docu_base_scoring_weighted.json` | Raw scoring output in JSON format, including individual scores, weighted calculations, and justification. |
| `docu_base_scoring_weighted.xlsx` | Converted scoring results in Excel format for direct integration into DocuBase evaluation tables or reporting. |

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
    
### Scoring Weight Justification

The scoring weights were allocated according to the relative impact of each criterion on the visibility and usability of safety-related interface entries in ChatGPT. The design emphasizes factors that determine whether users can efficiently locate, interpret, and act upon privacy or safety settings.

| Criterion | Weight | Rationale |
|----------|--------|-----------|
| **Menu Placement Visibility** | **0.25** | The most critical factor. If users cannot easily find where safety controls are located (e.g., nested under multiple menus), they are unlikely to use them. Direct discoverability is essential. |
| **Label Clarity** | **0.25** | Clear semantic expression (e.g., terminology like “Chat History & Training” or “Delete all chats”) significantly affects comprehension and correct usage. Ambiguous or indirect labels reduce safety effectiveness. |
| **Iconography Prominence** | 0.20 | Visual emphasis (e.g., toggle visibility, color cues, placement) helps users notice the control, but it is less influential than how easily the control can be located or understood. |
| **User Effort (Steps Required)** | 0.15 | The number of interactions needed (click depth) affects accessibility. However, as long as pathways are clearly communicated, it is secondary to placement and clarity. |
| **Trust & UX Confidence** | 0.15 | The perceived certainty that the control functions as intended (e.g., greyed-out history or confirmation messages) is valuable but does not directly affect discoverability or comprehension. |

**In summary, the highest weighting is assigned to functional discoverability (`Menu Placement`) and interpretability (`Label Clarity`). Visual aesthetics and interaction complexity are included but treated as supporting rather than primary factors.**

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
```

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
