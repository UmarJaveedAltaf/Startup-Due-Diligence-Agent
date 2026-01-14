# agents/candidates.py
import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3", temperature=0)

SYSTEM_PROMPT = """
You are an entity extraction agent.

TASK:
Extract ONLY early-stage startup company names.

STRICT RULES:
- Output ONLY company names
- One company per line
- NO descriptions
- NO roles
- NO media outlets
- NO platforms
- NO generic terms
- NO famous or late-stage companies
- If unsure, DO NOT include it
- Prefer obscure, seed-stage startups
"""

# 🚫 Big tech / enterprises
BLOCKLIST_KEYWORDS = [
    "google", "alphabet", "microsoft", "amazon", "meta",
    "medtronic", "pluralsight", "subsidiary",
    "holdings", "group", "inc", "corp", "pharma"
]

# 🚫 Late-stage indicators
LATE_STAGE_KEYWORDS = [
    "acquired", "public", "ipo", "unicorn",
    "nasdaq", "nyse"
]

# 🚫 Famous / scale-ups (VC sanity gate)
KNOWN_LARGE_COMPANIES = {
    "deepmind", "deepmind health",
    "hinge health", "omada health", "heartflow",
    "owkin", "freenome", "paige.ai",
    "zebra medical vision", "vicarious surgical",
    "pear therapeutics", "arterys", "sensyne health",
    "click therapeutics", "cerevance", "medable",
    "clarify health", "syapse", "mindstrong health",
    "karius", "inovalon", "terarecon"
}


def _clean_line(line: str) -> str | None:
    # 🔹 Remove bullets, numbers, symbols
    line = re.sub(r"^[\*\-\•]\s*", "", line)
    line = re.sub(r"^\d+[\.\)]\s*", "", line)
    line = line.strip()

    if not line:
        return None

    # Too long → not a company name
    if len(line.split()) > 4:
        return None

    lowered = line.lower()

    if any(bad in lowered for bad in BLOCKLIST_KEYWORDS):
        return None

    if any(bad in lowered for bad in LATE_STAGE_KEYWORDS):
        return None

    if lowered in KNOWN_LARGE_COMPANIES:
        return None

    if "'" in line or "(" in line:
        return None

    return line


def _llm_extract(prompt: str) -> list[str]:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
User query:
{prompt}

Return ONLY early-stage startup company names.
One per line.
"""
        ),
    ]

    response = llm.invoke(messages)
    raw_lines = response.content.split("\n")

    cleaned = []
    for line in raw_lines:
        c = _clean_line(line)
        if c:
            cleaned.append(c)

    return cleaned


def extract_candidates(user_query: str) -> list[str]:
    """
    STEP 2.6 — FINAL hardened candidate extraction
    """

    candidates = set()

    # Pass 1 — Direct
    candidates.update(_llm_extract(user_query))

    # Pass 2 — Similar startups (restricted)
    for c in list(candidates)[:2]:
        candidates.update(
            _llm_extract(f"seed stage AI healthcare startup similar to {c}")
        )

    # Pass 3 — Explicit early-stage search
    candidates.update(
        _llm_extract("US seed stage AI healthcare startup under 50 employees")
    )

    # 🔒 HARD CAP — prevents explosion
    return list(candidates)[:8]
