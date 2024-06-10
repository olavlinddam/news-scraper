import json
import logging
import uuid

from fastapi import APIRouter, status, Response

from app.features.news.club_url_resolver import ClubUrlResolver
from app.features.subscription.subscription_request import SubscriptionRequest
from app.features.subscription.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)
subscription_router = APIRouter(
    prefix="/subscription",
    tags=["subscription"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@subscription_router.post("/subscribe")
async def subscribe(subscriber: SubscriptionRequest):
    try:
        non_matching_clubs = ClubUrlResolver().check_club_collection_match(clubs=subscriber.club)
        if non_matching_clubs:
            message = f"Some clubs were not found: {', '.join(non_matching_clubs)}"
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=message)

        service = SubscriptionService("subscribers")
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
            content=json.dumps(error_response),  # Convert the dictionary to a JSON string
        )
