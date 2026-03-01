import sqlite3

class DataBase:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
    
    def InitDataBase(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT,
            password TEXT,
            session_id TEXT,
            session_status BOOLEAN)
        ''')
        self.db.commit()
    
    def InsertUserId(self, name, password):
        show_user_in_database = self.cursor.execute("SELECT login, password FROM users WHERE login = ? AND password = ?", (name, password)).fetchone()
        if show_user_in_database is None:
            self.cursor.execute("INSERT INTO users (login, password, session_id, session_status) VALUES (?,?,?,?)", (name, password, None, False))
            print(f"Пользователь {name} добавлен в базу данных users")
        else:
            print(f"Пользователь {name} уже есть в базе данных users")
        self.db.commit()
        
    def show_data_base(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        print("============================================================================")
        print("Все пользователи")
        for row in rows:
            print(f"ID: {row[0]}, Логин: {row[1]}, Статус сессии: {row[4]}")  # ИСПРАВЛЕНО: вывод логина вместо "Адрес"
        print("============================================================================")

    def ExamenationUser(self, name, password):
        examenation = self.cursor.execute("SELECT login, password FROM users WHERE login = ? AND password = ?", (name, password)).fetchone()
        if examenation:
            print("Вы успешно авторизировались")
            return True
        else:
            print("Неверный логин или пароль")
            return False
        
    def create_session_database(self, name, session_id, session_status):
        self.cursor.execute("UPDATE users SET session_id = ?, session_status = ? WHERE login = ?", (session_id, session_status, name))
        self.db.commit()