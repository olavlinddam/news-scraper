import logging
import uuid

import uvicorn
from fastapi import APIRouter, Depends, status, Response

from app.features.news.news_service import NewsService
from app.features.notification.notification_service import NotificationService
from app.features.subscription.subscription_service import SubscriptionService
from app.features.news.club_url_resolver import ClubUrlResolver

logger = logging.getLogger(__name__)
news_router = APIRouter(
    prefix="/news",
    tags=["news"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@news_router.get("/scrape")
async def scrape_news():
    try:
        news_service = NewsService()
        imported_news = await news_service.import_news()

        # Extract the 'club' value from each article and add it to a set to remove duplicates
        clubs_with_new_articles = set()
        for article in imported_news:
            clubs_with_new_articles.add(article.club)

        if len(clubs_with_new_articles) == 0:
            return Response(status_code=status.HTTP_200_OK,
                            content="No new articles found",
                            media_type="a")

        subscription_service = SubscriptionService("subscribers")
        subscribers = await subscription_service.get_subscribers(list(clubs_with_new_articles))

        notification_service = NotificationService()
        notification_service.push(documents=imported_news, subscribers=subscribers)

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
        service = NewsService()
        existing_news = await service.get_existing_news(database_name, collection_name)
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

