import requests
import typer
from app import config
# from app.authentication import get_logged_in_user
base_url = config.BACKEND_URL

def send_login_request(username: str, password: str) -> dict:
    """Send a login request to the backend."""
    url = f"{base_url}/auth/login"
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
    url = f"{base_url}/ec2/create"
    try:
        response = requests.post(url, headers=authentication_header, json={
            "ami": ami,
            "instance_type": instance_type,
            "name": name
        })
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 401:
            typer.echo(f"Permission denied: {response.json().get('detail')}")
            raise typer.Exit()
        else:
            typer.echo(f"Error requesting EC2 creation: {response.text}")
            typer.echo(f"HTTP Status code: {response.status_code}")
            raise typer.Exit()

    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error requesting EC2 creation (client side): {e}")
            raise typer.Exit()
        else:
            raise e

def send_ec2_list_request(authentication_header: dict) -> dict:
    url = f"{base_url}/ec2/list"
    try:
        response = requests.get(url, headers=authentication_header)
        if response.status_code == 200:
            data = response.json()
            return data.get("instances", [])
        else:
            typer.echo(f"Error requesting EC2 list: {response.text}")
            typer.echo(f"HTTP Status code: {response.status_code}")
            raise typer.Exit()
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error requesting EC2 list: {e}")
            raise typer.Exit()
        else:
            raise e

def send_ec2_delete_request(authentication_header: dict, instance: str) -> dict:
    url = f"{base_url}/ec2/delete"
    try:
        response = requests.delete(url, headers=authentication_header, json={
            "instance": instance
        })
        if response.status_code == 200:
            data = response.json()
            return f"Instance {data.get('instance_id')} terminated successfully."
        elif (
            response.status_code == 404
            and response.text == "Instance not found"
        ):
            return (
                f"Instance {instance} not found or does not belong to "
                f"your user. Note: You can only delete instances "
                "created using ResourceSphere."
            )
        else:
            typer.echo(f"Error requesting EC2 deletion: {response.text}")
            typer.echo(f"HTTP Status code: {response.status_code}")
            raise typer.Exit()
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error requesting EC2 deletion (client side): {e}")
            raise typer.Exit()
        else:
            raise e
def send_ec2_start_request(authentication_header: dict, instance_id: str) -> dict:
    url = f"{base_url}/ec2/start"
    try:
        response = requests.post(url, headers=authentication_header, json={
            "instance": instance_id
        })
        response_data = response.json()
        if response.status_code == 200:
            return f"Instance {response_data.get('instance_id')} started successfully."
        else:
            typer.echo(
                f"Error requesting EC2 start: {response_data.get('detail')}"
            )
            # typer.echo(f"HTTP Status code: {response.status_code}")
            raise typer.Exit()
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error requesting EC2 start (client side): {e}")
            raise typer.Exit()
        else:
            raise e

def send_ec2_stop_request(authentication_header: dict, instance_id: str) -> dict:
    url = f"{base_url}/ec2/stop"
    try:
        response = requests.post(url, headers=authentication_header, json={
            "instance": instance_id
        })
        response_data = response.json()
        if response.status_code == 200:
            return f"Instance {response_data.get('instance_id')} stopped successfully."
        else:
            typer.echo(
                f"Error requesting EC2 stop: {response_data.get('detail')}"
            )
            raise typer.Exit()
        
    except Exception as e:
        if not isinstance(e, typer.Exit):
            typer.echo(f"Error requesting EC2 stop (client side): {e}")
            raise typer.Exit()
        else:
            raise e
