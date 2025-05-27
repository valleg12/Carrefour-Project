# Guide d'Installation et de Déploiement

## Prérequis

### 1. Système d'Exploitation
- Linux (Ubuntu 20.04+)
- macOS (10.15+)
- Windows 10/11

### 2. Python
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 3. Clés API
- Clé API Perplexica (obtenir sur https://perplexica.ai)

## Installation

### 1. Cloner le Dépôt
```bash
git clone https://github.com/valleg12/Carrefour-Project.git
cd Carrefour-Project
```

### 2. Créer un Environnement Virtuel
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de l'Environnement
1. Créer un fichier `.env` à la racine du projet :
```bash
touch .env
```

2. Ajouter les variables d'environnement :
```env
PERPLEXICA_API_KEY=votre_clé_api
```

## Déploiement

### 1. Configuration du Système

#### 1.1 Vérification Standard
1. Placer le fichier CSV source dans le dossier racine
2. Vérifier le format du fichier :
   - Colonnes requises : `Marque`, `Société`
   - Format : CSV avec séparateur virgule
   - Encodage : UTF-8

#### 1.2 Vérification avec Multiprocessing
1. Configurer le nombre de processus :
   - Ouvrir `brand_verification_multiprocessing.py`
   - Ajuster `NUM_PROCESSES` selon votre CPU

#### 1.3 Analyse des Marques
1. Configurer les paramètres d'analyse :
   - Ouvrir `brand_analysis.py`
   - Ajuster les seuils de confiance

### 2. Exécution

#### 2.1 Vérification Standard
```bash
python brand_verification/brand_verification.py
```

#### 2.2 Vérification avec Multiprocessing
```bash
python brand_verification_multiprocessing/brand_verification_multiprocessing.py
```

#### 2.3 Analyse des Marques
```bash
python brand_analysis/brand_analysis.py
```

### 3. Résultats
- Les résultats sont sauvegardés dans `brand_verification_results.csv`
- Format des résultats :
  - Marque
  - Société
  - Score de confiance
  - Sources
  - Statut de vérification

## Maintenance

### 1. Mise à Jour
```bash
git pull origin main
pip install -r requirements.txt
```

### 2. Logs
- Les logs sont stockés dans `logs/`
- Format : `verification_YYYY-MM-DD.log`

### 3. Cache
- Le cache est stocké dans `cache/`
- Format : JSON
- Durée de vie : 30 jours

## Dépannage

### 1. Problèmes Courants

#### 1.1 Erreur de Clé API
```bash
# Vérifier le fichier .env
cat .env
# Vérifier la clé API sur Perplexica
```

#### 1.2 Erreur de Format CSV
```bash
# Vérifier le format du fichier
head -n 5 "Carrefour Geniathon - Tableau origine.csv"
```

#### 1.3 Erreur de Mémoire
- Réduire `NUM_PROCESSES`
- Augmenter la mémoire swap

### 2. Support
- Issues GitHub : https://github.com/valleg12/Carrefour-Project/issues
- Documentation : `/docs`
- Contact : [votre_email]

## Sécurité

### 1. Protection des Données
- Les clés API sont stockées dans `.env`
- Les données sensibles sont chiffrées
- Les logs ne contiennent pas d'informations sensibles

### 2. Bonnes Pratiques
- Ne jamais commiter `.env`
- Mettre à jour régulièrement les dépendances
- Vérifier les permissions des fichiers

## Performance

### 1. Optimisation
- Utiliser le multiprocessing pour les grands volumes
- Activer le cache pour les requêtes répétées
- Ajuster les timeouts selon votre connexion

### 2. Monitoring
- Surveiller l'utilisation CPU
- Vérifier l'espace disque
- Analyser les logs d'erreur 