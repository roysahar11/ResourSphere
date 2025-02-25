from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.authentication import get_username_from_token
from app import cloud_api
from app import users

router = APIRouter()


class EC2CreateRequest(BaseModel):
    name: str
    instance_type: str
    ami: str


class EC2CreateResponse(BaseModel):
    instance_id: str
    instance_public_ip: str
    message: str

def get_running_instances_amount(user: str) -> int:
    instances = cloud_api.get_ec2_instances_by_user(user, state="running")
    return len(instances)

@router.post("/ec2/create", response_model=EC2CreateResponse)
async def ec2_create_endpoint(request: EC2CreateRequest,
                        username: str = Depends(get_username_from_token)):
    #Verify the requested instance type and AMI are allowed
    try:
        permissions = users.get_user_permissions(username)
        if request.instance_type not in permissions.ec2_instance_types:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Instance type permission denied."
            )
        if (request.ami not in permissions.ami_choice.keys()
            and request.ami not in permissions.ami_choice.values()
        ):
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="AMI choice permission denied."
            )

        # Verify the user doesn't exceed the maximum running instances allowed
        print(get_running_instances_amount(username))
        print(permissions.ec2_max_running)
        if (
            get_running_instances_amount(username)
            >= permissions.ec2_max_running
        ):
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Your request exceeds the maximum number"
                     " of running instances allowed for the user."
            )

        # Launch the instance
        if request.ami in permissions.ami_choice.keys():
            ami = permissions.ami_choice[request.ami]
        else:
            ami = request.ami
        cloud_api_response = cloud_api.launch_ec2_instance(name=request.name,
                                            instance_type=request.instance_type,
                                            ami=ami, user=username)
        instance_id = cloud_api_response["instance_id"]
        public_ip = cloud_api_response["public_ip"]
        return {"instance_id": instance_id, "instance_public_ip": public_ip,
                "message": "message"}

    except Exception as e:
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=str(e))
        else:
            raise e
