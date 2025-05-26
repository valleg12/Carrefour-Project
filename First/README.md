# Système de Monitoring Automatique des Marques et Holdings

Ce projet vise à créer un système automatisé de monitoring des marques et holdings en France, avec les fonctionnalités suivantes :

## Fonctionnalités Principales

1. **Vérification de la Propriété des Marques**
   - Vérification automatique de la propriété des marques
   - Détection des changements de propriété
   - Historique des modifications

2. **Détection des Marques Manquantes**
   - Identification des marques non répertoriées
   - Alertes pour les nouvelles marques détectées
   - Intégration avec les bases de données existantes

3. **Hiérarchie des Marques**
   - Cartographie des relations entre marques
   - Visualisation de la structure des holdings
   - Mise à jour automatique des relations

## Structure du Projet

```
.
├── src/
│   ├── data/
│   │   ├── collectors/      # Collecteurs de données
│   │   ├── processors/      # Processeurs de données
│   │   └── validators/      # Validateurs de données
│   ├── models/             # Modèles de données
│   ├── services/           # Services métier
│   └── utils/              # Utilitaires
├── tests/                  # Tests unitaires et d'intégration
├── config/                 # Configuration
└── scripts/               # Scripts utilitaires
```

## Installation

1. Cloner le repository
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - Unix/MacOS : `source venv/bin/activate`
4. Installer les dépendances : `pip install -r requirements.txt`

## Configuration

1. Copier `.env.example` vers `.env`
2. Configurer les variables d'environnement dans `.env`

## Utilisation

```bash
# Lancer le système de monitoring
python src/main.py

# Lancer les tests
python -m pytest tests/
```

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. 