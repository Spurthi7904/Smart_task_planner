import requests

api_key = "GEMINI_API_KEY"

# Test listing available models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        models = response.json()
        print(" Available models:")
        for model in models.get("models", []):
            print(f"  - {model['name']} (Supports: {model.get('supportedGenerationMethods', [])})")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")