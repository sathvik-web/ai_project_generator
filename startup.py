"""
Startup script for AI Project Generator
Runs both backend and frontend services
"""

import subprocess
import os
import sys
import time
from pathlib import Path

def setup_environment():
    """Setup environment and check prerequisites."""
    print("🚀 AI Project Generator - Startup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Error: Python 3.11+ required")
        sys.exit(1)
    
    print("✓ Python version OK")
    
    # Check if dependencies are installed
    try:
        import fastapi
        import streamlit
        import pydantic
    except ImportError:
        print("❌ Dependencies not installed!")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✓ Dependencies installed")
    
    # Check .env file
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("⚠️  .env file not found")
            print("   Copy .env.example to .env and configure GitHub token")
            print("   Backend will work without GitHub integration")
        else:
            print("⚠️  Neither .env nor .env.example found")
    
    print("\n" + "=" * 50)
    print("Starting services...\n")

def start_backend():
    """Start FastAPI backend."""
    print("Starting FastAPI backend on http://localhost:8000")
    print("API docs: http://localhost:8000/api/docs\n")
    
    # Run backend in subprocess
    try:
        subprocess.run([
            sys.executable, "backend/main.py"
        ])
    except KeyboardInterrupt:
        print("\n✓ Backend stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def start_frontend():
    """Start Streamlit frontend."""
    time.sleep(2)  # Give backend time to start
    print("Starting Streamlit frontend on http://localhost:8501\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "frontend/app.py",
            "--logger.level=info"
        ])
    except KeyboardInterrupt:
        print("\n✓ Frontend stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main entry point."""
    setup_environment()
    
    # On Windows, we need to handle subprocess differently
    if sys.platform == "win32":
        print("Windows detected - Starting backend only")
        print("\nTo start frontend, open another terminal and run:")
        print("  streamlit run frontend/app.py\n")
        start_backend()
    else:
        # On Unix-like systems, run both
        import threading
        
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        frontend_thread = threading.Thread(target=start_frontend, daemon=True)
        
        backend_thread.start()
        frontend_thread.start()
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n✓ All services stopped")

if __name__ == "__main__":
    main()
