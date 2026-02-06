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

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('Tables in database:', tables)

    # Get the schema for each table
    for table in tables:
        table_name = table[0]
        print(f'\nSchema for table "{table_name}":')
        cursor.execute(f'PRAGMA table_info("{table_name}")')
        columns = cursor.fetchall()
        for col in columns:
            print(f'  Column: {col[1]}, Type: {col[2]}, Not Null: {bool(col[3])}, Default: {col[4]}, Primary Key: {bool(col[5])}')

    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()