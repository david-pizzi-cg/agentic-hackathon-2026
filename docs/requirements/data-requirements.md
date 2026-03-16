# Data Requirements — Dataverse Mock Data

All agents operate against synthetic data held in Dataverse. No real patient data at any stage.

## Entity Types

- **Patient records** — Demographics, medical history, allergies, current medications
- **Clinical encounters** — Consultation summaries, diagnoses, treatment plans
- **Clinical guidelines** — Reference knowledge base (e.g. NICE pathway extracts) for decision support
- **Medications & formulary** — Drug names, interactions, contraindications
- **Referrals** — Referral requests, statuses, pathway definitions
- **Appointments** — Schedules, availability slots, booking history
- **Audit log** — Agent actions, clinician decisions, overrides

## Synthetic Data Approach

Data must be realistic enough to demonstrate agent value but entirely synthetic. Consider using established synthetic healthcare datasets (e.g. Synthea) or hand-crafted scenarios that showcase key agent interactions.
