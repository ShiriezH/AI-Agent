import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


MAX_ITERATIONS = 20


def main():
    parser = argparse.ArgumentParser(description="AI Coding Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # Conversation history
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    for iteration in range(MAX_ITERATIONS):
        if args.verbose:
            print(f"\n--- Iteration {iteration + 1} ---")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
                temperature=0,
            ),
        )

        # 1️⃣ Add model candidates to conversation
        if not response.candidates:
            raise RuntimeError("Model returned no candidates")

        for candidate in response.candidates:
            messages.append(candidate.content)

        # 2️⃣ Handle function calls (if any)
        function_calls = response.function_calls
        function_responses = []

        if function_calls:
            for fc in function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)

                if not function_call_result.parts:
                    raise RuntimeError("Function call returned no parts")

                part = function_call_result.parts[0]

                if part.function_response is None:
                    raise RuntimeError("Missing function_response")

                if part.function_response.response is None:
                    raise RuntimeError("Empty function response")

                function_responses.append(part)

                if args.verbose:
                    print(f"-> {part.function_response.response}")

            # 3️⃣ Feed tool results back to the model
            messages.append(
                types.Content(
                    role="user",
                    parts=function_responses,
                )
            )

        else:
            # 4️⃣ No function calls → final answer
            print("\nFinal response:")
            print(response.text)
            return

    # Loop exhausted
    print("Error: maximum agent iterations reached without a final response")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
