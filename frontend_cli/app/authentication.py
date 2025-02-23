# resoursphere/commands/auth.py
import os
import getpass
from typing import Optional
import typer
from app import config
import requests


def save_local_user(username: str):
    """Save the username locally."""
    with open(config.LOCAL_USER_FILE, "w") as user_file:
        user_file.write(username)


def load_local_user() -> str:
    """Load the locally saved username, if it exists."""
    if os.path.exists(config.LOCAL_USER_FILE):
        with open(config.LOCAL_USER_FILE, "r") as user_file:
            return user_file.read().strip()
    return ""


def export_login_to_env(token: str, username: str):
    os.environ[config.TOKEN_ENV_VAR] = token
    os.environ[config.USER_ENV_VAR] = username


def get_token_from_env() -> str:
    return os.environ.get(config.TOKEN_ENV_VAR, "")


def get_user_from_env() -> str:
    return os.environ.get(config.USER_ENV_VAR, "")


def send_login_request(username: str, password: str) -> str:
    """Send a login request to the backend."""
    url = f"{config.BACKEND_URL}/auth/login"
    try:
        response = requests.post(url, json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            # typer.echo(response.status_code)
            typer.echo(f"Login failed: {response.text}")
            typer.echo(f"HTTP Status code: {response.status_code}")
            return {}
    except Exception as e:
        # typer.echo(response.status_code)
        typer.echo(f"Error during login: {e}")
        return {}


def refresh_token_request(token: str) -> str:
    """Call the backend to refresh the token."""
    url = f"{config.BACKEND_URL}/auth/refresh"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token", "")
        else:
            typer.echo(f"Token refresh failed: {response.text}")
            return ""
    except Exception as e:
        typer.echo(f"Error during token refresh: {e}")
        return ""


# def whoami_request(token: str) -> str:
#     """Call the backend 'whoami' endpoint to get the current user."""
#     url = f"{config.BACKEND_URL}/auth/me"
#     headers = {"Authorization": f"Bearer {token}"}
#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             return data.get("username", "")
#         else:
#             typer.echo(f"Whoami request failed: {response.text}")
#             return ""
#     except Exception as e:
#         typer.echo(f"Error during whoami request: {e}")
#         return ""