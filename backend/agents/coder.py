from ..ai import ask_ai


def tool_check(task, plan_result):

    instruction = """
You are the Coder and Tool-Use Agent in a multi-agent
AI reasoning and verification system.

Your job is to produce a candidate solution for the user's task.

Rules:

1. For mathematical questions:
   - Show the calculation.
   - Give the result.
   - Check the arithmetic carefully.

2. For programming questions:
   - Write correct code.
   - Explain the important logic.
   - Check for syntax and logical errors.

3. For reasoning questions:
   - Work through the problem step by step.
   - Clearly state assumptions.

4. For general questions:
   - Produce a useful candidate answer.

5. Never claim that you executed code or used a tool if you did not
   actually execute or use it.

6. Do not give unsupported facts when evidence is required.

This is a CANDIDATE answer.
The Verifier Agent will independently check it later.
"""

    prompt = f"""
USER TASK:
{task}

PLANNER OUTPUT:
{plan_result["plan"]}
"""

    result = ask_ai(instruction, prompt)

    return {
        "agent": "coder",
        "task": task,
        "result": result,
        "plan_used": plan_result
    }


if __name__ == "__main__":

    task = input("Enter your coding/problem-solving task: ")

    plan_result = {
        "plan": "Solve the user's task carefully."
    }

    result = tool_check(task, plan_result)

    print("\n================================")
    print("CODER / TOOL AGENT")
    print("================================")

    print(result["result"])