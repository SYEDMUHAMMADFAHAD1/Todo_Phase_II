import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent  # Go up to C:\hackthone2_clone\Todo_App
sys.path.insert(0, str(project_root))

# Also add the backend directory to the Python path
backend_dir = Path(__file__).parent  # C:\hackthone2_clone\Todo_App\backend
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
os.chdir(backend_dir)

print("Current working directory:", os.getcwd())
print("Python path added:", str(project_root))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

print("\nAfter loading .env:")
print("DATABASE_URL:", os.environ.get('DATABASE_URL'))
print("BETTER_AUTH_SECRET:", os.environ.get('BETTER_AUTH_SECRET'))

try:
    print("\nTrying to import main...")
    from backend.src.main import app
    print("Main app imported successfully!")

    print("\nTrying to initialize database...")
    import asyncio
    from backend.src.core.db import init_db

    async def test_init():
        try:
            await init_db()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            import traceback
            traceback.print_exc()

    asyncio.run(test_init())

except Exception as e:
    print(f"Error importing main app: {e}")
    import traceback
    traceback.print_exc()