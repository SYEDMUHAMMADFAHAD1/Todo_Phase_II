import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str | None = None
    password: str  # In a real app, this would be hashed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskBase(SQLModel):
    title: str = Field(max_length=255)
    description: str | None = None
    is_completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(sa_column_kwargs={"name": "user_id"}, index=True)  # Database field name
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def owner_id(self) -> str:
        """Property to access user_id as owner_id for internal compatibility."""
        return self.user_id


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None


class TaskRead(TaskBase):
    id: str  # Convert UUID to string for API
    user_id: str  # This will be populated from user_id
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        """Custom method to create TaskRead from Task with proper field mapping."""
        return cls(
            title=obj.title,
            description=obj.description,
            is_completed=obj.is_completed,
            id=str(obj.id),  # Convert UUID to string
            user_id=obj.user_id,  # Map user_id to user_id
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )
