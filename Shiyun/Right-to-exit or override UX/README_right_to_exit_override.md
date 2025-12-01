
# DocuBase Safety Evaluation – Right to Exit or Override UX

This repository contains all files required to reproduce the evidence collection and automated scoring workflow for evaluating **“Right to Exit or Override UX (withdrawal of consent, data deletion, override of prior permissions)”** in AI systems (ChatGPT, Claude).  
The branch follows the **ADA (Automated Document Analysis)** methodology and is part of Assignment 3 for the DocuBase measurement process.

The evaluation analyzes official documentation, privacy centers, regulatory guidance, and credible technical analysis to measure the clarity, accessibility, and effectiveness of exit-related user controls.

---

## Repository Structure

| File | Description |
|------|-------------|
| **`right_to_exit_override_prompt.txt`** | The reproducible prompt used for collecting evidence regarding exit/override mechanisms. This is the starting point of the workflow. |
| **`right_to_exit_override_references_rich_excerpt.xlsx`** | Evidence table with long-form excerpts and URLs from official and reputable sources. Used as the input for automated scoring. |
| **`score_right_to_exit_v1.ipynb`** | Jupyter Notebook performing automated scoring using GPT-4o (and optionally Claude models), with weighting logic and robust JSON parsing. |
| **`right_to_exit_scoring_weighted.json`** | Raw scoring results in JSON format, including unweighted scores, detailed weighted breakdowns, and scoring justifications. |
| **`right_to_exit_scoring_weighted.xlsx`** | Scoring output in Excel format for direct integration into DocuBase evaluation deliverables. |

---

## Workflow Overview

### **1. Evidence Collection**
Using the prompt in `right_to_exit_override_prompt.txt`, sources were compiled on:

- Account deletion (full exit)
- Opt-out of data retention
- Withdraw consent for training
- Temporary chat / non-retained chat modes
- Deletion of conversation history
- Override of previous privacy or data-sharing preferences

Deliverable:  
**`right_to_exit_override_references_rich_excerpt.xlsx`**

---

## 2. Scoring Design

Right-to-exit UX is scored along **five core criteria**, each 0–5 points:

| Criterion | Description | Weight |
|----------|-------------|--------|
| **Visibility & Accessibility** | How easy it is to find exit/override controls. | **0.25** |
| **Clarity of Labels** | Whether users can easily understand the actions. | **0.20** |
| **Effectiveness of Mechanism** | Whether the action is actually honored. | **0.30** |
| **Friction & Dark Patterns** | Whether obstacles exist. | **0.15** |
| **Regulatory Alignment** | Alignment with privacy laws. | **0.10** |

## Scoring Weight Justification

The scoring weights were allocated according to the relative impact of each criterion on the visibility and usability of exit-related interface controls. The design emphasizes factors that determine whether users can efficiently locate, interpret, and act upon privacy or consent-related settings.

| Criterion | Weight | Rationale |
|----------|--------|-----------|
| **Visibility & Accessibility** | **0.25** | The most critical factor. If users cannot easily find where exit or override controls are located (e.g., nested under multiple menus), they are unlikely to use them. Direct discoverability is essential. |
| **Clarity of Labels** | **0.20** | Clear semantic expression (e.g., terminology like “Delete all chats” or “Disable training”) significantly affects comprehension and correct usage. Ambiguous or indirect labels reduce effectiveness. |
| **Effectiveness of Mechanism** | **0.30** | The mechanism must reliably honor the user’s intention—deletion must delete, opt-out must disable future training use. This is the most outcome-critical dimension. |
| **Friction & Dark Patterns** | **0.15** | The number of interactions, delays, discouraging language, or procedural blockers affects accessibility. As long as pathways are understandable, this factor is secondary to placement and clarity. |
| **Regulatory Alignment** | **0.10** | Whether the system follows privacy obligations (e.g., GDPR erasure timelines, consent withdrawal rights). Essential for compliance but less influential on UX discoverability. |

---

## 3. Automated Scoring Execution

Implemented in:

**`score_right_to_exit_v1.ipynb`**

Capabilities include:

- Batch scoring using GPT-4o  
- JSON-safe parsing  
- Automatic weighted scoring  
- Detailed score breakdowns  
- 70‑word justification generation

Outputs:

- **JSON:** `right_to_exit_scoring_weighted.json`  
- **Excel:** `right_to_exit_scoring_weighted.xlsx`

---

## 4. Prompt Reproducibility

Stored in:

**`right_to_exit_override_prompt.txt`**

---

## Instructions for Reproduction

### Prerequisites

```bash
export OPENAI_API_KEY="your_key_here"
```

Run all cells in:

```
score_right_to_exit_v1.ipynb
```

---

## Notes on Output Interpretation

Each row outputs:

- `"scores"`  
- `"weighted_scores_detailed"`  
- `"weighted_final_score"`  
- `"justification"`  
- Metadata (source, ID, URL)

---

## Recommended Next Steps

- Integrate scoring XLSX into the Ethics Index  
- Compare GPT vs Claude performance  
- Re-run pipeline periodically for updates  

---

