# token refresh route — cookie-free.
#
# The client holds the refresh token and posts it in the request body; the API
# is stateless and sets no cookies (the frontend is on a different origin, so
# cookies here would be third-party and dropped by the browser).
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth.tokens import create_access_token
from app.core.config import settings
from jose import jwt, JWTError

router = APIRouter(tags=["auth"])


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(payload_in: RefreshRequest):
    try:
        payload = jwt.decode(
            payload_in.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=401, detail="Invalid token")

    return RefreshResponse(
        access_token=create_access_token(subject=subject),
        expires_in=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
