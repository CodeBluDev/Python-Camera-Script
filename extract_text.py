import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import sys
import os

def extract_text_from_image(image_path):
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Error: The image file {image_path} does not exist.")
        sys.exit(1)

    try:
        # Open the image file
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)
    
    # Pre-process the image: Convert to grayscale and enhance
    img = img.convert('L')  # Convert to grayscale
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen the image
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Increase contrast

    # Use Tesseract to extract text with specific configurations
    try:
        extracted_text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')  # PSM 6 assumes a single uniform block of text
        print("Extracted Text:\n", extracted_text)  # Debug: print the extracted text
    except pytesseract.TesseractError as e:
        print(f"Error during OCR: {e}")
        sys.exit(1)
    
    if not extracted_text.strip():
        print("No text found in the image. Try adjusting image quality or OCR settings.")
        sys.exit(1)
    
    return extracted_text

def filter_post_content(extracted_text):
    # Define patterns or keywords to filter out irrelevant text
    patterns_to_exclude = [
        r'\d{1,2}:\d{2}',  # Time patterns like 12:34
        r'https?://\S+',  # URLs
        r'@\w+',  # User handles
        r'#\w+',  # Hashtags
        r'—+',  # Long dashes or separators often found in UI
        r'^[\W_]+$',  # Lines that are only special characters
        r'facebook',  # UI elements like 'facebook'
        r'Post a story',  # Common Facebook UI text
        r'like|comment|share',  # Social media interaction buttons
    ]

    # Split text into lines
    lines = extracted_text.split('\n')

    # Filter lines based on patterns and heuristics
    relevant_lines = []
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:  # Skip empty or too short lines to avoid noise
            continue
        
        # Check if line matches any exclusion patterns
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in patterns_to_exclude):
            continue

        # Add the line if it seems to be relevant content
        relevant_lines.append(line)

    # Combine lines into coherent paragraphs or sentences
    filtered_text = " ".join(relevant_lines)
    
    # Further clean-up: Attempt to remove fragments by ensuring sentences are complete
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', filtered_text)
    filtered_sentences = [sentence for sentence in sentences if len(sentence.split()) > 3]  # Keeping sentences with more than 3 words
    
    final_filtered_text = " ".join(filtered_sentences)
    
    print("Filtered Post Content:", final_filtered_text)
    return final_filtered_text

if __name__ == "__main__":
    # Use the image path provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python3 extract_text.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    extracted_text = extract_text_from_image(image_path)
    filter_post_content(extracted_text)
