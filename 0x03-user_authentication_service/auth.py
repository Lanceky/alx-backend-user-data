#!/usr/bin/env python3
"""
Authentication module for handling user authentication
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash a password with salt using bcrypt
    Args:
        password (str): The password to hash
    Returns:
        bytes: The hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID
    Returns:
        str: String representation of new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with authentication database"""

    def __init__(self):
        """Initialize a new Auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        Args:
            email (str): User's email
            password (str): User's password
        Returns:
            User: Newly created user object
        Raises:
            ValueError: If user already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials
        Args:
            email (str): User's email
            password (str): User's password
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session for user
        Args:
            email (str): User's email
        Returns:
            str: Session ID if user exists
            None: If user doesn't exist
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user from session ID
        Args:
            session_id (str): Session ID
        Returns:
            User: User object if found
            None: If session ID is None or no user found
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user session
        Args:
            user_id (int): User ID
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token
        Args:
            email (str): User's email
        Returns:
            str: Reset token
        Raises:
            ValueError: If user doesn't exist
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password
        Args:
            reset_token (str): Reset token
            password (str): New password
        Raises:
            ValueError: If reset token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                               hashed_password=hashed_password,
                               reset_token=None)
        except NoResultFound:
            raise ValueError
