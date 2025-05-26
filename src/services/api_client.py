import requests
import logging
from typing import Dict, Optional
from datetime import datetime

class APIClient:
    def __init__(self, api_config: Dict):
        """
        Initialise le client API.
        
        Args:
            api_config: Configuration des APIs (URLs et clés API)
        """
        self.config = api_config
        self.logger = logging.getLogger(__name__)
        
    def get_brand_info(self, brand_name: str) -> Optional[Dict]:
        """
        Récupère les informations d'une marque depuis l'API WIPO.
        
        Args:
            brand_name: Nom de la marque à rechercher
            
        Returns:
            Dict: Informations sur la marque ou None en cas d'erreur
        """
        try:
            # API WIPO Global Brand Database
            url = "https://www3.wipo.int/branddb/jsp/select.jsp"
            params = {
                "q": f"{brand_name}",
                "fq": "country_desc:France",  # Filtrer pour la France
                "rows": 100,
                "wt": "json"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche de la marque {brand_name}: {str(e)}")
            return None
            
    def get_holding_info(self, holding_name: str) -> Optional[Dict]:
        """
        Récupère les informations d'un holding depuis l'API INSEE Sirene.
        
        Args:
            holding_name: Nom du holding à rechercher
            
        Returns:
            Dict: Informations sur le holding ou None en cas d'erreur
        """
        try:
            # API INSEE Sirene
            url = f"https://api.insee.fr/entreprises/sirene/V3/siret"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            params = {
                "q": f"denominationUniteLegale:{holding_name}",
                "nombre": 20
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche du holding {holding_name}: {str(e)}")
            return None
            
    def verify_ownership(self, brand_name: str, holding_name: str) -> bool:
        """
        Vérifie la relation d'appartenance entre une marque et un holding.
        
        Args:
            brand_name: Nom de la marque
            holding_name: Nom du holding
            
        Returns:
            bool: True si la relation est confirmée, False sinon
        """
        brand_info = self.get_brand_info(brand_name)
        holding_info = self.get_holding_info(holding_name)
        
        if not brand_info or not holding_info:
            return False
            
        try:
            # Vérifier dans les résultats WIPO
            brand_owner = None
            if 'response' in brand_info and 'docs' in brand_info['response']:
                for doc in brand_info['response']['docs']:
                    if 'holder' in doc:
                        brand_owner = doc['holder'].lower()
                        break
            
            # Vérifier dans les résultats INSEE
            holding_names = []
            if 'etablissements' in holding_info:
                for etab in holding_info['etablissements']:
                    if 'uniteLegale' in etab:
                        holding_names.append(etab['uniteLegale']['denominationUniteLegale'].lower())
            
            # Vérifier si le propriétaire de la marque correspond au holding
            if brand_owner and holding_names:
                return any(holding_name.lower() in brand_owner or 
                         any(h_name in brand_owner for h_name in holding_names))
            
            return False
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de la relation {brand_name} - {holding_name}: {str(e)}")
            return False 