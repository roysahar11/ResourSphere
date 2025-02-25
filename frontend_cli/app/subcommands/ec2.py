from app.authentication import (
    generate_authentication_header,
    get_current_user_permissions,
    get_logged_in_user
)
import typer
from typing import Optional
import os
import getpass
from app.api_requests import (
    send_ec2_create_request,
    send_ec2_list_request,
    send_ec2_delete_request,
    send_ec2_start_request,
    send_ec2_stop_request
)

ec2_cmd = typer.Typer()


@ec2_cmd.command("create")
def ec2_createt_cmd(
    ami: Optional[str] = typer.Option(None, "--ami", help="AMI ID or name"),
    instance_type: Optional[str] = typer.Option(None, "--type", "-t", help="EC2 instance type"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Name for the EC2 instance")
):
    authentication_header = generate_authentication_header()

    permissions = get_current_user_permissions()
    ami_choice = permissions.ami_choice
    instance_types = permissions.ec2_instance_types

    if instance_type is None:
        typer.echo("Please choose an instance type.")
        typer.echo("Available instance types:")
        for type in instance_types:
            typer.echo(f"{type}")
        instance_type = typer.prompt("Enter the instance type")
    
    if ami is None:
        typer.echo("Please choose an AMI.")
        typer.echo("Available AMIs:")
        for key, value in ami_choice.items():
            typer.echo(f"{key}: {value}")
        ami = typer.prompt("AMI ID or name")
        if ami not in ami_choice.keys() and ami not in ami_choice.values():
            typer.echo("Invalid AMI ID or name (You don't have access to this AMI)")
            raise typer.Exit()
    
    if name is None:
        name = typer.prompt("Enter a name for the EC2 instance")
    
    typer.echo("Launching EC2 instance...")
    response = send_ec2_create_request(
        authentication_header, ami, instance_type, name
    )

    typer.echo(f"EC2 instance {response.get('instance_id')} created successfully.")
    typer.echo(f"Public IP: {response.get('instance_public_ip')}")

@ec2_cmd.command("list")
def ec2_list_cmd():
    authentication_header = generate_authentication_header()
    typer.echo(f"Requesting EC2 instances list...")
    response = send_ec2_list_request(authentication_header)
    typer.echo(f"EC2 instances for user {get_logged_in_user()}:")
    table_data = [
        ["Name", "Instance ID", "Public IP Address", "State"]
    ]
    for instance in response:
        table_data.append([
            instance.get('name'),
            instance.get('instance_id'),
            instance.get('public_ip'),
            instance.get('state')
        ])
    
    column_widths = [
        max(len(str(item)) for item in column) for column in zip(*table_data)
    ]
    table = ""
    for row in table_data:
        table += " | ".join(f"{item:<{width}}" for item, width in zip(row, column_widths)) + "\n"
        if row == table_data[0]:
            table += "-+-".join("-" * width for width in column_widths) + "\n"
    
    typer.echo(table)

@ec2_cmd.command("delete")
def ec2_delete_cmd(
    instance: str = typer.Argument(..., help="Name or ID of the instance to delete")
):
    authentication_header = generate_authentication_header()
    typer.echo(f"Requesting deletion of EC2 instance {instance}...")
    response = send_ec2_delete_request(authentication_header, instance)
    typer.echo(response)

@ec2_cmd.command("start")
def ec2_start_cmd(
    instance: str = typer.Argument(..., help="Name or ID of the instance to start")
):
    authentication_header = generate_authentication_header()
    typer.echo(f"Requesting to start EC2 instance {instance}...")
    response = send_ec2_start_request(authentication_header, instance)
    typer.echo(response)

@ec2_cmd.command("stop")
def ec2_stop_cmd(
    instance: str = typer.Argument(..., help="Name or ID of the instance to stop")
):
    authentication_header = generate_authentication_header()
    typer.echo(f"Requesting to stop EC2 instance {instance}...")
    response = send_ec2_stop_request(authentication_header, instance)
    typer.echo(response)