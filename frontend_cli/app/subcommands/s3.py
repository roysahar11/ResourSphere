from app.api_requests import send_s3_create_request
from app.authentication import generate_authentication_header
import typer
from typing import Optional

s3_cmd = typer.Typer()


@s3_cmd.command("create")
def s3_create_cmd(
    name: Optional[str] = typer.Argument(None, help="Name of the bucket"),
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
