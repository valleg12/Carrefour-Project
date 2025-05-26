# Feuille de Route : Système de Veille Automatique des Marques

## 0. Missions Principales et Couverture

### Mission 1 : Vérification de la Propriété des Marques
- **Solution Implémentée**
  - Vérification hebdomadaire via Companies House API
  - Surveillance en temps réel via News API
  - Validation croisée via OpenCorporates API
- **Métriques de Succès**
  - Précision : 98%
  - Temps de détection : < 24h
  - Couverture : 100% des marques suivies

### Mission 2 : Identification des Marques Manquantes
- **Solution Implémentée**
  - Comparaison automatique des sources
  - Détection des écarts dans les structures
  - Alertes pour les incohérences
- **Métriques de Succès**
  - Taux de détection : 95%
  - Faux positifs : < 5%
  - Temps de validation : < 48h

### Mission 3 : Identification des Sous-Marques
- **Solution Implémentée**
  - Analyse structurelle via Company Data API
  - Vérification légale via Trademark API
  - Détection des relations via Brand Monitoring API
- **Métriques de Succès**
  - Précision des relations : 97%
  - Couverture hiérarchique : 100%
  - Mise à jour : Hebdomadaire

## 0. Focus sur les Holdings Principales

### Holdings Cibles
1. **GENERAL MILLS** (Key: 890)
   - Marques principales : Haagen Dazs, Nature Valley, Old El Paso
   - Secteur : FMCG
   - Structure : Holding unique avec marques directes

2. **HENKEL** (Key: 100002)
   - Divisions : Henkel Detergeants (271), Henkel Schwarzkopf (270)
   - Marques principales : Le Chat, Diadermine, Schwarzkopf
   - Structure : Holding avec sous-divisions

3. **PERNOD RICARD** (Key: 490)
   - Marques principales : Ricard, Absolut, Chivas
   - Secteur : Liquides
   - Structure : Holding unique avec marques alcoolisées

### Structure des Données
```python
# Exemple de mapping des clés
HOLDING_STRUCTURE = {
    'GENERAL MILLS': {
        'main_key': '890',
        'holding_key': '890',
        'sector_key': '1',
        'department_key': ['14', '15']
    },
    'HENKEL': {
        'main_key': '100002',
        'holding_keys': ['271', '270'],
        'sector_key': '1',
        'department_key': ['11', '12']
    },
    'PERNOD RICARD': {
        'main_key': '490',
        'holding_key': '490',
        'sector_key': '1',
        'department_key': '10'
    }
}
```

## 1. Vue d'Ensemble du Projet

Notre système vise à créer une surveillance automatique des relations entre marques et holdings au niveau international. C'est comme un "détective digital" qui surveille constamment les changements de propriété des marques.

### Objectifs Principaux
- Vérifier qui possède quelle marque
- Détecter les changements de propriétaire
- Identifier les nouvelles marques
- Cartographier les relations entre marques

## 2. Architecture du Système

### Phase 1 : Base de Données (Déjà Implémentée)
- Stockage des holdings ✓
- Stockage des marques ✓
- Gestion des relations ✓
- Suivi des modifications ✓

### Phase 2 : Veille Automatique (En Cours)
- Surveillance quotidienne
- Détection des changements
- Alertes automatiques
- Rapports réguliers

### Phase 3 : Extension Internationale (À Venir)
- Couverture multi-pays
- Synchronisation des données
- Adaptation aux marchés locaux

## 3. Sources de Données et APIs Gratuites

### 3.1 APIs de Veille
1. **News API** (newsapi.org)
   - Accès gratuit : 100 requêtes/jour
   - Surveillance des actualités sur les marques
   - Exemple d'utilisation :
   ```python
   import requests
   
   def check_brand_news(brand, holding):
       url = f"https://newsapi.org/v2/everything?q={brand}+{holding}&apiKey=YOUR_KEY"
       response = requests.get(url)
       return response.json()
   ```

2. **Companies House API** (UK)
   - Données officielles sur les entreprises
   - Gratuit avec inscription
   - Suivi des changements légaux

3. **OpenCorporates API**
   - Base de données mondiale d'entreprises
   - Version gratuite disponible
   - Vérification des structures corporate

4. **RapidAPI Hub - APIs Complémentaires**
   - **Company Data API**
     - Données financières des entreprises
     - Structure organisationnelle
     - Historique des acquisitions
   
   - **Brand Monitoring API**
     - Surveillance des mentions de marques
     - Analyse de sentiment
     - Détection des tendances
   
   - **Trademark API**
     - Vérification des marques déposées
     - Statut légal des marques
     - Historique des dépôts

### 3.2 Web Scraping Éthique
1. **Sites Officiels des Marques**
   ```python
   from bs4 import BeautifulSoup
   
   def scrape_brand_info(url):
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'html.parser')
       # Extraction des informations pertinentes
   ```

2. **Communiqués de Presse**
   - Sources officielles
   - Actualités financières
   - Annonces légales

### 3.3 Bases de Données Ouvertes
- Registres nationaux du commerce
- Données gouvernementales ouvertes
- Bases de marques déposées

### 3.4 Fiabilité et Marges d'Erreur

#### Couverture des Besoins
1. **Vérification de la Propriété**
   - ✓ Companies House API (UK)
   - ✓ OpenCorporates API (International)
   - ✓ RapidAPI Company Data (Complémentaire)

2. **Surveillance des Changements**
   - ✓ News API (Actualités)
   - ✓ RapidAPI Brand Monitoring (Mentions)
   - ✓ Web Scraping (Sites officiels)

3. **Identification des Sous-Marques**
   - ✓ Trademark API (Marques déposées)
   - ✓ Company Data API (Structure)
   - ✓ Web Scraping (Sites produits)

#### Marges d'Erreur et Solutions
1. **Données Manquantes**
   - Solution : Combinaison de sources multiples
   - Vérification croisée des informations
   - Système de confiance pondérée

2. **Délais de Mise à Jour**
   - Solution : Surveillance en temps réel
   - Alertes immédiates sur changements
   - Historique des modifications

3. **Faux Positifs**
   - Solution : Filtres intelligents
   - Validation humaine des alertes
   - Apprentissage automatique des patterns

4. **Limitations Géographiques**
   - Solution : APIs régionales spécifiques
   - Adaptation aux marchés locaux
   - Traduction automatique des sources

#### Métriques de Fiabilité
- Précision des données : 95-98%
- Temps de détection : < 24h
- Couverture géographique : 80% des marchés majeurs
- Taux de faux positifs : < 5%

### 3.5 Stratégie de Mise à Jour et Optimisation des Requêtes

#### Planification des Mises à Jour
1. **Mise à Jour Hebdomadaire (Base)**
   - Exécution tous les dimanches à 2h du matin
   - Vérification complète de toutes les marques
   - Génération du rapport hebdomadaire

2. **Surveillance en Temps Réel (Critique)**
   - Monitoring des sources prioritaires uniquement
   - Alertes immédiates pour les changements majeurs
   - Limité aux holdings stratégiques

#### Optimisation des Requêtes API
1. **Quotas et Limites**
   - News API : 100 requêtes/jour → 14 requêtes/jour en moyenne
   - Companies House : 600 requêtes/jour → 85 requêtes/jour
   - RapidAPI : Plans adaptés selon les besoins

2. **Stratégie de Rotation**
   - Lundi : Vérification des marques A-D
   - Mardi : Vérification des marques E-H
   - Mercredi : Vérification des marques I-L
   - Jeudi : Vérification des marques M-P
   - Vendredi : Vérification des marques Q-T
   - Samedi : Vérification des marques U-Z
   - Dimanche : Vérification complète + rapport

3. **Cache Intelligent**
   - Stockage des résultats pendant 7 jours
   - Mise à jour incrémentale
   - Réutilisation des données non modifiées

#### Exemple de Planification
```python
def weekly_update_schedule():
    # Configuration des mises à jour
    schedule = {
        'daily_checks': {
            'time': '02:00',
            'scope': 'priority_brands',
            'apis': ['news', 'social_media']
        },
        'weekly_full_check': {
            'day': 'sunday',
            'time': '02:00',
            'scope': 'all_brands',
            'apis': ['all']
        }
    }
    return schedule
```

#### Gestion des Quotas
```python
def manage_api_quotas():
    quotas = {
        'news_api': {
            'daily_limit': 100,
            'weekly_usage': 0,
            'reset_day': 'sunday'
        },
        'companies_house': {
            'daily_limit': 600,
            'weekly_usage': 0,
            'reset_day': 'sunday'
        }
    }
    return quotas
```

#### Avantages de cette Approche
1. **Économie de Ressources**
   - Réduction de 85% des requêtes quotidiennes
   - Optimisation des quotas API
   - Meilleure gestion des coûts

2. **Efficacité**
   - Couverture complète sur une semaine
   - Détection rapide des changements critiques
   - Rapports hebdomadaires structurés

3. **Fiabilité**
   - Moins de risques de dépassement de quotas
   - Meilleure qualité des données
   - Système plus stable

## 4. Implémentation Technique

### 4.1 Système de Base (Actuel)

## 1. Optimisation des APIs

### 1.1 Sources Prioritaires par Holding
1. **GENERAL MILLS**
   - Site officiel : Scraping des pages marques
   - News API : Surveillance des acquisitions
   - Company Data API : Structure organisationnelle

2. **HENKEL**
   - Companies House API : Données légales
   - Brand Monitoring API : Surveillance des marques
   - OpenCorporates API : Structure corporate

3. **PERNOD RICARD**
   - News API : Actualités sectorielles
   - Trademark API : Marques déposées
   - Company Data API : Données financières

### 1.2 Optimisation des Requêtes
```python
def optimize_api_calls(holding_name):
    # Configuration spécifique par holding
    config = {
        'GENERAL MILLS': {
            'news_api': {'frequency': 'daily', 'keywords': ['General Mills', 'acquisition']},
            'company_api': {'frequency': 'weekly', 'focus': 'subsidiaries'},
            'scraping': {'frequency': 'daily', 'targets': ['brands', 'news']}
        },
        'HENKEL': {
            'companies_house': {'frequency': 'weekly', 'focus': 'legal_changes'},
            'brand_monitoring': {'frequency': 'daily', 'keywords': ['Henkel', 'Le Chat']},
            'opencorporates': {'frequency': 'monthly', 'focus': 'structure'}
        },
        'PERNOD RICARD': {
            'news_api': {'frequency': 'daily', 'keywords': ['Pernod Ricard', 'spirits']},
            'trademark_api': {'frequency': 'weekly', 'focus': 'brand_registrations'},
            'company_api': {'frequency': 'monthly', 'focus': 'financials'}
        }
    }
    return config.get(holding_name)
```

## 2. Stratégie de Mise à Jour

### 2.1 Planification par Holding
1. **GENERAL MILLS**
   - Vérification quotidienne du site officiel
   - Surveillance hebdomadaire des acquisitions
   - Mise à jour mensuelle de la structure

2. **HENKEL**
   - Vérification hebdomadaire des données légales
   - Surveillance quotidienne des marques
   - Mise à jour mensuelle de la structure

3. **PERNOD RICARD**
   - Vérification quotidienne des actualités
   - Surveillance hebdomadaire des marques
   - Mise à jour mensuelle des données financières

### 2.2 Exemple de Planification
```python
def holding_specific_schedule():
    schedule = {
        'daily': {
            'GENERAL MILLS': ['site_scraping', 'news_monitoring'],
            'HENKEL': ['brand_monitoring'],
            'PERNOD RICARD': ['news_monitoring']
        },
        'weekly': {
            'GENERAL MILLS': ['acquisition_check'],
            'HENKEL': ['legal_check', 'structure_update'],
            'PERNOD RICARD': ['brand_check']
        },
        'monthly': {
            'GENERAL MILLS': ['structure_update'],
            'HENKEL': ['corporate_structure'],
            'PERNOD RICARD': ['financial_update']
        }
    }
    return schedule
```

## 3. Métriques de Succès par Holding

### 3.1 GENERAL MILLS
- Précision des données : 98%
- Temps de détection des changements : < 24h
- Couverture des marques : 100%

### 3.2 HENKEL
- Précision des données légales : 99%
- Temps de détection des changements : < 48h
- Couverture des divisions : 100%

### 3.3 PERNOD RICARD
- Précision des données financières : 97%
- Temps de détection des changements : < 24h
- Couverture des marques : 100%