from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3", temperature=0)

SYSTEM_PROMPT = """
You are a Planner & Orchestrator Agent.

Responsibilities:
- Decide which specialist agents to invoke.
- Ensure research is verified before final output.
- Enforce safety and trust over completeness.
"""

def create_plan(user_request: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_request)
    ]
    response = llm.invoke(messages)
    return response.content
