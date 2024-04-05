import json
import uuid

import uvicorn
from fastapi import APIRouter, Depends, status, Response

from app.services.fcbarcelona_service import fcbarcelona_service

router = APIRouter(
    prefix="/news",
    tags=["news"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def get_fcbarcelona_service():
    return fcbarcelona_service()


# region endpoints
@router.get("/scrape")
async def scrape(service: fcbarcelona_service = Depends(get_fcbarcelona_service)):
    try:
        await service.import_fcb_news()
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
async def get_fcb_news(service: fcbarcelona_service = Depends(get_fcbarcelona_service)):
    try:
        existing_news = await service.get_existing_fcb_news()
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
