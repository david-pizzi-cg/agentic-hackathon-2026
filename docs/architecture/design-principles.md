# Design Principles

- **Single responsibility** — Each agent has a single responsibility — no monolithic "do everything" agents
- **Orchestrated communication** — Agents communicate through a clear orchestration layer, not point-to-point
- **Human-in-the-loop** — Human-in-the-loop for all clinical decisions — agents assist, clinicians decide
- **Data sensitivity** — All patient data handling assumes NHS/HIPAA-level sensitivity — never log or store PII
- **Auditability** — Design for auditability — every agent action must be traceable
