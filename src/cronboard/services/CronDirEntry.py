class CronDirEntry:
    def __init__(self, name: str, path: str, is_dir: bool):
        self.name: str = name
        self.path: str = path
        self._is_dir: bool = is_dir

    def is_dir(self):
        return self._is_dir
