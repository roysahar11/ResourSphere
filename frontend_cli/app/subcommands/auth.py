from app.authentication import (
    save_login_token,
    get_saved_token,
    send_login_request,
    refresh_token_request,
    prompt_for_credentials_and_login,
    logout,
    # whoami_request,
)
import typer
from typing import Optional
import os
import getpass
from app import config

auth_cmd = typer.Typer()


@auth_cmd.command("login")
def login_cmd(
    user: Optional[str] = typer.Option(
        None, "-u", "--user", help="Username for login"),
    one_time: bool = typer.Option(
        False, "-o", help="One-time login (do not save credentials)")
):
    prompt_for_credentials_and_login(user, one_time)
    # if not user:
    #     user = typer.prompt("Enter your username: ")

    # password = getpass.getpass("Enter your password: ")
    # typer.echo(f"Logging in as {user}...")
    # login_response = send_login_request(user, password)
    # token = login_response.get("access_token")
    # if token:
    #     export_login_to_env(token, user)
    #     if not one_time:
    #         save_local_user(user)
    #     typer.echo("Login successful!")
    # else:
    #     typer.echo("Login failed (No token recieved from the server).")


# @auth_commands.command("status")
# def status():
#     """
#     Display the currently logged-in user.
#     """
#     token = get_token_from_env()
#     if not token:
#         typer.echo("Not logged in.")
#         raise typer.Exit()

#     username = whoami_request(token)
#     if username:
#         typer.echo(f"Logged in as: {username}")
#     else:
#         typer.echo("Failed to retrieve user info.")


@auth_cmd.command("logout")
def logout_cmd():
    """
    Log out and clear stored credentials.
    """
    logout()
    # os.environ.pop("RESOURSPHERE_TOKEN", None)
    # os.environ.pop("RESOURSPHERE_USER", None)
    # if os.path.exists(config.LOCAL_USER_FILE):
    #     os.remove(config.LOCAL_USER_FILE)
    # if os.path.exists(config.LOCAL_TOKEN_FILE):
    #     os.remove(config.LOCAL_TOKEN_FILE)
    # typer.echo("Logged out successfully.")


# @auth_cmd.command("refresh")
# def refresh():
#     """
#     Refresh the access token.
#     """
#     token = get_token_from_env()
#     if not token:
#         typer.echo("No token available. Please log in first.")
#         raise typer.Exit()

#     new_token = refresh_token_request(token)
#     if new_token:
#         user = os.environ.get("RESOURSPHERE_USER", "unknown")
#         export_login_to_env(new_token, user)
#         typer.echo("Token refreshed successfully!")
#     else:
#         typer.echo("Token refresh failed.")
