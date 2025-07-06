import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import base64
import json
from typing import Dict, Any
from utils.config import get_settings

class AIService:
    """Service for AI-powered medical report analysis using Gemini 2.0 Flash"""
    
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.google_api_key)
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=settings.google_api_key,
            temperature=0.1
        )
    
    async def analyze_medical_report(self, content: str, file_type: str) -> Dict[str, Any]:
        """
        Analyze medical report content and provide comprehensive insights.
        Also explain complex medical terms in laymen tclserms.
        
        Args:
            content: The processed content from the medical report
            file_type: Type of file (image/pdf)
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Create comprehensive prompt for medical analysis
            prompt = self._create_analysis_prompt(content, file_type)
            
            # Generate analysis using Gemini
            response = await self._generate_analysis(prompt)
            
            # Parse the response
            analysis = self._parse_analysis_response(response)
            
            # Extract and explain complex medical terms
            complex_terms = await self._extract_and_explain_terms(content)
            analysis["complex_terms"] = complex_terms
            
            return analysis
            
        except Exception as e:
            raise Exception(f"AI analysis failed: {str(e)}")
    
    def _create_analysis_prompt(self, content: str, file_type: str) -> str:
        """Create a comprehensive prompt for medical report analysis"""
        
        prompt = f"""
        You are a medical AI assistant with expertise in analyzing medical reports. 
        Please analyze the following medical report content and provide a comprehensive analysis.

        Report Content (from {file_type}):
        {content}

        Please provide your analysis in the following JSON format:
        {{
            "summary": "A concise 2-3 sentence summary of the main findings",
            "key_findings": [
                "Finding 1",
                "Finding 2",
                "Finding 3"
            ],
            "lifestyle_recommendations": [
                "Recommendation 1",
                "Recommendation 2",
                "Recommendation 3"
            ],
            "precautions": [
                "Precaution 1",
                "Precaution 2",
                "Precaution 3"
            ],
            "confidence_score": 0.85
        }}

        Guidelines for analysis:
        1. Focus on clinically relevant information
        2. Identify abnormal values and their significance
        3. Provide practical lifestyle recommendations
        4. Highlight important precautions and warnings
        5. Maintain medical accuracy and professionalism
        6. If the content is unclear or incomplete, note this in the summary
        7. Confidence score should reflect the clarity and completeness of the report
        8. Use simple, clear language that patients can understand

        Please respond with only the JSON object, no additional text.
        """
        
        return prompt
    
    async def _generate_analysis(self, prompt: str) -> str:
        """Generate analysis using Gemini model"""
        try:
            # Use the chat model for better structured responses
            messages = [HumanMessage(content=prompt)]
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            # Fallback to direct model call if chat fails
            response = self.model.generate_content(prompt)
            return response.text
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response into structured format"""
        try:
            # Clean the response and extract JSON
            response = response.strip()
            
            # Try to find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                analysis = json.loads(json_str)
            else:
                # If no JSON found, create a fallback response
                analysis = self._create_fallback_response(response)
            
            # Validate and ensure all required fields are present
            required_fields = ["summary", "key_findings", "lifestyle_recommendations", "precautions", "confidence_score"]
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = self._get_default_value(field)
            
            return analysis
            
        except json.JSONDecodeError:
            # If JSON parsing fails, create a fallback response
            return self._create_fallback_response(response)
    
    def _create_fallback_response(self, response: str) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails"""
        return {
            "summary": f"Analysis completed. Raw response: {response[:200]}...",
            "key_findings": ["Analysis completed but response format was unexpected"],
            "lifestyle_recommendations": ["Please consult with a healthcare professional for personalized advice"],
            "precautions": ["This analysis is for informational purposes only"],
            "confidence_score": 0.5
        }
    
    def _get_default_value(self, field: str) -> Any:
        """Get default values for missing fields"""
        defaults = {
            "summary": "Analysis completed but summary not available",
            "key_findings": ["Analysis completed but findings not available"],
            "lifestyle_recommendations": ["Please consult with a healthcare professional"],
            "precautions": ["This analysis is for informational purposes only"],
            "confidence_score": 0.5
        }
        return defaults.get(field, "")
    
    async def _extract_and_explain_terms(self, content: str) -> Dict[str, str]:
        """
        Extract complex medical terms from the content and provide simple explanations
        
        Args:
            content: The medical report content
            
        Returns:
            Dictionary mapping complex terms to their simple explanations
        """
        try:
            prompt = f"""
            You are a medical expert. Please identify complex medical terms, abbreviations, 
            and technical jargon from the following medical report content and provide 
            simple, easy-to-understand explanations for each term.

            Medical Report Content:
            {content}

            Please provide your response in the following JSON format:
            {{
                "term1": "Simple explanation in layman's terms",
                "term2": "Simple explanation in layman's terms",
                "term3": "Simple explanation in layman's terms"
            }}

            Guidelines:
            1. Focus on medical terms that patients might not understand
            2. Include abbreviations and their full meanings
            3. Explain in simple, non-technical language
            4. Limit to the most important 5-10 terms
            5. If no complex terms are found, return an empty object {{}}

            Please respond with only the JSON object, no additional text.
            """
            
            response = await self._generate_analysis(prompt)
            
            # Parse the response
            try:
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response[start_idx:end_idx]
                    terms = json.loads(json_str)
                else:
                    terms = {}
                    
            except json.JSONDecodeError:
                terms = {}
            
            return terms
            
        except Exception as e:
            print(f"Error extracting terms: {str(e)}")
            return {} 