from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ...authentication import get_username_from_token
from ... import pulumi
from ... import users

router = APIRouter()


class EC2CreateRequest(BaseModel):
    name: str
    instance_type: str
    ami: str


class EC2CreateResponse(BaseModel):
    instance_id: str
    instance_public_ip: str
    message: str


@router.post("/ec2/create", response_model=EC2CreateResponse)
def ec2_create_endpoint(request: EC2CreateRequest,
                        username: str = Depends(get_username_from_token)):
    #Verify the requested instance type and AMI are allowed
    permissions = users.get_user_permissions(username)
    if request.instance_type not in permissions.ec2_instance_types:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Instance type permission denied."
        )
    elif request.ami not in permissions.ami_choice:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="AMI choice permission denied."
        )

    #Verify the user doesn't exceed the maximum running instances allowed
    elif pulumi.get_running_ec2_instances(username) >= permissions.ec2_max_running:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Too many running instances for the user."
        )

    else:
    #launch the instance
        pulumi_response = pulumi.launch_ec2_instance(name=request.name,
                                          instance_type=request.instance_type,
                                          ami=request.ami, user=username)
        instance_id = pulumi_response["instance_id"]
        public_ip = pulumi_response["public_ip"]
        return {"instance_id": instance_id, "instance_public_ip": public_ip,
                "message": "message"}
