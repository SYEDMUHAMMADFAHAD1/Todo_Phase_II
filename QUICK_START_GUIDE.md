# 🚀 Quick Start Guide - Todo Application

## ✅ Current Status
- ✅ Backend Running on `http://localhost:8000`
- ✅ Frontend Running on `http://localhost:3000`
- ✅ Both servers fully operational
- ✅ Authentication system fully functional

---

## 📋 Access the Application

### Frontend (User Interface)
**Main Dashboard:** http://localhost:3000

#### Authentication Pages:
- **Sign Up Page:** http://localhost:3000/auth/signup
- **Sign In Page:** http://localhost:3000/auth/signin
- **Dashboard (Protected):** http://localhost:3000/authenticated/dashboard

---

## 🔐 Test Credentials

You can use the following test account that was created during testing:

```
Email: testuser@example.com
Password: SecurePassword123
```

Or create a new account by visiting the signup page.

---

## 📝 How to Use the Application

### 1️⃣ Create a New Account

1. Go to **http://localhost:3000/auth/signup**
2. Fill in the form:
   - **Full Name:** Your name
   - **Email:** Your email address
   - **Password:** At least 8 characters
   - **Confirm Password:** Must match password
3. Click **Sign Up**
4. ✅ You'll be logged in automatically and redirected to the dashboard

### 2️⃣ Sign In to Your Account

1. Go to **http://localhost:3000/auth/signin**
2. Enter your credentials:
   - **Email:** Your registered email
   - **Password:** Your password
3. Click **Sign In**
4. ✅ You'll be redirected to your dashboard

### 3️⃣ Create and Manage Tasks

1. After signing in, you'll see your dashboard
2. **Add a new task:** Click the input field and type your task
3. **Mark as complete:** Click the checkbox next to the task
4. **Delete a task:** Click the delete button
5. **View your tasks:** All your tasks appear on the dashboard

### 4️⃣ Sign Out

1. Look for the **Sign Out** button (usually in header or profile menu)
2. Click it
3. ✅ You'll be redirected to the sign in page

---

## 🔌 API Endpoints

### Authentication Endpoints

#### Sign Up
```bash
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "User Name"
}

Response:
{
  "user": { "id": "...", "email": "...", "name": "...", ... },
  "session": { "id": "...", "userId": "...", "expiresAt": "..." },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Sign In
```bash
POST /api/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123"
}

Response:
{
  "user": { ... },
  "session": { ... },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Get Session (Protected)
```bash
GET /api/auth/session
Authorization: Bearer <token>

Response:
{
  "user": { ... },
  "session": { ... }
}
```

#### Sign Out
```bash
POST /api/auth/signout

Response:
{
  "message": "Successfully signed out"
}
```

---

## 🛠️ Backend API Base URL

- **Development:** `http://localhost:8000/api`
- **Health Check:** `http://localhost:8000/health`

---

## 🗄️ Database

### Location
`./todo_app.db` (SQLite database file)

### User Table Schema
```sql
CREATE TABLE user (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  password TEXT NOT NULL,
  created_at DATETIME,
  updated_at DATETIME
)
```

---

## 🔑 Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite+aiosqlite:///./todo_app.db
BETTER_AUTH_SECRET=supersecretkeyfordevonly
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
BETTER_AUTH_SECRET=placeholder_secret_for_spec1
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## 🐛 Troubleshooting

### Issue: Backend not starting
**Solution:**
1. Check if port 8000 is already in use
2. Verify `aiosqlite` is installed: `pip install aiosqlite`
3. Restart the backend: `python backend/run_server.py`

### Issue: Frontend not starting
**Solution:**
1. Check if port 3000 is already in use
2. Install dependencies: `npm install` in frontend directory
3. Restart: `npm run dev`

### Issue: "Not authenticated" error
**Solution:**
1. Make sure you're logged in
2. Check if token is saved in localStorage
3. Try logging in again
4. Clear browser cache and cookies

### Issue: Login fails with "Incorrect email or password"
**Solution:**
1. Verify email is correct (case-sensitive)
2. Verify password is correct
3. Try signing up with a new account
4. Check backend logs for errors

---

## 📊 Test Data

### User Created During Testing
```
Email: testuser@example.com
Password: SecurePassword123
Name: Test User
```

You can use this account to log in and test the application.

---

## 📂 Project Structure

```
Todo_App/
├── backend/
│   ├── src/
│   │   ├── api/routers/
│   │   │   ├── auth.py (Authentication endpoints)
│   │   │   └── tasks.py (Task endpoints)
│   │   ├── core/
│   │   │   ├── config.py (Configuration)
│   │   │   └── db.py (Database setup)
│   │   ├── models/
│   │   │   └── task.py (Data models)
│   │   └── main.py (FastAPI app)
│   ├── run_server.py (Start backend)
│   └── requirements.txt (Dependencies)
├── frontend/
│   ├── app/
│   │   ├── (auth)/ (Auth pages)
│   │   │   ├── signup/page.tsx
│   │   │   └── signin/page.tsx
│   │   └── authenticated/ (Protected routes)
│   ├── src/
│   │   ├── components/ (React components)
│   │   ├── contexts/ (React Context)
│   │   ├── hooks/ (Custom hooks)
│   │   └── services/ (API services)
│   ├── package.json (Dependencies)
│   └── .env.local (Configuration)
└── AUTHENTICATION_TEST_REPORT.md (Test results)
```

---

## 🎯 Next Steps

1. ✅ Create an account at `http://localhost:3000/auth/signup`
2. ✅ Log in to access your dashboard
3. ✅ Start creating and managing tasks
4. ✅ Test the full application flow

---

## 📞 Support

For issues or questions:
1. Check the `AUTHENTICATION_TEST_REPORT.md` for detailed test results
2. Review backend logs for server errors
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly

---

**Everything is set up and ready to use! Happy coding! 🎉**
