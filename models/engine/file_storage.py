#!/usr/bin/python3
"""just for the FileStorage class."""
import datetime
import json
import os


class FileStorage:

    """serialization and deserialization of the base classes using this class."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns __objects"""
        # TODO: i think this should be a copy()
        return FileStorage.__objects

    def new(self, obj):
        """Sets new obj in __objects dictionary."""
        # TODO: shuld thesee b more precise specifiers really?
        ky = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[ky] = obj

    def save(self):
        """Serialize the __objects to a JSON file."""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as fl:
            dum = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(dum, fl)

    def classes(self):
        """Returns a dictionary all the classes and their ..."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review
                   }
        return classes

    def reload(self):
        """Deserialzes the JSON file into __objects, ie json.parse"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as fl:
            obdict = json.load(fl)
            obdict = {k: self.classes()[v["__class__"]](**v)
                        for k, v in obdict.items()}
            # TODO: overwrite or insert really?
            FileStorage.__objects = obdict

    def attributes(self):
        """Returns the valid attributes and their types for each classname."""
        attr = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attr
