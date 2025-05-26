# Explication du Code

## 1. Classe BrandVerification

```python
class BrandVerification:
    def __init__(self):
        self.perplexica_url = "http://localhost:3000/api/search"
```

Cette classe est le cœur du programme. Elle se connecte à l'API Perplexica pour la vérification des marques. Elle gère :
- La connexion à l'API
- La gestion des erreurs
- Le traitement des réponses
- Le calcul des scores de confiance

## 2. Création du Prompt (create_prompt)

```python
def create_prompt(self, brand_name: str, company_name: str, row: dict) -> str:
```

Cette fonction crée une demande détaillée pour l'API en :
- Intégrant le contexte (catégorie produit, sous-catégorie, unité business)
- Structurant la demande pour obtenir :
  - Vérification de propriété directe et indirecte
  - Changements récents
  - Présence sur le marché
  - Contexte historique
- Formatant la réponse attendue en JSON avec :
  - belongs_to (booléen)
  - explanation (en français)
  - sources (liste)
  - zones_geographiques
  - type_relation
  - details_relation

## 3. Calcul du Score de Confiance (calculate_confidence_score)

```python
def calculate_confidence_score(self, result, sources):
```

Cette fonction calcule un score de confiance sophistiqué en :
- Vérifiant les sources officielles et récentes
- Appliquant une pondération :
  - Score de base (50%)
  - Qualité des sources (30%)
  - Actualité des sources (20%)
- Appliquant des bonus :
  - +20% pour 2+ sources officielles et qualité ≥ 80%
  - +10% pour acquisitions historiques
  - +15% pour 3+ sources officielles
- Appliquant des malus :
  - 30% pour informations potentiellement obsolètes

## 4. Vérification de Marque (verify_brand)

```python
def verify_brand(self, brand_name, company_name, row=None):
```

Cette fonction gère la vérification complète d'une marque en :
- Faisant jusqu'à 3 tentatives de vérification
- Gérant les erreurs et timeouts
- Calculant le score de confiance
- Retournant un résultat structuré
- Gérant les cas d'échec avec un résultat par défaut

## 5. Traitement de Toutes les Marques (process_all_brands)

```python
def process_all_brands(self, input_file, output_file):
```

Cette fonction principale :
- Lit le fichier CSV d'entrée
- Crée les nouvelles colonnes nécessaires
- Pour chaque marque :
  - Vérifie si déjà traitée (cache)
  - Effectue la vérification
  - Enregistre les résultats
- Sauvegarde progressivement les résultats
- Génère un résumé des résultats

## 6. Formatage des Sources (format_sources)

```python
def format_sources(self, sources):
```

Cette fonction transforme les sources en format lisible en :
- Gérant les sources sous forme de dictionnaire
- Extrayant les métadonnées (titre, URL)
- Formatant les sources sous forme de texte
- Gérant les cas de sources vides

## 7. Vérification Manuelle (should_verify_manually)

```python
def should_verify_manually(self, result):
```

Cette fonction détermine si une vérification manuelle est nécessaire en :
- Vérifiant le score de confiance (< 100%)
- Analysant l'explication pour des phrases négatives
- Utilisant une liste étendue de phrases négatives (34 phrases)
- Retournant True si une vérification manuelle est recommandée

## Processus de Vérification

Le processus de vérification suit ces étapes :

1. **Préparation**
   - Lecture du fichier CSV
   - Création des colonnes nécessaires
   - Initialisation du cache

2. **Vérification**
   - Vérification de la marque
   - Calcul du score de confiance
   - Détection des cas à vérifier manuellement

3. **Validation**
   - Vérification des résultats
   - Formatage des sources
   - Calcul du score final

4. **Enregistrement**
   - Sauvegarde progressive des résultats
   - Génération du résumé
   - Gestion des erreurs

## Structure des Résultats

Les résultats sont sauvegardés avec :
- Propriété_Directe
- Score_Confiance
- Type_Relation
- Zones_Géographiques
- Détails_Relation
- Explication
- Sources
- À_Vérifier
- Statut_Vérification
- Erreur_Vérification 