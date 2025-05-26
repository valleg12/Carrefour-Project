import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from ..models.brand_model import Brand, Holding, VerificationResult
from .api_client import APIClient

class BrandManager:
    def __init__(self, data_dir: str = "data"):
        """
        Initialise le gestionnaire de marques.
        
        Args:
            data_dir: Répertoire pour stocker/charger les données
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.api_client = APIClient({})
        
    def load_brands_from_csv(self, file_path: str) -> List[Brand]:
        """
        Charge les marques depuis un fichier CSV.
        Format attendu: colonnes 'Brand Name' et 'Main Holding Name'
        
        Args:
            file_path: Chemin vers le fichier CSV
            
        Returns:
            List[Brand]: Liste des marques chargées
        """
        df = pd.read_csv(file_path, encoding='utf-8')
        brands = []
        
        for _, row in df.iterrows():
            brand = Brand(
                name=row['Brand Name'],
                holding_name=row['Main Holding Name']
            )
            brands.append(brand)
            
        return brands
        
    def group_by_holding(self, brands: List[Brand]) -> List[Holding]:
        """
        Groupe les marques par holding.
        
        Args:
            brands: Liste des marques à grouper
            
        Returns:
            List[Holding]: Liste des holdings avec leurs marques
        """
        holdings_dict: Dict[str, List[Brand]] = {}
        
        # Grouper les marques par holding
        for brand in brands:
            if brand.holding_name not in holdings_dict:
                holdings_dict[brand.holding_name] = []
            holdings_dict[brand.holding_name].append(brand)
        
        # Créer les objets Holding
        holdings = [
            Holding(name=holding_name, brands=brands_list)
            for holding_name, brands_list in holdings_dict.items()
        ]
        
        return holdings
        
    def verify_brand(self, brand: Brand) -> VerificationResult:
        """
        Vérifie si une marque appartient toujours à son holding.
        
        Args:
            brand: Marque à vérifier
            
        Returns:
            VerificationResult: Résultat de la vérification
        """
        is_verified = self.api_client.verify_ownership(brand.name, brand.holding_name)
        verification_date = datetime.now()
        
        # Mettre à jour le statut de la marque
        brand.verification_status = "OK" if is_verified else "NON"
        brand.last_verified = verification_date
        
        return VerificationResult(
            brand=brand,
            is_verified=is_verified,
            verification_date=verification_date
        )
        
    def verify_all_brands(self, brands: List[Brand]) -> List[VerificationResult]:
        """
        Vérifie toutes les marques.
        
        Args:
            brands: Liste des marques à vérifier
            
        Returns:
            List[VerificationResult]: Résultats des vérifications
        """
        results = []
        for brand in brands:
            result = self.verify_brand(brand)
            results.append(result)
        return results
        
    def export_results_to_csv(self, results: List[VerificationResult], output_file: str):
        """
        Exporte les résultats dans un fichier CSV.
        
        Args:
            results: Résultats des vérifications
            output_file: Chemin du fichier de sortie
        """
        data = []
        for result in results:
            data.append({
                'Brand Name': result.brand.name,
                'Main Holding Name': result.brand.holding_name,
                'Statut Appartenance vérifié': result.brand.verification_status,
                'Date Vérification': result.verification_date.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8') 