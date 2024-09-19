import cv2
import time
from datetime import datetime
import subprocess
import os  # Ensure the os module is imported

def capture_image():
    # Initialize the camera
    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Use the AVFoundation flag for macOS
    if not camera.isOpened():
        print("Failed to open the camera.")
        return None

    time.sleep(2)  # Allow the camera some time to adjust

    # Capture a single frame
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image.")
        camera.release()
        return None

    # Generate a filename with the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"photos/captured_image_{timestamp}.png"

    # Save the captured image to the specified path
    cv2.imwrite(image_path, frame)
    camera.release()
    print(f"Screenshot saved as {image_path}")
    return image_path

def run_extract_text(image_path):
    # Ensure the image has been saved correctly before proceeding
    if not image_path or not os.path.exists(image_path):
        print(f"Image path {image_path} is not accessible.")
        return None

    # Run the extract_text.py script with the captured image path
    print("\nExtracting text from the image...")
    extract_result = subprocess.run(['python3', 'extract_text.py', image_path], capture_output=True, text=True)
    print("Extract Text Output:\n", extract_result.stdout)  # Print the output for debugging
    if extract_result.stderr:
        print("Extract Text Error:\n", extract_result.stderr)  # Print errors if any

    # Check if extraction succeeded by extracting the filtered text from the output
    filtered_text = None
    for line in extract_result.stdout.splitlines():
        if line.startswith("Filtered Post Content:"):
            filtered_text = line.split("Filtered Post Content:")[-1].strip()
    
    if not filtered_text:
        print("Text extraction or filtering failed.")
        return None
    
    return filtered_text

def run_evaluate_with_ai(filtered_text):
    # Run the evaluate_with_ai.py script with the filtered text
    print("\nEvaluating extracted text with AI...")
    evaluate_result = subprocess.run(['python3', 'evaluate_with_ai.py', filtered_text], capture_output=True, text=True)
    print("Evaluate AI Output:\n", evaluate_result.stdout)  # Print the output for debugging
    if evaluate_result.stderr:
        print("Evaluate AI Error:\n", evaluate_result.stderr)  # Print errors if any

if __name__ == "__main__":
    # Step 1: Capture the image
    image_path = capture_image()
    if image_path:
        # Step 2: Extract text from the captured image
        filtered_text = run_extract_text(image_path)
        if filtered_text:
            # Step 3: Evaluate the extracted text with AI
            run_evaluate_with_ai(filtered_text)
