from ..ai import ask_ai
from ..evidence import create_evidence


def research(task, plan_result):

    evidence_record = create_evidence(task)

    sources = evidence_record["sources"]

    source_text = ""

    for i, source in enumerate(sources, start=1):

        source_text += f"""
SOURCE {i}
Title: {source["title"]}
URL: {source["url"]}
Snippet: {source["snippet"]}

"""

    instruction = """
You are the Researcher Agent in a multi-agent AI
reasoning and verification system.

Your job is to analyze the retrieved evidence.

For each important claim:

1. Identify the claim.
2. Identify which source supports it.
3. Explain whether the source provides enough support.
4. Identify conflicting or missing information.
5. Never invent information that is not present in the sources.

If there are no useful sources, clearly state that
the evidence is insufficient.

Do not produce the final answer yet.
"""

    prompt = f"""
USER TASK:
{task}

PLANNER OUTPUT:
{plan_result["plan"]}

RETRIEVED SOURCES:
{source_text}
"""

    result = ask_ai(instruction, prompt)

    evidence_record["research_report"] = result

    return {
        "agent": "researcher",
        "task": task,
        "evidence": evidence_record,
        "plan_used": plan_result
    }


if __name__ == "__main__":

    task = input("Enter your research task: ")

    plan_result = {
        "plan": "Identify and verify the information required."
    }

    result = research(task, plan_result)

    print("\n================================")
    print("RESEARCHER AGENT")
    print("================================")

    print("\nEVIDENCE STATUS:")
    print(result["evidence"]["status"])

    print("\nSOURCES:")

    for source in result["evidence"]["sources"]:
        print("\nTitle:", source["title"])
        print("URL:", source["url"])
        print("Snippet:", source["snippet"])

    print("\nRESEARCH REPORT:")
    print(result["evidence"]["research_report"])