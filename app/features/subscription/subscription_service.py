import logging

from app.features.subscription.subscriber import subscriber
from app.features.subscription.subscription_request import subscription_request
from app.data.repository import repository


class subscription_service:
    def __init__(self, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        self.logger = logging.getLogger(__name__)
        self.repository = repository(self.database_name, self.collection_name)

    async def process_subscription(self, request: subscription_request):
        try:
            repo = repository(self.database_name, self.collection_name)
            existing_subscriber_document = await repo.get_subscriber(request.url)

            if existing_subscriber_document is None:
                new_subscriber = subscriber(url=request.url, subscribed_to=[request.club])
                await self.repository.save_documents([new_subscriber.to_dict()])

            else:
                existing_subscriber = subscriber(existing_subscriber_document["url"],
                                                 existing_subscriber_document["subscribed_to"],
                                                 existing_subscriber_document["_id"])

                if request.club not in existing_subscriber.subscribed_to:
                    existing_subscriber.subscribed_to.append(request.club)
                     # Update the document in the database
                    update = {"$set": {"subscribed_to": existing_subscriber.subscribed_to}}
                    await self.repository.update_document(existing_subscriber._id, update)
                    

        except Exception as e:
            self.logger.exception("Error processing subscription:", e)
            raise Exception("Could not process subscription: " + str(e))
