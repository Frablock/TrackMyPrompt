import sqlite3

class UserDAO:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Créer la table Users si elle n'existe pas déjà
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute('''
                INSERT INTO Users (Username, Password) 
                VALUES (?, ?)
            ''', (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def delete_user(self, username):
        try:
            self.cursor.execute('''
                DELETE FROM Users 
                WHERE username = ?
            ''', (username))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def update_password(self, username, password):
        if self.user_exists(username):
            self.cursor.execute('''
                UPDATE Users
                SET Password = ?
                WHERE Username = ?
            ''', (password, username))
            self.conn.commit()
            return True
        else:
            return False

    def get_all_users(self):
        self.cursor.execute('''
            SELECT Username FROM Users
        ''')
        users = self.cursor.fetchall()
        return [user[0] for user in users]

    def get_password(self, username):
        self.cursor.execute('''
            SELECT Password FROM Users WHERE Username = ?
        ''', (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def user_exists(self, username):
        self.cursor.execute('''
            SELECT 1 FROM Users WHERE Username = ?
        ''', (username,))
        return self.cursor.fetchone() is not None

    def close(self):
        self.conn.close()