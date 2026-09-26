from ..ai import ask_ai


def verify(task, evidence, candidate_answer):

    instruction = """
You are the Verifier Agent in a multi-agent AI
reasoning and verification system.

Your job is to independently verify the candidate answer.

Check:

1. Is the answer relevant to the user's task?
2. Is the reasoning logically correct?
3. Are calculations correct?
4. Are factual claims supported by the available evidence?
5. Is there any obvious contradiction?
6. Is the answer complete enough for the question?

IMPORTANT:

For simple general questions such as:
- What is AI?
- What is Python?
- What is data science?
- Explain machine learning.

do not fail the answer merely because web evidence is limited.

If the candidate answer is reasonable and contains no obvious
incorrect claim, mark it as PASSED.

At the very beginning of your response, write exactly:

STATUS: PASSED

or

STATUS: FAILED

Then explain your verification.
"""

    sources = evidence.get("sources", [])

    source_text = ""

    for i, source in enumerate(sources, start=1):

        source_text += f"""
SOURCE {i}

Title:
{source.get("title", "")}

URL:
{source.get("url", "")}

Snippet:
{source.get("snippet", "")}

"""

    prompt = f"""
USER TASK:

{task}


AVAILABLE EVIDENCE:

{source_text}


CANDIDATE ANSWER:

{candidate_answer}


Now independently verify the candidate answer.
"""

    result = ask_ai(
        instruction,
        prompt
    )

    result_upper = result.upper()

    if "STATUS: PASSED" in result_upper:

        status = "passed"

    elif "STATUS: FAILED" in result_upper:

        status = "failed"

    else:

        # If the AI forgot the required STATUS,
        # do a simple fallback check.

        if (
            "correct" in result_upper
            and "incorrect" not in result_upper
        ):

            status = "passed"

        else:

            status = "failed"

    return {
        "agent": "verifier",
        "task": task,
        "status": status,
        "verification": result
    }