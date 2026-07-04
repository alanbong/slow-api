# test_filedriver.py
import unittest
from unittest.mock import patch, mock_open

from core.drivers.filedriver import FileDriver


EXPECTED_ATTRIBUTES = {
    '.filename': '.filename - path to file with extension',
}
EXPECTED_METHODS = {
    'read': '.read() - extracts entire file content as single string',
    'read_lines': '.read_lines() - extract list of stings',
    'write': '.write(lines) - overwrites file with new data',
    'append': '.append(line) - adds line in the end of file',
}


class TestFileDriver(unittest.TestCase):
    """
    FileDriver is module for operations on file.
    """

    def setUp(self):
        self.filename = 'fake_file.txt'
        self.driver = FileDriver(self.filename)

        self.public_attrs = [
            name for name
            in dir(self.driver)
            if not name.startswith('_')
        ]

    def test_1_class_exists_and_have_necessary_attributes(self):
        """Class exists in module and have necessary attributes."""

        print('Class FileDriver serves to work with text files on disk.\n')

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
                    has_attr, msg='FileDriver attribute .{attr} is missing.'
                )

    def test_2_class_have_necessary_methods(self):
        """Class have necassary methods"""

        actual_methods = [
            name for name
            in self.public_attrs
            if callable(getattr(self.driver, name))
        ]

        print(f'\nClass have {len(actual_methods)} methods:')

        self.assertEqual(
            len(EXPECTED_METHODS),
            len(actual_methods),
            msg=(
                f'Expected {len(EXPECTED_METHODS)} methods,'
                f'but found {len(actual_methods)}: {actual_methods}'
            ),
        )

        for method, description in EXPECTED_METHODS.items():
            with self.subTest(method=method):
                attr = getattr(self.driver, method, None)
                exists = attr is not None and callable(attr)
                self.assertTrue(exists, msg=f'Method .{method}() is missing')

    def test_3_read(self):
        """Test read method returns correct content."""
        print(f'\n    {EXPECTED_METHODS['read']}')

        content = "line1\nline2"
        with patch('builtins.open', mock_open(read_data=content)):
            result = self.driver.read()
            self.assertEqual(result, content)

    def test_4_read_lines(self):
        """Test read_lines filters empty lines and strips content."""
        print(f'\n    {EXPECTED_METHODS['read_lines']}')

        content = "  line1  \n\n  line2  \n  "
        with patch("builtins.open", mock_open(read_data=content)):
            result = self.driver.read_lines()
            self.assertEqual(result, ["line1", "line2"])

    def test_5_append(self):
        """Test append method writes line with newline."""
        print(f'\n    {EXPECTED_METHODS['append']}')

        with patch("builtins.open", mock_open()) as mocked_file:
            self.driver.append("new_line")
            mocked_file().write.assert_called_once_with("new_line\n")

    def test_6_write(self):
        """Test write method handles list of strings."""
        print(f'\n    {EXPECTED_METHODS['write']}')

        lines = ["one", "two"]
        with patch("builtins.open", mock_open()) as mocked_file:
            self.driver.write(lines)
            self.assertEqual(mocked_file().write.call_count, len(lines))
