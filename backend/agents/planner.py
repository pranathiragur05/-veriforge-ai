from ..ai import ask_ai


def plan(task):

    instruction = """
You are the Planner Agent in a multi-agent AI reasoning
and verification system.

Analyze the user's task and create a clear plan.

Identify:
1. What the user is asking.
2. What type of task it is.
3. What information or evidence is needed.
4. Whether calculations, coding, or tools are required.
5. How the final answer should be verified.

Do not solve the task yet.

Return a clear and structured plan.
"""

    result = ask_ai(instruction, task)

    return {
        "agent": "planner",
        "task": task,
        "plan": result
    }


if __name__ == "__main__":

    task = input("Enter your task: ")

    result = plan(task)

    print("\n================================")
    print("PLANNER AGENT")
    print("================================")

    print(result["plan"])