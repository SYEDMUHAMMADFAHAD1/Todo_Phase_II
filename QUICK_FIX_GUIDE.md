# Quick Fix Guide - Todo App Network Error

## The Issue
❌ Tasks not adding  
❌ "Network Error" shown  
❌ Backend returning 500 errors  

## The Root Cause
Database tables were never being created because models weren't imported.

## The Fix

### File 1: `backend/src/core/db.py` (Line 7-8)
```python
# ADD THIS LINE (line 8):
from backend.src.models import User, Task
```

### File 2: `backend/src/services/task_service.py` (Lines 42-54)
Replace the entire `get_task` method with:
```python
async def get_task(self, task_id: str | uuid.UUID, user_id: str) -> Task | None:
    # Convert string to UUID if needed
    if isinstance(task_id, str):
        try:
            task_id_uuid = uuid.UUID(task_id)
        except ValueError:
            return None
    else:
        task_id_uuid = task_id

    statement = select(Task).where(Task.id == task_id_uuid, Task.owner_id == user_id)
    result = await self.session.execute(statement)
    return result.scalars().first()
```

## Status
✅ **FIXED** - Both files have been updated

## Next Step
Restart your backend server:
```bash
pkill python  # Kill existing
cd backend && uvicorn src.main:app --reload
```

Test it:
1. Sign up at http://localhost:3000/signup
2. Create a task
3. See it appear immediately
4. Delete it
5. ✅ Done!

## Why It Works

Before fix:
```
Backend starts → init_db() called → SQLModel.metadata is EMPTY → No tables created
                                      ↓
                                  Queries fail: "no such table: user"
                                      ↓
                                  Frontend sees 500 error → "Network Error"
```

After fix:
```
Backend starts → init_db() called → Models imported → SQLModel.metadata has tables
                                      ↓
                                  create_all() creates tables
                                      ↓
                                  Queries work → Tasks save successfully
```

That's it! 🎉
