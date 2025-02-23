# resoursphere/main.py
import os
import typer
from app.subcommands.auth import auth_cmd
from app.authentication import get_user_from_env
from app import config

resoursphere_cmd = typer.Typer()

resoursphere_cmd.add_typer(auth_cmd, name="auth")

@resoursphere_cmd.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    ResourSphere CLI - Manage your AWS resources.
    
    When run without a subcommand, it displays the CLI version and current login status.
    """
    if ctx.invoked_subcommand is None:
        user = get_user_from_env()
        typer.echo(f"ResourSphere CLI v{config.CLI_VERSION}")
        typer.echo("by Roy Sahar")
        typer.echo(f"Configured to use Backend: {config.BACKEND_URL}")
        if user:
            typer.echo(f"Logged in as: {user}")
        else:
            typer.echo("Not logged in. Run 'resoursphere auth login' to log in.")

if __name__ == "__main__":
    resoursphere_cmd()
