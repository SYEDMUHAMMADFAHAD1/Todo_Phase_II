---
name: backend-skill
description: Generate backend routes, handle HTTP requests/responses, and connect applications to databases securely and efficiently.
---

# Backend Skill – Routes, Requests & Database

## Instructions

1. **Route generation**
   - Create RESTful API routes (GET, POST, PUT, DELETE)
   - Follow clean and consistent URL naming conventions
   - Group routes by feature or resource

2. **Request & response handling**
   - Parse request body, params, and query strings
   - Validate incoming data before processing
   - Return standardized JSON responses
   - Handle success and error states properly

3. **Database integration**
   - Connect to database (SQL or NoSQL)
   - Perform CRUD operations
   - Use environment variables for credentials
   - Handle connection errors and retries

4. **Middleware usage**
   - Authentication and authorization
   - Input validation
   - Error handling middleware
   - Logging and request tracking

## Best Practices
- Keep controllers thin and reusable
- Use services or repositories for business logic
- Never expose sensitive data in responses
- Use async/await with proper error handling
- Follow separation of concerns
- Secure endpoints with authentication where required

## Example Structure
```ts
// routes/user.routes.ts
import express from "express";
import { createUser, getUsers } from "../controllers/user.controller";

const router = express.Router();

router.post("/users", createUser);
router.get("/users", getUsers);

export default router;
