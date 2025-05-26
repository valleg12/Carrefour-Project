import requests
import json

def test_api():
    url = "http://localhost:3000/api/search"
    
    # Test simple
    payload = {
        "chatModel": {
            "provider": "openai",
            "name": "gpt-4o-mini"
        },
        "embeddingModel": {
            "provider": "openai",
            "name": "text-embedding-3-large"
        },
        "optimizationMode": "accuracy",
        "focusMode": "webSearch",
        "query": "Qui est le propriétaire de la marque Garnier?",
        "history": [],
        "systemInstructions": "Réponds en français.",
        "stream": False
    }
    
    try:
        print("Test de connexion à l'API...")
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        print("Connexion réussie!")
        print("Réponse:", response.json())
    except requests.exceptions.ConnectionError:
        print("Erreur: Impossible de se connecter à l'API. Vérifiez que le serveur est en cours d'exécution.")
    except requests.exceptions.Timeout:
        print("Erreur: L'API ne répond pas dans le délai imparti.")
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    test_api() 