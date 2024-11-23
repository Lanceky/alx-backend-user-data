#!/usr/bin/env python3
"""
User model definition for SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model that maps to the 'users' table.
    Attributes:
        id (int): The primary key.
        email (str): The user's email address (unique).
        hashed_password (str): The hashed password for the user.
        session_id (str): Session ID for the user (optional).
        reset_token (str): Reset token for password resets (optional).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
