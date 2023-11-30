#!/usr/bin/python3
"""
DBStorage module for the HBNB project
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
# Import other models like User, Place, State, City, etc.

class DBStorage:
    """
    DBStorage class for HBNB project
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes DBStorage instance
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects depending on the class name
        """
        # Implementation of all
