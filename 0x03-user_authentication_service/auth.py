#!/usr/bin/env python3
"""
Authentication logic for the application.
"""

import bcrypt
import uuid
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Generate a hashed password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID as a string."""
    return str(uuid.uuid4())


class Auth:
    """
    Auth class for managing user authentication.
    Methods:
        register_user: Register a new user.
        valid_login: Validate user login credentials.
        create_session: Create a session for a user.
        get_user_from_session_id: Retrieve a user by session ID.
        destroy_session: Log out a user by destroying their session.
    """
    def __init__(self) -> None:
        """Initialize the Auth instance with a DB instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with an email and password."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for a user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve a user by their session ID."""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Log out a user by destroying their session."""
        self._db.update_user(user_id, session_id=None)
