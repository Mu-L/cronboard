class CronDirEntry:
    def __init__(self, name: str, path: str, is_dir: bool):
        self.name = name
        self.path = path
        self._is_dir = is_dir

    def is_dir(self):
        return self._is_dir
