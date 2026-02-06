import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent  # C:\hackthone2_clone\Todo_App
sys.path.insert(0, str(project_root))

# Change to the project directory
os.chdir(project_root)

print("Testing individual components...")

try:
    print("1. Testing config import...")
    from backend.src.core.config import settings
    print("   Config imported successfully")
    print(f"   Database URL: {settings.DATABASE_URL}")
    print(f"   Auth Secret: {'*' * len(settings.BETTER_AUTH_SECRET)}")
except Exception as e:
    print(f"   Error importing config: {e}")

try:
    print("2. Testing database import...")
    from backend.src.core.db import init_db, get_session, engine
    print("   Database components imported successfully")
except Exception as e:
    print(f"   Error importing database: {e}")

try:
    print("3. Testing auth import...")
    from backend.auth import verify_token, get_current_user
    print("   Auth components imported successfully")
except Exception as e:
    print(f"   Error importing auth: {e}")

try:
    print("4. Testing models import...")
    from backend.src.models.task import Task, User
    print("   Models imported successfully")
except Exception as e:
    print(f"   Error importing models: {e}")

try:
    print("5. Testing services import...")
    from backend.src.services.task_service import TaskService
    print("   Services imported successfully")
except Exception as e:
    print(f"   Error importing services: {e}")

try:
    print("6. Testing routers import...")
    from backend.src.api.routers import tasks, auth
    print("   Routers imported successfully")
except Exception as e:
    print(f"   Error importing routers: {e}")

try:
    print("7. Testing main app import...")
    from backend.src.main import app
    print("   Main app imported successfully")
except Exception as e:
    print(f"   Error importing main app: {e}")

print("Component testing completed.")