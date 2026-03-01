import threading
import time

class Counter:
    def __init__(self, start_value):
        self.start_value = start_value
        self.thread = threading.Thread(target = self.run_, daemon=True)
        self.thread.start()

