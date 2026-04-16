# filedriver.py
class FileDriver:
    def __init__(self, filename):
        self.filename = filename

    def _open(self, mode):
        return open(self.filename, mode, encoding='utf-8')

    def read(self):
        with self._open('r') as f:
            return f.read()

    def read_lines(self):
        with self._open('r') as f:
            return [line.strip() for line in f if line.strip()]

    def append(self, line):
        with self._open('a') as f:
            f.write(line + '\n')

    def write(self, lines):
        with self._open('w') as f:
            for line in lines:
                f.write(line + '\n')
