import logging
from data.config import PROMPT_FILE

def get_prompt():
    """Read the prompt text from the prompt file."""
    try:
        with open(PROMPT_FILE, 'r') as f:
            return f.read().strip()
    except IOError as e:
        error_msg = f"Error reading prompt file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        raise
