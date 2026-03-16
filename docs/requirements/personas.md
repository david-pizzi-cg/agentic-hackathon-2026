# Personas and Interaction Model

## Key Personas

- **Clinician (GP/Specialist)** — Primary user; needs admin burden reduced
- **Receptionist/Admin** — Handles scheduling, referrals; benefits from automation
- **Patient** — Interacts via triage chatbot and status updates; expects clarity and reduced waiting anxiety
- **Clinical Lead** — Needs oversight dashboards and audit trails

## Interaction Model

Not all agent interactions are the same. Three distinct channels based on who initiates and how.

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

## Channel Mapping to Agents

- Triage Agent → primarily patient-facing
- Documentation Agent → primarily clinician-driven
- Clinical Decision Support Agent → primarily clinician-driven, with event-driven triggers post-consultation
- Referral Agent → clinician-driven initiation, event-driven status updates, patient-facing status queries
- Scheduling Agent → all three channels (clinician requests, patient self-service, automated rebooking)
