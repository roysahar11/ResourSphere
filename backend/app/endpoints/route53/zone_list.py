from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app.cloud_api import get_dns_zones_list
from typing import List, Dict, Any
from pydantic import BaseModel

class ZoneListResponse(BaseModel):
    zones: List[Dict[str, Any]]


router = APIRouter()

@router.get(
    "/route53/zones",
    tags=["route53"],
    summary="List DNS zones",
    description="Returns a list of DNS zones owned by the authenticated user",
    response_model=ZoneListResponse
)
async def list_dns_zones(username: str = Depends(get_username_from_token)) -> Dict[str, List[Dict[str, Any]]]:
    """
    List all DNS zones owned by the authenticated user.
    
    Returns:
        Dict containing a list of DNS zones with their details
    """
    try:
        zones = get_dns_zones_list(username)
        return {"zones": zones}
    except Exception as e:
        if not isinstance(e, HTTPException):
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve DNS zones: {str(e)}"
            )
        else:
            raise e
