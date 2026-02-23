import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompt import system_prompt
from call_function import available_functions, call_function




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
    for i in range(20):
        Model = "gemini-2.5-flash"
        response = client.models.generate_content(
        model=Model, 
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction=system_prompt)
        )

        if response.candidates:
            model_message = response.candidates[0].content
            candidate_content = response.candidates[0].content
            messages.append(
                types.Content(
                    role=candidate_content.role,
                    parts=candidate_content.parts,
                )
            )


        returned_response = response.text
        function_calls = response.function_calls
        #Getting token counts
        function_results = []

        # if args.verbose:
        #     print(f"User prompt: {args.user_prompt}")
        #     print(f"Prompt tokens: {input_tokens}")
        #     print(f"Response tokens: {output_tokens}")

        if function_calls:
            for function_call in function_calls:
                function_call_result = call_function(function_call)

                if not function_call_result.parts:
                    raise Exception("Error: Function call returned empty parts")

                first_part = function_call_result.parts[0]

                if not first_part.function_response:
                    raise Exception("Error: No function response in first part")

                if first_part.function_response.response is None:
                    raise Exception("Error: Function response has no response field")

                function_results.append(first_part)

                if args.verbose:
                    print(f"-> {first_part.function_response.response}")
                
                messages.append(function_call_result)
            continue

        else:
            print(returned_response)
            break
        
        
    

if __name__ == "__main__":
    main()
