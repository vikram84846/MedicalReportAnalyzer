from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
import os

from models import AnalysisRequest, AnalysisResponse
from services.ai_service import AIService
from services.file_processor import FileProcessor
from utils.config import get_settings

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Medical Report Analyzer API",
    description="AI-powered medical report analysis using Gemini 2.0 Flash",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
settings = get_settings()
ai_service = AIService()
file_processor = FileProcessor()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Medical Report Analyzer API is running"}

@app.post("/analyze/image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze a medical report image and provide insights
    """
    try:
        # Validate file type with fallback for None content_type
        if file.content_type is None:
            # Check file extension as fallback
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                raise HTTPException(status_code=400, detail="File must be an image (JPG, PNG, GIF, BMP)")
        elif not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Process the image
        image_data = await file_processor.process_image(file)
        
        # Analyze with AI
        analysis = await ai_service.analyze_medical_report(image_data, "image")
        
        return AnalysisResponse(
            success=True,
            summary=analysis["summary"],
            key_findings=analysis["key_findings"],
            lifestyle_recommendations=analysis["lifestyle_recommendations"],
            precautions=analysis["precautions"],
            confidence_score=analysis["confidence_score"],
            complex_terms=analysis.get("complex_terms", {})
        )
    
    except Exception as e:
        import traceback
        print(f"Error in analyze_image: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/pdf", response_model=AnalysisResponse)
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Analyze a PDF medical report and provide insights
    """
    try:
        # Validate file type with fallback for None content_type
        if file.content_type is None:
            # Check file extension as fallback
            if not file.filename or not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="File must be a PDF")
        elif file.content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Process the PDF
        pdf_data = await file_processor.process_pdf(file)
        
        # Analyze with AI
        analysis = await ai_service.analyze_medical_report(pdf_data, "pdf")
        
        return AnalysisResponse(
            success=True,
            summary=analysis["summary"],
            key_findings=analysis["key_findings"],
            lifestyle_recommendations=analysis["lifestyle_recommendations"],
            precautions=analysis["precautions"],
            confidence_score=analysis["confidence_score"],
            complex_terms=analysis.get("complex_terms", {})
        )
    
    except Exception as e:
        import traceback
        print(f"Error in analyze_pdf: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Medical Report Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze_image": "/analyze/image",
            "analyze_pdf": "/analyze/pdf"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True
    ) 