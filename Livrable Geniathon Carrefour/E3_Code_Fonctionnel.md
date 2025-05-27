# E3 - Code Fonctionnel

## 1. Lien vers le Code Source
Le code source est disponible sur GitHub : https://github.com/valleg12/Carrefour-Project

## 2. Documentation Technique

### 2.1 Structure du Projet
```
Carrefour-Project/
├── brand_verification/              # Module principal de vérification
│   ├── brand_verification.py       # Script de vérification des marques
│   └── README.md                   # Documentation spécifique au module
│
├── brand_verification_multiprocessing/  # Module d'optimisation
│   ├── brand_verification_multiprocessing.py  # Version parallélisée
│   └── README.md                   # Documentation spécifique au module
│
├── brand_analysis/                 # Module d'analyse
│   ├── brand_analysis.py          # Outil d'analyse des marques
│   └── README.md                  # Documentation spécifique au module
│
├── docs/                          # Documentation générale
│   ├── strategy.md               # Stratégie de code employée
│   ├── code_explanation.md       # Explication détaillée du code
│   └── cost_analysis.md          # Analyse des coûts du système
│
├── Carrefour Geniathon - Tableau origine.csv  # Fichier source des données
├── requirements.txt              # Dépendances Python
└── LICENSE                       # Licence MIT
```

### 2.2 Modules Principaux

#### 2.2.1 BrandVerification
- Vérification des marques
- Gestion des API
- Calcul des scores
- Documentation : `brand_verification/README.md`

#### 2.2.2 BrandVerificationMultiprocessing
- Optimisation des performances
- Gestion parallèle
- Synchronisation des résultats
- Documentation : `brand_verification_multiprocessing/README.md`

#### 2.2.3 BrandAnalysis
- Analyse des relations
- Détection des marques manquantes
- Génération de rapports
- Documentation : `brand_analysis/README.md`

### 2.3 Utilisation des Tokens
- **Prompt par requête** : ~600 tokens
- **Réponse par requête** : ~300-400 tokens
- **Total par requête** : ~900-1000 tokens
- **Total pour 285 marques** : ~333,000-370,000 tokens
  - 200 vérifications simples
  - 85 vérifications doubles
  - 370 vérifications au total

### 2.4 Coûts d'Utilisation
- **GPT-4 Turbo** : 0.03$ par 1K tokens
  - Coût total : ~10-11$ pour 285 marques
- **GPT-3.5 Turbo** : 0.002$ par 1K tokens
  - Coût total : ~0.67-0.74$ pour 285 marques

### 2.5 Optimisations
- Système de cache pour éviter les vérifications en double
- Vérification hybride (GPT-3.5 pour les cas simples, GPT-4 pour les cas complexes)
- Optimisation des prompts pour réduire la taille

## 3. Instructions d'Installation et de Déploiement

### 3.1 Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)
- Clé API Perplexica

### 3.2 Installation
1. Cloner le dépôt :
```bash
git clone https://github.com/valleg12/Carrefour-Project.git
cd Carrefour-Project
```

2. Créer un environnement virtuel :
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer l'environnement :
```bash
# Créer le fichier .env
echo "PERPLEXICA_API_KEY=votre_clé_api" > .env
```

### 3.3 Déploiement

#### 3.3.1 Vérification Standard
```bash
python brand_verification/brand_verification.py
```

#### 3.3.2 Vérification avec Multiprocessing
```bash
python brand_verification_multiprocessing/brand_verification_multiprocessing.py
```

#### 3.3.3 Analyse des Marques
```bash
python brand_analysis/brand_analysis.py
```

### 3.4 Support Nécessaire

#### 3.4.1 Clés API
- Obtenir une clé API sur https://perplexica.ai
- Configurer la clé dans le fichier `.env`

#### 3.4.2 Ressources Système
- CPU : 2+ cœurs recommandés
- RAM : 4GB minimum
- Stockage : 1GB libre

#### 3.4.3 Dépendances
- pandas>=2.0.0
- requests>=2.31.0
- numpy>=1.24.0
- tqdm>=4.65.0
- python-dotenv>=1.0.0
- openpyxl>=3.1.0
- python-dateutil>=2.8.2
- pytz>=2023.3
- six>=1.16.0
- urllib3>=2.0.7
- certifi>=2023.7.22
- charset-normalizer>=3.2.0
- idna>=3.4

## 4. Maintenance

### 4.1 Mise à Jour
```bash
git pull origin main
pip install -r requirements.txt
```

### 4.2 Logs
- Emplacement : `logs/`
- Format : `verification_YYYY-MM-DD.log`

### 4.3 Cache
- Emplacement : `cache/`
- Format : JSON
- Durée de vie : 30 jours

## 5. Sécurité

### 5.1 Protection des Données
- Les clés API sont stockées dans `.env`
- Les données sensibles sont chiffrées
- Les logs ne contiennent pas d'informations sensibles

### 5.2 Bonnes Pratiques
- Ne jamais commiter `.env`
- Mettre à jour régulièrement les dépendances
- Vérifier les permissions des fichiers

## 6. Support

### 6.1 Documentation
- Documentation générale : `/docs`
- Documentation par module : `*/README.md`
- Issues GitHub : https://github.com/valleg12/Carrefour-Project/issues

### 6.2 Contact
- Email : [votre_email]
- GitHub : https://github.com/valleg12 