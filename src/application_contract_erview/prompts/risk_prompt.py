# prompts/risk_prompt.py

def get_risk_audit_prompt(context_str: str, category_name: str, clause_text: str) -> str:
    """
    Compiles the synchronized, high-performance legal audit prompt layout.
    Hardcodes standard EduRisk compliance metrics to force Small Language Models (SLMs)
    to accurately capture commercial violations without reasoning failures.
    """
    return f"""
    You are a strict legal contract compliance auditor. Your absolute mandate is to detect hidden business risks and contractual imbalances.
    You must evaluate the Target Contract Clause against the hardcoded EduRisk Compliance Rules provided below.
    Use the provided Textbook Guidelines reference ONLY as supporting context to find the correct legal solutions and recommendations.

    [EduRisk Compliance Rules - Mandatory Checklist]:
    Rule 1 (Indemnification Category): If the clause forces our institution/customer to assume full responsibility, pay for legal claims, or hold the other party harmless for losses caused by the provider's/other party's own active negligence or willful misconduct, this is a severe violation.
    Rule 2 (Termination Category): If either party is allowed to terminate the agreement immediately without cause, without clear written advance notice (such as immediate effect), or completely deprives the breaching party of a reasonable opportunity to cure or correct the breach, this is a severe violation.
    Rule 3 (Limitation of Liability Category): If the other party/provider strictly caps their total monetary financial liability to a tiny, unfair, or nominal amount (e.g., $100 or less) while our institution's financial liability remains entirely unlimited, this is a severe violation.

    [Textbook Guidelines Reference (Context Source)]:
    {context_str}

    [Target Contract Clause to Audit]:
    Category/Type: {category_name}
    Text: {clause_text}

    EXPLICIT COMPLIANCE INSTRUCTIONS:
    1. Perform a concept-mapping check. Match broader terms (like "liability cap" to Limitation of Liability, or "hold harmless" to Indemnification).
    2. Check if the Target Contract Clause breaks or contradicts Rule 1, Rule 2, or Rule 3.
    3. If any violation or unfair commercial condition is found, you MUST set "has_violation" to true, set "risk_tier" to "High", and identify the exact broken rule.
    4. If the clause is perfectly safe, balanced, mutual, and does not violate any rule, set "has_violation" to false and leave auditing metadata blank.

    You MUST respond strictly in the following JSON format. Do not include any introduction, conversational filler, thinking process, markdown blocks, or code fences:
    {{
        "has_violation": true,
        "failed_checklist_question": "State the exact broken rule here (e.g., Rule 1: Unilateral Indemnification | Rule 2: Ambiguous Termination | Rule 3: One-Sided Liability Cap)",
        "clause_contradiction": "Identify and quote the exact unfair or risky phrase found inside the target contract clause text",
        "correct_rule_from_book": "Extract and state the correct professional legal standard or solution based on the textbook guidelines",
        "risk_tier": "High",
        "recommendation": "Provide clear, actionable, step-by-step instructions for the attorney to rewrite the clause and fix the risk safely"
    }}
    """
