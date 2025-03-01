from app.authentication import (
    generate_authentication_header
)
import typer
from typing import Optional
import os
import getpass

debug_cmd = typer.Typer()


@debug_cmd.command("gah")
def get_authentication_header_cmd():
    typer.echo(generate_authentication_header())