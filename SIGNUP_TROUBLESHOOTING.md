# 🔧 Signup Troubleshooting Guide

## ✅ Verify Everything is Working First

### Test 1: Check Backend Health
```
Open browser and go to: http://localhost:8000/health

Expected response:
{"status":"ok"}

✅ If you see this, backend is working correctly!
❌ If you see error, restart backend
```

### Test 2: Check Frontend Load
```
Open browser and go to: http://localhost:3000

Expected: You see the Todo app homepage

✅ If you see it, frontend is working correctly!
❌ If you see error, restart frontend
```

### Test 3: Check API Connection
```
Open browser and go to: http://localhost:3000/auth/signup

Expected: You see signup form with these fields:
- Full Name
- Email address
- Password
- Confirm Password
- Sign Up button

✅ If you see form, API connection is working!
❌ If blank or error, see solutions below
```

---

## 🚀 CORRECT SIGNUP PROCESS

### Step 1: Fill Form Correctly
```
❌ WRONG:
- Email: test (too short, no @)
- Password: 123 (too short, less than 8 chars)

✅ CORRECT:
- Email: myemail@example.com (must be valid email)
- Password: MyPassword123 (at least 8 characters)
```

### Step 2: Confirm Password Must Match
```
❌ WRONG:
- Password: MyPassword123
- Confirm: MyPassword12 (different!)

✅ CORRECT:
- Password: MyPassword123
- Confirm: MyPassword123 (exactly same!)
```

### Step 3: Use Valid Email
```
❌ WRONG:
- Email: testuser@example.com (already used!)
- Email: invalid-email (no @)
- Email: user@.com (incomplete)

✅ CORRECT:
- Email: john.doe@example.com
- Email: newemail2@test.com
- Email: user123@domain.org
```

---

## ❌ Common Errors and Solutions

### Error 1: "Failed to fetch"

**What it means:** Frontend can't connect to backend

**Solutions:**

```
1. Verify backend is running:
   ✓ Open http://localhost:8000/health
   ✓ Should show {"status":"ok"}

   If error:
   - Go to backend terminal
   - Press CTRL+C to stop
   - Type: python run_server.py
   - Wait for "Uvicorn running" message

2. Verify port 8000 is not blocked:
   - Windows: Run Command Prompt as Admin
   - Type: netstat -ano | findstr :8000
   - If nothing shows, port is free
   - If shows process, note PID and close it

3. Restart frontend:
   - Go to frontend terminal
   - Press CTRL+C to stop
   - Type: npm run dev
   - Wait for "Ready" message
```

---

### Error 2: "Email already exists"

**What it means:** You're using an email that already has an account

**Solutions:**

```
✅ Use a different email:
   - Instead of: testuser@example.com
   - Try: testuser2@example.com
   - Try: john.doe@test.com
   - Try: newemail123@domain.com

❌ Don't use:
   - testuser@example.com (already used!)
   - admin@test.com (if already exists)
   - Same email as before
```

---

### Error 3: "Password must be at least 8 characters"

**What it means:** Your password is too short

**Solutions:**

```
✅ Use a longer password:
   - Instead of: Pass (4 chars)
   - Use: Password123 (11 chars) ✓
   - Use: SecurePass123 (13 chars) ✓
   - Use: MyP@ssw0rd (10 chars) ✓

❌ Don't use:
   - 123 (too short)
   - pass (too short)
   - 12345 (too short)
   - password (only 8, but no numbers - OK actually)
```

---

### Error 4: "Passwords do not match"

**What it means:** Password and Confirm Password are different

**Solutions:**

```
Make sure they're exactly the same:

Step 1: Type password in Password field:
   MyPassword123

Step 2: Type exact same in Confirm Password:
   MyPassword123  ← Must be exactly the same!

❌ Don't do:
   Password: MyPassword123
   Confirm:  MyPassword12  ← Missing '3'!
```

---

### Error 5: "Fetch failed" / Network Error

**What it means:** Frontend and backend can't communicate

**Solutions:**

```
1. Check both servers are running:

   Backend check:
   ✓ Open new terminal window
   ✓ Go to: cd C:\hackthone2_clone\Todo_App\backend
   ✓ Run: python run_server.py
   ✓ Wait for: "Uvicorn running on http://0.0.0.0:8000"

   Frontend check:
   ✓ Open another new terminal window
   ✓ Go to: cd C:\hackthone2_clone\Todo_App\frontend
   ✓ Run: npm run dev
   ✓ Wait for: "✓ Ready in XXs"

2. Check Windows Firewall:
   ✓ Open Windows Defender Firewall
   ✓ Click "Allow an app through firewall"
   ✓ Make sure Python is checked ✓
   ✓ Make sure Node is checked ✓
   ✓ Click OK and try signup again

3. Check ports are not in use:
   ✓ Port 8000 (backend) - check with: netstat -ano | findstr :8000
   ✓ Port 3000 (frontend) - check with: netstat -ano | findstr :3000
   ✓ If in use, close that application and restart servers
```

---

### Error 6: Blank Page / Nothing Loads

**What it means:** Frontend or backend not responding

**Solutions:**

```
1. Restart frontend:
   ✓ Go to frontend terminal
   ✓ Press CTRL+C
   ✓ Type: npm run dev
   ✓ Wait 30 seconds

2. Restart backend:
   ✓ Go to backend terminal
   ✓ Press CTRL+C
   ✓ Type: python run_server.py
   ✓ Wait 5 seconds

3. If still blank:
   ✓ Close all terminal windows
   ✓ Open fresh terminal windows
   ✓ Start backend first
   ✓ Wait 5 seconds
   ✓ Start frontend second
   ✓ Wait for "Ready" message
```

---

### Error 7: Form Validation Errors

**What it means:** Form input doesn't meet requirements

**Solutions:**

```
Email validation errors:

❌ "user" → Not an email
✅ "user@example.com" → Valid email

❌ "example.com" → Missing @
✅ "user@example.com" → Has @

❌ "user@.com" → Missing domain
✅ "user@example.com" → Has domain


Password validation errors:

❌ "12345" → Not 8+ characters
✅ "MyPassword123" → 13 characters ✓

❌ "password" → No uppercase/number
✅ "Password123" → Has uppercase and number ✓

❌ "PASSWORD" → No lowercase/number
✅ "Password123" → Has lowercase and number ✓
```

---

## 🎯 STEP-BY-STEP WORKING EXAMPLE

Follow this exact process:

```
STEP 1: Make sure both servers running
   Terminal 1 (Backend):
   cd C:\hackthone2_clone\Todo_App\backend
   python run_server.py
   [Wait for: Uvicorn running on http://0.0.0.0:8000]

   Terminal 2 (Frontend):
   cd C:\hackthone2_clone\Todo_App\frontend
   npm run dev
   [Wait for: ✓ Ready in XXs]

STEP 2: Open browser
   Go to: http://localhost:3000/auth/signup

STEP 3: Fill form with VALID data
   Full Name: John Doe
   Email: john.doe.2026@example.com
   Password: MySecurePassword123
   Confirm: MySecurePassword123

STEP 4: Click Sign Up button

STEP 5: Expected result
   - Form disappears
   - Redirected to dashboard
   - See "John Doe" at top
   - See "Create Task" field
   - ✅ SIGNUP SUCCESSFUL!
```

---

## 📊 Verification Checklist

Before signup, verify all checkboxes:

```
□ Backend running?
  └─ Check: http://localhost:8000/health shows {"status":"ok"}

□ Frontend running?
  └─ Check: http://localhost:3000 loads without error

□ Signup page loads?
  └─ Check: http://localhost:3000/auth/signup shows form

□ Email is unique?
  └─ Check: Not using same email as before

□ Password is long enough?
  └─ Check: At least 8 characters

□ Passwords match?
  └─ Check: Password and Confirm are identical

□ Email is valid format?
  └─ Check: Has @ and domain (e.g., user@example.com)

All checked? → Try signup now! ✅
```

---

## 🆘 Still Not Working?

### Information to Collect:

1. **Screenshot of error message**
   - Take screenshot of exact error you see

2. **Browser console error**
   - Press F12 to open Developer Tools
   - Click "Console" tab
   - Copy any red error messages

3. **Backend terminal output**
   - Look for any red error messages
   - Copy and share with me

4. **Frontend terminal output**
   - Look for any error messages
   - Copy and share with me

### Tell me:

```
1. What error do you see exactly? (copy/paste)
2. Which step fails? (fill form, click button, etc)
3. Did you restart both servers? (yes/no)
4. Did you close old terminals first? (yes/no)
5. Are ports 3000 and 8000 free? (yes/no)
```

---

## ✅ Success Indicators

You know signup worked when you see:

```
✓ Form disappears
✓ Page redirects automatically
✓ Dashboard page loads
✓ Your name appears at top
✓ "Create Task" input field visible
✓ "Sign Out" button visible
✓ No error messages
✓ Can create and manage tasks
```

---

**Now try signup with the checklist above! Good luck! 🚀**
