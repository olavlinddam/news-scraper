import json
from app.dependencies import get_db_collection
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError


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
            self.client = AsyncIOMotorClient("172.18.0.2", 27017, username='user',
                                             password='pass')  # Connect asynchronously
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            return self.collection
        except ServerSelectionTimeoutError as e:
            print("Error connecting to the database:", e)
            return None

    async def save_documents(self, documents):
        """
        Saves multiple documents to the MongoDB collection.
        Raises an exception if the operation fails.
        """
        if self.collection is None:
            await self.get_db_collection()
        try:
            print("Saving documents. . .")
            await self.collection.insert_many(documents, ordered=True)
            # If insert_many completes without raising an exception, the operation was successful.
            print("Documents saved successfully.")
        except Exception as e:
            # Raising a new exception with a custom message
            raise Exception("Could not save news: " + str(e)) from e

    async def get_documents(self, limit):
        if self.collection is None:
            await self.get_db_collection()

        try:
            print("Retrieving documents. . .")
            news_cursor =  self.collection.find({}).limit(limit)
            db_news = [news for news in await news_cursor.to_list(length=100)]
            return db_news
        except Exception as e:
            raise Exception("Could not retrieve news: " + str(e))
