from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3", temperature=0)

SYSTEM_PROMPT = """
You are a Risk & Hallucination Detection Agent.

STRICT RULES:
- Treat all claims as UNTRUSTED by default.
- Mark a claim as 'Supported' ONLY if directly grounded in sources.
- If a claim is generic, mark: 'Plausible but unsupported'.
- If a claim includes numbers without evidence, mark: 'High hallucination risk'.
- If sources are generic or irrelevant, downgrade confidence.
- Prefer harsh judgment over leniency.

Return format:
- Claim:
- Verdict: Supported | Plausible | Unsupported | Hallucinated
- Confidence: High | Medium | Low
- Reason:
"""

def assess_risk(answer: str, sources: list) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"Answer:\n{answer}\n\nSources:\n{sources}"
        )
    ]
    response = llm.invoke(messages)
    return response.content
