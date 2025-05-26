import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'brand_monitoring'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Configuration des API
API_CONFIG = {
    'brand_registry': {
        'base_url': os.getenv('BRAND_REGISTRY_URL', 'https://api.brand-registry.com'),
        'api_key': os.getenv('BRAND_REGISTRY_API_KEY', '')
    },
    'company_registry': {
        'base_url': os.getenv('COMPANY_REGISTRY_URL', 'https://api.company-registry.com'),
        'api_key': os.getenv('COMPANY_REGISTRY_API_KEY', '')
    }
}

# Configuration du monitoring
MONITORING_CONFIG = {
    'check_interval': int(os.getenv('CHECK_INTERVAL', '86400')),  # en secondes (24h par défaut)
    'alert_threshold': int(os.getenv('ALERT_THRESHOLD', '1')),    # nombre de changements avant alerte
    'log_level': os.getenv('LOG_LEVEL', 'INFO')
}

# Chemins des fichiers
FILE_PATHS = {
    'data_dir': os.getenv('DATA_DIR', 'data'),
    'log_dir': os.getenv('LOG_DIR', 'logs'),
    'export_dir': os.getenv('EXPORT_DIR', 'exports')
}

# Créer les répertoires nécessaires
for path in FILE_PATHS.values():
    os.makedirs(path, exist_ok=True) 