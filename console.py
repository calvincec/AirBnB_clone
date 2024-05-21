#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def parse(arg):
    curlys = re.search(r"\{(.*?)\}", arg)
    brcks = re.search(r"\[(.*?)\]", arg)
    if curlys is None:
        if brcks is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lxr = split(arg[:brcks.span()[0]])
            retli = [i.strip(",") for i in lxr]
            retli.append(brcks.group())
            return retli
    else:
        lxr = split(arg[:curlys.span()[0]])
        retli = [i.strip(",") for i in lxr]
        retli.append(curlys.group())
        return retli


class HBNBCommand(cmd.Cmd):
    """now its the HolbertonBnB thing.

    Attributes:
        prompt (str): The command prmpt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """nothing done for empty line"""
        pass

    def default(self, arg):
        """Default if input is not recognized."""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        matching = re.search(r"\.", arg)
        if matching is not None:
            argn = [arg[:matching.span()[0]], arg[matching.span()[1]:]]
            matching = re.search(r"\((.*?)\)", argn[1])
            if matching is not None:
                command = [argn[1][:matching.span()[0]], matching.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argn[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """to exit the program."""
        return True

    def do_EOF(self, arg):
        """to exit the program on EOF."""
        print("")
        return True

    def do_create(self, arg):
        """make a new class 
        	instance and display its class id.
        """
        argn = parse(arg)
        if len(argn) == 0:
            print("** class name missing **")
        elif argn[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argn[0])().id)
            storage.save()

    def do_show(self, arg):
        """show the class instance of a given id.   """
        argn = parse(arg)
        obj_dict = storage.all()
        if len(argn) == 0:
            print("** class name missing **")
        elif argn[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argn) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argn[0], argn[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(argn[0], argn[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argn = parse(arg)
        obj_dict = storage.all()
        if len(argn) == 0:
            print("** class name missing **")
        elif argn[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argn) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argn[0], argn[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(argn[0], argn[1])]
            storage.save()

    def do_all(self, arg):
        """get all instances of a class or all classes."""
        argn = parse(arg)
        if len(argn) > 0 and argn[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argn) > 0 and argn[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argn) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """get the count of instances of a class."""
        argn = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argn[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """upate an instance of a class with new info."""
        argn = parse(arg)
        obj_dict = storage.all()

        if len(argn) == 0:
            print("** class name missing **")
            return False
        if argn[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argn) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argn[0], argn[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(argn) == 2:
            print("** attribute name missing **")
            return False
        if len(argn) == 3:
            try:
                type(eval(argn[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argn) == 4:
            obj = obj_dict["{}.{}".format(argn[0], argn[1])]
            if argn[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argn[2]])
                obj.__dict__[argn[2]] = valtype(argn[3])
            else:
                obj.__dict__[argn[2]] = argn[3]
        elif type(eval(argn[2])) == dict:
            obj = obj_dict["{}.{}".format(argn[0], argn[1])]
            for k, v in eval(argn[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
