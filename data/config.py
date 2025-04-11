import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file.
load_dotenv()

# Environment variables.
LLM_API_URL = os.getenv('LLM_API_URL')
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'qwen2-vl-7b-instruct')  # Default if not specified
if not LLM_API_URL:
    raise ValueError("LLM_API_URL is not set in the environment variables.")

# Directories and File Paths.
BASE_DIR = Path.cwd()
# Use an environment variable for DATA_DIR if provided, otherwise default to BASE_DIR / "data"
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
INPUT_IMAGES_DIR = BASE_DIR / "input_images"
OUTPUT_DIR = BASE_DIR / "output_responses"
LOG_FILE = BASE_DIR / "processing.log"
SETTINGS_FILE = DATA_DIR / "settings.json"
PROMPT_FILE = INPUT_IMAGES_DIR / "prompt.txt"
