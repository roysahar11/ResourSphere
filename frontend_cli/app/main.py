# resoursphere/main.py
import os
import typer
from app.subcommands.auth import auth_cmd
from app.subcommands.debug import debug_cmd
from app.subcommands.ec2 import ec2_cmd
from app.subcommands.s3 import s3_cmd
from app.subcommands.dns_zone import dns_zone_cmd
from app.authentication import get_saved_token, get_logged_in_user
from app import config

resoursphere_cmd = typer.Typer()

resoursphere_cmd.add_typer(auth_cmd, name="auth")
resoursphere_cmd.add_typer(debug_cmd, name="debug")
resoursphere_cmd.add_typer(ec2_cmd, name="ec2")
resoursphere_cmd.add_typer(s3_cmd, name="s3")
resoursphere_cmd.add_typer(dns_zone_cmd, name="dns-zone")

@resoursphere_cmd.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        user = get_logged_in_user()
        typer.echo(f"ResourSphere CLI v{config.CLI_VERSION}")
        typer.echo("by Roy Sahar")
        typer.echo(f"Configured to use Backend: {config.BACKEND_URL}")
        if user:
            typer.echo(f"Logged in as: {user}")
        else:
            typer.echo("Not logged in. Run 'resoursphere auth login' to log in.")

if __name__ == "__main__":
    resoursphere_cmd()
