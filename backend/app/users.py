import os
import yaml
from pydantic import BaseModel, Field

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(f"{CURRENT_DIR}/config/users.yml", "r") as users_config:
    users_db = yaml.safe_load(users_config)

with open(f"{CURRENT_DIR}/config/groups.yml", "r") as groups_config:
    groups = yaml.safe_load(groups_config)


# def load_users_db():
#     with open(f"{CURRENT_DIR}/config/users.yml", "r") as users:
#         return users_db

class Permissions(BaseModel):
    ec2_max_running: int = 0
    ec2_instance_types: list[str] = Field(default_factory=list)
    ami_choice: dict[str, str] = Field(default_factory=dict)


def get_user_permissions(username):
    user = users_db.get(username)
    permissions = {}
    if not user:
        return None
    else:
        user_group = user.get("group")
        if user_group:
            permissions.update(user_group.get("permissions", {}))
        permissions.update(user.get("permissions", {}))
    return Permissions(**permissions)
