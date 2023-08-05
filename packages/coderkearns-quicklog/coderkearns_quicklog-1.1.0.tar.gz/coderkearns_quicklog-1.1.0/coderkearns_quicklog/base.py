class BaseLogger(object):
    LEVELS = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4,
        "FATAL": 5
    }

    REVERSE_LEVELS = dict((v, k) for k, v in LEVELS.items())

    def __init__(self, level=1):
        if type(level) == str:
            level = self.get_level(level)
        self.level = level

    def log(self, level, *args):
        raise NotImplementedError("Logger must implement log()")

    def _log(self, level, *args):
        if self.level <= level:
            self.log(level, *args)

    def debug(self, *args):
        self._log(self.LEVELS["DEBUG"], *args)

    def info(self, *args):
        self._log(self.LEVELS["INFO"], *args)

    def warning(self, *args):
        self._log(self.LEVELS["WARNING"], *args)

    def error(self, *args):
        self._log(self.LEVELS["ERROR"], *args)

    def critical(self, *args):
        self._log(self.LEVELS["CRITICAL"], *args)

    def fatal(self, *args):
        self._log(self.LEVELS["FATAL"], *args)

    def set_level(self, level):
        if type(level) == str:
            level = self.get_level(level)
        self.level = level

    @classmethod
    def get_level_name(cls, level):
        return cls.REVERSE_LEVELS[level]

    @classmethod
    def get_level(cls, level_name):
        return cls.LEVELS[level_name]
