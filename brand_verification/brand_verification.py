import pandas as pd
import requests
import json
from typing import Dict, List, Tuple
import time
import re
import csv

class BrandVerification:
    def __init__(self):
        self.perplexica_url = "http://localhost:3000/api/search"

    def create_prompt(self, brand_name: str, company_name: str, row: dict) -> str:
        """
        Create a prompt for the API to verify brand ownership.
        The prompt is designed to get factual, verifiable information.
        """
        # Extraction du contexte
        product_category = row.get('Class Key - Description', '')
        sub_category = row.get('Group Class Key - Description', '')
        business_unit = row.get('Business Unit Description', '')
        
        # Conversion des Series pandas en string si nécessaire
        if isinstance(product_category, pd.Series):
            product_category = product_category.iloc[0] if not product_category.empty else ''
        if isinstance(sub_category, pd.Series):
            sub_category = sub_category.iloc[0] if not sub_category.empty else ''
        if isinstance(business_unit, pd.Series):
            business_unit = business_unit.iloc[0] if not business_unit.empty else ''
        
        context_info = []
        if product_category:
            context_info.append(f"Product category: {product_category}")
        if sub_category:
            context_info.append(f"Sub-category: {sub_category}")
        if business_unit:
            context_info.append(f"Business unit: {business_unit}")
        
        context_str = "\n".join(context_info)
        
        return f"""Please provide factual information about the brand '{brand_name}' and its relationship with '{company_name}'.
Context information:
{context_str}

Focus on verifiable facts and include specific details about:

1. Direct and indirect ownership:
- Is {brand_name} directly owned by {company_name}?
- If not, is it owned by a subsidiary or brand owned by {company_name}?
- What is the complete ownership chain (e.g., Brand → Subsidiary → {company_name})?
- When did each ownership relationship begin?
- If the brand is owned by another company, verify if that company is owned by {company_name}
- IMPORTANT: If the brand belongs to another brand that itself belongs to {company_name}, clearly state this in the explanation and set belongs_to to true
- VERY IMPORTANT: Specifically search for intermediate brands. For example, if {brand_name} belongs to brand X which belongs to {company_name}, this means {brand_name} indirectly belongs to {company_name} and belongs_to should be true

2. Recent changes:
- Have there been any recent ownership changes (last 2 years)?
- If the brand has been sold or transferred, when did this occur?
- What is the current status of the brand?
- If the brand is not owned by {company_name}, does {company_name} have distribution rights?
- In which geographical areas does {company_name} have distribution rights?
- What type of relationship exists (direct ownership, distribution agreement, license, etc.)?

3. Market presence:
- In which geographical areas is the brand active?
- What is the main product category of the brand?

4. Historical context:
- When was the brand acquired or created?
- Have there been any recent changes in ownership or distribution rights?

Please provide specific sources for your information, such as:
- Official company websites
- Trademark registries
- Annual reports
- Press releases
- Official announcements
- Recent press articles (last 2 years)

If you cannot find verifiable information about the relationship between {brand_name} and {company_name}, please state this clearly.

Format your response in JSON with the following fields:
{{
    "belongs_to": true/false,
    "explanation": "Explanation in French",
    "sources": ["list of sources"],
    "zones_geographiques": "List of geographical areas where the brand is active",
    "type_relation": "Type of relationship (direct ownership, distribution, license, etc.)",
    "details_relation": "Details about the relationship (dates, conditions, etc.)"
}}

IMPORTANT: All explanations must be in French."""

    def calculate_confidence_score(self, result, sources):
        """Calculate confidence score based on source quality and quantity."""
        # Vérification des sources
        official_sources = 0
        recent_sources = 0
        ownership_chain_verified = False
        
        # Vérifier les sources dans le contenu
        if isinstance(result, dict) and 'sources' in result:
            for source in result['sources']:
                if isinstance(source, str):
                    if any(domain in source.lower() for domain in [
                        '.com', '.org', '.gov', '.edu',
                        'annualreport', 'financial', 'press-release',
                        'investor', 'corporate', 'official',
                        'generalmills', 'sec.gov', 'businesswire',
                        'autoritedelaconcurrence', 'inpi.fr',
                        'marques.inpi.fr', 'data.inpi.fr',
                        'henkel.com', 'henkel.fr',
                        'marques.ic.gc.ca', 'tmdn.org',
                        'euipo.europa.eu', 'wipo.int'
                    ]):
                        official_sources += 1
                    if '2023' in source or '2024' in source or '2025' in source:
                        recent_sources += 1
        
        # Vérifier les sources de l'API
        for source in sources:
            if isinstance(source, dict):
                metadata = source.get('metadata', {})
                url = metadata.get('url', '').lower()
                title = metadata.get('title', '').lower()
                content = metadata.get('content', '').lower()
                
                # Vérification des sources officielles
                if any(domain in url for domain in [
                    '.com', '.org', '.gov', '.edu',
                    'annualreport', 'financial', 'press-release',
                    'investor', 'corporate', 'official',
                    'generalmills', 'sec.gov', 'businesswire',
                    'autoritedelaconcurrence', 'inpi.fr',
                    'marques.inpi.fr', 'data.inpi.fr',
                    'henkel.com', 'henkel.fr',
                    'marques.ic.gc.ca', 'tmdn.org',
                    'euipo.europa.eu', 'wipo.int'
                ]):
                    official_sources += 1
                
                # Vérification des sources récentes (moins de 2 ans)
                if '2023' in title or '2024' in title or '2025' in title:
                    recent_sources += 1
                
                # Vérification de la chaîne de propriété
                if 'subsidiary' in content or 'owned by' in content or 'acquisition' in content:
                    ownership_chain_verified = True
        
        # Règle 1: Source officielle directe = 100%
        if result.get('belongs_to', False) and official_sources > 0:
            return 100
        
        # Règle 2: Calcul du score pour les autres cas
        source_quantity = len(sources) + len(result.get('sources', []))
        source_quality = (official_sources / max(source_quantity, 1)) * 100
        recency_score = (recent_sources / max(source_quantity, 1)) * 100
        
        # Score de base selon la propriété
        base_score = 80 if result.get('belongs_to', False) else 20
        
        # Calcul du score final avec pondération
        final_score = (
            base_score * 0.4 +  # Score de base (40%)
            source_quality * 0.4 +  # Qualité des sources (40%)
            recency_score * 0.2  # Actualité des sources (20%)
        )
        
        # Bonus pour les informations très fiables
        if official_sources >= 2:
            final_score = min(100, final_score * 1.2)
        
        # Bonus pour la vérification de la chaîne de propriété
        if ownership_chain_verified:
            final_score = min(100, final_score * 1.15)
        
        # Malus pour les informations potentiellement obsolètes
        if recent_sources == 0 and 'sold' in result.get('explanation', '').lower():
            final_score = max(0, final_score * 0.7)
        
        print(f"\nDétail du calcul du score de confiance:")
        print(f"- Score de base: {base_score}%")
        print(f"- Qualité des sources: {source_quality}% ({official_sources}/{source_quantity} sources officielles)")
        print(f"- Actualité des sources: {recency_score}% ({recent_sources}/{source_quantity} sources récentes)")
        print(f"- Chaîne de propriété vérifiée: {'Oui' if ownership_chain_verified else 'Non'}")
        print(f"- Score final: {final_score}%")
        
        return min(100, max(0, final_score))

    def verify_brand(self, brand_name, company_name, row=None):
        """Vérifie si une marque appartient à une entreprise."""
        print(f"\nVerifying {brand_name} for {company_name}...")
        print("Sending request to Perplexica API for", brand_name, "...\n")
        
        # Convertir row en dict si c'est une Series pandas
        if isinstance(row, pd.Series):
            row = row.to_dict()
        
        max_attempts = 3
        attempt = 1
        while attempt <= max_attempts:
            print(f"Tentative {attempt}/{max_attempts}")
            try:
                payload = {
                    "chatModel": {
                        "provider": "openai",
                        "name": "gpt-4o-mini"
                    },
                    "embeddingModel": {
                        "provider": "openai",
                        "name": "text-embedding-3-large"
                    },
                    "optimizationMode": "speed",
                    "focusMode": "webSearch",
                    "query": self.create_prompt(brand_name, company_name, row or {}),
                    "history": [],
                    "systemInstructions": """Tu es un expert en vérification de propriété de marque. Ta tâche est de déterminer si une marque appartient à une entreprise spécifique.
Suis ces directives strictes:
1. Utilise UNIQUEMENT des sources officielles et fiables
2. N'utilise JAMAIS Wikipedia ou autre contenu collaboratif
3. Vérifie d'abord les sites web officiels des entreprises
4. Recherche les annonces d'acquisition
5. Vérifie via plusieurs sources fiables
6. Vérifie la propriété indirecte via les filiales ou sociétés mères
7. Réponds TOUJOURS en français
8. Inclus les zones géographiques et les détails de la relation
Retourne une réponse JSON avec les champs requis.""",
                    "stream": False
                }
                
                response = requests.post(
                    self.perplexica_url,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
                print("Perplexica API response:", result)
                
                if result and 'message' in result:
                    try:
                        # Extraire le JSON de la réponse
                        message = result['message']
                        json_start = message.find('{')
                        json_end = message.rfind('}') + 1
                        if json_start != -1 and json_end != -1:
                            json_str = message[json_start:json_end]
                            content = json.loads(json_str)
                            if isinstance(content, dict) and 'belongs_to' in content:
                                # Calculate confidence score
                                sources = result.get('sources', [])
                                # Ajouter les sources du contenu si elles existent
                                if 'sources' in content:
                                    sources.extend(content['sources'])
                                content['confidence'] = self.calculate_confidence_score(content, sources)
                                # Si la réponse est positive ou score > 0, on retourne
                                if content['confidence'] > 0 or content['belongs_to']:
                                    return content
                    except json.JSONDecodeError as e:
                        print(f"Erreur de parsing JSON: {str(e)}")
                
                print("Réponse invalide de l'API")
                attempt += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"Erreur lors de la vérification: {str(e)}")
                attempt += 1
                time.sleep(2)

        # Si tout échoue, retourner un résultat par défaut
        return {
            'belongs_to': False,
            'confidence': 0,
            'explanation': "Échec de la vérification - Pas de réponse de l'API",
            'sources': [],
            'type_relation': "Non déterminé",
            'zones_geographiques': "Non applicable",
            'details_relation': "Vérification impossible"
        }

    def process_all_brands(self, input_file, output_file):
        try:
            # Lire le fichier source en préservant toutes les colonnes
            df = pd.read_csv(input_file)
            total_brands = len(df)
            print(f"\n{'='*50}")
            print(f"Début de la vérification de {total_brands} marques")
            print(f"{'='*50}\n")
            
            # Dictionnaire pour stocker les résultats déjà vérifiés
            verified_brands = {}
            
            # Créer les nouvelles colonnes avec des valeurs par défaut
            new_columns = {
                'Propriété_Directe': False,
                'Score_Confiance': 0,
                'Type_Relation': 'Propriété directe',
                'Zones_Géographiques': '',
                'Détails_Relation': '',
                'Explication': '',
                'Sources': '',
                'À_Vérifier': True,
                'Statut_Vérification': 'Non vérifié',
                'Erreur_Vérification': ''
            }
            
            # Ajouter les nouvelles colonnes au DataFrame
            for col_name, default_value in new_columns.items():
                df[col_name] = default_value
            
            for index, row in df.iterrows():
                holding = row['Holding Name']
                brand = row['Brand Name']
                
                # Vérifier si la marque a déjà été traitée
                brand_key = f"{holding}_{brand}"
                if brand_key in verified_brands:
                    print(f"\n{'-'*50}")
                    print(f"Marque déjà vérifiée: {brand} pour {holding}")
                    print(f"Utilisation du résultat précédent")
                    print(f"{'-'*50}\n")
                    result = verified_brands[brand_key]
                    
                    # Mettre à jour les colonnes avec le résultat précédent
                    df.at[index, 'Propriété_Directe'] = result['Propriété_Directe']
                    df.at[index, 'Score_Confiance'] = result['Score_Confiance']
                    df.at[index, 'Type_Relation'] = result['Type_Relation']
                    df.at[index, 'Zones_Géographiques'] = result['Zones_Géographiques']
                    df.at[index, 'Détails_Relation'] = result['Détails_Relation']
                    df.at[index, 'Explication'] = result['Explication']
                    df.at[index, 'Sources'] = result['Sources']
                    df.at[index, 'À_Vérifier'] = result['À_Vérifier']
                    df.at[index, 'Statut_Vérification'] = result['Statut_Vérification']
                    df.at[index, 'Erreur_Vérification'] = result['Erreur_Vérification']
                    
                    # Sauvegarder après chaque mise à jour
                    df.to_csv(output_file, index=False)
                    continue
                
                print(f"\n{'-'*50}")
                print(f"Progression: {index + 1}/{total_brands}")
                print(f"Vérification de {brand} pour {holding}")
                print(f"{'-'*50}")
                
                try:
                    # Vérification de la marque
                    result = self.verify_brand(brand, holding, row)
                    
                    if result:
                        print(f"\nRésultat de la vérification:")
                        print(f"- Appartient à {holding}: {result['belongs_to']}")
                        print(f"- Confiance: {result['confidence']}%")
                        
                        # Format sources
                        sources = self.format_sources(result.get('sources', []))
                        
                        # Determine if manual verification is needed
                        needs_verification = self.should_verify_manually(result)
                        
                        # Mettre à jour les colonnes avec le résultat
                        df.at[index, 'Propriété_Directe'] = result['belongs_to']
                        df.at[index, 'Score_Confiance'] = result['confidence']
                        df.at[index, 'Type_Relation'] = result.get('type_relation', 'Propriété directe')
                        df.at[index, 'Zones_Géographiques'] = result.get('zones_geographiques', '')
                        df.at[index, 'Détails_Relation'] = result.get('details_relation', '')
                        df.at[index, 'Explication'] = result['explanation']
                        df.at[index, 'Sources'] = sources
                        df.at[index, 'À_Vérifier'] = needs_verification
                        df.at[index, 'Statut_Vérification'] = 'Succès'
                        df.at[index, 'Erreur_Vérification'] = ''
                        
                        # Stocker le résultat dans le dictionnaire des marques vérifiées
                        verified_brands[brand_key] = {
                            'Propriété_Directe': result['belongs_to'],
                            'Score_Confiance': result['confidence'],
                            'Type_Relation': result.get('type_relation', 'Propriété directe'),
                            'Zones_Géographiques': result.get('zones_geographiques', ''),
                            'Détails_Relation': result.get('details_relation', ''),
                            'Explication': result['explanation'],
                            'Sources': sources,
                            'À_Vérifier': needs_verification,
                            'Statut_Vérification': 'Succès',
                            'Erreur_Vérification': ''
                        }
                    else:
                        print("\nÉchec de la vérification")
                        # Mettre à jour les colonnes avec les valeurs par défaut
                        df.at[index, 'Statut_Vérification'] = 'Échec'
                        df.at[index, 'Erreur_Vérification'] = 'Échec de la vérification - Pas de réponse de l\'API'
                        
                        # Stocker le résultat dans le dictionnaire des marques vérifiées
                        verified_brands[brand_key] = {
                            'Propriété_Directe': False,
                            'Score_Confiance': 0,
                            'Type_Relation': 'Propriété directe',
                            'Zones_Géographiques': '',
                            'Détails_Relation': '',
                            'Explication': 'Échec de la vérification',
                            'Sources': '',
                            'À_Vérifier': True,
                            'Statut_Vérification': 'Échec',
                            'Erreur_Vérification': 'Échec de la vérification - Pas de réponse de l\'API'
                        }
                
                except Exception as e:
                    print(f"\nErreur lors de la vérification de {brand}: {str(e)}")
                    df.at[index, 'Statut_Vérification'] = 'Erreur'
                    df.at[index, 'Erreur_Vérification'] = str(e)
                    verified_brands[brand_key] = {
                        'Propriété_Directe': False,
                        'Score_Confiance': 0,
                        'Type_Relation': 'Propriété directe',
                        'Zones_Géographiques': '',
                        'Détails_Relation': '',
                        'Explication': f'Erreur: {str(e)}',
                        'Sources': '',
                        'À_Vérifier': True,
                        'Statut_Vérification': 'Erreur',
                        'Erreur_Vérification': str(e)
                    }
                
                print(f"\nRésultat enregistré pour {brand}")
                print(f"{'-'*50}\n")
                
                # Sauvegarder après chaque vérification
                df.to_csv(output_file, index=False)
            
            print(f"\n{'='*50}")
            print(f"Vérification terminée!")
            print(f"Résultats sauvegardés dans {output_file}")
            print(f"{'='*50}\n")
            
            # Afficher un résumé des résultats
            total_verifies = len(df)
            succes = len(df[df['Statut_Vérification'] == 'Succès'])
            echecs = len(df[df['Statut_Vérification'] == 'Échec'])
            erreurs = len(df[df['Statut_Vérification'] == 'Erreur'])
            
            print("\nRésumé des résultats:")
            print(f"Total des marques vérifiées: {total_verifies}")
            print(f"Vérifications réussies: {succes}")
            print(f"Échecs de vérification: {echecs}")
            print(f"Erreurs: {erreurs}")
            
        except Exception as e:
            print(f"\nErreur lors du traitement des marques: {e}")
            raise e

    def format_sources(self, sources):
        """Format sources into a readable string."""
        if not sources:
            return ""
            
        formatted_sources = []
        for source in sources:
            if isinstance(source, dict):
                metadata = source.get('metadata', {})
                title = metadata.get('title', 'No title')
                url = metadata.get('url', 'No URL')
                formatted_sources.append(f"{title} - {url}")
            elif isinstance(source, str):
                formatted_sources.append(source)
                
        return " | ".join(formatted_sources)

    def should_verify_manually(self, result):
        """Détermine si une vérification manuelle est nécessaire."""
        if not result:
            return True
        # Vérifier si la confiance est < 100%
        if result.get('confidence', 0) < 100:
            return True
        # Vérifier si l'explication contient des phrases négatives
        negative_phrases = [
            "no information indicating",
            "could not find",
            "no evidence",
            "not found",
            "pas d'information",
            "aucune preuve",
            "impossible de trouver",
            "no clear indication",
            "unable to confirm",
            "cannot verify",
            "no confirmation",
            "no documentation",
            "no official source",
            "no reliable source",
            "no definitive answer",
            "no conclusive evidence",
            "no direct evidence",
            "no explicit confirmation",
            "no clear ownership",
            "no clear relationship",
            "no clear connection",
            "no clear association",
            "no clear link",
            "no clear tie",
            "no clear bond",
            "no clear affiliation",
            "no clear partnership",
            "no clear alliance",
            "no clear agreement",
            "no clear contract",
            "no clear deal",
            "no clear arrangement",
            "no clear understanding"
        ]
        explanation = result.get('explanation', '').lower()
        return any(phrase in explanation for phrase in negative_phrases)

def main():
    verifier = BrandVerification()
    verifier.process_all_brands(
        "Carrefour Geniathon  - Tableau origine .csv",
        "brand_verification_results.csv"
    )

if __name__ == "__main__":
    main() 