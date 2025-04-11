import os
import requests
from tqdm import tqdm
from pathlib import Path
import logging
import base64

# Configuration
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
PROMPT = """Analyze the attached image of a user interface and generate a minimal product requirement summary with the following structure:

Controller:
    Controller name (e.g., CounselorController)
    List the actions/methods needed (e.g., edit, update, uploadProfilePicture)

Database:
    Main table name
    Fields (column names + types if visible/inferable)
    Note any relationships (e.g., city → country foreign key)

View:
    Blade file name (e.g., counselor/edit.blade.php)
    Key components or sections (e.g., profile image upload, basic info form)

Other Notes:
    Form behavior (e.g., dynamic dropdowns, validation, file upload handling)
    Required/optional field assumptions
    Permissions or role assumptions if relevant

- Format the response in clean bullet points, no extra explanation. Keep it short and developer-friendly."""
INPUT_IMAGES_DIR = Path("G:/Git temp/UI2TechSpecs/UI-2-Tech-Spec-Sheet/input_images")
OUTPUT_DIR = Path("G:/Git temp/UI2TechSpecs/UI-2-Tech-Spec-Sheet/output_responses")
LOG_FILE = Path("G:/Git temp/UI2TechSpecs/UI-2-Tech-Spec-Sheet/processing.log")

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_to_lm_studio(image_path):
    """Send image to LM Studio API"""
    try:
        # Read image and encode as base64
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare API request for vision model
        payload = {
            "model": "qwen2-vl-7b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
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

def process_images():
    """Main function to process all images"""
    try:
        # Create directories if they don't exist
        INPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Get all image files
        image_files = list(INPUT_IMAGES_DIR.glob("*.jpg")) + list(INPUT_IMAGES_DIR.glob("*.png"))
        
        if not image_files:
            msg = "No images found in the input directory."
            print(msg)
            logging.warning(msg)
            return
        
        # Process images with progress bar
        for image_path in tqdm(image_files, desc="Processing Images"):
            print(f"\nProcessing: {image_path.name}")
            
            # Send to LM Studio
            response = send_to_lm_studio(image_path)
            
            if response:
                # Save response
                output_file = OUTPUT_DIR / f"{image_path.stem}.txt"
                with open(output_file, 'w') as f:
                    f.write(response)
                print(f"Saved response to: {output_file}")
                
    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

if __name__ == "__main__":
    process_images()