import logging
import uuid
from typing import List

import uvicorn
from fastapi import APIRouter, Depends, status, Response
from starlette.responses import JSONResponse

from app.data.models.league import League
from app.dependencies import get_token_header
from app.features.admin.admin_service import AdminService
from app.features.news.news_service import NewsService
from app.features.notification.notification_service import NotificationService
from app.features.subscription.subscription_service import SubscriptionService
from app.features.news.club_url_resolver import ClubUrlResolver

logger = logging.getLogger(__name__)
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@admin_router.post("/league")
async def insert_leagues(leagues: List[League]):
    try:
        service = AdminService("admin", "leagues")
        await service.add_leagues(leagues)
        return JSONResponse(content={"message": "Leagues added successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": "Could not add leagues.", "detail": str(e)}, status_code=500)
