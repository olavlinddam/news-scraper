from typing import Annotated
from fastapi import Header, HTTPException
from pymongo import MongoClient



async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")



## TODO Replace with a more generic approach, and split this responsibility into other classes
def get_db_connection():
    client = MongoClient("mongo:27017")  # Use hostname and default port
    database_name = "news_scraper"
    collection_name = "articles"
    db = client[database_name]
    articles_collection = db[collection_name]
    return articles_collection  # Return the collection object directly


