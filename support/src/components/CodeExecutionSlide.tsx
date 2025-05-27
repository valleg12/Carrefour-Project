import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { InfoIcon, CheckCircle2Icon, AlertCircleIcon, DownloadIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

export function CodeExecutionSlide() {
  const [brandVerification, setBrandVerification] = useState(false);
  const [brandAnalysis, setBrandAnalysis] = useState(false);
  const [multiprocessing, setMultiprocessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);

  const executeCode = async (type: string) => {
    setProgress(0);
    // Simuler l'exécution du code
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));
      setProgress(i);
    }
    
    // Simuler les résultats
    setResults({
      type,
      insights: [
        {
          title: "Marques Vérifiées",
          value: "10/10",
          status: "success"
        },
        {
          title: "Score Moyen de Confiance",
          value: "85%",
          status: "success"
        },
        {
          title: "Marques à Vérifier Manuellement",
          value: "2",
          status: "warning"
        }
      ]
    });
  };

  const exportCSV = () => {
    // Simuler l'export du CSV
    const csvContent = "data:text/csv;charset=utf-8," + 
      "Brand Name,Holding Name,Belongs To,Confidence,Explanation\n" +
      "Brand1,Holding1,true,95,Verified\n" +
      "Brand2,Holding2,false,85,Needs verification";
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "brand_verification_results.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-3xl font-bold mb-8 text-center">Exécution du Code</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="bg-white/5 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
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
            <p className="text-sm text-gray-400 mb-4">
              Vérifie l'appartenance des 10 premières marques du CSV à leur holding respective.
              Utilise GPT-4 pour une analyse précise.
            </p>
            <Button 
              variant="outline" 
              className="w-full"
              onClick={exportCSV}
              disabled={!results}
            >
              <DownloadIcon className="mr-2 h-4 w-4" />
              Exporter CSV
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-white/5 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
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
            <p className="text-sm text-gray-400 mb-4">
              Analyse les relations entre les marques et identifie les sous-marques.
              Détecte les marques manquantes dans le portefeuille.
            </p>
            <Button 
              variant="outline" 
              className="w-full"
              onClick={exportCSV}
              disabled={!results}
            >
              <DownloadIcon className="mr-2 h-4 w-4" />
              Exporter CSV
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-white/5 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
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
            <p className="text-sm text-gray-400 mb-4">
              Version optimisée pour les grands volumes de données.
              Utilise le multiprocessing pour accélérer le traitement.
            </p>
            <Button 
              variant="outline" 
              className="w-full"
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
          <p className="text-sm text-center mt-2">
            Exécution en cours... {progress}%
          </p>
        </div>
      )}

      {results && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold mb-4">Insights</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {results.insights.map((insight: any, index: number) => (
              <Alert key={index} className={insight.status === 'success' ? 'bg-green-500/10' : 'bg-yellow-500/10'}>
                <div className="flex items-center gap-2">
                  {insight.status === 'success' ? (
                    <CheckCircle2Icon className="h-4 w-4 text-green-500" />
                  ) : (
                    <AlertCircleIcon className="h-4 w-4 text-yellow-500" />
                  )}
                  <AlertTitle>{insight.title}</AlertTitle>
                </div>
                <AlertDescription className="mt-2 text-lg font-bold">
                  {insight.value}
                </AlertDescription>
              </Alert>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 