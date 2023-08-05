from .base import BaseLogger

class MemoryLogger(BaseLogger):
    def __init__(self, level=1):
        super().__init__(level)
        self.logs = []

    def log(self, level, *args):
        level_name = self.get_level_name(level)
        self.logs.append([level_name, *args])

    def get_logs(self):
        return self.logs
