import subprocess
import sys
import os
from pathlib import Path

# Set environment variables if needed
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
os.environ.setdefault('BETTER_AUTH_SECRET', 'test_secret_for_dev')

# Change to the backend directory and run the server using subprocess
backend_dir = Path(__file__).parent / "backend"

if __name__ == "__main__":
    # Run the server from the backend directory using PYTHONPATH to handle imports
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_dir) + os.pathsep + env.get('PYTHONPATH', '')
    
    result = subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"  # Enable auto-reload for development
    ], cwd=backend_dir, env=env)

    if result.returncode != 0:
        print(f"Server exited with code: {result.returncode}")