from fastapi import APIRouter

router = APIRouter()


@router.post("/login", tags=["Auth"])
def login():
    return {"message": ""}


@router.post("/token", tags=["Auth"])
def get_token():
    return {"message": ""}


@router.post("/token/refresh", tags=["Auth"])
def refresh_token():
    return {"message": ""}


