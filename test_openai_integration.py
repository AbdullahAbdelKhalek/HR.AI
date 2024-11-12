from dotenv import load_dotenv
import os
from openai import OpenAI

def test_chat_completion():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the OpenAI API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return

    try:
        # Initialize the OpenAI client with the API key
        client = OpenAI(api_key=api_key)

        # Create a chat completion using the specified model
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with your desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        # Access the content using dot notation
        print(response.choices[0].message.content.strip())

    except Exception as e:
        print(f"OpenAI API Error: {e}")

if __name__ == "__main__":
    test_chat_completion()
