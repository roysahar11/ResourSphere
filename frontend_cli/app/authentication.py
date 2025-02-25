# resoursphere/commands/auth.py
import os
import getpass
from typing import Optional
import typer
from app import config
import requests
from app.api_requests import send_login_request

def save_login_token(token: str, username: str):
    os.environ[config.TOKEN_ENV_VAR] = token
    os.environ[config.USER_ENV_VAR] = username
    config.save_login_token(token)

def get_saved_token() -> str:
    token = (
        os.environ.get(config.TOKEN_ENV_VAR)
        or config.read_login_token()
        or ""
    )
    return token


def get_logged_in_user() -> str:
    if get_saved_token():
        return (
            os.environ.get(config.USER_ENV_VAR, "")
            or config.read_username()
            or ""
        )
    else:
        logout()
        return ""

def logout():
    os.environ.pop(config.TOKEN_ENV_VAR, None)
    os.environ.pop(config.USER_ENV_VAR, None)
    config.save_login_token("")
    config.save_username("")
    if os.path.exists(config.LOCAL_USER_PERMISSIONS_FILE):
        os.remove(config.LOCAL_USER_PERMISSIONS_FILE)
    if os.path.exists(config.LOCAL_TOKEN_EXPIRATION_FILE):
        os.remove(config.LOCAL_TOKEN_EXPIRATION_FILE)


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

def prompt_for_credentials_and_login(user=None, one_time=False) -> str:
    """
    Prompt the user to enter password and/or username (if not 
    provided to the function).
    """
    if not user:
        user = typer.prompt("Enter your username")

    password = getpass.getpass("Enter your password: ")
    typer.echo(f"Logging in as {user}...")
    login_response = send_login_request(user, password)
    token = login_response.get("access_token")
    token_expires_at = login_response.get("expires_at_utc")
    user_permissions = login_response.get("user_permissions")
    if token:
        save_login_token(token, user)
        if not one_time:
            config.save_username(user)
        if user_permissions: config.save_user_permissions(user_permissions)
        if token_expires_at: config.save_token_expiration(token_expires_at)
        typer.echo("Login successful!")
        return token
    else:
        typer.echo("Login failed (No token recieved from the server).")
        raise typer.Exit()

def generate_authentication_header():
    token = get_saved_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        user = get_logged_in_user()
        if not user:
            login = typer.confirm(
                "You are not logged in to the system. Do you want to login now?"
            )
            if not login:
                typer.echo(
                    "Action canceled. You can log in using 'resoursphere auth login'"
                )
                raise typer.Exit()
        token = prompt_for_credentials_and_login(user)
        return {"Authorization": f"Bearer {token}"}

def get_current_user_permissions() -> dict:
    return config.read_user_permissions()

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