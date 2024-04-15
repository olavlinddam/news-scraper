import json
import logging
import uuid

from fastapi import APIRouter, status, Response

from app.features.news.club_url_resolver import club_url_resolver
from app.features.subscription.subscription_request import subscription_request
from app.features.subscription.subscription_service import subscription_service

logger = logging.getLogger(__name__)
subscription_router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


        
@subscription_router.post("/subscribe")
async def subscribe(subscriber: subscription_request):
    try:
        database_name = "subscription"
        collection_name = "subscriptions"

        club = club_url_resolver().check_club_match(club=subscriber.club)
        if club == "Club not found":
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Club not found")

        service = subscription_service(database_name, collection_name)
        await service.process_subscription(subscriber)        
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        error_response = {
            "type": "https://example.com/probs/internal-error",
            "title": "Internal Server Error",
            "detail": "An unexpected error occurred." + str(e),
            "instance": str(uuid.uuid4()),
        }
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=json.dumps(error_response), # Convert the dictionary to a JSON string
        )
