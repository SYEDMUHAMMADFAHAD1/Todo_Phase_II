# 📋 Manual Testing Steps - Todo Creation

This guide walks you through EXACTLY what to test and what to expect.

---

## 🚀 Setup (1 minute)

### Terminal 1 - Start Backend
```bash
cd backend
python run_server.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Start Frontend
```bash
cd frontend
npm run dev
```

**Expected output:**
```
▲ Next.js 16.x
  ready on http://localhost:3000
```

---

## 📱 Test 1: Sign Up Fresh User (3 minutes)

### Step 1: Navigate to Signup
- Go to: http://localhost:3000/signup

### Step 2: Enter Credentials
- Email: `test@example.com`
- Password: `password123`
- Name: (leave empty or enter "Test User")

### Step 3: Click Sign Up
- Button should change to "Signing up..."

### Step 4: Verify Success
- ✅ Should redirect to dashboard
- ✅ Email should appear in top-right navbar
- ✅ Todo list should show "Loading..."
- ✅ No error messages

### Step 5: Open DevTools (F12)
- Console tab: Look for logs
  ```
  ✅ Token stored in localStorage
  🔐 Authorization header attached
  Fetching todos from /tasks...
  ```
- Storage tab:
  ```
  LocalStorage → http://localhost:3000
  todo_app_token: eyJhbGciOi... (should exist)
  ```

---

## ✅ Test 2: Create First Todo (5 minutes)

### Step 1: On Dashboard, Find Todo Form
- Title should say: "Create New Todo"
- Two fields: Title, Description
- Blue "Create Todo" button

### Step 2: Enter Todo Data
- Title: `Buy groceries`
- Description: (leave empty)

### Step 3: Click "Create Todo"
- Button text changes to: "Creating..."
- Form inputs disabled (grayed out)

### Step 4: Observe Success
- ✅ Button returns to "Create Todo"
- ✅ Form clears completely
- ✅ New todo appears in list below

**Expected list:**
```
Todos List
☐ Buy groceries    [Edit] [Delete]
```

### Step 5: Check DevTools → Console
Look for these logs:
```
Creating todo with data: {title: "Buy groceries", description: undefined}
🔐 Authorization header attached: {token: 'eyJhbGciOi...'}
Todo created successfully: {
  id: "550e8400-...",
  title: "Buy groceries",
  is_completed: false,
  user_id: "550e8400-...",
  created_at: "2026-01-29T...",
  updated_at: "2026-01-29T..."
}
```

### Step 6: Check DevTools → Network
- Find the POST request to `/api/tasks`
- Click on it
- Headers section:
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
  Content-Type: application/json
  ```
- Response section:
  ```
  201 Created
  {
    "id": "550e8400-...",
    "title": "Buy groceries",
    ...
  }
  ```

**✅ PASS** if all above are present

---

## ✅ Test 3: Create Second Todo (2 minutes)

### Step 1: Enter Another Todo
- Title: `Review PR #42`
- Description: `Check code quality and performance`

### Step 2: Click "Create Todo"

### Step 3: Verify
- ✅ Form clears
- ✅ New todo appears in list
- ✅ List now shows 2 items:
  ```
  ☐ Buy groceries
  ☐ Review PR #42
  ```

**✅ PASS** if both todos visible

---

## ⚠️ Test 4: Error - Empty Title (2 minutes)

### Step 1: Try Invalid Submit
- Leave title empty
- Click "Create Todo"

### Step 2: Verify Error
- ✅ Form does NOT submit
- ✅ Red error box appears: `"Title is required"`
- ✅ No API request made

### Step 3: Fix and Retry
- Enter title: `Workout`
- Click "Create Todo"
- ✅ Should succeed

**✅ PASS** if error shown and form not submitted

---

## ⚠️ Test 5: Simulate Network Error (5 minutes)

### Step 1: Stop Backend
- Go to Terminal 1 (backend)
- Press `Ctrl+C` to stop

### Step 2: Try to Create Todo
- Title: `This should fail`
- Click "Create Todo"

### Step 3: Observe Error
- ✅ Error message appears (e.g., "Network error" or "Failed to create todo")
- ✅ No crash
- ✅ Form stays intact

### Step 4: Check Console
- Should see error logs
- No "Uncaught Exception"

### Step 5: Restart Backend
- Go to Terminal 1
- Run: `python run_server.py`

### Step 6: Retry and Verify Recovery
- Try creating todo again
- ✅ Should work again

**✅ PASS** if error handled gracefully and recovery works

---

## ⚠️ Test 6: Simulate Auth Expiry (5 minutes)

### Step 1: Delete Token
- Open DevTools (F12)
- Go to Storage → LocalStorage → http://localhost:3000
- Right-click `todo_app_token`
- Select "Delete"

### Step 2: Try to Create Todo
- Title: `Test auth`
- Click "Create Todo"

### Step 3: Observe Behavior
- ✅ Error appears (should say "Unauthorized")
- ✅ OR redirected to /signin
- ✅ Token cleared from localStorage

### Step 4: Sign In Again
- Navigate to /signin or wait for redirect
- Enter same credentials: `test@example.com` / `password123`

### Step 5: Create Todo Again
- Title: `After re-login`
- Click "Create Todo"
- ✅ Should work again

**✅ PASS** if auth expiry handled and re-login works

---

## ✅ Test 7: Toggle Todo Completion (2 minutes)

### Step 1: Find a Todo
- Look for: `Buy groceries` in the list

### Step 2: Check the Checkbox
- Click the `☐` checkbox next to it

### Step 3: Observe Change
- ✅ Checkbox becomes `☑`
- ✅ Todo text might appear crossed-out
- ✅ "Completed" count increases

### Step 4: Check DevTools → Network
- Find PUT request to `/api/tasks/{id}`
- Should have Authorization header
- Response: 200 OK

**✅ PASS** if todo marked completed and API called

---

## 🗑️ Test 8: Delete Todo (2 minutes)

### Step 1: Find Delete Button
- Hover over a todo (e.g., "Workout")
- Click [Delete] or trash icon

### Step 2: Observe Removal
- ✅ Todo disappears from list immediately
- ✅ Count decreases

### Step 3: Check DevTools → Network
- Find DELETE request to `/api/tasks/{id}`
- Should have Authorization header
- Response: 200 OK

**✅ PASS** if todo deleted and API called

---

## 🔄 Test 9: Session Persistence (3 minutes)

### Step 1: Create a Todo
- Title: `Session test`
- Click "Create Todo"

### Step 2: Hard Refresh Page
- Press: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Or DevTools → Network → Disable Cache, then refresh

### Step 3: Observe Reload
- ✅ Page loads
- ✅ User still logged in (email in navbar)
- ✅ Todo "Session test" still visible

### Step 4: Check Storage
- DevTools → Storage → LocalStorage
- ✅ `todo_app_token` still exists

**✅ PASS** if session persists across refresh

---

## 🧾 Test 10: Todos Counter (2 minutes)

### Step 1: Note Current Count
- Look at dashboard stats (if showing)
- Or count todos in list manually

### Step 2: Create New Todo
- Create: `Counter test`

### Step 3: Verify Counter Increases
- ✅ Total count increases by 1

### Step 4: Mark as Completed
- ✅ Completed count increases
- ✅ Pending count decreases

### Step 5: Delete Todo
- ✅ Total count decreases

**✅ PASS** if counter updates correctly

---

## 📝 Final Checklist

Mark off each test as you complete it:

- [ ] Test 1: Sign Up & Auth
- [ ] Test 2: Create First Todo
- [ ] Test 3: Create Second Todo
- [ ] Test 4: Empty Title Error
- [ ] Test 5: Network Error
- [ ] Test 6: Auth Expiry
- [ ] Test 7: Toggle Completion
- [ ] Test 8: Delete Todo
- [ ] Test 9: Session Persistence
- [ ] Test 10: Todos Counter

---

## 🐛 If Something Fails

### Check Console (F12 → Console)
- Look for errors
- Note exact error message
- Screenshot or copy error

### Check Network (F12 → Network)
- Find the failed request
- Check Status code (should be 201 for create, 200 for others)
- Check Authorization header (should be present)
- Check Response (should have error message if it failed)

### Check Storage (F12 → Storage)
- Verify `todo_app_token` exists
- Verify token is not empty
- Verify token starts with `eyJ` (base64)

### Common Issues:

**❌ Issue: "Failed to create todo" generic error**
- Check: Is error an ApiErrorClass instance?
- Look in console for actual error from backend
- Check backend logs in Terminal 1

**❌ Issue: No Authorization header**
- Check: Is token in localStorage?
- Check: Does token exist in DevTools Storage?
- Try: Hard refresh (Ctrl+Shift+R)

**❌ Issue: 401 Unauthorized**
- Check: Has token expired?
- Check: Is backend running?
- Try: Sign out and sign in again

**❌ Issue: Network error**
- Check: Is backend running? (Terminal 1)
- Check: Is CORS configured? (should see in Network response headers)
- Try: Restart backend

---

## ✅ Success Criteria

**ALL tests pass if:**
- ✅ Can create todos without errors
- ✅ Todos appear instantly in list
- ✅ Authorization header sent with every request
- ✅ Error messages show actual error (not generic)
- ✅ Session persists across refresh
- ✅ Can toggle, update, delete todos
- ✅ No crashes or unhandled exceptions
- ✅ Console has proper debug logs

**Report Results:**
- Number of tests passed
- Any failures or errors
- Screenshots if issues found

---

**Good luck testing! 🚀**
