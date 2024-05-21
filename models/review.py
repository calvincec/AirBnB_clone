#!/usr/bin/python3
"""Module to get a Review class."""

from models.base_model import BaseModel


class Review(BaseModel):
    """Class for a Review."""
    place_id = ""
    user_id = ""
    text = ""
