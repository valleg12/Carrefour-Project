import logging
from typing import Dict, List, Optional
from datetime import datetime
from .api_client import APIClient

class BrandVerification:
    def __init__(self, api_config: Dict):
        """
        Initialise le service de vérification des marques.
        
        Args:
            api_config: Configuration des APIs (brand_registry et company_registry)
        """
        self.api_client = APIClient(api_config)
        self.logger = logging.getLogger(__name__)

    def verify_brand_ownership(self, brand_name: str, holding_name: str) -> str:
        """
        Vérifie si une marque appartient toujours au holding spécifié.
        
        Args:
            brand_name: Nom de la marque à vérifier
            holding_name: Nom du holding supposé posséder la marque
            
        Returns:
            str: "OK" si la marque appartient au holding, "NON" sinon
        """
        try:
            is_owned = self.api_client.verify_ownership(brand_name, holding_name)
            return "OK" if is_owned else "NON"
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de {brand_name}: {str(e)}")
            return "NON"

    def batch_verify_brands(self, brands_data: List[Dict]) -> List[Dict]:
        """
        Vérifie l'appartenance pour une liste de marques.
        
        Args:
            brands_data: Liste de dictionnaires contenant les informations des marques
                        [{"brand_name": "...", "holding_name": "..."}, ...]
                        
        Returns:
            List[Dict]: Liste mise à jour avec le statut de vérification
        """
        results = []
        for brand in brands_data:
            status = self.verify_brand_ownership(
                brand["brand_name"],
                brand["holding_name"]
            )
            results.append({
                **brand,
                "statut_appartenance_verifie": status,
                "date_verification": datetime.now().isoformat()
            })
            
        return results

    def generate_verification_report(self, verification_results: List[Dict]) -> Dict:
        """
        Génère un rapport de vérification.
        
        Args:
            verification_results: Résultats des vérifications
            
        Returns:
            Dict: Rapport avec statistiques et anomalies détectées
        """
        total = len(verification_results)
        ok_count = sum(1 for r in verification_results if r["statut_appartenance_verifie"] == "OK")
        non_count = total - ok_count
        
        return {
            "total_verifications": total,
            "marques_ok": ok_count,
            "marques_non": non_count,
            "date_rapport": datetime.now().isoformat(),
            "anomalies": [
                r for r in verification_results 
                if r["statut_appartenance_verifie"] == "NON"
            ]
        } 