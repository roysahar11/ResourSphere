from fastapi import APIRouter, Depends, HTTPException
from app.authentication import get_username_from_token
from app.cloud_api import create_s3_bucket, get_s3_buckets
from pydantic import BaseModel

router = APIRouter()

class S3CreateRequest(BaseModel):
    bucket_name: str
    public_access: bool = False

class S3CreateResponse(BaseModel):
    bucket_name: str
    status: str
    bucket_url: str

@router.post("/s3/create", response_model=S3CreateResponse)
async def create_bucket(
    request: S3CreateRequest, username: str = Depends(get_username_from_token)
):
    """
    Create a new S3 bucket
    """
    #check if the bucket already exists
    buckets = get_s3_buckets(username)
    if request.bucket_name in [bucket['name'] for bucket in buckets]:
        raise HTTPException(
            status_code=409,
            detail=f"Bucket {request.bucket_name} already exists"
        )
    result = create_s3_bucket(
        name=request.bucket_name,
        user=username,
        public=request.public_access
    )
    return result
