from fastapi import (
    APIRouter, Depends, HTTPException, File, UploadFile, FastAPI, Form
)
from app.authentication import get_username_from_token
from app.cloud_api import upload_file_to_s3_bucket, get_s3_buckets
from pydantic import BaseModel


# class UploadFileRequest(BaseModel):
#     bucket_name: str
#     file: UploadFile = File(...)

# class UploadFileResponse(BaseModel):
#     bucket_name: str
#     file_name: str
#     status: str

router = APIRouter()

@router.post("/s3/upload")
async def upload_file(
    bucket_name: str = Form(...),
    file: UploadFile = File(...),
    user: str = Depends(get_username_from_token)
):
    user_buckets = get_s3_buckets(user)
    if bucket_name not in [bucket['name'] for bucket in user_buckets]:
        raise HTTPException(
            status_code=404,
            detail=f"Bucket {bucket_name} does not exist, or is not "
            f"owned by user {user}."
        )
    return upload_file_to_s3_bucket(
        bucket_name=bucket_name, file=file
    )