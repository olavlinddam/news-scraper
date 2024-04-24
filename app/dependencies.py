from typing import Annotated
from bson import UuidRepresentation
from fastapi import Header, HTTPException
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "test":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


async def get_db_collection(database_name, collection_name):
    """
    Asynchronous function to get a database connection.

    Args:
        database_name: str - The name of the database.
        collection_name: str - The name of the collection within the database.

    Returns:
        MotorCollection - The specified collection within the specified database.
    """
    client = AsyncIOMotorClient("172.18.0.2", 27017, username='user', password='pass')  # Connect asynchronously
    client.uuid_representation = UuidRepresentation.STANDARD
    
    db = client[database_name]
    collection = db[collection_name]
    return collection
