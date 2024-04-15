import logging
import uuid

import uvicorn
from fastapi import APIRouter, Depends, status, Response

from app.features.news.news_service import news_service
from app.features.news.club_url_resolver import club_url_resolver

logger = logging.getLogger(__name__)
news_router = APIRouter(
    prefix="/news",
    tags=["news"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def get_news_service(database_name: str, collection_name: str, url_to_scrape: str = None):
    return news_service(database_name, collection_name, url_to_scrape)


@news_router.get("/scrape/{club}")
async def scrape_news(club: str):
    try:
        url_to_scrape = club_url_resolver().resolve_url(club)
        if url_to_scrape == "URL not found":
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Club not found")

        database_name = "news"
        collection_name = f"{club.lower()}"

        service = get_news_service(database_name, collection_name, url_to_scrape)
        await service.import_news()
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "type": "https://example.com/probs/internal-error",
                "title": "Internal Server Error",
                "detail": "An unexpected error occurred." + str(e),
                "instance": str(uuid.uuid4()),
            },
        )


@news_router.get("/{club}")
async def get_news(club: str):
    try:
        database_name = "news"
        collection_name = f"{club.lower()}"
        service = get_news_service(database_name, collection_name, None)
        existing_news = await service.get_existing_news()
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
