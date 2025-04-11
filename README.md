# Image Processor for UI to Tech Specs

This application processes UI images and generates technical specifications using a local AI model via LM Studio.

## Features
- Processes images in batches
- Generates technical specifications in text format
- Tracks processing history with batch IDs
- Detailed logging and error handling
- Automatic folder organization
- Progress tracking with visual indicators

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mhd-fettah/UI-2-Tech-Spec-Sheet.git
```

2. Navigate to the project directory:
```bash
cd UI2TechSpecs
```

3. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

4. Install required packages:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with the API URL of your LM Studio instance the default is :  :
```plaintext
LM_STUDIO_API_URL=http://localhost:1234/v1/chat/completions
```

## Usage

1. Place your UI images in the `input_images` folder
2. Add your prompt in `input_images/prompt.txt`
3. Run the application:
```bash
python image_processor.py
```

4. Processed results will be saved in `output_responses` folder

## Folder Structure
```
.
├── input_images/          # Folder for input images
├── output_responses/      # Folder for processed results
├── data/                  # Application data and settings
├── .env                   # Environment variables
├── image_processor.py     # Main application script
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## Requirements
- Python 3.8+
- LM Studio running locally
- Python packages:
  - requests
  - python-dotenv
  - tqdm

## Configuration

The application can be configured through the following files:

1. `.env` - Contains environment variables
2. `input_images/prompt.txt` - Contains the processing prompt
3. `data/settings.json` - Contains application settings

## Troubleshooting

1. **LM Studio not responding**:
   - Ensure LM Studio is running with the API enabled
   - Verify the API URL in `.env` matches your LM Studio configuration

2. **Prompt file issues**:
   - Ensure `input_images/prompt.txt` exists and is not empty
   - The file should contain your processing instructions

3. **Image processing errors**:
   - Supported formats: JPG, PNG
   - Ensure images are clear and properly formatted

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
```