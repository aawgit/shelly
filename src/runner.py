import json
import subprocess

from src.llm import ask_llm, ensure_list


def execute_user_request(nl_command, state=0):
    prompt_history = []
    res_parsed, prompt_0, state = ask_llm(nl_command, state)
    if res_parsed != -1:
        prompt_history.extend(prompt_0)
        prompt_history.append({"role": "assistant", "content": json.dumps(res_parsed)})
        res_type = res_parsed.get("type")
        if res_type == "commands":
            commands = ensure_list(res_parsed.get("response"))
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
