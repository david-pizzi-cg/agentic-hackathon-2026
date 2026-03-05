# AgentCare

Agentic healthcare workflow orchestrator for the Capgemini | Microsoft Agentic Industry Hackathon 2026. Automates clinical documentation, patient triage, and referral management using Microsoft AI platforms, freeing clinicians from administrative burden.

## Problem

Overburdened medical staff and heavy paperwork lead to slower patient service and clinician burnout. Routine tasks like documentation, triage, appointment scheduling, and referral management consume time that should be spent on direct patient care.

## Solution

An agentic system that orchestrates multiple AI-powered assistants to handle clinical admin workflows end-to-end, with a core focus on augmenting clinical decision-making:

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

### Agent Orchestration Flow
1. Documentation Agent captures and structures the consultation
2. Structured data is passed to Clinical Decision Support Agent
3. Clinical Decision Support Agent queries knowledge bases (guidelines, formularies, patient history)
4. Recommendations are surfaced back to clinician through Copilot interface
5. Clinician accepts, modifies, or dismisses — all actions logged for audit
6. Accepted actions trigger downstream agents (Referral, Scheduling) as needed

### Knowledge Sources (to be validated)
- Clinical guidelines (e.g. NICE, BNF for drug interactions)
- Patient record summaries (mock/synthetic data for hackathon)
- Formulary and contraindication databases
- Referral pathway definitions

### Guardrails
- Agent presents evidence with sources — never states a diagnosis
- Confidence indicators on all suggestions (high/medium/low with reasoning)
- All recommendations cite the specific guideline or data point they're based on
- Clinician override is always available and logged
- No autonomous actions — every clinical suggestion requires human approval

## Platform

- Microsoft 365 Copilot (Outlook/Teams integration for clinician workflows)
- Copilot Studio (low-code agent building and orchestration)
- Power Platform (connectors, automation, and data integration)
- Dataverse (data backbone for all agent entities and mock data)
- Exact technical implementation to be determined after architecture is finalised

## Data — Dataverse Mock Data Requirements

All agents operate against synthetic data held in Dataverse. No real patient data at any stage.

- **Patient records** — Demographics, medical history, allergies, current medications
- **Clinical encounters** — Consultation summaries, diagnoses, treatment plans
- **Clinical guidelines** — Reference knowledge base (e.g. NICE pathway extracts) for decision support
- **Medications & formulary** — Drug names, interactions, contraindications
- **Referrals** — Referral requests, statuses, pathway definitions
- **Appointments** — Schedules, availability slots, booking history
- **Audit log** — Agent actions, clinician decisions, overrides

Data must be realistic enough to demonstrate agent value but entirely synthetic. Consider using established synthetic healthcare datasets (e.g. Synthea) or hand-crafted scenarios that showcase key agent interactions.

## Repository Purpose

This repo is the **design and documentation home** for AgentCare. It holds architecture decisions, business requirements, user stories, submission materials, and any exportable artefacts.

The actual implementation lives in the Power Platform / Copilot Studio environment — agent definitions, Power Automate flows, Dataverse tables, and Copilot Studio configurations are built and maintained directly in those platforms. This repo links to and documents those assets but does not contain the runtime solution.

When implementation begins, Power Platform solution objects can be synced to source control via Dataverse Git integration (Azure DevOps only). This provides version control, change tracking, and human-readable diffs for all Power Platform artefacts including Power Apps, Copilot Studio agents, Power Automate flows, and Power Pages. See: https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview

## Project Structure

- `docs/` — Architecture decisions, business requirements, user stories, design docs
- `docs/architecture/` — Solution design, agent interaction diagrams, data flow
- `docs/requirements/` — Business requirements, personas, user journeys
- `docs/submission/` — Hackathon idea and project submission materials
- `docs/decisions/` — Lightweight ADRs for key design choices
- `assets/` — Diagrams, screenshots, demo recordings
- `data/` — Synthetic/mock data definitions and sample datasets for Dataverse seeding

## Design Principles

- Each agent has a single responsibility — no monolithic "do everything" agents
- Agents communicate through a clear orchestration layer, not point-to-point
- Human-in-the-loop for all clinical decisions — agents assist, clinicians decide
- All patient data handling assumes NHS/HIPAA-level sensitivity — never log or store PII
- Design for auditability — every agent action must be traceable

## Key Personas

- **Clinician (GP/Specialist)** — Primary user; needs admin burden reduced
- **Receptionist/Admin** — Handles scheduling, referrals; benefits from automation
- **Patient** — Interacts via triage chatbot and status updates; expects clarity and reduced waiting anxiety
- **Clinical Lead** — Needs oversight dashboards and audit trails

## Interaction Model

Not all agent interactions are the same. Three distinct channels based on who initiates and how:

### Clinician-Driven (via Teams/Outlook Copilot)
- Clinician asks for decision support during or after a consultation
- Requests clinical note summaries, guideline lookups, referral drafts
- Reviews and approves/dismisses agent recommendations
- Conversational interface embedded in existing M365 workflow — no context switching

### Patient-Facing (via Copilot Studio chatbot)
- Patient initiates triage — describes symptoms, gets urgency assessment and routing
- Patient checks status of referrals, upcoming appointments, pending actions
- Proactive updates pushed to patient — "your referral has been received", "appointment confirmed"
- Reduces frustration from waiting and "what happens next?" uncertainty
- Must be empathetic, clear, non-clinical in language — no jargon

### Event-Driven / Automated (via Power Automate)
- Triggered by system events, not human action
- Examples: new lab results arrive → notify clinician and update patient; referral status changes → update patient; appointment slot opens → suggest rebooking for waiting patients; post-consultation timer → prompt clinician to review unsigned notes
- Handles the "glue" workflows that currently fall through the cracks
- All automated actions are logged and visible to clinical staff

### Channel Mapping to Agents
- Triage Agent → primarily patient-facing
- Documentation Agent → primarily clinician-driven
- Clinical Decision Support Agent → primarily clinician-driven, with event-driven triggers post-consultation
- Referral Agent → clinician-driven initiation, event-driven status updates, patient-facing status queries
- Scheduling Agent → all three channels (clinician requests, patient self-service, automated rebooking)

## Microsoft Framework Alignment

This solution must align with two key Microsoft frameworks. Reference these throughout architecture and design decisions.

### CAF: AI Agent Adoption Guidance
Reference: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/

Follow Microsoft's four-phase AI agent adoption process:
1. **Plan for agents** — Business plan (justify the use case with measurable outcomes), technology plan (use the CAF decision tree to select SaaS vs custom build), organisational readiness, data architecture
2. **Govern and secure agents** — Responsible AI policies, governance standards, risk management aligned with Microsoft's Responsible AI principles and NIST AI RMF
3. **Build agents** — Follow platform guidance for Copilot Studio and Power Platform; prepare agent environment per CAF recommendations
4. **Manage agents** — Agent lifecycle, monitoring, observability, and continuous improvement

Key CAF considerations for AgentCare:
- Classify each agent by CAF agent categories: productivity (retrieval/synthesis), task (specific actions), or autonomous (multi-step planning)
- Use the CAF technology plan decision tree to validate platform choices
- Align organisational readiness — define platform team vs workload team responsibilities
- Adopt responsible AI standards as concrete, enforceable controls, not abstract principles

### Microsoft AI Decision Framework
Reference: https://microsoft.github.io/Microsoft-AI-Decision-Framework/

Apply the BXT (Business-Experience-Technology) methodology and 9 critical questions before selecting technologies:
- **Business**: What outcome are we trying to achieve? Can we quantify the impact?
- **Experience**: What is the user interaction pattern? (Conversational, autonomous, headless?)
- **Technology**: Start with the simplest technology that meets requirements — default to SaaS (Copilot Studio) before reaching for PaaS (Foundry)

Use the Decision Framework's visual decision tree to validate:
- Clinician-facing agents → M365 Copilot / Teams interaction → likely declarative agents or Copilot Studio
- Patient-facing agents → multi-channel chatbot → likely Copilot Studio
- Event-driven automation → Power Automate triggers, potentially Copilot Studio with event triggers
- Clinical Decision Support → may need richer orchestration — evaluate whether Copilot Studio meets requirements or if Foundry/Agent Service is needed

## Business Continuity and Resilience

AgentCare supports critical clinical workflows. Failure or degradation directly impacts patient care. Design for resilience from the start.

### Criticality Classification
- **Triage Agent** — HIGH: Patient safety impact if unavailable; must have fallback to human triage
- **Clinical Decision Support Agent** — HIGH: Clinicians depend on it during consultations; must degrade gracefully (clinician can still work without it, but quality of support drops)
- **Documentation Agent** — MEDIUM: Consultation can proceed without auto-summarisation; clinician documents manually as fallback
- **Referral Agent** — MEDIUM: Referrals can be processed manually; delays acceptable short-term
- **Scheduling Agent** — MEDIUM: Appointments can be booked manually; inconvenience but not safety-critical

### Resilience Requirements
- All agents must have a defined fallback mode — what happens when the agent is unavailable?
- No agent should be a single point of failure for patient safety
- Graceful degradation over hard failure — reduced functionality is better than no functionality
- Patient-facing agents must clearly communicate when they cannot help and route to a human
- Clinician-facing agents must never block a consultation — advisory only, never gating
- Event-driven automations must have dead-letter handling — no silently dropped events
- Audit trail must persist independently of agent availability

### Monitoring and Observability
- Agent health dashboards visible to clinical leads and IT
- Alerting on agent failures, degraded response times, and error rate spikes
- Track key metrics: response latency, recommendation accuracy, fallback activation rate
- Regular review cycles to assess agent performance and refine behaviour

## Current Phase

Architecture and business requirements — not yet selecting technical implementation. Focus on:
1. Defining clear user stories and acceptance criteria
2. Mapping agent responsibilities and interaction patterns
3. Designing data flows with privacy constraints
4. Preparing hackathon idea submission

## TODO

- [ ] Dedicated Responsible AI section — align with Microsoft's six principles (fairness, reliability/safety, privacy/security, inclusiveness, transparency, accountability), not just scattered guardrails
- [ ] Define success metrics — reduction in admin time per consultation, patient wait-time satisfaction, referral turnaround time, clinician adoption rate
- [ ] Define hackathon demo scope vs production vision — what's realistic for May 7th vs the full roadmap
- [ ] Accessibility considerations — patient-facing agents must account for language, health literacy levels, assistive technology
- [ ] Evaluate Dataverse Git integration for Power Platform ALM — Azure DevOps requirement, Managed Environments setup
- [ ] Write user stories and acceptance criteria for each agent
- [ ] Create agent interaction diagrams and data flow architecture
- [ ] Design Dataverse entity model for mock data
- [ ] Source or generate synthetic patient data (e.g. Synthea)
- [ ] Design clinical test scenarios for each agent — realistic multi-turn conversations covering happy path, edge cases, and failure modes
- [ ] Create Copilot Studio Agent Evaluation test sets — predefined questions, expected responses, and test methods per agent (up to 100 test cases per set, importable via CSV)
- [ ] Define test personas — e.g. anxious patient, patient with complex multi-drug regime, GP querying rare condition, receptionist rebooking urgent referral
- [ ] Prepare hackathon idea submission materials
- [ ] Recruit remaining team members (team size 2-5)

## Conventions

- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- Branches: `feature/<short-desc>`, `fix/<short-desc>`, `docs/<short-desc>`
- Document decisions in `docs/decisions/` as lightweight ADRs

## Don't

- Don't jump to implementation before architecture is agreed
- Don't store or log any PII/PHI in plain text — even in prototypes
- Don't design agents that make clinical decisions autonomously
- Don't commit secrets, API keys, or `.env` files