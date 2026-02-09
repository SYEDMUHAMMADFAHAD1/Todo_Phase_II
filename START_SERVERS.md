# How to Start the Todo App

## Problem Fixed
The "failed to fetch" error was caused by:
1. Backend server not running
2. Missing environment configuration files

## Configuration Files Created
- `backend/.env` - Backend environment variables
- `frontend/.env.local` - Frontend environment variables

## Starting the Application

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd C:\master_second_copy\Todo_App
python run_backend.py
```

Or alternatively:
```bash
cd C:\master_second_copy\Todo_App\backend
python run_server.py
```

**Expected output:**
- Server should start on `http://localhost:8000`
- You should see: "Application startup complete"

### Step 2: Start the Frontend Server

Open a **NEW** terminal (keep backend running) and run:

```bash
cd C:\master_second_copy\Todo_App\frontend
npm run dev
```

**Expected output:**
- Frontend should start on `http://localhost:3000`
- You should see: "Ready - started server on 0.0.0.0:3000"

### Step 3: Test Authentication

1. Open your browser to: `http://localhost:3000`
2. Click "Sign up" to create a new account
3. Fill in:
   - Name: Your Name
   - Email: test@example.com
   - Password: password123
   - Confirm Password: password123
4. Click "Sign up" button

**Expected result:**
- You should be redirected to `/authenticated/dashboard`
- You should see your todo list interface

## Troubleshooting

### Backend won't start
- Check if Python is installed: `python --version`
- Make sure dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use: `netstat -ano | findstr "8000"`

### Frontend won't start
- Check if Node.js is installed: `node --version`
- Install dependencies: `npm install`
- Check if port 3000 is already in use: `netstat -ano | findstr "3000"`

### Still getting "failed to fetch"
1. Verify backend is running: Open `http://localhost:8000/health` in browser
   - Should return: `{"status":"ok"}`
2. Check browser console for detailed error messages
3. Verify `.env` files are in correct locations:
   - `backend/.env` exists
   - `frontend/.env.local` exists

### Authentication Issues
- Clear browser localStorage: Open DevTools > Application > Storage > Clear site data
- Check backend logs for error messages
- Verify database file exists: `backend/todo_app.db`

## Next Steps

Once both servers are running and you can sign in:
- Create todos from the dashboard
- Test update, delete, and filter functionality
- Check the chat feature (if OpenAI API key is configured)

## Important Notes

- Keep both terminal windows open while using the app
- Press Ctrl+C in each terminal to stop the servers
- Backend must be started BEFORE frontend for proper initialization
