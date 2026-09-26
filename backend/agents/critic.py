from ..ai import ask_ai


def critique(task, evidence, tool_result, verification):

    instruction = """
You are the Critic Agent in a multi-agent AI reasoning
and verification system.

Your job is to critically review the candidate answer
after independent verification.

Do NOT simply agree with the Verifier Agent.

Check carefully for:

1. Contradictions between the evidence and candidate answer.
2. Unsupported factual claims.
3. Hallucinations or invented information.
4. Logical reasoning errors.
5. Missing important information.
6. Unsafe or risky recommendations.
7. Weak or insufficient evidence.
8. Whether the verifier may have missed an important problem.

At the beginning of your response, write exactly one:

RISK: LOW

or

RISK: MEDIUM

or

RISK: HIGH

Then provide:

Problems Found:
- List the problems, if any.

Correction Required:
- YES or NO

Reason:
- Explain your decision clearly.

Be objective and critical.
Do not invent evidence.
"""

    prompt = f"""
USER TASK:
{task}

RESEARCHER EVIDENCE:
{evidence}

CANDIDATE ANSWER:
{tool_result}

VERIFIER OUTPUT:
{verification}
"""

    result = ask_ai(instruction, prompt)

    if "RISK: HIGH" in result.upper():
        risk = "high"
    elif "RISK: MEDIUM" in result.upper():
        risk = "medium"
    else:
        risk = "low"

    return {
        "agent": "critic",
        "task": task,
        "risk": risk,
        "critique": result
    }


if __name__ == "__main__":

    task = input("Enter the task: ")

    evidence = "No external evidence available."

    tool_result = input("Enter the candidate answer: ")

    verification = input("Enter the verifier result: ")

    result = critique(
        task,
        evidence,
        tool_result,
        verification
    )

    print("\n================================")
    print("CRITIC AGENT")
    print("================================")

    print("Risk:", result["risk"])

    print()
    print(result["critique"])