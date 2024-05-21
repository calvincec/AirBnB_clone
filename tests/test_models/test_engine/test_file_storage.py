#!/usr/bin/python3
"""
Only to test storage element
"""
from datetime import datetime
import unittest
from time import sleep
import json
from models.engine.file_storage import FileStorage


class test_fileStorage(unittest.TestCase):
    """Test FileStorage class itself"""
    def test_instances(self):
        """check if instantation works"""
        ob = FileStorage()
        self.assertIsInstance(ob, FileStorage)

    def test_docs(self):
        """Test docstrings for class and methods"""
        self.assertIsNotNone(FileStorage.all)
        self.assertIsNotNone(FileStorage.new)
        self.assertIsNotNone(FileStorage.save)
        self.assertIsNotNone(FileStorage.reload)

    if __name__ == '__main__':
        unittest.main()
