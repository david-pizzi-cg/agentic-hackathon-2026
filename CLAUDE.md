# AgentCare

Agentic healthcare workflow orchestrator for the Capgemini | Microsoft Agentic Industry Hackathon 2026. Automates clinical documentation, patient triage, and referral management using Microsoft AI platforms, freeing clinicians from administrative burden.

## Repository Purpose

This repo is the **design and documentation home** for AgentCare. It holds architecture decisions, business requirements, user stories, submission materials, and any exportable artefacts.

The actual implementation lives in the Power Platform / Copilot Studio environment — agent definitions, Power Automate flows, Dataverse tables, and Copilot Studio configurations are built and maintained directly in those platforms. This repo links to and documents those assets but does not contain the runtime solution.

When implementation begins, Power Platform solution objects can be synced to source control via Dataverse Git integration (Azure DevOps only). See: https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview

## Project Structure

- `docs/architecture/` — Solution design, agent interaction diagrams, data flow, platform alignment
- `docs/requirements/` — Business requirements, personas, user journeys, data requirements
- `docs/submission/` — Hackathon idea and project submission materials
- `docs/decisions/` — Lightweight ADRs for key design choices
- `assets/` — Diagrams, screenshots, demo recordings
- `data/` — Synthetic/mock data definitions and sample datasets for Dataverse seeding

## Current Phase

Architecture and business requirements — not yet selecting technical implementation. Focus on:
1. Defining clear user stories and acceptance criteria
2. Mapping agent responsibilities and interaction patterns
3. Designing data flows with privacy constraints
4. Preparing hackathon idea submission

## Conventions

- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- Branches: `feature/<short-desc>`, `fix/<short-desc>`, `docs/<short-desc>`
- Document decisions in `docs/decisions/` as lightweight ADRs

## Don't

- Don't jump to implementation before architecture is agreed
- Don't store or log any PII/PHI in plain text — even in prototypes
- Don't design agents that make clinical decisions autonomously
- Don't commit secrets, API keys, or `.env` files
