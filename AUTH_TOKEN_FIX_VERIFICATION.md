# Auth Token Flow Fix - Verification Guide

## 🎯 What Was Fixed

**Problem:** Frontend stored JWT token in localStorage but browser requests never attached it, causing 401 Unauthorized on protected endpoints (GET/POST /tasks).

**Root Cause:** Race condition between token storage and axios interceptor initialization.

**Solution:** Synchronous token storage + fresh localStorage check on every request.

---

## ✅ Step-by-Step Verification

### 1. Start the Backend
```bash
cd backend
python run_server.py
# Or: uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify backend is running:**
- Open http://localhost:8000/health
- Should return: `{"status":"ok"}`

---

### 2. Start the Frontend
```bash
cd frontend
npm run dev
# Frontend will run on http://localhost:3000
```

---

### 3. Test 1: Sign Up

**URL:** http://localhost:3000/signup

**Steps:**
1. Fill in email (e.g., `test@example.com`)
2. Fill in password (e.g., `password123`)
3. Click "Sign Up"

**Expected Behavior:**
- ✅ Signup succeeds
- ✅ User email appears in navbar
- ✅ Redirects to dashboard (`/`)
- ✅ **NO error messages**

**Check in DevTools (F12):**
1. Open **Network** tab
2. Find the POST `/api/auth/signup` request
3. Check the response: should have `token`, `user`, `session`
4. Open **Storage → LocalStorage → http://localhost:3000**
5. Verify `todo_app_token` exists and contains a JWT (long base64 string)

---

### 4. Test 2: Fetch Tasks (After Signup)

**Expected Behavior:**
- ✅ Tasks list loads (even if empty)
- ✅ NO "Unauthorized" error
- ✅ Can see task creation form

**Check in DevTools (F12):**
1. Open **Network** tab
2. Find the GET `/api/tasks` request
3. Click on it → **Headers** tab
4. Scroll to **Request Headers**
5. **CRITICAL CHECK:** Should see:
   ```
   Authorization: Bearer eyJhbGci...
   ```
   If you see `Authorization: Bearer` without a token, the fix didn't work.

6. Check the **Response** tab
7. Should be an empty list `[]` or list of tasks

---

### 5. Test 3: Create a Task

**Steps:**
1. After signup, on the dashboard
2. Enter a task title in the input field
3. Click "Add Task"

**Expected Behavior:**
- ✅ Task is created successfully
- ✅ Task appears in the list immediately
- ✅ NO "Unauthorized" error

**Check in DevTools (F12):**
1. Open **Network** tab
2. Find the POST `/api/tasks` request
3. **Request Headers** should have:
   ```
   Authorization: Bearer eyJhbGci...
   Content-Type: application/json
   ```
4. **Response** should be the newly created task object with an `id`

---

### 6. Test 4: Sign Out and Sign In

**Sign Out:**
1. Click user menu (email in navbar)
2. Click "Sign Out"

**Expected Behavior:**
- ✅ Redirected to `/signin`
- ✅ `todo_app_token` removed from localStorage

**Sign In:**
1. Enter email and password from signup
2. Click "Sign In"

**Expected Behavior:**
- ✅ Sign in succeeds
- ✅ Email appears in navbar
- ✅ Can fetch tasks
- ✅ New token in localStorage

---

## 🔍 Deep Dive: Console Logs

Open **DevTools → Console** (F12 → Console tab)

You should see logs like:
```
🔐 Authorization header attached: { token: 'eyJhbGciOiJIUzI1NiIs...' }
✅ Token stored in localStorage
✅ Signin successful
```

**If you DON'T see the Authorization header log:**
- Token wasn't attached
- Fix didn't work
- Check localStorage manually

---

## 🐛 Troubleshooting

### ❌ Getting "Unauthorized" on task fetch?

1. **Check token exists in localStorage:**
   - DevTools → Storage → LocalStorage → http://localhost:3000
   - Look for `todo_app_token`
   - If missing: Sign up again

2. **Check token is attached to request:**
   - DevTools → Network
   - Click GET `/api/tasks`
   - Headers section → look for `Authorization: Bearer ...`
   - If missing: Browser cache issue, clear and restart

3. **Check backend is accepting the token:**
   - Open http://localhost:8000/docs (Swagger UI)
   - Try to authenticate with the token in the UI
   - If fails: Backend token verification issue

### ❌ Getting CORS errors?

**Error:** `Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution:**
1. Check `backend/src/main.py` CORS config
2. Verify `allow_origins` includes `http://localhost:3000`
3. Restart backend server

### ❌ Getting "Network Error" in browser?

1. Verify backend is running: http://localhost:8000/health
2. Check `NEXT_PUBLIC_API_URL` env var in frontend:
   - Should be `http://localhost:8000/api` or `http://localhost:8000/api/`
   - Check `frontend/.env.local` or `frontend/.env`
3. Restart frontend

---

## 📊 Expected Flow Diagram

```
User clicks "Sign Up"
        ↓
Frontend: fetch POST /api/auth/signup
        ↓
Backend: Create user + return token
        ↓
Frontend: Store token in localStorage SYNCHRONOUSLY
        ↓
Frontend: Update UI (show email)
        ↓
User navigates to dashboard
        ↓
Frontend: fetch GET /api/tasks
        ↓
Axios Interceptor: Check localStorage for token
        ↓
Axios Interceptor: Attach "Authorization: Bearer <token>"
        ↓
Backend: get_current_user verifies JWT
        ↓
Backend: Return user's tasks
        ↓
Frontend: Display tasks ✅
```

---

## 🎯 Commit Info

```
Commit: 411f149
Message: Fix: Resolve browser auth token flow race condition

Files Changed:
- backend/src/main.py (CORS config)
- frontend/src/lib/api-client.ts (Interceptor fix)
- frontend/src/services/auth-service.ts (Synchronous token storage)
```

---

## ✨ Key Changes Summary

### Before (Broken)
```typescript
// ❌ Race condition: Async import delays interceptor
import('@/lib/api-client').then(({ apiClient }) => {
  apiClient.setAuthToken(authResponse.token);
});
// Meanwhile, next request fires with NO token
```

### After (Fixed)
```typescript
// ✅ Synchronous: Token stored immediately
localStorage.setItem('todo_app_token', authResponse.token);
// Next request will find token in localStorage
```

---

## 📝 Testing Checklist

- [ ] Backend health check passes (http://localhost:8000/health)
- [ ] Frontend starts without errors (http://localhost:3000)
- [ ] Can sign up new user
- [ ] User email appears in navbar after signup
- [ ] GET /tasks request has Authorization header
- [ ] Tasks list loads successfully
- [ ] Can create a new task
- [ ] POST /tasks request has Authorization header
- [ ] New task appears in list immediately
- [ ] Sign out removes localStorage token
- [ ] Can sign in with same email/password
- [ ] Tasks still load after sign in
- [ ] Console shows `🔐 Authorization header attached` logs

---

All tests passing? 🎉 Auth token flow is FIXED!
