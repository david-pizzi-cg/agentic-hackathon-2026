# Solution Overview

An agentic system that orchestrates multiple AI-powered assistants to handle clinical admin workflows end-to-end, with a core focus on augmenting clinical decision-making.

## Agents

- **Clinical Decision Support Agent (core differentiator)** — Surfaces relevant patient history, flags drug interactions, suggests differential diagnoses, highlights applicable clinical guidelines (e.g. NICE), and recommends follow-up actions. Operates in real-time during consultations via Teams and asynchronously post-consultation to review notes against guidelines. The agent never decides — it presents evidence and the clinician applies judgement.
- **Documentation Agent** — Auto-summarises doctor-patient conversations into structured clinical notes, feeding structured data to the Clinical Decision Support Agent
- **Triage Agent** — Handles initial patient inquiries, assesses urgency, routes appropriately
- **Referral Agent** — Manages referral workflows, drafts letters, tracks status. Receives recommendations from Clinical Decision Support Agent when referral pathways may have been missed
- **Scheduling Agent** — Coordinates appointments based on urgency, availability, and patient preferences

## Clinical Decision Support — Key Scenarios

This is the primary differentiator and where the agentic architecture adds the most value.

### During Consultation (real-time, via Teams Copilot)
- Surface relevant patient history and previous encounters as conversation happens
- Flag potential drug interactions based on current medications and new prescriptions
- Suggest differential diagnoses based on reported symptoms
- Display applicable clinical guidelines (e.g. NICE pathways) relevant to the presenting condition
- Alert to allergies, contraindications, or risk factors from patient record

### Post-Consultation (asynchronous, via Outlook/Power Automate)
- Cross-reference clinical notes against relevant guidelines — flag gaps or missed steps
- Identify if a referral pathway was missed based on symptoms and diagnosis
- Suggest follow-up actions based on condition and clinical best practice
- Generate structured handoff summaries for multidisciplinary team reviews

## Agent Orchestration Flow

1. Documentation Agent captures and structures the consultation
2. Structured data is passed to Clinical Decision Support Agent
3. Clinical Decision Support Agent queries knowledge bases (guidelines, formularies, patient history)
4. Recommendations are surfaced back to clinician through Copilot interface
5. Clinician accepts, modifies, or dismisses — all actions logged for audit
6. Accepted actions trigger downstream agents (Referral, Scheduling) as needed

## Knowledge Sources (to be validated)

- Clinical guidelines (e.g. NICE, BNF for drug interactions)
- Patient record summaries (mock/synthetic data for hackathon)
- Formulary and contraindication databases
- Referral pathway definitions

## Guardrails

- Agent presents evidence with sources — never states a diagnosis
- Confidence indicators on all suggestions (high/medium/low with reasoning)
- All recommendations cite the specific guideline or data point they're based on
- Clinician override is always available and logged
- No autonomous actions — every clinical suggestion requires human approval
