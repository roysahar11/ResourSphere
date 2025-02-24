from app.authentication import (
    get_authentication_header,
    get_current_user_permissions
)
import typer
from typing import Optional
import os
import getpass

ec2_cmd = typer.Typer()


@ec2_cmd.command("create")
def ec2_createt_cmd():
    authentication_header = get_authentication_header()

    permissions = get_current_user_permissions()
    ami_choice = permissions.ami_choice
    instance_types = permissions.ec2_instance_types
    max_running = permissions.ec2_max_running
    
