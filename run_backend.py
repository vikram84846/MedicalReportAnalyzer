#!/usr/bin/env python3
"""
Startup script for the Medical Report Analyzer Backend
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables
load_dotenv()

def main():
    """Start the backend server"""
    try:
        # Import and run the backend
        from backend.main import app
        import uvicorn
        from backend.utils.config import get_settings
        
        settings = get_settings()
        
        print("🏥 Starting Medical Report Analyzer Backend...")
        print(f"📍 Server will be available at: http://{settings.backend_host}:{settings.backend_port}")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔄 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        uvicorn.run(
            "backend.main:app",
            host=settings.backend_host,
            port=settings.backend_port,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Error importing backend modules: {e}")
        print("💡 Make sure you have installed all dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 