# Data Model: Evolution of Todo Console Application

## Task Entity

**Fields**:
- `id`: int (unique identifier, auto-incrementing integer)
- `title`: str (required, non-empty string)
- `description`: str (optional, can be empty string)
- `completed`: bool (boolean, default: False)
- `created_at`: datetime (timestamp of creation, datetime object)

**Validation Rules**:
- `id` must be unique within the current session
- `title` must be a non-empty string (1+ characters)
- `description` can be empty but must be a string if provided
- `completed` must be a boolean value
- `created_at` is automatically set when the task is created

**State Transitions**:
- `completed` can transition from False to True (incomplete to complete)
- `completed` can transition from True to False (complete to incomplete)

**Relationships**:
- No relationships with other entities (standalone entity)

**Constraints**:
- All tasks are stored in memory during runtime only
- Task IDs are unique per runtime session
- Task data is not persisted beyond application lifecycle