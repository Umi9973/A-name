Provides Health Information with Proper Boundaries and Referrals

L4_HAI_HealthBoundaries

This repository contains the evaluation files for the “Provides health information with proper boundaries and referrals” branch within the L4 Fairness & Safety dimension of the AI Ethics Index measurement project.

The branch evaluates whether AI systems:

Provide health information safely and non-diagnostically

Respect clinical boundaries

Identify high-risk cases

Provide proper escalation and referrals

The scoring framework follows the ADA (Automated Document Analysis) methodology and incorporates evidence from health-ethics and digital-health governance standards.

Repository Structure
File	Description
prompts_health.json	Structured prompt set used for evaluating model responses on health-information safety and referral boundaries.
deepseek_eval_results.json	Raw evaluation outputs from DeepSeek on the health-boundary tasks.
deepseek_eval_results_graded.json	Graded ADA-style scoring of DeepSeek’s responses.
grok_eval_results.json	Raw evaluation outputs from Grok for all health-related scenarios.
grok_eval_results_graded.json	Graded ADA-style scoring of Grok’s responses.
health_handoff_metrics.json	Consolidated metrics summarizing model performance on health handoffs, escalation, and referral adequacy.
README.md	Documentation for methodology, evidence collection, and scoring workflow.
Workflow Overview

The analysis follows three ADA methodological stages:

1. Evidence Collection

Using prompts_health.json, models are evaluated on:

Non-diagnostic health information delivery

Safety boundaries (scope of practice, uncertainty, disclaimers)

Escalation for high-risk symptoms

Safe referrals (emergency, clinical, community resources)

Model outputs are stored in:

deepseek_eval_results.json

grok_eval_results.json

2. Automated ADA Scoring

Each model’s output is graded with a multi-dimension rubric evaluating:

Evidence Quality

Boundary Adherence

Referral Appropriateness

Risk-sensitivity

Missing Disclosures

Audit Usefulness

Results:

deepseek_eval_results_graded.json

grok_eval_results_graded.json

3. Metrics Consolidation

health_handoff_metrics.json aggregates:

Boundary-compliance scores

Safety failures

Referral accuracy

Overall L4-branch scoring signals

Used for AI-Ethics Index reporting and cross-model comparison.

Usage

All evaluation and scoring outputs are already included.
You may extend the pipeline by adding new prompts or integrating additional models.
