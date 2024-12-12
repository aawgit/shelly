from groq import Groq
import json
import sys
import os

# Read the API key from the environment variable
api_key = os.environ.get('GROQ_API_KEY')

if not api_key:
    raise ValueError("Error: The GROQ_API_KEY environment variable is not set.")

# Initialize the Groq client with the API key
client = Groq(
    api_key=api_key,
)


def prompt_llm(messages: list):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content


def ask_llm(nl_command, state=0):
    prompt = ""
    # Initial state
    if state == 0:
        prompt = [{
            "role": "user",
            "content": "You only speak JSON. I'm computer program created to assist a human by running shell commands."
                       f"The human asked me to '{nl_command}'. Please tell me "
                       "what shell commands to run to do the activity."
                       "If I need to run multiple commands, please return them in the correct order"
                       "Think about what more information you need and ask them."
                       "Please respond with a JSON format text in the following manner and don't include anything else"
                       "in the response."
                       """{"type": [Can be either "commands" or "information-request"],
                       "response": [List of shell commands or list of more information needed, separated by commas]
                       }

                       Example response 1:
                       {"type": "information-request",
                       "response": ["user id", "key path"]
                       }

                       Example response 2:
                       {"type": "commands",
                       "response": ["ssh -i 'keyfile.pem' user1@server"]
                       }
                  """
        }]
    # Responding to information request
    if state == 1:
        prompt = nl_command
    llm_res = prompt_llm(prompt)
    try:
        res_parsed = json.loads(llm_res)
        return res_parsed, prompt, state
    except Exception as e:
        print(e)
        return -1, None, None


def ensure_list(variable):
    if isinstance(variable, str):
        # Split the string by commas and remove any leading/trailing spaces
        return [item.strip() for item in variable.split(',')]
    elif isinstance(variable, list):
        return variable
    else:
        raise ValueError("Input should be either a list or a comma-separated string.")
