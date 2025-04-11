import base64
import logging
import requests
from data.prompt import get_prompt
from data.config import LM_STUDIO_API_URL

def send_to_lm_studio(image_path):
    """Send image data to LM Studio API and return the response."""
    try:
        # Read image and encode to base64
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = get_prompt()
        
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
