# storage.py
import os

from core.drivers.filedriver import FileDriver
from core.parsers.fileparser import FileParser


class BaseStorage:
    driver_class = FileDriver
    parser_class = FileParser
    base_dir = 'data'

    def __init__(self, entity, fields):
        self.entity = entity
        self.filename = f'{self.entity}.txt'
        self.fields = fields
        self.driver = self.driver_class(
            f'{self.base_dir}/{self.filename}')
        self.parser = self.parser_class()
        self._build_storage()

    def _build_storage(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        file = self.driver.filename
        if not os.path.exists(file) or os.path.getsize(file) == 0:
            headers = self.parser.serialize_headers(self.fields)
            self.driver.write([headers])

    def all(self):
        raw_rows = self.driver.read_lines()
        return self.parser.parse_rows(raw_rows, self.fields)

    def filter(self, **kwargs):
        result = []
        for item in self.all():
            match = True
            for key, value in kwargs.items():
                if str(item.get(key)) != str(value):
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def save_all(self, data):
        lines = self.parser.serialize_rows(data, self.fields)
        self.driver.write(lines)

    def create(self, data):
        line = self.parser.serialize_row(data, self.fields)
        self.driver.append(line)

