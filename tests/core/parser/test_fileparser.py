# test_fileparser.py
import unittest

from core.parsers.fileparser import FileParser

EXPECTED_ATTRIBUTES = {
    '.separator': (
        '.separator - string used to separate fields within a single line'),
}
EXPECTED_METHODS = {
    'parse_rows': (
        '.parse_rows(rows, fields) - skips the header and converts rows '
        'into a list of dictionaries'),
    'serialize_headers': (
        '.serialize_headers(fields) - joins field names into '
        'single header string'),
    'serialize_row': (
        '.serialize_row(data, fields) - converts a dictionary into '
        'separated string'),
    'serialize_rows': (
        '.serialize_rows(data, fields) - converts list of dicts '
        'into a list of strings (including header)'),
}


class TestFileParser(unittest.TestCase):
    """
    FileParser is module for serializer and parse data.
    """

    def setUp(self):
        self.parser = FileParser()

        self.public_attrs = [
            name for name
            in dir(self.driver)
            if not name_startswith('_')
        ]

    def test_1_class_exists_and_have_necessary_attributes(self):
        """Class exists in module and have necessary attributes."""

        print('Class FileParser serves to serialize data\n')

        actual_attrs = [
            name for name
            in self.public_attrs
            if not callable(getattr(self.driver, name))
        ]

        print(f'Class have {len(actual_attrs)} attributes:')

        self.assertEqual(
            len(EXPECTED_ATTRIBUTES),
            len(actual_attrs),
            msg=(
                f'Expected {len(EXPECTED_ATTRIBUTES)} attributes,'
                f'but found {len(actual_attrs)}: {actual_attrs}'
            ),
        )

        for attr, description in EXPECTED_ATTRIBUTES.items():
            with self.subTest(attr=attr):
                has_attr = hasattr(self.driver, attr)
                if has_attr:
                    print(f'\n    {description}')

                self.assertTrue(
                    has_attr, msg='FileParser attribute .{attr} is missing.'
                )

