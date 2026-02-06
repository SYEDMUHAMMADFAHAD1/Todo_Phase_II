import sqlite3
import sys
import os

# Add backend to path
backend_path = r"C:\master_second_copy\Todo_App\backend"
sys.path.insert(0, backend_path)
os.chdir(backend_path)

try:
    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()

    # Get column info to know the order
    cursor.execute('PRAGMA table_info(task);')
    columns = cursor.fetchall()
    print('Task table columns:')
    for i, col in enumerate(columns):
        print(f'  Position {i}: {col[1]} ({col[2]}) - Not Null: {bool(col[3])}, PK: {bool(col[5])}')

    print()
    # Get all tasks
    cursor.execute('SELECT * FROM task ORDER BY created_at DESC LIMIT 10;')
    tasks = cursor.fetchall()
    print('Recent tasks from DB:')
    for i, task in enumerate(tasks):
        print(f'  Task {i+1}: title=\"{task[0][:30]}...\", id=\"{task[3]}\", user_id=\"{task[4]}\"')
    
    print(f"\nTotal tasks in DB: {len(tasks)}")

    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()