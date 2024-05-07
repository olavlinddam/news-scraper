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
        # url_to_scrape = ClubUrlResolver().resolve_url(club)
        # if url_to_scrape == "URL not found":
        #     return Response(status_code=status.HTTP_404_NOT_FOUND, content="Club not found")


        clubs_urls = ClubUrlResolver().clubs_urls
        news_service = NewsService()
        imported_news = await news_service.import_news(clubs_urls)
        
        # Extract the 'club' value from each article and add it to a set to remove duplicates
        clubs_with_new_articles = set()
        for article in imported_news:
            clubs_with_new_articles.add(article.club)
         
        # clubs_with_new_articles = list(set(article['club'] for article in imported_news))
                
        subscription_service = SubscriptionService("subscribers")
        subscribers = await subscription_service.get_subscribers(list(clubs_with_new_articles))
        
        # TODO: CREATE A DICT OF SUBSCRIBERS AND THEIR NEWS TO PASS TO THE NOTIFICATION SERVICE
        
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
        
# @news_router.get("/scrape")
# async def scrape_news():
#     try:
#         urls_to_scrape = ClubUrlResolver().clubs_urls.values()


#         news_service = NewsService("news")
#         new_news_documents = await news_service.import_news()
        
        
#         subscription_service = SubscriptionService("subscribers")
#         subscribers = subscription_service.get_subscribers()
        
#         notification_service = NotificationService()
#         notification_service.push()
        
        
#         return Response(status_code=status.HTTP_200_OK)
#     except Exception as e:
#         return Response(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={
#                 "type": "https://example.com/probs/internal-error",
#                 "title": "Internal Server Error",
#                 "detail": "An unexpected error occurred." + str(e),
#                 "instance": str(uuid.uuid4()),
#             },
#         )


@news_router.get("/{club}")
async def get_news(club: str):
    try:
        database_name = "news"
        collection_name = f"{club.lower()}"
        service = NewsService(database_name, collection_name, None)
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
