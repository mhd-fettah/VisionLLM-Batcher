import os
import requests
from tqdm import tqdm
from pathlib import Path
import logging
import base64
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
LM_STUDIO_API_URL = os.getenv("LM_STUDIO_API_URL")

# Relative paths
INPUT_IMAGES_DIR = Path("input_images")
OUTPUT_DIR = Path("output_responses")
DATA_DIR = Path("data")
LOG_FILE = Path("processing.log")
SETTINGS_FILE = DATA_DIR / "settings.json"
PROMPT_FILE = INPUT_IMAGES_DIR / "prompt.txt"

def get_prompt():
    """Read prompt from file"""
    try:
        with open(PROMPT_FILE, 'r') as f:
            return f.read().strip()
    except IOError as e:
        error_msg = f"Error reading prompt file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        raise

def send_to_lm_studio(image_path):
    """Send image to LM Studio API"""
    try:
        # Read image and encode as base64
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Get current prompt
        prompt = get_prompt()
        
        # Prepare API request for vision model
        payload = {
            "model": "qwen2-vl-7b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.7
        }
        
        response = requests.post(LM_STUDIO_API_URL, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        error_msg = f"Error processing {image_path.name}: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        return None

# Add new paths
DATA_DIR = Path("G:/Git temp/UI2TechSpecs/UI-2-Tech-Spec-Sheet/data")
SETTINGS_FILE = DATA_DIR / "settings.json"
PROMPT_FILE = INPUT_IMAGES_DIR / "prompt.txt"

def load_settings():
    """Load settings from JSON file"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SETTINGS_FILE.exists():
        settings = {"batchID": 1}
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
        return settings
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except IOError as e:
        error_msg = f"Error saving settings: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        raise
    except json.JSONEncodeError as e:
        error_msg = f"Error encoding settings to JSON: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        raise

def process_images():
    """Main function to process all images"""
    try:
        # Load settings and setup batch
        settings = load_settings()
        batch_id = settings["batchID"]
        batch_input, batch_output = setup_batch_folders(batch_id)
        
        # Get all image files
        try:
            image_files = list(INPUT_IMAGES_DIR.glob("*.jpg")) + list(INPUT_IMAGES_DIR.glob("*.png"))
        except OSError as e:
            error_msg = f"Error accessing input directory: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
            return
        
        if not image_files:
            msg = "No images found in the input directory."
            print(msg)
            logging.warning(msg)
            return
        
        # Initialize counters
        success_count = 0
        fail_count = 0
        
        # Process images with progress bar
        for image_path in tqdm(image_files, desc="Processing Images"):
            try:
                print(f"\nProcessing: {image_path.name}")
                
                # Send to LM Studio
                response = send_to_lm_studio(image_path)
                
                if response:
                    try:
                        # Save response first
                        output_file = batch_output / f"{image_path.stem}.txt"
                        with open(output_file, 'w') as f:
                            f.write(response)
                        print(f"Saved response to: {output_file}")
                        
                        # Move image only after successful processing
                        new_image_path = batch_input / image_path.name
                        image_path.rename(new_image_path)
                        print(f"Moved image to: {new_image_path}")
                        success_count += 1
                    except (IOError, OSError) as e:
                        error_msg = f"Error saving/moving files for {image_path.name}: {str(e)}"
                        logging.error(error_msg)
                        print(error_msg)
                        fail_count += 1
                else:
                    fail_count += 1
                    
            except Exception as e:
                error_msg = f"Error processing {image_path.name}: {str(e)}"
                logging.error(error_msg)
                print(error_msg)
                fail_count += 1
        
        # Update batch ID for next run only after all images are processed
        try:
            settings["batchID"] += 1
            save_settings(settings)
        except Exception as e:
            error_msg = f"Error updating batch ID: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
            raise
        
        # Show detailed batch statistics
        print(f"\nBatch {batch_id} completed successfully.")
        print(f"Total images processed: {len(image_files)}")
        print(f"Successfully processed: {success_count}")
        print(f"Failed to process: {fail_count}")
        
    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

def setup_batch_folders(batch_id):
    """Create batch folders and move prompt file"""
    batch_input = INPUT_IMAGES_DIR / f"batch_{batch_id}"
    batch_output = OUTPUT_DIR / f"batch_{batch_id}"
    
    batch_input.mkdir(parents=True, exist_ok=True)
    batch_output.mkdir(parents=True, exist_ok=True)
    
    # Create prompt file if it doesn't exist
    if not PROMPT_FILE.exists():
        with open(PROMPT_FILE, 'w') as f:
            f.write(PROMPT)
    
    # Check if prompt file is empty
    if PROMPT_FILE.stat().st_size == 0:
        error_msg = "Error: Prompt file is empty. Please add the prompt text."
        logging.error(error_msg)
        raise ValueError(error_msg)
    
    return batch_input, batch_output

if __name__ == "__main__":
    process_images()