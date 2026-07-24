from fastapi import APIRouter

router = APIRouter(tags=["auth"])


@router.post("/logout")
def logout():
    """
    Sessions are stateless bearer tokens with no server-side or cookie state,
    so logging out is the client discarding its tokens. This endpoint exists so
    the frontend has a single call to make (and a place to hang token
    revocation later, if it's ever added).
    """
    return {"message": "Logged out successfully"}
