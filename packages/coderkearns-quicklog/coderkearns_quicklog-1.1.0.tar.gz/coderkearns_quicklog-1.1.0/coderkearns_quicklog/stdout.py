from .base import BaseLogger

class StdoutLogger(BaseLogger):
    def log(self, level, *args):
        print("[{}]".format(self.get_level_name(level)), *args)
