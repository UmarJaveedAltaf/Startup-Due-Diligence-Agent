# agents/evidence.py

import re
from typing import List, Dict, Optional


EMPLOYEE_REGEXES = [
    r"(\d{1,3})\s+employees",
    r"about\s+(\d{1,3})\s+employees",
    r"around\s+(\d{1,3})\s+employees",
    r"~\s*(\d{1,3})\s+employees",
    r"less\s+than\s+(\d{1,3})\s+employees",
]


def _extract_employee_count(text: str) -> Optional[int]:
    """
    Extract numeric employee count from text if explicitly stated.
    Returns int if found, else None.
    """
    text = text.lower()

    for pattern in EMPLOYEE_REGEXES:
        match = re.search(pattern, text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue

    return None


def validate_answer(claim: str, evidence_snippets: List[str]) -> Dict:
    """
    STRICT validation:
    - ACCEPT only if explicit numeric employee count < 50 is found
    - Early-stage / startup mentions alone are NOT sufficient
    """

    for snippet in evidence_snippets:
        employee_count = _extract_employee_count(snippet)

        if employee_count is not None:
            if employee_count < 50:
                return {
                    "accepted": True,
                    "employee_count_verified": True,
                    "employee_count": employee_count,
                    "cleaned_answer": (
                        f"Explicit employee count under 50 verified "
                        f"(~{employee_count} employees)."
                    ),
                }
            else:
                return {
                    "accepted": False,
                    "employee_count_verified": False,
                    "employee_count": employee_count,
                    "cleaned_answer": (
                        f"Employee count explicitly found "
                        f"({employee_count}), but not under 50."
                    ),
                }

    #  No explicit employee count found
    return {
        "accepted": False,
        "employee_count_verified": False,
        "cleaned_answer": "No explicit public employee-count evidence found.",
    }
