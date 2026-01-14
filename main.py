from agents.candidates import extract_candidates
from agents.researcher import research_company
from agents.evidence import validate_answer

user_goal = "Analyze AI healthcare startups in the US with under 50 employees"

print("\n🧠 CANDIDATE EXTRACTION\n")
candidates = extract_candidates(user_goal)
print(candidates)

print("\n🔍 PER-COMPANY EVIDENCE CHECK\n")

for company in candidates:
    print(f"\n--- {company} ---")

    research = research_company(company)

    if not research["snippets"]:
        print("No evidence found.")
        continue

    draft = f"{company} has under 50 employees."


    validated = validate_answer(
        draft,
        research["snippets"]
    )

    print("CLEANED:")
    print(validated["cleaned_answer"])

    if validated["removed_claims"]:
        print("REMOVED:")
        for r in validated["removed_claims"]:
            print("-", r["claim"])

    print("\n⚠️ NOTE: Output is conservative by design.")
    print("⚠️ Missing data indicates lack of evidence, not system failure.")
