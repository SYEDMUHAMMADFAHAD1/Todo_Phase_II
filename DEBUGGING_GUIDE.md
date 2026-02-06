# Frontend & Backend Debugging Guide

## Issues Fixed

### 1. ✅ CORS Header Issue (Backend)
**File**: `backend/src/main.py`
**Problem**: The CORS middleware wasn't exposing the `Authorization` header, which could cause issues with frontend JWT token handling.
**Fix**: Added `Authorization` to the `expose_headers` list.

```python
expose_headers=["Authorization", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"]
```

### 2. ✅ API URL Path Construction (Frontend)
**File**: `frontend/src/services/auth-service.ts`
**Problem**: The API base URL could have trailing slashes that might cause double slashes in URLs.
**Fix**: Added normalization to remove trailing slashes.

```typescript
const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');
```

### 3. ✅ Enhanced Error Logging (Frontend)
**Files**:
- `frontend/src/services/auth-service.ts`
- `frontend/src/components/auth/AuthForm.tsx`

**Problem**: Signup/signin fetch errors were not being logged clearly, making debugging difficult.
**Fixes**:
- Added console logs with emoji indicators to the signup and signin methods
- Added proper error handling in the form submission
- Better error messages displayed to the user

## How to Test

### Test 1: Verify Backend is Running
```bash
# Check if backend is accessible
curl http://localhost:8000/health
# Should return: {"status":"ok"}
```

### Test 2: Test Signup Flow
1. Open browser DevTools (F12)
2. Go to Console tab
3. Navigate to the signup page
4. Fill in the form:
   - Full Name: John Doe
   - Email: john@example.com
   - Password: Password123!
   - Confirm Password: Password123!
5. Click "Sign up"
6. **Check Console Output**:
   - Look for: `🔐 Signup request: { url: '...', email: '...' }`
   - Look for: `📡 Signup response status: 200`
   - Look for: `✅ Signup successful: { userId: '...' }`

If you see errors:
   - `❌ Signup error response: {...}` - Backend returned an error
   - `🚨 Signup error: ...` - Network or fetch error

### Test 3: Check Network Tab
1. Open DevTools → Network tab
2. Try to sign up
3. Find the request to `/api/auth/signup`
4. Check:
   - **Status**: Should be 200 (Success) or 409 (User exists)
   - **Headers**: Should have `Content-Type: application/json`
   - **Response**: Should contain `user`, `session`, and `token` objects

### Test 4: Check Local Storage
1. Open DevTools → Application → Local Storage
2. After successful signup, look for:
   - `todo_app_token` - Should contain your JWT token

## Common Issues & Solutions

### Issue: "Network Error" or "Failed to fetch"
**Possible Causes**:
1. Backend server is not running
2. CORS policy blocking request
3. Wrong API URL in `.env.local`

**Solutions**:
1. Start backend: `python -m backend.run_server` (or `python backend/run_server.py`)
2. Check frontend `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```
3. In DevTools Console, check if the URL is correct:
   ```javascript
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```

### Issue: "User with this email already exists" (409)
**Solution**: Use a different email address or clear the database

### Issue: "Sign up failed (500)"
**Possible Causes**:
1. Database error
2. Invalid data being sent

**Solutions**:
1. Check backend logs for detailed error message
2. Verify all required fields are being sent (email, password, name)

### Issue: Signup succeeds but not redirected to dashboard
**Possible Causes**:
1. Token not being saved to localStorage
2. AuthContext not updating state

**Check**:
```javascript
// In DevTools Console:
localStorage.getItem('todo_app_token')  // Should not be null
```

## API Endpoint Verification

### Signup Endpoint
- **URL**: `POST /api/auth/signup`
- **Backend Path**: `backend/src/api/routers/auth.py:111`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123",
    "name": "User Name"
  }
  ```
- **Success Response (200)**:
  ```json
  {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "User Name",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    },
    "session": {
      "id": "uuid_session",
      "userId": "uuid",
      "expiresAt": "timestamp",
      "createdAt": "timestamp"
    },
    "token": "jwt_token_here"
  }
  ```

### Signin Endpoint
- **URL**: `POST /api/auth/signin`
- **Backend Path**: `backend/src/api/routers/auth.py:55`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123"
  }
  ```
- **Success Response (200)**: Same as signup

## Database Check

### View Database Records
```bash
# Install sqlite3 if needed
sqlite3 backend/todo_app.db

# Query users
SELECT * FROM user;

# Query user count
SELECT COUNT(*) FROM user;
```

## Frontend Configuration

### Required Environment Variables
**File**: `frontend/.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
BETTER_AUTH_SECRET=placeholder_secret_for_spec1
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

### Backend Configuration
**File**: `backend/.env`
```
DATABASE_URL=sqlite+aiosqlite:///./todo_app.db
BETTER_AUTH_SECRET=supersecretkeyfordevonly
```

## Quick Debugging Checklist

- [ ] Backend is running (`python -m backend.run_server`)
- [ ] Frontend `.env.local` has correct `NEXT_PUBLIC_API_URL`
- [ ] Browser Console shows no CORS errors
- [ ] Network tab shows HTTP 200 response
- [ ] `localStorage.getItem('todo_app_token')` returns a value
- [ ] Database file exists (`backend/todo_app.db`)
- [ ] User appears in database after signup

## Next Steps

If everything is working:
1. Test signin with newly created credentials
2. Verify JWT token is being stored and sent with requests
3. Test accessing protected routes (dashboard)
4. Test task CRUD operations
