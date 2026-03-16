# AgentCare

Agentic healthcare workflow orchestrator for the Capgemini | Microsoft Agentic Industry Hackathon 2026. Automates clinical documentation, patient triage, and referral management using Microsoft AI platforms, freeing clinicians from administrative burden.

## Problem

Overburdened medical staff and heavy paperwork lead to slower patient service and clinician burnout. Routine tasks like documentation, triage, appointment scheduling, and referral management consume time that should be spent on direct patient care.

## Solution

An agentic system that orchestrates multiple AI-powered assistants to handle clinical admin workflows end-to-end, with a core focus on augmenting clinical decision-making:

| Agent | Role |
|---|---|
| **Clinical Decision Support** (core differentiator) | Surfaces patient history, flags drug interactions, suggests differential diagnoses, highlights clinical guidelines |
| **Documentation** | Auto-summarises consultations into structured clinical notes |
| **Triage** | Handles initial patient inquiries, assesses urgency, routes appropriately |
| **Referral** | Manages referral workflows, drafts letters, tracks status |
| **Scheduling** | Coordinates appointments based on urgency, availability, and preferences |

The system never makes clinical decisions — it presents evidence and the clinician applies judgement.

## Platform

- Microsoft 365 Copilot (Teams/Outlook integration)
- Copilot Studio (agent building and orchestration)
- Power Platform (connectors, automation, data integration)
- Dataverse (data backbone)

## Repository Structure

This repo is the **design and documentation home** for AgentCare. The actual implementation lives in the Power Platform / Copilot Studio environment.

```
docs/
  architecture/       Solution design, platform alignment, resilience, design principles
  requirements/       Personas, interaction model, data requirements
  submission/         Hackathon idea and project submission materials
  decisions/          Lightweight ADRs for key design choices
assets/               Diagrams, screenshots, demo recordings
data/                 Synthetic/mock data definitions and sample datasets
```

## Documentation

- [Solution Overview](docs/architecture/solution-overview.md) — Agents, orchestration flow, guardrails
- [Platform and Framework Alignment](docs/architecture/platform.md) — Microsoft CAF and AI Decision Framework
- [Resilience](docs/architecture/resilience.md) — Criticality classification, fallback modes
- [Design Principles](docs/architecture/design-principles.md) — Core architectural principles
- [Personas and Interaction Model](docs/requirements/personas.md) — Who uses the system and how
- [Data Requirements](docs/requirements/data-requirements.md) — Dataverse entities and synthetic data

## Current Phase

Architecture and business requirements — not yet selecting technical implementation. Focus on:
1. Defining clear user stories and acceptance criteria
2. Mapping agent responsibilities and interaction patterns
3. Designing data flows with privacy constraints
4. Preparing hackathon idea submission

## TODO

- [ ] Dedicated Responsible AI section
- [ ] Define success metrics
- [ ] Define hackathon demo scope vs production vision
- [ ] Accessibility considerations
- [ ] Evaluate Dataverse Git integration for Power Platform ALM
- [ ] Write user stories and acceptance criteria for each agent
- [ ] Create agent interaction diagrams and data flow architecture
- [ ] Design Dataverse entity model for mock data
- [ ] Source or generate synthetic patient data (e.g. Synthea)
- [ ] Design clinical test scenarios for each agent
- [ ] Create Copilot Studio Agent Evaluation test sets
- [ ] Define test personas
- [ ] Prepare hackathon idea submission materials
- [ ] Recruit remaining team members (team size 2-5)
