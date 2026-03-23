# AgentCare

Agentic healthcare workflow orchestrator for the Capgemini | Microsoft Agentic Industry Hackathon 2026. Automates clinical documentation, patient triage, and referral management using Microsoft AI platforms, freeing clinicians from administrative burden.

## Repository Purpose

This repo is the **design and documentation home** for AgentCare. It holds architecture decisions, business requirements, user stories, submission materials, and any exportable artefacts.

The actual implementation lives in the Power Platform / Copilot Studio environment — agent definitions, Power Automate flows, Dataverse tables, and Copilot Studio configurations are built and maintained directly in those platforms. This repo links to and documents those assets but does not contain the runtime solution.

When implementation begins, Power Platform solution objects can be synced to source control via Dataverse Git integration (Azure DevOps only). See: https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview

## Project Structure

- `index.html` — Landing page (start here)
- `html/` — Submission-ready HTML pages (self-contained, one per template slide) + consolidated requirements
- `assets/` — SVG diagrams (workflows, architecture, pain points, business process scope)
- `context/` — Hackathon template slides and guidance materials

## Current Phase

Idea submission preparation — deadline 30 March 2026. Focus on:
1. Finalising submission materials (5 slides mapped to template)
2. Refining business case with quantified KPIs
3. Validating architecture against judging criteria
4. Preparing for half-finals presentation

## Conventions

- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`)
- Branches: `feature/<short-desc>`, `fix/<short-desc>`, `docs/<short-desc>`
- Document decisions as lightweight ADRs

## SVG Diagram Quality Checks

Every time an SVG diagram is created or modified:
1. **Validate XML** — run `python -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')"` to catch syntax errors
2. **Check for overlapping elements** — verify that no boxes, text, or connectors overlap by comparing y/x coordinates and dimensions
3. **Consistent styling** — headers, footers, legends, font sizes, colours, and spacing must match across all workflow SVGs
4. **No double-dashes in XML comments** — `<!-- text -->` is valid, `<!-- --- text --- -->` is NOT (breaks browser rendering silently)
5. **Arrow markers** — verify arrowheads are visible and correctly oriented (use manual polygon for vertical arrows if marker orientation fails)

## Don't

- Don't jump to implementation before architecture is agreed
- Don't store or log any PII/PHI in plain text — even in prototypes
- Don't design agents that make clinical decisions autonomously
- Don't commit secrets, API keys, or `.env` files
