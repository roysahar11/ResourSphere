from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app.cloud_api import delete_dns_zone
from app.endpoints.route53.helper_functions import (
    get_zone_id_if_owned_by_user
)
from pydantic import BaseModel
# import uuid

router = APIRouter()


@router.delete("/route53/zone/{zone}/delete", tags=["route53"])
async def dns_zone_delete_endpoint(
    zone: str,
    user: str = Depends(get_username_from_token)
):
    """
    Delete a DNS zone in Route53
    """
    zone_id = get_zone_id_if_owned_by_user(zone, user)
    if not zone_id:
        raise HTTPException(
            status_code=404,
            detail=f"Zone {zone} does not exist or is not owned by user {user}"
        )
    try:
        delete_dns_zone(zone_id)
        return {
            "zone_id": zone_id,
            "status": "deleted"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(status_code=500, detail=f"Error deleting zone: {e}")
