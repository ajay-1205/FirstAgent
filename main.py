import os
from dotenv import load_dotenv
from google import genai




def main():

    #Loading API key from the .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("No API key found")
    client = genai.Client(api_key=api_key)

    #Getting response from the model
    Model = "gemini-2.5-flash"
    Contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    response = client.models.generate_content(
    model=Model, 
    contents=Contents
    )
    
    #Getting token counts
    if not response.usage_metadata:
        raise RuntimeError("No data regarding tokens are found")
    returned_response = response.text
    input_tokens = response.usage_metadata.prompt_token_count
    output_tokens = response.usage_metadata.candidates_token_count
    print(f"User prompt: {Contents}")
    print(f"Prompt tokens: {input_tokens}")
    print(f"Response tokens: {output_tokens}")
    print(response.text)
    

if __name__ == "__main__":
    main()
