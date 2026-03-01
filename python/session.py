import time
import uuid
import hashlib
import sqlite3
from SQLite3.database import DataBase as DB 

class Session:
    def __init__(self, db_connection=None, session: bool = False, session_ttl: int = 3600): 
        self.session = session
        self.session_ttl = session_ttl
        self.session_id = None
        self.db_connection = db_connection 

    def create_session(self, login):
        self.session = True
        self.session_id = str(uuid.uuid4())
        print(self.session_id)
        self.session_id_hash = hashlib.sha256(self.session_id.encode()).hexdigest()
        print(self.session_id_hash)
        print(f"Сессия {self.session_id_hash} получила свой срок жизни у пользователя {login}")
        self.create_at = time.time()
        print(self.create_at)


        DB(self.db_connection).create_session_database(login, self.session_id_hash, self.session)
    
    async def examenation_session(self):
        print(self.create_at, end="\r")
        if self.session_ttl <= 0:
            print(f"{self.session_id} отправлена на удаление")