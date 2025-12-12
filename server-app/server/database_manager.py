import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="server/database.db"):
        self.db_path = os.path.join(os.getcwd(), db_name)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS offline_messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, receiver TEXT, encrypted_content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def add_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user_password(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_all_users(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users

    def save_offline_message(self, sender, receiver, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO offline_messages (sender, receiver, encrypted_content) VALUES (?, ?, ?)", (sender, receiver, content))
        conn.commit()
        conn.close()

    def get_offline_messages(self, receiver):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sender, encrypted_content, timestamp FROM offline_messages WHERE receiver=?", (receiver,))
        messages = cursor.fetchall()
        cursor.execute("DELETE FROM offline_messages WHERE receiver=?", (receiver,))
        conn.commit()
        conn.close()
        return messages