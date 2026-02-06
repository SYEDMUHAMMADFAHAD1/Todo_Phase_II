import sqlite3

conn = sqlite3.connect(r'C:\master_second_copy\Todo_App\backend\test.db')
cursor = conn.cursor()
try:
    cursor.execute('SELECT id, title FROM task ORDER BY created_at DESC LIMIT 5;')
    tasks = cursor.fetchall()
    print('Latest tasks in test.db:')
    for task in tasks:
        print(f'  ID: \"{task[0]}\", Title: \"{task[1][:50]}...\"')
except Exception as e:
    print(f'Error: {e}')
    # Try without ordering
    try:
        cursor.execute('SELECT id, title FROM task LIMIT 5;')
        tasks = cursor.fetchall()
        print('Some tasks in test.db:')
        for task in tasks:
            print(f'  ID: \"{task[0]}\", Title: \"{task[1][:50]}...\"')
    except Exception as ex:
        print(f'Second attempt error: {ex}')
        
conn.close()