from typing import List
from pydantic import BaseModel


class SubscriptionRequest(BaseModel):
    url: str
    club: List[str]
