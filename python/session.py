from datetime import time
import asyncio

class Session:
    def __init__(self, session: bool = False, session_ttl: int = 3600):
        self.session = session
        self.session_ttl = session_ttl

    def create_session(self, login, id):
        self.session = True
        while True:
            self.timer_session()
            if self.timer_session() == False:
                self.session = False
                print("Сессия завершина")
                break


    def timer_session(self) -> bool:
        time(1.00)
        self.session_ttl -= 1
        if self.session_ttl > 0:
            return True
        else:
            return False
        