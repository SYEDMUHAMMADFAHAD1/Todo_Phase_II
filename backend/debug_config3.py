import os
from pathlib import Path

# Change to the backend directory
backend_dir = Path(__file__).parent
os.chdir(backend_dir)
print(f"Current working directory: {os.getcwd()}")

# Check if .env file exists and what it contains
env_file = backend_dir / ".env"
if env_file.exists():
    print(f".env file exists: {env_file}")
    with open(env_file, 'r') as f:
        content = f.read()
        print(f".env file content:\n{content}")
else:
    print(".env file does not exist in backend directory")

# Check for .env in parent directory
parent_env_file = backend_dir.parent / ".env"
if parent_env_file.exists():
    print(f"\nFound .env in parent directory: {parent_env_file}")
else:
    print("\nNo .env file in parent directory")

# Now try to load settings
import sys
sys.path.insert(0, str(backend_dir))  # Add backend dir to path
sys.path.insert(0, str(backend_dir / "src"))  # Add src dir to path

# Import settings
from core.config import settings  # Using relative import from src
print(f"\nLoaded DATABASE_URL: {settings.DATABASE_URL}")