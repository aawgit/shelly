import subprocess
from groq import Groq
import json
import sys

# Read the API key from a file
with open('/home/akalanka/projects/groq_key.txt', 'r') as file:
    api_key = file.read().strip()

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
    if state==0:
        prompt = [{
                    "role": "user",
                    "content": "I'm computer program created to assist a human by running shell commands."
                    f"The human asked me to '{nl_command}'. Please tell me "
                    "what shell commands to run to do the activity." 
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
    if state==1:
        prompt = nl_command
    llm_res = prompt_llm(prompt)
    try:
        res_parsed = json.loads(llm_res)
        return res_parsed, prompt, state
    except Exception as e:
        print(e)
        return -1, None, None

def execute_user_request(nl_command, state=0):
    prompt_history = []
    res_parsed, prompt_0, state = ask_llm(nl_command, state)
    if res_parsed != -1:
        prompt_history.extend(prompt_0)
        prompt_history.append({"role": "assistant", "content": json.dumps(res_parsed)})
        res_type = res_parsed.get("type")
        if res_type == "commands":
            commands = res_parsed.get("response")
            print(f"Following commands will run {commands}")
            # TODO: Add user input to verify
            for command in commands:
                answer = input(f" Shall I run '{command}'? (Yes/ No) ")
                if answer.lower()=='yes':
                    print(f"running shell commands {command}")
                    success, cmd_result = run_shell_command(command)
                    if success:
                        print(cmd_result)
                    else:
                        # TODO: Error handling
                        print(cmd_result)
                        break
                else:
                    print('Terminating command execution...')
                    break
            # If all commands ran successfully
            # TODO: Come up with a more intelligent message
            print('Commands executed successfully.')
        elif res_type == "information-request":
            state = 1
            needed_info = res_parsed.get("response")
            more_info = get_more_info(needed_info)
            prompt_history.append({"role": "user", "content": json.dumps(more_info)})
            llm_input = prompt_history
            execute_user_request(llm_input, state)
        else:
            # TODO: Create a restore point and retry from there
            print("Sorry, couldn't understand the LLMs response. You may try again.")
    else:
        print("Sorry, couldn't understand the LLMs response. You may try again.")

def get_more_info(prompts):
    """
    Prompts the user for information and saves responses in a dictionary.

    Args:
    prompts (list of str): List of prompts to ask the user.

    Returns:
    dict: Dictionary containing the prompts as keys and user responses as values.
    """
    user_info = {}
    for prompt in prompts:
        answer = input(f"{prompt}: ")
        user_info[prompt] = answer
    return user_info

def run_shell_command(command):
    try:
        # Run the shell command
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        # Return the command output
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        # Return the error output if the command fails
        return False, e.stderr

def get_user_input():
    """
    Collects user input passed as arguments when running the script.

    Returns:
    dict: Dictionary containing argument names and values.
    """
    if len(sys.argv) < 2:
        print("Please provide the command.")
        return None

    # Extract arguments (excluding the script name itself)
    arg1 = sys.argv[1]

    return arg1

if __name__ == "__main__":
    user_input = get_user_input()
    if user_input:
        print("User input:", user_input)
        execute_user_request(user_input)
