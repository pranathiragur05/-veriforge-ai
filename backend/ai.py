import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found in .env file."
    )


client = Groq(
    api_key=api_key
)


def ask_ai(instruction, task):

    try:

        prompt = f"""
SYSTEM INSTRUCTIONS:

{instruction}

USER TASK:

{task}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        if response.choices:
            return response.choices[0].message.content

        return """
AI SERVICE ERROR

Groq returned an empty response.
"""

    except Exception as error:

        print("\n================================")
        print("GROQ API ERROR")
        print("================================")
        print(error)
        print("================================\n")

        return f"""
AI SERVICE ERROR

Groq error:

{error}
"""