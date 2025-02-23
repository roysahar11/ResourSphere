from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from app.authentication import verify_password, generate_access_token
from app import users, config

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_permissions: dict


@router.post("/auth/login", response_model=LoginResponse)
async def login(login_req: LoginRequest):
    try:
        username = login_req.username
        user = users.get_user(username)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username does not exist."
            )

        if not verify_password(login_req.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        return {
            "access_token": generate_access_token(username),
            "token_type": "bearer",
            "user_permissions": users.get_user_permissions(username).model_dump()
        }

    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        # Log the error here
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred. Error: {e}"
        )
