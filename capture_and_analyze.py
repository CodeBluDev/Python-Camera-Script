pip uninstall opencv-python
pip uninstall requests
pip uninstall pytesseract
pip uninstall Pillow
pip uninstall sendgrid


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
        img = img.convert('L')
        img.save(image_path)  # Overwrite the original image
        print(f"Image converted to grayscale and saved as {image_path}")
        return image_path
    except Exception as e:
        print(f"Failed to convert image to grayscale: {e}")
        return image_path

def brighten_image(image_path):
    try:
        img = Image.open(image_path)
        enhancer = ImageEnhance.Brightness(img)
        brightened_img = enhancer.enhance(1.5)  # Increase brightness
        brightened_img.save(image_path)  # Overwrite the original image
        print(f"Brightened image saved as {image_path}")
    except Exception as e:
        print(f"Failed to brighten image: {e}")

def extract_text_from_image(image_path):
    try:
        grayscale_image_path = convert_to_grayscale(image_path)
        img = Image.open(grayscale_image_path)
        text = pytesseract.image_to_string(img, config='--psm 6')
        print(f"Extracted Text:\n{text}")
        return text
    except Exception as e:
        print(f"Failed to extract text from image: {e}")
        return None

def send_email(image_path):
    try:
        message = Mail(
            from_email=email_sender,
            to_emails=email_recipient,
            subject='New Realtor Inquiry',
            plain_text_content='The author is looking for a realtor. Here is the image.'
        )

        # Attach the image
        with open(image_path, 'rb') as attachment:
            encoded_file = base64.b64encode(attachment.read()).decode()  # Encode the file
            attached_file = Attachment(
                file_content=encoded_file,
                file_type='image/png',
                file_name=os.path.basename(image_path),
                disposition='attachment'
            )
            message.attachment = attached_file  # Add the attachment to the message

        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def analyze_text_with_openai(extracted_text):
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
            brighten_image(image_path)  # Brighten the image
            send_email(image_path)  # Send the email
        elif action.lower() == "delete":
            os.remove(image_path)
            print(f"Image {image_path} deleted as per instruction.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during text analysis: {e}")

if __name__ == "__main__":
    image_path = capture_image()
    if image_path:
        extracted_text = extract_text_from_image(image_path)
        if extracted_text:
            analyze_text_with_openai(extracted_text)
