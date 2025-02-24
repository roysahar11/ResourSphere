import os
import json
from datetime import datetime
from pydantic import BaseModel, Field


CLI_VERSION = "0.0.1"
BACKEND_URL = "http://localhost:8000"
TOKEN_ENV_VAR = "RESOURSPHERE_TOKEN"
USER_ENV_VAR = "RESOURSPHERE_USER"
LOCAL_CONFIG_DIR = os.path.expanduser("~/resoursphere")
# PASSWORD_ENV_VAR = "RESOURSPHERE_PASSWORD"
def get_local_config_dir():
    os.makedirs(LOCAL_CONFIG_DIR, exist_ok=True)
    return LOCAL_CONFIG_DIR

def get_local_temp_dir():
    TEMP_DIR = os.path.join(get_local_config_dir(), ".tmp")
    os.makedirs(TEMP_DIR, exist_ok=True)
    return TEMP_DIR

LOCAL_USER_FILE = os.path.join(get_local_config_dir(), ".user")
LOCAL_TOKEN_FILE = os.path.join(get_local_temp_dir(), ".token")
LOCAL_USER_PERMISSIONS_FILE = os.path.join(
    get_local_config_dir(), ".permissions"
    )
LOCAL_TOKEN_EXPIRATION_FILE = os.path.join(
    get_local_config_dir(), ".token_expires_at"
)

class Permissions(BaseModel):
    ec2_max_running: int = 0
    ec2_instance_types: list[str] = Field(default_factory=list)
    ami_choice: dict[str, str] = Field(default_factory=dict)


def save_login_token(token: str):
    with open(LOCAL_TOKEN_FILE, "w") as token_file:
        token_file.write(token)

def read_login_token() -> str:
    if os.path.exists(LOCAL_TOKEN_FILE):
        with open(LOCAL_TOKEN_FILE, "r") as token_file:
            return token_file.read().strip()
    return ""

def save_username(user: str):
    with open(LOCAL_USER_FILE, "w") as user_file:
        user_file.write(user)

def read_username() -> str:
    if os.path.exists(LOCAL_USER_FILE):
        with open(LOCAL_USER_FILE, "r") as user_file:
            return user_file.read().strip()
    return ""

def save_user_permissions(permissions: dict):
    with open(LOCAL_USER_PERMISSIONS_FILE, "w") as user_permissions_file:
        user_permissions_file.write(json.dumps(permissions))

def read_user_permissions() -> Permissions:
    if os.path.exists(LOCAL_USER_PERMISSIONS_FILE):
        with open(LOCAL_USER_PERMISSIONS_FILE, "r") as user_permissions_file:
            return Permissions(**json.loads(user_permissions_file.read()))
    return Permissions()

def save_token_expiration(expiration: datetime):
    with open(LOCAL_TOKEN_EXPIRATION_FILE, "w") as token_expiration_file:
        token_expiration_file.write(expiration)

def read_token_expiration() -> datetime:
    if os.path.exists(LOCAL_TOKEN_EXPIRATION_FILE):
        with open(LOCAL_TOKEN_EXPIRATION_FILE, "r") as token_expiration_file:
            return datetime.fromisoformat(token_expiration_file.read().strip())