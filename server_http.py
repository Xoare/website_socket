import socket
import sqlite3
import random
import os
from SQLite3.database import DataBase as DB 
from python.session import Session as SESS     

class HTTPServer:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.server_socket = False
        self.client_info = []
        self.database = None
        self.templates_dir = "templates"
        
    """Доступ к сайту"""
    def home_page(self, headers, client_socket):
        html_content = self.readHTMLstart("home.html")
        if html_content:
            client_socket.sendall(headers + html_content)
            return True
        return False

    """Инициализация базы данных"""
    def set_database(self, database):
        self.database = database
    
    """Контроль методов HTTP"""
    def control_methods_http(self, request_data, client_address):
        print(client_address)
        response_method = request_data.splitlines()[0]
        if response_method.startswith("POST"):
            return self.processing_post_method(request_data)
        return None, None
    
    """Обработка форм из POST запроса"""
    def processing_post_method(self, request_data):
        if request_data.split(" ")[1] == "/register":
            try:
                body = request_data.split("\r\n\r\n")[1]
                params = body.split("&")
                data = {}
                for param in params:
                    if "=" in param:
                        key, value = param.split("=")
                        data[key] = value
                name, password = data.get("name"), data.get("password")
                self.database.InsertUserId(name, password)
                return "home", None
            except:
                return None, None
            
        if request_data.split(" ")[1] == "/submit":
            try:
                body = request_data.split("\r\n\r\n")[1]
                params = body.split("&")    
                data = {}
                for param in params:
                    if "=" in param:
                        key, value = param.split("=")
                        data[key] = value
                name, password = data.get("name"), data.get("password")
                result = self.database.ExamenationUser(name, password)
                if result:
                    return "home", None
                else:
                    return None, "Неверный логин или пароль"
            except:
                return None, "Неверный логин или пароль"
                
    """Чтение файла HTML"""
    def readHTMLstart(self, file_html):
        try:
           file_path = os.path.join(self.templates_dir, file_html)
           with open(file_path, 'rb') as file:
               return file.read()
        except FileNotFoundError:
            print(f"Файл {file_html} не найден")
            pass
        except Exception as ex:
            print(f"Ошибка обработки файла: {ex}")
            pass

    """Запуск сокета сервера"""
    def StartSocketServer(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        print(f"Сервер запущен на http://{self.host}:{self.port}")
        print(f"Директория с шаблонами: {os.path.abspath(self.templates_dir)}")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                try:
                    print(f"Установлено соединение с пользователем {client_address}")
                    
                    request_data = client_socket.recv(1024).decode('utf-8')
                    
                    if request_data:
                        print(request_data.splitlines()[0])
                        page_type, error = self.control_methods_http(request_data, client_address)
                        print(page_type, error)
                    else:
                        print("Нет данных")
                    
                    headers = (
                        b"HTTP/1.1 200 OK\r\n"
                        b"Content-Type: text/html; charset=utf-8\r\n"
                        b"Connection: close\r\n"
                        b"\r\n"
                    )
                    
                    if page_type == "home":
                        self.home_page(headers, client_socket)
                    else:
                        html_content = self.readHTMLstart("authentification_user.html")
                        client_socket.sendall(headers + html_content)
                        
                except Exception as ex:
                    print(f"Попытка соединения с пользователем {client_address} завершилась неудачно по причине {ex}")
                finally:
                    client_socket.close()
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            if self.server_socket:
                self.server_socket.close()
    

if __name__ == "__main__":
    db_connection = sqlite3.connect('users.db')
    database = DB(db_connection)
    database.InitDataBase()

    session = SESS()

    server = HTTPServer('0.0.0.0', 8080)
    server.set_database(database)
    server.StartSocketServer()