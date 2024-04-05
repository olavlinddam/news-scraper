import json
from app.dependencies import get_db_collection
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
import logging


class document_dao:
    def __init__(self, database_name, collection_name):
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    async def get_db_collection(self):
        """
        Asynchronous function to get a database connection.

        Returns:
            MotorCollection - The specified collection within the specified database.
        """
        try:
            logging.info("Connecting to the database to fetch the " + self.collection_name + "collection.")
            self.client = AsyncIOMotorClient("172.18.0.2", 27017, username='user',
                                             password='pass')  # Connect asynchronously
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            return self.collection
        except ServerSelectionTimeoutError as e:
            logging.exception("Error connecting to the database:", e)
            return None

    async def save_documents(self, documents):
        """
        Saves multiple documents to the MongoDB collection.
        Raises an exception if the operation fails.
        """
        if self.collection is None:
            await self.get_db_collection()
        try:
            logging.info("Connecting to the database to save documents to the " + self.collection_name + "collection.")
            await self.collection.insert_many(documents, ordered=True)
            # If insert_many completes without raising an exception, the operation was successful.
            logging.info("Documents saved successfully.")
        except Exception as e:
            # Raising a new exception with a custom message
            logging.exception("Error saving documents:", e)
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
            logging.info("Connecting to the database to fetch documents from the " + self.collection_name + "collection.")
            news_cursor = self.collection.find({}).limit(limit)
            db_news = [news for news in await news_cursor.to_list(length=100)]
            return db_news
        except Exception as e:
            logging.exception("Error retrieving documents:", e)
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
            logging.info("Connecting to the database to fetch the latest news from the " + self.collection_name + " collection.")
            # Sort by 'created_at' in descending order to get the latest news first
            news_cursor = self.collection.find({}).sort("created_at", -1).limit(limit)
            latest_news = [news for news in await news_cursor.to_list(length=limit)]
            return latest_news
        except Exception as e:
            logging.exception("Error retrieving the latest news:", e)
            raise Exception("Could not retrieve the latest news: " + str(e))