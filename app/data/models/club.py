from pydantic import BaseModel


class Club(BaseModel):
    name: str
    url: str

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url
        }
