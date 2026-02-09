#!/usr/bin/env python
"""
Start script for the Todo application backend
This script starts the FastAPI application in the backend directory
"""

import os
import sys
from pathlib import Path

def main():
    # Add the backend directory to Python path
    backend_dir = Path(__file__).parent / "backend"
    sys.path.insert(0, str(backend_dir))
    
    # Temporarily modify sys.path to avoid conflicts with root src directory
    original_path = sys.path[:]
    # Remove the root src from path temporarily to avoid import conflicts
    root_src = str(Path(__file__).parent / "src")
    if root_src in sys.path:
        sys.path.remove(root_src)
    
    # Import and run the application
    from src.main import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
    # Restore original path if needed
    sys.path[:] = original_path

if __name__ == "__main__":
    main()