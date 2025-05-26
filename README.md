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

1. Cloner le dépôt :
```bash
git clone https://github.com/valleg12/Carrefour-Project.git
cd Carrefour-Project
```

2. Installer les dépendances :
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