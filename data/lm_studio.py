import base64
import logging
import requests
from data.prompt import get_prompt
from data.config import LLM_API_URL, LLM_MODEL_NAME

def send_to_lm_studio(image_path):
    """Send image data to LM Studio API and return the response."""
    try:
        # Read image and encode to base64.
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = get_prompt()
        
        payload = {
            "model": LLM_MODEL_NAME,
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
        
        # Add a timeout parameter to avoid hanging indefinitely.
        response = requests.post(LLM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        json_response = response.json()
        
        # Validate the expected response structure.
        choices = json_response.get('choices')
        if choices and isinstance(choices, list) and len(choices) > 0:
            return choices[0].get('message', {}).get('content')
        else:
            error_msg = f"Unexpected response format: {json_response}"
            logging.error(error_msg)
            return None
    except Exception as e:
        logging.exception("Error processing %s", image_path.name)
        print(f"Error processing {image_path.name}: {str(e)}")
        return None
