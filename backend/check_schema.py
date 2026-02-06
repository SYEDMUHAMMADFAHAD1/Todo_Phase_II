import sqlite3
import sys

print('Connecting to database...', flush=True)
conn = sqlite3.connect('todo_app.db')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('All tables:', tables, flush=True)

# Check if task table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task';")
task_table = cursor.fetchone()
print('Task table exists:', task_table is not None, flush=True)

if task_table:
    # Get table info for the task table
    cursor.execute('PRAGMA table_info(task)')
    columns = cursor.fetchall()
    print('Task table columns:', flush=True)
    for col in columns:
        print(f'  {col}', flush=True)
else:
    print('Task table does not exist', flush=True)

# Check if user table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
user_table = cursor.fetchone()
print('User table exists:', user_table is not None, flush=True)

if user_table:
    cursor.execute('PRAGMA table_info(user)')
    columns = cursor.fetchall()
    print('User table columns:', flush=True)
    for col in columns:
        print(f'  {col}', flush=True)

conn.close()
print('Connection closed.', flush=True)