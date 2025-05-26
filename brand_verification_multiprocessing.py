import pandas as pd
import requests
import json
from typing import Dict, List, Tuple
import time
import re
import multiprocessing
from multiprocessing import Pool, Manager
import os
from tqdm import tqdm

class BrandVerificationMulti:
    def __init__(self):
        self.perplexica_url = "http://localhost:3000/api/search"
        self.num_processes = multiprocessing.cpu_count()  # Nombre de processus = nombre de CPU

    def create_prompt(self, holding, brand):
        return f"""Analysez si la marque '{brand}' appartient à la société '{holding}' ou à l'une de ses filiales.
        Cette vérification est critique et nécessite une grande précision.
        
        RÈGLES DE VÉRIFICATION STRICTES :
        1. Vérification de la marque :
           - Recherchez la marque '{brand}' et ses variations courantes (majuscules/minuscules, accents)
           - Incluez les variations connues (ex: "Le Chat" = "LE CHAT")
           - Vérifiez aussi les noms commerciaux associés
        
        2. Critères d'évaluation :
           - Propriété directe : la marque est détenue par {holding} ou une de ses filiales
           - Licence exclusive : droits d'exploitation exclusifs accordés par {holding}
           - Licence partielle : droits d'exploitation non exclusifs
           - Droits d'exploitation régionaux : droits limités à certaines zones géographiques
        
        3. Niveau de confiance :
           - 100% : Documentation officielle incontestable (registres de marques, rapports annuels)
           - 80-99% : Sources officielles multiples concordantes
           - 60-79% : Source officielle unique fiable
           - <60% : Sources non officielles ou informations partielles
        
        Contexte d'analyse :
        - Marque à vérifier : '{brand}'
        - Société holding : {holding}
        
        Protocole de vérification :
        1. Consultation des registres officiels de marques
        2. Analyse des rapports annuels et documents financiers de {holding}
        3. Vérification des communiqués de presse et annonces d'acquisition
        4. Consultation des sites web officiels et portefeuilles de marques
        5. Analyse des documents de structure d'entreprise
        6. Vérification des sources d'autorité de la concurrence
        7. Consultation des bases de données de propriété intellectuelle
        
        Sources de référence prioritaires :
        - Registres officiels de marques et bases de données de propriété intellectuelle
        - Rapports annuels et états financiers des entreprises
        - Communiqués de presse officiels et annonces d'acquisition
        - Sites web corporatifs et portefeuilles de marques officiels
        - Documents de structure d'entreprise et organigrammes
        - Sources d'information commerciale accréditées
        - Autorités de la concurrence et organismes de régulation
        - Bases de données de brevets et marques déposées
        
        Sources à exclure :
        - Contenu généré par les utilisateurs (Wikipedia, forums, etc.)
        - Blogs et sites non officiels
        - Réseaux sociaux et contenus non vérifiés
        - Articles de presse sans sources officielles
        
        En cas d'absence d'information :
        - belongs_to: false
        - confidence: 0
        - explanation: "Aucune information vérifiable trouvée concernant la marque '{brand}'"
        - type_relation: "Aucune relation documentée"
        
        Format de réponse attendu (JSON) :
        {{
            "belongs_to": boolean,
            "confidence": number (0-100),
            "explanation": string (en français),
            "sources": array de sources fiables utilisées,
            "type_relation": string ("Propriété directe", "Licence exclusive", "Licence partielle", "Droits d'exploitation régionaux", "Aucune relation"),
            "zones_geographiques": string (zones concernées),
            "date_changement": string (date du dernier changement de propriété/licence),
            "details_relation": string (détails sur la nature de la relation)
        }}"""

    def calculate_confidence_score(self, result, sources):
        """Calculate confidence score based on source quality and quantity."""
        base_score = result.get('confidence', 0)
        
        # Facteurs de pondération
        source_quality = 0
        source_quantity = len(sources)
        official_sources = 0
        recent_sources = 0
        
        for source in sources:
            if isinstance(source, dict):
                metadata = source.get('metadata', {})
                url = metadata.get('url', '').lower()
                title = metadata.get('title', '').lower()
                
                # Vérification des sources officielles
                if any(domain in url for domain in [
                    '.com', '.org', '.gov', '.edu',
                    'annualreport', 'financial', 'press-release',
                    'investor', 'corporate', 'official',
                    'generalmills', 'sec.gov', 'businesswire',
                    'autoritedelaconcurrence', 'inpi.fr',  # Ajout des sources françaises
                    'marques.inpi.fr', 'data.inpi.fr',
                    'henkel.com', 'henkel.fr',
                    'marques.ic.gc.ca', 'tmdn.org',
                    'euipo.europa.eu', 'wipo.int'
                ]):
                    official_sources += 1
                
                # Vérification des sources récentes (moins de 2 ans)
                if '2023' in title or '2024' in title or '2025' in title:
                    recent_sources += 1
        
        # Calcul des scores
        source_quality = (official_sources / max(source_quantity, 1)) * 100
        recency_score = (recent_sources / max(source_quantity, 1)) * 100
        
        # Nouvelle pondération plus favorable
        final_score = (
            base_score * 0.5 +  # Score de base (50%)
            source_quality * 0.3 +  # Qualité des sources (30%)
            recency_score * 0.2  # Actualité des sources (20%)
        )
        
        # Bonus pour les informations très fiables
        if official_sources >= 2 and source_quality >= 80:
            final_score = min(100, final_score * 1.2)  # +20% de bonus
        
        # Bonus pour les informations historiques bien établies
        if 'acquisition' in result.get('explanation', '').lower() and official_sources >= 2:
            final_score = min(100, final_score * 1.1)  # +10% de bonus
            
        # Bonus pour les informations confirmées par plusieurs sources officielles
        if official_sources >= 3:
            final_score = min(100, final_score * 1.15)  # +15% de bonus
        
        return min(100, max(0, final_score))  # S'assurer que le score est entre 0 et 100

    def verify_with_perplexica(self, holding, brand):
        print(f"\nVerifying {brand} for {holding}...")
        print(f"Sending request to Perplexica API for {brand}...")
        
        payload = {
            "chatModel": {
                "provider": "openai",
                "name": "gpt-4o-mini"
            },
            "embeddingModel": {
                "provider": "openai",
                "name": "text-embedding-3-large"
            },
            "optimizationMode": "accuracy",
            "focusMode": "webSearch",
            "query": self.create_prompt(holding, brand),
            "history": [],
            "systemInstructions": """You are a brand ownership verification expert. Your task is to determine if a brand belongs to a specific company.
            Follow these strict guidelines:
            1. Vérification de la marque :
               - Vérifiez la marque exacte fournie et ses variations courantes
               - Incluez les variations connues (ex: "Le Chat" = "LE CHAT")
               - Vérifiez aussi les noms commerciaux associés
               - Recherchez dans les bases de données de marques déposées
            
            2. Sources de référence :
               - Utilisez UNIQUEMENT des sources officielles et vérifiables
               - Priorisez les registres de marques et documents légaux
               - Consultez les rapports annuels et documents financiers
               - Vérifiez les communiqués de presse officiels
               - Consultez les autorités de la concurrence
               - Vérifiez les sites officiels des entreprises
            
            3. Critères d'évaluation :
               - Propriété directe : marque détenue par la société ou ses filiales
               - Licence exclusive : droits d'exploitation exclusifs
               - Licence partielle : droits d'exploitation non exclusifs
               - Droits régionaux : droits limités à certaines zones
            
            4. Niveau de confiance :
               - 100% : Documentation officielle incontestable
               - 80-99% : Sources officielles multiples concordantes
               - 60-79% : Source officielle unique fiable
               - <60% : Sources non officielles ou informations partielles
            
            5. Sources à exclure :
               - Wikipedia et contenus générés par les utilisateurs
               - Blogs et sites non officiels
               - Réseaux sociaux et contenus non vérifiés
               - Articles sans sources officielles
            
            6. En cas d'absence d'information :
               - Faites une recherche approfondie avant de conclure
               - Vérifiez les sources officielles de l'entreprise
               - Consultez les bases de données de marques
               - Vérifiez les sites web corporatifs
               - Consultez les rapports annuels
               - Ne concluez à l'absence d'information qu'après une recherche exhaustive
            
            Return a JSON response with:
            - belongs_to: boolean
            - confidence: number (0-100)
            - explanation: string
            - sources: array of reliable sources used
            - type_relation: string
            - zones_geographiques: string
            - date_changement: string
            - details_relation: string""",
            "stream": False
        }
        
        max_retries = 5  # Augmenté de 3 à 5
        retry_delay = 15  # Augmenté de 10 à 15 secondes
        search_timeout = 120  # Augmenté de 60 à 120 secondes
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.perplexica_url,
                    json=payload,
                    timeout=search_timeout
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Parse the message content which contains the JSON response
                message_content = result.get('message', '{}')
                if isinstance(message_content, str):
                    # Remove any markdown code block indicators and clean the string
                    message_content = message_content.replace('```json', '').replace('```', '').strip()
                    
                    # Try to find JSON content within the string
                    try:
                        # First try direct JSON parsing
                        content = json.loads(message_content)
                    except json.JSONDecodeError:
                        # If that fails, try to extract JSON from the string
                        try:
                            # Look for JSON-like structure
                            json_start = message_content.find('{')
                            json_end = message_content.rfind('}') + 1
                            if json_start >= 0 and json_end > json_start:
                                json_str = message_content[json_start:json_end]
                                content = json.loads(json_str)
                            else:
                                raise json.JSONDecodeError("No JSON structure found", message_content, 0)
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON response: {e}")
                            if attempt < max_retries - 1:
                                print(f"Retrying in {retry_delay} seconds...")
                                time.sleep(retry_delay)
                                continue
                            return None
                else:
                    content = message_content
                
                # Validate required fields
                required_fields = ['belongs_to', 'explanation', 'confidence']
                if not all(field in content for field in required_fields):
                    print(f"Missing required fields in response: {content}")
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    return None
                
                # Calculate confidence score
                sources = result.get('sources', [])
                content['confidence'] = self.calculate_confidence_score(content, sources)
                
                return content
                
            except requests.exceptions.RequestException as e:
                print(f"Error making request to Perplexica API: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    return None
            except Exception as e:
                print(f"Unexpected error: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    return None

    def calculate_final_confidence(self, first_result, second_result):
        """Calculate final confidence using weighted average (40/60) between two verifications."""
        if not first_result or not second_result:
            return first_result or second_result
            
        # If both results agree on ownership
        if first_result['belongs_to'] == second_result['belongs_to']:
            # Calculate weighted average confidence (40/60)
            first_score = first_result['confidence']
            second_score = second_result['confidence']
            
            # Calcul de la moyenne pondérée 40/60
            final_confidence = (first_score * 0.4) + (second_score * 0.6)
            
            # Vérification de la cohérence des informations supplémentaires
            type_relation_match = first_result.get('type_relation') == second_result.get('type_relation')
            zones_match = first_result.get('zones_geographiques') == second_result.get('zones_geographiques')
            date_match = first_result.get('date_changement') == second_result.get('date_changement')
            
            # Ajustement du score en fonction de la cohérence des informations
            if not type_relation_match:
                final_confidence *= 0.9
            if not zones_match:
                final_confidence *= 0.9
            if not date_match:
                final_confidence *= 0.9
            
            # Combine explanations in a more concise way
            combined_explanation = f"{first_result['explanation']} {second_result['explanation']}"
            
            return {
                'belongs_to': first_result['belongs_to'],
                'confidence': final_confidence,
                'explanation': combined_explanation,
                'sources': first_result.get('sources', []) + second_result.get('sources', []),
                'type_relation': first_result.get('type_relation', 'Propriété directe'),
                'zones_geographiques': first_result.get('zones_geographiques', ''),
                'date_changement': first_result.get('date_changement', ''),
                'details_relation': first_result.get('details_relation', '')
            }
        else:
            # If results disagree, take the higher confidence result
            if first_result['confidence'] >= second_result['confidence']:
                return first_result
            return second_result

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

    def process_brand(self, args):
        """Process a single brand verification."""
        holding, brand, index, total = args
        print(f"\n{'-'*50}")
        print(f"Progression: {index + 1}/{total}")
        print(f"Vérification de {brand} pour {holding}")
        print(f"{'-'*50}")
        
        # First verification
        print("\n1ère vérification en cours...")
        first_result = self.verify_with_perplexica(holding, brand)
        
        if first_result:
            print(f"\nRésultat 1ère vérification:")
            print(f"- Appartient à {holding}: {first_result['belongs_to']}")
            print(f"- Confiance: {first_result['confidence']}%")
            
            # Si score < 70%, on fait une deuxième vérification
            if first_result['confidence'] < 70:
                print(f"\nConfiance < 70%, lancement 2ème vérification...")
                second_result = self.verify_with_perplexica(holding, brand)
                final_result = self.calculate_final_confidence(first_result, second_result)
                print(f"\nRésultat final après 2ème vérification:")
                print(f"- Appartient à {holding}: {final_result['belongs_to']}")
                print(f"- Confiance finale: {final_result['confidence']:.1f}%")
            else:
                # Si score ≥ 70%, on garde le premier résultat
                final_result = first_result
                print("\nConfiance ≥ 70%, pas de 2ème vérification nécessaire")
                print(f"- Confiance finale: {final_result['confidence']:.1f}%")
            
            # Determine if manual verification is needed
            needs_verification = self.should_verify_manually(final_result)
            
            return {
                'Propriété_Directe': final_result['belongs_to'],
                'Score_Confiance': final_result['confidence'],
                'Type_Relation': final_result.get('type_relation', 'Propriété directe'),
                'Zones_Géographiques': final_result.get('zones_geographiques', ''),
                'Date_Changement': final_result.get('date_changement', ''),
                'Détails_Relation': final_result.get('details_relation', ''),
                'Explication': final_result['explanation'],
                'Sources': final_result.get('sources', []),
                'À_Vérifier': needs_verification
            }
        else:
            print("\nÉchec de la vérification")
            return {
                'Propriété_Directe': False,
                'Score_Confiance': 0,
                'Type_Relation': 'Propriété directe',
                'Zones_Géographiques': '',
                'Date_Changement': '',
                'Détails_Relation': '',
                'Explication': 'Échec de la vérification',
                'Sources': [],
                'À_Vérifier': True
            }

    def process_all_brands(self, input_file, output_file):
        try:
            # Lire le fichier source en préservant l'ordre
            df = pd.read_csv(input_file)
            total_brands = len(df)
            print(f"\n{'='*50}")
            print(f"Début de la vérification de {total_brands} marques")
            print(f"{'='*50}\n")
            
            # Créer les nouvelles colonnes avec des valeurs par défaut
            new_columns = {
                'Propriété_Directe': False,
                'Score_Confiance': 0,
                'Type_Relation': 'Propriété directe',
                'Zones_Géographiques': '',
                'Date_Changement': '',
                'Détails_Relation': '',
                'Explication': '',
                'Sources': [],
                'À_Vérifier': True
            }
            
            # Ajouter les nouvelles colonnes à la fin du DataFrame
            for col, default_value in new_columns.items():
                df[col] = default_value
            
            # Préparer les arguments pour le multiprocessing
            args_list = [(row['Holding Name'], row['Brand Name'], i, total_brands) 
                        for i, row in df.iterrows()]
            
            # Créer un pool de processus
            with Pool(processes=self.num_processes) as pool:
                # Utiliser tqdm pour afficher la progression
                results = list(tqdm(
                    pool.imap(self.process_brand, args_list),
                    total=len(args_list),
                    desc="Vérification des marques"
                ))
            
            # Mettre à jour le DataFrame avec les résultats
            for i, result in enumerate(results):
                for col in result:
                    df.at[i, col] = result[col]
            
            # Sauvegarder les résultats
            df.to_csv(output_file, index=False)
            
            print(f"\n{'='*50}")
            print(f"Vérification terminée!")
            print(f"Résultats sauvegardés dans {output_file}")
            print(f"{'='*50}\n")
            
        except Exception as e:
            print(f"\nErreur lors du traitement des marques: {e}")
            raise e

def main():
    verifier = BrandVerificationMulti()
    output_file = "brand_verification_multiprocessing.csv"
    
    try:
        verifier.process_all_brands(
            "Carrefour Geniathon  - Tableau origine .csv",
            output_file
        )
        
        # Vérifier que le fichier a été créé
        if os.path.exists(output_file):
            print(f"\nLe fichier {output_file} a été créé avec succès!")
            # Afficher les premières lignes du fichier
            df = pd.read_csv(output_file)
            print("\nAperçu des résultats:")
            print(df.head())
        else:
            print(f"\nErreur: Le fichier {output_file} n'a pas été créé.")
            
    except Exception as e:
        print(f"\nUne erreur est survenue: {e}")

if __name__ == "__main__":
    main() 