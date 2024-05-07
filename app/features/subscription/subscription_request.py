from pydantic import BaseModel


class SubscriptionRequest(BaseModel):
    url: str
    club: str
