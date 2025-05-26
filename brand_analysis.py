import pandas as pd
import requests
import json
from typing import Dict, List, Tuple
import time
import re
from collections import defaultdict

class BrandAnalysis:
    def __init__(self):
        self.perplexica_url = "http://localhost:3000/api/search"
        self.verified_brands_file = "brand_verification_results.csv"
        self.holdings_brands_file = "holdings_brands.csv"

    def create_prompt(self, holding: str, known_brands: List[str]) -> str:
        """Crée un prompt simple pour vérifier les marques manquantes et les sous-marques."""
        return f"""Marques connues de {holding}: {', '.join(known_brands)}

1. Liste toutes les marques manquantes
2. Liste toutes les sous-marques (exemple: MIR Couleur est une sous-marque de MIR)

Format JSON:
{{
    "marques_manquantes": ["marque1", "marque2"],
    "sous_marques": [
        {{"marque_principale": "MIR", "sous_marque": "MIR Couleur"}}
    ]
}}"""

    def verify_holding_brands(self, holding: str, known_brands: List[str]) -> Dict:
        """Vérifie les marques d'une holding via l'API Perplexica."""
        print(f"\nVérification des marques de {holding}...")
        
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
            "query": self.create_prompt(holding, known_brands),
            "history": [],
            "systemInstructions": "Tu es un expert en marques. Liste les marques manquantes et les sous-marques. Réponds en français avec le format JSON demandé.",
            "stream": False
        }
        
        max_retries = 3
        retry_delay = 30
        search_timeout = 300
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.perplexica_url,
                    json=payload,
                    timeout=search_timeout
                )
                response.raise_for_status()
                
                result = response.json()
                message_content = result.get('message', '{}')
                
                if isinstance(message_content, str):
                    # Nettoyer le contenu JSON
                    message_content = message_content.replace('```json', '').replace('```', '').strip()
                    try:
                        content = json.loads(message_content)
                        if isinstance(content, dict):
                            # Vérifier si nous avons au moins une des clés attendues
                            if 'marques_manquantes' in content or 'sous_marques' in content:
                                print(f"Réponse reçue pour {holding}")
                                return content
                            else:
                                print(f"Format de réponse invalide pour {holding}")
                    except json.JSONDecodeError as e:
                        print(f"Erreur de décodage JSON pour {holding}: {str(e)}")
                
                if attempt < max_retries - 1:
                    print(f"Tentative {attempt + 1} échouée, nouvelle tentative dans {retry_delay} secondes...")
                    time.sleep(retry_delay)
                else:
                    print(f"Échec de la vérification pour {holding} après toutes les tentatives")
                    return None
                    
            except Exception as e:
                print(f"Erreur lors de la vérification de {holding}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    return None

    def clean_brand_list(self, brands: List[str]) -> List[str]:
        """Nettoie la liste des marques en supprimant les doublons et en normalisant les noms."""
        # Normaliser les noms (supprimer les espaces en trop, mettre en minuscules)
        normalized = [brand.strip().lower() for brand in brands]
        # Supprimer les doublons tout en préservant l'ordre
        seen = set()
        cleaned = []
        for brand in brands:
            norm = brand.strip().lower()
            if norm not in seen:
                seen.add(norm)
                cleaned.append(brand)
        return cleaned

    def extract_sub_brands(self, brands: List[str]) -> List[Dict]:
        """Extrait les sous-marques et crée une hiérarchie."""
        sub_brands = []
        for brand in brands:
            # Vérifier si c'est une sous-marque (contient un espace ou un tiret)
            if ' ' in brand or '-' in brand:
                parts = brand.replace('-', ' ').split()
                if len(parts) > 1:
                    main_brand = parts[0]
                    sub_brand = ' '.join(parts[1:])
                    sub_brands.append({
                        'Main Holding Name': '',  # Sera rempli plus tard
                        'Brand Name': main_brand,
                        'Sub-Brand Name': sub_brand,
                        'Marque Parente': main_brand,
                        'Statut sous marque': 'Vrai'
                    })
            else:
                # Marque principale
                sub_brands.append({
                    'Main Holding Name': '',  # Sera rempli plus tard
                    'Brand Name': brand,
                    'Sub-Brand Name': '',
                    'Marque Parente': '',
                    'Statut sous marque': 'Faux'
                })
        return sub_brands

    def process_holdings(self):
        """Traite toutes les holdings et leurs marques."""
        try:
            # Lire le fichier de vérification
            df = pd.read_csv(self.verified_brands_file)
            
            # Créer un dictionnaire des marques par holding
            holdings_brands = defaultdict(list)
            for _, row in df.iterrows():
                if row['Propriété_Directe']:
                    holdings_brands[row['Holding Name']].append(row['Brand Name'])
            
            # Créer les DataFrames pour les fichiers de sortie
            holdings_df = pd.DataFrame(columns=['Holding', 'Marques', 'Nouvelles Marques'])
            sub_brands_df = pd.DataFrame(columns=['Main Holding Name', 'Brand Name', 'Sub-Brand Name', 'Marque Parente', 'Statut sous marque'])
            
            # Pour chaque holding, vérifier les marques manquantes
            for holding, known_brands in holdings_brands.items():
                print(f"\nTraitement de {holding}...")
                
                # Nettoyer les marques connues
                known_brands = self.clean_brand_list(known_brands)
                
                # Vérifier les marques via l'API
                result = self.verify_holding_brands(holding, known_brands)
                
                # Initialiser la liste des nouvelles marques
                new_brands = []
                
                if result:
                    # Traiter les marques manquantes
                    if 'marques_manquantes' in result:
                        new_brands = self.clean_brand_list(result['marques_manquantes'])
                    
                    # Traiter les sous-marques
                    if 'sous_marques' in result:
                        for sub_brand_info in result['sous_marques']:
                            main_brand = sub_brand_info['marque_principale']
                            sub_brand = sub_brand_info['sous_marque']
                            
                            # Ajouter la marque principale si elle n'existe pas déjà
                            if not any(row['Brand Name'] == main_brand for _, row in sub_brands_df.iterrows()):
                                sub_brands_df = pd.concat([sub_brands_df, pd.DataFrame([{
                                    'Main Holding Name': holding,
                                    'Brand Name': main_brand,
                                    'Sub-Brand Name': '',
                                    'Marque Parente': '',
                                    'Statut sous marque': 'Faux'
                                }])], ignore_index=True)
                            
                            # Ajouter la sous-marque
                            sub_brands_df = pd.concat([sub_brands_df, pd.DataFrame([{
                                'Main Holding Name': holding,
                                'Brand Name': sub_brand,
                                'Sub-Brand Name': sub_brand,
                                'Marque Parente': main_brand,
                                'Statut sous marque': 'Vrai'
                            }])], ignore_index=True)
                
                # Ajouter la holding et ses marques au DataFrame principal
                holdings_df = pd.concat([holdings_df, pd.DataFrame({
                    'Holding': [holding],
                    'Marques': [', '.join(known_brands)],
                    'Nouvelles Marques': [', '.join(new_brands) if new_brands else 'Aucune']
                })], ignore_index=True)
            
            # Sauvegarder les fichiers
            holdings_df.to_csv(self.holdings_brands_file, index=False)
            sub_brands_df.to_csv('sub_brands.csv', index=False)
            print(f"\nFichiers sauvegardés:")
            print(f"- {self.holdings_brands_file}")
            print(f"- sub_brands.csv")
            
            # Afficher un résumé
            print("\nRésumé:")
            print(f"Nombre de holdings traitées: {len(holdings_df)}")
            total_brands = sum(len(row['Marques'].split(', ')) for _, row in holdings_df.iterrows())
            total_new_brands = sum(len(row['Nouvelles Marques'].split(', ')) if row['Nouvelles Marques'] != 'Aucune' else 0 for _, row in holdings_df.iterrows())
            print(f"Nombre total de marques (sans doublons): {total_brands}")
            print(f"Nombre de nouvelles marques détectées: {total_new_brands}")
            print(f"Nombre de sous-marques identifiées: {len(sub_brands_df[sub_brands_df['Statut sous marque'] == 'Vrai'])}")
            
        except Exception as e:
            print(f"Erreur lors du traitement: {str(e)}")
            raise e

def main():
    analyzer = BrandAnalysis()
    analyzer.process_holdings()

if __name__ == "__main__":
    main() 