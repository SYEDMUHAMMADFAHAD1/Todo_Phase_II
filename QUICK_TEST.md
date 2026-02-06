# Quick Test & Run Guide

## Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- Both servers running simultaneously

## Step 1: Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Option 1: Using Python directly
python -m backend.run_server

# Option 2: Using the run script (Windows)
python run_backend.py

# Option 3: Using the batch file (Windows)
start_backend.bat
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Test Backend is Running:**
```bash
# In another terminal
curl http://localhost:8000/health
# Should return: {"status":"ok"}
```

## Step 2: Start Frontend Development Server

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 16.0.0
  - Local:        http://localhost:3000
  - Environments: .env.local
```

## Step 3: Test Signup Flow

### Manual Testing
1. Open browser to `http://localhost:3000`
2. Click "Create your account" or navigate to `/signup`
3. Fill in:
   - **Full Name**: John Doe
   - **Email**: john@example.com
   - **Password**: Password123
   - **Confirm Password**: Password123
4. Click "Sign up"

### Expected Results
- ✅ No errors in browser console
- ✅ Redirected to dashboard
- ✅ User data visible on dashboard
- ✅ Token stored in localStorage

### Debugging with Console
Open DevTools (F12) and check Console tab:

```javascript
// Check API URL
console.log(process.env.NEXT_PUBLIC_API_URL)
// Output: http://localhost:8000/api

// Check token after signup
localStorage.getItem('todo_app_token')
// Output: eyJ0eXAiOiJKV1QiLCJhbGc... (long string)

// Check user data
sessionStorage.getItem('user')
// Output: {"id":"xxx","email":"john@example.com",...}
```

## Step 4: Test Signin Flow

1. Sign out (if already signed in)
2. Click "Sign in to your account" or navigate to `/signin`
3. Enter:
   - **Email**: john@example.com
   - **Password**: Password123
4. Click "Sign in"

### Expected Results
- ✅ Successfully authenticated
- ✅ Redirected to dashboard
- ✅ Tasks page loads

## Step 5: View Console Logs

**Signup Console Output Example:**
```
🔐 Signup request: {url: "http://localhost:8000/api/auth/signup", email: "john@example.com"}
📡 Signup response status: 200
✅ Signup successful: {userId: "550e8400-e29b-41d4-a716-446655440000"}
```

**If there's an error:**
```
🔐 Signup request: {url: "http://localhost:8000/api/auth/signup", email: "john@example.com"}
📡 Signup response status: 409
❌ Signup error response: {detail: "User with this email already exists"}
🚨 Signup error: User with this email already exists
```

## Network Tab Inspection

1. Open DevTools → Network tab
2. Attempt signup
3. Look for POST request to `/api/auth/signup`
4. Click on the request and check:

**Request Headers:**
```
POST /api/auth/signup HTTP/1.1
Host: localhost:8000
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "Password123",
  "name": "John Doe"
}
```

**Response Headers (Success):**
```
HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
```

**Response Body:**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "name": "John Doe",
    "createdAt": "2026-01-26T10:30:45",
    "updatedAt": "2026-01-26T10:30:45"
  },
  "session": {
    "id": "550e8400-e29b-41d4-a716-446655440000_session",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "expiresAt": "1706274645.123456",
    "createdAt": "1706273445.123456"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Mac/Linux

# Kill the process if needed
taskkill /PID <PID> /F         # Windows
kill -9 <PID>                   # Mac/Linux
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "Cannot find module" errors
```bash
# Ensure all dependencies are installed
npm install
# or in backend
pip install -r requirements.txt
```

### Database errors
```bash
# Remove old database and let it recreate
rm backend/todo_app.db
# Restart backend
python -m backend.run_server
```

### CORS errors in browser
```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/signup'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution**:
- Ensure backend is running
- Check CORS middleware in `backend/src/main.py` (already fixed)
- Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`

## Success Indicators

✅ All working correctly when:
1. Backend responds to health check
2. Frontend loads without errors
3. Network requests show 200 status codes
4. Console shows emoji logs (🔐 🔐 ✅)
5. Token appears in localStorage
6. User is redirected to dashboard
7. Dashboard displays user info and task list

## Files Modified in This Session

1. ✅ `backend/src/main.py` - Fixed CORS headers
2. ✅ `frontend/src/services/auth-service.ts` - Added error logging and URL normalization
3. ✅ `frontend/src/components/auth/AuthForm.tsx` - Enhanced error handling
