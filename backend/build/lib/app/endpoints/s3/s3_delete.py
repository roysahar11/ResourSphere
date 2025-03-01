from fastapi import APIRouter, HTTPException, Depends
from app.authentication import get_username_from_token
from app.cloud_api import delete_s3_bucket, get_s3_buckets
from pydantic import BaseModel


class DeleteBucketRequest(BaseModel):
    bucket_name: str

class DeleteBucketResponse(BaseModel):
    bucket_name: str
    status: str

router = APIRouter()

@router.delete("/s3/delete", response_model=DeleteBucketResponse, tags=["s3"])
async def s3_delete(
    request: DeleteBucketRequest,
    user: str = Depends(get_username_from_token)
):
    """
    Endpoint to delete an S3 bucket.
    """
    user_buckets = get_s3_buckets(user)
    if request.bucket_name not in [bucket['name'] for bucket in user_buckets]:
        raise HTTPException(
            status_code=404,
            detail=f"Bucket {request.bucket_name} not found, or is "
            f"not owned by user {user}."
        )
    try:
        result = delete_s3_bucket(request.bucket_name)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{e}"
        )


