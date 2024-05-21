#!/usr/bin/python3
"""The user class module for the HBNB project"""
from models.base_model import BaseModel


class User(BaseModel):
    """The user mnow."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
