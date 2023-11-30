#!usr/bin/python3
""" Test console.py """
import unittest
from unittest.mock import patch
from io import StringIO
import os
import json
from console import HBNBCommand
from models.engine.db_storage import DBStorage


class TestConsole(unittest.TestCase):
    """ This will test the console """

    @classmethod
    def setUpClass(cls):
        """ Setup for the test """
        cls.consol = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """ At the end of the test this will tear it down """
        del cls.consol

    def tearDown(self):
        """ Remove temporary file (file.json) created as a result """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_docstrings_in_console(self):
        """ Checking for docstrings """
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """ Test empty line input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """ Test create command input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")

    def test_show(self):
        """ Test show command input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_destroy(self):
        """ Test destroy command input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_update(self):
        """ Test update command input """
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update sldkfjsl")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_create_dbstorage(self):
        """Test create command with DBStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        self.assertIn("User", f.getvalue())

    def test_show_dbstorage(self):
        """Test show command with DBStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        my_id = f.getvalue()[f.getvalue().find('(')+1:f.getvalue().find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show User {}".format(my_id))
        self.assertIn("User", f.getvalue())

    def test_destroy_dbstorage(self):
        """Test destroy command with DBStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        my_id = f.getvalue()[f.getvalue().find('(')+1:f.getvalue().find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User {}".format(my_id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        self.assertNotIn("User", f.getvalue())

    def test_all_dbstorage(self):
        """Test all command with DBStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all")
        self.assertIn("User", f.getvalue())
        self.assertIn("BaseModel", f.getvalue())
        self.assertIn("State", f.getvalue())
        self.assertIn("City", f.getvalue())
        self.assertIn("Place", f.getvalue())
        self.assertIn("Amenity", f.getvalue())
        self.assertIn("Review", f.getvalue())

    def test_update_dbstorage(self):
        """Test update command with DBStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        my_id = f.getvalue()[f.getvalue().find('(')+1:f.getvalue().find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User {} name 'Betty'".format(my_id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        self.assertIn("'name': 'Betty'", f.getvalue())

    def test_create_filestorage(self):
        """Test create command with FileStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        self.assertIn("User", f.getvalue())

    def test_show_filestorage(self):
        """Test show command with FileStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        my_id = f.getvalue()[f.getvalue().find('(')+1:f.getvalue().find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show User {}".format(my_id))
        self.assertIn("User", f.getvalue())

    def test_destroy_filestorage(self):
        """Test destroy command with FileStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        my_id = f.getvalue()[f.getvalue().find('(')+1:f.getvalue().find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User {}".format(my_id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        self.assertNotIn("User", f.getvalue())

    def test_all_filestorage(self):
        """Test all command with FileStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create State")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create City")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Place")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Amenity")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create Review")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all")
        self.assertIn("User", f.getvalue())
        self.assertIn("BaseModel", f.getvalue())
        self.assertIn("State", f.getvalue())
        self.assertIn("City", f.getvalue())
        self.assertIn("Place", f.getvalue())
        self.assertIn("Amenity", f.getvalue())
        self.assertIn("Review", f.getvalue())

    def test_update_filestorage(self):
        """Test update command with FileStorage"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        my_id = f.getvalue()[f.getvalue().find('(')+1:f.getvalue().find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("update User {} name 'Betty'".format(my_id))
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all User")
        self.assertIn("'name': 'Betty'", f.getvalue())


if __name__ == "__main__":
    unittest.main()
