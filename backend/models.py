from werkzeug.security import generate_password_hash

# backend/models.py
import sqlite3

def init_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_task_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    init_user_table()
    init_task_table()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_pw = generate_password_hash(password)
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_task(user_id, title):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (user_id, title) VALUES (?, ?)', (user_id, title))
    conn.commit()
    conn.close()

def get_tasks_for_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def mark_task_complete(task_id, user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?', (task_id, user_id))
    conn.commit()
    conn.close()

def delete_task(task_id, user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
    conn.commit()
    conn.close()

def rename_task(task_id, new_title, user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET title = ? WHERE id = ? AND user_id = ?', (new_title, task_id, user_id))
    conn.commit()
    conn.close()

def get_pending_tasks(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE user_id = ? AND completed = 0', (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_completed_tasks(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE user_id = ? AND completed = 1', (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks
