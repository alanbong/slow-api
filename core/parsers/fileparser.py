# fileparser.py
class FileParser:
    separator = "::"

    def parse_rows(self, rows, fields):
        parsed_data = []
        for line in rows[1:]:
            values = line.split(self.separator)
            clean_values = []
            for value in values:
                if value == "None":
                    clean_values.append(None)
                else:
                    clean_values.append(value)

            item = dict(zip(fields, clean_values))
            parsed_data.append(item)

        return parsed_data

    def serialize_headers(self, fields):
        return self.separator.join(fields)

    def serialize_row(self, data: dict, fields):
        line = []
        for field in fields:
            value = data.get(field)
            if value is None:
                value = "None"
            line.append(str(value))

        return self.separator.join(line)

    def serialize_rows(self, data: list, fields):
        rows = []
        rows.append(self.serialize_headers(fields))
        for item in data:
            rows.append(self.serialize_row(item, fields))

        return rows
