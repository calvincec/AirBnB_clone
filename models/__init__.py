#!/usr/bin/python3
"""enable FileStorage Module to be auto init."""

from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
