import requests
import json

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
    
# Example usage
if __name__ == "__main__":
    # text = "Hello, this is a test for embedding."
    text = "¿Quién fue el primer presidente de los Estados Unidos?"
    try:
        embedding = get_embedding(text)
        print(f"Embedding ({len(embedding['embedding'])} dimensiones):")
        print("Embedding:", embedding)
    except Exception as e:
        print("Error:", e)