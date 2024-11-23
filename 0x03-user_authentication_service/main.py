#!/usr/bin/env python3
"""
End-to-end integration tests for the authentication service.
"""

import requests


BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user.
    Assert that the response status code is 200 and the response payload matches expectations.
    """
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}, f"Unexpected response payload: {response.json()}"


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.
    Assert that the response status code is 401.
    """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, f"Unexpected status code: {response.status_code}"


def log_in(email: str, password: str) -> str:
    """
    Log in a user with the correct credentials.
    Assert that the response status code is 200 and the response payload matches expectations.
    Return the session ID.
    """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert "email" in data and "message" in data, f"Unexpected response payload: {data}"
    assert data["email"] == email and data["message"] == "logged in", f"Unexpected response payload: {data}"
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Attempt to access the profile endpoint without being logged in.
    Assert that the response status code is 403.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Unexpected status code: {response.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Access the profile endpoint while logged in.
    Assert that the response status code is 200 and the response payload matches expectations.
    """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert "email" in data, f"Unexpected response payload: {data}"


def log_out(session_id: str) -> None:
    """
    Log out the user by invalidating the session.
    Assert that the response status code is 200.
    """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"


def reset_password_token(email: str) -> str:
    """
    Request a password reset token for the user.
    Assert that the response status code is 200 and the response payload contains a reset token.
    Return the reset token.
    """
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert "reset_token" in data, f"Unexpected response payload: {data}"
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password using a reset token.
    Assert that the response status code is 200 and the response payload matches expectations.
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}, f"Unexpected response payload: {response.json()}"


# Integration Test
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
