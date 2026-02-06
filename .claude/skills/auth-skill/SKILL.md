---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill – Secure Authentication

## Instructions

1. **User Signup**
   - Validate user input (email, password, username)
   - Hash passwords securely before storing
   - Prevent duplicate accounts
   - Store user records in the database

2. **User Signin**
   - Verify user credentials
   - Compare hashed passwords
   - Handle invalid login attempts gracefully
   - Return authentication tokens on success

3. **Password Security**
   - Use strong hashing algorithms (bcrypt, argon2)
   - Apply salting automatically
   - Never store plain-text passwords
   - Enforce minimum password strength

4. **JWT Token Management**
   - Generate access tokens on login
   - Use secure secret keys
   - Set token expiration
   - Verify tokens for protected routes
   - Support refresh tokens if required

5. **Better Auth Integration**
   - Configure Better Auth providers
   - Handle OAuth or credentials-based auth
   - Manage sessions securely
   - Sync user data with database
   - Handle callbacks and redirects

---

## Best Practices
- Always hash passwords before saving
- Use HTTPS in production
- Store secrets in environment variables
- Apply rate limiting on auth endpoints
- Implement proper error messages (avoid leaking details)
- Protect routes using middleware
- Follow OWASP authentication guidelines

---

## Example Structure

```ts
// Signup Example
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

export async function signup(req, res) {
  const { email, password } = req.body;

  const hashedPassword = await bcrypt.hash(password, 12);

  const user = await db.user.create({
    email,
    password: hashedPassword,
  });

  res.status(201).json({ message: "User created successfully" });
}
