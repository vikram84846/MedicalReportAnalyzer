import { useMutation } from '@tanstack/react-query';
import { api, MedicalAnalysis, ApiError } from '@/lib/api';
import { toast } from 'sonner';

export const useMedicalAnalysis = () => {
  const analyzeImageMutation = useMutation({
    mutationFn: api.analyzeImage,
    onError: (error: ApiError) => {
      toast.error(`Failed to analyze image: ${error.message}`);
    },
  });

  const analyzePdfMutation = useMutation({
    mutationFn: api.analyzePdf,
    onError: (error: ApiError) => {
      toast.error(`Failed to analyze PDF: ${error.message}`);
    },
  });

  const analyzeFile = async (file: File): Promise<MedicalAnalysis | null> => {
    try {
      if (file.type === 'application/pdf') {
        return await analyzePdfMutation.mutateAsync(file);
      } else if (file.type.startsWith('image/')) {
        return await analyzeImageMutation.mutateAsync(file);
      } else {
        throw new Error('Unsupported file type');
      }
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(400, 'Unsupported file type');
    }
  };

  return {
    analyzeFile,
    isAnalyzing: analyzeImageMutation.isPending || analyzePdfMutation.isPending,
    error: analyzeImageMutation.error || analyzePdfMutation.error,
  };
}; 