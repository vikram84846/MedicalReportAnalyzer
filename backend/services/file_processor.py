import io
import base64
from PIL import Image
import PyPDF2
from fastapi import UploadFile
import google.generativeai as genai
from typing import Optional
from utils.config import get_settings

class FileProcessor:
    """Service for processing medical report files (images and PDFs)"""
    
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def process_image(self, file: UploadFile) -> str:
        """
        Process an image file and extract text content
        
        Args:
            file: Uploaded image file
            
        Returns:
            Extracted text content from the image
        """
        try:
            # Read the image file
            image_data = await file.read()
            
            # Convert to PIL Image for processing
            image = Image.open(io.BytesIO(image_data))
            
            # Use Gemini Vision to extract text from image
            text_content = await self._extract_text_from_image(image, image_data)
            
            return text_content
            
        except Exception as e:
            raise Exception(f"Image processing failed: {str(e)}")
    
    async def process_pdf(self, file: UploadFile) -> str:
        """
        Process a PDF file and extract text content
        
        Args:
            file: Uploaded PDF file
            
        Returns:
            Extracted text content from the PDF
        """
        try:
            # Read the PDF file
            pdf_data = await file.read()
            
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(pdf_data)
            
            return text_content
            
        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")
    
    async def _extract_text_from_image(self, image: Image.Image, image_data: bytes) -> str:
        """
        Extract text from image using Gemini Vision
        
        Args:
            image: PIL Image object
            image_data: Raw image bytes
            
        Returns:
            Extracted text content
        """
        try:
            # Use the original image data for Gemini
            # Create prompt for text extraction
            prompt = """
            Please extract all the text content from this medical report image. 
            Focus on:
            1. Patient information
            2. Test results and values
            3. Medical terminology and diagnoses
            4. Dates and timestamps
            5. Doctor/hospital information
            
            Return the extracted text in a clear, readable format.
            """
            
            # Use Gemini Vision to extract text
            response = self.model.generate_content([prompt, {"mime_type": "image/png", "data": image_data}])
            
            return response.text
            
        except Exception as e:
            # Fallback: return basic image info
            return f"Image processing completed but text extraction failed: {str(e)}"
    
    def _extract_text_from_pdf(self, pdf_data: bytes) -> str:
        """
        Extract text from PDF using PyPDF2
        
        Args:
            pdf_data: PDF file bytes
            
        Returns:
            Extracted text content
        """
        try:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
            
            # Extract text from all pages
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
            
            # Clean up the extracted text
            text_content = self._clean_extracted_text(text_content)
            
            return text_content
            
        except Exception as e:
            raise Exception(f"PDF text extraction failed: {str(e)}")
    
    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean and format extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text content
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common PDF artifacts
        text = text.replace('\x00', '')  # Remove null bytes
        text = text.replace('\n\n\n', '\n\n')  # Reduce multiple newlines
        
        # Ensure text is not too long for AI processing
        if len(text) > 8000:
            text = text[:8000] + "... [Content truncated for processing]"
        
        return text
    
    def validate_file_size(self, file: UploadFile, max_size_mb: int = 10) -> bool:
        """
        Validate file size
        
        Args:
            file: Uploaded file
            max_size_mb: Maximum file size in MB
            
        Returns:
            True if file size is acceptable
        """
        # Read file size (this will be done in processing anyway)
        file_size = 0
        try:
            content = file.file.read()
            file_size = len(content)
            # Reset file pointer
            file.file.seek(0)
        except:
            pass
        
        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes 