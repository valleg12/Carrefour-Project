import pandas as pd
import requests
import json
import time
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm

class MultiprocessingQuick:
    def __init__(self):
        self.perplexica_url = "http://localhost:3000/api/search"
        self.num_processes = min(multiprocessing.cpu_count(), 4)  # Limiter à 4 processus max

    def create_prompt(self, brand_name: str, company_name: str) -> str:
        return f"""Please provide factual information about the brand '{brand_name}' and its relationship with '{company_name}'.
        Focus on verifiable facts and include specific details about ownership and relationship.
        Format your response in JSON with the following fields:
        {{
            "belongs_to": true/false,
            "explanation": "Explanation in French",
            "sources": ["list of sources"],
            "confidence": number (0-100)
        }}"""

    def verify_brand(self, args):
        brand_name, company_name = args
        print(f"\nVerifying {brand_name} for {company_name}...")
        
        payload = {
            "chatModel": {
                "provider": "openai",
                "name": "gpt-4o-mini"
            },
            "embeddingModel": {
                "provider": "openai",
                "name": "text-embedding-3-large"
            },
            "query": self.create_prompt(brand_name, company_name),
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
                    return {
                        'brand': brand_name,
                        'holding': company_name,
                        **json.loads(json_str)
                    }
            
            return None
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def process_quick_multiprocessing(self, input_file):
        try:
            # Lire les 10 premières lignes du CSV
            df = pd.read_csv(input_file).head(10)
            
            # Préparer les arguments pour le multiprocessing
            args_list = [(row['Brand Name'], row['Holding Name']) 
                        for _, row in df.iterrows()]
            
            # Créer un pool de processus
            with Pool(processes=self.num_processes) as pool:
                # Utiliser tqdm pour afficher la progression
                results = list(tqdm(
                    pool.imap(self.verify_brand, args_list),
                    total=len(args_list),
                    desc="Vérification des marques"
                ))
            
            # Filtrer les résultats None
            results = [r for r in results if r is not None]
            
            return results
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return []

if __name__ == "__main__":
    processor = MultiprocessingQuick()
    results = processor.process_quick_multiprocessing("Carrefour Geniathon - Tableau origine.csv")
    print(json.dumps(results, indent=2)) 