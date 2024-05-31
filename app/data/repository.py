import logging
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from app.features.subscription.subscriber import Subscriber


class Repository:
    def __init__(self, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.logger = logging.getLogger(__name__)

    async def get_db_collection(self):
        """
        Asynchronous function to get a database connection.

        Returns:
            MotorCollection - The specified collection within the specified database.
        """
        try:
            self.logger.info("Connecting to the database.")
            self.client = AsyncIOMotorClient("localhost", 27017, username='user', password='pass')  # Connect
            # asynchronously
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            return self.collection
        except ServerSelectionTimeoutError as e:
            self.logger.exception("Error connecting to the database:", e)
            return None

    async def save_documents(self, documents):
        """
        Saves multiple documents to the MongoDB collection.
        Raises an exception if the operation fails.
        """
        if self.collection is None:
            await self.get_db_collection()
        try:
            self.logger.info("Attempting to save documents to the " + self.collection_name + " collection.")
            await self.collection.insert_many(documents, ordered=True)
            # If insert_many completes without raising an exception, the operation was successful.
            self.logger.info("Documents saved successfully.")
        except Exception as e:
            # Raising a new exception with a custom message
            self.logger.exception("Error saving documents:", e)
            raise Exception("Could not save news: " + str(e)) from e

    async def get_documents(self, limit):
        """
        A function to retrieve documents from the collection up to a specified limit.

        :param limit: The maximum number of documents to retrieve.
        :return: A list of documents retrieved from the collection.
        """
        if self.collection is None:
            await self.get_db_collection()

        try:
            self.logger.info("Attempting to fetch documents from the " + self.collection_name + "collection.")
            cursor = self.collection.find({}).limit(limit)
            documents = [document for document in await cursor.to_list(length=100)]
            return documents
        except Exception as e:
            self.logger.exception("Error retrieving documents:", e)
            raise Exception("Could not retrieve news: " + str(e))

    async def get_latest_news(self, limit):
        """
        Retrieves the latest news documents from the collection up to a specified limit.

        :param limit: The maximum number of documents to retrieve.
        :return: A list of the latest news documents retrieved from the collection.
        """
        if self.collection is None:
            await self.get_db_collection()

        try:
            self.logger.info("Attempting to fetch the latest news from the " + self.collection_name + " collection.")
            # Sort by 'created_at' in descending order to get the latest news first
            news_cursor = self.collection.find({}).sort("created_at", -1).limit(limit)
            latest_news = [news for news in await news_cursor.to_list(length=limit)]
            return latest_news
        except Exception as e:
            self.logger.exception("Error retrieving the latest news:", e)
            raise Exception("Could not retrieve the latest news: " + str(e))

    async def get_subscriber(self, url):
        if self.collection is None:
            await self.get_db_collection()

        try:
            self.logger.info("Attempting to fetch the subscriber with the url: " + url)
            existing_subscriber = await self.collection.find_one({"url": url})

            #logging.info("Subscriber found: " + str(existing_subscriber["id"]))
            return existing_subscriber
        except Exception as e:
            self.logger.exception("Error retrieving the subscriber:", e)
            raise Exception("Could not retrieve the subscriber: " + str(e))

    async def update_document(self, id, update):
        """
        Updates a single document in the collection that matches the filter.

        :param filter: A dictionary specifying the criteria for the document to update.
        :param update: A dictionary specifying the update operations to perform.
        """
        if self.collection is None:
            await self.get_db_collection()

        try:
            # Ensure the _id is correctly formatted as an ObjectId
            # if id:
            #     filter = ObjectId(filter["_id"])

            self.logger.info(f"Attempting to update document with id {id} in the {self.collection_name} collection.")
            result = await self.collection.update_one({"_id": ObjectId(id)}, update)

            if result.modified_count > 0:
                self.logger.info("Document updated successfully.")
            else:
                message = "No documents matched the filter criteria."
                self.logger.info(message)
                raise DocumentNotFoundError(message)

        except DocumentNotFoundError as e:
            raise DocumentNotFoundError("No document matched the filter criteria.")
        except Exception as e:
            self.logger.exception("Error updating document:", e)
            raise Exception("Could not update document: " + str(e)) from e

    async def get_subscribers_by_clubs(self, clubs: List[str]):
        """
        Fetches all subscribers that are subscribed to any club in the provided list.

        :param clubs: A list of club names.
        :return: A list of subscriber documents.
        """
        if self.collection is None:
            await self.get_db_collection()

        self.logger.info(f"Fetching subscribers for clubs: {clubs}")
        # Construct the query to find subscribers who are subscribed to any of the clubs in the list
        query = {"subscribed_to": {"$in": clubs}}

        # Execute the query and fetch all matching documents
        subscribers = self.collection.find(query)

        # Convert the cursor to a list of dictionaries
        subscribers_list = await subscribers.to_list(length=None)

        return subscribers_list


#region Errors
class DocumentNotFoundError(Exception):
    "Raised when no document matched the filter"
    pass

#endregion
