# 🧪 Browser Testing Guide - Auth Token Flow

This guide shows you EXACTLY what to look for in your browser to verify the fix works.

---

## 🚀 Quick Start

### 1. Start Both Servers
```bash
# Terminal 1 - Backend
cd backend
python run_server.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Open Browser DevTools
- Chrome/Edge: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Shift+I` (Mac)
- Firefox: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Shift+I` (Mac)

---

## 📱 Test 1: Sign Up Flow

### Steps:
1. Navigate to http://localhost:3000/signup
2. Enter email: `test@example.com`
3. Enter password: `password123`
4. Click "Sign Up" button

### What You Should See:

#### ✅ Console Log (F12 → Console)
```
🔐 Signin request: {url: 'http://localhost:8000/api/auth/signin', email: 'test@example.com'}
✅ Signin successful
✅ Token stored in localStorage
🔐 Authorization header attached: { token: 'eyJhbGciOiJIUzI1NiIsInR...' }
```

#### ✅ Network Tab (F12 → Network)
Look for `signup` or `signin` request:

**Request:**
```
POST /api/auth/signup HTTP/1.1
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "name": "",
    "createdAt": "1706...",
    "updatedAt": "1706..."
  },
  "session": {
    "id": "550e8400-e29b-41d4-a716-446655440000_session",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "expiresAt": "1706...",
    "createdAt": "1706..."
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### ✅ Storage (F12 → Storage → LocalStorage)
Look for `http://localhost:3000`:
```
Key: todo_app_token
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**The token value should be a long string starting with `eyJ...`**

#### ✅ UI
- Email should appear in top-right navbar
- Should redirect to dashboard (/)
- Tasks section should load

---

## 📊 Test 2: Fetch Tasks (The Critical One)

After signup, you should be on the dashboard. Now we'll check if the Authorization header is attached.

### Steps:
1. Open DevTools (F12)
2. Go to Network tab
3. Refresh the page (Ctrl+R)
4. Look for a request that contains "tasks"

### What You Should See:

#### ✅ Request URL and Method
```
GET /api/tasks HTTP/1.1
```

#### ✅ Request Headers (CRITICAL - THIS IS THE FIX)
Scroll down in the Headers section:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJuYW1lIjoiIiwgZXhwIjoxNjk5OTk5OTk5fQ.xxx
Content-Type: application/json
```

**IF YOU DON'T SEE THE AUTHORIZATION HEADER → THE FIX DIDN'T WORK**

#### ✅ Response Status
```
200 OK
```

#### ✅ Response Body
```json
[
  {
    "id": "...",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Example task",
    "completed": false,
    "created_at": "...",
    "updated_at": "..."
  }
]
```

Or empty array `[]` if no tasks yet.

---

## ➕ Test 3: Create Task

### Steps:
1. On dashboard, enter task title in the input field
2. Click "Add Task" button
3. Task should appear in the list

### What You Should See:

#### ✅ Network Tab
Look for `tasks` POST request:

**Request:**
```
POST /api/tasks HTTP/1.1
Authorization: Bearer eyJhbGciOi...
Content-Type: application/json

{
  "title": "Buy groceries",
  "completed": false
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "completed": false,
  "created_at": "1706...",
  "updated_at": "1706..."
}
```

#### ✅ UI
- New task appears immediately in the list
- No error message
- Input field clears

---

## 🔄 Test 4: Sign Out & Sign In

### Sign Out Steps:
1. Click email in navbar (top-right)
2. Click "Sign Out"

### What You Should See:

#### ✅ Storage (F12 → Storage → LocalStorage)
- `todo_app_token` should be **GONE**

#### ✅ UI
- Redirected to `/signin` page
- Email removed from navbar

### Sign In Steps:
1. Enter the email: `test@example.com`
2. Enter the password: `password123`
3. Click "Sign In"

### What You Should See:

#### ✅ Console
```
🔐 Authorization header attached: { token: 'eyJhbGciOiJIUzI1NiIsInR...' }
```

#### ✅ Storage
- `todo_app_token` is back in localStorage

#### ✅ UI
- Email appears in navbar
- Tasks list loads
- Can create new tasks

---

## 🐛 Troubleshooting: Common Issues

### Issue 1: No Authorization Header
**What you see:** Network tab shows GET /tasks with NO Authorization header

**Cause:** Token not in localStorage or interceptor not working

**Fix:**
1. Check Storage tab: Is `todo_app_token` there?
   - NO → Sign up again
   - YES → Hard refresh (Ctrl+Shift+R)
2. Check console for errors
3. Clear browser cache and restart

### Issue 2: 401 Unauthorized Response
**What you see:** GET /tasks returns 401 status

**Network Response:**
```json
{
  "detail": "Missing authentication credentials",
  "headers": {"WWW-Authenticate": "Bearer"}
}
```

**Cause:** Authorization header not being sent

**Fix:**
1. Check Network tab → Request Headers → Is Authorization header there?
   - NO → Check browser cache (Ctrl+Shift+R)
   - YES → Token might be expired, sign out and sign in again

### Issue 3: CORS Error
**What you see:** Console error about CORS

**Error message:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Cause:** Backend CORS config not including localhost:3000

**Fix:**
1. Check `backend/src/main.py` CORS config
2. Ensure `allow_origins` includes `http://localhost:3000`
3. Restart backend server

### Issue 4: 500 Internal Server Error
**What you see:** GET /tasks returns 500

**Cause:** Backend error (not related to auth)

**Fix:**
1. Check backend terminal for error logs
2. Verify database is initialized: `python initialize_db.py`
3. Restart backend

### Issue 5: Infinite Loop / Redirect Loop
**What you see:** Page keeps redirecting

**Cause:** Token validation failing

**Fix:**
1. Clear localStorage: DevTools → Storage → LocalStorage → right-click `todo_app_token` → Delete
2. Sign out
3. Clear browser cache
4. Try signup again

---

## 📋 Browser DevTools Cheat Sheet

### Storage Tab (See localStorage)
```
F12 → Application (Chrome/Edge) or Storage (Firefox)
→ LocalStorage
→ http://localhost:3000
```

### Network Tab (See API requests)
```
F12 → Network
→ Refresh page or make action
→ Click on request (e.g., "tasks")
→ Headers tab → see Authorization header
```

### Console Tab (See logs)
```
F12 → Console
→ Should see logs like:
   🔐 Authorization header attached
   ✅ Token stored in localStorage
```

### Application/Cache (Clear cache)
```
F12 → Application/Storage
→ Service Workers
→ Unregister Service Worker
→ Or: Right-click page → Clear browsing data
```

---

## ✅ Complete Test Checklist

Mark these off as you test:

- [ ] Can sign up with email/password
- [ ] Email appears in navbar after signup
- [ ] localStorage contains `todo_app_token`
- [ ] GET /tasks has Authorization header with Bearer token
- [ ] GET /tasks returns 200 OK (not 401)
- [ ] Tasks list appears on dashboard
- [ ] Can create new task
- [ ] POST /tasks has Authorization header
- [ ] POST /tasks returns 201 Created
- [ ] New task appears in list immediately
- [ ] Can mark task as done
- [ ] PUT /tasks/{id} has Authorization header
- [ ] Can delete task
- [ ] DELETE /tasks/{id} has Authorization header
- [ ] Can sign out (token removed from storage)
- [ ] Can sign in with same credentials
- [ ] Tasks still load after sign in
- [ ] Console shows authorization logs (🔐)
- [ ] No 401 Unauthorized errors
- [ ] No CORS errors

---

## 🎯 The One Thing to Verify

**IF YOU ONLY HAVE TIME FOR ONE CHECK:**

1. Open DevTools (F12)
2. Go to Network tab
3. Refresh page
4. Find GET `/api/tasks` request
5. Click on it
6. Go to Headers tab
7. Look for this line:
   ```
   Authorization: Bearer eyJhbGciOi...
   ```

**If you see it → THE FIX WORKS** ✅

**If you don't see it → There's still an issue** ❌

---

## 📞 Need Help?

1. Check `AUTH_FIX_SUMMARY.md` for technical details
2. Check `AUTH_TOKEN_FIX_VERIFICATION.md` for step-by-step verification
3. Look at console logs and network requests
4. Check backend logs in terminal

---

**Now go test it! 🚀**
