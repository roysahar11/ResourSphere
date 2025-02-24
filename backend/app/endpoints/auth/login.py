from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta, datetime
from app.authentication import verify_password, generate_access_token
from app import users, config

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at_utc: datetime
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
        token = generate_access_token(username)
        return {
            "access_token": token.get("token"),
            "token_type": "bearer",
            "expires_at_utc": token.get("expires_at_utc"),
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
