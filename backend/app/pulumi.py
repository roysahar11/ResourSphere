def launch_ec2_instance(name: str, instance_type: str, ami: str, user: str):
    #[Pulumi code]
    #dummy response:
    return {"instance_id": "i-1234567890abcdef0",
            "public_ip": "36.145.32.3"}

def delete_ec2_instance(instance_id, user):
    #[Pulumi Code]
    #dummy response:
    return "Success"

def get_ec2_instances(user):
    #[Pulumi Code]
    #dummy response:
    return [{"name": "instance1", "instance_id": "i-1234567890abcdef0", "state": "running"},
            {"name": "instance2", "instance_id": "i-1234567890abcdef3", "state": "stopped"}]

def get_running_ec2_instances(user):
    #pulumi code
    #dummy response:
    return 1