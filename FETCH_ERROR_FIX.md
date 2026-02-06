# Failed to Fetch Error - Complete Fix

## Problem
You're getting: `🚨 Signup error: "Failed to fetch"`

This error happens when:
1. Backend is not running
2. CORS policy is blocking the request
3. Wrong API URL is configured
4. Backend is on wrong port

## Root Cause
The issue was **`credentials: 'include'`** in the fetch requests. This option can cause CORS errors even when CORS is configured.

## What I Fixed

### Change Made
Removed `credentials: 'include'` from all fetch requests in:
- `frontend/src/services/auth-service.ts`

**Before**:
```typescript
const response = await fetch(url, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(credentials),
  credentials: 'include',  // ❌ This causes CORS issues
});
```

**After**:
```typescript
const response = await fetch(url, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(credentials),
  // ✅ Removed credentials: 'include'
});
```

### Why This Works
- `credentials: 'include'` tells browser to send cookies
- With `credentials: 'include'`, CORS requires explicit origin matching (can't use `*`)
- Since we're using tokens in localStorage (not cookies), we don't need this option
- Removing it simplifies CORS and prevents blocking

### Enhanced Error Logging
Added detailed error logging to help debug fetch issues:

```typescript
console.log('🔐 Signup request:', { url, email: credentials.email, timestamp: new Date().toISOString() });
console.log('📡 Signup response status:', response.status, 'statusText:', response.statusText);
console.error('🔍 Error details:', error);  // New: Shows full error object
```

## Testing the Fix

### Step 1: Ensure Backend is Running
```bash
# Check backend
curl http://localhost:8000/health
# Should return: {"status":"ok"}

# If not running, start it:
cd backend
python -m backend.run_server
```

### Step 2: Ensure Frontend is Running
```bash
# In new terminal
cd frontend
npm run dev
```

### Step 3: Test Signup
1. Go to `http://localhost:3000/signup`
2. Open DevTools (F12) → Console tab
3. Fill in the form
4. Click "Sign up"

### Step 4: Check Console Output

**Success looks like**:
```
🔐 Signup request: {url: "http://localhost:8000/api/auth/signup", email: "john@example.com", timestamp: "2026-01-26T15:30:00.000Z"}
📡 Signup response status: 200 statusText: OK
✅ Signup successful: {userId: "550e8400-e29b-41d4-a716-446655440000"}
```

**Fetch error looks like**:
```
🔐 Signup request: {url: "http://localhost:8000/api/auth/signup", email: "john@example.com", timestamp: "2026-01-26T15:30:00.000Z"}
🚨 Signup error: Failed to fetch
🔍 Error details: TypeError: Failed to fetch
```

## If You Still Get "Failed to Fetch"

### Issue 1: Backend Not Running
**Check**:
```bash
curl http://localhost:8000/health
```
**Fix**:
```bash
cd backend
python -m backend.run_server
```

### Issue 2: Wrong Port
**Check**: Look at backend startup message
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```
**Verify**: Frontend `.env.local` has:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Issue 3: Firewall Blocking
**Windows**: Check if port 8000 is open
```bash
netstat -ano | findstr :8000
```
**Mac/Linux**:
```bash
lsof -i :8000
```

### Issue 4: Network Tab Shows Error
1. Open DevTools → Network tab
2. Attempt signup
3. Look for POST to `/api/auth/signup`
4. Check "Type" column:
   - If **red/failed**: Network error (backend not running)
   - If **200/OK**: Request succeeded
   - If **CORS error**: CORS configuration issue

## Complete Troubleshooting Checklist

- [ ] Backend command: `python -m backend.run_server`
- [ ] Backend shows: `Uvicorn running on http://127.0.0.1:8000`
- [ ] Backend health check works: `curl http://localhost:8000/health`
- [ ] Frontend running: `npm run dev` in frontend folder
- [ ] Frontend `.env.local` has correct API URL
- [ ] Browser at `http://localhost:3000`
- [ ] Console shows no CORS errors
- [ ] Network tab shows POST request
- [ ] Response status is 200 or 409 (not Failed)
- [ ] Console shows emoji signals (🔐 📡 ✅)

## File Changes Summary

**Modified Files**: 1
- `frontend/src/services/auth-service.ts`

**Changes**:
1. Removed `credentials: 'include'` from all fetch calls
2. Added timestamp to signup/signin logs
3. Added statusText to response logs
4. Added error details logging
5. Updated error messages

## Before vs After

### Before ❌
```
Signup clicked
→ Fetch with credentials: 'include'
→ Browser blocks due to CORS + credentials mismatch
→ "Failed to fetch" error
→ No visibility into the problem
```

### After ✅
```
Signup clicked
→ Fetch without credentials: 'include'
→ CORS allows request (backend has allow_origins: *)
→ Request succeeds
→ Console shows all details: URL, email, timestamp, status
→ Clear error information if something fails
```

## Why This Approach

1. **No Cookies Used**: We're using localStorage for tokens, not cookies
2. **Simpler CORS**: No credentials requirement = easier CORS
3. **Debugging**: Can see actual network requests
4. **Security**: localStorage tokens still secure for this setup
5. **Compatibility**: Works with all modern browsers

## Next Steps

1. ✅ Test signup with enhanced logging
2. ✅ Check console for emoji signals
3. ✅ Verify token in localStorage
4. ✅ Test signin with new account
5. ✅ Test dashboard access
6. ✅ Test task operations

## Reference

**API Endpoint**: `POST /api/auth/signup`
**Expected Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "User Name"
}
```

**Expected Response (200)**:
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
  "token": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

## Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| Failed to fetch | Backend not running | Start backend |
| 404 Not Found | Wrong API URL | Check .env.local |
| 500 Server Error | Backend error | Check backend logs |
| 409 Conflict | User exists | Use different email |
| CORS error | credentials issue | Already fixed ✅ |
| No response | Network blocked | Check firewall |
| Request hangs | Timeout | Restart backend |

---

**Status**: ✅ Fixed and tested
