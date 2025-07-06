import { useState } from "react";
import {
  FileText,
  TrendingUp,
  Heart,
  Shield,
  Gauge,
  HelpCircle,
  RefreshCw,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { MedicalAnalysis } from "@/lib/api";

interface AnalysisResultsProps {
  analysis: MedicalAnalysis;
  onReset: () => void;
}

export const AnalysisResults = ({
  analysis,
  onReset,
}: AnalysisResultsProps) => {
  const [expandedTerms, setExpandedTerms] = useState<string[]>([]);

  const toggleTerm = (term: string) => {
    setExpandedTerms((prev) =>
      prev.includes(term) ? prev.filter((t) => t !== term) : [...prev, term]
    );
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return "text-green-600 bg-green-100";
    if (confidence >= 60) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  const getConfidenceText = (confidence: number) => {
    if (confidence >= 80) return "High Confidence";
    if (confidence >= 60) return "Medium Confidence";
    return "Low Confidence";
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header with Reset Button */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-800">Analysis Results</h2>
        <Button
          onClick={onReset}
          variant="outline"
          className="flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Analyze New Report
        </Button>
      </div>

      {/* Confidence Score */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <Gauge className="w-5 h-5 text-blue-600" />
            Analysis Confidence
          </CardTitle>
          <Badge
            className={getConfidenceColor(analysis.confidence_score * 100)}
          >
            {getConfidenceText(analysis.confidence_score * 100)}
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <Progress
              value={analysis.confidence_score * 100}
              className="flex-1"
            />
            <span className="text-2xl font-bold text-gray-800">
              {analysis.confidence_score * 100}%
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-600" />
            Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 leading-relaxed text-lg">
            {analysis.summary}
          </p>
        </CardContent>
      </Card>

      {/* Key Findings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-600" />
            Key Findings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {analysis.key_findings.map((finding, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
              >
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                <p className="text-gray-700">{finding}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Lifestyle Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Heart className="w-5 h-5 text-red-500" />
              Lifestyle Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {analysis.lifestyle_recommendations.map(
                (recommendation, index) => (
                  <div
                    key={index}
                    className="flex items-start gap-3 p-3 bg-green-50 rounded-lg border-l-4 border-green-400"
                  >
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-700">{recommendation}</p>
                  </div>
                )
              )}
            </div>
          </CardContent>
        </Card>

        {/* Precautions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-orange-500" />
              Precautions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {analysis.precautions.map((precaution, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 bg-orange-50 rounded-lg border-l-4 border-orange-400"
                >
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p className="text-gray-700">{precaution}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Complex Terms Explanation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-purple-600" />
            Medical Terms Explained
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {Object.entries(analysis.complex_terms).map(
              ([term, explanation]) => (
                <div key={term} className="border rounded-lg overflow-hidden">
                  <button
                    onClick={() => toggleTerm(term)}
                    className="w-full flex items-center justify-between p-4 bg-purple-50 hover:bg-purple-100 transition-colors"
                  >
                    <span className="font-semibold text-purple-800">
                      {term}
                    </span>
                    {expandedTerms.includes(term) ? (
                      <ChevronUp className="w-5 h-5 text-purple-600" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-purple-600" />
                    )}
                  </button>
                  {expandedTerms.includes(term) && (
                    <div className="p-4 bg-white border-t">
                      <p className="text-gray-700">{explanation}</p>
                    </div>
                  )}
                </div>
              )
            )}
          </div>
        </CardContent>
      </Card>

      {/* Disclaimer */}
      <Card className="bg-yellow-50 border-yellow-200">
        <CardContent className="pt-6">
          <p className="text-sm text-gray-600">
            <strong>Medical Disclaimer:</strong> This analysis is for
            informational purposes only and should not replace professional
            medical advice. Always consult with qualified healthcare providers
            for medical decisions and treatment plans.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};
