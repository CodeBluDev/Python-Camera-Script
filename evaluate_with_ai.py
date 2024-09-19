import requests
import sys

# Set your OpenAI API key
api_key = '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'

def rate_need_for_realtor(extracted_text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an assistant that evaluates whether the text suggests a need for a realtor. Please rate the intent on a scale of 1 to 10, where 10 indicates a strong need for a realtor and 1 indicates no need. If the text is not relevant or does not suggest a need for a realtor, respond with 'null'."},
            {"role": "user", "content": f"Based on the following extracted text from a Facebook post, please rate from 1 to 10 how likely it is that the person needs a realtor. Provide only the number or 'null' if no relevant text is found:\n\nExtracted Text: {extracted_text}"}
        ]
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        rating = result['choices'][0]['message']['content'].strip()

        # Check if the response is a valid number or 'null'
        if rating.isdigit() and 1 <= int(rating) <= 10:
            print("Rating:", rating)
        elif rating.lower() == 'null':
            print("Rating: null")
        else:
            print("Rating: null (invalid response)")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Use the filtered text provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python3 evaluate_with_ai.py <filtered_text>")
        sys.exit(1)

    filtered_text = sys.argv[1]
    rate_need_for_realtor(filtered_text)
