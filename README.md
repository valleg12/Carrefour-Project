# Brand Verification System

Un système sophistiqué de vérification de propriété des marques utilisant l'IA pour analyser et valider les relations entre les marques et leurs propriétaires.

## Objectif

Ce projet vise à automatiser la vérification de la propriété des marques en utilisant l'IA pour analyser les sources officielles et déterminer avec précision les relations entre les marques et leurs propriétaires.

## Structure du Projet

- `brand_verification.py` : Script principal de vérification des marques
- `brand_verification_multiprocessing.py` : Version optimisée pour le traitement parallèle
- `brand_analysis.py` : Outil d'analyse des marques et de leurs relations
- `Carrefour Geniathon - Tableau origine.csv` : Fichier source des données
- `docs/` : Documentation détaillée du projet
  - `strategy.md` : Stratégie de code employée
  - `code_explanation.md` : Explication détaillée du code
  - `cost_analysis.md` : Analyse des coûts du système

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-username/brand-verification.git
cd brand-verification
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Vérification standard :
```bash
python brand_verification.py
```

2. Vérification avec multiprocessing (pour les grands volumes) :
```bash
python brand_verification_multiprocessing.py
```

3. Analyse des marques :
```bash
python brand_analysis.py
```

## Fonctionnalités

- Vérification systématique des marques
- Calcul de score de confiance sophistiqué
- Gestion intelligente des sources
- Optimisation des performances
- Structure de données claire
- Système de vérification manuelle
- Gestion des relations complexes
- Interface utilisateur informative

## Documentation

La documentation détaillée est disponible dans le dossier `docs/` :
- `strategy.md` : Stratégie de code employée
- `code_explanation.md` : Explication détaillée du code
- `cost_analysis.md` : Analyse des coûts du système

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 