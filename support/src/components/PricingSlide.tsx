import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function PricingSlide() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-3xl font-bold mb-8 text-center">Analyse des Coûts</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-white/5 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Utilisation des Tokens</span>
              <Badge variant="secondary">Optimisé</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span>Prompt par requête</span>
                <span className="font-mono">~600 tokens</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Réponse par requête</span>
                <span className="font-mono">~300-400 tokens</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Total par requête</span>
                <span className="font-mono">~900-1000 tokens</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Total pour 285 marques</span>
                <span className="font-mono">~333,000-370,000 tokens</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-white/5 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Coûts d'Utilisation</span>
              <Badge variant="secondary">Économique</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span>GPT-4 Turbo</span>
                <span className="font-mono">0.03$ / 1K tokens</span>
              </div>
              <div className="flex justify-between items-center">
                <span>GPT-3.5 Turbo</span>
                <span className="font-mono">0.002$ / 1K tokens</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Coût total (GPT-4)</span>
                <span className="font-mono">~10-11$</span>
              </div>
              <div className="flex justify-between items-center">
                <span>Coût total (GPT-3.5)</span>
                <span className="font-mono">~0.67-0.74$</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <Card className="bg-white/5 backdrop-blur-sm">
          <CardHeader>
            <CardTitle>Optimisations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside space-y-2">
              <li>Système de cache pour éviter les vérifications en double</li>
              <li>Vérification hybride (GPT-3.5 pour les cas simples, GPT-4 pour les cas complexes)</li>
              <li>Optimisation des prompts pour réduire la taille</li>
              <li>Multiprocessing pour les grands volumes de données</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 