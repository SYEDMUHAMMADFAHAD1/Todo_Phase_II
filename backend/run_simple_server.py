import sys
import os
from pathlib import Path

# Only add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
os.chdir(backend_dir)

# Import the app using relative imports
import uvicorn
from src.main import app

if __name__ == "__main__":
    print("Starting backend server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)