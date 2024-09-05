from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    return {"message": "You have hit home page"}


@router.get("/about")
async def about():
    return {"message": "You have hit about page"}
