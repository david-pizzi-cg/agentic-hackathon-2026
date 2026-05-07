"""Azure Function endpoints for the AgentCare diagnostic engine.

Deploy to Azure Function App: AgentCareDiagnosticFunction
Runtime: Python 3.11, v2 programming model
"""

import json
import logging
import math
import secrets
import time
from pathlib import Path

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# ── Data loading ─────────────────────────────────────────────────────

DATA_DIR = Path(__file__).resolve().parent / "data"


def _load_json(filename: str) -> dict:
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Diagnostic Engine (inlined) ──────────────────────────────────────

class DiagnosticEngine:
    """Stateless helper that scores conditions and selects next questions."""

    def __init__(self):
        self.conditions = _load_json("release_conditions.json")
        self.evidences = _load_json("release_evidences.json")

        self.evidence_to_conditions: dict[str, set[str]] = {}
        for cond_name, cond in self.conditions.items():
            all_evi = set(cond.get("symptoms", {})) | set(cond.get("antecedents", {}))
            for evi_id in all_evi:
                self.evidence_to_conditions.setdefault(evi_id, set()).add(cond_name)

        self.condition_evidences: dict[str, set[str]] = {}
        for cond_name, cond in self.conditions.items():
            self.condition_evidences[cond_name] = set(
                cond.get("symptoms", {})
            ) | set(cond.get("antecedents", {}))

        self.evidence_groups: dict[str, list[str]] = {}
        for evi_id, evi in self.evidences.items():
            parent = evi.get("code_question", evi_id)
            self.evidence_groups.setdefault(parent, []).append(evi_id)

    def score_conditions(self, present: set[str], absent: set[str]) -> list[tuple[str, float]]:
        scores: dict[str, float] = {}
        for cond_name, cond_evis in self.condition_evidences.items():
            if not cond_evis:
                continue
            match = len(present & cond_evis)
            contradict = len(absent & cond_evis)
            total = len(cond_evis)
            raw = (match + 0.5) / (total + 1.0) * (1.0 / (1.0 + contradict))
            scores[cond_name] = raw

        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def get_differential(self, present: set[str], absent: set[str], top_n: int = 5) -> list[dict]:
        ranked = self.score_conditions(present, absent)
        results = []
        for cond_name, prob in ranked[:top_n]:
            cond = self.conditions[cond_name]
            results.append({
                "condition": cond_name,
                "probability": round(prob, 4),
                "severity": cond.get("severity", 5),
                "icd10": cond.get("icd10-id", ""),
            })
        return results

    def get_askable_evidences(self, already_asked: set[str], present: set[str], absent: set[str]) -> list[str]:
        negative_parents: set[str] = set()
        for evi_id in absent:
            evi = self.evidences.get(evi_id)
            if evi and evi.get("code_question") == evi_id:
                negative_parents.add(evi_id)

        askable = []
        for evi_id, evi in self.evidences.items():
            if evi_id in already_asked:
                continue
            parent = evi.get("code_question", evi_id)
            if parent != evi_id and parent in negative_parents:
                continue
            if parent != evi_id and parent not in already_asked:
                continue
            askable.append(evi_id)
        return askable

    def select_next_question(self, already_asked: set[str], present: set[str], absent: set[str]) -> str | None:
        current_scores = self.score_conditions(present, absent)
        current_entropy = self._entropy([s for _, s in current_scores])

        askable = self.get_askable_evidences(already_asked, present, absent)
        if not askable:
            return None

        best_evi = None
        best_gain = -1.0

        for evi_id in askable:
            top_conditions = {name for name, _ in current_scores[:10]}
            conds_with_evi = self.evidence_to_conditions.get(evi_id, set())
            overlap = len(top_conditions & conds_with_evi)
            p_present = (overlap + 0.1) / (len(top_conditions) + 0.2)

            scores_if_yes = self.score_conditions(present | {evi_id}, absent)
            h_yes = self._entropy([s for _, s in scores_if_yes])

            scores_if_no = self.score_conditions(present, absent | {evi_id})
            h_no = self._entropy([s for _, s in scores_if_no])

            expected_entropy = p_present * h_yes + (1 - p_present) * h_no
            gain = current_entropy - expected_entropy

            if gain > best_gain:
                best_gain = gain
                best_evi = evi_id

        return best_evi

    def get_question_text(self, evidence_id: str) -> str:
        evi = self.evidences.get(evidence_id, {})
        return evi.get("question_en", f"Unknown evidence: {evidence_id}")

    def get_evidence_type(self, evidence_id: str) -> str:
        evi = self.evidences.get(evidence_id, {})
        return evi.get("data_type", "B")

    def get_evidence_options(self, evidence_id: str) -> list[dict]:
        evi = self.evidences.get(evidence_id, {})
        meanings = evi.get("value_meaning", {})
        default = evi.get("default_value")
        options = []
        for val_code, labels in meanings.items():
            if str(val_code) == str(default):
                continue
            options.append({"value": val_code, "label": labels.get("en", val_code)})
        return options

    def is_antecedent(self, evidence_id: str) -> bool:
        evi = self.evidences.get(evidence_id, {})
        return evi.get("is_antecedent", False)

    def get_severity_label(self, severity: int) -> str:
        return {1: "life-threatening", 2: "severe", 3: "moderate", 4: "mild", 5: "benign"}.get(severity, "unknown")

    @staticmethod
    def _entropy(probs: list[float]) -> float:
        h = 0.0
        for p in probs:
            if p > 0:
                h -= p * math.log2(p)
        return h


# ── Triage logic (inlined) ──────────────────────────────────────────

CONFIDENCE_THRESHOLD = 0.25


def triage(differential: list[dict], patient_says_resolved: bool = False) -> dict:
    if patient_says_resolved:
        if differential:
            worst = min(d["severity"] for d in differential[:3])
            if worst <= 2:
                return {"action": "urgent", "message": "Patient feels better but dangerous condition suspected. Recommend GP.", "severity": worst, "top_condition": differential[0]["condition"]}
        return {"action": "resolved", "message": "Patient reassured. Self-care advice.", "severity": 5, "top_condition": differential[0]["condition"] if differential else "None"}

    if not differential:
        return {"action": "routine", "message": "Unable to narrow down. Routine GP recommended.", "severity": 3, "top_condition": "Unknown"}

    top = differential[0]
    severity = top["severity"]
    prob = top["probability"]
    worst_severity = min(d["severity"] for d in differential[:3])
    severe1_prob = max((d["probability"] for d in differential[:3] if d["severity"] <= 1), default=0.0)

    if worst_severity <= 1 and severe1_prob >= CONFIDENCE_THRESHOLD:
        return {"action": "emergency", "message": "Possible medical emergency. Call 999 or attend A&E.", "severity": worst_severity, "top_condition": top["condition"]}
    if worst_severity == 2 and prob >= CONFIDENCE_THRESHOLD:
        return {"action": "emergency", "message": "Urgent medical attention needed. Call 999 or attend A&E.", "severity": worst_severity, "top_condition": top["condition"]}
    if severity <= 3:
        return {"action": "urgent", "message": "Priority appointment recommended today or tomorrow.", "severity": severity, "top_condition": top["condition"]}
    if severity == 4:
        return {"action": "routine", "message": "Routine GP appointment recommended.", "severity": severity, "top_condition": top["condition"]}
    return {"action": "resolved", "message": "Self-care likely sufficient. See GP if symptoms worsen.", "severity": severity, "top_condition": top["condition"]}


# ── SOAP generator (inlined) ────────────────────────────────────────

def generate_soap(engine: DiagnosticEngine, age, sex, chief_complaint, present_evidences, absent_evidences, differential, triage_action, known_antecedents=None) -> dict:
    return {
        "subjective": _build_subjective(engine, age, sex, chief_complaint, present_evidences, known_antecedents),
        "objective": _build_objective(engine, present_evidences, absent_evidences),
        "assessment": _build_assessment(engine, differential),
        "plan": _build_plan(engine, differential, triage_action),
    }


def _build_subjective(engine, age, sex, chief_complaint, present_evidences, known_antecedents):
    parts = []
    demo = []
    if age is not None:
        demo.append(f"{age}-year-old")
    if sex:
        demo.append("male" if sex.upper() == "M" else "female")
    if demo:
        parts.append(" ".join(demo) + " patient.")
    if chief_complaint:
        parts.append(f'Chief complaint: "{chief_complaint}".')
    symptoms = []
    for evi_id in sorted(present_evidences):
        evi = engine.evidences.get(evi_id, {})
        if not evi.get("is_antecedent", False):
            symptoms.append(f"- {evi.get('question_en', evi_id)}: Yes")
    if symptoms:
        parts.append("Patient reports:")
        parts.extend(symptoms)
    antecedents = known_antecedents or set()
    session_antecedents = {e for e in present_evidences if engine.evidences.get(e, {}).get("is_antecedent", False)}
    all_antecedents = antecedents | session_antecedents
    if all_antecedents:
        parts.append("Relevant history:")
        for evi_id in sorted(all_antecedents):
            parts.append(f"- {engine.evidences.get(evi_id, {}).get('question_en', evi_id)}: Yes")
    return "\n".join(parts)


def _build_objective(engine, present_evidences, absent_evidences):
    parts = ["[Pre-filled from patient self-report — clinician to verify with examination]"]
    positives = [engine.get_question_text(e) for e in sorted(present_evidences) if not engine.evidences.get(e, {}).get("is_antecedent", False)]
    if positives:
        parts.append("Pertinent positives:")
        parts.extend(f"- {p}" for p in positives)
    negatives = [engine.get_question_text(e) for e in sorted(absent_evidences) if not engine.evidences.get(e, {}).get("is_antecedent", False)]
    if negatives:
        parts.append("Pertinent negatives:")
        parts.extend(f"- {n}" for n in negatives)
    return "\n".join(parts)


def _build_assessment(engine, differential):
    if not differential:
        return "Unable to determine differential diagnosis from reported symptoms."
    parts = ["Differential diagnosis (ranked by likelihood):"]
    for i, d in enumerate(differential[:5], 1):
        sev = engine.get_severity_label(d["severity"])
        parts.append(f"{i}. {d['condition']} — likelihood {d['probability']:.0%}, severity: {sev}, ICD-10: {d['icd10']}")
    return "\n".join(parts)


def _build_plan(engine, differential, triage_action):
    action_map = {
        "emergency": "EMERGENCY: Patient advised to call 999 / attend A&E immediately.",
        "urgent": "URGENT: Priority appointment booked.",
        "routine": "ROUTINE: Standard GP appointment to be booked.",
        "resolved": "RESOLVED: Patient reassured. No appointment needed at this time.",
    }
    parts = [action_map.get(triage_action, f"Triage action: {triage_action}")]
    if not differential:
        parts.append("- Further assessment required.")
        return "\n".join(parts)
    severity = differential[0]["severity"]
    if severity <= 1:
        parts.extend(["- Immediate emergency assessment required.", "- Consider: ECG, troponin, D-dimer, ABG as appropriate.", "- Establish IV access and continuous monitoring."])
    elif severity <= 2:
        parts.extend(["- Urgent investigations recommended.", "- Consider: bloods (FBC, U&E, CRP), imaging, ECG as appropriate.", "- Review within 24 hours."])
    elif severity == 3:
        parts.extend(["- Standard investigations as clinically indicated.", "- Review within 48-72 hours or sooner if deterioration."])
    elif severity == 4:
        parts.extend(["- Conservative management / symptomatic treatment.", "- Safety-net: return if symptoms worsen or persist beyond 7 days."])
    else:
        parts.extend(["- Reassurance and self-care advice provided.", "- Patient to return if symptoms worsen or do not resolve."])
    return "\n".join(parts)


# ── File-backed session store ────────────────────────────────────────
# On Azure Linux Flex Consumption, /home is a persistent shared mount.
# Locally (Windows / macOS) we fall back to the OS temp directory.

_AZURE_HOME = Path("/home/agentcare_sessions")
_SESSION_DIR = _AZURE_HOME if _AZURE_HOME.parent.exists() else Path(__file__).resolve().parent / "_sessions"
_SESSION_DIR.mkdir(parents=True, exist_ok=True)

SESSION_TTL = 1800  # 30 minutes


def _session_path(sid: str) -> Path:
    # Sanitise to prevent path traversal
    safe = sid.replace("/", "").replace("\\", "").replace("..", "")
    return _SESSION_DIR / f"{safe}.json"


def _save_session(session: dict) -> None:
    path = _session_path(session["session_id"])
    path.write_text(json.dumps(session), encoding="utf-8")
    logging.info(f"SESSION_SAVE: sid={session['session_id']} path={path} exists_after={path.exists()}")


def _create_session(age=None, sex=None, chief_complaint=None, known_antecedents=None) -> dict:
    sid = secrets.token_urlsafe(16)
    session = {
        "session_id": sid,
        "age": age,
        "sex": sex,
        "chief_complaint": chief_complaint,
        "present_evidences": list(known_antecedents or []),
        "absent_evidences": [],
        "asked_evidences": list(known_antecedents or []),
        "turn": 0,
        "finished": False,
        "created_at": time.time(),
    }
    _save_session(session)
    _evict_stale()
    return session


def _get_session(sid: str) -> dict | None:
    path = _session_path(sid)
    logging.info(f"SESSION_GET: sid={sid!r} path={path} exists={path.exists()} dir_contents={list(_SESSION_DIR.glob('*.json'))}")
    if not path.exists():
        return None
    try:
        s = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if time.time() - s.get("created_at", 0) > SESSION_TTL:
        path.unlink(missing_ok=True)
        return None
    return s


def _evict_stale():
    now = time.time()
    for p in _SESSION_DIR.glob("*.json"):
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
            if now - s.get("created_at", 0) > SESSION_TTL:
                p.unlink(missing_ok=True)
        except (json.JSONDecodeError, OSError):
            p.unlink(missing_ok=True)


# ── Initialise engine once at cold start ─────────────────────────────

engine = DiagnosticEngine()

MAX_TURNS = 30


# ── HTTP Endpoints ───────────────────────────────────────────────────

@app.route(route="session/start", methods=["POST"])
def start_session(req: func.HttpRequest) -> func.HttpResponse:
    """Start a diagnostic session. Returns session_id and first question."""
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    session = _create_session(
        age=body.get("age"),
        sex=body.get("sex"),
        chief_complaint=body.get("chief_complaint"),
        known_antecedents=body.get("known_antecedents"),
    )

    present = set(session["present_evidences"])
    absent = set(session["absent_evidences"])
    asked = set(session["asked_evidences"])

    next_evi = engine.select_next_question(asked, present, absent)
    differential = engine.get_differential(present, absent, top_n=5)

    next_question = None
    if next_evi:
        session["asked_evidences"].append(next_evi)
        next_question = {
            "evidence_id": next_evi,
            "question": engine.get_question_text(next_evi),
            "data_type": engine.get_evidence_type(next_evi),
            "is_antecedent": engine.is_antecedent(next_evi),
            "options": engine.get_evidence_options(next_evi) if engine.get_evidence_type(next_evi) in ("C", "M") else None,
        }

    _save_session(session)

    return func.HttpResponse(json.dumps({
        "session_id": session["session_id"],
        "turn": 0,
        "finished": False,
        "next_question": next_question,
        "differential": differential,
    }), mimetype="application/json")


@app.route(route="session/answer", methods=["POST"])
def submit_answer(req: func.HttpRequest) -> func.HttpResponse:
    """Submit an answer and get the next question + updated differential."""
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    sid = body.get("session_id")
    evidence_id = body.get("evidence_id")
    logging.info(f"SUBMIT_ANSWER: raw_body={req.get_body().decode('utf-8', errors='replace')[:500]} sid={sid!r} evidence_id={evidence_id!r}")
    value = body.get("value")

    session = _get_session(sid)
    if not session:
        return func.HttpResponse(json.dumps({"error": "Session not found or expired"}), status_code=404, mimetype="application/json")
    if session["finished"]:
        return func.HttpResponse(json.dumps({"error": "Session already finished"}), status_code=400, mimetype="application/json")

    # Record the answer
    evi = engine.evidences.get(evidence_id, {})
    data_type = evi.get("data_type", "B")

    if data_type == "B":
        if str(value).lower() in ("true", "yes", "1"):
            session["present_evidences"].append(evidence_id)
        else:
            session["absent_evidences"].append(evidence_id)
    elif data_type == "C":
        session["present_evidences"].append(value)
        if evidence_id not in session["asked_evidences"]:
            session["asked_evidences"].append(evidence_id)
    elif data_type == "M":
        for v in str(value).split(","):
            v = v.strip()
            if v:
                session["present_evidences"].append(v)
        if evidence_id not in session["asked_evidences"]:
            session["asked_evidences"].append(evidence_id)

    session["turn"] += 1

    present = set(session["present_evidences"])
    absent = set(session["absent_evidences"])
    asked = set(session["asked_evidences"])

    finished = session["turn"] >= MAX_TURNS
    next_question = None

    if not finished:
        next_evi = engine.select_next_question(asked, present, absent)
        if next_evi:
            session["asked_evidences"].append(next_evi)
            next_question = {
                "evidence_id": next_evi,
                "question": engine.get_question_text(next_evi),
                "data_type": engine.get_evidence_type(next_evi),
                "is_antecedent": engine.is_antecedent(next_evi),
                "options": engine.get_evidence_options(next_evi) if engine.get_evidence_type(next_evi) in ("C", "M") else None,
            }
        else:
            finished = True

    session["finished"] = finished
    differential = engine.get_differential(present, absent, top_n=5)

    _save_session(session)

    return func.HttpResponse(json.dumps({
        "session_id": sid,
        "turn": session["turn"],
        "finished": finished,
        "next_question": next_question,
        "differential": differential,
    }), mimetype="application/json")


@app.route(route="session/{session_id}/differential", methods=["GET"])
def get_differential(req: func.HttpRequest) -> func.HttpResponse:
    """Get the current differential for a session."""
    sid = req.route_params.get("session_id")
    session = _get_session(sid)
    if not session:
        return func.HttpResponse(json.dumps({"error": "Session not found or expired"}), status_code=404, mimetype="application/json")

    present = set(session["present_evidences"])
    absent = set(session["absent_evidences"])
    differential = engine.get_differential(present, absent, top_n=10)

    return func.HttpResponse(json.dumps({"differential": differential}), mimetype="application/json")


@app.route(route="session/{session_id}/soap", methods=["POST"])
def get_soap(req: func.HttpRequest) -> func.HttpResponse:
    """Generate a SOAP note for the session."""
    sid = req.route_params.get("session_id")
    session = _get_session(sid)
    if not session:
        return func.HttpResponse(json.dumps({"error": "Session not found or expired"}), status_code=404, mimetype="application/json")

    present = set(session["present_evidences"])
    absent = set(session["absent_evidences"])
    differential = engine.get_differential(present, absent, top_n=5)
    triage_result = triage(differential)

    soap = generate_soap(
        engine,
        age=session["age"],
        sex=session["sex"],
        chief_complaint=session["chief_complaint"],
        present_evidences=present,
        absent_evidences=absent,
        differential=differential,
        triage_action=triage_result["action"],
    )

    return func.HttpResponse(json.dumps({
        "soap": soap,
        "triage": triage_result,
    }), mimetype="application/json")


@app.route(route="triage/disposition", methods=["POST"])
def get_disposition(req: func.HttpRequest) -> func.HttpResponse:
    """Determine triage disposition from a differential."""
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")

    differential = body.get("differential", [])
    patient_says_resolved = body.get("patient_says_resolved", False)

    result = triage(differential, patient_says_resolved)
    return func.HttpResponse(json.dumps(result), mimetype="application/json")


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check."""
    return func.HttpResponse(json.dumps({"status": "ok", "conditions_loaded": len(engine.conditions), "evidences_loaded": len(engine.evidences)}), mimetype="application/json")
