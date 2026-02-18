import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse




def main():
    #Parsing input from the CLI
    parser = argparse.ArgumentParser(description="AI-chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt should be added")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #Creating role for the model to give a flow to the chats
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #Loading API key from the .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found")
    client = genai.Client(api_key=api_key)

    #Getting response from the model
    Model = "gemini-2.5-flash"
    response = client.models.generate_content(
    model=Model, 
    contents=messages
    )
    
    #Getting token counts
    if not response.usage_metadata:
        raise RuntimeError("No data regarding tokens are found")
    returned_response = response.text
    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {input_tokens}")
        print(f"Response tokens: {output_tokens}")
    print(response.text)
    

if __name__ == "__main__":
    main()
