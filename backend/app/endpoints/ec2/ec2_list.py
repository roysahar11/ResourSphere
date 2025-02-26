from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app import cloud_api
from pydantic import BaseModel


router = APIRouter()

@router.get("/ec2/list", tags=["ec2"])
async def ec2_list_endpoint(username: str = Depends(get_username_from_token)):
    try:
        instances = cloud_api.get_ec2_instances_by_user(username)
        return {"instances": instances}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
