# Data Model: MCP Server & AI Task Tools Integration

## Entities

### Task (Existing)
**Description**: Represents a user's todo item with title, description, completion status, user ownership, and timestamps

**Fields**:
- id: UUID (Primary Key) - Unique identifier for the task
- title: String (Required, Max 255 chars) - The task title
- description: String (Optional) - Detailed description of the task
- is_completed: Boolean - Whether the task has been completed
- user_id: String (Foreign Key) - ID of the user who owns this task
- created_at: DateTime - Timestamp when the task was created
- updated_at: DateTime - Timestamp when the task was last updated

**Validation Rules**:
- title must not be empty
- user_id must correspond to an existing user
- created_at must be in the past
- updated_at must be >= created_at

**Relationships**:
- Belongs to User (via user_id foreign key)

### User (Existing)
**Description**: The authenticated entity that owns tasks and performs operations

**Fields**:
- id: String - Unique user identifier (from Better Auth)
- email: String - User's email address
- created_at: DateTime - When the user account was created
- updated_at: DateTime - When the user account was last updated

**Validation Rules**:
- email must be a valid email format
- id must be unique

**Relationships**:
- One-to-many with Task (one user has many tasks)

## MCP Tool Schemas

### AddTaskParams
**Description**: Parameters for the add_task MCP tool

**Fields**:
- title: String (Required) - The title of the task to create
- description: String (Optional) - The description of the task to create

**Validation Rules**:
- title must not be empty
- title length must be <= 255 characters

### AddTaskResult
**Description**: Result returned by the add_task MCP tool

**Fields**:
- success: Boolean - Whether the operation was successful
- task_id: String (Optional) - The ID of the created task if successful
- error: String (Optional) - Error message if the operation failed

### ListTasksParams
**Description**: Parameters for the list_tasks MCP tool

**Fields**:
- filter: String (Optional, Enum: 'all', 'pending', 'completed') - Filter for task status

**Validation Rules**:
- filter must be one of 'all', 'pending', or 'completed' if provided

### ListTasksResult
**Description**: Result returned by the list_tasks MCP tool

**Fields**:
- success: Boolean - Whether the operation was successful
- tasks: Array<Task> - List of tasks matching the filter
- error: String (Optional) - Error message if the operation failed

### UpdateTaskParams
**Description**: Parameters for the update_task MCP tool

**Fields**:
- task_id: String (Required) - The ID of the task to update
- title: String (Optional) - New title for the task
- description: String (Optional) - New description for the task

**Validation Rules**:
- task_id must not be empty
- If provided, title length must be <= 255 characters

### UpdateTaskResult
**Description**: Result returned by the update_task MCP tool

**Fields**:
- success: Boolean - Whether the operation was successful
- task: Task (Optional) - The updated task if successful
- error: String (Optional) - Error message if the operation failed

### CompleteTaskParams
**Description**: Parameters for the complete_task MCP tool

**Fields**:
- task_id: String (Required) - The ID of the task to mark as completed

**Validation Rules**:
- task_id must not be empty

### CompleteTaskResult
**Description**: Result returned by the complete_task MCP tool

**Fields**:
- success: Boolean - Whether the operation was successful
- task: Task (Optional) - The completed task if successful
- error: String (Optional) - Error message if the operation failed

### DeleteTaskParams
**Description**: Parameters for the delete_task MCP tool

**Fields**:
- task_id: String (Required) - The ID of the task to delete

**Validation Rules**:
- task_id must not be empty

### DeleteTaskResult
**Description**: Result returned by the delete_task MCP tool

**Fields**:
- success: Boolean - Whether the operation was successful
- error: String (Optional) - Error message if the operation failed

## State Transitions

### Task Lifecycle
1. **Creation**: New task created with is_completed = false
2. **Active**: Task exists but not completed
3. **Completed**: Task marked as completed (is_completed = true)
4. **Deleted**: Task removed from the system

## Database Constraints

1. **Foreign Key Integrity**: All foreign key relationships enforced at database level
2. **User Isolation**: Queries must always filter by authenticated user_id to prevent cross-user access
3. **Ownership Validation**: All operations must verify that the requesting user owns the task being operated on

## Indexing Strategy

1. **tasks.user_id**: Index for efficient user-specific queries
2. **tasks.is_completed**: Index for filtering by completion status
3. **tasks.user_id_is_completed**: Composite index for efficient queries that filter by both user and completion status