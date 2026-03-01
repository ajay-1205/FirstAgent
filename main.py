import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompt import system_prompt
from call_function import available_functions, call_function
import time
from collections import deque

REQUEST_LIMIT = 5          # max requests
TIME_WINDOW = 60           # seconds
request_times = deque()


def main():
    #Parsing input from the CLI
    parser = argparse.ArgumentParser(description="AI-chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt should be added")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    function_responses = []

    #Creating role for the model to give a flow to the chats
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #Loading API key from the .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found")
    client = genai.Client(api_key=api_key)

    #Getting response from the model
    MAX_STEPS = 8  # reduce from 20

    for i in range(MAX_STEPS):
        # SAFE MEMORY TRIMMING
        if len(messages) > 8:
            # Always keep the last 4 messages intact
            messages = messages[-8:]

        current_time = time.time()

        # Remove timestamps older than 60 seconds
        while request_times and current_time - request_times[0] > TIME_WINDOW:
            request_times.popleft()

        # If limit reached, wait
        if len(request_times) >= REQUEST_LIMIT:
            sleep_time = TIME_WINDOW - (current_time - request_times[0])
            print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

        # Record this request time
        request_times.append(time.time())



        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        function_calls = response.function_calls
        returned_response = response.text

        # If tool call exists
        if function_calls:
            for function_call in function_calls:

                function_call_result = call_function(function_call)

                if not function_call_result.parts:
                    raise Exception("Empty tool response")

                first_part = function_call_result.parts[0]

                if args.verbose:
                    print(f"-> {first_part.function_response.response}")

                # Append ONLY tool response
                messages.append(function_call_result)

                # TERMINATION LOGIC
                if function_call.name in ["write_file", "run_python_file"]:
                    print("Operation completed.")
                    return

            continue

        # No tool call = final answer
        else:
            print(returned_response)
            return
        
        
    

if __name__ == "__main__":
    main()
