from ddgs import DDGS

def web_search(query: str, max_results: int = 5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if r.get("body") and r.get("href"):
                results.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "source": r.get("href")
                })
    return results

def multi_query_search(company: str):
    queries = [
        f"{company} employee count",
        f"{company} number of employees",
        f"{company} Crunchbase employees",
        f"{company} company size"
    ]

    all_results = []
    for q in queries:
        all_results.extend(web_search(q, max_results=3))

    return all_results
