# API Contracts: Evolution of Todo Console Application

## Add Task Operation

**Input Parameters**:
- `title` (string, required): The title of the task (must be non-empty)
- `description` (string, optional): The description of the task (can be empty)

**Output**:
- `task` (object): The created task object with all fields including the generated ID

**Success Response**:
```
{
  "id": int,
  "title": string,
  "description": string,
  "completed": boolean,
  "created_at": datetime
}
```

**Error Conditions**:
- Title is empty or not provided
- Invalid data types provided

---

## View Tasks Operation

**Input Parameters**:
- None

**Output**:
- `tasks` (array): List of all task objects in the system

**Success Response**:
```
[
  {
    "id": int,
    "title": string,
    "description": string,
    "completed": boolean,
    "created_at": datetime
  },
  ...
]
```

**Error Conditions**:
- None (empty list returned if no tasks exist)

---

## Update Task Operation

**Input Parameters**:
- `task_id` (int, required): The ID of the task to update
- `title` (string, optional): The new title for the task
- `description` (string, optional): The new description for the task

**Output**:
- `task` (object): The updated task object

**Success Response**:
```
{
  "id": int,
  "title": string,
  "description": string,
  "completed": boolean,
  "created_at": datetime
}
```

**Error Conditions**:
- Task ID does not exist
- Invalid data types provided
- Task ID is not an integer

---

## Delete Task Operation

**Input Parameters**:
- `task_id` (int, required): The ID of the task to delete

**Output**:
- Success message confirming deletion

**Success Response**:
```
{
  "success": boolean,
  "message": string
}
```

**Error Conditions**:
- Task ID does not exist
- Task ID is not an integer

---

## Toggle Task Status Operation

**Input Parameters**:
- `task_id` (int, required): The ID of the task to toggle

**Output**:
- `task` (object): The task object with the updated completion status

**Success Response**:
```
{
  "id": int,
  "title": string,
  "description": string,
  "completed": boolean,
  "created_at": datetime
}
```

**Error Conditions**:
- Task ID does not exist
- Task ID is not an integer