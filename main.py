import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

def generate_response(prompt):

    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = prompt
    )
    print(response.text)
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
        )

def main():
    if len(sys.argv) < 2:
        sys.exit("No prompt provided, please enter a prompt line.")
    for i in range (1, len(sys.argv)):
        generate_response(sys.argv[i])

main()
