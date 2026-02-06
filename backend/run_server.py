import sys
import os
from pathlib import Path

# Add the project root directory to the Python path so we can import backend modules
project_root = Path(__file__).parent.parent  # C:\hackthone2_clone\Todo_App
sys.path.insert(0, str(project_root))

# Also add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
os.chdir(Path(__file__).parent)

# Import the app using absolute imports
import uvicorn
from src.main import app

if __name__ == "__main__":
    print("Starting backend server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)