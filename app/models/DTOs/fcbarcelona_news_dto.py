from pydantic import BaseModel
from typing import List


class FCBarcelonaNewsDTO(BaseModel):
    title: str
    url: str
    # Add more fields as needed


class FCBarcelonaNewsResponse(BaseModel):
    news: List[FCBarcelonaNewsDTO]
