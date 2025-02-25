from app.api_requests import (
    send_s3_create_request, send_s3_list_request, send_s3_delete_request
)
from app.authentication import generate_authentication_header
import typer
from typing import Optional


s3_cmd = typer.Typer()


@s3_cmd.command("create")
def s3_create_cmd(
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="Name of the bucket"
    ),
    public: Optional[bool] = typer.Option(
        False, "--public", help="Make the bucket publicly accessible"
    )
):
    authentication_header = generate_authentication_header()
    if not name:
        name = typer.prompt("Enter a name for the bucket")
    if not public:
        public = typer.confirm("Make the bucket publicly accessible?")
    if public:
        public = typer.confirm(
            "Are you sure you want to make the bucket publicly accessible?"
        )
    typer.echo(f"Requesting creation of bucket '{name}'...")
    response = send_s3_create_request(authentication_header, name, public)
    typer.echo(f"Bucket {response.get('bucket_name')} created successfully.")
    typer.echo(f"Bucket's URL: {response.get('url')}")

@s3_cmd.command("list")
def s3_list_cmd():
    authentication_header = generate_authentication_header()
    typer.echo("Requesting S3 buckets list...")
    response = send_s3_list_request(authentication_header)
    buckets = response.get('buckets', [])
    
    if not buckets:
        typer.echo(
            "No S3 buckets found (Note: you can only see buckets "
            "that are owned by you and managed by ResourSphere)."
        ) 
        return
    
    typer.echo("\nYour S3 buckets:")
    typer.echo("-" * 40)
    for bucket in buckets:
        typer.echo(f"{bucket['name']}")


@s3_cmd.command("delete")
def s3_delete_cmd(
    bucket_name: str = typer.Argument(..., help="Name of the bucket to delete")
):
    authentication_header = generate_authentication_header()
    typer.echo(f"Requesting deletion of bucket '{bucket_name}'...")
    response = send_s3_delete_request(authentication_header, bucket_name)
    typer.echo(f"Bucket '{response.get('bucket_name')}' deleted successfully.")