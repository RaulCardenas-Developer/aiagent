import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)



if api_key == None:
    raise RuntimeError("Api key is empty")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`
messages=[
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
response = client.chat.completions.create(
    model = "openrouter/free",messages=messages)
    

if args.verbose == True:
    if response.usage != None:
        prompt_token = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        print(f"User prompt: {args.user_prompt} \n"
            f"Prompt tokens: {prompt_token} \n"
        f"Response tokens: {completion_tokens}")

    else:
        raise RuntimeError("Failed API request")



print(response.choices[0].message.content)    

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
