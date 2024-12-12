import sys
from src.runner import execute_user_request

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
