#!/usr/bin/env python3
"""
This module provides the Auth class for managing API authentication.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage API authentication.

    Methods:
        require_auth: Determines if a path requires authentication.
        authorization_header: Retrieves the authorization header.
        current_user: Retrieves the current user.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require
                authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the Flask request object.

        Args:
            request: The Flask request object (optional).

        Returns:
            str: The Authorization header if present, None otherwise.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user associated with the Flask request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user, None if not available.
        """
        return None
