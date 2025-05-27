import pandas as pd
import requests
import json
import time

class BrandAnalysisQuick:
    def __init__(self):
        self.perplexica_url = "http://localhost:3000/api/search"

    def create_prompt(self, holding: str, known_brands: list) -> str:
        return f"""Analysez les marques de {holding} et leurs relations.
        Marques connues: {', '.join(known_brands)}
        
        Format JSON:
        {{
            "marques_manquantes": ["marque1", "marque2"],
            "sous_marques": [
                {{"marque_principale": "MARQUE", "sous_marque": "SOUS-MARQUE"}}
            ],
            "relations": [
                {{"marque1": "MARQUE1", "marque2": "MARQUE2", "type": "sous-marque/licence/distribution"}}
            ]
        }}"""

    def analyze_brands(self, holding: str, known_brands: list):
        print(f"\nAnalyzing brands for {holding}...")
        
        payload = {
            "chatModel": {
                "provider": "openai",
                "name": "gpt-4o-mini"
            },
            "embeddingModel": {
                "provider": "openai",
                "name": "text-embedding-3-large"
            },
            "query": self.create_prompt(holding, known_brands),
            "history": [],
            "stream": False
        }
        
        try:
            response = requests.post(
                self.perplexica_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if result and 'message' in result:
                message = result['message']
                json_start = message.find('{')
                json_end = message.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_str = message[json_start:json_end]
                    return json.loads(json_str)
            
            return None
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def process_quick_analysis(self, input_file):
        try:
            # Lire les 10 premières lignes du CSV
            df = pd.read_csv(input_file).head(10)
            
            # Grouper par holding
            holdings = df.groupby('Holding Name')['Brand Name'].apply(list).to_dict()
            results = []
            
            for holding, brands in holdings.items():
                result = self.analyze_brands(holding, brands)
                if result:
                    results.append({
                        'holding': holding,
                        'marques_manquantes': result.get('marques_manquantes', []),
                        'sous_marques': result.get('sous_marques', []),
                        'relations': result.get('relations', [])
                    })
                
                time.sleep(1)  # Pause pour éviter de surcharger l'API
            
            return results
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return []

if __name__ == "__main__":
    analyzer = BrandAnalysisQuick()
    results = analyzer.process_quick_analysis("Carrefour Geniathon - Tableau origine.csv")
    print(json.dumps(results, indent=2)) 