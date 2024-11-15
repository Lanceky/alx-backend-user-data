#!/usr/bin/env python3
"""
Auth class module for managing API authentication.
"""

from flask import request
from typing import List, TypeVar
import re


class Auth:
    """
    Auth class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.
        Supports star (*) wildcard at the end of excluded paths.
        """
        if path is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistency
        path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            # Remove trailing slash if exists (to handle star properly)
            excluded_path = excluded_path.rstrip('/')

            # Check if the excluded path ends with a star
            if excluded_path.endswith('*'):
                pattern = excluded_path[:-1]
                if path.startswith(pattern):
                    return False
            else:
                # Add trailing slash for non-star paths
                excluded_path = excluded_path + '/'
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.
        """
        return None