🧠 Startup Due Diligence Agent

Evidence-First AI Agent for Startup Analysis

An autonomous, evidence-driven AI agent that performs startup due diligence with a strict verification pipeline.
The system refuses to speculate and only accepts claims that are explicitly supported by public evidence.

⚠️ Design principle: No evidence → No acceptance.

🚀 What This Project Does

The Startup Due Diligence Agent analyzes startups based on a user query (e.g., “AI healthcare startups in the US with under 50 employees”) and:

Extracts real startup candidates (no media, no generic terms)

Performs focused per-company research

Validates claims using public evidence

Accepts only startups with explicitly verified employee counts

Rejects everything else with clear reasons

Presents results through a Gradio web UI

This mirrors real investor-grade diligence, not blog-style summaries.

🧩 System Architecture
User Query
   ↓
Candidate Extraction Agent
   ↓
Per-Company Research Agent
   ↓
Evidence Validator (Hard Gate)
   ↓
Accepted / Rejected Lists
   ↓
Gradio UI + Full Audit Log

🧠 Core Design Philosophy

❌ No guessing

❌ No extrapolation

❌ No vague “early-stage” assumptions

✅ Explicit numeric evidence only

✅ Transparent rejection reasons

✅ Full audit trail

This makes the system trustworthy, auditable, and defensible.

📂 Project Structure
startup-due-diligence-agent/
│
├── main.py                # CLI pipeline runner
├── requirements.txt
├── README.md
│
├── agents/
│   ├── candidates.py      # Multi-pass startup extraction
│   ├── researcher.py      # Per-company evidence retrieval
│   ├── evidence.py        # Hard validation + employee count detection
│   ├── planner.py
│   ├── finance.py
│   ├── risk.py
│
├── tools/
│   └── web_search.py      # Multi-query web search
│
├── memory/
│   └── vector_store.py    # FAISS-based evidence retrieval
│
├── config/
│   └── settings.py
│
└── ui/
    └── app.py             # Gradio web interface

🔍 Employee Count Verification (Key Feature)

A startup is ACCEPTED only if:

A numeric employee count is explicitly found

AND the count is < 50

AND the evidence comes from public sources

Examples:

✅ “~33 employees” → Accepted

❌ “Early-stage startup” → Rejected

❌ “Small team” → Rejected

❌ “50 employees” → Rejected

This logic is enforced in agents/evidence.py and cannot be bypassed.

🖥️ Web UI (Gradio)

The UI displays:

🟢 Accepted Startups (employee count verified)

🔴 Rejected Candidates (with reasons)

📜 Full Audit Log (every decision explained)

Run the UI:
python ui/app.py

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/<your-username>/startup-due-diligence-agent.git
cd startup-due-diligence-agent

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python ui/app.py


Requires a local Ollama setup with llama3.

🧪 Example Output

Accepted

Healium
SimX


Rejected

PrecisionLife — No explicit public evidence of employee count under 50
Proximie — Employee count found (105), exceeds limit


Each decision includes verbatim evidence justification.
🛑 Disclaimer

This tool relies only on publicly available information.
Rejection indicates insufficient evidence, not company size or quality.