from pydantic import BaseModel
from typing import List, Optional, Dict

class AnalysisRequest(BaseModel):
    """Request model for medical report analysis"""
    file_type: str
    content: str

class AnalysisResponse(BaseModel):
    """Response model for medical report analysis"""
    success: bool
    summary: str
    key_findings: List[str]
    lifestyle_recommendations: List[str]
    precautions: List[str]
    confidence_score: float
    complex_terms: Optional[Dict[str, str]] = None
    error_message: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    message: str 