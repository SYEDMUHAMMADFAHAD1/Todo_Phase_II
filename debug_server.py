import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent  # C:\hackthone2_clone\Todo_App
sys.path.insert(0, str(project_root))

print("Project root added to path:", str(project_root))

# Change to the project directory
os.chdir(project_root)

try:
    import uvicorn
    from backend.src.main import app
    print("Successfully imported app")
    
    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()