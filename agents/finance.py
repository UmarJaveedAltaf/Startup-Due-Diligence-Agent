from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3", temperature=0)

SYSTEM_PROMPT = """
You are a Financial Analyst Agent.

STRICT RULES:
- Extract ONLY numbers explicitly present in the input text.
- If a number does not appear verbatim, write: "Not found".
- NEVER estimate, infer, summarize, or normalize.
- If all numbers are weak or vague, say: "No verifiable financial data found."
- Output format:
  - Metric: Value | Evidence: exact phrase from text
"""


def analyze_financials(context: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=context)
    ]
    response = llm.invoke(messages)
    return response.content
