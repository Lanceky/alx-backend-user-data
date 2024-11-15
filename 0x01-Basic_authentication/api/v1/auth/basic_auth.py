#!/usr/bin/env python3
"""
BasicAuth module for managing basic authentication.
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar, Tuple
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    Implements Basic Authentication methods.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """
        Decodes the Base64 authorization header.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user credentials from decoded Base64 authorization header.
        Allows for passwords containing ':' character.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        # Split only on first occurrence of ':' to allow ':' in password
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return (email, pwd)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.
        Complete Basic authentication process.
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)
        if not base64_auth:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if not decoded_auth:
            return None

        email, pwd = self.extract_user_credentials(decoded_auth)
        if not email or not pwd:
            return None

        return self.user_object_from_credentials(email, pwd)