# test_openai.py

import openai

def test_openai_import():
    print(f"OpenAI version: {openai.__version__}")
    print("OpenAI module imported successfully.")

if __name__ == "__main__":
    test_openai_import()
