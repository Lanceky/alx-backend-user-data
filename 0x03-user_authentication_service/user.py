#!/usr/bin/env python3
"""
This module defines a SQLAlchemy model for the User table.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model representing a table `users` in the database.

    Attributes:
        id (int): The primary key of the user.
        email (str): The email address of the user (non-nullable).
        hashed_password (str): The hashed password of the user (non-nullable).
        session_id (str): The session ID associated with the user (nullable).
        reset_token (str): The reset token for the user (nullable).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
