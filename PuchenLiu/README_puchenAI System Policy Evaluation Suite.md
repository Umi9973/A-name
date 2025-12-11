# AI System Policy Evaluation Suite  
### Comprehensive Evaluation Framework for Agent Disclosure, Appeals & Remediation, Dark-Pattern Controls for Minors, and System Identity

This repository contains the full evaluation pipeline, datasets, model outputs, prompts, and scoring frameworks for analyzing AI system governance across four major evaluation branches:

1. **Automated Agent Disclosure & System Identity**
2. **Appeals and Remediation Process Evaluation**
3. **Dark-Pattern Controls for Minors**
4. **System Identity, Capabilities, and Limitations**

Multiple foundation models are evaluated, including:

- OpenAI GPT-4.1 / GPT-5.1  
- DeepSeek-V3 / DeepSeek-R1  
- Qwen-Max / Qwen3  
- DashScope API (for Qwen models)

All outputs include reproducible JSON, CSV, and TXT files.

---

##  Repository Structure

PuchenLiu/
│
├── Automated agent disclosure in user-facing interactions/
│   ├── DeepSeek-V3/
│   ├── GPT4.1/
│   ├── GPT5/
│   └── Qwen3/
│
├── Appeals and remediation process exists for affected users/
│   ├── DeepSeek/
│   ├── Qwen/
│   └── appeals_remediation_prompt.txt
│
├── Dark pattern controls for minors/
│   ├── DeepSeek/
│   ├── Qwen/
│   └── dark_pattern_prompt_latest.txt
│
├── System identity, capabilities, and limitations/
│   ├── DeepSeek-V3/
│   ├── Qwen3/
│   ├── GPT5-score/
│   └── system_identity_prompts.txt
│
├── GPT5-score/
└── README.md

---

##  Module Overview

### 1. Automated Agent Disclosure in User-Facing Interactions  
Evaluates whether AI systems properly disclose:

- AI vs human identity  
- Automation status  
- Misconception correction  
- Persistence of disclosure  
- Safety limitations  

---

### 2. Appeals & Remediation Evaluation  
Assesses whether platform policies provide meaningful rights and remedies using five authoritative frameworks:

- OECD AI Principles  
- UNGPs  
- GDPR  
- NIST AI RMF  
- Santa Clara Principles  

---

### 3. Dark-Pattern Controls for Minors  
Evaluates whether policy documents prevent manipulative UI patterns against minors, focusing on:

- Age-gating & verification  
- Parental consent  
- Transparency for minors  
- Safety escalation  
- Protection against deceptive design  

---

### 4. System Identity, Capabilities & Limitations  
Measures how clearly a model communicates:

- Identity  
- Capabilities & boundaries  
- Uncertainty  
- Safety disclaimers  
- Avoidance of overclaiming  

---

##  Running Any Evaluation

python DeepSeek-GPT4-score.py  
python Qwen-GPT4-score.py  
python GPT5-automated.py

---

##  Output Formats

JSON • CSV • TXT • PROMPT TXT

---

##  Reproducibility  
Deterministic temperature, logged prompts, version-specific folders.

---

##  Citation

Liu, Puchen. “AI System Policy Evaluation Suite…” 2025.

