from typing import List

from pydantic import BaseModel

from .club import Club


class League(BaseModel):
    name: str
    clubs: List[Club]

    def add_club(self, club: Club):
        self.clubs.append(club)

    def to_dict(self):
        return {
            "name": self.name,
            "clubs": [club.to_dict() for club in self.clubs]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'League':
        clubs = [Club(**club) for club in data.get('clubs', [])]
        return cls(
            id=str(data.get('_id')),
            name=data.get('name', ''),
            clubs=clubs
        )
