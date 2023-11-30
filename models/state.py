#!/usr/bin/python3
"""
State module for the HBNB project
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """
    State class for HBNB project
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    
    if models.storage_t == 'db':
        cities = relationship('City', backref='state', cascade='all, delete, delete-orphan')
    else:
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equals to the current State.id
            """
            return [city for city in models.storage.all('City').values() if city.state_id == self.id]
