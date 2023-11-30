#!/usr/bin/python3
"""Console Module"""
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update', 'create']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax."""
        if '.' not in line or '(' not in line or ')' not in line:
            return line

        try:
            pline = line[:]
            _cls = pline[:pline.find('.')]
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')
                _id = pline[0].replace('\"', '')
                _args = (
                    pline[2].replace(',', '')
                    if pline[2] and (pline[2][0] == '{' and pline[2][-1] == '}')
                    else pline[2]
                )

            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, arg):
        """Create an object of any class"""
        try:
            if not arg:
                raise SyntaxError("** class name missing **")

            arg_list = arg.split(" ")
            class_name = arg_list[0]

            if class_name not in HBNBCommand.classes:
                raise NameError("** class doesn't exist **")

            kw = {}
            for arg in arg_list[1:]:
                arg_splited = arg.split("=")
                attr_name, attr_val = arg_splited[0], eval(arg_splited[1])

                if type(attr_val) is str:
                    attr_val = attr_val.replace("_", " ").replace('"', '\\"')

                kw[attr_name] = attr_val

            new_instance = HBNBCommand.classes[class_name](**kw)
            new_instance.save()
            print(new_instance.id)

        except SyntaxError as e:
            print(e)
        except NameError as e:
            print(e)

    def help_create(self):
        """Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """Method to show an individual object"""
        try:
            if not args:
                raise SyntaxError("** class name missing **")

            new = args.partition(" ")
            c_name, c_id = new[0], new[2]

            if c_id and ' ' in c_id:
                c_id = c_id.partition(' ')[0]

            if not c_name:
                raise SyntaxError("** class name missing **")

            if c_name not in HBNBCommand.classes:
                raise NameError("** class doesn't exist **")

            if not c_id:
                raise SyntaxError("** instance id missing **")

            key = f"{c_name}.{c_id}"
            print(storage.all().get(key, "** no instance found **"))

        except SyntaxError as e:
            print(e)
        except NameError as e:
            print(e)

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        try:
            if not args:
                raise SyntaxError("** class name missing **")

            new = args.partition(" ")
            c_name, c_id = new[0], new[2]
            if c_id and ' ' in c_id:
                c_id = c_id.partition(' ')[0]

            if not c_name:
                raise SyntaxError("** class name missing **")

            if c_name not in HBNBCommand.classes:
                raise NameError("** class doesn't exist **")

            if not c_id:
                raise SyntaxError("** instance id missing **")

            key = f"{c_name}.{c_id}"
            storage.delete(key)
            storage.save()

        except SyntaxError as e:
            print(e)
        except NameError as e:
            print(e)

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        try:
            print_list = []

            if args:
                args = args.split(' ')[0]
                if args not in HBNBCommand.classes:
                    raise NameError("** class doesn't exist **")

                for k, v in storage.all(HBNBCommand.classes[args]).items():
                    print_list.append(str(v))
            else:
                for k, v in storage.all().items():
                    print_list.append(str(v))
            print(print_list)

        except NameError as e:
            print(e)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        try:
            if not args:
                raise SyntaxError("** class name missing **")

            count = sum(1 for k in storage.all() if k.split('.')[0] == args)
            print(count)

        except SyntaxError as e:
            print(e)

    def help_count(self):
        """Usage: count <class_name>"""
        print("Count current number of class instances")

    def do_update(self, args):
        """Updates a certain object with new info"""
        try:
            args = args.partition(" ")
            c_name, c_id = args[0], args[2]
            key = f"{c_name}.{c_id}"

            if not c_name:
                raise SyntaxError("** class name missing **")

            if c_name not in HBNBCommand.classes:
                raise NameError("** class doesn't exist **")

            if not c_id:
                raise SyntaxError("** instance id missing **")

            if key not in storage.all():
                raise KeyError("** no instance found **")

            if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
                kwargs = eval(args[2])
                args = [item for sublist in kwargs.items() for item in sublist]
            else:
                args = args[2]
                if args and args[0] == '\"':
                    second_quote = args.find('\"', 1)
                    att_name = args[1:second_quote]
                    args = args[second_quote + 1:]

                args = args.partition(' ')

                if not att_name and args[0] != ' ':
                    att_name = args[0]

                if args[2] and args[2][0] == '\"':
                    att_val = args[2][1:args[2].find('\"', 1)]

                if not att_val and args[2]:
                    att_val = args[2].partition(' ')[0]

                args = [att_name, att_val]

            new_dict = storage.all()[key]

            for i, att_name in enumerate(args):
                if i % 2 == 0:
                    att_val = args[i + 1]

                    if not att_name:
                        raise SyntaxError("** attribute name missing **")

                    if not att_val:
                        raise SyntaxError("** value missing **")

                    if att_name in HBNBCommand.types:
                        att_val = HBNBCommand.types[att_name](att_val)

                    setattr(new_dict, att_name, att_val)

            new_dict.save()

        except SyntaxError as e:
            print(e)
        except NameError as e:
            print(e)
        except KeyError as e:
            print(e)

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
