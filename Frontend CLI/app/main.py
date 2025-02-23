# resoursphere/main.py
import os
import typer
from resoursphere.commands import auth
from resoursphere.utils import get_token

app = typer.Typer()

app.add_typer(auth.app, name="auth")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    ResourSphere CLI - Manage your AWS resources.
    
    When run without a subcommand, it displays the CLI version and current login status.
    """
    VERSION = "1.0.0"
    token = get_token()
    if token:
        user = os.environ.get("RESOURSPHERE_USER", "unknown")
        typer.echo(f"ResourSphere CLI v{VERSION}")
        typer.echo(f"Logged in as: {user}")
        typer.echo("Try 'resoursphere auth whoami' for more details.")
    else:
        typer.echo(f"ResourSphere CLI v{VERSION}")
        typer.echo("Not logged in. Run 'resoursphere auth login' to log in.")

if __name__ == "__main__":
    app()
