import sys
import os
from pathlib import Path
import uvicorn

# Add the project root directory to the Python path
project_root = Path(__file__).parent  # C:\hackthone2_clone\Todo_App
sys.path.insert(0, str(project_root))

# Change to the project directory
os.chdir(project_root)

print("Starting server...")

try:
    from backend.src.main import app
    print("App imported successfully")
    
    # Run the server
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to continue...")