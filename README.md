# AgentCare

Agentic healthcare workflow orchestrator for the Capgemini | Microsoft Agentic Industry Hackathon 2026. Automates clinical documentation, patient triage, and referral management using Microsoft AI platforms, freeing clinicians from administrative burden.

## Problem

Four systemic issues erode clinical workflow performance:

1. **Fragmentation of workflow** — Clinicians, admin, and patients all compensate for disconnected systems, leading to rework, errors, and burnout
2. **Information bottlenecks** — Critical information locked inside emails, documents, phone calls, and EMR notes — not structured, visible, or sharable
3. **Constant micro-delays** — Waiting for replies, checking portals, re-typing data, correcting errors. Individually tiny, together catastrophic
4. **Failure to surface early warnings** — No proactive highlighting of urgent triage cues, inconsistent documentation, missing referral fields, or duplicated appointments

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
index.html                              Landing page — start here
html/
  01-case-overview.html                 Pain points, challenges, KPIs, stakeholders
  02-business-process.html              Process scope, agent mapping, outcomes
  03-functional-solution.html           Workflows (triage → consultation → referral), fallbacks
  04-technical-solution.html            Architecture, platform stack, security
  05-business-case.html                 KPIs, costs, break-even, risks
  consolidated-requirements.html        Personas, user stories, scenarios, data model, NFRs
assets/                                 SVG diagrams (workflows, architecture, pain points)
context/                                Hackathon template slides and guidance materials
```

## Documentation

### Submission Pages (open `index.html` in a browser)

1. [Case Overview](html/01-case-overview.html) — Process, challenges, use case, KPIs, stakeholders
2. [Business Process Scope](html/02-business-process.html) — Process hierarchy, agent mapping, outcomes
3. [Functional Solution](html/03-functional-solution.html) — Workflows, AI-human chemistry, fallbacks
4. [Technical Solution](html/04-technical-solution.html) — Architecture, platform, security, framework alignment
5. [Business Case](html/05-business-case.html) — KPIs, cost analysis, break-even, risks

### Reference

- [Consolidated Requirements](html/consolidated-requirements.html) — Personas, user stories, scenarios, data model, NFRs, success metrics

## Current Phase

Idea submission preparation — deadline 30 March 2026. Focus on:
1. Finalising submission materials (5 slides mapped to template)
2. Refining business case with quantified KPIs
3. Validating architecture against judging criteria
4. Preparing for half-finals presentation

## TODO

- [ ] Define hackathon demo scope vs production vision
- [ ] Source or generate synthetic patient data (e.g. Synthea)
- [ ] Design clinical test scenarios for each agent
- [ ] Recruit remaining team members (team size 2-5)
- [ ] Begin Copilot Studio agent implementation post-submission
