# Data Model

## Overview

The application uses **Neon Serverless PostgreSQL** as the primary data store. The schema is accessed via **SQLModel** (Python Backend) and **Better Auth** (Next.js Frontend / Node).

## Entities

### 1. User (Managed by Better Auth)
The `user` table is created and managed by the Better Auth library. The backend treats this as the source of truth for user identity.

*   **Table Name**: `user`
*   **Fields**:
    *   `id` (Text, PK): Unique User ID.
    *   `email` (Text, Unique): User email.
    *   `name` (Text): Display name.
    *   `emailVerified` (Boolean): Verification status.
    *   `image` (Text): Avatar URL.
    *   `createdAt` (Timestamp): Creation time.
    *   `updatedAt` (Timestamp): Update time.

### 2. Task (Managed by Backend)
The `task` table stores the user's todo items.

*   **Table Name**: `task`
*   **Fields**:
    *   `id` (UUID, PK): Unique Task identifier.
    *   `title` (Text, NOT NULL): Task title (max 255 chars).
    *   `description` (Text, NULL): Optional details.
    *   `is_completed` (Boolean, Default False): Status.
    *   `user_id` (Text, NOT NULL, FK): Foreign Key to `user.id`.
    *   `created_at` (Timestamp, Default Now): Creation time.
    *   `updated_at` (Timestamp, Default Now): Last update time.

## Relationships

*   **User -> Tasks**: One-to-Many.
*   **Task -> User**: Many-to-One.
*   **Constraint**: `user_id` in `task` table MUST reference a valid `id` in `user` table.

## Python Wrappers (SQLModel)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = None
    is_completed: bool = False

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True) # FK to User
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
```
