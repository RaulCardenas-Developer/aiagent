import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function



def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("Api key is empty")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )



    

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    iterations = False
    for _ in range(20):
    # call the model, handle responses, etc.
        response = client.chat.completions.create(
            model = "openrouter/free",
            messages=messages,
            tools=available_functions
        
        )
        if args.verbose == True:
            if response.usage != None:
                prompt_token = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens

                print(f"User prompt: {args.user_prompt} \n" 
                    f"Prompt tokens: {prompt_token} \n"
                f"Response tokens: {completion_tokens}")

            else:
                raise RuntimeError("Failed API request")

        message = response.choices[0].message
        messages.append(message) 

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == "":
                    raise Exception("result content is empty")
                if args.verbose == True:
                    print(f"-> {result_message['content']}")
                
                messages.append(result_message)

        else:
            print(message.content)
            iterations = True 
            break
        
    if not iterations:
        print("not enough iterations")
        exit(1)
        
    

if __name__ == "__main__":
    main()
