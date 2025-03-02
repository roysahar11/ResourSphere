from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.authentication import get_username_from_token
from app import users
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserPermissionsResponse(BaseModel):
    username: str
    permissions: dict

@router.get("/auth/me", response_model=UserPermissionsResponse)
async def get_current_user(username: str = Depends(get_username_from_token)):
    """
    Get the current user's information and permissions based on their JWT token.
    This endpoint is used to verify that a token is valid and to retrieve the user's permissions.
    """
    try:
        user_permissions = users.get_user_permissions(username)
        if not user_permissions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User permissions not found"
            )
        
        return {
            "username": username,
            "permissions": user_permissions.model_dump()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
