from .ai import ask_ai


def detect_risk(task, evidence, candidate_answer):

    instruction = """
You are the Risk and Contradiction Detection Agent.

Analyze the evidence and candidate answer.

Look for:

1. Contradictions between sources.
2. Claims that are not supported by the sources.
3. Missing or insufficient evidence.
4. Hallucinated information.
5. Logical inconsistencies.
6. Unsafe or potentially harmful recommendations.
7. Situations requiring additional verification.

At the beginning of your response, write exactly one:

RISK: LOW

or

RISK: MEDIUM

or

RISK: HIGH

Then provide:

CONTRADICTIONS:
List conflicting information.

UNSUPPORTED CLAIMS:
List claims without sufficient evidence.

SAFETY CONCERNS:
List any safety concerns.

RECOMMENDATION:
State whether the answer should be accepted, rechecked, or rejected.

Do not invent evidence.
"""

    sources = evidence.get("sources", [])

    source_text = ""

    for i, source in enumerate(sources, start=1):

        source_text += f"""
SOURCE {i}
Title: {source.get("title", "")}
URL: {source.get("url", "")}
Snippet: {source.get("snippet", "")}
"""

    prompt = f"""
USER TASK:
{task}

RETRIEVED EVIDENCE:
{source_text}

CANDIDATE ANSWER:
{candidate_answer}
"""

    result = ask_ai(instruction, prompt)

    result_upper = result.upper()

    if "RISK: HIGH" in result_upper:
        risk = "high"
    elif "RISK: MEDIUM" in result_upper:
        risk = "medium"
    else:
        risk = "low"

    return {
        "agent": "risk_detector",
        "task": task,
        "risk": risk,
        "analysis": result
    }


if __name__ == "__main__":

    task = input("Enter the task: ")

    evidence = {
        "sources": [
            {
                "title": "Example Source",
                "url": "https://example.com",
                "snippet": "Example evidence."
            }
        ]
    }

    candidate_answer = input("Enter the candidate answer: ")

    result = detect_risk(
        task,
        evidence,
        candidate_answer
    )

    print("\n================================")
    print("RISK & CONTRADICTION DETECTOR")
    print("================================")

    print("Risk:", result["risk"])

    print("\nAnalysis:")
    print(result["analysis"])