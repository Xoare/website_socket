import sqlite3
class DataBase:
    def __init__(self,db):
        self.db = db
        self.cursor = db.cursor()
    
    def InitDataBase(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            login TEXT,
            password TEXT)
            ''')
    
    def InsertUserId(self, name, password):
        show_user_in_database = self.cursor.execute("SELECT login, password FROM users WHERE login = ? AND password = ?", (name, password)).fetchone()
        if show_user_in_database is None:
            self.cursor.execute("INSERT INTO users (login, password) VALUES (?,?)",( name, password))
            print(f"Пользователь {name} с ID: <Доработка> добавлен в базу данных users")
        else:
            print(f"Пользователь {name} уже есть в базе данных users")
        self.db.commit()
        
    def show_data_base(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        print("============================================================================")
        print("Все пользователи")
        for row in rows:
            print(f"ID: {row[0]}, Адрес: {row[1]}")
        print("============================================================================")

    def ExamenationUser(self, name, password):
        examenation = self.cursor.execute("SELECT login, password FROM users WHERE login = ? AND password = ?", (name,password)).fetchone()
        if examenation:
            print("Вы успешно авторизировались")
        else:
            print("Неверный логин или пароль")