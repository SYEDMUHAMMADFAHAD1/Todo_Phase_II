import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
os.chdir(backend_dir)

# Set environment variables if needed
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
os.environ.setdefault('BETTER_AUTH_SECRET', 'test_secret_for_dev')

# Import and run the app
if __name__ == "__main__":
    import uvicorn
    from src.main import app

    print("Starting backend server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)