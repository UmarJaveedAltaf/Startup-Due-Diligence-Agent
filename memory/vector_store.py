from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3")

def build_vector_store(search_results):
    if not search_results:
        return None

    docs = []
    for r in search_results:
        content = f"{r['title']}\n{r['body']}"
        docs.append(
            Document(
                page_content=content,
                metadata={"source": r["source"]}
            )
        )

    if not docs:
        return None

    return FAISS.from_documents(docs, embeddings)
