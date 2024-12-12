import sys

from src.db import start_database, stop_database
from src.runner import run_shell_command, execute_user_request


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

def shelly_prompt(conn):
    """Interactive prompt for the user."""
    print("Welcome to Shelly! Type your commands below (type 'exit' to quit):")
    while True:
        user_input = input(">> ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting Shelly. Goodbye!")
            break
        execute_command(user_input, conn)

def execute_command(user_input, conn):
    """Handle user input, execute command, and persist result."""
    try:
        # Process natural language command (using your existing logic)
        success, result = execute_user_request(user_input)

        # Persist the command and result in the database
        # with conn:
        #     conn.execute('''
        #         INSERT INTO user_commands (command, result)
        #         VALUES (?, ?)
        #     ''', (user_input, result))

        # Display result
        print(result if success else f"Error: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    conn = start_database()

    try:
        # Launch the prompt
        shelly_prompt(conn)
    finally:
        # Ensure database is stopped even if an error occurs
        stop_database(conn)
