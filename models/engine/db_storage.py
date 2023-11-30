#!/usr/bin/python3
"""
This module defines a class to manage database storage for hbnb clone.
"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DBStorage class"""

    __engine = None
    __session = None

    def __init__(self):
        """Constructor"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""

        object_dict = {}
        classes = [User, State, City, Amenity, Place, Review]

        if cls:
            objects = self.__session.query(cls).all()

            for o in objects:
                object_dict[type(o).__name__ + "." + o.id] = o
        else:
            for elem in classes:
                objects = self.__session.query(elem).all()
                for o in objects:
                    object_dict[type(o).__name__ + "." + o.id] = o

        return object_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creating tables and the session"""
        Base.metadata.create_all(self.__engine)
        sessionn_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sessionn_factory)
        self.__session = Session()

    def close(self):
        """Closing session"""
        self.__session.close()
