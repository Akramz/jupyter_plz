"""Top-level package for plz."""
import itertools
import os
import time
import requests
import threading
from typing import Tuple
from IPython.display import Code
from IPython.core.magic import register_line_magic

# Set Package-level constants
__author__ = """Akram Zaytar"""
__email__ = 'zaytarakram@gmail.com'
__version__ = '0.1.1'


def get_openai_api_key() -> str:
    """Get the OpenAI API key from the environment variable `OPENAI_API_KEY`. Raises an error if it doesn't exist.

    Returns:
        str: The OpenAI API key
    """

    # Get the OpenAI API key from the environment variable OPENAI_API_KEY
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    # If the OpenAI API key is not found, raise an error
    if openai_api_key is None:
        raise ValueError('The `OPENAI_API_KEY` environment variable is not found. '
                         'Please export it in your shell. '
                         'For example: `export OPENAI_API_KEY=<your_api_key>` or '
                         'add it to your `.bashrc` (or other) file.')

    # Return the OpenAI API key
    return openai_api_key


def process_prompt(line: str) -> Tuple[str, str]:
    """Split the command text into the `desired output format` (default is `Python`) and the prompt text.

    Args:
        line (str): <line> in %plz <line>

    Returns:
        Tuple[str, str]: The desired output format and the prompt.

    Description:
        The line may come in the following formats:
            - `--<output_format> "<prompt>"`
            - `"<prompt>"`
        The output format is optional and defaults to `Python`.
        The prompt is required.
        We want to:
            1. Verify that the line is in one of the above formats.
            2. Extract the output format if it exists. If it doesn't, set it to `Python`.
            3. Extract the prompt.
    """

    # Trim the line
    line = line.strip()

    # Verify that the line is in one of the above formats
    if not (line.startswith('--') or line.startswith('"')):
        raise ValueError('The line must start with `--` or `"`')

    # Extract the output format if it exists. If it doesn't, set it to `Python`
    output_format = line.split(' ')[0][2:] if line.startswith('--') else 'Python'

    # Extract the prompt
    prompt = line.split(' ', 1)[1][1:-1] if line.startswith('--') else line[1:-1]

    # Return the output format and the prompt
    return output_format, prompt


def get_suggestion(api_key,
                   prompt,
                   output_format,
                   top_p=1,
                   stop="```",
                   temperature=0,
                   suffix="\n```",
                   max_tokens=1000,
                   presence_penalty=0,
                   frequency_penalty=0,
                   model="text-davinci-003"):
    """Get the suggestion from OpenAI.

    Args:
        api_key (str): The OpenAI API key. Billing should be enabled by providing credit card information to OpenAI.
        prompt (str): The prompt text. Example prompt: `create a function that adds two numbers.`
        output_format (str): The desired output format. Example output format: `Python` or `Markdown`.
        top_p (float, optional): The top_p parameter. Defaults to 1.
        stop (str, optional): The stop text for the suggestion. Defaults to "```".
        temperature (int, optional): The temperature parameter. Defaults to 0.
        suffix (str, optional): The suffix parameter. Defaults to "\n```".
        max_tokens (int, optional): The max_tokens parameter. Defaults to 1000.
        presence_penalty (int, optional): The presence_penalty parameter. Defaults to 0.
        frequency_penalty (int, optional): The frequency_penalty parameter. Defaults to 0.
        model (str, optional): The LLM model identifier. Defaults to "text-davinci-003".

    Returns:
        str: The suggestion
    """

    # Use the `requests` library to send a POST request to OpenAI's API: https://api.openai.com/v1/completions
    res = requests.post(
        "https://api.openai.com/v1/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "top_p": top_p,
            "stop": stop,
            "temperature": temperature,
            "suffix": suffix,
            "max_tokens": max_tokens,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "model": model,
            "prompt": f"{prompt}\n```{output_format.capitalize()}\n",
        }
    )

    # Validate the response
    if res.status_code != 200:
        raise ValueError(f"Something went wrong: {res.text}")

    # Get the code from the response
    code = res.json()["choices"][0]["text"]

    # Return the code
    return code


@register_line_magic
def plz(line: str) -> Code:
    """Magic function to use plz in Jupyter notebooks.

    Args:
        line (str): the user prompt used to generate Python code.
    """

    # Get the user's API key
    api_key = get_openai_api_key()

    # Get the output format and the prompt
    output_format, prompt = process_prompt(line)

    # Define the spinner characters
    animation_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    # Create a flag to stop the spinner
    stop_flag = False

    def spinner_thread():
        # Create an infinite loop
        while not stop_flag:
            # Print the current character and flush the output
            print(f"{next(spinner_iter)}", end="\r", flush=True)

            # Delay the loop for 0.1 seconds
            time.sleep(0.1)

        # Clear the spinner
        print("↓" + (" " * 30), end="\r", flush=True)

    # Create an iterator for the spinner characters
    spinner_iter = itertools.cycle(animation_chars).__iter__()

    # Start the spinner in a separate thread
    thread = threading.Thread(target=spinner_thread)
    thread.start()

    # Get the suggestion
    code = get_suggestion(api_key, prompt, output_format)

    # Stop the spinner
    stop_flag = True
    thread.join()

    # Output the code back to the user
    return Code(code, language=output_format.lower())
