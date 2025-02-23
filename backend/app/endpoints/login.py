from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta
from ..authentication import verify_password, generate_access_token
from .. import users, config

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_permissions: list


@router.post("/auth/login", response_model=LoginResponse)
def login(login_req: LoginRequest):
    username = login_req.username
    user = users.users_db.get(username)

    if user and verify_password(login_req.password, user["password_hash"]):
        return {"token": generate_access_token(username),
        "token_type": "bearer",
        "user_permissions": users.get_user_permissions(username)}

    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
        )
