# Business Continuity and Resilience

AgentCare supports critical clinical workflows. Failure or degradation directly impacts patient care. Design for resilience from the start.

## Criticality Classification

- **Triage Agent** — HIGH: Patient safety impact if unavailable; must have fallback to human triage
- **Clinical Decision Support Agent** — HIGH: Clinicians depend on it during consultations; must degrade gracefully (clinician can still work without it, but quality of support drops)
- **Documentation Agent** — MEDIUM: Consultation can proceed without auto-summarisation; clinician documents manually as fallback
- **Referral Agent** — MEDIUM: Referrals can be processed manually; delays acceptable short-term
- **Scheduling Agent** — MEDIUM: Appointments can be booked manually; inconvenience but not safety-critical

## Resilience Requirements

- All agents must have a defined fallback mode — what happens when the agent is unavailable?
- No agent should be a single point of failure for patient safety
- Graceful degradation over hard failure — reduced functionality is better than no functionality
- Patient-facing agents must clearly communicate when they cannot help and route to a human
- Clinician-facing agents must never block a consultation — advisory only, never gating
- Event-driven automations must have dead-letter handling — no silently dropped events
- Audit trail must persist independently of agent availability

## Monitoring and Observability

- Agent health dashboards visible to clinical leads and IT
- Alerting on agent failures, degraded response times, and error rate spikes
- Track key metrics: response latency, recommendation accuracy, fallback activation rate
- Regular review cycles to assess agent performance and refine behaviour
