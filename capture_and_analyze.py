import cv2
import datetime
import requests
import os
import pytesseract
from PIL import Image, ImageEnhance
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
import base64

# Set your OpenAI API key
api_key = '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'

# Email configuration
email_sender = 'mendel@codebludev.com'  # Your email
email_recipient = 'rosenblummm@gmail.com'  # Recipient's email
sendgrid_api_key = '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'  # Your SendGrid API key

def capture_image():
    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Use AVFoundation flag for macOS
    if not camera.isOpened():
        print("Failed to open the camera.")
        return None

    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image.")
        camera.release()
        return None

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"photos/captured_image_{timestamp}.png"

    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    cv2.imwrite(image_path, frame)
    camera.release()
    print(f"Screenshot saved as {image_path}")
    return image_path

def convert_to_grayscale(image_path):
    try:
        img = Image.open(image_path)
        grayscale_path = image_path.replace('.png', '_grayscale.png')
        img.convert('L').save(grayscale_path)  # Save as grayscale without overwriting the original
        print(f"Grayscale image saved as {grayscale_path}")
        return grayscale_path
    except Exception as e:
        print(f"Failed to convert image to grayscale: {e}")
        return image_path

def brighten_image(image_path):
    try:
        img = Image.open(image_path)
        enhancer = ImageEnhance.Brightness(img)
        brightened_img = enhancer.enhance(2.5)  # Increase brightness significantly
        return brightened_img  # Return the brightened image instead of saving it
    except Exception as e:
        print(f"Failed to brighten image: {e}")
        return None

def extract_text_from_image(image_path):
    try:
        grayscale_image_path = convert_to_grayscale(image_path)  # Convert to grayscale for text extraction
        img = Image.open(grayscale_image_path)
        text = pytesseract.image_to_string(img, config='--psm 6')
        print(f"Extracted Text:\n{text}")
        return text
    except Exception as e:
        print(f"Failed to extract text from image: {e}")
        return None

def send_email(image_path, brightened_img):
    try:
        message = Mail(
            from_email=email_sender,
            to_emails=email_recipient,
            subject='New Realtor Inquiry',
            plain_text_content='The author is looking for a realtor. Here is the image.'
        )

        # Save the brightened image temporarily before sending
        brightened_image_path = image_path.replace('.png', '_brightened.png')
        brightened_img.save(brightened_image_path)

        # Attach the brightened image
        with open(brightened_image_path, 'rb') as attachment:
            encoded_file = base64.b64encode(attachment.read()).decode()  # Encode the file
            attached_file = Attachment(
                file_content=encoded_file,
                file_type='image/png',
                file_name=os.path.basename(brightened_image_path),
                disposition='attachment'
            )
            message.attachment = attached_file  # Add the attachment to the message

        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print("Email sent successfully.")
        
        # Clean up the brightened image after sending
        os.remove(brightened_image_path)
    except Exception as e:
        print(f"Failed to send email: {e}")

def analyze_text_with_openai(extracted_text, image_path):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    question = (
        "For the following post on Facebook, if the author is looking for a realtor, respond with 'send'; if not, respond with 'delete'. Here is the post:\n\n"
    )

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an assistant that analyzes text extracted from images to determine the author's intent."},
            {"role": "user", "content": f"{question}{extracted_text}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        action = result['choices'][0]['message']['content'].strip()
        print("Analysis Result:", action)

        if action.lower() == "send":
            brightened_img = brighten_image(image_path)  # Brighten the original image
            if brightened_img:
                send_email(image_path, brightened_img)  # Send the email with the brightened image
        elif action.lower() == "delete":
            os.remove(image_path)  # Delete the image if not needed
            print(f"Image {image_path} deleted as per instruction.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during text analysis: {e}")

if __name__ == "__main__":
    image_path = capture_image()
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        if extracted_text:
            analyze_text_with_openai(extracted_text, image_path)
