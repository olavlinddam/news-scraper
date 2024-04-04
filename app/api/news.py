import json
import uuid

import uvicorn
from fastapi import APIRouter, Depends, status, Response

from app.services.fcbarcelona_service import import_fcb_news
from app.services.fcbarcelona_service import get_existing_fcb_news

router = APIRouter(
    prefix="/news",
    tags=["news"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# region endpoints
@router.get("/scrape")
async def scrape():
    try:
        await import_fcb_news()
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "https://example.com/probs/internal-error",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred." + str(e),
                "instance": str(uuid.uuid4()),
            },
        )


@router.get("/fcbarcelona")
async def get_fcb_news():
    """
    Retrieve articles related to FC Barcelona.

    Returns:
        dict: A dictionary containing the retrieved articles.
    """
    try:
        existing_news = await get_existing_fcb_news()
        return existing_news
    except Exception as e:
        print(e)
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "https://example.com/probs/internal-error",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred." + str(e),
                "instance": str(uuid.uuid4()),
            },
        )


# endregion


if __name__ == "__main__":
    uvicorn.run("app.api.news:router", host="0.0.0.0", port=8000)
