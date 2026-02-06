# 📝 Step-by-Step Signup Guide - FOLLOW THIS EXACTLY

## ⚠️ IMPORTANT: Server Restart Required

Before you start, **you must restart both servers** because we changed the database configuration.

---

## 🔄 STEP 0: Restart Both Servers

### Stop the Servers:
1. **Close Terminal 1 (Backend)** - Press `CTRL+C` if still running
2. **Close Terminal 2 (Frontend)** - Press `CTRL+C` if still running
3. **Wait 5 seconds** for ports to be released

### Start Backend Again:
1. **Open Command Prompt or Terminal**
2. **Navigate to backend folder:**
   ```
   cd C:\hackthone2_clone\Todo_App\backend
   ```
3. **Run backend:**
   ```
   python run_server.py
   ```
4. **Wait until you see:**
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```
5. ✅ **Backend is ready!**

### Start Frontend Again:
1. **Open New Command Prompt or Terminal**
2. **Navigate to frontend folder:**
   ```
   cd C:\hackthone2_clone\Todo_App\frontend
   ```
3. **Run frontend:**
   ```
   npm run dev
   ```
4. **Wait until you see:**
   ```
   ✓ Ready in XXs
   ```
5. ✅ **Frontend is ready!**

---

## ✅ STEP 1: Verify Both Servers Are Running

### Check Backend:
- Open browser and go to: **http://localhost:8000/health**
- You should see: `{"status":"ok"}`
- ✅ If you see this, backend is working!

### Check Frontend:
- Open browser and go to: **http://localhost:3000**
- You should see the Todo app homepage
- ✅ If you see this, frontend is working!

---

## 🔐 STEP 2: Navigate to Signup Page

1. **Open your browser** (Chrome, Firefox, Edge, etc.)
2. **Go to URL:** `http://localhost:3000/auth/signup`
3. **You should see a signup form with these fields:**
   - Full Name
   - Email address
   - Password
   - Confirm Password
   - Sign Up button

---

## 📋 STEP 3: Fill Out the Signup Form

**Follow these instructions EXACTLY:**

### Full Name:
- **Type:** `John Doe`
- ✅ Press Tab or click next field

### Email Address:
- **Type:** `testuser2@example.com`
- ⚠️ **IMPORTANT:** Use a NEW email (not testuser@example.com)
- ✅ Press Tab or click next field

### Password:
- **Type:** `MyPassword123`
- ⚠️ **IMPORTANT:** Must be at least 8 characters
- ⚠️ **IMPORTANT:** Use uppercase, lowercase, and numbers
- ✅ Press Tab or click next field

### Confirm Password:
- **Type:** `MyPassword123`
- ⚠️ **IMPORTANT:** Must match password above exactly
- ✅ Now form is ready to submit

---

## 🚀 STEP 4: Submit the Form

1. **Click the "Sign Up" button**
2. **Wait 2-3 seconds** (it's processing)
3. **You should see one of these outcomes:**

### ✅ SUCCESS - You see:
- Dashboard appears
- Your name/email shows at top
- You can see "Create Task" input field
- You see "Sign Out" button
- **This means signup worked!**

### ❌ ERROR - You see "fetch failed":
- **This is likely still a server issue**
- **Follow troubleshooting below**

---

## 🔧 TROUBLESHOOTING - If You Get "Fetch Failed" Error

### Issue 1: Servers Not Running
**Check:** Open browser and go to `http://localhost:8000/health`
- If you see `{"status":"ok"}` → Backend is running ✅
- If you see error → Backend is NOT running ❌
  - **Solution:** Restart backend with `python run_server.py`

### Issue 2: Frontend Not Running
**Check:** Open `http://localhost:3000`
- If you see Todo app → Frontend is running ✅
- If you see error → Frontend is NOT running ❌
  - **Solution:** Restart frontend with `npm run dev`

### Issue 3: Port Already in Use
**Error message:** `Address already in use`
- **Solution:**
  - Find and close the old process using port 8000 or 3000
  - Or restart your computer
  - Then start servers again

### Issue 4: Network Error / Connection Refused
**Steps to fix:**
1. Make sure backend is running on port 8000
2. Make sure frontend is running on port 3000
3. Check if Windows Firewall is blocking:
   - Go to Windows Defender Firewall
   - Click "Allow an app through firewall"
   - Make sure Python and Node are allowed
4. Restart both servers

---

## 📱 STEP 5: After Successful Signup

### You'll See:
✅ Dashboard page loads
✅ Your name appears (e.g., "John Doe")
✅ Your email appears
✅ "Create Task" input field visible
✅ "Sign Out" button visible
✅ No error messages

### Token Saved Automatically:
- ✅ Your login token is saved in browser
- ✅ You stay logged in even if you refresh page
- ✅ You stay logged in until you click "Sign Out"

---

## 🧪 STEP 6: Test Your Account

### Create a Task:
1. Find the input field that says "Create Task"
2. Type: `My first task`
3. Press Enter or click Add
4. ✅ Task should appear in list

### Mark Task Complete:
1. Click the checkbox next to task
2. ✅ Task should be marked complete

### Delete Task:
1. Click delete button (X or trash icon)
2. ✅ Task should disappear

---

## 🔑 STEP 7: Login With Your Account

### To Test Login:
1. Click "Sign Out" button
2. You'll be redirected to signin page
3. Enter your credentials:
   - Email: `testuser2@example.com` (the one you signed up with)
   - Password: `MyPassword123` (the one you set)
4. Click "Sign In"
5. ✅ You should be logged back in
6. ✅ You should see your tasks again

---

## 📋 COMPLETE EXAMPLE

### IF YOU FOLLOW THESE EXACT STEPS:

```
STEP 1: Restart both servers
        └─ Backend: Running on 8000 ✅
        └─ Frontend: Running on 3000 ✅

STEP 2: Open http://localhost:3000/auth/signup

STEP 3: Fill form:
        ├─ Full Name: John Doe
        ├─ Email: testuser2@example.com
        ├─ Password: MyPassword123
        └─ Confirm: MyPassword123

STEP 4: Click "Sign Up"
        └─ Wait 2-3 seconds

STEP 5: See dashboard ✅
        ├─ Your name shows
        ├─ Create Task field visible
        └─ Sign Out button visible

STEP 6: You're logged in! ✅
```

---

## ⚡ QUICK CHECKLIST

Before you start, check these:

- [ ] Backend running on http://localhost:8000 ✅
- [ ] Frontend running on http://localhost:3000 ✅
- [ ] Browser can access http://localhost:8000/health ✅
- [ ] Both servers show "Running" in terminal ✅
- [ ] No error messages in terminal ✅

---

## 🆘 Still Having Issues?

### Copy This Error Message:
1. **Open browser** → Press `F12` (Developer Tools)
2. **Click "Console" tab**
3. **Look for red error messages**
4. **Copy the exact error message**
5. **Tell me what it says**

### Common Errors and Fixes:

| Error | Solution |
|-------|----------|
| "Failed to fetch" | Backend not running on port 8000 |
| "Connection refused" | Backend crashed, restart it |
| "Cannot POST /api/auth/signup" | Backend routing issue, restart both |
| "Email already exists" | Use different email address |
| "Password must be at least 8" | Password too short, use 8+ chars |
| "Passwords do not match" | Confirm password doesn't match |

---

## 📞 If Nothing Works

Please tell me:
1. **What error do you see?** (exact message)
2. **Which server crashed?** (backend or frontend)
3. **What does the terminal say?** (copy error from terminal)
4. **Did you restart both servers?**

---

**Now follow these steps and signup! You got this! 🚀**
