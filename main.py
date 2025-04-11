import logging
from pathlib import Path
from tqdm import tqdm

# Import modules from the data folder
from data.config import INPUT_IMAGES_DIR
from data.settings import load_settings, save_settings
from data.batch_manager import setup_batch_folders
from data.lm_studio import send_to_lm_studio

def process_images():
    """Main function to process all images in the input_images directory."""
    try:
        # Load settings and setup batch folders
        settings = load_settings()
        batch_id = settings["batchID"]
        batch_input, batch_output = setup_batch_folders(batch_id)
        
        # Retrieve all image files (jpg and png)
        try:
            image_files = list(INPUT_IMAGES_DIR.glob("*.jpg")) + list(INPUT_IMAGES_DIR.glob("*.png"))
        except OSError as e:
            error_msg = f"Error accessing input directory: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
            return
        
        if not image_files:
            msg = "No images found in the input_images directory."
            print(msg)
            logging.warning(msg)
            return
        
        # Initialize counters for logging purposes
        success_count = 0
        fail_count = 0
        
        # Process each image with a progress bar
        for image_path in tqdm(image_files, desc="Processing Images"):
            try:
                print(f"\nProcessing: {image_path.name}")
                response = send_to_lm_studio(image_path)
                
                if response:
                    try:
                        # Save the API response to a text file
                        output_file = batch_output / f"{image_path.stem}.txt"
                        with open(output_file, 'w') as f:
                            f.write(response)
                        print(f"Saved response to: {output_file}")
                        
                        # Move image to batch input folder after success
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
        
        # Update the batch ID for the next run
        try:
            settings["batchID"] += 1
            save_settings(settings)
        except Exception as e:
            error_msg = f"Error updating batch ID: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
            raise
        
        # Summary of processing
        print(f"\nBatch {batch_id} completed successfully.")
        print(f"Total images processed: {len(image_files)}")
        print(f"Successfully processed: {success_count}")
        print(f"Failed to process: {fail_count}")
        
    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

if __name__ == "__main__":
    process_images()
