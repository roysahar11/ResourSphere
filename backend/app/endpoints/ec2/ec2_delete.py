from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app import cloud_api
from pydantic import BaseModel
from app.endpoints.ec2.helper_functions import verify_instance_and_return_id


router = APIRouter()

class DeleteInstanceRequest(BaseModel):
    instance: str

class DeleteInstanceResponse(BaseModel):
    instance_id: str
    status: str

@router.delete("/ec2/delete", response_model=DeleteInstanceResponse)
async def ec2_delete_endpoint(
    request: DeleteInstanceRequest,
    username: str = Depends(get_username_from_token)
):
    instance_id = verify_instance_and_return_id(username, request.instance)
    if not instance_id:
        raise HTTPException(
            status_code=404,
            detail="Instance not found"
        )
    
    try:
        return cloud_api.terminate_ec2_instance(
                    instance_id=instance_id, user=username
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
