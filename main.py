import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Make sure you have a .env file with GEMINI_API_KEY set."
        )

    client = genai.Client(api_key=api_key)

    # Build messages
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )

        # Optional debug info
        if args.verbose and response.usage_metadata:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {response.usage_metadata.candidates_token_count}"
            )

        # Text OR function calls
        function_calls = response.function_calls
        function_results = []

        if function_calls:
            for fc in function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)
                
                if not function_call_result.parts:
                    raise RuntimeError("Function call returned no parts")
                
                part = function_call_result.parts[0]
                
                if part.function_response is None:
                    raise RuntimeError("Missing function_response")
                
                if part.function_response.response is None:
                    raise RuntimeError("Function response was empty")
                
                function_results.append(part)
                
                if args.verbose:
                    print(f"-> {part.function_response.response}")
                    
        else:
            print(response.text)

    except Exception as e:
        print("Gemini API error occurred, but setup is correct.")
        print(str(e))


if __name__ == "__main__":
    main()
