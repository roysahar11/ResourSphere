# resoursphere/main.py
import os
import typer
from subcommands import auth_commands
import config

resoursphere_client = typer.Typer()

resoursphere_client.add_typer(auth_commands.app, name="auth")

@resoursphere_client.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    ResourSphere CLI - Manage your AWS resources.
    
    When run without a subcommand, it displays the CLI version and current login status.
    """
    user = auth_commands.get_user_from_env()
    typer.echo(f"ResourSphere CLI v{config.CLI_VERSION}")
    typer.echo("by Roy Sahar")
    typer.echo(f"Configured to use Backend: {config.BACKEND_URL}")
    if user:
        typer.echo(f"Logged in as: {user}")
    else:
        typer.echo("Not logged in. Run 'resoursphere auth login' to log in.")

if __name__ == "__main__":
    resoursphere_client()
