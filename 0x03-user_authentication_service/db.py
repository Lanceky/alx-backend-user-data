#!/usr/bin/env python3
"""
Database interaction class using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """
    DB class for managing database operations.
    Methods:
        add_user: Adds a new user to the database.
        find_user_by: Finds a user based on specified criteria.
        update_user: Updates attributes of an existing user.
    """
    def __init__(self) -> None:
        """Initialize a new DB instance with an SQLite database."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Return a database session, creating one if necessary."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database.
        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary filters.
        Args:
            kwargs: Filters to apply (e.g., email="user@example.com").
        Returns:
            User: The found User object.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.
        Args:
            user_id (int): The ID of the user to update.
            kwargs: Key-value pairs of attributes to update.
        Raises:
            ValueError: If an invalid attribute is provided.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"{key} is not a valid attribute of User.")
            setattr(user, key, value)
        self._session.commit()
