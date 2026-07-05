import json
import os
import re
import requests
from dotenv import load_dotenv

from doc_generator import create_docx

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

ALLOWED_DOC_TYPES = {
    "project_proposal",
    "meeting_minutes",
    "business_report",
    "sop",
    "product_spec",
    "technical_design",
}


SYSTEM_PROMPT = """
You are an autonomous AI business document agent.

Analyze the user's request and return ONLY valid JSON.
Do not use markdown.
Do not use backticks.
Do not add explanation text.

Choose exactly ONE value for document_type from this list:
project_proposal, meeting_minutes, business_report, sop, product_spec, technical_design

Return this exact JSON schema:
{
  "document_type": "one value from the allowed list",
  "title": "string",
  "assumptions": ["string"],
  "tasks": ["string"]
}
"""


def extract_json(text: str) -> dict:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    fenced_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced_match:
        return json.loads(fenced_match.group(1))

    brace_match = re.search(r"(\{.*\})", text, re.DOTALL)
    if brace_match:
        return json.loads(brace_match.group(1))

    raise ValueError("No valid JSON found in model response.")


def normalize_document_type(value: str) -> str:
    if not value:
        return "business_report"

    cleaned = value.strip().lower()

    if cleaned in ALLOWED_DOC_TYPES:
        return cleaned

    if "|" in cleaned:
        parts = [p.strip() for p in cleaned.split("|")]
        for part in parts:
            if part in ALLOWED_DOC_TYPES:
                return part

    cleaned = cleaned.replace(" ", "_")
    if cleaned in ALLOWED_DOC_TYPES:
        return cleaned

    return "business_report"


def normalize_plan(plan: dict) -> dict:
    title = plan.get("title", "Generated Business Document")
    assumptions = plan.get("assumptions", [])
    tasks = plan.get("tasks", [])

    if not isinstance(assumptions, list):
        assumptions = [str(assumptions)]

    if not isinstance(tasks, list):
        tasks = [str(tasks)]

    return {
        "document_type": normalize_document_type(plan.get("document_type", "business_report")),
        "title": str(title).strip() or "Generated Business Document",
        "assumptions": [str(a).strip() for a in assumptions if str(a).strip()],
        "tasks": [str(t).strip() for t in tasks if str(t).strip()],
    }


def get_fallback_plan(user_request: str) -> dict:
    return {
        "document_type": "business_report",
        "title": "Generated Business Report",
        "assumptions": [
            "Some information was missing, so reasonable defaults were applied.",
            "The target audience is business stakeholders.",
            "The timeline and scope were estimated from the request."
        ],
        "tasks": [
            "Analyze the request",
            "Identify the most suitable document structure",
            "Draft core sections",
            "Add assumptions and next steps",
            "Generate polished Word document"
        ]
    }


def build_sections(user_request: str, plan: dict) -> dict:
    title = plan.get("title", "Generated Business Document")
    doc_type = plan.get("document_type", "business_report").replace("_", " ").title()
    request_lower = user_request.lower()

    is_healthcare = "healthcare" in request_lower or "clinic" in request_lower or "hospital" in request_lower
    is_retail = "retail" in request_lower or "ecommerce" in request_lower or "e-commerce" in request_lower
    is_budget_limited = "limited budget" in request_lower or "budget" in request_lower
    is_compliance = "compliance" in request_lower or "regulation" in request_lower

    industry_note = "general business environment"
    if is_healthcare:
        industry_note = "healthcare environment with patient data sensitivity"
    elif is_retail:
        industry_note = "retail environment with high-volume customer interactions"

    risk_items = [
        "Incomplete or ambiguous requirements may affect final scope.",
        "Stakeholder expectations may differ from inferred assumptions."
    ]

    if is_budget_limited:
        risk_items.append("Budget constraints may reduce implementation speed or feature scope.")

    if is_compliance:
        risk_items.append("Compliance and regulatory requirements must be validated before rollout.")

    if is_healthcare:
        next_steps = [
            "Validate privacy, security, and compliance requirements.",
            "Review the draft with business and operational stakeholders.",
            "Refine implementation scope and rollout plan before execution."
        ]
    else:
        next_steps = [
            "Review the draft with stakeholders.",
            "Validate assumptions and missing details.",
            "Refine the scope, timeline, and resource plan before execution."
        ]

    return {
        "executive_summary": (
            f"This {doc_type} titled '{title}' was created based on the request: {user_request}. "
            f"The agent analyzed the input, created its own execution plan, made reasonable assumptions, "
            f"and generated a structured draft suitable for a {industry_note}."
        ),
        "objectives": [
            "Address the user's core business need.",
            "Provide a structured and actionable business document.",
            "Support faster stakeholder review and decision-making."
        ],
        "scope": [
            "Initial draft prepared from the provided natural language request.",
            "Includes assumptions, execution plan, timeline, risks, and next steps.",
            "Uses inferred context where exact details were not available."
        ],
        "timeline": [
            "Week 1: Requirement clarification and planning.",
            "Week 2: Solution design and stakeholder alignment.",
            "Week 3: Draft implementation preparation.",
            "Week 4: Internal review and risk evaluation.",
            "Week 5: Revision and readiness planning.",
            "Week 6: Final rollout preparation and approval."
        ],
        "risks": risk_items,
        "next_steps": next_steps
    }


def call_ollama(user_request: str) -> dict:
    url = f"{OLLAMA_BASE_URL}/api/chat"

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_request}
        ]
    }

    response = requests.post(url, json=payload, timeout=180)
    response.raise_for_status()

    data = response.json()
    content = data["message"]["content"]

    print("\nRAW OLLAMA RESPONSE:\n", content)

    return extract_json(content)


def run_agent(user_request: str) -> dict:
    used_fallback = False

    try:
        plan = call_ollama(user_request)
        plan = normalize_plan(plan)
    except Exception as e:
        print("OLLAMA parsing failed:", str(e))
        plan = get_fallback_plan(user_request)
        used_fallback = True

    plan["sections"] = build_sections(user_request, plan)

    document_path = create_docx(plan)

    return {
        "status": "success",
        "message": "Agent completed the request and generated the Word document.",
        "document_path": document_path,
        "plan": plan.get("tasks", []),
        "assumptions": plan.get("assumptions", []),
        "title": plan.get("title", "Generated Business Document"),
        "document_type": plan.get("document_type", "business_report"),
        "used_fallback": used_fallback
    }