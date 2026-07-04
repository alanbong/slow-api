# run script or 'python -m unittest discover -s tests -t . -v'
import unittest

if __name__ == "__main__":
    unittest.main(module=None, argv=[
                  "unit", "discover", "-s", "tests", "-t", "."])
