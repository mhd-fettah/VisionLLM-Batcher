import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
LM_STUDIO_API_URL = os.getenv("LM_STUDIO_API_URL")

# Directories and File Paths
BASE_DIR = Path.cwd()
INPUT_IMAGES_DIR = BASE_DIR / "input_images"
OUTPUT_DIR = BASE_DIR / "output_responses"
DATA_DIR = Path("G:/Git temp/UI2TechSpecs/UI-2-Tech-Spec-Sheet/data")
LOG_FILE = BASE_DIR / "processing.log"
SETTINGS_FILE = DATA_DIR / "settings.json"
PROMPT_FILE = INPUT_IMAGES_DIR / "prompt.txt"
