# Authentication Flow Diagram

## Sign Up Flow

```
Frontend (http://localhost:3000)          Backend (http://localhost:8000)
         │                                          │
         │ 1. User visits /auth/signup              │
         ├─────────────────────────────────────────→│
         │                                          │
         │ 2. Fills form with email, password, name │
         │                                          │
         │ 3. Frontend validates:                   │
         │    ✓ Email format                        │
         │    ✓ Password length (8+ chars)          │
         │    ✓ Passwords match                     │
         │                                          │
         │ 4. Send POST /api/auth/signup            │
         ├─────────────────────────────────────────→│
         │    {email, password, name}               │
         │                                          │
         │                            ┌─────────────▼──────────┐
         │                            │ Backend Processing:    │
         │                            │ 1. Check duplicate     │
         │                            │ 2. Hash password       │
         │                            │ 3. Create user in DB   │
         │                            │ 4. Generate JWT token  │
         │                            │ 5. Return user + token │
         │                            └─────────────┬──────────┘
         │                                          │
         │ 5. Receive response:                     │
         │←─────────────────────────────────────────┤
         │ {user, session, token}                   │
         │                                          │
         │ 6. Store token in localStorage           │
         │ 7. Update AuthContext                    │
         │ 8. Redirect to dashboard                 │
         └─────────────────────────────────────────→
             ✅ User signed up and logged in
```

---

## Login Flow

```
Frontend (http://localhost:3000)          Backend (http://localhost:8000)
         │                                          │
         │ 1. User visits /auth/signin              │
         ├─────────────────────────────────────────→│
         │                                          │
         │ 2. Fills form with email and password    │
         │                                          │
         │ 3. Frontend validates form               │
         │                                          │
         │ 4. Send POST /api/auth/signin            │
         ├─────────────────────────────────────────→│
         │    {email, password}                     │
         │                                          │
         │                            ┌─────────────▼──────────┐
         │                            │ Backend Processing:    │
         │                            │ 1. Find user by email  │
         │                            │ 2. Verify password     │
         │                            │ 3. Generate new JWT    │
         │                            │ 4. Return user + token │
         │                            └─────────────┬──────────┘
         │                                          │
         │ 5. Receive response:                     │
         │←─────────────────────────────────────────┤
         │ {user, session, token}                   │
         │                                          │
         │ 6. Store token in localStorage           │
         │ 7. Update AuthContext                    │
         │ 8. Redirect to dashboard                 │
         └─────────────────────────────────────────→
             ✅ User logged in successfully
```

---

## Protected Route Access

```
Frontend (http://localhost:3000)          Backend (http://localhost:8000)
         │                                          │
         │ 1. User accesses protected resource      │
         │                                          │
         │ 2. Get token from localStorage           │
         │    token = "eyJhbGciOiJIUzI1NiIs..."    │
         │                                          │
         │ 3. Send request with token:              │
         │    GET /api/auth/session                 │
         ├─────────────────────────────────────────→│
         │    Headers:                              │
         │    Authorization: Bearer {token}         │
         │                                          │
         │                            ┌─────────────▼──────────┐
         │                            │ Backend Validation:    │
         │                            │ 1. Extract token       │
         │                            │ 2. Verify signature    │
         │                            │ 3. Check expiration    │
         │                            │ 4. Extract user ID     │
         │                            │ 5. Get user from DB    │
         │                            └─────────────┬──────────┘
         │                                          │
         │ ✅ Token Valid                           │
         │←─────────────────────────────────────────┤
         │ {user, session}                          │
         │ Status: 200 OK                           │
         │                                          │
         │ 4. Render protected content              │
         └─────────────────────────────────────────→
             ✅ Access granted
```

---

## Unauthorized Access Attempt

```
Frontend (http://localhost:3000)          Backend (http://localhost:8000)
         │                                          │
         │ 1. User tries to access protected route  │
         │    (without valid token)                 │
         │                                          │
         │ 2. No token in localStorage              │
         │    (or token expired)                    │
         │                                          │
         │ 3. Send request without token:           │
         │    GET /api/auth/session                 │
         ├─────────────────────────────────────────→│
         │    (No Authorization header)             │
         │                                          │
         │                            ┌─────────────▼──────────┐
         │                            │ Backend Validation:    │
         │                            │ 1. Look for token      │
         │                            │ 2. Token not found     │
         │                            │ ❌ DENY ACCESS         │
         │                            └─────────────┬──────────┘
         │                                          │
         │ ❌ Unauthorized                          │
         │←─────────────────────────────────────────┤
         │ {detail: "Not authenticated"}            │
         │ Status: 403 Forbidden                    │
         │                                          │
         │ 4. Clear token from storage              │
         │ 5. Redirect to /auth/signin              │
         │ 6. Show error message                    │
         └─────────────────────────────────────────→
             ✅ Properly redirected to login
```

---

## JWT Token Structure

```
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
       eyJzdWIiOiJiOGRiNjBhMC0wMWNjLTQ3ZGYtODlmYy1lMzFiZWI3ZmY3ZjQiLCJl
       bWFpbCI6InRlc3R1c2VyQGV4YW1wbGUuY29tIiwibmFtZSI6IlRlc3QgVXNlciIs
       ImV4cCI6MTc2OTA3MTc5OS44MDQzOTM1fQ.
       _OOfhgjfnQr8fNzE3vVUOJlKrads-987xr8gTcfJhno

Decoded Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Decoded Payload:
{
  "sub": "b8db60a0-01cc-47df-89fc-e31beb7ff7f4",  // User ID
  "email": "testuser@example.com",                 // User email
  "name": "Test User",                             // User name
  "exp": 1769071799.8043935                        // Expiration time (30 mins)
}

Signature: Generated using HS256 + SECRET_KEY
```

---

## Database Schema

### Users Table
```
user
├── id (UUID) - Primary Key
├── email (String, UNIQUE) - User email address
├── name (String) - User display name
├── password (String) - Bcrypt hashed password
├── created_at (DateTime) - Account creation time
└── updated_at (DateTime) - Last update time
```

---

## Authentication Flow Summary

### Step-by-Step Process

1. **User Registration**
   - User fills signup form
   - Frontend validates input
   - Backend creates user with hashed password
   - JWT token generated automatically
   - User logged in and redirected to dashboard

2. **User Login**
   - User enters credentials
   - Backend verifies password against hash
   - JWT token issued
   - Token stored in frontend localStorage
   - User redirected to dashboard

3. **Accessing Protected Resources**
   - Frontend includes JWT in Authorization header
   - Backend validates token signature
   - Backend checks token expiration
   - If valid: grant access to resource
   - If invalid: return 403 Forbidden

4. **Token Storage**
   - Stored in browser localStorage
   - Persists across page reloads
   - Automatically included in API requests
   - Cleared on logout

---

## Security Features

✅ **Password Security**
- Bcrypt hashing with salt
- Passwords never stored in plain text
- Password verification on every login

✅ **Token Security**
- JWT with HS256 algorithm
- 30-minute expiration time
- Signature verification on every request
- Cannot be tampered with without secret key

✅ **Access Control**
- Token required for protected routes
- User can only access own data
- Proper HTTP status codes (401, 403)

✅ **Error Handling**
- Generic error messages (no user enumeration)
- Proper logging for debugging
- Graceful degradation on failure

---

## Frontend Implementation

### AuthContext
- Manages authentication state globally
- Provides user, session, and loading state
- Methods: signUp, signIn, signOut, refreshSession

### useAuth Hook
- Custom hook to access AuthContext
- Available in any component
- Returns auth functions and state

### Protected Routes
- Redirect to login if not authenticated
- Check token validity before rendering
- Clear token on 401 responses

### Token Management
- Store token in localStorage
- Include in every API request
- Clear on logout or expiration

---

## Backend Implementation

### Authentication Endpoints
- POST /api/auth/signup - Create account
- POST /api/auth/signin - Login
- GET /api/auth/session - Get current session (protected)
- POST /api/auth/signout - Logout

### Authentication Middleware
- Extract token from Authorization header
- Verify JWT signature
- Check token expiration
- Return user identity if valid
- Return 403 if invalid/missing

### Password Handling
- Hash on registration
- Verify on login
- Never log or expose passwords

---

## Testing Results

All 8 tests passed successfully:

✅ Signup with new user
✅ Login with valid credentials
✅ Access protected endpoint with token
✅ Deny access without token
✅ Logout functionality
✅ Duplicate email prevention
✅ Wrong password rejection
✅ Non-existent user handling

---

**Authentication System: Fully Operational ✅**
