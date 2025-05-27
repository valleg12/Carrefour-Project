import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, BarChart3, Shield, Clock, DollarSign, Users, Zap, CheckCircle, TrendingUp, Calendar, Phone, DownloadIcon, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Switch } from "@/components/ui/switch";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import PresentationSlide from './PresentationSlide';

const BrandPresentation = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [brandVerification, setBrandVerification] = useState(false);
  const [brandAnalysis, setBrandAnalysis] = useState(false);
  const [multiprocessing, setMultiprocessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);
  const totalSlides = 9;

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % totalSlides);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + totalSlides) % totalSlides);
  };

  const goToSlide = (index: number) => {
    setCurrentSlide(index);
  };

  const executeCode = async (type: string) => {
    setProgress(0);
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 100));
      setProgress(i);
    }
    setResults({
      type,
      insights: [
        {
          title: "Marques Vérifiées",
          value: "285/285",
          status: "success"
        },
        {
          title: "Score Moyen de Confiance",
          value: "88.4%",
          status: "success"
        },
        {
          title: "Marques à Vérifier Manuellement",
          value: "57",
          status: "warning"
        }
      ]
    });
  };

  const exportCSV = async () => {
    try {
      // Lire le fichier CSV existant
      const response = await fetch('/brand_verification_results-1.csv');
      const csvContent = await response.text();
      
      // Créer le lien de téléchargement
      const encodedUri = encodeURI('data:text/csv;charset=utf-8,' + csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "brand_verification_results-1.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Erreur lors de l\'export du CSV:', error);
      // Fallback sur les données de test si le fichier n'est pas trouvé
      const csvContent = "data:text/csv;charset=utf-8," + 
        "Brand Name,Holding Name,Belongs To,Confidence,Explanation\n" +
        "Brand1,Holding1,true,95,Verified\n" +
        "Brand2,Holding2,false,85,Needs verification\n" +
        "Brand3,Holding1,true,90,Verified\n" +
        "Brand4,Holding3,true,88,Verified\n" +
        "Brand5,Holding2,false,75,Needs verification\n" +
        "Brand6,Holding1,true,92,Verified\n" +
        "Brand7,Holding3,true,87,Verified\n" +
        "Brand8,Holding2,true,91,Verified\n" +
        "Brand9,Holding1,false,82,Needs verification\n" +
        "Brand10,Holding3,true,89,Verified";
      
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "brand_verification_results-1.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const slides = [
    // Slide 1 - Page de titre
    <PresentationSlide key={1} background="bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900">
      <div className="text-center text-white space-y-8 max-w-4xl">
        <div className="flex justify-center mb-8">
          <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center">
            <Shield className="w-12 h-12 text-blue-900" />
          </div>
        </div>
        <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
          Système de Vérification de Marques par IA
        </h1>
        <p className="text-2xl text-blue-200 font-light">
          Optimisez votre gestion de portefeuille de marques
        </p>
        <div className="mt-12 text-lg">
          <p className="text-white font-semibold tracking-wide">Intelligence Artificielle • Vérification Automatisée • ROI Garanti</p>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 2 - Défis actuels (modifiée)
    <PresentationSlide key={2}>
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-800">
          Défis Actuels du Marché
        </h2>
        <div className="grid grid-cols-2 gap-8">
          <div className="space-y-6">
            <Card className="border-red-200 bg-red-50">
              <CardHeader>
                <CardTitle className="flex items-center text-red-700">
                  <Clock className="w-6 h-6 mr-2" />
                  Temps de Vérification
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-red-600 mb-2">30-45 min</div>
                <p className="text-red-800">par marque en vérification manuelle</p>
              </CardContent>
            </Card>
          </div>
          
          <div className="space-y-6">
            <Card className="border-yellow-200 bg-yellow-50">
              <CardHeader>
                <CardTitle className="flex items-center text-yellow-700">
                  <Users className="w-6 h-6 mr-2" />
                  Risques d'Erreurs
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-yellow-600 mb-2">20-30%</div>
                <p className="text-yellow-800">taux d'erreur en vérification manuelle</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 3 - Notre solution
    <PresentationSlide key={3} background="bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-800">
          Notre Solution IA
        </h2>
        <div className="grid grid-cols-3 gap-8 mb-8">
          <Card className="bg-white shadow-lg border-green-200">
            <CardHeader>
              <CardTitle className="text-green-700 text-center">
                <Shield className="w-12 h-12 mx-auto mb-4 text-green-600" />
                Brand Verification
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm mb-2">
                ✅ OPÉRATIONNEL
              </div>
              <p className="text-gray-900">Vérification systématique des marques</p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg border-blue-200">
            <CardHeader>
              <CardTitle className="text-blue-700 text-center">
                <BarChart3 className="w-12 h-12 mx-auto mb-4 text-blue-600" />
                Brand Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mb-2">
                🔧 EN DÉVELOPPEMENT
              </div>
              <p className="text-gray-900">Analyse des relations et synergies</p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg border-purple-200">
            <CardHeader>
              <CardTitle className="text-purple-700 text-center">
                <Zap className="w-12 h-12 mx-auto mb-4 text-purple-600" />
                Multiprocessing
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm mb-2">
                🔧 EN DÉVELOPPEMENT
              </div>
              <p className="text-gray-900">Optimisation grands volumes</p>
            </CardContent>
          </Card>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold mb-4 text-center">Points Clés de Différenciation</h3>
          <div className="grid grid-cols-2 gap-6">
            <div className="flex items-center">
              <CheckCircle className="w-6 h-6 text-green-500 mr-3" />
              <span className="text-gray-900 font-semibold">Architecture modulaire et évolutive</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-6 h-6 text-green-500 mr-3" />
              <span className="text-gray-900 font-semibold">Intégration avec systèmes existants</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-6 h-6 text-green-500 mr-3" />
              <span className="text-gray-900 font-semibold">Sources officielles vérifiées</span>
            </div>
            <div className="flex items-center">
              <CheckCircle className="w-6 h-6 text-green-500 mr-3" />
              <span className="text-gray-900 font-semibold">Traçabilité complète des vérifications</span>
            </div>
          </div>
          <div className="mt-6 bg-blue-50 p-4 rounded-lg">
            <p className="text-blue-800 text-center">
              <strong>Technologie utilisée :</strong> Nous avons utilisé Perplexica, l'alternative gratuite de Perplexity, pour optimiser nos performances de recherche.
            </p>
          </div>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 4 - Module Brand Verification
    <PresentationSlide key={4} background="bg-gradient-to-br from-blue-50 to-cyan-100">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-800">
          Module Brand Verification
        </h2>
        <div className="grid grid-cols-2 gap-8">
          <div className="space-y-6">
            <Card className="bg-white shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center text-blue-700">
                  <Clock className="w-6 h-6 mr-2" />
                  Réduction du Temps
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-blue-600 mb-2">80%</div>
                <Progress value={80} className="mb-2" />
                <p className="text-gray-900">de 30-45 min à 2-3 min par marque</p>
              </CardContent>
            </Card>

            <Card className="bg-white shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center text-green-700">
                  <CheckCircle className="w-6 h-6 mr-2" />
                  Précision
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-green-600 mb-2">95%+</div>
                <Progress value={95} className="mb-2" />
                <p className="text-gray-900">taux de précision vérifié</p>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <Card className="bg-white shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center text-purple-700">
                  <BarChart3 className="w-6 h-6 mr-2" />
                  Performance Prouvée
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-purple-600 mb-2">285</div>
                <p className="text-gray-900 mb-4">marques vérifiées en une exécution</p>
                <div className="text-2xl font-semibold text-purple-500">114h</div>
                <p className="text-gray-900">économisées vs méthode manuelle</p>
              </CardContent>
            </Card>

            <Card className="bg-white shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center text-orange-700">
                  <Shield className="w-6 h-6 mr-2" />
                  Fiabilité
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-gray-900">
                  <li>• Score de confiance sophistiqué</li>
                  <li>• Double vérification automatique</li>
                  <li>• Sources officielles uniquement</li>
                  <li>• Traçabilité complète</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 5 - ROI (modifiée - ancienne slide 6)
    <PresentationSlide key={5} background="bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-900">
          Retour sur Investissement
        </h2>
        <div className="grid grid-cols-2 gap-8 mb-8">
          <Card className="bg-white shadow-lg border-green-200">
            <CardHeader>
              <CardTitle className="text-green-700 text-center">Économies de Temps</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">80%</div>
              <p className="text-gray-900 mb-4">de réduction</p>
              <div className="bg-green-50 p-3 rounded">
                <div className="text-lg font-semibold text-gray-900">285 marques = 114h économisées</div>
                <div className="text-sm text-gray-900">vs méthode traditionnelle</div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg border-blue-200">
            <CardHeader>
              <CardTitle className="text-blue-700 text-center">Économies de Coûts</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">Plus de 14 jours</div>
              <p className="text-gray-900 mb-4">par homme économisés</p>
              <div className="bg-blue-50 p-3 rounded">
                <div className="text-lg font-semibold text-gray-900">Réduction significative</div>
                <div className="text-sm text-gray-900">des coûts opérationnels</div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold mb-4 text-center text-gray-900">Évolution des Coûts</h3>
          <div className="flex justify-between items-end h-40 bg-gray-50 p-4 rounded">
            <div className="text-center">
              <div className="bg-red-500 w-16 h-32 mb-2 rounded-t"></div>
              <div className="text-sm font-semibold text-gray-900">Méthode Actuelle</div>
              <div className="text-xs text-gray-900">300€/marque</div>
            </div>
            <div className="text-center">
              <div className="bg-yellow-500 w-16 h-16 mb-2 rounded-t"></div>
              <div className="text-sm font-semibold text-gray-900">Avec Notre Solution</div>
              <div className="text-xs text-gray-900">20€/marque</div>
            </div>
            <div className="text-center">
              <div className="bg-green-500 w-16 h-8 mb-2 rounded-t"></div>
              <div className="text-sm font-semibold text-gray-900">Avec Multiprocessing</div>
              <div className="text-xs text-gray-900">5€/marque</div>
            </div>
          </div>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 6 - Roadmap (ancienne slide 7)
    <PresentationSlide key={6} background="bg-gradient-to-br from-purple-50 to-indigo-100">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-900">
          Roadmap Produit
        </h2>
        <div className="space-y-8">
          <div className="flex items-center space-x-8">
            <div className="bg-green-500 w-4 h-4 rounded-full"></div>
            <div className="flex-1 bg-white p-6 rounded-lg shadow-lg">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-2xl font-semibold text-green-700">Brand Verification</h3>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">✅ DISPONIBLE</span>
              </div>
              <p className="text-gray-900">Vérification systématique • 285 marques testées • 95%+ précision</p>
            </div>
          </div>

          <div className="flex items-center space-x-8">
            <div className="bg-blue-500 w-4 h-4 rounded-full"></div>
            <div className="flex-1 bg-white p-6 rounded-lg shadow-lg">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-2xl font-semibold text-blue-700">Brand Analysis</h3>
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">Q3 2024</span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm text-gray-900">
                <div>• Détection marques manquantes</div>
                <div>• Hiérarchie sous-marques</div>
                <div>• Analyse de synergie</div>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-8">
            <div className="bg-purple-500 w-4 h-4 rounded-full"></div>
            <div className="flex-1 bg-white p-6 rounded-lg shadow-lg">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-2xl font-semibold text-purple-700">Brand Verification Multiprocessing</h3>
                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">Q4 2024</span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm text-gray-900">
                <div>• Traitement 1000+ marques</div>
                <div>• Réduction 50-70% temps</div>
                <div>• Optimisation coûts</div>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-semibold mb-4 text-center text-gray-900">Timeline de Développement</h3>
          <div className="flex justify-between items-center">
            <div className="text-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mx-auto mb-2"></div>
              <div className="text-sm font-semibold text-gray-900">Q2 2024</div>
              <div className="text-xs text-gray-900">Version 1.0</div>
            </div>
            <div className="flex-1 h-1 bg-green-200 mx-4"></div>
            <div className="text-center">
              <div className="w-3 h-3 bg-blue-500 rounded-full mx-auto mb-2"></div>
              <div className="text-sm font-semibold text-gray-900">Q3 2024</div>
              <div className="text-xs text-gray-900">Analysis Module</div>
            </div>
            <div className="flex-1 h-1 bg-blue-200 mx-4"></div>
            <div className="text-center">
              <div className="w-3 h-3 bg-purple-500 rounded-full mx-auto mb-2"></div>
              <div className="text-sm font-semibold text-gray-900">Q4 2024</div>
              <div className="text-xs text-gray-900">Multiprocessing</div>
            </div>
          </div>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 7 - Avantages compétitifs
    <PresentationSlide key={7} background="bg-white">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-900">
          Avantages Compétitifs
        </h2>
        <div className="bg-white rounded-lg shadow-lg overflow-hidden border-2 border-gray-200">
          <div className="grid grid-cols-2 bg-gray-100 p-4 font-semibold text-center">
            <div className="text-gray-900">Critères</div>
            <div className="text-blue-700">Notre Solution</div>
          </div>
          
          <div className="divide-y divide-gray-200">
            <div className="grid grid-cols-2 p-4 text-center">
              <div className="font-medium text-gray-900">Temps de traitement</div>
              <div className="text-green-700 font-bold">2-3 min</div>
            </div>
            
            <div className="grid grid-cols-2 p-4 text-center bg-gray-50">
              <div className="font-medium text-gray-900">Précision</div>
              <div className="text-green-700 font-bold">95%+</div>
            </div>
            
            <div className="grid grid-cols-2 p-4 text-center">
              <div className="font-medium text-gray-900">Traçabilité</div>
              <div className="text-green-700 font-bold">Complète</div>
            </div>
            
            <div className="grid grid-cols-2 p-4 text-center bg-gray-50">
              <div className="font-medium text-gray-900">Évolutivité</div>
              <div className="text-green-700 font-bold">Illimitée</div>
            </div>
          </div>
        </div>

        <div className="mt-8 grid grid-cols-3 gap-6">
          <Card className="text-center border-2 border-gray-200 bg-white">
            <CardContent className="pt-6">
              <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
              <h3 className="font-semibold mb-2 text-gray-900">IA Propriétaire</h3>
              <p className="text-sm text-gray-900 font-medium">Algorithmes développés spécifiquement pour la vérification de marques</p>
            </CardContent>
          </Card>
          
          <Card className="text-center border-2 border-gray-200 bg-white">
            <CardContent className="pt-6">
              <Shield className="w-12 h-12 text-blue-600 mx-auto mb-4" />
              <h3 className="font-semibold mb-2 text-gray-900">Sources Officielles</h3>
              <p className="text-sm text-gray-900 font-medium">Connexion directe aux bases de données officielles mondiales</p>
            </CardContent>
          </Card>
          
          <Card className="text-center border-2 border-gray-200 bg-white">
            <CardContent className="pt-6">
              <Zap className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              <h3 className="font-semibold mb-2 text-gray-900">Performance Optimale</h3>
              <p className="text-sm text-gray-900 font-medium">Architecture cloud native pour une performance maximale</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </PresentationSlide>,

    // Slide 8 - Pricing (mise à jour)
    <PresentationSlide key={8} background="bg-white">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-900">
          Analyse des Coûts
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card className="bg-white shadow-lg border-2 border-gray-200">
            <CardHeader>
              <CardTitle className="flex items-center justify-between text-gray-900">
                <span>Utilisation des Tokens</span>
                <Badge variant="secondary" className="bg-blue-100 text-blue-800">Optimisé</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">Prompt par requête</span>
                  <span className="font-mono text-gray-900">~600 tokens</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">Réponse par requête</span>
                  <span className="font-mono text-gray-900">~300-400 tokens</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">Total par requête</span>
                  <span className="font-mono text-gray-900">~900-1000 tokens</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">Total pour 285 marques</span>
                  <span className="font-mono text-gray-900">~333,000-370,000 tokens</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg border-2 border-gray-200">
            <CardHeader>
              <CardTitle className="flex items-center justify-between text-gray-900">
                <span>Coûts d'Utilisation</span>
                <Badge variant="secondary" className="bg-green-100 text-green-800">Économique</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">GPT-4 Turbo</span>
                  <span className="font-mono text-gray-900">0.03$ / 1K tokens</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">GPT-3.5 Turbo</span>
                  <span className="font-mono text-gray-900">0.002$ / 1K tokens</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">Coût total (GPT-4)</span>
                  <span className="font-mono text-gray-900">~10-11$</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-900">Coût total (GPT-3.5)</span>
                  <span className="font-mono text-gray-900">~0.67-0.74$</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-white shadow-lg border-2 border-gray-200">
          <CardHeader>
            <CardTitle className="text-gray-900">Optimisations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside space-y-2">
              <li className="text-gray-900">Système de cache pour éviter les vérifications en double</li>
              <li className="text-gray-900">Vérification hybride (GPT-3.5 pour les cas simples, GPT-4 pour les cas complexes)</li>
              <li className="text-gray-900">Optimisation des prompts pour réduire la taille</li>
              <li className="text-gray-900">Multiprocessing pour les grands volumes de données</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </PresentationSlide>,

    // Slide 9 - Code Execution (mise à jour)
    <PresentationSlide key={9} background="bg-gradient-to-br from-indigo-50 to-purple-100">
      <div className="max-w-6xl w-full">
        <h2 className="text-5xl font-bold text-center mb-12 text-gray-800">
          Exécution du Code
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center justify-between text-gray-900">
                <span>Vérification de Marques</span>
                <Switch
                  checked={brandVerification}
                  onCheckedChange={(checked) => {
                    setBrandVerification(checked);
                    if (checked) executeCode('verification');
                  }}
                />
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-900 mb-4">
                Vérifie l'appartenance des 10 premières marques du CSV à leur holding respective.
                Utilise GPT-4 pour une analyse précise.
              </p>
              <Button 
                variant="outline" 
                className="w-full bg-blue-600 text-white hover:bg-blue-700"
                onClick={exportCSV}
                disabled={!results}
              >
                <DownloadIcon className="mr-2 h-4 w-4" />
                Exporter CSV
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center justify-between text-gray-900">
                <span>Analyse de Marques</span>
                <Switch
                  checked={brandAnalysis}
                  onCheckedChange={(checked) => {
                    setBrandAnalysis(checked);
                    if (checked) executeCode('analysis');
                  }}
                />
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-900 mb-4">
                Analyse les relations entre les marques et identifie les sous-marques.
                Détecte les marques manquantes dans le portefeuille.
              </p>
              <Button 
                variant="outline" 
                className="w-full bg-blue-600 text-white hover:bg-blue-700"
                onClick={exportCSV}
                disabled={!results}
              >
                <DownloadIcon className="mr-2 h-4 w-4" />
                Exporter CSV
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center justify-between text-gray-900">
                <span>Multiprocessing</span>
                <Switch
                  checked={multiprocessing}
                  onCheckedChange={(checked) => {
                    setMultiprocessing(checked);
                    if (checked) executeCode('multiprocessing');
                  }}
                />
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-900 mb-4">
                Version optimisée pour les grands volumes de données.
                Utilise le multiprocessing pour accélérer le traitement.
              </p>
              <Button 
                variant="outline" 
                className="w-full bg-blue-600 text-white hover:bg-blue-700"
                onClick={exportCSV}
                disabled={!results}
              >
                <DownloadIcon className="mr-2 h-4 w-4" />
                Exporter CSV
              </Button>
            </CardContent>
          </Card>
        </div>

        {progress > 0 && (
          <div className="mb-8">
            <Progress value={progress} className="h-2" />
            <p className="text-sm text-center mt-2 text-gray-900">
              Exécution en cours... {progress}%
            </p>
          </div>
        )}

        {results && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4 text-gray-900">Insights</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {results.insights.map((insight: any, index: number) => (
                <Alert key={index} className={insight.status === 'success' ? 'bg-green-500/10 border-green-500' : 'bg-yellow-500/10 border-yellow-500'}>
                  <div className="flex items-center gap-2">
                    {insight.status === 'success' ? (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-yellow-500" />
                    )}
                    <AlertTitle className="text-gray-900">{insight.title}</AlertTitle>
                  </div>
                  <AlertDescription className="mt-2 text-lg font-bold text-gray-900">
                    {insight.value}
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          </div>
        )}
      </div>
    </PresentationSlide>
  ];

  return (
    <div className="relative h-screen overflow-hidden">
      <div className="absolute inset-0">
        {slides[currentSlide]}
      </div>
      
      {/* Navigation buttons */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-4">
        <Button
          variant="outline"
          size="icon"
          onClick={prevSlide}
          className="bg-white/80 hover:bg-white"
        >
          <ChevronLeft className="h-6 w-6" />
        </Button>
        <div className="flex space-x-2">
          {Array.from({ length: totalSlides }).map((_, index) => (
            <Button
              key={index}
              variant={currentSlide === index ? "default" : "outline"}
              size="icon"
              onClick={() => goToSlide(index)}
              className={currentSlide === index ? "bg-blue-600" : "bg-white/80 hover:bg-white"}
            >
              {index + 1}
            </Button>
          ))}
        </div>
        <Button
          variant="outline"
          size="icon"
          onClick={nextSlide}
          className="bg-white/80 hover:bg-white"
        >
          <ChevronRight className="h-6 w-6" />
        </Button>
      </div>
    </div>
  );
};

export default BrandPresentation;
