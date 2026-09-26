import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("Checking Gemini API key...")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found.")
    exit()

print("API key found.")
print("Testing Gemini...")

try:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="What is 25 × 18?"
    )

    print()
    print("================================")
    print("GEMINI TEST SUCCESSFUL")
    print("================================")
    print(response.text)

except Exception as error:
    print()
    print("================================")
    print("GEMINI TEST FAILED")
    print("================================")
    print(error)
