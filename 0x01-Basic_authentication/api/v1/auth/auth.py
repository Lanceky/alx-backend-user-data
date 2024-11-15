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
        if path is None:
            return True
        if not excluded_paths:  # Checks if excluded_paths is None or empty
            return True

        # Normalize the path by ensuring it always ends with a slash for consistency
        normalized_path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            # Normalize the excluded_path as well
            normalized_excluded_path = excluded_path \
                if excluded_path.endswith('/') else excluded_path + '/'

            if normalized_path.startswith(normalized_excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the Flask request object.

        Args:
            request: The Flask request object (optional).

        Returns:
            str: The Authorization header if present, None otherwise.
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user associated with the Flask request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user, None if not available.
        """
        return None
