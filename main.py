import os
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


response = client.chat.completions.create(
    model = "openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
)
print(response.choices[0].message.content)    

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
