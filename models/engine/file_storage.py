#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
                for key in jo:
                    try:
                        class_name = jo[key]["__class__"]
                        if class_name in classes:
                            obj_class = classes[class_name]
                            self.__objects[key] = obj_class(**jo[key])
                        else:
                            raise ValueError(f"Unknown class '{class_name}' \
                            during deserialization.")
                    except Exception as e:
                        print(f"Error while deserializing object with key \
                        '{key}': {e}")
                    except FileNotFoundError:
                        print(f"Error: File '{self.__file_path}' not found \
                        during deserialization.")
                    except json.JSONDecodeError as e:
                        print(f"Error: Invalid JSON format in\
                        '{self.__file_path}': {e}")

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """retrieve just one object"""
        if cls is not None and id is not None:
            return self.__objects.get(cls, {}).get(id)
        else:
            return None

    def count(self, cls=None):
        """counts the number of objects in storage of a certain class
        or all objects in storage when no class given
        """
        if cls is not None:
            return len(self.__objects.get(cls, {}))
        else:
            total_count = 0
            for obj_dict in self.__objects.values():
                total_count += len(obj_dict)
            return total_count()

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
