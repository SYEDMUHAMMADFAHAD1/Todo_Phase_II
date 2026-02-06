import asyncio
import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent  # C:\hackthone2_clone\Todo_App
sys.path.insert(0, str(project_root))

# Change to the project directory
os.chdir(project_root)

async def test_database_connection():
    try:
        print("Testing database connection...")
        
        # Load environment
        from dotenv import load_dotenv
        load_dotenv(dotenv_path="./backend/.env")
        
        from backend.src.core.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import text
        
        async with engine.begin() as conn:
            # Test the connection
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            
        # Test creating tables
        from backend.src.core.db import init_db
        await init_db()
        print("Database initialized successfully!")
        
        # Test creating a session
        async with AsyncSession(engine) as session:
            print("Session created successfully!")
            
        print("Database test completed successfully!")
        
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_task_creation():
    try:
        print("\nTesting task creation...")
        
        # Load environment
        from dotenv import load_dotenv
        load_dotenv(dotenv_path="./backend/.env")
        
        from backend.src.core.db import engine
        from sqlalchemy.ext.asyncio import AsyncSession
        
        # Create a session
        async with AsyncSession(engine) as session:
            # Import task service
            from backend.src.services.task_service import TaskService
            from backend.src.models.task import TaskCreate
            
            # Create task service
            service = TaskService(session)
            
            # Create a test task
            task_create = TaskCreate(
                title="Test Task",
                description="This is a test task",
                is_completed=False
            )
            
            # Try to create a task (this will fail without a valid user_id)
            # But it should not cause an internal server error
            try:
                result = await service.create_task(task_create, "test_user_id")
                print("Task created successfully!")
            except Exception as e:
                print(f"Expected error during task creation (due to invalid user): {e}")
                
        print("Task creation test completed!")
        
    except Exception as e:
        print(f"Task creation test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    await test_database_connection()
    await test_task_creation()

if __name__ == "__main__":
    asyncio.run(main())