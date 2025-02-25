from fastapi import HTTPException
from app import cloud_api


def verify_instance_and_return_id(user: str, instance: str, state=None) -> str:
    user_instances = cloud_api.get_ec2_instances_by_user(user, state)
    instances = {
        instance["name"]: instance["instance_id"]
        for instance in user_instances
    }
    instance_id = (
        instances.get(instance)
        if instance in instances.keys()
        else instance if instance in instances.values()
        else ""
    )
    return instance_id