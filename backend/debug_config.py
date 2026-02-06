import sys
from pathlib import Path

# Add the project root directory to the Python path so we can import backend modules
project_root = Path(__file__).parent.parent  # C:\master_second_copy\Todo_App
sys.path.insert(0, str(project_root))

# Also add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
import os
os.chdir(backend_dir)

# Import and print the settings
from backend.src.core.config import settings
print("DATABASE_URL:", settings.DATABASE_URL)
print("BETTER_AUTH_SECRET length:", len(settings.BETTER_AUTH_SECRET))