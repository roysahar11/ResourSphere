from app.authentication import (
    generate_authentication_header
)
import typer
from typing import Optional
import os
import getpass
from app.api_requests import (
    send_dns_zone_create_request,
    send_dns_zone_delete_request,
    send_dns_zone_list_request
)

dns_zone_cmd = typer.Typer()


@dns_zone_cmd.command("create")
def zone_create_cmd(
    name: str = typer.Argument(..., help="Name of the DNS zone to create")
):
    authentication_header = generate_authentication_header()
    try:
        result = send_dns_zone_create_request(
            authentication_header, name
        )
        typer.echo(f"DNS zone '{result.get('zone_id')}' created successfully")
        return result
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error creating DNS zone (client side): {e}")
            raise typer.Exit()
        else:
            raise e


@dns_zone_cmd.command("delete")
def zone_delete_cmd(
    zone: str = typer.Argument(
        ..., help="Name or Zone ID of the DNS zone to delete"
    )
):
    authentication_header = generate_authentication_header()
    result = send_dns_zone_delete_request(
        authentication_header, zone
    )
    typer.echo(f"DNS zone '{result.get('zone_id')}' deleted successfully.")


@dns_zone_cmd.command("list")
def zone_list_cmd():
    authentication_header = generate_authentication_header()
    result = send_dns_zone_list_request(
        authentication_header
    )
    zones = result.get('zones', [])
    
    if not zones:
        typer.echo("No DNS zones found.")
        return
    
    # Calculate max widths based on content and headers
    zone_id_width = max(
        max(len(str(zone.get('zone_id', 'N/A'))) for zone in zones),
        len('Zone ID')
    )
    zone_name_width = max(
        max(len(str(zone.get('zone_name', 'N/A'))) for zone in zones),
        len('Zone Name') 
    )
    records_width = max(
        max(len(str(zone.get('record_count', 0))) for zone in zones),
        len('Records')
    )

    # Calculate total width for separator line
    total_width = zone_id_width + zone_name_width + records_width + 4  # 4 for spacing

    typer.echo("\nYour DNS zones:")
    typer.echo("-" * total_width)
    typer.echo(
        f"{'Zone ID':<{zone_id_width}} "
        f"{'Zone Name':<{zone_name_width}} "
        f"{'Records':<{records_width}}"
    )
    typer.echo("-" * total_width)
    for zone in zones:
        typer.echo(
            f"{zone.get('zone_id', 'N/A'):<{zone_id_width}} "
            f"{zone.get('name', 'N/A'):<{zone_name_width}} "
            f"{zone.get('record_count', 0):<{records_width}}"
        )
