from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app.cloud_api import create_dns_zone
from pydantic import BaseModel
# import uuid

router = APIRouter()


class ZoneCreateRequest(BaseModel):
    zone_name: str

class ZoneCreateResponse(BaseModel):
    zone_id: str
    name: str
    status: str


@router.post("/route53/zone/create", tags=["route53"])
async def dns_zone_create_endpoint(
    request: ZoneCreateRequest,
    user: dict = Depends(get_username_from_token)
):
    """
    Create a new DNS zone in Route53
    """
    try:
        result = create_dns_zone(request.zone_name, user)
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Error creating DNS zone: {str(e)}"
        )
