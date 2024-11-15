#!/usr/bin/env python3
"""
This module provides the Auth class for managing API authenticaiton
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage API authentication.

    Methods:
        require_auth: Determines if a path requires authentication.
        authorization_header: retrieves the authorization header
        current_user: Retrieves teh current user.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication

        Args:
            path: The path to check
            excluded_paths: A list of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the flask request object

        Args:
            request: The Flask request object

        Returns:
            str: The authorization if present, None otherwise.
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the curent user associated with the flask request.

        Args:
            request: The flask request object.

        Returns:
            TypeVar('user'): The current user, None if not available
        """
        return None