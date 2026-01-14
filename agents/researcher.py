from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tools.web_search import web_search, multi_query_search
from memory.vector_store import build_vector_store


llm = ChatOllama(model="llama3", temperature=0)

SYSTEM_PROMPT = """
You are a Research Agent.

STRICT RULES:
- Use ONLY the provided context.
- Do NOT introduce numbers unless explicitly present.
- If employee count is missing, say: "Not found in retrieved sources."
- Do NOT guess or estimate.
- Prefer being incomplete over being wrong.
- Write short, factual bullet points.
"""


def research_company(company: str) -> dict:
    """
    Focused company research with explicit employee-count queries.
    """

    queries = [
        f"{company} employee count",
        f"{company} number of employees",
        f"{company} company size LinkedIn",
        f"{company} Crunchbase employees",
        f"{company} staff count"
    ]

    search_results = multi_query_search(queries)

    vector_store = build_vector_store(search_results)

    if vector_store is None:
        return {
            "company": company,
            "snippets": [],
            "sources": []
        }

    docs = vector_store.similarity_search(
        query=f"{company} employees",
        k=5
    )

    return {
        "company": company,
        "snippets": [d.page_content for d in docs],
        "sources": [d.metadata.get("source", "unknown") for d in docs]
    }
