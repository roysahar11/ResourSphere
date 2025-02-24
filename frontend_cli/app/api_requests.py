import requests
import typer
from app import config

def send_login_request(username: str, password: str) -> dict:
    """Send a login request to the backend."""
    url = f"{config.BACKEND_URL}/auth/login"
    try:
        response = requests.post(url, json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            # typer.echo(response.status_code)
            typer.echo(f"Login failed: {response.text}")
            typer.echo(f"HTTP Status code: {response.status_code}")
            raise typer.Exit()
    except Exception as e:
        # typer.echo(response.status_code)
        typer.echo(f"Error during login: {e}")
        raise typer.Exit()
    
def send_ec2_create_request(
        authentication_header: dict,
        ami: str,
        instance_type: str,
        name: str) -> dict:
    """Send a create EC2 request to the backend."""
    url = f"{config.BACKEND_URL}/ec2/create"
    try:
        response = requests.post(url, headers=authentication_header, json={
            "ami_choice": ami_choice,
    