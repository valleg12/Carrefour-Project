# Proposition de Solution pour la Vérification de Marques

## Feuille de Route

1. **Phase 1 - Collecte de Données**
   - Intégration de sources de données officielles :
     * EDGAR Database (SEC) pour les entreprises cotées aux USA
     * Registre du commerce européen pour les entreprises européennes
     * API INSEE pour les entreprises françaises
   - Mise en place d'un système de stockage des données
   - Développement d'un scraper pour les sites officiels des entreprises
   - Intégration de Firecrawl pour le scraping automatisé

2. **Phase 2 - Développement MVP**
   - Création d'une interface simple pour la recherche de marques
   - Implémentation de l'algorithme de vérification de propriété
   - Tests et validation des résultats

3. **Phase 3 - Optimisation**
   - Amélioration de la précision des résultats
   - Optimisation des performances
   - Documentation et support

## Sources de Données

Nous utiliserons des sources de données officielles et gratuites :

1. **EDGAR Database (SEC)**
   - Données sur les entreprises cotées aux USA
   - Informations sur les filiales
   - Gratuit et officiel
   - Lien : https://www.sec.gov/edgar/searchedgar/companysearch.html

2. **Registre du commerce européen**
   - Données sur les entreprises européennes
   - Structure des groupes
   - Gratuit pour consultation
   - Lien : https://e-justice.europa.eu/content_business_registers_in_member_states-106-en.do

3. **API INSEE**
   - Données officielles sur les entreprises françaises
   - Gratuit avec clé API
   - Données à jour
   - Lien : https://api.insee.fr/

4. **Sites officiels des entreprises**
   - Vérification directe des informations
   - Données à jour
   - Complément aux sources officielles
   - Exemple : https://www.henkel.com/fr/company/our-company

5. **Firecrawl**
   - Solution de scraping automatisé
   - Configuration simple
   - Extraction structurée des données
   - Fonctionnalités clés :
     * Scraping de sites sans API
     * Extraction de données non structurées
     * Configuration visuelle des sélecteurs
     * Gestion des pages dynamiques
     * Export en JSON/CSV
   - Lien : https://firecrawl.dev/

**Autres options potentielles :**
- API Pappers (alternative à l'INSEE)
- API Infogreffe
- API Societe.com

**Option future (en suspens) : OpenCorporates**
- Plan Starter : 99€/mois
- 10,000 requêtes/mois
- Données structurées et complètes
- Lien : https://opencorporates.com/api_accounts/new

**Coût estimé pour le MVP :** 0€ (utilisation de sources gratuites)

Cette approche nous permettra d'avoir une couverture des grands groupes internationaux sans coût initial, en utilisant des sources de données officielles et gratuites, complétées par la vérification directe sur les sites des entreprises et le scraping automatisé. L'option OpenCorporates reste disponible pour une future amélioration si nécessaire. 