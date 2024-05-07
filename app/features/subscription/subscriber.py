from typing import List
from bson import ObjectId

class Subscriber:
    def __init__(self, url: str, subscribed_to: List[str], _id=None):
        if _id is None:
            self._id = ObjectId()
        else:
            self._id = ObjectId(_id)
        self.url = url
        self.subscribed_to = subscribed_to

    def to_dict(self):
        subscriber_dict = {
            "_id": self._id,
            "url": self.url,
            "subscribed_to": self.subscribed_to
        }
        return subscriber_dict

