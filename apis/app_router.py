from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    """
    Handle GET requests to the home page.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "You have hit home page"}


@router.get("/about")
async def about():
    """
    Handle GET requests to the about page.

    Returns:
        dict: A dictionary containing information about the about page.
    """
    return {"message": "You have hit about page"}
