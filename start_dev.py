#!/usr/bin/env python3
"""
Development startup script for Medical Report Analyzer
Starts both backend and frontend servers
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("🏥 Medical Report Analyzer - Development Server")
    print("=" * 50)
    print("Starting both backend and frontend servers...")
    print("Backend:  http://localhost:8000")
    print("Frontend: http://localhost:3000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 50)

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    try:
        subprocess.run([sys.executable, "run_backend.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the frontend server"""
    print("🎨 Starting frontend server...")
    frontend_dir = Path("medical-report-reader")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found. Make sure you're in the project root.")
        return
    
    try:
        # Change to frontend directory and start npm dev
        os.chdir(frontend_dir)
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except FileNotFoundError:
        print("❌ npm not found. Make sure Node.js is installed.")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def main():
    """Main function to start both servers"""
    print_banner()
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend
    start_frontend()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Development servers stopped")
        sys.exit(0) 