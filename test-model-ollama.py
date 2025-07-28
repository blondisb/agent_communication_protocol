import requests
import json
from colorama import Fore

def get_embedding(text, model="nomic-embed-text", base_url="http://localhost:11434"):
    url = f"{base_url}/api/embeddings"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": text
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()
        else:
            raise requests.exceptions.HTTPError(f"Error: {response.status_code} - {response.text}")
        
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Request failed: {e}")


def test_model_chat_completion(text):
    from litellm import completion

    response = completion(
        # model="ollama/llama3.1:8b",
        model="ollama/qwen2.5:0.5b",
        api_base = "http://localhost:11434",
        messages=[{"role": "user", "content": "¿Qué es la inteligencia artificial?"}]
    )

    return (response['choices'][0]['message']['content'])



# Example usage
if __name__ == "__main__":
    text = "¿Quién fue el primer presidente de los Estados Unidos?"

    try:
        # result = get_embedding(text)
        result = test_model_chat_completion(text)
        # print(f"Embedding ({len(embedding['embedding'])} dimensiones):")
        print(Fore.LIGHTBLACK_EX + "\n=======================\n RESULT: \n" +  result + Fore.RESET)

    except Exception as e:
        print("Error:", e)