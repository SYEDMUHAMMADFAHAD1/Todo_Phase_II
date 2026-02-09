"""
Verification script to check if the Todo App is properly configured
"""
import sys
import os
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"[OK] {description}: Found")
        return True
    else:
        print(f"[FAIL] {description}: Missing")
        return False

def check_env_file(path, required_vars):
    """Check if .env file has required variables"""
    if not os.path.exists(path):
        print(f"[FAIL] {path}: File missing")
        return False

    with open(path, 'r') as f:
        content = f.read()

    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)

    if missing_vars:
        print(f"[WARN] {path}: Missing variables: {', '.join(missing_vars)}")
        return False
    else:
        print(f"[OK] {path}: All required variables present")
        return True

def main():
    print("=" * 60)
    print("Todo App Setup Verification")
    print("=" * 60)
    print()

    base_path = Path(__file__).parent
    all_good = True

    # Check backend .env
    print("1. Checking Backend Configuration...")
    backend_env = base_path / "backend" / ".env"
    required_backend_vars = [
        "DATABASE_URL",
        "BETTER_AUTH_SECRET",
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    ]
    if not check_env_file(backend_env, required_backend_vars):
        all_good = False
    print()

    # Check frontend .env.local
    print("2. Checking Frontend Configuration...")
    frontend_env = base_path / "frontend" / ".env.local"
    required_frontend_vars = [
        "NEXT_PUBLIC_API_URL"
    ]
    if not check_env_file(frontend_env, required_frontend_vars):
        all_good = False
    print()

    # Check key files exist
    print("3. Checking Key Files...")
    files_to_check = [
        (base_path / "backend" / "run_server.py", "Backend run script"),
        (base_path / "frontend" / "package.json", "Frontend package.json"),
        (base_path / "backend" / "src" / "main.py", "Backend main.py"),
        (base_path / "frontend" / "src" / "services" / "auth-service.ts", "Auth service"),
    ]

    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_good = False
    print()

    # Summary
    print("=" * 60)
    if all_good:
        print("[SUCCESS] All checks passed! You're ready to start the servers.")
        print()
        print("Next steps:")
        print("1. Terminal 1: cd backend && python run_server.py")
        print("2. Terminal 2: cd frontend && npm run dev")
        print("3. Open browser: http://localhost:3000")
    else:
        print("[ERROR] Some checks failed. Please review the errors above.")
        print()
        print("See START_SERVERS.md for detailed instructions.")
    print("=" * 60)

    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
