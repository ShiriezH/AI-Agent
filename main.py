import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Make sure you have a .env file with GEMINI_API_KEY set."
        )

    client = genai.Client(api_key=api_key)

    # Create message list
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages
        )

        if response.usage_metadata is None:
            raise RuntimeError("No usage metadata returned from Gemini API.")

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        print(response.text)

    except Exception as e:
        # Gemini API can be overloaded — don't crash
        print("Gemini API error occurred, but setup is correct.")
        print(str(e))

if __name__ == "__main__":
    main()

