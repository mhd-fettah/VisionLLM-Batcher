import logging
from data.config import INPUT_IMAGES_DIR, OUTPUT_DIR, PROMPT_FILE

def setup_batch_folders(batch_id):
    """Create batch-specific input and output folders and verify the prompt file."""
    batch_input = INPUT_IMAGES_DIR / f"batch_{batch_id}"
    batch_output = OUTPUT_DIR / f"batch_{batch_id}"
    
    batch_input.mkdir(parents=True, exist_ok=True)
    batch_output.mkdir(parents=True, exist_ok=True)
    
    # Verify that the prompt file exists and is non-empty
    if not PROMPT_FILE.exists():
        error_msg = "Error: Prompt file does not exist. Please add the prompt text."
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    if PROMPT_FILE.stat().st_size == 0:
        error_msg = "Error: Prompt file is empty. Please add the prompt text."
        logging.error(error_msg)
        raise ValueError(error_msg)
    
    return batch_input, batch_output
