import logging
from typing import List

from app.features.subscription.subscriber import Subscriber
from app.features.subscription.subscription_request import SubscriptionRequest
from app.data.repository import Repository


class SubscriptionService:
    def __init__(self, collection_name: str):
        self.database_name = "subscription"
        self.collection_name = collection_name
        self.logger = logging.getLogger(__name__)
        self.repository = Repository(self.database_name, self.collection_name)

    async def process_subscription(self, request: SubscriptionRequest):
        try:
            self.logger.info(f"Processing subscription request for subscriber with url {request.url}")
            existing_subscriber_document = await self.repository.get_subscriber(request.url)

            if existing_subscriber_document is None:
                await self.create_subscriber(request)
            else:
                await self.update_subscriber(request, existing_subscriber_document)
        except Exception as e:
            self.logger.exception("Error processing subscription:", e)
            raise Exception("Could not process subscription: " + str(e))

    async def get_subscribers(self, clubs: List[str]):
        if len(clubs) == 0:
            self.logger.info("Error fetching subscribers: 'Provided list of clubs is empty'")
            return

        subscribers = await self.repository.get_subscribers_by_clubs(clubs)
        return subscribers

    async def create_subscriber(self, request: SubscriptionRequest):
        self.logger.info(f"No subscriber found with url {request.url}, inserting a new subscriber into"
                         f"subscriber collection.")
        new_subscriber = Subscriber(url=request.url, subscribed_to=request.club)
        await self.repository.save_documents([new_subscriber.to_dict()])
        self.logger.info(f"Subscriber with url {request.url} inserted successfully.")

    async def update_subscriber(self, request: SubscriptionRequest, existing_subscriber_document):
        self.logger.info(f"Subscriber found with id: '{existing_subscriber_document['_id']}'. Updating club list.")

        existing_subscriber: Subscriber = Subscriber(existing_subscriber_document["url"],
                                                     existing_subscriber_document["subscribed_to"],
                                                     existing_subscriber_document["_id"])

        # Overwrite the clubs a subscriber is subscribed to with the new list received form the request.
        existing_subscriber.subscribed_to = request.club
        # Update the document in the database
        update = {"$set": {"subscribed_to": existing_subscriber.subscribed_to}}
        await self.repository.update_document(existing_subscriber._id, update)
