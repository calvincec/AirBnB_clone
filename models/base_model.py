#!/usr/bin/python3
"""The Module for base class
	for the AirBnB clone console only.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:

    """just for base model of the entire object hierarchy order in the project."""

    def __init__(self, *args, **kwargs):
        """Initializes a Base instance to the class.

        Args:
            - *args: contains all arguments
            - **kwargs: a dict to which all key value pairs
						of the instance are stored.
        """

        if kwargs is not None and kwargs != {}:
            for objekt in kwargs:
                if objekt == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif objekt == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[objekt] = kwargs[objekt]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns the string output of the class
        	in form of JSON file."""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """changes the updated_at attribute
        to the present date and time."""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns an instance in form of a dictionary."""

        dic = self.__dict__.copy()
        dic["__class__"] = type(self).__name__
        dic["created_at"] = dic["created_at"].isoformat()
        dic["updated_at"] = dic["updated_at"].isoformat()
        return dic
