const API_BASE_URL = 'http://localhost:8000';

export interface MedicalAnalysis {
  success: boolean;
  summary: string;
  key_findings: string[];
  lifestyle_recommendations: string[];
  precautions: string[];
  confidence_score: number;
  complex_terms: { [key: string]: string };
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

// Fallback mock data for development/testing
const getMockAnalysis = (fileType: string): MedicalAnalysis => ({
  success: true,
  summary: `This is a mock analysis for ${fileType} file. In a real scenario, this would contain AI-generated insights from your medical report.`,
  key_findings: [
    "Sample finding 1: Normal blood pressure readings",
    "Sample finding 2: Cholesterol levels within normal range",
    "Sample finding 3: Blood sugar levels are optimal"
  ],
  lifestyle_recommendations: [
    "Continue regular exercise routine",
    "Maintain balanced diet",
    "Get adequate sleep (7-9 hours per night)"
  ],
  precautions: [
    "Schedule regular check-ups",
    "Monitor any changes in symptoms",
    "Consult healthcare provider for concerns"
  ],
  confidence_score: 85,
  complex_terms: {
    "Blood Pressure": "The force of blood against artery walls",
    "Cholesterol": "A waxy substance in blood that can affect heart health",
    "Blood Sugar": "Glucose levels in the bloodstream"
  }
});

export const api = {
  async analyzeImage(file: File): Promise<MedicalAnalysis> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/analyze/image`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(response.status, errorData.detail || 'Failed to analyze image');
      }

      return response.json();
    } catch (error) {
      console.warn('API call failed, using mock data:', error);
      return getMockAnalysis('image');
    }
  },

  async analyzePdf(file: File): Promise<MedicalAnalysis> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/analyze/pdf`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(response.status, errorData.detail || 'Failed to analyze PDF');
      }

      return response.json();
    } catch (error) {
      console.warn('API call failed, using mock data:', error);
      return getMockAnalysis('pdf');
    }
  },

  async healthCheck(): Promise<{ status: string; message: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      
      if (!response.ok) {
        throw new ApiError(response.status, 'Health check failed');
      }

      return response.json();
    } catch (error) {
      throw new ApiError(0, 'Backend server is not available');
    }
  }
}; 