from fastapi import APIRouter, Depends
from app.authentication import get_username_from_token
from app.cloud_api import get_s3_buckets
from pydantic import BaseModel
from typing import List

router = APIRouter()

class S3BucketResponse(BaseModel):
    name: str
    url: str

class S3ListResponse(BaseModel):
    buckets: List[S3BucketResponse]

@router.get("/s3/list", response_model=S3ListResponse)
async def list_buckets(username: str = Depends(get_username_from_token)):
    """
    List all S3 buckets owned by the authenticated user
    """
    buckets = get_s3_buckets(username)
    return {"buckets": buckets}
