from .base import BaseLogger

class FileLogger(BaseLogger):
    def __init__(self, path, level=1):
        super().__init__(level)
        self.path = path
        self.file = None

    def open(self):
        if not self.file:
            self.file = open(self.path, "a")

    def close(self):
        if self.file:
            self.file.close()
            self.file = None

    def log(self, level, *args):
        if not self.file:
            self.open()
        self.file.write("[{}] {}\n".format(self.get_level_name(level), " ".join(args)))
        self.file.flush()
