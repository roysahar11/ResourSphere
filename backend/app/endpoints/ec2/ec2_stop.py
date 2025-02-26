from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app import cloud_api
from pydantic import BaseModel
from app.endpoints.ec2.helper_functions import verify_instance_and_return_id

router = APIRouter()

class StopInstanceRequest(BaseModel):
    instance: str

@router.post("/ec2/stop", tags=["ec2"])
async def ec2_stop_endpoint(
    request: StopInstanceRequest,
    username: str = Depends(get_username_from_token)
):
    instance_id = verify_instance_and_return_id(
        user=username,
        instance=request.instance,
        state="running"
    )
    if not instance_id:
        raise HTTPException(
            status_code=404,
            detail="Instance not found, or is not in a running state "
            "(Note: you can only start and stop instances that you own "
            "and that are managed by ResourSphere)"
        )
    
    try:
        return cloud_api.stop_ec2_instance(instance_id)
    except Exception as e:
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=str(e))
        else:
            raise e
        
        
