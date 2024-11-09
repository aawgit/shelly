# Shelly
Shelly us a simple command line tool which can convert natural language instructions to Linux shell commands and execute them. It uses a LLM in the back end and currently supports LLAMA on [Groq](https://console.groq.com/keys).

## Example usage
`$ shelly "Commit the current version of this repo and push to the main branch. Use an appropriate message"`

## Setup
 - Clone the repo
 - Create the Python virtual environment in the root directory of the project (Optional, but recommended)
 - Install Python dependencies `pip install -r requirements.txt`
 - Obtain a (free) API key from [Groq](https://console.groq.com/keys)
 - Set the GROQ_API_KEY environment variable to the Groq key.
 - Set the alias so that Shelly can be accessed from any working directory easily. `alias shelly='/home/<path to venv>/venv/bin/python3 /<path to the local repo>/shelly/main.py'
