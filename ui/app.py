import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr

from agents.candidates import extract_candidates
from agents.researcher import research_company
from agents.evidence import validate_answer


def run_analysis(user_query: str):
    accepted = []
    rejected = []
    audit_log = []

    audit_log.append("⏳ Starting analysis...\n")

    # ---- Candidate Extraction ----
    candidates = extract_candidates(user_query)
    audit_log.append("🧠 CANDIDATE EXTRACTION")
    audit_log.append(str(candidates))
    audit_log.append("")

    if not candidates:
        return "None", "None", "No candidates found."

    # ---- Per-company Evidence Check ----
    for company in candidates:
        audit_log.append(f"🔍 Analyzing {company}")

        research = research_company(company)
        snippets = research.get("snippets", [])

        verdict = validate_answer(
            claim=f"{company} has under 50 employees",
            evidence_snippets=snippets
        )

        # ✅ FINAL ACCEPTANCE RULE (CORRECT)
        if verdict.get("employee_count_verified") is True:
            accepted.append(company)
            audit_log.append("🟢 ACCEPTED — Employee count explicitly verified")
        else:
            reason = "No explicit public evidence of employee count under 50"
            rejected.append(f"{company} — {reason}")
            audit_log.append("🔴 REJECTED — Insufficient employee-count evidence")

        audit_log.append(verdict.get("cleaned_answer", "No verified claims"))
        audit_log.append("-" * 50)

    # ---- Final Outputs ----
    accepted_text = "\n".join(accepted) if accepted else "None"
    rejected_text = "\n".join(rejected) if rejected else "None"
    audit_text = "\n".join(audit_log)

    return accepted_text, rejected_text, audit_text


# ===================== UI =====================

with gr.Blocks(title="Autonomous Startup Analyst") as demo:
    gr.Markdown("# 🧠 Autonomous Startup Analyst")
    gr.Markdown(
        "Evidence-first AI agent for startup due diligence. "
        "**The system prefers no answer over an incorrect one.**"
    )

    query = gr.Textbox(
        label="Analysis Query",
        value="Analyze AI healthcare startups in the US with under 50 employees"
    )

    run_btn = gr.Button("Run Analysis")

    accepted_box = gr.Textbox(
        label="🟢 Accepted Startups (Employee Count Verified)",
        lines=6
    )

    rejected_box = gr.Textbox(
        label="🔴 Rejected Candidates (Insufficient Evidence)",
        lines=10
    )

    audit_box = gr.Textbox(
        label="📜 Full Audit Log",
        lines=18
    )

    run_btn.click(
        fn=run_analysis,
        inputs=query,
        outputs=[accepted_box, rejected_box, audit_box]
    )

demo.launch()
