import logging
import time
import uuid
from pathlib import Path

# Setup centralized logging using the LOG_FILE defined in the config.
from data.config import LOG_FILE, INPUT_IMAGES_DIR, OUTPUT_DIR
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from data.settings import load_settings, save_settings
from data.batch_manager import setup_batch_folders
from data.lm_studio import send_to_lm_studio
from data.display_manager import init_progress, update_description, write_message, print_summary

def process_images():
    """Main function to process all images in the input_images directory."""
    try:
        # Load settings and set up batch folders
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

        success_count = 0
        fail_count = 0
        total_images = len(image_files)
        start_time = time.time()

        # Initialize the progress bar using our display manager module.
        pbar = init_progress(total_images)

        # Process each image
        for image_path in image_files:
            update_description(pbar, image_path.name)
            iteration_start = time.time()

            response = send_to_lm_studio(image_path)
            if response:
                try:
                    # Save the API response to a file.
                    output_file = batch_output / f"{image_path.stem}.txt"
                    with open(output_file, 'w') as f:
                        f.write(response)
                    write_message(pbar, f"[+] Saved response for {image_path.name}")

                    # Move image after successful processing.
                    new_image_path = batch_input / image_path.name
                    # Avoid file name collision by appending a unique identifier if needed.
                    if new_image_path.exists():
                        new_image_path = batch_input / f"{image_path.stem}_{uuid.uuid4().hex}{image_path.suffix}"
                    image_path.rename(new_image_path)
                    write_message(pbar, f"[+] Moved {image_path.name}")
                    success_count += 1
                except (IOError, OSError) as e:
                    write_message(pbar, f"[-] Error handling {image_path.name}: {str(e)}")
                    logging.exception(f"Error handling {image_path.name}")
                    fail_count += 1
            else:
                write_message(pbar, f"[-] Failed processing {image_path.name}")
                fail_count += 1

            iter_time = time.time() - iteration_start
            write_message(pbar, f"    -> Took {iter_time:.2f} seconds.")
            pbar.update(1)

        total_time = time.time() - start_time
        avg_time = total_time / total_images if total_images else 0

        # Update batch ID for the next run.
        try:
            settings["batchID"] += 1
            save_settings(settings)
        except Exception as e:
            error_msg = f"Error updating batch ID: {str(e)}"
            logging.exception(error_msg)
            print(error_msg)
            raise

        # Print the final processing summary.
        print_summary(batch_id, total_images, success_count, fail_count, total_time, avg_time)

    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        logging.exception(error_msg)
        print(error_msg)

if __name__ == "__main__":
    process_images()
