from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Brand:
    """Représente une marque"""
    name: str
    holding_name: str
    verification_status: Optional[str] = None  # 'OK' ou 'NON'
    last_verified: Optional[datetime] = None
    
@dataclass
class Holding:
    """Représente un holding avec ses marques"""
    name: str
    brands: List[Brand]
    verification_date: Optional[datetime] = None

@dataclass
class VerificationResult:
    """Résultat de la vérification d'une marque"""
    brand: Brand
    is_verified: bool
    verification_date: datetime
    details: str = "" 