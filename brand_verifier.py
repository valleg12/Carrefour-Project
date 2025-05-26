import requests
import pandas as pd
from datetime import datetime
import time
import logging
from collections import defaultdict

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration de l'API
MISTRAL_API_KEY = "KKtoSVdLkOLT3pbHw0bCzbCuV0rKHJoa"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def get_holding_brands(holding_name):
    """
    Demande à l'API Mistral de lister toutes les marques appartenant à une holding.
    """
    try:
        # Préparation du prompt pour Mistral
        prompt = f"""
        Liste toutes les marques qui appartiennent actuellement à la holding '{holding_name}'.
        Réponds uniquement avec une liste de marques, une par ligne, sans commentaires ni explications.
        """
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        brands = result['choices'][0]['message']['content'].strip().split('\n')
        
        # Nettoyage des résultats
        brands = [brand.strip() for brand in brands if brand.strip()]
        
        logger.info(f"Marques trouvées pour {holding_name} : {len(brands)}")
        return brands
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche des marques de {holding_name} : {str(e)}")
        return []

def process_csv(input_file, output_file):
    """
    Traite le fichier CSV et vérifie l'appartenance des marques.
    """
    try:
        # Lecture du CSV
        logger.info(f"Lecture du fichier {input_file}")
        df = pd.read_csv(input_file)
        
        # Création d'un dictionnaire pour stocker les marques par holding
        holding_brands = defaultdict(list)
        
        # Récupération des holdings uniques
        unique_holdings = df['Main Holding Name'].unique()
        logger.info(f"Nombre de holdings uniques trouvées : {len(unique_holdings)}")
        
        # Pour chaque holding, récupérer ses marques
        for holding in unique_holdings:
            logger.info(f"Recherche des marques pour {holding}")
            brands = get_holding_brands(holding)
            holding_brands[holding] = brands
            
            # Pause pour éviter de surcharger l'API
            time.sleep(1)
        
        # Création d'un nouveau DataFrame pour les résultats
        results = []
        for holding, brands in holding_brands.items():
            for brand in brands:
                results.append({
                    'Main Holding Name': holding,
                    'Brand Name': brand,
                    'Source': 'Mistral API',
                    'Date de vérification': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Conversion en DataFrame et sauvegarde
        results_df = pd.DataFrame(results)
        logger.info(f"Sauvegarde des résultats dans {output_file}")
        results_df.to_csv(output_file, index=False)
        logger.info(f"Traitement terminé avec succès. {len(results)} marques trouvées.")
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement : {str(e)}")
        raise

if __name__ == "__main__":
    input_file = "Carrefour Geniathon  - Tableau origine .csv"
    output_file = f"marques_par_holding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        process_csv(input_file, output_file)
    except Exception as e:
        logger.error(f"Erreur fatale : {str(e)}") 