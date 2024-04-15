from pydantic import BaseModel


class subscription_request(BaseModel):
    url: str
    club: str
