# Platform and Microsoft Framework Alignment

## Platform Stack

- Microsoft 365 Copilot (Outlook/Teams integration for clinician workflows)
- Copilot Studio (low-code agent building and orchestration)
- Power Platform (connectors, automation, and data integration)
- Dataverse (data backbone for all agent entities and mock data)
- Exact technical implementation to be determined after architecture is finalised

## CAF: AI Agent Adoption Guidance

Reference: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/

Follow Microsoft's four-phase AI agent adoption process:
1. **Plan for agents** — Business plan (justify the use case with measurable outcomes), technology plan (use the CAF decision tree to select SaaS vs custom build), organisational readiness, data architecture
2. **Govern and secure agents** — Responsible AI policies, governance standards, risk management aligned with Microsoft's Responsible AI principles and NIST AI RMF
3. **Build agents** — Follow platform guidance for Copilot Studio and Power Platform; prepare agent environment per CAF recommendations
4. **Manage agents** — Agent lifecycle, monitoring, observability, and continuous improvement

### Key CAF Considerations for AgentCare

- Classify each agent by CAF agent categories: productivity (retrieval/synthesis), task (specific actions), or autonomous (multi-step planning)
- Use the CAF technology plan decision tree to validate platform choices
- Align organisational readiness — define platform team vs workload team responsibilities
- Adopt responsible AI standards as concrete, enforceable controls, not abstract principles

## Microsoft AI Decision Framework

Reference: https://microsoft.github.io/Microsoft-AI-Decision-Framework/

Apply the BXT (Business-Experience-Technology) methodology and 9 critical questions before selecting technologies:
- **Business**: What outcome are we trying to achieve? Can we quantify the impact?
- **Experience**: What is the user interaction pattern? (Conversational, autonomous, headless?)
- **Technology**: Start with the simplest technology that meets requirements — default to SaaS (Copilot Studio) before reaching for PaaS (Foundry)

### Decision Framework Validation

- Clinician-facing agents → M365 Copilot / Teams interaction → likely declarative agents or Copilot Studio
- Patient-facing agents → multi-channel chatbot → likely Copilot Studio
- Event-driven automation → Power Automate triggers, potentially Copilot Studio with event triggers
- Clinical Decision Support → may need richer orchestration — evaluate whether Copilot Studio meets requirements or if Foundry/Agent Service is needed
