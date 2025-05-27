# Brand Verification System

Un système sophistiqué de vérification de propriété des marques utilisant l'IA pour analyser et valider les relations entre les marques et leurs propriétaires.

## Objectif

Ce projet vise à automatiser la vérification de la propriété des marques en utilisant l'IA pour analyser les sources officielles et déterminer avec précision les relations entre les marques et leurs propriétaires.

## Structure du Projet

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

## Modules

### 1. Brand Verification
Le module principal de vérification des marques, opérationnel et prêt à l'emploi.
- Vérification systématique des marques
- Calcul de score de confiance sophistiqué
- Gestion intelligente des sources
- Documentation complète dans `brand_verification/README.md`

### 2. Brand Verification Multiprocessing
Version optimisée pour le traitement parallèle (en développement).
- Optimisation pour les grands volumes
- Utilisation du multiprocessing Python
- Documentation dans `brand_verification_multiprocessing/README.md`

### 3. Brand Analysis
Outil d'analyse des marques et de leurs relations (en développement).
- Détection de marques manquantes
- Analyse des relations entre marques
- Documentation dans `brand_analysis/README.md`

## Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- Docker (recommandé pour Perplexica)
- Ollama (pour les modèles locaux)

### 2. Installation de Docker

#### macOS
1. Téléchargez Docker Desktop depuis [docker.com](https://www.docker.com/products/docker-desktop)
2. Installez l'application en la glissant dans le dossier Applications
3. Lancez Docker Desktop et attendez que l'icône dans la barre de menu indique que Docker est prêt

#### Windows
1. Téléchargez Docker Desktop depuis [docker.com](https://www.docker.com/products/docker-desktop)
2. Exécutez l'installateur et suivez les instructions
3. Redémarrez votre ordinateur si demandé
4. Lancez Docker Desktop depuis le menu Démarrer

#### Linux (Ubuntu)
```bash
# Mise à jour des paquets
sudo apt update
sudo apt upgrade

# Installation des prérequis
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Ajout de la clé GPG Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Ajout du dépôt Docker
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Installation de Docker
sudo apt update
sudo apt install docker-ce

# Vérification de l'installation
sudo docker run hello-world
```

### 3. Installation de Perplexica

Il y a deux façons d'installer Perplexica - Avec Docker (recommandé) ou Sans Docker.

#### Installation avec Docker (Recommandé)

1. Assurez-vous que Docker est installé et en cours d'exécution sur votre système.

2. Clonez le dépôt Perplexica :
```bash
git clone https://github.com/ItzCrazyKns/Perplexica.git
```

3. Naviguez vers le répertoire du projet et renommez `sample.config.toml` en `config.toml`.

4. Configurez le fichier `config.toml` :
   - OPENAI : Votre clé API OpenAI (si vous utilisez les modèles OpenAI)
   - OLLAMA : URL de l'API Ollama (http://host.docker.internal:11434 par défaut)
   - GROQ : Votre clé API Groq (si vous utilisez les modèles Groq)
   - ANTHROPIC : Votre clé API Anthropic (si vous utilisez les modèles Anthropic)

5. Lancez Perplexica avec Docker :
```bash
docker compose up -d
```

6. Accédez à Perplexica via http://localhost:3000

### 4. Installation du Projet

1. Clonez le dépôt :
```bash
git clone https://github.com/valleg12/Carrefour-Project.git
cd Carrefour-Project
```

2. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

## Utilisation

### Vérification Standard
```bash
python brand_verification/brand_verification.py
```

### Vérification avec Multiprocessing
```bash
python brand_verification_multiprocessing/brand_verification_multiprocessing.py
```

### Analyse des Marques
```bash
python brand_analysis/brand_analysis.py
```

## Documentation

La documentation est organisée en plusieurs niveaux :

1. **Documentation par Module**
   - Chaque module possède son propre README.md détaillé
   - Explications spécifiques et cas d'utilisation

2. **Documentation Générale** (dossier `docs/`)
   - `strategy.md` : Stratégie de code employée
   - `code_explanation.md` : Explication détaillée du code
   - `cost_analysis.md` : Analyse des coûts du système

## Fonctionnalités

- Vérification systématique des marques
- Calcul de score de confiance sophistiqué
- Gestion intelligente des sources
- Optimisation des performances
- Structure de données claire
- Système de vérification manuelle
- Gestion des relations complexes
- Interface utilisateur informative

## Contribution

Les contributions sont les bienvenues ! Veuillez :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 