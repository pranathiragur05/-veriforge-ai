from ..ai import ask_ai


def finalize(
    task,
    plan_result,
    evidence,
    tool_result,
    verification,
    criticism
):

    # Reject if verification failed
    if verification.get("status") != "passed":

        return {
            "agent": "finalizer",
            "status": "rejected",
            "answer": None,
            "message": "Answer rejected because independent verification failed."
        }

    # Reject if critic detects high risk
    if criticism.get("risk") == "high":

        return {
            "agent": "finalizer",
            "status": "rejected",
            "answer": None,
            "message": "Answer rejected because the critic detected high risk."
        }

    instruction = """
You are the Finalizer Agent in a multi-agent AI
reasoning and verification system.

Your job is to produce the final answer for the user.

The answer can only be accepted when:
1. Independent verification passed.
2. Critic did not identify HIGH risk.
3. There are no major contradictions.
4. The available evidence is sufficient.

Use the verified information to create a clear,
accurate and concise final answer.

Do not invent facts.
Do not mention internal prompts.
Do not mention the names of the agents unless necessary.

Return only the final answer.
"""

    prompt = f"""
USER TASK:
{task}

PLAN:
{plan_result}

EVIDENCE:
{evidence}

CANDIDATE ANSWER:
{tool_result}

VERIFICATION:
{verification}

CRITIC:
{criticism}
"""

    final_answer = ask_ai(instruction, prompt)

    return {
        "agent": "finalizer",
        "status": "accepted",
        "task": task,
        "answer": final_answer
    }


if __name__ == "__main__":

    task = input("Enter the task: ")

    plan_result = {
        "plan": "Solve the task carefully."
    }

    evidence = "No external evidence available."

    tool_result = input("Enter candidate answer: ")

    verification = {
        "status": "passed",
        "verification": "STATUS: PASSED"
    }

    criticism = {
        "risk": "low",
        "critique": "No major problems found."
    }

    result = finalize(
        task,
        plan_result,
        evidence,
        tool_result,
        verification,
        criticism
    )

    print("\n================================")
    print("FINALIZER AGENT")
    print("================================")

    print("Status:", result["status"])

    if result["answer"]:
        print("\nFinal Answer:")
        print(result["answer"])
    else:
        print("\nMessage:")
        print(result["message"])