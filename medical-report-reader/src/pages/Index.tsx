import { useState } from "react";
import { FileUpload } from "@/components/FileUpload";
import { AnalysisResults } from "@/components/AnalysisResults";
import { Header } from "@/components/Header";
import { Stethoscope, Upload, FileText } from "lucide-react";
import { useMedicalAnalysis } from "@/hooks/useMedicalAnalysis";
import { useHealthCheck } from "@/hooks/useHealthCheck";
import { MedicalAnalysis } from "@/lib/api";
import { toast } from "sonner";

const Index = () => {
  const [analysis, setAnalysis] = useState<MedicalAnalysis | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { analyzeFile, isAnalyzing, error } = useMedicalAnalysis();
  const {
    data: healthData,
    isLoading: isHealthLoading,
    error: healthError,
  } = useHealthCheck();

  const handleFileUpload = async (file: File) => {
    setUploadedFile(file);

    try {
      const result = await analyzeFile(file);
      if (result) {
        setAnalysis(result);
        toast.success("Analysis completed successfully!");
      }
    } catch (error) {
      console.error("Analysis failed:", error);
      setAnalysis(null);
    }
  };

  const handleReset = () => {
    setAnalysis(null);
    setUploadedFile(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <Header />

      <main className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-6">
            <div className="p-3 bg-blue-100 rounded-full">
              <Stethoscope className="w-8 h-8 text-blue-600" />
            </div>
            <h1 className="text-4xl font-bold text-gray-800">
              Medical Report Analyzer
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload your medical reports and get comprehensive analysis with
            AI-powered insights, lifestyle recommendations, and
            easy-to-understand explanations.
          </p>
        </div>

        {!analysis && !isAnalyzing && (
          <div className="max-w-2xl mx-auto">
            {/* Connection Status */}
            <div className="mb-6 p-4 rounded-lg border">
              <div className="flex items-center gap-2 mb-2">
                <div
                  className={`w-3 h-3 rounded-full ${
                    healthError
                      ? "bg-red-500"
                      : healthData
                      ? "bg-green-500"
                      : "bg-yellow-500"
                  }`}
                ></div>
                <span className="font-medium">
                  {healthError
                    ? "Backend Disconnected"
                    : healthData
                    ? "Backend Connected"
                    : "Connecting to Backend..."}
                </span>
              </div>
              {healthError && (
                <p className="text-sm text-red-600">
                  Please make sure the backend server is running at
                  http://localhost:8000
                </p>
              )}
            </div>

            <FileUpload
              onFileUpload={handleFileUpload}
              disabled={!!healthError}
            />

            <div className="mt-12 grid md:grid-cols-3 gap-6">
              <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
                <Upload className="w-8 h-8 text-blue-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-800 mb-2">
                  Easy Upload
                </h3>
                <p className="text-sm text-gray-600">
                  Support for images and PDF files
                </p>
              </div>
              <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
                <FileText className="w-8 h-8 text-green-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-800 mb-2">
                  AI Analysis
                </h3>
                <p className="text-sm text-gray-600">
                  Advanced medical report interpretation
                </p>
              </div>
              <div className="text-center p-6 bg-white rounded-lg shadow-sm border">
                <Stethoscope className="w-8 h-8 text-purple-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-800 mb-2">
                  Expert Insights
                </h3>
                <p className="text-sm text-gray-600">
                  Personalized recommendations
                </p>
              </div>
            </div>
          </div>
        )}

        {isAnalyzing && (
          <div className="max-w-2xl mx-auto text-center">
            <div className="bg-white rounded-2xl shadow-lg p-12">
              <div className="animate-spin w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full mx-auto mb-6"></div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                Analyzing Your Report
              </h3>
              <p className="text-gray-600">
                Our AI is carefully reviewing your medical data...
              </p>
              {uploadedFile && (
                <p className="text-sm text-gray-500 mt-2">
                  Processing: {uploadedFile.name}
                </p>
              )}
            </div>
          </div>
        )}

        {analysis && (
          <AnalysisResults analysis={analysis} onReset={handleReset} />
        )}
      </main>
    </div>
  );
};

export default Index;
