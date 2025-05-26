import logging
from pathlib import Path
from datetime import datetime
from services.brand_manager import BrandManager

def setup_logging():
    """Configure le système de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Point d'entrée principal du programme"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialiser le gestionnaire de marques
    manager = BrandManager()
    
    try:
        # Charger les marques depuis le fichier CSV
        input_file = "data/marques.csv"  # À adapter selon votre fichier
        logger.info(f"Chargement des marques depuis {input_file}")
        brands = manager.load_brands_from_csv(input_file)
        
        # Grouper par holding
        holdings = manager.group_by_holding(brands)
        logger.info(f"Nombre de holdings trouvés : {len(holdings)}")
        
        # Vérifier toutes les marques
        logger.info("Début de la vérification des marques")
        results = manager.verify_all_brands(brands)
        
        # Exporter les résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/resultats_verification_{timestamp}.csv"
        logger.info(f"Export des résultats vers {output_file}")
        manager.export_results_to_csv(results, output_file)
        
        # Afficher un résumé
        ok_count = sum(1 for r in results if r.is_verified)
        total = len(results)
        logger.info(f"Vérification terminée : {ok_count}/{total} marques OK")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution : {str(e)}")
        raise

if __name__ == "__main__":
    main() 