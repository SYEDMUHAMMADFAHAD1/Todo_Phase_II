import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"

# Set environment variables
os.environ.setdefault('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
os.environ.setdefault('BETTER_AUTH_SECRET', 'test_secret_for_dev')

if __name__ == "__main__":
    import subprocess
    import sys
    
    # Set up the environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_dir) + os.pathsep + env.get('PYTHONPATH', '')
    
    # Run uvicorn as a subprocess with the correct PYTHONPATH
    result = subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "src.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ], cwd=backend_dir, env=env)
    
    if result.returncode != 0:
        print(f"Server exited with code: {result.returncode}")